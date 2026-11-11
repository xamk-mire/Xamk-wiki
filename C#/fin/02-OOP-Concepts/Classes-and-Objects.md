# Luokat, oliot ja konstruktorit

Staattisista metodeista siirrytään **olioihin**: data ja sen käsittely kootaan yhteen tyyppiin. Tämä sivu on se ensimmäinen askel — kapselointi ja perintä tulevat seuraavaksi.

Taustateoria: [Mitä on OOP?](What-is-OOP.md) · Propertyt: [Properties](../00-Basics/Properties.md)

## Kartta

| Käsite | Yksi lause |
|--------|------------|
| Luokka | Piirustus omassa tiedostossaan (`Movie.cs`): mitä tietoja ja toimintoja tyypillä on |
| Olio | Yksi kappale luokasta — jokaisella omat arvot, samat metodit |
| `new` | Luo olion muistiin ja ajaa konstruktorin: `new Movie("Kauhua keskiyöllä", 102)` |
| Property | Olion tieto: `public string Title { get; set; }` |
| Olion metodi | Ilman `static`; näkee olion omat propertyt: `movie.Describe()` |
| Konstruktori | Metodi luokan nimellä ilman paluutyyppiä; ajetaan `new`-kutsussa |
| Oletuskonstruktori | Tyhjä `new Movie()`, joka katoaa, kun kirjoitat oman (CS1729) |
| Viite vs arvo | `Movie b = a` osoittaa samaan olioon; `int y = x` kopioi luvun |
| `null` | Olio-muuttuja ilman `new`-kutsua; piste-kutsu kaataa ohjelman |

## Luokka on piirustus, olio on kappale

**Luokka** (`class`) kuvaa, millaisia tietoja ja toimintoja tyypillä on. **Olio** (object, instance) on yksi konkreettinen kappale tuosta tyypistä.

```
Luokka Pizza          Olio 1              Olio 2
┌─────────────┐      ┌─────────────┐     ┌─────────────┐
│ Name        │  →   │ "Margherita"│     │ "Pepperoni" │
│ Price       │      │  8.50       │     │  10.00      │
│ Describe()  │      │ Describe()  │     │ Describe()  │
└─────────────┘      └─────────────┘     └─────────────┘
```

Sama luokka, monta oliota — jokaisella omat arvot, samat metodit.

```csharp
class Pizza
{
    public string Name { get; set; }
    public decimal Price { get; set; }

    public void Describe()
    {
        Console.WriteLine($"{Name}: {Price:F2} €");
    }
}

Pizza first = new Pizza();
first.Name = "Margherita";
first.Price = 8.50m;

Pizza second = new Pizza();
second.Name = "Pepperoni";
second.Price = 10.00m;

first.Describe();   // Margherita: 8,50 €
second.Describe();  // Pepperoni: 10,00 €
```

| Käsite | Merkitys |
|--------|----------|
| `class Pizza` | Tyypin määrittely — ei vielä yhtään pizzaa |
| `new Pizza()` | Luo olion muistiin |
| `first.Name` | Tämän olion kenttä/property |
| `first.Describe()` | Kutsuu metodia **tälle** oliolle |

Aiemmin metodit olivat usein `static` ja asuivat `Program`-luokassa. Olion metodi kuuluu oliolle: se näkee olion omat arvot ilman että niitä annetaan parametreina.

Luokka kirjoitetaan omaan tiedostoon: **Add → Class…** → `Movie.cs`. Yksi luokka, yksi tiedosto — Visual Studio näkee projektin kaikki `.cs`-tiedostot ilman `using`-riviä.

Olio syntyy vain `new`-kutsulla. `Movie m;` ilman `new`-sanaa on `null` — muuttuja ei osoita mihinkään — ja `m.Title` kaataa ohjelman: **NullReferenceException**. Korjaus on aina sama: `new`.

## Property — olion julkinen tieto

Property näyttää muuttujalta, mutta se on luokan jäsen. Auto-property riittää alkuun:

```csharp
public string Name { get; set; }
public decimal Price { get; set; }
```

`get` lukee arvon, `set` asettaa sen. Nimeäminen: propertyt **PascalCase** (`Name`), paikalliset muuttujat **camelCase** (`name`). Syvemmin: [Properties](../00-Basics/Properties.md).

## Konstruktori — olion syntymä

Konstruktori on metodi, joka ajetaan **automaattisesti** kun kirjoitat `new`. Sen nimi on sama kuin luokan, eikä sillä ole paluutyyppiä (ei edes `void`).

```csharp
class Pizza
{
    public string Name { get; set; }
    public decimal Price { get; set; }

    public Pizza(string name, decimal price)
    {
        Name = name;
        Price = price;
    }
}

Pizza pizza = new Pizza("Margherita", 8.50m);
```

Ilman konstruktoria arvot pitää asettaa rivi riviltä — ja joku rivi unohtuu helposti. Konstruktori pakottaa antamaan tarvittavat tiedot heti.

### Parametriton konstruktori

