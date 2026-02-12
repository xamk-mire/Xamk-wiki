# Säikeet (Threads) — Moniajo C#:ssa

## Sisällysluettelo

1. [Mikä on säie?](#mikä-on-säie)
2. [Prosessi vs säie](#prosessi-vs-säie)
3. [Miten ohjelma suoritetaan?](#miten-ohjelma-suoritetaan)
4. [Yksi säie vs monta säiettä](#yksi-säie-vs-monta-säiettä)
5. [ThreadPool](#threadpool)
6. [Säikeet ja async/await](#säikeet-ja-asyncawait)
7. [Säikeisturvallisuus](#säikeisturvallisuus)
8. [Yhteenveto](#yhteenveto)
9. [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Mikä on säie?

**Säie** (thread) on ohjelman pienin suoritusyksikkö. Se on "polku" jota pitkin ohjelmasi koodi etenee — rivi kerrallaan, ylhäältä alas.

Kun käynnistät C#-ohjelman, käyttöjärjestelmä luo sille **yhden säikeen** (main thread). Tämä säie suorittaa `Program.cs`:n koodin rivi riviltä.

```
Yksinkertainen ohjelma — yksi säie:

Main Thread: [Console.WriteLine("Hei")] → [int x = 5 + 3] → [Console.WriteLine(x)]
             ──────────────────────────────────────────────────────────────────────▶ aika
```

### Arkielämän analogia

Ajattele säiettä **kokkina keittiössä**:

- **Yksi kokki (yksi säie)** = Yksi ihminen tekee kaiken yksin: pilkkoo sipulit, paistaa lihan, keittää riisin. Peräkkäin, yksi asia kerrallaan.
- **Kolme kokkia (kolme säiettä)** = Kolme ihmistä työskentelee samassa keittiössä: yksi pilkkoo, toinen paistaa, kolmas keittää. Samanaikaisesti, mutta pitää koordinoida ettei tule törmäyksiä.

```
Yksi kokki (yksi säie):
  Kokki: [Sipulit 5min] → [Liha 10min] → [Riisi 8min]
  Yhteensä: 23 minuuttia

Kolme kokkia (kolme säiettä):
  Kokki 1: [Sipulit 5min]
  Kokki 2: [Liha 10min]
  Kokki 3: [Riisi 8min]
  Yhteensä: 10 minuuttia (pisimmän ajan mukaan)
```

---

## Prosessi vs säie

### Prosessi

**Prosessi** on käynnissä oleva ohjelma. Kun avaat Visual Studion, selaimen tai oman C#-ohjelmasi, käyttöjärjestelmä luo kullekin **prosessin**.

Jokaisella prosessilla on:
- Oma muistialue (muut prosessit eivät näe sitä)
- Vähintään yksi säie
- Oma prosessorin aika

### Säie

**Säie** on prosessin sisällä oleva suorituspolku. Yhdessä prosessissa voi olla monta säiettä.

Saman prosessin säikeet **jakavat saman muistin** — ne näkevät samat muuttujat. Tämä on sekä hyödyllistä (datan jakaminen on helppoa) että vaarallista (race condition).

```
┌─────────────────────────────────────────┐
│ PROSESSI (esim. sinun C#-ohjelmasi)     │
│                                         │
│  ┌───────────┐  Jaettu muisti:          │
│  │ Säie 1    │  - muuttujat             │
│  │ (Main)    │  - oliot                 │
│  └───────────┘  - staattiset kentät     │
│  ┌───────────┐                          │
│  │ Säie 2    │  Kaikki säikeet näkevät  │
│  │ (Tausta)  │  SAMAT muuttujat!        │
│  └───────────┘                          │
│  ┌───────────┐  → Siksi tarvitaan       │
│  │ Säie 3    │    lock, Interlocked,    │
│  │ (Tausta)  │    ConcurrentDictionary  │
│  └───────────┘                          │
└─────────────────────────────────────────┘
```

| Ominaisuus | Prosessi | Säie |
|------------|----------|------|
| **Muisti** | Oma, erillinen | Jaettu prosessin sisällä |
| **Luominen** | Hidas (käyttöjärjestelmä luo) | Nopea |
| **Kommunikointi** | Vaikeaa (prosessien välinen) | Helppoa (sama muisti) |
| **Kaatuminen** | Yksi prosessi ei kaada toista | Yksi säie voi kaataa koko prosessin |
| **Esimerkki** | Chrome, Visual Studio, sinun ohjelma | Main thread, taustasäie, ThreadPool-säie |

---

## Miten ohjelma suoritetaan?

### Yksisäikeinen suoritus

Normaali C#-ohjelma suoritetaan **yhdellä säikeellä** (main thread):

```csharp
// Kaikki tämä tapahtuu YHDELLÄ säikeellä, peräkkäin:
Console.WriteLine("1. Hei");        // Main thread suorittaa
int result = LaskeJotain();          // Main thread suorittaa
Console.WriteLine($"2. Tulos: {result}"); // Main thread suorittaa
```

```
Main Thread: [WriteLine] → [LaskeJotain] → [WriteLine]
             ────────────────────────────────────────▶ aika

Kaikki tapahtuu peräkkäin, yksi asia kerrallaan.
```

### Monisäikeinen suoritus

Kun käytät `Task.Run`, `Parallel.ForEach` tai vastaavaa, .NET luo **lisää säikeitä**:

```csharp
// Käynnistä laskenta toisella säikeellä
Task<int> task = Task.Run(() => RaskasLaskenta());

// Main thread jatkaa SAMAAN AIKAAN
Console.WriteLine("Laskenta käynnissä...");

// Odota tulosta
int tulos = await task;
```

```
Main Thread:  [Task.Run] → [WriteLine "käynnissä"] → ... → [await: saa tuloksen]
                  │
                  └──▶ Taustasäie: [RaskasLaskenta ████████████]
                       (ThreadPool-säie tekee raskaan työn)
```

### Entä async/await?

`async/await` **ei luo uutta säiettä!** Se vapauttaa nykyisen säikeen odotuksen ajaksi:

```csharp
// async/await EI luo uutta säiettä:
string data = await httpClient.GetStringAsync(url);
```

```
Main Thread:  [GetStringAsync] → (säie VAPAUTETAAN) → ... → [jatka kun data saapuu]
                    │                                              │
                    └── HTTP-pyyntö lähtee                         │
                        Käyttöjärjestelmä hoitaa                   │
                        EI tarvita säiettä odotukseen!  ───────────┘
```

**Tärkeä ero:**

| Toiminto | Luoko uuden säikeen? | Selitys |
|----------|---------------------|---------|
| `await httpClient.GetAsync()` | **Ei** | I/O-operaatio — käyttöjärjestelmä hoitaa, säie vapaa |
| `await Task.Delay(1000)` | **Ei** | Ajastin — käyttöjärjestelmä hoitaa, säie vapaa |
| `Task.Run(() => Laske())` | **Kyllä** | CPU-työ siirretään ThreadPool-säikeelle |
| `Parallel.ForEach(...)` | **Kyllä** | Useita ThreadPool-säikeitä rinnakkain |
| `new Thread(() => ...).Start()` | **Kyllä** | Luodaan kokonaan uusi säie (harvoin tarpeen) |

---

## Yksi säie vs monta säiettä

### Milloin yksi säie riittää?

Yksinkertaisissa ohjelmissa yksi säie (main thread) riittää mainiosti:

```csharp
// Yksinkertainen ohjelma — yksi säie riittää
Console.Write("Nimesi: ");
string nimi = Console.ReadLine()!;
Console.WriteLine($"Hei {nimi}!");
```

### Milloin tarvitaan monta säiettä?

**1. Pitkä operaatio jäädyttäisi ohjelman:**

```csharp
// ❌ Yksi säie: ohjelma "jäätyy" 5 sekunniksi
Thread.Sleep(5000);  // Main thread lukittu!
Console.WriteLine("Tämä tulostuu vasta 5s jälkeen");

// ✅ Asynkroninen: ohjelma ei jäädy
await Task.Delay(5000);  // Main thread vapaa muuhun!
Console.WriteLine("5s kulunut");
```

**2. Raskas laskenta hyötyy useasta ytimestä:**

```csharp
// ❌ Yksi säie: käyttää yhtä ydintä
foreach (string kuva in kuvat)
    MuunnaKoko(kuva);  // Peräkkäin, hidas

// ✅ Monta säiettä: käyttää kaikkia ytimiä
Parallel.ForEach(kuvat, kuva =>
    MuunnaKoko(kuva));  // Rinnakkain, nopea!
```

**3. Web-sovellus palvelee monta käyttäjää:**

```
ASP.NET Core palvelin:

  Käyttäjä A → [Säie 1: Käsittele pyyntö A]
  Käyttäjä B → [Säie 2: Käsittele pyyntö B]  ← Samanaikaisesti!
  Käyttäjä C → [Säie 3: Käsittele pyyntö C]

  Ilman säikeitä: A odottaa → B odottaa → C odottaa (hidas!)
  Säikeillä: A, B, C käsitellään samanaikaisesti (nopea!)
```

---

## ThreadPool

### Mikä on ThreadPool?

.NET ylläpitää **säievarastoa** (ThreadPool) — joukkoa valmiita säikeitä jotka odottavat työtä. Tämä on tärkeä käsite ymmärtää, koska `Task.Run`, `Parallel.ForEach` ja monet muut käyttävät sitä.

```
ThreadPool (säievarasto):

  ┌─────────────────────────────────────────┐
  │  [Säie 1: vapaa]  [Säie 2: TYÖSSÄ]     │
  │  [Säie 3: vapaa]  [Säie 4: TYÖSSÄ]     │
  │  [Säie 5: vapaa]  [Säie 6: vapaa]      │
  │  [Säie 7: vapaa]  [Säie 8: TYÖSSÄ]     │
  └─────────────────────────────────────────┘
       ↑                     ↑
       │                     │
  Task.Run(() => ...)   Parallel.ForEach(...)
  "Anna mulle vapaa      "Anna mulle MONTA
   säie tehdäkseni         säiettä rinnakkain!"
   tätä työtä!"
```

### Miksi ThreadPool eikä uusia säikeitä?

```csharp
// ❌ HUONO: Uuden säikeen luominen on hidasta ja raskasta
for (int i = 0; i < 100; i++)
{
    new Thread(() => Työ(i)).Start();  // 100 uutta säiettä! Hidasta!
}

// ✅ HYVÄ: ThreadPool kierrättää säikeitä
for (int i = 0; i < 100; i++)
{
    Task.Run(() => Työ(i));  // Käyttää ThreadPool:n valmiita säikeitä
}
```

| Ominaisuus | `new Thread()` | `Task.Run` (ThreadPool) |
|------------|---------------|------------------------|
| **Säikeen luominen** | Uusi joka kerta (hidas) | Kierrättää valmiita (nopea) |
| **Resurssien käyttö** | Raskas (~1MB muistia/säie) | Kevyt (jaettu varasto) |
| **Hallinta** | Manuaalinen | Automaattinen |
| **Käyttö** | Harvoin tarpeen | ✅ Suositeltu |

### Miten async/await käyttää ThreadPoolia?

```csharp
public async Task<string> HaeDataAsync()
{
    // 1. Main thread kutsuu tätä
    Console.WriteLine($"Säie: {Thread.CurrentThread.ManagedThreadId}"); // Esim: "Säie: 1"

    // 2. await vapauttaa säikeen (säie 1 palaa ThreadPooliin)
    string data = await httpClient.GetStringAsync(url);

    // 3. Joku ThreadPool-säie jatkaa tästä (voi olla eri säie!)
    Console.WriteLine($"Säie: {Thread.CurrentThread.ManagedThreadId}"); // Esim: "Säie: 7"

    return data;
}
```

```
Ennen await:
  Säie 1 (Main): [HaeDataAsync alkaa] → [GetStringAsync alkaa] → säie vapautetaan
                                                                     ↓
Odotuksen aikana:                                               Säie 1 vapaa!
  Käyttöjärjestelmä hoitaa HTTP-pyynnön                         Tekee muita töitä
                                                                     ↓
Awaitin jälkeen:
  Säie 7 (Pool): [data saapui] → [jatka HaeDataAsync] → [return data]
```

**Tärkeää:**
- `await`:n jälkeen koodi voi jatkua **eri säikeessä** kuin ennen `await`:ia
- Tämä on normaalia ja turvallista
- Siksi jaettu data pitää suojata (lock, Interlocked, ConcurrentDictionary)

---

## Säikeet ja async/await

### async/await ei ole sama asia kuin monisäikeisyys

Tämä on yleinen väärinkäsitys. Selvennetään:

```csharp
// Tämä EI luo uutta säiettä:
await Task.Delay(1000);

// Tämä LUO uuden säikeen (ThreadPool):
await Task.Run(() => RaskasLaskenta());
```

**Mikä ero?**

- `Task.Delay`, `httpClient.GetAsync`, `stream.ReadAsync` — **I/O-operaatioita**. Käyttöjärjestelmä hoitaa odotuksen, säiettä ei tarvita.
- `Task.Run` — **siirtää CPU-työn** ThreadPool-säikeelle. Luo uuden säikeen.

### Visualisointi: async/await vs Thread

```
async/await (I/O):
  Säie 1: [Aloita HTTP-pyyntö] → VAPAA → [Saa vastauksen, jatka]
                                   ↑
                          Ei säiettä odotukseen!
                          Käyttöjärjestelmä hoitaa.

Task.Run (CPU-työ):
  Säie 1: [Task.Run] → VAPAA → [await: saa tuloksen]
               │
               └──▶ Säie 2 (ThreadPool): [████ Raskas laskenta ████]
                    Erillinen säie tekee työn.
```

### Miksi tämä on tärkeää?

Web-sovelluksessa (ASP.NET Core) palvelin palvelee **tuhansia pyyntöjä** samanaikaisesti. Jos jokainen pyyntö varaisi säikeen odotuksen ajaksi, säikeet loppuisivat nopeasti:

```
❌ Synkroninen (Thread.Sleep / .Result):
  1000 pyyntöä = 1000 lukittua säiettä = muisti loppuu!

✅ Asynkroninen (async/await):
  1000 pyyntöä = muutama säie vuorottelee = skaalautuu!
```

---

## Säikeisturvallisuus

### Miksi jaettu data on vaarallista?

Koska saman prosessin säikeet **jakavat muistin**, kaksi säiettä voi yrittää muuttaa samaa muuttujaa samaan aikaan:

```csharp
int laskuri = 0;

// Kaksi säiettä kasvattavat samaa laskuria:
Task.Run(() => { for (int i = 0; i < 1000; i++) laskuri++; });
Task.Run(() => { for (int i = 0; i < 1000; i++) laskuri++; });

// Tulos: laskuri < 2000! (pitäisi olla 2000)
```

```
Miksi tulos on väärä?

  Säie A: Lue laskuri (5) → Laske 5+1=6 → Kirjoita 6
  Säie B:    Lue laskuri (5) → Laske 5+1=6 → Kirjoita 6

  Molemmat lukivat arvon 5 → molemmat kirjoittivat 6
  Yksi lisäys HÄVISI! Pitäisi olla 7.
```

### Ratkaisut

| Ongelma | Ratkaisu | Milloin käyttää |
|---------|----------|-----------------|
| Yksittäisen arvon päivitys | `Interlocked` | Laskurit (int, long) |
| Usean arvon päivitys yhdessä | `lock` | Monimutkaisempi logiikka |
| Asynkroninen lukitus | `SemaphoreSlim` | async-koodissa, kapasiteettirajoitus |
| Säikeisturvallinen kokoelma | `ConcurrentDictionary` | Jaettu data usean säikeen välillä |

> 📚 Tarkemmin: [Synkronointi](Synchronization.md) ja [Concurrent Collections](Concurrent-Collections.md)

---

## Yhteenveto

### Perusperiaatteet

| Käsite | Selitys |
|--------|---------|
| **Säie (Thread)** | Ohjelman suorituspolku — rivi riviltä etenevä koodi |
| **Main Thread** | Ohjelman pääsäie — luodaan automaattisesti käynnistyksessä |
| **ThreadPool** | .NET:n ylläpitämä varasto valmiita säikeitä — Task.Run käyttää tätä |
| **Prosessi** | Käynnissä oleva ohjelma — sisältää yhden tai useamman säikeen |
| **Jaettu muisti** | Saman prosessin säikeet näkevät samat muuttujat |
| **Race condition** | Kaksi säiettä muuttaa samaa dataa samaan aikaan → virheitä |

### Muistilista

1. **Yksi säie** suorittaa koodia peräkkäin, rivi kerrallaan
2. **Monta säiettä** voi suorittaa koodia samanaikaisesti
3. **async/await** ei luo uusia säikeitä — se vapauttaa säikeen I/O-odotuksen ajaksi
4. **Task.Run** siirtää CPU-työn ThreadPool-säikeelle
5. **ThreadPool** kierrättää säikeitä — käytä Task.Run, älä `new Thread()`
6. **Jaettu data** pitää suojata (lock, Interlocked, ConcurrentDictionary)
7. **await:n jälkeen** koodi voi jatkua eri säikeessä — tämä on normaalia

### Ravintola-analogia kertauksena

| Ohjelmointikäsite | Ravintola-vastine |
|-------------------|-------------------|
| Säie (Thread) | Kokki |
| Main Thread | Pääkokki joka aloittaa työvuoron |
| ThreadPool | Kokkien taukotila (valmiita kokkeja odottamassa) |
| Task.Run | "Hei, tarvitaan kokki tekemään tämä!" |
| async/await | Kokki laittaa uunin päälle ja tekee muuta odotellessa |
| lock | "Yksi kokki kerrallaan saa käyttää veistä" |
| SemaphoreSlim | "Max 3 kokkia keittiössä samaan aikaan" |
| Race condition | Kaksi kokkia yrittää maustaa samaa kattilaa → liikaa suolaa |

---

## Hyödyllisiä linkkejä

- [Microsoft: Threads and threading](https://learn.microsoft.com/en-us/dotnet/standard/threading/threads-and-threading)
- [Microsoft: The managed thread pool](https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool)
- [Microsoft: Managed threading best practices](https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-best-practices)
- [Thread.Sleep](../../00-Basics/Thread-Sleep.md) — Perusesittely säikeen pausettamisesta

### Seuraavaksi

- [Async/Await](Async-Await.md) — Opi asynkroninen ohjelmointi (tärkein taito!)
- [Synkronointi](Synchronization.md) — Opi suojaamaan jaettu data
