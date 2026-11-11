# Satunnaisluvut (Random)

**`Random`** on luokka, jonka olio antaa satunnaislukuja. Olio luodaan **kerran**, ja samaa oliota käytetään kaikissa arvonnoissa. Luvun pyytää `Next`-metodi.

Arjen esimerkki: noppa. Heität saman nopan uudestaan ja uudestaan. Et hae jokaista heittoa varten uutta noppaa kaupasta.

Tyypillinen tilanne: lottorivi, jossa seitsemän eri numeroa väliltä 1–40. `Next(1, 41)` antaa yhden numeron, lista pitää kirjaa jo arvotuista, ja silmukka jatkuu, kunnes listassa on seitsemän.

**Microsoft:** [Random class](https://learn.microsoft.com/fi-fi/dotnet/api/system.random) — kaikki metodit; tämä sivu kattaa ne, joita tarvitset alussa.

## Kartta

| Asia | Yksi lause |
|------|------------|
| `static Random random = new Random();` | Luodaan kerran luokan tasolla, käytetään kaikkialla |
| `random.Next()` | Kokonaisluku nollasta ylöspäin, raja ei ole käytännössä kiinnostava |
| `random.Next(max)` | Kokonaisluku `0` … `max - 1` |
| `random.Next(min, max)` | Kokonaisluku `min` … `max - 1`; **yläraja ei kuulu mukaan** |
| `random.NextDouble()` | Desimaaliluku `0.0` … `1.0` (1.0 ei kuulu mukaan) |
| `list.Contains(n)` ennen `Add` | Uniikit luvut: hylätty numero ei lisää mitään |
| `letters[random.Next(letters.Length)]` | Satunnainen alkio kokoelmasta |

## Luo kerran, käytä monta kertaa

```csharp
class Program
{
    static Random random = new Random();   // yksi olio koko ohjelmalle

    static void Main(string[] args)
    {
        int first = random.Next(1, 7);
        int second = random.Next(1, 7);
    }
}
```

Luokan tason kenttä näkyy kaikille metodeille — katso [näkyvyysalueet](Scopes.md#luokan-taso--jaettu-tieto). Toinen hyvä paikka on `Main`-metodin alku, jos arvonta tehdään vain siellä.

Miksi kerran? Arvonta on yhdessä paikassa, ja sitä on helppo muuttaa. `new Random()` silmukan sisällä luo joka kierroksella uuden olion turhaan ja hämärtää koodia: lukija kysyy, miksi noppa vaihtuu joka heitolla. Vanhassa .NET Frameworkissa silmukassa luodut oliot antoivat vielä samat luvut peräkkäin. Nykyisessä .NETissä niin ei käy, mutta tapa on silti huono.

## Next — yläraja ei kuulu mukaan

```csharp
int die = random.Next(1, 7);       // 1, 2, 3, 4, 5 tai 6 — ei koskaan 7
int index = random.Next(10);       // 0 … 9
int lotto = random.Next(1, 41);    // 1 … 40
```

`Next(min, max)` palauttaa luvun, joka on vähintään `min` ja **pienempi kuin** `max`. Kun haluat luvun 1–6, kirjoitat `Next(1, 7)`. Sääntö on sama kuin `for`-silmukan ehdossa `i < 6`: yläraja on raja, ei viimeinen arvo.

`NextDouble()` antaa desimaaliluvun väliltä `0.0`–`1.0`. Sitä tarvitaan harvemmin; kokonaisluvut riittävät pitkälle.

## Arvonta omassa metodissa

```csharp
static int SpinReel()
{
    return random.Next(1, 7);      // yksikätisen rosvon rulla 1–6
}

static int DrawNumber()
{
    return random.Next(1, 41);     // lottonumero 1–40
}
```

Metodi kertoo nimellään, mitä arvotaan. Rajat ovat yhdessä paikassa: jos lotto muuttuu 1–39:ksi, muutat yhden rivin. Katso [funktiot ja metodit](Functions-and-Methods.md).

## Uniikit luvut — while, ei for

```csharp
List<int> numbers = new List<int>();

while (numbers.Count < 7)
{
    int n = random.Next(1, 41);

    if (!numbers.Contains(n))
    {
        numbers.Add(n);
    }
}
```

Silmukka jatkuu, kunnes listassa on **seitsemän** lukua. Jos arvottu numero on jo listassa, kierros ei lisää mitään, ja silmukka arpoo uuden.

`for (int i = 0; i < 7; i++)` on tässä väärä työkalu. Se tekee tasan seitsemän kierrosta. Jos kaksi arvontaa osuu samaan numeroon ja duplikaatti hylätään, listaan jää kuusi lukua. Kierrosten määrä ei ole sama kuin lukujen määrä. Katso [Contains](Data-Structures.md#list--koko-kasvaa).

## Satunnainen alkio kokoelmasta

```csharp
string[] letters = { "A", "B", "C", "D" };
string letter = letters[random.Next(letters.Length)];   // indeksi 0 … 3

List<string> names = new List<string> { "Matti", "Liisa", "Pekka" };
string name = names[random.Next(names.Count)];
```

`Next(letters.Length)` antaa `0` … `Length - 1`, eli juuri lailliset indeksit. Taulukolla `Length`, listalla `Count` — katso [indeksi alkaa nollasta](Data-Structures.md#indeksi-alkaa-nollasta).

## Satunnainen odotus

```csharp
int waitMs = random.Next(1000, 5001);   // 1000 … 5000 ms eli 1–5 s
Thread.Sleep(waitMs);
```

Pelissä satunnainen tauko tuntuu luonnollisemmalta kuin aina sama. `Thread.Sleep` pysäyttää ohjelman millisekunneiksi — katso [Thread.Sleep](Thread-Sleep.md).

## Yleisiä virheitä

**1. `Next(1, 20)` ei koskaan anna lukua 20**

Yläraja ei kuulu mukaan. Luku 1–20 on `Next(1, 21)`.

**2. `new Random()` silmukan sisällä**

Luo olio kerran luokan tasolla tai `Main`-metodin alussa. Silmukassa luominen on turhaa ja tekee koodista vaikeamman lukea.

**3. `for` seitsemän kertaa ja duplikaatit hylätään**

Listaan jää vähemmän kuin seitsemän lukua. Käytä `while (numbers.Count < 7)`.

**4. `Next(0, 1)` on aina 0**

Väli `0` … `1 - 1` sisältää vain nollan. Kolikonheitto on `Next(0, 2)` tai `Next(2)`.

## Yhteenveto

- `Random` on luokka. Luo olio kerran (`static Random random = new Random();`) ja käytä samaa kaikissa arvonnoissa.
- `Next(min, max)`: yläraja ei kuulu mukaan. Noppa on `Next(1, 7)`.
- Arvonta omassa metodissa (`DrawNumber`), rajat yhdessä paikassa.
- Uniikit luvut: `while (list.Count < n)` + `Contains` ennen `Add`. `for` kiinteällä määrällä ei toimi.
- Satunnainen alkio: `items[random.Next(items.Length)]`.

Seuraavaksi: [Thread.Sleep](Thread-Sleep.md) · [Tietorakenteet](Data-Structures.md) · [Ohjausrakenteet](Control-Structures.md)
