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
9. [Muotovirhe ja sääntövirhe](#muotovirhe-ja-sääntövirhe)
10. [Milloin DTO:ta ei tarvita](#milloin-dtota-ei-tarvita)
11. [Yhteenveto](#yhteenveto)

---

## Johdanto

**DTO (Data Transfer Object)** on yksinkertainen olio, jonka ainoa tehtävä on siirtää dataa ohjelmiston kerrosten välillä. DTOs:t ovat keskeinen osa hyvin arkkitehtoitua sovellusta.

Sama aihe Web API:n näkökulmasta, käytännön mapping-esimerkkien kanssa: [DTO:t ja Mapping](../WebAPI/DTOs-and-Mapping.md#miksi-entiteetti-ei-kelpaa-apin-rajapinnaksi).

---

## Mikä on DTO?

### Määritelmä

**Data Transfer Object** on:
- Yksinkertainen data-container
- Ei liiketoimintalogiikkaa
- Käytetään datan siirtämiseen kerrosten välillä
- Tyypillisesti POCO (Plain Old CLR Object) eli tavallinen C#-luokka ilman kehyksen kantaluokkia

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
    public bool IsAdmin { get; private set; }

    public User(string username, string email, string passwordHash)
    {
        Username = username;
        Email = email;
        PasswordHash = passwordHash;
    }
    
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

DTO ratkaisee kolme ongelmaa, jotka syntyvät, kun entiteetti kulkee sellaisenaan rajapinnan läpi.

**Tietovuoto.** Kun API palauttaa entiteetin, vastauksessa ovat kaikki sen kentät. Mukana on myös kenttiä, joita ei ollut tarkoitus näyttää, kuten `PasswordHash` tai sisäiset muistiinpanot. Jos entiteettiin lisätään myöhemmin uusi kenttä, se näkyy ulospäin heti, eikä kukaan tehnyt siitä päätöstä.

**Kytkentä.** Jos vastauksen muoto on sama kuin sisäinen malli, jokainen sisäinen muutos muuttaa myös rajapintaa. Kentän uudelleennimeäminen tai tyypin vaihtaminen rikkoo silloin asiakasohjelmat, esimerkiksi selainsovelluksen. DTO on rajapinnan oma muoto, joka pysyy samana, vaikka sisäinen malli muuttuu.

**Over-posting.** Kun API ottaa entiteetin vastaan sellaisenaan, käyttäjä voi lähettää myös kenttiä, joita hänen ei kuulu hallita, kuten `id` tai `isAdmin`. Sisään tuleva DTO sisältää vain ne kentät, jotka käyttäjä saa antaa. Muut kentät asettaa järjestelmä.

Alla sama asia esimerkkien kanssa.

### 1. Turvallisuus: Estää Over-posting

**Ongelma ilman DTO:ta:**

Moni entiteetti on kirjoitettu julkisilla settereillä. Oletetaan, että `User` näyttää tältä:

```csharp
public class User
{
    public int Id { get; set; }
    public string Username { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public bool IsAdmin { get; set; }
}
```

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
  "passwordHash": "abc",
  "id": 999,              // ← Käyttäjä asettaa ID:n!
  "isAdmin": true         // ← Käyttäjä asettaa admin-oikeudet!
}
```

Private setterit suojaavat tältä osittain, mutta entiteetti on silti väärä tyyppi rajapinnalle: sen muoto on sisäinen asia, ei lupaus asiakkaalle.

**Ratkaisu DTO:lla:**

```csharp
// API ottaa vastaan DTO:n
[HttpPost]
public IActionResult Create([FromBody] CreateUserDto dto) // ✅
{
    // Entiteetti luodaan konstruktorilla (ks. User-luokka sivun alussa).
    // DTO:ssa ei ole Id- eikä IsAdmin-kenttää, joten käyttäjä ei voi asettaa niitä.
    var user = new User(dto.Username, dto.Email, HashPassword(dto.Password));
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
- Muodon validointi rajalla (esim. Data Annotations tai FluentValidation). Liiketoimintasäännöt eivät kuulu tänne, ks. [Muotovirhe ja sääntövirhe](#muotovirhe-ja-sääntövirhe)

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

Ulos lähtevä DTO muotoillaan **näkymää varten**: siinä on se, mitä yksi sivu tai lista tarvitsee, ei entiteetin koko sisältöä. Siksi samasta entiteetistä voi olla useita lukumalleja, esimerkiksi kevyt listarivi ja tarkempi yksityiskohtanäkymä.

---

## DTOs Clean Architecturessa

### Sijoittaminen

DTO:t kuuluvat **Application-kerrokseen** tai pienessä projektissa **API-kerrokseen**. Tiimit tekevät tämän eri tavoin, ja molemmat ovat käytössä. Yksi sääntö on sama kaikissa: **Domain ei tunne DTO:ita.** Entiteetissä ei ole `ToDto()`-metodia eikä viittausta DTO-luokkiin, koska silloin sisin kerros riippuisi rajapinnan muodosta. Muunnos tehdään Applicationissa tai API:ssa.

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
- Suurissa projekteissa: mapping-kirjasto, jos käsin kirjoitettu mapping käy työlääksi

> **Lisenssi:** AutoMapper oli pitkään MIT-lisensoitu. Versiosta 15 (2025) alkaen se julkaistaan kaksoislisenssillä (RPL-1.5 tai kaupallinen lisenssi) ja vaatii lisenssiavaimen. Tarkista kirjaston voimassa olevat lisenssiehdot ennen käyttöönottoa.

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

DTO:n validaattori tarkistaa vain **muodon**: onko kenttä annettu ja onko se oikean muotoinen.

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
        RuleFor(x => x.StartTime).NotEmpty();   // Kenttä on annettu
        RuleFor(x => x.EndTime).NotEmpty();     // Kenttä on annettu
    }
}
```

Sääntö "loppuaika on alkuajan jälkeen" ei kuulu validaattoriin. Se on varauksen oma sääntö, joten se tarkistetaan domainissa: entiteetissä tai aikaväliä kuvaavassa value objectissa. Jos sääntö on vain validaattorissa, sen voi ohittaa luomalla varauksen muuta reittiä. Katso [Muotovirhe ja sääntövirhe](#muotovirhe-ja-sääntövirhe).

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

**Ratkaisu:** Erota kaksi eri tarkistusta:

- **Muototarkistus** (kenttä puuttuu, väärä tyyppi) tehdään rajalla, esimerkiksi Data Annotations- tai FluentValidation-validaattorissa.
- **Sääntötarkistus** (`EndTime > StartTime`, kesto enintään 8 tuntia) tehdään domainissa.

DTO:ssa itsessään ei ole kumpaakaan.

---

## Muotovirhe ja sääntövirhe

Syötteessä voi olla kahdenlaisia virheitä. Ne tarkistetaan eri paikoissa ja niihin vastataan eri statuskoodilla.

| | Muotovirhe | Sääntövirhe |
|---|-----------|-------------|
| **Mikä se on** | Syötteen muoto on väärä: kenttä puuttuu, tyyppi on väärä, päivämäärää ei voi lukea | Syöte on muodoltaan kunnossa, mutta se rikkoo liiketoimintasäännön |
| **Esimerkki** | `startTime` puuttuu | Tila on jo varattu samalle ajalle |
| **Missä tarkistetaan** | Rajalla (API): mallin sidonta ja DTO:n validaattori | Domainissa: entiteetti, value object tai use case |
| **Statuskoodi** | `400 Bad Request` | `409 Conflict` tai `422 Unprocessable Content` |

Miksi ero on tärkeä? Muototarkistus ei tarvitse tietoa järjestelmän tilasta, joten se voidaan tehdä heti rajalla. Sääntö kuuluu domainiin, koska sen pitää päteä aina, tuli pyyntö mistä tahansa: toisesta reitistä, taustatyöstä tai testistä.

**DTO:n validaattorissa ei saa olla liiketoimintasääntöjä.** Jos sääntö on vain validaattorissa, se on voimassa vain sillä yhdellä reitillä.

Valinnasta 409:n ja 422:n välillä ja siitä, miten sääntövirhe kulkee paluuarvona rajalle, kerrotaan sivulla [Result Pattern](../Patterns/Result-Pattern.md#missä-virhe-syntyy-ja-mikä-statuskoodi).

---

## Milloin DTO:ta ei tarvita

DTO on lisää koodia: luokka ja muunnos jokaiselle suunnalle. Joskus se ei maksa itseään takaisin.

- **Hyvin pieni sisäinen työkalu.** Käyttäjiä on muutama, rajapinnalla on yksi asiakas ja sama tiimi muuttaa molempia yhtä aikaa.
- **DTO olisi entiteetin tarkka kopio pysyvästi.** Jos luokassa ei ole piilotettavia kenttiä eikä sääntöjä, kopio ei suojaa miltään.

Oikotiellä on hinta, ja se kannattaa tietää etukäteen:

- Jokainen entiteettiin lisätty kenttä näkyy heti ulospäin.
- Sisäisen mallin muutos on samalla rajapinnan muutos.
- DTO:n lisääminen myöhemmin muuttaa rajapintaa, ja asiakkaat pitää päivittää samalla.

Jos rajapinnalla on ulkopuolisia käyttäjiä tai entiteetissä on yksikin kenttä, jota ei saa näyttää tai jota käyttäjä ei saa asettaa, käytä DTO:ta alusta asti.

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
- Tarkista muoto rajalla (Data Annotations tai FluentValidation), säännöt domainissa
- Erilliset DTOs eri käyttötapauksille
- Domain ei tunne DTO:ita

**Anti-patterns:**
- Älä käytä yhtä DTO:ta kaikkeen
- Älä tallenna DTO:ta suoraan
- Älä lisää logiikkaa DTO:hon

### Seuraavat askeleet

- Tutustu [Clean Architecture](Clean-Architecture.md)
- Lue [DTO:t ja Mapping](../WebAPI/DTOs-and-Mapping.md) - sama aihe Web API:n näkökulmasta
- Tutustu [AutoMapper:iin](https://automapper.io/) (tarkista lisenssi ennen käyttöönottoa)
- Opi [FluentValidation](https://fluentvalidation.net/)

---

**Muista:** DTOs:t ovat väline, ei päämäärä. Käytä niitä kun ne tuovat arvoa!
