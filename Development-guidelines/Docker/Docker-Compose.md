# Docker Compose

Docker Compose on työkalu usean Docker-kontin sovellusten määrittelyyn ja ajamiseen. Sen avulla voit kuvata koko sovelluksen infrastruktuurin yhdessä YAML-tiedostossa ja hallita kaikkia kontteja yhdellä komennolla.

## Ongelma: Usean palvelun hallinta

Kuvittele tyypillinen web-sovellus, joka tarvitsee:
- ASP.NET Core API
- PostgreSQL-tietokanta
- Redis-välimuisti
- Seq-lokipalvelin

Ilman Docker Composea joutuisit ajamaan jokaisen palvelun erikseen:

```bash
# 😫 Ilman Docker Composea -- 4 erillistä komentoa, joissa kymmeniä parametreja:
docker network create myapp-network

docker run -d --name postgres --network myapp-network \
  -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data \
  postgres:16-alpine

docker run -d --name redis --network myapp-network redis:alpine

docker run -d --name seq --network myapp-network \
  -e ACCEPT_EULA=Y -p 5341:80 datalust/seq

docker run -d --name api --network myapp-network \
  -p 8080:8080 -e "ConnectionStrings__Default=Host=postgres;..." \
  --depends-on postgres myapp:latest
```

```bash
# ✅ Docker Composella -- yksi komento:
docker compose up -d
```

Kaikki konfiguraatio on yhdessä `docker-compose.yml`-tiedostossa, ja koko ympäristö käynnistetään tai sammutetaan yhdellä komennolla.

## Miksi Docker Compose?

| Hyöty | Selitys |
|---|---|
| **Yksi komento** | `docker compose up -d` käynnistää kaiken |
| **Infrastruktuuri koodina** | `docker-compose.yml` on versioitavissa gitissä |
| **Automaattiset verkot** | Palvelut löytävät toisensa nimellä (DNS) -- ei IP-osoitteita |
| **Toistettavuus** | Jokainen kehittäjä saa identtisen ympäristön |
| **Helppo siivous** | `docker compose down` poistaa kaiken kerralla |
| **Ympäristömuuttujat** | `.env`-tiedosto keskitetysti kaikille palveluille |

---

## docker-compose.yml -rakenne

```yaml
# docker-compose.yml

services:
  # Palvelu 1: Web-sovellus
  web:
    image: nginx:alpine
    ports:
      - "8080:80"

  # Palvelu 2: Tietokanta
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: salasana
```

### Perusrakenne

```yaml
services:       # Palveluiden määrittely (pakolllinen)
  palvelu1:
    ...
  palvelu2:
    ...

volumes:        # Nimetyt volumet (valinnainen)
  ...

networks:       # Mukautetut verkot (valinnainen)
  ...
```

---

## Palvelun konfiguraatio

### image - Valmiin imagen käyttö

```yaml
services:
  db:
    image: postgres:16-alpine
```

### build - Imagen rakentaminen Dockerfilestä

```yaml
services:
  web:
    build: .                  # Dockerfile samassa kansiossa

  # Tarkempi konfiguraatio
  api:
    build:
      context: ./backend      # Build-konteksti (kansio)
      dockerfile: Dockerfile   # Dockerfile-tiedoston nimi
      args:                    # Build-argumentit
        BUILD_CONFIGURATION: Release
```

### ports - Porttimappaukset

```yaml
services:
  web:
    ports:
      - "8080:80"          # isäntä:kontti
      - "443:443"
      - "127.0.0.1:3000:3000"  # Vain localhost
```

### volumes - Datan liittäminen

```yaml
services:
  db:
    volumes:
      - db-data:/var/lib/postgresql/data    # Nimetty volume
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # Bind mount

  web:
    volumes:
      - ./src:/app/src        # Bind mount (kehitys, hot reload)

volumes:
  db-data:                    # Nimetyn volumen määrittely
```

### environment - Ympäristömuuttujat

```yaml
services:
  api:
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=db;Database=mydb;Username=postgres;Password=salasana

    # Tai map-muodossa
    environment:
      ASPNETCORE_ENVIRONMENT: Development
      DB_HOST: db
```

### env_file - Ympäristömuuttujat tiedostosta

```yaml
services:
  api:
    env_file:
      - .env              # Lataa .env-tiedostosta
      - .env.local         # Lataa toinen tiedosto
```

`.env`-tiedosto:
```
DB_HOST=db
DB_PASSWORD=salasana
DB_NAME=mydb
```

