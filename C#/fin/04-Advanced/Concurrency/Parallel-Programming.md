# Rinnakkaisohjelmointi (Parallel Programming)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Milloin rinnakkaistaa?](#milloin-rinnakkaistaa)
3. [Parallel.For ja Parallel.ForEach](#parallelfor-ja-parallelforeach)
4. [Parallel.ForEachAsync](#parallelforeachasync)
5. [PLINQ (Parallel LINQ)](#plinq-parallel-linq)
6. [Task.Run ja manuaalinen rinnakkaistaminen](#taskrun-ja-manuaalinen-rinnakkaistaminen)
7. [Thread Safety rinnakkaisessa koodissa](#thread-safety-rinnakkaisessa-koodissa)
8. [Best Practices](#best-practices)
9. [Yhteenveto](#yhteenveto)
10. [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Johdanto

**Rinnakkaisohjelmointi** (parallel programming) tarkoittaa työn jakamista **usealle prosessoriytimelle** samanaikaisesti suoritettavaksi. Tämä nopeuttaa **CPU-intensiivisiä** operaatioita merkittävästi.

```
Peräkkäinen suoritus (1 ydin):
  Core 1: [Tehtävä 1][Tehtävä 2][Tehtävä 3][Tehtävä 4]
  Aika: ████████████████████████ (4 sekuntia)

Rinnakkainen suoritus (4 ydintä):
  Core 1: [Tehtävä 1]
  Core 2: [Tehtävä 2]
  Core 3: [Tehtävä 3]
  Core 4: [Tehtävä 4]
  Aika: ██████ (1 sekunti) ← 4× nopeampi!
```

---

## Milloin rinnakkaistaa?

### CPU-bound vs I/O-bound

| Tyyppi | Selitys | Ratkaisu | Esimerkki |
|--------|---------|----------|-----------|
| **CPU-bound** | Prosessori tekee raskasta työtä | `Parallel` / `Task.Run` | Kuvankäsittely, laskenta, pakkaus |
| **I/O-bound** | Odotetaan ulkoista resurssia | `async/await` | HTTP, tietokanta, tiedostot |

```csharp
// CPU-bound → Parallel
string[] kuvat = Directory.GetFiles("kuvat", "*.jpg");
Parallel.ForEach(kuvat, kuva => MuunnaKoko(kuva));

// I/O-bound → async/await + Task.WhenAll
string[] urls = new[] { "https://api1.com", "https://api2.com", "https://api3.com" };
IEnumerable<Task<string>> tasks = urls.Select(url => httpClient.GetStringAsync(url));
string[] results = await Task.WhenAll(tasks);
```

### Milloin EI kannata rinnakkaistaa?

```csharp
// ❌ Liian pieni työ — rinnakkaistamisen overhead on suurempi kuin hyöty
Parallel.For(0, 10, i =>
{
    int tulos = i * 2;  // Liian nopea operaatio!
});

// ✅ Riittävän raskas työ — rinnakkaistaminen kannattaa
Parallel.For(0, 10, i =>
{
    string hash = ComputeExpensiveHash(data[i]);  // Raskas laskenta
});
```

**Nyrkkisäännöt:**
- ✅ Rinnakkaista kun yksittäinen iteraatio kestää **yli 1ms**
- ✅ Rinnakkaista kun alkioita on **satoja tai tuhansia**
- ❌ Älä rinnakkaista **muutamaa nopeaa operaatiota**
- ❌ Älä rinnakkaista **I/O-operaatioita** (käytä async/await)

---

## Parallel.For ja Parallel.ForEach

### Parallel.For

```csharp
// Rinnakkainen for-silmukka
Parallel.For(0, 1000, i =>
{
    int tulos = RaskasLaskenta(i);
    Console.WriteLine($"Valmis: {i}, tulos: {tulos}");
});

Console.WriteLine("Kaikki valmiita!"); // Odottaa kaikkien valmistumista
```

### Parallel.ForEach

```csharp
string[] tiedostot = Directory.GetFiles("data", "*.csv");

// Käsittele tiedostot rinnakkain
Parallel.ForEach(tiedostot, tiedosto =>
{
    string data = File.ReadAllText(tiedosto);
    List<string[]> tulos = ParseCsv(data);
    Console.WriteLine($"Käsitelty: {Path.GetFileName(tiedosto)}, rivejä: {tulos.Count}");
});
```

### ParallelOptions — säädä rinnakkaisuutta

```csharp
ParallelOptions options = new ParallelOptions
{
    // Rajoita samanaikaisten säikeiden määrää
    MaxDegreeOfParallelism = 4,  // Max 4 ydintä

    // CancellationToken peruutusta varten
    CancellationToken = cancellationToken
};

try
{
    Parallel.ForEach(data, options, item =>
    {
        ProcessItem(item);
    });
}
catch (OperationCanceledException)
{
    Console.WriteLine("Rinnakkainen suoritus peruutettu.");
}
```

### MaxDegreeOfParallelism — ohjeet

```csharp
// CPU-intensiivinen työ: käytä kaikkia ytimiä
MaxDegreeOfParallelism = Environment.ProcessorCount  // Esim. 8

// Jätä tilaa muille prosesseille
MaxDegreeOfParallelism = Environment.ProcessorCount - 1  // 7

// I/O-sekoitettu työ: vähemmän
MaxDegreeOfParallelism = Environment.ProcessorCount / 2  // 4

// Testaa ja mittaa! Oletus (-1) antaa .NET:n päättää
MaxDegreeOfParallelism = -1  // Oletus, yleensä hyvä
```

### Parallel — palauta tuloksia

```csharp
// Parallel.ForEach ei palauta tuloksia suoraan
// Käytä ConcurrentBag:ia tai thread-local -muuttujia

ConcurrentBag<ProcessingResult> tulokset = new ConcurrentBag<ProcessingResult>();

Parallel.ForEach(data, item =>
{
    ProcessingResult tulos = Process(item);
    tulokset.Add(tulos);  // Säikeisturvallinen!
});

Console.WriteLine($"Käsitelty {tulokset.Count} alkiota");
```

### Parallel — paikallinen tila (thread-local)

```csharp
// Tehokkaampi: thread-local summa (vältetään turhaa lukitusta)
long kokonaissumma = 0;

Parallel.For(0, 1_000_000,
    // Alusta thread-local muuttuja
    () => 0L,

    // Suorita (kukin säie laskee omaan summaansa)
    (i, state, localSum) =>
    {
        return localSum + RaskasLaskenta(i);
    },

    // Yhdistä thread-local summat
    localSum =>
    {
        Interlocked.Add(ref kokonaissumma, localSum);
    }
);

Console.WriteLine($"Summa: {kokonaissumma}");
```

---

## Parallel.ForEachAsync

`.NET 6+` esitteli `Parallel.ForEachAsync` joka yhdistää rinnakkaisen suorituksen ja **async/await**:n.

### Peruskäyttö

```csharp
List<string> urls = Enumerable.Range(1, 100)
    .Select(i => $"https://api.example.com/items/{i}")
    .ToList();

await Parallel.ForEachAsync(urls, async (url, ct) =>
{
    string data = await httpClient.GetStringAsync(url, ct);
    Console.WriteLine($"Haettu: {url}, pituus: {data.Length}");
});
```

### ParallelOptions

```csharp
ParallelOptions options = new ParallelOptions
{
    MaxDegreeOfParallelism = 10,  // Max 10 samanaikaista
    CancellationToken = cancellationToken
};

await Parallel.ForEachAsync(urls, options, async (url, ct) =>
{
    HttpResponseMessage response = await httpClient.GetAsync(url, ct);
    response.EnsureSuccessStatusCode();
    string content = await response.Content.ReadAsStringAsync(ct);
    await ProcessContentAsync(content, ct);
});
```

### Käytännön esimerkki: Bulk API -kutsut

```csharp
public class BulkApiProcessor
{
    private readonly HttpClient _httpClient;
    private readonly ConcurrentBag<ApiResult> _results = new();
    private int _processed = 0;

    public async Task<List<ApiResult>> ProcessBulkAsync(
        List<int> ids,
        int maxConcurrency = 20,
        CancellationToken ct = default)
    {
        ParallelOptions options = new ParallelOptions
        {
            MaxDegreeOfParallelism = maxConcurrency,
            CancellationToken = ct
        };

        await Parallel.ForEachAsync(ids, options, async (id, ct) =>
        {
            try
            {
                ApiResponse? response = await _httpClient.GetFromJsonAsync<ApiResponse>(
                    $"api/items/{id}", ct);

                _results.Add(new ApiResult(id, true, response));
            }
            catch (Exception ex)
            {
                _results.Add(new ApiResult(id, false, null, ex.Message));
            }
            finally
            {
                int count = Interlocked.Increment(ref _processed);
                if (count % 100 == 0)
                    Console.WriteLine($"Käsitelty: {count}/{ids.Count}");
            }
        });

        return _results.ToList();
    }
}

public record ApiResult(int Id, bool Success, ApiResponse? Data, string? Error = null);
public record ApiResponse(string Name, decimal Value);
```

### Parallel.ForEachAsync vs muut tavat

```csharp
List<int> items = Enumerable.Range(1, 100).ToList();

// ❌ Peräkkäinen — hidas
foreach (int item in items)
{
    await ProcessAsync(item);
}
// → 100 × 100ms = 10 000ms

// ❌ Task.WhenAll kaikki kerralla — voi ylikuormittaa
IEnumerable<Task> tasks = items.Select(i => ProcessAsync(i));
await Task.WhenAll(tasks);
// → 100 samanaikaista! Voi olla liikaa

// ✅ Parallel.ForEachAsync — hallittu rinnakkaisuus
await Parallel.ForEachAsync(items,
    new ParallelOptions { MaxDegreeOfParallelism = 10 },
    async (item, ct) => await ProcessAsync(item));
// → Max 10 samanaikaisesti, hallittu kuormitus
```

---

## PLINQ (Parallel LINQ)

PLINQ (Parallel Language-Integrated Query) mahdollistaa LINQ-kyselyiden **automaattisen rinnakkaistamisen**.

### Peruskäyttö — AsParallel()

```csharp
IEnumerable<int> luvut = Enumerable.Range(1, 1_000_000);

// Normaali LINQ (peräkkäinen)
List<int> tulokset = luvut
    .Where(n => OnAlkuluku(n))
    .ToList();

// PLINQ (rinnakkainen) — lisää vain AsParallel()!
List<int> rinnakkaiset = luvut
    .AsParallel()
    .Where(n => OnAlkuluku(n))
    .ToList();
```

### AsOrdered — säilytä järjestys

```csharp
// Oletuksena PLINQ EI takaa järjestystä
List<int> tulokset = data
    .AsParallel()
    .Select(x => Process(x))
    .ToList();  // Järjestys voi olla mikä tahansa!

// AsOrdered säilyttää järjestyksen
List<int> jarjestetyt = data
    .AsParallel()
    .AsOrdered()            // Säilytä alkuperäinen järjestys
    .Select(x => Process(x))
    .ToList();              // Sama järjestys kuin syötteessä
```

**Huom:** `AsOrdered()` hidastaa hieman, koska tulokset pitää järjestää.

### WithDegreeOfParallelism — rajoita rinnakkaisuutta

```csharp
List<int> tulokset = data
    .AsParallel()
    .WithDegreeOfParallelism(4)  // Max 4 säiettä
    .Select(x => RaskasLaskenta(x))
    .ToList();
```

### PLINQ — aggregaatti-operaatiot

```csharp
IEnumerable<int> luvut = Enumerable.Range(1, 10_000_000);

// Rinnakkainen summa
long summa = luvut
    .AsParallel()
    .Sum(n => (long)n);

// Rinnakkainen keskiarvo
double keskiarvo = luvut
    .AsParallel()
    .Average();

// Rinnakkainen ryhmittely
Dictionary<string, int> ryhmat = data
    .AsParallel()
    .GroupBy(x => x.Category)
    .ToDictionary(g => g.Key, g => g.Count());
```

### PLINQ — ForAll (sivuvaikutukset)

```csharp
// ForAll on nopeampi kuin foreach rinnakkaisille tuloksille
data.AsParallel()
    .Where(x => x.IsActive)
    .ForAll(x =>
    {
        // ⚠️ Säikeisturvallinen operaatio!
        ProcessItem(x);
    });
```

### PLINQ — milloin käyttää?

```csharp
// ✅ HYVÄ: Raskas laskenta isolla datamäärällä
List<int> alkuluvut = Enumerable.Range(2, 1_000_000)
    .AsParallel()
    .Where(n => OnAlkuluku(n))  // CPU-intensiivinen
    .ToList();

// ❌ HUONO: Kevyt operaatio (overhead > hyöty)
List<int> tuplat = Enumerable.Range(1, 100)
    .AsParallel()
    .Select(n => n * 2)  // Liian nopea!
    .ToList();

// ❌ HUONO: I/O-operaatiot (käytä async)
List<string> tulokset = urls
    .AsParallel()
    .Select(url => httpClient.GetStringAsync(url).Result)  // Blokkaa säikeitä!
    .ToList();
```

### PLINQ — poikkeukset

```csharp
try
{
    List<double> tulokset = data
        .AsParallel()
        .Select(x =>
        {
            if (x < 0) throw new ArgumentException($"Negatiivinen: {x}");
            return Math.Sqrt(x);
        })
        .ToList();
}
catch (AggregateException ae)
{
    // PLINQ käärii poikkeukset AggregateExceptioniin
    foreach (Exception ex in ae.InnerExceptions)
    {
        Console.WriteLine($"Virhe: {ex.Message}");
    }
}
```

---

## Task.Run ja manuaalinen rinnakkaistaminen

### Useita Task.Run-kutsuja rinnakkain

```csharp
// Käynnistä useita CPU-tehtäviä rinnakkain
Task<string> task1 = Task.Run(() => LaskeHash("data1"));
Task<string> task2 = Task.Run(() => LaskeHash("data2"));
Task<string> task3 = Task.Run(() => LaskeHash("data3"));

string[] tulokset = await Task.WhenAll(task1, task2, task3);

Console.WriteLine($"Hash 1: {tulokset[0]}");
Console.WriteLine($"Hash 2: {tulokset[1]}");
Console.WriteLine($"Hash 3: {tulokset[2]}");
```

### Task.Run — pitkäkestoinen taustatehtävä

```csharp
// TaskCreationOptions.LongRunning — oma säie pitkälle tehtävälle
Task task = Task.Factory.StartNew(() =>
{
    while (!cancellationToken.IsCancellationRequested)
    {
        ProcessQueue();
        Thread.Sleep(100);
    }
}, cancellationToken, TaskCreationOptions.LongRunning, TaskScheduler.Default);
```

### Task.Run vs Parallel vs PLINQ

| Tapa | Käyttökohde | Vahvuus |
|------|-------------|---------|
| `Task.Run` + `WhenAll` | Muutama erillinen tehtävä | Yksinkertainen, joustava |
| `Parallel.ForEach` | Iso kokoelma, CPU-työ | Automaattinen partitiointi |
| `Parallel.ForEachAsync` | Iso kokoelma, async-työ | Hallittu async-rinnakkaisuus |
| `PLINQ` | LINQ-kyselyt, aggregaatit | Deklaratiivinen, helppo |

---

## Thread Safety rinnakkaisessa koodissa

### Ongelma: Jaettu muuttuva data

```csharp
// ❌ VAARALLISTA: Jaettu lista
List<int> tulokset = new List<int>();

Parallel.For(0, 1000, i =>
{
    tulokset.Add(i * 2);  // Race condition! List ei ole säikeisturvallinen
});
// → IndexOutOfRangeException tai korruptoitunut data
```

### Ratkaisu 1: ConcurrentBag

```csharp
// ✅ Säikeisturvallinen kokoelma
ConcurrentBag<int> tulokset = new ConcurrentBag<int>();

Parallel.For(0, 1000, i =>
{
    tulokset.Add(i * 2);  // Turvallinen!
});
```

### Ratkaisu 2: Thread-local + yhdistäminen

```csharp
// ✅ Tehokkaampi: Jokainen säie kerää omat tulokset
ConcurrentBag<List<int>> kaikkiTulokset = new ConcurrentBag<List<int>>();

Parallel.ForEach(
    Partitioner.Create(0, 1000),
    () => new List<int>(),  // Thread-local lista
    (range, state, localList) =>
    {
        for (int i = range.Item1; i < range.Item2; i++)
        {
            localList.Add(i * 2);  // Ei lukitusta!
        }
        return localList;
    },
    localList => kaikkiTulokset.Add(localList)  // Yhdistä lopussa
);

List<int> tulos = kaikkiTulokset.SelectMany(l => l).ToList();
```

### Ratkaisu 3: Interlocked yksittäisille arvoille

```csharp
// ✅ Atominen laskuri
long summa = 0;

Parallel.For(0, 1_000_000, i =>
{
    Interlocked.Add(ref summa, i);
});

Console.WriteLine($"Summa: {summa}");
```

### Yleinen virhe: UI-päivitys taustasäikeestä

```csharp
// ❌ WPF/WinForms: Ei voi päivittää UI:ta taustasäikeestä
Parallel.ForEach(data, item =>
{
    string tulos = Process(item);
    label.Text = tulos;  // Kaatuu! Väärä säie!
});

// ✅ Palauta tulokset ja päivitä UI pääsäikeessä
ConcurrentBag<string> tulokset = new ConcurrentBag<string>();
await Task.Run(() =>
{
    Parallel.ForEach(data, item =>
    {
        tulokset.Add(Process(item));
    });
});
// Nyt ollaan UI-säikeessä
label.Text = string.Join(", ", tulokset);
```

---

## Best Practices

### 1. Mittaa ennen rinnakkaistamista

```csharp
using System.Diagnostics;

Stopwatch sw = Stopwatch.StartNew();

// Peräkkäinen
foreach (object item in data)
    Process(item);
Console.WriteLine($"Peräkkäinen: {sw.ElapsedMilliseconds}ms");

sw.Restart();

// Rinnakkainen
Parallel.ForEach(data, item => Process(item));
Console.WriteLine($"Rinnakkainen: {sw.ElapsedMilliseconds}ms");

// Vertaa — rinnakkaisuus ei aina ole nopeampi!
```

### 2. Käytä Partitioner:ia suurille kokoelmille

```csharp
// Partitioner jakaa datan suurempiin paloihin
// → Vähemmän overheadia kuin yksi alkio kerrallaan
Parallel.ForEach(
    Partitioner.Create(0, data.Length, data.Length / Environment.ProcessorCount),
    range =>
    {
        for (int i = range.Item1; i < range.Item2; i++)
        {
            Process(data[i]);
        }
    });
```

### 3. Vältä liikaa rinnakkaisuutta

```csharp
// ❌ Liikaa: Sisäkkäinen rinnakkaistaminen
Parallel.ForEach(categories, category =>
{
    Parallel.ForEach(category.Products, product =>  // ❌ Liikaa säikeitä!
    {
        Process(product);
    });
});

// ✅ Parempi: Rinnakkaista vain ulompi silmukka
Parallel.ForEach(categories, category =>
{
    foreach (Product product in category.Products)  // Peräkkäinen sisällä
    {
        Process(product);
    }
});
```

### 4. Tue peruutusta

```csharp
CancellationTokenSource cts = new CancellationTokenSource();
ParallelOptions options = new ParallelOptions { CancellationToken = cts.Token };

try
{
    Parallel.ForEach(data, options, (item, state) =>
    {
        if (ShouldStop(item))
        {
            state.Stop();   // Pysäytä pian (ei uusia iteraatioita)
            // TAI
            state.Break();  // Pysäytä tietyn indeksin jälkeen
            return;
        }

        Process(item);
    });
}
catch (OperationCanceledException)
{
    Console.WriteLine("Peruutettu.");
}
```

### 5. Valitse oikea työkalu

```
I/O-operaatioita (HTTP, DB, tiedostot)?
│
├─ Yksittäisiä kutsuja? → async/await + Task.WhenAll
├─ Monta kutsua? → Parallel.ForEachAsync
└─ Jono/virta? → Channel<T>

CPU-laskentaa?
│
├─ Iso kokoelma? → Parallel.ForEach
├─ LINQ-kysely? → PLINQ (.AsParallel())
└─ Muutama tehtävä? → Task.Run + Task.WhenAll
```

---

## Yhteenveto

### Muistilista

1. **`Parallel.ForEach`** — CPU-intensiivinen rinnakkaissilmukka
2. **`Parallel.ForEachAsync`** — Asynkroninen rinnakkaissilmukka (.NET 6+)
3. **`PLINQ` (AsParallel)** — LINQ-kyselyiden rinnakkaistaminen
4. **`Task.Run` + `WhenAll`** — Muutaman tehtävän rinnakkaistaminen
5. **`MaxDegreeOfParallelism`** — Rajoita samanaikaisia säikeitä

### Tärkeimmät säännöt

- ✅ Rinnakkaista **CPU-intensiivistä työtä** (laskenta, kuvankäsittely)
- ✅ Käytä **async/await** I/O-operaatioihin
- ✅ **Mittaa aina** — rinnakkaisuus ei aina nopeuta
- ✅ Käytä **ConcurrentBag** tai **Interlocked** jaettuun dataan
- ✅ **Rajoita rinnakkaisuutta** (MaxDegreeOfParallelism)
- ❌ Älä rinnakkaista **triviaalia työtä** (overhead > hyöty)
- ❌ Älä käytä **sisäkkäisiä Parallel-silmukoita**
- ❌ Älä käytä **tavallista List:ia** rinnakkaisessa koodissa

---

## Hyödyllisiä linkkejä

- [Microsoft: Parallel programming in .NET](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/)
- [Microsoft: Parallel.ForEach](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreach)
- [Microsoft: Parallel.ForEachAsync](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreachasync)
- [Microsoft: Introduction to PLINQ](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/introduction-to-plinq)
- [Microsoft: Potential pitfalls in data and task parallelism](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/potential-pitfalls-in-data-and-task-parallelism)

### Aiheeseen liittyvää

- [Async/Await](Async-Await.md) — Asynkroninen ohjelmointi
- [Synkronointi](Synchronization.md) — lock, SemaphoreSlim, Interlocked
- [Concurrent Collections](Concurrent-Collections.md) — Säikeisturvalliset kokoelmat
