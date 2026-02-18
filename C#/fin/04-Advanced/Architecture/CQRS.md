# CQRS (Command Query Responsibility Segregation)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [CQS-periaate - Tausta](#cqs-periaate---tausta)
3. [Mikä on CQRS?](#mikä-on-cqrs)
4. [Ongelma: Yhteinen malli lukemiselle ja kirjoittamiselle](#ongelma-yhteinen-malli-lukemiselle-ja-kirjoittamiselle)
5. [Ratkaisu: Erilliset mallit](#ratkaisu-erilliset-mallit)
6. [CQRS-tasot](#cqrs-tasot)
7. [CQRS käytännössä C#:lla](#cqrs-käytännössä-clla)
8. [CQRS + MediatR](#cqrs--mediatr)
9. [CQRS + Clean Architecture](#cqrs--clean-architecture)
10. [CQRS + Event Sourcing](#cqrs--event-sourcing)
11. [Milloin käyttää CQRS:ää?](#milloin-käyttää-cqrsää)
12. [Best Practices](#best-practices)
13. [Anti-patterns](#anti-patterns)
14. [Yhteenveto](#yhteenveto)

---

## Johdanto

**CQRS (Command Query Responsibility Segregation)** on arkkitehtuurimalli, joka erottaa sovelluksen **luku-** (Query) ja **kirjoitusoperaatiot** (Command) toisistaan. Perusideana on, että datan lukeminen ja muokkaaminen ovat fundamentaalisesti erilaisia toimintoja, ja niillä pitäisi olla omat erilliset mallinsa.

**Perusidea:**

```
Perinteinen malli:
┌──────────────────────┐
│     ProductService    │
│  ─────────────────── │
│  GetAll()       READ  │
│  GetById()      READ  │
│  Create()      WRITE  │
│  Update()      WRITE  │
│  Delete()      WRITE  │
└──────────┬───────────┘
           │
     ┌─────┴─────┐
     │ Database  │
     └───────────┘

CQRS-malli:
┌──────────────┐    ┌───────────────┐
│  Query Side  │    │ Command Side  │
│ ──────────── │    │ ───────────── │
│ GetAll()     │    │ Create()      │
│ GetById()    │    │ Update()      │
│              │    │ Delete()      │
└──────┬───────┘    └───────┬───────┘
       │                    │
  ┌────┴────┐          ┌───┴────┐
  │ Read DB │          │Write DB│
  └─────────┘          └────────┘
```

---

## CQS-periaate - Tausta

CQRS perustuu **Bertrand Meyerin CQS-periaatteeseen** (Command Query Separation):

> "Every method should either be a command that performs an action, or a query that returns data to the caller, but not both."

### CQS käytännössä

```csharp
public class ShoppingCart
{
    private readonly List<CartItem> _items = new();

    // ✅ QUERY: Palauttaa arvon, EI muuta tilaa
    public decimal GetTotalPrice()
    {
        return _items.Sum(item => item.Price * item.Quantity);
    }

    // ✅ QUERY: Palauttaa arvon, EI muuta tilaa
    public int GetItemCount()
    {
        return _items.Count;
    }

    // ✅ COMMAND: Muuttaa tilaa, EI palauta arvoa (void)
    public void AddItem(CartItem item)
    {
        _items.Add(item);
    }

    // ✅ COMMAND: Muuttaa tilaa, EI palauta arvoa (void)
    public void RemoveItem(int itemId)
    {
        _items.RemoveAll(i => i.Id == itemId);
    }

    // ❌ CQS-RIKKOMUS: Muuttaa tilaa JA palauttaa arvon
    public CartItem AddAndReturnItem(CartItem item)
    {
        _items.Add(item);
        return item;  // Muuttaa tilaa JA palauttaa → hämärä tarkoitus
    }
}
```

### CQS vs CQRS

| | CQS | CQRS |
|---|---|---|
| **Taso** | Metodi-taso | Arkkitehtuuri-taso |
| **Scope** | Yksittäinen luokka | Koko sovellus |
| **Idea** | Metodi joko lukee tai kirjoittaa | Erilliset mallit lukemiselle ja kirjoittamiselle |
| **Keksi** | Bertrand Meyer | Greg Young |

---

## Mikä on CQRS?

CQRS vie CQS-periaatteen arkkitehtuuritasolle: sen sijaan, että **sama malli** käsittelisi sekä lukemisen että kirjoittamisen, käytetään **erillisiä malleja**.

### Command (Komento)

**Command** muuttaa järjestelmän tilaa:

```
Command = "Tee jotain"
  - CreateProduct     → Luo tuote
  - UpdateProduct     → Päivitä tuote
  - DeleteProduct     → Poista tuote
  - PlaceOrder        → Tee tilaus

Ominaisuudet:
  - Muuttaa dataa (side effect)
  - Ei tyypillisesti palauta dataa (tai palauttaa vain ID:n)
  - Validoidaan ennen suoritusta
  - Voi epäonnistua business-sääntöjen vuoksi
```

### Query (Kysely)

**Query** lukee dataa muuttamatta tilaa:

```
Query = "Kerro minulle jotain"
  - GetProductById    → Palauta tuote
  - GetAllProducts    → Palauta kaikki tuotteet
  - SearchProducts    → Hae tuotteita
  - GetOrderHistory   → Palauta tilaushistoria

Ominaisuudet:
  - EI muuta dataa (no side effects)
  - Palauttaa aina dataa (DTO:na)
  - Voidaan optimoida lukemiselle
  - Turvallinen kutsua milloin tahansa
```

---

## Ongelma: Yhteinen malli lukemiselle ja kirjoittamiselle

### Tyypillinen Service-luokka

```csharp
// ❌ Yksi service hoitaa kaiken
public class ProductService
{
    private readonly AppDbContext _context;

    public ProductService(AppDbContext context)
    {
        _context = context;
    }

    // READ - Tarvitsee vain muutaman kentän
    public async Task<List<ProductListDto>> GetAllAsync()
    {
        return await _context.Products
            .Select(p => new ProductListDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .ToListAsync();
    }

    // READ - Tarvitsee kaikki kentät + relaatiot
    public async Task<ProductDetailDto> GetByIdAsync(int id)
    {
        return await _context.Products
            .Include(p => p.Category)
            .Include(p => p.Reviews)
            .Where(p => p.Id == id)
            .Select(p => new ProductDetailDto { /* ... */ })
            .FirstOrDefaultAsync();
    }

    // WRITE - Validoi, luo, tallenna
    public async Task<int> CreateAsync(CreateProductDto dto)
    {
        // Validointi...
        // Business rules...
        var product = new Product { Name = dto.Name, Price = dto.Price };
        _context.Products.Add(product);
        await _context.SaveChangesAsync();
        return product.Id;
    }

    // WRITE - Validoi, hae, päivitä, tallenna
    public async Task UpdateAsync(int id, UpdateProductDto dto)
    {
        var product = await _context.Products.FindAsync(id);
        // Validointi + Business rules...
        product.Name = dto.Name;
        product.Price = dto.Price;
        await _context.SaveChangesAsync();
    }
}
```

### Ongelmat

**1. Service kasvaa valtavaksi (God Class)**

```csharp
public class ProductService  // 500+ riviä, 15+ metodia
{
    // 5 read-metodia: GetAll, GetById, Search, GetByCategory, GetPopular
    // 4 write-metodia: Create, Update, Delete, UpdateStock
    // 3 helper-metodia: Validate, MapToDto, CheckPermissions
    // → Kaikki samassa luokassa!
}
```

**2. Luku ja kirjoitus vaativat eri optimointeja**

```csharp
// READ tarvitsee: nopeat kyselyt, cachea, projection (Select)
// WRITE tarvitsee: validoinnin, transaktiot, domain logiikan, tapahtumien julkaisun

// Yhteinen malli ei ole optimaalinen kummallekaan!
```

**3. Eri DTO:t eri operaatioille**

```csharp
// Lista-näkymä: Id, Name, Price (3 kenttää)
// Detaili-näkymä: Kaikki kentät + relaatiot (20+ kenttää)
// Luominen: Name, Price, CategoryId, Description
// Päivittäminen: Id, Name, Price

// Yksi yhteinen malli ei sovi mihinkään kunnolla
```

**4. Testattavuus kärsii**

```csharp
// Haluat testata vain CreateAsync-metodia,
// mutta joudut mockaamaan koko servicen
// riippuvuudet (joita myös read-metodit käyttävät)
```

---

## Ratkaisu: Erilliset mallit

CQRS ratkaisee nämä ongelmat erottamalla luku- ja kirjoituspuolen:

### Ennen (ilman CQRS:ää)

```
Controller
    ↓
ProductService (kaikki operaatiot)
    ↓
  Database
```

### Jälkeen (CQRS)

```
Controller
    ↓                      ↓
GetAllProductsQuery    CreateProductCommand
    ↓                      ↓
QueryHandler           CommandHandler
    ↓                      ↓
  Read Model           Write Model
    ↓                      ↓
  Database             Database
```

### Käytännön ero

```csharp
// === ENNEN: Yksi service ===
public class ProductService
{
    public Task<List<ProductDto>> GetAllAsync() { /* ... */ }
    public Task<ProductDto> GetByIdAsync(int id) { /* ... */ }
    public Task<int> CreateAsync(CreateProductDto dto) { /* ... */ }
    public Task UpdateAsync(int id, UpdateProductDto dto) { /* ... */ }
    public Task DeleteAsync(int id) { /* ... */ }
}

// === JÄLKEEN: Erilliset Query- ja Command-handlerit ===

// Query-puoli (Read)
public record GetAllProductsQuery : IRequest<List<ProductDto>>;
public class GetAllProductsQueryHandler : IRequestHandler<GetAllProductsQuery, List<ProductDto>>
{
    // Optimoitu lukemiselle: projection, caching, read-only context
}

public record GetProductByIdQuery(int Id) : IRequest<ProductDto>;
public class GetProductByIdQueryHandler : IRequestHandler<GetProductByIdQuery, ProductDto>
{
    // Voi käyttää eri datanlähdettä kuin write-puoli
}

// Command-puoli (Write)
public record CreateProductCommand(string Name, decimal Price) : IRequest<int>;
public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, int>
{
    // Validointi, business rules, domain events
}

public record UpdateProductCommand(int Id, string Name, decimal Price) : IRequest;
public class UpdateProductCommandHandler : IRequestHandler<UpdateProductCommand>
{
    // Validointi, optimistic concurrency, audit trail
}
```

---

## CQRS-tasot

CQRS:ää voi soveltaa eri syvyyksillä. Ei tarvitse aina mennä äärimmäisyyksiin:

### Taso 1: Erillinen koodimalli (yleisin)

Sama tietokanta, mutta eri luokat lukemiselle ja kirjoittamiselle:

```
┌──────────────┐    ┌───────────────┐
│ Query Handler│    │Command Handler│
│  (Read DTO)  │    │ (Domain Model)│
└──────┬───────┘    └───────┬───────┘
       │                    │
       └────────┬───────────┘
                │
         ┌──────┴──────┐
         │  Sama DB    │
         └─────────────┘
```

```csharp
// Query: Käyttää kevyitä DTO:ita, projection, AsNoTracking
public class GetProductsQueryHandler : IRequestHandler<GetProductsQuery, List<ProductListDto>>
{
    private readonly AppDbContext _context;

    public async Task<List<ProductListDto>> Handle(
        GetProductsQuery request, CancellationToken ct)
    {
        return await _context.Products
            .AsNoTracking()  // Ei change trackingia → nopeampi
            .Select(p => new ProductListDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .ToListAsync(ct);
    }
}

// Command: Käyttää domain-mallia, validointia, change trackingia
public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, int>
{
    private readonly AppDbContext _context;

    public async Task<int> Handle(
        CreateProductCommand request, CancellationToken ct)
    {
        var product = new Product(request.Name, request.Price);
        product.Validate();  // Domain-validointi
        
        _context.Products.Add(product);
        await _context.SaveChangesAsync(ct);
        
        return product.Id;
    }
}
```

**Tämä on suositelluin aloitustaso.** Se tarjoaa hyvän rakenteen ilman infrastruktuurin monimutkaisuutta.

### Taso 2: Erillinen tietokantayhteys

Eri DbContext lukemiselle ja kirjoittamiselle, mutta sama tietokanta:

```
┌──────────────┐    ┌───────────────┐
│ Query Handler│    │Command Handler│
└──────┬───────┘    └───────┬───────┘
       │                    │
┌──────┴───────┐    ┌───────┴───────┐
│ReadDbContext  │    │WriteDbContext  │
│(AsNoTracking)│    │(Full tracking) │
└──────┬───────┘    └───────┬───────┘
       │                    │
       └────────┬───────────┘
                │
         ┌──────┴──────┐
         │  Sama DB    │
         └─────────────┘
```

```csharp
// Read-only DbContext
public class ReadDbContext : DbContext
{
    public ReadDbContext(DbContextOptions<ReadDbContext> options) 
        : base(options) 
    {
        ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.NoTracking;
    }
    
    public DbSet<Product> Products => Set<Product>();
}

// Write DbContext
public class WriteDbContext : DbContext
{
    public WriteDbContext(DbContextOptions<WriteDbContext> options) 
        : base(options) { }
    
    public DbSet<Product> Products => Set<Product>();
}
```

### Taso 3: Erilliset tietokannat

Eri tietokanta lukemiselle ja kirjoittamiselle (eventual consistency):

```
┌──────────────┐    ┌───────────────┐
│ Query Handler│    │Command Handler│
└──────┬───────┘    └───────┬───────┘
       │                    │
┌──────┴───────┐    ┌───────┴───────┐
│  Read DB     │←───│  Write DB     │
│ (Denormalized│    │ (Normalized)  │
│  materialized│    │               │
│  views)      │    │               │
└──────────────┘    └───────────────┘
                Synkronointi
              (events, projections)
```

> **Huom:** Taso 3 on monimutkainen ja sitä tarvitaan harvoin. Aloita aina tasosta 1 ja siirry eteenpäin vain tarpeen mukaan.

---

## CQRS käytännössä C#:lla

### Ilman MediatR:ia (manuaalinen toteutus)

CQRS:n ymmärtämiseksi on hyvä nähdä miten se toimii ilman kirjastoja:

**Query-rajapinta ja toteutus:**

```csharp
// Geneerinen Query-rajapinta
public interface IQuery<TResult> { }

// Geneerinen Query Handler -rajapinta
public interface IQueryHandler<TQuery, TResult> 
    where TQuery : IQuery<TResult>
{
    Task<TResult> HandleAsync(TQuery query, CancellationToken ct = default);
}

// Konkreettinen Query
public record GetProductByIdQuery(int Id) : IQuery<ProductDto?>;

// Konkreettinen Handler
public class GetProductByIdQueryHandler 
    : IQueryHandler<GetProductByIdQuery, ProductDto?>
{
    private readonly AppDbContext _context;

    public GetProductByIdQueryHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<ProductDto?> HandleAsync(
        GetProductByIdQuery query, CancellationToken ct)
    {
        return await _context.Products
            .AsNoTracking()
            .Where(p => p.Id == query.Id)
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .FirstOrDefaultAsync(ct);
    }
}
```

**Command-rajapinta ja toteutus:**

```csharp
// Geneerinen Command-rajapinta
public interface ICommand { }
public interface ICommand<TResult> { }

// Geneerinen Command Handler
public interface ICommandHandler<TCommand> 
    where TCommand : ICommand
{
    Task HandleAsync(TCommand command, CancellationToken ct = default);
}

public interface ICommandHandler<TCommand, TResult> 
    where TCommand : ICommand<TResult>
{
    Task<TResult> HandleAsync(TCommand command, CancellationToken ct = default);
}

// Konkreettinen Command
public record CreateProductCommand(
    string Name, 
    decimal Price) : ICommand<int>;

// Konkreettinen Handler
public class CreateProductCommandHandler 
    : ICommandHandler<CreateProductCommand, int>
{
    private readonly AppDbContext _context;

    public CreateProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<int> HandleAsync(
        CreateProductCommand command, CancellationToken ct)
    {
        var product = new Product
        {
            Name = command.Name,
            Price = command.Price
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync(ct);

        return product.Id;
    }
}
```

**Dispatcher (yksinkertainen mediator):**

```csharp
public interface IQueryDispatcher
{
    Task<TResult> DispatchAsync<TResult>(
        IQuery<TResult> query, CancellationToken ct = default);
}

public class QueryDispatcher : IQueryDispatcher
{
    private readonly IServiceProvider _serviceProvider;

    public QueryDispatcher(IServiceProvider serviceProvider)
    {
        _serviceProvider = serviceProvider;
    }

    public async Task<TResult> DispatchAsync<TResult>(
        IQuery<TResult> query, CancellationToken ct)
    {
        var handlerType = typeof(IQueryHandler<,>)
            .MakeGenericType(query.GetType(), typeof(TResult));

        dynamic handler = _serviceProvider.GetRequiredService(handlerType);
        
        return await handler.HandleAsync((dynamic)query, ct);
    }
}
```

> Kuten näet, manuaalinen toteutus vaatii paljon boilerplate-koodia. Tämän takia **MediatR** on suosituin tapa toteuttaa CQRS .NET-sovelluksissa.

---

## CQRS + MediatR

MediatR tekee CQRS:n toteutuksesta helppoa, koska `IRequest<T>` ja `IRequestHandler<T, TResult>` toimivat suoraan Command/Query-malleina.

### Kansiorakenne (Feature-based)

```
Application/
├── Features/
│   ├── Products/
│   │   ├── Commands/
│   │   │   ├── CreateProduct/
│   │   │   │   ├── CreateProductCommand.cs
│   │   │   │   ├── CreateProductCommandHandler.cs
│   │   │   │   └── CreateProductCommandValidator.cs
│   │   │   ├── UpdateProduct/
│   │   │   │   ├── UpdateProductCommand.cs
│   │   │   │   └── UpdateProductCommandHandler.cs
│   │   │   └── DeleteProduct/
│   │   │       ├── DeleteProductCommand.cs
│   │   │       └── DeleteProductCommandHandler.cs
│   │   ├── Queries/
│   │   │   ├── GetAllProducts/
│   │   │   │   ├── GetAllProductsQuery.cs
│   │   │   │   └── GetAllProductsQueryHandler.cs
│   │   │   └── GetProductById/
│   │   │       ├── GetProductByIdQuery.cs
│   │   │       └── GetProductByIdQueryHandler.cs
│   │   └── DTOs/
│   │       ├── ProductListDto.cs
│   │       └── ProductDetailDto.cs
│   └── Orders/
│       ├── Commands/
│       └── Queries/
```

### Marker-rajapinnat selkeyttämään

Voit luoda omat marker-rajapinnat erottamaan Commandit ja Queryt:

```csharp
// Marker-rajapinnat
public interface ICommand : IRequest { }
public interface ICommand<TResponse> : IRequest<TResponse> { }
public interface IQuery<TResponse> : IRequest<TResponse> { }

// Käyttö - nyt näkee heti onko kyseessä Command vai Query
public record CreateProductCommand(string Name, decimal Price) : ICommand<int>;
public record GetProductByIdQuery(int Id) : IQuery<ProductDto>;
```

### Controller MediatR:llä

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;

    public ProductsController(IMediator mediator)
    {
        _mediator = mediator;
    }

    // QUERY-operaatiot
    [HttpGet]
    public async Task<ActionResult<List<ProductListDto>>> GetAll()
    {
        return Ok(await _mediator.Send(new GetAllProductsQuery()));
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDetailDto>> GetById(int id)
    {
        var result = await _mediator.Send(new GetProductByIdQuery(id));
        return result is null ? NotFound() : Ok(result);
    }

    // COMMAND-operaatiot
    [HttpPost]
    public async Task<ActionResult<int>> Create(CreateProductCommand command)
    {
        var id = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetById), new { id }, id);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, UpdateProductCommand command)
    {
        if (id != command.Id) return BadRequest();
        await _mediator.Send(command);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        await _mediator.Send(new DeleteProductCommand(id));
        return NoContent();
    }
}
```

> Katso myös: [MediatR](../Patterns/MediatR.md) - Täydellinen MediatR-materiaali Pipeline Behavioreilla ja Notificationeilla

---

## CQRS + Clean Architecture

CQRS sopii luonnollisesti Clean Architecture -arkkitehtuuriin:

```
┌─────────────────────────────────────────┐
│              WebApi (Controllers)        │
│                    │                     │
│           IMediator.Send(...)            │
│                    │                     │
├─────────────────────────────────────────┤
│           Application Layer             │
│  ┌────────────────┬───────────────┐     │
│  │  Commands/     │  Queries/     │     │
│  │  Handlers      │  Handlers     │     │
│  │  Validators    │  DTOs         │     │
│  └────────┬───────┴───────┬───────┘     │
│           │               │             │
│     IRepository     IReadRepository     │
├─────────────────────────────────────────┤
│           Domain Layer                  │
│      Entities, Value Objects            │
├─────────────────────────────────────────┤
│         Infrastructure Layer            │
│    DbContext, Repositories, Services    │
└─────────────────────────────────────────┘
```

### Erilliset repositoryt lukemiselle ja kirjoittamiselle

```csharp
// Write Repository - Domain-malli
public interface IProductRepository
{
    Task<Product> GetByIdAsync(int id, CancellationToken ct);
    Task AddAsync(Product product, CancellationToken ct);
    Task UpdateAsync(Product product, CancellationToken ct);
    Task DeleteAsync(Product product, CancellationToken ct);
}

// Read Repository - DTO:t suoraan
public interface IProductReadRepository
{
    Task<List<ProductListDto>> GetAllAsync(CancellationToken ct);
    Task<ProductDetailDto?> GetByIdAsync(int id, CancellationToken ct);
    Task<List<ProductListDto>> SearchAsync(string term, CancellationToken ct);
}
```

---

## CQRS + Event Sourcing

CQRS yhdistetään usein **Event Sourcing** -malliin (mutta ne ovat erillisiä malleja!):

```
Command Side:                    Query Side:
                                 
CreateOrder                      
    ↓                            
Command Handler                  
    ↓                            
OrderCreatedEvent ──────→ Event Handler
    ↓                        ↓
Event Store              Read Model (denormalized)
(tapahtumahistoria)          ↓
                         Read Database
                             ↓
                         Query Handler
                             ↓
                         OrderDto
```

**Event Sourcing** tallentaa tilan muutokset tapahtumina sen sijaan, että tallentaisi nykyisen tilan:

```csharp
// Perinteinen: Tallennetaan nykyinen tila
// Order { Id: 1, Status: "Shipped", Total: 99.90 }

// Event Sourcing: Tallennetaan tapahtumat
// 1. OrderCreated { Id: 1, Total: 99.90 }
// 2. PaymentReceived { OrderId: 1, Amount: 99.90 }
// 3. OrderShipped { OrderId: 1, TrackingNumber: "ABC123" }
// → Nykyinen tila lasketaan tapahtumista
```

> **Huom:** Event Sourcing lisää merkittävästi monimutkaisuutta. Käytä vain kun oikeasti tarvitset täydellistä tapahtumahistoriaa (esim. pankkijärjestelmät, kirjanpito).

---

## Milloin käyttää CQRS:ää?

### Käytä CQRS:ää kun:

| Tilanne | Miksi CQRS auttaa |
|---|---|
| ✅ Luku- ja kirjoitusoperaatiot ovat hyvin erilaisia | Omat optimoinnit kummallekin |
| ✅ Sovelluksessa on paljon enemmän lukuoperaatioita | Query-puolen voi skaalata erikseen |
| ✅ Domain-logiikka on monimutkaista | Command-puolelle oma rikas domain-malli |
| ✅ Tiimissä useita kehittäjiä | Vähemmän merge-konflikteja |
| ✅ Käytät Clean Architecture -arkkitehtuuria | Luonnollinen yhteensopivuus |
| ✅ Tarvitset Pipeline Behavioreita | Validointi, logging, caching ketjutettuna |

### Älä käytä CQRS:ää kun:

| Tilanne | Miksi ei |
|---|---|
| ❌ Yksinkertainen CRUD-sovellus | Lisää turhaa monimutkaisuutta |
| ❌ Luku- ja kirjoitusmallit ovat identtisiä | Ei hyötyä erottamisesta |
| ❌ Pieni projekti, 1-2 kehittäjää | Overhead ylittää hyödyt |
| ❌ Ei tarvetta cross-cutting concerneille | Pipeline Behaviorit turhia |

---

## Best Practices

### 1. Aloita yksinkertaisesta (Taso 1)

```csharp
// ✅ HYVÄ: Aloita yhdellä tietokannalla, erillisillä handlereilla
// Siirry monimutkaisempaan vasta kun tarve ilmenee

// ❌ HUONO: Aloita heti erillisillä tietokannoilla ja Event Sourcingilla
```

### 2. Nimeä Commands ja Queries johdonmukaisesti

```csharp
// ✅ HYVÄ: Selkeä nimeämiskonventio
// Commands: [Verbi][Kohde]Command
public record CreateProductCommand(...) : IRequest<int>;
public record UpdateProductPriceCommand(...) : IRequest;
public record DeleteProductCommand(...) : IRequest;

// Queries: Get[Kohde(t)][Ehto]Query
public record GetAllProductsQuery : IRequest<List<ProductDto>>;
public record GetProductByIdQuery(int Id) : IRequest<ProductDto>;
public record GetProductsByCategoryQuery(int CategoryId) : IRequest<List<ProductDto>>;
```

### 3. Query-handlerit: AsNoTracking ja Projection

```csharp
// ✅ HYVÄ: Optimoitu lukemiselle
public async Task<List<ProductListDto>> Handle(
    GetAllProductsQuery request, CancellationToken ct)
{
    return await _context.Products
        .AsNoTracking()                    // Ei change trackingia
        .Select(p => new ProductListDto    // Projection: vain tarvittavat kentät
        {
            Id = p.Id,
            Name = p.Name,
            Price = p.Price
        })
        .ToListAsync(ct);
}

// ❌ HUONO: Hakee kaiken ja mapittaa muistissa
public async Task<List<ProductListDto>> Handle(
    GetAllProductsQuery request, CancellationToken ct)
{
    var products = await _context.Products
        .Include(p => p.Category)
        .Include(p => p.Reviews)
        .ToListAsync(ct);  // Kaikki kentät + relaatiot muistiin
    
    return products.Select(p => new ProductListDto { ... }).ToList();
}
```

### 4. Yksi Handler = Yksi operaatio

```csharp
// ✅ HYVÄ: Jokainen handler tekee yhden asian
public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, int> { }
public class UpdateProductCommandHandler : IRequestHandler<UpdateProductCommand> { }

// ❌ HUONO: Yksi handler hoitaa monta asiaa
public class ProductCommandHandler : 
    IRequestHandler<CreateProductCommand, int>,
    IRequestHandler<UpdateProductCommand>,
    IRequestHandler<DeleteProductCommand> { }
```

---

## Anti-patterns

### 1. "CQRS kaikkeen" -ajattelu

```csharp
// ❌ HUONO: CQRS yksinkertaiselle asetustiedon hakuun
public record GetAppSettingsQuery : IRequest<AppSettings>;

// ✅ HYVÄ: Yksinkertainen asia suoraan
var settings = _configuration.GetSection("App").Get<AppSettings>();
```

### 2. Query joka muuttaa tilaa

```csharp
// ❌ HUONO: Query tekee sivuvaikutuksen (CQS-rikkomus!)
public class GetProductQueryHandler : IRequestHandler<GetProductQuery, ProductDto>
{
    public async Task<ProductDto> Handle(GetProductQuery request, CancellationToken ct)
    {
        var product = await _context.Products.FindAsync(request.Id);
        product.ViewCount++;                      // ← Muuttaa tilaa!
        await _context.SaveChangesAsync(ct);      // ← Sivuvaikutus!
        return new ProductDto { ... };
    }
}

// ✅ HYVÄ: Erillinen command katselukerroille
public record IncrementProductViewCountCommand(int ProductId) : IRequest;
```

### 3. Command joka palauttaa liikaa dataa

```csharp
// ❌ HUONO: Command palauttaa koko olion
public record CreateProductCommand(...) : IRequest<ProductDetailDto>;

// ✅ HYVÄ: Command palauttaa vain ID:n (tai ei mitään)
public record CreateProductCommand(...) : IRequest<int>;
// → Client hakee detailit erikseen: GetProductByIdQuery
```

---

## Yhteenveto

### CQRS pähkinänkuoressa

| Käsite | Kuvaus |
|---|---|
| **CQS** | Metodi joko lukee tai kirjoittaa, ei molempia |
| **CQRS** | Sovellustason CQS: erilliset mallit lukemiselle ja kirjoittamiselle |
| **Command** | Muuttaa tilaa (Create, Update, Delete) |
| **Query** | Lukee dataa (Get, Search, List) |
| **Taso 1** | Erillinen koodimalli, sama tietokanta (suositelluin aloitustaso) |
| **Taso 2** | Erillinen tietokantayhteys (ReadDbContext / WriteDbContext) |
| **Taso 3** | Erilliset tietokannat + Event Sourcing (harvoin tarpeellinen) |

### Hyödyt

- Selkeä vastuunjako (Single Responsibility)
- Optimoitu lukeminen ja kirjoittaminen erikseen
- Helpompi testata (yksi handler kerrallaan)
- Skaalautuu isoihin projekteihin
- Luonnollinen yhteensopivuus Clean Architecturen kanssa
- Pipeline Behaviors cross-cutting concerneille

### Hyödyllisiä linkkejä

- [CQRS Pattern - Microsoft Docs](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) - Virallinen dokumentaatio
- [Martin Fowler: CQRS](https://martinfowler.com/bliki/CQRS.html) - Alkuperäinen artikkeli
- [Greg Young: CQRS Documents](https://cqrs.files.wordpress.com/2010/11/cqrs_documents.pdf) - CQRS:n keksijän dokumentaatio
- [MediatR](../Patterns/MediatR.md) - MediatR-kirjasto CQRS:n toteutukseen

---

[Takaisin: Arkkitehtuuri](README.md) | [Takaisin: Edistyneet aiheet](../README.md)
