# Layered Architecture (Kerrosarkkitehtuuri)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on Layered Architecture?](#mikä-on-layered-architecture)
3. [Kerrokset](#kerrokset)
4. [Periaatteet](#periaatteet)
5. [Edut ja haitat](#edut-ja-haitat)
6. [Milloin käyttää?](#milloin-käyttää)
7. [Käytännön esimerkki](#käytännön-esimerkki)
8. [Parhaat käytännöt](#parhaat-käytännöt)
9. [Yhteenveto](#yhteenveto)

---

## Johdanto

Layered Architecture (tai N-tier Architecture) on yksi vanhimmista ja yleisimmistä arkkitehtuurimalleista ohjelmistokehityksessä. Se on yksinkertainen, helppo ymmärtää ja toimii hyvin monissa sovelluksissa.

### Missä käytetään?

- Web-sovellukset (ASP.NET Core MVC)
- Desktop-sovellukset
- CRUD-sovellukset (Create, Read, Update, Delete)
- Perinteiset enterprise-sovellukset

---

## Mikä on Layered Architecture?

Layered Architecture jakaa sovelluksen **vaakasuoriin kerroksiin**, jossa jokainen kerros vastaa tietystä vastuualueesta. Ylemmät kerrokset kommunikoivat alemman kerroksen kanssa, mutta alemmat kerrokset eivät tiedä ylemmistä kerroksista.

### Rakenne

```
┌─────────────────────────────┐
│   Presentation Layer (UI)   │ ← Käyttöliittymä
├─────────────────────────────┤     ↓
│   Business Logic Layer      │ ← Liiketoimintalogiikka
├─────────────────────────────┤     ↓
│   Data Access Layer         │ ← Tietokannan käsittely
├─────────────────────────────┤     ↓
│   Database                  │ ← Tietokanta
└─────────────────────────────┘
```

---

## Kerrokset

### 1. Presentation Layer (Esityskerros)

**Vastuu:** Käyttöliittymä ja käyttäjän vuorovaikutus

**Sisältää:**
- Controllers (ASP.NET MVC)
- Views / Pages
- ViewModels / DTOs
- UI-logiikka (validointi, muotoilu)

**Tekn

ologiat:**
- ASP.NET Core MVC / Razor Pages
- Blazor
- WPF / WinForms
- React / Angular (frontend)

### 2. Business Logic Layer (Liiketoimintalogiikkakerros)

**Vastuu:** Liiketoimintasäännöt ja -logiikka

**Sisältää:**
- Service-luokat
- Business rules -validointi
- Laskelmat ja muunnokset
- Työnkulut (workflows)

**Esimerkki:** Alennuslaskenta, tilauksen vahvistus, käyttäjäoikeuksien tarkistus

### 3. Data Access Layer (Tiedon käsittelykerros)

**Vastuu:** Tietokannan käsittely

**Sisältää:**
- Repository-luokat
- Database Context (Entity Framework)
- SQL-kyselyt / LINQ
- Datan hakeminen ja tallentaminen

**Teknologiat:**
- Entity Framework Core
- Dapper
- ADO.NET

### 4. Database (Tietokanta)

**Vastuu:** Datan tallentaminen

**Teknologiat:**
- SQL Server
- PostgreSQL
- MySQL
- SQLite

---

## Periaatteet

### 1. Kerrosten välinen kommunikaatio

**Sääntö:** Ylemmät kerrokset voivat kutsua alempia kerroksia, mutta alemmat kerrokset EIVÄT saa kutsua ylempiä.

```
Presentation → Business Logic → Data Access → Database
    ✅              ✅              ✅
    ❌ ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

### 2. Separation of Concerns (Vastuiden erottelu)

Jokainen kerros vastaa omasta vastuualueestaan:

- **UI** ei tiedä tietokannasta
- **Business Logic** ei tiedä miten data tallennetaan
- **Data Access** ei tiedä mistä dataa kysytään

### 3. Abstraktio

Jokainen kerros tarjoaa rajapinnan ylemmälle kerrokselle:

```csharp
// Business Logic Layer tarjoaa rajapinnan
public interface IProductService
{
    Task<Product> GetProductAsync(int id);
    Task CreateProductAsync(Product product);
}

// Presentation Layer käyttää rajapintaa
public class ProductController
{
    private IProductService _productService;
    
    public ProductController(IProductService productService)
    {
        _productService = productService;
    }
}
```

---

## Edut ja haitat

### Edut

✅ **Yksinkertainen ja helppo ymmärtää**
- Selkeä rakenne
- Helppo oppia uusille kehittäjille
- Yleisesti tunnettu malli

✅ **Selkeä vastuiden jako**
- Jokainen kerros vastaa yhdestä asiasta
- Helppo löytää oikea paikka koodille

✅ **Kerroksia voi kehittää erikseen**
- UI-tiimi voi työskennellä itsenäisesti
- Backend-tiimi voi työskennellä itsenäisesti

✅ **Soveltuu hyvin pieniin ja keskisuuriin sovelluksiin**
- Ei ylimääräistä kompleksisuutta
- Nopea aloittaa

### Haitat

❌ **Riippuvuus suunta alaspäin**
- Business Logic riippuu Data Access:sta
- Vaikea vaihtaa tietokantaa
- Testaaminen vaatii tietokannan

❌ **Tietokantamalli "valuu" ylemmille kerroksille**
- Entity Framework -mallit käytetään suoraan UI:ssa
- Muutokset tietokantaan vaikuttavat koko sovellukseen

❌ **Vaikea testata ilman tietokantaa**
- Business Logic testit vaativat tietokannan
- Hitaat testit

❌ **Monolittisuus**
- Kaikki koodi yhdessä projektissa
- Vaikea skaalata

---

## Milloin käyttää?

### ✅ Käytä kun:

- **Pieni tai keskisuuri sovellus** (alle 10 kehittäjää)
- **CRUD-sovellus** (Create, Read, Update, Delete)
- **Yksinkertainen liiketoimintalogiikka**
- **Nopea kehitys tärkeää**
- **Tiimi tuntee perinteisen kerrosarkkitehtuurin**

### ❌ Älä käytä kun:

- **Sovellus on suuri ja monimutkainen**
- **Vaatii korkeaa testattavuutta**
- **Teknologia saattaa vaihtua** (esim. tietokanta)
- **Vaatii mikropalveluarkkitehtuuria**
- **Liiketoimintalogiikka on monimutkaista**

---

## Käytännön esimerkki

Toteutetaan yksinkertainen tuotehallintasovellus Layered Architecture -mallilla.

### Projektirakenne

```
ProductManagement/
├── ProductManagement.Web/          (Presentation Layer)
│   ├── Controllers/
│   │   └── ProductController.cs
│   ├── Views/
│   └── Program.cs
├── ProductManagement.Business/     (Business Logic Layer)
│   ├── Services/
│   │   └── ProductService.cs
│   └── Models/
│       └── Product.cs
├── ProductManagement.DataAccess/   (Data Access Layer)
│   ├── Repositories/
│   │   └── ProductRepository.cs
│   ├── Data/
│   │   └── ApplicationDbContext.cs
│   └── Entities/
│       └── ProductEntity.cs
└── ProductManagement.Database/     (Database)
    └── SQL Scripts
```

### 1. Database Layer

Tietokantataulu (SQL):

```sql
CREATE TABLE Products (
    Id INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(200) NOT NULL,
    Price DECIMAL(18,2) NOT NULL,
    Stock INT NOT NULL,
    CreatedDate DATETIME NOT NULL DEFAULT GETDATE()
);
```

### 2. Data Access Layer

**Entities/ProductEntity.cs:**

```csharp
namespace ProductManagement.DataAccess.Entities;

public class ProductEntity
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int Stock { get; set; }
    public DateTime CreatedDate { get; set; }
}
```

**Data/ApplicationDbContext.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using ProductManagement.DataAccess.Entities;

namespace ProductManagement.DataAccess.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<ProductEntity> Products { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<ProductEntity>(entity =>
        {
            entity.ToTable("Products");
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Name).IsRequired().HasMaxLength(200);
            entity.Property(e => e.Price).HasColumnType("decimal(18,2)");
            entity.Property(e => e.Stock).IsRequired();
            entity.Property(e => e.CreatedDate).HasDefaultValueSql("GETDATE()");
        });
    }
}
```

**Repositories/ProductRepository.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using ProductManagement.DataAccess.Data;
using ProductManagement.DataAccess.Entities;

namespace ProductManagement.DataAccess.Repositories;

public class ProductRepository
{
    private readonly ApplicationDbContext _context;

    public ProductRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<ProductEntity?> GetByIdAsync(int id)
    {
        return await _context.Products.FindAsync(id);
    }

    public async Task<List<ProductEntity>> GetAllAsync()
    {
        return await _context.Products
            .OrderBy(p => p.Name)
            .ToListAsync();
    }

    public async Task<List<ProductEntity>> GetAvailableProductsAsync()
    {
        return await _context.Products
            .Where(p => p.Stock > 0)
            .OrderBy(p => p.Name)
            .ToListAsync();
    }

    public async Task<int> AddAsync(ProductEntity product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        return product.Id;
    }

    public async Task UpdateAsync(ProductEntity product)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync();
    }

    public async Task DeleteAsync(int id)
    {
        ProductEntity? product = await GetByIdAsync(id);
        if (product != null)
        {
            _context.Products.Remove(product);
            await _context.SaveChangesAsync();
        }
    }

    public async Task<bool> ExistsAsync(int id)
    {
        return await _context.Products.AnyAsync(p => p.Id == id);
    }
}
```

### 3. Business Logic Layer

**Models/Product.cs:**

```csharp
namespace ProductManagement.Business.Models;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int Stock { get; set; }
    public DateTime CreatedDate { get; set; }

    // Business logic methods
    public bool IsAvailable()
    {
        return Stock > 0;
    }

    public bool IsLowStock()
    {
        return Stock > 0 && Stock <= 10;
    }

    public decimal GetTotalValue()
    {
        return Price * Stock;
    }
}
```

**Services/ProductService.cs:**

```csharp
using ProductManagement.Business.Models;
using ProductManagement.DataAccess.Repositories;
using ProductManagement.DataAccess.Entities;

namespace ProductManagement.Business.Services;

public class ProductService
{
    private readonly ProductRepository _productRepository;

    public ProductService(ProductRepository productRepository)
    {
        _productRepository = productRepository;
    }

    public async Task<Product?> GetProductAsync(int id)
    {
        ProductEntity? entity = await _productRepository.GetByIdAsync(id);
        
        if (entity == null)
            return null;

        return MapToModel(entity);
    }

    public async Task<List<Product>> GetAllProductsAsync()
    {
        List<ProductEntity> entities = await _productRepository.GetAllAsync();
        return entities.Select(MapToModel).ToList();
    }

    public async Task<List<Product>> GetAvailableProductsAsync()
    {
        List<ProductEntity> entities = await _productRepository.GetAvailableProductsAsync();
        return entities.Select(MapToModel).ToList();
    }

    public async Task<int> CreateProductAsync(Product product)
    {
        // Business rules validation
        ValidateProduct(product);

        // Additional business logic
        if (product.Price <= 0)
            throw new ArgumentException("Hinta ei voi olla nolla tai negatiivinen");

        if (product.Stock < 0)
            throw new ArgumentException("Varasto ei voi olla negatiivinen");

        if (string.IsNullOrWhiteSpace(product.Name))
            throw new ArgumentException("Tuotteen nimi on pakollinen");

        // Map to entity and save
        ProductEntity entity = MapToEntity(product);
        entity.CreatedDate = DateTime.Now;

        int id = await _productRepository.AddAsync(entity);
        return id;
    }

    public async Task UpdateProductAsync(Product product)
    {
        // Check if exists
        bool exists = await _productRepository.ExistsAsync(product.Id);
        if (!exists)
            throw new InvalidOperationException("Tuotetta ei löydy");

        // Validate
        ValidateProduct(product);

        // Update
        ProductEntity entity = MapToEntity(product);
        await _productRepository.UpdateAsync(entity);
    }

    public async Task DeleteProductAsync(int id)
    {
        bool exists = await _productRepository.ExistsAsync(id);
        if (!exists)
            throw new InvalidOperationException("Tuotetta ei löydy");

        await _productRepository.DeleteAsync(id);
    }

    public async Task<bool> PurchaseProductAsync(int productId, int quantity)
    {
        Product? product = await GetProductAsync(productId);
        
        if (product == null)
            return false;

        // Business logic: Check stock
        if (product.Stock < quantity)
            throw new InvalidOperationException($"Ei tarpeeksi varastossa. Saatavilla: {product.Stock}");

        // Reduce stock
        product.Stock -= quantity;
        await UpdateProductAsync(product);

        return true;
    }

    public async Task RestockProductAsync(int productId, int quantity)
    {
        if (quantity <= 0)
            throw new ArgumentException("Täydennysmäärän pitää olla positiivinen");

        Product? product = await GetProductAsync(productId);
        
        if (product == null)
            throw new InvalidOperationException("Tuotetta ei löydy");

        product.Stock += quantity;
        await UpdateProductAsync(product);
    }

    // Private helper methods
    private void ValidateProduct(Product product)
    {
        if (product == null)
            throw new ArgumentNullException(nameof(product));

        if (string.IsNullOrWhiteSpace(product.Name))
            throw new ArgumentException("Tuotteen nimi on pakollinen");

        if (product.Name.Length > 200)
            throw new ArgumentException("Tuotteen nimi saa olla enintään 200 merkkiä");

        if (product.Price < 0)
            throw new ArgumentException("Hinta ei voi olla negatiivinen");

        if (product.Stock < 0)
            throw new ArgumentException("Varasto ei voi olla negatiivinen");
    }

    private Product MapToModel(ProductEntity entity)
    {
        return new Product
        {
            Id = entity.Id,
            Name = entity.Name,
            Price = entity.Price,
            Stock = entity.Stock,
            CreatedDate = entity.CreatedDate
        };
    }

    private ProductEntity MapToEntity(Product model)
    {
        return new ProductEntity
        {
            Id = model.Id,
            Name = model.Name,
            Price = model.Price,
            Stock = model.Stock,
            CreatedDate = model.CreatedDate
        };
    }
}
```

### 4. Presentation Layer

**Controllers/ProductController.cs:**

```csharp
using Microsoft.AspNetCore.Mvc;
using ProductManagement.Business.Models;
using ProductManagement.Business.Services;

namespace ProductManagement.Web.Controllers;

public class ProductController : Controller
{
    private readonly ProductService _productService;

    public ProductController(ProductService productService)
    {
        _productService = productService;
    }

    // GET: /Product
    public async Task<IActionResult> Index()
    {
        List<Product> products = await _productService.GetAllProductsAsync();
        return View(products);
    }

    // GET: /Product/Details/5
    public async Task<IActionResult> Details(int id)
    {
        Product? product = await _productService.GetProductAsync(id);
        
        if (product == null)
            return NotFound();

        return View(product);
    }

    // GET: /Product/Create
    public IActionResult Create()
    {
        return View();
    }

    // POST: /Product/Create
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Create(Product product)
    {
        if (!ModelState.IsValid)
            return View(product);

        try
        {
            await _productService.CreateProductAsync(product);
            TempData["SuccessMessage"] = "Tuote luotu onnistuneesti!";
            return RedirectToAction(nameof(Index));
        }
        catch (ArgumentException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View(product);
        }
    }

    // GET: /Product/Edit/5
    public async Task<IActionResult> Edit(int id)
    {
        Product? product = await _productService.GetProductAsync(id);
        
        if (product == null)
            return NotFound();

        return View(product);
    }

    // POST: /Product/Edit/5
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Edit(int id, Product product)
    {
        if (id != product.Id)
            return BadRequest();

        if (!ModelState.IsValid)
            return View(product);

        try
        {
            await _productService.UpdateProductAsync(product);
            TempData["SuccessMessage"] = "Tuote päivitetty onnistuneesti!";
            return RedirectToAction(nameof(Index));
        }
        catch (InvalidOperationException ex)
        {
            return NotFound();
        }
        catch (ArgumentException ex)
        {
            ModelState.AddModelError("", ex.Message);
            return View(product);
        }
    }

    // GET: /Product/Delete/5
    public async Task<IActionResult> Delete(int id)
    {
        Product? product = await _productService.GetProductAsync(id);
        
        if (product == null)
            return NotFound();

        return View(product);
    }

    // POST: /Product/Delete/5
    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> DeleteConfirmed(int id)
    {
        try
        {
            await _productService.DeleteProductAsync(id);
            TempData["SuccessMessage"] = "Tuote poistettu onnistuneesti!";
            return RedirectToAction(nameof(Index));
        }
        catch (InvalidOperationException)
        {
            return NotFound();
        }
    }

    // POST: /Product/Purchase/5
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Purchase(int id, int quantity)
    {
        if (quantity <= 0)
        {
            TempData["ErrorMessage"] = "Määrän pitää olla positiivinen";
            return RedirectToAction(nameof(Details), new { id });
        }

        try
        {
            await _productService.PurchaseProductAsync(id, quantity);
            TempData["SuccessMessage"] = $"Ostos onnistui! Määrä: {quantity}";
            return RedirectToAction(nameof(Details), new { id });
        }
        catch (InvalidOperationException ex)
        {
            TempData["ErrorMessage"] = ex.Message;
            return RedirectToAction(nameof(Details), new { id });
        }
    }

    // POST: /Product/Restock/5
    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Restock(int id, int quantity)
    {
        if (quantity <= 0)
        {
            TempData["ErrorMessage"] = "Täydennysmäärän pitää olla positiivinen";
            return RedirectToAction(nameof(Details), new { id });
        }

        try
        {
            await _productService.RestockProductAsync(id, quantity);
            TempData["SuccessMessage"] = $"Varasto täydennetty! Määrä: {quantity}";
            return RedirectToAction(nameof(Details), new { id });
        }
        catch (InvalidOperationException ex)
        {
            TempData["ErrorMessage"] = ex.Message;
            return RedirectToAction(nameof(Details), new { id });
        }
    }
}
```

**Program.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using ProductManagement.DataAccess.Data;
using ProductManagement.DataAccess.Repositories;
using ProductManagement.Business.Services;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllersWithViews();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Data Access Layer
builder.Services.AddScoped<ProductRepository>();

// Business Logic Layer
builder.Services.AddScoped<ProductService>();

WebApplication app = builder.Build();

// Configure the HTTP request pipeline
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Product}/{action=Index}/{id?}");

app.Run();
```

---

## Parhaat käytännöt

### 1. Noudata kerrosten riippuvuussääntöjä

```csharp
// ✅ Hyvä: Presentation riippuu Business Logic:sta
public class ProductController
{
    private readonly ProductService _productService;
}

// ❌ Huono: Presentation käyttää suoraan Data Access:ia
public class ProductController
{
    private readonly ProductRepository _productRepository; // Ohitetaan Business Logic!
}
```

### 2. Käytä DTO:ita kerroksien välillä

```csharp
// Business Layer
public class Product { ... }

// Presentation Layer (API)
public class ProductDto
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    // Ei sisällä sisäisiä kenttiä
}
```

### 3. Älä paljasta tietokantaentiteettejä UI:lle

```csharp
// ❌ Huono: Entity Framework -mallit UI:ssa
public IActionResult Index()
{
    List<ProductEntity> products = _context.Products.ToList(); // EF entity
    return View(products);
}

// ✅ Hyvä: Business-mallit UI:ssa
public async Task<IActionResult> Index()
{
    List<Product> products = await _productService.GetAllProductsAsync(); // Business model
    return View(products);
}
```

### 4. Keskitä liiketoimintalogiikka Business Layer:iin

```csharp
// ❌ Huono: Liiketoimintalogiikka Controller:ssa
public async Task<IActionResult> Purchase(int id, int quantity)
{
    Product product = await _productService.GetProductAsync(id);
    if (product.Stock < quantity) // Business logic leaks to UI!
        return BadRequest();
    product.Stock -= quantity;
    await _productService.UpdateProductAsync(product);
}

// ✅ Hyvä: Liiketoimintalogiikka Service:ssä
public async Task<IActionResult> Purchase(int id, int quantity)
{
    await _productService.PurchaseProductAsync(id, quantity); // Business logic in service
    return Ok();
}
```

### 5. Käytä Dependency Injection:ia

```csharp
// Program.cs
builder.Services.AddScoped<ProductRepository>();
builder.Services.AddScoped<ProductService>();

// Controller
public class ProductController : Controller
{
    private readonly ProductService _productService;
    
    public ProductController(ProductService productService)
    {
        _productService = productService;
    }
}
```

### 6. Testaa jokaista kerrosta erikseen

```csharp
// Business Logic Layer testi
[Fact]
public async Task CreateProduct_ValidProduct_ReturnsId()
{
    // Arrange
    Mock<ProductRepository> mockRepo = new Mock<ProductRepository>();
    ProductService service = new ProductService(mockRepo.Object);
    
    Product product = new Product { Name = "Test", Price = 10, Stock = 5 };
    
    // Act
    int id = await service.CreateProductAsync(product);
    
    // Assert
    Assert.True(id > 0);
}
```

---

## Yhteenveto

### Layered Architecture sopii kun:

✅ Rakennat pientä tai keskisuurta sovellusta
✅ Tarvitset nopean kehitysvauhdin
✅ CRUD-toiminnot ovat pääasiallinen toiminnallisuus
✅ Tiimi tuntee perinteisen kerrosarkkitehtuurin
✅ Sovellus ei vaadi korkeaa testattavuutta

### Haas teet:

❌ Riippuvuus suunta alaspäin (Business → Data Access)
❌ Vaikea testata ilman tietokantaa
❌ Tietokantamallit "vuotavat" UI:hin
❌ Ei sovi suuriin, monimutkaisiin sovelluksiin

### Muista:

- **Noudata kerrosten riippuvuussääntöjä**
- **Keskitä liiketoimintalogiikka Business Layer:iin**
- **Käytä Dependency Injection:ia**
- **Refaktoroi Clean Architecture:en jos sovellus kasvaa**

---

## Seuraavaksi

Kun Layered Architecture alkaa tuntua rajoitteiselta:

- **[Clean Architecture](Clean-Architecture.md)** - Käännä riippuvuudet päinvastaiseen suuntaan
- **[Hexagonal Architecture](Hexagonal-Architecture.md)** - Portit ja adapterit
- **[CQRS](CQRS.md)** - Erottele lukeminen ja kirjoittaminen

### Hyödyllisiä linkkejä

- [Microsoft: Layered Architecture](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ee658109(v=pandp.10))
- [Martin Fowler: Presentation Domain Data Layering](https://martinfowler.com/bliki/PresentationDomainDataLayering.html)
