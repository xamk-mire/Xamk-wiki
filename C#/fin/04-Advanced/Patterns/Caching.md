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
User → API → Cache (0.5ms)    ✅ Ei tietokantakyselyä
User → API → Cache (0.5ms)    ✅
```

Millisekunnit ovat tällä sivulla suuntaa antavia esimerkkejä. Todellinen ero riippuu kyselystä, tietokannasta ja verkosta, joten mittaa se omassa sovelluksessasi.

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
- ✅ **Nopeampi vastausaika**: muistista lukeminen on selvästi nopeampaa kuin tietokantakysely
- ✅ **Vähemmän tietokantakyselyitä**: sama data haetaan tietokannasta vain kerran
- ✅ **Parempi käyttökokemus**: sivu latautuu nopeammin
- ✅ **Pienempi kuorma tietokannalle**, mikä voi myös laskea kustannuksia

**Hinta:** välimuistissa oleva data voi olla vanhaa. Suurin osa tästä sivusta käsittelee sitä, miten vanhentunut data poistetaan oikeaan aikaan (katso [Cache Invalidation](#cache-invalidation)).

---

## Caching-strategiat

### 1. Cache-Aside (Lazy Loading)

**Yleisin strategia.** Sovellus hoitaa välimuistin itse kolmessa vaiheessa:

1. **Katso välimuistista.** Jos data löytyy (*cache hit*), palauta se.
2. **Jos ei löydy (*cache miss*), lue lähteestä.** Lähde on yleensä tietokanta.
3. **Tallenna tulos välimuistiin** ja palauta se. Seuraava kysyjä saa datan vaiheessa 1.

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

**Jokainen kirjoitus päivittää samalla kertaa sekä tietokannan että cachen.** Cache on siis heti kirjoituksen jälkeen ajan tasalla. Tässä esimerkissä tietokanta päivitetään ensin: jos se epäonnistuu, cacheen ei jää dataa, jota tietokannassa ei ole.

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
- ✅ Selain tallentaa vastauksen välimuistiin automaattisesti
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
- ❌ Data on vanhaa siihen asti, kun aikaraja täyttyy (tässä enintään 5 minuuttia)
- ❌ Cache voi vanhentua, vaikka data ei ole muuttunut, jolloin se haetaan turhaan uudestaan

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
- ❌ Jokaisen kirjoituspolun pitää muistaa poistaa cache. Jos yksi unohtaa, data jää vanhaksi.

### Ratkaisu 3: Cache Tags

**Ryhmittele cachet tagien mukaan.** Tagi on merkintä, jolla monta cache-avainta voi poistaa yhdellä kutsulla.

`IMemoryCache` **ei tue tageja**: siinä ei ole `AddTag`- tai `RemoveByTag`-metodia. Tagit löytyvät `HybridCache`-kirjastosta (`Microsoft.Extensions.Caching.Hybrid`, .NET 9:stä alkaen):

```csharp
// Program.cs
builder.Services.AddHybridCache();
```

```csharp
// Tallenna tagin kanssa (HybridCache _hybridCache)
var product = await _hybridCache.GetOrCreateAsync(
    $"product_{id}",
    async ct => await _repository.GetByIdAsync(id, ct),
    tags: new[] { "products" },
    cancellationToken: cancellationToken);

// Poista kaikki "products"-tagilla merkityt
await _hybridCache.RemoveByTagAsync("products", cancellationToken);
```

Myös ASP.NET Coren output caching tukee tageja (`[OutputCache(Tags = ...)]` ja `IOutputCacheStore.EvictByTagAsync`). Pelkällä `IMemoryCache`lla saman voi tehdä alla olevalla tokenilla (Ratkaisu 4).

**Microsoft:** [HybridCache library in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid)

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

Tapahtumapohjainen tyhjennys pitää datan tuoreena. Aikaraja on turvaverkko: jos jokin kirjoituspolku unohtaa tyhjentää cachen, vanha data poistuu silti viimeistään aikarajan jälkeen.

```csharp
// Kirjoitus: poista heti (event-based)
public async Task UpdateProductAsync(Product product)
{
    await _repository.UpdateAsync(product);

    _cache.Remove($"product_{product.Id}");
}

