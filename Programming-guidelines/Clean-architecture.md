# Overview

**Clean Architecture** is a layered architectural style that organizes software into concentric circles (or layers). Each layer has a well-defined role, and **all dependencies point inwards**—toward the most critical part of the system: the **core business logic** (or domain). The outer layers handle implementation details (e.g., frameworks, databases, user interfaces) that can change over time without affecting the domain logic.

At a high level, Clean Architecture looks like this (from innermost to outermost layer):

1. **Entities (Domain Model)**  
   - Encapsulate enterprise-wide, core business rules and data.  
   - Typically, these are **plain** objects with minimal dependencies (no direct database or framework references).

2. **Use Cases (Application Layer / Interactors)**  
   - Contain application-specific business rules and orchestrate how data flows between entities and other parts of the system.  
   - Coordinate tasks (e.g., “Create Order,” “Process Payment”) using domain entities.  
   - No knowledge of UI, database, or external services; only deals with abstractions.

3. **Interface Adapters (Adapters / Gateways / Presenters)**  
   - Translate data between **Use Cases** and **Frameworks/Drivers**.  
   - Could include **repositories**, **DTOs** (Data Transfer Objects), **presenters**, **controllers**, etc.  
   - Responsible for **input/output formatting**: parsing incoming requests, formatting outgoing responses.

4. **Frameworks and Drivers (Infrastructure Layer)**  
   - Outer layer containing **databases**, **web frameworks**, **UI frameworks**, **third-party services**, etc.  
   - Operates through adapters (interfaces) defined in the more central layers.  
   - Should contain **no business logic**—if possible, only implementation details of the system’s boundaries.

---

## Key Principles

1. **Dependency Rule**:  
   All source code dependencies point **inward**, toward higher-level policies (business rules). Inner layers know nothing about outer layers.

2. **Separation of Concerns**:  
   Each layer focuses on a distinct set of responsibilities (domain logic, application orchestration, data access, presentation).

3. **Testability**:  
   Since business rules reside in framework-agnostic layers, they can be tested **without** spinning up databases or web servers.

4. **Flexibility & Maintainability**:  
   When changing a database, UI, or external API, the inner layers remain unaffected. This reduces coupling and makes large-scale refactors safer.

---

## Conceptual C# Example

Below is a *simplified* example of how you might structure a Clean Architecture in C#. Real-world scenarios tend to be more complex but follow these core ideas.

### 1. Entities (Domain Layer)

```csharp
namespace CleanArchitecture.Domain
{
    // Core domain object
    public class Order
    {
        public int Id { get; private set; }
        public decimal Total { get; private set; }
        public bool IsPaid { get; private set; }

        public Order(int id, decimal total)
        {
            Id = id;
            Total = total;
            IsPaid = false;
        }

        public void Pay()
        {
            // Business rule: you can only pay if the order is not already paid
            if (IsPaid)
            {
                throw new InvalidOperationException("Order is already paid.");
            }
            IsPaid = true;
        }
    }
}
```

- **Purpose**: Contains the **enterprise-wide** business rules (`Order`).
- **No** references to frameworks, databases, or UI.

### 2. Use Cases (Application Layer)

```csharp
namespace CleanArchitecture.Application
{
    public interface IOrderRepository
    {
        Order GetById(int orderId);
        void Save(Order order);
    }

    public class PayOrderUseCase
    {
        private readonly IOrderRepository _orderRepository;

        public PayOrderUseCase(IOrderRepository orderRepository)
        {
            _orderRepository = orderRepository;
        }

        public void Execute(int orderId)
        {
            // 1. Get the order from a repository
            var order = _orderRepository.GetById(orderId);

            // 2. Perform the domain action
            order.Pay();

            // 3. Persist the changes
            _orderRepository.Save(order);
        }
    }
}
```

- **Purpose**: Implements application-specific business rules (use cases).  
- **No** knowledge of *how* `IOrderRepository` is implemented (database, in-memory, etc.).  
- Coordinates domain actions (`order.Pay()`).

