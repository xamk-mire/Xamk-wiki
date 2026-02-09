# Docker-perusteet

## Mikä on Docker?

Docker on avoimen lähdekoodin alusta, joka mahdollistaa sovellusten pakkaamisen, jakelun ja ajamisen **konteissa** (containers). Kontit ovat kevyitä, eristettyjä ympäristöjä, jotka sisältävät kaiken sovelluksen tarvitseman: koodin, ajonaikaiset kirjastot, järjestelmätyökalut ja asetukset.

### Ongelma: "Toimii minun koneellani"

Olet ehkä kokenut tilanteen, jossa:
- Sovellus toimii sinun koneellasi, mutta ei kaverin koneella
- Asennat projektin ja saat virheen: "vaatii Node.js 18" -- sinulla on versio 20
- Tietokanta on eri versiota kehityksessä ja tuotannossa
- Projekti vaatii 5 eri palvelua (tietokanta, cache, viestijono...) ja jokainen pitää asentaa erikseen

Docker ratkaisee nämä ongelmat **pakkaamalla sovelluksen ja kaiken sen tarvitseman yhteen pakettiin**, joka toimii identtisesti kaikkialla.

### Analogia: Rahtikontti

Docker on saanut nimensä rahtikonteista. Ennen konttien keksimistä jokainen lasti pakattiin eri tavalla, ja satamissa tarvittiin erilaisia laitteita eri lastimuodoille. Rahtikontti standardisoi kuljetuksen -- sisällä voi olla mitä tahansa, mutta ulkopuolelta kontti on aina samankokoinen ja käsitellään samalla tavalla.

Docker tekee saman ohjelmistoille: **sisällä voi olla mikä tahansa sovellus**, mutta ulkopuolelta kaikki kontit käynnistetään, pysäytetään ja hallitaan samalla tavalla.

### Miksi Docker?

- **Yhdenmukainen ympäristö** - Sovellus toimii samalla tavalla kehittäjän koneella, CI/CD-palvelimella ja tuotannossa
- **Nopea käyttöönotto** - Sovellukset käynnistyvät sekunneissa (ei minuuteissa kuten virtuaalikoneet)
- **Eristys** - Sovellukset eivät häiritse toisiaan -- voit ajaa Node.js 18 ja Node.js 20 -sovelluksia rinnakkain
- **Skaalautuvuus** - Helppoa lisätä tai poistaa kontteja kuorman mukaan
- **Versionhallinta** - Docker-imaget ovat versioituja, voit palata aiempaan versioon hetkessä
- **Helppo kehitysympäristö** - Uusi kehittäjä saa ympäristön pystyyn yhdellä komennolla

### Kontit vs. virtuaalikoneet

| Ominaisuus | Kontti (Docker) | Virtuaalikone |
|---|---|---|
| Käynnistysaika | Sekunteja | Minuutteja |
| Koko | Megatavuja | Gigatavuja |
| Käyttöjärjestelmä | Jakaa isäntä-OS:n ytimen | Oma täysi OS |
| Suorituskyky | Lähes natiivi | Overhead virtualisoinnista |
| Eristys | Prosessitason eristys | Täysi laitteistotason eristys |
| Resurssien käyttö | Vähäinen | Merkittävä |

```
Virtuaalikoneet:                    Kontit (Docker):
┌─────────┐ ┌─────────┐           ┌─────────┐ ┌─────────┐
│ Sovellus│ │ Sovellus│           │ Sovellus│ │ Sovellus│
├─────────┤ ├─────────┤           ├─────────┤ ├─────────┤
│ Kirjast.│ │ Kirjast.│           │ Kirjast.│ │ Kirjast.│
├─────────┤ ├─────────┤           └────┬────┘ └────┬────┘
│ Vieras  │ │ Vieras  │                │           │
│ OS      │ │ OS      │           ┌────┴───────────┴────┐
├─────────┤ ├─────────┤           │   Docker Engine      │
└────┬────┘ └────┬────┘           ├────────────────────-─┤
┌────┴───────────┴────┐           │   Isäntä-OS          │
│   Hypervisor        │           ├──────────────────────┤
├─────────────────────┤           │   Laitteisto          │
│   Isäntä-OS         │           └──────────────────────┘
├─────────────────────┤
│   Laitteisto         │
└─────────────────────┘
```

---

## Dockerin asennus

### Windows

