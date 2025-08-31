# Object-Oriented Programming (OOP)

## Definition

**OOP** is a programming paradigm that models software as a set of **objects** that combine **state** (data) and **behavior** (methods). You design around **domain concepts** (Customer, Order, Invoice) rather than around sequences of actions.

> Goal: make complex systems easier to **reason about**, **extend**, and **maintain** by aligning code with real-world concepts.

---

## Why It Matters

1. **Model alignment** – Code mirrors domain language (easier to discuss with stakeholders).
2. **Encapsulation** – Hide internals; reduce coupling; protect invariants.
3. **Reusability & Extensibility** – Shared contracts and behavior (interfaces/abstractions).
4. **Testability** – Clear boundaries enable small, focused unit tests.

---

## Core Concepts (The Big Four)

1. **Encapsulation**
   Keep data private; expose operations that enforce invariants.
2. **Abstraction**
   Expose **what** something does, not **how** it does it (interfaces/base types).
3. **Inheritance**
   Share behavior via parent/child hierarchies (use sparingly).
4. **Polymorphism**
   Treat different types through a common interface and let each supply its own behavior.

---

## C# Mini-Examples (Encapsulation, Abstraction, Inheritance & Polymorphism)

Absolutely — here are **C#** examples for the four OOP pillars. For each one you’ll see a **bad** (anti-pattern) version, a **better** version, and an explanation of what changed and why it matters.

---

# 1) Encapsulation

> Keep state private and expose only safe operations that preserve invariants.

### ❌ Bad: Leaky state, broken invariants

```csharp
public class ShoppingCart
{
    public List<CartItem> Items = new();       // anyone can mutate
    public decimal Total;                       // caller can desync this from Items

    public void RecalculateTotal()
    {
        Total = Items.Sum(i => i.Price * i.Quantity);
    }
}

public class CartItem
{
    public string Sku;
    public decimal Price;
    public int Quantity;
}

// Somewhere else
var cart = new ShoppingCart();
cart.Items.Add(new CartItem { Sku = "ABC", Price = -5m, Quantity = 1000 }); // invalid!
cart.Total = 999_999m;                       // lies
```

**What’s wrong**

* Public fields allow **any** code to create invalid state (negative price, giant quantity).
* `Total` can diverge from `Items`. The class can’t protect itself.

### ✅ Better: Guard invariants, narrow surface

```csharp
public sealed class ShoppingCart
{
    private readonly List<CartItem> _items = new();
    public IReadOnlyList<CartItem> Items => _items; // expose read-only view

    public decimal Total => _items.Sum(i => i.Subtotal);

    public void AddItem(string sku, decimal price, int quantity)
    {
        _items.Add(CartItem.Create(sku, price, quantity));
    }

    public void RemoveItem(string sku)
    {
        var index = _items.FindIndex(i => i.Sku == sku);
        if (index >= 0) _items.RemoveAt(index);
    }
}

public sealed class CartItem
{
    public string Sku { get; }
    public decimal Price { get; }
    public int Quantity { get; }
    public decimal Subtotal => Price * Quantity;

    private CartItem(string sku, decimal price, int quantity)
    {
        Sku = sku;
        Price = price;
        Quantity = quantity;
    }

    public static CartItem Create(string sku, decimal price, int quantity)
    {
        if (string.IsNullOrWhiteSpace(sku)) throw new ArgumentException("SKU required.");
        if (price <= 0) throw new ArgumentOutOfRangeException(nameof(price));
        if (quantity <= 0) throw new ArgumentOutOfRangeException(nameof(quantity));
        return new CartItem(sku, price, quantity);
    }
}
```

**Why this is better**

* State is private; you can’t create invalid `CartItem`s.
* `Total` is derived, so it **can’t drift** out of sync.
* The type enforces its own rules (encapsulation preserves invariants).

---

# 2) Abstraction

> Depend on **what** something does (contract), not **how** it does it (concrete class).

### ❌ Bad: High-level code hard-wired to details

```csharp
public class ReportService
{
    public string BuildAndSendMonthlyReport()
    {
        // concrete dependencies baked in — hard to test and to change
        var repo = new SqlOrderRepository("connstring");
        var emailer = new SmtpEmailer("smtp.company");

        var data = repo.FetchMonthly();
        var body = string.Join("\n", data.Select(d => $"{d.Id}:{d.Total}"));
        emailer.Send("ops@company.com", "Monthly Report", body);

        return body;
    }
}
```

**What’s wrong**

* `ReportService` constructs concrete dependencies (DB + SMTP).
* You can’t unit test without a real DB/SMTP; swapping implementations is invasive.

### ✅ Better: Program to interfaces; inject dependencies

```csharp
public interface IOrderReadModel
{
    IEnumerable<OrderDto> FetchMonthly();
}

public interface IEmailer
{
    void Send(string to, string subject, string body);
}

public sealed class ReportService
{
    private readonly IOrderReadModel _orders;
    private readonly IEmailer _email;

    public ReportService(IOrderReadModel orders, IEmailer email)
    {
        _orders = orders;
        _email = email;
    }

    public string BuildAndSendMonthlyReport()
    {
        var data = _orders.FetchMonthly();
        var body = string.Join("\n", data.Select(d => $"{d.Id}:{d.Total:c}"));
        _email.Send("ops@company.com", "Monthly Report", body);
        return body;
    }
}
```

**Why this is better**

* `ReportService` depends on **abstractions** (`IOrderReadModel`, `IEmailer`).
* Works with any implementation (EF Core, HTTP API, in-memory fake).
* Testable and flexible (follows DIP; abstraction is an OOP superpower).

---

