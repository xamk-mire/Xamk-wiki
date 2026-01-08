# Suunnittelu periaatteet (Design Principles)

Eri suunnittelu periaatteet ohjelmoinnissa viittaavat yleisiin ohjeisiin ja käytäntöihin, jotka auttavat ohjelmoijia luomaan tehokkaita, ylläpidettäviä ja laadukkaita ohjelmistoja. Vaikka periaatteet voivat vaihdella kontekstista riippuen, tässä on joitakin yleisiä ohjelmoinnin design-periaatteita.

**Suosittelen tutustumaan SOLID-periaatteisiin eniten.** Löydät [täältä](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/) hyvät esimerkit ja selitykset kullekkin periaatteelle.

## Yleisimmät käytänteet

### 1. DRY (Don't Repeat Yourself)

Vältä koodin toistamista. Kun sama koodinpätkä toistuu useissa paikoissa, se voi olla merkki siitä, että sinun pitäisi eristää se yhteen paikkaan, esimerkiksi funktioon tai luokkaan.

**Esimerkki - Huono**:
```csharp
public void ProcessOrder1()
{
    // 50 riviä koodia
    Console.WriteLine("Order processed");
    // Sama 50 riviä koodia toistuu
}

public void ProcessOrder2()
{
    // Sama 50 riviä koodia toistuu
    Console.WriteLine("Order processed");
    // Sama 50 riviä koodia toistuu
}
```

**Esimerkki - Hyvä**:
```csharp
private void CommonProcessing()
{
    // 50 riviä koodia
}

public void ProcessOrder1()
{
    CommonProcessing();
    Console.WriteLine("Order processed");
}

public void ProcessOrder2()
{
    CommonProcessing();
    Console.WriteLine("Order processed");
}
```

### 2. KISS (Keep It Simple, Stupid)

Yksinkertaisuus on avain. Älä tee koodista monimutkaista, ellei ole ehdottoman välttämätöntä.

**Esimerkki - Liian monimutkainen**:
```csharp
public bool IsEven(int number)
{
    return number % 2 == 0 ? true : false;
}
```

**Esimerkki - Yksinkertainen**:
```csharp
public bool IsEven(int number)
{
    return number % 2 == 0;
}
```

### 3. YAGNI (You Aren't Gonna Need It)

Älä lisää ominaisuuksia ennakoiden tulevia tarpeita. Lisää ominaisuuksia vain, kun ne ovat todella tarpeellisia.

**Esimerkki - YAGNI-rikkomus**:
```csharp
public class User
{
    // Tulevaisuudessa tarvitaan ehkä...
    public string TwitterHandle { get; set; }
    public string InstagramHandle { get; set; }
    public string LinkedInProfile { get; set; }
    // ... vaikka näitä ei vielä tarvita
}
```

**Esimerkki - YAGNI-noudattaminen**:
```csharp
public class User
{
    public string Name { get; set; }
    public string Email { get; set; }
    // Lisätään muita kenttiä vasta kun ne todella tarvitaan
}
```

## SOLID-periaatteet

### 4. Single Responsibility Principle (SRP)

Jokaisella luokalla tai moduulilla tulisi olla vain yksi syy muuttua. Toisin sanoen, yksi osa koodia tulisi keskittyä vain yhteen tehtävään.

**Esimerkki - SRP-rikkomus**:
```csharp
public class User
{
    public string Name { get; set; }
    public string Email { get; set; }

    public void SaveToDatabase() { /* ... */ }
    public void SendEmail() { /* ... */ }
    public void GenerateReport() { /* ... */ }
}
```

**Esimerkki - SRP-noudattaminen**:
```csharp
public class User
{
    public string Name { get; set; }
    public string Email { get; set; }
}

public class UserRepository
{
    public void Save(User user) { /* ... */ }
}

public class EmailService
{
    public void SendEmail(string to, string message) { /* ... */ }
}

public class ReportGenerator
{
    public void GenerateReport(User user) { /* ... */ }
}
```

### 5. Open-Closed Principle

Ohjelmiston osien (esim. luokkien) tulisi olla avoimia laajennuksille, mutta suljettuja muutoksille. Tämä tarkoittaa, että voit lisätä uusia ominaisuuksia perimällä luokkia tai implementoimalla rajapintoja, mutta ilman alkuperäisen koodin muuttamista.

**Esimerkki - OCP-rikkomus**:
```csharp
public class AreaCalculator
{
    public double CalculateArea(object shape)
    {
        if (shape is Rectangle)
        {
            // Laskenta
        }
        else if (shape is Circle)
        {
            // Laskenta
        }
        // Jokainen uusi muoto vaatii muutoksen tähän luokkaan
    }
}
```

**Esimerkki - OCP-noudattaminen**:
```csharp
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

public class Circle : IShape
{
    public double Radius { get; set; }

    public double CalculateArea() => Math.PI * Radius * Radius;
}

public class AreaCalculator
{
    public double CalculateArea(IShape shape)
    {
        return shape.CalculateArea();  // Ei tarvitse muuttaa uusien muotojen lisäämiseksi
    }
}
```

### 6. Liskov's Substitution Principle

Aliluokan tulisi olla korvattavissa sen yläluokalla ilman, että se aiheuttaa ongelmia.

**Esimerkki - LSP-rikkomus**:
```csharp
public class Bird
{
    public virtual void Fly() { /* ... */ }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        throw new NotImplementedException("Penguins can't fly!");
    }
}
```

