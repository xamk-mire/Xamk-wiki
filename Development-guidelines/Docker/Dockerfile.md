# Dockerfile

Dockerfile on tekstimuotoinen ohjetiedosto, joka sisältää kaikki komennot Docker-imagen rakentamiseen. Se on kuin **resepti**, joka kertoo Dockerille vaihe vaiheelta, miten image rakennetaan.

## Miten Dockerfile toimii?

Kun suoritat `docker build -t myapp .`, Docker lukee Dockerfilen rivi kerrallaan ja suorittaa jokaisen instruktion. Jokainen instruktio luo **uuden kerroksen** (layer) imageen:

```
Dockerfile                          Image (kerrokset)
┌──────────────────────┐           ┌───────────────────┐
│ FROM node:20-alpine  │──────────►│ Kerros 1: Node.js │ (perus-image)
├──────────────────────┤           ├───────────────────┤
│ WORKDIR /app         │──────────►│ Kerros 2: /app    │
├──────────────────────┤           ├───────────────────┤
│ COPY package.json .  │──────────►│ Kerros 3: paketti │
├──────────────────────┤           ├───────────────────┤
│ RUN npm install      │──────────►│ Kerros 4: riipp.  │
├──────────────────────┤           ├───────────────────┤
│ COPY . .             │──────────►│ Kerros 5: koodi   │
└──────────────────────┘           └───────────────────┘
```

