# Concurrency — Samanaikaisuus yleisesti

## Sisällysluettelo

1. [Mitä on concurrency?](#mitä-on-concurrency)
2. [Miksi concurrencya tarvitaan?](#miksi-concurrencya-tarvitaan)
3. [Concurrency vs Parallelism vs Asynchrony](#concurrency-vs-parallelism-vs-asynchrony)
4. [Concurrencyn haasteet](#concurrencyn-haasteet)
5. [Concurrency-mallit](#concurrency-mallit)
6. [Concurrency C#:ssa ja .NET:ssä](#concurrency-cssa-ja-netssä)
7. [Milloin käyttää mitäkin?](#milloin-käyttää-mitäkin)
8. [Yhteenveto](#yhteenveto)
9. [Jatko-opiskelu](#jatko-opiskelu)

---

## Mitä on concurrency?

**Concurrency** (samanaikaisuus) tarkoittaa ohjelman kykyä käsitellä useita tehtäviä päällekkäisten ajanjaksojen aikana. Se ei välttämättä tarkoita että tehtävät suoritetaan tasan samalla hetkellä — vaan että ohjelma pystyy **hallitsemaan** useita asioita samanaikaisesti.

### Arkielämäanalogia

Kuvittele ravintolan keittiö:

**Ilman concurrencya (peräkkäisesti):**
```
Kokki: [Ota tilaus 1] → [Valmista annos 1] → [Tarjoile 1]
       → [Ota tilaus 2] → [Valmista annos 2] → [Tarjoile 2]
       → [Ota tilaus 3] → [Valmista annos 3] → [Tarjoile 3]

Kokonaisaika: 30 minuuttia (jokainen tilaus odottaa edellistä)
```

**Concurrencyn kanssa:**
```
Kokki: [Tilaus 1 uuniin] → [Aloita tilaus 2] → [Tarkista tilaus 1]
       → [Tilaus 2 hellalle] → [Tilaus 3 aloitus] → [Tilaus 1 valmis!]
       → [Tarkista tilaus 2] → ...

Kokonaisaika: 12 minuuttia (tehtäviä limitetään päällekkäin)
```

Huomaa: **yksikin kokki** voi käsitellä useita tilauksia samanaikaisesti. Hän ei kloonaa itseään — hän vain järjestää työnsä fiksummin.

Tämä on concurrencyn ydinajatus: **työn organisointia**, ei välttämättä useamman työntekijän käyttämistä.

---

## Miksi concurrencya tarvitaan?

### 1. Suorituskyky

Modernit tietokoneet sisältävät useita prosessorin ytimiä. Jos ohjelma käyttää vain yhtä ydintä, suurin osa laskentatehosta jää hyödyntämättä:

```
4-ytiminen prosessori, yksisäikeinen ohjelma:

  Ydin 1: ████████████████  (100% kuormitettu)
  Ydin 2: ░░░░░░░░░░░░░░░░  (tyhjäkäynti)
  Ydin 3: ░░░░░░░░░░░░░░░░  (tyhjäkäynti)
  Ydin 4: ░░░░░░░░░░░░░░░░  (tyhjäkäynti)

  → 75% laskentatehosta menee hukkaan!

4-ytiminen prosessori, rinnakkainen ohjelma:

  Ydin 1: ████████████████  (100%)
  Ydin 2: ████████████████  (100%)
  Ydin 3: ████████████████  (100%)
  Ydin 4: ████████████████  (100%)

  → Jopa 4x nopeampi!
```

### 2. Reagointikyky (responsiveness)

Käyttöliittymäsovelluksissa (desktop, mobiili) yksi säie hoitaa käyttöliittymän piirtämisen. Jos tämä säie tekee raskasta työtä (tietokantahaku, tiedoston lataus), käyttöliittymä **jäätyy**:

```
Ilman concurrencya:
  UI-säie: [Piirrä nappi] → [Lataa 10MB tiedosto...............] → [Piirrä vastaus]
                              ↑ Käyttöliittymä jäätynyt 5 sekuntia!

Concurrencyn kanssa:
  UI-säie:    [Piirrä nappi] → [Animaatio] → [Animaatio] → [Piirrä vastaus]
  Taustasäie: [Lataa 10MB tiedosto...............................] → Valmis!
              ↑ Käyttöliittymä reagoi koko ajan!
```

### 3. Resurssien tehokas käyttö

Monet operaatiot (HTTP-kutsut, tietokantakyselyt, tiedostojen luku) ovat **I/O-operaatioita** — ohjelma odottaa ulkoista järjestelmää. Ilman concurrencya säie seisoo toimettomana odotuksen ajan:

```
Synkroninen (hukkaa aikaa):
  Säie: [Lähetä HTTP-kutsu] → [ODOTA 200ms.........] → [Käsittele vastaus]
                                ↑ Säie ei tee mitään!

Asynkroninen (tehokas):
  Säie: [Lähetä HTTP-kutsu] → [Tee muuta työtä] → [Käsittele vastaus]
                                ↑ Säie palvelee muita pyyntöjä!
```

### 4. Skaalautuvuus

Web-palvelin käsittelee satoja tai tuhansia pyyntöjä samanaikaisesti. Ilman concurrencya jokainen käyttäjä joutuisi odottamaan kaikkien edellisten pyyntöjen valmistumista:

```
Synkroninen web-palvelin (1 pyyntö kerrallaan):
  Käyttäjä 1: [Pyyntö] → [Vastaus]
  Käyttäjä 2:                      [Pyyntö] → [Vastaus]
  Käyttäjä 3:                                            [Pyyntö] → [Vastaus]
  → Jokainen odottaa vuoroaan

Asynkroninen web-palvelin (monta pyyntöä samanaikaisesti):
  Käyttäjä 1: [Pyyntö] → [Vastaus]
  Käyttäjä 2: [Pyyntö] → [Vastaus]
  Käyttäjä 3: [Pyyntö] → [Vastaus]
  → Kaikki palvellaan samanaikaisesti
```

---

## Concurrency vs Parallelism vs Asynchrony

Nämä kolme käsitettä sekoitetaan usein. Ne ovat eri asioita, vaikka liittyvät toisiinsa:

### Concurrency (samanaikaisuus)

**Määritelmä:** Ohjelman kyky käsitellä useita tehtäviä päällekkäisten ajanjaksojen aikana.

Concurrency on **rakenteellinen** ominaisuus — se on tapa organisoida ohjelma niin että se voi käsitellä useita tehtäviä. Tehtävät eivät välttämättä suoritu samalla hetkellä.

```
Concurrency yhdellä ytimellä (vuorottelu):

  Säie A: ██░░██░░██░░██
  Säie B: ░░██░░██░░██░░

  → Molemmat "etenevät" samanaikaisesti, mutta suorittuvat vuorotellen
  → Kuin kokki joka vaihtaa tehtävien välillä
```

### Parallelism (rinnakkaisuus)

**Määritelmä:** Useiden tehtävien suoritus kirjaimellisesti **samalla hetkellä** eri prosessorin ytimillä.

Parallelism on concurrencyn **erikoistapaus** — se vaatii fyysisesti useamman suoritusyksikön.

```
Parallelism kahdella ytimellä:

  Ydin 1: ████████████████
  Ydin 2: ████████████████

  → Molemmat suorittuvat AIDOSTI samaan aikaan
  → Kuin kaksi kokkia jotka työskentelevät samanaikaisesti
```

### Asynchrony (asynkronisuus)

**Määritelmä:** Tehtävän aloittaminen ilman että odotetaan sen valmistumista — jatketaan muuta työtä ja palataan tulokseen myöhemmin.

Asynkronisuus on **suoritustapa** — se kertoo miten tehtävä käynnistetään ja miten tulosta odotetaan.

```
Asynkroninen operaatio:

  Säie: [Käynnistä I/O] → [Tee muuta] → [I/O valmis, käsittele tulos]
                           ↑ Säie vapaa!

  → Säie ei seiso paikallaan odotuksen ajan
  → Kuin kokki joka laittaa uunin päälle ja tekee salaattia sillä välin
```

### Miten ne liittyvät toisiinsa?

```
                    ┌─────────────────────────────┐
                    │       CONCURRENCY           │
                    │  (samanaikaisuuden hallinta) │
                    │                             │
                    │  ┌───────────┐ ┌──────────┐ │
                    │  │PARALLELISM│ │ASYNCHRONY│ │
                    │  │(eri ytim.)│ │(I/O-odot)│ │
                    │  └───────────┘ └──────────┘ │
                    └─────────────────────────────┘

Concurrency = yläkäsite (useiden tehtävien hallinta)
Parallelism = yksi tapa toteuttaa (eri ytimillä samaan aikaan)
Asynchrony  = toinen tapa toteuttaa (vapauta säie odotuksen ajaksi)
```

| Käsite | Avainajatus | Vaatii useita ytimiä? | C#-työkalut |
|--------|------------|----------------------|-------------|
| **Concurrency** | Useiden tehtävien hallinta | Ei | Task, async/await, lock |
| **Parallelism** | Aidosti samaan aikaan | Kyllä | Parallel.ForEach, PLINQ, Task.Run |
| **Asynchrony** | Vapauta säie odotuksen ajaksi | Ei | async/await, Task.Delay |

### Konkreettinen esimerkki

**Tilanne:** 100 kuvaa pitää ladata internetistä ja käsitellä.

```
1. Synkroninen (ei concurrencya):
   Lataa kuva 1 → Käsittele 1 → Lataa kuva 2 → Käsittele 2 → ...
   Aika: 100 x (lataus + käsittely) = HIDAS

2. Asynkroninen (async/await):
   Käynnistä 100 latausta samanaikaisesti (await Task.WhenAll)
   → Säie vapautetaan jokaisen latauksen ajaksi
   → Käsittele jokainen kun valmis
   Aika: pisimmän latauksen + käsittelyn verran

3. Rinnakkainen (Parallel.ForEach):
   Käsittele kuvia 4 ytimellä samanaikaisesti
   → CPU-työ jaetaan ytimien kesken
   Aika: 100 käsittelyä / 4 ydintä = ~25 käsittelyä

4. Asynkroninen + rinnakkainen (paras):
   Lataa kaikki asynkronisesti (I/O) + käsittele rinnakkain (CPU)
   → I/O ei blokkaa, CPU-työ jaetaan ytimille
   Aika: nopein mahdollinen
```

---

## Concurrencyn haasteet

Concurrency ei ole ilmaista — se tuo mukanaan ongelmia joita yksisäikeisessä ohjelmassa ei ole.

### 1. Race condition (kilpailutilanne)

Kun kaksi säiettä lukee ja kirjoittaa samaa dataa samanaikaisesti, tulos on ennustamaton:

```
Tilanne: Kaksi säiettä kasvattaa laskuria (_count = 0)

  Odotettu tulos:  0 + 1 + 1 = 2
  Mahdollinen tulos: 1 (toinen lisäys hävisi!)

  Säie A: LUE (0) → LASKE (1) → KIRJOITA (1)
  Säie B:    LUE (0) → LASKE (1) → KIRJOITA (1)
                                              ↑ Molemmat kirjoittivat 1!
```

**Ratkaisu:** Synkronointimekanismit (`lock`, `Interlocked`, `SemaphoreSlim`)

> Lue lisää: [Synkronointi](Synchronization.md)

### 2. Deadlock (lukkiutuminen)

Kaksi säiettä odottaa toistensa resursseja — kumpikaan ei pääse eteenpäin:

```
  Säie A: Hankki lukko 1, yrittää hankkia lukko 2 → ODOTTAA...
  Säie B: Hankki lukko 2, yrittää hankkia lukko 1 → ODOTTAA...

  → Molemmat odottavat ikuisesti! Ohjelma jumittuu.

  Analogia: Kaksi autoa kapeassa kujassa vastakkain.
  Kumpikaan ei voi peruuttaa. Kumpikaan ei pääse eteenpäin.
```

**Ratkaisuja:**
- Hanki lukot aina samassa järjestyksessä
- Käytä timeout-arvoja lukkojen hankintaan
- Vältä sisäkkäisiä lukkoja
- Käytä korkeamman tason abstraktioita (Channel, ConcurrentDictionary)

> Lue lisää: [Synkronointi — Deadlock](Synchronization.md#deadlock)

### 3. Starvation (nälkiintyminen)

Säie ei koskaan pääse suoritukseen koska muut säikeet pitävät resursseja varattuna:

```
  Säie A (korkea prioriteetti): ████████████████████████████████
  Säie B (korkea prioriteetti): ████████████████████████████████
  Säie C (matala prioriteetti): ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                                 ↑ Säie C ei koskaan pääse suoritukseen!
```

**Ratkaisu:** .NET:n ThreadPool ja Task-järjestelmä hoitavat prioriteetit yleensä oikein automaattisesti.

### 4. Thread-safety (säikeisturvallisuus)

Koodi on **säikeisturvallinen** (thread-safe) kun se toimii oikein myös usean säikeen käyttäessä sitä samanaikaisesti. Suurin osa tavallisesta koodista EI ole säikeisturvallista:

```csharp
// EI säikeisturvallinen:
List<int> lista = new List<int>();
// Jos kaksi säiettä kutsuu Add:ia samaan aikaan → kaatuminen tai datan menetys

// Säikeisturvallinen vaihtoehto:
ConcurrentBag<int> lista = new ConcurrentBag<int>();
// Useat säikeet voivat lisätä turvallisesti
```

> Lue lisää: [Säikeet — Säikeisturvallisuus](Threads.md#säikeisturvallisuus)

### 5. Monimutkaisuus

Concurrency-koodi on vaikeampaa kirjoittaa, lukea, testata ja debugata:

```
Yksisäikeinen bugi:
  → Aja ohjelma uudelleen → Sama bugi joka kerta → Helppo toistaa

Monisäikeinen bugi (race condition):
  → Aja 10 kertaa → Toimii 9 kertaa → Epäonnistuu 1 kerta
  → "Toimii minun koneellani!" → Tuotannossa kaatuu joka päivä
```

**Tästä syystä:** Käytä concurrencya vain kun tarvitset sitä. Yksinkertainen koodi on paras koodi.

---

## Concurrency-mallit

### 1. Shared State (jaettu tila)

Säikeet jakavat saman muistin ja kommunikoivat muuttamalla yhteisiä muuttujia. Vaatii synkronointia.

```
  Säie A ──┐
           ├──→ [Jaettu muisti] ← Tarvitsee suojausta (lock, Interlocked)
  Säie B ──┘

  C#-työkalut: lock, Interlocked, SemaphoreSlim, ConcurrentDictionary
```

**Edut:** Nopea kommunikaatio (muisti on nopea)
**Haitat:** Altis race conditioneille ja deadlockeille

### 2. Message Passing (viestinvälitys)

Säikeet kommunikoivat lähettämällä viestejä toisilleen. Ei jaettua tilaa — ei race conditioneja.

```
  Tuottaja ──→ [Kanava/Jono] ──→ Kuluttaja

  C#-työkalut: Channel<T>, BlockingCollection<T>
```

**Edut:** Ei race conditioneja, selkeä rakenne
**Haitat:** Hieman hitaampi kuin suora muistinkäyttö

### 3. Producer-Consumer (tuottaja-kuluttaja)

Yksi tai useampi tuottaja luo dataa, yksi tai useampi kuluttaja käsittelee sitä. Välissä on jono.

```
  [Tuottaja 1] ──┐
                  ├──→ [Jono (Channel)] ──→ [Kuluttaja]
  [Tuottaja 2] ──┘

  Ravintola-analogia:
  [Tarjoilija 1] ──┐
                    ├──→ [Tilauslappupidike] ──→ [Kokki]
  [Tarjoilija 2] ──┘
```

> Lue lisää: [Concurrent Collections — Channel](Concurrent-Collections.md#channel)

### 4. Fork-Join (haarautuminen ja yhdistäminen)

Työ jaetaan osiin, osat suoritetaan rinnakkain, ja tulokset yhdistetään.

```
                 ┌──→ [Osa 1] ──┐
  [Työ] ──Fork──→├──→ [Osa 2] ──├──Join──→ [Tulos]
                 └──→ [Osa 3] ──┘

  C#-työkalut: Task.WhenAll, Parallel.ForEach, PLINQ
```

> Lue lisää: [Parallel-ohjelmointi](Parallel-Programming.md)

---

## Concurrency C#:ssa ja .NET:ssä

.NET tarjoaa useita tasoja concurrencyn toteuttamiseen. Moderni C# suosii korkeamman tason abstraktioita:

### Abstraktiotasot (ylhäältä alas)

```
Taso 4 (korkein): PLINQ, Parallel.ForEachAsync
  → "Käsittele tämä lista rinnakkain"
  → Helpoin käyttää, vähiten kontrollia

Taso 3: async/await, Task.WhenAll, Channel<T>
  → "Käynnistä tämä asynkronisesti, odota myöhemmin"
  → Modernin C#:n perusta

Taso 2: Task.Run, ConcurrentDictionary, SemaphoreSlim
  → "Suorita taustasäikeessä, suojaa jaettu data"
  → Enemmän kontrollia

Taso 1: Thread, lock, Monitor, Interlocked
  → "Luo säie, lukitse resurssi"
  → Matalan tason kontrolli

Taso 0 (matalin): Thread, Mutex, ManualResetEvent
  → Käyttöjärjestelmätason synkronointi
  → Harvoin tarvitaan suoraan
```

**Nyrkkisääntö:** Aloita ylimmältä tasolta. Siirry alemmas vain jos tarvitset enemmän kontrollia.

### C#:n concurrency-työkalut ja milloin käyttää

| Työkalu | Käyttötarkoitus | Esimerkki |
|---------|----------------|-----------|
| `async/await` | I/O-odotukset (HTTP, DB, tiedostot) | `await httpClient.GetAsync(url)` |
| `Task.WhenAll` | Useiden async-operaatioiden odotus | Lataa 10 kuvaa samaan aikaan |
| `Task.Run` | CPU-työn siirto taustasäikeeseen | Raskas laskenta UI-sovelluksessa |
| `Parallel.ForEach` | CPU-intensiivinen lista | Käsittele 1000 kuvaa |
| `Parallel.ForEachAsync` | Asynkroninen rinnakkainen lista | 1000 API-kutsua, max 10 kerrallaan |
| `PLINQ` | Rinnakkaiset LINQ-kyselyt | `.AsParallel().Where(...)` |
| `lock` | Suojaa koodilohko (yksi säie kerrallaan) | Laskurin päivitys |
| `Interlocked` | Atominen yksittäisen arvon muutos | `Interlocked.Increment(ref count)` |
| `SemaphoreSlim` | Rajoita samanaikaisuutta (N kerrallaan) | Max 5 DB-yhteyttä |
| `Channel<T>` | Asynkroninen jono säikeiden välillä | Producer-consumer pipeline |
| `ConcurrentDictionary` | Säikeisturvallinen hakurakenne | Jaettu cache |
| `CancellationToken` | Peruutusmekanismi | Timeout, käyttäjän peruutus |

---

## Milloin käyttää mitäkin?

### Päätöspuu

```
Onko tehtävä I/O-pohjainen (HTTP, DB, tiedosto)?
├── KYLLÄ → Käytä async/await
│   ├── Yksi operaatio → await GetAsync()
│   ├── Monta operaatiota → await Task.WhenAll(...)
│   └── Monta + rajoitettu → Parallel.ForEachAsync (MaxDegreeOfParallelism)
│
└── EI → Onko tehtävä CPU-intensiivinen?
    ├── KYLLÄ → Käytä Parallel / Task.Run
    │   ├── Lista → Parallel.ForEach / PLINQ
    │   └── Yksittäinen raskas työ → Task.Run (UI-sovelluksissa)
    │
    └── EI → Tarvitseeko jakaa dataa säikeiden välillä?
        ├── KYLLÄ
        │   ├── Yksittäinen laskuri → Interlocked
        │   ├── Useita muuttujia yhdessä → lock
        │   ├── Dictionary → ConcurrentDictionary
        │   └── Jono/pipeline → Channel<T>
        │
        └── EI → Ei tarvitse concurrencya!
```

### I/O-bound vs CPU-bound

Tämä on tärkein erottelu concurrency-työkalun valinnassa:

| | I/O-bound | CPU-bound |
|---|---|---|
| **Mitä tapahtuu** | Odotetaan ulkoista järjestelmää | Prosessori laskee |
| **Esimerkit** | HTTP-kutsu, DB-kysely, tiedoston luku | Kuvankäsittely, salaus, laskenta |
| **Säie odotuksen ajan** | Ei tee mitään (voidaan vapauttaa) | Laskee aktiivisesti (tarvitsee ytimen) |
| **Oikea työkalu** | `async/await` | `Parallel`, `Task.Run` |
| **Miksi** | Vapauta säie muiden palveltavaksi | Hyödynnä useita prosessoriytimiä |

```
I/O-bound (async/await):
  Säie: [Lähetä] → VAPAA → [Käsittele vastaus]
                   ↑ Säie palvelee muita pyyntöjä

CPU-bound (Parallel):
  Ydin 1: [Laske osa 1]
  Ydin 2: [Laske osa 2]   ← Kaikki ytimet laskevat
  Ydin 3: [Laske osa 3]
  Ydin 4: [Laske osa 4]
```

---

## Yhteenveto

### Muistisäännöt

1. **Concurrency = tehtävien hallinta**, ei välttämättä samanaikaista suoritusta
2. **async/await I/O:lle**, **Parallel CPU:lle** — älä sekoita
3. **Jaettu data tarvitsee suojausta** — lock, Interlocked, tai säikeisturvalliset kokoelmat
4. **Käytä korkeimman tason abstraktiota** joka riittää
5. **Älä käytä concurrencya turhaan** — yksinkertainen koodi on paras koodi

### Kokonaiskartta

```
┌─────────────────────────────────────────────────────────────┐
│                    CONCURRENCY C#:SSA                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   ASYNC      │  │  SYNKRONOINTI │  │  PARALLEL    │      │
│  │              │  │              │  │              │      │
│  │ async/await  │  │ lock         │  │ Parallel.For │      │
│  │ Task.WhenAll │  │ Interlocked  │  │ PLINQ        │      │
│  │ Task.Delay   │  │ SemaphoreSlim│  │ Task.Run     │      │
│  │ Channel<T>   │  │ ConcDictionary│  │              │      │
│  │              │  │              │  │              │      │
│  │ I/O-bound    │  │ Jaettu data  │  │ CPU-bound    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  Peruutus: CancellationToken                                │
│  Perusta: Thread, ThreadPool                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Jatko-opiskelu

Suosittelemme opiskelua tässä järjestyksessä:

1. **[Säikeet (Threads)](Threads.md)** — Ymmärrä mikä säie on ja miten ohjelma suoritetaan
2. **[Async/Await](Async-Await.md)** — Modernin C#:n perusta, I/O-operaatiot
3. **[Synkronointi](Synchronization.md)** — Jaetun datan suojaaminen (lock, SemaphoreSlim)
4. **[Concurrent Collections](Concurrent-Collections.md)** — Säikeisturvalliset tietorakenteet
5. **[Parallel-ohjelmointi](Parallel-Programming.md)** — CPU-intensiivinen rinnakkaisuus

### Käytännön harjoitus

Kokeile opittuja asioita käytännössä: [Ravintolan tilausjärjestelmä -harjoitus](../../../Assigments/ConcurrencyExercises/README.md)

### Ulkoiset lähteet

- [Microsoft: Asynchronous programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [Microsoft: Parallel programming in .NET](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/)
- [Microsoft: Thread-safe collections](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)
- [Stephen Cleary: Async Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
- [Joe Albahari: Threading in C#](https://www.albahari.com/threading/)