1. Lataa [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Suorita asennusohjelma
3. Varmista, että **WSL 2** (Windows Subsystem for Linux) on käytössä
4. Käynnistä Docker Desktop
5. Testaa asennus:

```bash
docker --version
docker run hello-world
```

### Linux (Ubuntu/Debian)

```bash
# Päivitä paketit
sudo apt update

# Asenna tarvittavat paketit
sudo apt install ca-certificates curl gnupg

# Lisää Dockerin GPG-avain
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Lisää Docker-repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Asenna Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Testaa asennus
sudo docker run hello-world
```

### macOS

1. Lataa [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
2. Avaa `.dmg`-tiedosto ja vedä Docker Applications-kansioon
3. Käynnistä Docker Desktop
4. Testaa asennus:

```bash
docker --version
docker run hello-world
```

---

## Docker-arkkitehtuuri

Docker käyttää asiakas-palvelin -arkkitehtuuria:

```
┌──────────────────────────────────────────────┐
│                Docker Client (CLI)            │
│  docker build, docker pull, docker run, ...   │
└──────────────┬───────────────────────────────┘
               │ REST API
┌──────────────▼───────────────────────────────┐
│              Docker Daemon (dockerd)           │
│  Hallinnoi imageja, kontteja, verkkoja, ...    │
├───────────┬──────────────┬───────────────────┤
│  Images   │  Containers  │  Networks/Volumes  │
└───────────┴──────────────┴───────────────────┘
               │
┌──────────────▼───────────────────────────────┐
│            Docker Registry (Docker Hub)        │
│  Imagejen tallennus ja jakelu                  │
└──────────────────────────────────────────────┘
```

- **Docker Client (CLI)** - Käyttäjän rajapinta Dockeriin. Komennot kuten `docker run` lähetetään daemonille.
- **Docker Daemon (dockerd)** - Taustaprosessi, joka hallinnoi kontteja, imageja, verkkoja ja volumeja.
- **Docker Registry** - Imagejen tallennus- ja jakelupaikka. Docker Hub on oletusrekisteri.

---

## Keskeiset käsitteet

### Image (kuva) ja Container (kontti)

Nämä kaksi käsitettä ovat Dockerin ydin. Niiden ero on tärkeää ymmärtää:

**Image** on kuin **luokka (class)** olio-ohjelmoinnissa:
- Lukuoikeus (read-only) -malli, joka sisältää kaiken sovelluksen tarvitseman
- Koostuu kerroksista (layers) -- jokainen Dockerfilen rivi luo yhden kerroksen
- Ei ole itsessään käynnissä -- se on "ohje" kontin luomiseen
- Ladataan registrystä (Docker Hub) tai rakennetaan Dockerfilestä

**Container** on kuin **olio (object)** -- instanssi imagesta:
- Ajettava instanssi imagesta -- kuin `new MyClass()` olio-ohjelmoinnissa
- Eristetty prosessi isäntäkoneella (oma tiedostojärjestelmä, verkko, prosessit)
- Voidaan käynnistää, pysäyttää, poistaa ja luoda uudelleen
- **Muutokset kontin sisällä häviävät**, kun kontti poistetaan (ellei käytetä volumeja)
- Samasta imagesta voi luoda monta konttia (kuten samasta luokasta monta oliota)

```
Image:                        Kontit:
┌─────────────────┐          ┌─────────────────┐
│  nginx:alpine   │──────────│  web-1 (running)│
│  (read-only)    │          └─────────────────┘
│                 │          ┌─────────────────┐
│  Kaikki         │──────────│  web-2 (running)│
│  tarvittava     │          └─────────────────┘
│  sisällä        │          ┌─────────────────┐
│                 │──────────│  web-3 (stopped)│
└─────────────────┘          └─────────────────┘
 "Luokka"                    "Oliot"
```

```bash
# IMAGE-komennot:
docker images            # Listaa paikalliset imaget
docker pull nginx        # Lataa image Docker Hubista
docker rmi nginx         # Poista image

# CONTAINER-komennot:
docker run nginx         # Luo ja käynnistä kontti imagesta
docker run -d nginx      # Käynnistä taustalla (-d = detached)
docker ps                # Listaa käynnissä olevat kontit
docker ps -a             # Listaa kaikki kontit (myös pysäytetyt)
```

### Registry (rekisteri)

Registry on **imagejen tallennus- ja jakelupaikka** -- kuten GitHub on koodille, Docker Registry on Docker-imagille.

- **Docker Hub** ([hub.docker.com](https://hub.docker.com)) on julkinen oletusrekisteri, josta löydät tuhansia valmiita imageja (nginx, postgres, node, dotnet...)
- Voi käyttää myös yksityisiä rekisterejä (esim. Azure Container Registry, GitHub Container Registry, AWS ECR)
- Kun kirjoitat `docker pull nginx`, Docker lataa imagen Docker Hubista

### Volume (volyymi)

- Mekanismi **datan säilyttämiseen** kontin elinkaaren yli
- Ilman volumeja kaikki kontin sisälle tallennettu data häviää kontin poistossa
- Erityisen tärkeä tietokannoille -- et halua menettää kaikkea dataa kontin uudelleenkäynnistyksessä!
- Katso lisää: [Volumet ja Verkot](Volumet-ja-Verkot.md)

### Network (verkko)

- Mahdollistaa **konttien välisen kommunikaation** -- esim. API-kontti puhuu tietokantakontille
- Docker luo automaattisesti verkon, jossa kontit löytävät toisensa nimellä (DNS)
- Katso lisää: [Volumet ja Verkot](Volumet-ja-Verkot.md)

---

## Peruskomennot

### Mitä `docker run` tekee taustalla?

Kun kirjoitat `docker run nginx`, Docker tekee seuraavat asiat:

```
docker run nginx
       │
       ▼
1. Onko image "nginx" paikallisesti?
       │
   Ei ──► docker pull nginx (lataa Docker Hubista)
       │
       ▼
2. Luo uusi kontti imagesta (docker create)
       │
       ▼
3. Luo kontin tiedostojärjestelmä (kirjoituskerros imagen päälle)
       │
       ▼
4. Luo verkkoliitäntä kontille (IP-osoite Docker-verkossa)
       │
       ▼
5. Käynnistä kontin prosessi (docker start)
       │
       ▼
6. Suorita CMD/ENTRYPOINT -komento (esim. nginx -g "daemon off;")
```

### Konttien hallinta

```bash
# Luo ja käynnistä kontti imagesta
docker run <image>

# Luo ja käynnistä kontti taustalle, nimeä se ja avaa portti
docker run -d --name myapp -p 8080:80 nginx
# -d         = taustalla (detached), terminaali vapautuu käyttöön
# --name     = kontin nimi (muuten Docker antaa satunnaisen nimen)
# -p 8080:80 = porttimappaus (isäntä:kontti)
#              isäntäkoneen portti 8080 → kontin portti 80
```

> **Porttimappaus selitettynä:** Kontti on eristetty -- sen portit eivät näy isäntäkoneelle ilman `-p`-lippua. `-p 8080:80` tarkoittaa: "kun joku menee osoitteeseen `localhost:8080`, ohjaa liikenne kontin porttiin 80".

```bash
# Listaa käynnissä olevat kontit
docker ps

# Listaa kaikki kontit (myös pysäytetyt)
docker ps -a

# Pysäytä kontti (lähettää SIGTERM-signaalin, odottaa 10s, sitten SIGKILL)
docker stop <kontin-nimi-tai-id>

# Käynnistä pysäytetty kontti uudelleen
docker start <kontin-nimi-tai-id>

# Käynnistä kontti uudelleen (stop + start)
docker restart <kontin-nimi-tai-id>

# Poista kontti (kontin tulee olla pysäytettynä)
docker rm <kontin-nimi-tai-id>

# Poista käynnissä oleva kontti pakotetusti
docker rm -f <kontin-nimi-tai-id>

# Poista kaikki pysäytetyt kontit kerralla
docker container prune
```

### Imagejen hallinta

```bash
# Listaa paikalliset imaget (koko, tagi, luontiaika)
docker images

# Lataa image rekisteristä
docker pull <image>:<tag>
# Esim: docker pull postgres:16-alpine

# Rakenna image Dockerfilestä
docker build -t <nimi>:<tag> .
# -t = tagi (nimi:versio)
# .  = build-konteksti (nykyinen kansio)

# Poista image
docker rmi <image>

# Poista käyttämättömät imaget (jotka eivät liity mihinkään konttiin)
docker image prune
```

### Kontin tarkastelu ja debuggaus

```bash
# Näytä kontin lokit (stdout/stderr)
docker logs <kontin-nimi-tai-id>

# Seuraa lokeja reaaliajassa (kuin tail -f)
docker logs -f <kontin-nimi-tai-id>

# Näytä viimeiset 100 lokiriviä ja seuraa
docker logs -f --tail 100 <kontin-nimi-tai-id>

# Avaa interaktiivinen shell käynnissä olevaan konttiin
docker exec -it <kontin-nimi-tai-id> bash
# -i = interaktiivinen (stdin auki)
# -t = pseudo-TTY (terminaalinäkymä)
# Huom: Alpine-imagessa käytä sh (ei bash)

# Suorita yksittäinen komento kontissa
docker exec <kontin-nimi-tai-id> ls /app

# Tarkastele kontin yksityiskohtia (verkko, volumet, env-muuttujat...)
docker inspect <kontin-nimi-tai-id>

# Näytä kaikkien konttien resurssien käyttö reaaliajassa (CPU, muisti, verkko)
docker stats
```

### Järjestelmän hallinta

```bash
# Näytä Dockerin levytilan käyttö (imaget, kontit, volumet, cache)
docker system df

# Siivoa käyttämättömät resurssit (pysäytetyt kontit, käyttämättömät verkot, dangling imaget)
docker system prune

# Siivoa kaikki, mukaan lukien käyttämättömät imaget (vapauttaa paljon tilaa!)
docker system prune -a

# Yksittäisten resurssien siivous
docker container prune    # Poista pysäytetyt kontit
docker image prune -a     # Poista käyttämättömät imaget
docker volume prune       # Poista käyttämättömät volumet
docker network prune      # Poista käyttämättömät verkot
```

---

## Kontin elinkaari

```
docker create        docker start         docker stop
    │                    │                     │
    ▼                    ▼                     ▼
┌────────┐         ┌──────────┐          ┌──────────┐
│ Created │────────▶│ Running  │─────────▶│ Stopped  │
└────────┘         └──────────┘          └──────────┘
                        │                     │
                        │ docker pause        │ docker start
                        ▼                     │
                   ┌──────────┐               │
                   │ Paused   │               │
                   └──────────┘               │
                                              │
                                    docker rm │
                                              ▼
                                        ┌──────────┐
                                        │ Removed  │
                                        └──────────┘
```

> **Huom!** `docker run` = `docker create` + `docker start` yhdistettynä.

---

## Käytännön esimerkki 1: Nginx-webpalvelin

Käynnistetään Nginx-webpalvelin Docker-kontissa -- nolla asennuksia tarvitaan:

```bash
# 1. Käynnistä Nginx-kontti (lataa imagen automaattisesti jos ei ole paikallisesti)
docker run -d --name my-nginx -p 8080:80 nginx

# 2. Avaa selaimessa: http://localhost:8080
# Näet Nginx-oletussivun -- toimii ilman Nginx-asennusta!

# 3. Tarkastele lokeja -- näet HTTP-pyynnöt
docker logs my-nginx

# 4. Mene kontin sisään ja tutki
docker exec -it my-nginx bash
# Olet nyt kontin sisällä! Kokeile:
#   ls /usr/share/nginx/html/   # Nginx-tiedostot
#   cat /etc/nginx/nginx.conf   # Nginx-konfiguraatio
#   exit                         # Poistu kontista

# 5. Pysäytä kontti
docker stop my-nginx

# 6. Poista kontti
docker rm my-nginx
```

## Käytännön esimerkki 2: PostgreSQL-tietokanta

Käynnistä tietokanta yhdellä komennolla -- ei asennusta, ei konfigurointia:

```bash
# 1. Käynnistä PostgreSQL-tietokanta
docker run -d \
  --name my-postgres \
  -e POSTGRES_PASSWORD=salasana123 \
  -e POSTGRES_DB=testdb \
  -p 5432:5432 \
  postgres:16-alpine

# 2. Yhdistä tietokantaan kontin sisältä
docker exec -it my-postgres psql -U postgres -d testdb

# 3. Kokeile SQL-kyselyä:
#   SELECT version();
#   CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);
#   INSERT INTO test (name) VALUES ('Docker on helppoa!');
#   SELECT * FROM test;
#   \q    -- poistu

# 4. Pysäytä ja poista
docker stop my-postgres && docker rm my-postgres
```

> **Huomaa:** Koska emme käyttäneet volumea, tietokantadata häviää kontin poiston yhteydessä. Tuotannossa käytetään aina volumeja -- katso [Volumet ja Verkot](Volumet-ja-Verkot.md).

---

## Yhteenveto

| Käsite | Kuvaus | Analogia |
|---|---|---|
| **Image** | Read-only malli, josta kontit luodaan | Luokka (class) |
| **Container** | Ajettava instanssi imagesta | Olio (object) |
| **Registry** | Imagejen tallennus- ja jakelupaikka | GitHub koodille |
| **Volume** | Datan säilytys kontin elinkaaren yli | Ulkoinen kiintolevy |
| **Network** | Konttien välinen kommunikaatio | Lähiverkko |
| **Dockerfile** | Ohje imagen rakentamiseen | Makefile / resepti |
| **Docker Compose** | Usean kontin sovellusten hallinta | Orkestrointi |

### Seuraavat askeleet

| Aihe | Kuvaus |
|---|---|
| [Dockerfile](Dockerfile.md) | Opi rakentamaan omia imageja |
| [Docker Compose](Docker-Compose.md) | Opi hallitsemaan useita kontteja |
| [Volumet ja Verkot](Volumet-ja-Verkot.md) | Opi datan säilytys ja konttien välinen kommunikaatio |

Seuraavaksi: [Dockerfile](Dockerfile.md)
