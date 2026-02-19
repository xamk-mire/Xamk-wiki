# SOLID-periaatteet

SOLID on viiden suunnitteluperiaatteen kokoelma, jonka tarkoituksena on tehdä olio-ohjelmoinnista ylläpidettävämpää, joustavampaa ja ymmärrettävämpää. Periaatteet esitteli Robert C. Martin (tunnetaan myös nimellä "Uncle Bob"), ja ne ovat yksi tärkeimmistä ohjelmoinnin suunnitteluperiaatteista.

**Muita materiaaleja:**
- [SOLID Principles in C# - C# Corner](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)
- [Microsoft - Architectural Principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles)
- [Suunnitteluperiaatteet (DRY, KISS, YAGNI ym.)](Design-Principles.md)

## Miksi SOLID?

Ilman selkeitä suunnitteluperiaatteita koodi muuttuu nopeasti vaikeaksi ymmärtää ja ylläpitää. SOLID auttaa välttämään yleisiä ongelmia:

| Ongelma | SOLID-ratkaisu |
|---------|----------------|
| Luokka tekee liikaa asioita | Single Responsibility Principle |
| Uusi ominaisuus vaatii vanhan koodin muuttamista | Open/Closed Principle |
| Aliluokka rikkoo yläluokan toiminnan | Liskov Substitution Principle |
| Luokka pakotetaan toteuttamaan turhia metodeja | Interface Segregation Principle |
| Luokat ovat tiukasti sidottuja toisiinsa | Dependency Inversion Principle |

---

## S - Single Responsibility Principle (SRP)

> *"Luokalla tulisi olla vain yksi syy muuttua."*

Jokaisen luokan tulisi vastata vain yhdestä asiasta. Jos luokka hoitaa useita vastuualueita, muutos yhdessä vastuualueessa voi rikkoa toisen.

### Huono esimerkki

```csharp
public class Employee
{
    public string Name { get; set; }
    public decimal Salary { get; set; }

    public decimal CalculatePay()
    {
        return Salary * 1.0m;
    }

    public void SaveToDatabase()
    {
        // Tallentaa tietokantaan
        Console.WriteLine($"Saving {Name} to database...");
    }

    public string GenerateReport()
    {
        // Luo raportin
        return $"Employee Report: {Name}, Salary: {Salary:C}";
    }

    public void SendPayslipEmail()
    {
        // Lähettää sähköpostin
        Console.WriteLine($"Sending payslip to {Name}...");
    }
}
```

Tässä `Employee`-luokalla on **neljä eri syytä muuttua**:
1. Työntekijän tiedot muuttuvat
2. Palkanmaksulogiikka muuttuu
3. Raportointivaatimukset muuttuvat
4. Sähköpostipalvelu muuttuu

### Hyvä esimerkki

```csharp
public class Employee
{
    public string Name { get; set; }
    public string Email { get; set; }
    public decimal Salary { get; set; }
}

public class PayCalculator
{
    public decimal CalculatePay(Employee employee)
    {
        return employee.Salary * 1.0m;
    }

    public decimal CalculatePayWithBonus(Employee employee, decimal bonusPercentage)
    {
        return employee.Salary * (1 + bonusPercentage / 100);
    }
}

public class EmployeeRepository
{
    public void Save(Employee employee)
    {
        Console.WriteLine($"Saving {employee.Name} to database...");
    }

    public Employee GetByName(string name)
    {
        // Hakee tietokannasta
        return new Employee { Name = name };
    }
}

public class ReportGenerator
{
    public string GenerateEmployeeReport(Employee employee)
    {
        return $"Employee Report: {employee.Name}, Salary: {employee.Salary:C}";
    }
}

public class EmailService
{
    public void SendPayslipEmail(Employee employee, string reportContent)
    {
        Console.WriteLine($"Sending payslip to {employee.Email}: {reportContent}");
    }
}
```

Nyt jokaisella luokalla on **yksi selkeä vastuu**:
- `Employee` — tietomalli
- `PayCalculator` — palkanlasku
- `EmployeeRepository` — tietokantatoiminnot
- `ReportGenerator` — raportointi
- `EmailService` — sähköpostit

### Käytännön vinkki

Kysy itseltäsi: *"Jos vaatimus X muuttuu, pitääkö minun muuttaa tätä luokkaa?"* Jos useampi eri vaatimus aiheuttaa muutoksen samaan luokkaan, luokalla on liian monta vastuuta.

---

## O - Open/Closed Principle (OCP)

> *"Ohjelmiston osien tulisi olla avoimia laajennuksille, mutta suljettuja muutoksille."*

Kun tarvitset uutta toiminnallisuutta, sinun ei pitäisi joutua muuttamaan olemassa olevaa koodia — sen sijaan laajennat sitä uusilla luokilla.

### Huono esimerkki

```csharp
public class AreaCalculator
{
    public double CalculateArea(object shape)
    {
        if (shape is Rectangle rectangle)
        {
            return rectangle.Width * rectangle.Height;
        }
        else if (shape is Circle circle)
        {
            return Math.PI * circle.Radius * circle.Radius;
        }
        else if (shape is Triangle triangle)
        {
            return 0.5 * triangle.Base * triangle.Height;
        }
        // Jokainen uusi muoto vaatii tämän metodin muuttamista!
        throw new ArgumentException("Unknown shape");
    }
}
```

Joka kerta kun lisäät uuden muodon, joudut muokkaamaan `CalculateArea`-metodia. Tämä rikkoo OCP:tä.

### Hyvä esimerkki

```csharp
public interface IShape
{
    double CalculateArea();
    string Name { get; }
}

public class Rectangle : IShape
{
    public double Width { get; set; }
    public double Height { get; set; }
    public string Name => "Suorakulmio";

    public double CalculateArea() => Width * Height;
}

public class Circle : IShape
{
    public double Radius { get; set; }
    public string Name => "Ympyrä";

    public double CalculateArea() => Math.PI * Radius * Radius;
}

public class Triangle : IShape
{
    public double Base { get; set; }
    public double Height { get; set; }
    public string Name => "Kolmio";

    public double CalculateArea() => 0.5 * Base * Height;
}

// Tätä luokkaa ei tarvitse koskaan muuttaa uusien muotojen lisäämiseksi
public class AreaCalculator
{
    public double CalculateTotalArea(IEnumerable<IShape> shapes)
    {
        return shapes.Sum(shape => shape.CalculateArea());
    }

    public void PrintAreas(IEnumerable<IShape> shapes)
    {
        foreach (var shape in shapes)
        {
            Console.WriteLine($"{shape.Name}: {shape.CalculateArea():F2}");
        }
    }
}
```

Nyt voit lisätä uusia muotoja luomalla uusia luokkia ilman, että `AreaCalculator`-luokkaa tarvitsee muuttaa:

```csharp
// Uusi muoto — ei vaadi muutoksia mihinkään olemassa olevaan koodiin
public class Hexagon : IShape
{
    public double SideLength { get; set; }
    public string Name => "Kuusikulmio";

    public double CalculateArea() => (3 * Math.Sqrt(3) / 2) * SideLength * SideLength;
}
```

### Realistisempi esimerkki: Alennuslaskuri

```csharp
// Huono: if-else-ketju joka kasvaa jatkuvasti
public class DiscountCalculatorBad
{
    public decimal CalculateDiscount(string customerType, decimal amount)
    {
        if (customerType == "Regular")
            return amount * 0.05m;
        else if (customerType == "Premium")
            return amount * 0.10m;
        else if (customerType == "VIP")
            return amount * 0.20m;
        // Uusi asiakastyyppi = muutos tähän metodiin
        return 0;
    }
}

// Hyvä: Strategia-malli + OCP
public interface IDiscountStrategy
{
    decimal CalculateDiscount(decimal amount);
}

public class RegularDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal amount) => amount * 0.05m;
}

public class PremiumDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal amount) => amount * 0.10m;
}

public class VipDiscount : IDiscountStrategy
{
    public decimal CalculateDiscount(decimal amount) => amount * 0.20m;
}

public class DiscountCalculator
{
    private readonly IDiscountStrategy _strategy;

    public DiscountCalculator(IDiscountStrategy strategy)
    {
        _strategy = strategy;
    }

    public decimal Calculate(decimal amount) => _strategy.CalculateDiscount(amount);
}
```

---

## L - Liskov Substitution Principle (LSP)

> *"Aliluokan tulee olla korvattavissa yläluokallaan ilman, että ohjelman toiminta rikkoutuu."*

Jos luokka `B` perii luokan `A`, niin `B`:n pitää pystyä toimimaan kaikkialla, missä `A`:ta käytetään, ilman yllätyksiä.

### Huono esimerkki

```csharp
public class Bird
{
    public virtual void Fly()
    {
        Console.WriteLine("I'm flying!");
    }
}

public class Eagle : Bird
{
    public override void Fly()
    {
        Console.WriteLine("Eagle soaring high!");
    }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        // LSP-rikkomus: pingviini ei voi lentää!
        throw new NotSupportedException("Penguins can't fly!");
    }
}

// Tämä koodi kaatuu ajonaikaisesti pingviinin kohdalla
public class BirdWatcher
{
    public void WatchBirdsFly(List<Bird> birds)
    {
        foreach (var bird in birds)
        {
            bird.Fly(); // Heittää poikkeuksen Penguin-oliolle
        }
    }
}
```

### Hyvä esimerkki

```csharp
public abstract class Bird
{
    public string Name { get; set; }
    public abstract void Move();
}

public interface IFlyable
{
    void Fly();
}

public interface ISwimmable
{
    void Swim();
}

public class Eagle : Bird, IFlyable
{
    public override void Move()
    {
        Fly();
    }

    public void Fly()
    {
        Console.WriteLine($"{Name} is soaring through the sky!");
    }
}

public class Penguin : Bird, ISwimmable
{
    public override void Move()
    {
        Swim();
    }

    public void Swim()
    {
        Console.WriteLine($"{Name} is swimming gracefully!");
    }
}

public class Duck : Bird, IFlyable, ISwimmable
{
    public override void Move()
    {
        Console.WriteLine($"{Name} is waddling around!");
    }

    public void Fly()
    {
        Console.WriteLine($"{Name} is flying!");
    }

    public void Swim()
    {
        Console.WriteLine($"{Name} is swimming!");
    }
}

// Nyt kaikki linnut voivat liikkua ilman yllätyksiä
public class BirdWatcher
{
    public void WatchBirdsMove(List<Bird> birds)
    {
        foreach (var bird in birds)
        {
            bird.Move(); // Toimii kaikilla linnuilla
        }
    }
}
```

### Klassinen esimerkki: Suorakulmio ja neliö

```csharp
// Huono: Neliö perii suorakulmion, mutta rikkoo sen käyttäytymisen
public class RectangleBad
{
    public virtual double Width { get; set; }
    public virtual double Height { get; set; }

    public double CalculateArea() => Width * Height;
}

public class SquareBad : RectangleBad
{
    public override double Width
    {
        get => base.Width;
        set
        {
            base.Width = value;
            base.Height = value; // Sivuvaikutus — rikkoo yläluokan oletuksen
        }
    }

    public override double Height
    {
        get => base.Height;
        set
        {
            base.Height = value;
            base.Width = value; // Sivuvaikutus — rikkoo yläluokan oletuksen
        }
    }
}

// Tämä testi epäonnistuu neliöllä:
// rectangle.Width = 5; rectangle.Height = 10;
// CalculateArea() palauttaa 100 eikä 50

// Hyvä: Käytetään yhteistä rajapintaa
public interface IShape
{
    double CalculateArea();
}

public class Rectangle : IShape
{
    public double Width { get; set; }
    public double Height { get; set; }

    public double CalculateArea() => Width * Height;
}

public class Square : IShape
{
    public double Side { get; set; }

    public double CalculateArea() => Side * Side;
}
```

### LSP:n nyrkkisääntö

Jos huomaat kirjoittavasi `if (object is SpecificType)` -tarkistuksia tai `throw new NotSupportedException()` -poikkeuksia aliluokassa, perintähierarkia on todennäköisesti väärä.

---

## I - Interface Segregation Principle (ISP)

> *"Asiakkaita ei pidä pakottaa riippumaan rajapinnoista, joita ne eivät käytä."*

Isot, "jättiläis"-rajapinnat tulisi jakaa pienempiin ja tarkempiin rajapintoihin, jotta luokat toteuttavat vain ne metodit, joita ne oikeasti tarvitsevat.

### Huono esimerkki

```csharp
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
    void AttendMeeting();
    void WriteReport();
}

public class FullTimeEmployee : IWorker
{
    public void Work() => Console.WriteLine("Working full-time");
    public void Eat() => Console.WriteLine("Eating lunch");
    public void Sleep() => Console.WriteLine("Sleeping at home");
    public void AttendMeeting() => Console.WriteLine("In a meeting");
    public void WriteReport() => Console.WriteLine("Writing report");
}

public class Intern : IWorker
{
    public void Work() => Console.WriteLine("Working as intern");
    public void Eat() => Console.WriteLine("Eating lunch");
    public void Sleep() => Console.WriteLine("Sleeping at home");
    public void AttendMeeting() => throw new NotSupportedException("Interns don't attend meetings");
    public void WriteReport() => throw new NotSupportedException("Interns don't write reports");
}

public class Robot : IWorker
{
    public void Work() => Console.WriteLine("Robot working 24/7");
    public void Eat() => throw new NotSupportedException("Robots don't eat!");
    public void Sleep() => throw new NotSupportedException("Robots don't sleep!");
    public void AttendMeeting() => throw new NotSupportedException("Robots don't attend meetings!");
    public void WriteReport() => Console.WriteLine("Generating automated report");
}
```

`Robot` joutuu toteuttamaan `Eat()` ja `Sleep()`, vaikka niillä ei ole mitään tekemistä robotin kanssa.

### Hyvä esimerkki

```csharp
public interface IWorkable
{
    void Work();
}

public interface IFeedable
{
    void Eat();
}

public interface ISleepable
{
    void Sleep();
}

public interface IMeetingAttendee
{
    void AttendMeeting();
}

public interface IReportWriter
{
    void WriteReport();
}

// Kokopäiväinen työntekijä toteuttaa kaikki tarvittavat rajapinnat
public class FullTimeEmployee : IWorkable, IFeedable, ISleepable, IMeetingAttendee, IReportWriter
{
    public void Work() => Console.WriteLine("Working full-time");
    public void Eat() => Console.WriteLine("Eating lunch");
    public void Sleep() => Console.WriteLine("Sleeping at home");
    public void AttendMeeting() => Console.WriteLine("In a meeting");
    public void WriteReport() => Console.WriteLine("Writing report");
}

// Harjoittelija toteuttaa vain relevantit rajapinnat
public class Intern : IWorkable, IFeedable, ISleepable
{
    public void Work() => Console.WriteLine("Working as intern");
    public void Eat() => Console.WriteLine("Eating lunch");
    public void Sleep() => Console.WriteLine("Sleeping at home");
}

// Robotti toteuttaa vain ne rajapinnat, joita se oikeasti käyttää
public class Robot : IWorkable, IReportWriter
{
    public void Work() => Console.WriteLine("Robot working 24/7");
    public void WriteReport() => Console.WriteLine("Generating automated report");
}
```

### Realistisempi esimerkki: Tiedostopalvelu

```csharp
// Huono: Yksi iso rajapinta
public interface IFileManager
{
    void ReadFile(string path);
    void WriteFile(string path, string content);
    void DeleteFile(string path);
    void CompressFile(string path);
    void EncryptFile(string path);
    void UploadToCloud(string path);
}

// Hyvä: Eriytetyt rajapinnat
public interface IFileReader
{
    string ReadFile(string path);
}

public interface IFileWriter
{
    void WriteFile(string path, string content);
    void DeleteFile(string path);
}

public interface IFileCompressor
{
    void CompressFile(string path);
}

public interface IFileEncryptor
{
    void EncryptFile(string path);
}

public interface ICloudUploader
{
    Task UploadToCloud(string path);
}

// Paikallinen tiedostopalvelu — ei tarvitse pilvilataus-toiminnallisuutta
public class LocalFileService : IFileReader, IFileWriter
{
    public string ReadFile(string path) => File.ReadAllText(path);
    public void WriteFile(string path, string content) => File.WriteAllText(path, content);
    public void DeleteFile(string path) => File.Delete(path);
}

// Pilvipalvelu toteuttaa vain sille kuuluvat rajapinnat
public class CloudFileService : IFileReader, IFileWriter, ICloudUploader
{
    public string ReadFile(string path) => File.ReadAllText(path);
    public void WriteFile(string path, string content) => File.WriteAllText(path, content);
    public void DeleteFile(string path) => File.Delete(path);
    public async Task UploadToCloud(string path) 
    {
        // Pilvilataus-logiikka
        await Task.Delay(1000);
    }
}
```

### ISP:n nyrkkisääntö

Jos rajapintaa toteuttava luokka jättää metodeja tyhjiksi tai heittää `NotSupportedException`/`NotImplementedException`-poikkeuksia, rajapinta on liian laaja ja pitäisi pilkkoa pienempiin osiin.

---

## D - Dependency Inversion Principle (DIP)

> *"Ylemmän tason moduulit eivät saa riippua alemman tason moduuleista. Molempien tulee riippua abstraktioista."*

Tämä periaate tarkoittaa, että luokat eivät saa luoda suoraan riippuvuuksiaan, vaan ne saavat ne ulkopuolelta (rajapintojen kautta). Tämä tekee koodista testattavan ja joustavan.

### Huono esimerkki

```csharp
// Alemman tason moduuli
public class SqlDatabase
{
    public void Save(string data)
    {
        Console.WriteLine($"Saving '{data}' to SQL Server...");
    }
}

// Alemman tason moduuli
public class SmtpEmailSender
{
    public void Send(string to, string message)
    {
        Console.WriteLine($"Sending email via SMTP to {to}: {message}");
    }
}

// Ylemmän tason moduuli — riippuu suoraan konkreettisista luokista
public class OrderService
{
    private readonly SqlDatabase _database = new SqlDatabase();
    private readonly SmtpEmailSender _emailSender = new SmtpEmailSender();

    public void PlaceOrder(string order, string customerEmail)
    {
        _database.Save(order);
        _emailSender.Send(customerEmail, $"Order confirmed: {order}");
    }
}
```

Ongelmia:
- `OrderService` on sidottu `SqlDatabase`-luokkaan — entä jos vaihdetaan PostgreSQL:ään?
- `OrderService` on sidottu `SmtpEmailSender`-luokkaan — entä jos käytetään SendGridiä?
- `OrderService` on mahdoton yksikkötestata ilman oikeaa tietokantaa ja sähköpostipalvelinta

### Hyvä esimerkki

```csharp
// Abstraktiot (rajapinnat)
public interface IDatabase
{
    void Save(string data);
}

public interface IEmailSender
{
    void Send(string to, string message);
}

// Alemman tason moduulit toteuttavat rajapinnat
public class SqlDatabase : IDatabase
{
    public void Save(string data)
    {
        Console.WriteLine($"Saving '{data}' to SQL Server...");
    }
}

public class PostgreSqlDatabase : IDatabase
{
    public void Save(string data)
    {
        Console.WriteLine($"Saving '{data}' to PostgreSQL...");
    }
}

public class SmtpEmailSender : IEmailSender
{
    public void Send(string to, string message)
    {
        Console.WriteLine($"SMTP: Sending to {to}: {message}");
    }
}

public class SendGridEmailSender : IEmailSender
{
    public void Send(string to, string message)
    {
        Console.WriteLine($"SendGrid: Sending to {to}: {message}");
    }
}

// Ylemmän tason moduuli riippuu vain abstraktioista
public class OrderService
{
    private readonly IDatabase _database;
    private readonly IEmailSender _emailSender;

    public OrderService(IDatabase database, IEmailSender emailSender)
    {
        _database = database;
        _emailSender = emailSender;
    }

    public void PlaceOrder(string order, string customerEmail)
    {
        _database.Save(order);
        _emailSender.Send(customerEmail, $"Order confirmed: {order}");
    }
}
```

### Käyttö ASP.NET Core:ssa (Dependency Injection)

DIP toteutetaan käytännössä **Dependency Injection** -mekanismilla. ASP.NET Core:ssa tämä tapahtuu `Program.cs`-tiedostossa:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Rekisteröidään riippuvuudet — toteutuksen voi vaihtaa helposti
builder.Services.AddScoped<IDatabase, PostgreSqlDatabase>();
builder.Services.AddScoped<IEmailSender, SendGridEmailSender>();
builder.Services.AddScoped<OrderService>();

var app = builder.Build();
```

Nyt `OrderService` saa automaattisesti oikeat toteutukset konstruktorin kautta, eikä sen tarvitse tietää konkreettisista luokista mitään.

### Yksikkötestaus DIP:n avulla

DIP:n suurin käytännön hyöty on testattavuus:

```csharp
// Testeissä voidaan käyttää mock-toteutuksia
public class FakeDatabase : IDatabase
{
    public List<string> SavedItems { get; } = new();

    public void Save(string data)
    {
        SavedItems.Add(data);
    }
}

public class FakeEmailSender : IEmailSender
{
    public List<(string To, string Message)> SentEmails { get; } = new();

    public void Send(string to, string message)
    {
        SentEmails.Add((to, message));
    }
}

// Yksikkötesti
[Fact]
public void PlaceOrder_SavesOrderAndSendsEmail()
{
    // Arrange
    var fakeDb = new FakeDatabase();
    var fakeEmail = new FakeEmailSender();
    var service = new OrderService(fakeDb, fakeEmail);

    // Act
    service.PlaceOrder("Laptop", "asiakas@email.com");

    // Assert
    Assert.Single(fakeDb.SavedItems);
    Assert.Equal("Laptop", fakeDb.SavedItems[0]);
    Assert.Single(fakeEmail.SentEmails);
    Assert.Equal("asiakas@email.com", fakeEmail.SentEmails[0].To);
}
```

---

## SOLID käytännössä: Kokonainen esimerkki

Alla on esimerkki, jossa kaikki viisi SOLID-periaatetta toteutuvat yhdessä:

```csharp
// === Rajapinnat (ISP) ===
public interface IOrderRepository
{
    void Save(Order order);
    Order GetById(int id);
}

public interface INotificationService
{
    Task NotifyAsync(string recipient, string message);
}

public interface IPriceCalculator
{
    decimal CalculateTotal(Order order);
}

// === Tietomalli (SRP) ===
public class Order
{
    public int Id { get; set; }
    public string CustomerEmail { get; set; }
    public List<OrderItem> Items { get; set; } = new();
    public DateTime CreatedAt { get; set; }
}

public class OrderItem
{
    public string ProductName { get; set; }
    public decimal Price { get; set; }
    public int Quantity { get; set; }
}

// === Hinnanlaskenta (SRP + OCP) ===
public interface IDiscount
{
    decimal Apply(decimal total);
}

public class NoDiscount : IDiscount
{
    public decimal Apply(decimal total) => total;
}

public class PercentageDiscount : IDiscount
{
    private readonly decimal _percentage;

    public PercentageDiscount(decimal percentage)
    {
        _percentage = percentage;
    }

    public decimal Apply(decimal total) => total * (1 - _percentage / 100);
}

public class PriceCalculator : IPriceCalculator
{
    private readonly IDiscount _discount;

    public PriceCalculator(IDiscount discount)
    {
        _discount = discount;
    }

    public decimal CalculateTotal(Order order)
    {
        var subtotal = order.Items.Sum(item => item.Price * item.Quantity);
        return _discount.Apply(subtotal);
    }
}

// === Tilauspalvelu (SRP + DIP) ===
public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly INotificationService _notificationService;
    private readonly IPriceCalculator _priceCalculator;

    public OrderService(
        IOrderRepository repository,
        INotificationService notificationService,
        IPriceCalculator priceCalculator)
    {
        _repository = repository;
        _notificationService = notificationService;
        _priceCalculator = priceCalculator;
    }

    public async Task PlaceOrderAsync(Order order)
    {
        var total = _priceCalculator.CalculateTotal(order);
        order.CreatedAt = DateTime.UtcNow;

        _repository.Save(order);

        await _notificationService.NotifyAsync(
            order.CustomerEmail,
            $"Tilauksesi #{order.Id} on vahvistettu. Summa: {total:C}");
    }
}
```

### Miksi tämä on hyvä?

| Periaate | Toteutus |
|----------|----------|
| **SRP** | Jokaisella luokalla on yksi vastuu (hinnoittelu, tallennus, ilmoitukset) |
| **OCP** | Uusia alennustyyppejä voidaan lisätä ilman olemassa olevan koodin muuttamista |
| **LSP** | Kaikki `IDiscount`-toteutukset toimivat oikein korvattaessa toisiaan |
| **ISP** | Rajapinnat ovat pieniä ja kohdennettuja (ei yhtä "jättirajapintaa") |
| **DIP** | `OrderService` riippuu vain rajapinnoista, ei konkreettisista toteutuksista |

---

## Yhteenveto

| Periaate | Lyhenne | Ydinsanoma |
|----------|---------|------------|
| Single Responsibility | **S** | Yksi luokka, yksi vastuu |
| Open/Closed | **O** | Avoin laajennuksille, suljettu muutoksille |
| Liskov Substitution | **L** | Aliluokka korvaa yläluokan ilman ongelmia |
| Interface Segregation | **I** | Pienet, kohdennetut rajapinnat |
| Dependency Inversion | **D** | Riippu abstraktioista, ei toteutuksista |

### Milloin soveltaa SOLID-periaatteita?

- **Aina kun kirjoitat tuotantokoodia** — SOLID tekee koodista ylläpidettävää
- **Erityisesti tiimityössä** — Muut ymmärtävät koodiasi helpommin
- **Kun koodi kasvaa** — Pienet projektit selviävät ilmankin, mutta kasvaessaan SOLID maksaa itsensä takaisin

### Milloin ei kannata ylisuunnitella?

- Prototyypit ja kokeilut — yksinkertaisuus ensin
- Hyvin pienet sovellukset — SOLID voi tuoda turhaa monimutkaisuutta
- Muista: **KISS** (Keep It Simple, Stupid) ja **YAGNI** (You Aren't Gonna Need It) täydentävät SOLIDia

## Hyödyllisiä linkkejä

- [SOLID Principles in C# - C# Corner](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)
- [Microsoft - Architectural Principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles)
- [Dependency Injection](Dependency-Injection.md)
- [Suunnittelumallit (Design Patterns)](Design-Patterns.md)
- [Suunnitteluperiaatteet (DRY, KISS, YAGNI)](Design-Principles.md)

Seuraavaksi: [Dependency Injection](Dependency-Injection.md)
