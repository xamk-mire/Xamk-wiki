# Service-kerros ja Dependency Injection Web API:ssa

## Sisällysluettelo

1. [Miksi controller ei saa sisältää kaikkea logiikkaa?](#miksi-controller-ei-saa-sisältää-kaikkea-logiikkaa)
2. [Mikä on service?](#mikä-on-service)
3. [Interface ja toteutus](#interface-ja-toteutus)
4. [Dependency Injection — miten service saadaan controlleriin?](#dependency-injection---miten-service-saadaan-controlleriin)
5. [Elinkaaret: Scoped, Singleton, Transient](#elinkaaret-scoped-singleton-transient)
6. [Rekisteröinti Program.cs:ssä](#rekisteröinti-programcsssä)
7. [Koko esimerkki](#koko-esimerkki)
8. [Projektikansiorakenne](#projektikansiorakenne)
9. [Yhteenveto](#yhteenveto)

---

## Miksi controller ei saa sisältää kaikkea logiikkaa?

Kun aloitat koodaamaan, on houkutus kirjoittaa kaikki koodi suoraan controlleriin. Tämä toimii pienissä projekteissa, mutta aiheuttaa ongelmia myöhemmin.

### Ongelma: "Fat Controller"

```csharp
// HUONO — kaikki logiikka controllerissa
[HttpPost]
public async Task<IActionResult> Create(Product product)
{
    // Validointia
    if (string.IsNullOrWhiteSpace(product.Name))
        return BadRequest("Nimi puuttuu.");
    if (product.Price < 0)
        return BadRequest("Hinta ei voi olla negatiivinen.");

    // Tietokantakoodi
    _context.Products.Add(product);
    await _context.SaveChangesAsync();

    // Sähköpostin lähetys (lisätty myöhemmin)
    await _emailService.SendNewProductNotification(product);

    // Välimuistin tyhjennys (lisätty vielä myöhemmin)
    _cache.Remove("all-products");

    return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
}
```

Mitä ongelmia tästä seuraa?
- Controller kasvaa satoja rivejä pitkäksi
- Sama logiikka kopioituu useaan paikkaan
- Testaaminen on vaikea — logiikka on sidottu HTTP-kerrokseen
- Vaikea muuttaa yhtä asiaa rikkomatta muita

### Ratkaisu: yksi vastuu per luokka

```
Controller vastaa:    "Mitä HTTP-pyynnöllä haluttiin?"
Service vastaa:       "Mitä sovellus tekee?"
Repository/DbContext: "Miten data haetaan?"
```

---

## Mikä on service?

**Service** on luokka, joka sisältää **sovelluksen liiketoimintalogiikan**. Controller kutsuu servicea, eikä tiedä miten se toimii sisältä.

```csharp
// Controller — ohut, vain HTTP-liimaa
[HttpPost]
public async Task<IActionResult> Create(Product product)
{
    var created = await _productService.CreateAsync(product);
    return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
}

// Service — sisältää logiikan
public async Task<Product> CreateAsync(Product product)
{
    if (string.IsNullOrWhiteSpace(product.Name))
        throw new ArgumentException("Nimi puuttuu.");

    _context.Products.Add(product);
    await _context.SaveChangesAsync();

    return product;
}
```

Nyt controller on ohut — se vain vastaanottaa pyynnön, kutsuu servicea ja palauttaa vastauksen.

---

## Interface ja toteutus

Servicet toteutetaan yleensä **interface-toteutus -parilla**:

```csharp
// 1. Interface — sopimus siitä mitä service tekee
public interface IProductService
{
    Task<List<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(int id);
    Task<Product> CreateAsync(Product product);
    Task<Product?> UpdateAsync(int id, Product product);
    Task<bool> DeleteAsync(int id);
}

// 2. Toteutus — konkreettinen koodi
public class ProductService : IProductService
{
    private readonly AppDbContext _context;

    public ProductService(AppDbContext context)
    {
        _context = context;
    }

    public async Task<List<Product>> GetAllAsync()
    {
        return await _context.Products.ToListAsync();
    }

    public async Task<Product?> GetByIdAsync(int id)
    {
        return await _context.Products.FindAsync(id);
    }

    // ... muut metodit
}
```

### Miksi interface?

| Ilman interfacea | Interfacen kanssa |
|-----------------|-------------------|
| Controller on sidottu `ProductService`-luokkaan | Controller riippuu vain `IProductService`-sopimuksesta |
| Testauksessa pitää käyttää oikeaa tietokantaa | Testauksessa voidaan korvata mock-toteutuksella |
| Toteutusta on vaikea vaihtaa | Toteutus voidaan vaihtaa muuttamatta controlleria |

> Lisää DI:n teoriasta: [Dependency Injection](../Dependency-Injection.md)

---

## Dependency Injection — miten service saadaan controlleriin?

**Dependency Injection (DI)** tarkoittaa, että luokka **ei luo itse tarvitsemiaan riippuvuuksia** — ne annetaan sille ulkoapäin.

### Ilman DI — huono

```csharp
public class ProductsController : ControllerBase
{
    private readonly ProductService _service;

    public ProductsController()
    {
        // Controller luo itse servicen — HUONO
        _service = new ProductService(new AppDbContext(...));
    }
}
```

Ongelmat: controller on sidottu konkreettiseen luokkaan, testaaminen on mahdotonta.

### DI:n kanssa — hyvä

```csharp
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;

    // ASP.NET Core antaa servicen automaattisesti konstruktorin kautta
    public ProductsController(IProductService service)
    {
        _service = service;
    }
}
```

ASP.NET Core:n **DI-kontti** huolehtii automaattisesti siitä, että oikea `IProductService`-toteutus luodaan ja annetaan controllerille. Sinun täytyy vain rekisteröidä service (katso alla).

---

## Elinkaaret: Scoped, Singleton, Transient

Kun rekisteröit servicen, määrität sen **elinkaaren** — kuinka kauan sama instanssi elää:

| Elinkaari | Kesto | Käytetään |
|-----------|-------|-----------|
| **Scoped** | Yksi HTTP-pyyntö | Yleisin — palvelut jotka käyttävät DbContextia |
| **Singleton** | Sovelluksen koko elinkaari | Konfiguraatio, välimuisti, yhteyspoolit |
| **Transient** | Luodaan uusi joka kerta | Kevyet, tillattomat apuluokat |

```csharp
// Scoped — uusi instanssi per HTTP-pyyntö (YLEISIN VALINTA)
builder.Services.AddScoped<IProductService, ProductService>();

// Singleton — yksi instanssi koko sovellukselle
builder.Services.AddSingleton<ICacheService, CacheService>();

// Transient — uusi instanssi joka kerta kun pyydetään
builder.Services.AddTransient<IEmailValidator, EmailValidator>();
```

> **Muistisääntö:** Käytä lähes aina `AddScoped` kun service käyttää `DbContext`:ia. `DbContext` itsessään on aina Scoped.

---

## Rekisteröinti Program.cs:ssä

Kaikki servicet rekisteröidään `Program.cs`:ssä ennen `app.Build()`-kutsua:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Tietokanta
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));

// Servicet
builder.Services.AddScoped<IProductService, ProductService>();
builder.Services.AddScoped<ICategoryService, CategoryService>();

builder.Services.AddControllers();
// ...

var app = builder.Build();
```

ASP.NET Core osaa nyt automaattisesti:
1. Luoda `AppDbContext`-instanssin per pyyntö
2. Injektoida sen `ProductService`-konstruktoriin
3. Injektoida `ProductService`:n `ProductsController`-konstruktoriin

---

## Koko esimerkki

### Projektikansiorakenne

```
ProductApi/
├── Controllers/
│   └── ProductsController.cs    ← ohut, vain HTTP
├── Services/
│   ├── IProductService.cs       ← interface (sopimus)
│   └── ProductService.cs        ← toteutus (logiikka)
├── Data/
│   └── AppDbContext.cs          ← tietokantayhteys
├── Models/
│   └── Product.cs               ← entiteetti
└── Program.cs
```

### IProductService.cs

```csharp
public interface IProductService
{
    Task<List<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(int id);
    Task<Product> CreateAsync(Product product);
    Task<Product?> UpdateAsync(int id, Product product);
    Task<bool> DeleteAsync(int id);
}
```

### ProductService.cs

```csharp
public class ProductService : IProductService
{
    private readonly AppDbContext _context;

    public ProductService(AppDbContext context)
    {
        _context = context;
    }

    public async Task<List<Product>> GetAllAsync()
    {
        return await _context.Products.ToListAsync();
    }

    public async Task<Product?> GetByIdAsync(int id)
    {
        return await _context.Products.FindAsync(id);
    }

    public async Task<Product> CreateAsync(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        return product;
    }

    public async Task<Product?> UpdateAsync(int id, Product product)
    {
        var existing = await _context.Products.FindAsync(id);
        if (existing == null) return null;

        existing.Name = product.Name;
        existing.Price = product.Price;
        existing.Description = product.Description;

        await _context.SaveChangesAsync();
        return existing;
    }

    public async Task<bool> DeleteAsync(int id)
    {
        var product = await _context.Products.FindAsync(id);
        if (product == null) return false;

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();
        return true;
    }
}
```

### ProductsController.cs

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IProductService _service;

    public ProductsController(IProductService service)
    {
        _service = service;
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var products = await _service.GetAllAsync();
        return Ok(products);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var product = await _service.GetByIdAsync(id);
        return product == null ? NotFound() : Ok(product);
    }

    [HttpPost]
    public async Task<IActionResult> Create(Product product)
    {
        var created = await _service.CreateAsync(product);
        return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, Product product)
    {
        var updated = await _service.UpdateAsync(id, product);
        return updated == null ? NotFound() : Ok(updated);
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var deleted = await _service.DeleteAsync(id);
        return deleted ? NoContent() : NotFound();
    }
}
```

Huomaa kuinka **controller on nyt täysin vapaa tietokantakoodista**. Se vain kutsuu servicea ja palauttaa vastauksen.

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Service** | Luokka joka sisältää liiketoimintalogiikan |
| **Interface** | Sopimus siitä mitä service tekee |
| **DI** | Riippuvuudet annetaan konstruktorin kautta |
| **Scoped** | Uusi instanssi per HTTP-pyyntö (yleisin) |
| **Singleton** | Yksi instanssi koko sovellukselle |
| **Transient** | Uusi instanssi joka kerta |
| **AddScoped** | Rekisteröi Scoped-palvelu DI-konttiin |

### Seuraavaksi

- [Services-harjoitus](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Services) — Refaktoroi ProductApi service-kerroksella
- [Authentication harjoitus](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Authentication) — Lisää JWT-autentikointi
- [Dependency Injection — teoria](../Dependency-Injection.md) — DI syvemmin
