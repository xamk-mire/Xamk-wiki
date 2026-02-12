# Async/Await - Asynkroninen ohjelmointi

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi asynkroninen ohjelmointi?](#miksi-asynkroninen-ohjelmointi)
3. [async ja await perusteet](#async-ja-await-perusteet)
4. [Task ja Task\<T\>](#task-ja-taskt)
5. [Task.WhenAll ja Task.WhenAny](#taskwhenall-ja-taskwhenany)
6. [CancellationToken](#cancellationtoken)
7. [ValueTask](#valuetask)
8. [Virheenkäsittely async-koodissa](#virheenkäsittely-async-koodissa)
9. [Anti-patterns ja sudenkuopat](#anti-patterns-ja-sudenkuopat)
10. [Best Practices](#best-practices)
11. [Yhteenveto](#yhteenveto)
12. [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Johdanto

**Asynkroninen ohjelmointi** mahdollistaa pitkäkestoisten operaatioiden (tietokanta, HTTP, tiedostot) suorittamisen **ilman säikeen blokkausta**. C#:n `async`/`await`-malli tekee asynkronisesta koodista lähes yhtä luettavaa kuin synkronisesta.

**Perusidea:**

```
Synkroninen (blokkaa):
  Thread: ████ [odottaa DB:tä 200ms...] ████
                ↑ Säie on lukittu!

Asynkroninen (ei blokkaa):
  Thread: ████ → vapauta säie → ████ (jatka kun DB vastaa)
               ↑ Säie tekee muuta työtä odotuksen ajan
```

---

## Miksi asynkroninen ohjelmointi?

### Ongelma: Synkroninen koodi blokkaa

```csharp
// ❌ Synkroninen - blokkaa säikeen
public string GetData()
{
    string result = httpClient.GetStringAsync("https://api.example.com/data").Result; // BLOKKAA!
    return result;
}
```

**Ongelmia:**
- Säie on lukittu odotuksen ajan
- Web-sovelluksessa: vähemmän samanaikaisia pyyntöjä
- UI-sovelluksessa: käyttöliittymä jäätyy
- Skaalautuvuus kärsii

### Ratkaisu: Asynkroninen koodi

```csharp
// ✅ Asynkroninen - ei blokkaa säiettä
public async Task<string> GetDataAsync()
{
    string result = await httpClient.GetStringAsync("https://api.example.com/data");
    return result;
}
```

**Edut:**
- ✅ Säie vapautuu odotuksen ajaksi
- ✅ Parempi skaalautuvuus (enemmän samanaikaisia pyyntöjä)
- ✅ UI pysyy responsiivisena
- ✅ Tehokkaampi resurssien käyttö

### Performance-vertailu (ASP.NET Core)

| Metrikka | Synkroninen | Asynkroninen | Parannus |
|----------|-------------|--------------|----------|
| Samanaikaiset pyynnöt | 100 | 10 000+ | **100×** |
| Säikeiden käyttö | 1 per pyyntö | Jaettu | **Tehokkaampi** |
| Muistin käyttö | Korkea | Matala | **Merkittävä** |

---

## async ja await perusteet

### Syntaksi

```csharp
// async-avainsana metodin määrittelyssä
// await-avainsana asynkronisen operaation edessä
public async Task<string> HaeDataAsync()
{
    string tulos = await HaeTietokannasta();
    return tulos;
}
```

**Säännöt:**
1. `async`-avainsana lisätään metodin paluuarvon eteen
2. Paluuarvo on `Task`, `Task<T>` tai `ValueTask<T>`
3. `await` voidaan käyttää vain `async`-metodin sisällä
4. Metodin nimi päättyy konvention mukaan `Async`-sanaan

### Perusesimerkki

```csharp
using System.Net.Http;

public class DataService
{
    private readonly HttpClient _httpClient = new();

    // Asynkroninen metodi joka palauttaa stringin
    public async Task<string> HaeSaaAsync(string kaupunki)
    {
        Console.WriteLine("Haetaan säätietoja...");

        // await vapauttaa säikeen odotuksen ajaksi
        string vastaus = await _httpClient.GetStringAsync(
            $"https://api.weather.com/{kaupunki}");

        Console.WriteLine("Säätiedot saatu!");
        return vastaus;
    }
}

// Käyttö
DataService service = new DataService();
string saa = await service.HaeSaaAsync("Helsinki");
Console.WriteLine(saa);
```

### Task vs Task\<T\> vs void

```csharp
// Task<T> - palauttaa arvon
public async Task<int> LaskeAsync()
{
    await Task.Delay(100);
    return 42;
}

// Task - ei palauta arvoa (kuten void, mutta awaitable)
public async Task TallennaAsync(string data)
{
    await File.WriteAllTextAsync("data.txt", data);
}

// ❌ async void - VÄLTÄ! (paitsi event handlerit)
// Poikkeuksia ei voi catchata!
public async void VaarallinenMetodi()
{
    await Task.Delay(100);
    throw new Exception("Tätä ei voi catchata!");
}
```

### Miten async/await toimii?

```csharp
public async Task<string> EsimerkkiAsync()
{
    Console.WriteLine("1. Ennen awaitia");   // Suoritetaan kutsuvassa säikeessä

    await Task.Delay(1000);                   // Säie vapautetaan 1s ajaksi

    Console.WriteLine("2. Awaitin jälkeen"); // Suoritetaan (mahdollisesti eri) säikeessä

    return "Valmis";
}
```

```
Mitä tapahtuu kulissien takana:

1. Metodi alkaa normaalisti
2. await-kohdassa:
   a. Task ei ole valmis → metodi "pysähtyy"
   b. Säie vapautetaan takaisin ThreadPooliin
   c. Kääntäjä luo state machinen (IAsyncStateMachine)
3. Kun Task valmistuu:
   a. Jatkuu state machinen seuraavasta tilasta
   b. Säie (mahdollisesti eri) jatkaa suoritusta
```

---

## Task ja Task\<T\>

### Task — asynkroninen operaatio

`Task` edustaa käynnissä olevaa tai tulevaisuudessa valmistuvaa operaatiota.

```csharp
// Task.Run — suorita CPU-työ taustasäikeessä
Task<int> laskentatask = Task.Run(() =>
{
    // Raskas laskenta
    int summa = 0;
    for (int i = 0; i < 1_000_000; i++)
        summa += i;
    return summa;
});

int tulos = await laskentatask;
Console.WriteLine($"Summa: {tulos}");
```

### Task.Delay — asynkroninen odotus

```csharp
// ✅ Task.Delay — ei blokkaa säiettä
await Task.Delay(2000); // Odota 2 sekuntia asynkronisesti

// ❌ Thread.Sleep — blokkaa säikeen
Thread.Sleep(2000); // Säie on lukittu 2 sekuntia!
```

> **Vinkki:** Katso lisää [Thread.Sleep vs Task.Delay](../../00-Basics/Thread-Sleep.md)

### Task.Run — milloin käyttää?

```csharp
// ✅ HYVÄ: CPU-intensiivinen työ UI-sovelluksessa
int tulos = await Task.Run(() => RaskasLaskenta());

// ❌ HUONO: I/O-operaatio Task.Run:ssa (turhaa)
string data = await Task.Run(() => httpClient.GetStringAsync(url)); // Älä tee näin!

// ✅ HYVÄ: I/O-operaatio suoraan
string data = await httpClient.GetStringAsync(url);
```

**Nyrkkisääntö:**
- `Task.Run` → CPU-intensiivinen työ
- `await` suoraan → I/O-operaatiot (HTTP, tietokanta, tiedostot)

---

## Task.WhenAll ja Task.WhenAny

### Task.WhenAll — odota kaikkien valmistumista

```csharp
// Käynnistä kolme API-kutsua SAMANAIKAISESTI
Task<string> task1 = httpClient.GetStringAsync("https://api.example.com/users");
Task<string> task2 = httpClient.GetStringAsync("https://api.example.com/products");
Task<string> task3 = httpClient.GetStringAsync("https://api.example.com/orders");

// Odota kaikkien valmistumista
string[] tulokset = await Task.WhenAll(task1, task2, task3);

Console.WriteLine($"Users: {tulokset[0]}");
Console.WriteLine($"Products: {tulokset[1]}");
Console.WriteLine($"Orders: {tulokset[2]}");
```

**Suoritusaikavertailu:**

```
Peräkkäin (await yksi kerrallaan):
  Task1: ████████ (200ms)
  Task2:         ████████ (200ms)
  Task3:                 ████████ (200ms)
  Yhteensä: 600ms

Samanaikaisesti (Task.WhenAll):
  Task1: ████████ (200ms)
  Task2: ████████ (200ms)
  Task3: ████████ (200ms)
  Yhteensä: 200ms ← 3× nopeampi!
```

### Käytännön esimerkki: Dashboard-data

```csharp
public async Task<DashboardDto> HaeDashboardAsync(int userId)
{
    // Käynnistä kaikki haut SAMAAN AIKAAN
    Task<User> userTask = _userRepository.GetByIdAsync(userId);
    Task<List<Order>> ordersTask = _orderRepository.GetByUserIdAsync(userId);
    Task<UserStats> statsTask = _statsService.GetUserStatsAsync(userId);

    // Odota kaikkien valmistumista
    await Task.WhenAll(userTask, ordersTask, statsTask);

    return new DashboardDto
    {
        User = userTask.Result,       // Jo valmis, ei blokkaa
        Orders = ordersTask.Result,
        Stats = statsTask.Result
    };
}
```

### Task.WhenAny — odota ensimmäistä valmistuvaa

```csharp
// Käytä nopeinta API:a
Task<string> eurooppaTask = httpClient.GetStringAsync("https://eu.api.example.com/data");
Task<string> usaTask = httpClient.GetStringAsync("https://us.api.example.com/data");

// Kumpi vastaa ensin?
Task<string> nopein = await Task.WhenAny(eurooppaTask, usaTask);
string tulos = await nopein;

Console.WriteLine($"Nopein vastasi: {tulos}");
```

### Task.WhenAny — timeout-pattern

```csharp
public async Task<string?> HaeTimeoutillaAsync(string url, int timeoutMs)
{
    Task<string> dataTask = httpClient.GetStringAsync(url);
    Task timeoutTask = Task.Delay(timeoutMs);

    // Kumpi valmistuu ensin?
    Task valmistunut = await Task.WhenAny(dataTask, timeoutTask);

    if (valmistunut == timeoutTask)
    {
        Console.WriteLine("Timeout! Pyyntö kesti liian kauan.");
        return null;
    }

    return await dataTask;
}
```

---

## CancellationToken

`CancellationToken` mahdollistaa asynkronisten operaatioiden **peruuttamisen**.

### Peruskäyttö

```csharp
public async Task<string> HaeDataAsync(CancellationToken cancellationToken = default)
{
    // Tarkista onko peruutettu
    cancellationToken.ThrowIfCancellationRequested();

    // Välitä token eteenpäin
    string response = await httpClient.GetStringAsync(
        "https://api.example.com/data",
        cancellationToken);

    return response;
}
```

### CancellationTokenSource

```csharp
// Luo CancellationTokenSource
using CancellationTokenSource cts = new CancellationTokenSource();

// Peruuta automaattisesti 5 sekunnin jälkeen
cts.CancelAfter(TimeSpan.FromSeconds(5));

try
{
    string data = await HaeDataAsync(cts.Token);
    Console.WriteLine(data);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Operaatio peruutettiin (timeout).");
}
```

### Manuaalinen peruutus

```csharp
using CancellationTokenSource cts = new CancellationTokenSource();

// Käynnistä pitkä operaatio taustalla
Task task = PitkaOperaatioAsync(cts.Token);

// Käyttäjä painaa Enter → peruuta
Console.WriteLine("Paina Enter peruuttaaksesi...");
Console.ReadLine();
cts.Cancel();

try
{
    await task;
}
catch (OperationCanceledException)
{
    Console.WriteLine("Peruutettu!");
}
```

### CancellationToken ASP.NET Core:ssa

```csharp
// ASP.NET Core antaa automaattisesti CancellationTokenin
// joka peruuntuu kun käyttäjä sulkee yhteyden
[HttpGet("products")]
public async Task<IActionResult> GetProducts(CancellationToken cancellationToken)
{
    List<Product> products = await _repository.GetAllAsync(cancellationToken);
    return Ok(products);
}

// Repository
public async Task<List<Product>> GetAllAsync(CancellationToken cancellationToken)
{
    return await _db.Products
        .AsNoTracking()
        .ToListAsync(cancellationToken);  // Välitä token eteenpäin!
}
```

### CancellationToken — linked tokens

```csharp
// Yhdistä useita peruutusehtoja
using CancellationTokenSource timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
using CancellationTokenSource linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
    timeoutCts.Token,
    httpContext.RequestAborted  // Käyttäjä sulkee yhteyden
);

// Peruuntuu JOS:
// 1. Timeout (30s) ylittyy TAI
// 2. Käyttäjä sulkee yhteyden
await ProsessoiAsync(linkedCts.Token);
```

---

## ValueTask

`ValueTask<T>` on optimoitu versio `Task<T>`:stä tilanteisiin joissa tulos on usein **jo valmiina**.

### Milloin käyttää?

```csharp
// Esimerkki: Cache joka palauttaa usein heti
public ValueTask<Product?> GetProductAsync(int id)
{
    // 90% ajasta: cache hit → ei tarvita Task-allokointia
    if (_cache.TryGetValue(id, out Product? cached))
        return new ValueTask<Product?>(cached);  // Ei allokaatiota!

    // 10% ajasta: cache miss → haetaan async
    return new ValueTask<Product?>(GetFromDatabaseAsync(id));
}

private async Task<Product?> GetFromDatabaseAsync(int id)
{
    Product? product = await _db.Products.FindAsync(id);
    _cache[id] = product;
    return product;
}
```

### Task vs ValueTask

| Ominaisuus | `Task<T>` | `ValueTask<T>` |
|------------|-----------|-----------------|
| **Allokaatio** | Aina (heap) | Ei, jos tulos on heti valmis |
| **Await useasti** | ✅ Kyllä | ❌ Vain kerran! |
| **Tallenna muuttujaan** | ✅ Kyllä | ❌ Vaarallista |
| **Käyttö** | Oletusvalinta | Optimointi (hot path) |

**Nyrkkisääntö:**
- Käytä `Task<T>` oletuksena
- Käytä `ValueTask<T>` vain kun profilointi osoittaa tarpeen (esim. cache-skenaariot)

---

## Virheenkäsittely async-koodissa

### try/catch toimii normaalisti

```csharp
public async Task<string> HaeDataTurvallisestiAsync()
{
    try
    {
        string data = await httpClient.GetStringAsync("https://api.example.com/data");
        return data;
    }
    catch (HttpRequestException ex)
    {
        Console.WriteLine($"HTTP-virhe: {ex.Message}");
        return "Varatietoa";
    }
    catch (TaskCanceledException)
    {
        Console.WriteLine("Pyyntö aikakatkaistiin.");
        return "Timeout";
    }
}
```

### Virheenkäsittely Task.WhenAll:ssa

```csharp
Task<string> task1 = HaeAsync("https://api1.example.com");
Task<string> task2 = HaeAsync("https://api2.example.com");
Task<string> task3 = HaeAsync("https://api3.example.com");

try
{
    string[] tulokset = await Task.WhenAll(task1, task2, task3);
}
catch (Exception ex)
{
    // HUOM: await heittää vain ensimmäisen poikkeuksen!
    Console.WriteLine($"Virhe: {ex.Message}");

    // Kaikkien poikkeusten tarkistus:
    if (task1.IsFaulted) Console.WriteLine($"Task1: {task1.Exception?.InnerException?.Message}");
    if (task2.IsFaulted) Console.WriteLine($"Task2: {task2.Exception?.InnerException?.Message}");
    if (task3.IsFaulted) Console.WriteLine($"Task3: {task3.Exception?.InnerException?.Message}");
}
```

### AggregateException

```csharp
Task task = Task.WhenAll(
    Task.Run(() => throw new InvalidOperationException("Virhe 1")),
    Task.Run(() => throw new ArgumentException("Virhe 2"))
);

try
{
    await task;
}
catch
{
    // task.Exception on AggregateException joka sisältää KAIKKI virheet
    if (task.Exception != null)
    {
        foreach (Exception ex in task.Exception.InnerExceptions)
        {
            Console.WriteLine($"Virhe: {ex.GetType().Name}: {ex.Message}");
        }
    }
}

// Tulostus:
// Virhe: InvalidOperationException: Virhe 1
// Virhe: ArgumentException: Virhe 2
```

---

## Anti-patterns ja sudenkuopat

### 1. async void — ÄLÄ KÄYTÄ

```csharp
// ❌ VAARALLISTA: async void
public async void LataaTiedot()
{
    string data = await httpClient.GetStringAsync(url);
    // Jos tämä heittää poikkeuksen → sovellus kaatuu!
    // Poikkeusta EI VOI catchata kutsuvassa koodissa!
}

// ✅ OIKEIN: async Task
public async Task LataaTiedotAsync()
{
    string data = await httpClient.GetStringAsync(url);
}

// ✅ POIKKEUS: Event handlerit (ainoa OK käyttökohde async void:lle)
button.Click += async (sender, e) =>
{
    await LataaTiedotAsync();
};
```

### 2. .Result ja .Wait() — deadlock-riski

```csharp
// ❌ DEADLOCK-RISKI (erityisesti ASP.NET ja WPF:ssä)
public string GetData()
{
    // .Result blokkaa säikeen JA odottaa Taskin valmistumista
    // Mutta Task yrittää palata samaan säikeeseen → deadlock!
    string result = GetDataAsync().Result;
    return result;
}

// ❌ Sama ongelma .Wait():lla
public void SaveData()
{
    SaveDataAsync().Wait(); // Deadlock!
}

// ✅ OIKEIN: async "kuplii ylös"
public async Task<string> GetDataAsync()
{
    return await httpClient.GetStringAsync(url);
}
```

### 3. Async ei "kupli ylös" — sync-over-async

```csharp
// ❌ HUONO: Synkroninen metodi kutsuu asynkronista
public List<Product> GetProducts()
{
    // Blokkaa ja voi aiheuttaa deadlockin
    return GetProductsAsync().Result;
}

// ✅ HYVÄ: Tee koko ketju asynkroniseksi
public async Task<List<Product>> GetProductsAsync()
{
    return await _repository.GetAllAsync();
}
```

**Nyrkkisääntö:** Async kuplii ylöspäin — kun yksi metodi on async, myös kutsuvien metodien tulee olla async.

### 4. Turha async/await

```csharp
// ❌ TURHA: async/await ei tee mitään hyödyllistä
public async Task<int> HaeIdAsync()
{
    return await _repository.GetIdAsync();  // Turha wrapper
}

// ✅ PAREMPI: Palauta Task suoraan
public Task<int> HaeIdAsync()
{
    return _repository.GetIdAsync();  // Ei turhaa state machinea
}

// ⚠️ MUTTA: Jos metodissa on try/catch, using tai muuta logiikkaa → käytä async/await
public async Task<int> HaeIdTurvallisestiAsync()
{
    try
    {
        return await _repository.GetIdAsync();
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Virhe!");
        return -1;
    }
}
```

### 5. await silmukassa (N+1 ongelma)

```csharp
// ❌ HIDAS: Peräkkäiset kutsut silmukassa
foreach (int id in productIds)
{
    Product product = await _repository.GetByIdAsync(id);  // Odottaa jokaista erikseen!
    products.Add(product);
}

// ✅ NOPEAMPI: Samanaikaiset kutsut
IEnumerable<Task<Product>> tasks = productIds.Select(id => _repository.GetByIdAsync(id));
Product[] products = await Task.WhenAll(tasks);

// ✅ TAI: Yksi kysely joka hakee kaikki kerralla
List<Product> products = await _repository.GetByIdsAsync(productIds);
```

---

## Best Practices

### 1. Nimeä async-metodit Async-päätteellä

```csharp
// ✅ Selkeä nimeäminen
public async Task<User> GetUserAsync(int id) { ... }
public async Task SaveAsync(User user) { ... }
public async Task<List<Order>> GetOrdersAsync() { ... }
```

### 2. Välitä CancellationToken aina eteenpäin

```csharp
// ✅ Token kulkee koko ketjun läpi
public async Task<Product> GetProductAsync(int id, CancellationToken ct = default)
{
    Product? dbProduct = await _db.Products.FindAsync(new object[] { id }, ct);
    List<Review> reviews = await _reviewService.GetReviewsAsync(id, ct);
    return MapToProduct(dbProduct, reviews);
}
```

### 3. Käytä ConfigureAwait(false) kirjastoissa

```csharp
// Kirjastokoodissa: ei tarvita UI-kontekstia
public async Task<string> GetDataAsync()
{
    string result = await httpClient.GetStringAsync(url)
        .ConfigureAwait(false);  // Ei palaa alkuperäiseen kontekstiin
    return result;
}

// ASP.NET Core:ssa: EI tarvita (ei SynchronizationContextia)
// WPF/WinForms:ssa: ConfigureAwait(false) kirjastoissa
```

### 4. Vältä turhia Task.Run-kutsuja

```csharp
// ❌ Turha Task.Run I/O-operaatiolle
List<Product> data = await Task.Run(() => _db.Products.ToListAsync());

// ✅ Suoraan await
List<Product> data = await _db.Products.ToListAsync();

// ✅ Task.Run vain CPU-työlle
string hash = await Task.Run(() => ComputeExpensiveHash(data));
```

### 5. Disposoi resurssit oikein

```csharp
public async Task ProsessoiTiedostoAsync(string polku)
{
    // ✅ await using - asynkroninen disposeinti
    await using FileStream stream = new FileStream(polku, FileMode.Open, FileAccess.Read,
        FileShare.Read, bufferSize: 4096, useAsync: true);
    await using StreamReader reader = new StreamReader(stream);

    string sisalto = await reader.ReadToEndAsync();
    Console.WriteLine(sisalto);
}
```

---

## Yhteenveto

### Perusperiaatteet

| Periaate | Selitys |
|----------|---------|
| `async Task<T>` | Asynkroninen metodi joka palauttaa arvon |
| `async Task` | Asynkroninen metodi ilman paluuarvoa |
| `await` | Odota operaation valmistumista vapauttaen säie |
| `Task.WhenAll` | Suorita useita operaatioita samanaikaisesti |
| `CancellationToken` | Peruuta asynkroninen operaatio |

### Muistilista

1. **Älä käytä `async void`** — käytä `async Task`
2. **Älä käytä `.Result` tai `.Wait()`** — käytä `await`
3. **Async kuplii ylös** — tee koko kutsuketju asynciksi
4. **Välitä `CancellationToken`** — mahdollistaa peruutuksen
5. **Käytä `Task.WhenAll`** — samanaikaiset operaatiot rinnakkain
6. **`Task.Run` vain CPU-työlle** — I/O:lle suora `await`
7. **Nimeä metodit `Async`-päätteellä** — selkeä konventio

---

## Hyödyllisiä linkkejä

- [Microsoft: Asynchronous programming with async and await](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [Microsoft: Task-based asynchronous pattern (TAP)](https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap)
- [Stephen Cleary: Async Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
- [Microsoft: Cancellation in managed threads](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)

### Seuraavaksi

- [Synkronointi (lock, SemaphoreSlim)](Synchronization.md) — Opi suojaamaan jaettu data asynkronisessa koodissa