**Esimerkki - LSP-noudattaminen**:
```csharp
public abstract class Bird
{
    public abstract void Move();
}

public class FlyingBird : Bird
{
    public override void Move() => Fly();
    public virtual void Fly() { /* ... */ }
}

public class Penguin : Bird
{
    public override void Move() => Swim();
    public void Swim() { /* ... */ }
}
```

### 7. Interface Segregation Principle

Älä pakota luokkia toteuttamaan rajapintoja, joita ne eivät käytä. Rajapinnat tulisi pitää yksinkertaisina ja tarkoituksenmukaisina.

**Esimerkki - ISP-rikkomus**:
```csharp
public interface IWorker
{
    void Work();
    void Eat();
    void Sleep();
}

public class Human : IWorker
{
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
}

public class Robot : IWorker
{
    public void Work() { /* ... */ }
    public void Eat() { throw new NotImplementedException(); }  // Robotit eivät syö!
    public void Sleep() { throw new NotImplementedException(); }  // Robotit eivät nuku!
}
```

**Esimerkki - ISP-noudattaminen**:
```csharp
public interface IWorkable
{
    void Work();
}

public interface IEatable
{
    void Eat();
}

public interface ISleepable
{
    void Sleep();
}

public class Human : IWorkable, IEatable, ISleepable
{
    public void Work() { /* ... */ }
    public void Eat() { /* ... */ }
    public void Sleep() { /* ... */ }
}

public class Robot : IWorkable
{
    public void Work() { /* ... */ }
    // Ei tarvitse toteuttaa Eat() tai Sleep()
}
```

### 8. Dependency Inversion Principle

Riippuvuuksien tulisi kohdistua abstraktioihin, ei yksityiskohtiin. Tämä tarkoittaa, että yläasteen moduulien ei pitäisi olla riippuvaisia ala-asteen moduuleista, vaan molempien tulisi riippua abstraktioista.

**Esimerkki - DIP-rikkomus**:
```csharp
public class UserService
{
    private Database _database = new Database();  // Riippuvuus konkreettiseen luokkaan

    public void SaveUser(User user)
    {
        _database.Save(user);
    }
}
```

**Esimerkki - DIP-noudattaminen**:
```csharp
public interface IRepository
{
    void Save(User user);
}

public class DatabaseRepository : IRepository
{
    public void Save(User user) { /* ... */ }
}

public class UserService
{
    private readonly IRepository _repository;  // Riippuvuus abstraktioon

    public UserService(IRepository repository)
    {
        _repository = repository;
    }

    public void SaveUser(User user)
    {
        _repository.Save(user);
    }
}
```

## Muut tärkeät periaatteet

### 9. Composition Over Inheritance

Perimisen sijaan koostumus (eli osien yhdistäminen) voi olla joustavampi tapa rakentaa ohjelmistoja.

**Esimerkki - Perintä**:
```csharp
public class Animal
{
    public void Eat() { /* ... */ }
}

public class Dog : Animal
{
    public void Bark() { /* ... */ }
}

public class Cat : Animal
{
    public void Meow() { /* ... */ }
}
```

**Esimerkki - Koostumus**:
```csharp
public interface IEatable
{
    void Eat();
}

public interface IBarkable
{
    void Bark();
}

public class Dog
{
    private IEatable _eater;
    private IBarkable _barker;

    public Dog(IEatable eater, IBarkable barker)
    {
        _eater = eater;
        _barker = barker;
    }

    public void Eat() => _eater.Eat();
    public void Bark() => _barker.Bark();
}
```

### 10. Loose Coupling

Osat ohjelmistosta tulisi suunnitella siten, että ne ovat vähemmän riippuvaisia toisistaan, mikä tekee koodista helpommin muokattavaa ja ylläpidettävää.

**Esimerkki - Tiukka kytkentä**:
```csharp
public class OrderService
{
    private EmailService _emailService = new EmailService();  // Tiukka kytkentä

    public void ProcessOrder(Order order)
    {
        // Käsittely...
        _emailService.SendEmail(order.CustomerEmail, "Order confirmed");
    }
}
```

**Esimerkki - Löysä kytkentä**:
```csharp
public interface INotificationService
{
    void Notify(string recipient, string message);
}

public class OrderService
{
    private readonly INotificationService _notificationService;  // Löysä kytkentä

    public OrderService(INotificationService notificationService)
    {
        _notificationService = notificationService;
    }

    public void ProcessOrder(Order order)
    {
        // Käsittely...
        _notificationService.Notify(order.CustomerEmail, "Order confirmed");
    }
}
```

## Yhteenveto

Nämä periaatteet auttavat ohjelmoijia luomaan ohjelmistoja, jotka ovat joustavia, ylläpidettäviä ja laadukkaita. Vaikka ne ovat hyviä ohjeita, niitä tulisi soveltaa harkiten ja ottaen huomioon projektiin liittyvät erityisvaatimukset.

### Keskeiset opit:

- **DRY**: Vältä toistoa
- **KISS**: Pidä yksinkertaisena
- **YAGNI**: Älä ennakoi tarpeita
- **SOLID**: Viisi keskeistä periaatetta laadukkaaseen koodiin
- **Composition Over Inheritance**: Suosi koostumusta
- **Loose Coupling**: Vältä tiukkaa kytkentää

## Hyödyllisiä linkkejä

- [SOLID Principles in C#](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)
- [Microsoftin dokumentaatio](https://learn.microsoft.com/en-us/dotnet/standard/modern-web-apps-azure-architecture/architectural-principles)

