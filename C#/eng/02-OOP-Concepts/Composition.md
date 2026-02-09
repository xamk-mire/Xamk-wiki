# Composition

## Table of Contents

1. [Introduction](#introduction)
2. [What is Composition?](#what-is-composition)
3. [Problem It Solves](#problem-it-solves)
4. [Composition vs Inheritance](#composition-vs-inheritance)
5. [Composition vs Aggregation](#composition-vs-aggregation)
6. [Composition over Inheritance](#composition-over-inheritance)
7. [Practical Examples](#practical-examples)
8. [Design Patterns with Composition](#design-patterns-with-composition)
9. [Best Practices](#best-practices)
10. [Common Mistakes](#common-mistakes)
11. [Summary](#summary)

---

## Introduction

Composition is a technique where **a complex object is built from simpler parts**. It is one of the most important principles in software development.

**In short:** Composition describes a **"has-a"** (owns) relationship: "A car HAS an engine", "A computer HAS a CPU".

**Analogy:** A car is NOT an engine—a car HAS an engine. A car is made of parts: engine, tires, steering, etc.

---

## What is Composition?

Composition means that a class **contains** other classes as member variables.

```csharp
// Simple example:
public class Engine
{
    public void Start()
    {
        Console.WriteLine("Engine starts");
    }
}

public class Car
{
    private Engine engine; // Car "has-a" Engine (composition)

    public Car()
    {
        engine = new Engine(); // Car creates the engine
    }

    public void Start()
    {
        engine.Start(); // Car uses the engine
    }
}
```

**Key points:**

- Car **owns** the Engine
- Car **creates** the Engine
- When Car is destroyed, Engine is destroyed too
- Car **delegates** work to the Engine

---

## Problem It Solves

### Without Composition (Problem)

```csharp
// ❌ BAD: Everything in one class - "God Object"
public class Car
{
    // Engine logic
    private bool engineRunning;
    private int enginePower;
    private string engineType;

    public void StartEngine()
    {
        engineRunning = true;
        Console.WriteLine($"Starting {engineType} engine, {enginePower} HP");
    }

    public void StopEngine()
    {
        engineRunning = false;
        Console.WriteLine("Engine stops");
    }

    // Tire logic
    private int tirePressure;
    private string tireBrand;
    private int numberOfTires;

    public void CheckTirePressure()
    {
        Console.WriteLine($"Tire pressure: {tirePressure} PSI");
    }

    public void InflateTires(int pressure)
    {
        tirePressure = pressure;
    }

    // Seat logic
    private int numberOfSeats;
    private bool hasLeatherSeats;
    private bool seatsHeated;

    public void AdjustSeats()
    {
        Console.WriteLine("Adjusting seats");
    }

    // GPS logic
    private double latitude;
    private double longitude;
    private string destination;

    public void Navigate(string dest)
    {
        destination = dest;
        Console.WriteLine($"Navigating to: {destination}");
    }

    // ... and so on - class grows huge!
}
```

**Problems:**

- ❌ Class too large (100+ lines → 1000+ lines)
- ❌ Hard to maintain
- ❌ Hard to test
- ❌ Hard to reuse
- ❌ Violates Single Responsibility Principle
- ❌ Tight coupling - everything depends on everything

### With Composition (Solution)

```csharp
// ✅ GOOD: Small, focused classes
public class Engine
{
    public string Type { get; set; }
    public int Power { get; set; }
    private bool isRunning;

    public void Start()
    {
        isRunning = true;
        Console.WriteLine($"Starting {Type} engine, {Power} HP");
    }

    public void Stop()
    {
        isRunning = false;
        Console.WriteLine("Engine stops");
    }

    public bool IsRunning => isRunning;
}

public class Tire
{
    public string Brand { get; set; }
    public int Pressure { get; private set; }

    public void CheckPressure()
    {
        Console.WriteLine($"Tire pressure: {Pressure} PSI, Brand: {Brand}");
    }

    public void Inflate(int pressure)
    {
        Pressure = pressure;
        Console.WriteLine($"Tire inflated: {Pressure} PSI");
    }
}

public class Seat
{
    public bool IsLeather { get; set; }
    public bool IsHeated { get; set; }
    private int position;

    public void Adjust(int newPosition)
    {
        position = newPosition;
        Console.WriteLine($"Seat adjusted to position: {position}");
    }
}

public class GPS
{
    private double latitude;
    private double longitude;
    private string currentDestination;

    public void Navigate(string destination)
    {
        currentDestination = destination;
        Console.WriteLine($"Navigating to: {destination}");
        Console.WriteLine($"Current location: {latitude}, {longitude}");
    }

    public void UpdateLocation(double lat, double lon)
    {
        latitude = lat;
        longitude = lon;
    }
}

// ✅ Car is composed of parts (Composition)
public class Car
{
    // Composition - car OWNS these parts
    private readonly Engine engine;
    private readonly Tire[] tires;
    private readonly Seat[] seats;
    private readonly GPS gps;

    public string Brand { get; set; }
    public string Model { get; set; }

    public Car(string brand, string model)
    {
        Brand = brand;
        Model = model;

        // Car creates and owns the parts
        engine = new Engine { Type = "V6", Power = 250 };
        tires = new Tire[4]
        {
            new Tire { Brand = "Michelin", Pressure = 32 },
            new Tire { Brand = "Michelin", Pressure = 32 },
            new Tire { Brand = "Michelin", Pressure = 32 },
            new Tire { Brand = "Michelin", Pressure = 32 }
        };
        seats = new Seat[5]
        {
            new Seat { IsLeather = true, IsHeated = true },
            new Seat { IsLeather = true, IsHeated = true },
            new Seat { IsLeather = true, IsHeated = false },
            new Seat { IsLeather = true, IsHeated = false },
            new Seat { IsLeather = true, IsHeated = false }
        };
        gps = new GPS();
    }

    // Car delegates work to parts
    public void Start()
    {
        Console.WriteLine($"Starting {Brand} {Model}");
        engine.Start();
    }

    public void Stop()
    {
        Console.WriteLine($"Stopping {Brand} {Model}");
        engine.Stop();
    }

    public void CheckAllTires()
    {
        Console.WriteLine("Checking all tires:");
        foreach (Tire tire in tires)
        {
            tire.CheckPressure();
        }
    }

    public void AdjustDriverSeat(int position)
    {
        seats[0].Adjust(position); // Driver's seat
    }

    public void NavigateTo(string destination)
    {
        gps.Navigate(destination);
    }
}

// Usage:
Car car = new Car("Toyota", "Corolla");
car.Start();
car.CheckAllTires();
car.NavigateTo("Helsinki");
car.Stop();
```

**Benefits:**

- ✅ Small, manageable classes
- ✅ Easy to maintain
- ✅ Easy to test (test Engine separately)
- ✅ Reusable (Engine can be used elsewhere)
- ✅ Follows Single Responsibility
- ✅ Loose coupling

---

## Composition vs Inheritance

### The Problem with Inheritance

```csharp
// ❌ Misuse of inheritance
public class Engine
{
    public void Start() { }
    public void Stop() { }
}

// ❌ WRONG: A car is NOT an engine!
public class Car : Engine
{
    // Now Car has Start() and Stop() but...
    // This is semantically wrong!
}
```

### Composition vs Inheritance Comparison

| Feature            | Composition                  | Inheritance                 |
| ------------------ | ---------------------------- | --------------------------- |
| **Relationship**   | "Has-a" (owns)               | "Is-a" (is)                 |
| **Flexibility**    | ✅ Very flexible             | ⚠️ Rigid                    |
| **Runtime change** | ✅ Can swap parts            | ❌ Cannot change base class |
| **Multiple**       | ✅ Unlimited number of parts | ❌ One base class           |
| **Coupling**       | ✅ Loose                     | ⚠️ Tight                    |
| **Testability**    | ✅ Easy to test parts        | ⚠️ Harder to test           |
| **Example**        | Car has Engine               | Dog is Animal               |

### When to Use Which?

```csharp
// ✅ Use COMPOSITION when:
// - "Has-a" relationship
// - You want flexibility
// - You want to swap parts at runtime

public class Car
{
    private IEngine engine; // Can be swapped!

    public void SetEngine(IEngine newEngine)
    {
        engine = newEngine; // Swap the engine
    }
}

// ✅ Use INHERITANCE when:
// - "Is-a" relationship is truly clear
// - You want to share common functionality
// - Polymorphism is important

public abstract class Animal
{
    public abstract void MakeSound();
}

public class Dog : Animal // Dog IS AN Animal ✅
{
    public override void MakeSound()
    {
        Console.WriteLine("Woof!");
    }
}
```

### Example: "Composition over Inheritance"

```csharp
// ❌ BAD: Inheritance hierarchy becomes complex
public class Vehicle { }
public class LandVehicle : Vehicle { }
public class WaterVehicle : Vehicle { }
public class AirVehicle : Vehicle { }
public class AmphibiousVehicle : LandVehicle { } // But it also swims! Problem!

// ✅ GOOD: Composition
public interface IMovementMethod
{
    void Move();
}

public class WheelMovement : IMovementMethod
{
    public void Move() => Console.WriteLine("Moving on wheels");
}

public class PropellerMovement : IMovementMethod
{
    public void Move() => Console.WriteLine("Moving with propeller");
}

public class WingMovement : IMovementMethod
{
    public void Move() => Console.WriteLine("Moving with wings");
}

public class Vehicle
{
    private List<IMovementMethod> movementMethods = new List<IMovementMethod>();

    public void AddMovementMethod(IMovementMethod method)
    {
        movementMethods.Add(method);
    }

    public void Move()
    {
        foreach (var method in movementMethods)
        {
            method.Move();
        }
    }
}

// Usage:
Vehicle car = new Vehicle();
car.AddMovementMethod(new WheelMovement());

Vehicle boat = new Vehicle();
boat.AddMovementMethod(new PropellerMovement());

Vehicle amphibious = new Vehicle();
amphibious.AddMovementMethod(new WheelMovement());
amphibious.AddMovementMethod(new PropellerMovement());
// Now amphibious can move both ways!
```

---

## Composition vs Aggregation

### Composition (Strong Ownership)

- **Owner creates** the component
- **Component lifetime** depends on the owner
- When owner is destroyed, component is destroyed

```csharp
// ✅ COMPOSITION: Car owns and creates the engine
public class Car
{
    private Engine engine; // Car OWNS the Engine

    public Car()
    {
        engine = new Engine(); // Car CREATES the Engine
    }
    // When Car is destroyed, Engine is destroyed too
}
```

### Aggregation (Weak Ownership)

- **Owner receives** the component from outside
- **Component lifetime** does not depend on the owner
- When owner is destroyed, component can still exist

```csharp
// ✅ AGGREGATION: Car uses a driver, but doesn't own one
public class Driver
{
    public string Name { get; set; }
}

public class Car
{
    private Driver driver; // Car USES Driver, but doesn't own

    public void SetDriver(Driver d)
    {
        driver = d; // Driver comes from outside
    }
    // When Car is destroyed, Driver still exists
}

// Usage:
Driver john = new Driver { Name = "John" };
Car car1 = new Car();
car1.SetDriver(john);

Car car2 = new Car();
car2.SetDriver(john); // Same driver, different car!
```

### Comparison:

| Feature          | Composition    | Aggregation        |
| ---------------- | -------------- | ------------------ |
| **Ownership**    | Strong         | Weak               |
| **Creation**     | Owner creates  | Comes from outside |
| **Lifetime**     | Dependent      | Independent        |
| **Example**      | Car-Engine     | Car-Driver         |
| **UML notation** | Filled diamond | Empty diamond      |

---

## Composition over Inheritance

One of the most important principles in software development: **"Prefer composition over inheritance"**.

### Why?

1. **Flexibility** - You can swap parts at runtime
2. **Avoid hierarchy issues** - No deep inheritance spiral
3. **Better reuse** - Parts work in many contexts
4. **Easier to test** - Test parts separately

### Example: Game Character

```csharp
// ❌ BAD: Inheritance hierarchy
public abstract class Character { }
public class Warrior : Character { }
public class Mage : Character { }
public class Archer : Character { }
public class WarriorMage : ??? { } // Problem! Can't inherit from both!

// ✅ GOOD: Composition (Component Pattern)
public interface IAbility
{
    void Use();
    string Name { get; }
}

public class MeleeAttack : IAbility
{
    public string Name => "Melee attack";
    public void Use() => Console.WriteLine("Strikes with sword!");
}

public class MagicSpell : IAbility
{
    public string Name => "Magic spell";
    public void Use() => Console.WriteLine("Casts fireball!");
}

public class RangedAttack : IAbility
{
    public string Name => "Ranged attack";
    public void Use() => Console.WriteLine("Shoots arrow!");
}

public class Healing : IAbility
{
    public string Name => "Healing";
    public void Use() => Console.WriteLine("Heals wounds!");
}

// Character is composed of abilities
public class Character
{
    public string Name { get; set; }
    private List<IAbility> abilities = new List<IAbility>();

    public void AddAbility(IAbility ability)
    {
        abilities.Add(ability);
        Console.WriteLine($"{Name} learned ability: {ability.Name}");
    }

    public void UseAllAbilities()
    {
        Console.WriteLine($"\n{Name} uses all abilities:");
        foreach (var ability in abilities)
        {
            ability.Use();
        }
    }
}

// Usage - full flexibility!
Character warrior = new Character { Name = "Warrior" };
warrior.AddAbility(new MeleeAttack());

Character mage = new Character { Name = "Mage" };
mage.AddAbility(new MagicSpell());
mage.AddAbility(new Healing());

Character battlemage = new Character { Name = "Battlemage" };
battlemage.AddAbility(new MeleeAttack());
battlemage.AddAbility(new MagicSpell());
battlemage.AddAbility(new Healing());
// Can combine any abilities!

warrior.UseAllAbilities();
mage.UseAllAbilities();
battlemage.UseAllAbilities();
```

---

## Practical Examples

### Example 1: Computer

```csharp
public class CPU
{
    public string Model { get; set; }
    public double Speed { get; set; }
    public int Cores { get; set; }

    public void Process()
    {
        Console.WriteLine($"CPU: {Model} ({Cores} cores @ {Speed}GHz) processing data");
    }
}

public class RAM
{
    public int Capacity { get; set; }
    public string Type { get; set; }

    public void LoadData()
    {
        Console.WriteLine($"RAM: Loading data into {Capacity}GB {Type} memory");
    }
}

public class Storage
{
    public int Capacity { get; set; }
    public string Type { get; set; } // SSD, HDD

    public void Read()
    {
        Console.WriteLine($"Storage: Reading from {Type} ({Capacity}GB)");
    }

    public void Write()
    {
        Console.WriteLine($"Storage: Writing to {Type} ({Capacity}GB)");
    }
}

public class GPU
{
    public string Model { get; set; }
    public int VRAM { get; set; }

    public void Render()
    {
        Console.WriteLine($"GPU: {Model} ({VRAM}GB) rendering graphics");
    }
}

// Computer is composed of parts
public class Computer
{
    private readonly CPU cpu;
    private readonly RAM ram;
    private readonly Storage storage;
    private readonly GPU gpu; // Optional

    public string Brand { get; set; }
    public string Model { get; set; }

    // Composition - computer creates the parts
    public Computer(string brand, string model, bool hasGPU = false)
    {
        Brand = brand;
        Model = model;

        cpu = new CPU { Model = "Intel i7-12700K", Speed = 3.6, Cores = 12 };
        ram = new RAM { Capacity = 32, Type = "DDR5" };
        storage = new Storage { Capacity = 1000, Type = "NVMe SSD" };

        if (hasGPU)
        {
            gpu = new GPU { Model = "RTX 4080", VRAM = 16 };
        }
    }

    public void Boot()
    {
        Console.WriteLine($"\n═══ Booting {Brand} {Model} ═══");
        storage.Read();
        ram.LoadData();
        cpu.Process();
        if (gpu != null)
        {
            gpu.Render();
        }
        Console.WriteLine("Computer booted!\n");
    }

    public void RunApplication(string appName)
    {
        Console.WriteLine($"\n═══ Starting application: {appName} ═══");
        storage.Read();
        ram.LoadData();
        cpu.Process();
        if (gpu != null && appName.Contains("Game"))
        {
            gpu.Render();
        }
    }
}

// Usage:
Computer gamingPC = new Computer("Custom", "Gaming PC", hasGPU: true);
gamingPC.Boot();
gamingPC.RunApplication("Cyberpunk 2077 Game");

Computer officePC = new Computer("Dell", "OptiPlex", hasGPU: false);
officePC.Boot();
officePC.RunApplication("Microsoft Word");
```

### Example 2: Restaurant (Component Pattern)

```csharp
public class Kitchen
{
    public void PrepareFood(string dish)
    {
        Console.WriteLine($"Kitchen prepares: {dish}");
    }
}

public class WaitingStaff
{
    public void ServeFood(string dish, int tableNumber)
    {
        Console.WriteLine($"Waiter brings food: {dish} to table {tableNumber}");
    }

    public void TakeOrder(string order)
    {
        Console.WriteLine($"Waiter takes order: {order}");
    }
}

public class Bar
{
    public void PrepareDrink(string drink)
    {
        Console.WriteLine($"Bar prepares drink: {drink}");
    }
}

public class CashRegister
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Cash register processes payment: {amount:C}");
    }
}

// Restaurant is composed of parts
public class Restaurant
{
    private readonly Kitchen kitchen;
    private readonly WaitingStaff staff;
    private readonly Bar bar;
    private readonly CashRegister cashRegister;

    public string Name { get; set; }

    public Restaurant(string name)
    {
        Name = name;
        kitchen = new Kitchen();
        staff = new WaitingStaff();
        bar = new Bar();
        cashRegister = new CashRegister();
    }

    public void ServeCustomer(int tableNumber, string food, string drink, decimal price)
    {
        Console.WriteLine($"\n═══ {Name} - Table {tableNumber} ═══");

        staff.TakeOrder($"{food} and {drink}");
        kitchen.PrepareFood(food);
        bar.PrepareDrink(drink);
        staff.ServeFood(food, tableNumber);
        cashRegister.ProcessPayment(price);

        Console.WriteLine("Customer served!\n");
    }
}

// Usage:
Restaurant restaurant = new Restaurant("Little Deer");
restaurant.ServeCustomer(5, "Reindeer steak", "Coca-Cola", 25.50m);
restaurant.ServeCustomer(12, "Salmon pasta", "Beer", 18.90m);
```

---

## Design Patterns with Composition

### 1. Composite Pattern

```csharp
// Component
public interface IGraphic
{
    void Draw();
}

// Leaf
public class Circle : IGraphic
{
    public void Draw()
    {
        Console.WriteLine("Drawing circle");
    }
}

// Leaf
public class Rectangle : IGraphic
{
    public void Draw()
    {
        Console.WriteLine("Drawing rectangle");
    }
}

// Composite
public class Group : IGraphic
{
    private List<IGraphic> children = new List<IGraphic>();

    public void Add(IGraphic graphic)
    {
        children.Add(graphic);
    }

    public void Draw()
    {
        Console.WriteLine("Drawing group:");
        foreach (var child in children)
        {
            child.Draw();
        }
    }
}

// Usage:
Circle circle = new Circle();
Rectangle rect = new Rectangle();

Group group = new Group();
group.Add(circle);
group.Add(rect);
group.Add(new Circle());

group.Draw(); // Draws everything
```

### 2. Decorator Pattern

```csharp
public interface ICoffee
{
    string GetDescription();
    decimal GetCost();
}

// Base
public class SimpleCoffee : ICoffee
{
    public string GetDescription() => "Coffee";
    public decimal GetCost() => 2.00m;
}

// Decorator Base
public abstract class CoffeeDecorator : ICoffee
{
    protected ICoffee coffee;

    public CoffeeDecorator(ICoffee coffee)
    {
        this.coffee = coffee;
    }

    public virtual string GetDescription() => coffee.GetDescription();
    public virtual decimal GetCost() => coffee.GetCost();
}

// Concrete Decorators
public class Milk : CoffeeDecorator
{
    public Milk(ICoffee coffee) : base(coffee) { }

    public override string GetDescription() => coffee.GetDescription() + ", Milk";
    public override decimal GetCost() => coffee.GetCost() + 0.50m;
}

public class Sugar : CoffeeDecorator
{
    public Sugar(ICoffee coffee) : base(coffee) { }

    public override string GetDescription() => coffee.GetDescription() + ", Sugar";
    public override decimal GetCost() => coffee.GetCost() + 0.25m;
}

// Usage:
ICoffee coffee = new SimpleCoffee();
coffee = new Milk(coffee);
coffee = new Sugar(coffee);

Console.WriteLine($"{coffee.GetDescription()}: {coffee.GetCost():C}");
// Output: "Coffee, Milk, Sugar: $2.75"
```

---

## Best Practices

### ✅ DO (Do This):

1. **Prefer composition over inheritance**

```csharp
// ✅ GOOD
public class Car
{
    private Engine engine; // Has-a
}
```

2. **Use interfaces for flexibility**

```csharp
// ✅ GOOD
public class Car
{
    private IEngine engine; // Can be swapped!
}
```

3. **Dependency Injection**

```csharp
// ✅ GOOD - Inject dependencies
public class Car
{
    private IEngine engine;

    public Car(IEngine engine)
    {
        this.engine = engine;
    }
}
```

4. **Keep classes small**

```csharp
// ✅ GOOD - One responsibility per class
public class Engine { } // Engine only
public class Tire { }   // Tire only
```

### ❌ DON'T (Don't Do This):

1. **Don't create God Objects**

```csharp
// ❌ BAD - Too complex
public class Car
{
    // 500 lines of code for everything...
}
```

2. **Don't use inheritance for "has-a" relationships**

```csharp
// ❌ BAD - Car is NOT an Engine!
public class Car : Engine { }
```

3. **Don't expose internal parts**

```csharp
// ❌ BAD
public class Car
{
    public Engine Engine { get; set; } // Exposes internal part!
}

// ✅ GOOD
public class Car
{
    private Engine engine; // Hidden

    public void Start()
    {
        engine.Start(); // Delegation
    }
}
```

---

## Common Mistakes

### Mistake 1: Wrong Relationship

```csharp
// ❌ WRONG - Using inheritance for wrong relationship
public class Car : Engine { } // Car is not an Engine!

// ✅ CORRECT
public class Car
{
    private Engine engine; // Car has an Engine
}
```

### Mistake 2: Too Tight Coupling

```csharp
// ❌ BAD - Tied to concrete class
public class Car
{
    private PetrolEngine engine; // Only petrol engine!
}

// ✅ GOOD - Interface
public class Car
{
    private IEngine engine; // Any engine
}
```

### Mistake 3: No Delegation

```csharp
// ❌ BAD - Car exposes Engine
public class Car
{
    public Engine Engine { get; set; }
}

// From outside:
car.Engine.Start(); // Shouldn't be visible!

// ✅ GOOD - Delegation
public class Car
{
    private Engine engine;

    public void Start()
    {
        engine.Start(); // Car delegates to Engine
    }
}

// From outside:
car.Start(); // Clear!
```

---

## Summary

Composition is one of the most important principles in software development.

### Remember:

- ✅ **"Has-a"** relationship - owns parts
- ✅ **Composition over Inheritance** - prefer composition
- ✅ **Flexibility** - you can swap parts
- ✅ **Modularity** - small, independent parts
- ✅ **Testability** - test parts separately
- ✅ **Reuse** - parts work in many contexts

### Composition vs:

- **Inheritance**: Has-a vs Is-a
- **Aggregation**: Strong ownership vs Weak ownership

### Composition enables:

- 🧩 Modular structure
- 🔄 Swapping parts at runtime
- 🧪 Easy testability
- 📦 Better reuse
- 🎯 Single Responsibility Principle

**Next step:** You have now covered all core OOP concepts! Continue to the [Design Principles](../04-Advanced/Design-Principles.md) and [Design Patterns](../04-Advanced/Design-Patterns.md) materials.

---
