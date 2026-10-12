# Luokat, oliot ja konstruktorit

Staattisista metodeista siirrytään **olioihin**: data ja sen käsittely kootaan yhteen tyyppiin. Tämä sivu on se ensimmäinen askel — kapselointi ja perintä tulevat seuraavaksi.

Taustateoria: [Mitä on OOP?](What-is-OOP.md) · Propertyt: [Properties](../00-Basics/Properties.md)

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

Jos et kirjoita konstruktoria, C# luo tyhjän oletuskonstruktorin. Silloin `new Pizza()` toimii. Kun kirjoitat **oman** konstruktorin parametreilla, oletuskonstruktori katoaa — `new Pizza()` ei enää käänny, ellei lisää myös parametritonta versiota (kuormitus).

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

`Main` pysyy `static` — se on ohjelman käynnistyspiste, ei "yksi pizza".

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

## Yhteenveto

- Luokka = tyyppi, olio = `new`-kutsulla luotu kappale
- Propertyt pitävät olion tiedot; konstruktori asettaa ne syntyessä
- Samaa luokkaa voi olla monta oliota listassa
- Olion metodi näkee olion omat arvot — parametreja tarvitaan vähemmän

Seuraavaksi: [Properties](../00-Basics/Properties.md) · [Kapselointi](Encapsulation.md) · [Perintä](Inheritance.md)