> **Huom!** Älä tallenna `.env`-tiedostoja, jotka sisältävät salaisuuksia, versionhallintaan. Lisää `.env` `.gitignore`-tiedostoon.

### depends_on - Palveluiden riippuvuudet

`depends_on` määrittää, missä järjestyksessä palvelut käynnistetään. Tämä on tärkeää, koska esim. API ei voi yhdistää tietokantaan, jos tietokanta ei ole vielä käynnissä.

```yaml
services:
  api:
    # Yksinkertainen: "käynnistä db ennen api:a"
    depends_on:
      - db

    # Parempi: "odota, että db on OIKEASTI valmis vastaanottamaan yhteyksiä"
    depends_on:
      db:
        condition: service_healthy  # Vaatii healthcheck-määrityksen db-palvelulle
```

> **Tärkeä ero:** Pelkkä `depends_on: - db` varmistaa vain, että tietokontakontti on **käynnistetty** -- ei sitä, että tietokanta on **valmis** vastaanottamaan yhteyksiä. Tietokannan käynnistyminen kestää tyypillisesti 5-30 sekuntia. Käytä aina `condition: service_healthy` yhdessä healthcheckin kanssa.

### restart - Uudelleenkäynnistyskäytäntö

Mitä tapahtuu, jos kontti kaatuu? `restart`-asetus määrittää, yrittääkö Docker käynnistää sen uudelleen automaattisesti.

```yaml
services:
  api:
    restart: unless-stopped
```

| Vaihtoehto | Toiminta | Käyttökohde |
|---|---|---|
| `"no"` | Ei uudelleenkäynnistystä (oletus) | Kertaluontoiset tehtävät |
| `on-failure` | Uudelleen vain virheen sattuessa (exit code ≠ 0) | Kehitys |
| `always` | Aina uudelleen, myös Docker-uudelleenkäynnistyksen jälkeen | Tuotanto |
| `unless-stopped` | Kuten `always`, mutta ei jos pysäytetty manuaalisesti | Suositeltu yleisin |

### healthcheck - Terveystarkistus

Healthcheck kertoo Dockerille, miten tarkistaa onko palvelu **oikeasti toimintakunnossa** (ei vain käynnissä).

```yaml
services:
  db:
    image: postgres:16-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]  # Komento, joka tarkistaa terveyden
      interval: 10s      # Kuinka usein tarkistetaan
      timeout: 5s        # Kuinka kauan odotetaan vastausta
      retries: 5         # Montako epäonnistumista ennen "unhealthy"-tilaa
      start_period: 30s  # Anna palvelulle aikaa käynnistyä ennen tarkistuksia
```

```
Healthcheck-kulku:
                          start_period (30s)
┌─────────────────────────────────────────────────────────────────┐
│ Kontti käynnistyy... tietokanta alustuu... taulut luodaan...   │
└─────────────────────────────────────────────────────────────────┘
                 │
                 ▼
    ┌─── interval (10s) ───┐
    │                      │
    ▼                      ▼
 pg_isready?            pg_isready?          pg_isready?
    ❌ (retries: 1/5)      ❌ (retries: 2/5)    ✅ → HEALTHY!
```

### networks - Verkkomääritykset

```yaml
services:
  api:
    networks:
      - frontend
      - backend

  db:
    networks:
      - backend            # Vain backend-verkossa

networks:
  frontend:
  backend:
```

---

## Ympäristömuuttujat

### .env-tiedosto Compose-muuttujille

Docker Compose lukee automaattisesti `.env`-tiedoston samasta kansiosta:

```
# .env (Docker Compose -muuttujat)
POSTGRES_VERSION=16
APP_PORT=8080
```

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:${POSTGRES_VERSION}-alpine
  web:
    ports:
      - "${APP_PORT}:80"
```

### Muuttujien prioriteetti

1. Komentorivillä asetetut muuttujat (`docker compose run -e VAR=arvo`)
2. `environment`-osio `docker-compose.yml`:ssä
3. `env_file`-tiedostot
4. Dockerfilen `ENV`-instruktio

---

## Mitä `docker compose up` tekee taustalla?

Kun suoritat `docker compose up -d`, Docker Compose tekee seuraavat asiat automaattisesti:

```
docker compose up -d
        │
        ▼
1. Lue docker-compose.yml ja .env-tiedostot
        │
        ▼
2. Luo verkko: <projektinimi>_default
   (kaikki palvelut samassa verkossa, löytävät toisensa nimellä)
        │
        ▼
