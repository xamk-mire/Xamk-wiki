# Controllers — ASP.NET Core -kontrollerit

## Sisällysluettelo

1. [Mikä on controller?](#mikä-on-controller)
2. [ASP.NET Core Web API -projektin rakenne](#aspnet-core-web-api--projektin-rakenne)
3. [Controllerin anatomia](#controllerin-anatomia)
4. [Reititys (Routing)](#reititys-routing)
5. [HTTP-metodiattribuutit](#http-metodiattribuutit)
6. [Parametrien vastaanottaminen](#parametrien-vastaanottaminen)
7. [Paluuarvot ja statuskoodit](#paluuarvot-ja-statuskoodit)
8. [Model-luokat](#model-luokat)
9. [Koko esimerkki: ProductsController](#koko-esimerkki-productscontroller)
10. [Yhteenveto](#yhteenveto)

---

## Mikä on controller?

**Controller** (kontrolleri) on luokka, joka **vastaanottaa HTTP-pyyntöjä ja palauttaa vastauksia**. Se on ikään kuin vastaanottovirkailija — ottaa vastaan asiakkaan pyynnön, käsittelee sen ja antaa vastauksen.

```
HTTP-pyyntö                    Controller                     Vastaus
────────────►  GET /api/products  ────►  ProductsController  ────►  200 OK + JSON
```

Jokaisella controllerilla on yksi tai useampi **toimintometodi** (action method), joka vastaa tietynlaiseen pyyntöön:

```csharp
public class ProductsController : ControllerBase
{
    [HttpGet]          // GET /api/products
    public IActionResult GetAll() { ... }

    [HttpGet("{id}")]  // GET /api/products/5
    public IActionResult GetById(int id) { ... }

    [HttpPost]         // POST /api/products
    public IActionResult Create(Product product) { ... }
}
```

### Controller vs. Minimal API

ASP.NET Coressa on kaksi tapaa rakentaa API:

| | Controllers | Minimal API |
|---|-------------|-------------|
| **Rakenne** | Luokkapohjainen | Funktiopohjainen |
| **Tiedostot** | Omat luokat `Controllers/`-kansiossa | Kaikki `Program.cs`:ssä |
| **Soveltuu** | Isommat projektit, selkeä rakenne | Pienet projektit, nopea prototypointi |
| **Oppiminen** | Enemmän opittavaa, mutta selkeämpi | Helpompi aloittaa |

Tässä materiaalissa keskitymme **controller-pohjaiseen** lähestymistapaan, koska se on yleisin tapa rakentaa tuotantotason API:ta.

---

## ASP.NET Core Web API -projektin rakenne

Kun luot uuden Web API -projektin komennolla `dotnet new webapi --use-controllers`, saat seuraavan rakenteen:

```
MyApi/
├── Controllers/
│   └── WeatherForecastController.cs   ← Esimerkkicontroller
├── Properties/
│   └── launchSettings.json            ← Käynnistysasetukset (portit, Swagger)
├── appsettings.json                   ← Sovelluksen asetukset
├── appsettings.Development.json       ← Kehitysympäristön asetukset
├── MyApi.csproj                       ← Projektitiedosto (riippuvuudet)
├── MyApi.http                         ← HTTP-pyyntötiedosto testausta varten
└── Program.cs                         ← Sovelluksen käynnistys ja konfigurointi
```

### Program.cs — sovelluksen sydän

`Program.cs` konfiguroi ja käynnistää sovelluksen:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Palveluiden rekisteröinti (dependency injection)
builder.Services.AddControllers();
builder.Services.AddOpenApi();

var app = builder.Build();

// Middlewaret (pyyntöputki)
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();
app.UseAuthorization();

// Yhdistä controllerit reitteihin
app.MapControllers();

app.Run();
```

> **Huom:** `Program.cs` -pohja voi vaihdella .NET-version mukaan. Esimerkiksi vanhemmissa versioissa Swagger/OpenAPI rekisteröidään `AddSwaggerGen()`/`UseSwagger()`-kutsuilla.

Tärkeimmät rivit:
- `AddControllers()` — rekisteröi kaikki controller-luokat
- `MapControllers()` — yhdistää controllerien reitit HTTP-pyyntöihin

---

## Controllerin anatomia

Controller-luokalla on neljä tärkeää osaa:

```csharp
// 1. Attribuutit — kertovat ASP.NET Corelle miten tätä luokkaa käytetään
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase  // 2. Perintä ControllerBase:sta
{
    // 3. Kenttä tietovarastolle
    private static readonly List<Product> _products = new();

    // 4. Toimintometodit (action methods)
    [HttpGet]
    public IActionResult GetAll()
    {
        return Ok(_products);
    }
}
```

### 1. `[ApiController]` -attribuutti

Kertoo ASP.NET Corelle, että tämä on API-kontrolleri. Se aktivoi:
- **Automaattisen model-validoinnin** — jos data on virheellinen, palautetaan 400 Bad Request ilman omaa koodia
- **Automaattisen `[FromBody]`-päättelyn** — POST/PUT-pyynnön body luetaan automaattisesti
- **Paremmat virhevastaukset** — virheviestit ovat standardimuotoisia

### 2. `ControllerBase`

Controller perii `ControllerBase`-luokan, joka tarjoaa valmiit apumetodit vastausten luomiseen:

| Metodi | Statuskoodi | Käyttö |
|--------|-------------|--------|
| `Ok(data)` | 200 | Palauta data onnistuneesti |
| `CreatedAtAction(...)` | 201 | Uusi resurssi luotiin |
| `NoContent()` | 204 | Onnistui, ei palautettavaa dataa |
| `BadRequest(...)` | 400 | Virheellinen pyyntö |
| `NotFound()` | 404 | Resurssia ei löytynyt |

### 3. `[Route("api/[controller]")]` -attribuutti

Määrittää controllerin **perusreitin** (base route). `[controller]` korvataan automaattisesti luokan nimellä ilman "Controller"-päätettä:

```
ProductsController  →  api/products
UsersController     →  api/users
OrdersController    →  api/orders
```

---

## Reititys (Routing)

**Reititys** tarkoittaa sitä, miten ASP.NET Core päättelee mikä controller ja metodi käsittelee tietyn HTTP-pyynnön.

### Attribute Routing

ASP.NET Core Web API käyttää **attribuuttireitistystä** — reitit määritellään attribuuteilla suoraan controlleriin:

```csharp
[ApiController]
[Route("api/[controller]")]          // Perusreitti: api/products
public class ProductsController : ControllerBase
{
    [HttpGet]                         // GET api/products
    public IActionResult GetAll() { ... }

    [HttpGet("{id}")]                 // GET api/products/5
    public IActionResult GetById(int id) { ... }

    [HttpGet("search")]              // GET api/products/search?name=kahvi
    public IActionResult Search([FromQuery] string name) { ... }
}
```

### Reitin muodostuminen

Lopullinen reitti = `[Route]` + `[HttpMethod]`:

```
[Route("api/[controller]")] = "api/products"

[HttpGet]          → GET  api/products
[HttpGet("{id}")]  → GET  api/products/{id}
[HttpGet("search")]→ GET  api/products/search
[HttpPost]         → POST api/products
```

### Route-parametrit

`{id}` on **route-parametri** — se täytetään URL:sta:

```csharp
[HttpGet("{id}")]
public IActionResult GetById(int id)  // id tulee URL:sta
{
    // GET api/products/5  →  id = 5
    // GET api/products/42 →  id = 42
}
```

---

## HTTP-metodiattribuutit

Jokaiselle HTTP-metodille on oma attribuutti:

| Attribuutti | HTTP-metodi | Käyttö |
|-------------|-------------|--------|
| `[HttpGet]` | GET | Hae tietoa |
| `[HttpPost]` | POST | Luo uusi resurssi |
| `[HttpPut]` | PUT | Päivitä olemassa oleva |
| `[HttpDelete]` | DELETE | Poista resurssi |
| `[HttpPatch]` | PATCH | Päivitä osittain |

Näitä käytetään toimintometodien (action method) yläpuolella:

```csharp
[HttpGet]        // Vastaa GET-pyyntöihin
public IActionResult GetAll() { ... }

[HttpPost]       // Vastaa POST-pyyntöihin
public IActionResult Create([FromBody] Product product) { ... }

[HttpPut("{id}")]    // Vastaa PUT-pyyntöihin osoitteessa api/products/{id}
public IActionResult Update(int id, [FromBody] Product product) { ... }

[HttpDelete("{id}")] // Vastaa DELETE-pyyntöihin osoitteessa api/products/{id}
public IActionResult Delete(int id) { ... }
```

> 📖 Lisää attribuuteista: [Attribuutit - Teoria](../Attributes.md) ja [Attribuutit - Esimerkit](../Attributes-Examples.md)

---

## Parametrien vastaanottaminen

Controller voi vastaanottaa dataa useasta eri paikasta:

### 1. Route-parametrit `[FromRoute]`

Data tulee URL-polusta. Tämä on oletusarvo route-parametreille, joten `[FromRoute]`-attribuuttia ei tarvitse kirjoittaa erikseen:

```csharp
[HttpGet("{id}")]
public IActionResult GetById(int id)  // [FromRoute] on automaattinen
{
    // GET api/products/5  →  id = 5
}
```

### 2. Query-parametrit `[FromQuery]`

Data tulee URL:n query string -osasta (`?key=value`):

```csharp
[HttpGet("search")]
public IActionResult Search([FromQuery] string name, [FromQuery] decimal? minPrice)
{
    // GET api/products/search?name=kahvi&minPrice=10
    // name = "kahvi", minPrice = 10
}
```

### 3. Body `[FromBody]`

Data tulee pyynnön rungosta (body) JSON-muodossa. `[ApiController]`-attribuutin ansiosta `[FromBody]` on automaattinen monimutkaisille tyypeille:

```csharp
[HttpPost]
public IActionResult Create(Product product)  // [FromBody] on automaattinen
{
    // POST api/products
    // Body: { "name": "Kahvikuppi", "price": 12.99 }
    // product.Name = "Kahvikuppi", product.Price = 12.99
}
```

### Yhteenveto parametrien lähteistä

| Lähde | Attribuutti | Esimerkki URL |
|-------|-------------|---------------|
| URL-polku | `[FromRoute]` (automaattinen) | `/api/products/5` |
| Query string | `[FromQuery]` | `/api/products?name=kahvi` |
| Pyynnön body | `[FromBody]` (automaattinen) | POST + JSON body |

---

## Paluuarvot ja statuskoodit

Controller-metodit palauttavat `IActionResult`-tyyppisen arvon, joka sisältää sekä **statuskoodin** että mahdollisen **datan**:

```csharp
[HttpGet]
public IActionResult GetAll()
{
    return Ok(_products);           // 200 OK + tuotelista JSON:na
}

[HttpGet("{id}")]
public IActionResult GetById(int id)
{
    var product = _products.FirstOrDefault(p => p.Id == id);

    if (product == null)
        return NotFound();          // 404 Not Found

    return Ok(product);             // 200 OK + tuote JSON:na
}

[HttpPost]
public IActionResult Create(Product product)
{
    _products.Add(product);

    return CreatedAtAction(         // 201 Created + Location-header
        nameof(GetById),
        new { id = product.Id },
        product
    );
}

[HttpDelete("{id}")]
public IActionResult Delete(int id)
{
    var product = _products.FirstOrDefault(p => p.Id == id);

    if (product == null)
        return NotFound();          // 404 Not Found

    _products.Remove(product);
    return NoContent();             // 204 No Content
}
```

### Paluuarvojen valinta

| Tilanne | Metodi | Statuskoodi |
|---------|--------|-------------|
| Data haettu onnistuneesti | `Ok(data)` | 200 |
| Uusi resurssi luotu | `CreatedAtAction(...)` | 201 |
| Toiminto onnistui, ei dataa | `NoContent()` | 204 |
| Virheellinen syöte | `BadRequest("viesti")` | 400 |
| Resurssia ei löydy | `NotFound()` | 404 |

---

## Model-luokat

**Model** (malli) on C#-luokka, joka kuvaa datan rakennetta. ASP.NET Core muuntaa modelit automaattisesti JSON:ksi (ja JSON:n modeliksi).

```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }  // Valinnainen kenttä (nullable)
}
```

### Model ja JSON -vastaavuus

```
C#-property     ←→     JSON-kenttä
─────────────────────────────────────
Id              ←→     "id"
Name            ←→     "name"
Price           ←→     "price"
Description     ←→     "description"
```

ASP.NET Core käyttää oletuksena **camelCase**-muotoilua JSON:ssa (`Name` → `"name"`).

### Models-kansio

Mallit sijoitetaan tyypillisesti omaan `Models/`-kansioon:

```
MyApi/
├── Controllers/
│   └── ProductsController.cs
├── Models/
│   └── Product.cs              ← Model-luokka
├── Program.cs
└── ...
```

---

## Koko esimerkki: ProductsController

Tässä on täydellinen esimerkki controllerista, joka toteuttaa kaikki CRUD-operaatiot:

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private static readonly List<Product> _products = new()
    {
        new Product { Id = 1, Name = "Kahvikuppi", Price = 12.99m },
        new Product { Id = 2, Name = "Teepannu", Price = 24.50m }
    };

    private static int _nextId = 3;

    [HttpGet]
    public IActionResult GetAll()
    {
        return Ok(_products);
    }

    [HttpGet("{id}")]
    public IActionResult GetById(int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        if (product == null) return NotFound();
        return Ok(product);
    }

    [HttpPost]
    public IActionResult Create(Product product)
    {
        product.Id = _nextId++;
        _products.Add(product);

        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }

    [HttpPut("{id}")]
    public IActionResult Update(int id, Product product)
    {
        var existing = _products.FirstOrDefault(p => p.Id == id);
        if (existing == null) return NotFound();

        existing.Name = product.Name;
        existing.Price = product.Price;
        existing.Description = product.Description;

        return Ok(existing);
    }

    [HttpDelete("{id}")]
    public IActionResult Delete(int id)
    {
        var product = _products.FirstOrDefault(p => p.Id == id);
        if (product == null) return NotFound();

        _products.Remove(product);
        return NoContent();
    }
}
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Controller** | Luokka joka käsittelee HTTP-pyyntöjä |
| **`[ApiController]`** | Aktivoi API-toiminnot (automaattinen validointi, `[FromBody]`) |
| **`[Route]`** | Määrittää controllerin perusreitin |
| **`[HttpGet]` jne.** | Yhdistää metodin tiettyyn HTTP-metodiin |
| **`IActionResult`** | Paluutyyppi joka sisältää statuskoodin ja datan |
| **Model** | C#-luokka joka kuvaa datan rakennetta |
| **Route-parametri** | `{id}` — data URL-polusta |
| **Query-parametri** | `?key=value` — data URL:n query stringistä |
| **`[FromBody]`** | Data pyynnön JSON-rungosta |

### Seuraavaksi

Kun ymmärrät controllerien toiminnan, siirry rakentamaan ensimmäinen Web API:
- [Backend Basics -tutoriaali](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend%20basics) — Ohjattu harjoitus askel askeleelta
- [Layered Architecture](../Architecture/Layered-Architecture.md) — Miten backend rakennetaan kerroksittain
- [Dependency Injection](../Dependency-Injection.md) — Miten palveluita käytetään controllereissa
