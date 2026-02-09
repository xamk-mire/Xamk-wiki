# .NET-sovelluksen kontitus Dockerilla

Tämä materiaali käsittelee .NET-sovellusten (konsolisovellukset ja ASP.NET Core Web API) kontitusta Dockerilla. Opit käyttämään Microsoftin virallisia Docker-imageja, kirjoittamaan tehokkaita multi-stage Dockerfileja ja debuggaamaan sovelluksia Docker-konteissa.

> **Edellytykset:** Tutustu ensin [Docker-perusteisiin](https://github.com/xamk-mire/Xamk-wiki/blob/main/Development-guidelines/Docker/Docker-Perusteet.md) ja [Dockerfile-ohjeisiin](https://github.com/xamk-mire/Xamk-wiki/blob/main/Development-guidelines/Docker/Dockerfile.md).

---

## Microsoftin viralliset .NET Docker -imaget

Microsoft tarjoaa viralliset Docker-imaget .NET-sovelluksille. Imaget löytyvät [Microsoft Container Registrystä (MCR)](https://mcr.microsoft.com/) -- ei Docker Hubista.

### Tärkeimmät imaget ja milloin niitä käytetään

| Image | Sisältö | Milloin käytät? |
|---|---|---|
| `mcr.microsoft.com/dotnet/sdk` | .NET SDK + kääntäjä + NuGet + CLI-työkalut | **Rakennusvaiheessa** (`dotnet build`, `dotnet publish`) |
| `mcr.microsoft.com/dotnet/aspnet` | ASP.NET Core runtime + Kestrel-webpalvelin | **Ajoaikana** -- web-sovellukset (API, MVC, Razor) |
| `mcr.microsoft.com/dotnet/runtime` | .NET runtime (ilman web-komponentteja) | **Ajoaikana** -- konsolisovellukset, background-workerit |
| `mcr.microsoft.com/dotnet/runtime-deps` | Vain käyttöjärjestelmän riippuvuudet | Self-contained sovellusten ajaminen (harvinainen) |

```
Milloin mitäkin imagea:

┌─────────────────────────────────────────────────────────┐
│ Rakennusvaihe (Dockerfile: FROM ... AS build)           │
│   → Käytä: dotnet/sdk                                   │
│   → Sisältää: kääntäjä, NuGet, dotnet CLI               │
│   → Koko: ~800 MB (ei haittaa, ei mene tuotantoon!)      │
└────────────────────────────┬────────────────────────────┘
                             │ COPY --from=build
                             ▼
┌─────────────────────────────────────────────────────────┐
│ Ajoympäristö (Dockerfile: FROM ... AS runtime)           │
│                                                          │
│   Web-sovellus (API/MVC)?                                │
│     → Käytä: dotnet/aspnet (~110 MB alpine)              │
│                                                          │
│   Konsolisovellus / Worker?                              │
│     → Käytä: dotnet/runtime (~90 MB alpine)              │
└─────────────────────────────────────────────────────────┘
```

### Imagejen koot (arviot, .NET 8)

| Image | Debian | Alpine | Säästö |
|---|---|---|---|
| `dotnet/sdk:8.0` | ~800 MB | ~500 MB | 38% |
| `dotnet/aspnet:8.0` | ~220 MB | ~110 MB | **50%** |
| `dotnet/runtime:8.0` | ~190 MB | ~90 MB | **53%** |

> **Suositus:** Käytä **aina** Alpine-pohjaisia imageja tuotannossa (`8.0-alpine`). Ne ovat puolet pienempiä, nopeampia ladata ja turvallisempia. SDK-imagella ei ole väliä, koska se ei päädy lopulliseen tuotanto-imageen.

### Versiotagit ja niiden merkitys

```dockerfile
# ✅ Tarkka versio (suositeltu tuotannossa -- täysin toistettava)
FROM mcr.microsoft.com/dotnet/sdk:8.0.100

# ✅ Pääversio (saa automaattisesti patch-päivitykset -- hyvä kompromissi)
FROM mcr.microsoft.com/dotnet/sdk:8.0

# ✅ Alpine-pohjainen (pienempi image)
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine

# ❌ Vältä: latest (voi vaihtua mihin tahansa versioon milloin tahansa!)
FROM mcr.microsoft.com/dotnet/sdk:latest
```

> **Miksi `latest` on vaarallinen?** Kuvittele, että Dockerfile toimii tänään. Kuukauden päästä Microsoft julkaisee .NET 9:n, `latest` vaihtuu versioon 9.0, ja build rikkoutuu koska koodisi ei ole yhteensopiva. Käytä aina eksplisiittistä versiota.

---

## Konsolisovelluksen Dockerfile

### Projektirakenne

```
MyConsoleApp/
├── MyConsoleApp.csproj
├── Program.cs
├── Dockerfile
└── .dockerignore
```

### .dockerignore

```
**/.dockerignore
**/.git
**/.vs
**/.vscode
**/bin
**/obj
**/Dockerfile*
**/docker-compose*
**/*.user
**/*.suo
**/README.md
```

### Yksinkertainen Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . .
RUN dotnet publish -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/runtime:8.0
WORKDIR /app
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MyConsoleApp.dll"]
```

### Optimoitu Dockerfile (multi-stage + cache)

```dockerfile
# Vaihe 1: Riippuvuuksien palautus
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS restore
WORKDIR /src
COPY MyConsoleApp.csproj .
RUN dotnet restore

# Vaihe 2: Rakentaminen
FROM restore AS build
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

# Vaihe 3: Ajoympäristö
FROM mcr.microsoft.com/dotnet/runtime:8.0-alpine AS runtime
WORKDIR /app

# Luo ei-root käyttäjä
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "MyConsoleApp.dll"]
```

### Rakentaminen ja ajaminen

```bash
# Rakenna image
docker build -t myconsoleapp:1.0 .

# Aja kontti
docker run myconsoleapp:1.0

# Aja kontti ympäristömuuttujalla
docker run -e "MY_SETTING=arvo" myconsoleapp:1.0
```

---

## ASP.NET Core Web API:n Dockerfile

### Projektirakenne

```
MyWebApi/
├── Controllers/
│   └── WeatherController.cs
├── Program.cs
├── MyWebApi.csproj
├── appsettings.json
├── appsettings.Development.json
├── Dockerfile
└── .dockerignore
```

### .dockerignore

```
**/.dockerignore
**/.git
**/.vs
**/.vscode
**/bin
**/obj
**/Dockerfile*
**/docker-compose*
**/*.user
**/*.suo
**/README.md
**/appsettings.Development.json
```

### Dockerfile

```dockerfile
# Vaihe 1: Riippuvuuksien palautus
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS restore
WORKDIR /src
COPY MyWebApi.csproj .
RUN dotnet restore

# Vaihe 2: Rakentaminen ja julkaisu
FROM restore AS build
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

# Vaihe 3: Tuotantoimage
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app

# Ympäristömuuttujat
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080

# Luo ei-root käyttäjä
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

COPY --from=build /app/publish .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "MyWebApi.dll"]
```

### Rakentaminen ja ajaminen

```bash
# Rakenna image
docker build -t mywebapi:1.0 .

