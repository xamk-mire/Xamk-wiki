# Docker-volumet ja -verkot

Kontit ovat oletuksena **lyhytikäisiä** (ephemeral) -- kun kontti poistetaan, kaikki sen sisällä oleva data häviää. Docker-volumet ratkaisevat tämän ongelman. Docker-verkot puolestaan mahdollistavat konttien välisen kommunikaation.

---

## Volumet (Volumes)

### Ongelma: Data häviää kontin mukana

Kuvittele tilanne: ajat PostgreSQL-tietokantaa Docker-kontissa, lisäät sinne tuhansia rivejä dataa, ja sitten päivität imagen uuteen versioon:

```bash
# 1. Käynnistä tietokanta (ILMAN volumea)
docker run -d --name db postgres:16-alpine

# 2. Lisää 1000 riviä dataa...
# 3. Pysäytä ja poista kontti
docker stop db && docker rm db

# 4. 💀 KAIKKI DATA ON HÄVINNYT!
# Kontin tiedostojärjestelmä poistettiin kontin mukana
```

```
Ilman volumea:                  Volumen kanssa:
┌──────────────┐               ┌──────────────┐
│    Kontti     │               │    Kontti     │
│  ┌────────┐  │               │  ┌────────┐  │
│  │  Data  │  │  docker rm    │  │  Data ──┼──┼──► Volume (isäntäkone)
│  └────────┘  │  ──────────►  │  └────────┘  │
│              │    💀 GONE     │              │    docker rm
└──────────────┘               └──────────────┘    ──────────►  ✅ DATA SÄILYY!
```

### Miksi volumeja tarvitaan?

| Käyttötarkoitus | Selitys | Esimerkki |
|---|---|---|
| **Datan pysyvyys** | Data säilyy kontin poiston jälkeen | Tietokantadata |
| **Datan jakaminen** | Useat kontit voivat käyttää samaa dataa | Jaetut logitiedostot |
| **Kehitystyö** | Koodimuutokset näkyvät kontissa reaaliajassa | Hot reload |
| **Konfiguraatio** | Ulkoiset asetustiedostot kontille | nginx.conf |
| **Varmuuskopiointi** | Data on isäntäkoneella, ei kontin sisällä | Tietokanta-backupit |

### Kolme tapaa liittää dataa

#### 1. Named Volumes (nimetyt volumet)

Docker hallinnoi volumea automaattisesti -- sinun ei tarvitse tietää missä data fyysisesti sijaitsee. Paras valinta **tuotantodatalle** (esim. tietokantadata).

```bash
# -v syntaksi: <volumen-nimi>:<polku-kontissa>
docker run -d --name db \
  -v my-data:/var/lib/postgresql/data \
  postgres:16-alpine

# ▲ "my-data" on volumen nimi
# ▲ "/var/lib/postgresql/data" on polku KONTIN sisällä, johon volume liitetään
```

**Miten se toimii?**

```
Isäntäkone (sinun tietokone)          Kontti
┌───────────────────────────┐        ┌───────────────────────┐
│ Docker hallinnoi:         │        │                       │
│ /var/lib/docker/volumes/  │◄──────►│ /var/lib/postgresql/  │
│   my-data/_data/          │ synk.  │   data/               │
│     PG_VERSION            │        │     PG_VERSION        │
│     base/                 │        │     base/             │
│     global/               │        │     global/           │
└───────────────────────────┘        └───────────────────────┘
       ▲                                    ▲
       │ Data säilyy täällä                 │ Kontti näkee datan täällä
       │ vaikka kontti poistetaan            │
```

```bash
# Volumen hallintakomennot
docker volume ls                    # Listaa kaikki volumet
docker volume create my-data        # Luo volume manuaalisesti
docker volume inspect my-data       # Näytä volumen tiedot (sijainti, luontiaika)
docker volume rm my-data            # Poista volume (data häviää!)
docker volume prune                 # Poista KAIKKI käyttämättömät volumet
```

Docker Compose -esimerkki:

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - db-data:/var/lib/postgresql/data   # Liitä nimetty volume

# TÄRKEÄ: Nimetyt volumet täytyy määritellä myös tiedoston lopussa
volumes:
  db-data:    # Ilman tätä Docker Compose ei tunnista volumea