# 3) Inheritance

> Share and specialize behavior along a true **is-a** hierarchy. Prefer composition when in doubt.

### ❌ Bad: Base class forces behavior some children can’t support

```csharp
public class Vehicle
{
    public virtual void StartEngine()
    {
        // start an internal combustion or electric engine
    }

    public virtual void Move(int meters)
    {
        // generic movement
    }
}

public class Car : Vehicle
{
    public override void StartEngine() { /* vroom */ }
    public override void Move(int meters) { /* roll */ }
}

public class Bicycle : Vehicle
{
    public override void StartEngine()
    {
        // 🚨 LSP violation: bicycles don't have engines
        throw new NotSupportedException("Bicycles have no engine.");
    }

    public override void Move(int meters) { /* pedal */ }
}
```

**What’s wrong**

* The base class assumes every vehicle has an engine.
* Bicycle.StartEngine() must throw, which breaks Liskov Substitution Principle (LSP).
* Anywhere a Vehicle is expected, passing a Bicycle can produce runtime surprises.

### ✅ Better (Option A): Separate types under an abstract base

```csharp
public abstract class Vehicle
{
    public abstract void Move(int meters);
}

public abstract class MotorVehicle : Vehicle
{
    // Only motor vehicles know how to start engines
    public abstract void StartEngine();
}

public sealed class Car : MotorVehicle
{
    private bool _running;

    public override void StartEngine() => _running = true;

    public override void Move(int meters)
    {
        if (!_running) throw new InvalidOperationException("Engine not started.");
        // roll forward meters...
    }
}

public sealed class Bicycle : Vehicle
{
    public override void Move(int meters)
    {
        // pedal forward meters...
    }
}
```

**Why this is better**

* Vehicle models the common abstraction: “things that can move.”
* MotorVehicle adds engine-specific behavior without forcing it on all vehicles.
* Car : MotorVehicle (has an engine), Bicycle : Vehicle (no engine).
* Anywhere a Vehicle is expected, both Car and Bicycle work for movement; engine logic is isolated to motor vehicles—no surprises.

---

# 4) Polymorphism

> One message, many implementations. Avoid `switch`/`if` webs on type.

### ❌ Bad: Type switches (OCP violation, brittle)

```csharp
public enum AnimalType { Dog, Cat, Duck }

public class Animal
{
    public AnimalType Type { get; set; }
}

public static class AnimalSounds
{
    public static string Speak(Animal a)
    {
        return a.Type switch
        {
            AnimalType.Dog  => "Woof",
            AnimalType.Cat  => "Meow",
            AnimalType.Duck => "Quack",
            _ => "..."
        };
    }
}

// Adding a new animal requires editing this method every time.
```

**What’s wrong**

* Central “god switch” that must be edited for every new type (breaks **Open-Closed Principle**).
* Spreads behavior away from the objects that own it.

### ✅ Better: Dispatch to the object (dynamic polymorphism)

```csharp
public interface IAnimal
{
    string Speak();
}

public sealed class Dog : IAnimal { public string Speak() => "Woof"; }
public sealed class Cat : IAnimal { public string Speak() => "Meow"; }
public sealed class Duck : IAnimal { public string Speak() => "Quack"; }

// Client code
IEnumerable<IAnimal> animals = new IAnimal[] { new Dog(), new Cat(), new Duck() };
foreach (var a in animals)
{
    Console.WriteLine(a.Speak());  // polymorphic call; no switch needed
}
```

**Why this is better**

* Call sites don’t branch on type; adding a new animal means **adding a class**, not editing existing logic.
* Behavior lives with the type that knows it (Tell, Don’t Ask).

---

## Quick Review Checklist

* **Encapsulation**: Are fields private? Are invariants enforced in constructors/methods? Any “drifting” derived values?
* **Abstraction**: Do high-level policies depend on interfaces? Can we swap implementations and unit test easily?
* **Inheritance**: Is the relationship truly **is-a**? Does substitution hold (no surprises)? Could composition be cleaner?
* **Polymorphism**: Are there type switches you could replace with virtual/override or interface methods?


---

## Good OOP Design Habits

* **Favor composition over inheritance** (prefer assembling objects to deep class trees).
* **Program to interfaces** (DIP); inject dependencies.
* **Apply SRP and small classes** (one reason to change).
* **Keep invariants inside the type** (protect state, validate in constructors/mutators).
* **Use ubiquitous language** (names mirroring the domain).

---

## Common Pitfalls

* **God objects** (do-everything classes).
* **Deep inheritance hierarchies** (fragile base class problem).
* **Anemic domain models** (all data, no behavior; logic leaks elsewhere).
* **Over-abstraction** (interfaces for everything without need).
* **Tight coupling** (types know too much about each other’s internals).

---

## When OOP Shines vs. When to Rethink

* **Great for**: rich domain models, long-lived business apps, UI component systems, plugin architectures.
* **Consider alternatives**: data-heavy pipelines, pure transformations, or massively parallel numeric work—often simpler with **functional** or **data-oriented** styles.

---

## Quick Glossary

* **Class**: blueprint for objects.
* **Object**: instance with state + behavior.
* **Method**: behavior (function) on a class/object.
* **Property/Field**: exposed/hidden state.
* **Interface**: contract (no implementation).
* **Abstract class**: partial implementation + contract.
* **Virtual/Override**: hooks for polymorphic behavior.
* **Generic**: type-safe reuse across types.

---

### Bottom Line

Use OOP to **model the domain**, **encapsulate invariants**, and **extend via abstractions**—then keep designs honest with small, cohesive types, composition over inheritance, and tests that pin behavior to contracts.
