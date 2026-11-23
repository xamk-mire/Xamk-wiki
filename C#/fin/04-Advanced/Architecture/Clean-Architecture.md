# Clean Architecture

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on Clean Architecture?](#mikä-on-clean-architecture)
3. [Kerrokset](#kerrokset)
   - [Kehien nimet ja .NET-projektit](#kehien-nimet-ja-net-projektit)
4. [Dependency Rule](#dependency-rule)
   - [Projektiviittaukset: kääntäjä valvoo Dependency Rulea](#projektiviittaukset-kääntäjä-valvoo-dependency-rulea)
   - [Composition root](#composition-root)
   - [Miksi rajapinta on Domainissa ja toteutus Infrastructuressa](#miksi-rajapinta-on-domainissa-ja-toteutus-infrastructuressa)
5. [Edut ja haitat](#edut-ja-haitat)
6. [Milloin käyttää?](#milloin-käyttää)
7. [Käytännön esimerkki](#käytännön-esimerkki)
8. [Parhaat käytännöt](#parhaat-käytännöt)
9. [Yhteenveto](#yhteenveto)

---

## Johdanto

Clean Architecture on Robert C. Martinin (Uncle Bob) luoma arkkitehtuurimalli, joka korostaa **riippumattomuutta** ja **testattavuutta**. Se on yksi suosituimmista arkkitehtuurimalleista modernissa ohjelmistokehityksessä.

### Keskeiset periaatteet

1. **Domain on keskiössä** - Liiketoimintalogiikka on tärkein
2. **Riippuvuudet osoittavat sisäänpäin** - Ulkokerrokset riippuvat sisäkerroksista
3. **Teknologiariippumattomuus** - Voit vaihtaa tietokannan, UI:n tai frameworkin
4. **Testattavuus** - Ydin on testattavissa ilman ulkoisia riippuvuuksia

---

## Mikä on Clean Architecture?

Clean Architecture on kehämalli, jossa sovellus jaetaan **konsentrisiin kehiin**. Mitä sisempänä kehä on, sitä tärkeämpi se on liiketoiminnalle.

### Rakenne

```
┌───────────────────────────────────────┐
│  Infrastructure & Frameworks          │ ← UI, Database, External APIs
│  ┌─────────────────────────────────┐  │
│  │  Interface Adapters             │  │ ← Controllers, Presenters, Gateways
│  │  ┌───────────────────────────┐  │  │
│  │  │  Application Business      │  │  │ ← Use Cases
│  │  │  Rules                     │  │  │
│  │  │  ┌─────────────────────┐  │  │  │
│  │  │  │  Enterprise         │  │  │  │ ← Entities (Domain)
│  │  │  │  Business Rules     │  │  │  │
│  │  │  └─────────────────────┘  │  │  │
│  │  └───────────────────────────┘  │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘

Riippuvuudet: ← ← ← ← ← (Sisäänpäin)
```

---

## Kerrokset

### Kerrosten vastuualueet - Ytimekäs yhteenveto

| Layer | Vastaa kysymykseen |
|-------|-------------------|
| **Entities (Domain)** | Mitkä ovat säännöt ja käsitteet? |
| **Use Cases (Application)** | Mitä sovellus tekee? |
| **Interface Adapters** | Miten data muunnetaan? |
| **Infrastructure** | Miten tämä on teknisesti toteutettu? |

### Kehien nimet ja .NET-projektit

Alkuperäinen malli nimeää kehät yleisillä nimillä. .NET-ratkaisussa kehät ovat yleensä neljä projektia, joilla on omat vakiintuneet nimensä. Sama asia on siis kahdella nimellä:

| Kehä (alkuperäinen nimi) | .NET-projekti | Vastuu yhdellä lauseella |
|---|---|---|
| **Entities** | `Domain` | Entiteetit, value objectit ja säännöt, sekä repositoryjen rajapinnat. |
| **Use Cases** | `Application` | Käyttötapaukset: hae olio, kutsu sen metodia, tallenna. Myös lukumallit (read model) eli näkymät, jotka lasketaan datasta. |
| **Interface Adapters** | `API` (tai `Web`) | Controllerit: muuntavat HTTP-pyynnön käyttötapauksen kutsuksi ja tuloksen statuskoodiksi. |
| **Frameworks & Drivers** | `Infrastructure` | EF Core, tietokanta ja repositoryjen toteutukset. |

Kaksi tarkennusta:

- ASP.NET Core on itsekin framework, joten `API`-projekti kuuluu osittain myös uloimpaan kehään. Käytännössä `API` ja `Infrastructure` ovat molemmat ulkokehällä: toinen on sovelluksen sisääntulo, toinen sen tallennus.
- `API`-projektissa on myös **composition root** eli kohta, jossa rajapinnat kytketään toteutuksiin. Se selitetään kohdassa [Composition root](#composition-root).

Tämän sivun esimerkissä projektit ovat `OrderManagement.Domain`, `.Application`, `.Infrastructure` ja `.Web`.

### Yksityiskohtainen vastuunjako

#### 1. Entities / Domain Layer (Sisimmäinen kehä)

**Kysymys: Mitkä säännöt ja käsitteet tässä liiketoiminnassa ovat?**

**Vastaa esimerkiksi:**
- Mitä tarkoittaa "tilaus", "käyttäjä", "tuote", "lasku"
- Mitkä säännöt ovat aina totta
- Mikä on sallittua ja mikä ei
- Mitä liiketoiminnan invariantit ovat (esim. "saldo ei voi olla negatiivinen")

**Ei vastaa:**
- HTTP:stä tai API:sta
- Tietokannasta tai SQL:stä
- Frameworkeista
- Miten käyttöliittymä toimii
- Miten data tallennetaan

**Tyypillinen sisältö:**
- Domain-oliot (Entities)
- Value Objects
- Liiketoimintasäännöt
- Domain-logiikka
- Rajapinnat repositoryille (määritellään täällä!)

**Ei riippuvuuksia mihinkään!** - Tärkein kerros, puhtain koodi.

---

#### 2. Use Cases / Application Layer

**Kysymys: Mitä sovellus tekee käyttäjän pyynnölle?**

**Vastaa esimerkiksi:**
- Mitä tapahtuu, kun käyttäjä "luo tilauksen"
- Missä järjestyksessä asioita tehdään
- Mitä useita domain-olioita tarvitaan yhden toiminnon suorittamiseen
- Miten työnkulut (workflows) toteutetaan
- Miten transaktiot hallitaan

**Ei vastaa:**
- Miten data fyysisesti tallennetaan
- Miten käyttöliittymä näyttää asiat
- HTTP-protokollan yksityiskohdista
- Tietokantateknologiasta

**Tyypillinen sisältö:**
- Use Case -luokat (yksi per käyttötapaus)
- Application services
- DTO:t (Data Transfer Objects)
- Kutsut repositoryihin (rajapintojen kautta)
- Orkestrointi logiikka

**Riippuu vain:** Domain Layer:stä

---

#### 3. Interface Adapters

**Kysymys: Miten data muunnetaan eri muotojen välillä?**

**Vastaa esimerkiksi:**
- HTTP Request → DTO → Domain Entity
- Domain Entity → DTO → HTTP Response
- Miten ulkoinen API kommunikoi sisäisten Use Case:jen kanssa
- Miten UI saa dataa muodossa jota se ymmärtää

**Ei vastaa:**
- Mitä liiketoimintasäännöt ovat (se on Domain)
- Miten työnkulku toimii (se on Use Cases)
- Konkreettisesta tietokantateknologiasta (se on Infrastructure)

**Tyypillinen sisältö:**
- Controllers (API endpoints)
- Presenters
- View Models
- API Request/Response -mallit
- Muunnokset (Mappers)

**Riippuu:** Use Cases Layer:stä

---

#### 4. Frameworks & Drivers / Infrastructure

**Kysymys: Miten sovellus on kytketty ulkomaailmaan?**

**Vastaa esimerkiksi:**
- Miten data tallennetaan tietokantaan (EF Core, SQL)
- Miten lähetetään sähköposti (SMTP, SendGrid)
- Miten kutsutaan ulkoista APIa
- Miten lokitus toimii
- Miten tiedostoja käsitellään

**Ei vastaa:**
- Milloin jotain tehdään (se on Use Cases)
- Miksi jokin sääntö on olemassa (se on Domain)
- Mitä liiketoimintalogiikkaa suoritetaan

**Tyypillinen sisältö:**
- Repository-toteutukset (IOrderRepository → OrderRepository)
- Database Context (EF Core)
- External API -klientit
- File system, cache (Redis), cloud services (Azure)
- Email services, logging frameworks

**Riippuu:** Kaikista sisemmistä kerroksista (rajapintojen kautta)

---

### Riippuvuussuunta (Dependency Rule)

```
Infrastructure → Interface Adapters → Use Cases → Domain
     ✅               ✅                 ✅
     ❌ ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

**Tärkeää:** 
- Ulommat kerrokset tuntevat sisemmät kerrokset
- Sisemmät kerrokset EIVÄT tunne ulompia kerroksia
- Domain on täysin riippumaton kaikesta
- Riippuvuudet käännetään rajapintojen avulla (Dependency Inversion)

---

### 1. Entities (Domain Layer) - Sisimmäinen kehä

**Vastuu:** Liiketoiminnan ydinlogiikka

**Sisältää:**
- Domain-mallit (entities)
- Business rules
- Domain-logiikka
- Value objects

**Ei riippuvuuksia mihinkään!**

```csharp
public class Order
{
    private readonly List<OrderItem> _items = new();

    public int Id { get; private set; }
    public IReadOnlyList<OrderItem> Items => _items;
    public OrderStatus Status { get; private set; } = OrderStatus.Pending;
    
    // Domain logic
    public decimal GetTotal()
    {
        return Items.Sum(item => item.Price * item.Quantity);
    }
    
    public void Confirm()
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException("Tilaus on jo vahvistettu");
        
        if (Items.Count == 0)
            throw new InvalidOperationException("Tilauksessa ei ole tuotteita");
        
        Status = OrderStatus.Confirmed;
    }
}
```

Setterit ovat `private`. Tilaa voi muuttaa vain olion omilla metodeilla, ja ne tarkistavat säännöt. Tätä kutsutaan rikkaaksi malliksi. Katso [Aneeminen ja rikas malli](Domain-Driven-Design.md#aneeminen-ja-rikas-malli).

### 2. Use Cases (Application Layer)

**Vastuu:** Sovelluksen käyttötapaukset

**Sisältää:**
- Use case -luokat
- Application-logiikka
- Orkestrointi (coordinating): hae olio, kutsu sen metodia, tallenna
- DTO:t ja lukumallit

Use case käyttää repositoryja rajapintojen kautta. Rajapinnat on määritelty Domain-kerroksessa.

**Riippuu vain Domain Layer:stä**

```csharp
public class CreateOrderUseCase
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;
    
    public async Task<OrderResponseDto> ExecuteAsync(CreateOrderDto dto)
    {
        // Use case logic
        Order order = new Order(dto.CustomerName);
        
        // Validate and add items
        foreach (var itemDto in dto.Items)
        {
            Product product = await _productRepository.GetByIdAsync(itemDto.ProductId);
            order.AddItem(new OrderItem { ... });
        }
        
        // Save
        await _orderRepository.AddAsync(order);
        
        return new OrderResponseDto { ... };
    }
}
```

### 3. Interface Adapters

**Vastuu:** Muuntaa dataa eri muotoihin

**Sisältää:**
- Controllers
- Presenters
- Gateways
- DTO:t (Data Transfer Objects)

**Riippuu Use Case Layer:stä**

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrderController : ControllerBase
{
    private readonly CreateOrderUseCase _createOrderUseCase;
    
    [HttpPost]
    public async Task<ActionResult<OrderResponseDto>> CreateOrder([FromBody] CreateOrderDto dto)
    {
        OrderResponseDto order = await _createOrderUseCase.ExecuteAsync(dto);
        return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order);
    }
}
```

### 4. Frameworks & Drivers (Infrastructure)

**Vastuu:** Ulkoiset työkalut ja teknologia

**Sisältää:**
- Database (Entity Framework)
- UI Frameworks (ASP.NET Core)
- External APIs
- Logging, Email, jne.

**Riippuu kaikista sisemmistä kerroksista**

```csharp
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public async Task<Order> GetByIdAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id);
    }
}
```

---

## Dependency Rule

**Tärkein sääntö:** Riippuvuudet osoittavat AINA sisäänpäin.

```
Infrastructure → Interface Adapters → Use Cases → Entities
    ✅              ✅                  ✅
    ❌ ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

### Miten tämä toteutetaan?

**Dependency Inversion Principle:**

```csharp
// ❌ Huono: Use Case riippuu Infrastructure:sta
public class CreateOrderUseCase
{
    private OrderRepository _repository = new OrderRepository(); // Konkreettinen riippuvuus
}

// ✅ Hyvä: Use Case riippuu rajapinnasta (sisäkerros määrittelee)
public class CreateOrderUseCase
{
    private readonly IOrderRepository _repository; // Rajapinta
    
    public CreateOrderUseCase(IOrderRepository repository)
    {
        _repository = repository;
    }
}

// Infrastructure toteuttaa rajapinnan
public class OrderRepository : IOrderRepository { ... }
```

### Projektiviittaukset: kääntäjä valvoo Dependency Rulea

Clean Architecturessa kerrokset ovat **erillisiä projekteja**, eivät kansioita. Projekti voi käyttää toisen projektin luokkia vain, jos sillä on **projektiviittaus** (project reference) siihen. Viittaukset tehdään näin:

```
API ────────────► Application ────► Domain
 │                                    ▲
 └──► Infrastructure ─────────────────┘
      (Infrastructure viittaa myös Applicationiin, jos se tarvitsee sen tyyppejä)
```

| Projekti | Viittaa projekteihin |
|---|---|
| `Domain` | Ei mihinkään |
| `Application` | `Domain` |
| `Infrastructure` | `Domain` (ja tarvittaessa `Application`) |
| `API` | `Application` ja `Infrastructure` |

**Mitä tästä seuraa:** `Domain`-projektilla ei ole viittausta `Infrastructure`-projektiin. Jos joku kirjoittaa entiteettiin `using OrderManagement.Infrastructure;`, koodi **ei käänny**. Virhe näkyy heti, ei vasta koodikatselmuksessa. Sama koskee `Application`-projektia: use case ei voi käyttää `DbContext`ia, koska projekti ei näe sitä.

Tämä on ero kerrosarkkitehtuuriin, jossa kerrokset ovat usein kansioita yhdessä projektissa. Kansioiden välillä kääntäjä ei estä mitään.

**Mitä kääntäjä ei valvo:** `API`-projekti viittaa `Infrastructure`-projektiin, koska sen pitää kytkeä rajapinnat toteutuksiin käynnistyksessä. Siksi controller *pystyy* teknisesti käyttämään repositorya tai `DbContext`ia suoraan, ja koodi kääntyy. Sääntö "controller kutsuu vain use casea" on siis sopimus, joka tarkistetaan koodikatselmuksessa.

| Sääntö | Kuka valvoo |
|---|---|
| Domain ei käytä Infrastructurea | Kääntäjä |
| Application ei käytä Infrastructurea | Kääntäjä |
| Controller ei käytä repositorya suoraan | Ihminen koodikatselmuksessa |

### Composition root

**Composition root** on se yksi kohta sovelluksessa, jossa rajapinnat sidotaan toteutuksiin. ASP.NET Core -sovelluksessa se on `Program.cs`, joka ajetaan kerran käynnistyksessä.

```csharp
// API/Program.cs – ainoa paikka, joka tuntee konkreettiset luokat
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddScoped<ConfirmOrderUseCase>();
```

**Minkä ongelman se ratkaisee?** Use case tuntee vain rajapinnan `IOrderRepository`. Jonkun täytyy silti päättää, mikä luokka sen toteuttaa. Jos tämä päätös olisi hajallaan ympäri koodia, toteutuksen vaihtaminen vaatisi muutoksia moneen paikkaan. Composition rootissa päätös on yhdessä tiedostossa.

**Missä kerroksessa se on?** Uloimmassa projektissa eli `API`ssa. Composition rootin täytyy nähdä sekä rajapinta (`Domain`) että toteutus (`Infrastructure`). Tästä syystä `API` saa viitata `Infrastructure`-projektiin. Viittaus on olemassa kytkemistä varten, ei siksi, että controllerit käyttäisivät Infrastructuren luokkia.

**Milloin sitä ei tarvita?** Pienessä ohjelmassa ilman rajapintoja ei ole mitään kytkettävää. Silloin oliot luodaan `new`-sanalla siellä, missä niitä tarvitaan.

Lisää rekisteröinnistä ja elinkaarista: [Dependency Injection](../Dependency-Injection.md).

### Miksi rajapinta on Domainissa ja toteutus Infrastructuressa

Repositoryn **rajapinta** (`IOrderRepository`) on `Domain`-projektissa. Sen **toteutus** (`OrderRepository`) on `Infrastructure`-projektissa. Jako tuntuu aluksi oudolta, koska molemmat liittyvät tallennukseen.

Syy on se, kuka rajapinnan omistaa. Rajapinta kertoo, mitä sovelluksen ydin *tarvitsee*: "anna tilaus tunnisteella", "tallenna tilaus". Se on ytimen vaatimus, joten se kuuluu ytimeen. Toteutus kertoo, *miten* tarve täytetään EF Corella. Se on tekninen yksityiskohta, joten se kuuluu ulkokehälle.

```
Application ──► Domain (IOrderRepository) ◄── Infrastructure (OrderRepository)
   käyttää            rajapinta                    toteuttaa
```

Molemmat nuolet osoittavat sisäänpäin, kohti Domainia.

**Mitä hajoaa, jos rajapinta siirretään Infrastructureen?**

```
Application ──► Infrastructure (IOrderRepository + OrderRepository)
```

- Use case tarvitsee rajapintaa, joten `Application`-projektin pitäisi viitata `Infrastructure`-projektiin. Nuoli kääntyy ulospäin, ja Dependency Rule rikkoutuu.
- Viittauksen mukana `Application` näkee myös `DbContext`in ja EF Coren. Kääntäjä ei enää estä use casea käyttämästä niitä.
- Use case -testi tarvitsisi mukaansa Infrastructure-projektin ja sen kirjastot.

Jotkut tiimit sijoittavat repositoryjen rajapinnat `Application`-projektiin. Sekin noudattaa Dependency Rulea, koska nuoli osoittaa yhä sisäänpäin. Tällä sivulla rajapinnat ovat `Domain`-projektissa.

---

## Edut ja haitat

### Edut

✅ **Liiketoimintalogiikka on riippumaton**
- Voit vaihtaa tietokannan (SQL Server → PostgreSQL)
- Voit vaihtaa UI:n (MVC → Blazor)
- Voit vaihtaa frameworkin

✅ **Erittäin testattava**
- Domain-logiikka testattavissa ilman tietokantaa
- Use case:t testattavissa fake- tai mock-riippuvuuksilla
- Nopeat testit

✅ **Teknologian vaihto on helppoa**
- Tietokanta, UI, framework ovat vaihdettavissa
- Liiketoimintalogiikka pysyy samana

✅ **Noudattaa SOLID-periaatteita**
- Dependency Inversion Principle
- Single Responsibility Principle
- Interface Segregation Principle

✅ **Skaalautuu hyvin**
- Sopii pienistä suuriin projekteihin
- Helppo laajentaa

### Haitat

❌ **Alkuun monimutkaisempi**
- Enemmän projekteja
- Enemmän rajapintoja
- Enemmän koodia

❌ **Vaatii enemmän suunnittelua**
- Pitää miettiä kerrosja­koa
- Pitää suunnitella rajapinnat

❌ **Yliinsinööriä pienissä projekteissa**
- TODO-lista ei tarvitse Clean Architecture:a
- Yksinkertainen CRUD-sovellus ei hyödy

❌ **Vaatii tiimiltä ymmärrystä**
- Kaikki kehittäjät pitää kouluttaa
- Vaatii kurinalaisuutta

---

## Milloin käyttää?

### ✅ Käytä kun:

- **Sovelluksessa on paljon liiketoimintasääntöjä**, ja ne muuttuvat
- **Pitkäikäinen projekti** (yli 2 vuotta ylläpidossa)
- **Liiketoimintalogiikka on monimutkaista**
- **Testattavuus on tärkeää**
- **Teknologia saattaa vaihtua**
- **Tiimi ymmärtää arkkitehtuurin**

### ❌ Älä käytä kun:

- **Sääntöjä on vähän**: sovellus lähinnä tallentaa ja näyttää dataa
- **Yksinkertainen CRUD-sovellus**
- **Nopea prototyyppi tai MVP**
- **Tiimi ei tunne arkkitehtuuria**
- **Projektin elinikä on lyhyt** (alle 6kk)

Ratkaiseva tekijä on sääntöjen määrä ja monimutkaisuus, ei tiimin koko. Yksin tehty sovellus, jossa on paljon sääntöjä, hyötyy Clean Architecturesta. Ison tiimin sovellus, jossa ei ole sääntöjä, ei hyödy.

---

## Käytännön esimerkki

Toteutetaan tilausjärjestelmä Clean Architecture -mallilla.

### Projektirakenne

```
OrderManagement/
├── OrderManagement.Domain/         (Entities)
│   ├── Entities/
│   │   ├── Order.cs
│   │   ├── OrderItem.cs
│   │   └── Product.cs
│   ├── Interfaces/
│   │   ├── IOrderRepository.cs
│   │   └── IProductRepository.cs
│   └── Enums/
│       └── OrderStatus.cs
├── OrderManagement.Application/    (Use Cases)
│   ├── UseCases/
│   │   ├── CreateOrderUseCase.cs
│   │   ├── GetOrderUseCase.cs
│   │   └── ConfirmOrderUseCase.cs
│   └── DTOs/
│       ├── CreateOrderDto.cs
│       └── OrderResponseDto.cs
├── OrderManagement.Infrastructure/ (Frameworks & Drivers)
│   ├── Data/
│   │   └── ApplicationDbContext.cs
│   ├── Repositories/
│   │   ├── OrderRepository.cs
│   │   └── ProductRepository.cs
│   └── DependencyInjection.cs
└── OrderManagement.Web/            (Interface Adapters)
    ├── Controllers/
    │   └── OrderController.cs
    └── Program.cs
```

### 1. Domain Layer (Entities)

**Domain/Entities/Order.cs:**

```csharp
namespace OrderManagement.Domain.Entities;

public class Order
{
    private readonly List<OrderItem> _items = new();

    public int Id { get; private set; }
    public string CustomerName { get; private set; }
    public IReadOnlyList<OrderItem> Items => _items;
    public DateTime OrderDate { get; private set; }
    public OrderStatus Status { get; private set; }

    // Uusi tilaus on aina Pending-tilassa. Tilaa ei voi asettaa ulkoa.
    public Order(string customerName)
    {
        if (string.IsNullOrWhiteSpace(customerName))
            throw new ArgumentException("Asiakkaan nimi on pakollinen");

        CustomerName = customerName;
        OrderDate = DateTime.UtcNow;
        Status = OrderStatus.Pending;
    }

    // Domain logic - Business rules
    public decimal GetTotal()
    {
        return Items.Sum(item => item.Price * item.Quantity);
    }

    public void AddItem(OrderItem item)
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException("Ei voi lisätä tuotteita vahvistettuun tilaukseen");

        if (item.Quantity <= 0)
            throw new ArgumentException("Määrän pitää olla positiivinen");

        _items.Add(item);
    }

    public void Confirm()
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException("Tilaus on jo vahvistettu");

        if (Items.Count == 0)
            throw new InvalidOperationException("Tilauksessa ei ole tuotteita");

        if (GetTotal() <= 0)
            throw new InvalidOperationException("Tilauksen summa ei voi olla nolla");

        Status = OrderStatus.Confirmed;
    }

    public void Cancel()
    {
        if (Status == OrderStatus.Delivered)
            throw new InvalidOperationException("Ei voi peruuttaa toimitettua tilausta");

        Status = OrderStatus.Cancelled;
    }

    public bool CanBeModified()
    {
        return Status == OrderStatus.Pending;
    }
}

public class OrderItem
{
    public int ProductId { get; set; }
    public string ProductName { get; set; }
    public decimal Price { get; set; }
    public int Quantity { get; set; }

    public decimal GetSubtotal()
    {
        return Price * Quantity;
    }
}

public enum OrderStatus
{
    Pending,
    Confirmed,
    Shipped,
    Delivered,
    Cancelled
}
```

**Huomaa:** `Order`in setterit ovat `private` ja tuotelista on ulospäin vain luettava (`IReadOnlyList`). Tilausta voi muuttaa vain metodeilla `AddItem`, `Confirm` ja `Cancel`, jotka tarkistavat säännöt. EF Core osaa silti täyttää olion: se käyttää kenttää `_items` ja asettaa private-setterit. `OrderItem` ja `Product` on jätetty esimerkissä yksinkertaisiksi (julkiset setterit). Oikeassa sovelluksessa nekin suojattaisiin samalla tavalla.

**Domain/Entities/Product.cs:**

```csharp
namespace OrderManagement.Domain.Entities;

public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int Stock { get; set; }

    // Domain logic
    public bool IsAvailable()
    {
        return Stock > 0;
    }

    public void ReduceStock(int quantity)
    {
        if (quantity > Stock)
            throw new InvalidOperationException($"Ei tarpeeksi varastossa. Saatavilla: {Stock}");

        Stock -= quantity;
    }

    public void IncreaseStock(int quantity)
    {
        if (quantity <= 0)
            throw new ArgumentException("Määrän pitää olla positiivinen");

        Stock += quantity;
    }
}
```

**Domain/Interfaces/IOrderRepository.cs:**

```csharp
using OrderManagement.Domain.Entities;

namespace OrderManagement.Domain.Interfaces;

public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id);
    Task<List<Order>> GetAllAsync();
    Task<List<Order>> GetByCustomerAsync(string customerName);
    Task<int> AddAsync(Order order);
    Task UpdateAsync(Order order);
}
```

Rajapinnassa ei ole `DeleteAsync`-metodia, koska mikään käyttötapaus ei poista tilausta. Repositoryn metodit tulevat käyttötapausten tarpeista, eivät valmiista CRUD-listasta. Katso [Mitä repository tekee ja mitä ei](../Patterns/Repository-Pattern.md#mitä-repository-tekee-ja-mitä-ei).

**Domain/Interfaces/IProductRepository.cs:**

```csharp
using OrderManagement.Domain.Entities;

namespace OrderManagement.Domain.Interfaces;

public interface IProductRepository
{
    Task<Product?> GetByIdAsync(int id);
    Task<List<Product>> GetAllAsync();
    Task<List<Product>> GetAvailableAsync();
    Task UpdateAsync(Product product);
}
```

### 2. Application Layer (Use Cases)

**Application/DTOs/CreateOrderDto.cs:**

```csharp
namespace OrderManagement.Application.DTOs;

public class CreateOrderDto
{
    public string CustomerName { get; set; }
    public List<OrderItemDto> Items { get; set; } = new();
}

public class OrderItemDto
{
    public int ProductId { get; set; }
    public int Quantity { get; set; }
}

public class OrderResponseDto
{
    public int Id { get; set; }
    public string CustomerName { get; set; }
    public decimal Total { get; set; }
    public string Status { get; set; }
    public DateTime OrderDate { get; set; }
    public List<OrderItemResponseDto> Items { get; set; } = new();
}

public class OrderItemResponseDto
{
    public string ProductName { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public decimal Subtotal { get; set; }
}
```

**Application/UseCases/CreateOrderUseCase.cs:**

```csharp
using OrderManagement.Domain.Entities;
using OrderManagement.Domain.Interfaces;
using OrderManagement.Application.DTOs;

namespace OrderManagement.Application.UseCases;

public class CreateOrderUseCase
{
    private readonly IOrderRepository _orderRepository;
    private readonly IProductRepository _productRepository;

    public CreateOrderUseCase(
        IOrderRepository orderRepository,
        IProductRepository productRepository)
    {
        _orderRepository = orderRepository;
        _productRepository = productRepository;
    }

    public async Task<OrderResponseDto> ExecuteAsync(CreateOrderDto dto)
    {
        // Syötteen tarkistus
        if (dto.Items == null || dto.Items.Count == 0)
            throw new ArgumentException("Tilaus ei voi olla tyhjä");

        // Luo domain entity (konstruktori tarkistaa nimen ja asettaa tilan)
        Order order = new Order(dto.CustomerName);

        // Hae tuotteet ja lisää tilaukseen
        foreach (OrderItemDto itemDto in dto.Items)
        {
            Product? product = await _productRepository.GetByIdAsync(itemDto.ProductId);
            
            // Tämä tarkistus kuuluu use caseen: se vaatii haun repositorysta
            if (product == null)
                throw new ArgumentException($"Tuotetta {itemDto.ProductId} ei löydy");

            // Varaston riittävyyttä ei tarkisteta täällä.
            // Se on Product-olion oma sääntö: ReduceStock heittää poikkeuksen.

            // Lisää tuote tilaukseen (domain logic)
            order.AddItem(new OrderItem
            {
                ProductId = product.Id,
                ProductName = product.Name,
                Price = product.Price,
                Quantity = itemDto.Quantity
            });

            // Vähennä varastosta (domain logic)
            product.ReduceStock(itemDto.Quantity);
            await _productRepository.UpdateAsync(product);
        }

        // Tallenna tilaus (EF Core asettaa order.Id:n tallennuksessa)
        await _orderRepository.AddAsync(order);

        // Palauta DTO
        return MapToResponseDto(order);
    }

    private OrderResponseDto MapToResponseDto(Order order)
    {
        return new OrderResponseDto
        {
            Id = order.Id,
            CustomerName = order.CustomerName,
            Total = order.GetTotal(),
            Status = order.Status.ToString(),
            OrderDate = order.OrderDate,
            Items = order.Items.Select(item => new OrderItemResponseDto
            {
                ProductName = item.ProductName,
                Quantity = item.Quantity,
                Price = item.Price,
                Subtotal = item.GetSubtotal()
            }).ToList()
        };
    }
}
```

**Application/UseCases/GetOrderUseCase.cs:**

```csharp
using OrderManagement.Domain.Entities;
using OrderManagement.Domain.Interfaces;
using OrderManagement.Application.DTOs;

namespace OrderManagement.Application.UseCases;

public class GetOrderUseCase
{
    private readonly IOrderRepository _orderRepository;

    public GetOrderUseCase(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }

    public async Task<OrderResponseDto?> ExecuteAsync(int orderId)
    {
        Order? order = await _orderRepository.GetByIdAsync(orderId);
        
        if (order == null)
            return null;

        return new OrderResponseDto
        {
            Id = order.Id,
            CustomerName = order.CustomerName,
            Total = order.GetTotal(),
            Status = order.Status.ToString(),
            OrderDate = order.OrderDate,
            Items = order.Items.Select(item => new OrderItemResponseDto
            {
                ProductName = item.ProductName,
                Quantity = item.Quantity,
                Price = item.Price,
                Subtotal = item.GetSubtotal()
            }).ToList()
        };
    }

    public async Task<List<OrderResponseDto>> GetAllOrdersAsync()
    {
        List<Order> orders = await _orderRepository.GetAllAsync();
        
        return orders.Select(order => new OrderResponseDto
        {
            Id = order.Id,
            CustomerName = order.CustomerName,
            Total = order.GetTotal(),
            Status = order.Status.ToString(),
            OrderDate = order.OrderDate
        }).ToList();
    }
}
```

**Application/UseCases/ConfirmOrderUseCase.cs:**

```csharp
using OrderManagement.Domain.Entities;
using OrderManagement.Domain.Interfaces;

namespace OrderManagement.Application.UseCases;

public class ConfirmOrderUseCase
{
    private readonly IOrderRepository _orderRepository;

    public ConfirmOrderUseCase(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }

    public async Task ExecuteAsync(int orderId)
    {
        Order? order = await _orderRepository.GetByIdAsync(orderId);
        
        if (order == null)
            throw new ArgumentException("Tilausta ei löydy");

        // Domain logic
        order.Confirm();

        // Tallenna
        await _orderRepository.UpdateAsync(order);
    }
}
```

### 3. Infrastructure Layer

**Infrastructure/Data/ApplicationDbContext.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using OrderManagement.Domain.Entities;

namespace OrderManagement.Infrastructure.Data;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public DbSet<Order> Orders { get; set; }
    public DbSet<Product> Products { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Order configuration
        modelBuilder.Entity<Order>(entity =>
        {
            entity.ToTable("Orders");
            entity.HasKey(o => o.Id);
            entity.Property(o => o.CustomerName).IsRequired().HasMaxLength(200);
            entity.Property(o => o.OrderDate).IsRequired();
            entity.Property(o => o.Status).IsRequired();
            
            entity.OwnsMany(o => o.Items, item =>
            {
                item.ToTable("OrderItems");
                item.WithOwner().HasForeignKey("OrderId");
                item.Property<int>("Id");
                item.HasKey("Id");
                item.Property(i => i.ProductName).IsRequired();
                item.Property(i => i.Price).HasColumnType("decimal(18,2)");
                item.Property(i => i.Quantity).IsRequired();
            });
        });

        // Product configuration
        modelBuilder.Entity<Product>(entity =>
        {
            entity.ToTable("Products");
            entity.HasKey(p => p.Id);
            entity.Property(p => p.Name).IsRequired().HasMaxLength(200);
            entity.Property(p => p.Price).HasColumnType("decimal(18,2)");
            entity.Property(p => p.Stock).IsRequired();
        });
    }
}
```

**Infrastructure/Repositories/OrderRepository.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using OrderManagement.Domain.Entities;
using OrderManagement.Domain.Interfaces;
using OrderManagement.Infrastructure.Data;

namespace OrderManagement.Infrastructure.Repositories;

public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;

    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Order?> GetByIdAsync(int id)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id);
    }

    public async Task<List<Order>> GetAllAsync()
    {
        return await _context.Orders
            .Include(o => o.Items)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync();
    }

    public async Task<List<Order>> GetByCustomerAsync(string customerName)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .Where(o => o.CustomerName == customerName)
            .OrderByDescending(o => o.OrderDate)
            .ToListAsync();
    }

    public async Task<int> AddAsync(Order order)
    {
        _context.Orders.Add(order);
        await _context.SaveChangesAsync();
        return order.Id;
    }

    public async Task UpdateAsync(Order order)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync();
    }
}
```

**Infrastructure/Repositories/ProductRepository.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using OrderManagement.Domain.Entities;
using OrderManagement.Domain.Interfaces;
using OrderManagement.Infrastructure.Data;

namespace OrderManagement.Infrastructure.Repositories;

public class ProductRepository : IProductRepository
{
    private readonly ApplicationDbContext _context;

    public ProductRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<Product?> GetByIdAsync(int id)
    {
        return await _context.Products.FindAsync(id);
    }

    public async Task<List<Product>> GetAllAsync()
    {
        return await _context.Products.ToListAsync();
    }

    public async Task<List<Product>> GetAvailableAsync()
    {
        return await _context.Products
            .Where(p => p.Stock > 0)
            .ToListAsync();
    }

    public async Task UpdateAsync(Product product)
    {
        _context.Products.Update(product);
        await _context.SaveChangesAsync();
    }
}
```

### 4. Web Layer (Interface Adapters)

**Web/Controllers/OrderController.cs:**

```csharp
using Microsoft.AspNetCore.Mvc;
using OrderManagement.Application.UseCases;
using OrderManagement.Application.DTOs;

namespace OrderManagement.Web.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrderController : ControllerBase
{
    private readonly CreateOrderUseCase _createOrderUseCase;
    private readonly GetOrderUseCase _getOrderUseCase;
    private readonly ConfirmOrderUseCase _confirmOrderUseCase;

    public OrderController(
        CreateOrderUseCase createOrderUseCase,
        GetOrderUseCase getOrderUseCase,
        ConfirmOrderUseCase confirmOrderUseCase)
    {
        _createOrderUseCase = createOrderUseCase;
        _getOrderUseCase = getOrderUseCase;
        _confirmOrderUseCase = confirmOrderUseCase;
    }

    [HttpGet]
    public async Task<ActionResult<List<OrderResponseDto>>> GetAllOrders()
    {
        List<OrderResponseDto> orders = await _getOrderUseCase.GetAllOrdersAsync();
        return Ok(orders);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<OrderResponseDto>> GetOrder(int id)
    {
        OrderResponseDto? order = await _getOrderUseCase.ExecuteAsync(id);
        
        if (order == null)
            return NotFound();

        return Ok(order);
    }

    [HttpPost]
    public async Task<ActionResult<OrderResponseDto>> CreateOrder([FromBody] CreateOrderDto dto)
    {
        try
        {
            OrderResponseDto order = await _createOrderUseCase.ExecuteAsync(dto);
            return CreatedAtAction(nameof(GetOrder), new { id = order.Id }, order);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            return Conflict(ex.Message);
        }
    }

    [HttpPost("{id}/confirm")]
    public async Task<IActionResult> ConfirmOrder(int id)
    {
        try
        {
            await _confirmOrderUseCase.ExecuteAsync(id);
            return Ok();
        }
        catch (ArgumentException ex)
        {
            return NotFound(ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(ex.Message);
        }
    }
}
```

**Web/Program.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using OrderManagement.Domain.Interfaces;
using OrderManagement.Application.UseCases;
using OrderManagement.Infrastructure.Data;
using OrderManagement.Infrastructure.Repositories;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Repositories (Infrastructure)
builder.Services.AddScoped<IOrderRepository, OrderRepository>();
builder.Services.AddScoped<IProductRepository, ProductRepository>();

// Use Cases (Application)
builder.Services.AddScoped<CreateOrderUseCase>();
builder.Services.AddScoped<GetOrderUseCase>();
builder.Services.AddScoped<ConfirmOrderUseCase>();

WebApplication app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

---

## Parhaat käytännöt

### 1. Noudata Dependency Rule:a

```csharp
// ✅ Hyvä: Domain määrittelee rajapinnan
// Domain/Interfaces/IOrderRepository.cs
public interface IOrderRepository { ... }

// Infrastructure toteuttaa rajapinnan
// Infrastructure/Repositories/OrderRepository.cs
public class OrderRepository : IOrderRepository { ... }

// ❌ Huono: Domain riippuu Infrastructure:sta
// Domain/Entities/Order.cs
public class Order
{
    private OrderRepository _repository; // ❌ Riippuvuus ulkoiseen!
}
```

### 2. Use Case per toiminto

```csharp
// ✅ Hyvä: Yksi Use Case per käyttötapaus
public class CreateOrderUseCase { ... }
public class GetOrderUseCase { ... }
public class ConfirmOrderUseCase { ... }

// ❌ Huono: Yksi suuri service kaikelle
public class OrderService
{
    public void CreateOrder() { ... }
    public void GetOrder() { ... }
    public void ConfirmOrder() { ... }
    // 20 muuta metodia...
}
```

### 3. Domain-logiikka Domain Layer:iin

```csharp
// ✅ Hyvä: Business rules Domain-entiteetissä
public class Order
{
    public void Confirm()
    {
        if (Status != OrderStatus.Pending)
            throw new InvalidOperationException("Tilaus on jo vahvistettu");
        
        if (Items.Count == 0)
            throw new InvalidOperationException("Tilauksessa ei ole tuotteita");
        
        Status = OrderStatus.Confirmed;
    }
}

// ❌ Huono: Business rules Use Case:ssa
public class ConfirmOrderUseCase
{
    public async Task ExecuteAsync(int orderId)
    {
        Order order = await _orderRepository.GetByIdAsync(orderId);
        
        // Business logic vuotaa Use Case:en! ❌
        if (order.Status != OrderStatus.Pending)
            throw new InvalidOperationException();
        
        if (order.Items.Count == 0)
            throw new InvalidOperationException();
        
        order.Status = OrderStatus.Confirmed; // Ei edes käänny, kun setteri on private
    }
}
```

Private-setteri tekee säännöstä pakollisen: use case ei pysty ohittamaan `Confirm()`-metodia.

Use case ei myöskään toista sääntöä, jonka entiteetti jo tarkistaa. Jos sama sääntö on kahdessa paikassa, ne ajautuvat ajan myötä eri versioiksi.

### 4. Käytä DTO:ita kerroksien välillä

```csharp
// ✅ Hyvä: DTO UI:lle
public class OrderResponseDto
{
    public int Id { get; set; }
    public string CustomerName { get; set; }
    public decimal Total { get; set; }
    // Vain tarvittavat kentät
}

// ❌ Huono: Domain entity suoraan UI:lle
[HttpGet("{id}")]
public async Task<ActionResult<Order>> GetOrder(int id)
{
    Order order = await _orderRepository.GetByIdAsync(id); // ❌ Entity vuotaa API:in
    return Ok(order);
}
```

### 5. Testaa jokaista kerrosta erikseen

```csharp
// Domain Layer testi (ei riippuvuuksia)
[Fact]
public void Order_Confirm_ThrowsIfAlreadyConfirmed()
{
    // Arrange: tila saadaan aikaan olion omilla metodeilla
    Order order = new Order("Matti");
    order.AddItem(new OrderItem { ProductId = 1, ProductName = "Test", Price = 10, Quantity = 1 });
    order.Confirm();
    
    // Act & Assert
    Assert.Throws<InvalidOperationException>(() => order.Confirm());
}

// Use Case testi (repositoryt korvataan mockeilla tai käsin kirjoitetuilla fakeilla)
[Fact]
public async Task CreateOrderUseCase_ValidOrder_ReturnsOrderDto()
{
    // Arrange
    Mock<IOrderRepository> mockRepo = new Mock<IOrderRepository>();
    Mock<IProductRepository> mockProductRepo = new Mock<IProductRepository>();
    
    Product product = new Product { Id = 1, Name = "Test", Price = 10, Stock = 5 };
    mockProductRepo.Setup(r => r.GetByIdAsync(1)).ReturnsAsync(product);
    
    CreateOrderUseCase useCase = new CreateOrderUseCase(mockRepo.Object, mockProductRepo.Object);
    
    // Act
    OrderResponseDto result = await useCase.ExecuteAsync(new CreateOrderDto
    {
        CustomerName = "John",
        Items = new List<OrderItemDto> { new() { ProductId = 1, Quantity = 2 } }
    });
    
    // Assert
    Assert.Equal("John", result.CustomerName);
    Assert.Equal(20, result.Total);
}
```

Domain-testi ei tarvitse yhtään korviketta, koska sääntö on entiteetissä. Use case -testi tarvitsee korvikkeen repositorylle. Katso [Domain-testi ja use case -testi](../UnitTesting/Unit-Testing.md#domain-testi-ja-use-case--testi).

---

## Yhteenveto

### Clean Architecture sopii kun:

✅ Sovelluksessa on paljon liiketoimintasääntöjä
✅ Projekti on pitkäikäinen (yli 2 vuotta)
✅ Liiketoimintalogiikka on monimutkaista
✅ Testattavuus on tärkeää
✅ Teknologia saattaa vaihtua
✅ Tiimi ymmärtää arkkitehtuurin

### Haasteet:

❌ Alkuun monimutkaisempi kuin Layered
❌ Vaatii enemmän koodia (rajapinnat, DTO:t)
❌ Yliinsinööriä pienissä projekteissa
❌ Vaatii tiimiltä koulutusta

### Muista:

- **Riippuvuudet AINA sisäänpäin**
- **Domain on keskiössä**
- **Teknologiariippumattomuus**
- **Testattavuus**
- **Aloita yksinkertaisesta, refaktoroi kun tarve tulee**

---

## Seuraavaksi

Kun Clean Architecture on hallussa:

- **[Hexagonal Architecture](Hexagonal-Architecture.md)** - Toinen näkökulma samaan asiaan
- **[Domain-Driven Design](Domain-Driven-Design.md)** - Miten Domain-kerroksen sisältö mallinnetaan
- **[CQRS](CQRS.md)** - Erottele lukeminen ja kirjoittaminen

### Hyödyllisiä linkkejä

- [The Clean Architecture Blog by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Microsoft: Clean Architecture with ASP.NET Core](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures#clean-architecture)
- [Jason Taylor: Clean Architecture Solution Template](https://github.com/jasontaylordev/CleanArchitecture)