Jos et kirjoita konstruktoria, C# luo tyhjän oletuskonstruktorin. Silloin `new Pizza()` toimii. Kun kirjoitat **oman** konstruktorin parametreilla, oletuskonstruktori katoaa — `new Pizza()` ei enää käänny: **CS1729** (*'Pizza' does not contain a constructor that takes 0 arguments*). Tämä yllättää kaikki kerran, yleensä vanhassa koodissa, joka vielä käyttää `new Pizza()`-kutsua.

Korjaus: muuta kutsut käyttämään uutta konstruktoria, tai lisää parametriton versio takaisin. Konstruktoreita voi kuormittaa kuten metodeja — C# valitsee parametrien perusteella:

```csharp
public Pizza() { }                              // parametriton
public Pizza(string name, decimal price) { ... } // kuormitettu
```

### `this` — tämä olio

Jos parametrin nimi on sama kuin propertyn, `this` erottaa ne:

```csharp
public Pizza(string name, decimal price)
{
    this.Name = name;   // this.Name = olion property
    this.Price = price;
}
```

PascalCase-propertyllä (`Name`) ja camelCase-parametrilla (`name`) `this` ei ole pakollinen, mutta se tekee tarkoituksen näkyväksi.

## Oliot kokoelmassa

Kassan menu on luonteva `List<Pizza>` — ei erillisiä `pizza1`, `pizza2`-muuttujia:

```csharp
List<Pizza> menu = new List<Pizza>
{
    new Pizza("Margherita", 8.50m),
    new Pizza("Pepperoni", 10.00m),
    new Pizza("Vege", 9.50m)
};

foreach (Pizza pizza in menu)
{
    pizza.Describe();
}
```

Uusi pizza = yksi `new` ja `Add`. Sama idea kuin merkkijonotaulukossa, mutta nyt jokaisella alkiolla on **useita tietoja** yhdessä paketissa.

### Olio olion sisällä

Olion property voi olla toinen olio. Kassassa `Receipt` tuntee tilauksensa, ja `Order` tuntee lippunsa:

```csharp
class Order
{
    private List<Ticket> tickets = new List<Ticket>();

    public int CountByCategory(AgeCategory category) { ... }   // laskee listasta
}

class Receipt
{
    public Order Order { get; private set; }
    public decimal Total { get; private set; }
}

int children = receipt.Order.CountByCategory(AgeCategory.Child);
```

Lapsilippujen määrä lasketaan suoraan olioista, kun sitä tarvitaan. Se on luotettavampaa kuin erillinen `categoryCounts`-laskuri, joka pitää muistaa päivittää jokaisessa myyntikohdassa — jos yksi päivitys unohtuu tai tehdään kahdesti, raportti valehtelee hiljaa. Oliossa on vain yksi totuus.

## Vertailu: staattinen metodi vs olion metodi

```csharp
// Staattinen: data parametreina, ei oliota
static decimal GetUnitPrice(int age) { ... }

// Olio: data asuu oliossa
pizza.Price
pizza.Describe()
```

| | Staattinen (`static`) | Olion metodi |
|--|----------------------|--------------|
| Kutsu | `GetUnitPrice(40)` | `pizza.Describe()` |
| Data | Parametreina tai luokan vakioina | Olion omat propertyt |
| Monta kappaletta | Ei — yksi jaettu | Jokainen olio on oma |

`Main` pysyy `static` — se on ohjelman käynnistyspiste, ei "yksi pizza". `ReadInt` on `static` samasta syystä: se ei tarvitse minkään olion tietoja. `Describe()` ei ole `static`, koska se käyttää olion omaa tietoa.

Jos puolet menevät sekaisin, kääntäjä antaa **CS0120** kumpaankin suuntaan:

- `static void Print() { Console.WriteLine(Name); }` luokan sisällä — kenen `Name`? Staattinen metodi ei ole minkään olion sisällä. Korjaus: olio parametrina (`Print(Pizza pizza)` → `pizza.Name`) tai `static` pois.
- `Pizza.Describe();` — olion metodi kutsuttiin luokan nimellä. Piirustus ei osaa esitellä itseään, vain kappale: `pizza.Describe()`.

