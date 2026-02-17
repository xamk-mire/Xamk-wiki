# What is OOP? (Object-Oriented Programming)

## Table of Contents

1. [Introduction](#introduction)
2. [Why Did OOP Emerge?](#why-did-oop-emerge)
3. [The Four Pillars of OOP](#the-four-pillars-of-oop)
4. [Additional OOP Techniques](#additional-oop-techniques)
5. [OOP vs Other Paradigms](#oop-vs-other-paradigms)
6. [Advantages and Disadvantages of OOP](#advantages-and-disadvantages-of-oop)
7. [When to Use OOP?](#when-to-use-oop)
8. [Summary](#summary)

---

## Introduction

**Object-Oriented Programming** (OOP) is a programming paradigm in which **programs are built from objects** that combine data and behavior in one place.

**Simply put:** Instead of writing code that handles data and functions separately, OOP combines them into **objects** that represent real-world things.

### Short Example:

```csharp
// ❌ Without OOP (Procedural style)
string dogName = "Rex";
int dogAge = 3;
void MakeDogSound(string name)
{
    Console.WriteLine($"{name} barks!");
}
MakeDogSound(dogName);

// ✅ With OOP
public class Dog
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public void MakeSound()
    {
        Console.WriteLine($"{Name} barks!");
    }
}

Dog dog = new Dog { Name = "Rex", Age = 3 };
dog.MakeSound();
```

**Benefits:**
- ✅ Data and behavior together
- ✅ Easier to understand (represents a real dog)
- ✅ Easy to create multiple dogs
- ✅ Can add new features easily

---

## Why Did OOP Emerge?

### Problem: Procedural Programming Became Too Complex

**In the 1960s–70s** programs were written **procedurally**:
- Functions that process data
- Data and logic separated
- As programs grew, they became hard to manage

```csharp
// Procedural example (1970s style)
string[] studentNames = new string[100];
int[] studentAges = new int[100];
double[] studentGrades = new double[100];

void AddStudent(int index, string name, int age, double grade)
{
    studentNames[index] = name;
    studentAges[index] = age;
    studentGrades[index] = grade;
}

void PrintStudent(int index)
{
    Console.WriteLine($"{studentNames[index]}, {studentAges[index]}, {studentGrades[index]}");
}

// Problems:
// - All arrays must be maintained separately
// - Easy to mix up indices
// - Hard to extend (add field → change everything)
```

### Solution: Object-Oriented Programming

**In the 1980s** OOP became widespread (C++, Smalltalk):
- Data and logic combined into **objects**
- Objects represent real things
- Easier to manage complexity

```csharp
// OOP example (modern style)
public class Student
{
    public string Name { get; set; }
    public int Age { get; set; }
    public double Grade { get; set; }
    
    public void Print()
    {
        Console.WriteLine($"{Name}, {Age} years old, Grade: {Grade}");
    }
    
    public bool IsPassing()
    {
        return Grade >= 1.0;
    }
}

List<Student> students = new List<Student>();
students.Add(new Student { Name = "John", Age = 20, Grade = 4.5 });
students.Add(new Student { Name = "Jane", Age = 22, Grade = 3.8 });

foreach (Student student in students)
{
    student.Print();
}

// Benefits:
// ✅ All student data in one place
// ✅ Easy to add new fields
// ✅ Methods can be called naturally: student.Print()
```

---

## The Four Pillars of OOP

OOP is based on **four core principles**:

### 1. 🔒 Encapsulation

**"Hide internal details, expose only what matters"**

Encapsulation means combining data and methods and **restricting access** to them.

```csharp
public class BankAccount
{
    private decimal balance; // ❌ No access from outside!
    
    public decimal Balance
    {
        get { return balance; }
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0) // ✅ Validation
        {
            balance += amount;
            Console.WriteLine($"Deposited: {amount:C}");
        }
    }
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance) // ✅ Safety
        {
            balance -= amount;
            Console.WriteLine($"Withdrawn: {amount:C}");
            return true;
        }
        Console.WriteLine("Not enough money!");
        return false;
    }
}

// Usage:
BankAccount account = new BankAccount();
account.Deposit(100);
account.Withdraw(30);
// account.balance = 1000000; // ❌ DOESN'T WORK - protected!
```

**Why important?**
- ✅ Prevents invalid data
- ✅ Can change internal implementation
- ✅ Better security

**Read more:** [Encapsulation](Encapsulation.md)

---

### 2. 👪 Inheritance

**"Create new classes based on existing ones"**

Inheritance enables an **"is-a"** relationship: "A dog IS an animal".

```csharp
// Base class (parent/base class)
public class Animal
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} makes a sound");
    }
    
    public void Eat()
    {
        Console.WriteLine($"{Name} eats");
    }
}

// Derived classes (child/derived classes)
public class Dog : Animal
{
    public string Breed { get; set; }
    
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} barks: Woof woof!");
    }
    
    public void Fetch()
    {
        Console.WriteLine($"{Name} fetches the ball");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} meows: Meow!");
    }
    
    public void Scratch()
    {
        Console.WriteLine($"{Name} scratches");
    }
}

// Usage:
Dog dog = new Dog { Name = "Rex", Age = 3, Breed = "Labrador" };
dog.MakeSound(); // "Rex barks: Woof woof!"
dog.Eat();       // Inherited from Animal
dog.Fetch();     // Only on Dog

Cat cat = new Cat { Name = "Whiskers", Age = 2 };
cat.MakeSound(); // "Whiskers meows: Meow!"
cat.Eat();       // Inherited from Animal
cat.Scratch();   // Only on Cat
```

**Why important?**
- ✅ Avoid code duplication
- ✅ Common behavior in one place
- ✅ Keeps hierarchy clear

**Read more:** [Inheritance](Inheritance.md)

---

### 3. 🎭 Polymorphism

**"Same interface, different implementations"**

Polymorphism means **you can treat different types of objects the same way**.

```csharp
// Polymorphism in action
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex", Age = 3 },
    new Cat { Name = "Whiskers", Age = 2 },
    new Dog { Name = "Buddy", Age = 5 },
    new Cat { Name = "Fluffy", Age = 1 }
};

// Treat all the same way!
foreach (Animal animal in animals)
{
    animal.MakeSound(); // ✅ Calls the right version!
    animal.Eat();
    Console.WriteLine();
}

// Output:
// Rex barks: Woof woof!
// Rex eats
//
// Whiskers meows: Meow!
// Whiskers eats
//
// ... etc
```

**Why important?**
- ✅ No if-else for type checks
- ✅ Code stays simple
- ✅ Easy to add new types

**Read more:** [Polymorphism](Polymorphism.md)

---

### 4. 🎨 Abstraction

**"Hide complexity, show only what matters"**

Abstraction means **focusing on WHAT is done, not HOW**.

```csharp
// Abstract class - cannot instantiate directly
public abstract class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    // Abstract method - MUST implement in derived classes
    public abstract double CalculateArea();
    
    // Regular method - can use directly
    public void Display()
    {
        Console.WriteLine($"{Color} {Name}, Area: {CalculateArea():F2}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
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
}

// Usage:
Shape[] shapes = new Shape[]
{
    new Circle { Name = "Circle", Color = "Red", Radius = 5 },
    new Rectangle { Name = "Rectangle", Color = "Blue", Width = 4, Height = 6 }
};

foreach (Shape shape in shapes)
{
    shape.Display(); // ✅ Polymorphism + Abstraction!
}
```

**Why important?**
- ✅ Enforces a consistent structure
- ✅ Hides complexity
- ✅ Easy to extend

**Read more:** [Interfaces](Interfaces.md) and [Polymorphism](Polymorphism.md)

---

## Additional OOP Techniques

### 5. 🧩 Composition

**"Build complex objects from simpler parts"**

Composition describes a **"has-a"** (owns) relationship: "A car HAS an engine".

```csharp
// Parts
public class Engine
{
    public void Start() => Console.WriteLine("Engine starts");
    public void Stop() => Console.WriteLine("Engine stops");
}

public class Wheel
{
    public string Brand { get; set; }
    public void Rotate() => Console.WriteLine($"{Brand} wheel rotates");
}

// Car is composed of parts
public class Car
{
    private Engine engine;    // Car HAS-A Engine
    private Wheel[] wheels;   // Car HAS-A Wheels
    
    public string Brand { get; set; }
    
    public Car(string brand)
    {
        Brand = brand;
        engine = new Engine();
        wheels = new Wheel[4]
        {
            new Wheel { Brand = "Michelin" },
            new Wheel { Brand = "Michelin" },
            new Wheel { Brand = "Michelin" },
            new Wheel { Brand = "Michelin" }
        };
    }
    
    public void Start()
    {
        Console.WriteLine($"{Brand} starts");
        engine.Start();
        foreach (Wheel wheel in wheels)
        {
            wheel.Rotate();
        }
    }
    
    public void Stop()
    {
        Console.WriteLine($"{Brand} stops");
        engine.Stop();
    }
}

// Usage:
Car car = new Car("Toyota");
car.Start();
car.Stop();
```

**Why important?**
- ✅ More flexible than inheritance
- ✅ Can swap parts at runtime
- ✅ Avoids deep inheritance hierarchy

**"Composition over Inheritance"** – prefer composition over inheritance!

**Read more:** [Composition](Composition.md)

---

### 6. 🔌 Interfaces

**"Define a 'contract' for what a class must implement"**

Interfaces define **WHAT** must be done, but not **HOW**.

```csharp
// Interface - "contract"
public interface IFlyable
{
    void TakeOff();
    void Fly();
    void Land();
}

// Classes implement the contract
public class Airplane : IFlyable
{
    public void TakeOff() => Console.WriteLine("Airplane takes off from runway");
    public void Fly() => Console.WriteLine("Airplane flies");
    public void Land() => Console.WriteLine("Airplane lands");
}

public class Bird : IFlyable
{
    public void TakeOff() => Console.WriteLine("Bird takes flight");
    public void Fly() => Console.WriteLine("Bird flies");
    public void Land() => Console.WriteLine("Bird lands");
}

// Usage - polymorphism with interfaces
IFlyable[] flyers = new IFlyable[]
{
    new Airplane(),
    new Bird()
};

foreach (IFlyable flyer in flyers)
{
    flyer.TakeOff();
    flyer.Fly();
    flyer.Land();
    Console.WriteLine();
}
```

**Why important?**
- ✅ A class can implement **multiple** interfaces (vs one base class)
- ✅ Loose coupling
- ✅ Easy to test (mock objects)

**Read more:** [Interfaces](Interfaces.md)

---

## OOP vs Other Paradigms

### Procedural Programming (C, Pascal)

```csharp
// Procedural style
string[] names = new string[100];
int[] ages = new int[100];

void PrintPerson(int index)
{
    Console.WriteLine($"{names[index]}, {ages[index]}");
}
```

**Characteristics:**
- ✅ Simple for small programs
- ❌ Hard to manage large programs
- ❌ Data and logic separated

### Functional Programming (F#, Haskell)

```csharp
// Functional style in C#
var adults = people
    .Where(p => p.Age >= 18)
    .Select(p => p.Name)
    .ToList();
```

**Characteristics:**
- ✅ Immutable data
- ✅ Pure functions (no side effects)
- ⚠️ Can be harder to understand

### Object-Oriented Programming (C#, Java, Python)

```csharp
// OOP style
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public bool IsAdult() => Age >= 18;
}

List<Person> adults = people.Where(p => p.IsAdult()).ToList();
```

**Characteristics:**
- ✅ Clear structure
- ✅ Easy to model the real world
- ✅ Good for large projects

**In practice:** Modern C# combines all paradigms!

---

## Advantages and Disadvantages of OOP

### ✅ Advantages:

1. **Reusability**
```csharp
// Write once, use many times
public class Logger
{
    public void Log(string message) { }
}

// Used in many projects
```

2. **Modularity**
```csharp
// Break a big problem into smaller parts
public class Car
{
    private Engine engine;
    private GPS gps;
    private Radio radio;
}
```

3. **Maintainability**
```csharp
// Changes are localized
public class BankAccount
{
    // Change only this class, not all code
}
```

4. **Scalability**
```csharp
// Easy to add new features
public class NewAnimal : Animal { }
```

5. **Testability**
```csharp
// Test classes separately
[Test]
public void BankAccount_Deposit_IncreasesBalance()
{
    BankAccount account = new BankAccount();
    account.Deposit(100);
    Assert.AreEqual(100, account.Balance);
}
```

### ❌ Disadvantages:

1. **Complexity**
- Can be too complex for small programs
- Steeper learning curve

2. **Performance**
- Slightly slower than procedural (but rarely an issue)
- More memory

3. **Over-engineering**
- Easy to create overly complex structure
- "God objects" – classes that do too much

**Solution:** Use OOP **reasonably** – don't force everything into objects.

---

## When to Use OOP?

### ✅ Use OOP when:

- ✅ Large projects (1000+ lines)
- ✅ Team develops together
- ✅ You want to reuse code
- ✅ Modeling the real world (car, account, user)
- ✅ Project will grow over time

### ⚠️ Consider alternatives when:

- ⚠️ Small script (<100 lines)
- ⚠️ Simple data processing
- ⚠️ Performance is critical (game loop, real-time)

**Remember:** C# supports multiple paradigms – use the right tool for the job!

---

## Summary

### The four pillars of OOP:

| Pillar | Description | Key |
|--------|-------------|-----|
| **Encapsulation** | Hide internal details | Data + Methods together |
| **Inheritance** | Share common behavior | "Is-a" relationship |
| **Polymorphism** | Treat different objects the same way | Same interface |
| **Abstraction** | Hide complexity | WHAT, not HOW |

### Additional techniques:

- **Composition** – Build from parts ("has-a")
- **Interfaces** – Define contracts

### Why OOP?

- ✅ Easy to model the real world
- ✅ Clear structure for large projects
- ✅ Reusable and maintainable code
- ✅ Easy to test
- ✅ Suited for team work

---

## Next Steps

### 1. **Dive into individual concepts:**

Recommended learning order:

1. [Encapsulation](Encapsulation.md) – Start here!
2. [Inheritance](Inheritance.md)
3. [Polymorphism](Polymorphism.md)
4. [Interfaces](Interfaces.md)
5. [Composition](Composition.md)

### 2. **See the overview:**

- [OOP Techniques – Overview](OOP-Techniques-Overview.md) – Summary of all techniques

### 3. **Continue to advanced topics:**

- [Design Principles](../04-Advanced/Design-Principles.md) – SOLID principles
- [Design Patterns](../04-Advanced/Design-Patterns.md) – Reusable solution patterns

---

**Ready to start?** Begin with [Encapsulation](Encapsulation.md) and work through in order!
