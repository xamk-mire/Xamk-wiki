# Concurrency Cheat Sheet — Muistisäännöt ja pikavalinnat

Tämä on käytännön pikaopas: kun kohtaat tilanteen, katso tästä mikä työkalu on oikea.

---

## Päätöspuu: "Mitä minun pitäisi käyttää?"

```
1. Odotatko jotain ulkoista? (HTTP, tietokanta, tiedosto, API)
   │
   ├── KYLLÄ → async/await
   │   │
   │   ├── Yksi operaatio?
   │   │   └── await GetAsync(url)
   │   │
   │   ├── Monta operaatiota samaan aikaan?
   │   │   └── await Task.WhenAll(task1, task2, task3)
   │   │
   │   ├── Monta operaatiota, mutta rajoita määrää?
   │   │   └── Parallel.ForEachAsync + MaxDegreeOfParallelism
   │   │
   │   └── Haluat voida peruuttaa?
   │       └── Välitä CancellationToken joka metodille
   │
   └── EI → Tekeekö prosessori raskasta laskentaa?
       │
       ├── KYLLÄ
       │   ├── Iso lista käsiteltävänä?
       │   │   └── Parallel.ForEach tai PLINQ (.AsParallel())
       │   │
       │   └── Yksi raskas työ (UI ei saa jäätyä)?
       │       └── await Task.Run(() => RaskasLaskenta())
       │
       └── EI → Jaetaanko dataa säikeiden välillä?
           │
           ├── KYLLÄ → Katso "Datan suojaaminen" alla
           │
           └── EI → Ei tarvitse concurrencya!
```

---

## Datan suojaaminen: "Miten suojaan jaetun datan?"

```
Montako muuttujaa muutetaan kerralla?
│
├── YKSI luku (int, long)?
│   └── Interlocked.Increment / Interlocked.Add
│       Nopein vaihtoehto. Ei lukkoja.
│
├── USEITA muuttujia yhdessä (esim. summa + lukumäärä)?
│   │
│   ├── Synkroninen koodi?
│   │   └── lock (_lukko) { muuttuja1++; muuttuja2 += arvo; }
│   │
│   └── Asynkroninen koodi (tarvitaan await)?
│       └── SemaphoreSlim(1, 1) + WaitAsync/Release
│           (lock:n sisällä EI voi käyttää await:ia!)
│
├── Dictionary / hakurakenne?
│   └── ConcurrentDictionary<TKey, TValue>
│       GetOrAdd, AddOrUpdate, TryAdd — atomisia operaatioita
│
├── Jono säikeiden välillä (producer-consumer)?
│   │
│   ├── Asynkroninen koodi?
│   │   └── Channel<T> (moderni, suositeltu)
│   │
│   └── Synkroninen koodi?
│       └── BlockingCollection<T> (vanhempi)
│
└── Haluat rajoittaa montako säiettä pääsee samanaikaisesti?
    └── SemaphoreSlim(N, N)
        Esim. SemaphoreSlim(5, 5) = max 5 kerrallaan
```

---

## 10 kultaista sääntöä

### 1. I/O:lle async, CPU:lle Parallel

```
I/O (HTTP, DB, tiedosto)  →  async/await
CPU (laskenta, kuvat)     →  Parallel.ForEach / Task.Run
```

Älä sekoita näitä. `Task.Run` I/O-operaatiolle on turhaa. `Thread.Sleep` async-koodissa on virhe.

### 2. Älä koskaan käytä Thread.Sleep async-koodissa

```csharp
// VÄÄRIN — lukitsee säikeen
async Task TeeJotainAsync()
{
    Thread.Sleep(1000);     // Säie jumissa!
}

// OIKEIN — vapauttaa säikeen
async Task TeeJotainAsync()
{
    await Task.Delay(1000); // Säie vapaa!
}
```

### 3. Async kuplii ylöspäin

Kun yksi metodi on async, kaikki sen kutsujat pitää tehdä async:ksi. Älä katkaise ketjua `.Result`:lla tai `.Wait()`:lla.

```csharp
// VÄÄRIN — deadlock-riski
string data = GetDataAsync().Result;

// OIKEIN
string data = await GetDataAsync();
```

### 4. Task.WhenAll kun haluat nopeutta

Jos sinulla on monta riippumatonta operaatiota, käynnistä ne kaikki ja odota yhdessä:

