# Käyttöoikeudet (Access Modifiers)

**Käyttöoikeus** kertoo, kuka saa koskea luokkaan, metodiin tai propertyyn. Se ei ole sama asia kuin [näkyvyysalue](Scopes.md). Scope vastaa: *missä lohkossa nimi elää?* Käyttöoikeus vastaa: *saako toinen luokka koskea tähän jäseneen?*

Alussa riittää kaksi sanaa: **`public`** ja **`private`**.

Arjen esimerkki: kassan näyttö on `public` — asiakas näkee hinnan. Kassan sisäinen laskukaava on `private` — asiakas ei muuta sitä.

**Microsoft:** [Access modifiers](https://learn.microsoft.com/fi-fi/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers)

## Kartta

| Sana | Kuka näkee | Alussa |
|------|------------|--------|
| `public` | Kuka tahansa | Metodit ja propertyt, joita kutsutaan ulkoa |
| `private` | Vain tämä luokka | Kentät, apumetodit |
| `protected` | Tämä luokka ja perivät luokat | Kun opit perinnän |
| `internal` | Sama projekti | Oletus luokalle ilman sanaa |

## public ja private

```csharp
public class Ticket
{
    private int age;                 // vain Ticketin sisällä

    public int Age                   // muut luokat saavat lukea ja asettaa
    {
        get { return age; }
        set { age = value; }
    }

    public decimal GetPrice()
    {
        return age < 12 ? 7.50m : 12.00m;
    }
}

Ticket ticket = new Ticket();
ticket.Age = 20;                     // OK: Age on public
decimal price = ticket.GetPrice();   // OK
// ticket.age = 20;                  // virhe: age on private
```

Nyrkkisääntö: kentät `private`, se mitä tarjotaan ulos `public`. Näin luokka pitää tilansa kasassa. Katso [propertyt](Properties.md) ja [kapselointi](../02-OOP-Concepts/Encapsulation.md).

Luokan jäsen ilman sanaa on C#:ssa `private`. Luokka ilman sanaa on `internal` (näkyy samassa projektissa). Alussa merkitse luokka `public`-sanalla, kun sitä käytetään muualta.

## Analogiat

| Sana | Kuva |
|------|------|
| `public` | Avoin kirjasto — kuka tahansa saa tulla |
| `private` | Oma päiväkirja — vain sinä |
| `protected` | Perheessä jaettu esine — sinä ja lapsesi, ei naapuri |
| `internal` | Työpaikan käytävä — saman firman väki, ei ulkopuoliset |

## protected ja internal — myöhemmin

`protected` tarvitaan, kun aliluokka käyttää kantaluokan jäsentä. Siihen palataan [perinnässä](../02-OOP-Concepts/Inheritance.md).

`internal` rajaa jäsenen samaan projektiin. Hyödyllinen kirjastoissa. Yhdessä Console App -projektissa et huomaa eroa `public`-sanaan.

Yhdistelmät `protected internal` ja `private protected` ovat harvinaisia. Älä opettele niitä ennen perusosia.

## Yhteenveto

- `public` = ulkoa saa käyttää. `private` = vain luokan sisällä.
- Kentät piiloon. Propertyt ja metodit esille tarpeen mukaan.
- Scope (lohko) ja käyttöoikeus (kuka) ovat eri kysymykset.
- `protected` perintään, `internal` projektiin — myöhemmin.

Seuraavaksi: [Propertyt](Properties.md) · [Näkyvyysalueet](Scopes.md) · [Kapselointi](../02-OOP-Concepts/Encapsulation.md)
