# Rajapinnat (Interfaces)

## Mitä rajapinnat ovat?

[Rajapinnat](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/interface) antavat mahdollisuuden määritellä "sopimus", jonka toteuttavat luokat on täytettävä. Toisin kuin perintä, joka kuvaa "on" -suhdetta, rajapinnat usein kuvaavat **"voi tehdä"** -suhteita, esimerkiksi "Lentokone voi lentää". Rajapinnat antavat luokille mahdollisuuden toteuttaa useita toimintoja ilman monen perinnän monimutkaisuutta.

## Perussyntaksi

```csharp
// Rajapinnan määrittely
public interface IInterfaceName
{
    // Metodien, propertyjen, tapahtumien määrittelyt
    void MethodName();
    string PropertyName { get; set; }
}

// Luokan toteutus
public class MyClass : IInterfaceName
{
    // Täytyy toteuttaa kaikki rajapinnan jäsenet
    public void MethodName()
    {
        // Toteutus
    }
    
    public string PropertyName { get; set; }
}
```

## Esimerkki 1: Yksinkertainen rajapinta

```csharp
public interface IDriveable
{
    void StartEngine();
    void StopEngine();
}

public class Car : IDriveable
{
    public void StartEngine()
    {
        Console.WriteLine("Auton moottori käynnistyy");
    }
    
    public void StopEngine()
    {
        Console.WriteLine("Auton moottori sammuu");
    }
}

// Käyttö
IDriveable vehicle = new Car();
vehicle.StartEngine();
vehicle.StopEngine();
```

## Esimerkki 2: Useita rajapintoja

```csharp
public interface IDriveable
{
    void StartEngine();
    void StopEngine();
}

public interface IRefuelable
{
    void Refuel();
}

// ✅ Luokka voi toteuttaa useita rajapintoja
public class Car : IDriveable, IRefuelable
{
    public void StartEngine()
    {
        Console.WriteLine("Auton moottori käynnistyy");
    }
    
    public void StopEngine()
    {
        Console.WriteLine("Auton moottori sammuu");
    }
    
    public void Refuel()
    {
        Console.WriteLine("Tankataan autoa");
    }
}

// Käyttö
Car car = new Car();
IDriveable driveable = car;
IRefuelable refuelable = car;

driveable.StartEngine();
refuelable.Refuel();
driveable.StopEngine();
```

## Miksi rajapintoja käytetään?

### 1. Monimuotoisuus (Polymorphism)

Rajapintojen avulla eri luokkia voidaan käsitellä yhtenäisesti, kunhan ne toteuttavat saman rajapinnan.

```csharp
public interface IShape
{
    double CalculateArea();
    void Draw();
}

public class Circle : IShape
{
    public double Radius { get; set; }
    
    public double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public void Draw()
    {
        Console.WriteLine($"Piirretään ympyrä, säde: {Radius}");
    }
}

public class Rectangle : IShape
{
    public double Width { get; set; }
    public double Height { get; set; }
    
    public double CalculateArea()
    {
        return Width * Height;
    }
    
    public void Draw()
    {
        Console.WriteLine($"Piirretään suorakulmio, {Width}x{Height}");
    }
}

// ✅ Yhtenäinen käsittely eri tyyppisille olioille
public void ProcessShapes(IShape[] shapes)
{
    foreach (IShape shape in shapes)
    {
        shape.Draw();
        Console.WriteLine($"Pinta-ala: {shape.CalculateArea()}");
    }
}

// Käyttö
IShape[] shapes = new IShape[]
{
    new Circle { Radius = 5 },
    new Rectangle { Width = 4, Height = 6 }
};
ProcessShapes(shapes);
```

### 2. Joustavuus ja laajennettavuus

Voit vaihtaa rajapintaa toteuttavia komponentteja ilman, että koodissa oleva muu toiminnallisuus kärsii.

```csharp
public interface IDataStorage
{
    void Save(string data);
    string Load();
}

public class FileStorage : IDataStorage
{
    private string filePath;
    
    public FileStorage(string path)
    {
        filePath = path;
    }
    
    public void Save(string data)
    {
        File.WriteAllText(filePath, data);
    }
    
    public string Load()
    {
        return File.ReadAllText(filePath);
    }
}

public class DatabaseStorage : IDataStorage
{
    public void Save(string data)
    {
        // Toteutus tietokantaan tallentamiseen
        Console.WriteLine("Tallennetaan tietokantaan...");
    }
    
    public string Load()
    {
        // Toteutus tietokannasta lukemiseen
        Console.WriteLine("Luetaan tietokannasta...");
        return "Data tietokannasta";
    }
}

// ✅ Sama koodi toimii molemmilla toteutuksilla
public class DataManager
{
    private IDataStorage storage;
    
    public DataManager(IDataStorage storage)
    {
        this.storage = storage;
    }
    
    public void SaveData(string data)
    {
        storage.Save(data);
    }
}

// Käyttö - helppo vaihtaa toteutus!
DataManager manager1 = new DataManager(new FileStorage("data.txt"));
DataManager manager2 = new DataManager(new DatabaseStorage());
```

### 3. Moniperintä

Koska C# ei tue luokkien moniperintää, rajapintoja voidaan käyttää saavuttamaan samankaltainen vaikutus.

