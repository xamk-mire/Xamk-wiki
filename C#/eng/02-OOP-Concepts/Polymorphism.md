# Polymorphism

## Table of Contents

1. [Introduction](#introduction)
2. [What is Polymorphism?](#what-is-polymorphism)
3. [Problem It Solves](#problem-it-solves)
4. [Compile-time Polymorphism](#compile-time-polymorphism)
5. [Runtime Polymorphism](#runtime-polymorphism)
6. [Abstract Classes and Polymorphism](#abstract-classes-and-polymorphism)
7. [Interface-based Polymorphism](#interface-based-polymorphism)
8. [Practical Examples](#practical-examples)
9. [Benefits of Polymorphism](#benefits-of-polymorphism)
10. [Best Practices](#best-practices)
11. [Common Mistakes](#common-mistakes)
12. [Summary](#summary)

---

## Introduction

Polymorphism (from Greek "many forms") is one of the four fundamental pillars of object-oriented programming. It enables **using the same interface for different object types**.

**In short:** Polymorphism means you can treat different types of objects in a uniform way.

**Example:** All animals can make sounds, but each animal makes its own sound.

---

## What is Polymorphism?

Polymorphism is divided into two main types:

### 1. Compile-time Polymorphism (Static Polymorphism)
- **Method Overloading** - Same method name, different parameters
- **Operator Overloading** - Operator overloading
- Resolved at **compile time**

### 2. Runtime Polymorphism (Dynamic Polymorphism)
- **Method Overriding** - Overriding in inheritance
- **Virtual methods** - virtual/override
- **Abstract methods** - abstract/override
- **Interface implementations** - IInterface
- Resolved at **runtime**

```csharp
// Simple example:
Animal animal1 = new Dog();    // Polymorphism
Animal animal2 = new Cat();    // Polymorphism
Animal animal3 = new Bird();   // Polymorphism

// Same interface, different implementations:
animal1.MakeSound(); // "Woof woof!"
animal2.MakeSound(); // "Meow!"
animal3.MakeSound(); // "Chirp chirp!"
```

---

## Problem It Solves

### Without Polymorphism (Problem)

```csharp
// ❌ BAD: Need to check each type separately
public class AnimalHandler
{
    public void HandleAnimal(Animal animal)
    {
        // We have to check the type...
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
            Console.WriteLine("Chirp!");
        }
        else if (animal is Horse)
        {
            Console.WriteLine("Neigh!");
        }
        else if (animal is Cow)
        {
            Console.WriteLine("Moo!");
        }
        // ... If we have 20 animal types, this becomes huge!
    }
    
    public void FeedAnimals(List<Animal> animals)
    {
        foreach (Animal animal in animals)
        {
            // Same problem for every operation...
            if (animal is Dog)
            {
                Console.WriteLine("Feed dog food");
            }
            else if (animal is Cat)
            {
                Console.WriteLine("Feed cat food");
            }
            // ... etc
        }
    }
}
```

**Problems:**
- ❌ Lots of if-else statements
- ❌ Difficult to maintain
- ❌ Adding a new animal requires changes everywhere
- ❌ Easy to forget updating some place
- ❌ Violates Open/Closed Principle
- ❌ Doesn't scale

### With Polymorphism (Solution)

```csharp
// ✅ GOOD: Polymorphism handles everything
public abstract class Animal
{
    public string Name { get; set; }
    
    // Virtual method - can be overridden
    public abstract void MakeSound();
    public abstract void Eat();
}

public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} barks: Woof woof!");
    }
    
    public override void Eat()
    {
        Console.WriteLine($"{Name} eats dog food");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} meows: Meow!");
    }
    
    public override void Eat()
    {
        Console.WriteLine($"{Name} eats cat food");
    }
}

public class Bird : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} sings: Chirp chirp!");
    }
    
    public override void Eat()
    {
        Console.WriteLine($"{Name} eats seeds");
    }
}

// ✅ Simple, scalable code
public class AnimalHandler
{
    public void HandleAnimal(Animal animal)
    {
        animal.MakeSound(); // ✅ No type checks!
    }
    
    public void FeedAnimals(List<Animal> animals)
    {
        foreach (Animal animal in animals)
        {
            animal.Eat(); // ✅ Simple!
        }
    }
    
    public void ProcessAnimals(Animal[] animals)
    {
        foreach (Animal animal in animals)
        {
            animal.MakeSound();
            animal.Eat();
        }
    }
}

// Usage:
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex" },
    new Cat { Name = "Whiskers" },
    new Bird { Name = "Tweety" },
    new Dog { Name = "Buddy" }
};

AnimalHandler handler = new AnimalHandler();
handler.ProcessAnimals(animals);
// Output:
// Rex barks: Woof woof!
// Rex eats dog food
// Whiskers meows: Meow!
// Whiskers eats cat food
// Tweety sings: Chirp chirp!
// Tweety eats seeds
// Buddy barks: Woof woof!
// Buddy eats dog food
```

**Benefits:**
- ✅ No type checks
- ✅ Easy to add new types
- ✅ Code stays simple
- ✅ Scalable
- ✅ Follows Open/Closed Principle

---

## Compile-time Polymorphism

### Method Overloading

Same method name, **different parameters**. Resolved at **compile time**.

```csharp
public class Calculator
{
    // Same name "Add", different parameters
    public int Add(int a, int b)
    {
        Console.WriteLine("Int version");
        return a + b;
    }
    
    public double Add(double a, double b)
    {
        Console.WriteLine("Double version");
        return a + b;
    }
    
    public int Add(int a, int b, int c)
    {
        Console.WriteLine("Three parameters");
        return a + b + c;
    }
    
    public string Add(string a, string b)
    {
        Console.WriteLine("String version");
        return a + b;
    }
}

// Usage:
Calculator calc = new Calculator();
calc.Add(5, 3);           // Calls int version → 8
calc.Add(5.5, 3.2);       // Calls double version → 8.7
calc.Add(1, 2, 3);        // Calls three parameter version → 6
calc.Add("Hello", " World"); // Calls string version → "Hello World"
```

### Examples of Method Overloading

```csharp
public class Printer
{
    // Printing different types
    public void Print(int value)
    {
        Console.WriteLine($"Number: {value}");
    }
    
    public void Print(string value)
    {
        Console.WriteLine($"Text: {value}");
    }
    
    public void Print(double value)
    {
        Console.WriteLine($"Decimal: {value:F2}");
    }
    
    public void Print(int[] values)
    {
        Console.WriteLine($"Array: [{string.Join(", ", values)}]");
    }
    
    // Different number of parameters
    public void Print(string value, bool uppercase)
    {
        Console.WriteLine(uppercase ? value.ToUpper() : value);
    }
}

// Usage:
Printer printer = new Printer();
printer.Print(42);                    // "Number: 42"
printer.Print("Hello");               // "Text: Hello"
printer.Print(3.14159);               // "Decimal: 3.14"
printer.Print(new int[] { 1, 2, 3 }); // "Array: [1, 2, 3]"
printer.Print("hello", true);         // "HELLO"
```

### Optional Parameters vs Overloading

```csharp
// Option 1: Overloading
public void Connect(string server)
{
    Connect(server, 80); // Default port
}

public void Connect(string server, int port)
{
    Console.WriteLine($"Connecting: {server}:{port}");
}

// Option 2: Optional parameters (often better)
public void Connect(string server, int port = 80)
{
    Console.WriteLine($"Connecting: {server}:{port}");
}

// Both work:
Connect("example.com");      // Uses port 80
Connect("example.com", 443); // Uses port 443
```

---

## Runtime Polymorphism

### Method Overriding (Virtual/Override)

Derived class **overrides** base class method. Resolved at **runtime**.

```csharp
// Base class
public class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    // Virtual - can be overridden
    public virtual double CalculateArea()
    {
        return 0;
    }
    
    public virtual void Draw()
    {
        Console.WriteLine($"Drawing {Name}");
    }
    
    public virtual void DisplayInfo()
    {
        Console.WriteLine($"Shape: {Name}");
        Console.WriteLine($"Color: {Color}");
        Console.WriteLine($"Area: {CalculateArea():F2}");
    }
}

// Derived classes override methods
public class Circle : Shape
{
    public double Radius { get; set; }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public override void Draw()
    {
        Console.WriteLine($"Drawing circle, radius: {Radius}");
    }
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }
    
    public override double CalculateArea()
    {
        return Width * Height;
    }
    
    public override void Draw()
    {
        Console.WriteLine($"Drawing rectangle, {Width}x{Height}");
    }
}

public class Triangle : Shape
{
    public double Base { get; set; }
    public double Height { get; set; }
    
    public override double CalculateArea()
    {
        return 0.5 * Base * Height;
    }
    
    public override void Draw()
    {
        Console.WriteLine($"Drawing triangle, base: {Base}, height: {Height}");
    }
}

// ✅ Polymorphism in action
public class ShapeProcessor
{
    public void ProcessShapes(Shape[] shapes)
    {
        double totalArea = 0;
        
        foreach (Shape shape in shapes)
        {
            shape.Draw();              // Calls correct version
            double area = shape.CalculateArea(); // Calls correct version
            Console.WriteLine($"Area: {area:F2}\n");
            totalArea += area;
        }
        
        Console.WriteLine($"Total area: {totalArea:F2}");
    }
}

// Usage:
Shape[] shapes = new Shape[]
{
    new Circle { Name = "Circle", Color = "Red", Radius = 5 },
    new Rectangle { Name = "Rectangle", Color = "Blue", Width = 4, Height = 6 },
    new Triangle { Name = "Triangle", Color = "Green", Base = 4, Height = 3 }
};

ShapeProcessor processor = new ShapeProcessor();
processor.ProcessShapes(shapes);
```

### Runtime Type Resolution

```csharp
// Important concept: Type is resolved at runtime
Shape shape;

if (DateTime.Now.Hour < 12)
{
    shape = new Circle { Radius = 5 };
}
else
{
    shape = new Rectangle { Width = 4, Height = 6 };
}

// Compiler doesn't know which type, but polymorphism works!
shape.CalculateArea(); // Calls correct method at runtime
```

---

## Abstract Classes and Polymorphism

Abstract classes force derived classes to implement certain methods.

```csharp
// Abstract base class
public abstract class Vehicle
{
    public string Brand { get; set; }
    public string Model { get; set; }
    public int Year { get; set; }
    
    // Abstract methods - MUST implement
    public abstract void Start();
    public abstract void Stop();
    public abstract double CalculateFuelConsumption();
    
    // Virtual method - can override (not required)
    public virtual void Honk()
    {
        Console.WriteLine("Beep!");
    }
    
    // Regular method - cannot override
    public void DisplayInfo()
    {
        Console.WriteLine($"{Brand} {Model} ({Year})");
        Console.WriteLine($"Consumption: {CalculateFuelConsumption()} l/100km");
    }
}

public class Car : Vehicle
{
    public int NumberOfDoors { get; set; }
    
    public override void Start()
    {
        Console.WriteLine($"{Brand} {Model} starts");
    }
    
    public override void Stop()
    {
        Console.WriteLine($"{Brand} {Model} stops");
    }
    
    public override double CalculateFuelConsumption()
    {
        return 7.5; // Average
    }
    
    public override void Honk()
    {
        Console.WriteLine("Beep beep!");
    }
}

public class Truck : Vehicle
{
    public double LoadCapacity { get; set; }
    
    public override void Start()
    {
        Console.WriteLine($"{Brand} truck starts (heavy)");
    }
    
    public override void Stop()
    {
        Console.WriteLine($"{Brand} truck stops (long braking distance)");
    }
    
    public override double CalculateFuelConsumption()
    {
        return 25.0 + (LoadCapacity * 0.5); // Depends on load
    }
    
    public override void Honk()
    {
        Console.WriteLine("HONK HONK! (loud sound)");
    }
}

public class Motorcycle : Vehicle
{
    public bool HasSidecar { get; set; }
    
    public override void Start()
    {
        Console.WriteLine($"{Brand} motorcycle starts (vroom!)");
    }
    
    public override void Stop()
    {
        Console.WriteLine($"{Brand} motorcycle stops");
    }
    
    public override double CalculateFuelConsumption()
    {
        return HasSidecar ? 5.0 : 3.5;
    }
}

// Polymorphism in action:
public class VehicleFleet
{
    private List<Vehicle> vehicles = new List<Vehicle>();
    
    public void AddVehicle(Vehicle vehicle)
    {
        vehicles.Add(vehicle);
    }
    
    public void StartAll()
    {
        Console.WriteLine("Starting all vehicles:\n");
        foreach (Vehicle vehicle in vehicles)
        {
            vehicle.Start(); // Polymorphism!
        }
    }
    
    public void TestHorns()
    {
        Console.WriteLine("\nHorns:\n");
        foreach (Vehicle vehicle in vehicles)
        {
            vehicle.Honk(); // Polymorphism!
        }
    }
    
    public double CalculateTotalFuelConsumption()
    {
        double total = 0;
        foreach (Vehicle vehicle in vehicles)
        {
            total += vehicle.CalculateFuelConsumption(); // Polymorphism!
        }
        return total;
    }
}

// Usage:
VehicleFleet fleet = new VehicleFleet();
fleet.AddVehicle(new Car { Brand = "Toyota", Model = "Corolla", Year = 2023, NumberOfDoors = 4 });
fleet.AddVehicle(new Truck { Brand = "Volvo", Model = "FH16", Year = 2022, LoadCapacity = 20 });
fleet.AddVehicle(new Motorcycle { Brand = "Harley", Model = "Davidson", Year = 2023, HasSidecar = false });

fleet.StartAll();
fleet.TestHorns();
Console.WriteLine($"\nTotal consumption: {fleet.CalculateTotalFuelConsumption():F1} l/100km");
```

---

## Interface-based Polymorphism

Interfaces provide pure polymorphism without inheritance hierarchy.

```csharp
// Interfaces
public interface IDrawable
{
    void Draw();
    void Erase();
}

public interface IResizable
{
    void Resize(double scale);
}

public interface IMovable
{
    void Move(int x, int y);
}

// Classes can implement multiple interfaces
public class Circle : IDrawable, IResizable, IMovable
{
    public double Radius { get; set; }
    public int X { get; set; }
    public int Y { get; set; }
    
    public void Draw()
    {
        Console.WriteLine($"Drawing circle at ({X}, {Y}), radius: {Radius}");
    }
    
    public void Erase()
    {
        Console.WriteLine("Erasing circle");
    }
    
    public void Resize(double scale)
    {
        Radius *= scale;
        Console.WriteLine($"Circle size changed, new radius: {Radius}");
    }
    
    public void Move(int x, int y)
    {
        X = x;
        Y = y;
        Console.WriteLine($"Circle moved to ({X}, {Y})");
    }
}

public class TextBox : IDrawable, IMovable
{
    public string Text { get; set; }
    public int X { get; set; }
    public int Y { get; set; }
    
    public void Draw()
    {
        Console.WriteLine($"Drawing text '{Text}' at ({X}, {Y})");
    }
    
    public void Erase()
    {
        Console.WriteLine("Erasing text");
    }
    
    public void Move(int x, int y)
    {
        X = x;
        Y = y;
        Console.WriteLine($"Text moved to ({X}, {Y})");
    }
}

// Polymorphism through interfaces
public class DrawingCanvas
{
    private List<IDrawable> drawables = new List<IDrawable>();
    
    public void Add(IDrawable drawable)
    {
        drawables.Add(drawable);
    }
    
    public void DrawAll()
    {
        foreach (IDrawable drawable in drawables)
        {
            drawable.Draw(); // Polymorphism!
        }
    }
    
    public void MoveAllDrawables(int deltaX, int deltaY)
    {
        foreach (IDrawable drawable in drawables)
        {
            // Check if it supports movement
            if (drawable is IMovable movable)
            {
                movable.Move(deltaX, deltaY);
            }
        }
    }
    
    public void ResizeAllResizables(double scale)
    {
        foreach (IDrawable drawable in drawables)
        {
            if (drawable is IResizable resizable)
            {
                resizable.Resize(scale);
            }
        }
    }
}
```

---

## Practical Examples

### Example 1: Payment Processing

```csharp
// Abstract base class
public abstract class PaymentMethod
{
    public string AccountHolder { get; set; }
    
    public abstract bool ProcessPayment(decimal amount);
    public abstract string GetPaymentDetails();
    
    public virtual void LogTransaction(decimal amount)
    {
        Console.WriteLine($"[{DateTime.Now}] Payment processed: {amount:C}");
    }
}

public class CreditCard : PaymentMethod
{
    public string CardNumber { get; set; }
    public DateTime ExpiryDate { get; set; }
    
    public override bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Paying with credit card: {amount:C}");
        // Real logic here...
        LogTransaction(amount);
        return true;
    }
    
    public override string GetPaymentDetails()
    {
        return $"Credit card: ****{CardNumber.Substring(CardNumber.Length - 4)}";
    }
}

public class PayPal : PaymentMethod
{
    public string Email { get; set; }
    
    public override bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Paying with PayPal ({Email}): {amount:C}");
        LogTransaction(amount);
        return true;
    }
    
    public override string GetPaymentDetails()
    {
        return $"PayPal: {Email}";
    }
}

public class BankTransfer : PaymentMethod
{
    public string BankAccount { get; set; }
    public string BankName { get; set; }
    
    public override bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Bank transfer ({BankName}): {amount:C}");
        LogTransaction(amount);
        return true;
    }
    
    public override string GetPaymentDetails()
    {
        return $"Bank transfer: {BankName} - {BankAccount}";
    }
}

// Payment Processor - polymorphism!
public class PaymentProcessor
{
    public void ProcessPayments(List<PaymentMethod> payments, decimal amount)
    {
        foreach (PaymentMethod payment in payments)
        {
            Console.WriteLine($"Payment method: {payment.GetPaymentDetails()}");
            payment.ProcessPayment(amount);
            Console.WriteLine();
        }
    }
}

// Usage:
List<PaymentMethod> paymentMethods = new List<PaymentMethod>
{
    new CreditCard { AccountHolder = "John", CardNumber = "1234567890123456", ExpiryDate = DateTime.Now.AddYears(2) },
    new PayPal { AccountHolder = "Jane", Email = "jane@example.com" },
    new BankTransfer { AccountHolder = "Bob", BankAccount = "FI1234567890", BankName = "Nordea" }
};

PaymentProcessor processor = new PaymentProcessor();
processor.ProcessPayments(paymentMethods, 99.99m);
```

### Example 2: Document Processing

```csharp
public interface IDocument
{
    string Title { get; set; }
    void Open();
    void Save();
    void Print();
}

public class WordDocument : IDocument
{
    public string Title { get; set; }
    public string Content { get; set; }
    
    public void Open()
    {
        Console.WriteLine($"Opening Word document: {Title}");
    }
    
    public void Save()
    {
        Console.WriteLine($"Saving Word document: {Title}");
    }
    
    public void Print()
    {
        Console.WriteLine($"Printing Word document: {Title}");
        Console.WriteLine($"Content: {Content}");
    }
}

public class ExcelSpreadsheet : IDocument
{
    public string Title { get; set; }
    public int Rows { get; set; }
    public int Columns { get; set; }
    
    public void Open()
    {
        Console.WriteLine($"Opening Excel spreadsheet: {Title}");
    }
    
    public void Save()
    {
        Console.WriteLine($"Saving Excel spreadsheet: {Title}");
    }
    
    public void Print()
    {
        Console.WriteLine($"Printing Excel spreadsheet: {Title}");
        Console.WriteLine($"Size: {Rows} rows x {Columns} columns");
    }
}

public class PdfDocument : IDocument
{
    public string Title { get; set; }
    public int PageCount { get; set; }
    
    public void Open()
    {
        Console.WriteLine($"Opening PDF document: {Title}");
    }
    
    public void Save()
    {
        Console.WriteLine("PDF is read-only, cannot save");
    }
    
    public void Print()
    {
        Console.WriteLine($"Printing PDF: {Title} ({PageCount} pages)");
    }
}

// Document Manager
public class DocumentManager
{
    public void ProcessDocuments(IDocument[] documents)
    {
        foreach (IDocument doc in documents)
        {
            doc.Open();
            doc.Print();
            doc.Save();
            Console.WriteLine();
        }
    }
}
```

---

## Benefits of Polymorphism

### 1. Flexibility
```csharp
// You can add new types without breaking existing code
public class NewAnimal : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("New sound!");
    }
}
// All existing code works immediately!
```

### 2. Extensibility (Open/Closed Principle)
```csharp
// Classes are open for extension, but closed for modification
// Don't need to change AnimalHandler class when adding a new animal
```

### 3. Less Code
```csharp
// Without polymorphism: 50 lines of if-else statements
// With polymorphism: 5 lines of clear code
```

### 4. Easy to Test
```csharp
// You can create mock objects from interfaces
public class MockAnimal : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Test sound");
    }
}
```

---

## Best Practices

### ✅ DO (Do This):

1. **Use polymorphism to avoid type checks**
```csharp
// ✅ GOOD
animal.MakeSound();

// ❌ BAD
if (animal is Dog) { ... }
```

2. **Use interfaces for flexibility**
```csharp
// ✅ GOOD
public void ProcessPayment(IPaymentMethod payment) { }

// ❌ BAD
public void ProcessPayment(CreditCard card) { } // Limited
```

3. **Design interfaces carefully**
```csharp
// ✅ GOOD - Small, focused interface
public interface IDrawable
{
    void Draw();
}

// ❌ BAD - Too large interface
public interface IEverything
{
    void Draw();
    void Save();
    void Load();
    void Print();
    void Email();
    void Export();
    // ... 20 methods ...
}
```

4. **Document virtual methods**
```csharp
/// <summary>
/// Calculates the animal's daily food requirement in kilograms.
/// Derived classes should override this method based on animal size.
/// </summary>
public virtual double CalculateDailyFood() { return 1.0; }
```

### ❌ DON'T (Don't Do This):

1. **Don't check type instead of using polymorphism**
```csharp
// ❌ BAD
if (shape is Circle)
{
    ((Circle)shape).DrawCircle();
}

// ✅ GOOD
shape.Draw();
```

2. **Don't violate Liskov Substitution Principle**
```csharp
// ❌ BAD - Square doesn't behave correctly as Rectangle
public class Square : Rectangle
{
    public override void SetWidth(int width)
    {
        base.SetWidth(width);
        base.SetHeight(width); // Also changes height!
    }
}
```

3. **Don't overload incorrectly**
```csharp
// ❌ Confusing - different functionality with same name
public int Calculate(int a, int b)
{
    return a + b; // Addition
}

public int Calculate(int a, int b, int c)
{
    return a * b * c; // Multiplication? Why?
}
```

---

## Common Mistakes

### Mistake 1: Wrong Casting

```csharp
// ❌ BAD
Animal animal = new Dog();
Cat cat = (Cat)animal; // ❌ Runtime error!

// ✅ GOOD - check first
if (animal is Cat cat)
{
    cat.Meow();
}

// OR
Cat cat = animal as Cat;
if (cat != null)
{
    cat.Meow();
}
```

### Mistake 2: Forgetting Override

```csharp
// ❌ BAD - no override
public class Dog : Animal
{
    public void MakeSound() // Doesn't override!
    {
        Console.WriteLine("Woof!");
    }
}

// ✅ GOOD
public class Dog : Animal
{
    public override void MakeSound() // Overrides!
    {
        Console.WriteLine("Woof!");
    }
}
```

### Mistake 3: Ambiguous Parameters

```csharp
// ❌ Confusing
public void Process(int value) { }
public void Process(long value) { }

Process(10); // Which is called? int (but not clear)
```

---

## Summary

Polymorphism is a powerful tool that makes code flexible and maintainable.

### Remember:
- ✅ **Compile-time**: Method overloading, operator overloading
- ✅ **Runtime**: Method overriding, virtual/abstract/interface
- ✅ Avoid type checks (is, as)
- ✅ Use interfaces for flexibility
- ✅ Follow Liskov Substitution Principle
- ✅ Keep interfaces small and focused

### Polymorphism enables:
- 🎯 Uniform handling of different objects
- 🔧 Easy extensibility
- 📦 Clean code without if-else statements
- ✨ Adherence to Open/Closed Principle

**Next step:** Once you master polymorphism, continue to the [Interfaces](Interfaces.md) and [Composition](Composition.md) materials.

---