// Luku: aseta aikaraja aina kun tallennat cacheen (turvaverkko)
public async Task<Product?> GetProductAsync(int id)
{
    return await _cache.GetOrCreateAsync(
        $"product_{id}",
        async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(10);
            return await _repository.GetByIdAsync(id);
        });
}
```

### Järjestys: tallenna, tyhjennä, ilmoita

Kun muutos kirjataan, tehdään usein kolme asiaa: data tallennetaan, välimuisti tyhjennetään ja selaimille ilmoitetaan muutoksesta (esimerkiksi [SignalR](../SignalR/README.md):llä). Järjestyksellä on väliä.

```csharp
// Command-handlerissa: otteluun kirjataan tulos, sarjataulukko muuttuu
await _matches.SaveAsync(match, ct);                          // 1. tallenna
_standingsCache.Clear();                                      // 2. tyhjennä välimuisti
await _notifier.StandingsChangedAsync(match.LeagueId, ct);    // 3. ilmoita selaimille
```

Mitä tapahtuu, jos järjestys on väärä:

| Väärä järjestys | Seuraus |
|---|---|
| **Ilmoitus ennen välimuistin tyhjennystä** | Selaimet hakevat sarjataulukon heti ilmoituksen saatuaan. Välimuistissa on vielä vanha taulukko, joten ne saavat vanhan datan. |
| **Tyhjennys ennen tallennusta** | Samaan aikaan tuleva lukupyyntö ei löydä dataa välimuistista. Se lukee tietokannasta vanhan tilan, koska tallennus on vielä kesken, ja laittaa sen takaisin välimuistiin. Vanha data jää sinne aikarajan loppuun asti. |

Muistisääntö: jokainen vaihe tehdään vasta, kun edellinen on valmis. Ensin totuus on tietokannassa, sitten vanha kopio poistetaan, ja vasta sitten muita pyydetään hakemaan.

### Välimuisti omassa kerroksessaan

Yllä handler kutsuu `_standingsCache.Clear()`. Handler on Application-kerroksessa, eikä se saa riippua välimuistin tekniikasta. Ratkaisu on sama kuin repositoryssa: **rajapinta määritellään Application-kerroksessa, toteutus on Infrastructure-kerroksessa.**

```csharp
// Application: handler tuntee vain tämän
public interface IStandingsCache
{
    void Clear();
}
```

```csharp
// Infrastructure: ainoa paikka, jossa IMemoryCache näkyy
public class MemoryStandingsCache : IStandingsCache
{
    public const string Key = "standings";

    private readonly IMemoryCache _cache;

    public MemoryStandingsCache(IMemoryCache cache)
    {
        _cache = cache;
    }

    public void Clear()
    {
        _cache.Remove(Key);
    }
}
```

Handler ei näe `IMemoryCache`a lainkaan. Se sanoo vain "tyhjennä sarjataulukon välimuisti". Jos välimuisti vaihdetaan myöhemmin Redisiin, muutos tehdään Infrastructure-kerrokseen eikä handleriin kosketa. Handlerin testissä rajapinnan tilalle annetaan tekaistu toteutus.

Lukupuolella välimuisti lisätään samassa kerroksessa decoratorilla: katso [Decorator Pattern cachingille](#decorator-pattern-cachingille).

**Milloin tätä ei tarvita?** Kun sovelluksessa ei ole erillisiä kerroksia tai välimuistia käytetään vain aikarajalla ilman tyhjennystä. Silloin rajapinta ei ratkaise mitään.

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

**Missä decorator asuu?** `CachedProductRepository` kuuluu Infrastructure-kerrokseen, koska se tuntee `IMemoryCache`n. Rajapinta `IProductRepository` on Application-kerroksessa. Tarkemmin: [Decorator Pattern](Decorator-Pattern.md).

### DI Registration

```csharp
// Program.cs (tässä services = builder.Services)

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
| **Nopeus** | ⚡⚡ Nopein (luku omasta muistista) | ⚡ Nopea (verkkokutsu ja serialisointi) |
| **Jaettu** | Ei (per server) | Kyllä (kaikki serverit) |
| **Persistenssi** | Häviää restartin yhteydessä | Voidaan säilyttää |
| **Skalautuvuus** | Rajoitettu | Erinomainen |
| **Kustannus** | Ei erillistä kustannusta | Erillinen palvelu, josta maksetaan |
| **Käyttö** | Yksittäinen server | Load-balanced API:t |

### Hybrid Cache (Two-tier)

**Yhdistä IMemoryCache + Redis.**

