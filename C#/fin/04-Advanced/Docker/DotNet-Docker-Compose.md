# Docker Compose .NET-projekteissa

Tämä materiaali käsittelee Docker Composen käyttöä .NET-projekteissa. Opit konfiguroimaan ASP.NET Core -sovelluksen yhdessä tietokannan kanssa, hallitsemaan connection stringejä, terveystarkistuksia ja kehitysympäristöä Docker Composella.

> **Edellytykset:** Tutustu ensin [Docker Compose -perusteisiin](https://github.com/xamk-mire/Xamk-wiki/blob/main/Development-guidelines/Docker/Docker-Compose.md) ja [.NET-sovelluksen kontitukseen](DotNet-Docker.md).

## Kokonaiskuva: .NET + Docker Compose

Tyypillisessä .NET-projektissa Docker Compose yhdistää useita palveluita:

```
docker-compose.yml hallinnoi koko ympäristöä:

┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose                            │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │ API      │───►│ Postgres │    │ pgAdmin  │               │
│  │ (build)  │    │ (image)  │    │ (image)  │               │
│  │ :8080    │    │ :5432    │    │ :5050    │               │
│  └──────────┘    └──────────┘    └──────────┘               │
│       │               │                                      │
│       │          ┌────┴────┐                                 │
│       │          │ Volume  │ ← Tietokantadata säilyy         │
│       │          │ pg-data │                                 │
│       │          └─────────┘                                 │
│       │                                                      │
│  ┌────┴──────────────────────────────────────┐               │
│  │ .env-tiedosto                              │               │
│  │ DB_PASSWORD=xxx   DB_NAME=mydb             │               │
│  └────────────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## ASP.NET Core + SQL Server

### Projektirakenne

```
MyWebApi/
├── Controllers/
│   └── ProductsController.cs
├── Data/
│   └── AppDbContext.cs
├── Models/
│   └── Product.cs
├── Program.cs
├── MyWebApi.csproj
├── appsettings.json
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── .env
```

### Dockerfile

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS restore
WORKDIR /src
COPY MyWebApi.csproj .
RUN dotnet restore

FROM restore AS build
COPY . .
RUN dotnet publish -c Release -o /app/publish --no-restore

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
ENV ASPNETCORE_URLS=http://+:8080
COPY --from=build /app/publish .
EXPOSE 8080
ENTRYPOINT ["dotnet", "MyWebApi.dll"]
```

### docker-compose.yml

```yaml
services:
  # ASP.NET Core Web API
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Server=sqlserver;Database=${DB_NAME};User Id=sa;Password=${DB_PASSWORD};TrustServerCertificate=True
    depends_on:
      sqlserver:
        condition: service_healthy
    restart: unless-stopped

  # SQL Server
  sqlserver:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - MSSQL_SA_PASSWORD=${DB_PASSWORD}
    ports:
      - "1433:1433"
    volumes:
      - sqlserver-data:/var/opt/mssql
    healthcheck:
      test: /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "${DB_PASSWORD}" -C -Q "SELECT 1" -b
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s
    restart: unless-stopped

volumes:
  sqlserver-data:
```

### .env

```
DB_NAME=MyAppDb
DB_PASSWORD=Your_Strong_Password123!
```

> **Huom!** SQL Serverin salasanan tulee olla tarpeeksi vahva (iso kirjain, pieni kirjain, numero, erikoismerkki, vähintään 8 merkkiä). Muuten SQL Server ei käynnisty.

### Käynnistys ja testaus

```bash
# Käynnistä kaikki palvelut
docker compose up -d

# Tarkista tila
docker compose ps

# Seuraa API:n lokeja
docker compose logs -f api

# Testaa API
curl http://localhost:8080/weatherforecast

# Pysäytä
docker compose down
```

---

## ASP.NET Core + PostgreSQL

### docker-compose.yml

```yaml
services:
  # ASP.NET Core Web API
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=postgres;Port=5432;Database=${DB_NAME};Username=postgres;Password=${DB_PASSWORD}
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  # PostgreSQL
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # Valinnainen: alkudata
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 15s
    restart: unless-stopped

volumes:
  postgres-data:
```

### .env

```
DB_NAME=myappdb
DB_PASSWORD=kehitys_salasana
```

### Valinnainen: init.sql (alkudata)

```sql
-- Tämä ajetaan automaattisesti kun tietokanta luodaan ensimmäisen kerran
CREATE TABLE IF NOT EXISTS Products (
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Price DECIMAL(10,2) NOT NULL
);

INSERT INTO Products (Name, Price) VALUES
    ('Tuote 1', 19.99),
    ('Tuote 2', 29.99),
    ('Tuote 3', 39.99);
```

---

## Connection string -konfigurointi

Connection string -hallinta on yksi tärkeimmistä asioista ymmärtää .NET + Docker -ympäristössä. Tässä käydään läpi miten connection string kulkee `.env`-tiedostosta aina sovelluksen `DbContext`-luokkaan asti.

### Koko ketju: .env → docker-compose → ympäristömuuttuja → ASP.NET Core → DbContext

```
1. .env-tiedosto                    2. docker-compose.yml
┌──────────────────────────┐       ┌──────────────────────────────────────────┐
│ DB_PASSWORD=salasana123  │──────►│ environment:                             │
│ DB_NAME=myappdb          │       │   - ConnectionStrings__DefaultConnection │
└──────────────────────────┘       │     =Host=postgres;Password=${DB_PASSWORD}│
                                   └──────────────────┬───────────────────────┘
                                                      │
3. Kontin ympäristömuuttuja                           │
┌──────────────────────────────────────────────────────▼──┐
│ ConnectionStrings__DefaultConnection=                    │
│   Host=postgres;Port=5432;Database=myappdb;              │
│   Username=postgres;Password=salasana123                 │
└──────────────────────────────────┬──────────────────────┘
                                   │
4. ASP.NET Core konfiguraatio      │  (lukee automaattisesti!)
┌──────────────────────────────────▼──────────────────────┐
│ builder.Configuration.GetConnectionString("Default...") │
│                                                          │
│ Prioriteettijärjestys:                                   │
│   1. appsettings.json (oletusarvot)                      │
│   2. appsettings.Development.json                        │
│   3. Ympäristömuuttujat ← TÄMÄ VOITTAA! ★               │
└──────────────────────────────────┬──────────────────────┘
                                   │
5. Entity Framework Core           │
┌──────────────────────────────────▼──────────────────────┐
│ options.UseNpgsql(connectionString)                      │
│ → Yhdistää palveluun "postgres" Docker-verkossa           │
└─────────────────────────────────────────────────────────┘
```

### appsettings.json (oletusarvot paikalliseen kehitykseen)

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=mydb;Username=postgres;Password=localdev"
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

> **Huom:** `appsettings.json` sisältää **paikallisen kehityksen** oletusarvot (Host=**localhost**). Docker-ympäristössä nämä ylikirjoitetaan ympäristömuuttujalla (Host=**postgres**).

### Ympäristömuuttujalla ylikirjoitus

Docker Compose -ympäristössä ympäristömuuttuja ylikirjoittaa `appsettings.json`-arvon:

```yaml
environment:
  # Kaksi alaviivaa (__) = JSON-hierarkian erotin
  # ConnectionStrings : DefaultConnection  →  ConnectionStrings__DefaultConnection
  - ConnectionStrings__DefaultConnection=Host=postgres;Port=5432;Database=mydb;Username=postgres;Password=secret
```

### Program.cs - konfiguraation lataus

```csharp
var builder = WebApplication.CreateBuilder(args);

// ASP.NET Core lukee konfiguraation automaattisesti -- sinun ei tarvitse tehdä mitään erityistä!
// Se lukee järjestyksessä:
// 1. appsettings.json                    → Host=localhost (paikallinen)
// 2. appsettings.{Environment}.json      → Ympäristökohtaiset arvot
// 3. Ympäristömuuttujat                  → Host=postgres (Docker) ← TÄMÄ VOITTAA

// Rekisteröi DbContext -- sama koodi toimii paikallisesti JA Dockerissa!
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
```

### Palvelun nimi = hostname (DNS)

Docker Compose -ympäristössä palvelun nimi toimii DNS-nimenä. **Tämä on avainasia ymmärtää:**

```yaml
services:
  api:
    environment:
      # ↓ "postgres" viittaa alla olevaan palvelun nimeen
      - ConnectionStrings__DefaultConnection=Host=postgres;Port=5432;...
  
  postgres:    # ← TÄMÄ NIMI = DNS-nimi Docker-verkossa
    image: postgres:16-alpine
```

```
Paikallisessa kehityksessä:        Docker-ympäristössä:
Host=localhost                      Host=postgres
      │                                   │
      ▼                                   ▼
 PostgreSQL asennettuna              PostgreSQL-kontti nimeltä "postgres"
 omalla koneella                     Docker-verkossa
```

> **Käytännössä:** Ainoa asia joka muuttuu paikallisen ja Docker-ympäristön välillä on `Host`-arvo: `localhost` → palvelun nimi (esim. `postgres`). Muu connection string pysyy samana.

---

## Health checkit

### Miksi health checkejä tarvitaan?

Kuvittele tilanne ilman health checkejä:

```
Ilman health checkejä:
1. PostgreSQL-kontti käynnistyy      (ei vielä valmis!)
2. API-kontti käynnistyy välittömästi
3. API yrittää yhdistää tietokantaan
4. 💥 "Connection refused" -- tietokanta ei ole vielä valmis!
```

Health checkit ratkaisevat tämän: Docker tarkistaa **onko palvelu oikeasti toimintakunnossa** (ei pelkästään käynnissä), ja muut palvelut odottavat kunnes tarkistus onnistuu.

```
Health checkien kanssa:
1. PostgreSQL-kontti käynnistyy
2. Docker tarkistaa: "pg_isready?" ❌ (alustuu vielä)
3. Docker odottaa 10s, tarkistaa uudelleen: "pg_isready?" ❌
4. Docker odottaa 10s, tarkistaa: "pg_isready?" ✅ → HEALTHY!
5. API-kontti käynnistyy (tietokanta on valmis)
6. API yhdistää tietokantaan ✅
```

### Tietokanta health check

```yaml
# PostgreSQL -- pg_isready tarkistaa onko tietokanta valmis vastaanottamaan yhteyksiä
postgres:
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres"]
    interval: 10s       # Tarkista 10 sekunnin välein
    timeout: 5s         # Odota vastausta max 5 sekuntia
    retries: 5          # 5 epäonnistumisen jälkeen → "unhealthy"
    start_period: 15s   # Anna 15s aikaa käynnistyä ennen tarkistuksia

# SQL Server -- suorittaa SQL-kyselyn tarkistaakseen toiminnan
sqlserver:
  healthcheck:
    test: /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "${DB_PASSWORD}" -C -Q "SELECT 1" -b
    interval: 10s
    timeout: 5s
    retries: 10         # SQL Server on hitaampi käynnistymään → enemmän yrityksiä
    start_period: 30s   # SQL Server tarvitsee enemmän aikaa
```

### ASP.NET Core health check -endpoint

ASP.NET Core -sovellukseen voi lisätä oman `/health`-endpointin, joka tarkistaa myös tietokantayhteyden:

#### 1. Lisää NuGet-paketit

```bash
# Perus health check (sisältyy ASP.NET Coreen)
dotnet add package Microsoft.Extensions.Diagnostics.HealthChecks

# Tietokantakohtaiset health checkit:
dotnet add package AspNetCore.HealthChecks.NpgSql      # PostgreSQL
dotnet add package AspNetCore.HealthChecks.SqlServer    # SQL Server
dotnet add package AspNetCore.HealthChecks.Redis        # Redis
```

#### 2. Konfiguroi Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// Lisää health check -- tarkistaa tietokantayhteyden
builder.Services.AddHealthChecks()
    .AddNpgSql(
        builder.Configuration.GetConnectionString("DefaultConnection")!,
        name: "postgresql",               // Health checkin nimi (näkyy logeissa)
        tags: new[] { "db", "postgresql" } // Tagit suodatusta varten
    );

var app = builder.Build();

// Rekisteröi /health-endpoint
app.MapHealthChecks("/health");
// GET /health → 200 OK (Healthy) tai 503 Service Unavailable (Unhealthy)

app.Run();
```

#### 3. Docker Compose health check API:lle

```yaml
services:
  api:
    healthcheck:
      # wget tarkistaa, vastaako /health-endpoint 200 OK
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:8080/health"]
      interval: 30s       # API:n health check harvemmin (ei kuormita)
      timeout: 10s
      retries: 3
      start_period: 15s   # Anna sovellukselle aikaa käynnistyä
```

### depends_on + health check = turvallinen käynnistysjärjestys

```yaml
services:
  api:
    depends_on:
      postgres:
        condition: service_healthy  # ← Avain! Odota HEALTHY-tilaa
```

```
Käynnistysjärjestys visualisoituna:

Aika:  0s          10s         20s         25s
       │           │           │           │
       ▼           ▼           ▼           ▼
DB:    [käynnistyy][alustuu...][pg_isready ✅] → HEALTHY
                                              │
API:                                          └──► [käynnistyy] → [yhdistää DB:hen ✅]
```

> **Vinkki:** Jos et käytä `condition: service_healthy`, API yrittää yhdistää tietokantaan heti kun kontti on käynnistetty -- joka johtaa `Connection refused` -virheeseen.

---

## Kehitysympäristön konfigurointi

### Hot Reload kontissa

Hot reload mahdollistaa koodimuutosten näkymisen automaattisesti ilman kontin uudelleenkäynnistystä.

#### docker-compose.override.yml (kehitys)

```yaml
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - DOTNET_USE_POLLING_FILE_WATCHER=true  # Tärkeä: tiedostomuutosten havaitseminen
    volumes:
      - ./:/src                               # Liitä lähdekoodi
    ports:
      - "8080:8080"
```

#### Dockerfile.dev (kehitysimage)

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0
WORKDIR /src

# Kopioi projekti ja palauta riippuvuudet
COPY *.csproj .
RUN dotnet restore

# Kopioi kaikki tiedostot
COPY . .

# Käytä dotnet watch hot reload -toimintoa
ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080
ENTRYPOINT ["dotnet", "watch", "run", "--no-launch-profile"]
```

> **Huom!** `DOTNET_USE_POLLING_FILE_WATCHER=true` on tärkeä Docker-ympäristössä, koska tiedostojärjestelmän inotify-ilmoitukset eivät aina toimi bind mountien kanssa.

### Kehitys vs. tuotanto

```bash
# Kehityksessä (override ladataan automaattisesti)
docker compose up -d

# Tuotannossa
docker compose -f docker-compose.yml up -d
```

---

## Täydellinen esimerkki: ASP.NET Core + PostgreSQL + pgAdmin

```yaml
# docker-compose.yml
services:
  # ASP.NET Core Web API
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=postgres;Port=5432;Database=${DB_NAME};Username=postgres;Password=${DB_PASSWORD}
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped

  # PostgreSQL tietokanta
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # pgAdmin - tietokannan hallintapaneeli
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    depends_on:
      - postgres
    restart: unless-stopped

volumes:
  postgres-data:
```

### .env

```
DB_NAME=myappdb
DB_PASSWORD=kehitys_salasana
```

### Käynnistys

```bash
# Käynnistä kaikki
docker compose up -d

# Palvelut:
# API:          http://localhost:8080
# pgAdmin:      http://localhost:5050
#   - Email:    admin@admin.com
#   - Password: admin
#   - Lisää palvelin: Host=postgres, Port=5432, Username=postgres

# Pysäytä
docker compose down

# Pysäytä ja poista tietokantadata
docker compose down -v
```

---

## EF Core -migraatiot Docker-ympäristössä

Tietokannan skeema (taulut, sarakkeet, indeksit) täytyy luoda ennen kuin sovellus voi käyttää sitä. EF Core -migraatiot hoitavat tämän automaattisesti.

### Vaihtoehto 1: Migraatio sovelluksen käynnistyessä (suositeltu kehityksessä)

```csharp
// Program.cs
var app = builder.Build();

// Aja migraatiot automaattisesti käynnistyessä
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.Migrate(); // Luo/päivittää taulut automaattisesti
}

app.Run();
```

**Edut:** Ei tarvitse muistaa ajaa migraatioita manuaalisesti.
**Haitat:** Tuotannossa usean instanssin kanssa voi aiheuttaa kilpailutilanteen (race condition). Tuotannossa käytä vaihtoehtoa 2.

### Vaihtoehto 2: Migraatio erillisellä komennolla (suositeltu tuotannossa)

```bash
# Aja migraatio käynnissä olevassa kontissa
docker compose exec api dotnet ef database update

# Tai luo väliaikainen kontti, aja migraatio ja poista kontti
docker compose run --rm api dotnet ef database update
#                  ^^^^ --rm poistaa kontin automaattisesti ajon jälkeen
```

### Vaihtoehto 3: EnsureCreated (vain testaukseen)

```csharp
// Luo tietokannan ja taulut ilman migraatioita -- EI migraatiohistoriaa!
db.Database.EnsureCreated();
```

> **Varoitus:** `EnsureCreated` ei käytä migraatioita eikä seuraa skeemamuutoksia. Käytä tätä vain yksikkötestien in-memory-tietokannoissa.

---

## Vianmääritys

### Yleisimmät ongelmat ja ratkaisut

| Ongelma | Tyypillinen virheilmoitus | Syy | Ratkaisu |
|---|---|---|---|
| API ei yhdistä tietokantaan | `Connection refused` | Tietokanta ei ole vielä valmis | Käytä `depends_on` + `condition: service_healthy` |
| Väärä hostname | `No such host is known` | Connection stringissä `Host=localhost` | Vaihda `Host=postgres` (palvelun nimi!) |
| SQL Server ei käynnisty | Kontti sammuaa heti | Heikko salasana | Vahva salasana: iso+pieni kirjain, numero, erikoismerkki, 8+ merkkiä |
| Hot reload ei toimi | Koodimuutokset eivät näy | Tiedostojärjestelmä ei havaitse muutoksia | Lisää `DOTNET_USE_POLLING_FILE_WATCHER=true` |
| Portti varattu | `Bind for 0.0.0.0:5432 failed: port is already allocated` | Toinen ohjelma käyttää porttia | Vaihda isäntäkoneen porttia: `"5433:5432"` |
| Data häviää | Tietokanta tyhjä restartin jälkeen | Named volume puuttuu | Lisää `volumes: - pgdata:/var/lib/postgresql/data` |
| Image ei päivity | Vanhat muutokset näkyvät | Docker käyttää vanhaa imagea cachesta | Käytä `docker compose up -d --build` |

### Vianmäärityspolku (step by step)

Kun jokin ei toimi, käy läpi nämä vaiheet järjestyksessä:

```bash
# 1. Ovatko kaikki palvelut käynnissä?
docker compose ps
# Tarkista State-sarake: "running", "exited", "restarting"...

# 2. Miksi palvelu ei käynnisty? Tarkista lokit!
docker compose logs api         # API:n lokit
docker compose logs postgres    # Tietokannan lokit
docker compose logs --tail 50   # Viimeiset 50 riviä kaikista

# 3. Onko health check OK?
docker compose ps
# Tarkista Health-sarake: "healthy", "unhealthy", "starting"

# 4. Toimiiko verkko? Testaa konttien välinen yhteys:
docker compose exec api sh -c "wget -qO- http://localhost:8080/health"

# 5. Onko ympäristömuuttujat oikein?
docker compose exec api printenv | sort
# Tarkista, että ConnectionStrings__... on oikein

# 6. Onko volume luotu?
docker volume ls

# 7. "Nuclear option" -- aloita puhtaalta pöydältä:
docker compose down -v          # Poista kontit JA volumet
docker compose up -d --build    # Rakenna ja käynnistä uudelleen
```

---

## Yhteenveto

| Konfiguraatio | Kuvaus |
|---|---|
| `depends_on` + `service_healthy` | Varmista käynnistysjärjestys |
| `ConnectionStrings__` | Connection string ympäristömuuttujana |
| Palvelun nimi = hostname | Konttien välinen DNS-resoluutio |
| Named volumes | Tietokantadatan pysyvyys |
| Health checkit | Palvelun valmiuden varmistaminen |
| `.env`-tiedosto | Salaisuuksien ja muuttujien hallinta |
| `docker-compose.override.yml` | Kehitysympäristön asetukset |

Takaisin: [Docker C#/.NET-kehityksessä](README.md) | [Docker-perusteet](https://github.com/xamk-mire/Xamk-wiki/tree/main/Development-guidelines/Docker)
