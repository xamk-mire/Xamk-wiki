# Staattiset luokat ja metodit (`static`)

`static` tarkoittaa: tämä kuuluu **luokalle**, ei yksittäiselle oliolle.

Ennen olio-ohjelmointia kirjoitat `static` jokaisen metodin eteen. Siksi `Main` voi kutsua `PrintHeader()`-metodia ilman `new Program()`.

Arjen esimerkki: teatterin hinnasto seinällä. Hinnasto ei kuulu yhdelle asiakkaalle. Se on yhteinen. `const decimal AdultPrice` on seinähinnasto. Yhden asiakkaan ikä `age` ei ole `static` — se vaihtuu asiakkaittain.

**Microsoft:** [Static classes and members](https://learn.microsoft.com/fi-fi/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members)

## Kartta

| Kirjoitus | Merkitys alussa |
|-----------|-----------------|
| `static void Main` | Ohjelman aloitus |
| `static decimal GetUnitPrice` | Apumetodi, kutsutaan suoraan |
| `const decimal ChildPrice` | Yhteinen vakio, näkyy kaikille metodeille |
| `static class` | Luokka, josta ei tehdä oliota: `Math.Round(x)`, ei `new Math()` |
| Olion metodi ilman `static` | Näkee olion omat propertyt; kutsutaan oliolla: `movie.Describe()` |
| CS0120 | Sekoitit puolet: staattinen metodi käyttää olion tietoa, tai olion metodi kutsuttiin luokan nimellä |

## Miksi `static` on joka metodissa?

`Main` on `static`. Staattinen metodi voi kutsua suoraan vain toisia staattisia metodeja.

```csharp
class Program
{
    const decimal AdultPrice = 12.00m;

    static void Main(string[] args)
    {
        decimal price = GetUnitPrice(40);
        Console.WriteLine(price);
    }

    static decimal GetUnitPrice(int age)
    {
        if (age < 12)
        {
            return 7.50m;
        }

        if (age < 65)
        {
            return AdultPrice;
        }

        return 9.00m;
    }
}
```

Jos poistat `static`-sanan `GetUnitPrice`-metodista, `Main` ei voi kutsua sitä. Käännösvirhe **CS0120** kertoo, että olion jäsentä ei voi käyttää ilman oliota.

`const` luokan tasolla on jo yhteinen. Sitä ei merkitä `static`-sanalla erikseen — vakio on valmiiksi luokan tasolla.

Lisää metodeista: [Funktiot ja metodit](Functions-and-Methods.md). Näkyvyys: [Näkyvyysalueet](Scopes.md).

## Kutsu luokan nimen kautta

Kun metodi on `static`, sitä kutsutaan luokan nimellä, jos ollaan toisen luokan puolella:

```csharp
decimal area = Math.PI * 2 * 2;     // Math on valmis staattinen luokka
int bigger = Math.Max(3, 8);        // 8
```

Omassa `Program`-luokassa nimeä ei tarvitse toistaa: `GetUnitPrice(40)` riittää.

`Math` on hyvä esimerkki valmiista staattisesta luokasta: `Math.Round`, `Math.Max` ja muut saavat kaiken datan parametreina, eikä `new Math()` käänny. Katso [Math-luokka](Math.md).

## Olion metodi vai staattinen — CS0120

`Movie`-luokan `Describe()` ei ole `static`, koska se käyttää olion omaa tietoa: `Title` tarkoittaa sen elokuvan nimeä, jolle metodia kutsuttiin. `Main` ja `ReadInt` ovat `static`, koska ne eivät kuulu millekään oliolle — `ReadInt` ei tarvitse yhdenkään elokuvan tietoja.

Sama käännösvirhe tulee kumpaankin suuntaan:

```csharp
class Movie
{
    public string Title { get; set; }

    static void Print()
    {
        Console.WriteLine(Title);   // CS0120: kenen Title?
    }
}

Movie.Describe();                   // CS0120: olion metodi ilman oliota
```

Korjaus: anna olio parametrina (`static void Print(Movie movie)` ja `movie.Title`) tai poista `static`. Olion metodi kutsutaan aina oliolla: `movie.Describe()`.

## Mitä `static` ei ole

`static` ei tarkoita "arvo ei muutu". Se tarkoittaa "yhteinen luokalle".

Muuttuva yhteinen laskuri on mahdollinen (`static int customersServed`), mutta alussa vältä sitä. Kaksi metodia voi yllättäen muuttaa samaa lukua. Asiakkaan ikä ja lippumäärä pysyvät tavallisina muuttujina.

Arvo, joka **ei** muutu, merkitään `const`-sanalla.

## Staattinen luokka — Math

`static class` on lipas apumetodeille. Siitä ei voi tehdä oliota (`new` ei käänny), ja kaikki jäsenet ovat `static`. Käytät sellaista jo: `Math.Round(x, 2)` kutsutaan luokan nimellä, `new Math()` ei käänny. Oma staattinen luokka näyttää samalta:

```csharp
public static class PriceList
{
    public const decimal ChildPrice = 7.50m;

    public static decimal GetUnitPrice(int age)
    {
        if (age < 12)
        {
            return ChildPrice;
        }

        if (age < 65)
        {
            return 12.00m;
        }

        return 9.00m;
    }
}

// decimal p = PriceList.GetUnitPrice(40);
// PriceList list = new PriceList();   // virhe
```

Omaa staattista luokkaa et tarvitse, kun kaikki on vielä `Program`-luokassa. `Math` riittää esimerkiksi.

Olio, jolla on oma tila (yhden lipun tiedot, yhden tilin saldo), **ei** ole `static`. Siihen palataan [luokissa](../02-OOP-Concepts/Classes-and-Objects.md).

Extension-metodit, staattinen konstruktori ja säikeet ovat myöhempää. Älä opettele niitä ennen olioita.

## Yhteenveto

- `static` = kuuluu luokalle. Alussa jokainen metodi on `static`.
- `Main` kutsuu vain staattisia metodeja suoraan.
- Yhteinen hinta: `const` luokan tasolle.
- `static` ei tarkoita vakioita. Vakio on `const`.
- `Math` on staattinen luokka: `Math.Round(x)`, ei `new Math()`.
- Olion metodi (`Describe`) ei ole `static`, koska se käyttää olion omaa tietoa. CS0120 kumpaankin suuntaan: staattinen metodi ei näe `Title`-propertyä, ja `Movie.Describe()` ei käy ilman oliota.

Seuraavaksi: [Funktiot ja metodit](Functions-and-Methods.md) · [Näkyvyysalueet](Scopes.md) · [Math-luokka](Math.md) · [Luokat ja oliot](../02-OOP-Concepts/Classes-and-Objects.md)
