# DDD Käytännön Esimerkki - Verkkokaupan Tilausjärjestelmä

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Skenaarion kuvaus](#skenaarion-kuvaus)
3. [Projektin rakenne](#projektin-rakenne)
4. [Domain Layer](#domain-layer)
5. [Application Layer](#application-layer)
6. [Infrastructure Layer](#infrastructure-layer)
7. [Presentation Layer](#presentation-layer)
8. [Kokonaisuus toiminnassa](#kokonaisuus-toiminnassa)
9. [Yhteenveto](#yhteenveto)

---

## Johdanto

Tämä esimerkki näyttää, miten **Domain-Driven Design (DDD)** yhdistetään **Clean Architecture**:n kanssa. Rakennamme yksinkertaisen verkkokaupan tilausjärjestelmän, joka demonstroi DDD:n keskeisiä konsepteja.

### Mitä käsitellään?

- ✅ **Entities** (Order, Customer, Product)
- ✅ **Value Objects** (Money, Address, Email)
- ✅ **Aggregates** (Order Aggregate)
- ✅ **Domain Events** (OrderPlaced, OrderCancelled)
- ✅ **Repositories** (IOrderRepository)
- ✅ **Domain Services** (OrderPricingService)
- ✅ **Use Cases** (PlaceOrderCommand)

### Bounded Context

Keskitymme yhteen Bounded Contextiin: **Order Management**

```
┌─────────────────────────────────────┐
│      Order Management Context       │
├─────────────────────────────────────┤
│  • Orders (Tilaukset)               │
│  • Order Items (Tilausrivit)        │
│  • Pricing (Hinnoittelu)            │
│  • Order Status (Tilatila)          │
└─────────────────────────────────────┘
```

---

## Skenaarion kuvaus

### Liiketoimintavaatimukset

**Asiakkaana haluan:**
1. Tehdä tilauksen tuotteista
2. Lisätä/poistaa tuotteita tilaukseen
3. Nähdä tilauksen kokonaissumman
4. Saada alennus asiakastasoni mukaan
5. Vahvistaa tilaus
6. Peruuttaa tilaus tarvittaessa

**Liiketoimintasäännöt:**
- Tilauksen minimisumma on 10€
- Tyhjää tilausta ei voi vahvistaa
- Vahvistettua tilausta ei voi muokata
- Alennukset: Gold 15%, Silver 10%, Bronze 5%
- Kun tilaus vahvistetaan, lähetetään vahvistusviesti

---

## Projektin rakenne

```
OrderManagement/
├── OrderManagement.Domain/              ← Domain Layer (DDD Core)
│   ├── Entities/
│   │   ├── Order.cs
│   │   └── OrderItem.cs
│   ├── ValueObjects/
│   │   ├── Money.cs
│   │   ├── Email.cs
│   │   └── Address.cs
│   ├── Enums/
│   │   ├── OrderStatus.cs
│   │   └── CustomerLevel.cs
│   ├── Events/
│   │   ├── OrderPlacedEvent.cs
│   │   └── OrderCancelledEvent.cs
│   ├── Interfaces/
│   │   └── IOrderRepository.cs
│   ├── Services/
│   │   └── OrderPricingService.cs
│   ├── Exceptions/
│   │   └── DomainException.cs
│   └── Common/
│       ├── Entity.cs
│       ├── ValueObject.cs
│       ├── IAggregateRoot.cs
│       └── IDomainEvent.cs
│
├── OrderManagement.Application/         ← Application Layer (Use Cases)
│   ├── Commands/
│   │   ├── PlaceOrderCommand.cs
│   │   ├── AddOrderItemCommand.cs
│   │   └── CancelOrderCommand.cs
│   ├── Handlers/
│   │   ├── PlaceOrderHandler.cs
│   │   ├── AddOrderItemHandler.cs
│   │   └── CancelOrderHandler.cs
│   ├── Queries/
│   │   └── GetOrderByIdQuery.cs
│   └── DTOs/
│       └── OrderDto.cs
│
├── OrderManagement.Infrastructure/      ← Infrastructure Layer
│   ├── Persistence/
│   │   ├── ApplicationDbContext.cs
│   │   ├── Repositories/
│   │   │   └── OrderRepository.cs
│   │   └── Configurations/
│   │       ├── OrderConfiguration.cs
│   │       └── OrderItemConfiguration.cs
│   └── Services/
│       └── EmailService.cs
│
└── OrderManagement.API/                 ← Presentation Layer
    └── Controllers/
        └── OrdersController.cs
```

---

## Domain Layer

Domain Layer on DDD:n **ydin**. Se sisältää kaiken liiketoimintalogiikan.

### 1. Base Classes

#### Entity.cs

```csharp
namespace OrderManagement.Domain.Common;

public abstract class Entity
{
    public int Id { get; protected set; }
    
    private readonly List<IDomainEvent> _domainEvents = new();
    public IReadOnlyList<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();
    
    protected void AddDomainEvent(IDomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }
    
    public void ClearDomainEvents()
    {
        _domainEvents.Clear();
    }
    
    public override bool Equals(object? obj)
    {
        if (obj is not Entity other)
            return false;
            
        if (ReferenceEquals(this, other))
            return true;
            
        if (GetType() != other.GetType())
            return false;
            
        return Id == other.Id;
    }
    
    public override int GetHashCode()
    {
        return Id.GetHashCode();
    }
}
```

#### ValueObject.cs

```csharp
namespace OrderManagement.Domain.Common;

public abstract class ValueObject
{
    protected abstract IEnumerable<object> GetEqualityComponents();
    
    public override bool Equals(object? obj)
    {
        if (obj == null || obj.GetType() != GetType())
            return false;
            
        var other = (ValueObject)obj;
        return GetEqualityComponents().SequenceEqual(other.GetEqualityComponents());
    }
    
    public override int GetHashCode()
    {
        return GetEqualityComponents()
            .Select(x => x?.GetHashCode() ?? 0)
            .Aggregate((x, y) => x ^ y);
    }
    
    public static bool operator ==(ValueObject? left, ValueObject? right)
    {
        if (left is null && right is null)
            return true;
            
        if (left is null || right is null)
            return false;
            
        return left.Equals(right);
    }
    
    public static bool operator !=(ValueObject? left, ValueObject? right)
    {
        return !(left == right);
    }
}
```

#### IAggregateRoot.cs

```csharp
namespace OrderManagement.Domain.Common;

// Marker interface - merkitsee Aggregate Root:n
public interface IAggregateRoot
{
}
```

#### IDomainEvent.cs

```csharp
namespace OrderManagement.Domain.Common;

public interface IDomainEvent
{
    DateTime OccurredOn { get; }
}
```

#### DomainException.cs

```csharp
namespace OrderManagement.Domain.Exceptions;

public class DomainException : Exception
{
    public DomainException(string message) : base(message)
    {
    }
    
    public DomainException(string message, Exception innerException) 
        : base(message, innerException)
    {
    }
}
```

### 2. Enums

#### OrderStatus.cs

```csharp
namespace OrderManagement.Domain.Enums;

public enum OrderStatus
{
    Draft = 0,          // Luonnos, voidaan muokata
    Submitted = 1,      // Vahvistettu
    Processing = 2,     // Käsittelyssä
    Shipped = 3,        // Lähetetty
    Delivered = 4,      // Toimitettu
    Cancelled = 5       // Peruttu
}
```

#### CustomerLevel.cs

```csharp
namespace OrderManagement.Domain.Enums;

public enum CustomerLevel
{
    Standard = 0,
    Bronze = 1,
    Silver = 2,
    Gold = 3
}
```

### 3. Value Objects

#### Money.cs

```csharp
namespace OrderManagement.Domain.ValueObjects;

public class Money : ValueObject
{
    public decimal Amount { get; }
    public string Currency { get; }
    
    public Money(decimal amount, string currency)
    {
        if (amount < 0)
            throw new ArgumentException("Amount cannot be negative", nameof(amount));
            
        if (string.IsNullOrWhiteSpace(currency))
            throw new ArgumentException("Currency is required", nameof(currency));
            
        Amount = amount;
        Currency = currency.ToUpperInvariant();
    }
    
    // Factory methods
    public static Money Zero(string currency) => new(0, currency);
    public static Money Euro(decimal amount) => new(amount, "EUR");
    
    // Operaatiot
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException(
                $"Cannot add {other.Currency} to {Currency}");
                
        return new Money(Amount + other.Amount, Currency);
    }
    
    public Money Subtract(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException(
                $"Cannot subtract {other.Currency} from {Currency}");
                
        return new Money(Amount - other.Amount, Currency);
    }
    
    public Money Multiply(decimal multiplier)
    {
        return new Money(Amount * multiplier, Currency);
    }
    
    public Money ApplyDiscount(decimal percentage)
    {
        if (percentage < 0 || percentage > 100)
            throw new ArgumentException("Percentage must be between 0 and 100");
            
        var discountAmount = Amount * (percentage / 100);
        return new Money(Amount - discountAmount, Currency);
    }
    
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Amount;
        yield return Currency;
    }
    
    public override string ToString() => $"{Amount:F2} {Currency}";
}
```

#### Email.cs

```csharp
namespace OrderManagement.Domain.ValueObjects;

public class Email : ValueObject
{
    public string Value { get; }
    
    public Email(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            throw new ArgumentException("Email cannot be empty", nameof(value));
            
        if (!IsValidEmail(value))
            throw new ArgumentException("Invalid email format", nameof(value));
            
        Value = value.ToLowerInvariant();
    }
    
    private static bool IsValidEmail(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            return false;
            
        // Yksinkertainen validointi
        var parts = email.Split('@');
        return parts.Length == 2 
            && !string.IsNullOrWhiteSpace(parts[0]) 
            && !string.IsNullOrWhiteSpace(parts[1])
            && parts[1].Contains('.');
    }
    
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Value;
    }
    
    public override string ToString() => Value;
}
```

#### Address.cs

```csharp
namespace OrderManagement.Domain.ValueObjects;

public class Address : ValueObject
{
    public string Street { get; }
    public string City { get; }
    public string PostalCode { get; }
    public string Country { get; }
    
    public Address(string street, string city, string postalCode, string country)
    {
        if (string.IsNullOrWhiteSpace(street))
            throw new ArgumentException("Street is required", nameof(street));
        if (string.IsNullOrWhiteSpace(city))
            throw new ArgumentException("City is required", nameof(city));
        if (string.IsNullOrWhiteSpace(postalCode))
            throw new ArgumentException("Postal code is required", nameof(postalCode));
        if (string.IsNullOrWhiteSpace(country))
            throw new ArgumentException("Country is required", nameof(country));
            
        Street = street;
        City = city;
        PostalCode = postalCode;
        Country = country;
    }
    
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Street;
        yield return City;
        yield return PostalCode;
        yield return Country;
    }
    
    public override string ToString() 
        => $"{Street}, {PostalCode} {City}, {Country}";
}
```

### 4. Entities

#### OrderItem.cs

```csharp
namespace OrderManagement.Domain.Entities;

// OrderItem on osa Order Aggregatea - ei Aggregate Root
public class OrderItem : Entity
{
    public int OrderId { get; private set; }
    public int ProductId { get; private set; }
    public string ProductName { get; private set; } = string.Empty;
    public int Quantity { get; private set; }
    public Money UnitPrice { get; private set; } = null!;
    
    public Money TotalPrice => UnitPrice.Multiply(Quantity);
    
    // EF Core constructor
    private OrderItem() { }
    
    // Internal constructor - vain Order voi luoda OrderItem:ejä
    internal OrderItem(int productId, string productName, int quantity, Money unitPrice)
    {
        if (quantity <= 0)
            throw new DomainException("Quantity must be greater than zero");
            
        if (unitPrice.Amount <= 0)
            throw new DomainException("Unit price must be greater than zero");
            
        ProductId = productId;
        ProductName = productName ?? throw new ArgumentNullException(nameof(productName));
        Quantity = quantity;
        UnitPrice = unitPrice;
    }
    
    internal void IncreaseQuantity(int amount)
    {
        if (amount <= 0)
            throw new DomainException("Amount must be greater than zero");
            
        Quantity += amount;
    }
    
    internal void DecreaseQuantity(int amount)
    {
        if (amount <= 0)
            throw new DomainException("Amount must be greater than zero");
            
        if (Quantity - amount < 0)
            throw new DomainException("Quantity cannot be negative");
            
        Quantity -= amount;
    }
    
    internal void UpdateQuantity(int newQuantity)
    {
        if (newQuantity <= 0)
            throw new DomainException("Quantity must be greater than zero");
            
        Quantity = newQuantity;
    }
}
```

#### Order.cs (Aggregate Root)

```csharp
namespace OrderManagement.Domain.Entities;

// Order on Aggregate Root - pääsy koko Aggregateen sen kautta
public class Order : Entity, IAggregateRoot
{
    public int CustomerId { get; private set; }
    public string CustomerName { get; private set; } = string.Empty;
    public Email CustomerEmail { get; private set; } = null!;
    public Address ShippingAddress { get; private set; } = null!;
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; } = null!;
    public Money? DiscountAmount { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime? SubmittedAt { get; private set; }
    
    // Private collection - ei suoraa pääsyä ulkoa
    private readonly List<OrderItem> _items = new();
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    
    // EF Core constructor
    private Order() { }
    
    // Factory method
    public static Order CreateDraft(
        int customerId, 
        string customerName, 
        Email customerEmail,
        Address shippingAddress)
    {
        if (string.IsNullOrWhiteSpace(customerName))
            throw new DomainException("Customer name is required");
            
        return new Order
        {
            CustomerId = customerId,
            CustomerName = customerName,
            CustomerEmail = customerEmail ?? throw new ArgumentNullException(nameof(customerEmail)),
            ShippingAddress = shippingAddress ?? throw new ArgumentNullException(nameof(shippingAddress)),
            Status = OrderStatus.Draft,
            TotalAmount = Money.Zero("EUR"),
            CreatedAt = DateTime.UtcNow
        };
    }
    
    // === LIIKETOIMINTALOGIIKKA ===
    
    public void AddItem(int productId, string productName, int quantity, Money unitPrice)
    {
        ValidateCanModify();
        
        // Jos tuote on jo tiluksessa, lisää määrää
        var existingItem = _items.FirstOrDefault(i => i.ProductId == productId);
        if (existingItem != null)
        {
            existingItem.IncreaseQuantity(quantity);
        }
        else
        {
            var newItem = new OrderItem(productId, productName, quantity, unitPrice);
            _items.Add(newItem);
        }
        
        RecalculateTotal();
    }
    
    public void RemoveItem(int orderItemId)
    {
        ValidateCanModify();
        
        var item = _items.FirstOrDefault(i => i.Id == orderItemId);
        if (item == null)
            throw new DomainException($"Order item {orderItemId} not found");
            
        _items.Remove(item);
        RecalculateTotal();
    }
    
    public void UpdateItemQuantity(int orderItemId, int newQuantity)
    {
        ValidateCanModify();
        
        var item = _items.FirstOrDefault(i => i.Id == orderItemId);
        if (item == null)
            throw new DomainException($"Order item {orderItemId} not found");
            
        item.UpdateQuantity(newQuantity);
        RecalculateTotal();
    }
    
    public void ApplyDiscount(decimal discountPercentage)
    {
        ValidateCanModify();
        
        if (discountPercentage < 0 || discountPercentage > 100)
            throw new DomainException("Discount percentage must be between 0 and 100");
            
        var discountAmount = TotalAmount.Amount * (discountPercentage / 100);
        DiscountAmount = new Money(discountAmount, "EUR");
        
        RecalculateTotal();
    }
    
    public void Submit()
    {
        if (Status != OrderStatus.Draft)
            throw new DomainException("Only draft orders can be submitted");
            
        if (!_items.Any())
            throw new DomainException("Cannot submit an empty order");
            
        ValidateMinimumAmount();
        
        Status = OrderStatus.Submitted;
        SubmittedAt = DateTime.UtcNow;
        
        // Domain Event - tilaus vahvistettu
        AddDomainEvent(new OrderPlacedEvent(
            Id, 
            CustomerId, 
            CustomerEmail, 
            TotalAmount,
            DateTime.UtcNow));
    }
    
    public void Cancel(string reason)
    {
        if (Status == OrderStatus.Delivered)
            throw new DomainException("Cannot cancel delivered order");
            
        if (Status == OrderStatus.Cancelled)
            throw new DomainException("Order is already cancelled");
            
        var previousStatus = Status;
        Status = OrderStatus.Cancelled;
        
        // Domain Event - tilaus peruttu
        AddDomainEvent(new OrderCancelledEvent(
            Id, 
            CustomerId, 
            reason,
            previousStatus,
            DateTime.UtcNow));
    }
    
    // === PRIVATE HELPER METHODS ===
    
    private void ValidateCanModify()
    {
        if (Status != OrderStatus.Draft)
            throw new DomainException(
                $"Cannot modify order in {Status} status. Only draft orders can be modified.");
    }
    
    private void ValidateMinimumAmount()
    {
        const decimal minimumOrderAmount = 10.0m;
        
        if (TotalAmount.Amount < minimumOrderAmount)
            throw new DomainException(
                $"Order total must be at least {minimumOrderAmount} EUR");
    }
    
    private void RecalculateTotal()
    {
        var subtotal = _items.Sum(i => i.TotalPrice.Amount);
        var total = subtotal;
        
        if (DiscountAmount != null)
        {
            total -= DiscountAmount.Amount;
        }
        
        TotalAmount = new Money(total, "EUR");
    }
}
```

### 5. Domain Events

#### OrderPlacedEvent.cs

```csharp
namespace OrderManagement.Domain.Events;

public class OrderPlacedEvent : IDomainEvent
{
    public int OrderId { get; }
    public int CustomerId { get; }
    public Email CustomerEmail { get; }
    public Money TotalAmount { get; }
    public DateTime OccurredOn { get; }
    
    public OrderPlacedEvent(
        int orderId, 
        int customerId, 
        Email customerEmail,
        Money totalAmount,
        DateTime occurredOn)
    {
        OrderId = orderId;
        CustomerId = customerId;
        CustomerEmail = customerEmail;
        TotalAmount = totalAmount;
        OccurredOn = occurredOn;
    }
}
```

#### OrderCancelledEvent.cs

```csharp
namespace OrderManagement.Domain.Events;

public class OrderCancelledEvent : IDomainEvent
{
    public int OrderId { get; }
    public int CustomerId { get; }
    public string Reason { get; }
    public OrderStatus PreviousStatus { get; }
    public DateTime OccurredOn { get; }
    
    public OrderCancelledEvent(
        int orderId, 
        int customerId, 
        string reason,
        OrderStatus previousStatus,
        DateTime occurredOn)
    {
        OrderId = orderId;
        CustomerId = customerId;
        Reason = reason ?? throw new ArgumentNullException(nameof(reason));
        PreviousStatus = previousStatus;
        OccurredOn = occurredOn;
    }
}
```

### 6. Domain Services

#### IOrderPricingService.cs

```csharp
namespace OrderManagement.Domain.Services;

public interface IOrderPricingService
{
    decimal CalculateDiscountPercentage(CustomerLevel customerLevel);
    Money ApplyCustomerDiscount(Money amount, CustomerLevel customerLevel);
}
```

#### OrderPricingService.cs

```csharp
namespace OrderManagement.Domain.Services;

// Domain Service - logiikka joka ei kuulu yhteen Entityyn
public class OrderPricingService : IOrderPricingService
{
    public decimal CalculateDiscountPercentage(CustomerLevel customerLevel)
    {
        return customerLevel switch
        {
            CustomerLevel.Gold => 15m,
            CustomerLevel.Silver => 10m,
            CustomerLevel.Bronze => 5m,
            CustomerLevel.Standard => 0m,
            _ => 0m
        };
    }
    
    public Money ApplyCustomerDiscount(Money amount, CustomerLevel customerLevel)
    {
        var discountPercentage = CalculateDiscountPercentage(customerLevel);
        
        if (discountPercentage == 0)
            return amount;
            
        return amount.ApplyDiscount(discountPercentage);
    }
}
```

### 7. Repository Interface

#### IOrderRepository.cs

```csharp
namespace OrderManagement.Domain.Interfaces;

// Repository interface määritellään Domain Layerissa
// Implementaatio on Infrastructure Layerissa
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(int id, CancellationToken cancellationToken = default);
    Task<List<Order>> GetByCustomerIdAsync(int customerId, CancellationToken cancellationToken = default);
    Task<List<Order>> GetAllAsync(CancellationToken cancellationToken = default);
    Task AddAsync(Order order, CancellationToken cancellationToken = default);
    Task UpdateAsync(Order order, CancellationToken cancellationToken = default);
    Task DeleteAsync(int id, CancellationToken cancellationToken = default);
    Task<bool> ExistsAsync(int id, CancellationToken cancellationToken = default);
}
```

---

## Application Layer

Application Layer sisältää **Use Cases** - mitä sovellus tekee.

### 1. Commands

#### PlaceOrderCommand.cs

```csharp
namespace OrderManagement.Application.Commands;

public class PlaceOrderCommand
{
    public int CustomerId { get; set; }
    public string CustomerName { get; set; } = string.Empty;
    public string CustomerEmail { get; set; } = string.Empty;
    public AddressDto ShippingAddress { get; set; } = null!;
    public List<OrderItemDto> Items { get; set; } = new();
    public CustomerLevel CustomerLevel { get; set; }
}

public class AddressDto
{
    public string Street { get; set; } = string.Empty;
    public string City { get; set; } = string.Empty;
    public string PostalCode { get; set; } = string.Empty;
    public string Country { get; set; } = string.Empty;
}

public class OrderItemDto
{
    public int ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
}
```

#### AddOrderItemCommand.cs

```csharp
namespace OrderManagement.Application.Commands;

public class AddOrderItemCommand
{
    public int OrderId { get; set; }
    public int ProductId { get; set; }
    public string ProductName { get; set; } = string.Empty;
    public int Quantity { get; set; }
    public decimal UnitPrice { get; set; }
}
```

#### CancelOrderCommand.cs

```csharp
namespace OrderManagement.Application.Commands;

public class CancelOrderCommand
{
    public int OrderId { get; set; }
    public string Reason { get; set; } = string.Empty;
}
```

### 2. Handlers

#### PlaceOrderHandler.cs

```csharp
namespace OrderManagement.Application.Handlers;

public class PlaceOrderHandler
{
    private readonly IOrderRepository _orderRepository;
    private readonly IOrderPricingService _pricingService;
    
    public PlaceOrderHandler(
        IOrderRepository orderRepository,
        IOrderPricingService pricingService)
    {
        _orderRepository = orderRepository;
        _pricingService = pricingService;
    }
    
    public async Task<int> HandleAsync(
        PlaceOrderCommand command, 
        CancellationToken cancellationToken = default)
    {
        // 1. Luo Value Objects
        var email = new Email(command.CustomerEmail);
        var shippingAddress = new Address(
            command.ShippingAddress.Street,
            command.ShippingAddress.City,
            command.ShippingAddress.PostalCode,
            command.ShippingAddress.Country);
        
        // 2. Luo Order (Aggregate Root)
        var order = Order.CreateDraft(
            command.CustomerId,
            command.CustomerName,
            email,
            shippingAddress);
        
        // 3. Lisää tuotteet
        foreach (var item in command.Items)
        {
            var unitPrice = Money.Euro(item.UnitPrice);
            order.AddItem(item.ProductId, item.ProductName, item.Quantity, unitPrice);
        }
        
        // 4. Käytä Domain Service:ä alennukseen
        var discountPercentage = _pricingService.CalculateDiscountPercentage(command.CustomerLevel);
        if (discountPercentage > 0)
        {
            order.ApplyDiscount(discountPercentage);
        }
        
        // 5. Vahvista tilaus
        order.Submit();
        
        // 6. Tallenna
        await _orderRepository.AddAsync(order, cancellationToken);
        
        // 7. Domain Events käsitellään (esim. MediatR)
        // Events lähetetään automaattisesti SaveChanges:issa
        
        return order.Id;
    }
}
```

#### AddOrderItemHandler.cs

```csharp
namespace OrderManagement.Application.Handlers;

public class AddOrderItemHandler
{
    private readonly IOrderRepository _orderRepository;
    
    public AddOrderItemHandler(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }
    
    public async Task HandleAsync(
        AddOrderItemCommand command, 
        CancellationToken cancellationToken = default)
    {
        // 1. Hae Order (Aggregate Root)
        var order = await _orderRepository.GetByIdAsync(command.OrderId, cancellationToken);
        
        if (order == null)
            throw new DomainException($"Order {command.OrderId} not found");
        
        // 2. Käytä domain-logiikkaa
        var unitPrice = Money.Euro(command.UnitPrice);
        order.AddItem(command.ProductId, command.ProductName, command.Quantity, unitPrice);
        
        // 3. Tallenna
        await _orderRepository.UpdateAsync(order, cancellationToken);
    }
}
```

#### CancelOrderHandler.cs

```csharp
namespace OrderManagement.Application.Handlers;

public class CancelOrderHandler
{
    private readonly IOrderRepository _orderRepository;
    
    public CancelOrderHandler(IOrderRepository orderRepository)
    {
        _orderRepository = orderRepository;
    }
    
    public async Task HandleAsync(
        CancelOrderCommand command, 
        CancellationToken cancellationToken = default)
    {
        // 1. Hae Order
        var order = await _orderRepository.GetByIdAsync(command.OrderId, cancellationToken);
        
        if (order == null)
            throw new DomainException($"Order {command.OrderId} not found");
        
        // 2. Peruuta (domain-logiikka validoi)
        order.Cancel(command.Reason);
        
        // 3. Tallenna
        await _orderRepository.UpdateAsync(order, cancellationToken);
        
        // Domain Event (OrderCancelledEvent) käsitellään automaattisesti
    }
}
```

---

## Infrastructure Layer

Infrastructure Layer sisältää **tekniset yksityiskohdat** (tietokanta, ulkoiset palvelut).

### 1. DbContext

#### ApplicationDbContext.cs

```csharp
namespace OrderManagement.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();
    public DbSet<OrderItem> OrderItems => Set<OrderItem>();
    
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
        base.OnModelCreating(modelBuilder);
    }
    
    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Käsittele Domain Events ennen tallennusta
        var domainEvents = ChangeTracker.Entries<IAggregateRoot>()
            .Select(e => e.Entity)
            .Where(e => e.DomainEvents.Any())
            .SelectMany(e => e.DomainEvents)
            .ToList();
        
        var result = await base.SaveChangesAsync(cancellationToken);
        
        // Lähetä Domain Events (esim. MediatR:n kautta)
        foreach (var domainEvent in domainEvents)
        {
            // await _mediator.Publish(domainEvent, cancellationToken);
        }
        
        return result;
    }
}
```

### 2. Entity Configurations

#### OrderConfiguration.cs

```csharp
namespace OrderManagement.Infrastructure.Persistence.Configurations;

public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");
        
        builder.HasKey(o => o.Id);
        
        builder.Property(o => o.CustomerName)
            .IsRequired()
            .HasMaxLength(200);
        
        // Value Object: Email
        builder.OwnsOne(o => o.CustomerEmail, email =>
        {
            email.Property(e => e.Value)
                .HasColumnName("CustomerEmail")
                .IsRequired()
                .HasMaxLength(255);
        });
        
        // Value Object: Address
        builder.OwnsOne(o => o.ShippingAddress, address =>
        {
            address.Property(a => a.Street)
                .HasColumnName("ShippingStreet")
                .IsRequired()
                .HasMaxLength(200);
                
            address.Property(a => a.City)
                .HasColumnName("ShippingCity")
                .IsRequired()
                .HasMaxLength(100);
                
            address.Property(a => a.PostalCode)
                .HasColumnName("ShippingPostalCode")
                .IsRequired()
                .HasMaxLength(20);
                
            address.Property(a => a.Country)
                .HasColumnName("ShippingCountry")
                .IsRequired()
                .HasMaxLength(100);
        });
        
        // Value Object: Money
        builder.OwnsOne(o => o.TotalAmount, money =>
        {
            money.Property(m => m.Amount)
                .HasColumnName("TotalAmount")
                .HasColumnType("decimal(18,2)")
                .IsRequired();
                
            money.Property(m => m.Currency)
                .HasColumnName("Currency")
                .IsRequired()
                .HasMaxLength(3);
        });
        
        builder.OwnsOne(o => o.DiscountAmount, money =>
        {
            money.Property(m => m.Amount)
                .HasColumnName("DiscountAmount")
                .HasColumnType("decimal(18,2)");
                
            money.Property(m => m.Currency)
                .HasColumnName("DiscountCurrency")
                .HasMaxLength(3);
        });
        
        builder.Property(o => o.Status)
            .IsRequired()
            .HasConversion<string>();
        
        // Relationship: Order -> OrderItems
        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);
        
        // Ignore Domain Events (ei tietokantaan)
        builder.Ignore(o => o.DomainEvents);
    }
}
```

#### OrderItemConfiguration.cs

```csharp
namespace OrderManagement.Infrastructure.Persistence.Configurations;

public class OrderItemConfiguration : IEntityTypeConfiguration<OrderItem>
{
    public void Configure(EntityTypeBuilder<OrderItem> builder)
    {
        builder.ToTable("OrderItems");
        
        builder.HasKey(i => i.Id);
        
        builder.Property(i => i.ProductName)
            .IsRequired()
            .HasMaxLength(200);
        
        builder.Property(i => i.Quantity)
            .IsRequired();
        
        // Value Object: Money (UnitPrice)
        builder.OwnsOne(i => i.UnitPrice, money =>
        {
            money.Property(m => m.Amount)
                .HasColumnName("UnitPrice")
                .HasColumnType("decimal(18,2)")
                .IsRequired();
                
            money.Property(m => m.Currency)
                .HasColumnName("Currency")
                .IsRequired()
                .HasMaxLength(3);
        });
        
        // Ignore calculated property
        builder.Ignore(i => i.TotalPrice);
    }
}
```

### 3. Repository Implementation

#### OrderRepository.cs

```csharp
namespace OrderManagement.Infrastructure.Persistence.Repositories;

public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<Order?> GetByIdAsync(int id, CancellationToken cancellationToken = default)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id, cancellationToken);
    }
    
    public async Task<List<Order>> GetByCustomerIdAsync(
        int customerId, 
        CancellationToken cancellationToken = default)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .Where(o => o.CustomerId == customerId)
            .OrderByDescending(o => o.CreatedAt)
            .ToListAsync(cancellationToken);
    }
    
    public async Task<List<Order>> GetAllAsync(CancellationToken cancellationToken = default)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .ToListAsync(cancellationToken);
    }
    
    public async Task AddAsync(Order order, CancellationToken cancellationToken = default)
    {
        await _context.Orders.AddAsync(order, cancellationToken);
        await _context.SaveChangesAsync(cancellationToken);
    }
    
    public async Task UpdateAsync(Order order, CancellationToken cancellationToken = default)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync(cancellationToken);
    }
    
    public async Task DeleteAsync(int id, CancellationToken cancellationToken = default)
    {
        var order = await GetByIdAsync(id, cancellationToken);
        if (order != null)
        {
            _context.Orders.Remove(order);
            await _context.SaveChangesAsync(cancellationToken);
        }
    }
    
    public async Task<bool> ExistsAsync(int id, CancellationToken cancellationToken = default)
    {
        return await _context.Orders.AnyAsync(o => o.Id == id, cancellationToken);
    }
}
```

---

## Presentation Layer

### OrdersController.cs

```csharp
namespace OrderManagement.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly PlaceOrderHandler _placeOrderHandler;
    private readonly AddOrderItemHandler _addOrderItemHandler;
    private readonly CancelOrderHandler _cancelOrderHandler;
    private readonly IOrderRepository _orderRepository;
    
    public OrdersController(
        PlaceOrderHandler placeOrderHandler,
        AddOrderItemHandler addOrderItemHandler,
        CancelOrderHandler cancelOrderHandler,
        IOrderRepository orderRepository)
    {
        _placeOrderHandler = placeOrderHandler;
        _addOrderItemHandler = addOrderItemHandler;
        _cancelOrderHandler = cancelOrderHandler;
        _orderRepository = orderRepository;
    }
    
    [HttpPost]
    public async Task<IActionResult> PlaceOrder([FromBody] PlaceOrderCommand command)
    {
        try
        {
            var orderId = await _placeOrderHandler.HandleAsync(command);
            return CreatedAtAction(nameof(GetOrder), new { id = orderId }, new { orderId });
        }
        catch (DomainException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }
    
    [HttpGet("{id}")]
    public async Task<IActionResult> GetOrder(int id)
    {
        var order = await _orderRepository.GetByIdAsync(id);
        
        if (order == null)
            return NotFound();
            
        return Ok(order);
    }
    
    [HttpGet("customer/{customerId}")]
    public async Task<IActionResult> GetCustomerOrders(int customerId)
    {
        var orders = await _orderRepository.GetByCustomerIdAsync(customerId);
        return Ok(orders);
    }
    
    [HttpPost("{id}/items")]
    public async Task<IActionResult> AddOrderItem(int id, [FromBody] AddOrderItemCommand command)
    {
        try
        {
            command.OrderId = id;
            await _addOrderItemHandler.HandleAsync(command);
            return Ok();
        }
        catch (DomainException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }
    
    [HttpPost("{id}/cancel")]
    public async Task<IActionResult> CancelOrder(int id, [FromBody] CancelOrderCommand command)
    {
        try
        {
            command.OrderId = id;
            await _cancelOrderHandler.HandleAsync(command);
            return Ok();
        }
        catch (DomainException ex)
        {
            return BadRequest(new { error = ex.Message });
        }
    }
}
```

### Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Database
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Domain Services
builder.Services.AddScoped<IOrderPricingService, OrderPricingService>();

// Repositories
builder.Services.AddScoped<IOrderRepository, OrderRepository>();

// Handlers
builder.Services.AddScoped<PlaceOrderHandler>();
builder.Services.AddScoped<AddOrderItemHandler>();
builder.Services.AddScoped<CancelOrderHandler>();

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

---

## Kokonaisuus toiminnassa

### Esimerkki: Tilauksen tekeminen

```
1. HTTP POST /api/orders
   ↓
2. OrdersController.PlaceOrder()
   ↓
3. PlaceOrderHandler.HandleAsync()
   ├─→ Luo Value Objects (Email, Address, Money)
   ├─→ Order.CreateDraft() (Factory Method)
   ├─→ Order.AddItem() (Domain Logic)
   ├─→ OrderPricingService (Domain Service)
   ├─→ Order.ApplyDiscount() (Domain Logic)
   ├─→ Order.Submit() (Domain Logic)
   │   └─→ AddDomainEvent(OrderPlacedEvent) ← Event
   └─→ OrderRepository.AddAsync()
       └─→ DbContext.SaveChangesAsync()
           └─→ Publish Domain Events
               └─→ OrderPlacedEventHandler
                   └─→ Send Email Notification
```

### Tietovirta

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                     │
│  OrdersController → Vastaanottaa HTTP request            │
└───────────────────────────┬──────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│                   Application Layer                       │
│  PlaceOrderHandler → Orkestroi use case:n                │
└───────────────────────────┬──────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│                     Domain Layer                          │
│  Order (Aggregate) → Liiketoimintalogiikka              │
│  OrderPricingService → Domain-logiikka                   │
│  OrderPlacedEvent → Tapahtuma                            │
└───────────────────────────┬──────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                     │
│  OrderRepository → Tietokantatallentuu                   │
│  ApplicationDbContext → EF Core                          │
└──────────────────────────────────────────────────────────┘
```

### Testaus

**Unit Test - Domain Logic:**

```csharp
public class OrderTests
{
    [Fact]
    public void Order_AddItem_IncreasesTotalAmount()
    {
        // Arrange
        var order = Order.CreateDraft(
            1, 
            "John Doe",
            new Email("john@example.com"),
            new Address("Street 1", "City", "12345", "Country"));
        
        // Act
        order.AddItem(1, "Product A", 2, Money.Euro(10));
        
        // Assert
        Assert.Equal(Money.Euro(20), order.TotalAmount);
    }
    
    [Fact]
    public void Order_Submit_EmptyOrder_ThrowsException()
    {
        // Arrange
        var order = Order.CreateDraft(
            1, 
            "John Doe",
            new Email("john@example.com"),
            new Address("Street 1", "City", "12345", "Country"));
        
        // Act & Assert
        Assert.Throws<DomainException>(() => order.Submit());
    }
    
    [Fact]
    public void Order_Cancel_AlreadyCancelled_ThrowsException()
    {
        // Arrange
        var order = Order.CreateDraft(
            1, 
            "John Doe",
            new Email("john@example.com"),
            new Address("Street 1", "City", "12345", "Country"));
        order.Cancel("Test");
        
        // Act & Assert
        Assert.Throws<DomainException>(() => order.Cancel("Test again"));
    }
}
```

---

## Yhteenveto

### Mitä saavutimme?

✅ **Clean Architecture + DDD yhdistelmä**
- Domain Layer sisältää kaiken liiketoimintalogiikan
- Ei riippuvuuksia infrastruktuuriin
- Testattava ilman tietokantaa

✅ **DDD Building Blocks käytössä**
- **Entities**: Order, OrderItem
- **Value Objects**: Money, Email, Address
- **Aggregate**: Order + OrderItems
- **Domain Events**: OrderPlacedEvent, OrderCancelledEvent
- **Repository**: IOrderRepository
- **Domain Service**: OrderPricingService

✅ **Liiketoimintalogiikka Domain-kerroksessa**
- Validointi domain-malleissa
- Invariantit suojattu
- Selkeät liiketoimintasäännöt

✅ **Ubiquitous Language**
- PlaceOrder(), Cancel(), Submit()
- Sama kieli koodissa ja liiketoiminnassa

### Keskeiset opit

| Konsepti | Esimerkki projektista |
|----------|----------------------|
| **Entity** | Order, OrderItem (identiteetti) |
| **Value Object** | Money, Email, Address (arvo) |
| **Aggregate Root** | Order (pääsy muihin aggregaatin osiin) |
| **Domain Event** | OrderPlacedEvent (jotain tapahtui) |
| **Repository** | IOrderRepository (abstraktio) |
| **Domain Service** | OrderPricingService (moneen entityyn liittyvä logiikka) |
| **Use Case** | PlaceOrderHandler (sovelluksen toiminto) |

### Seuraavat askeleet

1. 📖 Lue DDD teoria: **[Domain-Driven-Design.md](Domain-Driven-Design.md)**
2. 🏗️ Tutustu Clean Architecture:iin: **[Clean-Architecture.md](Clean-Architecture.md)**
3. 💻 Kokeile rakentaa oma DDD-sovellus
4. 📚 Lue lisää: Eric Evansin "Domain-Driven Design"

### Hyödyllisiä linkkejä

- [Microsoft: DDD in .NET](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/)
- [DDD Reference by Eric Evans](https://www.domainlanguage.com/ddd/reference/)
- [Implementing DDD by Vaughn Vernon](https://vaughnvernon.com/)

---

**Muista:** Pidä se yksinkertaisena! Käytä DDD:tä vain kun kompleksisuus sitä vaatii. 🚀
