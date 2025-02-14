# SOLID Principles in Object-Oriented Programming

SOLID is an acronym that represents five foundational design principles in object-oriented programming (OOP). These principles help create software that is more maintainable, extensible, and robust.

## Table of Contents
1. [Single Responsibility Principle (SRP)](#1-single-responsibility-principle-srp)
2. [Open-Closed Principle (OCP)](#2-open-closed-principle-ocp)
3. [Liskov Substitution Principle (LSP)](#3-liskov-substitution-principle-lsp)
4. [Interface Segregation Principle (ISP)](#4-interface-segregation-principle-isp)
5. [Dependency Inversion Principle (DIP)](#5-dependency-inversion-principle-dip)
6. [Summary](#6-summary)

---

## 1. Single Responsibility Principle (SRP)

**Definition**  
A class should have one and only one reason to change.

### Before SRP
```csharp
public class Order
{
    // Properties (Id, Date, Total, etc.)
}

public class OrderService
{
    public void CreateOrder(Order order)
    {
        // Logic to create an order
    }

    public void SendOrderConfirmationEmail(Order order)
    {
        // Logic to send email confirmation
    }
}
```
In this example, the `OrderService` class is handling both **order creation** and **sending confirmation emails**. These are two distinct responsibilities.

### After SRP
```csharp
public class Order
{
    // Properties (Id, Date, Total, etc.)
}

public class OrderService
{
    public void CreateOrder(Order order)
    {
        // Logic to create an order
    }
}

public class EmailService
{
    public void SendOrderConfirmationEmail(Order order)
    {
        // Logic to send email confirmation
    }
}
```
Now, `OrderService` is responsible **only** for creating orders, while `EmailService` handles sending emails. Each class has a single responsibility.

---

## 2. Open-Closed Principle (OCP)

**Definition**  
Software entities (classes, modules, functions, etc.) should be **open for extension** but **closed for modification**.

### Before OCP
```csharp
public class PaymentProcessor
{
    public void ProcessPayment(string paymentType)
    {
        if (paymentType == "CreditCard")
        {
            // Process credit card payment
        }
        else if (paymentType == "PayPal")
        {
            // Process PayPal payment
        }
        // If you add a new payment method, you have to modify this method again
    }
}
```
Here, each time a new payment method is introduced, we must **modify** the `ProcessPayment` method—risking regressions and violating OCP.

### After OCP
```csharp
public interface IPaymentMethod
{
    void Pay();
}

public class CreditCardPayment : IPaymentMethod
{
    public void Pay()
    {
        // Logic to process credit card payment
    }
}

public class PayPalPayment : IPaymentMethod
{
    public void Pay()
    {
        // Logic to process PayPal payment
    }
}

public class PaymentProcessor
{
    public void ProcessPayment(IPaymentMethod paymentMethod)
    {
        paymentMethod.Pay();
    }
}
```
`PaymentProcessor` now relies on an **interface** rather than concrete types. Adding a new payment method (e.g., `GooglePayPayment`) involves creating a new class that implements `IPaymentMethod`—no changes to `PaymentProcessor` are required.

---

## 3. Liskov Substitution Principle (LSP)

**Definition**  
Subtypes should be substitutable for their base types **without affecting the correctness** of the program.

### Before LSP
```csharp
public class Bird
{
    public virtual void Fly()
    {
        // Default flying logic
    }
}

public class Ostrich : Bird
{
    public override void Fly()
    {
        // Ostriches can't fly, but this method is forced by inheritance
        // This might throw an exception or do nothing, violating expectations
        throw new NotSupportedException("Ostriches cannot fly!");
    }
}
```
A `Bird` is expected to fly, but an `Ostrich` cannot. Substituting `Ostrich` where a `Bird` is expected can break the system.

### After LSP
```csharp
public interface IFlyable
{
    void Fly();
}

public abstract class Bird
{
    // Common bird properties
}

public class Eagle : Bird, IFlyable
{
    public void Fly()
    {
        // Eagle-specific flying logic
    }
}

public class Ostrich : Bird
{
    // Ostrich has no flying capability
}
```
Here, **only birds that can actually fly** implement `IFlyable`. An `Ostrich` doesn’t implement `IFlyable`, so there is no broken expectation about flying.

---

## 4. Interface Segregation Principle (ISP)

**Definition**  
No client should be forced to depend on methods it does not use. Instead of one large interface, use multiple smaller, more specific interfaces.

### Before ISP
```csharp
public interface IWorker
{
    void Work();
    void EatLunch();
}

public class RobotWorker : IWorker
{
    public void Work()
    {
        // Robot-specific work
    }

    public void EatLunch()
    {
        // Robots don't eat lunch
        // But we are forced to implement this method
        throw new NotImplementedException();
    }
}
```
`RobotWorker` is forced to implement `EatLunch()`, which is irrelevant.

### After ISP
```csharp
public interface IWorker
{
    void Work();
}

public interface IHumanWorker : IWorker
{
    void EatLunch();
}

public class RobotWorker : IWorker
{
    public void Work()
    {
        // Robot-specific work
    }
}

public class Employee : IHumanWorker
{
    public void Work()
    {
        // Employee-specific work
    }

    public void EatLunch()
    {
        // Employee eats lunch
    }
}
```
By splitting the interface into `IWorker` and `IHumanWorker`, each class implements **only** what it needs.

---

## 5. Dependency Inversion Principle (DIP)

**Definition**  
- High-level modules should not depend on low-level modules; both should depend on abstractions.  
- Abstractions should not depend on details; details should depend on abstractions.

### Before DIP
```csharp
public class EmailService
{
    public void SendEmail(string message)
    {
        // Logic to send email
    }
}

public class Notification
{
    private EmailService _emailService = new EmailService();

    public void Send(string message)
    {
        _emailService.SendEmail(message);
    }
}
```
`Notification` (a high-level module) depends on `EmailService` (a low-level module). If we want to use SMS, push notifications, or something else, we have to modify `Notification`.

### After DIP
```csharp
public interface IMessageService
{
    void SendMessage(string message);
}

public class EmailService : IMessageService
{
    public void SendMessage(string message)
    {
        // Logic to send email
    }
}

public class SmsService : IMessageService
{
    public void SendMessage(string message)
    {
        // Logic to send SMS
    }
}

public class Notification
{
    private readonly IMessageService _messageService;

    public Notification(IMessageService messageService)
    {
        _messageService = messageService;
    }

    public void Send(string message)
    {
        _messageService.SendMessage(message);
    }
}
```
`Notification` now depends on an **abstraction** (`IMessageService`). Changing the way messages are sent involves providing a different implementation (like `SmsService`) without altering the `Notification` class.

---

## Summary of the SOLID Principles in C#

1. **Single Responsibility Principle (SRP)**  
   Each class or module should have **one reason to change**.
2. **Open-Closed Principle (OCP)**  
   Classes should be **open for extension, closed for modification**.
3. **Liskov Substitution Principle (LSP)**  
   Derived classes should be **substitutable** for their base classes without breaking the system.
4. **Interface Segregation Principle (ISP)**  
   **Split** large interfaces into **smaller, more specific** ones to avoid forcing classes to implement unused methods.
5. **Dependency Inversion Principle (DIP)**  
   **Depend on abstractions**, not on concrete implementations.

By applying these principles, you create code that is **more modular**, **easier to maintain**, and **simpler to extend**.