```

#### 2. Bind Mounts (sidotut liitokset)

Liittää **isäntäkoneen kansion** suoraan konttiin. Muutokset näkyvät molempiin suuntiin reaaliajassa. Paras valinta **kehitystyöhön** (lähdekoodin liittäminen kontiin hot reloadia varten).

```
Isäntäkone                           Kontti
┌──────────────────────┐            ┌──────────────────────┐
│ ./src/               │            │ /app/src/            │
│   index.js ◄─ muokkaat tätä       │   index.js ◄─ kontti näkee muutoksen
│   utils.js           │ ◄────────► │   utils.js           │
│                      │  synk.     │                      │
└──────────────────────┘            └──────────────────────┘
```

```bash
# -v syntaksi: <isäntäkoneen-polku>:<polku-kontissa>
docker run -d --name web \
  -v $(pwd)/src:/app/src \
  -p 3000:3000 \
  node:20-alpine

# Windows PowerShell
docker run -d --name web `
  -v ${PWD}/src:/app/src `
  -p 3000:3000 `
  node:20-alpine
```

Docker Compose -esimerkki:

```yaml
services:
  web:
    build: .
    volumes:
      - ./src:/app/src          # Lähdekoodi (hot reload kehityksessä)
      - ./config:/app/config    # Konfiguraatiotiedostot
```

> **Vinkki:** Bind mount tunnistaa siitä, että polku alkaa `./`, `../` tai `/` -- se viittaa isäntäkoneen tiedostojärjestelmään. Named volume on pelkkä nimi ilman polkua (esim. `db-data:/var/lib/...`).

#### 3. tmpfs Mounts (väliaikainen muisti)

Data tallennetaan vain **muistiin (RAM)**. Häviää, kun kontti pysäytetään. Hyödyllinen väliaikaiselle datalle ja salaisuuksille, joita ei haluta tallentaa levylle.

```bash
docker run -d --name app \
  --tmpfs /app/temp \
  myapp:latest
```

> **Käyttökohteet:** Väliaikaiset tiedostot, istuntodata, salaisuudet joita ei saa tallentaa levylle.

### Vertailu

| Ominaisuus | Named Volume | Bind Mount | tmpfs |
|---|---|---|---|
| Sijainti | Docker hallinnoi | Isäntäkoneen polku | Muisti (RAM) |
| Pysyvyys | Kyllä | Kyllä | Ei |
| Suorituskyky | Hyvä | Vaihteleva | Erinomainen |
| Käyttökohde | Tuotantodata | Kehitys | Väliaikainen data |
| Jaettavissa | Kyllä | Kyllä | Ei |
| Varmuuskopiointi | Helppoa | Helppoa | Ei mahdollista |

### Read-only volumet

Voit liittää volumen vain-luku -tilassa:

```bash
docker run -d \
  -v ./config:/app/config:ro \
  myapp:latest
```

```yaml
services:
  web:
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
```

### Volumen varmuuskopiointi

```bash
# Varmuuskopioi volume tar-tiedostoon
docker run --rm \
  -v my-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz -C /data .

# Palauta varmuuskopio
docker run --rm \
  -v my-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /data
```

---

## Verkot (Networks)

### Miksi verkkoja tarvitaan?

Oletuksena Docker-kontit ovat **eristettyjä** -- ne eivät näe toisiaan. Mutta sovelluksesi tarvitsee usein yhteyttä muihin palveluihin: API puhuu tietokannalle, web-sovellus puhuu API:lle jne.

Docker-verkot ratkaisevat tämän: kontit **samassa verkossa** voivat kommunikoida keskenään ja löytävät toisensa **palvelun nimellä** (DNS), ilman IP-osoitteita.

```
Ilman Docker-verkkoa:              Docker-verkossa:
┌──────────┐  ┌──────────┐       ┌──────────────────────────┐
│   API    │  │    DB    │       │      my-network          │
│          │  │          │       │  ┌──────┐  ┌──────────┐  │
│ Ei tiedä │  │ Ei tiedä │       │  │ API  │──│ DB       │  │
│ DB:stä   │  │ API:sta  │       │  │      │  │          │  │
└──────────┘  └──────────┘       │  │Host= │  │ Port=    │  │
                                 │  │ "db" │  │  5432    │  │
                                 │  └──────┘  └──────────┘  │
                                 └──────────────────────────┘
```

### Docker-verkkojen perusteet