### 3. Interface Adapters

```csharp
namespace CleanArchitecture.Infrastructure.Persistence
{
    using CleanArchitecture.Application;
    using CleanArchitecture.Domain;
    using System.Collections.Generic;
    using System.Linq;

    // A simple in-memory repository for demonstration
    public class InMemoryOrderRepository : IOrderRepository
    {
        private readonly List<Order> _orders = new List<Order>();

        public Order GetById(int orderId)
        {
            return _orders.FirstOrDefault(o => o.Id == orderId);
        }

        public void Save(Order order)
        {
            // If order doesn't exist, add it; if it does, update it
            var existingOrder = GetById(order.Id);
            if (existingOrder == null)
            {
                _orders.Add(order);
            }
            else
            {
                // For simplicity, do nothing extra here
            }
        }
    }
}
```

- **Purpose**: Concrete implementation of `IOrderRepository` that interfaces with some form of storage (in this case, **in-memory** for demo).  
- Real-world scenario: A repository that uses EF Core, Dapper, or any other data access technology—**outer details** that the core application logic need not know.

### 4. Frameworks and Drivers (UI / Composition Root)

```csharp
namespace CleanArchitecture.Web
{
    using CleanArchitecture.Application;
    using CleanArchitecture.Domain;
    using CleanArchitecture.Infrastructure.Persistence;
    using Microsoft.AspNetCore.Mvc;

    [Route("api/[controller]")]
    [ApiController]
    public class OrdersController : ControllerBase
    {
        private readonly PayOrderUseCase _payOrderUseCase;
        private readonly IOrderRepository _orderRepository;  // For demonstration only

        // Composition root: wiring up dependencies
        public OrdersController()
        {
            _orderRepository = new InMemoryOrderRepository();
            _payOrderUseCase = new PayOrderUseCase(_orderRepository);

            // In a real-world app, a DI container (like .NET Core's built-in) 
            // would typically handle instantiations and injections.
        }

        [HttpPost("pay/{orderId}")]
        public ActionResult PayOrder(int orderId)
        {
            _payOrderUseCase.Execute(orderId);
            return Ok("Order paid successfully.");
        }

        // Additional endpoints could be added here
    }
}
```

- **Purpose**: The **outermost layer**, containing the **web or UI** framework code (`ASP.NET` in this example).  
- Responsible for **receiving** HTTP requests, **instantiating** use cases (and repositories), and **coordinating** responses.  
- **No** domain or core logic here. It simply orchestrates calls to the Application Layer.

---

## Benefits of Clean Architecture

1. **Framework Independence**: Business logic doesn’t rely on any particular framework. You can switch to a different UI, database, or library without rewriting core rules.  
2. **Testability**: With dependencies inverted (toward abstractions), you can plug in test doubles or mocks for repositories and services easily.  
3. **Maintainability**: By separating concerns, changes in UI or data storage affect only the outer layers, not the domain or use cases.  
4. **Decoupled Code**: The domain model and application rules remain unaffected by outside concerns (databases, APIs, UI frameworks).

---

## Common Misconceptions

1. **It’s Not Just Folder Structure**: Clean Architecture is more about **dependency flow** than merely having “nice folders.” You can have well-labeled directories but still violate dependency rules.  
2. **It’s Not Just for Large Apps**: Even smaller projects benefit from layered boundaries if they anticipate future growth or complexity.  
3. **It Doesn’t Require a Particular Tech Stack**: Clean Architecture is language/framework-agnostic. Whether in C#, Java, Python, or JavaScript, the principles remain the same.

---

## Conclusion

**Clean Architecture** structures your application around the **core business logic**, shielding it from implementation details. By inverting dependencies, you **minimize coupling** and maximize the **testability** and **flexibility** of your system. This approach is particularly valuable in large, evolving projects where requirements, frameworks, and technologies may change over time, but the core business rules remain consistent and stable.