# Käynnistä kontti
docker run -d -p 8080:8080 --name myapi mywebapi:1.0

# Testaa API
curl http://localhost:8080/weatherforecast

# Tarkastele lokeja
docker logs myapi

# Pysäytä ja poista
docker stop myapi && docker rm myapi
```

---

## Multi-stage build -strategia .NET-projekteille

### Miksi multi-stage build on välttämätön .NET:lle?

.NET-sovellusten kohdalla multi-stage build on erityisen tärkeä, koska SDK-image on **erittäin suuri** (~800 MB) verrattuna runtime-imageen (~110 MB Alpine).

```
SDK-image (~800 MB)             Runtime-image (~110 MB)
┌────────────────────┐          ┌────────────────────┐
│ .NET SDK            │          │ .NET Runtime        │
│ C#-kääntäjä (Roslyn)│         │ Sovellus.dll        │
│ MSBuild             │          │ appsettings.json    │
│ NuGet CLI           │  COPY   │ riippuvuudet.dll    │
│ dotnet CLI          │ ──────► │                     │
│ Lähdekoodi (.cs)    │         │ Ei SDK:ta ✓         │
│ .csproj-tiedostot   │         │ Ei lähdekoodia ✓    │
│ NuGet-cache         │         │ Ei kääntäjää ✓      │
└────────────────────┘          └────────────────────┘
 HÄVITETÄÄN                      Tämä menee tuotantoon