```csharp
// HITAASTI (peräkkäin):
string a = await HaeA();    // 2s
string b = await HaeB();    // 2s
// Yhteensä: 4s

// NOPEASTI (samanaikaisesti):
Task<string> taskA = HaeA();
Task<string> taskB = HaeB();
string[] tulokset = await Task.WhenAll(taskA, taskB);
// Yhteensä: 2s (pisimmän mukaan)
```

### 5. CancellationToken AINA mukaan

Välitä CancellationToken jokaiseen async-metodiin. Muuten operaatiota ei voi peruuttaa.

```csharp
// Metodi ottaa tokenin vastaan
public async Task<string> HaeAsync(CancellationToken ct = default)
{
    return await _http.GetStringAsync(url, ct);  // Välitä eteenpäin!
}
```

### 6. Interlocked yhdelle, lock monelle

```csharp
// Yksi arvo → Interlocked (nopea)
Interlocked.Increment(ref _laskuri);

// Monta arvoa yhdessä → lock (turvallinen)
lock (_lukko)
{
    _kokonaisAika += kesto;
    _lukumäärä++;
}
```

### 7. SemaphoreSlim.Release() AINA finally-lohkossa

```csharp
await _semaphore.WaitAsync(ct);
try
{
    await TeeJotainAsync(ct);
}
finally
{
    _semaphore.Release();  // Vapautetaan AINA, myös virheen sattuessa
}
```

Jos unohdat `finally`:n ja operaatio heittää poikkeuksen, paikka jää ikuisesti varatuksi.

### 8. Älä käytä async void

```csharp
// VÄÄRIN — poikkeuksia ei voi käsitellä
async void TeeJotain() { ... }

// OIKEIN
async Task TeeJotainAsync() { ... }

// AINOA poikkeus: event handlerit
button.Click += async (s, e) => { await TeeJotainAsync(); };
```

### 9. Älä käytä tavallista List/Dictionary rinnakkaisessa koodissa

```csharp
// VÄÄRIN — kaatuu tai korruptoi datan
List<int> lista = new List<int>();
Parallel.For(0, 1000, i => lista.Add(i));

// OIKEIN — säikeisturvallinen
ConcurrentBag<int> bag = new ConcurrentBag<int>();
Parallel.For(0, 1000, i => bag.Add(i));
```

### 10. Mittaa ennen rinnakkaistamista

Rinnakkaisuus ei ole aina nopeampi — siinä on overheadia. Mittaa ensin:

```csharp
Stopwatch sw = Stopwatch.StartNew();
// ... koodi ...
Console.WriteLine($"Kesto: {sw.ElapsedMilliseconds}ms");
```

Rinnakkaista vain kun yksittäinen iteraatio kestää yli 1ms tai alkioita on satoja/tuhansia.

---

## Pikavalintataulu

| Tilanne | Työkalu | Esimerkki |
|---------|---------|-----------|
| HTTP-kutsu | `await httpClient.GetAsync()` | API-haku |
| Tietokantakysely | `await db.ToListAsync(ct)` | EF Core |
| Monta I/O-operaatiota | `await Task.WhenAll(...)` | 10 API-kutsua samaan aikaan |
| Monta I/O + rajoitus | `Parallel.ForEachAsync` + `MaxDegreeOfParallelism` | 1000 kutsua, max 20 kerrallaan |
| Raskas CPU-laskenta | `await Task.Run(() => ...)` | Hash-laskenta UI-sovelluksessa |
| Iso lista + CPU-työ | `Parallel.ForEach` | 10 000 kuvan käsittely |
| LINQ + CPU-työ | `.AsParallel().Where(...)` | Miljoonan rivin suodatus |
| Laskuri (int) | `Interlocked.Increment` | Tilausten lukumäärä |
| Monta muuttujaa yhdessä | `lock` | Keskiarvon laskenta (summa + määrä) |
| Lukitus async-koodissa | `SemaphoreSlim(1,1)` | Asynkroninen kriittinen osio |
| Max N samanaikaisesti | `SemaphoreSlim(N,N)` | Max 3 kokkia keittiössä |
| Jaettu avain-arvo -data | `ConcurrentDictionary` | Cache, tilausten seuranta |
| Tuottaja-kuluttaja -jono | `Channel<T>` | Tilausjono, taustaprosessointi |
| Viive async-koodissa | `await Task.Delay(ms)` | Simuloitu odotus |
| Peruutusmekanismi | `CancellationToken` | Timeout, käyttäjän peruutus |
| Lazy-alustus | `Lazy<T>` | Singleton, kerran haettava data |

