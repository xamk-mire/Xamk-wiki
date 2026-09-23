# Funktiot ja metodit (Functions and Methods)

**Metodi** on nimetty pala koodia. Se kirjoitetaan **kerran** ja sitä kutsutaan **monesti**.

Ilman metodia sama `if`-ketju kopioituu jokaiseen paikkaan, jossa hintaa tarvitaan. Kun sääntö muuttuu, joudut korjaamaan kaikki kopiot. Metodissa korjaus on yhdessä paikassa.

C#:ssa funktiot asuvat luokassa, joten puhutaan yleensä **metodeista**. Sana "funktio" tarkoittaa samaa asiaa yleisessä ohjelmoinnissa.

**Microsoft:** [Methods](https://learn.microsoft.com/fi-fi/dotnet/csharp/programming-guide/classes-and-structs/methods)

## Kartta

| Termi | Yksi lause |
|-------|------------|
| Määrittely | Kertoo, mitä metodi tekee — ei aja mitään yksin |
| Kutsu | Ajaa metodin juuri tässä kohdassa |
| `void` | Metodi ei palauta arvoa — se vain tekee (tulostaa, kysyy) |
| Paluutyyppi | `int`, `decimal`, `string`… kutsuja saa tuloksen `return`-lauseella |
| Parametri | Metodin oma muuttuja, vastaanottaa arvon |
| Argumentti | Arvo, joka annetaan kutsussa |
| `static` | Ennen olioita: kirjoita `static` jokaisen metodin eteen |
| `Main` | Ohjelman aloitus — suoritus alkaa täältä |

## static ja Main

Ennen olio-ohjelmointia metodit merkitään `static`-sanalla ja ne asuvat `Program`-luokassa. `Main` on käynnistyspiste. Suoritus alkaa sieltä, kun painat Ctrl+F5.

```csharp
class Program
{
    static void Main(string[] args)
    {
        PrintHeader();
        decimal price = GetUnitPrice(40);  // 12.00
        Console.WriteLine(price);
    }

    static void PrintHeader()
    {
        Console.WriteLine("=== Elokuvateatteri Tähti ===");
    }

    static decimal GetUnitPrice(int age)
    {
        if (age < 12)
        {
            return 7.50m;
        }

        if (age < 65)
        {
            return 12.00m;
        }

        return 9.00m;
    }
}
```

| Osa | Selitys |
|-----|---------|
| `static` | Kuuluu luokalle. Alussa kirjoita `static` jokaisen metodin eteen. Ilman sitä kutsu `Main`ista ei käänny. |
| `void` | Ei palauta arvoa |
| `decimal` | Palauttaa hinnan `return`-lauseella |
| `Main` | Visual Studion "top-level statements" voi piilottaa tämän. Rakenne avataan myöhemmin. |

Metodien järjestyksellä tiedostossa ei ole väliä. Suoritus alkaa `Main`ista. `GetUnitPrice` ei ala itsestään, vaikka se on tiedostossa ylempänä tai alempana.

## Määrittely vs kutsu

| | Määrittely | Kutsu |
|---|---|---|
| **Koodi** | `static void PrintHeader() { ... }` | `PrintHeader();` |
| **Mitä tekee** | Kertoo *mitä* metodi tekee | Suorittaa metodin juuri tässä kohdassa |
| **Montako kertaa** | Kirjoitetaan kerran | Voidaan kutsua vaikka sata kertaa |

Kutsu tarvitsee sulkeet `()`. Ilman niitä C# ei aja metodia.

Kun `Main` kutsuu `GetUnitPrice(40)`:

1. Suoritus hyppää metodiin.
2. Parametri `age` saa arvon `40`.
3. `if`-ketju valitsee `12.00m`.
4. `return` lähettää hinnan takaisin.
5. `Main` jatkaa: `price` on `12.00m`.

## Parametri vs argumentti

**Parametri** on metodin oma muuttuja. **Argumentti** on arvo, joka kopioidaan parametriin kutsussa.

Järjestys ratkaisee, ei nimi.

```csharp
static decimal GetDiscount(string? code, decimal subtotal)
{
    // ...
}

decimal discount = GetDiscount(discountCode, subtotal);
// argumentti discountCode → parametri code
// argumentti subtotal     → parametri subtotal
```

Jos vaihdat argumenttien paikkaa, C# ei varoita nimistä. Väärä arvo menee väärään parametriin. Klassinen ikuisen silmukan syy: `ReadInt(prompt, 8, 1)` kun tarkoitus oli `min=1, max=8`.

Parametriin kopioituu **arvo**. Metodin sisällä `age++` ei muuta `Main`in muuttujaa. Alussa tämä riittää. `ref` ja `out` ovat myöhempää asiaa.

## return — anna tulos ja lopeta

`return` palauttaa arvon kutsujalle **ja lopettaa metodin**. Riville `return`in jälkeen ei mennä.

```csharp
static decimal GetUnitPrice(int age)
{
    if (age < 12)
    {
        return 7.50m;
    }

    if (age < 65)
    {
        return 12.00m;
    }

    return 9.00m;
}
```

Jos tyyppi ei ole `void`, **jokaisesta** polusta pitää löytyä `return`. Muuten käännösvirhe: *not all code paths return a value*.

`void`-metodissa `return;` saa olla ilman arvoa. Se vain poistuu metodista.

Tallenna paluuarvo muuttujaan, jos tarvitset sitä myöhemmin:

```csharp
decimal price = GetUnitPrice(age);
decimal lineTotal = price * ticketCount;
```

Tai käytä suoraan: `Console.WriteLine(GetUnitPrice(40));`

## Käännösvirhe vai kaatuminen?

| | Käännösvirhe | Ajonaikainen virhe (poikkeus) |
|---|---|---|
| **Milloin** | Ennen ajoa — ohjelma ei käänny | Kesken ajon — ohjelma kaatuu |
| **Missä** | Error List, punainen alleviivaus | Konsolin virheilmoitus |
| **Esimerkki** | Puuttuva `return` tai `;` | `FormatException` syötteestä `"abc"` |

## Kuormitus — sama nimi, eri parametrit

Sama metodinimi voi esiintyä useasti, jos parametrit eroavat määrältä tai tyypiltä. C# valitsee version **argumenttien** perusteella.

```csharp
static int ReadInt(string prompt)
{
    Console.Write(prompt);
    string text = Console.ReadLine();
    int value;
    bool ok = int.TryParse(text, out value);

    while (!ok)
    {
        Console.WriteLine("Anna kokonaisluku.");
        Console.Write(prompt);
        text = Console.ReadLine();
        ok = int.TryParse(text, out value);
    }

    return value;
}

static int ReadInt(string prompt, int min, int max)
{
    int value = ReadInt(prompt);   // kutsuu yksinkertaista versiota

    while (value < min || value > max)
    {
        Console.WriteLine($"Anna luku väliltä {min}–{max}.");
        value = ReadInt(prompt);
    }

    return value;
}

int age = ReadInt("Anna ikäsi: ", 0, 130);        // 3 argumenttia → tarkistava
int raw = ReadInt("Anna mikä tahansa luku: ");    // 1 argumentti → yksinkertainen
```

Huomaa: luku luetaan `TryParse`-silmukalla, ei `Convert.ToInt32`-kutsulla. `Convert.ToInt32` kaataisi ohjelman syötteellä `abc` — `TryParse` kysyy uudelleen.

Nimi `ReadInt` toistuu, mutta tehtävä on sama idea: lue luku. Toinen versio lisää rajat.

## Yleisiä virheitä

**1. Unohdit `static`**

`Main` on `static`. Se voi kutsua suoraan vain `static`-metodeja. Ilman `static`-sanaa tulee käännösvirhe.

**2. Unohdit sulkeet kutsussa**

`PrintHeader;` ei aja metodia. Oikein: `PrintHeader();`

**3. Paluuarvo hukataan**

`GetUnitPrice(40);` laskee hinnan ja heittää sen pois. Tallenna: `decimal price = GetUnitPrice(40);`

**4. Argumentit väärässä järjestyksessä**

Nimet eivät suojaa. Tarkista määrittelyn sulkeet.

## Valinnaiset nimet ja oletusarvot — myöhemmin

Parametrille voi antaa oletuksen (`string greeting = "Hei"`) tai nimetä argumentin kutsussa (`min: 1, max: 8`). Alussa kirjoita argumentit järjestyksessä.

`ref`, `out`, tuplet, lambda ja extension-metodit kuuluvat myöhempään. Rekursio (metodi kutsuu itseään): [Rekursio](Recursion.md).

`static` tarkemmin: [Staattiset luokat ja metodit](Static-Classes-and-Methods.md). Näkyvyys: [Näkyvyysalueet](Scopes.md).

## Yhteenveto

- Metodi kirjoitetaan kerran, kutsutaan monesti. Tuloste ei muutu, rakenne paranee.
- `void` tekee. Muu tyyppi palauttaa arvon `return`-lauseella.
- Parametri vastaanottaa, argumentti annetaan — järjestyksessä.
- Alussa `static` jokaiseen metodiin. Suoritus alkaa `Main`ista.
- Kuormitus: sama nimi, eri parametrit.

Seuraavaksi: [Näkyvyysalueet](Scopes.md) · [Staattiset luokat ja metodit](Static-Classes-and-Methods.md) · [Ohjausrakenteet](Control-Structures.md)
