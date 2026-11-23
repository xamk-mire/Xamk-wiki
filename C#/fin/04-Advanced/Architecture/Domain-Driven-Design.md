# Domain-Driven Design (DDD)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on Domain-Driven Design?](#mikä-on-domain-driven-design)
3. [Historia](#historia)
4. [Mitä ongelmia DDD ratkaisee?](#mitä-ongelmia-ddd-ratkaisee)
5. [Keskeiset käsitteet](#keskeiset-käsitteet)
6. [Strategic Design](#strategic-design)
7. [Tactical Design](#tactical-design)
   - [Invariantti](#invariantti)
   - [Aneeminen ja rikas malli](#aneeminen-ja-rikas-malli)
   - [Mihin sääntö kuuluu? (nyrkkisääntö)](#mihin-sääntö-kuuluu-nyrkkisääntö)
   - [Ei entiteetti eikä value object](#ei-entiteetti-eikä-value-object)
   - [Milloin value objectia ei kannata tehdä](#milloin-value-objectia-ei-kannata-tehdä)
8. [DDD ja arkkitehtuurit](#ddd-ja-arkkitehtuurit)
9. [Edut ja haitat](#edut-ja-haitat)
10. [Milloin käyttää DDD:tä?](#milloin-käyttää-dddtä)
11. [Parhaat käytännöt](#parhaat-käytännöt)
12. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Domain-Driven Design (DDD)** on lähestymistapa monimutkaisten ohjelmistojärjestelmien suunnitteluun ja kehittämiseen, jossa **liiketoiminta-alue (domain)** on keskiössä. DDD ei ole arkkitehtuurimalli vaan **suunnittelufilosofia**, joka auttaa organisoimaan koodia liiketoiminnan tarpeiden mukaan.

### Keskeiset periaatteet

1. **Domain on keskiössä** - Liiketoimintalogiikka on tärkein osa sovellusta
2. **Ubiquitous Language** - Yhteinen kieli kehittäjien ja domain-eksperttien välillä
3. **Bounded Context** - Selkeät kontekstirajat eri osajärjestelmille
4. **Iteratiivinen kehitys** - Domain-malli kehittyy ymmärryksen kasvaessa

---

## Mikä on Domain-Driven Design?

### Määritelmä

> "Domain-Driven Design on lähestymistapa ohjelmistokehitykseen, jossa monimutkaisten tarpeiden yhteydessä suunnittelun keskipisteenä on liiketoiminta-alue ja sen logiikka."
> 
> — Eric Evans, Domain-Driven Design (2003)

### DDD:n ydin

DDD keskittyy kolmeen pääalueeseen:

**1. Domain (Liiketoiminta-alue)**
- Mitä ongelmaa ratkaistaan?
- Mitkä ovat liiketoimintasäännöt?
- Kuka käyttää sovellusta ja miksi?

**2. Model (Malli)**
- Miten liiketoiminta-alue mallinnetaan koodissa?
- Mitkä käsitteet ovat tärkeitä?
- Miten ne liittyvät toisiinsa?

**3. Ubiquitous Language (Yhteinen kieli)**
- Sama terminologia koodissa ja liiketoiminnassa
- Ei teknistä jargonia domain-malleissa
- Kaikki käyttävät samoja termejä

### Esimerkki: Verkkokauppa

```
Liiketoiminta sanoo:          DDD-malli:
"Asiakas tekee tilauksen"  →  Customer.PlaceOrder()
"Tilaus sisältää tuotteita" →  Order.AddOrderItem(Product)
"Maksu hyväksytään"        →  Payment.Approve()
```

**Huomaa:** Koodi puhuu samaa kieltä kuin liiketoiminta!

---

## Historia

### 2003: Eric Evansin kirja

Domain-Driven Design syntyi, kun Eric Evans julkaisi kirjansa **"Domain-Driven Design: Tackling Complexity in the Heart of Software"** vuonna 2003.

### Miksi DDD syntyi?

**Ongelma 1990-luvulla:**
```
┌─────────────────────────────────────┐
│  Sovellukset kasvoivat              │
│  Liiketoimintalogiikka monimutkaistui │
│  Kehittäjät eivät ymmärtäneet domaineja │
│  Domain-ekspertit eivät ymmärtäneet koodia │
└─────────────────────────────────────┘
           ↓
    Huono kommunikaatio
    Bugit ja virheet
    Kallis ylläpito
```

**Ratkaisu: DDD**
```
┌─────────────────────────────────────┐
│  Yhteinen kieli (Ubiquitous Language) │
│  Domain-malli koodin ytimessä       │
│  Kehittäjät ja domain-ekspertit     │
│  työskentelevät yhdessä             │
└─────────────────────────────────────┘
```

### Kehitys vuosien varrella

| Vuosi | Tapahtuma |
|-------|-----------|
| **2003** | Eric Evansin DDD-kirja julkaistaan |
| **2005-2010** | DDD leviää enterprise-sovelluksiin |
| **2010** | CQRS ja Event Sourcing yhdistetään DDD:hen |
| **2013** | Vaughn Vernonin "Implementing DDD" -kirja |
| **2015+** | Microservices + DDD (Bounded Context per service) |
| **2020+** | DDD modernissa .NET-kehityksessä |

---

## Mitä ongelmia DDD ratkaisee?

### Ongelma 1: Kompleksinen liiketoimintalogiikka

**❌ Ilman DDD:tä:**

```csharp
// Liiketoimintalogiikka levällään kaikkialla
public class OrderController : Controller
{
    [HttpPost]
    public IActionResult CreateOrder(OrderDto dto)
    {
        // Liiketoimintasääntöjä controllerissa 🚫
        if (dto.Items.Sum(i => i.Price * i.Quantity) < 10)
            return BadRequest("Minimum order is 10€");
        
        if (dto.CustomerId == null)
            return BadRequest("Customer required");
        
        // Tietokantalogiikkaa controllerissa 🚫
        var order = new Order 
        { 
            CustomerId = dto.CustomerId,
            Total = dto.Items.Sum(i => i.Price * i.Quantity)
        };
        _context.Orders.Add(order);
        _context.SaveChanges();
        
        return Ok(order.Id);
    }
}
```

**✅ DDD:llä:**

```csharp
// Controller on ohut, liiketoimintalogiikka domain-mallissa
public class OrderController : Controller
{
    private readonly IOrderService _orderService;
    
    [HttpPost]
    public async Task<IActionResult> CreateOrder(PlaceOrderCommand command)
    {
        var result = await _orderService.PlaceOrderAsync(command);
        return result.IsSuccess ? Ok(result.Value) : BadRequest(result.Error);
    }
}

// Liiketoimintalogiikka domain-mallissa ✅
public class Order : Entity<OrderId>
{
    public void PlaceOrder(Customer customer, List<OrderItem> items)
    {
        ValidateMinimumAmount(items);
        ValidateCustomer(customer);
        
        Status = OrderStatus.Pending;
        TotalAmount = CalculateTotal(items);
        
        // Domain event
        AddDomainEvent(new OrderPlacedEvent(Id, customer.Id));
    }
    
    private void ValidateMinimumAmount(List<OrderItem> items)
    {
        if (items.Sum(i => i.TotalPrice.Amount) < 10)
            throw new DomainException("Minimum order amount is 10€");
    }
}
```

### Ongelma 2: Kehittäjät ja domain-ekspertit puhuvat eri kieltä

**❌ Ongelma:**

```
Domain-ekspertti: "Kun asiakas tekee tilauksen..."
Kehittäjä:        "Okei, eli insert into orders table..."
Domain-ekspertti: "Tilaus pitää validoida..."
Kehittäjä:        "Mitä validointeja? En tiennyt."
```

**✅ DDD:n ratkaisu - Ubiquitous Language:**

```
Domain-ekspertti: "Kun asiakas tekee tilauksen..."
Kehittäjä:        "Customer.PlaceOrder()?"
Domain-ekspertti: "Kyllä! Ja tilaus pitää validoida ensin."
Kehittäjä:        "Order.Validate()? Mitä sääntöjä?"
Domain-ekspertti: "Minimisumma, asiakastiedot..."
```

Koodi käyttää **samoja termejä** kuin liiketoiminta!

### Ongelma 3: Huono modulaarisuus

**❌ Ilman DDD:tä:**
```
Kaikki samassa kontekstissa
→ Tiukka kytkös
→ Vaikea testata
→ Vaikea ylläpitää
```

**✅ DDD:llä:**
```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Orders     │  │   Customers  │  │   Inventory  │
│   Context    │  │   Context    │  │   Context    │
└──────────────┘  └──────────────┘  └──────────────┘
     ↑                  ↑                  ↑
Bounded Context    Bounded Context   Bounded Context
```

---

## Keskeiset käsitteet

### Domain (Liiketoiminta-alue)

**Domain** on sovelluksen **liiketoiminta-alue** - se mitä sovellus tekee.

**Esimerkkejä:**
- Verkkokauppa → Tilausten hallinta, maksaminen, toimitus
- Pankki → Tilit, siirrot, lainat
- Sairaala → Potilaat, diagnoosit, lääkitykset

### Subdomain (Osa-alue)

Domain jaetaan pienempiin **subdomain:eihin**:

```
Verkkokauppa (Domain)
├── Order Management (Core Subdomain) ← Kriittisin
├── Inventory (Supporting Subdomain)
├── Shipping (Supporting Subdomain)
└── Email Notifications (Generic Subdomain)
```

**Tyypit:**

| Subdomain | Kuvaus | Esimerkki |
|-----------|--------|-----------|
| **Core** | Yrityksen ydinosaaminen, kilpailuetu | Tilausten hallinta |
| **Supporting** | Tukee ydintoimintoa | Varastonhallinta |
| **Generic** | Yleinen, ei kilpailuetua | Sähköposti, lokitus |

### Ubiquitous Language (Yhteinen kieli)

**Yhteinen kieli**, jota **kaikki** käyttävät:

✅ **Käytetään:**
- Domain-eksperttien kanssa keskusteluissa
- Dokumentaatiossa
- Koodissa (luokat, metodit, muuttujat)
- Testeissä

**Esimerkki:**

```csharp
// ❌ Huono - tekninen kieli
public class DataObject
{
    public int Id { get; set; }
    public string Field1 { get; set; }
    public decimal Field2 { get; set; }
    
    public void Process()
    {
        // Mitä tämä tekee?
    }
}

// ✅ Hyvä - Ubiquitous Language
public class Order
{
    public OrderId Id { get; private set; }
    public Customer Customer { get; private set; }
    public Money TotalAmount { get; private set; }
    
    public void PlaceOrder()
    {
        // Selkeä tarkoitus!
    }
}
```

---

## Strategic Design

**Strategic Design** keskittyy **kokonaisuuteen** - miten domain jaetaan osiin.

### Bounded Context (Kontekstiraja)

**Bounded Context** on raja, jonka sisällä tietty domain-malli on voimassa.

```
┌─────────────────────────────────────────────────────────┐
│                    VERKKOKAUPPA                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────────┐  ┌──────────────────┐           │
│  │  Order Context   │  │ Customer Context │           │
│  │                  │  │                  │           │
│  │  Order           │  │  Customer        │           │
│  │  - Id            │  │  - Id            │           │
│  │  - Items         │  │  - Name          │           │
│  │  - Total         │  │  - Email         │           │
│  │                  │  │  - Address       │           │
│  │  PlaceOrder()    │  │  Register()      │           │
│  └──────────────────┘  └──────────────────┘           │
│          ↓                      ↓                      │
│   Tilaus-konteksti       Asiakas-konteksti            │
│   tuntee Order:in        tuntee Customer:in           │
│   eri tavalla kuin       eri tavalla kuin             │
│   muut kontekstit        muut kontekstit              │
└─────────────────────────────────────────────────────────┘
```

**Miksi Bounded Context?**

- Sama termi voi tarkoittaa eri asioita eri konteksteissa
- Esim. "Customer" Order Context:ssa vs. Marketing Context:ssa

**Esimerkki:**

```csharp
// Order Context - Customer on yksinkertainen
namespace OrderContext
{
    public class Customer
    {
        public CustomerId Id { get; }
        public string Name { get; }
        // Vain tilauksen kannalta oleellinen tieto
    }
}

// Customer Context - Customer on monimutkainen
namespace CustomerContext
{
    public class Customer
    {
        public CustomerId Id { get; }
        public string FirstName { get; }
        public string LastName { get; }
        public Email Email { get; }
        public Address BillingAddress { get; }
        public Address ShippingAddress { get; }
        public List<Order> OrderHistory { get; }
        public LoyaltyPoints Points { get; }
        // Paljon enemmän tietoa ja logiikkaa
    }
}
```

### Context Map

**Context Map** näyttää miten Bounded Contextit liittyvät toisiinsa.

```
┌─────────────────┐         ┌─────────────────┐
│  Order Context  │────────▶│ Payment Context │
│                 │  API    │                 │
└─────────────────┘         └─────────────────┘
        │
        │ Events
        ↓
┌─────────────────┐         ┌─────────────────┐
│Shipping Context │◀────────│Inventory Context│
│                 │  Check  │                 │
└─────────────────┘  Stock  └─────────────────┘
```

**Suhdetyypit:**

| Suhde | Kuvaus |
|-------|--------|
| **Partnership** | Kaksi tiimiä työskentelevät yhdessä |
| **Shared Kernel** | Jaettu ydin, molemmat muokkaavat |
| **Customer-Supplier** | Downstream riippuu upstream:sta |
| **Conformist** | Downstream hyväksyy upstream:n mallin |
| **Anti-Corruption Layer** | Käännöskerros suojaamaan omaa mallia |

---

## Tactical Design

**Tactical Design** keskittyy **yksityiskohtiin** - miten domain-malli rakennetaan.

### Building Blocks (Rakennuspalikat)

#### 1. Entity (Entiteetti)

**Entity** on olio, jolla on **identiteetti** ja joka elää ajan kuluessa.

**Tunnusmerkit:**
- ✅ Uniikki identiteetti (Id)
- ✅ Muuttuva (mutable)
- ✅ Identiteetti säilyy muutosten jälkeen

**Esimerkki:**

```csharp
public class Order : Entity<OrderId>
{
    // Identiteetti (Id) tulee kantaluokasta Entity<OrderId>
    
    // Muuttuvia arvoja
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }
    public DateTime CreatedAt { get; private set; }
    
    // Private setter - vain domain-logiikka muuttaa
    private readonly List<OrderItem> _items = new();
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    
    // Liiketoimintalogiikka
    public void AddItem(Product product, int quantity)
    {
        if (Status != OrderStatus.Draft)
            throw new DomainException("Cannot modify confirmed order");
            
        var item = new OrderItem(product, quantity);
        _items.Add(item);
        RecalculateTotal();
    }
    
    public void Submit()
    {
        if (!_items.Any())
            throw new DomainException("Cannot submit empty order");
            
        Status = OrderStatus.Submitted;
        AddDomainEvent(new OrderSubmittedEvent(Id));
    }
    
    private void RecalculateTotal()
    {
        TotalAmount = new Money(_items.Sum(i => i.TotalPrice.Amount), "EUR");
    }
}

// Base class: tunniste, vertailu ja domain-tapahtumien lista
public abstract class Entity<TId> where TId : notnull
{
    public TId Id { get; protected set; } = default!;
    
    private readonly List<IDomainEvent> _domainEvents = new();
    public IReadOnlyList<IDomainEvent> DomainEvents => _domainEvents.AsReadOnly();
    
    protected void AddDomainEvent(IDomainEvent domainEvent) => _domainEvents.Add(domainEvent);
    public void ClearDomainEvents() => _domainEvents.Clear();
    
    public override bool Equals(object? obj)
    {
        // Vertailu ID:n perusteella
        if (obj is not Entity<TId> other || other.GetType() != GetType())
            return false;
            
        return Id.Equals(other.Id);
    }
    
    public override int GetHashCode() => Id.GetHashCode();
}
```

`IDomainEvent` esitellään alempana kohdassa Domain Event.

**Milloin käyttää?**
- Kun identiteetti on tärkeä (esim. Order, Customer, Product)
- Kun olio muuttuu ajan kuluessa

#### 2. Value Object (Arvo-olio)

**Value Object** on olio, joka määritellään **arvoillaan**, ei identiteetillä.

**Tunnusmerkit:**
- ✅ Ei identiteettiä
- ✅ Muuttumaton (immutable)
- ✅ Vertailu arvojen perusteella

**Esimerkki:**

```csharp
public class Money : ValueObject
{
    public decimal Amount { get; }
    public string Currency { get; }
    
    public Money(decimal amount, string currency)
    {
        if (amount < 0)
            throw new ArgumentException("Amount cannot be negative");
            
        if (string.IsNullOrWhiteSpace(currency))
            throw new ArgumentException("Currency is required");
            
        Amount = amount;
        Currency = currency;
    }
    
    // Operaatiot palauttavat UUDEN olion
    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("Cannot add different currencies");
            
        return new Money(Amount + other.Amount, Currency);
    }
    
    public Money Multiply(decimal multiplier)
    {
        return new Money(Amount * multiplier, Currency);
    }
    
    // Vertailu arvojen perusteella
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Amount;
        yield return Currency;
    }
    
    public override string ToString() => $"{Amount:F2} {Currency}";
}

// Base class
public abstract class ValueObject
{
    protected abstract IEnumerable<object> GetEqualityComponents();
    
    public override bool Equals(object obj)
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
}
```

**Lisää esimerkkejä:**

```csharp
// Address
public class Address : ValueObject
{
    public string Street { get; }
    public string City { get; }
    public string PostalCode { get; }
    public string Country { get; }
    
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Street;
        yield return City;
        yield return PostalCode;
        yield return Country;
    }
}

// Email
public class Email : ValueObject
{
    public string Value { get; }
    
    public Email(string value)
    {
        if (!IsValid(value))
            throw new ArgumentException("Invalid email format");
            
        Value = value;
    }
    
    private static bool IsValid(string email)
    {
        return !string.IsNullOrWhiteSpace(email) && email.Contains("@");
    }
    
    protected override IEnumerable<object> GetEqualityComponents()
    {
        yield return Value;
    }
}
```

**Milloin käyttää?**
- Kun identiteetti ei ole tärkeä (esim. Money, Address, Email)
- Kun haluat kapsuloida validointia
- Kun haluat immutable-olioita

#### 3. Aggregate (Aggregaatti)

**Aggregate** on **kokoelma** toisiinsa liittyviä olioita, joita käsitellään yhtenä yksikkönä.

**Tunnusmerkit:**
- ✅ Aggregate Root - pääolio, joka "omistaa" muut
- ✅ Consistency Boundary - yhtenäisyyden raja
- ✅ Kaikki muutokset Aggregate Root:n kautta

```
┌─────────────────────────────────────┐
│        Order (Aggregate Root)       │ ← Ainoa julkinen pääsy
├─────────────────────────────────────┤
│  - OrderId                          │
│  - Customer                         │
│  - Status                           │
│  - TotalAmount                      │
│                                     │
│  ┌────────────────────────────┐    │
│  │  OrderItem (Internal)      │    │ ← Ei suoraa pääsyä ulkoa
│  │  - Product                 │    │
│  │  - Quantity                │    │
│  │  - Price                   │    │
│  └────────────────────────────┘    │
│                                     │
│  Methods:                           │
│  - AddItem()                        │
│  - RemoveItem()                     │
│  - Submit()                         │
└─────────────────────────────────────┘
```

**Esimerkki:**

```csharp
// Aggregate Root
public class Order : Entity<OrderId>, IAggregateRoot
{
    public CustomerId CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    public Money TotalAmount { get; private set; }
    
    // Private collection - ei suoraa pääsyä!
    private readonly List<OrderItem> _items = new();
    public IReadOnlyList<OrderItem> Items => _items.AsReadOnly();
    
    // Domain-tapahtumien lista (DomainEvents, AddDomainEvent) tulee kantaluokasta
    
    // Kaikki muutokset Aggregate Root:n kautta
    public void AddItem(ProductId productId, int quantity, Money unitPrice)
    {
        ValidateCanModify();
        
        var existingItem = _items.FirstOrDefault(i => i.ProductId == productId);
        if (existingItem != null)
        {
            existingItem.IncreaseQuantity(quantity);
        }
        else
        {
            _items.Add(new OrderItem(productId, quantity, unitPrice));
        }
        
        RecalculateTotal();
    }
    
    public void RemoveItem(OrderItemId itemId)
    {
        ValidateCanModify();
        
        var item = _items.FirstOrDefault(i => i.Id == itemId);
        if (item == null)
            throw new DomainException("Item not found");
            
        _items.Remove(item);
        RecalculateTotal();
    }
    
    public void Submit()
    {
        if (!_items.Any())
            throw new DomainException("Cannot submit empty order");
            
        if (Status != OrderStatus.Draft)
            throw new DomainException("Only draft orders can be submitted");
            
        Status = OrderStatus.Submitted;
        AddDomainEvent(new OrderSubmittedEvent(Id, CustomerId, TotalAmount));
    }
    
    private void ValidateCanModify()
    {
        if (Status != OrderStatus.Draft)
            throw new DomainException("Cannot modify non-draft order");
    }
    
    private void RecalculateTotal()
    {
        var total = _items.Sum(i => i.TotalPrice.Amount);
        TotalAmount = new Money(total, "EUR");
    }
}

// Internal Entity - osa Aggregatea
public class OrderItem : Entity<OrderItemId>
{
    public ProductId ProductId { get; private set; }
    public int Quantity { get; private set; }
    public Money UnitPrice { get; private set; }
    public Money TotalPrice => UnitPrice.Multiply(Quantity);
    
    // Internal constructor - vain Order voi luoda
    internal OrderItem(ProductId productId, int quantity, Money unitPrice)
    {
        if (quantity <= 0)
            throw new DomainException("Quantity must be positive");
            
        Id = OrderItemId.New();
        ProductId = productId;
        Quantity = quantity;
        UnitPrice = unitPrice;
    }
    
    internal void IncreaseQuantity(int amount)
    {
        if (amount <= 0)
            throw new DomainException("Amount must be positive");
            
        Quantity += amount;
    }
}
```

**Aggregate Design Rules:**

1. ✅ **Viittaa toisiin Aggregateihin ID:llä**
```csharp
// ✅ Hyvä
public class Order
{
    public CustomerId CustomerId { get; private set; } // Vain ID
}

// ❌ Huono
public class Order
{
    public Customer Customer { get; private set; } // Koko olio
}
```

2. ✅ **Pidä Aggregatet pieninä**
```csharp
// ✅ Hyvä - Order ja Customer ovat eri Aggregateja
Order + OrderItems (yksi Aggregate)
Customer (toinen Aggregate)

// ❌ Huono - Kaikki yhdessä
Order + OrderItems + Customer + CustomerAddresses + ...
```

3. ✅ **Muokkaa yhtä Aggregatea kerrallaan**

#### 4. Domain Event (Domain-tapahtuma)

**Domain Event** kuvaa jotain **tapahtunutta** domainissa.

**Tunnusmerkit:**
- ✅ Menneessä aikamuodossa (OrderPlaced, PaymentProcessed)
- ✅ Immutable
- ✅ Sisältää kontekstitiedot

**Esimerkki:**

```csharp
public interface IDomainEvent
{
    DateTime OccurredOn { get; }
}

public class OrderSubmittedEvent : IDomainEvent
{
    public OrderId OrderId { get; }
    public CustomerId CustomerId { get; }
    public Money TotalAmount { get; }
    public DateTime OccurredOn { get; }
    
    public OrderSubmittedEvent(OrderId orderId, CustomerId customerId, Money totalAmount)
    {
        OrderId = orderId;
        CustomerId = customerId;
        TotalAmount = totalAmount;
        OccurredOn = DateTime.UtcNow;
    }
}

// Käyttö: lista ja metodit AddDomainEvent / ClearDomainEvents ovat kantaluokassa Entity<TId>
public class Order : Entity<OrderId>, IAggregateRoot
{
    public void Submit()
    {
        // ... validointi ...
        
        Status = OrderStatus.Submitted;
        
        // Lisää domain event
        AddDomainEvent(new OrderSubmittedEvent(Id, CustomerId, TotalAmount));
    }
}

// Event Handler
public class OrderSubmittedEventHandler : INotificationHandler<OrderSubmittedEvent>
{
    private readonly IEmailService _emailService;
    
    public async Task Handle(OrderSubmittedEvent notification, CancellationToken ct)
    {
        // Lähetä vahvistusviesti
        await _emailService.SendOrderConfirmationAsync(
            notification.CustomerId, 
            notification.OrderId);
    }
}
```

**Milloin käyttää?**
- Kun haluat erottaa huolenaiheita (Separation of Concerns)
- Kun eri Bounded Contextit kommunikoivat
- Eventual Consistency -tilanteissa

#### 5. Repository

**Repository** on abstraktio **tiedon tallennukselle**.

**Tunnusmerkit:**
- ✅ Yksi repository per Aggregate Root
- ✅ Collection-tyyppinen rajapinta
- ✅ Piilottaa tietokantayksityiskohdat

**Esimerkki:**

```csharp
// Domain Layer - Interface
public interface IOrderRepository
{
    Task<Order?> GetByIdAsync(OrderId id);
    Task<List<Order>> GetByCustomerIdAsync(CustomerId customerId);
    Task AddAsync(Order order);
    Task UpdateAsync(Order order);
}

// Infrastructure Layer - Implementation
public class OrderRepository : IOrderRepository
{
    private readonly ApplicationDbContext _context;
    
    public OrderRepository(ApplicationDbContext context)
    {
        _context = context;
    }
    
    public async Task<Order?> GetByIdAsync(OrderId id)
    {
        return await _context.Orders
            .Include(o => o.Items)
            .FirstOrDefaultAsync(o => o.Id == id);
    }
    
    public async Task<List<Order>> GetByCustomerIdAsync(CustomerId customerId)
    {
        return await _context.Orders
            .Where(o => o.CustomerId == customerId)
            .ToListAsync();
    }
    
    public async Task AddAsync(Order order)
    {
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();
    }
    
    public async Task UpdateAsync(Order order)
    {
        _context.Orders.Update(order);
        await _context.SaveChangesAsync();
    }
}
```

Repository hakee ja tallentaa. Se ei päätä liiketoimintasääntöjä, ja sen metodit tulevat käyttötapausten tarpeista. Siksi rajapinnassa ei ole esimerkiksi `DeleteAsync`-metodia, jos mikään käyttötapaus ei poista tilausta. Lisää: [Repository Pattern](../Patterns/Repository-Pattern.md#mitä-repository-tekee-ja-mitä-ei).

#### 6. Domain Service

**Domain Service** sisältää logiikkaa, joka **ei kuulu yhteen Entityyn**.

**Milloin käyttää?**
- Kun operaatio koskee useita Aggregateja
- Kun logiikka ei luontaisesti kuulu mihinkään Entityyn

**Esimerkki:**

```csharp
public interface IOrderPricingService
{
    Money CalculateTotal(Order order, Customer customer);
}

public class OrderPricingService : IOrderPricingService
{
    public Money CalculateTotal(Order order, Customer customer)
    {
        var subtotal = order.Items.Sum(i => i.TotalPrice.Amount);
        
        // Alennukset asiakkaan tason mukaan
        var discount = customer.Level switch
        {
            CustomerLevel.Gold => subtotal * 0.15m,
            CustomerLevel.Silver => subtotal * 0.10m,
            CustomerLevel.Bronze => subtotal * 0.05m,
            _ => 0m
        };
        
        return new Money(subtotal - discount, "EUR");
    }
}
```

#### 7. Factory

**Factory** luo monimutkaisia olioita.

Yksinkertaisin factory on entiteetin oma **staattinen tehdasmetodi**. Se on luokan sisällä, joten se saa asettaa private-setterit. Erillinen `OrderFactory`-luokka ei pystyisi siihen: setterit ovat `private`, eikä koodi kääntyisi.

**Esimerkki:**

```csharp
public class Order : Entity<OrderId>, IAggregateRoot
{
    // Private-konstruktori: tilauksen voi luoda vain tehdasmetodilla
    private Order() { }
    
    public static Order CreateDraft(CustomerId customerId)
    {
        return new Order
        {
            Id = OrderId.New(),
            CustomerId = customerId,
            Status = OrderStatus.Draft,
            TotalAmount = new Money(0, "EUR"),
            CreatedAt = DateTime.UtcNow
        };
    }
    
    public static Order CreateFrom(Order existingOrder)
    {
        Order newOrder = CreateDraft(existingOrder.CustomerId);
        
        foreach (OrderItem item in existingOrder.Items)
        {
            newOrder.AddItem(item.ProductId, item.Quantity, item.UnitPrice);
        }
        
        return newOrder;
    }
    
    // ... ominaisuudet ja muut metodit kuten yllä ...
}
```

### Invariantti

**Invariantti** on sääntö, jonka pitää olla voimassa aina. Ei vain tallennushetkellä, vaan jokaisen metodikutsun jälkeen.

Esimerkkejä sarjasovelluksesta, jossa on joukkueita ja otteluita:

- Ottelun koti- ja vierasjoukkue eivät ole sama joukkue.
- Ottelun tulos kirjataan vain kerran.
- Maalimäärä ei ole negatiivinen.

**Minkä ongelman se ratkaisee?** Jos sääntö tarkistetaan vain yhdessä servicessä, toinen koodipolku voi ohittaa sen. Silloin tietokantaan päätyy olio, jonka ei pitäisi olla mahdollinen. Kun olio itse vartioi invarianttiaan, virheellistä oliota ei voi olla olemassa.

**Kuka sen omistaa?** Invariantti, joka koskee vain olion omaa dataa, kuuluu oliolle itselleen: entiteetille tai value objectille. Se tarkistetaan konstruktorissa ja jokaisessa metodissa, joka muuttaa tilaa.

**Mikä ei ole invariantti?** Syötteen muototarkistus ("kenttä ei saa olla tyhjä JSON:ssa") on controllerin asia. Sääntö, joka vaatii haun tietokannasta ("nimi on vapaana"), ei ole yhden olion invariantti. Se tarkistetaan use casessa.

### Aneeminen ja rikas malli

**Aneeminen malli** (anemic model) on luokka, jossa on vain dataa. Säännöt ovat jossain muualla, yleensä servicessä.

```csharp
// Aneeminen: kuka tahansa voi asettaa minkä tahansa arvon
public class Match
{
    public int Id { get; set; }
    public int HomeTeamId { get; set; }
    public int AwayTeamId { get; set; }
    public int? HomeGoals { get; set; }
    public int? AwayGoals { get; set; }
}
```

Mikään ei estä kirjoittamasta `match.AwayTeamId = match.HomeTeamId;` tai kirjaamasta tulosta toiseen kertaan.

**Rikas malli** (rich model) on luokka, joka luodaan ja jota muutetaan vain sen omilla metodeilla. Metodit tarkistavat invariantit.

```csharp
// Rikas: olio vartioi omia sääntöjään
public class Match
{
    public int Id { get; private set; }
    public int HomeTeamId { get; private set; }
    public int AwayTeamId { get; private set; }
    public int? HomeGoals { get; private set; }
    public int? AwayGoals { get; private set; }

    public bool HasResult => HomeGoals.HasValue;

    public Match(int homeTeamId, int awayTeamId)
    {
        if (homeTeamId == awayTeamId)
            throw new InvalidOperationException("Koti- ja vierasjoukkue eivät voi olla sama");

        HomeTeamId = homeTeamId;
        AwayTeamId = awayTeamId;
    }

    public void RecordResult(int homeGoals, int awayGoals)
    {
        if (HasResult)
            throw new InvalidOperationException("Tulos on jo kirjattu");

        if (homeGoals < 0 || awayGoals < 0)
            throw new ArgumentException("Maalimäärä ei voi olla negatiivinen");

        HomeGoals = homeGoals;
        AwayGoals = awayGoals;
    }
}
```

| | Aneeminen malli | Rikas malli |
|---|---|---|
| Setterit | `public` | `private` |
| Säännöt | Servicessä | Oliossa itsessään |
| Voiko olio olla virheellisessä tilassa? | Kyllä | Ei |
| Säännön testaus | Tarvitaan service ja usein korvike repositorylle | `new Match(...)` ja metodikutsu riittää |

**Milloin aneeminen malli riittää?** Kun sovelluksessa ei ole juuri sääntöjä ja se vain tallentaa ja näyttää dataa. Silloin rikas malli on turhaa työtä. Myös DTO:t ovat tarkoituksella pelkkää dataa.

### Mihin sääntö kuuluu? (nyrkkisääntö)

Kysy: **mitä dataa tarkistus tarvitsee?**

- Tarvitsee vain olion omaa dataa → **entiteetti tai value object**.
- Tarvitsee haun tai toisen olion → **use case** (Application-kerros).

| Sääntö | Mitä dataa tarvitaan | Paikka |
|---|---|---|
| Koti- ja vierasjoukkue eivät saa olla sama | Ottelun omat kaksi kenttää | Entiteetti (`Match`) |
| Molempien joukkueiden pitää olla olemassa | Haku joukkueiden tallennuksesta | Use case |
| Pelinumeron pitää olla positiivinen | Pelkkä numero | Entiteetti tai value object |
| Pelinumero on joukkueen sisällä uniikki | Joukkueen muiden pelaajien numerot | Use case |

Use case näyttää silloin tältä: hae, tarkista se mikä vaatii haun, kutsu olion metodia, tallenna.

```csharp
public async Task ExecuteAsync(int homeTeamId, int awayTeamId)
{
    // Vaatii haun -> use case tarkistaa
    if (await _teams.GetByIdAsync(homeTeamId) == null ||
        await _teams.GetByIdAsync(awayTeamId) == null)
        throw new ArgumentException("Joukkuetta ei löydy");

    // Koskee vain ottelun omaa dataa -> konstruktori tarkistaa
    Match match = new Match(homeTeamId, awayTeamId);

    await _matches.AddAsync(match);
}
```

**Repository ei päätä sääntöä.** Se hakee ja tallentaa. Jos repositoryssa on metodi, jonka nimi kuulostaa säännöltä (esimerkiksi `IsNumberTaken`), sääntö on valunut väärään paikkaan. Parempi on kysely, joka palauttaa dataa, ja päätös tehdään use casessa.

**Controller ei päätä sääntöä.** Se muuntaa pyynnön kutsuksi ja tuloksen statuskoodiksi.

Jos uniikkiussääntö koskee olioita, jotka kuuluvat samaan aggregaattiin (joukkue omistaa pelaajansa), aggregaatin juuri voi tarkistaa sen itse. Nyrkkisääntö pätee silloinkin: tarkistus on siellä, missä tarvittava data on.

### Ei entiteetti eikä value object

Kaikki mallin käsitteet eivät ole entiteettejä tai value objecteja. Kaksi tavallista tapausta:

**1. Pelkkä arvo jonkun toisen datassa**

Pelaajan pelinumero on `int`-kenttä `Player`-entiteetissä. Sillä ei ole identiteettiä, joten se ei ole entiteetti. Sille ei myöskään ole tehty omaa luokkaa, joten se ei ole value object. Se on vain entiteetin ominaisuus, ja entiteetti tarkistaa sen säännön (positiivinen).

**2. Laskettu näkymä**

Sarjataulukko lasketaan otteluiden tuloksista. Sitä ei tallenneta, eikä sillä ole omia sääntöjä tai identiteettiä. Se on **lukumalli** (read model): luokka, joka on tehty vain näyttämistä varten.

```csharp
// Application-kerros: lukumalli, ei entiteetti
public record StandingsRow(string TeamName, int Played, int Wins, int Draws, int Losses, int Points);
```

| Käsite | Mikä se on | Missä kerroksessa |
|---|---|---|
| Joukkue, ottelu | Entiteetti | Domain |
| Pelinumero | Entiteetin kenttä (`int`) | Domain, osana entiteettiä |
| Sarjataulukko | Lukumalli, lasketaan pyydettäessä | Application |

**Miksi lukumalli on Applicationissa?** Sarjataulukon laskeminen on käyttötapaus: "näytä sarjatilanne". Se lukee otteluita ja muodostaa niistä näkymän. Domainiin kuuluvat ne oliot, joilla on tila ja säännöt.

**Miksi sitä ei tallenneta?** Tallennettu taulukko olisi kopio tiedosta, joka on jo otteluissa. Kopio voi jäädä vanhaksi. Tallentaminen kannattaa vasta, jos laskeminen on mitatusti liian hidasta.

### Milloin value objectia ei kannata tehdä

Value objectia ei tehdä siksi, että DDD:ssä on sellaisia. Jokainen uusi luokka on lisää koodia, joka pitää lukea, testata ja kertoa tietokannalle.

Value object ansaitsee paikkansa, kun toinen näistä pätee:

- **Arvolla on omia sääntöjä**, jotka muuten toistuisivat monessa paikassa. Esimerkki: sähköpostiosoitteen muoto.
- **Arvossa on useita kenttiä, jotka kuuluvat yhteen.** Esimerkki: rahasumma ja valuutta, tai ottelun tulos (kotimaalit ja vierasmaalit).

| Arvo | Value object? | Perustelu |
|---|---|---|
| Rahasumma + valuutta | Kyllä | Kaksi kenttää kuuluu yhteen, ja laskusäännöt ovat omat |
| Ottelun tulos (2–1) | Usein kyllä | Kaksi kenttää kuuluu yhteen, ja voittaja päätellään niistä |
| Joukkueen nimi | Yleensä ei | Yksi `string`, yksi tarkistus entiteetin konstruktorissa riittää |
| Pelinumero | Yleensä ei | Yksi `int`, yksi tarkistus entiteetissä riittää |

Jos epäröit, aloita kentällä ja tarkistuksella entiteetissä. Tee value object vasta, kun sama tarkistus alkaa toistua toisessa paikassa.

---

## DDD ja arkkitehtuurit

DDD toimii erityisen hyvin tiettyjen arkkitehtuurimallien kanssa.

### DDD + Clean Architecture

**Täydellinen yhdistelmä!**

```
┌───────────────────────────────────────┐
│         Infrastructure Layer          │ ← Repositories, EF Core
│  ┌─────────────────────────────────┐  │
│  │      Application Layer          │  │ ← Use Cases, Commands
│  │  ┌───────────────────────────┐  │  │
│  │  │     Domain Layer          │  │  │ ← DDD: Entities, Value Objects
│  │  │  (DDD Building Blocks)    │  │  │    Aggregates, Domain Events
│  │  └───────────────────────────┘  │  │
│  └─────────────────────────────────┘  │
└───────────────────────────────────────┘
```

**Domain Layer sisältää:**
- ✅ Entities
- ✅ Value Objects
- ✅ Aggregates
- ✅ Domain Events
- ✅ Repository Interfaces
- ✅ Domain Services

**Application Layer:**
- ✅ Use Cases
- ✅ Commands/Queries
- ✅ Application Services

**Infrastructure Layer:**
- ✅ Repository Implementations
- ✅ EF Core DbContext
- ✅ External Services

**Katso käytännön esimerkki:** [DDD-Example.md](DDD-Example.md)

### DDD + Microservices

**Bounded Context per Microservice**

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ Order Service   │   │Customer Service │   │Inventory Service│
│                 │   │                 │   │                 │
│ Order Context   │   │Customer Context │   │Inventory Context│
│ (Bounded)       │   │ (Bounded)       │   │ (Bounded)       │
└─────────────────┘   └─────────────────┘   └─────────────────┘
        ↓                      ↓                      ↓
   Own Database         Own Database           Own Database
```

---

## Edut ja haitat

### Edut ✅

| Etu | Selitys |
|-----|---------|
| **Parempi kommunikaatio** | Kehittäjät ja domain-ekspertit puhuvat samaa kieltä |
| **Liiketoimintalogiikka keskiössä** | Teknologia on detail, domain on ydin |
| **Modulaarinen** | Bounded Contexts eristävät osia |
| **Testattava** | Domain-logiikka testattavissa ilman infraa |
| **Ylläpidettävä** | Selkeä rakenne, helppo ymmärtää |
| **Skaalautuva** | Bounded Contextit voivat olla microservicejä |

### Haitat ❌

| Haitta | Selitys |
|--------|---------|
| **Jyrkkä oppimiskäyrä** | Vaatii ymmärrystä monista konsepteista |
| **Ylimääräinen kompleksisuus** | Pienissä projekteissa "overkill" |
| **Vaatii domain-eksperttejä** | Ilman heitä vaikea saavuttaa täysi hyöty |
| **Enemmän koodia** | Entities, Value Objects, jne. lisäävät riviä |
| **Vaatii tiimityötä** | Yksin vaikea soveltaa täydellisesti |

---

## Milloin käyttää DDD:tä?

### ✅ Käytä DDD:tä kun:

**1. Kompleksinen domain**
```
Jos sovelluksessa on monimutkaisia liiketoimintasääntöjä
→ DDD auttaa organisoimaan logiikan
```

**2. Pitkäikäinen projekti**
```
Jos projekti elää vuosia
→ DDD:n rakenne maksaa itsensä takaisin
```

**3. Suuri tiimi**
```
Jos 10+ kehittäjää
→ Bounded Contexts auttavat jakamaan työtä
```

**4. Domain-ekspertit saatavilla**
```
Jos liiketoiminnan asiantuntijat voivat auttaa
→ Ubiquitous Language syntyy
```

**5. Core Domain**
```
Jos rakennat yrityksen ydintoimintoa
→ Investoi laatuun DDD:llä
```

### ❌ Älä käytä DDD:tä kun:

**1. Yksinkertainen CRUD**
```
Jos vain tallennat/luet dataa
→ Layered Architecture riittää
```

**2. Pieni projekti**
```
Jos 1-3 kehittäjää, < 6kk
→ DDD on liikaa
```

**3. Prototyyppi**
```
Jos nopea proof-of-concept
→ Pidä se yksinkertaisena
```

**4. Generic Subdomain**
```
Jos rakennat esim. email-palvelua
→ Käytä valmista kirjastoa
```

**5. Ei domain-eksperttejä**
```
Jos et pääse keskustelemaan liiketoiminnan kanssa
→ DDD:n täysi hyöty jää saavuttamatta
```

### Päätöksenteon matriisi

| Projektin koko | Domain-kompleksisuus | Suositus |
|----------------|----------------------|----------|
| Pieni | Yksinkertainen | ❌ Ei DDD (Layered) |
| Pieni | Kompleksinen | ⚠️ Tactical DDD (ei täysi DDD) |
| Suuri | Yksinkertainen | ⚠️ Clean Architecture |
| Suuri | Kompleksinen | ✅ Täysi DDD |

---

## Parhaat käytännöt

### 1. Aloita Ubiquitous Language:sta

```
1. Haastattele domain-eksperttejä
2. Dokumentoi keskeiset termit
3. Käytä samoja termejä koodissa
4. Päivitä sanastoa jatkuvasti
```

### 2. Tunnista Bounded Contextit

```
1. Etsi luonnolliset rajat domainissa
2. Jokaisella kontekstilla oma malli
3. Määrittele kontekstien väliset suhteet
4. Piirra Context Map
```

### 3. Pidä Aggregatet pieninä

```csharp
// ✅ Hyvä - Pieni Aggregate
Order + OrderItems

// ❌ Huono - Iso Aggregate
Order + OrderItems + Customer + Products + Inventory + ...
```

### 4. Käytä Value Objecteja, kun arvolla on omia sääntöjä

```csharp
// ❌ Huono: sähköpostin muoto ja summan valuutta pitää tarkistaa joka paikassa erikseen
public string Email { get; set; } // Ei validointia
public decimal Amount { get; set; } // Ei valuuttaa

// ✅ Hyvä: sääntö on yhdessä paikassa
public Email Email { get; private set; } // Validoitu Value Object
public Money Amount { get; private set; } // Summa ja valuutta yhdessä
```

Älä silti kääri jokaista `string`- ja `int`-kenttää omaan luokkaansa. Katso [Milloin value objectia ei kannata tehdä](#milloin-value-objectia-ei-kannata-tehdä).

### 5. Domain Events välittämään muutoksia

```csharp
// Kun Order submitted → lähetä email
public void Submit()
{
    Status = OrderStatus.Submitted;
    AddDomainEvent(new OrderSubmittedEvent(Id, CustomerId, TotalAmount)); // ← Event
}
```

### 6. Repository per Aggregate Root

```csharp
// ✅ Hyvä
IOrderRepository // Order on Aggregate Root
ICustomerRepository // Customer on Aggregate Root

// ❌ Huono
IOrderItemRepository // OrderItem ei ole Aggregate Root!
```

### 7. Testaa domain-logiikka

```csharp
[Fact]
public void Order_AddItem_IncreasesTotalAmount()
{
    // Arrange: ei tietokantaa eikä korvikkeita, pelkkä olio
    Order order = Order.CreateDraft(CustomerId.New());
    
    // Act
    order.AddItem(ProductId.New(), 2, new Money(10, "EUR"));
    
    // Assert
    Assert.Equal(new Money(20, "EUR"), order.TotalAmount);
}
```

---

## Yhteenveto

### Mitä opimme?

**Domain-Driven Design** on:
- 🎯 Lähestymistapa kompleksisten sovelluksien kehittämiseen
- 🗣️ Yhteinen kieli (Ubiquitous Language) kehittäjien ja liiketoiminnan välillä
- 🧩 Modulaarinen rakenne (Bounded Contexts)
- 🏗️ Rakennuspalikat (Entities, Value Objects, Aggregates, jne.)

### Keskeiset opit

1. **DDD ei ole arkkitehtuuri** - se on suunnittelufilosofia
2. **Domain on keskiössä** - teknologia on detail
3. **Bounded Context** - selkeät rajat eri osajärjestelmille
4. **Ubiquitous Language** - sama kieli koodissa ja liiketoiminnassa
5. **Tactical Design** - Entities, Value Objects, Aggregates
6. **Käytä DDD:tä vain kun tarvitset** - ei kaikkiin projekteihin

### Seuraavat askeleet

1. 📖 Lue käytännön esimerkki: **[DDD-Example.md](DDD-Example.md)**
2. 🏗️ Tutustu arkkitehtuureihin: **[Clean-Architecture.md](Clean-Architecture.md)**
3. 📚 Lue Eric Evansin "Domain-Driven Design" -kirja
4. 💻 Kokeile rakentaa pieni DDD-sovellus

### Hyödyllisiä linkkejä

**Kirjat:**
- "Domain-Driven Design" - Eric Evans (2003)
- "Implementing Domain-Driven Design" - Vaughn Vernon (2013)
- "Domain-Driven Design Distilled" - Vaughn Vernon (2016)

**Online-resurssit:**
- [DDD Community](https://dddcommunity.org/)
- [Microsoft: DDD in .NET](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/)
- [Martin Fowler: DDD](https://martinfowler.com/tags/domain%20driven%20design.html)

---

**Muista:** DDD on väline, ei päämäärä. Käytä sitä kun se tuo arvoa projektillesi! 🚀
