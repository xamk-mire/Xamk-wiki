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
| `{ get; private set; }` | Ulkoa voi lukea, vain luokka voi muuttaa |
| Vain `get` | Laskettu tai lukittu arvo, ei asetusta |

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

## private set — ulkoa ei saa muuttaa

Saldoa ei aseteta suoraan. Talletus ja nosto muuttavat sitä metodeilla.

```csharp
public class BankAccount
{
    public decimal Balance { get; private set; }

    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            Balance += amount;
        }
    }
}

BankAccount account = new BankAccount();
account.Deposit(100);
Console.WriteLine(account.Balance);   // 100
// account.Balance = 1_000_000;       // ei käänny
```

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
- `private set` estää muutoksen luokan ulkopuolelta.

Seuraavaksi: [Luokat ja oliot](../02-OOP-Concepts/Classes-and-Objects.md) · [Kapselointi](../02-OOP-Concepts/Encapsulation.md) · [Käyttöoikeudet](Access-Modifiers.md)
