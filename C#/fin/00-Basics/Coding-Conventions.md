# Koodauskäytännöt (Coding Conventions)

Koodia lukee kaksi tahoa: **tietokone** ja **ihminen**. Tietokone hyväksyy monenlaisen ulkoasun, jos syntaksi on oikein. Ihmisen on vaikea lukea koodia, jossa nimet ovat `a`, `b` ja `x2` ja sisennys hyppii.

**Koodauskäytäntö** on yhteinen tapa kirjoittaa: nimet, sisennys, aaltosulkeet. C#:ssa noudatetaan Microsoftin tapaa. Kurssilla sama tapa, jotta opettaja ja opiskelija lukevat samaa kieltä.

Kirjoita ensin ohjelma toimimaan. Siisti nimet ja sisennys ennen palautusta. Visual Studio auttaa: **Ctrl+K**, sitten **Ctrl+D** muotoilee tiedoston.

**Microsoft:** [Nimet](https://learn.microsoft.com/fi-fi/dotnet/csharp/fundamentals/coding-style/identifier-names) · [Käytännöt](https://learn.microsoft.com/fi-fi/dotnet/csharp/fundamentals/coding-style/coding-conventions)

## Kartta

| Käytäntö | Alussa riittää |
|----------|----------------|
| camelCase | Paikalliset muuttujat: `ticketCount`, `unitPrice` |
| PascalCase | Metodit ja luokat: `GetUnitPrice`, `Program` |
| Englanti koodissa | `ticketCount`, ei `lippumaara` — tulosteet saavat olla suomeksi |
| 4 välilyöntiä | Sisennä lohkon sisältö |
| Aaltosulkeet omalla rivillä | C#-tyyli |
| Kuvaava nimi | `age` ei `a`, `isStudent` ei `flag` |

## Kaksi kirjoitustapaa

**camelCase** alkaa pienellä. Seuraavat sanat isolla: `ticketCount`.

**PascalCase** alkaa isolla: `GetUnitPrice`.

| Mikä | Tapa | Esimerkki |
|------|------|-----------|
| Muuttuja metodin sisällä | camelCase | `int ticketCount = 2;` |
| Parametri | camelCase | `GetUnitPrice(int age)` |
| Metodi | PascalCase | `PrintHeader()` |
| Luokka | PascalCase | `class Program` |
| Vakio (`const`) | PascalCase | `const decimal ChildPrice = 7.50m;` |

```csharp
class Program
{
    const decimal AdultPrice = 12.00m;

    static void Main(string[] args)
    {
        int ticketCount = 2;
        decimal total = AdultPrice * ticketCount;
        PrintTotal(total);
    }

    static void PrintTotal(decimal total)
    {
        Console.WriteLine($"Maksettavaa: {total:F2} €");
    }
}
```

Nimi on kirjainkokoherkkä: `age` ja `Age` ovat eri nimet. C# ei sekoita niitä.

## Säännöt nimelle

1. Alkaa kirjaimella tai alaviivalla `_`.
2. Saa sisältää kirjaimia, numeroita ja alaviivoja.
3. Ei saa olla varattu sana (`int`, `class`, `void`).
4. Ei saa sisältää välilyöntiä eikä viivaa.

```csharp
int age = 25;              // hyvä
string firstName = "Matti";
int _count = 0;            // sallittu, harvoin tarpeen alussa

// int 2age = 25;          // ei voi alkaa numerolla
// string first-name = ""; // viiva ei käy
// int class = 5;          // varattu sana
```

## Nimen pitää kertoa tarkoitus

```csharp
int userAge = 25;
string customerName = "Matti";
bool isStudent = true;

// int a = 25;
// string n = "Matti";
// bool flag = true;
```

Totuusarvoille luonteva alku on `is`, `has` tai `can`: `isAdult`, `hasDiscount`.

Nimet kirjoitetaan **englanniksi**: muuttujat, metodit ja luokat. Käyttäjälle näkyvät tulosteet ja kommentit saavat olla suomeksi. Näin koodi näyttää samalta kuin työelämässä, ja englanninkieliset virheilmoitukset sekä dokumentaatio istuvat samaan tekstiin.

Metodin nimi on **verbi + kohde**: `PrintHeader`, `GetUnitPrice`, `ReadInt`. Pelkkä `Price` ei kerro, tulostetaanko vai palautetaanko arvo. Testi: täydennä lause *"tämä metodi ___"* — jos lause ei synny, nimi on huono.

Vakiintunut etuliite kertoo lukijalle jo paluutyypin:

| Etuliite | Lupaa | Esimerkki |
|----------|-------|-----------|
| `Print…` | tulostaa, ei palauta mitään (`void`) | `PrintReceipt` |
| `Read…` | kysyy käyttäjältä ja palauttaa luetun arvon | `ReadInt` |
| `Get…` | päättelee tai laskee ja palauttaa arvon | `GetUnitPrice` |
| `Is…` / `Has…` / `Can…` | palauttaa `bool`-arvon | `IsAdult` |

Nimi ei saa valehdella: jos `GetPrice` myös tulostaa, metodi tekee enemmän kuin nimi lupaa — ja seuraava lukija yllättyy. Yksi metodi, yksi työ.

Lyhenteitä kannattaa välttää, paitsi tuttuja (`id`, `i` silmukan laskurina). `custNm` on huonompi kuin `customerName`.

## Muotoilu

Sisennykseen **4 välilyöntiä**, ei kaksi. Visual Studion oletus on tämä.

Aaltosulkeet `{` ja `}` omalle rivilleen:

```csharp
static decimal GetUnitPrice(int age)
{
    if (age < 12)
    {
        return 7.50m;
    }

    return 12.00m;
}
```

Älä kirjoita `{` metodin nimen perään samalle riville. Se on toisen kielen tyyli.

Jätä tyhjä rivi metodien väliin. Älä jätä kymmentä tyhjää riviä.

Jos sisennys on sekaisin, älä korjaa käsin rivi riviltä. Valitse tiedosto ja paina **Ctrl+K**, **Ctrl+D**.

## Kommentit

Kommentti selittää **miksi**, ei sitä mitä koodi jo sanoo.

```csharp
// Ikä 65+ käyttää seniorin hintaa — raja on sama kuin lippusäännöissä
if (age >= 65)
{
    price = 9.00m;
}

// Huono: toistaa koodin
// if age is greater than or equal to 65
```

`//` on yhden rivin kommentti. `/* ... */` peittää useita rivejä. Älä jätä vanhaa koodia kommentteihin "varmuuden vuoksi" — sen hoitaa Git.

XML-kommentit (`/// <summary>`) kuuluvat julkisiin kirjastoihin. Alussa tavallinen `//` riittää.

## Yhteenveto

- Koodia luetaan. Nimeä niin, että rivi kertoo tarkoituksen.
- Muuttujat camelCase, metodit ja luokat PascalCase.
- Neljä välilyöntiä, aaltosulkeet omalla rivillä, **Ctrl+K Ctrl+D**.
- Kommentoi syy, älä itsestäänselvyyttä.

Seuraavaksi: [Visual Studio -vinkit](Visual-Studio-Tips.md) · [Muuttujat](Variables.md) · [Funktiot ja metodit](Functions-and-Methods.md)
