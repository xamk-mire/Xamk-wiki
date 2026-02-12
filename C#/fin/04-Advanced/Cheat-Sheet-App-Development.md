# C# Sovellusrakentamisen Cheat Sheet — Milloin mitäkin tekniikkaa?

Tämä on käytännön pikaopas: kun rakennat C#-konsolisovellusta, katso tästä mikä tekniikka sopii mihinkin tilanteeseen.

---

## Päätöspuu: "Miten mallinnan tämän datan?"

```
Tarvitsetko datan säilyttämistä ja logiikkaa?
│
├── KYLLÄ → class
│   │
│   ├── Tarvitaanko validointia (esim. hinta ei saa olla negatiivinen)?
│   │   └── Property + private set + validointi konstruktorissa tai setterissä
│   │
│   ├── Onko kyseessä vain dataa ilman logiikkaa (DTO, siirto-olio)?
│   │   └── record tai class pelkillä auto-propertyillä
│   │
│   └── Onko arvoja rajattu joukko (esim. tila, tyyppi, rooli)?
│       └── enum
│
└── EI → Onko kyseessä operaatioita / toimintoja?
    │
    ├── KYLLÄ → Service-luokka (esim. PricingService, ReservationService)
    │
    └── EI → Ei tarvitse omaa luokkaa
```

---

## Päätöspuu: "Milloin interface, milloin abstract class?"

```
Tarvitseeko useampi luokka toteuttaa sama sopimus?
│
├── KYLLÄ
│   │
│   ├── Onko yhteistä koodia jota jaetaan?
│   │   └── abstract class (yhteinen pohja + pakolliset abstract-metodit)
│   │
│   └── Ei yhteistä koodia, vain sama rajapinta?
│       └── interface
│           Hyöty: mockattavissa testeissä, löyhä kytkentä
│
└── EI → Ei tarvita interfacea tai abstraktia luokkaa
    └── Konkreettinen luokka riittää
```

**Nyrkkisääntö:** Jos haluat testata service-luokan ilman sen riippuvuuksia → tee riippuvuuksille interface.

---

## Päätöspuu: "Miten järjestän koodin?"

```
Mitä koodi tekee?
│
├── Käyttäjän kanssa kommunikointi (valikot, syötteet, tulosteet)?
│   └── UI-kerros (Program.cs tai omat UI-luokat)
│       Ei business-logiikkaa tänne!
│
├── Sääntöjä ja laskentaa (validointi, hinnoittelu, päällekkäisyyksien tarkistus)?
│   └── Service-kerros (esim. ReservationService, PricingService)
│       Tänne kaikki business-logiikka.
│
├── Datan tallentaminen ja lataaminen?
│   └── Repository/DataStore-kerros (esim. JsonRepository, FileDataStore)
│       Vain tallennus ja haku, ei logiikkaa.
│
└── Datan rakenne (mitä tietoja olio sisältää)?
    └── Model-kerros (esim. Room, Guest, Reservation)
        Propertyja, validointia, ei muuta.
```

```
Tyypillinen kerrosrakenne:

  UI (Program.cs)
       │
       ▼
  Service (business-logiikka)
       │
       ▼
  Repository (datan tallennus/lataus)
       │
       ▼
  Models (datarakenteet)
```

---

## Päätöspuu: "Miten tallennan dataa pysyvästi?"

```
Käytätkö tietokantaa?
│
├── KYLLÄ → Entity Framework Core / Dapper
│
└── EI → Tiedostopohjainen tallennus
    │
    ├── Pitääkö datan olla ihmisen luettavissa?
    │   └── JSON (System.Text.Json)
    │
    └── Ei tarvitse olla luettavissa?
        └── JSON silti usein yksinkertaisin vaihtoehto
```

### JSON tallennus/lataus

```csharp
// Tallentaminen
var options = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(data, options);
await File.WriteAllTextAsync("data.json", json);

// Lataaminen
string json = await File.ReadAllTextAsync("data.json");
var data = JsonSerializer.Deserialize<List<MyModel>>(json);
```

### Milloin async tiedosto-operaatioissa?

```
Luetko/kirjoitatko tiedostoa?
│
├── KYLLÄ → Käytä async-versioita (ReadAllTextAsync, WriteAllTextAsync)
│           Vapauttaa säikeen odotuksen ajaksi
│
└── EI → Ei tarvita asyncia
```

---

