# HTTP-metodit ja statuskoodit — Referenssi

Tämä dokumentti on kattava referenssi HTTP-metodeista ja statuskoodeista REST API -kehityksessä. Käytä tätä hakuteoksena kun tarvitset muistutuksen siitä, mitä metodia tai statuskoodia pitää käyttää tietyssä tilanteessa.

---

## Sisällysluettelo

1. [HTTP-metodit](#http-metodit)
2. [Milloin käyttää mitäkin metodia?](#milloin-käyttää-mitäkin-metodia)
3. [HTTP-statuskoodit](#http-statuskoodit)
4. [Milloin palauttaa mitäkin statuskoodia?](#milloin-palauttaa-mitäkin-statuskoodia)
5. [Metodit ja statuskoodit yhdessä](#metodit-ja-statuskoodit-yhdessä)
6. [ASP.NET Core -esimerkit](#aspnet-core--esimerkit)

---

## HTTP-metodit

HTTP-metodi kertoo palvelimelle **mitä operaatiota pyynnöllä halutaan tehdä**. Metodi on osa jokaista HTTP-pyyntöä.

### Kaikki REST API:ssa käytetyt metodit

| Metodi | CRUD | Tarkoitus | Onko body? | Idempotent? |
|--------|------|-----------|------------|-------------|
| **GET** | Read | Hae resurssi tai lista | Ei | Kyllä |
| **POST** | Create | Luo uusi resurssi | Kyllä | Ei |
| **PUT** | Update | Korvaa resurssi kokonaan | Kyllä | Kyllä |
| **PATCH** | Update | Päivitä resurssia osittain | Kyllä | Ei aina |
| **DELETE** | Delete | Poista resurssi | Ei (yleensä) | Kyllä |
| **HEAD** | - | Kuten GET, mutta ilman bodya | Ei | Kyllä |
| **OPTIONS** | - | Kysy mitä metodeja resurssi tukee | Ei | Kyllä |

> **Idempotent** tarkoittaa, että saman pyynnön voi lähettää useita kertoja ja lopputulos on sama. Esimerkiksi `DELETE /api/products/1` tuottaa aina saman lopputuloksen — tuote on poistettu — vaikka sen lähettäisi kymmenen kertaa.

---

## Milloin käyttää mitäkin metodia?

### GET — Hae tietoa

Käytä aina kun **luet** dataa ilman muutoksia palvelimella.

```
GET /api/products           → Hae kaikki tuotteet
GET /api/products/5         → Hae tuote ID:llä 5
GET /api/products?name=kuppi → Hae tuotteet hakusanalla
GET /api/users/42/orders    → Hae käyttäjän 42 tilaukset
```

Säännöt:
- Ei muuta palvelimen tilaa
- Ei pyyntörunkoa (body)
- Voidaan välimuistittaa (cacheable)
- Voidaan toistaa useita kertoja turvallisesti

### POST — Luo uusi resurssi

Käytä kun **luot uuden** resurssin tai lähetät dataa käsiteltäväksi.

```
POST /api/products          → Luo uusi tuote
POST /api/users             → Rekisteröi uusi käyttäjä
POST /api/auth/login        → Kirjautuminen (lähettää tunnukset)
POST /api/orders            → Luo uusi tilaus
```

Säännöt:
- Luo uuden resurssin tai käynnistää toiminnon
- Pyyntörunko (body) sisältää luotavan resurssin tiedot JSON-muodossa
- Palautetaan yleensä **201 Created** ja luotu resurssi
- Ei idempotent — sama pyyntö kahdesti luo kaksi resurssia

### PUT — Päivitä resurssi kokonaan

Käytä kun **korvaat** olemassa olevan resurssin tiedot kokonaan uusilla.

```
PUT /api/products/5         → Korvaa tuote 5 täysin uusilla tiedoilla
PUT /api/users/42           → Korvaa käyttäjä 42 tiedot
```

Säännöt:
- URL sisältää resurssin ID:n
- Body sisältää **kaikki** resurssin kentät, myös muuttumattomat
- Jos resurssia ei löydy, voidaan palauttaa 404 tai luoda uusi (riippuu toteutuksesta)
- Idempotent — saman pyynnön voi toistaa turvallisesti

**PUT vs PATCH:**

```
// PUT: Lähetä kaikki kentät
PUT /api/products/5
{
  "name": "Uusi nimi",
  "price": 15.99,       // pakollinen, vaikka ei muutu
  "description": "..."  // pakollinen, vaikka ei muutu
}

// PATCH: Lähetä vain muuttuvat kentät
PATCH /api/products/5
{
  "price": 15.99        // vain hinta muuttuu
}
```

### PATCH — Päivitä resurssia osittain

Käytä kun **muutat vain osan** resurssin kentistä.

```
PATCH /api/products/5       → Muuta vain tuotteen hintaa
PATCH /api/users/42         → Muuta vain käyttäjän sähköpostia
```

Säännöt:
- Body sisältää **vain muuttuvat** kentät
- Tehokkaampi kuin PUT, kun muutetaan vain osa tiedoista
- Käytetään harvemmin kuin PUT — monissa yksinkertaisissa API:issa käytetään PUT kaikkeen päivittämiseen

### DELETE — Poista resurssi

Käytä kun **poistat** resurssin.

```
DELETE /api/products/5      → Poista tuote 5
DELETE /api/users/42        → Poista käyttäjä 42
DELETE /api/orders/99       → Poista tilaus 99
```

Säännöt:
- URL sisältää poistettavan resurssin ID:n
- Ei yleensä pyyntörunkoa (body)
- Palautetaan yleensä **204 No Content** (ei palauteta poistettua dataa)
- Idempotent — tuote 5 on poistettu riippumatta siitä, lähetetäänkö pyyntö kerran vai kymmenen kertaa

### HEAD — Tarkista resurssin olemassaolo

Toimii kuten GET, mutta palvelin palauttaa vain headerit ilman bodya. Käytetään tarkistamaan onko resurssi olemassa ilman datan lataamista.

```
HEAD /api/products/5        → Tarkista onko tuote 5 olemassa
```

Käyttökohteet:
- Tarkista onko resurssi muuttunut (ehto `Last-Modified`)
- Tarkista tiedostokoko ennen latausta (`Content-Length`)

### OPTIONS — Kysy tuettuja metodeja

Palvelin palauttaa mitä HTTP-metodeja kyseinen URL tukee. Selaimet käyttävät tätä automaattisesti CORS-tarkistukseen.

```
OPTIONS /api/products       → Vastaus: Allow: GET, POST, OPTIONS
```

---

## HTTP-statuskoodit

Jokaisessa HTTP-vastauksessa on **statuskoodi**, joka kertoo miten pyyntö onnistui. Koodi on kolminumeroinen luku.

### 2xx — Onnistuminen

| Koodi | Nimi | Milloin käytetään |
|-------|------|-------------------|
| **200** | OK | Pyyntö onnistui ja data palautetaan. Yleisin vastaus GET- ja PUT-pyynnöille. |
| **201** | Created | Uusi resurssi luotiin onnistuneesti. Käytetään POST-vastauksissa. |
| **202** | Accepted | Pyyntö vastaanotettu, mutta käsittely ei ole vielä valmis (asynkroninen toiminto). |
| **204** | No Content | Pyyntö onnistui, mutta ei ole mitään palautettavaa. Käytetään DELETE-vastauksissa. |

### 3xx — Uudelleenohjaus

| Koodi | Nimi | Milloin käytetään |
|-------|------|-------------------|
| **301** | Moved Permanently | Resurssi on siirretty pysyvästi uuteen osoitteeseen. |
| **302** | Found | Resurssi löytyy tilapäisesti eri osoitteesta. |
| **304** | Not Modified | Resurssi ei ole muuttunut sitten viimeisen haun (cache on ajantasainen). |

### 4xx — Client-virheet

> Nämä tarkoittavat, että **pyyntö on virheellinen** — ongelma on pyytävässä osapuolessa (client).

| Koodi | Nimi | Milloin käytetään |
|-------|------|-------------------|
| **400** | Bad Request | Pyyntö on muodoltaan virheellinen. Puuttuvat pakolliset kentät, väärä tietotyyppi, validointivirhe. |
| **401** | Unauthorized | Käyttäjä ei ole kirjautunut sisään. Pyyntö vaatii autentikoinnin (esim. JWT-token puuttuu tai on vanhentunut). |
| **403** | Forbidden | Käyttäjä on kirjautunut, mutta hänellä ei ole oikeutta tähän toimintoon. |
| **404** | Not Found | Pyydettua resurssia ei löydy. Tuotetta, käyttäjää tai muuta resurssia ei ole olemassa. |
| **405** | Method Not Allowed | HTTP-metodi ei ole sallittu tälle reitille (esim. DELETE ei ole toteutettu). |
| **409** | Conflict | Pyyntö on ristiriidassa resurssin nykyisen tilan kanssa. Esim. yritetään luoda käyttäjä jo olemassa olevalla sähköpostilla. |
| **410** | Gone | Resurssi on poistettu pysyvästi eikä sitä enää ole. |
| **415** | Unsupported Media Type | Pyynnön `Content-Type` ei ole tuettu. Esim. lähetettiin XML kun odotettiin JSON. |
| **422** | Unprocessable Entity | Pyyntö on muodoltaan oikein, mutta data on semanttisesti virheellistä. |
| **429** | Too Many Requests | Client lähettää liian monta pyyntöä liian nopeasti (rate limiting). |

### 5xx — Server-virheet

> Nämä tarkoittavat, että **palvelin epäonnistui** — ongelma on backendissä, ei clientissä.

| Koodi | Nimi | Milloin käytetään |
|-------|------|-------------------|
| **500** | Internal Server Error | Odottamaton virhe palvelimella. Yleinen "jotain meni pieleen" -vastaus. |
| **501** | Not Implemented | Toimintoa ei ole toteutettu. |
| **502** | Bad Gateway | Välityspalvelin sai virheellisen vastauksen. |
| **503** | Service Unavailable | Palvelin ei pysty käsittelemään pyyntöjä juuri nyt (ylikuormitus tai huolto). |
| **504** | Gateway Timeout | Välityspalvelin ei saanut vastausta ajoissa. |

---

## 401 vs 403 — Yleinen sekaannus

Näiden kahden ero on tärkeä:

```
401 Unauthorized  = "Kuka olet? Kirjaudu sisään ensin."
403 Forbidden     = "Tiedän kuka olet, mutta sinulla ei ole lupaa tähän."
```

**Esimerkkejä:**

```
// Käyttäjä ei ole kirjautunut sisään
GET /api/orders                    → 401 Unauthorized
// Header: WWW-Authenticate: Bearer

// Käyttäjä on kirjautunut, mutta yrittää päästä admin-sivulle
GET /api/admin/users               → 403 Forbidden

// Käyttäjä yrittää lukea toisen käyttäjän yksityisiä tietoja
GET /api/users/99/private-data     → 403 Forbidden
```

---

## Milloin palauttaa mitäkin statuskoodia?

### GET-pyyntöihin

```
GET /api/products           → 200 OK  (lista, vaikka tyhjä [])
GET /api/products/5         → 200 OK  (tuote löytyi)
GET /api/products/999       → 404 Not Found  (tuotetta ei ole)
GET /api/orders             → 401 Unauthorized  (ei kirjautunut)
GET /api/admin/stats        → 403 Forbidden  (ei admin-oikeuksia)
```

### POST-pyyntöihin

```
POST /api/products          → 201 Created  (tuote luotiin)
POST /api/products          → 400 Bad Request  (nimi puuttuu)
POST /api/users             → 409 Conflict  (sähköposti on jo käytössä)
POST /api/auth/login        → 200 OK  (kirjautuminen onnistui, palautetaan token)
POST /api/auth/login        → 401 Unauthorized  (väärä salasana)
```

### PUT/PATCH-pyyntöihin

```
PUT /api/products/5         → 200 OK  (päivitetty tuote palautetaan)
PUT /api/products/5         → 400 Bad Request  (virheellinen data)
PUT /api/products/999       → 404 Not Found  (tuotetta ei ole)
PATCH /api/products/5       → 200 OK  (osittain päivitetty tuote)
```

### DELETE-pyyntöihin

```
DELETE /api/products/5      → 204 No Content  (poistettu, ei palautettavaa dataa)
DELETE /api/products/999    → 404 Not Found  (tuotetta ei ole)
DELETE /api/products/5      → 403 Forbidden  (ei oikeutta poistaa)
```

---

## Metodit ja statuskoodit yhdessä

Tässä kattava yhteenvetotaulukko yleisimmistä yhdistelmistä:

| Operaatio | Metodi | URL | Onnistuminen | Epäonnistuminen |
|-----------|--------|-----|--------------|-----------------|
| Hae lista | GET | `/api/products` | 200 | 401, 403 |
| Hae yksi | GET | `/api/products/5` | 200 | 404, 401, 403 |
| Luo uusi | POST | `/api/products` | 201 | 400, 401, 403, 409 |
| Korvaa | PUT | `/api/products/5` | 200 | 400, 404, 401, 403 |
| Päivitä osittain | PATCH | `/api/products/5` | 200 | 400, 404, 401, 403 |
| Poista | DELETE | `/api/products/5` | 204 | 404, 401, 403 |
| Kirjaudu | POST | `/api/auth/login` | 200 | 400, 401 |

---

## ASP.NET Core -esimerkit

Tässä esimerkkejä siitä, miten eri statuskoodit palautetaan ASP.NET Core -controllerissa:

```csharp
// 200 OK
return Ok(product);

// 201 Created — palautetaan myös Location-header
return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);

// 202 Accepted — asynkroninen käsittely käynnistetty
return Accepted();

// 204 No Content
return NoContent();

// 400 Bad Request — valinnainen virheilmoitus
return BadRequest();
return BadRequest("Tuotteen nimi on pakollinen.");
return BadRequest(new { Error = "Hinta ei voi olla negatiivinen." });

// 401 Unauthorized — lisätään WWW-Authenticate header
return Unauthorized();

// 403 Forbidden
return Forbid();

// 404 Not Found
return NotFound();
return NotFound($"Tuotetta ID:llä {id} ei löydy.");

// 405 Method Not Allowed
return StatusCode(405);

// 409 Conflict
return Conflict("Sähköpostiosoite on jo käytössä.");

// 422 Unprocessable Entity
return UnprocessableEntity("Päivämäärä on menneisyydessä.");

// 429 Too Many Requests
return StatusCode(429);

// 500 Internal Server Error — ei yleensä palauteta manuaalisesti
return StatusCode(500, "Odottamaton virhe.");
```

### Esimerkki: kattava controller-metodi

```csharp
[HttpPost]
public IActionResult Create(Product product)
{
    // 400 — puuttuvat tiedot (hoidetaan automaattisesti [ApiController]-attribuutilla)
    // mutta voit lisätä omaa validointia:
    if (product.Price < 0)
        return BadRequest("Hinta ei voi olla negatiivinen.");

    // 409 — nimi on jo olemassa
    if (_products.Any(p => p.Name == product.Name))
        return Conflict($"Tuote nimellä '{product.Name}' on jo olemassa.");

    product.Id = _nextId++;
    _products.Add(product);

    // 201 — luotiin onnistuneesti
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}

[HttpGet("{id}")]
public IActionResult GetById(int id)
{
    var product = _products.FirstOrDefault(p => p.Id == id);

    // 404 — ei löydy
    if (product == null)
        return NotFound($"Tuotetta ID:llä {id} ei löydy.");

    // 200 — löytyi
    return Ok(product);
}
```

---

## Ulkoiset linkit

- [HTTP Status Codes (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [HTTP Request Methods (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods)
- [HTTP Status Codes — pikaopas](https://httpstatuses.io/)
- [REST API -suunnitteluperiaatteet (Microsoft)](https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design)