> **Miksi kerroksilla on väliä?** Docker tallentaa jokaisen kerroksen välimuistiin. Jos kerros ei muutu, Dockerin ei tarvitse rakentaa sitä uudelleen. Tämä tekee uudelleenrakentamisesta **erittäin nopeaa**. Lisää tästä [Kerrosten välimuisti](#kerrosten-välimuisti-layer-caching) -osiossa.

## Perusrakenne

```dockerfile
# Kommentit alkavat risuaidalla
FROM <perus-image>          # Perus-image, jonka päälle rakennetaan
WORKDIR /app                # Asetetaan työkansio
COPY . .                    # Kopioidaan tiedostot
RUN <komento>               # Suoritetaan komento rakennusvaiheessa
EXPOSE <portti>             # Dokumentoidaan käytetty portti
CMD ["komento"]             # Oletuskomento kontin käynnistyessä
```

---

## Tärkeimmät instruktiot

### FROM - Perus-image

Jokainen Dockerfile alkaa `FROM`-instruktiolla. Se määrittää perus-imagen, jonka päälle rakennetaan. Kukaan ei rakenna imagea tyhjästä -- aina käytetään valmista pohjaa, jossa on jo käyttöjärjestelmä ja tarvittavat työkalut.

```dockerfile
# Käytä virallista Node.js-imagea
FROM node:20-alpine

# Käytä virallista .NET-imagea
FROM mcr.microsoft.com/dotnet/sdk:8.0

# Käytä minimaalista Linux-imagea
FROM alpine:3.19

# Aloita tyhjästä (vain staattisille binääreille)
FROM scratch
```

#### Alpine vs. täysi image

| Image | Koko | Pohjana |
|---|---|---|
| `node:20` | ~1 GB | Debian Linux (täysi) |
| `node:20-slim` | ~200 MB | Debian Linux (karsittu) |
| `node:20-alpine` | ~130 MB | Alpine Linux (minimaalinen) |

> **Suositus:** Käytä Alpine-pohjaisia imageja aina kun mahdollista. Ne ovat pienempiä, nopeampia ladata ja turvallisempia (vähemmän hyökkäyspintaa). Jos jokin kirjasto ei toimi Alpinella, käytä `slim`-versiota.

### WORKDIR - Työkansio

Asettaa työkansion kaikille seuraaville instruktioille. Jos kansiota ei ole, Docker luo sen automaattisesti.

```dockerfile
WORKDIR /app

# Voit käyttää useita WORKDIR-instruktioita
WORKDIR /app
WORKDIR src
# Nyt työkansio on /app/src
```

### COPY - Tiedostojen kopiointi

Kopioi tiedostoja ja kansioita isäntäkoneelta imageen.

```dockerfile
# Kopioi kaikki tiedostot nykyisestä kansiosta työkansion
COPY . .

# Kopioi yksittäinen tiedosto
COPY package.json .

# Kopioi useita tiedostoja
COPY package.json package-lock.json ./

# Kopioi kansio
COPY src/ ./src/

# Muuta omistajuus kopioinnin yhteydessä
COPY --chown=appuser:appgroup . .
```

### ADD - Tiedostojen lisäys

Toimii kuten `COPY`, mutta tukee myös URL-osoitteita ja automaattista arkistojen purkamista.

```dockerfile
# Lataa tiedosto URL:stä
ADD https://example.com/file.tar.gz /app/

# Pura arkisto automaattisesti
ADD archive.tar.gz /app/
```

> **Suositus:** Käytä `COPY`-instruktiota aina kun mahdollista. `ADD` on tarpeellinen vain URL-latauksissa ja arkistojen purkamisessa.

### RUN - Komennon suoritus

Suorittaa komennon imagen rakennusvaiheessa. Jokainen `RUN`-instruktio luo uuden kerroksen.

```dockerfile
# Asenna paketteja
RUN apt-get update && apt-get install -y curl

# .NET-sovelluksen riippuvuuksien palautus
RUN dotnet restore

# Node.js-riippuvuuksien asennus
RUN npm ci

# Useita komentoja yhdellä RUN-instruktiolla (vähentää kerroksia)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### CMD - Oletuskomento

Määrittää komennon, joka suoritetaan kontin käynnistyessä. Dockerfile voi sisältää vain yhden `CMD`-instruktion.

```dockerfile
# Exec-muoto (suositeltu)
CMD ["dotnet", "MyApp.dll"]

# Shell-muoto
CMD dotnet MyApp.dll

# Node.js-esimerkki
CMD ["node", "server.js"]
```

### ENTRYPOINT - Kiinteä käynnistyskomento

Samanlainen kuin `CMD`, mutta `ENTRYPOINT`-komentoa ei voi ohittaa kontin käynnistyessä ilman `--entrypoint`-lippua.

```dockerfile
# Käytä ENTRYPOINT + CMD yhdessä
ENTRYPOINT ["dotnet"]
CMD ["MyApp.dll"]
# Tuloksena: dotnet MyApp.dll

# CMD:n voi tällöin ohittaa
# docker run myimage AnotherApp.dll
# Tuloksena: dotnet AnotherApp.dll
```

> **Muistisääntö:**
> - `CMD` = "oletuskomento, jonka käyttäjä voi korvata"
> - `ENTRYPOINT` = "kiinteä komento, jonka argumentteja voidaan muuttaa"

### EXPOSE - Portin dokumentointi

Dokumentoi, mitä porttia kontti kuuntelee. Ei avaa porttia itsessään - se tehdään `docker run -p` -komennolla.

```dockerfile
# Web-sovellus
EXPOSE 80
EXPOSE 443

# Useita portteja
EXPOSE 8080 8443
```

### ENV - Ympäristömuuttujat

Asettaa ympäristömuuttujia, jotka ovat käytettävissä sekä rakennusvaiheessa että kontin ajon aikana.

```dockerfile
ENV NODE_ENV=production
ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:80

# Useita muuttujia
ENV APP_NAME=MyApp \
    APP_VERSION=1.0
```

### ARG - Rakennusaikaiset muuttujat

Muuttujia, jotka ovat käytettävissä vain imagen rakennusvaiheessa (ei kontin ajon aikana).

```dockerfile
ARG DOTNET_VERSION=8.0
FROM mcr.microsoft.com/dotnet/sdk:${DOTNET_VERSION}

ARG BUILD_CONFIGURATION=Release
RUN dotnet build -c ${BUILD_CONFIGURATION}
```

```bash
# Aseta ARG-arvo rakennusvaiheessa
docker build --build-arg DOTNET_VERSION=9.0 -t myapp .
```

### USER - Käyttäjän vaihto

Vaihtaa käyttäjän, jolla seuraavat komennot ja kontti ajetaan.

```dockerfile
# Luo käyttäjä ja vaihda siihen
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser
```

> **Turvallisuus:** Älä aja sovelluksia root-käyttäjänä tuotannossa. Käytä aina erillistä käyttäjää.

### HEALTHCHECK - Terveystarkistus

Määrittää komennon, jolla Docker tarkistaa kontin terveyden.

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1
```

---

## Build-konteksti (Build Context)

Kun suoritat `docker build -t myapp .`, piste (`.`) määrittää **build-kontekstin** eli kansion, jonka sisällön Docker lähettää Docker Daemonille. Docker Daemon tarvitsee nämä tiedostot `COPY`- ja `ADD`-instruktioiden suorittamiseen.

```bash
docker build -t myapp .
#                     ^ build-konteksti = nykyinen kansio

docker build -t myapp ./backend
#                     ^ build-konteksti = backend-kansio
```

> **Tärkeää ymmärtää:** Docker lähettää **koko** build-kontekstin (kaikki tiedostot kansiossa) Daemonille ennen rakentamisen aloittamista. Jos kansiossa on paljon turhia tiedostoja (esim. `node_modules/`, `.git/`, `bin/`, `obj/`), lähetys kestää pitkään ja vie turhaan tilaa.

```
Sending build context to Docker daemon  856.2MB   <-- HIDAS!
vs.
Sending build context to Docker daemon  12.5MB    <-- NOPEA!
```

Ratkaisu: `.dockerignore`-tiedosto.

## .dockerignore

`.dockerignore`-tiedosto toimii kuten `.gitignore` -- se määrittää, mitkä tiedostot **jätetään pois build-kontekstista**. Tämä:

1. **Nopeuttaa rakennusta** -- vähemmän tiedostoja lähetetään Docker Daemonille
2. **Pienentää imagea** -- turhat tiedostot eivät päädy imageen
3. **Parantaa turvallisuutta** -- salaisuudet (`.env`, avaimet) eivät päädy imageen
4. **Estää cache-ongelmia** -- esim. paikallinen `bin/`-kansio ei ylikirjoita kontin tiedostoja

```
# .dockerignore

# Versionhallinta
.git
.gitignore

# IDE-tiedostot
.vs/
.vscode/
*.user
*.suo

# Build-tulosteet
bin/
obj/
node_modules/

# Docker-tiedostot
Dockerfile
docker-compose*.yml
.dockerignore

# Dokumentaatio
README.md
docs/

# Ympäristömuuttujat (salaisuudet!)
.env
.env.local
```

---

## Kerrosten välimuisti (Layer Caching)

Dockerin tehokkuus perustuu kerrosten välimuistiin. Ymmärtämällä miten cache toimii, voit tehdä imagen rakentamisesta **huomattavasti nopeampaa**.

### Miten cache toimii?

Docker tarkistaa jokaiselle kerrokselle: "Onko tämä instruktio JA sen syötteet muuttuneet edellisen rakennuksen jälkeen?"

- **Jos ei** → käytä välimuistia (sekunneissa)
- **Jos kyllä** → rakenna tämä ja KAIKKI seuraavat kerrokset uudelleen

```
Dockerfile                  1. build    2. build (koodimuutos)
┌──────────────────────┐    
│ FROM node:20-alpine  │    rakennetaan  ✅ CACHED
├──────────────────────┤    
│ COPY package.json .  │    rakennetaan  ✅ CACHED (package.json ei muuttunut)
├──────────────────────┤    
│ RUN npm install      │    rakennetaan  ✅ CACHED (ei tarvitse asentaa uudelleen!)
├──────────────────────┤    
│ COPY . .             │    rakennetaan  🔄 RAKENNETAAN (koodi muuttui)
├──────────────────────┤    
│ CMD ["node", "app"]  │    rakennetaan  🔄 RAKENNETAAN (edellinen muuttui)
└──────────────────────┘    
                            ~60s          ~3s  ← VALTAVA ero!
```

### Käytännön sääntö

**Järjestä Dockerfile niin, että harvoin muuttuvat asiat ovat YLHÄÄLLÄ ja usein muuttuvat asiat ALHAALLA:**

```dockerfile
# ✅ HYVÄ järjestys:
FROM node:20-alpine
WORKDIR /app

# 1. Kopioi ENSIN vain riippuvuustiedostot
COPY package.json package-lock.json ./

# 2. Asenna riippuvuudet (cache toimii niin kauan kuin package.json ei muutu)
RUN npm ci

# 3. Kopioi lähdekoodi VIIMEISENÄ (muuttuu useimmin)
COPY . .

CMD ["node", "server.js"]
```

```dockerfile
# ❌ HUONO järjestys:
FROM node:20-alpine
WORKDIR /app

# Kopioidaan KAIKKI kerralla -- yksikin koodimuutos rikkoo cachen
COPY . .

# npm install ajetaan JOKA KERTA kun mikä tahansa tiedosto muuttuu!
RUN npm ci

CMD ["node", "server.js"]
```

---

## Multi-stage build

Multi-stage build mahdollistaa usean `FROM`-instruktion käytön samassa Dockerfilessa. Se on Dockerin **tärkein optimointitekniikka** tuotantoimageja rakennettaessa.

### Ongelma: Yksivaiheinen build

```dockerfile
# HUONO: SDK + kaikki build-työkalut jäävät lopulliseen imageen
FROM mcr.microsoft.com/dotnet/sdk:8.0
WORKDIR /app
COPY . .
RUN dotnet publish -c Release -o /app/publish
CMD ["dotnet", "publish/MyApp.dll"]
# Imagen koko: ~800 MB 😱
```

**Mikä on ongelmana?**
- Lopullinen image sisältää .NET SDK:n, kääntäjän, NuGet-työkalut -- **niitä ei tarvita ajon aikana**
- Image on valtava (~800 MB) → hidas ladata, hidas käynnistää
- SDK-työkalut lisäävät hyökkäyspintaa (turvallisuusriski)
- Lähdekoodi on imagen sisällä (turhaa ja mahdollinen tietoturvariski)

### Ratkaisu: Multi-stage build

Ajatus on yksinkertainen: **käytä yhtä imagea rakentamiseen, toista ajamiseen**. Vain lopputulos (käännetyt tiedostot) kopioidaan lopulliseen imageen.

```dockerfile
# ────── VAIHE 1: Rakenna sovellus (build stage) ──────
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY *.csproj .
RUN dotnet restore
COPY . .
RUN dotnet publish -c Release -o /app/publish
# Tässä vaiheessa image on ~800 MB -- mutta se EI ole lopullinen image!

# ────── VAIHE 2: Luo tuotantoimage (runtime stage) ──────
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS runtime
WORKDIR /app
COPY --from=build /app/publish .
#     ^^^^^^^^^^^^
#     Kopioi VAIN käännetyt DLL:t build-vaiheesta
#     SDK, lähdekoodi, NuGet-cache -- kaikki jää pois!
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyApp.dll"]
# Lopullinen image: ~110 MB ✅
```

### Visuaalinen vertailu

```
Yksivaiheinen:                Multi-stage:
┌─────────────────┐          ┌─────────────────┐   ┌──────────────────┐
│ .NET SDK (~700MB)│          │ .NET SDK (~700MB)│   │ .NET Runtime     │
│ Kääntäjä        │          │ Kääntäjä        │   │   (~100MB)       │
│ NuGet           │          │ NuGet           │   │                  │
│ Lähdekoodi      │          │ Lähdekoodi      │──►│ Sovellus (DLL)   │
│ Sovellus (DLL)  │          │ Sovellus (DLL)  │   │ appsettings.json │
│                 │          │                 │   │                  │
│   ~800 MB       │          │ HÄVITETÄÄN ✗    │   │   ~110 MB ✓      │
└─────────────────┘          └─────────────────┘   └──────────────────┘
 Tämä menee tuotantoon        Build-vaihe          Tämä menee tuotantoon
```

### Hyödyt

| Ominaisuus | Ilman multi-stage | Multi-stage |
|---|---|---|
| Imagen koko | ~800 MB (SDK) | ~110 MB (runtime + alpine) |
| Sisältö | SDK + kääntäjä + lähdekoodi | Vain runtime + DLL:t |
| Turvallisuus | SDK-työkalut mukana | Minimaalinen hyökkäyspinta |
| Latausaika | Hidas | Nopea |
| Muistinkäyttö | Korkea | Matala |

---

## Parhaat käytännöt (yhteenveto)

| # | Käytäntö | Miksi? |
|---|---|---|
| 1 | Käytä pieniä perus-imageja (`alpine`, `slim`) | Pienempi image = nopeampi lataus, vähemmän haavoittuvuuksia |
| 2 | Hyödynnä kerrosten välimuistia | Nopea uudelleenrakentaminen (katso [Layer Caching](#kerrosten-välimuisti-layer-caching)) |
| 3 | Yhdistä RUN-instruktiot | Vähemmän kerroksia = pienempi image |
| 4 | Käytä multi-stage buildia | Lopullinen image sisältää vain tarvittavan (katso [Multi-stage](#multi-stage-build)) |
| 5 | Älä aja root-käyttäjänä | Turvallisuus -- rajoittaa vahinkoa jos kontti murretaan |
| 6 | Käytä .dockerignore-tiedostoa | Nopeampi build, ei turhia tiedostoja imagessa |
| 7 | Merkitse versiot tarkasti | Toistettavat buildit -- `latest` voi muuttua milloin tahansa |

### Esimerkit

```dockerfile
# ✅ Pienet imaget
FROM node:20-alpine         # ~130 MB
# ❌ FROM node:20           # ~1 GB

# ✅ Yhdistetyt RUN-instruktiot (yksi kerros)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
# ❌ Kolme erillistä RUN-instruktiota = kolme turhaa kerrosta

# ✅ Ei-root käyttäjä
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser
USER appuser

# ✅ Tarkat versiot
FROM node:20.11-alpine3.19    # Tarkka, toistettava
FROM node:20-alpine           # OK, saa patch-päivitykset
# ❌ FROM node:latest         # Voi rikkoutua milloin tahansa!
```

---

## Imagen rakentaminen ja ajaminen

```bash
# Rakenna image nykyisestä kansiosta
docker build -t myapp:1.0 .

# Rakenna eri Dockerfilestä
docker build -f Dockerfile.dev -t myapp:dev .

# Rakenna ARG-arvoilla
docker build --build-arg BUILD_CONFIGURATION=Debug -t myapp:debug .

# Käynnistä kontti imagesta
docker run -d -p 8080:80 --name myapp myapp:1.0

# Käynnistä ympäristömuuttujilla
docker run -d -p 8080:80 -e "ASPNETCORE_ENVIRONMENT=Development" myapp:1.0
```

---

## Yhteenveto

| Instruktio | Tarkoitus |
|---|---|
| `FROM` | Perus-image |
| `WORKDIR` | Työkansio |
| `COPY` | Kopioi tiedostoja |
| `RUN` | Suorita komento (rakennusaikana) |
| `CMD` | Oletuskomento (ajoaikana) |
| `ENTRYPOINT` | Kiinteä käynnistyskomento |
| `EXPOSE` | Dokumentoi portti |
| `ENV` | Ympäristömuuttuja (rakennus + ajo) |
| `ARG` | Rakennusaikainen muuttuja |
| `USER` | Käyttäjän vaihto |
| `HEALTHCHECK` | Terveystarkistus |

Seuraavaksi: [Docker Compose](Docker-Compose.md)