## LINQ pikavalintataulu: "Mitä LINQ-metodia käytän?"

| Haluan... | LINQ-metodi | Esimerkki |
|-----------|-------------|-----------|
| Suodattaa listan | `.Where()` | `items.Where(x => x.IsActive)` |
| Muuntaa listan toiseen muotoon | `.Select()` | `items.Select(x => x.Name)` |
| Järjestää | `.OrderBy()` / `.OrderByDescending()` | `items.OrderBy(x => x.Price)` |
| Etsiä yhden | `.FirstOrDefault()` | `items.FirstOrDefault(x => x.Id == id)` |
| Tarkistaa onko yhtään | `.Any()` | `items.Any(x => x.Status == "Active")` |
| Tarkistaa täyttävätkö kaikki ehdon | `.All()` | `items.All(x => x.Price > 0)` |
| Laskea lukumäärä | `.Count()` | `items.Count(x => x.Type == "Suite")` |
| Laskea summa | `.Sum()` | `items.Sum(x => x.TotalPrice)` |
| Laskea keskiarvo | `.Average()` | `items.Average(x => x.Rating)` |
| Ryhmitellä | `.GroupBy()` | `items.GroupBy(x => x.Type)` |
| Yhdistää kaksi listaa | `.Join()` | Kaksi listaa yhteisen avaimen perusteella |
| Tarkistaa onko päällekkäisyyksiä | `.Any()` + ehto | `existing.Any(x => x.Start < end && x.End > start)` |
| Ottaa N ensimmäistä | `.Take(n)` | `items.Take(10)` |
| Ohittaa N ensimmäistä | `.Skip(n)` | `items.Skip(20).Take(10)` |

### Ketjutus

LINQ-metodeja voi ketjuttaa:

```csharp
var results = items
    .Where(x => x.IsActive)
    .OrderBy(x => x.Name)
    .Select(x => new { x.Name, x.Price })
    .ToList();
```

---

## Validointi: "Mihin validointi kuuluu?"

```
Missä kerroksessa validoin?
│
├── Model-kerros: Datan eheys
│   └── "Hinta ei voi olla negatiivinen", "Nimi ei voi olla tyhjä"
│   └── Toteutus: konstruktori tai property setter heittää ArgumentException
│
├── Service-kerros: Business-säännöt
│   └── "Päällekkäisiä varauksia ei saa olla", "Budjetti ei saa ylittyä"
│   └── Toteutus: metodi tarkistaa ja heittää InvalidOperationException
│
└── UI-kerros: Syötteen muoto
    └── "Onko päivämäärä oikeassa muodossa?", "Onko kenttä tyhjä?"
    └── Toteutus: tarkista ennen servicen kutsumista
```

---

## Yksikkötestaus: "Mitä testaan ja miten?"

```
Mitä testaat?
│
├── Business-logiikkaa (service)?
│   │
│   ├── Onko riippuvuuksia muihin luokkiin?
│   │   └── KYLLÄ → Mockaa riippuvuudet (Moq)
│   │       Edellytys: riippuvuudet ovat interfaceja
│   │
│   └── Ei riippuvuuksia?
│       └── Testaa suoraan: new MyService() + kutsu + Assert
│
├── Mallin validointia?
│   └── Testaa: oikeat arvot → olio luodaan, väärät → poikkeus
│
└── UI-logiikkaa / Program.cs?
    └── ÄLÄ testaa UI:ta yksikkötesteillä.
        Testaa vain business-logiikka servicen kautta.
```

### Testien nimeäminen

```
MetodinNimi_Tilanne_OdotettuTulos

Esim:
  CalculatePrice_ThreeNights_ReturnsCorrectTotal
  CreateReservation_OverlappingDates_ThrowsException
  FindByEmail_NonExistent_ReturnsNull
```

### Testirakenne (AAA)

```csharp
[Fact]
public void MetodinNimi_Tilanne_OdotettuTulos()
{
    // Arrange - valmistele
    var mock = new Mock<IRepository>();
    mock.Setup(x => x.GetAll()).Returns(testData);
    var service = new MyService(mock.Object);

    // Act - suorita
    var result = service.Calculate(input);

    // Assert - varmista
    Assert.Equal(expected, result);
}
```

### Milloin Fact, milloin Theory?

