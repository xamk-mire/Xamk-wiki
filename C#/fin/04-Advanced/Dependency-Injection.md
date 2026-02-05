# Dependency Injection ja Dependency Inversion

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Dependency Inversion Principle (DIP)](#dependency-inversion-principle-dip)
3. [Tight Coupling - Ongelma](#tight-coupling---ongelma)
4. [Dependency Injection (DI)](#dependency-injection-di)
5. [DI:n tyypit](#din-tyypit)
6. [Miksi DI on tärkeää?](#miksi-di-on-tärkeää)
7. [DI ja yksikkötestaus](#di-ja-yksikkötestaus)
8. [DI Containerit](#di-containerit)
9. [ASP.NET Core DI](#aspnet-core-di)
10. [Parhaat käytännöt](#parhaat-käytännöt)
11. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Dependency Injection (DI)** on suunnittelumalli, joka toteuttaa **Dependency Inversion Principle (DIP)** -periaatteen. DI on yksi tärkeimmistä konsepteista modernissa ohjelmistokehityksessä, erityisesti:

- Yksikkötestauksessa (mocking)
- Clean Architecture -arkkitehtuurissa
- ASP.NET Core -sovelluksissa

Tämä materiaali selittää molemmat käsitteet ja näyttää miten niitä käytetään käytännössä.

---

## Dependency Inversion Principle (DIP)

**Dependency Inversion Principle** on SOLID-periaatteiden viides kirjain (D). Se määrittelee:

> 1. Ylemmän tason moduulit eivät saa riippua alemman tason moduuleista. Molempien tulee riippua abstraktioista.
> 2. Abstraktiot eivät saa riippua yksityiskohdista. Yksityiskohtien tulee riippua abstraktioista.

### Mitä tämä tarkoittaa käytännössä?

**Ilman DIP:**
```
OrderService → PaymentService (konkreettinen luokka)
     ↓
Ylätaso riippuu alatasosta
```

**DIP:n kanssa:**
```
OrderService → IPaymentService (interface)
                    ↑
              PaymentService

Molemmat riippuvat abstraktiosta (interface)
```

### Esimerkki: DIP-rikkomus

```csharp
// ❌ HUONO: OrderService riippuu suoraan PaymentService-luokasta
public class OrderService
{
    // Riippuvuus konkreettiseen luokkaan!
    private PaymentService _paymentService = new PaymentService();
    
    public void ProcessOrder(Order order)
    {
        _paymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}
```

**Ongelmat:**
- `OrderService` on tiukasti kytketty `PaymentService`-luokkaan
- Et voi vaihtaa `PaymentService`:ä toiseen toteutukseen
- Et voi mockata `PaymentService`:ä testeissä
- Jos `PaymentService` muuttuu, `OrderService` voi hajota

### Esimerkki: DIP-noudattaminen

```csharp
// ✅ HYVÄ: OrderService riippuu abstraktiosta (interface)

// 1. Määritellään abstraktio
public interface IPaymentService
{
    bool ProcessPayment(int customerId, decimal amount);
    bool RefundPayment(int customerId, decimal amount);
}

// 2. Konkreettinen toteutus toteuttaa interfacen
public class PaymentService : IPaymentService
{
    public bool ProcessPayment(int customerId, decimal amount)
    {
        // Oikea toteutus
        return true;
    }
    
    public bool RefundPayment(int customerId, decimal amount)
    {
        // Oikea toteutus
        return true;
    }
}

// 3. OrderService riippuu vain interfacesta
public class OrderService
{
    private readonly IPaymentService _paymentService;
    
    // Riippuvuus injektoidaan konstruktorissa
    public OrderService(IPaymentService paymentService)
    {
        _paymentService = paymentService;
    }
    
    public void ProcessOrder(Order order)
    {
        _paymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}
```

**Hyödyt:**
- `OrderService` ei tiedä mitä `IPaymentService`:n toteutusta käytetään
- Voit vaihtaa toteutuksen helposti (StripePaymentService, MockPaymentService)
- Testattavuus paranee merkittävästi

---

## Tight Coupling - Ongelma

**Tight coupling** (tiukka kytkentä) tarkoittaa tilannetta, jossa luokka on vahvasti riippuvainen toisesta luokasta.

### Tunnusmerkit

```csharp
// ❌ Tight coupling -merkkejä:

public class OrderService
{
    // 1. new-avainsana luokan sisällä
    private PaymentService _payment = new PaymentService();
    
    // 2. Staattisten metodien kutsuminen
    private void Log() => Logger.Log("...");
    
    // 3. Konkreettiset luokat kentissä
    private EmailService _email;
    
    public OrderService()
    {
        // 4. Riippuvuuksien luominen konstruktorissa
        _email = new EmailService();
    }
}
```

### Ongelmat testattavuudessa

```csharp
// Yritetään testata OrderService:ä
[Fact]
public void ProcessOrder_ValidOrder_ReturnsTrue()
{
    // ❌ ONGELMA: Emme voi kontrolloida PaymentService:n käyttäytymistä!
    var service = new OrderService();
    
    // Tämä kutsu käyttää OIKEAA PaymentService:ä
    // - Hidas (oikea tietokantakutsu)
    // - Sivuvaikutuksia (veloittaa oikeasti!)
    // - Ei toistettava (tietokannan tila muuttuu)
    var result = service.ProcessOrder(order);
    
    // Emme voi testata:
    // - Mitä tapahtuu kun maksu epäonnistuu?
    // - Kutsuttiinko PaymentService:ä oikein?
}
```

### Visualisointi

```
TIGHT COUPLING:

┌─────────────────┐
│  OrderService   │
│                 │
│  new Payment()──┼────► PaymentService (konkreettinen)
│  new Email()────┼────► EmailService (konkreettinen)
│  new Logger()───┼────► Logger (konkreettinen)
│                 │
└─────────────────┘

Testissä EI VOI vaihtaa näitä!


LOOSE COUPLING (DI):

┌─────────────────┐
│  OrderService   │
│                 │
│  IPayment ◄─────┼────┐
│  IEmail ◄───────┼────┤ Injektoidaan ulkopuolelta
│  ILogger ◄──────┼────┤
│                 │    │
└─────────────────┘    │
                       │
         ┌─────────────┴─────────────┐
         │                           │
    TUOTANNOSSA:              TESTISSÄ:
    PaymentService            Mock<IPayment>
    EmailService              Mock<IEmail>
    FileLogger                Mock<ILogger>
```

---

## Dependency Injection (DI)

**Dependency Injection** on tekniikka, jolla toteutetaan DIP. Riippuvuudet "injektoidaan" (annetaan) ulkopuolelta sen sijaan, että luokka loisi ne itse.

### Perusidea

```csharp
// ❌ ILMAN DI: Luokka luo riippuvuudet itse
public class OrderService
{
    private IPaymentService _payment = new PaymentService(); // Luo itse
}

// ✅ DI:N KANSSA: Riippuvuudet annetaan ulkopuolelta
public class OrderService
{
    private readonly IPaymentService _payment;
    
    public OrderService(IPaymentService payment) // Injektoidaan
    {
        _payment = payment;
    }
}
```

---

## DI:n tyypit

### 1. Constructor Injection (Suositeltu)

Riippuvuudet annetaan konstruktorin kautta.

```csharp
public class OrderService
{
    private readonly IPaymentService _paymentService;
    private readonly IInventoryService _inventoryService;
    private readonly INotificationService _notificationService;
    
    // Kaikki riippuvuudet konstruktorissa
    public OrderService(
        IPaymentService paymentService,
        IInventoryService inventoryService,
        INotificationService notificationService)
    {
        _paymentService = paymentService ?? throw new ArgumentNullException(nameof(paymentService));
        _inventoryService = inventoryService ?? throw new ArgumentNullException(nameof(inventoryService));
        _notificationService = notificationService ?? throw new ArgumentNullException(nameof(notificationService));
    }
}
```

**Hyödyt:**
- ✅ Riippuvuudet ovat selkeästi näkyvissä
- ✅ Objekti on valmis käytettäväksi heti luonnin jälkeen
- ✅ Riippuvuudet voidaan tehdä `readonly`:ksi
- ✅ Helppo testata

**Milloin käyttää:** Lähes aina. Tämä on suositeltu tapa.

### 2. Property Injection

Riippuvuudet asetetaan property:n kautta.

```csharp
public class OrderService
{
    // Property injection
    public IPaymentService PaymentService { get; set; }
    
    public void ProcessOrder(Order order)
    {
        if (PaymentService == null)
            throw new InvalidOperationException("PaymentService not set");
            
        PaymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// Käyttö
var service = new OrderService();
service.PaymentService = new PaymentService(); // Asetetaan jälkikäteen
```

**Hyödyt:**
- Valinnaisten riippuvuuksien asettaminen
- Joskus tarpeen legacy-koodissa

**Haitat:**
- ❌ Objekti voi olla epävalidissa tilassa
- ❌ Riippuvuus voidaan unohtaa asettaa
- ❌ Ei ole thread-safe

**Milloin käyttää:** Harvoin. Vain valinnaisille riippuvuuksille.

### 3. Method Injection

Riippuvuus annetaan metodin parametrina.

```csharp
public class OrderService
{
    // Method injection - riippuvuus annetaan kutsuhetkellä
    public void ProcessOrder(Order order, IPaymentService paymentService)
    {
        paymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// Käyttö
var service = new OrderService();
service.ProcessOrder(order, new PaymentService());
```

**Hyödyt:**
- Riippuvuus voi vaihtua joka kutsukerralla

**Haitat:**
- ❌ Kutsuja joutuu aina antamaan riippuvuuden
- ❌ Voi johtaa pitkiin parametrilistoihin

**Milloin käyttää:** Kun riippuvuus vaihtelee kutsujen välillä.

---

## Miksi DI on tärkeää?

### 1. Testattavuus

DI mahdollistaa mockauksen:

```csharp
// TESTISSÄ: Voit mockata riippuvuudet
[Fact]
public void ProcessOrder_PaymentSucceeds_ReturnsTrue()
{
    // Arrange - Luo mock
    var paymentMock = new Mock<IPaymentService>();
    paymentMock.Setup(x => x.ProcessPayment(It.IsAny<int>(), It.IsAny<decimal>()))
               .Returns(true);
    
    // Injektoi mock
    var service = new OrderService(paymentMock.Object);
    
    // Act
    var result = service.ProcessOrder(order);
    
    // Assert
    Assert.True(result);
    paymentMock.Verify(x => x.ProcessPayment(123, 100m), Times.Once);
}
```

### 2. Löysä kytkentä (Loose Coupling)

Luokat eivät ole sidottuja tiettyihin toteutuksiin:

```csharp
// Sama OrderService toimii eri maksupalvelujen kanssa
var stripeService = new OrderService(new StripePaymentService());
var paypalService = new OrderService(new PayPalPaymentService());
var testService = new OrderService(new MockPaymentService());
```

### 3. Single Responsibility

Luokka ei vastaa riippuvuuksiensa luomisesta:

```csharp
// ❌ OrderService vastaa liian monesta asiasta
public class OrderService
{
    private IPaymentService _payment;
    
    public OrderService()
    {
        // Tietää miten PaymentService luodaan
        // Tietää mitä konfiguraatiota se tarvitsee
        var config = new PaymentConfig { ApiKey = "..." };
        _payment = new PaymentService(config);
    }
}

// ✅ OrderService keskittyy omaan tehtäväänsä
public class OrderService
{
    private readonly IPaymentService _payment;
    
    public OrderService(IPaymentService payment)
    {
        _payment = payment; // Ei tiedä/välitä miten luotiin
    }
}
```

### 4. Konfiguroitavuus

Sovelluksen käyttäytymistä voi muuttaa ilman koodimuutoksia:

```csharp
// Kehityksessä
services.AddScoped<IEmailService, FakeEmailService>();

// Tuotannossa
services.AddScoped<IEmailService, SendGridEmailService>();
```

---

## DI ja yksikkötestaus

DI:n tärkein hyöty on **mockauksen mahdollistaminen** yksikkötesteissä.

### Ilman DI:tä - Vaikea testata

```csharp
public class OrderService
{
    private PaymentService _payment = new PaymentService();
    
    public bool ProcessOrder(Order order)
    {
        return _payment.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// ❌ TESTI EI TOIMI KUNNOLLA
[Fact]
public void ProcessOrder_Test()
{
    var service = new OrderService();
    
    // Ongelma: Käyttää oikeaa PaymentService:ä!
    // - Hidasta (oikea API-kutsu)
    // - Sivuvaikutuksia (veloittaa oikeasti)
    // - Ei voi testata virhetilanteita
    var result = service.ProcessOrder(order);
}
```

### DI:n kanssa - Helppo testata

```csharp
public class OrderService
{
    private readonly IPaymentService _payment;
    
    public OrderService(IPaymentService payment)
    {
        _payment = payment;
    }
    
    public bool ProcessOrder(Order order)
    {
        return _payment.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// ✅ TESTI TOIMII HYVIN
[Fact]
public void ProcessOrder_PaymentSucceeds_ReturnsTrue()
{
    // Arrange - Luo mock joka palauttaa true
    var paymentMock = new Mock<IPaymentService>();
    paymentMock.Setup(x => x.ProcessPayment(It.IsAny<int>(), It.IsAny<decimal>()))
               .Returns(true);
    
    var service = new OrderService(paymentMock.Object);
    
    // Act
    var result = service.ProcessOrder(new Order { CustomerId = 1, TotalPrice = 100 });
    
    // Assert
    Assert.True(result);
}

[Fact]
public void ProcessOrder_PaymentFails_ReturnsFalse()
{
    // Arrange - Luo mock joka palauttaa false
    var paymentMock = new Mock<IPaymentService>();
    paymentMock.Setup(x => x.ProcessPayment(It.IsAny<int>(), It.IsAny<decimal>()))
               .Returns(false); // Simuloi epäonnistumista!
    
    var service = new OrderService(paymentMock.Object);
    
    // Act
    var result = service.ProcessOrder(new Order { CustomerId = 1, TotalPrice = 100 });
    
    // Assert
    Assert.False(result);
}
```

---

## DI Containerit

**DI Container** (tai IoC Container) on framework, joka hallinnoi riippuvuuksien luomista ja elinkaarta automaattisesti.

### Ilman containeria

```csharp
// Käsin luodut riippuvuudet - työlästä!
var logger = new FileLogger();
var config = new AppConfig();
var database = new SqlDatabase(config.ConnectionString);
var userRepository = new UserRepository(database, logger);
var emailService = new SmtpEmailService(config);
var userService = new UserService(userRepository, emailService, logger);

// Jos UserService:llä on 10 riippuvuutta, tämä kasvaa nopeasti...
```

### DI Containerin kanssa

```csharp
// Rekisteröinti (tehdään kerran sovelluksen alussa)
services.AddSingleton<ILogger, FileLogger>();
services.AddSingleton<IAppConfig, AppConfig>();
services.AddScoped<IDatabase, SqlDatabase>();
services.AddScoped<IUserRepository, UserRepository>();
services.AddScoped<IEmailService, SmtpEmailService>();
services.AddScoped<IUserService, UserService>();

// Container hoitaa luomisen automaattisesti
var userService = serviceProvider.GetService<IUserService>();
// Kaikki riippuvuudet luodaan ja injektoidaan automaattisesti!
```

### Suosittuja DI Containereita

| Container | Käyttö |
|-----------|--------|
| **Microsoft.Extensions.DependencyInjection** | ASP.NET Core, sisäänrakennettu |
| **Autofac** | Monipuolinen, paljon ominaisuuksia |
| **Ninject** | Helppo käyttää |
| **Unity** | Microsoftin (vanhempi) |

---

## ASP.NET Core DI

ASP.NET Core sisältää sisäänrakennetun DI Containerin.

### Rekisteröinti (Program.cs tai Startup.cs)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Rekisteröi palvelut
builder.Services.AddScoped<IPaymentService, StripePaymentService>();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<IEmailService, SendGridEmailService>();

// Singleton - yksi instanssi koko sovelluksen elinkaaren
builder.Services.AddSingleton<ILogger, FileLogger>();

// Transient - uusi instanssi joka kerta
builder.Services.AddTransient<IGuidGenerator, GuidGenerator>();

var app = builder.Build();
```

### Elinkaaret

| Elinkaari | Kuvaus | Käyttö |
|-----------|--------|--------|
| **Singleton** | Yksi instanssi koko sovellukselle | Loggerit, konfiguraatio |
| **Scoped** | Yksi instanssi per HTTP-pyyntö | Repositoryt, DbContext |
| **Transient** | Uusi instanssi joka kerta | Kevyet, tilattomat palvelut |

### Käyttö Controllerissa

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;
    
    // DI Container injektoi automaattisesti!
    public OrdersController(IOrderService orderService)
    {
        _orderService = orderService;
    }
    
    [HttpPost]
    public IActionResult CreateOrder(OrderDto orderDto)
    {
        var result = _orderService.ProcessOrder(orderDto);
        return Ok(result);
    }
}
```

---

## Parhaat käytännöt

### 1. Käytä Constructor Injectionia

```csharp
// ✅ Hyvä
public class OrderService
{
    private readonly IPaymentService _payment;
    
    public OrderService(IPaymentService payment)
    {
        _payment = payment;
    }
}
```

### 2. Käytä readonly-kenttiä

```csharp
// ✅ Hyvä - readonly estää vahingossa tapahtuvan muutoksen
private readonly IPaymentService _payment;

// ❌ Huono - voidaan muuttaa vahingossa
private IPaymentService _payment;
```

### 3. Tarkista null konstruktorissa

```csharp
public OrderService(IPaymentService payment)
{
    _payment = payment ?? throw new ArgumentNullException(nameof(payment));
}
```

### 4. Pidä konstruktorit yksinkertaisina

```csharp
// ✅ Hyvä - vain sijoituksia
public OrderService(IPaymentService payment)
{
    _payment = payment;
}

// ❌ Huono - logiikkaa konstruktorissa
public OrderService(IPaymentService payment)
{
    _payment = payment;
    _payment.Initialize(); // Ei logiikkaa tänne!
    LoadConfiguration();   // Ei logiikkaa tänne!
}
```

### 5. Vältä Service Locator -antipattern

```csharp
// ❌ Huono - Service Locator (antipattern)
public class OrderService
{
    public void ProcessOrder(Order order)
    {
        // Riippuvuus on piilotettu!
        var payment = ServiceLocator.GetService<IPaymentService>();
        payment.ProcessPayment(order);
    }
}

// ✅ Hyvä - Explicit DI
public class OrderService
{
    private readonly IPaymentService _payment;
    
    public OrderService(IPaymentService payment)
    {
        _payment = payment; // Riippuvuus on näkyvissä
    }
}
```

### 6. Rajapinnat omaan kansioon

```
MyApp/
├── Services/
│   ├── Interfaces/
│   │   ├── IPaymentService.cs
│   │   ├── IOrderService.cs
│   │   └── IEmailService.cs
│   ├── PaymentService.cs
│   ├── OrderService.cs
│   └── EmailService.cs
```

---

## Yhteenveto

### Dependency Inversion Principle (DIP)
- Ylätason moduulit eivät saa riippua alatason moduuleista
- Molemmat riippuvat abstraktioista (interface)

### Dependency Injection (DI)
- Tekniikka DIP:n toteuttamiseen
- Riippuvuudet annetaan ulkopuolelta (injektoidaan)
- Constructor Injection on suositeltu tapa

### Hyödyt

| Hyöty | Kuvaus |
|-------|--------|
| **Testattavuus** | Mockaus mahdollista |
| **Löysä kytkentä** | Luokat eivät riipu toteutuksista |
| **Joustavuus** | Toteutuksen voi vaihtaa helposti |
| **Ylläpidettävyys** | Muutokset eivät leviä |

### Muistisääntö

```
❌ new = tight coupling = vaikea testata
✅ interface + DI = loose coupling = helppo testata
```

---

## Tehtävät

Harjoittele DI:tä ja mockausta:
- [UnitTestingObjects](../../../Assigments/UnitTestingObjects/README.md) - Olioiden testaaminen

---

## Hyödyllisiä linkkejä

- [Microsoft: Dependency Injection](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
- [SOLID Principles](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)
- [Moq Quickstart](https://github.com/moq/moq4/wiki/Quickstart)