```

### Restore-vaiheen optimointi (cache-strategia)

Tämä on .NET-Dockerfilen **tärkein optimointi**. Ajatus: `.csproj`-tiedostot muuttuvat **harvoin** (vain kun lisäät/poistat NuGet-paketteja), mutta lähdekoodi muuttuu **jatkuvasti**.

```dockerfile
# ✅ HYVÄ: Restore erikseen (hyödyntää Docker-cachea)
COPY MyWebApi.csproj .          # Kerros 1: vain .csproj
RUN dotnet restore              # Kerros 2: NuGet-pakettien lataus (cached!)
COPY . .                        # Kerros 3: lähdekoodi (muuttuu usein)
RUN dotnet publish -c Release -o /app/publish --no-restore
```

```dockerfile
# ❌ HUONO: Kaikki kerralla (restore JOKA KERTA kun koodi muuttuu)
COPY . .                        # Kerros 1: kaikki tiedostot (muuttuu joka kerta)
RUN dotnet publish -c Release -o /app/publish  # Kerros 2: restore + build joka kerta!
```

**Käytännön vaikutus:**

```
Hyvä järjestys (koodimuutos):          Huono järjestys (koodimuutos):
┌──────────────────────────────┐       ┌──────────────────────────────┐
│ COPY .csproj          CACHED │       │ COPY . .           REBUILD! │
│ RUN dotnet restore    CACHED │       │ RUN dotnet publish REBUILD! │
│ COPY . .              BUILD  │       │                             │
│ RUN dotnet publish    BUILD  │       │                             │
│                              │       │                             │
│ Aika: ~10 sekuntia      ✅   │       │ Aika: ~60 sekuntia     ❌   │
└──────────────────────────────┘       └──────────────────────────────┘
```

### Solution-tason multi-stage build

Jos projektissa on useita projekteja (esim. solution):

```
MySolution/
├── MySolution.sln
├── src/
│   ├── MyWebApi/
│   │   └── MyWebApi.csproj
│   └── MyLibrary/
│       └── MyLibrary.csproj
└── tests/
    └── MyWebApi.Tests/
        └── MyWebApi.Tests.csproj
```

```dockerfile
# Vaihe 1: Restore
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS restore
WORKDIR /src

# Kopioi solution ja projektiviittaukset
COPY MySolution.sln .
COPY src/MyWebApi/MyWebApi.csproj src/MyWebApi/
COPY src/MyLibrary/MyLibrary.csproj src/MyLibrary/
RUN dotnet restore

# Vaihe 2: Build
FROM restore AS build
COPY . .
RUN dotnet publish src/MyWebApi/MyWebApi.csproj -c Release -o /app/publish --no-restore

# Vaihe 3: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyWebApi.dll"]
```

---

## Ympäristömuuttujat .NET Docker -konteissa

### Tärkeimmät ympäristömuuttujat

| Muuttuja | Kuvaus | Esimerkkiarvo | Miksi tärkeä? |
|---|---|---|---|
| `ASPNETCORE_ENVIRONMENT` | Sovelluksen ympäristö | `Development`, `Production` | Määrittää, mitä `appsettings.{Env}.json`-tiedostoa käytetään |
| `ASPNETCORE_URLS` | Kuunneltavat URL:t | `http://+:8080` | Määrittää millä portilla sovellus kuuntelee kontissa |
| `DOTNET_RUNNING_IN_CONTAINER` | Onko kontissa | `true` (automaattinen) | .NET optimoi muistinkäytön konttiympäristöön |
| `ConnectionStrings__*` | Tietokantayhteydet | `Host=db;...` | Ylikirjoittaa appsettings.json-arvot |

### Miten ympäristömuuttujat toimivat ASP.NET Coressa?

ASP.NET Core lukee konfiguraation **useasta lähteestä** tietyssä prioriteettijärjestyksessä. Myöhempi ylikirjoittaa aiemman:

```
Prioriteetti (alin → ylin):

1. appsettings.json                    ◄── Oletusarvot
2. appsettings.{Environment}.json      ◄── Ympäristökohtaiset arvot
3. Ympäristömuuttujat                  ◄── Docker-kontissa annetut arvot ★
4. Komentoriviargumentit               ◄── Harvoin käytetty konteissa
```

**Tärkeä sääntö:** Kaksi alaviivaa (`__`) ympäristömuuttujassa korvaavat hierarkian erottimen (`:` tai `.`):

```json
// appsettings.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=dev"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  }
}
```

```bash
# Vastaavat ympäristömuuttujat (ylikirjoittavat JSON-arvot):
ConnectionStrings__DefaultConnection=Host=db;Database=prod;...
#                 ^^
#                 Kaksi alaviivaa = hierarkian erotin
Logging__LogLevel__Default=Warning
```

### Käytännön esimerkit

```bash
# Docker run -komennolla
docker run -d \
  -e "ASPNETCORE_ENVIRONMENT=Development" \
  -e "ConnectionStrings__DefaultConnection=Host=db;Database=mydb;Username=sa;Password=secret" \
  -p 8080:8080 \
  mywebapi:1.0
```