| Tilanne | Käytä | Esimerkki |
|---------|-------|-----------|
| Yksi skenaario | `[Fact]` | "Peruutus toimii" |
| Sama logiikka, eri arvot | `[Theory]` + `[InlineData]` | "Hinta lasketaan oikein 1, 3, 7 yölle" |

```csharp
[Theory]
[InlineData(1, 89)]
[InlineData(3, 267)]
[InlineData(7, 623)]
public void CalculatePrice_DifferentNights_ReturnsCorrectTotal(int nights, decimal expected)
{
    // ...
}
```

---

## Dependency Injection: "Miksi ja miten?"

```
Luokka A käyttää luokkaa B.
│
├── A luo B:n itse: new B()
│   └── ONGELMA: A:ta ei voi testata ilman oikeaa B:tä
│
└── A saa B:n konstruktorissa: A(IB b)
    └── RATKAISU: Testissä voi antaa mock-B:n, tuotannossa oikean B:n
```

```csharp
// HUONO — tight coupling
public class OrderService
{
    private DatabaseRepository _repo = new DatabaseRepository();
}

// HYVÄ — löyhä kytkentä
public class OrderService
{
    private readonly IRepository _repo;

    public OrderService(IRepository repo)
    {
        _repo = repo;
    }
}
```

---

## Poikkeusten käsittely: "Mitä poikkeuksia heitän?"

| Tilanne | Poikkeus | Esimerkki |
|---------|----------|-----------|
| Virheellinen parametri | `ArgumentException` | Tyhjä nimi, negatiivinen hinta |
| Null-parametri | `ArgumentNullException` | `email` on null |
| Arvo alueen ulkopuolella | `ArgumentOutOfRangeException` | Määrä on -1 |
| Business-sääntö estää operaation | `InvalidOperationException` | Päällekkäinen varaus, suljettu projekti |
| Dataa ei löydy | Palauta `null` tai heitä `KeyNotFoundException` | ID:llä ei löydy |

```csharp
// Validointi servicessä
public Reservation Create(int roomId, DateTime start, DateTime end)
{
    if (end <= start)
        throw new ArgumentException("Lopun pitää olla alun jälkeen.");

    if (HasOverlap(roomId, start, end))
        throw new InvalidOperationException("Päällekkäinen varaus.");

    // ... luo varaus
}
```

---

## Pikavalintataulu: koko sovelluksen rakentaminen

| Vaihe | Mitä tehdään | Tekniikka |
|-------|-------------|-----------|
| 1. Mallit | Luo dataluokat propertyillä ja validoinnilla | `class`, `enum`, encapsulation |
| 2. Rajapinnat | Määrittele sopimukset palveluille | `interface` |
| 3. Repository | Toteuta datan tallennus ja lataus | `System.Text.Json`, `async/await`, `File.ReadAllTextAsync` |
| 4. Palvelut | Toteuta business-logiikka | Service-luokat, LINQ, DI konstruktorissa |
| 5. UI | Rakenna käyttöliittymä joka kutsuu palveluita | `Console.ReadLine`, `Console.WriteLine` |
| 6. Testit | Testaa palveluiden logiikka | xUnit, Moq, `[Fact]`, `[Theory]` |

---

## 10 kultaista sääntöä

1. **UI ei sisällä logiikkaa** — UI lukee syötteitä ja näyttää tuloksia, service päättää mitä tapahtuu.
2. **Service ei tiedä UI:sta** — Service palauttaa dataa, ei tulosta konsoliin.
3. **Validoi kahdessa paikassa** — Model varmistaa datan eheyden, service varmistaa business-säännöt.
4. **Interface riippuvuuksille** — Jos luokka A käyttää luokkaa B, anna A:lle `IB` eikä `B`.
5. **Yksi vastuu per luokka** — `PricingService` laskee hintoja, `ReservationService` hallitsee varauksia.
6. **LINQ ennen foreach** — Jos suodatat, järjestät tai ryhmittelet, käytä LINQ:ia.
7. **Async tiedostoille** — `File.ReadAllTextAsync` / `WriteAllTextAsync`, ei synkronisia versioita.
8. **Testaa logiikkaa, älä UI:ta** — Testaa servicet suoraan, mockaa riippuvuudet.
9. **Nimeä selkeästi** — `SearchAvailableRooms`, ei `GetRooms2` tai `DoStuff`.
10. **Heitä poikkeus väärälle syötteelle** — `ArgumentException` virheelliselle datalle, `InvalidOperationException` business-sääntörikkomukselle.
