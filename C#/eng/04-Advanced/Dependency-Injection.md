# Dependency Injection and Dependency Inversion

## Table of Contents

1. [Introduction](#introduction)
2. [Dependency Inversion Principle (DIP)](#dependency-inversion-principle-dip)
3. [Tight Coupling - The Problem](#tight-coupling---the-problem)
4. [Dependency Injection (DI)](#dependency-injection-di)
5. [Types of DI](#types-of-di)
6. [Why is DI Important?](#why-is-di-important)
7. [DI and Unit Testing](#di-and-unit-testing)
8. [DI Containers](#di-containers)
9. [ASP.NET Core DI](#aspnet-core-di)
10. [Best Practices](#best-practices)
11. [Summary](#summary)

---

## Introduction

**Dependency Injection (DI)** is a design pattern that implements the **Dependency Inversion Principle (DIP)**. DI is one of the most important concepts in modern software development, especially in:

- Unit testing (mocking)
- Clean Architecture
- ASP.NET Core applications

This material explains both concepts and shows how to use them in practice.

---

## Dependency Inversion Principle (DIP)

**Dependency Inversion Principle** is the fifth letter (D) of the SOLID principles. It states:

> 1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
> 2. Abstractions should not depend on details. Details should depend on abstractions.

### What does this mean in practice?

**Without DIP:**

```
OrderService → PaymentService (concrete class)
     ↓
High level depends on low level
```

**With DIP:**

```
OrderService → IPaymentService (interface)
                    ↑
              PaymentService

Both depend on the abstraction (interface)
```

### Example: DIP Violation

```csharp
// ❌ BAD: OrderService depends directly on PaymentService
public class OrderService
{
    // Dependency on concrete class!
    private PaymentService _paymentService = new PaymentService();

    public void ProcessOrder(Order order)
    {
        _paymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}
```

**Problems:**

- `OrderService` is tightly coupled to `PaymentService`
- You cannot swap `PaymentService` for another implementation
- You cannot mock `PaymentService` in tests
- If `PaymentService` changes, `OrderService` might break

### Example: Following DIP

```csharp
// ✅ GOOD: OrderService depends on abstraction (interface)

// 1. Define abstraction
public interface IPaymentService
{
    bool ProcessPayment(int customerId, decimal amount);
    bool RefundPayment(int customerId, decimal amount);
}

// 2. Concrete implementation implements the interface
public class PaymentService : IPaymentService
{
    public bool ProcessPayment(int customerId, decimal amount)
    {
        // Real implementation
        return true;
    }

    public bool RefundPayment(int customerId, decimal amount)
    {
        // Real implementation
        return true;
    }
}

// 3. OrderService depends only on the interface
public class OrderService
{
    private readonly IPaymentService _paymentService;

    // Dependency injected via constructor
    public OrderService(IPaymentService paymentService)
    {
        _paymentService = paymentService;
    }

    public void ProcessOrder(Order order)
    {
        _paymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}
```

**Benefits:**

- `OrderService` does not know which `IPaymentService` implementation is used
- You can easily swap implementations (StripePaymentService, MockPaymentService)
- Testability improves significantly

---

## Tight Coupling - The Problem

**Tight coupling** means a class is strongly dependent on another class.

### Common Signs

```csharp
// ❌ Signs of tight coupling:

public class OrderService
{
    // 1. new keyword inside the class
    private PaymentService _payment = new PaymentService();

    // 2. Calling static methods
    private void Log() => Logger.Log("...");

    // 3. Concrete classes in fields
    private EmailService _email;

    public OrderService()
    {
        // 4. Creating dependencies in constructor
        _email = new EmailService();
    }
}
```

### Testability Problems

```csharp
// Trying to test OrderService
[Fact]
public void ProcessOrder_ValidOrder_ReturnsTrue()
{
    // ❌ PROBLEM: We cannot control PaymentService behavior!
    var service = new OrderService();

    // This call uses the REAL PaymentService
    // - Slow (real database call)
    // - Side effects (actually charges!)
    // - Not repeatable (database state changes)
    var result = service.ProcessOrder(order);

    // We cannot test:
    // - What happens when payment fails?
    // - Was PaymentService called correctly?
}
```

### Visualization

```
TIGHT COUPLING:

┌─────────────────┐
│  OrderService   │
│                 │
│  new Payment()──┼────► PaymentService (concrete)
│  new Email()────┼────► EmailService (concrete)
│  new Logger()───┼────► Logger (concrete)
│                 │
└─────────────────┘

In tests you CANNOT swap these!


LOOSE COUPLING (DI):

┌─────────────────┐
│  OrderService   │
│                 │
│  IPayment ◄─────┼────┐
│  IEmail ◄───────┼────┤ Injected from outside
│  ILogger ◄──────┼────┤
│                 │    │
└─────────────────┘    │
                       │
         ┌─────────────┴─────────────┐
         │                           │
    PRODUCTION:                TESTING:
    PaymentService             Mock<IPayment>
    EmailService               Mock<IEmail>
    FileLogger                 Mock<ILogger>
```

---

## Dependency Injection (DI)

**Dependency Injection** is a technique to implement DIP. Dependencies are "injected" (provided) from outside instead of being created by the class itself.

### Basic Idea

```csharp
// ❌ WITHOUT DI: Class creates dependencies itself
public class OrderService
{
    private IPaymentService _payment = new PaymentService(); // Creates itself
}

// ✅ WITH DI: Dependencies are provided from outside
public class OrderService
{
    private readonly IPaymentService _payment;

    public OrderService(IPaymentService payment) // Injected
    {
        _payment = payment;
    }
}
```

---

## Types of DI

### 1. Constructor Injection (Recommended)

Dependencies are passed through the constructor.

```csharp
public class OrderService
{
    private readonly IPaymentService _paymentService;
    private readonly IInventoryService _inventoryService;
    private readonly INotificationService _notificationService;

    // All dependencies in constructor
    public OrderService(
        IPaymentService paymentService,
        IInventoryService inventoryService,
        INotificationService notificationService)
    {
        _paymentService = paymentService ?? throw new ArgumentNullException(nameof(paymentService));
        _inventoryService = inventoryService ?? throw new ArgumentNullException(nameof(inventoryService));
        _notificationService = notificationService ?? throw new ArgumentNullException(nameof(notificationService));
    }
}
```

**Benefits:**

- ✅ Dependencies are clearly visible
- ✅ Object is ready to use right after creation
- ✅ Dependencies can be `readonly`
- ✅ Easy to test

**When to use:** Almost always. This is the recommended approach.

### 2. Property Injection

Dependencies are set via properties.

```csharp
public class OrderService
{
    // Property injection
    public IPaymentService PaymentService { get; set; }

    public void ProcessOrder(Order order)
    {
        if (PaymentService == null)
            throw new InvalidOperationException("PaymentService not set");

        PaymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// Usage
var service = new OrderService();
service.PaymentService = new PaymentService(); // Set later
```

**Benefits:**

- Set optional dependencies
- Sometimes needed in legacy code

**Drawbacks:**

- ❌ Object can be in an invalid state
- ❌ Dependency can be forgotten
- ❌ Not thread-safe

**When to use:** Rarely. Only for optional dependencies.

### 3. Method Injection

Dependency is passed as a method parameter.

```csharp
public class OrderService
{
    // Method injection - dependency provided at call time
    public void ProcessOrder(Order order, IPaymentService paymentService)
    {
        paymentService.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// Usage
var service = new OrderService();
service.ProcessOrder(order, new PaymentService());
```

**Benefits:**

- Dependency can vary per call

**Drawbacks:**

- ❌ Caller must always provide the dependency
- ❌ Can lead to long parameter lists

**When to use:** When the dependency varies between calls.

---

## Why is DI Important?

### 1. Testability

DI enables mocking:

```csharp
// IN TESTS: You can mock dependencies
[Fact]
public void ProcessOrder_PaymentSucceeds_ReturnsTrue()
{
    // Arrange - Create mock
    var paymentMock = new Mock<IPaymentService>();
    paymentMock.Setup(x => x.ProcessPayment(It.IsAny<int>(), It.IsAny<decimal>()))
               .Returns(true);

    // Inject mock
    var service = new OrderService(paymentMock.Object);

    // Act
    var result = service.ProcessOrder(order);

    // Assert
    Assert.True(result);
    paymentMock.Verify(x => x.ProcessPayment(123, 100m), Times.Once);
}
```

### 2. Loose Coupling

Classes are not tied to specific implementations:

```csharp
// The same OrderService works with different payment services
var stripeService = new OrderService(new StripePaymentService());
var paypalService = new OrderService(new PayPalPaymentService());
var testService = new OrderService(new MockPaymentService());
```

### 3. Single Responsibility

The class does not create its dependencies:

```csharp
// ❌ OrderService does too much
public class OrderService
{
    private IPaymentService _payment;

    public OrderService()
    {
        // Knows how to create PaymentService
        // Knows what configuration it needs
        var config = new PaymentConfig { ApiKey = "..." };
        _payment = new PaymentService(config);
    }
}

// ✅ OrderService focuses on its own responsibility
public class OrderService
{
    private readonly IPaymentService _payment;

    public OrderService(IPaymentService payment)
    {
        _payment = payment; // Doesn't know/care how it was created
    }
}
```

### 4. Configurability

You can change application behavior without code changes:

```csharp
// Development
services.AddScoped<IEmailService, FakeEmailService>();

// Production
services.AddScoped<IEmailService, SendGridEmailService>();
```

---

## DI and Unit Testing

The most important benefit of DI is **enabling mocking** in unit tests.

### Without DI - Hard to Test

```csharp
public class OrderService
{
    private PaymentService _payment = new PaymentService();

    public bool ProcessOrder(Order order)
    {
        return _payment.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// ❌ TEST DOES NOT WORK PROPERLY
[Fact]
public void ProcessOrder_Test()
{
    var service = new OrderService();

    // Problem: Uses real PaymentService!
    // - Slow (real API call)
    // - Side effects (charges for real)
    // - Cannot test error scenarios
    var result = service.ProcessOrder(order);
}
```

### With DI - Easy to Test

```csharp
public class OrderService
{
    private readonly IPaymentService _payment;

    public OrderService(IPaymentService payment)
    {
        _payment = payment;
    }

    public bool ProcessOrder(Order order)
    {
        return _payment.ProcessPayment(order.CustomerId, order.TotalPrice);
    }
}

// ✅ TEST WORKS WELL
[Fact]
public void ProcessOrder_PaymentSucceeds_ReturnsTrue()
{
    // Arrange - Create mock returning true
    var paymentMock = new Mock<IPaymentService>();
    paymentMock.Setup(x => x.ProcessPayment(It.IsAny<int>(), It.IsAny<decimal>()))
               .Returns(true);

    var service = new OrderService(paymentMock.Object);

    // Act
    var result = service.ProcessOrder(new Order { CustomerId = 1, TotalPrice = 100 });

    // Assert
    Assert.True(result);
}

[Fact]
public void ProcessOrder_PaymentFails_ReturnsFalse()
{
    // Arrange - Create mock returning false
    var paymentMock = new Mock<IPaymentService>();
    paymentMock.Setup(x => x.ProcessPayment(It.IsAny<int>(), It.IsAny<decimal>()))
               .Returns(false); // Simulate failure!

    var service = new OrderService(paymentMock.Object);

    // Act
    var result = service.ProcessOrder(new Order { CustomerId = 1, TotalPrice = 100 });

    // Assert
    Assert.False(result);
}
```

---

## DI Containers

A **DI container** (or IoC container) is a framework that automatically manages dependency creation and lifecycle.

### Without a container

```csharp
// Manually created dependencies - tedious!
var logger = new FileLogger();
var config = new AppConfig();
var database = new SqlDatabase(config.ConnectionString);
var userRepository = new UserRepository(database, logger);
var emailService = new SmtpEmailService(config);
var userService = new UserService(userRepository, emailService, logger);

// If UserService has 10 dependencies, this grows quickly...
```

### With a DI container

```csharp
// Registration (done once at app startup)
services.AddSingleton<ILogger, FileLogger>();
services.AddSingleton<IAppConfig, AppConfig>();
services.AddScoped<IDatabase, SqlDatabase>();
services.AddScoped<IUserRepository, UserRepository>();
services.AddScoped<IEmailService, SmtpEmailService>();
services.AddScoped<IUserService, UserService>();

// Container handles creation automatically
var userService = serviceProvider.GetService<IUserService>();
// All dependencies are created and injected automatically!
```

### Popular DI Containers

| Container                                    | Usage                           |
| -------------------------------------------- | ------------------------------- |
| **Microsoft.Extensions.DependencyInjection** | ASP.NET Core, built-in          |
| **Autofac**                                  | Feature-rich, many capabilities |
| **Ninject**                                  | Easy to use                     |
| **Unity**                                    | Microsoft (older)               |

---

## ASP.NET Core DI

ASP.NET Core includes a built-in DI container.

### Registration (Program.cs or Startup.cs)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Register services
builder.Services.AddScoped<IPaymentService, StripePaymentService>();
builder.Services.AddScoped<IOrderService, OrderService>();
builder.Services.AddScoped<IEmailService, SendGridEmailService>();

// Singleton - one instance for the entire application lifetime
builder.Services.AddSingleton<ILogger, FileLogger>();

// Transient - new instance each time
builder.Services.AddTransient<IGuidGenerator, GuidGenerator>();

var app = builder.Build();
```

### Lifetimes

| Lifetime      | Description                    | Usage                           |
| ------------- | ------------------------------ | ------------------------------- |
| **Singleton** | One instance for the whole app | Loggers, configuration          |
| **Scoped**    | One instance per HTTP request  | Repositories, DbContext         |
| **Transient** | New instance every time        | Lightweight, stateless services |

### Usage in a Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly IOrderService _orderService;

    // DI container injects automatically!
    public OrdersController(IOrderService orderService)
    {
        _orderService = orderService;
    }

    [HttpPost]
    public IActionResult CreateOrder(OrderDto orderDto)
    {
        var result = _orderService.ProcessOrder(orderDto);
        return Ok(result);
    }
}
```

---

## Best Practices

### 1. Use Constructor Injection

```csharp
// ✅ Good
public class OrderService
{
    private readonly IPaymentService _payment;

    public OrderService(IPaymentService payment)
    {
        _payment = payment;
    }
}
```

### 2. Use readonly fields

```csharp
// ✅ Good - readonly prevents accidental changes
private readonly IPaymentService _payment;

// ❌ Bad - can be changed accidentally
private IPaymentService _payment;
```

### 3. Check for null in constructor

```csharp
public OrderService(IPaymentService payment)
{
    _payment = payment ?? throw new ArgumentNullException(nameof(payment));
}
```

### 4. Keep constructors simple

```csharp
// ✅ Good - only assignments
public OrderService(IPaymentService payment)
{
    _payment = payment;
}

// ❌ Bad - logic in constructor
public OrderService(IPaymentService payment)
{
    _payment = payment;
    _payment.Initialize(); // No logic here!
    LoadConfiguration();   // No logic here!
}
```

### 5. Avoid the Service Locator anti-pattern

```csharp
// ❌ Bad - Service Locator (anti-pattern)
public class OrderService
{
    public void ProcessOrder(Order order)
    {
        // Dependency is hidden!
        var payment = ServiceLocator.GetService<IPaymentService>();
        payment.ProcessPayment(order);
    }
}

// ✅ Good - Explicit DI
public class OrderService
{
    private readonly IPaymentService _payment;

    public OrderService(IPaymentService payment)
    {
        _payment = payment; // Dependency is visible
    }
}
```

### 6. Put interfaces in their own folder

```
MyApp/
├── Services/
│   ├── Interfaces/
│   │   ├── IPaymentService.cs
│   │   ├── IOrderService.cs
│   │   └── IEmailService.cs
│   ├── PaymentService.cs
│   ├── OrderService.cs
│   └── EmailService.cs
```

---

## Summary

### Dependency Inversion Principle (DIP)

- High-level modules must not depend on low-level modules
- Both depend on abstractions (interface)

### Dependency Injection (DI)

- Technique to implement DIP
- Dependencies are provided externally (injected)
- Constructor Injection is the recommended approach

### Benefits

| Benefit             | Description                              |
| ------------------- | ---------------------------------------- |
| **Testability**     | Mocking is possible                      |
| **Loose coupling**  | Classes do not depend on implementations |
| **Flexibility**     | Implementation can be swapped easily     |
| **Maintainability** | Changes do not spread                    |

### Rule of Thumb

```
❌ new = tight coupling = hard to test
✅ interface + DI = loose coupling = easy to test
```

---

## Useful links

- [Microsoft: Dependency Injection](https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection)
- [SOLID Principles](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)
- [Moq Quickstart](https://github.com/moq/moq4/wiki/Quickstart)
