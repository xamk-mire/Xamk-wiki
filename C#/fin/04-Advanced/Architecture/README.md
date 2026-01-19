# Ohjelmistoarkkitehtuuri

Tervetuloa ohjelmistoarkkitehtuurin maailmaan! Tämä osio käsittelee eri arkkitehtuurimalleja, niiden soveltamista ja parhaita käytäntöjä.

## Mikä on ohjelmistoarkkitehtuuri?

Ohjelmistoarkkitehtuuri määrittelee sovelluksen rakenteen, komponenttien väliset suhteet ja periaatteet, joiden mukaan sovellus rakennetaan. Hyvä arkkitehtuuri tekee koodista:

- ✅ **Ylläpidettävän** - Helppo ymmärtää ja muokata
- ✅ **Testattavan** - Komponentit voidaan testata erikseen
- ✅ **Laajennettavan** - Uusia ominaisuuksia voi lisätä helposti
- ✅ **Riippumattoman** - Teknologian vaihto on mahdollista

## Arkkitehtuurimallit

### Perusarkkitehtuurit

1. **[Layered Architecture](Layered-Architecture.md)** (Kerrosarkkitehtuuri)
   - Yksinkertainen ja yleinen malli
   - Sovellus jaetaan kerroksiin (UI, Business Logic, Data Access)
   - Sopii: Pienet ja keskisuuret CRUD-sovellukset

2. **[Clean Architecture](Clean-Architecture.md)**
   - Domain-keskinen arkkitehtuuri
   - Riippuvuudet osoittavat sisäänpäin
   - Sopii: Keskisuuret ja suuret sovellukset, jotka vaativat testattavuutta

3. **[Hexagonal Architecture](Hexagonal-Architecture.md)** (Ports and Adapters)
   - Portit ja adapterit -malli
   - Sovelluksen ydin eristettynä
   - Sopii: Integraatiorikkaat sovellukset

4. **[Onion Architecture](Onion-Architecture.md)**
   - Sipulikerrokset domain-mallin ympärillä
   - Domain Services vs. Application Services
   - Sopii: Domain-Driven Design (DDD) projektit

### Skaalautuvat arkkitehtuurit

5. **[Microservices Architecture](Microservices-Architecture.md)**
   - Pienet, itsenäiset palvelut
   - Jokainen palvelu omalla tietokannalla
   - Sopii: Suuret organisaatiot, korkea skaalautuvuus

6. **[CQRS](CQRS.md)** (Command Query Responsibility Segregation)
   - Lukeminen ja kirjoittaminen erotettu
   - Optimoitu suorituskyky
   - Sopii: Suorituskykykriittiset sovellukset

7. **[Event-Driven Architecture](Event-Driven-Architecture.md)**
   - Event:eihin perustuva kommunikaatio
   - Löyhä kytkös komponenttien välillä
   - Sopii: Real-time sovellukset, mikropalvelut

### UI-arkkitehtuurit

8. **[MVC ja MVVM](MVC-MVVM.md)**
   - MVC: Model-View-Controller (ASP.NET Core)
   - MVVM: Model-View-ViewModel (WPF, MAUI)
   - Sopii: Web- ja desktop-sovellukset

## Arkkitehtuurien vertailu

| Arkkitehtuuri | Kompleksisuus | Testattavuus | Skaalautuvuus | Sopii... |
|---------------|---------------|--------------|---------------|----------|
| **Layered** | ⭐⭐ | ⭐⭐ | ⭐⭐ | Pienet projektit, CRUD |
| **Clean** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Keskisuuret-suuret projektit |
| **Hexagonal** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Integraatiorikkaat projektit |
| **Onion** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | DDD-projektit |
| **Microservices** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Suuret organisaatiot |
| **CQRS** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Suorituskykykriittiset |
| **Event-Driven** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Real-time, integraatiot |

## Oppimisjärjestys

Suosittelemme opiskelua seuraavassa järjestyksessä:

