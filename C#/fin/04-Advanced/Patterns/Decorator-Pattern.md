# Decorator Pattern

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on Decorator Pattern?](#mikä-on-decorator-pattern)
3. [Milloin käyttää?](#milloin-käyttää)
4. [Toteutus C#:lla](#toteutus-clla)
5. [Käytännön esimerkkejä](#käytännön-esimerkkejä)
6. [Decorator vs Inheritance](#decorator-vs-inheritance)
7. [Best Practices](#best-practices)
8. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Decorator Pattern** on suunnittelumalli, joka mahdollistaa toiminnallisuuden lisäämisen olemassa olevaan olioon dynaamisesti ilman että muutetaan sen alkuperäistä koodia.

**Gang of Four määritelmä:**
> "Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality."

---

## Mikä on Decorator Pattern?

### Perusidea

Decorator **wrappaa** (käärii) alkuperäisen olion ja lisää siihen uutta toiminnallisuutta:

```
Original Object
      ↓
   Decorator (wraps)
      ↓
  Enhanced Object
```

### Visuaalinen esimerkki

**Ilman Decorator:ia:**

```csharp
class Coffee
{
    public decimal Cost() => 2.0m;
}
```

**Decorator:ien kanssa:**

```csharp
Coffee
  → MilkDecorator (wraps Coffee)
    → SugarDecorator (wraps MilkDecorator)
      → WhipCreamDecorator (wraps SugarDecorator)
        = Decorated Coffee (Cost = 2.0 + 0.5 + 0.2 + 0.7 = 3.4€)
```

---

## Milloin käyttää?

### Käyttötapaukset

**Käytä Decorator:ia kun:**

1. ✅ Haluat lisätä toiminnallisuutta ilman alkuperäisen koodin muuttamista
2. ✅ Toiminnallisuus pitää olla lisättävissä dynaamisesti runtime:ssa
3. ✅ Inheritance johtaisi "class explosion" -ongelmaan
4. ✅ Haluat noudattaa Open/Closed Principle:a
5. ✅ Tarvitset ketjutettavia toiminnallisuuksia

**Esimerkkejä:**

- **Caching** - Lisää caching repository:lle
- **Logging** - Lisää logging palvelulle
- **Validation** - Lisää validointi ennen toimintoa
- **Authorization** - Lisää oikeustarkistukset
- **Retry logic** - Lisää uudelleenyrityslogiikka
- **Performance monitoring** - Lisää ajanmittaus

---

## Toteutus C#:lla

### Perusrakenne

```csharp
// 1. Component Interface
public interface IComponent
{
    string Operation();
}

// 2. Concrete Component (alkuperäinen)
public class ConcreteComponent : IComponent
{
    public string Operation()
    {
        return "ConcreteComponent";
    }
}

// 3. Base Decorator
public abstract class Decorator : IComponent
{
    protected IComponent _component;
    
    public Decorator(IComponent component)
    {
        _component = component;
    }
    
    public virtual string Operation()
    {
        return _component.Operation();
    }
}

// 4. Concrete Decorators
public class ConcreteDecoratorA : Decorator
{
    public ConcreteDecoratorA(IComponent component) : base(component)
    {
    }
    
    public override string Operation()
    {
        return $"ConcreteDecoratorA({base.Operation()})";
    }
}

public class ConcreteDecoratorB : Decorator
{
    public ConcreteDecoratorB(IComponent component) : base(component)
    {
    }
    
    public override string Operation()
    {
        return $"ConcreteDecoratorB({base.Operation()})";
    }
}
```

### Käyttö

```csharp
// Alkuperäinen
IComponent component = new ConcreteComponent();
Console.WriteLine(component.Operation());
// Output: ConcreteComponent

// Yksi decorator
component = new ConcreteDecoratorA(component);
Console.WriteLine(component.Operation());
// Output: ConcreteDecoratorA(ConcreteComponent)

// Toinen decorator (ketjutus)
component = new ConcreteDecoratorB(component);
Console.WriteLine(component.Operation());
// Output: ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))
```

---

## Käytännön esimerkkejä

### Esimerkki 1: Caching Decorator

**Ongelma:** Haluat lisätä caching:in repository:lle ilman että muutat alkuperäistä koodia.

```csharp
// 1. Interface
public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id);
    Task<IEnumerable<Product>> GetAllAsync();
}

// 2. Alkuperäinen Repository (ei tiedä cachesta)
public class ProductRepository : IProductRepository
{
    private readonly DbContext _db;
    
    public ProductRepository(DbContext db)
    {
        _db = db;
    }
    
    public async Task<Product?> GetByIdAsync(int id)
    {
        return await _db.Products.FindAsync(id);
    }
    
    public async Task<IEnumerable<Product>> GetAllAsync()
    {
        return await _db.Products.ToListAsync();
    }
}

// 3. Cached Decorator (lisää cachingin)
public class CachedProductRepository : IProductRepository
{
    private readonly IProductRepository _inner;
    private readonly IMemoryCache _cache;
    
    public CachedProductRepository(IProductRepository inner, IMemoryCache cache)
    {
        _inner = inner;
        _cache = cache;
    }
    
    public async Task<Product?> GetByIdAsync(int id)
    {
        string cacheKey = $"product_{id}";
        
        // Yritä cachesta
        if (_cache.TryGetValue(cacheKey, out Product? cached))
            return cached;
        
        // Delegoi alkuperäiselle
        var product = await _inner.GetByIdAsync(id);
        
        // Tallenna cacheen
        if (product != null)
            _cache.Set(cacheKey, product, TimeSpan.FromMinutes(10));
        
        return product;
    }
    
    public async Task<IEnumerable<Product>> GetAllAsync()
    {
        const string cacheKey = "products_all";
        
        if (_cache.TryGetValue(cacheKey, out IEnumerable<Product>? cached))
            return cached!;
        
        var products = await _inner.GetAllAsync();
        
        _cache.Set(cacheKey, products, TimeSpan.FromMinutes(10));
        return products;
    }
}
```

**DI Registration:**

```csharp
services.AddMemoryCache();

// Alkuperäinen
services.AddScoped<ProductRepository>();

// Decorator
services.AddScoped<IProductRepository>(provider =>
{
    var db = provider.GetRequiredService<DbContext>();
    var cache = provider.GetRequiredService<IMemoryCache>();
    
    var inner = new ProductRepository(db);
    return new CachedProductRepository(inner, cache);
});
```

**Käyttö:**

```csharp
public class ProductService
{
    private readonly IProductRepository _repository;  // ← Saa CachedProductRepository:n
    
    public ProductService(IProductRepository repository)
    {
        _repository = repository;
    }
    
    public async Task<Product?> GetProductAsync(int id)
    {
        // Automaattisesti käyttää cachea
        return await _repository.GetByIdAsync(id);
    }
}
```

### Esimerkki 2: Logging Decorator

```csharp
public interface IOrderService
{
    Task<Order> CreateOrderAsync(CreateOrderDto dto);
}

public class OrderService : IOrderService
{
    public async Task<Order> CreateOrderAsync(CreateOrderDto dto)
    {
        // Business logic
        var order = new Order { ... };
        await _repository.SaveAsync(order);
        return order;
    }
}

// Logging Decorator
public class LoggingOrderService : IOrderService
{
    private readonly IOrderService _inner;
    private readonly ILogger<LoggingOrderService> _logger;
    
    public LoggingOrderService(IOrderService inner, ILogger<LoggingOrderService> logger)
    {
        _inner = inner;
        _logger = logger;
    }
    
    public async Task<Order> CreateOrderAsync(CreateOrderDto dto)
    {
        _logger.LogInformation("Creating order for {UserId}", dto.UserId);
        
        var stopwatch = Stopwatch.StartNew();
        
        try
        {
            var order = await _inner.CreateOrderAsync(dto);
            
            stopwatch.Stop();
            _logger.LogInformation(
                "Order {OrderId} created successfully in {ElapsedMs}ms", 
                order.Id, 
                stopwatch.ElapsedMilliseconds);
            
            return order;
        }
        catch (Exception ex)
        {
            stopwatch.Stop();
            _logger.LogError(ex, 
                "Failed to create order for {UserId} after {ElapsedMs}ms", 
                dto.UserId, 
                stopwatch.ElapsedMilliseconds);
            throw;
        }
    }
}
```

### Esimerkki 3: Retry Decorator

```csharp
public class RetryOrderService : IOrderService
{
    private readonly IOrderService _inner;
    private readonly int _maxRetries = 3;
    
    public RetryOrderService(IOrderService inner)
    {
        _inner = inner;
    }
    
    public async Task<Order> CreateOrderAsync(CreateOrderDto dto)
    {
        int attempt = 0;
        
        while (true)
        {
            attempt++;
            
            try
            {
                return await _inner.CreateOrderAsync(dto);
            }
            catch (Exception ex) when (attempt < _maxRetries && IsTransient(ex))
            {
                await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, attempt)));  // Exponential backoff
                // Retry
            }
        }
    }
    
    private bool IsTransient(Exception ex)
    {
        // Tarkista onko transient error (timeout, connection, etc.)
        return ex is TimeoutException || ex is HttpRequestException;
    }
}
```

### Esimerkki 4: Ketjutetut Decoratorit

**Voit ketjuttaa useita decorator:eja:**

```csharp
services.AddScoped<IOrderService>(provider =>
{
    var logger = provider.GetRequiredService<ILogger<LoggingOrderService>>();
    var cache = provider.GetRequiredService<IMemoryCache>();
    
    // 1. Alkuperäinen
    IOrderService service = new OrderService();
    
    // 2. Lisää retry
    service = new RetryOrderService(service);
    
    // 3. Lisää caching
    service = new CachedOrderService(service, cache);
    
    // 4. Lisää logging (uloin, logittaa kaikki)
    service = new LoggingOrderService(service, logger);
    
    return service;
});
```

**Suoritusjärjestys:**

```
Request
  ↓
LoggingOrderService (log start)
  ↓
CachedOrderService (check cache)
  ↓ (cache miss)
RetryOrderService (retry on error)
  ↓
OrderService (business logic)
  ↓
RetryOrderService (success)
  ↓
CachedOrderService (save to cache)
  ↓
LoggingOrderService (log success)
  ↓
Response
```

---

## Decorator vs Inheritance

### Inheritance-ongelma

**Kuvittele että tarvitset:**
- OrderService
- OrderService + Logging
- OrderService + Caching
- OrderService + Logging + Caching
- OrderService + Retry
- OrderService + Retry + Logging
- OrderService + Retry + Caching
- OrderService + Retry + Logging + Caching

→ **8 luokkaa!** (2³ kombinaatiota)

**Inheritance:**

```csharp
class OrderService { }
class LoggingOrderService : OrderService { }
class CachedOrderService : OrderService { }
class LoggingCachedOrderService : LoggingOrderService { }  // ← Duplikaatiota!
// ... ja niin edelleen
```

**Ongelma:**
- ❌ Class explosion (eksponentiaalinen määrä luokkia)
- ❌ Ei dynaamista, compile-time valinta
- ❌ Vaikea ylläpitää

### Decorator-ratkaisu

**Decorator Pattern:**

```csharp
// Vain 4 luokkaa:
class OrderService { }
class LoggingOrderService : IOrderService { }
class CachedOrderService : IOrderService { }
class RetryOrderService : IOrderService { }

// Ketjutetaan runtime:ssa
IOrderService service = new OrderService();
service = new RetryOrderService(service);
service = new CachedOrderService(service);
service = new LoggingOrderService(service);
```

**Edut:**
- ✅ Vain N luokkaa (lineaarinen)
- ✅ Dynaaminen, runtime-valinta
- ✅ Helppo ylläpitää
- ✅ Open/Closed Principle

### Vertailu

| Aspekti | Inheritance | Decorator |
|---------|-------------|-----------|
| **Luokkien määrä** | 2ⁿ (eksponentiaalinen) | N (lineaarinen) |
| **Joustavuus** | Compile-time | Runtime |
| **Ylläpito** | Vaikea | Helppo |
| **Ketjutus** | Ei mahdollinen | Kyllä |
| **Open/Closed** | Rikkouu | Noudattaa |

---

## Best Practices

### 1. Käytä interfacea

**❌ Älä:**

```csharp
public class CachedProductRepository : ProductRepository  // ← Inheritance
{
    // ...
}
```

**✅ Käytä interfacea:**

```csharp
public class CachedProductRepository : IProductRepository  // ← Interface
{
    private readonly IProductRepository _inner;
    // ...
}
```

**Miksi:**
- Parempi testattavuus
- Ei riipu konkreettisesta toteutuksesta
- Voi wrappaa mitä tahansa IProductRepository-toteutusta

### 2. Delegoi kaikki metodit

**❌ Älä:**

```csharp
public class CachedProductRepository : IProductRepository
{
    public async Task<Product?> GetByIdAsync(int id)
    {
        // Caching logic
    }
    
    // ← GetAllAsync puuttuu! Compile error.
}
```

**✅ Toteuta kaikki:**

```csharp
public class CachedProductRepository : IProductRepository
{
    public async Task<Product?> GetByIdAsync(int id)
    {
        // Caching logic
    }
    
    public async Task<IEnumerable<Product>> GetAllAsync()
    {
        return await _inner.GetAllAsync();  // ← Delegoi
    }
}
```

### 3. Single Responsibility

**Jokainen decorator tekee vain yhden asian:**

```csharp
// ✅ Hyvä: Vain caching
public class CachedProductRepository : IProductRepository { }

// ✅ Hyvä: Vain logging
public class LoggingProductRepository : IProductRepository { }

// ❌ Huono: Caching + Logging
public class CachedLoggingProductRepository : IProductRepository { }
```

### 4. Nimeä selvästi

```csharp
// ✅ Hyvä
CachedProductRepository
LoggingOrderService
RetryHttpClient

// ❌ Huono
ProductRepositoryDecorator  // ← Mikä decorator?
EnhancedOrderService        // ← Mitä "enhanced"?
```

### 5. DI-rekisteröinti järjestyksessä

```csharp
// Uloin decorator rekisteröidään viimeisenä
services.AddScoped<IOrderService>(provider =>
{
    IOrderService service = new OrderService();
    
    service = new RetryOrderService(service);      // ← Sisin
    service = new CachedOrderService(service);     // ← Keskimmäinen
    service = new LoggingOrderService(service);    // ← Uloin
    
    return service;
});
```

**Suoritus:**
```
Request → Logging → Cache → Retry → OrderService
```

---

## Yhteenveto

### Milloin käyttää Decorator:ia?

**Käytä kun:**
- ✅ Haluat lisätä toiminnallisuutta ilman alkuperäisen koodin muuttamista (Open/Closed)
- ✅ Tarvitset dynaamista toiminnallisuuden lisäystä runtime:ssa
- ✅ Inheritance johtaisi "class explosion" -ongelmaan
- ✅ Haluat ketjuttaa toiminnallisuuksia

**Älä käytä kun:**
- ❌ Tarvitset vain yhden lisätoiminnallisuuden (inheritance riittää)
- ❌ Interface muuttuu usein (kaikki decoratorit pitää päivittää)
- ❌ Performance on kriittinen (decorator lisää overhead:ia)

### Yleisimmät käyttötapaukset

1. **Caching** - Lisää caching repository:lle
2. **Logging** - Lisää logging palvelulle
3. **Retry** - Lisää uudelleenyrityslogiikka
4. **Authorization** - Lisää oikeustarkistukset
5. **Validation** - Lisää validointi
6. **Monitoring** - Lisää performance-mittaus

### Key Takeaways

1. **Decorator wrappaa** alkuperäisen olion ja lisää toiminnallisuutta
2. **Noudattaa Open/Closed** - Ei muuta alkuperäistä koodia
3. **Ketjutettava** - Voit yhdistää useita decorator:eja
4. **Parempi kuin inheritance** - Ei class explosion -ongelmaa
5. **Käytä interfacea** - Parempi testattavuus ja joustavuus

---

## Lisämateriaali

### Ulkoiset linkit

- [Refactoring Guru: Decorator Pattern](https://refactoring.guru/design-patterns/decorator)
- [Microsoft: Decorator Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/decorator)
- [Gang of Four: Design Patterns](https://en.wikipedia.org/wiki/Design_Patterns)

### Liittyvät aiheet

- [Caching](Caching.md)
- [Design Patterns](../Design-Patterns.md)
- [SOLID Principles](../Design-Principles.md)

### Tehtävät

- **Clean Architecture API: Part 5 - Caching** *(kurssitehtävä Moodlessa)*

---

**Hyvää decorator-matkaa!** Käytä decoratoreita lisätäksesi toiminnallisuutta ilman alkuperäisen koodin muuttamista. 🎨
