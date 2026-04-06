# Backend ja API

## Sisällysluettelo

1. [Mikä on backend?](#mikä-on-backend)
2. [Client-Server -malli](#client-server--malli)
3. [Mikä on API?](#mikä-on-api)
4. [Mikä on REST?](#mikä-on-rest)
5. [HTTP-metodit](#http-metodit)
6. [HTTP-statuskoodit](#http-statuskoodit)
7. [JSON - API:n tietomuoto](#json---apin-tietomuoto)
8. [HTTP-pyynnön ja vastauksen rakenne](#http-pyynnön-ja-vastauksen-rakenne)
9. [Yhteenveto](#yhteenveto)

---

## Mikä on backend?

**Backend** on sovelluksen "taustaosa" — se osa, jota käyttäjä ei näe suoraan. Backend käsittelee tietoa, tallentaa dataa tietokantaan ja toteuttaa sovelluksen logiikan.

Vertaa sitä ravintolaan:

```
┌──────────────────────────────────────────────────────┐
│                    RAVINTOLA                          │
├──────────────────┬───────────────────────────────────┤
│   SALI           │          KEITTIÖ                  │
│   (Frontend)     │          (Backend)                │
│                  │                                   │
│ - Asiakas näkee  │ - Asiakas ei näe                  │
│ - Ruokalista     │ - Ruoan valmistus                 │
│ - Tilaaminen     │ - Raaka-aineiden hallinta          │
│ - Ruoan syönti   │ - Reseptit (logiikka)             │
│                  │ - Varasto (tietokanta)             │
└──────────────────┴───────────────────────────────────┘
```

**Frontend** (esim. React-sovellus, mobiiliappi tai verkkosivu) on se, mitä käyttäjä näkee ja käyttää selaimessa. **Backend** on palvelin, joka vastaa frontendin pyyntöihin.

### Mitä backend tekee?

| Tehtävä | Esimerkki |
|---------|-----------|
| **Tiedon tallennus** | Käyttäjä rekisteröityy → backend tallentaa tiedot tietokantaan |
| **Tiedon haku** | Käyttäjä avaa tuotelistan → backend hakee tuotteet tietokannasta |
| **Logiikan suoritus** | Käyttäjä tekee tilauksen → backend tarkistaa varastosaldon ja laskee hinnan |
| **Tietoturva** | Backend tarkistaa, onko käyttäjällä oikeus nähdä tietoja |

---

## Client-Server -malli

Web-sovellukset toimivat **client-server -mallilla**:

```
┌──────────┐         HTTP-pyyntö          ┌──────────┐
│          │  ──────────────────────────►  │          │
│  Client  │                              │  Server  │
│ (Selain) │  ◄──────────────────────────  │(Backend) │
│          │         HTTP-vastaus          │          │
└──────────┘                              └──────────┘
```

1. **Client** (asiakas) lähettää **pyynnön** (request) palvelimelle
2. **Server** (palvelin) käsittelee pyynnön ja lähettää **vastauksen** (response) takaisin

Tämä on kuin posti: kirjoitat kirjeen (pyyntö), lähetät sen (HTTP), vastaanottaja lukee sen ja lähettää vastauksen takaisin.

### Käytännön esimerkki

Kun käyttäjä avaa verkkokaupan tuotesivun:

```
1. Selain (client) lähettää pyynnön:
   GET https://kauppa.fi/api/products

2. Backend (server) vastaanottaa pyynnön

3. Backend hakee tuotteet tietokannasta

4. Backend lähettää vastauksen:
   [
     { "id": 1, "name": "Kahvikuppi", "price": 12.99 },
     { "id": 2, "name": "Teepannu", "price": 24.50 }
   ]

5. Selain näyttää tuotteet käyttäjälle
```

---

## Mikä on API?

**API** (Application Programming Interface) on **rajapinta**, jonka kautta eri ohjelmat voivat kommunikoida keskenään. Se on kuin tarjoilija ravintolassa — välittää tietoa keittiön (backend) ja asiakkaan (client) välillä.

API määrittelee:
- **Mitä voi pyytää** (mitkä toiminnot ovat käytettävissä)
- **Miten pyydetään** (missä muodossa pyyntö lähetetään)
- **Mitä saa vastaukseksi** (missä muodossa tieto palautetaan)

### Web API

**Web API** on API, jota käytetään internetin (HTTP-protokollan) yli. Kun puhutaan backend-kehityksestä, tarkoitetaan lähes aina Web API:a.

```
┌─────────────┐     HTTP      ┌─────────────┐     Kysely     ┌─────────────┐
│   Frontend  │ ───────────►  │   Web API   │ ────────────►  │  Tietokanta │
│   (React)   │ ◄───────────  │  (Backend)  │ ◄────────────  │ (Database)  │
└─────────────┘     JSON      └─────────────┘     Data        └─────────────┘
```

### Miksi API:a tarvitaan?

- ✅ **Erottaa frontendin ja backendin** — molempia voi kehittää itsenäisesti
- ✅ **Sama backend, monta clientia** — web-sovellus, mobiiliappi ja kolmannen osapuolen sovellukset voivat kaikki käyttää samaa API:a
- ✅ **Selkeä sopimus** — kaikki tietävät miten dataa pyydetään ja palautetaan
- ✅ **Turvallisuus** — backend päättää mitä tietoja paljastetaan

---

## Mikä on REST?

**REST** (Representational State Transfer) on arkkitehtuurityyli, joka määrittelee miten Web API:t suunnitellaan. REST ei ole teknologia tai kirjasto — se on joukko periaatteita.

### REST:n perusperiaatteet

**1. Resurssit (Resources)**

Kaikki on **resursseja**, joilla on oma osoite (URL):

```
/api/products        ← Tuotteet (kokoelma)
/api/products/1      ← Yksittäinen tuote (id: 1)
/api/users           ← Käyttäjät (kokoelma)
/api/users/42        ← Yksittäinen käyttäjä (id: 42)
```

**2. HTTP-metodit kuvaavat toimintoa**

Sama URL, eri toiminto metodista riippuen:

```
GET    /api/products     ← Hae kaikki tuotteet
POST   /api/products     ← Luo uusi tuote
GET    /api/products/1   ← Hae tuote 1
PUT    /api/products/1   ← Päivitä tuote 1
DELETE /api/products/1   ← Poista tuote 1
```

**3. Tilattomuus (Stateless)**

Jokainen pyyntö on itsenäinen — palvelin ei muista aiempia pyyntöjä. Kaikki tarvittava tieto sisältyy jokaiseen pyyntöön.

**4. JSON-vastaukset**

Data lähetetään ja vastaanotetaan yleisimmin **JSON-muodossa** (JavaScript Object Notation).

---

## HTTP-metodit

HTTP-metodit kertovat palvelimelle, **mitä halutaan tehdä**. Neljä yleisintä:

| Metodi | Tarkoitus | Esimerkki | CRUD-operaatio |
|--------|-----------|-----------|----------------|
| **GET** | Hae tietoa | Hae kaikki tuotteet | **R**ead |
| **POST** | Luo uusi | Lisää uusi tuote | **C**reate |
| **PUT** | Päivitä olemassa oleva | Muuta tuotteen hintaa | **U**pdate |
| **DELETE** | Poista | Poista tuote | **D**elete |

### CRUD

**CRUD** tulee sanoista **C**reate, **R**ead, **U**pdate, **D**elete. Lähes kaikki API:t toteuttavat nämä neljä perusoperaatiota.

### Esimerkit

**GET** — Hae tietoa (ei muuta mitään palvelimella):

```http
GET /api/products HTTP/1.1
Host: localhost:5000
```

Vastaus:
```json
[
  { "id": 1, "name": "Kahvikuppi", "price": 12.99 },
  { "id": 2, "name": "Teepannu", "price": 24.50 }
]
```

**POST** — Luo uusi resurssi (lähettää dataa palvelimelle):

```http
POST /api/products HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "name": "Vesipullo",
  "price": 8.99
}
```

Vastaus:
```json
{
  "id": 3,
  "name": "Vesipullo",
  "price": 8.99
}
```

**PUT** — Päivitä olemassa oleva resurssi:

```http
PUT /api/products/3 HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "name": "Vesipullo",
  "price": 9.99
}
```

**DELETE** — Poista resurssi:

```http
DELETE /api/products/3 HTTP/1.1
Host: localhost:5000
```

---

## HTTP-statuskoodit

Kun palvelin vastaa pyyntöön, se palauttaa aina **statuskoodin**, joka kertoo miten pyyntö onnistui.

### Yleisimmät statuskoodit

| Koodi | Nimi | Merkitys | Milloin käytetään |
|-------|------|----------|-------------------|
| **200** | OK | Pyyntö onnistui | GET onnistui, PUT onnistui |
| **201** | Created | Uusi resurssi luotiin | POST onnistui |
| **204** | No Content | Onnistui, ei palautettavaa dataa | DELETE onnistui |
| **400** | Bad Request | Virheellinen pyyntö | Puuttuvat tai virheelliset tiedot |
| **404** | Not Found | Resurssia ei löytynyt | Haettiin tuotetta jota ei ole |
| **500** | Internal Server Error | Palvelinvirhe | Odottamaton virhe backendissä |

### Statuskoodien ryhmät

Statuskoodit on jaettu ryhmiin ensimmäisen numeron mukaan:

```
1xx — Informaatio (harvoin käytetty)
2xx — Onnistuminen  ✅
3xx — Uudelleenohjaus
4xx — Client-virhe  ❌ (pyytäjän vika)
5xx — Server-virhe  ❌ (palvelimen vika)
```

**Muistisääntö:** 2xx = kaikki hyvin, 4xx = sinun vikasi, 5xx = palvelimen vika.

### Käytännön esimerkki

```
GET  /api/products      → 200 OK (tuotteet löytyivät)
GET  /api/products/999  → 404 Not Found (tuotetta ei ole)
POST /api/products      → 201 Created (tuote luotiin)
POST /api/products      → 400 Bad Request (nimi puuttuu)
DELETE /api/products/1   → 204 No Content (tuote poistettiin)
```

---

## JSON - API:n tietomuoto

**JSON** (JavaScript Object Notation) on yleisin tietomuoto Web API:ssa. Se on ihmisen luettavissa ja koneen käsiteltävissä.

### JSON:n perussäännöt

```json
{
  "name": "Kahvikuppi",
  "price": 12.99,
  "inStock": true,
  "tags": ["keittiö", "juomat"],
  "manufacturer": {
    "name": "Mukit Oy",
    "country": "Finland"
  }
}
```

| Tyyppi | Esimerkki | C#-vastaavuus |
|--------|-----------|---------------|
| Teksti (string) | `"Kahvikuppi"` | `string` |
| Numero (number) | `12.99` | `int`, `double`, `decimal` |
| Totuusarvo (boolean) | `true` / `false` | `bool` |
| Lista (array) | `["a", "b"]` | `List<string>` |
| Objekti (object) | `{ "key": "value" }` | luokka (class) |
| Tyhjä (null) | `null` | `null` |

### JSON ja C# -luokat

ASP.NET Core muuntaa JSON:n automaattisesti C#-luokiksi (ja toisin päin). Tätä kutsutaan **serialisoinniksi** ja **deserialisoinniksi**.

```csharp
// C#-luokka
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
}
```

```json
// Sama tieto JSON-muodossa
{
  "id": 1,
  "name": "Kahvikuppi",
  "price": 12.99
}
```

ASP.NET Core tekee tämän muunnoksen automaattisesti — sinun ei tarvitse kirjoittaa sille koodia.

> 📖 Lisää JSON:sta: [JSON-perusteet](../../00-Basics/JSON.md)

---

## HTTP-pyynnön ja vastauksen rakenne

### HTTP-pyyntö (Request)

Jokaisessa HTTP-pyynnössä on:

```
┌─────────────────────────────────────────┐
│  HTTP-pyyntö                            │
├─────────────────────────────────────────┤
│  1. Metodi + URL                        │
│     POST /api/products HTTP/1.1         │
│                                         │
│  2. Headerit (otsikkotiedot)            │
│     Content-Type: application/json      │
│     Authorization: Bearer eyJhb...      │
│                                         │
│  3. Body (runko) - valinnainen          │
│     { "name": "Kahvikuppi" }            │
└─────────────────────────────────────────┘
```

- **Metodi + URL** — mitä tehdään ja mihin resurssiin
- **Headerit** — metatietoa pyynnöstä (tietomuoto, autentikointi, jne.)
- **Body** — lähetettävä data (POST, PUT ja PATCH -pyynnöissä)

### HTTP-vastaus (Response)

```
┌─────────────────────────────────────────┐
│  HTTP-vastaus                           │
├─────────────────────────────────────────┤
│  1. Statuskoodi                         │
│     HTTP/1.1 201 Created                │
│                                         │
│  2. Headerit                            │
│     Content-Type: application/json      │
│     Location: /api/products/3           │
│                                         │
│  3. Body (palautettu data)              │
│     { "id": 3, "name": "Kahvikuppi" }  │
└─────────────────────────────────────────┘
```

- **Statuskoodi** — onnistuiko pyyntö
- **Headerit** — metatietoa vastauksesta
- **Body** — palautettu data JSON-muodossa

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Backend** | Sovelluksen taustaosa, joka käsittelee logiikan ja datan |
| **API** | Rajapinta, jonka kautta ohjelmat kommunikoivat |
| **REST** | Periaatteet, joiden mukaan API suunnitellaan |
| **HTTP-metodi** | Kertoo mitä tehdään (GET, POST, PUT, DELETE) |
| **Statuskoodi** | Kertoo miten pyyntö onnistui (200, 201, 404...) |
| **JSON** | Tietomuoto, jolla data siirretään API:ssa |
| **CRUD** | Create, Read, Update, Delete — neljä perusoperaatiota |

### Seuraavaksi

Kun ymmärrät nämä peruskäsitteet, jatka seuraavaan materiaaliin:
- [Controllers](Controllers.md) — Miten ASP.NET Core käsittelee HTTP-pyyntöjä