---

## Yleiset virheet ja korjaukset

| Virhe | Miksi väärin | Korjaus |
|-------|-------------|---------|
| `Thread.Sleep(1000)` async-metodissa | Lukitsee säikeen | `await Task.Delay(1000)` |
| `GetAsync().Result` | Deadlock-riski | `await GetAsync()` |
| `async void Metodi()` | Poikkeuksia ei voi käsitellä | `async Task MetodiAsync()` |
| `_laskuri++` rinnakkaisessa koodissa | Race condition | `Interlocked.Increment(ref _laskuri)` |
| `lock` + `await` sisällä | Käännösvirhe / deadlock | `SemaphoreSlim(1,1).WaitAsync()` |
| `List.Add()` rinnakkaisesti | Kaatuminen / datan menetys | `ConcurrentBag` tai `lock` |
| `Dictionary[key] = x` rinnakkaisesti | Kaatuminen | `ConcurrentDictionary` |
| `SemaphoreSlim.Release()` ilman `finally` | Paikka jää varattuksi virhetilanteessa | Laita `try/finally`-lohkoon |
| `Task.Run(() => httpClient.GetAsync(...))` | Turha säie I/O-operaatiolle | Suoraan `await httpClient.GetAsync(...)` |
| Sisäkkäiset `Parallel.ForEach` | Liikaa säikeitä, hidas | Rinnakkaista vain ulompi silmukka |

---

## Ravintola-analogia pikaopas

| C#-käsite | Ravintola |
|-----------|-----------|
| **Säie** | Kokki |
| **async/await** | Kokki laittaa ajastimen ja tekee muuta sillä aikaa |
| **Thread.Sleep** | Kokki seisoo paikallaan ja tuijottaa kelloa |
| **Task.WhenAll** | "Tilaus valmis kun KAIKKI annokset on tehty" |
| **Task.Run** | "Hei, tarvitaan kokki tekemään tämä!" |
| **CancellationToken** | Asiakas peruu tilauksen |
| **lock** | Vain yksi kokki saa päivittää liitutaulua kerrallaan |
| **Interlocked** | Nopea laskurin klikkaus (atominen) |
| **SemaphoreSlim(3,3)** | Keittiöön mahtuu max 3 kokkia |
| **Channel** | Tilauslappu-pidike tiskin päällä |
| **ConcurrentDictionary** | Seinätaulu jossa tilausten status |
| **Parallel.ForEach** | Jaa 100 annoksen pilkkominen 4 kokille |
| **Race condition** | Kaksi kokkia maustaa samaa kattilaa → liikaa suolaa |
| **Deadlock** | Kaksi kokkia kapeassa käytävässä vastakkain — kumpikaan ei pääse ohi |

---

## Muistisäännöt lauseina

1. **"Odottaako koodi jotain?"** → async/await
2. **"Laskeeko koodi jotain raskasta?"** → Parallel / Task.Run
3. **"Muuttavatko useat säikeet samaa dataa?"** → Suojaa se (lock, Interlocked, Concurrent*)
4. **"Montako muuttujaa muuttuu kerralla?"** → Yksi = Interlocked, monta = lock
5. **"Tarvitaanko await lukon sisällä?"** → SemaphoreSlim, ei lock
6. **"Pitääkö rajoittaa samanaikaisuutta?"** → SemaphoreSlim(N, N)
7. **"Pitääkö siirtää dataa säikeeltä toiselle?"** → Channel\<T\>
8. **"Voiko tämän peruuttaa?"** → CancellationToken
9. **"Toimiiko tämä oikein jos 1000 säiettä tekee saman yhtä aikaa?"** → Jos et ole varma, suojaa
10. **"Onko tämä nopeampi rinnakkaisena?"** → Mittaa, älä arvaa

---

## Lisämateriaali

- [Concurrency yleisesti](Concurrency-General.md) — Kokonaiskuva ja käsitteet
- [Säikeet](Threads.md) — Mikä on säie ja miten ohjelma suoritetaan
- [Async/Await](Async-Await.md) — Asynkronisen ohjelmoinnin perusteet
- [Synkronointi](Synchronization.md) — lock, SemaphoreSlim, Interlocked
- [Concurrent Collections](Concurrent-Collections.md) — ConcurrentDictionary, Channel
- [Parallel-ohjelmointi](Parallel-Programming.md) — Parallel.ForEach, PLINQ
