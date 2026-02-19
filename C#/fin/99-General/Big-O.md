# Big O -notaatio

## Mikä on Big O — yksinkertaisesti?

Kuvittele, että sinulle annetaan nimilista ja sinun pitää etsiä sieltä tietty henkilö. Jos listalla on 10 nimeä, se on helppoa. Mutta entä jos listalla on **miljoona** nimeä?

Big O -notaatio vastaa kysymykseen: **"Kuinka paljon hitaammaksi ohjelma muuttuu, kun dataa tulee lisää?"**

Se ei mittaa sekunteja tai millisekunteja — se mittaa **kasvuvauhtia**. Kaksi algoritmia voivat olla yhtä nopeita 10 alkiolla, mutta miljoonalla alkiolla toinen voi olla **miljoonia kertoja** hitaampi.

**Muita materiaaleja:**
- [Big O Cheat Sheet – Time Complexity Chart](https://www.freecodecamp.org/news/big-o-cheat-sheet-time-complexity-chart/)
- [Big-O Algorithm Complexity Cheat Sheet](https://www.bigocheatsheet.com/)
- [Algoritmi](Algorithm.md)
- [Lajittelualgoritmit](Sorting-Algorithms.md)

---

## Peruskäsitteet ennen Big O:ta

Ennen kuin sukellamme Big O:hon, käydään läpi muutama käsite, jotka toistuvat jatkuvasti.

### Mikä on `n`?

`n` tarkoittaa **syötteen kokoa** — eli kuinka paljon dataa algoritmillesi annetaan.

| Tilanne | Mikä on `n`? |
|---------|-------------|
| Listan lajittelu | Listan alkioiden määrä |
| Nimen etsiminen taulukosta | Taulukon rivien määrä |
| Sanan etsiminen tekstistä | Tekstin merkkien määrä |
| Käyttäjien haku tietokannasta | Käyttäjien määrä tietokannassa |

Kun sanotaan "O(n)", tarkoitetaan: *"Operaatioiden määrä kasvaa samassa suhteessa kuin datan määrä."*

---

### Mikä on logaritmi (log)?

Logaritmi on käsite, joka tulee vastaan Big O:ssa usein, mutta moni kokee sen vaikeaksi. Se on kuitenkin yksinkertainen idea.

**Logaritmi on potenssilaskun vastakohta.** Se vastaa kysymykseen: *"Kuinka monta kertaa pitää jakaa kahdella, ennen kuin jäljellä on 1?"*

| Alku | ÷2 | ÷2 | ÷2 | ÷2 | ÷2 | Jakojen määrä |
|------|-----|-----|-----|-----|-----|---------------|
| 8 | 4 | 2 | 1 | | | **3** |
| 16 | 8 | 4 | 2 | 1 | | **4** |
| 32 | 16 | 8 | 4 | 2 | 1 | **5** |
| 1024 | 512 | 256 | 128 | ... | 1 | **10** |

Eli:
- **log₂(8) = 3** — koska 2 × 2 × 2 = 8 (kolme kertomista)
- **log₂(16) = 4** — koska 2 × 2 × 2 × 2 = 16
- **log₂(1024) = 10** — koska 2¹⁰ = 1024
- **log₂(1 000 000) ≈ 20** — miljoona alkiota, mutta vain 20 askelta!

**Arkielämän esimerkki:** Kuvittele, että etsit sanaa sanakirjasta. Et ala ensimmäiseltä sivulta — avaat kirjan keskeltä. Jos sana on "ennen" keskikohtaa, jätät oikean puoliskon kokonaan pois. Toista sama jäljellä olevalle puoliskolle. Joka kerta puolitat etsittävän alueen. Tuhatsivuisesta kirjasta löydät sanan noin **10 avauksella** — se on logaritmista kasvua.

**Miksi tämä on tärkeää?** Koska logaritminen kasvu on **todella hidasta**:

| Datan koko (n) | log₂(n) — askeleet |
|---------------|-------------------|
| 10 | 3 |
| 100 | 7 |
| 1 000 | 10 |
| 100 000 | 17 |
| 1 000 000 | 20 |
| 1 000 000 000 | 30 |

Miljardista alkiosta löydät etsimäsi **30 askeleella**. Siksi logaritminen aika on niin hyvä.

---

### Mikä on n² (neliö)?

`n²` tarkoittaa "n kertaa n". Jos dataa on 10 alkiota, tehdään 10 × 10 = 100 operaatiota.

Se syntyy tyypillisesti, kun joudut **vertailemaan jokaista alkiota jokaiseen toiseen alkioon** — eli kaksi sisäkkäistä silmukkaa.

| n | n² |
|---|-----|
| 10 | 100 |
| 100 | 10 000 |
| 1 000 | 1 000 000 |
| 10 000 | 100 000 000 |

Kasvu on **rajua**: 10-kertaistamalla datan, työmäärä 100-kertaistuu.

---

### Mikä on 2ⁿ (eksponentti)?

`2ⁿ` tarkoittaa, että työmäärä **kaksinkertaistuu** joka kerta kun lisäät yhden alkion.

| n | 2ⁿ |
|---|-----|
| 5 | 32 |
| 10 | 1 024 |
| 20 | 1 048 576 (yli miljoona) |
| 30 | 1 073 741 824 (yli miljardi) |
| 40 | ~1 000 miljardia |

Käytännössä jo `n = 30` on liikaa useimmille tietokoneille. Eksponentiaalista algoritmia ei voi käyttää muuten kuin hyvin pienille syötteille.

---

### Mikä on n! (faktoriaalinen)?

`n!` (luetaan "n kertoma") tarkoittaa: **n × (n-1) × (n-2) × ... × 2 × 1**

- 3! = 3 × 2 × 1 = 6
- 5! = 5 × 4 × 3 × 2 × 1 = 120
- 10! = 3 628 800
- 15! = 1 307 674 368 000

Faktoriaalinen kasvu on niin nopeaa, että jo **15 alkiota** tuottaa yli biljoona operaatiota. Tämä liittyy ongelmiin, joissa etsitään kaikki mahdolliset järjestykset (permutaatiot).

---

## Big O:n perusidea

Nyt kun ymmärrät taustakäsitteet, mennään itse Big O:hon.

**"O" tulee sanasta "Order"** (suuruusluokka). `O(n)` tarkoittaa: *"Tämä algoritmi tekee suuruusluokaltaan n operaatiota."*

Big O kuvaa **pahimman tapauksen** (worst case) — eli mitä tapahtuu kun data on "pahimmassa mahdollisessa" järjestyksessä tai kokoonpanossa.

### Kolme tärkeää sääntöä

**1. Vakiot jätetään pois**

Big O:ta kiinnostaa vain kasvuvauhti, ei tarkat luvut.

```
O(2n)   → O(n)     — kertoimella ei väliä
O(n/2)  → O(n)     — sama kasvu
O(500)  → O(1)     — 500 on vakio, se ei kasva
O(3n²)  → O(n²)    — kerroin pois
```

Miksi? Koska kun n on miljoona, sillä ei ole merkitystä onko operaatioita 2n vai 3n — molemmat ovat lineaarisia. Mutta sillä on valtava ero, onko kasvu n vai n².

**2. Vain suurin termi merkitsee**

```
O(n² + n)       → O(n²)       — n on mitätön n²:een verrattuna
O(n³ + n² + n)  → O(n³)       — n³ dominoi
O(n + log n)    → O(n)        — n dominoi
```

Kun n on miljoona: n² = 1 000 000 000 000, mutta n = 1 000 000. Pienempi termi on merkityksetön.

**3. Pahin tapaus**

Big O analysoi aina pahimman mahdollisen tilanteen:

```csharp
// Etsitään lukua listasta
int LinearSearch(int[] array, int target)
{
    for (int i = 0; i < array.Length; i++)
    {
        if (array[i] == target)
            return i;
    }
    return -1;
}

// Paras tapaus: luku on ensimmäisenä → O(1)
// Keskimääräinen tapaus: luku on keskellä → O(n/2) → O(n)
// Pahin tapaus: lukua ei ole listassa → O(n) — kaikki käydään läpi
// Big O = O(n) (pahin tapaus)
```

---

## Aikavaativuusluokat

### O(1) — Vakioaika

**Selkokielellä:** Kestää aina saman verran, vaikka dataa olisi miljoona tai miljardi.

Se on kuin tietäisit tarkan hyllynumeron kirjastossa — kävelet suoraan oikeaan paikkaan riippumatta kirjaston koosta.

```csharp
// Hae taulukon alkio indeksillä — aina yhtä nopea
int GetFirst(int[] array)
{
    return array[0];
}

// Dictionary-haku — avaimen perusteella suoraan oikeaan paikkaan
string GetUserName(Dictionary<int, string> users, int id)
{
    return users[id];
}

// Listan pituuden tarkistus — C# tietää sen valmiiksi
int GetCount(List<int> list)
{
    return list.Count;
}
```

**Milloin saat O(1):n?**
- Taulukon indeksillä haku: `array[5]`
- Dictionary/HashSet-operaatiot: `dict[key]`, `set.Contains(x)`
- Pinon (Stack) push/pop
- Muuttujan luku

---

### O(log n) — Logaritminen aika

**Selkokielellä:** Joka askeleella jäljellä oleva työ **puolittuu**. Vaikka data kymmenkertaistuisi, askeleet kasvavat vain vähän.

Tämä on binäärihaun aika. Binäärihaku toimii **vain järjestetyssä datassa** — se avaa aina keskikohdan ja päättelee, kummalla puolella etsittävä arvo on.

```csharp
// Binäärihaku askeleittain selitettynä:
// Etsitään lukua 7 järjestetystä taulukosta [1, 3, 5, 7, 9, 11, 13]
//
// Askel 1: Tarkista keskimmäinen (indeksi 3) → arvo 7 → LÖYTYI!
//
// Jos etsittäisiin lukua 11:
// Askel 1: Keskikohta = 7, 11 > 7 → etsi oikealta puolelta [9, 11, 13]
// Askel 2: Keskikohta = 11 → LÖYTYI!

int BinarySearch(int[] sortedArray, int target)
{
    int left = 0;
    int right = sortedArray.Length - 1;

    while (left <= right)
    {
        int mid = left + (right - left) / 2;

        if (sortedArray[mid] == target)
            return mid;                   // Löytyi!
        else if (sortedArray[mid] < target)
            left = mid + 1;              // Etsittävä on oikealla
        else
            right = mid - 1;             // Etsittävä on vasemmalla
    }

    return -1; // Ei löytynyt
}
```

**Konkreettinen vertailu — lineaarinen vs. logaritminen haku:**

| Alkioita | Lineaarinen haku O(n) | Binäärihaku O(log n) |
|----------|----------------------|---------------------|
| 10 | max 10 askelta | max 4 askelta |
| 1 000 | max 1 000 askelta | max 10 askelta |
| 1 000 000 | max 1 000 000 askelta | max 20 askelta |
| 1 000 000 000 | max 1 000 000 000 askelta | max 30 askelta |

Miljardista alkiosta löydät etsimäsi **30 askeleella**. Lineaarinen haku tarvitsisi pahimmillaan miljardin askelta.

---

### O(n) — Lineaarinen aika

**Selkokielellä:** Jos data tuplaantuu, työmäärä tuplaantuu. Yksi silmukka, joka käy kaikki läpi.

```csharp
// Suurimman luvun etsiminen — jokainen alkio käydään kerran läpi
int FindMax(int[] array)
{
    int max = array[0];

    for (int i = 1; i < array.Length; i++)
    {
        if (array[i] > max)
            max = array[i];
    }

    return max;
}

// Kaikkien lukujen summa
int Sum(int[] array)
{
    int total = 0;

    foreach (var item in array)
    {
        total += item;
    }

    return total;
}
```

**Milloin saat O(n):n?**
- Yksi `for`- tai `foreach`-silmukka koko datan yli
- `list.Contains(x)` — käy listan läpi kunnes löytää
- `Where()`, `Select()` LINQ-operaatiot

**Tärkeä huomio — peräkkäiset silmukat:**

```csharp
// Tämä on O(n), EI O(n²)
// Kaksi erillistä silmukkaa = O(n) + O(n) = O(2n) = O(n)
foreach (var item in list)  { /* ... */ }  // O(n)
foreach (var item in list)  { /* ... */ }  // O(n)
```

Peräkkäiset silmukat **lasketaan yhteen** (O(n) + O(n) = O(n)). Vain **sisäkkäiset** silmukat kertovat.

---

### O(n log n) — Lineaarilogaritminen aika

**Selkokielellä:** Tämä on **tehokkaan lajittelun** nopeus. Se on hieman hitaampi kuin O(n), mutta paljon nopeampi kuin O(n²).

Mistä "n log n" tulee? Kuvittele lajittelualgoritmia, joka:
1. **Jakaa** datan puoliksi (log n kertaa, koska puolitus log n kertaa johtaa yksittäisiin alkioihin)
2. Jokaisessa jaossa **käy läpi** kaikki n alkiota yhdistämiseksi

Siis: n alkiota × log n tasoa = **n log n** operaatiota.

```csharp
// C#:n sisäänrakennettu lajittelu — O(n log n)
int[] numbers = { 5, 2, 8, 1, 9, 3 };
Array.Sort(numbers);
// Tulos: { 1, 2, 3, 5, 8, 9 }

// LINQ OrderBy — myös O(n log n)
var sorted = students.OrderBy(s => s.LastName).ToList();
```

| Alkioita | O(n) | O(n log n) | O(n²) |
|----------|------|-----------|-------|
| 100 | 100 | 664 | 10 000 |
| 1 000 | 1 000 | 9 966 | 1 000 000 |
| 1 000 000 | 1 000 000 | 19 931 568 | 1 000 000 000 000 |

Huomaa: O(n log n) on paljon lähempänä O(n):ää kuin O(n²):ta.

---

### O(n²) — Neliöllinen aika

**Selkokielellä:** Kaksi **sisäkkäistä** silmukkaa, joissa molemmat käyvät koko datan läpi. Jokaista alkiota verrataan jokaiseen toiseen alkioon.

```csharp
// Bubble Sort — yksinkertainen mutta hidas lajittelu
void BubbleSort(int[] array)
{
    // Ulompi silmukka: n kertaa
    for (int i = 0; i < array.Length - 1; i++)
    {
        // Sisempi silmukka: n kertaa (joka ulomman kierroksella!)
        for (int j = 0; j < array.Length - i - 1; j++)
        {
            if (array[j] > array[j + 1])
            {
                (array[j], array[j + 1]) = (array[j + 1], array[j]);
            }
        }
    }
}
// 10 alkiota: ~100 vertailua — ok
// 10 000 alkiota: ~100 000 000 vertailua — hidasta!
```

**Kuinka tunnistaa O(n²)?** Katso sisäkkäisiä silmukoita:

```csharp
// Tämä on O(n²) — sisäkkäiset silmukat
for (int i = 0; i < n; i++)        // n kertaa
{
    for (int j = 0; j < n; j++)    // × n kertaa = n²
    {
        // operaatio
    }
}
```

**Esimerkki — duplikaattien etsiminen kahdella tavalla:**

```csharp
// HIDAS tapa: O(n²) — vertaa jokaista jokaiseen
bool HasDuplicatesSlow(int[] array)
{
    for (int i = 0; i < array.Length; i++)
    {
        for (int j = i + 1; j < array.Length; j++)
        {
            if (array[i] == array[j])
                return true;
        }
    }
    return false;
}

// NOPEA tapa: O(n) — muistaa jo nähdyt HashSetissä
bool HasDuplicatesFast(int[] array)
{
    var seen = new HashSet<int>();

    foreach (var item in array)
    {
        if (!seen.Add(item))    // Add palauttaa false, jos arvo on jo setissä
            return true;
    }
    return false;
}
```

---

### O(2ⁿ) — Eksponentiaalinen aika

**Selkokielellä:** Työmäärä **kaksinkertaistuu** joka kerta kun syöte kasvaa yhdellä. Käytännössä käyttökelvoton, jos n > 30.

Klassinen esimerkki on Fibonaccin lukujonon laskeminen rekursiolla:

```csharp
// O(2ⁿ) — hidas rekursiivinen Fibonacci
// Jokainen kutsu tekee kaksi uutta kutsua → puurakenne kasvaa räjähdysmäisesti
int FibonacciSlow(int n)
{
    if (n <= 1) return n;
    return FibonacciSlow(n - 1) + FibonacciSlow(n - 2);
}

// Miksi tämä on niin hidas? Piirretään kutsupuu luvulle 5:
//
//                    Fib(5)
//                  /        \
//             Fib(4)        Fib(3)
//            /     \        /     \
//        Fib(3)  Fib(2)  Fib(2)  Fib(1)
//       /    \    /   \   /   \
//    Fib(2) Fib(1) ... ...  ...
//    /   \
// Fib(1) Fib(0)
//
// Fib(3) lasketaan UUDESTAAN monta kertaa!
```

Sama tehokkaasti — silmukalla O(n):

```csharp
// O(n) — nopea iteratiivinen Fibonacci
int FibonacciFast(int n)
{
    if (n <= 1) return n;

    int prev = 0;
    int curr = 1;

    for (int i = 2; i <= n; i++)
    {
        int next = prev + curr;
        prev = curr;
        curr = next;
    }

    return curr;
}
```

Ero käytännössä:

| n | FibonacciSlow (kutsuja) | FibonacciFast (askelia) |
|---|------------------------|----------------------|
| 10 | 177 | 10 |
| 20 | 21 891 | 20 |
| 30 | 2 692 537 | 30 |
| 40 | 331 160 281 | 40 |
| 50 | ~40 000 000 000 | 50 |

Hidasta versiota luvulle 50 joutuisit odottamaan **tunteja**. Nopea versio on **välitön**.

---

### O(n!) — Faktoriaalinen aika

**Selkokielellä:** Kaikki mahdolliset järjestykset. 10 alkiolla yli 3 miljoonaa yhdistelmää, 15 alkiolla yli biljoona.

```csharp
// Kaikkien järjestysten (permutaatioiden) generointi
// Esim. [1, 2, 3] → [1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]
void GeneratePermutations(int[] array, int start, List<int[]> results)
{
    if (start == array.Length - 1)
    {
        results.Add((int[])array.Clone());
        return;
    }

    for (int i = start; i < array.Length; i++)
    {
        (array[start], array[i]) = (array[i], array[start]);
        GeneratePermutations(array, start + 1, results);
        (array[start], array[i]) = (array[i], array[start]);
    }
}
```

| n | n! (permutaatioita) |
|---|-------------------|
| 5 | 120 |
| 10 | 3 628 800 |
| 12 | 479 001 600 |
| 15 | 1 307 674 368 000 |
| 20 | ~2 400 000 000 000 000 000 |

Käytännössä faktooriaalista algoritmia ei voi ajaa yli 12-15 alkiolle.

---

## Vertailutaulukko

| Big O | Nimi | Selitys | 10 alkiota | 1 000 alkiota | Esimerkki |
|-------|------|---------|-----------|-------------|-----------|
| O(1) | Vakio | Aina sama aika | 1 | 1 | `dict[key]` |
| O(log n) | Logaritminen | Puolittuu joka askeleella | 3 | 10 | Binäärihaku |
| O(n) | Lineaarinen | Käy kaikki kerran läpi | 10 | 1 000 | `foreach`-silmukka |
| O(n log n) | Lineaarilog. | Tehokas lajittelu | 33 | 9 966 | `Array.Sort()` |
| O(n²) | Neliöllinen | Sisäkkäiset silmukat | 100 | 1 000 000 | Bubble sort |
| O(2ⁿ) | Eksponent. | Tuplaantuu per alkio | 1 024 | mahdoton | Rekursiivinen Fibonacci |
| O(n!) | Faktoriaal. | Kaikki järjestykset | 3 628 800 | mahdoton | Permutaatiot |

### Nopeusjärjestys (nopeimmasta hitaimpaan)

```
O(1)  →  O(log n)  →  O(n)  →  O(n log n)  →  O(n²)  →  O(2ⁿ)  →  O(n!)
 ↑                                                                      ↑
 |          HYVÄ — käytä näitä          |    HUONO — vältä näitä        |
 nopein                                                              hitain
```

---

## "Amortized" — keskimääräinen aika

Joskus näet merkinnän **O(1)\*** tai **"amortized O(1)"**. Tämä tarkoittaa, että operaatio on **yleensä** O(1), mutta **joskus harvoin** hitaampi.

**Esimerkki: `List<T>.Add()`**

C#:n `List<T>` on sisäisesti taulukko. Kun taulukko on täynnä ja lisäät uuden alkion:
1. Luodaan uusi, isompi taulukko (yleensä 2× kokoinen)
2. Kopioidaan kaikki vanhat alkiot uuteen taulukkoon — O(n)
3. Lisätään uusi alkio

```csharp
var list = new List<int>(); // sisäinen taulukko: koko 4

list.Add(1); // O(1) — mahtuu
list.Add(2); // O(1) — mahtuu
list.Add(3); // O(1) — mahtuu
list.Add(4); // O(1) — mahtuu
list.Add(5); // O(n) — taulukko täynnä! Kopioidaan 4 alkiota uuteen, isompaan taulukkoon
list.Add(6); // O(1) — taas mahtuu uuteen taulukkoon
// ...
```

Koska kallis kopiointi tapahtuu niin harvoin, **keskimäärin** jokainen `Add` on O(1). Siksi sanotaan "amortized O(1)".

---

## Tilavaativuus (Space Complexity)

Big O:ta käytetään myös **muistinkäytön** kuvaamiseen. Tilavaativuus kertoo, kuinka paljon **lisämuistia** algoritmi tarvitsee (syötteen oman muistin lisäksi).

```csharp
// O(1) tilavaativuus — vain yksi lisämuuttuja
int Sum(int[] array)
{
    int total = 0;

    foreach (var item in array)
    {
        total += item;
    }

    return total;
}

// O(n) tilavaativuus — luodaan uusi, yhtä suuri taulukko
int[] DoubleValues(int[] array)
{
    var result = new int[array.Length];

    for (int i = 0; i < array.Length; i++)
    {
        result[i] = array[i] * 2;
    }

    return result;
}

// O(n²) tilavaativuus — n × n matriisi
int[,] CreateMatrix(int n)
{
    return new int[n, n];
}
```

**Aika vs. tila — tasapainon valinta:**

Usein voit **vaihtaa muistia nopeuteen**. Esimerkki duplikaattien etsimisestä:

| Tapa | Aikavaativuus | Tilavaativuus |
|------|--------------|--------------|
| Kaksi silmukkaa | O(n²) | O(1) — ei lisämuistia |
| HashSet | O(n) | O(n) — tarvitsee HashSetin |

HashSet-tapa on nopeampi, mutta käyttää enemmän muistia. Yleensä **nopeus voittaa**, koska muistia on enemmän kuin aikaa.

---

## C#:n yleisten operaatioiden Big O

### Tietorakenteet

| Operaatio | Array | List\<T\> | Dictionary\<K,V\> | HashSet\<T\> | LinkedList\<T\> |
|-----------|-------|-----------|-------------------|-------------|----------------|
| Haku indeksillä | O(1) | O(1) | - | - | O(n) |
| Haku avaimella | - | - | O(1)* | O(1)* | - |
| Lisäys loppuun | - | O(1)* | O(1)* | O(1)* | O(1) |
| Lisäys alkuun | - | O(n) | - | - | O(1) |
| Poisto | - | O(n) | O(1)* | O(1)* | O(1) |
| Contains | O(n) | O(n) | O(1)* | O(1)* | O(n) |

*\* = amortized (keskimääräinen tapaus)*

**Käytännön opetus:** Jos teet paljon `Contains`-tarkistuksia, käytä `HashSet<T>` tai `Dictionary<K,V>` eikä `List<T>`.

### LINQ-operaatiot

| LINQ-metodi | Aikavaativuus | Selitys |
|-------------|--------------|---------|
| `Where()` | O(n) | Suodattaa — käy kaikki läpi |
| `Select()` | O(n) | Muuntaa jokaisen alkion |
| `First()` | O(1) – O(n) | Parhaimmillaan löytyy heti, pahimmillaan viimeinen |
| `Any()` | O(1) – O(n) | Lopettaa heti kun löytää ensimmäisen |
| `Count()` | O(1) tai O(n) | O(1) jos kokoelmalla on `Count`-property, muuten O(n) |
| `OrderBy()` | O(n log n) | Lajittelu |
| `Distinct()` | O(n) | Käyttää HashSetiä sisäisesti |
| `Contains()` Listalla | O(n) | Käy kaikki läpi |
| `Contains()` HashSetillä | O(1) | Suora haku |

---

## Käytännön vinkkejä

### 1. Tunnista silmukkarakenne → tiedät Big O:n

```csharp
// Ei silmukkaa → O(1)
return array[0];

// Yksi silmukka → O(n)
for (int i = 0; i < n; i++) { }

// Silmukka joka puolittaa → O(log n)
while (n > 0) { n = n / 2; }

// Kaksi SISÄKKÄISTÄ silmukkaa → O(n²)
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++) { }

// Kaksi PERÄKKÄISTÄ silmukkaa → O(n) (ei n²!)
for (int i = 0; i < n; i++) { }
for (int j = 0; j < n; j++) { }

// Kolme sisäkkäistä silmukkaa → O(n³)
for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
        for (int k = 0; k < n; k++) { }
```

### 2. Valitse oikea tietorakenne

```csharp
// ONGELMA: "Onko tämä arvo jo olemassa?"

// Huono: List — O(n) joka tarkistuksella
var list = new List<string>();
if (!list.Contains("Helsinki"))   // O(n) — käy kaikki läpi
    list.Add("Helsinki");

// Hyvä: HashSet — O(1) joka tarkistuksella
var set = new HashSet<string>();
set.Add("Helsinki");              // O(1) — suora haku
```

```csharp
// ONGELMA: "Hae käyttäjä ID:n perusteella"

// Huono: List — O(n) joka haulla
var users = new List<User>();
var user = users.FirstOrDefault(u => u.Id == 42); // O(n)

// Hyvä: Dictionary — O(1) joka haulla
var usersById = new Dictionary<int, User>();
var user = usersById[42]; // O(1)
```

### 3. Vältä turhia LINQ-materialisointeja

```csharp
// Huono: ToList() kesken ketjun pakottaa koko listan luomisen
var result = list
    .Where(x => x.IsActive)
    .ToList()                    // TURHA — materialisoi koko listan
    .Where(x => x.Age > 18)
    .ToList()                    // TURHA — materialisoi uudestaan
    .Select(x => x.Name)
    .ToList();                   // vasta tässä tarvitaan

// Hyvä: ketjuta, materialisoi vasta lopussa
var result = list
    .Where(x => x.IsActive && x.Age > 18)
    .Select(x => x.Name)
    .ToList();                   // yksi läpikäynti
```

### 4. Mittaa Stopwatchilla kun olet epävarma

```csharp
using System.Diagnostics;

int[] testData = Enumerable.Range(0, 100_000).ToArray();

var sw = Stopwatch.StartNew();
BubbleSort(testData);           // O(n²)
sw.Stop();
Console.WriteLine($"Bubble Sort: {sw.ElapsedMilliseconds} ms");

testData = Enumerable.Range(0, 100_000).ToArray();
sw.Restart();
Array.Sort(testData);           // O(n log n)
sw.Stop();
Console.WriteLine($"Array.Sort: {sw.ElapsedMilliseconds} ms");

// Tulokset 100 000 alkiolla (esimerkki):
// Bubble Sort: ~15 000 ms (15 sekuntia)
// Array.Sort:  ~12 ms
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **n** | Datan koko (alkioiden määrä) |
| **O(...)** | Kuvaa operaatioiden kasvuvauhtia suhteessa n:ään |
| **log n** | "Kuinka monta kertaa n puolittuu?" — kasvaa hitaasti |
| **n²** | "n kertaa n" — syntyy sisäkkäisistä silmukoista |
| **2ⁿ** | Kaksinkertaistuu per lisäys — kasvaa räjähdysmäisesti |
| **n!** | Kaikki järjestykset — kasvaa käsittämättömän nopeasti |
| **Amortized** | Keskimääräinen aika — yleensä nopea, harvoin hidas |
| **Vakiot pois** | O(3n) = O(n), koska kiinnostaa vain kasvuvauhti |
| **Suurin termi** | O(n² + n) = O(n²), koska n² dominoi |
| **Pahin tapaus** | Big O kuvaa aina pahinta mahdollista tilannetta |

### Nyrkkisäännöt

| Big O | Taso | Toimintaohje |
|-------|------|-------------|
| O(1), O(log n) | Erinomainen | Skaalautuu käytännössä rajattomasti |
| O(n) | Hyvä | Lineaarinen kasvu, yleensä hyväksyttävä |
| O(n log n) | Kelvollinen | Tehokkain mahdollinen lajittelu |
| O(n²) | Varoitus | Hidas yli 1 000 alkiolla — etsi parempi tapa |
| O(2ⁿ), O(n!) | Mahdoton | Ei toimi yli 15-20 alkiolla — vaatii toisenlaisen lähestymistavan |

### Tärkein oppi

Oikea **tietorakenteen valinta** on usein tärkein optimointi:
- Tarvitsetko nopeaa hakua? → `Dictionary` tai `HashSet` (O(1)) eikä `List` (O(n))
- Tarvitsetko lajittelua? → `Array.Sort()` tai `OrderBy()` (O(n log n))
- Tarvitsetko duplikaattien poistoa? → `HashSet` (O(n)) eikä sisäkkäisiä silmukoita (O(n²))

Seuraavaksi: [Lajittelualgoritmit](Sorting-Algorithms.md) | [Algoritmi](Algorithm.md)
