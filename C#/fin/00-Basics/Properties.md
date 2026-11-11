# Propertyt (ominaisuudet)

**Property** on luokan julkinen ovi yksityiseen tietoon. Ulkoa kirjoitat `ticket.Age = 20` kuin kenttään. Sisällä luokka päättää, mitä asetukselle tapahtuu.

Ilman propertyä joko paljastat kentän kaikille (`public int age`) tai kirjoitat `GetAge` / `SetAge`-metodit. Property on C#:n lyhyt tapa samaan asiaan.

Luokat ensin: [Luokat, oliot ja konstruktorit](../02-OOP-Concepts/Classes-and-Objects.md). Kapselointi: [Kapselointi](../02-OOP-Concepts/Encapsulation.md).

**Microsoft:** [Properties](https://learn.microsoft.com/fi-fi/dotnet/csharp/programming-guide/classes-and-structs/properties)

## Kartta

| Kirjoitus | Merkitys |
|-----------|----------|
| `{ get; set; }` | Autoproperty — C# luo piilokentän |
| `get` | Arvon luku |
| `set` | Arvon asetus. Uusi arvo on `value` |
| `{ get; private set; }` | Ulkoa voi lukea, vain luokka voi muuttaa — ulkoa asetus on CS0272 |
| Vain `get` | Laskettu tai lukittu arvo, ei asetusta |
| `public int Count { get { return tickets.Count; } }` | Laskettu property: ei omaa kenttää, arvo lasketaan joka luvulla |

## Autoproperty — aloita tästä

```csharp
public class Ticket
{
    public int Age { get; set; }
    public decimal Price { get; set; }
}

Ticket ticket = new Ticket();
ticket.Age = 20;                 // set
Console.WriteLine(ticket.Age);   // get
```

Nimi on PascalCase. Tämä riittää, kun arvoa ei tarvitse tarkistaa.

Älä tee kentästä julkista (`public int age;`), jos voit käyttää propertyä. Tavan näkee muualla C#-koodissa, ja myöhemmin voit lisätä tarkistuksen rikkomatta kutsuja.

## Getter ja setter itse kirjoitettuna

Kun asetus pitää tarkistaa, kirjoita runko auki. Piilokenttä on `private` ja camelCase.

```csharp
public class Ticket
{
    private int age;

    public int Age
    {
        get { return age; }
        set
        {
            if (value < 0 || value > 130)
            {
                throw new ArgumentException("Ikä ei kelpaa.");
            }
            age = value;
        }
    }
}
```

`value` on avainsana setterissä. Se on se arvo, jonka kutsuja kirjoitti yhtäläisyysmerkin oikealle.

Laskettu arvo ei tarvitse kenttää:

```csharp
public class Rectangle
{
    public double Width { get; set; }
    public double Height { get; set; }

    public double Area
    {
        get { return Width * Height; }
    }
}
```

`Area` vain luetaan. `rect.Area = 10` ei käänny.

Sama idea listan koolle. `TicketOrder` pitää liput `private`-listassa, ja `Count` kertoo määrän:

```csharp
public class TicketOrder
{
    private List<Ticket> tickets = new List<Ticket>();

    public int Count
    {
        get { return tickets.Count; }
    }
}
```

`Count` ei ole oma kenttä, jota pitäisi muistaa päivittää — arvo lasketaan listasta joka kerta, kun joku lukee `order.Count`. Ulkoa ei voi asettaa: `order.Count = 3` ei käänny. Listan suojaamisesta lisää: [käyttöoikeudet](Access-Modifiers.md#luokka-joka-omistaa-listan).

## private set — ulkoa ei saa muuttaa

Myytyjen lippujen määrää ei aseteta suoraan. Myynti muuttaa sitä metodilla, joka tarkistaa määrän.

```csharp
public class Movie
{
    public string Title { get; set; }
    public int TicketsSold { get; private set; }

    public void Sell(int count)
    {
        if (count > 0)
        {
            TicketsSold += count;
        }
    }
}

Movie movie = new Movie();
movie.Sell(3);
Console.WriteLine(movie.TicketsSold);   // 3
// movie.TicketsSold = 100;             // CS0272: set accessor is inaccessible
```

`get` on julkinen, `set` yksityinen. Luokan sisällä `TicketsSold += count` toimii; luokan ulkopuolella `movie.TicketsSold = 100` pysähtyy käännösvirheeseen **CS0272**. Se on hyvä uutinen: kääntäjä estää virheen, jota et ajossa huomaisi.

Jos `set` olisi julkinen, `Main` voisi kirjoittaa `movie.TicketsSold = -5` tai myydä ohi salin koon, eikä kukaan huomaisi. `Sell` on ainoa reitti, ja tarkistus on yhdessä paikassa — ei jokaisessa viidessätoista kutsukohdassa.

## Oletusarvo

```csharp
public class Settings
{
    public string Theme { get; set; } = "Light";
    public int MaxItems { get; set; } = 10;
}
```

`init` (asetus vain luonnissa) ja write-only-propertyt ovat myöhempää. Alussa `{ get; set; }` ja tarvittaessa tarkistus setterissä riittävät.

## Yhteenveto

- Property on ovi kenttään: `get` lukee, `set` asettaa.
- Autoproperty `{ get; set; }` on oletus.
- Tarkistus kirjoitetaan setteriin. Uusi arvo on `value`.
- `private set` estää muutoksen luokan ulkopuolelta (CS0272). Muutos kulkee metodin kautta, jossa tarkistus on.
- Laskettu property (`Count`) ei tarvitse kenttää: arvo lasketaan joka luvulla.

Seuraavaksi: [Luokat ja oliot](../02-OOP-Concepts/Classes-and-Objects.md) · [Kapselointi](../02-OOP-Concepts/Encapsulation.md) · [Käyttöoikeudet](Access-Modifiers.md)
