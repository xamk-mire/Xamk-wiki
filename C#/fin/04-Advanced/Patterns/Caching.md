# Caching (Välimuistitus)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi caching on tärkeä?](#miksi-caching-on-tärkeä)
3. [Caching-strategiat](#caching-strategiat)
4. [Cache Levels](#cache-levels)
5. [ASP.NET Core Caching](#aspnet-core-caching)
6. [Cache Invalidation](#cache-invalidation)
7. [Decorator Pattern cachingille](#decorator-pattern-cachingille)
8. [Distributed Caching](#distributed-caching)
9. [Best Practices](#best-practices)
10. [Anti-patterns](#anti-patterns)
11. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Caching** (välimuistitus) on tekniikka, jossa usein käytetyt tai kalliit tulokset tallennetaan väliaikaisesti muistiin. Caching on yksi tehokkaimmista tavoista parantaa sovelluksen suorituskykyä.

**Perusidea:**

```
Ilman cachea:
User → API → Database (50ms)
User → API → Database (50ms)  ← Sama kysely!
User → API → Database (50ms)  ← Sama kysely taas!

Cachella:
User → API → Database (50ms) → Tallenna cacheen
User → API → Cache (0.5ms)    ✅ 100× nopeampi!
User → API → Cache (0.5ms)    ✅
```

---

## Miksi caching on tärkeä?

### Ongelma: Toistuvat kyselyt

**Tyypillinen skenaario:**

```csharp
// Käyttäjä lataa tuotesivun
var product = await _db.Products.FindAsync(123);  // 50ms

// Käyttäjä refreshaa sivun
var product = await _db.Products.FindAsync(123);  // 50ms ← Sama data!

// Toinen käyttäjä katsoo samaa tuotetta
var product = await _db.Products.FindAsync(123);  // 50ms ← Sama data taas!
```

**Ongelma:**
- Sama data haetaan 3 kertaa
- Joka kerta 50ms latenssi
- Database tekee samaa työtä yhä uudelleen

### Ratkaisu: Caching

```csharp
// Käyttäjä lataa tuotesivun
var product = await GetProductAsync(123);  // 50ms → Cache

// Käyttäjä refreshaa sivun
var product = await GetProductAsync(123);  // 0.5ms ← Cachesta!

// Toinen käyttäjä katsoo samaa tuotetta
var product = await GetProductAsync(123);  // 0.5ms ← Cachesta!
```

**Edut:**
- ✅ **100× nopeampi** vastausaika (0.5ms vs 50ms)
- ✅ **90% vähemmän** database-kyselyitä
- ✅ **Parempi UX** - Instant response
- ✅ **Alhaisemmat kustannukset** - Vähemmän database CPU/IOPS

### Performance-vertailu

| Metrikka | Ilman cachea | Cachella | Parannus |
|----------|--------------|----------|----------|
| Vastausaika | 50ms | 0.5ms | **100×** |
| DB kyselyt/min | 1000 | 100 | **90% vähennys** |
| DB CPU | 80% | 10% | **88% vähennys** |
| Kustannukset | 200€/kk | 50€/kk | **75% säästö** |

---

## Caching-strategiat

### 1. Cache-Aside (Lazy Loading)

**Yleisin strategia.**

```csharp
public async Task<Product> GetProductAsync(int id)
{
    // 1. Yritä hakea cachesta
    if (_cache.TryGetValue($"product_{id}", out Product? cached))
        return cached;
    
    // 2. Ei löytynyt → Hae tietokannasta
    var product = await _db.Products.FindAsync(id);
    
    // 3. Tallenna cacheen
    _cache.Set($"product_{id}", product, TimeSpan.FromMinutes(10));
    
    return product;
}
```

**Sopii:**
- Read-heavy workloads
- Data joka ei muutu usein
- Yleisin strategia

**Edut:**
- ✅ Yksinkertainen
- ✅ Cache täyttyy vain tarvittavalla datalla

**Haitat:**
- ❌ Cache miss on hidas (database + cache write)

### 2. Read-Through Cache

**Cache käsittelee automaattisesti database-kyselyt.**

```csharp
// Cache wrapper hoitaa database-haun automaattisesti
public class CachedRepository<T>
{
    public async Task<T?> GetByIdAsync(int id)
    {
        return await _cache.GetOrCreateAsync(
            $"{typeof(T).Name}_{id}",
            async entry =>
            {
                entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10);
                return await _db.Set<T>().FindAsync(id);
            });
    }
}
```

**Sopii:**
- Abstraktoitu cache-logiikka
- Repository Pattern
- Decorator Pattern

### 3. Write-Through Cache

**Kirjoitus menee ensin cacheen, sitten DB:hen.**

```csharp
public async Task UpdateProductAsync(Product product)
{
    // 1. Päivitä tietokanta
    await _db.UpdateAsync(product);
    
    // 2. Päivitä cache
    _cache.Set($"product_{product.Id}", product, TimeSpan.FromMinutes(10));
}
```

**Sopii:**
- Write-heavy workloads
- Data pitää olla aina ajan tasalla

**Haitat:**
- ❌ Jokainen kirjoitus on hidas (DB + cache)

### 4. Write-Behind (Write-Back) Cache

**Kirjoitus menee ensin cacheen, DB päivitetään asynkronisesti.**

```csharp
public async Task UpdateProductAsync(Product product)
{
    // 1. Päivitä heti cache
    _cache.Set($"product_{product.Id}", product);
    
    // 2. Lisää queue:hun (background job päivittää DB:n)
    await _updateQueue.EnqueueAsync(product);
}
```

**Sopii:**
- Erittäin korkea throughput
- Eventual consistency OK
- Logging, analytics

**Haitat:**
- ❌ Data voi kadota jos cache kaatuu
- ❌ Monimutkainen

### 5. Cache-on-Demand (Refresh-Ahead)

**Cache päivitetään ennen kuin se vanhenee.**

```csharp
var cacheOptions = new MemoryCacheEntryOptions()
    .SetAbsoluteExpiration(TimeSpan.FromMinutes(60))
    .RegisterPostEvictionCallback((key, value, reason, state) =>
    {
        if (reason == EvictionReason.Expired)
        {
            // Lataa uudelleen ennen kuin joku kysyy
            Task.Run(() => RefreshCacheAsync(key));
        }
    });
```

**Sopii:**
- Data jota käytetään paljon
- Cache miss on kallis

---

## Cache Levels

### 1. Application-level Cache (In-Memory)

```csharp
// IMemoryCache - Sovelluksen muistissa
builder.Services.AddMemoryCache();

public class ProductService
{
    private readonly IMemoryCache _cache;
    
    public ProductService(IMemoryCache cache)
    {
        _cache = cache;
    }
}
```

**Edut:**
- ⚡ Erittäin nopea (nanosekunteja)
- ✅ Yksinkertainen
- ✅ Sisäänrakennettu .NET:iin

**Haitat:**
- ❌ Ei jaettu servereiden välillä
- ❌ Häviää sovelluksen restartin yhteydessä
- ❌ Rajoitettu muisti

**Käyttö:**
- Yksittäinen server
- Kehitys
- Pienet sovellukset

### 2. Distributed Cache (Redis, Memcached)

```csharp
// Redis - Jaettu cache
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "localhost:6379";
});

public class ProductService
{
    private readonly IDistributedCache _cache;
    
    public ProductService(IDistributedCache cache)
    {
        _cache = cache;
    }
}
```

**Edut:**
- ✅ Jaettu monen serverin välillä
- ✅ Skaalautuu hyvin
- ✅ Persistenssi (Redis)

**Haitat:**
- ❌ Hitaampi kuin in-memory (verkko-overhead)
- ❌ Vaatii erillisen palvelimen

**Käyttö:**
- Load-balanced API:t (monta serveriä)
- Microservices
- Tuotanto

### 3. HTTP Response Cache

```csharp
[ResponseCache(Duration = 60)]
[HttpGet("{id}")]
public async Task<IActionResult> GetProduct(int id)
{
    var product = await _service.GetProductAsync(id);
    return Ok(product);
}
```

**Edut:**
- ✅ Browser cachettaa automaattisesti
- ✅ Vähentää API-kuormaa

**Haitat:**
- ❌ Ei hallintaa cachetusta datasta
- ❌ Cache ei päivity heti

### 4. CDN Cache (Content Delivery Network)

**Staattinen sisältö (kuvat, CSS, JS) cachetetaan CDN:ssä.**

```csharp
// Esim. Azure CDN, CloudFlare, AWS CloudFront
// Käyttäjä: Helsinki → CDN: Amsterdam (10ms)
// vs.
// Käyttäjä: Helsinki → Server: USA (150ms)
```

---

## ASP.NET Core Caching

### IMemoryCache

**Peruskäyttö:**

```csharp
public class ProductService
{
    private readonly IMemoryCache _cache;
    private readonly ProductRepository _repository;
    
    public ProductService(IMemoryCache cache, ProductRepository repository)
    {
        _cache = cache;
        _repository = repository;
    }
    
    public async Task<Product?> GetProductAsync(int id)
    {
        string cacheKey = $"product_{id}";
        
        // Yritä hakea cachesta
        if (_cache.TryGetValue(cacheKey, out Product? cached))
        {
            Console.WriteLine($"[CACHE HIT] Product {id}");
            return cached;
        }
        
        // Ei löytynyt → Hae tietokannasta
        Console.WriteLine($"[CACHE MISS] Product {id}");
        var product = await _repository.GetByIdAsync(id);
        
        if (product != null)
        {
            // Tallenna cacheen
            var cacheOptions = new MemoryCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
            };
            _cache.Set(cacheKey, product, cacheOptions);
        }
        
        return product;
    }
}
```

### Cache Options

#### 1. Absolute Expiration

```csharp
var options = new MemoryCacheEntryOptions
{
    // Vanhenee 10 minuutin jälkeen (riippumatta käytöstä)
    AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
};
```

**Käyttö:**
- Data joka vanhenee tietyn ajan jälkeen
- Esim. API rate limits, session tokens

#### 2. Sliding Expiration

```csharp
var options = new MemoryCacheEntryOptions
{
    // Vanhenee jos ei käytetä 5 minuuttiin
    SlidingExpiration = TimeSpan.FromMinutes(5)
};
```

**Käyttö:**
- Data joka käytetään usein (pysyy cachessa)
- Harvinaiset datat vanhenevat automaattisesti

#### 3. Yhdistetty (Absolute + Sliding)

```csharp
var options = new MemoryCacheEntryOptions
{
    SlidingExpiration = TimeSpan.FromMinutes(5),
    AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
};
```

**Käyttö:**
- Sliding: Pysyy jos käytetään
- Absolute: Vanhenee viimeistään 1h jälkeen

#### 4. Priority

```csharp
var options = new MemoryCacheEntryOptions
{
    Priority = CacheItemPriority.High  // Low, Normal, High, NeverRemove
};
```

**Käyttö:**
- `High`: Tärkeä data (resources, konfiguraatio)
- `Normal`: Normaali data
- `Low`: Väliaikainen data

Kun muisti loppuu, Low-priority poistetaan ensin.

#### 5. Size Limit

```csharp
// Cache size limit
builder.Services.AddMemoryCache(options =>
{
    options.SizeLimit = 1024;  // 1024 "units"
});

// Per-item size
var options = new MemoryCacheEntryOptions
{
    Size = 1  // Tämä item vie 1 "unit"
};
```

### GetOrCreate Pattern

```csharp
public async Task<Product?> GetProductAsync(int id)
{
    return await _cache.GetOrCreateAsync(
        $"product_{id}",
        async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10);
            entry.Priority = CacheItemPriority.High;
            
            // Tämä suoritetaan vain jos cache miss
            return await _repository.GetByIdAsync(id);
        });
}
```

---

## Cache Invalidation

> "There are only two hard things in Computer Science: cache invalidation and naming things."
> — Phil Karlton

### Ongelma

**Cache voi sisältää vanhentunutta dataa:**

```csharp
// Käyttäjä hakee tuotteen
var product = await GetProductAsync(1);  // Cache: { name: "Old Name" }

// Admin päivittää tuotteen
await UpdateProductAsync(1, "New Name");  // DB: { name: "New Name" }

// Käyttäjä hakee uudelleen
var product = await GetProductAsync(1);  // Cache: { name: "Old Name" } ❌
```

### Ratkaisu 1: Time-based Invalidation

**Cache vanhenee automaattisesti.**

```csharp
_cache.Set("product_1", product, TimeSpan.FromMinutes(5));
```

**Edut:**
- ✅ Yksinkertainen
- ✅ Ei ylläpitoa

**Haitat:**
- ❌ Data voi olla vanhentunutta 5 minuuttia
- ❌ Cache voi vanhentua liian aikaisin

### Ratkaisu 2: Event-based Invalidation

**Poista cache kun data muuttuu.**

```csharp
public async Task UpdateProductAsync(Product product)
{
    // 1. Päivitä tietokanta
    await _repository.UpdateAsync(product);
    
    // 2. Poista cache
    _cache.Remove($"product_{product.Id}");
    _cache.Remove("products_all");  // Lista-cache
}
```

**Edut:**
- ✅ Data aina ajantasalla

**Haitat:**
- ❌ Pitää muistaa poistaa cache joka paikassa

### Ratkaisu 3: Cache Tags

**Ryhmittele cachet tagien mukaan.**

```csharp
// Tallenna tag:ien kanssa
_cache.Set("product_1", product, new MemoryCacheEntryOptions()
    .AddTag("products"));

_cache.Set("product_2", product, new MemoryCacheEntryOptions()
    .AddTag("products"));

// Poista kaikki "products"-tagilla
_cache.RemoveByTag("products");
```

**Huom:** Vaatii extension-kirjaston (esim. `EasyCaching`).

### Ratkaisu 4: Cache Dependencies

```csharp
var cts = new CancellationTokenSource();

var options = new MemoryCacheEntryOptions()
    .AddExpirationToken(new CancellationChangeToken(cts.Token));

_cache.Set("product_list", products, options);

// Invalidoi
cts.Cancel();  // Poistaa kaikki cachet jotka riippuvat tästä tokenista
```

### Best Practice: Yhdistä strategiat

```csharp
public async Task UpdateProductAsync(Product product)
{
    await _repository.UpdateAsync(product);
    
    // 1. Poista heti (event-based)
    _cache.Remove($"product_{product.Id}");
    
    // 2. Mutta aseta myös expiration (safety net)
    var options = new MemoryCacheEntryOptions
    {
        AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
    };
}
```

---

## Decorator Pattern cachingille

**Decorator Pattern mahdollistaa cachingin lisäämisen ilman alkuperäisen koodin muuttamista.**

### Ilman Decoratoria (❌)

```csharp
public class ProductRepository : IProductRepository
{
    private readonly IMemoryCache _cache;
    private readonly DbContext _db;
    
    public async Task<Product?> GetByIdAsync(int id)
    {
        // Cache logic sekoittuu repository-logiikkaan
        if (_cache.TryGetValue($"product_{id}", out Product? cached))
            return cached;
        
        var product = await _db.Products.FindAsync(id);
        
        _cache.Set($"product_{id}", product);
        return product;
    }
}
```

**Ongelma:**
- Repository tietää cachesta (Separation of Concerns rikki)
- Vaikea testata
- Ei voi helposti poistaa cachea

### Decorator Patternilla (✅)

```csharp
// 1. Interface
public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id);
}

// 2. Alkuperäinen repository (ei tiedä cachesta)
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
        
        if (_cache.TryGetValue(cacheKey, out Product? cached))
            return cached;
        
        // Delegoi alkuperäiselle
        var product = await _inner.GetByIdAsync(id);
        
        if (product != null)
            _cache.Set(cacheKey, product, TimeSpan.FromMinutes(10));
        
        return product;
    }
}
```

### DI Registration

```csharp
// Program.cs / Startup.cs

services.AddMemoryCache();

// Alkuperäinen repository
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

**Edut:**
- ✅ Separation of Concerns
- ✅ Cache voidaan helposti poistaa
- ✅ Testattavuus (voi mockata inner:iä)
- ✅ Open/Closed Principle

---

## Distributed Caching

### Redis

**Redis on yleisin distributed cache.**

#### Asennus

```bash
dotnet add package Microsoft.Extensions.Caching.StackExchangeRedis
```

#### Konfiguraatio

```csharp
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = "localhost:6379";
    options.InstanceName = "MyApp_";
});
```

#### Käyttö

```csharp
public class ProductService
{
    private readonly IDistributedCache _cache;
    
    public ProductService(IDistributedCache cache)
    {
        _cache = cache;
    }
    
    public async Task<Product?> GetProductAsync(int id)
    {
        string cacheKey = $"product_{id}";
        
        // Hae Redis:istä (serialisoitu string)
        var cachedJson = await _cache.GetStringAsync(cacheKey);
        
        if (cachedJson != null)
        {
            return JsonSerializer.Deserialize<Product>(cachedJson);
        }
        
        // Hae DB:stä
        var product = await _repository.GetByIdAsync(id);
        
        if (product != null)
        {
            // Tallenna Redis:iin
            var json = JsonSerializer.Serialize(product);
            var options = new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10)
            };
            await _cache.SetStringAsync(cacheKey, json, options);
        }
        
        return product;
    }
}
```

#### IMemoryCache vs IDistributedCache

| Aspekti | IMemoryCache | IDistributedCache (Redis) |
|---------|--------------|---------------------------|
| **Nopeus** | ⚡⚡ Nopein (0.001ms) | ⚡ Nopea (1-5ms) |
| **Jaettu** | Ei (per server) | Kyllä (kaikki serverit) |
| **Persistenssi** | Häviää restartin yhteydessä | Voidaan säilyttää |
| **Skalautuvuus** | Rajoitettu | Erinomainen |
| **Kustannus** | Ilmainen | 20-100€/kk |
| **Käyttö** | Yksittäinen server | Load-balanced API:t |

### Hybrid Cache (Two-tier)

**Yhdistä IMemoryCache + Redis.**

```csharp
public class HybridCacheService
{
    private readonly IMemoryCache _l1Cache;  // Level 1 (nopea)
    private readonly IDistributedCache _l2Cache;  // Level 2 (jaettu)
    
    public async Task<T?> GetAsync<T>(string key)
    {
        // 1. Yritä L1 (memory)
        if (_l1Cache.TryGetValue(key, out T? l1Value))
            return l1Value;
        
        // 2. Yritä L2 (Redis)
        var l2Json = await _l2Cache.GetStringAsync(key);
        if (l2Json != null)
        {
            var l2Value = JsonSerializer.Deserialize<T>(l2Json);
            
            // Tallenna L1:een
            _l1Cache.Set(key, l2Value, TimeSpan.FromMinutes(5));
            
            return l2Value;
        }
        
        return default;
    }
}
```

**Edut:**
- L1: Erittäin nopea (0.001ms)
- L2: Jaettu kaikille servereille
- Parhaat puolet molemmista

---

## Best Practices

### 1. Cache vain kannattavaa dataa

**Cachettamisen arvoista:**
- ✅ Usein haettu data (käyttäjäprofiili, tuotteet)
- ✅ Kallis laskenta (raportit, aggregaatit)
- ✅ Ulkoiset API-kutsut (sää, valuuttakurssit)
- ✅ Harvoin muuttuva data (kategoriat, asetukset)

**Älä cacheta:**
- ❌ Jatkuvasti muuttuva data (stock prices)
- ❌ Käyttäjäkohtainen data (salasanat, tokenit)
- ❌ Erittäin suuri data (videot, suuret tiedostot)
- ❌ Data joka haetaan vain kerran

### 2. Käytä oikeaa cache duration:ia

```csharp
// Harvoin muuttuva (kategoriat, maat)
TimeSpan.FromHours(24)

// Keskivertodata (tuotteet, käyttäjät)
TimeSpan.FromMinutes(10)

// Usein muuttuva (varasto, tilaukset)
TimeSpan.FromMinutes(1)

// External API (weather, exchange rates)
TimeSpan.FromMinutes(15)
```

### 3. Käytä cache keys:eja järkevästi

**Hyvä:**
```csharp
$"product_{id}"                    // product_123
$"user_{userId}_profile"           // user_42_profile
$"orders_page_{page}_size_{size}"  // orders_page_1_size_10
```

**Huono:**
```csharp
"product"          // Ei uniikki!
$"{id}"            // Mikä entity?
"cache123"         // Ei kuvaava
```

### 4. Mittaa cache performance

```csharp
public class CacheMetrics
{
    public long Hits { get; set; }
    public long Misses { get; set; }
    
    public double HitRate => 
        Hits + Misses > 0 
            ? (double)Hits / (Hits + Misses) * 100 
            : 0;
}

// Repository:ssä
if (_cache.TryGetValue(key, out var value))
{
    _metrics.Hits++;
    return value;
}

_metrics.Misses++;
```

**Tavoitteet:**
- **70-90% hit rate** = Hyvä
- **>90% hit rate** = Erinomainen
- **<50% hit rate** = Tarkista strategia

### 5. Vältä cache stampede

**Ongelma:**

```csharp
// Cache vanhenee klo 10:00
// 1000 pyyntöä samanaikaisesti klo 10:00:01
// → 1000 database-kyselyä!
```

**Ratkaisu: Lock**

```csharp
private static readonly SemaphoreSlim _lock = new(1, 1);

public async Task<Product?> GetProductAsync(int id)
{
    if (_cache.TryGetValue($"product_{id}", out Product? cached))
        return cached;
    
    // Lock: Vain yksi thread hakee DB:stä
    await _lock.WaitAsync();
    try
    {
        // Double-check
        if (_cache.TryGetValue($"product_{id}", out cached))
            return cached;
        
        var product = await _repository.GetByIdAsync(id);
        _cache.Set($"product_{id}", product, TimeSpan.FromMinutes(10));
        
        return product;
    }
    finally
    {
        _lock.Release();
    }
}
```

### 6. Cache-friendly database queries

```csharp
// ❌ Huono: Include lataa kaikki related entities
var product = await _db.Products
    .Include(p => p.Category)
    .Include(p => p.Reviews)  // 100 review:ta!
    .FirstOrDefaultAsync(p => p.Id == id);

// ✅ Hyvä: Vain tarvittava data
var product = await _db.Products
    .Select(p => new ProductDto
    {
        Id = p.Id,
        Name = p.Name,
        CategoryName = p.Category.Name,
        ReviewCount = p.Reviews.Count  // Aggregaatti, ei kaikkia rivejä
    })
    .FirstOrDefaultAsync(p => p.Id == id);
```

---

## Anti-patterns

### 1. Cachettaa kaikki

**❌ Älä:**

```csharp
// Cachettaa jokainen database-kysely
_cache.Set("everything", await _db.Everything.ToListAsync());
```

**Ongelma:**
- Muisti loppuu
- Invalidation on vaikeaa
- Cache hit rate laskee

**✅ Cacheta valikoivasti:**
- Usein haettu data
- Kallis laskenta

### 2. Unohtaa cache invalidation

**❌ Älä:**

```csharp
// Päivitä tietokanta, mutta älä invalidoi cachea
public async Task UpdateProductAsync(Product product)
{
    await _db.SaveChangesAsync();
    // ← Cache invalidation puuttuu!
}
```

**✅ Invalidoi aina:**

```csharp
public async Task UpdateProductAsync(Product product)
{
    await _db.SaveChangesAsync();
    _cache.Remove($"product_{product.Id}");
}
```

### 3. Cachettaa käyttäjäkohtaista dataa väärällä key:llä

**❌ Älä:**

```csharp
// Kaikki käyttäjät jakavat saman cachen!
_cache.Set("user_profile", profile);
```

**✅ Käytä user-specific key:tä:**

```csharp
_cache.Set($"user_{userId}_profile", profile);
```

### 4. Liian pitkä cache duration

**❌ Älä:**

```csharp
// 24h cache usein muuttuvalle datalle
_cache.Set("products", products, TimeSpan.FromHours(24));
```

**✅ Sopiva duration:**

```csharp
// 10min cache tuotteille
_cache.Set("products", products, TimeSpan.FromMinutes(10));
```

### 5. Syncronous cache calls distributed cachessa

**❌ Älä:**

```csharp
// Blocking call Redis:iin
var value = _cache.GetString(key);  // ← Sync!
```

**✅ Käytä async:**

```csharp
var value = await _cache.GetStringAsync(key);
```

---

## Yhteenveto

### Milloin käyttää cachea?

**Cacheta kun:**
- ✅ Data haetaan usein
- ✅ Data muuttuu harvoin
- ✅ Kysely on kallis (DB, API)
- ✅ Vastausajan pitää olla nopea

**Älä cacheta kun:**
- ❌ Data muuttuu jatkuvasti
- ❌ Data on käyttäjäkohtaista (salasanat, tokenit)
- ❌ Data on erittäin suuri
- ❌ Data haetaan vain kerran

### Cache-strategioiden valinta

| Strategia | Käyttö |
|-----------|--------|
| **Cache-Aside** | Yleisin, read-heavy |
| **Read-Through** | Abstraktoitu, repository |
| **Write-Through** | Write-heavy, data aina ajan tasalla |
| **Write-Behind** | Erittäin korkea throughput |
| **Refresh-Ahead** | Data jota käytetään paljon |

### IMemoryCache vs Redis

| Käyttötapaus | Suositus |
|--------------|----------|
| Yksittäinen server | IMemoryCache |
| Load-balanced (monta serveriä) | Redis |
| Kehitys | IMemoryCache |
| Tuotanto (pieni) | IMemoryCache |
| Tuotanto (suuri) | Redis |
| Mikropalvelut | Redis |

### Key Takeaways

1. **Caching parantaa suorituskykyä merkittävästi** (10-100× nopeampi)
2. **Cache invalidation on vaikeaa** - Suunnittele huolellisesti
3. **Käytä Decorator Pattern:ia** - Separation of Concerns
4. **Mittaa performance** - Hit rate, latenssi
5. **Yhdistä time-based ja event-based invalidation**

---

## Lisämateriaali

### Ulkoiset linkit

- [Microsoft: Caching in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory)
- [Microsoft: Distributed caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/distributed)
- [Redis Documentation](https://redis.io/docs/)
- [Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

### Kirjastot

- **Microsoft.Extensions.Caching.Memory** - In-memory cache
- **Microsoft.Extensions.Caching.StackExchangeRedis** - Redis
- **EasyCaching** - Cache abstractions + tags
- **FusionCache** - Hybrid cache (L1 + L2)

### Tehtävät

- **Clean Architecture API: Part 5 - Caching** *(kurssitehtävä Moodlessa)*

---

**Hyvää cachetus-matkaa!** Muista: Cache vain kannattavaa, ja invalidoi oikein. 🚀