```csharp
public interface IFlyable
{
    void Fly();
}

public interface ISwimmable
{
    void Swim();
}

public interface IWalkable
{
    void Walk();
}

// ✅ Luokka voi toteuttaa useita rajapintoja
public class Duck : IFlyable, ISwimmable, IWalkable
{
    public void Fly()
    {
        Console.WriteLine("Ankka lentää");
    }
    
    public void Swim()
    {
        Console.WriteLine("Ankka ui");
    }
    
    public void Walk()
    {
        Console.WriteLine("Ankka kävelee");
    }
}

// Käyttö
Duck duck = new Duck();
IFlyable flyable = duck;
ISwimmable swimmable = duck;
IWalkable walkable = duck;

flyable.Fly();
swimmable.Swim();
walkable.Walk();
```

## Muita huomioita

- Rajapinnoissa ei voi olla jäsenmuuttujia, mutta niissä voi olla [propertyjä](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/properties) (ominaisuuksia)
- Rajapinnoissa ei voi olla määritettyjä konstruktoreita, koska ne eivät sisällä toteutusta tosin kuin luokat
- Yhdessä luokassa voidaan toteuttaa monta rajapintaa, mutta perintä voi tapahtua vain yhdestä yläluokasta

### Esimerkki: Rajapinta propertyillä

```csharp
public interface IVehicle
{
    string Brand { get; set; }  // Property on sallittu
    int Speed { get; }          // Vain luku
    void Accelerate();
    void Brake();
}

public class Car : IVehicle
{
    public string Brand { get; set; }
    public int Speed { get; private set; }
    
    public void Accelerate()
    {
        Speed += 10;
        Console.WriteLine($"Nopeus kasvaa: {Speed} km/h");
    }
    
    public void Brake()
    {
        Speed = Math.Max(0, Speed - 10);
        Console.WriteLine($"Jarrutetaan: {Speed} km/h");
    }
}
```

## Mitä yleisiä tekniikoita rajapinnat mahdollistavat?

Rajapinnat ovat keskeisiä ohjelmistosuunnittelun periaatteiden ja suunnittelumallien (design patterns) toteuttamisessa. Ne mahdollistavat useita tekniikoita ja malleja, jotka parantavat ohjelmistojen joustavuutta, laajennettavuutta ja ylläpidettävyyttä.

### 1. Dependency Inversion Principle (DIP)

Tämä on yksi [SOLID](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)-periaatteista. Sen sijaan, että korkean tason moduulit olisivat riippuvaisia alhaisen tason moduuleista, molempien tulisi olla riippuvaisia abstraktioista (esim. rajapinnoista).

```csharp
// ❌ HUONO: Riippuvuus konkreettisesta luokasta
public class OrderService
{
    private FileLogger logger = new FileLogger(); // Riippuvuus!
}

// ✅ HYVÄ: Riippuvuus abstraktiosta
public interface ILogger
{
    void Log(string message);
}

public class OrderService
{
    private ILogger logger; // Riippuvuus rajapintaan
    
    public OrderService(ILogger logger)
    {
        this.logger = logger; // Dependency Injection
    }
}
```

### 2. Strategy Pattern

Suunnittelumalli, joka mahdollistaa algoritmin valinnan lennossa.

```csharp
public interface IPaymentStrategy
{
    void Pay(decimal amount);
}

public class CreditCardPayment : IPaymentStrategy
{
    public void Pay(decimal amount)
    {
        Console.WriteLine($"Maksettu {amount} euroa luottokortilla");
    }
}

public class PayPalPayment : IPaymentStrategy
{
    public void Pay(decimal amount)
    {
        Console.WriteLine($"Maksettu {amount} euroa PayPalilla");
    }
}

public class PaymentProcessor
{
    private IPaymentStrategy strategy;
    
    public void SetStrategy(IPaymentStrategy strategy)
    {
        this.strategy = strategy;
    }
    
    public void ProcessPayment(decimal amount)
    {
        strategy.Pay(amount);
    }
}
```

### 3. Dependency Injection

Tekniikka, jossa luokan riippuvuudet syötetään luokalle sen sijaan, että luokka loisi ne itse.

```csharp
public interface IEmailService
{
    void SendEmail(string to, string subject, string body);
}

public class SmtpEmailService : IEmailService
{
    public void SendEmail(string to, string subject, string body)
    {
        // SMTP-toteutus
        Console.WriteLine($"Lähetetään sähköposti: {subject} -> {to}");
    }
}

public class UserService
{
    private IEmailService emailService;
    
    // Dependency Injection konstruktorissa
    public UserService(IEmailService emailService)
    {
        this.emailService = emailService;
    }
    
    public void RegisterUser(string email)
    {
        // Rekisteröinti-logiikka
        emailService.SendEmail(email, "Tervetuloa!", "Rekisteröityminen onnistui");
    }
}
```

## Yhteenveto

Rajapinnat ovat keskeisiä C#-ohjelmoinnin OOP-ominaisuuksia, jotka edistävät löyhää kytkentää ja koodin uudelleenkäyttöä. Ne mahdollistavat monia tekniikoita ja malleja, joilla pyritään tekemään ohjelmistoista joustavampia, ylläpidettävämpiä ja testattavampia.