Docker luo oletuksena verkkoja, joiden avulla kontit voivat kommunikoida keskenään. Kontit samassa verkossa voivat löytää toisensa **palvelun nimellä** (DNS) -- ei tarvita IP-osoitteita.

### Verkkotyypit

#### 1. Bridge (silta) - Oletus

Oletusverkkotyyppi. Kontit samassa bridge-verkossa voivat kommunikoida keskenään.

```bash
# Luo bridge-verkko
docker network create my-network

# Käynnistä kontit samassa verkossa
docker run -d --name api --network my-network myapi:latest
docker run -d --name db --network my-network postgres:16-alpine

# Nyt "api"-kontti voi yhdistää tietokantaan nimellä "db"
# Connection string: Host=db;Port=5432;...
```

#### 2. Host

Kontti käyttää suoraan isäntäkoneen verkkoa. Ei porttimappausta - kontti kuuntelee suoraan isäntäkoneen portteja.

```bash
docker run -d --network host nginx
# Nginx on nyt suoraan portissa 80 isäntäkoneella
```

> **Huom!** Host-verkko toimii vain Linuxissa. Windowsissa ja macOS:ssä Docker Desktop käyttää virtuaalikonetta, joten host-verkko ei toimi samalla tavalla.

#### 3. None

Kontti on täysin eristetty verkosta. Ei verkkoyhteyttä.

```bash
docker run -d --network none myapp
```

### Verkkojen hallinta

```bash
# Listaa verkot
docker network ls

# Luo verkko
docker network create my-network

# Tarkastele verkon tietoja
docker network inspect my-network

# Liitä käynnissä oleva kontti verkkoon
docker network connect my-network my-container

# Poista kontti verkosta
docker network disconnect my-network my-container

# Poista verkko
docker network rm my-network

# Poista käyttämättömät verkot
docker network prune
```

### Verkot Docker Composessa

Docker Compose luo automaattisesti **oman verkon** kaikille palveluille. Palvelut löytävät toisensa palvelun nimellä.

```yaml
services:
  api:
    build: .
    ports:
      - "5000:5000"
    # "api"-kontti voi yhdistää "db"-konttiin nimellä "db"

  db:
    image: postgres:16-alpine
    # "db"-kontti on saavutettavissa nimellä "db"

# Docker Compose luo automaattisesti verkon: <projektinimi>_default
# Molemmat palvelut ovat tässä verkossa
```

#### Mukautetut verkot Composessa

Voit eristää palveluja eri verkkoihin:

```yaml
services:
  # Frontend pääsee vain API:in
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    networks:
      - frontend-network

  # API pääsee sekä frontendiin että tietokantaan
  api:
    build: ./api
    ports:
      - "5000:5000"
    networks:
      - frontend-network
      - backend-network

  # Tietokanta on eristetty - vain API pääsee siihen
  db:
    image: postgres:16-alpine
    networks:
      - backend-network

networks:
  frontend-network:
  backend-network:
```

```
┌─────────────────────────────────────────┐
│          frontend-network                │
│  ┌──────────┐       ┌──────────┐        │
│  │ Frontend │◄─────►│   API    │        │
│  └──────────┘       └─────┬────┘        │
│                           │              │
└───────────────────────────┼──────────────┘
                            │
┌───────────────────────────┼──────────────┐
│          backend-network  │              │
│                     ┌─────▼────┐         │
│                     │   API    │         │
│                     └─────┬────┘         │
│                           │              │
│                     ┌─────▼────┐         │
│                     │    DB    │         │
│                     └──────────┘         │
└──────────────────────────────────────────┘
```

---

## Konttien välinen kommunikaatio

### DNS-palvelunimillä (Docker Compose)

Docker Compose -ympäristössä palvelut löytävät toisensa automaattisesti palvelun nimellä. **Palvelun nimi = DNS-nimi verkossa.** Ei tarvita IP-osoitteita!

```yaml
services:
  api:
    environment:
      # "db" viittaa alla olevaan palveluun nimeltä "db"
      - ConnectionStrings__Default=Host=db;Port=5432;Database=mydb;Username=postgres;Password=secret
      # "cache" viittaa alla olevaan palveluun nimeltä "cache"
      - Redis__Connection=cache:6379

  db:              # ◄── Tämä palvelun nimi = DNS-nimi "db"
    image: postgres:16-alpine

  cache:           # ◄── Tämä palvelun nimi = DNS-nimi "cache"
    image: redis:alpine
```