3. Luo nimetyt volumet (esim. db-data)
        │
        ▼
4. Käynnistä palvelut oikeassa järjestyksessä (depends_on):
   4a. postgres käynnistyy ──► healthcheck alkaa
   4b. Odota healthcheck ✅
   4c. api käynnistyy (tietokanta on valmis!)
        │
        ▼
5. Kaikki palvelut käynnissä taustalla ✅
```

> **DNS-palvelunnimet:** Docker Compose asettaa jokaiselle palvelulle DNS-nimen, joka on sama kuin palvelun nimi YAML-tiedostossa. Jos palvelu on nimeltään `postgres`, muut palvelut voivat yhdistää siihen hostnamella `postgres` -- ei tarvita IP-osoitteita!

---

## Peruskomennot

### Käynnistys ja sammutus

```bash
# Käynnistä kaikki palvelut taustalle
docker compose up -d

# Käynnistä ja rakenna imaget uudelleen
docker compose up -d --build

# Käynnistä yksittäinen palvelu
docker compose up -d api

# Pysäytä ja poista kontit
docker compose down

# Pysäytä, poista kontit JA volumet (tietokannan data häviää!)
docker compose down -v

# Pysäytä, poista kontit ja imaget
docker compose down --rmi all
```

### Tarkastelu

```bash
# Listaa palvelut ja niiden tila
docker compose ps

# Näytä lokeja
docker compose logs

# Seuraa lokeja reaaliajassa
docker compose logs -f

# Yksittäisen palvelun lokit
docker compose logs -f api

# Näytä resurssien käyttö
docker compose top
```

### Hallinta

```bash
# Suorita komento palvelussa
docker compose exec api bash

# Käynnistä palvelu uudelleen
docker compose restart api

# Pysäytä palvelu
docker compose stop api

# Rakenna imaget (ilman käynnistystä)
docker compose build

# Vedä imaget rekisteristä
docker compose pull

# Skaalaa palvelua (esim. 3 instanssia)
docker compose up -d --scale api=3
```

---

## Käytännön esimerkki: Web + tietokanta

Tässä esimerkissä käynnistetään Node.js-sovellus ja PostgreSQL-tietokanta:

### Kansiorakenne

```
my-project/
├── docker-compose.yml
├── .env
├── Dockerfile
├── package.json
└── src/
    └── index.js
```

### docker-compose.yml

```yaml
services:
  # Web-sovellus
  web:
    build: .
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:${DB_PASSWORD}@db:5432/${DB_NAME}
      - NODE_ENV=development
    volumes:
      - ./src:/app/src          # Hot reload kehityksessä
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  # PostgreSQL-tietokanta
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - db-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

volumes:
  db-data:
```

### .env

```
APP_PORT=3000
DB_PASSWORD=kehitys_salasana
DB_NAME=myapp
```

### Käynnistys

```bash
# Käynnistä kaikki
docker compose up -d

# Tarkista tila
docker compose ps

# Seuraa lokeja
docker compose logs -f

# Pysäytä
docker compose down
```

---

## Usean Compose-tiedoston käyttö

Voit jakaa konfiguraation useaan tiedostoon, esim. kehitys- ja tuotantoasetuksiin:

### docker-compose.yml (perus)

```yaml
services:
  api:
    build: .
    ports:
      - "5000:5000"
```

### docker-compose.override.yml (kehitys, ladataan automaattisesti)

```yaml
services:
  api:
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
    volumes:
      - ./src:/app/src
```

### docker-compose.prod.yml (tuotanto)

```yaml
services:
  api:
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
    restart: always
```

```bash
# Kehityksessä (käyttää automaattisesti docker-compose.yml + docker-compose.override.yml)
docker compose up -d

# Tuotannossa (ohita override, käytä prod-tiedostoa)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Yhteenveto

| Komento | Kuvaus |
|---|---|
| `docker compose up -d` | Käynnistä palvelut taustalle |
| `docker compose up -d --build` | Käynnistä ja rakenna uudelleen |
| `docker compose down` | Pysäytä ja poista kontit |
| `docker compose down -v` | Pysäytä ja poista kontit + volumet |
| `docker compose ps` | Listaa palvelut |
| `docker compose logs -f` | Seuraa lokeja |
| `docker compose exec <palvelu> bash` | Avaa shell palveluun |
| `docker compose restart <palvelu>` | Käynnistä palvelu uudelleen |
| `docker compose build` | Rakenna imaget |

Seuraavaksi: [Volumet ja Verkot](Volumet-ja-Verkot.md)
