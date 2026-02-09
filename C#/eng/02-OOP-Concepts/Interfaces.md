# Interfaces

## Table of Contents

1. [Introduction](#introduction)
2. [What Are Interfaces?](#what-are-interfaces)
3. [Problem They Solve](#problem-they-solve)
4. [Basic Syntax](#basic-syntax)
5. [Interfaces vs Abstract Classes](#interfaces-vs-abstract-classes)
6. [Multiple Interfaces](#multiple-interfaces)
7. [Interface Segregation](#interface-segregation)
8. [Dependency Injection](#dependency-injection)
9. [Practical Examples](#practical-examples)
10. [Design Patterns with Interfaces](#design-patterns-with-interfaces)
11. [Best Practices](#best-practices)
12. [Common Mistakes](#common-mistakes)
13. [Summary](#summary)

---

## Introduction

Interfaces are one of the most important tools in modern software development. They define a **contract** that a class must implement.

**In short:** An interface is a list of methods, properties, and events **without implementation**. It specifies "WHAT" is done, but not "HOW".

**Analogy:** An interface is like an electrical socket standard—it defines what shape of plug fits, but doesn't care where the electricity comes from.

---

## What Are Interfaces?

An interface defines:

- ✅ **Method signatures** (name, parameters, return value)
- ✅ **Properties** (get/set)
- ✅ **Events**
- ✅ **Indexers**

An interface does **NOT** define:

- ❌ Implementation
- ❌ Fields
- ❌ Constructors
- ❌ Access modifiers (everything is implicitly public)

```csharp
// Simple interface
public interface IAnimal
{
    // Methods (no implementation!)
    void MakeSound();
    void Eat();

    // Properties
    string Name { get; set; }
    int Age { get; }

    // C# 8.0+: Default implementation (optional)
    void Sleep()
    {
        Console.WriteLine($"{Name} sleeps");
    }
}

// Class implements the interface
public class Dog : IAnimal
{
    public string Name { get; set; }
    public int Age { get; private set; }

    // MUST implement interface methods
    public void MakeSound()
    {
        Console.WriteLine($"{Name} barks: Woof woof!");
    }

    public void Eat()
    {
        Console.WriteLine($"{Name} eats dog food");
    }

    // Sleep() is optional (has default implementation)
}
```

---

## Problem They Solve

### Without Interfaces (Problem)

```csharp
// ❌ BAD: Dependency on concrete class
public class EmailService
{
    private SmtpClient smtpClient; // Tied to one implementation!

    public EmailService()
    {
        smtpClient = new SmtpClient(); // Hard to test!
    }

    public void SendEmail(string to, string subject, string body)
    {
        smtpClient.Send(to, subject, body);
    }
}

// Problems:
// 1. Cannot easily switch from SMTP to something else
// 2. Hard to test (needs real SMTP server)
// 3. EmailService is tied to SmtpClient (tight coupling)
```

### With Interfaces (Solution)

```csharp
// ✅ GOOD: Dependency on abstraction (interface)
public interface IEmailSender
{
    void SendEmail(string to, string subject, string body);
    Task SendEmailAsync(string to, string subject, string body);
}

// Implementation 1: SMTP
public class SmtpEmailSender : IEmailSender
{
    private string smtpServer;

    public SmtpEmailSender(string server)
    {
        smtpServer = server;
    }

    public void SendEmail(string to, string subject, string body)
    {
        Console.WriteLine($"Sending via SMTP ({smtpServer}): {subject} -> {to}");
        // Actual SMTP logic...
    }

    public async Task SendEmailAsync(string to, string subject, string body)
    {
        await Task.Run(() => SendEmail(to, subject, body));
    }
}

// Implementation 2: SendGrid API
public class SendGridEmailSender : IEmailSender
{
    private string apiKey;

    public SendGridEmailSender(string key)
    {
        apiKey = key;
    }

    public void SendEmail(string to, string subject, string body)
    {
        Console.WriteLine($"Sending via SendGrid API: {subject} -> {to}");
        // SendGrid API call...
    }

    public async Task SendEmailAsync(string to, string subject, string body)
    {
        await Task.Run(() => SendEmail(to, subject, body));
    }
}

// Implementation 3: Console (for testing)
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

// EmailService is now flexible!
public class EmailService
{
    private readonly IEmailSender emailSender; // Interface!

    // Dependency Injection - we get the implementation from outside
    public EmailService(IEmailSender sender)
    {
        emailSender = sender;
    }

    public void SendWelcomeEmail(string to, string name)
    {
        string subject = $"Welcome, {name}!";
        string body = $"Hi {name}, welcome to our service!";
        emailSender.SendEmail(to, subject, body);
    }
}

// Usage - easy to swap implementation!
// In production:
IEmailSender productionSender = new SmtpEmailSender("smtp.example.com");
EmailService emailService1 = new EmailService(productionSender);

// In testing:
IEmailSender testSender = new ConsoleEmailSender();
EmailService emailService2 = new EmailService(testSender);

// Alternatively:
IEmailSender sendGridSender = new SendGridEmailSender("api-key-123");
EmailService emailService3 = new EmailService(sendGridSender);
```

**Benefits:**

- ✅ Easy to swap implementations
- ✅ Easy to test (mock objects)
- ✅ Loose coupling
- ✅ Follows Dependency Inversion Principle

---

## Basic Syntax

### Basic Interface

```csharp
// Naming convention: I + PascalCase
public interface IShape
{
    // Methods
    double CalculateArea();
    double CalculatePerimeter();
    void Draw();

    // Properties
    string Name { get; set; }
    string Color { get; set; }

    // Read-only property
    int Id { get; }
}

// Implementation
public class Circle : IShape
{
    private static int nextId = 1;

    public double Radius { get; set; }

    // IShape implementation
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
        Console.WriteLine($"Drawing {Color} circle '{Name}', radius: {Radius}");
    }
}
```

### Interface Inheritance

```csharp
// Interfaces can inherit from other interfaces
public interface IDrawable
{
    void Draw();
}

public interface IResizable
{
    void Resize(double scale);
}

// Combined interface
public interface IGraphicObject : IDrawable, IResizable
{
    void Move(int x, int y);
    int X { get; set; }
    int Y { get; set; }
}

// Implementation
public class Shape : IGraphicObject
{
    public int X { get; set; }
    public int Y { get; set; }

    // IDrawable
    public void Draw()
    {
        Console.WriteLine($"Drawing at ({X}, {Y})");
    }

    // IResizable
    public void Resize(double scale)
    {
        Console.WriteLine($"Scaling {scale}x");
    }

    // IGraphicObject
    public void Move(int x, int y)
    {
        X = x;
        Y = y;
        Console.WriteLine($"Moved to ({X}, {Y})");
    }
}
```

---

## Interfaces vs Abstract Classes

| Feature              | Interface                                   | Abstract Class                       |
| -------------------- | ------------------------------------------- | ------------------------------------ |
| **Multiple**         | ✅ Class can implement multiple             | ❌ Only one base class               |
| **Implementation**   | ❌ No implementation (except default C# 8+) | ✅ Can have implementation           |
| **Fields**           | ❌ No fields                                | ✅ Can have fields                   |
| **Constructor**      | ❌ No constructor                           | ✅ Can have constructor              |
| **Access modifiers** | ❌ All public                               | ✅ Can have private, protected, etc. |
| **Purpose**          | "Can-do" relationships                      | "Is-a" relationships                 |
| **Example**          | `IFlyable`, `ISwimmable`                    | `Animal`, `Vehicle`                  |

### When to Use Which?

```csharp
// ✅ Use INTERFACE when:
// - You want to define a "can-do" relationship
// - You want to allow a class to implement multiple capabilities
// - You want loose coupling

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

// Duck can fly AND swim
public class Duck : IFlyable, ISwimmable
{
    public void Fly() => Console.WriteLine("Duck flies");
    public double MaxAltitude => 100;

    public void Swim() => Console.WriteLine("Duck swims");
    public double MaxDepth => 5;
}

// ✅ Use ABSTRACT CLASS when:
// - You want to share common code
// - You want to define an "is-a" relationship
// - You need fields or constructors

public abstract class Animal
{
    // Common fields
    protected string name;
    protected int age;

    // Constructor
    protected Animal(string name, int age)
    {
        this.name = name;
        this.age = age;
    }

    // Common implementation
    public void Eat()
    {
        Console.WriteLine($"{name} eats");
    }

    // Abstract method
    public abstract void MakeSound();
}
```

---

## Multiple Interfaces

C# does not support multiple inheritance for classes, but **with interfaces you can implement multiple**.

```csharp
// Different capabilities in their own interfaces
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

// Human can walk and swim
public class Human : IWalkable, ISwimmable
{
    public string Name { get; set; }

    public void Walk()
    {
        Console.WriteLine($"{Name} walks");
    }

    public void Run()
    {
        Console.WriteLine($"{Name} runs");
    }

    public void Swim()
    {
        Console.WriteLine($"{Name} swims");
    }

    public void Dive()
    {
        Console.WriteLine($"{Name} dives");
    }
}

// Duck can do everything!
public class Duck : IFlyable, ISwimmable, IWalkable
{
    public string Name { get; set; }

    public void Fly() => Console.WriteLine($"{Name} flies");
    public void Land() => Console.WriteLine($"{Name} lands");

    public void Swim() => Console.WriteLine($"{Name} swims");
    public void Dive() => Console.WriteLine($"{Name} dives");

    public void Walk() => Console.WriteLine($"{Name} walks");
    public void Run() => Console.WriteLine($"{Name} runs (slowly)");
}

// Airplane can only fly
public class Airplane : IFlyable
{
    public string Model { get; set; }

    public void Fly() => Console.WriteLine($"{Model} flies");
    public void Land() => Console.WriteLine($"{Model} lands");
}

// Polymorphism works:
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

// Usage:
Duck duck = new Duck { Name = "Donald" };
Airplane plane = new Airplane { Model = "Boeing 747" };
Human human = new Human { Name = "John" };

List<IFlyable> flyers = new List<IFlyable> { duck, plane };
List<ISwimmable> swimmers = new List<ISwimmable> { duck, human };

TransportManager manager = new TransportManager();
manager.MakeFlyersLand(flyers);
manager.MakeSwimmersSwim(swimmers);
```

---

## Interface Segregation

**Interface Segregation Principle (ISP):** Don't force a class to implement methods it doesn't need.

### ❌ Bad: Interface Too Large

```csharp
// ❌ BAD: "God Interface" - too many methods
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

// Robot has to implement methods it doesn't need!
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

### ✅ Good: Small, Focused Interfaces

```csharp
// ✅ GOOD: Split into smaller parts
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

// Human implements everything
public class Human : IWorkable, IFeedable, ISleepable, ICommunicator
{
    public void Work() { Console.WriteLine("Working"); }
    public void Eat() { Console.WriteLine("Eating"); }
    public void Sleep() { Console.WriteLine("Sleeping"); }
    public void SendEmail() { Console.WriteLine("Sending email"); }
    public void MakePhoneCall() { Console.WriteLine("Making phone call"); }
}

// Robot implements only what it needs
public class Robot : IWorkable, ICommunicator
{
    public void Work() { Console.WriteLine("Working 24/7"); }
    public void SendEmail() { Console.WriteLine("Sending automated message"); }
    public void MakePhoneCall() { Console.WriteLine("Automated phone robot"); }
    // No Eat() or Sleep() - doesn't need them!
}
```

---

## Dependency Injection

Interfaces are central to the Dependency Injection pattern.

### Example: Logging

```csharp
// Interface
public interface ILogger
{
    void LogInfo(string message);
    void LogWarning(string message);
    void LogError(string message, Exception ex);
}

// Implementation 1: Console
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

// Implementation 2: File
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

// Implementation 3: Null (no logging)
public class NullLogger : ILogger
{
    public void LogInfo(string message) { }
    public void LogWarning(string message) { }
    public void LogError(string message, Exception ex) { }
}

// Usage: UserService depends on ILogger interface
public class UserService
{
    private readonly ILogger logger;

    // Dependency Injection in constructor
    public UserService(ILogger logger)
    {
        this.logger = logger;
    }

    public void CreateUser(string username, string email)
    {
        try
        {
            logger.LogInfo($"Creating user: {username}");

            // User creation logic...

            logger.LogInfo($"User {username} created successfully");
        }
        catch (Exception ex)
        {
            logger.LogError($"Failed to create user {username}", ex);
            throw;
        }
    }
}

// Usage - easy to swap logger
// In development:
ILogger devLogger = new ConsoleLogger();
UserService userService1 = new UserService(devLogger);

// In production:
ILogger prodLogger = new FileLogger("application.log");
UserService userService2 = new UserService(prodLogger);

// In testing:
ILogger testLogger = new NullLogger();
UserService userService3 = new UserService(testLogger);
```

---

## Practical Examples

### Example 1: Data Storage

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

// SQL implementation
public class SqlRepository<T> : IRepository<T> where T : class
{
    private string connectionString;

    public SqlRepository(string connStr)
    {
        connectionString = connStr;
    }

    public T GetById(int id)
    {
        Console.WriteLine($"SQL: Fetching {typeof(T).Name} with ID {id}");
        // SQL logic...
        return null;
    }

    public IEnumerable<T> GetAll()
    {
        Console.WriteLine($"SQL: Fetching all {typeof(T).Name}");
        return new List<T>();
    }

    public void Add(T entity)
    {
        Console.WriteLine($"SQL: Adding {typeof(T).Name}");
    }

    public void Update(T entity)
    {
        Console.WriteLine($"SQL: Updating {typeof(T).Name}");
    }

    public void Delete(int id)
    {
        Console.WriteLine($"SQL: Deleting {typeof(T).Name} with ID {id}");
    }
}

// MongoDB implementation
public class MongoRepository<T> : IRepository<T> where T : class
{
    private string databaseName;

    public MongoRepository(string dbName)
    {
        databaseName = dbName;
    }

    public T GetById(int id)
    {
        Console.WriteLine($"MongoDB: Fetching {typeof(T).Name} with ID {id}");
        return null;
    }

    public IEnumerable<T> GetAll()
    {
        Console.WriteLine($"MongoDB: Fetching all {typeof(T).Name}");
        return new List<T>();
    }

    public void Add(T entity)
    {
        Console.WriteLine($"MongoDB: Adding {typeof(T).Name}");
    }

    public void Update(T entity)
    {
        Console.WriteLine($"MongoDB: Updating {typeof(T).Name}");
    }

    public void Delete(int id)
    {
        Console.WriteLine($"MongoDB: Deleting {typeof(T).Name} with ID {id}");
    }
}

// Domain model
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
}

// Service uses interface
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

// Usage - easy to switch database
IRepository<User> sqlRepo = new SqlRepository<User>("Server=...;Database=...");
IRepository<User> mongoRepo = new MongoRepository<User>("mongodb://localhost");

UserService service1 = new UserService(sqlRepo);    // SQL
UserService service2 = new UserService(mongoRepo);  // MongoDB
```

### Example 2: Payment Processing (Strategy Pattern)

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
        Console.WriteLine($"Paying {amount:C} with credit card (**** {cardNumber.Substring(cardNumber.Length - 4)})");
        return true;
    }

    public string GetPaymentMethodName() => "Credit Card";
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
        Console.WriteLine($"Paying {amount:C} with PayPal ({email})");
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
        Console.WriteLine($"Paying {amount:C} with MobilePay ({phoneNumber})");
        return true;
    }

    public string GetPaymentMethodName() => "MobilePay";
}

// Checkout uses Strategy pattern
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
            Console.WriteLine("Select payment method!");
            return;
        }

        Console.WriteLine($"Payment method: {paymentStrategy.GetPaymentMethodName()}");
        Console.WriteLine($"Total: {totalAmount:C}");

        if (paymentStrategy.ProcessPayment(totalAmount))
        {
            Console.WriteLine("Payment successful!");
            totalAmount = 0;
        }
        else
        {
            Console.WriteLine("Payment failed!");
        }
    }
}

// Usage:
Checkout checkout = new Checkout();
checkout.AddItem(29.99m);
checkout.AddItem(15.50m);
checkout.AddItem(8.95m);

// Customer selects payment method
checkout.SetPaymentStrategy(new CreditCardPayment("1234567890123456"));
// OR
// checkout.SetPaymentStrategy(new PayPalPayment("user@example.com"));
// OR
// checkout.SetPaymentStrategy(new MobilePayPayment("+358401234567"));

checkout.ProcessCheckout();
```

---

## Design Patterns with Interfaces

### 1. Factory Pattern

```csharp
public interface IVehicle
{
    void Drive();
    string GetVehicleType();
}

public class Car : IVehicle
{
    public void Drive() => Console.WriteLine("Driving car");
    public string GetVehicleType() => "Car";
}

public class Motorcycle : IVehicle
{
    public void Drive() => Console.WriteLine("Driving motorcycle");
    public string GetVehicleType() => "Motorcycle";
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
        Console.WriteLine($"News agency: {news}");
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
        Console.WriteLine($"{name} received: {message}");
    }
}
```

---

## Best Practices

### ✅ DO (Do This):

1. **Name interfaces with I prefix**

```csharp
public interface IRepository { }  // ✅
public interface ILogger { }       // ✅
```

2. **Keep interfaces small (ISP)**

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

3. **Use descriptive names**

```csharp
public interface IFlyable { }     // ✅ Tells what classes can fly
public interface ISaveable { }    // ✅ Tells what classes can save
```

4. **Design interfaces to be stable**

```csharp
// Don't change the interface constantly - breaks implementations
```

5. **Document interfaces well**

```csharp
/// <summary>
/// Defines methods for storing data.
/// Implementations may use database, files, etc.
/// </summary>
public interface IDataStorage
{
    /// <summary>
    /// Saves data. Throws IOException if save fails.
    /// </summary>
    void Save(string data);
}
```

### ❌ DON'T (Don't Do This):

1. **Don't make interfaces too large**

```csharp
// ❌ BAD - 20 methods in one interface
public interface IGodInterface
{
    void Method1();
    void Method2();
    // ... 18 more ...
}
```

2. **Don't put implementation in interface (except C# 8+ default)**

```csharp
// ❌ Generally NO (except C# 8+ default implementation)
public interface IBad
{
    void Method()
    {
        // Implementation...
    }
}
```

3. **Don't forget to honor the interface contract**

```csharp
// ❌ BAD - Breaks the contract
public interface ISaveable
{
    bool Save(); // Returns true if successful
}

public class Bad : ISaveable
{
    public bool Save()
    {
        return false; // Always returns false - breaks expectation!
    }
}
```

---

## Common Mistakes

### Mistake 1: Interface with implementation (before C# 8)

```csharp
// ❌ DOESN'T WORK (before C# 8)
public interface IBad
{
    void Method()
    {
        Console.WriteLine("Implementation");
    }
}

// ✅ C# 8+ default implementation (optional)
public interface IGood
{
    void Method()
    {
        Console.WriteLine("Default implementation");
    }
}
```

### Mistake 2: Forgetting to implement something

```csharp
public interface IExample
{
    void Method1();
    void Method2();
    void Method3();
}

// ❌ WON'T COMPILE - Method3 missing
public class Bad : IExample
{
    public void Method1() { }
    public void Method2() { }
    // Method3 missing!
}
```

### Mistake 3: Interface too large

```csharp
// ❌ Violates Interface Segregation Principle
public interface IWorker
{
    void Work();
    void Eat();      // Robot doesn't eat
    void Sleep();    // Robot doesn't sleep
    void Code();
}
```

---

## Summary

Interfaces are one of the most important tools in modern software development.

### Remember:

- ✅ Interfaces define **"WHAT"** not **"HOW"**
- ✅ A class can implement **multiple** interfaces
- ✅ Use **Interface Segregation** - keep interfaces small
- ✅ **Dependency Injection** - inject interfaces
- ✅ Name with **I** prefix (ILogger, IRepository)
- ✅ Design for stability - don't change often

### Interfaces enable:

- **Plug-and-play** architecture
- **Testability** (mock objects)
- **Flexibility** (swap implementations)
- **Loose coupling**
- **Adherence to SOLID principles**

**Next step:** Once you master interfaces, continue to the [Composition](Composition.md) material, which shows how to build systems from components.

---