1. **Layered Architecture** - Aloita yksinkertaisesta
2. **Clean Architecture** - Ymmärrä riippuvuuksien suunta
3. **Hexagonal Architecture** - Opettele portit ja adapterit
4. **CQRS** - Erottele lukeminen ja kirjoittaminen
5. **Event-Driven** - Asynkroninen kommunikaatio
6. **Microservices** - Hajautetut järjestelmät

## Valitse arkkitehtuuri projektin mukaan

### Pieni projekti (1-3 kehittäjää, < 6kk)
→ **Layered Architecture** tai yksinkertainen **Clean Architecture**

### Keskisuuri projekti (3-10 kehittäjää, 6kk-2v)
→ **Clean Architecture** tai **Hexagonal Architecture**

### Suuri projekti (10+ kehittäjää, 2v+)
→ **Clean Architecture** + **CQRS** tai **Microservices**

### Kompleksinen domain
→ **Clean/Onion Architecture** + Domain-Driven Design

### Korkea suorituskyky
→ **CQRS** + Event Sourcing

### Integraatiorikkaat järjestelmät
→ **Hexagonal Architecture** tai **Event-Driven Architecture**

## Yleiset periaatteet

### 1. Dependency Inversion Principle

Liiketoimintalogiikka ei saa riippua infrastruktuurista:

```csharp
// ❌ Huono
public class OrderService
{
    private SqlServerRepository _repository = new SqlServerRepository();
}

// ✅ Hyvä
public class OrderService
{
    private IOrderRepository _repository;
    
    public OrderService(IOrderRepository repository)
    {
        _repository = repository;
    }
}
```

### 2. Separation of Concerns

Jokainen komponentti vastaa yhdestä asiasta:

- **UI** - Käyttöliittymä ja käyttäjän vuorovaikutus
- **Business Logic** - Liiketoimintasäännöt ja logiikka
- **Data Access** - Tietokannan käsittely
- **Infrastructure** - Ulkoiset palvelut ja teknologia

### 3. Testattavuus

Hyvä arkkitehtuuri mahdollistaa yksikkötestauksen:

```csharp
[Fact]
public async Task CreateOrder_ValidOrder_ReturnsOrderId()
{
    // Arrange - Mock riippuvuudet
    Mock<IOrderRepository> mockRepo = new Mock<IOrderRepository>();
    mockRepo.Setup(r => r.AddAsync(It.IsAny<Order>())).ReturnsAsync(1);
    
    OrderService service = new OrderService(mockRepo.Object);
    
    // Act
    int orderId = await service.CreateOrderAsync(new Order());
    
    // Assert
    Assert.Equal(1, orderId);
}
```

### 4. Aloita yksinkertaisesta

**Älä ylisuunnittele!**

- Aloita yksinkertaisesta arkkitehtuurista
- Refaktoroi monimutkaisempaan kun tarve tulee
- Älä käytä Microservices:ia 3 hengen tiimissä
- Älä käytä Clean Architecture:a TODO-listassa

**Muista:** "Make it work, make it right, make it fast" - Kent Beck

## Hyödyllisiä linkkejä

### Dokumentaatio
- [Microsoft: Architectural patterns](https://learn.microsoft.com/en-us/azure/architecture/patterns/)
- [Microsoft: .NET Architecture Guides](https://learn.microsoft.com/en-us/dotnet/architecture/)
- [Martin Fowler: Software Architecture Guide](https://martinfowler.com/architecture/)

### Kirjat
- Clean Architecture by Robert C. Martin
- Patterns of Enterprise Application Architecture by Martin Fowler
- Domain-Driven Design by Eric Evans
- Building Microservices by Sam Newman

### Blogit
- [The Clean Architecture Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Martin Fowler's Blog](https://martinfowler.com/)

## Seuraavaksi

Kun olet tutustunut arkkitehtuureihin, voit syventää tietämystäsi:

- [Suunnitteluperiaatteet](../Design-Principles.md) - SOLID, DRY, KISS
- [Suunnittelumallit](../Design-Patterns.md) - Singleton, Factory, Observer, jne.
- [Yksikkötestaus](../Unit-Testing.md) - Testaa arkkitehtuuria

---

**Muista:** Arkkitehtuuri on väline, ei tavoite. Valitse projektin tarpeisiin sopiva malli!
