# Säikeisturvalliset kokoelmat (Concurrent Collections)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi Concurrent Collections?](#miksi-concurrent-collections)
3. [ConcurrentDictionary](#concurrentdictionary)
4. [ConcurrentQueue ja ConcurrentStack](#concurrentqueue-ja-concurrentstack)
5. [ConcurrentBag](#concurrentbag)
6. [BlockingCollection](#blockingcollection)
7. [Channel](#channel)
8. [Vertailutaulukko](#vertailutaulukko)
9. [Yhteenveto](#yhteenveto)
10. [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Johdanto

`System.Collections.Concurrent`-nimiavaruus sisältää **säikeisturvallisia kokoelmia** jotka on suunniteltu moniajoon. Ne ovat turvallisia käyttää usean säikeen toimesta **ilman erillistä lukitusta**.

```csharp
using System.Collections.Concurrent;
```

---

## Miksi Concurrent Collections?

### Ongelma: Tavalliset kokoelmat eivät ole säikeisturvallisia

```csharp
// ❌ VAARALLISTA: Dictionary useassa säikeessä
Dictionary<int, string> dictionary = new Dictionary<int, string>();

// Rinnakkaiset kirjoitukset → InvalidOperationException tai korruptoitunut data!
Parallel.For(0, 1000, i =>
{
    dictionary[i] = $"Arvo {i}";  // ❌ Kaatuu!
});
```

### Ratkaisu 1: Dictionary + lock

```csharp
// ✅ Toimii, mutta hidas (kaikki jonottavat samaa lukkoa)
Dictionary<int, string> dictionary = new Dictionary<int, string>();
object lukko = new object();

Parallel.For(0, 1000, i =>
{
    lock (lukko)
    {
        dictionary[i] = $"Arvo {i}";
    }
});
```

### Ratkaisu 2: ConcurrentDictionary (parempi!)

```csharp
// ✅ Nopea ja turvallinen (sisäinen partitioitu lukitus)
ConcurrentDictionary<int, string> dictionary = new ConcurrentDictionary<int, string>();

Parallel.For(0, 1000, i =>
{
    dictionary[i] = $"Arvo {i}";  // Ei lukkoa tarvita!
});
```

### Performance-vertailu

| Tapa | 1M operaatiota (4 säiettä) | Turvallisuus |
|------|---------------------------|--------------|
| `Dictionary` (ei lukkoa) | ⚡ Nopein, mutta... | ❌ Kaatuu! |
| `Dictionary` + `lock` | ~300ms | ✅ Turvallinen |
| `ConcurrentDictionary` | ~150ms | ✅ Turvallinen |

---

## ConcurrentDictionary

`ConcurrentDictionary<TKey, TValue>` on **yleisin concurrent-kokoelma**. Se käyttää sisäistä partitioitua lukitusta, joten useat säikeet voivat lukea ja kirjoittaa eri osioihin samanaikaisesti.

### Peruskäyttö

```csharp
ConcurrentDictionary<string, int> cache = new ConcurrentDictionary<string, int>();

// Lisää tai päivitä
cache["avain1"] = 42;
cache.TryAdd("avain2", 100);  // Lisää vain jos avain ei ole olemassa

// Lue
if (cache.TryGetValue("avain1", out int arvo))
{
    Console.WriteLine($"Arvo: {arvo}");
}

// Poista
cache.TryRemove("avain1", out _);
```

### GetOrAdd — hae tai lisää

```csharp
ConcurrentDictionary<string, List<string>> cache = new ConcurrentDictionary<string, List<string>>();

// Jos avain löytyy → palauta arvo
// Jos ei löydy → luo uusi arvo, tallenna ja palauta
List<string> kaupungit = cache.GetOrAdd("suomi", key => new List<string>
{
    "Helsinki", "Tampere", "Turku"
});

Console.WriteLine($"Kaupungit: {string.Join(", ", kaupungit)}");
```

**Tärkeä huomio:** `GetOrAdd`-lambda voidaan kutsua useita kertoja rinnakkaisesti (factory ei ole lukittu), mutta vain yksi tulos tallennetaan.

```csharp
// ⚠️ Varoitus: Factory voidaan kutsua moneen kertaan!
List<string> result = cache.GetOrAdd("key", key =>
{
    Console.WriteLine("Factory kutsuttu!");  // Voi tulostua monta kertaa!
    return KallisOperaatio(key);
});

// ✅ Jos factory on kallis, käytä Lazy<T>
ConcurrentDictionary<string, Lazy<ExpensiveResult>> lazyCache = new ConcurrentDictionary<string, Lazy<ExpensiveResult>>();

Lazy<ExpensiveResult> result = lazyCache.GetOrAdd("key",
    key => new Lazy<ExpensiveResult>(() => KallisOperaatio(key)));

ExpensiveResult actualResult = result.Value;  // Factory kutsutaan vain kerran
```

### AddOrUpdate — lisää tai päivitä

```csharp
ConcurrentDictionary<string, int> sanalaskuri = new ConcurrentDictionary<string, int>();

string[] sanat = { "kissa", "koira", "kissa", "lintu", "kissa", "koira" };

foreach (string sana in sanat)
{
    sanalaskuri.AddOrUpdate(
        sana,
        addValue: 1,                       // Jos avain ei ole → lisää arvolla 1
        updateValueFactory: (key, old) => old + 1  // Jos avain on → kasvata yhdellä
    );
}

// Tulostus:
foreach (KeyValuePair<string, int> pari in sanalaskuri)
{
    Console.WriteLine($"{pari.Key}: {pari.Value}");
}
// kissa: 3
// koira: 2
// lintu: 1
```

### ConcurrentDictionary — käytännön esimerkki: Rate Limiter

```csharp
public class SimpleRateLimiter
{
    private readonly ConcurrentDictionary<string, RequestInfo> _requests = new();
    private readonly int _maxRequests;
    private readonly TimeSpan _window;

    public SimpleRateLimiter(int maxRequests, TimeSpan window)
    {
        _maxRequests = maxRequests;
        _window = window;
    }

    public bool IsAllowed(string clientId)
    {
        DateTime now = DateTime.UtcNow;

        RequestInfo info = _requests.AddOrUpdate(
            clientId,
            // Uusi asiakas
            _ => new RequestInfo { Count = 1, WindowStart = now },
            // Olemassa oleva asiakas
            (_, existing) =>
            {
                if (now - existing.WindowStart > _window)
                {
                    // Uusi aikaikkuna
                    return new RequestInfo { Count = 1, WindowStart = now };
                }
                existing.Count++;
                return existing;
            });

        return info.Count <= _maxRequests;
    }

    private class RequestInfo
    {
        public int Count { get; set; }
        public DateTime WindowStart { get; set; }
    }
}

// Käyttö: max 100 pyyntöä per minuutti
SimpleRateLimiter limiter = new SimpleRateLimiter(100, TimeSpan.FromMinutes(1));

if (limiter.IsAllowed("client-123"))
    Console.WriteLine("Sallittu");
else
    Console.WriteLine("Rate limit ylitetty!");
```

---

## ConcurrentQueue ja ConcurrentStack

### ConcurrentQueue\<T\> — FIFO (first in, first out)

```csharp
ConcurrentQueue<string> jono = new ConcurrentQueue<string>();

// Lisää jonoon (useat säikeet voivat lisätä samanaikaisesti)
jono.Enqueue("Tehtävä 1");
jono.Enqueue("Tehtävä 2");
jono.Enqueue("Tehtävä 3");

// Ota jonosta (turvallinen rinnakkaiskäyttö)
if (jono.TryDequeue(out string? tehtava))
{
    Console.WriteLine($"Käsitellään: {tehtava}");
}

// Kurkista seuraavaan (ei poista)
if (jono.TryPeek(out string? seuraava))
{
    Console.WriteLine($"Seuraavana: {seuraava}");
}

Console.WriteLine($"Jonossa: {jono.Count}");
```

### Käytännön esimerkki: Lokijono

```csharp
public class AsyncLogger
{
    private readonly ConcurrentQueue<string> _logQueue = new();
    private readonly CancellationTokenSource _cts = new();

    public AsyncLogger()
    {
        // Taustasäie käsittelee lokiviestit
        Task.Run(ProcessLogsAsync);
    }

    public void Log(string message)
    {
        _logQueue.Enqueue($"[{DateTime.Now:HH:mm:ss}] {message}");
    }

    private async Task ProcessLogsAsync()
    {
        while (!_cts.IsCancellationRequested)
        {
            while (_logQueue.TryDequeue(out string? viesti))
            {
                await File.AppendAllTextAsync("app.log", viesti + "\n");
            }

            await Task.Delay(100);  // Odota ennen seuraavaa tarkistusta
        }
    }

    public void Stop() => _cts.Cancel();
}
```

### ConcurrentStack\<T\> — LIFO (last in, first out)

```csharp
ConcurrentStack<int> pino = new ConcurrentStack<int>();

// Lisää pinoon
pino.Push(1);
pino.Push(2);
pino.Push(3);

// Ota pinosta (viimeisin ensin)
if (pino.TryPop(out int arvo))
{
    Console.WriteLine($"Pinosta: {arvo}");  // 3
}

// Ota useita kerralla
int[] tulokset = new int[2];
int saadut = pino.TryPopRange(tulokset);
Console.WriteLine($"Saatiin {saadut} alkiota: {string.Join(", ", tulokset.Take(saadut))}");
```

---

## ConcurrentBag

`ConcurrentBag<T>` on **järjestämätön kokoelma** joka on optimoitu tilanteisiin joissa sama säie sekä lisää että poistaa alkioita.

```csharp
ConcurrentBag<string> bag = new ConcurrentBag<string>();

// Lisää (useasta säikeestä)
Parallel.For(0, 100, i =>
{
    bag.Add($"Item {i}");
});

Console.WriteLine($"Bag sisältää {bag.Count} alkiota");

// Ota yksi (järjestys ei ole taattu!)
if (bag.TryTake(out string? item))
{
    Console.WriteLine($"Otettiin: {item}");
}
```

### Milloin ConcurrentBag?

- ✅ Sama säie lisää ja poistaa (esim. object pool)
- ✅ Järjestyksellä ei ole väliä
- ❌ **Älä käytä** jos tarvitset FIFO-järjestystä → `ConcurrentQueue`
- ❌ **Älä käytä** jos eri säikeet lisäävät ja poistavat → `ConcurrentQueue`

### Esimerkki: Object Pool

```csharp
public class SimpleObjectPool<T>
{
    private readonly ConcurrentBag<T> _pool = new();
    private readonly Func<T> _factory;

    public SimpleObjectPool(Func<T> factory)
    {
        _factory = factory;
    }

    public T Rent()
    {
        return _pool.TryTake(out T? item) ? item : _factory();
    }

    public void Return(T item)
    {
        _pool.Add(item);
    }
}

// Käyttö: StringBuilder-pooli
SimpleObjectPool<StringBuilder> pool = new SimpleObjectPool<StringBuilder>(() => new StringBuilder());

StringBuilder sb = pool.Rent();
sb.Append("Hello");
string tulos = sb.ToString();
sb.Clear();
pool.Return(sb);  // Palauta pooliin uusiokäyttöön
```

---

## BlockingCollection

`BlockingCollection<T>` on **korkeamman tason tuottaja-kuluttaja -kokoelma**. Se blokkaa kuluttajan kunnes dataa on saatavilla ja tukee kapasiteettirajoitusta.

### Peruskäyttö

```csharp
// Kapasiteetti: max 10 alkiota kerrallaan
using BlockingCollection<string> collection = new BlockingCollection<string>(boundedCapacity: 10);

// Tuottaja (eri säikeessä)
Task producer = Task.Run(() =>
{
    for (int i = 0; i < 20; i++)
    {
        collection.Add($"Viesti {i}");  // Blokkaa jos täynnä!
        Console.WriteLine($"Tuotettu: Viesti {i}");
    }
    collection.CompleteAdding();  // Merkitse valmis
});

// Kuluttaja (eri säikeessä)
Task consumer = Task.Run(() =>
{
    // GetConsumingEnumerable blokkaa ja odottaa uutta dataa
    foreach (string viesti in collection.GetConsumingEnumerable())
    {
        Console.WriteLine($"Kulutettu: {viesti}");
        Thread.Sleep(100);  // Simuloi prosessointia
    }
});

await Task.WhenAll(producer, consumer);
```

### Producer-Consumer pattern usealla kuluttajalla

```csharp
using BlockingCollection<WorkItem> tyojono = new BlockingCollection<WorkItem>(boundedCapacity: 100);

// Useita tuottajia
Task[] producers = Enumerable.Range(0, 3).Select(id =>
    Task.Run(() =>
    {
        for (int i = 0; i < 10; i++)
        {
            tyojono.Add(new WorkItem { Id = id * 10 + i, Data = $"Data-{id}-{i}" });
        }
    })).ToArray();

// Useita kuluttajia
Task[] consumers = Enumerable.Range(0, 2).Select(id =>
    Task.Run(() =>
    {
        foreach (WorkItem item in tyojono.GetConsumingEnumerable())
        {
            Console.WriteLine($"Worker {id}: Käsittely {item.Id}");
            Thread.Sleep(50);
        }
    })).ToArray();

await Task.WhenAll(producers);
tyojono.CompleteAdding();  // Kaikki tuotettu
await Task.WhenAll(consumers);

record WorkItem { public int Id { get; init; } public string Data { get; init; } = ""; }
```

### BlockingCollection — rajoitukset

- **Blokkaa säikeen** — ei async-tukea (`Add` ja `Take` ovat synkronisia)
- **Vanhentunut käytäntö** — `Channel<T>` on moderni korvaaja

---

## Channel

`Channel<T>` on **.NET:n moderni producer-consumer** -ratkaisu. Se tukee `async/await`:ia ja on suunniteltu asynkronisiin scenaarioihin.

```csharp
using System.Threading.Channels;
```

### Peruskäyttö

```csharp
// Luo rajoitettu kanava (max 100 viestiä)
Channel<string> channel = Channel.CreateBounded<string>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait  // Odota jos täynnä
});

// Tuottaja
Task producer = Task.Run(async () =>
{
    for (int i = 0; i < 50; i++)
    {
        await channel.Writer.WriteAsync($"Viesti {i}");
        Console.WriteLine($"Kirjoitettu: Viesti {i}");
    }
    channel.Writer.Complete();  // Ei enää viestejä
});

// Kuluttaja
Task consumer = Task.Run(async () =>
{
    await foreach (string viesti in channel.Reader.ReadAllAsync())
    {
        Console.WriteLine($"Luettu: {viesti}");
        await Task.Delay(50);
    }
});

await Task.WhenAll(producer, consumer);
```

### Channel — rajoittamaton vs rajoitettu

```csharp
// Rajoittamaton: ei ylärajaa (varoitus: muisti voi loppua!)
Channel<string> unbounded = Channel.CreateUnbounded<string>();

// Rajoitettu: max N alkiota
Channel<string> bounded = Channel.CreateBounded<string>(new BoundedChannelOptions(100)
{
    // Mitä tehdään kun kanava on täynnä?
    FullMode = BoundedChannelFullMode.Wait,        // Odota (oletus)
    // FullMode = BoundedChannelFullMode.DropOldest,  // Pudota vanhin
    // FullMode = BoundedChannelFullMode.DropNewest,  // Pudota uusin
    // FullMode = BoundedChannelFullMode.DropWrite,   // Pudota kirjoitus

    SingleReader = true,   // Optimointi: vain yksi lukija
    SingleWriter = false   // Useita kirjoittajia
});
```

### Channel — käytännön esimerkki: Background Processing

```csharp
public class BackgroundJobProcessor
{
    private readonly Channel<JobRequest> _channel;

    public BackgroundJobProcessor()
    {
        _channel = Channel.CreateBounded<JobRequest>(new BoundedChannelOptions(1000)
        {
            SingleReader = true
        });
    }

    // API kutsuu tätä — palauttaa heti
    public async Task<bool> EnqueueJobAsync(JobRequest job, CancellationToken ct = default)
    {
        return _channel.Writer.TryWrite(job);
    }

    // Taustaprosessi käsittelee jonoa
    public async Task ProcessJobsAsync(CancellationToken ct)
    {
        await foreach (JobRequest job in _channel.Reader.ReadAllAsync(ct))
        {
            try
            {
                Console.WriteLine($"Käsitellään: {job.Name}");
                await ProcessJobAsync(job, ct);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Virhe: {ex.Message}");
            }
        }
    }

    private async Task ProcessJobAsync(JobRequest job, CancellationToken ct)
    {
        // Simuloi työtä
        await Task.Delay(1000, ct);
        Console.WriteLine($"Valmis: {job.Name}");
    }
}

public record JobRequest(string Name, string Payload);
```

### Channel — ASP.NET Core Background Service

```csharp
// 1. Rekisteröi DI:ssä
builder.Services.AddSingleton(Channel.CreateBounded<EmailRequest>(100));
builder.Services.AddHostedService<EmailSenderService>();

// 2. Controller kirjoittaa kanavaan
[ApiController]
[Route("api/[controller]")]
public class EmailController : ControllerBase
{
    private readonly Channel<EmailRequest> _channel;

    public EmailController(Channel<EmailRequest> channel)
    {
        _channel = channel;
    }

    [HttpPost]
    public async Task<IActionResult> SendEmail(EmailRequest request)
    {
        await _channel.Writer.WriteAsync(request);
        return Accepted();  // 202 — käsitellään taustalla
    }
}

// 3. BackgroundService lukee kanavasta
public class EmailSenderService : BackgroundService
{
    private readonly Channel<EmailRequest> _channel;

    public EmailSenderService(Channel<EmailRequest> channel)
    {
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        await foreach (EmailRequest request in _channel.Reader.ReadAllAsync(ct))
        {
            await SendEmailAsync(request);
        }
    }

    private async Task SendEmailAsync(EmailRequest request)
    {
        Console.WriteLine($"Lähetetään sähköposti: {request.To}");
        await Task.Delay(500);  // Simuloi lähetystä
    }
}

public record EmailRequest(string To, string Subject, string Body);
```

### BlockingCollection vs Channel

| Ominaisuus | `BlockingCollection<T>` | `Channel<T>` |
|------------|------------------------|--------------|
| **Async-tuki** | ❌ Synkroninen | ✅ Täysi async |
| **Suorituskyky** | Hyvä | ⚡ Parempi |
| **Kapasiteettihallinta** | Rajoitettu | Monipuolinen (Wait, Drop) |
| **Moderni .NET** | Vanha | ✅ Suositeltu |
| **`await foreach`** | ❌ | ✅ |
| **Single reader/writer optimointi** | ❌ | ✅ |

---

## Vertailutaulukko

| Kokoelma | Järjestys | Duplikaatit | Async | Käyttökohde |
|----------|-----------|-------------|-------|-------------|
| `ConcurrentDictionary<K,V>` | Ei | Avain uniikki | Ei | Cache, lookup, laskurit |
| `ConcurrentQueue<T>` | FIFO | ✅ | Ei | Tehtäväjonot, lokitus |
| `ConcurrentStack<T>` | LIFO | ✅ | Ei | Undo, peruutuspinot |
| `ConcurrentBag<T>` | Ei | ✅ | Ei | Object pool, sama säie lisää/poistaa |
| `BlockingCollection<T>` | FIFO* | ✅ | ❌ | Producer-consumer (synkroninen) |
| `Channel<T>` | FIFO | ✅ | ✅ | Producer-consumer (asynkroninen) |

\* BlockingCollection voi käyttää mitä tahansa `IProducerConsumerCollection<T>`:ia pohjalla.

### Valintaopas

```
Tarvitsetko säikeisturvallista kokoelmaa?
│
├─ Avain-arvo -pareja?
│  └─ → ConcurrentDictionary<K,V>
│
├─ Tuottaja-kuluttaja (producer-consumer)?
│  ├─ Asynkroninen (async/await)?
│  │  └─ → Channel<T>
│  └─ Synkroninen?
│     └─ → BlockingCollection<T>
│
├─ FIFO-jono?
│  └─ → ConcurrentQueue<T>
│
├─ LIFO-pino?
│  └─ → ConcurrentStack<T>
│
└─ Object pool / järjestyksellä ei väliä?
   └─ → ConcurrentBag<T>
```

---

## Yhteenveto

### Muistilista

1. **`ConcurrentDictionary`** — Yleisin: cache, laskurit, lookup
2. **`ConcurrentQueue`** — FIFO-jono usealle säikeelle
3. **`Channel<T>`** — Moderni producer-consumer (suosi tätä!)
4. **`BlockingCollection`** — Vanhempi producer-consumer (synkroninen)
5. **`ConcurrentBag`** — Object pool -skenaariot

### Tärkeimmät säännöt

- ✅ Käytä `Concurrent*`-kokoelmia monen säikeen kanssa
- ✅ Käytä `Channel<T>`:ia async producer-consumer -tarpeisiin
- ✅ `GetOrAdd` + `Lazy<T>` kun factory on kallis
- ❌ Älä käytä tavallista `Dictionary`:a ilman lukitusta moniajossa
- ❌ Älä oleta järjestystä `ConcurrentBag`:stä

---

## Hyödyllisiä linkkejä

- [Microsoft: System.Collections.Concurrent](https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent)
- [Microsoft: ConcurrentDictionary](https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent.concurrentdictionary-2)
- [Microsoft: System.Threading.Channels](https://learn.microsoft.com/en-us/dotnet/core/extensions/channels)
- [Microsoft: Producer-consumer patterns](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)
- [Stephen Toub: Channels](https://devblogs.microsoft.com/dotnet/an-introduction-to-system-threading-channels/)

### Seuraavaksi

- [Parallel-ohjelmointi](Parallel-Programming.md) — Hyödynnä monta ydintä rinnakkaisella suorituksella
