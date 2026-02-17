# Object-Oriented Programming Techniques and the Problems They Solve

At the heart of object-oriented programming (OOP) is the idea of dividing an application into logical units—**objects**—that represent real-world concepts or parts of the application. On this page we introduce OOP concepts (encapsulation, inheritance, polymorphism, composition, and interfaces), describe what problems they solve, and provide C# code examples.

---

## Encapsulation

**Problem encapsulation solves:**
Without encapsulation, a class’s internal data (variables) can be read and modified in countless ways from the outside, which can break the class’s integrity and make it harder to maintain.

**Solution:**
*Encapsulation* hides the implementation details of a class by exposing public `get` and `set` methods (or properties) for working with its data. This ensures data safety and a clear interface for external users.

### Before encapsulation (problem)

```csharp
// ❌ BAD: Public fields, no control
public class BankAccount
{
    public decimal balance; // Anyone can change it directly!
    public string accountNumber;
}

// Usage - dangerous!
BankAccount account = new BankAccount();
account.balance = -1000; // We can set a negative balance!
account.balance = 999999; // Or an unrealistically large amount!
```

### With encapsulation (solution)

```csharp
// ✅ GOOD: Encapsulated implementation
public class BankAccount
{
    private decimal balance; // Private field
    private string accountNumber;
    
    public string AccountNumber
    {
        get { return accountNumber; }
        private set { accountNumber = value; }
    }
    
    public decimal Balance
    {
        get { return balance; }
        // No setter - balance cannot be changed directly!
    }
    
    public BankAccount(string accountNumber, decimal initialBalance)
    {
        this.accountNumber = accountNumber;
        if (initialBalance >= 0)
            this.balance = initialBalance;
        else
            throw new ArgumentException("Initial balance cannot be negative");
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            balance += amount;
            Console.WriteLine($"Deposited {amount} euros. New balance: {balance}");
        }
        else
        {
            throw new ArgumentException("Deposit amount must be positive");
        }
    }
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance)
        {
            balance -= amount;
            Console.WriteLine($"Withdrawn {amount} euros. New balance: {balance}");
            return true;
        }
        Console.WriteLine("Withdrawal failed: insufficient balance or invalid amount.");
        return false;
    }
}
```

**More information:** See [Encapsulation](Encapsulation.md)

---

## Inheritance

**Problem inheritance solves:**
Repeated code, duplicated logic, and hard-to-manage parallel versions of classes.

**Solution:**
*Inheritance* lets a new class (derived class) inherit properties and methods from an existing class (base class), making code reuse and maintenance easier. Inheritance often models an **“is-a” relationship** (e.g. “Dog is an Animal”).

### Without inheritance (problem)

```csharp
// ❌ BAD: Code duplication
public class Dog
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public void Eat() { Console.WriteLine($"{Name} eats"); }
    public void Sleep() { Console.WriteLine($"{Name} sleeps"); }
    public void Bark() { Console.WriteLine($"{Name} barks: Woof woof!"); }
}

public class Cat
{
    public string Name { get; set; } // Duplication!
    public int Age { get; set; }     // Duplication!
    
    public void Eat() { Console.WriteLine($"{Name} eats"); } // Duplication!
    public void Sleep() { Console.WriteLine($"{Name} sleeps"); } // Duplication!
    public void Meow() { Console.WriteLine($"{Name} meows: Meow!"); }
}
```

### With inheritance (solution)

```csharp
// ✅ GOOD: Base class
public class Animal
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public void Eat()
    {
        Console.WriteLine($"{Name} eats");
    }
    
    public void Sleep()
    {
        Console.WriteLine($"{Name} sleeps");
    }
    
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} makes a sound");
    }
}

// ✅ Derived classes
public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} barks: Woof woof!");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} meows: Meow!");
    }
}
```

**More information:** See [Inheritance](Inheritance.md)

---

## Polymorphism

**Problem polymorphism solves:**
The need to treat objects from different classes in a **uniform** way without the caller having to know the exact implementation.

**Solution:**
*Polymorphism* allows the same method call to behave differently depending on which class (base or derived) the object belongs to. In C#, polymorphism is implemented with `virtual`, `override`, `abstract`, and interfaces.

### Method calls without polymorphism (problem)