.NET 9:stä alkaen tähän on valmis kirjasto, `HybridCache` (`Microsoft.Extensions.Caching.Hybrid`). Se hoitaa kaksi tasoa, serialisoinnin, tagit ja cache stampede -suojan. Käytä uudessa koodissa sitä: [Microsoft: HybridCache](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid). Alla oleva käsin kirjoitettu luokka näyttää vain, mitä kahden tason välimuisti sisältä tekee.

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
- L1: Erittäin nopea, koska data on sovelluksen omassa muistissa
- L2: Jaettu kaikille servereille
- Molempien hyödyt samassa ratkaisussa

---

## Best Practices

### 1. Cache vain kannattavaa dataa

Nyrkkisääntö: cacheta dataa, jota **luetaan usein ja joka muuttuu harvoin**.

**Cachettamisen arvoista:**
- ✅ Usein haettu data (tuotteet, sarjataulukko)
- ✅ Kallis laskenta (raportit, aggregaatit)
- ✅ Ulkoiset API-kutsut (sää, valuuttakurssit)
- ✅ Harvoin muuttuva data (kategoriat, asetukset)

**Älä cacheta:**
- ❌ Dataa, jonka sääntötarkistus tarvitsee tuoreena. Jos handler päättää välimuistin perusteella, onko tuotetta varastossa tai onko tulos jo kirjattu, se voi päättää vanhan tiedon pohjalta. Sääntö tarkistetaan aina tietokannasta haetusta entiteetistä.
- ❌ Jatkuvasti muuttuva data (stock prices)
- ❌ Salaisuudet (salasanat, tokenit)
- ❌ Erittäin suuri data (videot, suuret tiedostot)
- ❌ Data joka haetaan vain kerran

**Käyttäjäkohtainen data** (esimerkiksi käyttäjäprofiili) ei ole kielletty, mutta se vaatii tarkkuutta. Avaimessa pitää olla käyttäjän tunniste, muuten yksi käyttäjä näkee toisen tiedot (katso [Anti-patterns](#anti-patterns), kohta 3). Hyöty on myös pienempi, koska saman rivin lukee vain yksi käyttäjä.

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

**Suuntaa antavat tavoitteet (nyrkkisääntö, ei standardi):**
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

### 1. Kaiken cachettaminen

**❌ Älä:**

```csharp
// Jokainen database-kysely cacheen
_cache.Set("everything", await _db.Everything.ToListAsync());
```

**Ongelma:**
- Muisti loppuu
- Invalidation on vaikeaa
- Cache hit rate laskee

**✅ Cacheta valikoivasti:**
- Usein haettu data
- Kallis laskenta

### 2. Cache invalidationin unohtaminen

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

### 3. Käyttäjäkohtaisen datan cachettaminen väärällä key:llä

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

### 5. Synkroniset cache-kutsut distributed cachessa

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
- ❌ Sääntötarkistus tarvitsee datan tuoreena
- ❌ Data muuttuu jatkuvasti
- ❌ Data on salaista (salasanat, tokenit)
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

1. **Caching nopeuttaa usein toistuvia lukuja** - Mittaa hyöty omassa sovelluksessasi
2. **Cache invalidation on vaikeaa** - Suunnittele huolellisesti
3. **Käytä Decorator Pattern:ia** - Separation of Concerns
4. **Mittaa performance** - Hit rate, latenssi
5. **Yhdistä time-based ja event-based invalidation**
6. **Järjestys kirjoituksessa: tallenna, tyhjennä, ilmoita**
7. **Handler tuntee vain oman kerroksensa rajapinnan** - `IMemoryCache` näkyy vain Infrastructure-kerroksessa

---

## Lisämateriaali

### Ulkoiset linkit

- [Microsoft: Caching in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/memory)
- [Microsoft: Distributed caching](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/distributed)
- [Microsoft: HybridCache library in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/hybrid)
- [Redis Documentation](https://redis.io/docs/)
- [Cache-Aside Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside)

### Kirjastot

- **Microsoft.Extensions.Caching.Memory** - In-memory cache
- **Microsoft.Extensions.Caching.StackExchangeRedis** - Redis
- **Microsoft.Extensions.Caching.Hybrid** - HybridCache: kaksi tasoa (L1 + L2) ja tagit
- **EasyCaching** - Cache abstractions + tags
- **FusionCache** - Hybrid cache (L1 + L2)

### Liittyvät aiheet

- [Decorator Pattern](Decorator-Pattern.md) - Välimuistin lisääminen muuttamatta alkuperäistä luokkaa
- [SignalR](../SignalR/README.md) - Selaimille ilmoittaminen välimuistin tyhjennyksen jälkeen

---

**Muista:** cacheta vain kannattavaa, ja invalidoi oikein.
