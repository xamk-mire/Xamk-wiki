# Näkyvyysalueet (Scopes)

**Näkyvyysalue** kertoo, missä muuttujan nimeä saa käyttää. Muuttuja ei ole olemassa "koko ohjelmassa". Se elää siinä lohkossa, jossa se esiteltiin.

Arjen esimerkki: tiskillä oleva lappu. Kassatyöntekijä näkee sen. Toisessa huoneessa oleva henkilö ei näe. `Main`-metodi on yksi huone. `GetUnitPrice` on toinen.

Tyypillinen tilanne: `Main`issä esitelty `childPrice` ei näy `GetUnitPrice`-metodille. Jaettu tieto (hinnat) siirretään **luokan tasolle** (`const decimal ChildPrice`).

**Microsoft:** [Scope of variables](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/variables#941-variable-scopes) — speksi on raskas; tämä sivu riittää alkuun.

## Kartta

| Missä esittelit | Missä näkyy | Esimerkki |
|-----------------|-------------|-----------|
| Metodin sisällä | Vain siinä metodissa | `int age` `Main`issa |
| `if` / `for` / `do`-lohkon sisällä | Vain sen lohkon sisällä | `int price` `if`-suluissa |
| Luokan tasolla (`const` / kenttä) | Kaikissa luokan metodeissa | `const decimal ChildPrice` |
| `do`-lohkon sisällä | **Ei** näy `while`-ehdossa | `continueAnswer` pitää esitellä ennen `do` |

`public` ja `private` ovat eri asia. Ne kertovat, kuka **luokan ulkopuolella** saa koskea jäseneen. Katso [käyttöoikeudet](Access-Modifiers.md).

## Metodi on oma huone

```csharp
class Program
{
    static void Main(string[] args)
    {
        int age = 20;
        decimal price = GetUnitPrice(age);   // OK: age annetaan argumenttina
        // GetUnitPrice ei näe Mainin age-muuttujaa nimeltä
    }

    static decimal GetUnitPrice(int age)     // tämä age on ERI muuttuja
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

`Main`in `age` ja parametrin `age` voivat käyttää samaa nimeä. Ne ovat silti kaksi säilöä. Arvo **kopioituu** kutsuessa. Katso [parametri vs argumentti](Functions-and-Methods.md#parametri-vs-argumentti).

Tämä ei käänny:

```csharp
static void Main(string[] args)
{
    decimal childPrice = 7.50m;
    decimal price = GetUnitPrice(8);
}

static decimal GetUnitPrice(int age)
{
    // return childPrice;   // virhe: The name 'childPrice' does not exist
    return 7.50m;
}
```

C# ei etsi muuttujaa naapurimetodista. Jos hinta tarvitaan useassa metodissa, nosta se luokan tasolle.

## Luokan taso — jaettu tieto

```csharp
class Program
{
    const decimal ChildPrice = 7.50m;
    const decimal AdultPrice = 12.00m;
    const decimal SeniorPrice = 9.00m;

    static decimal GetUnitPrice(int age)
    {
        if (age < 12)
        {
            return ChildPrice;
        }

        if (age < 65)
        {
            return AdultPrice;
        }

        return SeniorPrice;
    }
}
```

`const` luokan tasolla näkyy kaikille metodeille. Hinta on yhdessä paikassa. Nimi on PascalCase — [koodauskäytännöt](Coding-Conventions.md).

## Lohko — aaltosulkeiden sisällä

`if`, `for`, `while` ja `do` luovat oman lohkon. Lohkossa esitelty muuttuja kuolee, kun lohko päättyy.

```csharp
static void Example()
{
    int age = 20;   // näkyy koko metodissa

    if (age >= 18)
    {
        decimal price = 12.00m;
        Console.WriteLine(price);   // OK
    }

    // Console.WriteLine(price);    // virhe: price ei ole näkyvissä
}
```

Siksi `do-while`-ehdon muuttuja esitellään **ennen** silmukkaa:

```csharp
string? continueAnswer;   // täällä
do
{
    Console.Write("Uusi asiakas (k/e): ");
    continueAnswer = Console.ReadLine();
}
while (continueAnswer == "k");
```

Jos `string? continueAnswer` on `do`-lohkon sisällä, `while` ei näe sitä. Virhe: *The name 'continueAnswer' does not exist*. Sama idea [ohjausrakenteissa](Control-Structures.md#do-while--tee-ensin-kysy-sitten).

## Namespace ja projekti — myöhemmin

Luokat voidaan ryhmitellä `namespace`-lohkoon. Toisen projektin luokat eivät näy ilman viittausta. `internal` rajoittaa näkyvyyden samaan projektiin.

Alussa yksi `Program`-luokka riittää. Älä opettele assembly-rajoja ennen kuin sinulla on useita projekteja.

## Yhteenveto

- Muuttuja näkyy siinä lohkossa, jossa se syntyi — ei naapurimetodissa.
- Jaettu arvo (hinnat): `const` luokan tasolle.
- `do-while`-ehdon muuttuja esitellään ennen `do`-sanaa.
- `public` / `private` on käyttöoikeus, ei sama asia kuin scope.

Seuraavaksi: [Funktiot ja metodit](Functions-and-Methods.md) · [Staattiset luokat ja metodit](Static-Classes-and-Methods.md) · [Käyttöoikeudet](Access-Modifiers.md)
