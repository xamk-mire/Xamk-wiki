# Rajapinnat (Interfaces)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mitä rajapinnat ovat?](#mitä-rajapinnat-ovat)
3. [Ongelma joka ratkaistaan](#ongelma-joka-ratkaistaan)
4. [Perussyntaksi](#perussyntaksi)
5. [Rajapinnat vs Abstraktit luokat](#rajapinnat-vs-abstraktit-luokat)
6. [Useita rajapintoja](#useita-rajapintoja)
7. [Interface Segregation](#interface-segregation)
8. [Dependency Injection](#dependency-injection)
9. [Käytännön esimerkit](#käytännön-esimerkit)
10. [Design Patterns rajapinnoilla](#design-patterns-rajapinnoilla)
11. [Best Practices](#best-practices)
12. [Yleiset virheet](#yleiset-virheet)
13. [Yhteenveto](#yhteenveto)

---

## Johdanto

Rajapinnat (Interfaces) ovat yksi tärkeimmistä työkaluista modernissa ohjelmistokehityksessä. Ne määrittelevät **sopimuksen** (contract) mitä luokan on toteutettava.

**Lyhyesti:** Rajapinta on lista metodeista, propertyjä ja tapahtumista **ilman toteutusta**. Se kertoo "MITÄ" tehdään, mutta ei "MITEN".

**Analogia:** Rajapinta on kuin sähköpistorasian standardi - se määrittelee minkä muotoinen pistoke sopii, mutta ei välitä mistä sähkö tulee.

---

## Mitä rajapinnat ovat?

Rajapinta määrittelee:
- ✅ **Metodien signatuurit** (nimi, parametrit, paluuarvo)
- ✅ **Propertyt** (get/set)
- ✅ **Tapahtumat** (events)
- ✅ **Indekserit** (indexers)

Rajapinta **EI** määrittele:
- ❌ Toteutusta (implementation)
- ❌ Kenttiä (fields)
- ❌ Konstruktoreja
- ❌ Access modifiereitä (kaikki on implisiittisesti public)

```csharp
// Yksinkertainen rajapinta
public interface IAnimal
{
    // Metodit (ei toteutusta!)
    void MakeSound();
    void Eat();
    
    // Propertyt
    string Name { get; set; }
    int Age { get; }
    
    // C# 8.0+: Default toteutus (optional)
    void Sleep()
    {
        Console.WriteLine($"{Name} nukkuu");
    }
}

// Luokka toteuttaa rajapinnan
public class Dog : IAnimal
{
    public string Name { get; set; }
    public int Age { get; private set; }
    
    // PAKKO toteuttaa rajapinnan metodit
    public void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
    
    public void Eat()
    {
        Console.WriteLine($"{Name} syö koiraruokaa");
    }
    
    // Sleep() on optional (on default toteutus)
}
```

---

## Ongelma joka ratkaistaan

### Ilman rajapintoja (ongelma)

```csharp
// ❌ HUONO: Riippuvuus konkreettisesta luokasta
public class EmailService
{
    private SmtpClient smtpClient; // Sidottu yhteen toteutukseen!
    
    public EmailService()
    {
        smtpClient = new SmtpClient(); // Vaikea testata!
    }
    
    public void SendEmail(string to, string subject, string body)
    {
        smtpClient.Send(to, subject, body);
    }
}

// Ongelmat:
// 1. Ei voi vaihtaa SMTP:stä johonkin muuhun helposti
// 2. Vaikea testata (tarvitsee oikean SMTP-palvelimen)
// 3. EmailService on sidottu SmtpClient:iin (tight coupling)
```

### Rajapintojen avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Riippuvuus abstraktioon (rajapintaan)
public interface IEmailSender
{
    void SendEmail(string to, string subject, string body);
    Task SendEmailAsync(string to, string subject, string body);
}

// Toteutus 1: SMTP
public class SmtpEmailSender : IEmailSender
{
    private string smtpServer;
    
    public SmtpEmailSender(string server)
    {
        smtpServer = server;
    }
    
    public void SendEmail(string to, string subject, string body)
    {
        Console.WriteLine($"Lähetetään SMTP:llä ({smtpServer}): {subject} -> {to}");
        // Todellinen SMTP-logiikka...
    }
    
    public async Task SendEmailAsync(string to, string subject, string body)
    {
        await Task.Run(() => SendEmail(to, subject, body));
    }
}

// Toteutus 2: SendGrid API
public class SendGridEmailSender : IEmailSender
{
    private string apiKey;
    
    public SendGridEmailSender(string key)
    {
        apiKey = key;
    }
    
    public void SendEmail(string to, string subject, string body)
    {
        Console.WriteLine($"Lähetetään SendGrid API:lla: {subject} -> {to}");
        // SendGrid API kutsu...
    }
    
    public async Task SendEmailAsync(string to, string subject, string body)
    {
        await Task.Run(() => SendEmail(to, subject, body));
    }
}

// Toteutus 3: Console (testaukseen)
public class ConsoleEmailSender : IEmailSender
{
    public void SendEmail(string to, string subject, string body)
    {
        Console.WriteLine($"[TEST EMAIL]");
        Console.WriteLine($"To: {to}");
        Console.WriteLine($"Subject: {subject}");
        Console.WriteLine($"Body: {body}");
    }
    
    public async Task SendEmailAsync(string to, string subject, string body)
    {
        await Task.Run(() => SendEmail(to, subject, body));
    }
}

// EmailService nyt joustava!
public class EmailService
{
    private readonly IEmailSender emailSender; // Rajapinta!
    
    // Dependency Injection - saamme toteutuksen ulkopuolelta
    public EmailService(IEmailSender sender)
    {
        emailSender = sender;
    }
    
    public void SendWelcomeEmail(string to, string name)
    {
        string subject = $"Tervetuloa, {name}!";
        string body = $"Hei {name}, tervetuloa palveluumme!";
        emailSender.SendEmail(to, subject, body);
    }
}

// Käyttö - helppo vaihtaa toteutusta!
// Tuotannossa:
IEmailSender productionSender = new SmtpEmailSender("smtp.example.com");
EmailService emailService1 = new EmailService(productionSender);

// Testauksessa:
IEmailSender testSender = new ConsoleEmailSender();
EmailService emailService2 = new EmailService(testSender);

// Vaihtoehtoisesti:
IEmailSender sendGridSender = new SendGridEmailSender("api-key-123");
EmailService emailService3 = new EmailService(sendGridSender);
```

**Hyödyt:**
- ✅ Helppo vaihtaa toteutusta
- ✅ Helppo testata (mock-objektit)
- ✅ Löyhä kytkentä (loose coupling)
- ✅ Noudattaa Dependency Inversion Principle

---

## Perussyntaksi

### Perusrajapinta

```csharp
// Nimeämiskäytäntö: I + PascalCase
public interface IShape
{
    // Metodit
    double CalculateArea();
    double CalculatePerimeter();
    void Draw();
    
    // Propertyt
    string Name { get; set; }
    string Color { get; set; }
    
    // Read-only property
    int Id { get; }
}

// Toteutus
public class Circle : IShape
{
    private static int nextId = 1;
    
    public double Radius { get; set; }
    
    // IShape toteutus
    public string Name { get; set; }
    public string Color { get; set; }
    public int Id { get; }
    
    public Circle(double radius)
    {
        Radius = radius;
        Id = nextId++;
    }
    
    public double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public double CalculatePerimeter()
    {
        return 2 * Math.PI * Radius;
    }
    
    public void Draw()
    {
        Console.WriteLine($"Piirretään {Color} ympyrä '{Name}', säde: {Radius}");
    }
}
```

### Rajapinnan perintä

```csharp
// Rajapinnat voivat periä toisia rajapintoja
public interface IDrawable
{
    void Draw();
}

public interface IResizable
{
    void Resize(double scale);
}

// Yhdistetty rajapinta
public interface IGraphicObject : IDrawable, IResizable
{
    void Move(int x, int y);
    int X { get; set; }
    int Y { get; set; }
}

// Toteutus
public class Shape : IGraphicObject
{
    public int X { get; set; }
    public int Y { get; set; }
    
    // IDrawable
    public void Draw()
    {
        Console.WriteLine($"Piirretään kohtaan ({X}, {Y})");
    }
    
    // IResizable
    public void Resize(double scale)
    {
        Console.WriteLine($"Skaalataan {scale}x");
    }
    
    // IGraphicObject
    public void Move(int x, int y)
    {
        X = x;
        Y = y;
        Console.WriteLine($"Siirretty kohtaan ({X}, {Y})");
    }
}
```

---

## Rajapinnat vs Abstraktit luokat

| Ominaisuus | Interface | Abstract Class |
|------------|-----------|----------------|
| **Useita** | ✅ Luokka voi toteuttaa useita | ❌ Vain yksi yläluokka |
| **Toteutus** | ❌ Ei toteutusta (paitsi default C# 8+) | ✅ Voi olla toteutus |
| **Kentät** | ❌ Ei kenttiä | ✅ Voi olla kenttiä |
| **Konstruktori** | ❌ Ei konstruktoria | ✅ Voi olla konstruktori |
| **Access modifiers** | ❌ Kaikki public | ✅ Voi olla private, protected, jne |
| **Käyttötarkoitus** | "Can-do" suhteet | "Is-a" suhteet |
| **Esimerkki** | `IFlyable`, `ISwimmable` | `Animal`, `Vehicle` |

### Milloin käyttää mitäkin?

```csharp
// ✅ Käytä RAJAPINTAA kun:
// - Haluat määritellä "can-do" suhteen
// - Haluat sallialuokan toteuttaa useita ominaisuuksia
// - Haluat löyhän kytkennän

public interface IFlyable
{
    void Fly();
    double MaxAltitude { get; }
}

public interface ISwimmable
{
    void Swim();
    double MaxDepth { get; }
}

// Ankka voi lentää JA uida
public class Duck : IFlyable, ISwimmable
{
    public void Fly() => Console.WriteLine("Ankka lentää");
    public double MaxAltitude => 100;
    
    public void Swim() => Console.WriteLine("Ankka ui");
    public double MaxDepth => 5;
}

// ✅ Käytä ABSTRAKTIA LUOKKAA kun:
// - Haluat jakaa yhteistä koodia
// - Haluat määritellä "is-a" suhteen
// - Tarvitset kenttiä tai konstruktoreita

public abstract class Animal
{
    // Yhteiset kentät
    protected string name;
    protected int age;
    
    // Konstruktori
    protected Animal(string name, int age)
    {
        this.name = name;
        this.age = age;
    }
    
    // Yhteinen toteutus
    public void Eat()
    {
        Console.WriteLine($"{name} syö");
    }
    
    // Abstrakti metodi
    public abstract void MakeSound();
}
```

---

## Useita rajapintoja

C# ei tue moniperintää luokille, mutta **rajapinnoilla voit toteuttaa useita**.

```csharp
// Eri kyvyt omissa rajapinnoissaan
public interface IFlyable
{
    void Fly();
    void Land();
}

public interface ISwimmable
{
    void Swim();
    void Dive();
}

public interface IWalkable
{
    void Walk();
    void Run();
}

// Ihminen voi kävellä ja uida
public class Human : IWalkable, ISwimmable
{
    public string Name { get; set; }
    
    public void Walk()
    {
        Console.WriteLine($"{Name} kävelee");
    }
    
    public void Run()
    {
        Console.WriteLine($"{Name} juoksee");
    }
    
    public void Swim()
    {
        Console.WriteLine($"{Name} ui");
    }
    
    public void Dive()
    {
        Console.WriteLine($"{Name} sukeltaa");
    }
}

// Ankka voi tehdä kaikkea!
public class Duck : IFlyable, ISwimmable, IWalkable
{
    public string Name { get; set; }
    
    public void Fly() => Console.WriteLine($"{Name} lentää");
    public void Land() => Console.WriteLine($"{Name} laskeutuu");
    
    public void Swim() => Console.WriteLine($"{Name} ui");
    public void Dive() => Console.WriteLine($"{Name} sukeltaa");
    
    public void Walk() => Console.WriteLine($"{Name} kävelee");
    public void Run() => Console.WriteLine($"{Name} juoksee (hitaasti)");
}

// Lentokone voi vain lentää
public class Airplane : IFlyable
{
    public string Model { get; set; }
    
    public void Fly() => Console.WriteLine($"{Model} lentää");
    public void Land() => Console.WriteLine($"{Model} laskeutuu");
}

// Polymorfismi toimii:
public class TransportManager
{
    public void MakeFlyersLand(List<IFlyable> flyers)
    {
        foreach (IFlyable flyer in flyers)
        {
            flyer.Land();
        }
    }
    
    public void MakeSwimmersSwim(List<ISwimmable> swimmers)
    {
        foreach (ISwimmable swimmer in swimmers)
        {
            swimmer.Swim();
        }
    }
}

// Käyttö:
Duck duck = new Duck { Name = "Donald" };
Airplane plane = new Airplane { Model = "Boeing 747" };
Human human = new Human { Name = "Matti" };

List<IFlyable> flyers = new List<IFlyable> { duck, plane };
List<ISwimmable> swimmers = new List<ISwimmable> { duck, human };

TransportManager manager = new TransportManager();
manager.MakeFlyersLand(flyers);
manager.MakeSwimmersSwim(swimmers);
```

---

## Interface Segregation

**Interface Segregation Principle (ISP):** Älä pakota luokkaa toteuttamaan metodeja joita se ei tarvitse.

### ❌ Huono: Liian iso rajapinta

```csharp
// ❌ HUONO: "God Interface" - liian monta metodia
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
    void TakeBreak();
    void AttendMeeting();
    void SendEmail();
    void MakePhoneCall();
}

// Robot joutuu toteuttamaan metodit joita se ei tarvitse!
public class Robot : IWorker
{
    public void Work() { /* OK */ }
    public void Eat() { throw new NotImplementedException(); } // ❌
    public void Sleep() { throw new NotImplementedException(); } // ❌
    public void TakeBreak() { throw new NotImplementedException(); } // ❌
    public void AttendMeeting() { /* OK */ }
    public void SendEmail() { /* OK */ }
    public void MakePhoneCall() { /* OK */ }
}
```

### ✅ Hyvä: Pienet, keskittyneet rajapinnat

```csharp
// ✅ HYVÄ: Pilkottu pienempiin osiin
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

public interface ICommunicator
{
    void SendEmail();
    void MakePhoneCall();
}

// Ihminen toteuttaa kaiken
public class Human : IWorkable, IFeedable, ISleepable, ICommunicator
{
    public void Work() { Console.WriteLine("Työskentelee"); }
    public void Eat() { Console.WriteLine("Syö"); }
    public void Sleep() { Console.WriteLine("Nukkuu"); }
    public void SendEmail() { Console.WriteLine("Lähettää sähköpostia"); }
    public void MakePhoneCall() { Console.WriteLine("Soittaa puhelun"); }
}

// Robot toteuttaa vain tarvitsemansa
public class Robot : IWorkable, ICommunicator
{
    public void Work() { Console.WriteLine("Työskentelee 24/7"); }
    public void SendEmail() { Console.WriteLine("Lähettää automaattisen viestin"); }
    public void MakePhoneCall() { Console.WriteLine("Automaattinen puhelinrobotti"); }
    // Ei Eat() eikä Sleep() - ei tarvitse!
}
```

---

## Dependency Injection

Rajapinnat ovat keskeisiä Dependency Injection -mallissa.

### Esimerkki: Logging

```csharp
// Rajapinta
public interface ILogger
{
    void LogInfo(string message);
    void LogWarning(string message);
    void LogError(string message, Exception ex);
}

// Toteutus 1: Console
public class ConsoleLogger : ILogger
{
    public void LogInfo(string message)
    {
        Console.ForegroundColor = ConsoleColor.White;
        Console.WriteLine($"[INFO] {message}");
        Console.ResetColor();
    }
    
    public void LogWarning(string message)
    {
        Console.ForegroundColor = ConsoleColor.Yellow;
        Console.WriteLine($"[WARNING] {message}");
        Console.ResetColor();
    }
    
    public void LogError(string message, Exception ex)
    {
        Console.ForegroundColor = ConsoleColor.Red;
        Console.WriteLine($"[ERROR] {message}: {ex.Message}");
        Console.ResetColor();
    }
}

// Toteutus 2: File
public class FileLogger : ILogger
{
    private string filePath;
    
    public FileLogger(string path)
    {
        filePath = path;
    }
    
    public void LogInfo(string message)
    {
        File.AppendAllText(filePath, $"[INFO] {DateTime.Now}: {message}\n");
    }
    
    public void LogWarning(string message)
    {
        File.AppendAllText(filePath, $"[WARNING] {DateTime.Now}: {message}\n");
    }
    
    public void LogError(string message, Exception ex)
    {
        File.AppendAllText(filePath, $"[ERROR] {DateTime.Now}: {message} - {ex.Message}\n");
    }
}

// Toteutus 3: Null (ei lokitusta)
public class NullLogger : ILogger
{
    public void LogInfo(string message) { }
    public void LogWarning(string message) { }
    public void LogError(string message, Exception ex) { }
}

// Käyttö: UserService riippuu ILogger-rajapinnasta
public class UserService
{
    private readonly ILogger logger;
    
    // Dependency Injection konstruktorissa
    public UserService(ILogger logger)
    {
        this.logger = logger;
    }
    
    public void CreateUser(string username, string email)
    {
        try
        {
            logger.LogInfo($"Luodaan käyttäjä: {username}");
            
            // Käyttäjän luontilogiikka...
            
            logger.LogInfo($"Käyttäjä {username} luotu onnistuneesti");
        }
        catch (Exception ex)
        {
            logger.LogError($"Käyttäjän {username} luonti epäonnistui", ex);
            throw;
        }
    }
}

// Käyttö - helppo vaihtaa logger:ia
// Kehityksessä:
ILogger devLogger = new ConsoleLogger();
UserService userService1 = new UserService(devLogger);

// Tuotannossa:
ILogger prodLogger = new FileLogger("application.log");
UserService userService2 = new UserService(prodLogger);

// Testauksessa:
ILogger testLogger = new NullLogger();
UserService userService3 = new UserService(testLogger);
```

---

## Käytännön esimerkit

### Esimerkki 1: Datan tallennus

```csharp
// Repository Pattern
public interface IRepository<T> where T : class
{
    T GetById(int id);
    IEnumerable<T> GetAll();
    void Add(T entity);
    void Update(T entity);
    void Delete(int id);
}

// SQL-toteutus
public class SqlRepository<T> : IRepository<T> where T : class
{
    private string connectionString;
    
    public SqlRepository(string connStr)
    {
        connectionString = connStr;
    }
    
    public T GetById(int id)
    {
        Console.WriteLine($"SQL: Haetaan {typeof(T).Name} ID:llä {id}");
        // SQL-logiikka...
        return null;
    }
    
    public IEnumerable<T> GetAll()
    {
        Console.WriteLine($"SQL: Haetaan kaikki {typeof(T).Name}");
        return new List<T>();
    }
    
    public void Add(T entity)
    {
        Console.WriteLine($"SQL: Lisätään {typeof(T).Name}");
    }
    
    public void Update(T entity)
    {
        Console.WriteLine($"SQL: Päivitetään {typeof(T).Name}");
    }
    
    public void Delete(int id)
    {
        Console.WriteLine($"SQL: Poistetaan {typeof(T).Name} ID:llä {id}");
    }
}

// MongoDB-toteutus
public class MongoRepository<T> : IRepository<T> where T : class
{
    private string databaseName;
    
    public MongoRepository(string dbName)
    {
        databaseName = dbName;
    }
    
    public T GetById(int id)
    {
        Console.WriteLine($"MongoDB: Haetaan {typeof(T).Name} ID:llä {id}");
        return null;
    }
    
    public IEnumerable<T> GetAll()
    {
        Console.WriteLine($"MongoDB: Haetaan kaikki {typeof(T).Name}");
        return new List<T>();
    }
    
    public void Add(T entity)
    {
        Console.WriteLine($"MongoDB: Lisätään {typeof(T).Name}");
    }
    
    public void Update(T entity)
    {
        Console.WriteLine($"MongoDB: Päivitetään {typeof(T).Name}");
    }
    
    public void Delete(int id)
    {
        Console.WriteLine($"MongoDB: Poistetaan {typeof(T).Name} ID:llä {id}");
    }
}

// Domain model
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}

// Service käyttää rajapintaa
public class UserService
{
    private readonly IRepository<User> repository;
    
    public UserService(IRepository<User> repo)
    {
        repository = repo;
    }
    
    public void RegisterUser(string name, string email)
    {
        User user = new User { Name = name, Email = email };
        repository.Add(user);
    }
    
    public User GetUser(int id)
    {
        return repository.GetById(id);
    }
}

// Käyttö - helppo vaihtaa tietokantaa
IRepository<User> sqlRepo = new SqlRepository<User>("Server=...;Database=...");
IRepository<User> mongoRepo = new MongoRepository<User>("mongodb://localhost");

UserService service1 = new UserService(sqlRepo);    // SQL
UserService service2 = new UserService(mongoRepo);  // MongoDB
```

### Esimerkki 2: Maksujen käsittely (Strategy Pattern)

```csharp
public interface IPaymentStrategy
{
    bool ProcessPayment(decimal amount);
    string GetPaymentMethodName();
}

public class CreditCardPayment : IPaymentStrategy
{
    private string cardNumber;
    
    public CreditCardPayment(string number)
    {
        cardNumber = number;
    }
    
    public bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Maksetaan {amount:C} luottokortilla (**** {cardNumber.Substring(cardNumber.Length - 4)})");
        return true;
    }
    
    public string GetPaymentMethodName() => "Luottokortti";
}

public class PayPalPayment : IPaymentStrategy
{
    private string email;
    
    public PayPalPayment(string email)
    {
        this.email = email;
    }
    
    public bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Maksetaan {amount:C} PayPal:lla ({email})");
        return true;
    }
    
    public string GetPaymentMethodName() => "PayPal";
}

public class MobilePayPayment : IPaymentStrategy
{
    private string phoneNumber;
    
    public MobilePayPayment(string phone)
    {
        phoneNumber = phone;
    }
    
    public bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Maksetaan {amount:C} MobilePay:llä ({phoneNumber})");
        return true;
    }
    
    public string GetPaymentMethodName() => "MobilePay";
}

// Checkout käyttää Strategy-patternia
public class Checkout
{
    private IPaymentStrategy paymentStrategy;
    private decimal totalAmount;
    
    public void SetPaymentStrategy(IPaymentStrategy strategy)
    {
        paymentStrategy = strategy;
    }
    
    public void AddItem(decimal price)
    {
        totalAmount += price;
    }
    
    public void ProcessCheckout()
    {
        if (paymentStrategy == null)
        {
            Console.WriteLine("Valitse maksutapa!");
            return;
        }
        
        Console.WriteLine($"Maksutapa: {paymentStrategy.GetPaymentMethodName()}");
        Console.WriteLine($"Summa: {totalAmount:C}");
        
        if (paymentStrategy.ProcessPayment(totalAmount))
        {
            Console.WriteLine("Maksu onnistui!");
            totalAmount = 0;
        }
        else
        {
            Console.WriteLine("Maksu epäonnistui!");
        }
    }
}

// Käyttö:
Checkout checkout = new Checkout();
checkout.AddItem(29.99m);
checkout.AddItem(15.50m);
checkout.AddItem(8.95m);

// Asiakas valitsee maksutavan
checkout.SetPaymentStrategy(new CreditCardPayment("1234567890123456"));
// TAI
// checkout.SetPaymentStrategy(new PayPalPayment("user@example.com"));
// TAI
// checkout.SetPaymentStrategy(new MobilePayPayment("+358401234567"));

checkout.ProcessCheckout();
```

---

## Design Patterns rajapinnoilla

### 1. Factory Pattern

```csharp
public interface IVehicle
{
    void Drive();
    string GetVehicleType();
}

public class Car : IVehicle
{
    public void Drive() => Console.WriteLine("Ajataan autolla");
    public string GetVehicleType() => "Auto";
}

public class Motorcycle : IVehicle
{
    public void Drive() => Console.WriteLine("Ajataan moottoripyörällä");
    public string GetVehicleType() => "Moottoripyörä";
}

// Factory
public interface IVehicleFactory
{
    IVehicle CreateVehicle();
}

public class CarFactory : IVehicleFactory
{
    public IVehicle CreateVehicle() => new Car();
}

public class MotorcycleFactory : IVehicleFactory
{
    public IVehicle CreateVehicle() => new Motorcycle();
}
```

### 2. Observer Pattern

```csharp
public interface IObserver
{
    void Update(string message);
}

public interface ISubject
{
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void Notify(string message);
}

public class NewsAgency : ISubject
{
    private List<IObserver> observers = new List<IObserver>();
    
    public void Attach(IObserver observer)
    {
        observers.Add(observer);
    }
    
    public void Detach(IObserver observer)
    {
        observers.Remove(observer);
    }
    
    public void Notify(string message)
    {
        foreach (IObserver observer in observers)
        {
            observer.Update(message);
        }
    }
    
    public void PublishNews(string news)
    {
        Console.WriteLine($"Uutistoimisto: {news}");
        Notify(news);
    }
}

public class NewsChannel : IObserver
{
    private string name;
    
    public NewsChannel(string channelName)
    {
        name = channelName;
    }
    
    public void Update(string message)
    {
        Console.WriteLine($"{name} vastaanotti: {message}");
    }
}
```

---

## Best Practices

### ✅ DO (Tee näin):

1. **Nimeä rajapinnat I-prefiksillä**
```csharp
public interface IRepository { }  // ✅
public interface ILogger { }      // ✅
```

2. **Pidä rajapinnat pieninä (ISP)**
```csharp
public interface IReadable
{
    string Read();
}

public interface IWritable
{
    void Write(string data);
}
```

3. **Käytä kuvaavia nimiä**
```csharp
public interface IFlyable { }     // ✅ Kertoomitkä luokat voivat lentää
public interface ISaveable { }    // ✅ Kertoo mitä luokat voivat tallentaa
```

4. **Suunnittele rajapinnat stabiileiksi**
```csharp
// Älä muuta rajapintaa jatkuvasti - rikkoo toteutukset
```

5. **Dokumentoi rajapinnat hyvin**
```csharp
/// <summary>
/// Määrittelee metodit datan tallentamiseen.
/// Toteutukset voivat käyttää tietokantaa, tiedostoja, tms.
/// </summary>
public interface IDataStorage
{
    /// <summary>
    /// Tallentaa datan. Heittää IOException jos tallennus epäonnistuu.
    /// </summary>
    void Save(string data);
}
```

### ❌ DON'T (Älä tee näin):

1. **Älä tee liian isoja rajapintoja**
```csharp
// ❌ HUONO - 20 metodia yhdessä rajapinnassa
public interface IGodInterface
{
    void Method1();
    void Method2();
    // ... 18 muuta ...
}
```

2. **Älä laita toteutusta rajapintaan (paitsi default C# 8+)**
```csharp
// ❌ Yleensä EI (paitsi C# 8+ default toteutus)
public interface IBad
{
    void Method()
    {
        // Toteutus...
    }
}
```

3. **Älä unohda noudattaa rajapinnan sopimusta**
```csharp
// ❌ HUONO - Rikkoo sopimuksen
public interface ISaveable
{
    bool Save(); // Palauttaa true jos onnistui
}

public class Bad : ISaveable
{
    public bool Save()
    {
        return false; // Palauttaa aina false - rikkoo odotuksen!
    }
}
```

---

## Yleiset virheet

### Virhe 1: Rajapinta jossa on toteutus (ennen C# 8)

```csharp
// ❌ EI TOIMI (ennen C# 8)
public interface IBad
{
    void Method()
    {
        Console.WriteLine("Toteutus");
    }
}

// ✅ C# 8+ default toteutus (valinnainen)
public interface IGood
{
    void Method()
    {
        Console.WriteLine("Default toteutus");
    }
}
```

### Virhe 2: Unohtaa toteuttaa jotain

```csharp
public interface IExample
{
    void Method1();
    void Method2();
    void Method3();
}

// ❌ EI KÄÄNNY - puuttuu Method3
public class Bad : IExample
{
    public void Method1() { }
    public void Method2() { }
    // Method3 puuttuu!
}
```

### Virhe 3: Liian iso rajapinta

```csharp
// ❌ Rikkoo Interface Segregation Principle
public interface IWorker
{
    void Work();
    void Eat();      // Robotti ei syö
    void Sleep();    // Robotti ei nuku
    void Code();
}
```

---

## Yhteenveto

Rajapinnat ovat yksi tärkeimmistä työkaluista modernissa ohjelmistokehityksessä.

### Muista:
- ✅ Rajapinnat määrittelevät **"MITÄ"** ei **"MITEN"**
- ✅ Luokka voi toteuttaa **useita** rajapintoja
- ✅ Käytä **Interface Segregation** - pidä rajapinnat pieninä
- ✅ **Dependency Injection** - injektoi rajapintoja
- ✅ Nimeä **I**-prefiksillä (ILogger, IRepository)
- ✅ Suunnittele stabiiliksi - älä muuta usein

### Rajapinnat mahdollistavat:
- **Plug-and-play** arkkitehtuurin
- **Testattavuuden** (mock-objektit)
- **Joustavuuden** (vaihda toteutusta)
- **Löyhän kytkennän** (loose coupling)
- **SOLID-periaatteiden** noudattamisen

**Seuraava askel:** Kun hallitset rajapinnat, jatka [Yhdistäminen (Composition)](Composition.md) materiaaliin, joka näyttää miten rakentaa järjestelmiä osista.

---

