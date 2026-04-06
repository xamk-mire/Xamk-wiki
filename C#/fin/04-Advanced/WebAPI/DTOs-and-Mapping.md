# DTO:t ja Mapping — API-rajapinnan erottaminen tietokannasta

## Sisällysluettelo

1. [Miksi entiteetti ei kelpaa API:n rajapinnaksi?](#miksi-entiteetti-ei-kelpaa-apin-rajapinnaksi)
2. [Mikä on DTO?](#mikä-on-dto)
3. [Over-posting — tietoturvariski ilman DTO:ita](#over-posting---tietoturvariski-ilman-dtoita)
4. [Request- ja Response-luokat](#request--ja-response-luokat)
5. [Mapping — muunnokset entiteetin ja DTO:n välillä](#mapping---muunnokset-entiteetin-ja-dton-välillä)
6. [Extension methodit](#extension-methodit)
7. [Mapping-luokka käytännössä](#mapping-luokka-käytännössä)
8. [Yhteenveto](#yhteenveto)

---

## Miksi entiteetti ei kelpaa API:n rajapinnaksi?

Kun rakennat Web API:n, voi tuntua luontevalta käyttää **samaa luokkaa** sekä tietokannassa (entiteetti) että API:n rajapinnalla. Se toimii — mutta aiheuttaa kaksi vakavaa ongelmaa:

**1. API on sidottu tietokantaan**

```csharp
// ❌ Entiteetti palautetaan suoraan
[HttpGet]
public async Task<IActionResult> GetAll()
{
    var products = await _context.Products.ToListAsync();
    return Ok(products);
}
```

Jos lisäät entiteettiin uuden kentän (esim. `InternalNotes`), se näkyy **automaattisesti** API:n vastauksessa — vaikka clientin ei pitäisi nähdä sitä.

**2. Client voi muokata kenttiä, joihin sillä ei ole oikeutta**

```csharp
// ❌ Entiteetti suoraan parametrina
[HttpPost]
public async Task<IActionResult> Create(Product product) { ... }
```

Client voi lähettää bodyssä `"id": 999` tai `"createdAt": "2020-01-01"` — kenttiä, joiden pitäisi olla palvelimen hallinnassa.

Ratkaisu on **DTO** (Data Transfer Object).

---

## Mikä on DTO?

**DTO** (Data Transfer Object) on yksinkertainen luokka, joka kuvaa **mitä data API:n rajapinnalla näyttää** — ei mitä se on tietokannassa. DTO toimii suodattimena entiteetin ja API:n välillä:

```
Client              API (DTO)            Tietokanta (Entiteetti)
────────────        ─────────────        ───────────────────────
CreateRequest  →    Product-olio     →   Products-taulu
                    ProductResponse  ←   Products-taulu
```

DTO:lla ratkaistaan molemmat ongelmat:

- **Over-posting estetään**: `CreateProductRequest` ei sisällä `Id`- tai `CreatedAt`-kenttää — client ei voi edes yrittää lähettää niitä
- **API ja tietokanta erotetaan**: `ProductResponse` määrittää tarkasti mitä clientille palautetaan

---

## Over-posting — tietoturvariski ilman DTO:ita

**Over-posting** tarkoittaa tilannetta, jossa client lähettää HTTP-pyynnössä kenttiä, joita sen ei pitäisi pystyä asettamaan.

### Esimerkki

Jos controller ottaa vastaan `Product`-entiteetin suoraan:

```csharp
[HttpPost]
public async Task<IActionResult> Create(Product product)
{
    _context.Products.Add(product);
    await _context.SaveChangesAsync();
    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}
```

Client voi lähettää:

```json
{
  "id": 999,
  "name": "Ilmainen tuote",
  "price": 0.00,
  "createdAt": "2020-01-01T00:00:00"
}
```

EF Core saattaa kohdella tätä olemassa olevan rivin päivityksenä (koska `Id = 999` on asetettu), tai client saa väärennetyn luontiajan.

### Ratkaisu: erillinen Request-luokka

```csharp
public class CreateProductRequest
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
}
```

Luokassa **ei ole** `Id`-, `CreatedAt`- tai `UpdatedAt`-kenttää — client ei voi lähettää niitä, koska ASP.NET Core jättää tuntemattomat kentät huomiotta.

---

## Request- ja Response-luokat

DTO:t jaetaan tyypillisesti kahteen kategoriaan:

### Request-luokat (sisään tuleva data)

**`CreateProductRequest`** — mitä client lähettää kun luo uuden tuotteen:

```csharp
public class CreateProductRequest
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
}
```

**`UpdateProductRequest`** — mitä client lähettää kun päivittää tuotteen:

```csharp
public class UpdateProductRequest
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
}
```

Päivitettävän tuotteen Id tulee URL:sta (`PUT /api/products/5`), ei bodystä.

### Response-luokka (ulos lähtevä data)

**`ProductResponse`** — mitä API palauttaa clientille:

```csharp
public class ProductResponse
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}
```

Responsessa on `CreatedAt` ja `UpdatedAt` (hyödyllistä tietoa clientille), mutta niitä **ei ole** Request-luokissa — palvelin asettaa ne automaattisesti.

### Kansiorakenne

```
Models/
├── BaseEntity.cs
├── Product.cs              ← Tietokantaentiteetti
└── Dtos/
    ├── CreateProductRequest.cs
    ├── UpdateProductRequest.cs
    └── ProductResponse.cs
```

---

## Mapping — muunnokset entiteetin ja DTO:n välillä

Kun DTO:t ovat käytössä, controllerissa tarvitaan **muunnoskoodia** entiteetin ja DTO:n välillä:

```csharp
// Jokaisessa endpointissa toistuva muunnoskoodi
var response = new ProductResponse
{
    Id = product.Id,
    Name = product.Name,
    Price = product.Price,
    Description = product.Description,
    CreatedAt = product.CreatedAt,
    UpdatedAt = product.UpdatedAt
};
```

Tämä muunnos toistuu **jokaisessa endpointissa**, mikä rikkoo **DRY-periaatetta** (Don't Repeat Yourself). Jos entiteettiin lisätään kenttä, joudut muistamaan päivittää jokaisen kohdan.

Ratkaisu: siirrä muunnokset **yhteen paikkaan** erilliseen mapping-luokkaan.

---

## Extension methodit

**Extension method** on C#:n ominaisuus, jolla voit lisätä olemassa olevaan luokkaan uusia metodeja ilman, että muutat itse luokkaa.

### Syntaksi

```csharp
// Normaali staattinen metodi — kutsutaan näin:
var response = ProductMappings.ToResponse(product);

// Extension method — kutsutaan näin:
var response = product.ToResponse();
```

Extension method tekee koodista luettavampaa, koska metodi "kuuluu" siihen olioon jota muunnetaan.

### Säännöt

Extension methodilla on kolme vaatimusta:

```csharp
public static class ProductMappings          // 1. Luokan TÄYTYY olla static
{
    public static ProductResponse ToResponse(  // 2. Metodin TÄYTYY olla static
        this Product product)                  // 3. Ensimmäinen parametri alkaa this-avainsanalla
    {
        // ...
    }
}
```

| Sääntö | Miksi? |
|--------|--------|
| `static class` | Extension methodit eivät tarvitse instanssia |
| `static` metodi | Samasta syystä |
| `this` ensimmäisessä parametrissa | Kertoo C#:lle, että tämä on extension method kyseiselle tyypille |

### Ennen ja jälkeen

```csharp
// ❌ Ilman extension methodia — 6 riviä muunnosta jokaisessa endpointissa
var response = new ProductResponse
{
    Id = product.Id,
    Name = product.Name,
    Price = product.Price,
    Description = product.Description,
    CreatedAt = product.CreatedAt,
    UpdatedAt = product.UpdatedAt
};

// ✅ Extension methodilla — 1 rivi
var response = product.ToResponse();
```

---

## Mapping-luokka käytännössä

Kaikki muunnokset kootaan yhteen `ProductMappings`-luokkaan:

```csharp
public static class ProductMappings
{
    // Product → ProductResponse (entiteetti → API-vastaus)
    public static ProductResponse ToResponse(this Product product)
    {
        return new ProductResponse
        {
            Id = product.Id,
            Name = product.Name,
            Price = product.Price,
            Description = product.Description,
            CreatedAt = product.CreatedAt,
            UpdatedAt = product.UpdatedAt
        };
    }

    // CreateProductRequest → Product (luontipyyntö → entiteetti)
    public static Product ToEntity(this CreateProductRequest request)
    {
        return new Product
        {
            Name = request.Name,
            Price = request.Price,
            Description = request.Description
        };
    }

    // UpdateProductRequest → päivittää olemassa olevaa Product-oliota
    public static void UpdateEntity(this UpdateProductRequest request, Product product)
    {
        product.Name = request.Name;
        product.Price = request.Price;
        product.Description = request.Description;
    }
}
```

### Kolme mapping-metodia

| Metodi | Suunta | Tarkoitus |
|--------|--------|-----------|
| `ToResponse()` | Entity → DTO | Muuntaa tietokantaentiteetin API-vastaukseksi |
| `ToEntity()` | DTO → Entity | Muuntaa luontipyynnön uudeksi entiteetiksi |
| `UpdateEntity()` | DTO → Entity (olemassa oleva) | Päivittää olemassa olevan entiteetin kentät |

**`ToEntity()`** ei aseta `Id`:tä tai `CreatedAt`:ia — tietokanta ja `SaveChangesAsync`-ylikirjoitus hoitavat ne.

**`UpdateEntity()`** ei luo uutta oliota vaan muuttaa olemassa olevaa. EF Core seuraa muutoksia `ChangeTracker`:in avulla, joten riittää muuttaa kentät ja kutsua `SaveChangesAsync()`.

### Käyttö controllerissa

```csharp
[HttpPost]
public async Task<IActionResult> Create(CreateProductRequest request)
{
    var product = request.ToEntity();

    _context.Products.Add(product);
    await _context.SaveChangesAsync();

    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product.ToResponse());
}

[HttpPut("{id}")]
public async Task<IActionResult> Update(int id, UpdateProductRequest request)
{
    var existing = await _context.Products.FindAsync(id);
    if (existing is null) return NotFound();

    request.UpdateEntity(existing);
    await _context.SaveChangesAsync();

    return Ok(existing.ToResponse());
}
```

### Kansiorakenne

```
ProductApi/
├── Controllers/
│   └── ProductsController.cs
├── Models/
│   ├── BaseEntity.cs
│   ├── Product.cs
│   └── Dtos/
│       ├── CreateProductRequest.cs
│       ├── UpdateProductRequest.cs
│       └── ProductResponse.cs
├── Mappings/
│   └── ProductMappings.cs      ← Kaikki muunnokset yhdessä paikassa
└── Program.cs
```

> **Automaattiset mapperit:** Kirjastot kuten **AutoMapper** ja **Mapster** tekevät muunnokset automaattisesti kenttien nimien perusteella. Ne ovat hyödyllisiä suurissa projekteissa, mutta piilottavat mitä oikeasti tapahtuu. Käsin kirjoitetut mapperit ovat selkeämpiä ja helpompia debugata.

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **DTO** | Data Transfer Object — erottaa API-rajapinnan tietokannasta |
| **Over-posting** | Tietoturvaongelma: client lähettää kenttiä joita sen ei kuulu hallita |
| **Request-luokka** | Kuvaa mitä client saa lähettää (ei Id:tä, ei aikaleimoja) |
| **Response-luokka** | Kuvaa mitä API palauttaa clientille |
| **Extension method** | Lisää olemassa olevaan tyyppiin uuden metodin (`this`-avainsana) |
| **Mapping-luokka** | Kokoaa kaikki muunnokset yhteen paikkaan (DRY-periaate) |
| **`ToResponse()`** | Entity → DTO |
| **`ToEntity()`** | Request → Entity |
| **`UpdateEntity()`** | Request → päivittää olemassa olevaa entityä |

### Seuraavaksi

- [Entity Framework Core](Entity-Framework.md) — Tietokantakäsittelyn perusteet
- [BaseEntity ja automaattiset aikaleimakentät](BaseEntity.md) — Kantaluokka ja ChangeTracker
- [Service-kerros ja DI](Services-and-DI.md) — Liiketoimintalogiikan erottaminen controllerista