Lisää: [Staattiset luokat ja metodit](../00-Basics/Static-Classes-and-Methods.md#olion-metodi-vai-staattinen--cs0120).

## Viite vai arvo — olio on osoite

`int`-muuttuja sisältää luvun. Olio-muuttuja sisältää **osoitteen** olioon. Ero näkyy, kun sijoitat muuttujan toiseen:

```csharp
int x = 5;
int y = x;      // y saa kopion luvusta
y = 9;
Console.WriteLine(x);   // 5 — x ei muuttunut

Pizza a = new Pizza("Margherita", 8.50m);
Pizza b = a;    // b saa kopion OSOITTEESTA — sama pizza
b.Name = "Pepperoni";
Console.WriteLine(a.Name);   // Pepperoni — a muuttui, koska a ja b ovat sama olio
```

```
Arvo                              Viite

 x ┌───┐   y ┌───┐                a ┌───┐
   │ 5 │     │ 9 │                  │ ●─┼──┐   ┌──────────────────┐
   └───┘     └───┘                  └───┘  ├──►│ Name = Pepperoni │
  kaksi laatikkoa                 b ┌───┐  │   │ Price = 8.50     │
                                    │ ●─┼──┘   └──────────────────┘
                                    └───┘       yksi olio, kaksi nimeä
```

| Tyyppi | Sijoitus `b = a` | Esimerkkejä |
|--------|------------------|-------------|
| **Arvotyyppi** | Kopioi arvon. `a` ja `b` elävät erikseen | `int`, `decimal`, `double`, `bool`, `char`, enum |
| **Viitetyyppi** | Kopioi osoitteen. `a` ja `b` ovat sama olio | Omat luokat, `List<T>`, taulukot, `Dictionary` |

Uusi olio syntyy **vain** `new`-kutsulla. `Pizza c = new Pizza("Pepperoni", 8.50m)` on eri olio kuin `a`, vaikka arvot ovat samat — ja `a == c` on `false`, koska `==` vertaa olioilla osoitteita, ei sisältöä.

Sama sääntö koskee metodin parametreja: `int` menee metodiin kopiona (muutos ei näy kutsujalle), olio menee viitteenä — `Rename(pizza, "Vege")` muuttaa kutsujan pizzaa ilman `return`-lausetta. Jos metodi sen sijaan kirjoittaa `pizza = new Pizza(...)`, se vaihtaa vain oman parametrinsa osoittamaan uuteen olioon; kutsujan muuttuja ei muutu.

Listassa sama: `Pizza first = menu[0]; first.Price = 9m;` muuttaa listan ensimmäistä pizzaa, koska `first` osoittaa siihen.

`string` on teknisesti viitetyyppi, mutta käyttäytyy kuin arvo: sitä ei voi muuttaa paikallaan, joten `s2 = s1; s2 = "x"` ei koske `s1`-muuttujaan. Alussa voit ajatella `string`-tyypin arvona.

**Microsoft:** [Reference types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/reference-types) · [Value types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/value-types)

## Pieni kokonainen esimerkki

```csharp
class OrderLine
{
    public string Product { get; set; }
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }

    public OrderLine(string product, int quantity, decimal unitPrice)
    {
        Product = product;
        Quantity = quantity;
        UnitPrice = unitPrice;
    }

    public decimal LineTotal()
    {
        return UnitPrice * Quantity;
    }
}

OrderLine line = new OrderLine("Pepperoni", 2, 10.00m);
Console.WriteLine($"{line.Product}: {line.LineTotal():F2} €");
```

## Yleisiä virheitä

| Virhe | Mitä tapahtuu | Korjaus |
|-------|---------------|---------|
| `Movie m; m.Title = "x";` | `m` on `null` → **NullReferenceException** ajossa (tai CS0165 käännöksessä, jos arvoa ei annettu lainkaan) | `Movie m = new Movie(...);` |
| `if (a == b)` kahdella oliolla | Vertaa osoitteita, ei sisältöä — kaksi samannimistä elokuvaa ovat eri olioita | Vertaa propertyjä: `a.Title == b.Title` |
| `movie = new Movie(...)` metodin sisällä | Vaihtaa vain parametrin osoittamaan uuteen olioon; kutsujan muuttuja ei muutu | Muuta propertyjä (`movie.Title = ...`) tai palauta uusi olio `return`-lauseella |
| `new Movie()` ei käänny (**CS1729**) | Oma konstruktori poisti oletuskonstruktorin | Käytä uutta konstruktoria tai lisää `public Movie() { }` |
| `Movie.Describe()` tai `Title` staattisessa metodissa (**CS0120**) | Olion jäsen ilman oliota | Kutsu oliolla, tai anna olio parametrina |

## Yhteenveto

- Luokka = tyyppi omassa tiedostossaan, olio = `new`-kutsulla luotu kappale. Ilman `new`-sanaa muuttuja on `null`
- Propertyt pitävät olion tiedot; konstruktori asettaa ne syntyessä
- Samaa luokkaa voi olla monta oliota listassa
- Olion metodi näkee olion omat arvot — parametreja tarvitaan vähemmän. CS0120 kertoo, että staattinen ja oliopuoli menivät sekaisin
- Olio-muuttuja on osoite: `b = a` ei kopioi oliota, uusi olio syntyy vain `new`-kutsulla
- Olio voi sisältää olion (`receipt.Order`): tieto lasketaan olioista, ei erillisestä laskurista

Seuraavaksi: [Properties](../00-Basics/Properties.md) · [Kapselointi](Encapsulation.md) · [Perintä](Inheritance.md)

## Hyödyllisiä linkkejä

- [Microsoft: Classes](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/types/classes) — luokka, olio, `new`
- [Microsoft: Object-oriented programming tutorial](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/oop) — pankkitili-esimerkki alusta loppuun
- [Microsoft: Constructors](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/constructors)
- [Microsoft: Properties](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties)
- [Microsoft: Reference types vs value types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/reference-types)
