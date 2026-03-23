# Repository Pattern

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi Repository Pattern?](#miksi-repository-pattern)
3. [Perusrakenne](#perusrakenne)
4. [Generic Repository vs. Spesifi Repository](#generic-repository-vs-spesifi-repository)
5. [Repository Clean Architecturessa](#repository-clean-architecturessa)
6. [Unit of Work](#unit-of-work)
7. [Repository ja Unit Testing](#repository-ja-unit-testing)
8. [Best Practices](#best-practices)
9. [Anti-patterns](#anti-patterns)
10. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Repository Pattern** on suunnittelumalli, joka abstrahoi tietokantakäsittelyn rajapinnan (interface) taakse. Sovelluksen liiketoimintalogiikka ei tiedä mistä data tulee — tietokannasta, muistista, API:sta vai tiedostosta. Se tietää vain **mitä dataa** se pyytää.

**Perusidea:**

```
Ilman Repository Pattern:
Controller → DbContext.Products.Where(p => p.Price > 100).ToListAsync()
     ↓
Controller tuntee EF Core:n suoraan (tight coupling)

Repository Patternilla:
Controller → IProductRepository.GetExpensiveAsync(100)
     ↓
Controller tuntee vain rajapinnan (loose coupling)
```

Repository toimii **välittäjänä** (mediator) sovelluslogiikan ja tietokantateknologian välillä. Ajattele sitä "tietovarastona", jolta voit pyytää objekteja ilman tietoa siitä, miten ne on tallennettu.

---

## Miksi Repository Pattern?

### Ongelma: Suora EF Core -käyttö

```csharp
public class BookingController : ControllerBase
{
    private readonly AppDbContext _db;

    public BookingController(AppDbContext db)
    {
        _db = db;
    }

    [HttpGet]
    public async Task<ActionResult<List<Booking>>> GetAll()
    {
        // Controller tuntee EF Core:n, tietokantataulut ja kyselysyntaksin
        var bookings = await _db.Bookings
            .Include(b => b.Room)
            .Where(b => b.StartDate > DateTime.Today)
            .OrderBy(b => b.StartDate)
            .ToListAsync();

        return Ok(bookings);
    }
}
```

**Ongelmat:**

| Ongelma | Selitys |
|---------|---------|
| **Tight coupling** | Controller riippuu suoraan EF Core:sta ja `DbContext`:sta |
| **Ei testattava** | Yksikkötestissä tarvitaan oikea tietokanta tai monimutkainen In-Memory-konfiguraatio |
| **Toistuva koodi** | Sama `Include` + `Where` -ketju kopioidaan moneen paikkaan |
| **Teknologialukko** | EF Core:n vaihto toiseen ORM:iin vaatisi jokaisen controllerin muuttamista |
| **Liiketoimintalogiikka vuotaa** | Controller tietää miten dataa suodatetaan — ei sen tehtävä |

### Ratkaisu: Repository Pattern

```csharp
public class BookingController : ControllerBase
{
    private readonly IBookingRepository _bookingRepository;

    public BookingController(IBookingRepository bookingRepository)
    {
        _bookingRepository = bookingRepository;
    }

    [HttpGet]
    public async Task<ActionResult<List<Booking>>> GetAll()
    {
        // Controller ei tiedä EF Coresta mitään
        var bookings = await _bookingRepository.GetUpcomingAsync();
        return Ok(bookings);
    }
}
```

**Edut:**

- ✅ **Loose coupling** — Controller riippuu vain rajapinnasta
- ✅ **Testattava** — Repository voidaan mockata yksikkötesteissä
- ✅ **DRY** — Kyselylogiikka on yhdessä paikassa
- ✅ **Vaihdettavissa** — Tietokantateknologia voidaan vaihtaa ilman sovelluslogiikan muuttamista
- ✅ **Selkeä vastuu** — Repository vastaa datasta, Controller vastaa HTTP:stä

---

## Perusrakenne

### 1. Rajapinta (Interface)

Rajapinta määrittelee **mitä operaatioita** repository tarjoaa:

```csharp
public interface IBookingRepository
{
    Task<Booking?> GetByIdAsync(int id);
    Task<List<Booking>> GetAllAsync();
    Task<List<Booking>> GetUpcomingAsync();
    Task<List<Booking>> GetByRoomAsync(int roomId);
    Task<Booking> AddAsync(Booking booking);
    Task UpdateAsync(Booking booking);
    Task DeleteAsync(int id);
    Task<bool> HasOverlappingBookingAsync(int roomId, DateTime start, DateTime end);
}
```

### 2. Toteutus (Implementation)

Toteutus sisältää varsinaisen tietokantalogiikan:

```csharp
public class BookingRepository : IBookingRepository
{
    private readonly AppDbContext _db;

    public BookingRepository(AppDbContext db)
    {
        _db = db;
    }

    public async Task<Booking?> GetByIdAsync(int id)
    {
        return await _db.Bookings
            .Include(b => b.Room)
            .FirstOrDefaultAsync(b => b.Id == id);
    }

    public async Task<List<Booking>> GetAllAsync()
    {
        return await _db.Bookings
            .Include(b => b.Room)
            .OrderBy(b => b.StartDate)
            .ToListAsync();
    }

    public async Task<List<Booking>> GetUpcomingAsync()
    {
        return await _db.Bookings
            .Include(b => b.Room)
            .Where(b => b.StartDate > DateTime.Today)
            .OrderBy(b => b.StartDate)
            .ToListAsync();
    }

    public async Task<Booking> AddAsync(Booking booking)
    {
        _db.Bookings.Add(booking);
        await _db.SaveChangesAsync();
        return booking;
    }

    public async Task<bool> HasOverlappingBookingAsync(
        int roomId, DateTime start, DateTime end)
    {
        return await _db.Bookings.AnyAsync(b =>
            b.RoomId == roomId &&
            b.StartDate < end &&
            b.EndDate > start);
    }

    // ... muut metodit
}
```

### 3. DI-rekisteröinti

```csharp
// Program.cs
builder.Services.AddScoped<IBookingRepository, BookingRepository>();
```

`AddScoped` tarkoittaa, että jokaiselle HTTP-pyynnölle luodaan oma repository-instanssi — sama elinkaari kuin `DbContext`:lla.

---

## Generic Repository vs. Spesifi Repository

### Generic Repository

Generic Repository tarjoaa yleiset CRUD-operaatiot kaikille entiteeteille:

```csharp
public interface IRepository<T> where T : class
{
    Task<T?> GetByIdAsync(int id);
    Task<List<T>> GetAllAsync();
    Task<T> AddAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}
```

```csharp
public class Repository<T> : IRepository<T> where T : class
{
    protected readonly AppDbContext _db;
    protected readonly DbSet<T> _dbSet;

    public Repository(AppDbContext db)
    {
        _db = db;
        _dbSet = db.Set<T>();
    }

    public virtual async Task<T?> GetByIdAsync(int id)
    {
        return await _dbSet.FindAsync(id);
    }

    public virtual async Task<List<T>> GetAllAsync()
    {
        return await _dbSet.ToListAsync();
    }

    public virtual async Task<T> AddAsync(T entity)
    {
        _dbSet.Add(entity);
        await _db.SaveChangesAsync();
        return entity;
    }

    // ... muut metodit
}
```

### Spesifi Repository

Spesifi repository laajentaa geneeristä ja lisää entiteettikohtaisia metodeja:

```csharp
public interface IBookingRepository : IRepository<Booking>
{
    Task<List<Booking>> GetUpcomingAsync();
    Task<bool> HasOverlappingBookingAsync(int roomId, DateTime start, DateTime end);
}
```

```csharp
public class BookingRepository : Repository<Booking>, IBookingRepository
{
    public BookingRepository(AppDbContext db) : base(db) { }

    public async Task<List<Booking>> GetUpcomingAsync()
    {
        return await _dbSet
            .Include(b => b.Room)
            .Where(b => b.StartDate > DateTime.Today)
            .OrderBy(b => b.StartDate)
            .ToListAsync();
    }

    public async Task<bool> HasOverlappingBookingAsync(
        int roomId, DateTime start, DateTime end)
    {
        return await _dbSet.AnyAsync(b =>
            b.RoomId == roomId &&
            b.StartDate < end &&
            b.EndDate > start);
    }
}
```

### Vertailu

| Ominaisuus | Generic Repository | Spesifi Repository |
|-----------|-------------------|-------------------|
| Koodin toisto | Vähemmän (CRUD jaettu) | Enemmän |
| Kyselyjen tarkkuus | Rajoitettu | Täysin kontrolloitava |
| Monimutkaiset kyselyt | Hankala toteuttaa | Helppo toteuttaa |
| Clean Architecture | Rajapinta voi vuotaa teknologiaa | Rajapinta kuvaa domainia |
| Suositus | Pohjaluokkana (base class) | Julkinen rajapinta |

**Suositus:** Käytä geneeristä repositoryä **pohjaluokkana** (`Repository<T>`) ja spesifejä repositoryja **julkisena rajapintana** (`IBookingRepository`). Näin saat molemmat hyödyt.

---

## Repository Clean Architecturessa

Clean Architecturessa Repository Pattern noudattaa **Dependency Inversion Principleä (DIP)**:

```
┌─────────────────────────────────────────────────┐
│  Domain Layer                                   │
│  ┌───────────────────────────────────────────┐  │
│  │  IBookingRepository  (rajapinta)          │  │
│  │  Booking             (entiteetti)         │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
         ▲ riippuu (implements)
┌─────────────────────────────────────────────────┐
│  Infrastructure Layer                           │
│  ┌───────────────────────────────────────────┐  │
│  │  BookingRepository   (EF Core -toteutus)  │  │
│  │  AppDbContext                             │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Tärkeä sääntö:** Rajapinta (`IBookingRepository`) sijaitsee **Domain**- tai **Application**-kerroksessa. Toteutus (`BookingRepository`) sijaitsee **Infrastructure**-kerroksessa.

```
Domain/Interfaces/IBookingRepository.cs      ← Rajapinta
Infrastructure/Repositories/BookingRepository.cs  ← Toteutus
```

Tämä tarkoittaa, että **Domain ei riipu infrastruktuurista** — se ei tiedä EF Core:sta, SQL:stä tai mistään tietokantatekniikasta. Riippuvuus on käännetty ylösalaisin (DIP).

### Käytännön esimerkki: Use Case käyttää repositoryä

```csharp
// Application-kerroksessa
public class CreateBookingUseCase
{
    private readonly IBookingRepository _bookingRepository;
    private readonly IRoomRepository _roomRepository;

    public CreateBookingUseCase(
        IBookingRepository bookingRepository,
        IRoomRepository roomRepository)
    {
        _bookingRepository = bookingRepository;
        _roomRepository = roomRepository;
    }

    public async Task<Result<Booking>> ExecuteAsync(CreateBookingDto dto)
    {
        var room = await _roomRepository.GetByIdAsync(dto.RoomId);
        if (room is null)
            return Result<Booking>.Failure("Huonetta ei löydy");

        bool hasOverlap = await _bookingRepository
            .HasOverlappingBookingAsync(dto.RoomId, dto.StartDate, dto.EndDate);

        if (hasOverlap)
            return Result<Booking>.Failure("Huone on jo varattu kyseiselle ajalle");

        var booking = new Booking
        {
            RoomId = dto.RoomId,
            StartDate = dto.StartDate,
            EndDate = dto.EndDate
        };

        await _bookingRepository.AddAsync(booking);
        return Result<Booking>.Success(booking);
    }
}
```

---

## Unit of Work

**Unit of Work** -malli hallinnoi useiden repositoryjen muutosten tallentamista yhtenä transaktiona.

### Ongelma: Jokainen repository tallentaa erikseen

```csharp
// ❌ Kaksi erillistä SaveChangesAsync-kutsua
await _bookingRepository.AddAsync(booking);    // SaveChangesAsync() #1
await _paymentRepository.AddAsync(payment);    // SaveChangesAsync() #2
// Jos #2 epäonnistuu, #1 on jo tallennettu!
```

### Ratkaisu: Unit of Work

```csharp
public interface IUnitOfWork
{
    IBookingRepository Bookings { get; }
    IPaymentRepository Payments { get; }
    Task<int> SaveChangesAsync();
}
```

```csharp
public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _db;

    public UnitOfWork(AppDbContext db)
    {
        _db = db;
        Bookings = new BookingRepository(db);
        Payments = new PaymentRepository(db);
    }

    public IBookingRepository Bookings { get; }
    public IPaymentRepository Payments { get; }

    public async Task<int> SaveChangesAsync()
    {
        return await _db.SaveChangesAsync();
    }
}
```

```csharp
// ✅ Kaikki tallennetaan yhdessä transaktiossa
_unitOfWork.Bookings.Add(booking);
_unitOfWork.Payments.Add(payment);
await _unitOfWork.SaveChangesAsync();  // Molemmat tallentuvat tai kumpikaan ei
```

> **Huomio:** EF Core:n `DbContext` toimii itsessään jo Unit of Work -mallina. Erillinen UoW-abstraktio on hyödyllinen lähinnä silloin, kun haluat erottaa SaveChanges-kutsun repositoryista.

---

## Repository ja Unit Testing

Repository Pattern tekee yksikkötestauksesta helppoa, koska repository voidaan **mockata**:

### Use Casen testaaminen

```csharp
public class CreateBookingUseCaseTests
{
    [Fact]
    public async Task Execute_WhenRoomAvailable_ReturnsSuccess()
    {
        // Arrange
        var mockBookingRepo = new Mock<IBookingRepository>();
        var mockRoomRepo = new Mock<IRoomRepository>();

        mockRoomRepo
            .Setup(r => r.GetByIdAsync(1))
            .ReturnsAsync(new Room { Id = 1, Name = "Kokoushuone A" });

        mockBookingRepo
            .Setup(r => r.HasOverlappingBookingAsync(1, It.IsAny<DateTime>(), It.IsAny<DateTime>()))
            .ReturnsAsync(false);

        var useCase = new CreateBookingUseCase(
            mockBookingRepo.Object,
            mockRoomRepo.Object);

        // Act
        var result = await useCase.ExecuteAsync(new CreateBookingDto
        {
            RoomId = 1,
            StartDate = DateTime.Today.AddDays(1),
            EndDate = DateTime.Today.AddDays(2)
        });

        // Assert
        Assert.True(result.IsSuccess);
        mockBookingRepo.Verify(
            r => r.AddAsync(It.IsAny<Booking>()), Times.Once);
    }

    [Fact]
    public async Task Execute_WhenRoomHasOverlap_ReturnsFailure()
    {
        // Arrange
        var mockBookingRepo = new Mock<IBookingRepository>();
        var mockRoomRepo = new Mock<IRoomRepository>();

        mockRoomRepo
            .Setup(r => r.GetByIdAsync(1))
            .ReturnsAsync(new Room { Id = 1 });

        mockBookingRepo
            .Setup(r => r.HasOverlappingBookingAsync(1, It.IsAny<DateTime>(), It.IsAny<DateTime>()))
            .ReturnsAsync(true);  // Päällekkäinen varaus!

        var useCase = new CreateBookingUseCase(
            mockBookingRepo.Object,
            mockRoomRepo.Object);

        // Act
        var result = await useCase.ExecuteAsync(new CreateBookingDto
        {
            RoomId = 1,
            StartDate = DateTime.Today.AddDays(1),
            EndDate = DateTime.Today.AddDays(2)
        });

        // Assert
        Assert.False(result.IsSuccess);
        Assert.Equal("Huone on jo varattu kyseiselle ajalle", result.Error);
        mockBookingRepo.Verify(
            r => r.AddAsync(It.IsAny<Booking>()), Times.Never);
    }
}
```

**Ilman Repository Patternia** pitäisi testata DbContext:a suoraan — mikä vaatisi joko InMemory-tietokannan tai monimutkaisia mock-konfiguraatioita.

---

## Best Practices

### 1. Rajapinta kuvaa domainia, ei teknologiaa

```csharp
// ✅ Hyvä — domain-kielellä
Task<List<Booking>> GetUpcomingAsync();
Task<bool> HasOverlappingBookingAsync(int roomId, DateTime start, DateTime end);

// ❌ Huono — vuotaa teknologiaa
IQueryable<Booking> GetQueryable();
Task<List<Booking>> FindAsync(Expression<Func<Booking, bool>> predicate);
```

### 2. Palauta domain-olioita, ei EF Core -entiteettejä

```csharp
// ✅ Repository palauttaa domain-olion
Task<Booking?> GetByIdAsync(int id);

// ❌ Repository vuotaa EF Core -käsitteitä
Task<EntityEntry<Booking>> AddAsync(Booking booking);
```

### 3. Älä paljasta IQueryable

```csharp
// ❌ Vuotaa EF Core:n kyselykieli ulos
public IQueryable<Booking> GetAll()
{
    return _db.Bookings.AsQueryable();
}

// ✅ Repository tekee kyselyn valmiiksi
public async Task<List<Booking>> GetAllAsync()
{
    return await _db.Bookings.ToListAsync();
}
```

### 4. Yksi repository per aggregaatti

Domain-Driven Designissa jokainen **aggregaattijuuri** saa oman repositorynsa:

```csharp
// ✅ Booking on aggregaattijuuri
IBookingRepository

// ✅ Room on aggregaattijuuri
IRoomRepository

// ❌ BookingItem ei ole aggregaattijuuri — ei omaa repositorya
// BookingItemit haetaan Bookingin kautta
```

---

## Anti-patterns

### 1. "Leaking Abstraction" — IQueryable rajapinnassa

```csharp
// ❌ Kuka tahansa voi rakentaa mielivaltaisia kyselyitä
public interface IRepository<T>
{
    IQueryable<T> Query { get; }
}

// Tämä mitätöi Repository Patternin koko idean
var result = _repo.Query
    .Include(b => b.Room)
    .Where(b => b.StartDate > today)
    .ToListAsync();  // EF Core -riippuvuus vuotaa!
```

### 2. Liian geneerinen rajapinta

```csharp
// ❌ Kaikki operaatiot ovat yleisiä — ei domainkieltä
public interface IGenericRepository<T>
{
    Task<T?> FindAsync(Expression<Func<T, bool>> predicate);
    Task<List<T>> WhereAsync(Expression<Func<T, bool>> predicate);
}

// Käyttö ei kerro mitään liiketoiminnasta:
var bookings = await _repo.WhereAsync(b => b.StartDate > today && b.RoomId == 5);
```

### 3. Repository ilman rajapintaa

```csharp
// ❌ Konkreettinen luokka — ei voi mockata, ei DIP
public class BookingRepository
{
    private readonly AppDbContext _db;
    // ...
}

// ✅ Rajapinta + toteutus
public interface IBookingRepository { ... }
public class BookingRepository : IBookingRepository { ... }
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Repository Pattern** | Abstrahoi tietokantakäsittelyn rajapinnan taakse |
| **Interface** | Määrittelee mitä operaatioita on saatavilla (Domain/Application-kerroksessa) |
| **Implementation** | Sisältää EF Core -logiikan (Infrastructure-kerroksessa) |
| **Generic Repository** | Yleiset CRUD-operaatiot pohjaluokkana |
| **Spesifi Repository** | Entiteettikohtaiset kyselyt domain-kielellä |
| **Unit of Work** | Hallinnoi useiden repositoryjen transaktioita |
| **DIP** | Riippuvuuden kääntö — Domain ei riipu infrastruktuurista |
| **Testattavuus** | Repository mockataan yksikkötesteissä |

**Muista:**
- Repository **abstrahoi** tietokantateknologian pois sovelluslogiikasta
- Rajapinta käyttää **domain-kieltä**, ei teknologiakieltä
- Clean Architecturessa rajapinta on **Domain/Application**-kerroksessa, toteutus **Infrastructure**-kerroksessa
- **Älä paljasta** `IQueryable` tai `Expression<Func<T, bool>>` rajapinnassa

---

## Hyödyllisiä linkkejä

- [Microsoft: Repository Pattern](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/infrastructure-persistence-layer-design#the-repository-pattern)
- [Microsoft: Unit of Work](https://learn.microsoft.com/en-us/aspnet/mvc/overview/older-versions/getting-started-with-ef-5-using-mvc-4/implementing-the-repository-and-unit-of-work-patterns-in-an-asp-net-mvc-application)
- [Clean Architecture -materiaali](../Architecture/Clean-Architecture.md)
- [Dependency Injection](../Dependency-Injection.md)
- [SOLID-periaatteet](../SOLID.md)