```
Miten DNS-resoluutio toimii:

API-kontti haluaa yhdistää tietokantaan:
"Host=db;Port=5432"
       │
       ▼
Docker DNS: "db" → 172.18.0.3 (postgres-kontin IP)
       │
       ▼
Yhteys muodostetaan konttien välillä Docker-verkossa
```

> **Käytännössä:** Sinun ei koskaan tarvitse tietää konttien IP-osoitteita. Käytä aina palvelun nimeä (esim. `db`, `redis`, `api`).

### ports vs. expose

```yaml
services:
  api:
    ports:
      - "5000:5000"   # Avaa isäntäkoneelle JA Docker-verkolle
    expose:
      - "5000"         # Avaa VAIN Docker-verkolle (ei isäntäkoneelle)
```

```
                    ┌── ports ────────────────────────────────┐
                    │                                         │
Selain/Postman ────►│ localhost:5000 ──► api-kontti:5000     │
(isäntäkone)        │                                         │
                    └─────────────────────────────────────────┘

                    ┌── expose ──────────────────────────────┐
                    │                                         │
Selain/Postman  ✗   │ (ei pääsyä ulkoa)                      │
                    │                                         │
db-kontti ─────────►│ api:5000 ──► api-kontti:5000           │
(Docker-verkossa)   │                                         │
                    └─────────────────────────────────────────┘
```

| Asetus | Ulkoa (isäntäkone) | Docker-verkosta (muut kontit) | Käyttökohde |
|---|---|---|---|
| `ports` | ✅ Kyllä | ✅ Kyllä | API, web-sovellus |
| `expose` | ❌ Ei | ✅ Kyllä | Tietokanta (ei tarvitse ulkoista pääsyä) |
| Ei kumpaakaan | ❌ Ei | ✅ Kyllä (samassa verkossa) | Sisäiset palvelut |

> **Turvallisuusvinkki:** Tuotannossa tietokanta- ja cache-palvelut kannattaa jättää ilman `ports`-mappausta -- ne eivät tarvitse pääsyä ulkoa. Kehityksessä `ports` on kätevä, jotta voit yhdistää tietokantaan suoraan pgAdmin:lla tai muulla työkalulla.

---

## Käytännön esimerkki: Kolmen palvelun sovellus

```yaml
# docker-compose.yml
services:
  # Frontend (React)
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
    networks:
      - app-network

  # Backend API (.NET)
  api:
    build: ./api
    ports:
      - "5000:5000"
    environment:
      - ConnectionStrings__Default=Host=db;Database=mydb;Username=postgres;Password=${DB_PASSWORD}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - api-logs:/app/logs
    networks:
      - app-network

  # Tietokanta (PostgreSQL)
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: mydb
    volumes:
      - db-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

volumes:
  db-data:
  api-logs:

networks:
  app-network:
```

---

## Yhteenveto

### Volumet

| Tyyppi | Käyttökohde | Pysyvyys |
|---|---|---|
| **Named Volume** | Tuotantodata (tietokannat) | Kyllä |
| **Bind Mount** | Kehitystyö (lähdekoodi) | Kyllä |
| **tmpfs** | Väliaikainen/sensitiivinen data | Ei |

### Verkot

| Tyyppi | Kuvaus | Käyttökohde |
|---|---|---|
| **Bridge** | Eristetty verkko konteille | Yleisin, oletus |
| **Host** | Isäntäkoneen verkko | Suorituskyky (vain Linux) |
| **None** | Ei verkkoa | Täysi eristys |

### Tärkeimmät komennot

```bash
# Volumet
docker volume ls                    # Listaa volumet
docker volume create <nimi>         # Luo volume
docker volume inspect <nimi>        # Tarkastele volumea
docker volume rm <nimi>             # Poista volume
docker volume prune                 # Poista käyttämättömät

# Verkot
docker network ls                   # Listaa verkot
docker network create <nimi>        # Luo verkko
docker network inspect <nimi>       # Tarkastele verkkoa
docker network connect <verkko> <kontti>    # Liitä kontti
docker network disconnect <verkko> <kontti> # Poista kontti
```

Seuraavaksi: [Docker C#/.NET-kehityksessä](https://github.com/xamk-mire/Xamk-wiki/tree/main/C%23/fin/04-Advanced/Docker)