```yaml
# Docker Composessa (suositeltu tapa)
services:
  api:
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=db;Database=mydb;Username=sa;Password=secret
```

> **Käytännön vinkki:** Älä kovakoodaa connection stringiä `docker-compose.yml`-tiedostoon. Käytä `.env`-tiedostoa muuttujille kuten salasanat -- katso [Docker Compose .NET-projekteissa](DotNet-Docker-Compose.md).

---

## Debuggaus Docker-kontissa

### Visual Studio Docker -tuki

Visual Studio tukee Docker-konttien debuggausta suoraan. Se luo automaattisesti Dockerfile-tiedoston ja konfiguroi debuggauksen.

1. **Lisää Docker-tuki projektiin:**
   - Klikkaa projektia hiiren oikealla > **Add** > **Docker Support**
   - Valitse **Linux** tai **Windows**

2. **Käynnistä debuggaus:**
   - Valitse **Docker** launch-profiili
   - Paina **F5** (Debug) tai **Ctrl+F5** (ilman debuggausta)

3. Visual Studio:
   - Rakentaa Docker-imagen
   - Käynnistää kontin
   - Liittää debuggerin konttiin
   - Tukee breakpointeja, watch-ikkunaa jne.

### Docker-lokit

```bash
# Tarkastele kontin lokeja
docker logs myapi

# Seuraa lokeja reaaliajassa
docker logs -f myapi

# Näytä viimeiset 50 riviä
docker logs --tail 50 myapi
```

### Kontin sisällä tutkiminen

```bash
# Avaa shell konttiin
docker exec -it myapi bash

# Alpine-pohjaisissa imageissa käytä sh
docker exec -it myapi sh

# Tarkista ympäristömuuttujat
docker exec myapi printenv

# Tarkista prosessit
docker exec myapi ps aux

# Tarkista verkkoyhteydet
docker exec myapi wget -qO- http://localhost:8080/health
```

---

## Yleisimmät virheet ja ratkaisut

| Ongelma | Syy | Ratkaisu |
|---|---|---|
| `Could not find file '/app/MyApp.dll'` | ENTRYPOINT viittaa väärään DLL-nimeen | Tarkista, että DLL-nimi vastaa projektin nimeä: `ENTRYPOINT ["dotnet", "MyWebApi.dll"]` |
| `Unable to bind to http://localhost:5000` | Sovellus kuuntelee vain localhostia | Käytä `ASPNETCORE_URLS=http://+:8080` (+ = kaikki osoitteet) |
| Image on valtava (~800 MB) | Käytetään SDK-imagea ajoaikana | Käytä multi-stage buildia: `aspnet:8.0-alpine` runtime-vaiheessa |
| `dotnet restore` kestää kauan joka kerta | Cache ei toimi -- kaikki kopioidaan kerralla | Kopioi `.csproj` ensin, sitten `dotnet restore`, sitten `COPY . .` |
| Portti ei toimi | Porttimappaus puuttuu tai on väärä | Varmista: `-p 8080:8080` ja `ASPNETCORE_URLS=http://+:8080` porttien täytyy täsmätä |
| `Permission denied` Alpine-imagessa | Käyttäjäoikeudet puuttuvat | Luo käyttäjä ja anna oikeudet: `RUN adduser...` + `USER appuser` |
| `appsettings.Development.json` ei lataudu | Ympäristö on oletuksena `Production` | Aseta `ASPNETCORE_ENVIRONMENT=Development` ympäristömuuttujalla |

---

## Yhteenveto: .NET Dockerfile -vaiheet

```
1. RESTORE              2. BUILD                3. RUNTIME
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│ SDK image      │     │ SDK image      │     │ Runtime image  │
│                │     │                │     │                │
│ Kopioi .csproj │     │ Kopioi koodi   │     │ Kopioi publish │
│ dotnet restore │────►│ dotnet publish │────►│ Ei SDK:ta      │
│                │     │                │     │ Ei koodia      │
│ NuGet cache ✓  │     │ Käännetty ✓    │     │ Pieni image ✓  │
└────────────────┘     └────────────────┘     └────────────────┘
```

| Vaihe | Tehtävä | Image |
|---|---|---|
| Restore | NuGet-pakettien palautus | `dotnet/sdk` |
| Build | Koodin kääntäminen ja julkaisu | `dotnet/sdk` |
| Runtime | Sovelluksen ajaminen | `dotnet/aspnet` tai `dotnet/runtime` |

Seuraavaksi: [Docker Compose .NET-projekteissa](DotNet-Docker-Compose.md)
