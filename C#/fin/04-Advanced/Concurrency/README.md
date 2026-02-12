# Rinnakkaisuus ja Asynkronisuus C#:ssa

Tervetuloa C#:n rinnakkaisuus- ja asynkronisuusmateriaaleihin! Tämä osio käsittelee moniajoa, asynkronista ohjelmointia, synkronointimekanismeja, säikeisturvallisia kokoelmia ja rinnakkaisohjelmointia.

## Sisältö

### Yleiskatsaus
- [Concurrency yleisesti](Concurrency-General.md) - Mitä on samanaikaisuus, miksi sitä tarvitaan, concurrency vs parallelism vs asynchrony, haasteet ja mallit — **Lue ensin!**
- [Cheat Sheet — Muistisäännöt](Cheat-Sheet.md) - Päätöspuu, pikavalintataulu, 10 kultaista sääntöä, yleiset virheet — **Pidä käden ulottuvilla!**

### Perusteet
- [Säikeet (Threads)](Threads.md) - Mikä on säie, prosessi vs säie, ThreadPool, säikeisturvallisuus

### Asynkroninen ohjelmointi
- [Async/Await](Async-Await.md) - Asynkronisen ohjelmoinnin perusteet, Task, CancellationToken, virheenkäsittely

### Synkronointimekanismit
- [Synkronointi](Synchronization.md) - lock, Monitor, SemaphoreSlim, Mutex, Interlocked, deadlock

### Säikeisturvalliset kokoelmat
- [Concurrent Collections](Concurrent-Collections.md) - ConcurrentDictionary, ConcurrentQueue, Channel, BlockingCollection

### Rinnakkaisohjelmointi
- [Parallel-ohjelmointi](Parallel-Programming.md) - Parallel.ForEach, PLINQ, Task.Run, rinnakkaistaminen

---

## Keskeiset käsitteet

### Concurrency vs Parallelism vs Asynchrony

Nämä kolme käsitettä sekoitetaan usein toisiinsa:

| Käsite | Selitys | Esimerkki |
|--------|---------|-----------|
| **Concurrency** (samanaikaisuus) | Useiden tehtävien hallinta samaan aikaan — eivät välttämättä suoritu yhtä aikaa | Yksi kokki valmistaa kolmea ruokaa vuorotellen |
| **Parallelism** (rinnakkaisuus) | Useiden tehtävien suoritus kirjaimellisesti samaan aikaan eri prosessoreilla | Kolme kokkia valmistaa kukin omaa ruokaansa |
| **Asynchrony** (asynkronisuus) | Tehtävän aloitus ilman odottamista — jatka muuta työtä kunnes tulos on valmis | Kokki laittaa uunin päälle ja tekee sillä välin salaattia |

```
Concurrency (samanaikaisuus):
  Thread 1: ████░░░░████░░░░████
  Thread 2: ░░░░████░░░░████░░░░
  → Vuorottelu yhdellä ytimellä

Parallelism (rinnakkaisuus):
  Core 1: ████████████████████
  Core 2: ████████████████████
  → Aidosti samaan aikaan eri ytimillä

Asynchrony (asynkronisuus):
  Thread:  ████──────████──────████
                ↑ I/O odotus    ↑ I/O odotus
  → Säie vapautetaan odotuksen ajaksi
```

### Milloin käyttää mitäkin?

| Tilanne | Ratkaisu | Esimerkki |
|---------|----------|-----------|
| **I/O-operaatiot** (tietokanta, HTTP, tiedostot) | `async/await` | API-kutsut, DB-kyselyt |
| **CPU-intensiivinen laskenta** | `Parallel` / `Task.Run` | Kuvankäsittely, datan prosessointi |
| **Jaettu data usean säikeen välillä** | `lock` / `ConcurrentDictionary` | Yhteinen laskuri, jaettu cache |
| **Rajoitettu resurssien käyttö** | `SemaphoreSlim` | Max 5 samanaikaista API-kutsua |
| **Producer-Consumer** | `Channel<T>` / `BlockingCollection` | Viestijonot, taustaprosessointi |

---

## Oppimisjärjestys

Suosittelemme opiskelua seuraavassa järjestyksessä:

1. **[Concurrency yleisesti](Concurrency-General.md)** - Aloita tästä! Ymmärrä kokonaiskuva: mitä concurrency on, miksi sitä tarvitaan, ja miten eri lähestymistavat eroavat
2. **[Säikeet (Threads)](Threads.md)** - Ymmärrä mitä säie on ja miten ohjelma suoritetaan
   - Mikä on säie ja prosessi
   - ThreadPool
   - Miten async/await liittyy säikeisiin
3. **[Async/Await](Async-Await.md)** - Asynkroninen ohjelmointi on modernin C#:n perusta
   - async/await syntaksi
   - Task ja Task<T>
   - CancellationToken
   - Virheenkäsittely ja anti-patternit
4. **[Synkronointi](Synchronization.md)** - Opi suojaamaan jaettu data
   - lock-lause
   - SemaphoreSlim
   - Deadlockin välttäminen
5. **[Concurrent Collections](Concurrent-Collections.md)** - Säikeisturvalliset tietorakenteet
   - ConcurrentDictionary
   - Channel
   - Producer-Consumer pattern
6. **[Parallel-ohjelmointi](Parallel-Programming.md)** - Hyödynnä monta ydintä
   - Parallel.ForEach
   - PLINQ
   - Milloin rinnakkaistaa

---

## Esitieto

Ennen tätä osiota on hyvä hallita:
- [C# perusteet](../../00-Basics/) - Muuttujat, funktiot, tietorakenteet
- [Delegates ja Lambda](../../00-Basics/Delegates.md) - Delegaatit ja lambda-lausekkeet
- [LINQ](../../00-Basics/LINQ.md) - LINQ-kyselyt (PLINQ:a varten)
- [Thread.Sleep](../../00-Basics/Thread-Sleep.md) - Säikeiden peruskäsitteet

---

## Hyödyllisiä linkkejä

- [Microsoft: Asynchronous programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [Microsoft: Parallel programming in .NET](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/)
- [Microsoft: Thread-safe collections](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)
- [Stephen Cleary: Async Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
