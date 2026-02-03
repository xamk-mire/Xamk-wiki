# DTOs (Data Transfer Objects)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on DTO?](#mikä-on-dto)
3. [Miksi DTO:ita käytetään?](#miksi-dtoita-käytetään)
4. [Input vs Output DTOs](#input-vs-output-dtos)
5. [DTOs Clean Architecturessa](#dtos-clean-architecturessa)
6. [Mapping-strategiat](#mapping-strategiat)
7. [Best Practices](#best-practices)
8. [Anti-patterns](#anti-patterns)
9. [Yhteenveto](#yhteenveto)

---

## Johdanto

**DTO (Data Transfer Object)** on yksinkertainen olio, jonka ainoa tehtävä on siirtää dataa ohjelmiston kerrosten välillä. DTOs:t ovat keskeinen osa hyvin arkkitehtoitua sovellusta.

---

## Mikä on DTO?

### Määritelmä

**Data Transfer Object** on:
- Yksinkertainen data-container
- Ei liiketoimintalogiikkaa
- Käytetään datan siirtämiseen kerrosten välillä
- Tyypillisesti POJOs (Plain Old C# Objects)

### Esimerkki

```csharp
// DTO
public class CreateUserDto
{
    public string Username { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

// vs. Domain Entity
public class User
{
    public int Id { get; private set; }
    public string Username { get; private set; } = string.Empty;
    public string Email { get; private set; } = string.Empty;
    public string PasswordHash { get; private set; } = string.Empty;
    
    // Business logic
    public void ChangeEmail(string newEmail)
    {
        if (!IsValidEmail(newEmail))
            throw new ArgumentException("Invalid email");
        Email = newEmail;
    }
}
```

**Ero:**
- DTO = Vain data, ei logiikkaa
- Entity = Data + liiketoimintalogiikka

---

## Miksi DTO:ita käytetään?

### 1. Turvallisuus: Estää Over-posting

**Ongelma ilman DTO:ta:**

```csharp
// API ottaa vastaan Domain-entiteetin
[HttpPost]
public IActionResult Create([FromBody] User user) // ❌
{
    _context.Users.Add(user);
    _context.SaveChanges();
    return Ok();
}
```

**Käyttäjä voi lähettää:**
```json
{
  "username": "hacker",
  "email": "hacker@evil.com",
  "password": "123",
  "id": 999,              // ← Käyttäjä asettaa ID:n!
  "isAdmin": true         // ← Käyttäjä asettaa admin-oikeudet!
}
```

**Ratkaisu DTO:lla:**

```csharp
// API ottaa vastaan DTO:n
[HttpPost]
public IActionResult Create([FromBody] CreateUserDto dto) // ✅
{
    var user = new User
    {
        Username = dto.Username,
        Email = dto.Email,
        PasswordHash = HashPassword(dto.Password)
        // Id ja IsAdmin asetetaan järjestelmän toimesta!
    };
    _context.Users.Add(user);
    _context.SaveChanges();
    return Ok();
}
```

### 2. Separation of Concerns

**API contract erillään Domain-mallista:**

```csharp
// Domain voi muuttua...
public class Order
{
    public int Id { get; set; }
    public List<OrderItem> Items { get; set; }  // ← Navigation property
    public Money TotalAmount { get; set; }      // ← Value Object
    public OrderState State { get; set; }       // ← Complex state machine
}

// ...mutta API pysyy samana
public class OrderResponseDto
{
    public int Id { get; set; }
    public decimal Total { get; set; }          // ← Yksinkertainen decimal
    public string Status { get; set; }          // ← String
    public List<OrderItemDto> Items { get; set; }
}
```

### 3. Joustavuus: Eri näkymät samasta datasta

```csharp
// Input: Mitä käyttäjä lähettää
public class CreateProductDto
{
    public string Name { get; set; }
    public decimal Price { get; set; }
}

// Output: Mitä käyttäjä saa takaisin
public class ProductResponseDto
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public DateTime CreatedAt { get; set; }
    public string CreatedBy { get; set; }
}

// List view: Kevyempi versio listauksiin
public class ProductListItemDto
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
}
```

### 4. Optimointi: Vain tarvittava data

```csharp
// Frontend tarvitsee vain nimen ja hinnan
public class ProductSummaryDto
{
    public string Name { get; set; }
    public decimal Price { get; set; }
}

// vs. koko Entity Navigation Propertiesineen
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; }
    public decimal Price { get; set; }
    public Category Category { get; set; }        // ← Ei tarvita!
    public List<Review> Reviews { get; set; }     // ← Ei tarvita!
    public List<Image> Images { get; set; }       // ← Ei tarvita!
}
```

---

## Input vs Output DTOs

### Input DTOs (Command DTOs)

**Mitä käyttäjä lähettää:**

```csharp
// Create
public class CreateBookingDto
{
    public int ResourceId { get; set; }
    public string BookedBy { get; set; } = string.Empty;
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
    // Ei: Id, Status, CreatedAt
}

// Update
public class UpdateBookingDto
{
    public int Id { get; set; }  // ← Nyt tarvitaan Id
    public string BookedBy { get; set; } = string.Empty;
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
}
```

**Piirteet:**
- Vain muokattavat kentät
- Ei järjestelmän luomia kenttiä (Id, CreatedAt, jne.)
- Validointi (käytetään FluentValidation:ia)

### Output DTOs (Response DTOs)

**Mitä käyttäjä saa takaisin:**

```csharp
public class BookingResponseDto
{
    public int Id { get; set; }
    public int ResourceId { get; set; }
    public string ResourceName { get; set; } = string.Empty; // ← Johdettu tieto
    public string BookedBy { get; set; } = string.Empty;
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
    public string Status { get; set; } = string.Empty;
    public DateTime CreatedAt { get; set; }
}
```

**Piirteet:**
- Kaikki relevantit tiedot
- Voi sisältää johdettua dataa (esim. ResourceName)
- Enum:it usein stringeinä

---

## DTOs Clean Architecturessa

### Sijoittaminen

**Vaihtoehto 1: Application Layer** ← **Suositeltu**

```
BookingSystem.Application/
├── DTOs/
│   ├── Bookings/
│   │   ├── CreateBookingDto.cs
│   │   └── BookingResponseDto.cs
│   └── Resources/
│       ├── CreateResourceDto.cs
│       └── ResourceResponseDto.cs
└── UseCases/
    └── CreateBookingUseCase.cs  ← Käyttää DTOs:ia
```

**Vaihtoehto 2: Presentation Layer**

```
BookingSystem.API/
├── DTOs/
│   └── ...
└── Controllers/
    └── BookingsController.cs  ← Käyttää DTOs:ia
```

**Suositus:** Application Layer, koska:
- Use Cases voivat palauttaa DTO:ita
- Vähemmän mappingia
- DTO:t eivät ole UI-spesifejä

### Käyttö

```csharp
// Controller
[HttpPost]
public async Task<ActionResult<BookingResponseDto>> Create(
    [FromBody] CreateBookingDto dto)
{
    var result = await _createBookingUseCase.ExecuteAsync(dto);
    return Ok(result);
}

// Use Case
public class CreateBookingUseCase
{
    public async Task<BookingResponseDto> ExecuteAsync(CreateBookingDto dto)
    {
        // Map DTO → Domain
        var booking = new Booking
        {
            ResourceId = dto.ResourceId,
            BookedBy = dto.BookedBy,
            // ...
        };
        
        // Business logic...
        
        // Map Domain → DTO
        return new BookingResponseDto
        {
            Id = booking.Id,
            // ...
        };
    }
}
```

---

## Mapping-strategiat

### 1. Manuaalinen mapping

**Edut:**
- ✅ Eksplisiittinen kontrolli
- ✅ Ei ylimääräisiä riippuvuuksia
- ✅ Helppo debugata

**Haitat:**
- ❌ Enemmän koodia
- ❌ Toistoa

```csharp
var dto = new BookingResponseDto
{
    Id = booking.Id,
    ResourceId = booking.ResourceId,
    BookedBy = booking.BookedBy,
    StartTime = booking.StartTime,
    EndTime = booking.EndTime,
    Status = booking.Status.ToString(),
    CreatedAt = booking.CreatedAt
};
```

### 2. Extension methods

**Edut:**
- ✅ Uudelleenkäytettävä
- ✅ Fluent API
- ✅ Yksinkertainen

```csharp
public static class BookingMappingExtensions
{
    public static BookingResponseDto ToDto(this Booking booking)
    {
        return new BookingResponseDto
        {
            Id = booking.Id,
            ResourceId = booking.ResourceId,
            // ...
        };
    }
    
    public static Booking ToDomain(this CreateBookingDto dto)
    {
        return new Booking
        {
            ResourceId = dto.ResourceId,
            BookedBy = dto.BookedBy,
            // ...
        };
    }
}

// Käyttö
var dto = booking.ToDto();
var domain = createDto.ToDomain();
```

### 3. AutoMapper

**Edut:**
- ✅ Vähemmän koodia
- ✅ Convention-based mapping

**Haitat:**
- ❌ "Magic" (vaikea debugata)
- ❌ Performance-kustannus
- ❌ Ylimääräinen riippuvuus

```csharp
// Configuration
public class BookingMappingProfile : Profile
{
    public BookingMappingProfile()
    {
        CreateMap<Booking, BookingResponseDto>()
            .ForMember(dest => dest.Status, 
                opt => opt.MapFrom(src => src.Status.ToString()));
                
        CreateMap<CreateBookingDto, Booking>();
    }
}

// Usage
var dto = _mapper.Map<BookingResponseDto>(booking);
```

**Suositus:**
- Pienissä projekteissa: Manuaalinen tai Extension methods
- Suurissa projekteissa: AutoMapper (jos tarvitaan)

---

## Best Practices

### 1. Nimeä selkeästi

```csharp
// ✅ Hyvä
CreateBookingDto
UpdateBookingDto
BookingResponseDto
BookingListItemDto

// ❌ Huono
BookingDto      // Mikä DTO? Input vai Output?
BookingModel    // Sekoittuu Domain Model:iin
BookingRequest  // Epäselvä
```

### 2. Pidä DTOs yksinkertaisina

```csharp
// ✅ Hyvä - Vain data
public class CreateUserDto
{
    public string Username { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
}

// ❌ Huono - Logiikkaa DTO:ssa
public class CreateUserDto
{
    public string Username { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    
    public bool IsValid()  // ← Ei logiikkaa DTO:ssa!
    {
        return !string.IsNullOrEmpty(Username) && 
               Email.Contains("@");
    }
}
```

### 3. Käytä Data Annotations tai FluentValidation

```csharp
// Option 1: Data Annotations
public class CreateBookingDto
{
    [Required]
    public int ResourceId { get; set; }
    
    [Required]
    [MinLength(2)]
    public string BookedBy { get; set; } = string.Empty;
}

// Option 2: FluentValidation (suositellaan)
public class CreateBookingDtoValidator : AbstractValidator<CreateBookingDto>
{
    public CreateBookingDtoValidator()
    {
        RuleFor(x => x.ResourceId).GreaterThan(0);
        RuleFor(x => x.BookedBy).NotEmpty().MinimumLength(2);
        RuleFor(x => x.EndTime).GreaterThan(x => x.StartTime);
    }
}
```

### 4. Älä paljasta sisäisiä rakenteita

```csharp
// ❌ Huono - Paljastaa sisäisen rakenteen
public class OrderResponseDto
{
    public int Id { get; set; }
    public List<OrderItem> Items { get; set; }  // ← Domain Entity!
}

// ✅ Hyvä - Käyttää nested DTO:ta
public class OrderResponseDto
{
    public int Id { get; set; }
    public List<OrderItemDto> Items { get; set; }  // ← DTO
}

public class OrderItemDto
{
    public int ProductId { get; set; }
    public string ProductName { get; set; }
    public int Quantity { get; set; }
}
```

---

## Anti-patterns

### 1. Yksi DTO kaikille

```csharp
// ❌ Huono - Sama DTO:lle kaikelle
public class BookingDto
{
    public int? Id { get; set; }  // ← Nullable koska Create ei tarvitse
    public int ResourceId { get; set; }
    public string BookedBy { get; set; }
    public string? Status { get; set; }  // ← Nullable koska Create ei lähetä
    public DateTime? CreatedAt { get; set; }
}
```

**Ongelma:**
- Epäselvä mikä kenttä on pakollinen missäkin
- Nullable kaikkialla
- Vaikea validoida

**Ratkaisu:** Erilliset DTOs eri käyttötapauksille

### 2. DTO suoraan tietokantaan

```csharp
// ❌ Huono - DTO talletetaan suoraan
public async Task CreateAsync(CreateUserDto dto)
{
    await _context.Users.AddAsync(dto);  // ← DTO tietokantaan!
    await _context.SaveChangesAsync();
}
```

**Ongelma:**
- Sekoitat kerrokset
- Tight coupling
- Vaikea testata

**Ratkaisu:** Mappi DTO → Domain → Database

### 3. Liikaa logiikkaa DTO:ssa

```csharp
// ❌ Huono
public class BookingDto
{
    public DateTime StartTime { get; set; }
    public DateTime EndTime { get; set; }
    
    public TimeSpan Duration => EndTime - StartTime;  // ← Laskettu property OK
    
    public bool IsValid()  // ← Liikaa logiikkaa!
    {
        return EndTime > StartTime && 
               Duration.TotalHours <= 8;
    }
}
```

**Ratkaisu:** Validointi Domain:ssa tai FluentValidation:ssa

---

## Yhteenveto

### Keskeiset opit

**Mikä on DTO?**
- Yksinkertainen data-container
- Ei liiketoimintalogiikkaa
- Siirtää dataa kerrosten välillä

**Miksi käyttää?**
- ✅ Turvallisuus (estää over-posting)
- ✅ Separation of Concerns
- ✅ Joustavuus (eri Input/Output)
- ✅ Optimointi (vain tarvittava data)

**Best Practices:**
- Nimeä selkeästi (Create/Update/Response)
- Pidä yksinkertaisina
- Käytä FluentValidation:ia
- Erilliset DTOs eri käyttötapauksille

**Anti-patterns:**
- Älä käytä yhtä DTO:ta kaikkeen
- Älä tallenna DTO:ta suoraan
- Älä lisää logiikkaa DTO:hon

### Seuraavat askeleet

- Tutustu [Clean Architecture](Clean-Architecture.md)
- Kokeile [AutoMapper:ia](https://automapper.org/)
- Opi [FluentValidation](https://fluentvalidation.net/)

---

**Muista:** DTOs:t ovat väline, ei päämäärä. Käytä niitä kun ne tuovat arvoa!
