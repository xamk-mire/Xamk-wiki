# Synkronointimekanismit

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi synkronointi?](#miksi-synkronointi)
3. [lock](#lock)
4. [Monitor](#monitor)
5. [SemaphoreSlim](#semaphoreslim)
6. [Mutex](#mutex)
7. [ReaderWriterLockSlim](#readerwriterlockslim)
8. [Interlocked](#interlocked)
9. [Double-checked locking](#double-checked-locking)
10. [Deadlock](#deadlock)
11. [Vertailutaulukko](#vertailutaulukko)
12. [Yhteenveto](#yhteenveto)
13. [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Johdanto

Kun useat säikeet käyttävät **samaa dataa**, tarvitaan **synkronointimekanismeja** estämään kilpailutilanteet (race conditions) ja varmistamaan datan eheys.

**Ongelma ilman synkronointia:**

```
Thread 1: Lue laskuri (arvo: 10)
Thread 2: Lue laskuri (arvo: 10)
Thread 1: Kirjoita laskuri (10 + 1 = 11)
Thread 2: Kirjoita laskuri (10 + 1 = 11)  ← Pitäisi olla 12!
```

---

## Miksi synkronointi?

### Race condition -esimerkki

```csharp
// ❌ VAARALLISTA: Ei synkronointia
public class Laskuri
{
    private int _arvo = 0;

    public void Kasvata()
    {
        _arvo++;  // EI ole atominen operaatio!
        // Taustalla: 1) Lue _arvo  2) Lisää 1  3) Kirjoita _arvo
    }

    public int Arvo => _arvo;
}

// Testaa race conditionia
Laskuri laskuri = new Laskuri();
IEnumerable<Task> tasks = Enumerable.Range(0, 1000).Select(_ =>
    Task.Run(() => laskuri.Kasvata()));

await Task.WhenAll(tasks);
Console.WriteLine($"Odotettu: 1000, Todellinen: {laskuri.Arvo}");
// Tulostus: Odotettu: 1000, Todellinen: 987 (tai jokin muu <1000)
```

---

## lock

`lock` on **yksinkertaisin synkronointimekanismi**. Se varmistaa, että vain yksi säie kerrallaan suorittaa suojatun koodilohkon.

### Peruskäyttö

```csharp
public class SaikeisturvallinenLaskuri
{
    private int _arvo = 0;
    private readonly object _lukko = new();  // Lock-objekti

    public void Kasvata()
    {
        lock (_lukko)  // Vain yksi säie kerrallaan
        {
            _arvo++;  // Nyt turvallinen!
        }
    }

    public int Arvo
    {
        get
        {
            lock (_lukko)
            {
                return _arvo;
            }
        }
    }
}

// Nyt toimii oikein!
SaikeisturvallinenLaskuri laskuri = new SaikeisturvallinenLaskuri();
IEnumerable<Task> tasks = Enumerable.Range(0, 1000).Select(_ =>
    Task.Run(() => laskuri.Kasvata()));

await Task.WhenAll(tasks);
Console.WriteLine($"Arvo: {laskuri.Arvo}");
// Tulostus: Arvo: 1000 ✅
```

### Miten lock toimii?

```
Thread 1: lock(_lukko) → Saa lukon → Suorittaa koodin → Vapauttaa lukon
Thread 2: lock(_lukko) → ODOTTAA... → Saa lukon → Suorittaa koodin → Vapauttaa
Thread 3: lock(_lukko) → ODOTTAA.............. → Saa lukon → Suorittaa → Vapauttaa
```

### lock-säännöt

```csharp
// ✅ HYVÄ: Käytä yksityistä readonly-objektia
private readonly object _lukko = new();

// ❌ HUONO: Lukita this
lock (this)  // Kuka tahansa voi lukita saman objektin ulkopuolelta!
{
    // ...
}

// ❌ HUONO: Lukita tyyppiä
lock (typeof(MyClass))  // Globaali lukko, vaikuttaa kaikkiin instansseihin!
{
    // ...
}

// ❌ HUONO: Lukita stringiä
lock ("myLock")  // String interning: sama "myLock" on sama objekti!
{
    // ...
}
```

### lock C# 13 (.NET 9) — System.Threading.Lock

```csharp
// C# 13 esittelee dedikoidun Lock-tyypin
public class ModerniLaskuri
{
    private int _arvo = 0;
    private readonly Lock _lukko = new();  // System.Threading.Lock

    public void Kasvata()
    {
        lock (_lukko)  // Kääntäjä optimoi automaattisesti
        {
            _arvo++;
        }
    }

    // Voi myös käyttää Scope-syntaksia
    public void KasvataScope()
    {
        using (_lukko.EnterScope())
        {
            _arvo++;
        }
    }
}
```

### lock:n rajoitukset

- **Ei tue `await`:ia** — lock-lohkon sisällä ei voi käyttää `await`
- **Blokkaa säikeen** — odottava säie ei tee muuta
- **Vain yhden prosessin sisällä** — ei toimi prosessien välillä

```csharp
// ❌ EI TOIMI: await lock:n sisällä
lock (_lukko)
{
    await Task.Delay(100);  // Käännösvirhe!
}

// ✅ Käytä SemaphoreSlim:iä asynkroniseen lukitukseen
await _semaphore.WaitAsync();
try
{
    await Task.Delay(100);  // Toimii!
}
finally
{
    _semaphore.Release();
}
```

---

## Monitor

`lock` on syntaktinen sokeri (syntactic sugar) `Monitor`-luokalle. `Monitor` tarjoaa enemmän kontrollia.

### lock vs Monitor

```csharp
// Nämä ovat identtisiä:

// lock-versio
lock (_lukko)
{
    // Kriittinen osio
}

// Monitor-versio (mitä kääntäjä tekee)
Monitor.Enter(_lukko);
try
{
    // Kriittinen osio
}
finally
{
    Monitor.Exit(_lukko);
}
```

### Monitor.TryEnter — timeout

```csharp
private readonly object _lukko = new();

public bool YritaKasvattaa(int timeoutMs = 1000)
{
    // Yritä saada lukko tietyn ajan sisällä
    if (Monitor.TryEnter(_lukko, TimeSpan.FromMilliseconds(timeoutMs)))
    {
        try
        {
            _arvo++;
            return true;
        }
        finally
        {
            Monitor.Exit(_lukko);
        }
    }

    Console.WriteLine("Lukkoa ei saatu — timeout!");
    return false;
}
```

### Monitor.Wait ja Monitor.Pulse — tuottaja-kuluttaja

```csharp
public class YksinkertainenJono<T>
{
    private readonly Queue<T> _jono = new();
    private readonly object _lukko = new();

    public void Lisaa(T item)
    {
        lock (_lukko)
        {
            _jono.Enqueue(item);
            Monitor.Pulse(_lukko);  // Herätä odottava säie
        }
    }

    public T Ota()
    {
        lock (_lukko)
        {
            // Odota kunnes jonossa on jotain
            while (_jono.Count == 0)
            {
                Monitor.Wait(_lukko);  // Vapauta lukko ja odota
            }

            return _jono.Dequeue();
        }
    }
}
```

---

## SemaphoreSlim

`SemaphoreSlim` on **monipuolisin synkronointimekanismi**:
- Tukee `await`:ia (asynkroninen lukitus)
- Rajoittaa samanaikaisten pääsyjen määrää
- Kevyempi kuin `Semaphore`

### Asynkroninen lukitus (korvaa lock:n async-koodissa)

```csharp
public class SaikeisturvallinenCache
{
    private readonly Dictionary<string, string> _cache = new();
    private readonly SemaphoreSlim _semaphore = new(1, 1);  // Max 1 kerrallaan

    public async Task<string> GetOrAddAsync(string key, Func<Task<string>> factory)
    {
        await _semaphore.WaitAsync();  // ✅ Asynkroninen lukitus!
        try
        {
            if (_cache.TryGetValue(key, out string? cached))
                return cached;

            string value = await factory();  // ✅ Voi käyttää await!
            _cache[key] = value;
            return value;
        }
        finally
        {
            _semaphore.Release();
        }
    }
}
```

### Rajoitettu samanaikaisuus

```csharp
// Rajoita: max 5 samanaikaista HTTP-kutsua
private readonly SemaphoreSlim _httpThrottle = new(5, 5);

public async Task<string[]> HaeKaikkiAsync(string[] urls)
{
    IEnumerable<Task<string>> tasks = urls.Select(async url =>
    {
        await _httpThrottle.WaitAsync();  // Odota vuoroa
        try
        {
            Console.WriteLine($"Haetaan: {url}");
            return await httpClient.GetStringAsync(url);
        }
        finally
        {
            _httpThrottle.Release();  // Vapauta paikka seuraavalle
        }
    });

    return await Task.WhenAll(tasks);
}

// Esimerkki: 20 URL:ia, max 5 samanaikaisesti
string[] urls = Enumerable.Range(1, 20)
    .Select(i => $"https://api.example.com/item/{i}")
    .ToArray();

string[] results = await HaeKaikkiAsync(urls);
```

```
Suoritus (max 5 samanaikaisesti):
  Erä 1: [1] [2] [3] [4] [5]  ← 5 samanaikaisesti
  Erä 2: [6] [7] [8] [9] [10] ← Seuraavat 5
  Erä 3: [11][12][13][14][15]
  Erä 4: [16][17][18][19][20]
```

### SemaphoreSlim — timeout ja CancellationToken

```csharp
private readonly SemaphoreSlim _semaphore = new(1, 1);

public async Task<bool> YritaLukitaAsync(CancellationToken ct)
{
    // Yritä saada lukko 5 sekunnissa, kunnioita peruutusta
    bool saatiin = await _semaphore.WaitAsync(
        TimeSpan.FromSeconds(5),
        ct);

    if (!saatiin)
    {
        Console.WriteLine("Timeout — lukkoa ei saatu!");
        return false;
    }

    try
    {
        await TeeTyoAsync(ct);
        return true;
    }
    finally
    {
        _semaphore.Release();
    }
}
```

### SemaphoreSlim — cache stampede -suoja

```csharp
// Estä "cache stampede": vain yksi haku kerrallaan per avain
public class StampedeGuardedCache
{
    private readonly IMemoryCache _cache;
    private readonly ConcurrentDictionary<string, SemaphoreSlim> _locks = new();

    public async Task<T> GetOrCreateAsync<T>(
        string key,
        Func<Task<T>> factory,
        TimeSpan expiration)
    {
        if (_cache.TryGetValue(key, out T? cached))
            return cached!;

        // Oma semaphore per avain
        SemaphoreSlim semaphore = _locks.GetOrAdd(key, _ => new SemaphoreSlim(1, 1));
        await semaphore.WaitAsync();
        try
        {
            // Double-check: joku muu saattoi jo hakea
            if (_cache.TryGetValue(key, out cached))
                return cached!;

            T value = await factory();
            _cache.Set(key, value, expiration);
            return value;
        }
        finally
        {
            semaphore.Release();
        }
    }
}
```

---

## Mutex

`Mutex` on synkronointimekanismi joka toimii **prosessien välillä**. Käytetään harvemmin kuin `lock` tai `SemaphoreSlim`.

### Käyttökohde: Vain yksi instanssi sovelluksesta

```csharp
// Estä saman sovelluksen useampi instanssi
using Mutex mutex = new Mutex(false, "Global\\MinunSovellus_UniqueId");

if (!mutex.WaitOne(0))
{
    Console.WriteLine("Sovellus on jo käynnissä!");
    return;
}

try
{
    Console.WriteLine("Sovellus käynnistetty.");
    // Sovelluksen normaali suoritus...
    Console.ReadLine();
}
finally
{
    mutex.ReleaseMutex();
}
```

### Mutex vs lock vs SemaphoreSlim

| Ominaisuus | `lock` | `SemaphoreSlim` | `Mutex` |
|------------|--------|-----------------|---------|
| **Async-tuki** | ❌ | ✅ | ❌ |
| **Prosessien välillä** | ❌ | ❌ | ✅ |
| **Max samanaikaisia** | 1 | N (konfiguroitava) | 1 |
| **Suorituskyky** | ⚡ Nopein | ⚡ Nopea | 🐢 Hidas |
| **Käyttökohde** | Yksinkertainen lukitus | Async + throttling | Prosessien välinen |

---

## ReaderWriterLockSlim

`ReaderWriterLockSlim` **erottelee lukijat ja kirjoittajat**: useat säikeet voivat lukea samanaikaisesti, mutta kirjoitus on yksinoikeudella.

### Peruskäyttö

```csharp
public class SaikeisturvallinenRekisteri
{
    private readonly Dictionary<string, string> _data = new();
    private readonly ReaderWriterLockSlim _rwLock = new();

    // Useat säikeet voivat lukea SAMANAIKAISESTI
    public string? Lue(string avain)
    {
        _rwLock.EnterReadLock();
        try
        {
            return _data.TryGetValue(avain, out string? arvo) ? arvo : null;
        }
        finally
        {
            _rwLock.ExitReadLock();
        }
    }

    // Vain YKSI säie kerrallaan voi kirjoittaa
    public void Kirjoita(string avain, string arvo)
    {
        _rwLock.EnterWriteLock();
        try
        {
            _data[avain] = arvo;
        }
        finally
        {
            _rwLock.ExitWriteLock();
        }
    }

    // Upgradeable: Lue ensin, kirjoita tarvittaessa
    public string LueJaPaivita(string avain, string oletusarvo)
    {
        _rwLock.EnterUpgradeableReadLock();
        try
        {
            if (_data.TryGetValue(avain, out string? arvo))
                return arvo;

            // Tarvitaan kirjoitus
            _rwLock.EnterWriteLock();
            try
            {
                _data[avain] = oletusarvo;
                return oletusarvo;
            }
            finally
            {
                _rwLock.ExitWriteLock();
            }
        }
        finally
        {
            _rwLock.ExitUpgradeableReadLock();
        }
    }
}
```

### Milloin ReaderWriterLockSlim?

```
Paljon lukuja, vähän kirjoituksia:
  Reader 1: ████ ████ ████ ████  (samanaikaisesti!)
  Reader 2: ████ ████ ████ ████
  Writer:        ██                (yksinoikeus)
  Reader 3: ████      ████ ████

→ Lukijat eivät estä toisiaan
→ Kirjoittaja estää kaikki muut
```

**Käytä kun:**
- Lukuja on paljon enemmän kuin kirjoituksia (esim. 90% luku, 10% kirjoitus)
- Lukuoperaatiot ovat nopeita

**Älä käytä kun:**
- Lukujen ja kirjoitusten suhde on tasainen → käytä `lock`
- Tarvitset async-tukea → käytä `SemaphoreSlim`

---

## Interlocked

`Interlocked`-luokka tarjoaa **atomiset operaatiot** yksinkertaisille arvoille. Ei vaadi lukkoja!

### Peruskäyttö

```csharp
public class AtominenLaskuri
{
    private int _arvo = 0;

    // ✅ Atominen kasvatus (ei tarvita lock:ia!)
    public void Kasvata()
    {
        Interlocked.Increment(ref _arvo);
    }

    // ✅ Atominen vähennys
    public void Vahenna()
    {
        Interlocked.Decrement(ref _arvo);
    }

    // ✅ Atominen lisäys
    public void Lisaa(int maara)
    {
        Interlocked.Add(ref _arvo, maara);
    }

    // ✅ Atominen luku
    public int Arvo => Interlocked.CompareExchange(ref _arvo, 0, 0);
}
```

### CompareExchange — ehdollinen päivitys

```csharp
// "Jos arvo on X, vaihda se Y:ksi"
// Atominen operaatio, ei tarvitse lock:ia

public class AtominenMax
{
    private int _max = int.MinValue;

    public void PaivitaMax(int uusiArvo)
    {
        int nykyinen;
        do
        {
            nykyinen = _max;
            if (uusiArvo <= nykyinen)
                return;  // Ei tarvitse päivittää
        }
        while (Interlocked.CompareExchange(ref _max, uusiArvo, nykyinen) != nykyinen);
        // Jos joku muu muutti _max:ia välissä → yritä uudelleen
    }

    public int Max => _max;
}
```

### Interlocked — käyttökohteet

```csharp
// Yhtäaikaisten pyyntöjen laskuri
public class RequestCounter
{
    private long _totalRequests = 0;
    private int _activeRequests = 0;

    public async Task<T> TrackRequestAsync<T>(Func<Task<T>> handler)
    {
        Interlocked.Increment(ref _totalRequests);
        Interlocked.Increment(ref _activeRequests);
        try
        {
            return await handler();
        }
        finally
        {
            Interlocked.Decrement(ref _activeRequests);
        }
    }

    public long TotalRequests => Interlocked.Read(ref _totalRequests);
    public int ActiveRequests => _activeRequests;
}
```

### Interlocked vs lock

| Ominaisuus | `Interlocked` | `lock` |
|------------|---------------|--------|
| **Suorituskyky** | ⚡⚡ Erittäin nopea | ⚡ Nopea |
| **Käyttökohde** | Yksittäiset arvot (int, long) | Monimutkainen logiikka |
| **Monimutkaisuus** | Yksinkertainen | Yksinkertainen |
| **Useita operaatioita** | ❌ Vain yksi kerrallaan | ✅ Monta operaatiota |

---

## Double-checked locking

**Double-checked locking** on optimointitekniikka joka välttää turhia lukituksia.

### Tyypillinen esimerkki: Lazy-alustus

```csharp
public class SingletonService
{
    private static SingletonService? _instance;
    private static readonly object _lukko = new();

    // ❌ HUONO: Lukitsee JOKA kutsulla
    public static SingletonService InstanceHuono
    {
        get
        {
            lock (_lukko)
            {
                if (_instance == null)
                    _instance = new SingletonService();
                return _instance;
            }
        }
    }

    // ✅ HYVÄ: Double-checked locking
    public static SingletonService Instance
    {
        get
        {
            if (_instance == null)  // 1. tarkistus (ei lukkoa)
            {
                lock (_lukko)
                {
                    if (_instance == null)  // 2. tarkistus (lukon sisällä)
                    {
                        _instance = new SingletonService();
                    }
                }
            }
            return _instance;
        }
    }

    // ✅ PARAS: Käytä Lazy<T>
    private static readonly Lazy<SingletonService> _lazy =
        new(() => new SingletonService());

    public static SingletonService InstanceParas => _lazy.Value;
}
```

### Lazy\<T\> — helpoin tapa

```csharp
public class AppConfig
{
    // Lazy<T> hoitaa säikeisturvallisuuden automaattisesti
    private static readonly Lazy<AppConfig> _instance =
        new(() => new AppConfig());

    public static AppConfig Instance => _instance.Value;

    // Myös async-kontekstissa
    private readonly Lazy<Task<List<string>>> _kaupungit;

    public AppConfig()
    {
        _kaupungit = new Lazy<Task<List<string>>>(
            () => HaeKaupungitAsync());
    }

    public Task<List<string>> Kaupungit => _kaupungit.Value;

    private async Task<List<string>> HaeKaupungitAsync()
    {
        // Haetaan vain kerran
        return await httpClient.GetFromJsonAsync<List<string>>(
            "https://api.example.com/cities") ?? new();
    }
}
```

---

## Deadlock

**Deadlock** syntyy kun kaksi (tai useampaa) säiettä odottavat toisiaan ikuisesti.

### Klassinen deadlock

```csharp
// ❌ DEADLOCK!
private readonly object _lukkoA = new();
private readonly object _lukkoB = new();

// Thread 1
public void Metodi1()
{
    lock (_lukkoA)           // 1. Saa lukon A
    {
        Thread.Sleep(100);   // Simuloi työtä
        lock (_lukkoB)       // 3. Odottaa lukkoa B... (Thread 2:lla!)
        {
            Console.WriteLine("Metodi1 valmis");
        }
    }
}

// Thread 2
public void Metodi2()
{
    lock (_lukkoB)           // 2. Saa lukon B
    {
        Thread.Sleep(100);   // Simuloi työtä
        lock (_lukkoA)       // 4. Odottaa lukkoa A... (Thread 1:llä!)
        {
            Console.WriteLine("Metodi2 valmis");
        }
    }
}

// Käynnistä → DEADLOCK!
Task.Run(() => Metodi1());
Task.Run(() => Metodi2());
```

```
Deadlock-tilanne:

  Thread 1: Omistaa A, odottaa B ──────┐
                                        │
  Thread 2: Omistaa B, odottaa A ──┐    │
                                   │    │
            ┌──────────────────────┘    │
            │  ┌────────────────────────┘
            ▼  ▼
         IKUINEN ODOTUS!
```

### Deadlockin välttäminen

```csharp
// ✅ Ratkaisu 1: Hanki lukot AINA samassa järjestyksessä
public void Metodi1Korjattu()
{
    lock (_lukkoA)       // Aina A ensin
    {
        lock (_lukkoB)   // Sitten B
        {
            Console.WriteLine("Metodi1 valmis");
        }
    }
}

public void Metodi2Korjattu()
{
    lock (_lukkoA)       // Aina A ensin (sama järjestys!)
    {
        lock (_lukkoB)   // Sitten B
        {
            Console.WriteLine("Metodi2 valmis");
        }
    }
}
```

```csharp
// ✅ Ratkaisu 2: Käytä Monitor.TryEnter timeoutilla
public bool TurvallisempiMetodi()
{
    lock (_lukkoA)
    {
        if (Monitor.TryEnter(_lukkoB, TimeSpan.FromSeconds(5)))
        {
            try
            {
                Console.WriteLine("Valmis!");
                return true;
            }
            finally
            {
                Monitor.Exit(_lukkoB);
            }
        }
        else
        {
            Console.WriteLine("Ei saatu lukkoa B — mahdollinen deadlock!");
            return false;
        }
    }
}
```

```csharp
// ✅ Ratkaisu 3: Käytä yhtä lukkoa
private readonly object _yhteisLukko = new();

public void Metodi1Yksinkertainen()
{
    lock (_yhteisLukko)
    {
        // Kaikki kriittinen koodi yhden lukon sisällä
        Console.WriteLine("Valmis");
    }
}
```

### async/await deadlock

```csharp
// ❌ DEADLOCK (WPF/WinForms, vanha ASP.NET)
public void Button_Click(object sender, EventArgs e)
{
    // .Result blokkaa UI-säikeen
    // GetDataAsync yrittää palata UI-säikeeseen → deadlock!
    string data = GetDataAsync().Result;
}

// ✅ RATKAISU 1: Käytä async/await
public async void Button_Click(object sender, EventArgs e)
{
    string data = await GetDataAsync();
}

// ✅ RATKAISU 2: ConfigureAwait(false) kirjastossa
public async Task<string> GetDataAsync()
{
    return await httpClient.GetStringAsync(url)
        .ConfigureAwait(false);  // Ei vaadi UI-säiettä
}
```

---

## Vertailutaulukko

| Mekanismi | Async | Prosessien välillä | Max samanaikaiset | Suorituskyky | Käyttökohde |
|-----------|-------|--------------------|-------------------|--------------|-------------|
| `lock` | ❌ | ❌ | 1 | ⚡⚡⚡ | Yksinkertainen lukitus |
| `Monitor` | ❌ | ❌ | 1 | ⚡⚡⚡ | lock + timeout + Wait/Pulse |
| `SemaphoreSlim` | ✅ | ❌ | N | ⚡⚡ | Async lukitus, throttling |
| `Mutex` | ❌ | ✅ | 1 | ⚡ | Prosessien välinen lukitus |
| `ReaderWriterLockSlim` | ❌ | ❌ | N lukijaa / 1 kirjoittaja | ⚡⚡ | Read-heavy skenaariot |
| `Interlocked` | - | ❌ | - | ⚡⚡⚡⚡ | Atomiset yksittäisarvot |
| `Lazy<T>` | ✅ | ❌ | - | ⚡⚡⚡ | Lazy-alustus |

### Valintaopas

```
Tarvitsetko synkronointia?
│
├─ Yksittäinen arvo (int, long)?
│  └─ → Interlocked
│
├─ Tarvitaanko await lock:n sisällä?
│  └─ → SemaphoreSlim(1, 1)
│
├─ Rajoitettu samanaikaisuus (max N)?
│  └─ → SemaphoreSlim(N, N)
│
├─ Paljon lukuja, vähän kirjoituksia?
│  └─ → ReaderWriterLockSlim
│
├─ Prosessien välinen lukitus?
│  └─ → Mutex
│
├─ Lazy-alustus?
│  └─ → Lazy<T>
│
└─ Muu yksinkertainen lukitus?
   └─ → lock
```

---

## Yhteenveto

### Muistilista

1. **`lock`** — Yksinkertainen, nopea, käytä oletuksena synkroniselle koodille
2. **`SemaphoreSlim`** — Asynkroninen lukitus ja throttling (`WaitAsync`)
3. **`Interlocked`** — Atomiset operaatiot yksittäisille arvoille (nopein)
4. **`Mutex`** — Prosessien välinen lukitus (harvoin tarvittu)
5. **`ReaderWriterLockSlim`** — Read-heavy skenaariot
6. **`Lazy<T>`** — Säikeisturvallinen lazy-alustus

### Tärkeimmät säännöt

- ✅ Pidä lukittu osio **mahdollisimman lyhyenä**
- ✅ Hanki lukot **aina samassa järjestyksessä** (deadlockin esto)
- ✅ Käytä `SemaphoreSlim`:iä kun tarvitset `await`:ia lukon sisällä
- ✅ Vapauta lukko **aina** (käytä `try/finally`)
- ❌ Älä kutsu **ulkoista koodia** lukon sisältä
- ❌ Älä lukitse `this`:iä, tyyppejä tai stringejä

---

## Hyödyllisiä linkkejä

- [Microsoft: lock statement](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/lock)
- [Microsoft: SemaphoreSlim](https://learn.microsoft.com/en-us/dotnet/api/system.threading.semaphoreslim)
- [Microsoft: Interlocked](https://learn.microsoft.com/en-us/dotnet/api/system.threading.interlocked)
- [Microsoft: ReaderWriterLockSlim](https://learn.microsoft.com/en-us/dotnet/api/system.threading.readerwriterlockslim)
- [Microsoft: Managed threading best practices](https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-best-practices)

### Seuraavaksi

- [Concurrent Collections](Concurrent-Collections.md) — Säikeisturvalliset kokoelmat jotka eivät tarvitse manuaalista lukitusta