```csharp
// ❌ BAD: Must check type
public void MakeAnimalSound(Animal animal)
{
    if (animal is Dog)
    {
        Console.WriteLine("Woof woof!");
    }
    else if (animal is Cat)
    {
        Console.WriteLine("Meow!");
    }
    else if (animal is Bird)
    {
        Console.WriteLine("Chirp chirp!");
    }
    // But if we have 10 animal types, the code gets complex...
}
```

### With polymorphism (solution)

```csharp
// ✅ GOOD: Uniform handling
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex" },
    new Cat { Name = "Whiskers" },
    new Bird { Name = "Tweety" }
};

foreach (Animal animal in animals)
{
    animal.MakeSound(); // Each calls its own version!
}
// Output:
// Rex barks: Woof woof!
// Whiskers meows: Meow!
// Tweety sings: Chirp chirp!
```

**More information:** See [Polymorphism](Polymorphism.md)

---

## Composition

**Problem composition solves:**
An oversized “everything in one” class with too many responsibilities, making the code hard to maintain.

**Solution:**
*Composition* means a class is made up of instances of other classes. This allows using smaller, logical modules, improving clarity and maintainability.

### Without composition (problem)

```csharp
// ❌ BAD: Everything in one class
public class Car
{
    // Engine properties
    public bool EngineRunning { get; set; }
    public int EnginePower { get; set; }
    
    // Tire properties
    public int TirePressure { get; set; }
    public string TireBrand { get; set; }
    
    // Seat properties
    public int NumberOfSeats { get; set; }
    public bool HasLeatherSeats { get; set; }
    
    // ... and much more - too complex!
}
```

### With composition (solution)

```csharp
// ✅ GOOD: Small, focused classes
public class Engine
{
    public bool IsRunning { get; private set; }
    public int Power { get; set; }
    
    public void Start() { IsRunning = true; Console.WriteLine("Engine starts"); }
    public void Stop() { IsRunning = false; Console.WriteLine("Engine stops"); }
}

public class Tire
{
    public int Pressure { get; set; }
    public string Brand { get; set; }
    
    public void CheckPressure() { Console.WriteLine($"Tire pressure: {Pressure} PSI"); }
}

// ✅ Composed class
public class Car
{
    private Engine engine;      // Composition
    private Tire[] tires;       // Composition
    
    public Car(Engine engine, Tire[] tires)
    {
        this.engine = engine;
        this.tires = tires;
    }
    
    public void Start() { engine.Start(); }
    public void CheckAllTires() { foreach (var tire in tires) tire.CheckPressure(); }
}
```

**More information:** See [Composition](Composition.md)

---

## Interfaces

**Problem interfaces solve:**
The need to commit to a specific “contract” in multiple classes without using multiple inheritance, and to define common methods that different classes can implement in their own way.

**Solution:**
An *interface* defines a set of methods (and/or properties) that a class must implement if it is to “adhere to” that interface. This adds flexibility, since one class can implement multiple interfaces.

### With interface (solution)

```csharp
// ✅ GOOD: Interface defines the contract
public interface IFlyable
{
    void Fly();
}

public interface ISwimmable
{
    void Swim();
}

// ✅ A class can implement multiple interfaces
public class Duck : IFlyable, ISwimmable
{
    public void Fly()
    {
        Console.WriteLine("Duck flies");
    }
    
    public void Swim()
    {
        Console.WriteLine("Duck swims");
    }
}

// ✅ Uniform handling
IFlyable[] flyables = new IFlyable[] { new Duck(), new Airplane() };
foreach (var flyable in flyables)
{
    flyable.Fly(); // Each implements its own version
}
```

**More information:** See [Interfaces](Interfaces.md)

---

## Summary

These techniques—encapsulation, inheritance, polymorphism, composition, and interfaces—form the foundation of object-oriented programming. Each addresses a particular kind of problem, and together they make code **clearer, easier to maintain, and more flexible**.

### Recommendation: Study in order

1. **Encapsulation** – Foundation for protecting data
2. **Inheritance** – Code reuse
3. **Polymorphism** – Flexible handling
4. **Composition** – Modular structure
5. **Interfaces** – Contracts and multiple “inheritance”

Each concept builds on the previous one, and together they provide a solid basis for object-oriented programming.
