# Inheritance

## Table of Contents

1. [Introduction](#introduction)
2. [What is Inheritance?](#what-is-inheritance)
3. [Problem It Solves](#problem-it-solves)
4. [Basic Syntax](#basic-syntax)
5. [Virtual, Override, and Base](#virtual-override-and-base)
6. [Abstract Classes](#abstract-classes)
7. [Sealed Classes](#sealed-classes)
8. [Inheritance Hierarchies](#inheritance-hierarchies)
9. [When to Use Inheritance?](#when-to-use-inheritance)
10. [Pitfalls and Warnings](#pitfalls-and-warnings)
11. [Best Practices](#best-practices)
12. [Summary](#summary)

---

## Introduction

Inheritance is one of the four fundamental pillars of object-oriented programming. It enables **code reuse** and the creation of **hierarchical structures**.

**In short:** Inheritance describes an **"is-a"** relationship: "A Dog IS an Animal", "A Car IS a Vehicle".

---

## What is Inheritance?

Inheritance is a mechanism where a **new class (derived class/child class)** can inherit properties and methods from an **existing class (base class/parent class)**.

```csharp
// Base class (parent class, superclass)
public class Animal
{
    public string Name { get; set; }
    public void Eat() => Console.WriteLine($"{Name} eats");
}

// Derived class (child class, subclass)
public class Dog : Animal  // Dog inherits from Animal
{
    public void Bark() => Console.WriteLine($"{Name} barks");
}

// Usage:
Dog dog = new Dog { Name = "Rex" };
dog.Eat();  // ✅ Inherited from Animal
dog.Bark(); // ✅ Dog's own method
```

**Benefits of Inheritance:**
- ✅ Avoids code duplication (DRY - Don't Repeat Yourself)
- ✅ Creates logical hierarchies
- ✅ Enables polymorphism
- ✅ Facilitates maintenance

---

## Problem It Solves

### Without Inheritance (Problem)

```csharp
// ❌ BAD: Same code repeats in multiple classes
public class Dog
{
    public string Name { get; set; }      // Duplication!
    public int Age { get; set; }          // Duplication!
    public string Species { get; set; }   // Duplication!
    
    public void Eat()                     // Duplication!
    {
        Console.WriteLine($"{Name} eats");
    }
    
    public void Sleep()                   // Duplication!
    {
        Console.WriteLine($"{Name} sleeps");
    }
    
    public void Bark()                    // Only in Dog
    {
        Console.WriteLine($"{Name} barks: Woof woof!");
    }
}

public class Cat
{
    public string Name { get; set; }      // Duplication!
    public int Age { get; set; }          // Duplication!
    public string Species { get; set; }   // Duplication!
    
    public void Eat()                     // Duplication!
    {
        Console.WriteLine($"{Name} eats");
    }
    
    public void Sleep()                   // Duplication!
    {
        Console.WriteLine($"{Name} sleeps");
    }
    
    public void Meow()                    // Only in Cat
    {
        Console.WriteLine($"{Name} meows: Meow!");
    }
}

public class Bird
{
    // ... same duplication continues...
}
```

**Problems:**
- ❌ Code duplication
- ❌ Changes need to be made in multiple places
- ❌ Easy to forget updating some class
- ❌ Difficult to maintain
- ❌ Doesn't scale (10+ animals = lots of duplication)

### With Inheritance (Solution)

```csharp
// ✅ GOOD: Common functionality in base class
public class Animal
{
    // Common properties
    public string Name { get; set; }
    public int Age { get; set; }
    public string Species { get; set; }
    
    // Common methods
    public void Eat()
    {
        Console.WriteLine($"{Name} eats");
    }
    
    public void Sleep()
    {
        Console.WriteLine($"{Name} sleeps");
    }
    
    // Virtual method that derived classes can override
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} makes a sound");
    }
}

// ✅ Dog inherits from Animal - no duplication!
public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} barks: Woof woof!");
    }
    
    public void Fetch()
    {
        Console.WriteLine($"{Name} fetches the ball");
    }
}

// ✅ Cat inherits from Animal - no duplication!
public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} meows: Meow!");
    }
    
    public void Climb()
    {
        Console.WriteLine($"{Name} climbs a tree");
    }
}

// ✅ Bird inherits from Animal - no duplication!
public class Bird : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} sings: Chirp chirp!");
    }
    
    public void Fly()
    {
        Console.WriteLine($"{Name} flies");
    }
}
```

**Benefits:**
- ✅ Common code in one place
- ✅ Changes made once
- ✅ Easy to add new animals
- ✅ Clear structure

---

## Basic Syntax

### Simple Inheritance

```csharp
// Basic form:
public class BaseClass
{
    // Base class members
}

public class DerivedClass : BaseClass
{
    // Derived class members + inherited members
}
```

### Example: Vehicle Hierarchy

```csharp
// Base class
public class Vehicle
{
    public string Brand { get; set; }
    public int Year { get; set; }
    public string Color { get; set; }
    
    public void Start()
    {
        Console.WriteLine($"{Brand} starts");
    }
    
    public void Stop()
    {
        Console.WriteLine($"{Brand} stops");
    }
    
    public virtual void Honk()
    {
        Console.WriteLine("Beep!");
    }
}

// Derived class: Car
public class Car : Vehicle
{
    public int NumberOfDoors { get; set; }
    public string BodyType { get; set; } // Sedan, SUV, Coupe...
    
    public override void Honk()
    {
        Console.WriteLine("Beep beep!");
    }
    
    public void OpenTrunk()
    {
        Console.WriteLine("Trunk opened");
    }
}

// Derived class: Motorcycle
public class Motorcycle : Vehicle
{
    public bool HasSidecar { get; set; }
    
    public override void Honk()
    {
        Console.WriteLine("Vroom vroom!");
    }
    
    public void DoWheelie()
    {
        Console.WriteLine("Rear wheel in the air!");
    }
}

// Usage:
Car car = new Car 
{ 
    Brand = "Toyota", 
    Year = 2023, 
    Color = "Blue",
    NumberOfDoors = 4,
    BodyType = "Sedan"
};

car.Start();        // Inherited from Vehicle
car.Honk();         // Overridden version
car.OpenTrunk();    // Car's own method
```

---

## Virtual, Override, and Base

### Virtual - Method That Can Be Overridden

```csharp
public class Animal
{
    // Virtual - derived classes CAN override (but don't have to)
    public virtual void MakeSound()
    {
        Console.WriteLine("Some sound");
    }
    
    // Regular method - CANNOT be overridden
    public void Breathe()
    {
        Console.WriteLine("Breathing");
    }
}
```

### Override - Override Base Class Method

```csharp
public class Dog : Animal
{
    // Override - overrides the base class virtual method
    public override void MakeSound()
    {
        Console.WriteLine("Woof woof!");
    }
}
```

### Base - Reference to Base Class

```csharp
public class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    public Shape(string name, string color)
    {
        Name = name;
        Color = color;
        Console.WriteLine($"Shape created: {name}");
    }
    
    public virtual double CalculateArea()
    {
        return 0;
    }
    
    public virtual void Display()
    {
        Console.WriteLine($"Shape: {Name}, Color: {Color}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    // Constructor calls base class constructor
    public Circle(string name, string color, double radius) 
        : base(name, color)  // ← Calls Shape constructor
    {
        Radius = radius;
        Console.WriteLine($"Circle created, radius: {radius}");
    }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public override void Display()
    {
        base.Display();  // ← Calls base class Display method
        Console.WriteLine($"Radius: {Radius}, Area: {CalculateArea():F2}");
    }
}

// Usage:
Circle circle = new Circle("Circle", "Red", 5.0);
circle.Display();
// Output:
// Shape created: Circle
// Circle created, radius: 5
// Shape: Circle, Color: Red
// Radius: 5, Area: 78.54
```

### New - Hides Base Class Method (Rarely Used)

```csharp
public class Base
{
    public void Method()
    {
        Console.WriteLine("Base method");
    }
}

public class Derived : Base
{
    // new - hides base class method (does NOT override!)
    public new void Method()
    {
        Console.WriteLine("Derived method");
    }
}

// Usage:
Derived d = new Derived();
d.Method(); // "Derived method"

Base b = d;
b.Method(); // "Base method" ← Note! Different from override
```

⚠️ **Warning:** `new` is different from `override`. Usually `override` is the better choice.

---

## Abstract Classes

An **abstract class** is a class from which **you cannot create a direct instance**. It is intended only as a base class.

### When to Use?
- When you want to define a common foundation, but it doesn't make sense to create an instance of it
- When you want to force derived classes to implement certain methods

### Example: Shapes

```csharp
// ❌ Cannot create instance: new Shape() doesn't work
public abstract class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    // Abstract method - MUST be implemented in derived classes
    public abstract double CalculateArea();
    public abstract double CalculatePerimeter();
    
    // Regular method - can be used directly
    public virtual void Display()
    {
        Console.WriteLine($"Shape: {Name}, Color: {Color}");
        Console.WriteLine($"Area: {CalculateArea():F2}");
        Console.WriteLine($"Perimeter: {CalculatePerimeter():F2}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    // MUST implement abstract methods
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public override double CalculatePerimeter()
    {
        return 2 * Math.PI * Radius;
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
    
    public override double CalculatePerimeter()
    {
        return 2 * (Width + Height);
    }
}

public class Triangle : Shape
{
    public double Base { get; set; }
    public double Height { get; set; }
    public double SideA { get; set; }
    public double SideB { get; set; }
    public double SideC { get; set; }
    
    public override double CalculateArea()
    {
        return 0.5 * Base * Height;
    }
    
    public override double CalculatePerimeter()
    {
        return SideA + SideB + SideC;
    }
}

// Usage:
// Shape shape = new Shape(); // ❌ DOESN'T WORK - abstract!

Shape circle = new Circle { Name = "Circle", Color = "Blue", Radius = 5 };
Shape rectangle = new Rectangle { Name = "Rectangle", Color = "Red", Width = 4, Height = 6 };

circle.Display();
rectangle.Display();

// Polymorphism:
Shape[] shapes = { circle, rectangle };
foreach (Shape shape in shapes)
{
    shape.Display(); // Each uses its own implementation
}
```

### Abstract vs Virtual

| Feature | Abstract | Virtual |
|---------|----------|---------|
| Implementation | No implementation | Has implementation |
| Override | MUST override | Can override (not required) |
| Class | Only in abstract classes | In any class |
| Instance | Cannot create | Can create |

---

## Sealed Classes

A **sealed class** is a class from which **you cannot inherit**.

### When to Use?
- When you want to prevent inheritance
- For security reasons
- Performance (minor optimization)

```csharp
// ✅ Sealed - cannot inherit
public sealed class FinalClass
{
    public void DoSomething()
    {
        Console.WriteLine("This works");
    }
}

// ❌ DOESN'T WORK - cannot inherit from sealed class
// public class DerivedClass : FinalClass
// {
// }
```

### Sealed Methods

```csharp
public class Base
{
    public virtual void Method()
    {
        Console.WriteLine("Base");
    }
}

public class Middle : Base
{
    // Sealed - prevents further overriding
    public sealed override void Method()
    {
        Console.WriteLine("Middle");
    }
}

public class Final : Middle
{
    // ❌ DOESN'T WORK - Method is sealed
    // public override void Method() { }
}
```

---

## Inheritance Hierarchies

### Depth vs. Breadth

```csharp
// ❌ BAD: Too deep inheritance hierarchy
Animal
  ↓
Mammal
  ↓
Carnivore
  ↓
Canine
  ↓
Dog
  ↓
Labrador  // 6 levels!

// ✅ GOOD: Shallower hierarchy
Animal
  ↓
Dog (contains breed as property, not inheritance)
```

**Recommendation:** Keep inheritance hierarchy shallow (max 2-3 levels).

### Example: Employees

```csharp
// Basic hierarchy
public abstract class Employee
{
    public string Name { get; set; }
    public int Id { get; set; }
    public decimal BaseSalary { get; set; }
    
    public abstract decimal CalculateSalary();
    
    public virtual void Display()
    {
        Console.WriteLine($"ID: {Id}, Name: {Name}, Salary: {CalculateSalary():C}");
    }
}

public class FullTimeEmployee : Employee
{
    public decimal MonthlyBonus { get; set; }
    
    public override decimal CalculateSalary()
    {
        return BaseSalary + MonthlyBonus;
    }
}

public class PartTimeEmployee : Employee
{
    public int HoursWorked { get; set; }
    public decimal HourlyRate { get; set; }
    
    public override decimal CalculateSalary()
    {
        return HoursWorked * HourlyRate;
    }
}

public class Contractor : Employee
{
    public decimal ProjectFee { get; set; }
    
    public override decimal CalculateSalary()
    {
        return ProjectFee;
    }
}

// Usage:
Employee[] employees =
{
    new FullTimeEmployee { Name = "John", Id = 1, BaseSalary = 3000, MonthlyBonus = 500 },
    new PartTimeEmployee { Name = "Jane", Id = 2, HoursWorked = 80, HourlyRate = 25 },
    new Contractor { Name = "Bob", Id = 3, ProjectFee = 5000 }
};

foreach (Employee emp in employees)
{
    emp.Display(); // Polymorphism in action
}
```

---

## When to Use Inheritance?

### ✅ Use Inheritance When:

1. **"Is-a" relationship is truly clear**
```csharp
Dog is Animal  // ✅ Clear
Car is Vehicle // ✅ Clear
```

2. **You want to share common functionality**
```csharp
public abstract class Animal
{
    public void Eat() { ... }     // All animals eat
    public void Sleep() { ... }   // All animals sleep
}
```

3. **You want to use polymorphism**
```csharp
Animal[] animals = { new Dog(), new Cat(), new Bird() };
foreach (Animal animal in animals)
{
    animal.MakeSound(); // Each makes its own sound
}
```

### ❌ DON'T Use Inheritance When:

1. **Relationship is "has-a" not "is-a"**
```csharp
// ❌ BAD - Car is NOT an Engine!
public class Car : Engine { }

// ✅ GOOD - Car HAS an Engine
public class Car
{
    private Engine engine;
}
```

2. **You only want to share methods**
```csharp
// ❌ BAD - misusing inheritance for sharing
public class Logger
{
    public void Log(string msg) { ... }
}
public class UserService : Logger { } // ← Wrong!

// ✅ GOOD - use composition
public class UserService
{
    private Logger logger;
    public UserService(Logger logger) { this.logger = logger; }
}
```

3. **Class is already too complex**
```csharp
// ❌ If base class is already huge, inheritance makes it even more complex
```

---

## Pitfalls and Warnings

### 1. Fragile Base Class Problem

```csharp
// Base class changes can break derived classes
public class Base
{
    public virtual void Method()
    {
        Console.WriteLine("Base");
        Helper(); // Internal call
    }
    
    protected virtual void Helper()
    {
        Console.WriteLine("Helper");
    }
}

public class Derived : Base
{
    public override void Helper()
    {
        Console.WriteLine("Derived Helper");
        // Can cause surprises if Base changes
    }
}
```

**Solution:** Document clearly which methods can be overridden and how.

### 2. Violating Liskov Substitution Principle

```csharp
// ❌ BAD: Derived class violates base class contract
public class Bird
{
    public virtual void Fly()
    {
        Console.WriteLine("Flies");
    }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        throw new NotSupportedException("Penguin cannot fly!");
    }
}

// Problem:
Bird bird = new Penguin();
bird.Fly(); // ❌ Throws exception - surprising!
```

**Solution:** Design hierarchy better:
```csharp
// ✅ GOOD: Separate flying and non-flying birds
public abstract class Bird { }
public abstract class FlyingBird : Bird
{
    public abstract void Fly();
}
public class Sparrow : FlyingBird
{
    public override void Fly() { ... }
}
public class Penguin : Bird
{
    // No Fly method!
}
```

### 3. Too Deep Hierarchy

```csharp
// ❌ BAD: 6 levels of inheritance
GameObject → Entity → LivingEntity → Animal → Mammal → Dog

// ✅ GOOD: Shallow hierarchy + composition
GameObject → Entity (contains components)
```

### 4. Yo-Yo Problem

```csharp
// Hard to follow what happens when you need to jump up and down the hierarchy
public class A
{
    public virtual void Method() { B(); }
    protected virtual void B() { }
}

public class C : A
{
    protected override void B() { D(); }
    protected virtual void D() { }
}

public class E : C
{
    protected override void D() { }
}

// Hard to understand what E.Method() does!
```

---

## Best Practices

### ✅ DO (Do This):

1. **Use inheritance for "is-a" relationships**
```csharp
public class Dog : Animal { } // ✅ Dog IS an animal
```

2. **Keep hierarchies shallow (2-3 levels max)**
```csharp
Animal → Dog // ✅ Good
```

3. **Use abstract classes for common functionality**
```csharp
public abstract class Shape
{
    public abstract double Area();
}
```

4. **Document virtual methods**
```csharp
/// <summary>
/// Calculates the area of the shape.
/// Derived classes MUST override this method.
/// </summary>
public virtual double CalculateArea() { ... }
```

5. **Use sealed to prevent inheritance if needed**
```csharp
public sealed class SecurityCriticalClass { }
```

### ❌ DON'T (Don't Do This):

1. **Don't use inheritance just for sharing**
```csharp
// ❌ UserService is NOT a Logger
public class UserService : Logger { }
```

2. **Don't create too deep hierarchies**
```csharp
// ❌ 6+ levels is too much
```

3. **Don't violate Liskov Substitution Principle**
```csharp
// ❌ Derived class must not violate base class contract
```

4. **Don't use new to hide methods**
```csharp
// ❌ Use override, not new
public new void Method() { }
```

---

## Summary

Inheritance is a powerful tool, but it must be used wisely.

### Remember:
- ✅ Use for "is-a" relationships
- ✅ Keep hierarchies shallow
- ✅ Use abstract classes appropriately
- ✅ Document virtual methods
- ✅ Consider if composition is a better alternative
- ✅ Follow Liskov Substitution Principle

### When inheritance vs. composition?
- **Inheritance**: Clear "is-a" relationship, common functionality
- **Composition**: "Has-a" relationship, flexibility, less coupling

**Next step:** Once you master inheritance, continue to the [Polymorphism](Polymorphism.md) material, which builds on inheritance.

---
