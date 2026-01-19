# Hexagonal Architecture (Ports and Adapters)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on Hexagonal Architecture?](#mikä-on-hexagonal-architecture)
3. [Portit ja Adapterit](#portit-ja-adapterit)
4. [Periaatteet](#periaatteet)
5. [Edut ja haitat](#edut-ja-haitat)
6. [Milloin käyttää?](#milloin-käyttää)
7. [Käytännön esimerkki](#käytännön-esimerkki)
8. [Parhaat käytännöt](#parhaat-käytännöt)
9. [Yhteenveto](#yhteenveto)

---

## Johdanto

Hexagonal Architecture (tai Ports and Adapters) on Alistair Cockburnin vuonna 2005 luoma arkkitehtuurimalli. Se on hyvin samankaltainen kuin Clean Architecture, mutta painottaa **portteja** ja **adaptereita** kommunikointitapana sovelluksen ytimen ja ulkomaailman välillä.

### Miksi "Hexagonal"?

Kuusikulmio (hexagon) ei ole pakollinen - se on vain symbolinen tapa näyttää että sovelluksella voi olla useita **portteja** (rajapintoja) eri suuntiin. Voit ajatella sitä kuin älykästä älypuhelinta, jossa on useita liitäntöjä: USB-C, kuulokeliitäntä, langaton lataus, jne.

---

## Mikä on Hexagonal Architecture?

Hexagonal Architecture erottaa sovelluksen **ytimen** (core logic) ja **ulkopuolella olevat järjestelmät** (database, UI, external APIs) käyttämällä **portteja** (ports) ja **adaptereita** (adapters).

### Rakenne

```
        ┌─────────────────┐
        │   Web UI        │
        │   (Adapter)     │
        └────────┬────────┘
                 │
          ┌──────▼──────┐
          │ Primary Port│ (Interface)
          └──────┬──────┘
                 │
    ┌────────────▼────────────┐
    │                         │
    │   Application Core      │  (Domain + Use Cases)
    │   (Business Logic)      │
    │                         │
    └────────────┬────────────┘
                 │
          ┌──────▼──────┐
          │Secondary Port│ (Interface)
          └──────┬──────┘
                 │
        ┌────────▼────────┐
        │   Database      │
        │   (Adapter)     │
        └─────────────────┘
```

---

## Portit ja Adapterit

### Port (Portti) - Rajapinta

**Port** on rajapinta (interface), joka määrittelee miten ulkomaailma kommunikoi sovelluksen ytimen kanssa.

**Kaksi tyyppiä:**

1. **Primary Ports (Driving Ports)** - "Ajava portti"
   - UI → Application
   - Sovellusta kutsutaan tämän portin kautta
   - Esim: `IOrderService`, `IUserService`

2. **Secondary Ports (Driven Ports)** - "Ajettu portti"
   - Application → Database/External Services
   - Sovellus kutsuu tätä porttia
   - Esim: `IOrderRepository`, `IEmailService`

### Adapter (Sovitin) - Konkreettinen toteutus

**Adapter** on konkreettinen toteutus portille. Se muuntaa ulkoisen järjestelmän kutsut portin mukaisiksi ja päinvastoin.

**Esimerkkejä:**
- `RestApiAdapter` - HTTP API
- `SqlServerAdapter` - SQL Server -tietokanta
- `SmtpEmailAdapter` - SMTP-sähköposti
- `RabbitMqAdapter` - RabbitMQ-viestijono

### Esimerkki

```csharp
// PRIMARY PORT (Sovellus tarjoaa)
public interface IUserService
{
    Task<User> RegisterUserAsync(string email, string name);
}

// PRIMARY ADAPTER (UI käyttää)
public class UserController : ControllerBase
{
    private readonly IUserService _userService;
    
    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterRequest request)
    {
        User user = await _userService.RegisterUserAsync(request.Email, request.Name);
        return Ok(user);
    }
}

// SECONDARY PORT (Sovellus tarvitsee)
public interface IUserRepository
{
    Task<int> AddAsync(User user);
    Task<User?> GetByEmailAsync(string email);
}

// SECONDARY ADAPTER (Tietokanta toteuttaa)
public class SqlUserRepository : IUserRepository
{
    private readonly DbContext _context;
    
    public async Task<int> AddAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user.Id;
    }
}
```

---

## Periaatteet

### 1. Dependency Inversion

**Sovelluksen ydin määrittelee rajapinnat (portit), ulkoiset adapterit toteuttavat ne.**

```csharp
// ✅ Hyvä: Core määrittelee portin
// Core/Ports/IEmailService.cs
public interface IEmailService
{
    Task SendWelcomeEmailAsync(string email, string name);
}

// Infrastructure toteuttaa adapterin
// Infrastructure/Adapters/SmtpEmailAdapter.cs
public class SmtpEmailAdapter : IEmailService
{
    public async Task SendWelcomeEmailAsync(string email, string name)
    {
        // SMTP logic
    }
}
```

### 2. Testattavuus

Ydin voidaan testata ilman ulkoisia riippuvuuksia:

```csharp
[Fact]
public async Task RegisterUser_SendsWelcomeEmail()
{
    // Arrange - Mock adapter
    Mock<IUserRepository> mockRepo = new Mock<IUserRepository>();
    Mock<IEmailService> mockEmail = new Mock<IEmailService>();
    
    UserService service = new UserService(mockRepo.Object, mockEmail.Object);
    
    // Act
    await service.RegisterUserAsync("test@example.com", "John");
    
    // Assert
    mockEmail.Verify(e => e.SendWelcomeEmailAsync("test@example.com", "John"), Times.Once);
}
```

### 3. Teknologiariippumattomuus

Voit vaihtaa adapterin ilman ytimen muutoksia:

```csharp
// Program.cs - Development
builder.Services.AddScoped<IEmailService, MockEmailAdapter>();

// Program.cs - Production
builder.Services.AddScoped<IEmailService, SmtpEmailAdapter>();

// Tai myöhemmin
builder.Services.AddScoped<IEmailService, SendGridAdapter>();
```

---

## Edut ja haitat

### Edut

✅ **Erittäin testattava**
- Ydin testattavissa ilman ulkoisia riippuvuuksia
- Adapterit voidaan korvata mock:eilla

✅ **Ulkoiset järjestelmät helppo vaihtaa**
- Vaihda tietokanta (SQL → PostgreSQL → MongoDB)
- Vaihda email-palvelu (SMTP → SendGrid)
- Vaihda UI (REST API → GraphQL → gRPC)

✅ **Selkeä erottelu business logic vs. infrastructure**
- Sovelluksen ydin ei tiedä mistään infrastruktuurista
- Infrastruktuuri ei sisällä liiketoimintalogiikkaa

✅ **Voidaan kehittää useita adaptereita rinnakkain**
- Eri tiimit voivat työskennellä eri adaptereissa
- Esim: Web UI, Mobile API, CLI samanaikaisesti

✅ **Helppo integroida uusia järjestelmiä**
- Luo uusi adapter, ei muuta ytimen koodia

### Haitat

❌ **Vaatii enemmän rajapintoja**
- Jokaiselle ulkoiselle järjestelmälle oma portti
- Enemmän koodia ylläpidettävänä

❌ **Alkuun monimutkaisempi pienissä projekteissa**
- Yliinsinööriä yksinkertaisille sovelluksille
- TODO-lista ei tarvitse Hexagonal Architecture:a

❌ **Mappausta tarvitaan eri kerroksien välillä**
- Domain models ↔ DTOs ↔ Database entities
- AutoMapper tai manuaalinen mappaus

❌ **Vaatii tiimiltä ymmärrystä**
- Kaikki pitää ymmärtää portit ja adapterit
- Vaatii kurinalaisuutta

---

## Milloin käyttää?

### ✅ Käytä kun:

- **Sovelluksessa on useita ulkoisia integraatioita**
  - Email, SMS, payment gateways, external APIs

- **Teknologia voi vaihtua**
  - Tietokanta, message broker, email-palvelu

- **Mikropalveluarkkitehtuuri**
  - Jokainen palvelu on oma hexagoni

- **Sovellus vaatii korkeaa testattavuutta**
  - Ydin pitää olla helposti testattavissa

- **Useita UI-rajapintoja**
  - Web, Mobile, CLI, GraphQL

### ❌ Älä käytä kun:

- **Pieni sovellus** (alle 5 kehittäjää)
- **Yksinkertainen CRUD-sovellus**
- **Nopea prototyyppi**
- **Ei ulkoisia integraatioita**

---

## Käytännön esimerkki

Toteutetaan käyttäjähallintajärjestelmä Hexagonal Architecture -mallilla.

### Projektirakenne

```
UserManagement/
├── UserManagement.Core/            (Application Core)
│   ├── Domain/
│   │   └── User.cs
│   ├── Ports/
│   │   ├── Primary/
│   │   │   └── IUserService.cs
│   │   └── Secondary/
│   │       ├── IUserRepository.cs
│   │       └── IEmailService.cs
│   └── Services/
│       └── UserService.cs
├── UserManagement.Adapters.Web/    (Primary Adapter)
│   ├── Controllers/
│   │   └── UserController.cs
│   └── Program.cs
├── UserManagement.Adapters.Database/ (Secondary Adapter)
│   ├── SqlUserRepository.cs
│   └── ApplicationDbContext.cs
└── UserManagement.Adapters.Email/  (Secondary Adapter)
    ├── SmtpEmailAdapter.cs
    └── SendGridEmailAdapter.cs
```

### 1. Core (Application Core)

**Core/Domain/User.cs:**

```csharp
namespace UserManagement.Core.Domain;

public class User
{
    public int Id { get; set; }
    public string Email { get; set; }
    public string Name { get; set; }
    public bool IsActive { get; set; }
    public DateTime RegisteredDate { get; set; }

    // Domain logic
    public void Activate()
    {
        if (IsActive)
            throw new InvalidOperationException("Käyttäjä on jo aktivoitu");
        
        IsActive = true;
    }

    public void Deactivate()
    {
        if (!IsActive)
            throw new InvalidOperationException("Käyttäjä ei ole aktiivinen");
        
        IsActive = false;
    }

    public bool CanLogin()
    {
        return IsActive;
    }
}
```

**Core/Ports/Primary/IUserService.cs (Primary Port):**

```csharp
using UserManagement.Core.Domain;

namespace UserManagement.Core.Ports.Primary;

// PRIMARY PORT - Sovellusta kutsutaan tämän portin kautta
public interface IUserService
{
    Task<User?> GetUserAsync(int id);
    Task<User?> GetUserByEmailAsync(string email);
    Task<User> RegisterUserAsync(string email, string name);
    Task ActivateUserAsync(int userId);
    Task DeactivateUserAsync(int userId);
    Task<bool> ChangeEmailAsync(int userId, string newEmail);
}
```

**Core/Ports/Secondary/IUserRepository.cs (Secondary Port):**

```csharp
using UserManagement.Core.Domain;

namespace UserManagement.Core.Ports.Secondary;

// SECONDARY PORT - Sovellus kutsuu tätä porttia
public interface IUserRepository
{
    Task<User?> GetByIdAsync(int id);
    Task<User?> GetByEmailAsync(string email);
    Task<int> AddAsync(User user);
    Task UpdateAsync(User user);
    Task DeleteAsync(int id);
    Task<bool> ExistsAsync(int id);
}
```

**Core/Ports/Secondary/IEmailService.cs (Secondary Port):**

```csharp
namespace UserManagement.Core.Ports.Secondary;

// SECONDARY PORT - Sovellus kutsuu tätä porttia
public interface IEmailService
{
    Task SendWelcomeEmailAsync(string email, string name);
    Task SendActivationEmailAsync(string email);
    Task SendEmailChangeConfirmationAsync(string email, string newEmail);
}
```

**Core/Services/UserService.cs:**

```csharp
using UserManagement.Core.Domain;
using UserManagement.Core.Ports.Primary;
using UserManagement.Core.Ports.Secondary;

namespace UserManagement.Core.Services;

public class UserService : IUserService
{
    private readonly IUserRepository _userRepository;
    private readonly IEmailService _emailService;

    public UserService(IUserRepository userRepository, IEmailService emailService)
    {
        _userRepository = userRepository;
        _emailService = emailService;
    }

    public async Task<User?> GetUserAsync(int id)
    {
        return await _userRepository.GetByIdAsync(id);
    }

    public async Task<User?> GetUserByEmailAsync(string email)
    {
        return await _userRepository.GetByEmailAsync(email);
    }

    public async Task<User> RegisterUserAsync(string email, string name)
    {
        // Validointi
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Sähköposti on pakollinen");

        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Nimi on pakollinen");

        // Tarkista että käyttäjä ei ole jo olemassa
        User? existingUser = await _userRepository.GetByEmailAsync(email);
        if (existingUser != null)
            throw new InvalidOperationException("Käyttäjä on jo rekisteröity");

        // Luo uusi käyttäjä (domain entity)
        User user = new User
        {
            Email = email,
            Name = name,
            IsActive = false,
            RegisteredDate = DateTime.UtcNow
        };

        // Tallenna (Secondary Port)
        int userId = await _userRepository.AddAsync(user);
        user.Id = userId;

        // Lähetä tervetuloviesti (Secondary Port)
        await _emailService.SendWelcomeEmailAsync(email, name);

        return user;
    }

    public async Task ActivateUserAsync(int userId)
    {
        User? user = await _userRepository.GetByIdAsync(userId);
        
        if (user == null)
            throw new ArgumentException("Käyttäjää ei löydy");

        // Domain logic
        user.Activate();

        // Tallenna
        await _userRepository.UpdateAsync(user);

        // Lähetä aktivointivahvistus
        await _emailService.SendActivationEmailAsync(user.Email);
    }

    public async Task DeactivateUserAsync(int userId)
    {
        User? user = await _userRepository.GetByIdAsync(userId);
        
        if (user == null)
            throw new ArgumentException("Käyttäjää ei löydy");

        // Domain logic
        user.Deactivate();

        // Tallenna
        await _userRepository.UpdateAsync(user);
    }

    public async Task<bool> ChangeEmailAsync(int userId, string newEmail)
    {
        if (string.IsNullOrWhiteSpace(newEmail))
            throw new ArgumentException("Sähköposti on pakollinen");

        User? user = await _userRepository.GetByIdAsync(userId);
        
        if (user == null)
            return false;

        // Tarkista että uusi email ei ole käytössä
        User? existingUser = await _userRepository.GetByEmailAsync(newEmail);
        if (existingUser != null && existingUser.Id != userId)
            throw new InvalidOperationException("Sähköposti on jo käytössä");

        string oldEmail = user.Email;
        user.Email = newEmail;

        // Tallenna
        await _userRepository.UpdateAsync(user);

        // Lähetä vahvistus
        await _emailService.SendEmailChangeConfirmationAsync(oldEmail, newEmail);

        return true;
    }
}
```

### 2. Primary Adapter (Web API)

**Adapters.Web/Controllers/UserController.cs:**

```csharp
using Microsoft.AspNetCore.Mvc;
using UserManagement.Core.Domain;
using UserManagement.Core.Ports.Primary;

namespace UserManagement.Adapters.Web.Controllers;

[ApiController]
[Route("api/[controller]")]
public class UserController : ControllerBase
{
    private readonly IUserService _userService;

    public UserController(IUserService userService)
    {
        _userService = userService;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<User>> GetUser(int id)
    {
        User? user = await _userService.GetUserAsync(id);
        
        if (user == null)
            return NotFound();

        return Ok(user);
    }

    [HttpGet("by-email/{email}")]
    public async Task<ActionResult<User>> GetUserByEmail(string email)
    {
        User? user = await _userService.GetUserByEmailAsync(email);
        
        if (user == null)
            return NotFound();

        return Ok(user);
    }

    [HttpPost("register")]
    public async Task<ActionResult<User>> Register([FromBody] RegisterRequest request)
    {
        try
        {
            User user = await _userService.RegisterUserAsync(request.Email, request.Name);
            return CreatedAtAction(nameof(GetUser), new { id = user.Id }, user);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            return Conflict(ex.Message);
        }
    }

    [HttpPost("{id}/activate")]
    public async Task<IActionResult> Activate(int id)
    {
        try
        {
            await _userService.ActivateUserAsync(id);
            return Ok();
        }
        catch (ArgumentException ex)
        {
            return NotFound(ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpPost("{id}/deactivate")]
    public async Task<IActionResult> Deactivate(int id)
    {
        try
        {
            await _userService.DeactivateUserAsync(id);
            return Ok();
        }
        catch (ArgumentException ex)
        {
            return NotFound(ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            return BadRequest(ex.Message);
        }
    }

    [HttpPut("{id}/email")]
    public async Task<IActionResult> ChangeEmail(int id, [FromBody] ChangeEmailRequest request)
    {
        try
        {
            bool success = await _userService.ChangeEmailAsync(id, request.NewEmail);
            
            if (!success)
                return NotFound();

            return Ok();
        }
        catch (ArgumentException ex)
        {
            return BadRequest(ex.Message);
        }
        catch (InvalidOperationException ex)
        {
            return Conflict(ex.Message);
        }
    }
}

public class RegisterRequest
{
    public string Email { get; set; }
    public string Name { get; set; }
}

public class ChangeEmailRequest
{
    public string NewEmail { get; set; }
}
```

**Adapters.Web/Program.cs:**

```csharp
using UserManagement.Core.Ports.Primary;
using UserManagement.Core.Ports.Secondary;
using UserManagement.Core.Services;
using UserManagement.Adapters.Database;
using UserManagement.Adapters.Email;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// Core Services (Primary Port implementation)
builder.Services.AddScoped<IUserService, UserService>();

// Secondary Adapters
builder.Services.AddScoped<IUserRepository, SqlUserRepository>();

// Email adapter - valitse ympäristön mukaan
if (builder.Environment.IsDevelopment())
{
    builder.Services.AddScoped<IEmailService, MockEmailAdapter>();
}
else
{
    builder.Services.AddScoped<IEmailService, SendGridEmailAdapter>();
}

WebApplication app = builder.Build();

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

### 3. Secondary Adapter (Database)

**Adapters.Database/SqlUserRepository.cs:**

```csharp
using Microsoft.EntityFrameworkCore;
using UserManagement.Core.Domain;
using UserManagement.Core.Ports.Secondary;

namespace UserManagement.Adapters.Database;

public class SqlUserRepository : IUserRepository
{
    private readonly ApplicationDbContext _context;

    public SqlUserRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<User?> GetByIdAsync(int id)
    {
        return await _context.Users.FindAsync(id);
    }

    public async Task<User?> GetByEmailAsync(string email)
    {
        return await _context.Users
            .FirstOrDefaultAsync(u => u.Email == email);
    }

    public async Task<int> AddAsync(User user)
    {
        _context.Users.Add(user);
        await _context.SaveChangesAsync();
        return user.Id;
    }

    public async Task UpdateAsync(User user)
    {
        _context.Users.Update(user);
        await _context.SaveChangesAsync();
    }

    public async Task DeleteAsync(int id)
    {
        User? user = await GetByIdAsync(id);
        if (user != null)
        {
            _context.Users.Remove(user);
            await _context.SaveChangesAsync();
        }
    }

    public async Task<bool> ExistsAsync(int id)
    {
        return await _context.Users.AnyAsync(u => u.Id == id);
    }
}
```

### 4. Secondary Adapter (Email)

**Adapters.Email/SmtpEmailAdapter.cs:**

```csharp
using System.Net.Mail;
using UserManagement.Core.Ports.Secondary;

namespace UserManagement.Adapters.Email;

public class SmtpEmailAdapter : IEmailService
{
    private readonly string _smtpServer;
    private readonly int _smtpPort;
    private readonly string _fromEmail;

    public SmtpEmailAdapter(string smtpServer, int smtpPort, string fromEmail)
    {
        _smtpServer = smtpServer;
        _smtpPort = smtpPort;
        _fromEmail = fromEmail;
    }

    public async Task SendWelcomeEmailAsync(string email, string name)
    {
        string subject = "Tervetuloa!";
        string body = $"Hei {name},\n\nTervetuloa palveluumme!\n\nYstävällisin terveisin,\nTiimi";
        
        await SendEmailAsync(email, subject, body);
    }

    public async Task SendActivationEmailAsync(string email)
    {
        string subject = "Tilisi on aktivoitu";
        string body = "Tilisi on nyt aktivoitu. Voit nyt kirjautua sisään.";
        
        await SendEmailAsync(email, subject, body);
    }

    public async Task SendEmailChangeConfirmationAsync(string email, string newEmail)
    {
        string subject = "Sähköpostiosoite vaihdettu";
        string body = $"Sähköpostiosoitteesi on vaihdettu.\n\nVanha: {email}\nUusi: {newEmail}";
        
        await SendEmailAsync(newEmail, subject, body);
    }

    private async Task SendEmailAsync(string to, string subject, string body)
    {
        using SmtpClient client = new SmtpClient(_smtpServer, _smtpPort);
        client.EnableSsl = true;
        
        MailMessage message = new MailMessage(_fromEmail, to, subject, body);
        
        await client.SendMailAsync(message);
    }
}
```

**Adapters.Email/SendGridEmailAdapter.cs:**

```csharp
using SendGrid;
using SendGrid.Helpers.Mail;
using UserManagement.Core.Ports.Secondary;

namespace UserManagement.Adapters.Email;

public class SendGridEmailAdapter : IEmailService
{
    private readonly string _apiKey;
    private readonly string _fromEmail;

    public SendGridEmailAdapter(string apiKey, string fromEmail)
    {
        _apiKey = apiKey;
        _fromEmail = fromEmail;
    }

    public async Task SendWelcomeEmailAsync(string email, string name)
    {
        string subject = "Tervetuloa!";
        string body = $"Hei {name}, tervetuloa palveluumme!";
        
        await SendEmailAsync(email, subject, body);
    }

    public async Task SendActivationEmailAsync(string email)
    {
        string subject = "Tilisi on aktivoitu";
        string body = "Tilisi on nyt aktivoitu.";
        
        await SendEmailAsync(email, subject, body);
    }

    public async Task SendEmailChangeConfirmationAsync(string email, string newEmail)
    {
        string subject = "Sähköpostiosoite vaihdettu";
        string body = $"Sähköpostiosoitteesi on vaihdettu: {newEmail}";
        
        await SendEmailAsync(newEmail, subject, body);
    }

    private async Task SendEmailAsync(string to, string subject, string body)
    {
        SendGridClient client = new SendGridClient(_apiKey);
        
        EmailAddress from = new EmailAddress(_fromEmail);
        EmailAddress toAddress = new EmailAddress(to);
        
        SendGridMessage msg = MailHelper.CreateSingleEmail(from, toAddress, subject, body, body);
        
        Response response = await client.SendEmailAsync(msg);
    }
}
```

**Adapters.Email/MockEmailAdapter.cs (Development):**

```csharp
using UserManagement.Core.Ports.Secondary;

namespace UserManagement.Adapters.Email;

public class MockEmailAdapter : IEmailService
{
    public Task SendWelcomeEmailAsync(string email, string name)
    {
        Console.WriteLine($"[MOCK EMAIL] Tervetuloviesti: {email} ({name})");
        return Task.CompletedTask;
    }

    public Task SendActivationEmailAsync(string email)
    {
        Console.WriteLine($"[MOCK EMAIL] Aktivointiviesti: {email}");
        return Task.CompletedTask;
    }

    public Task SendEmailChangeConfirmationAsync(string email, string newEmail)
    {
        Console.WriteLine($"[MOCK EMAIL] Email-muutosvahvistus: {email} → {newEmail}");
        return Task.CompletedTask;
    }
}
```

---

## Parhaat käytännöt

### 1. Portit Core-projektissa, Adapterit omissa projekteissaan

```csharp
// ✅ Hyvä struktuuri
UserManagement/
├── Core/                  (Portit täällä)
│   ├── Ports/
│   │   ├── Primary/
│   │   └── Secondary/
│   └── Services/
├── Adapters.Web/          (Primary Adapter)
├── Adapters.Database/     (Secondary Adapter)
└── Adapters.Email/        (Secondary Adapter)
```

### 2. Nimeä portit selkeästi

```csharp
// ✅ Hyvä: Selkeä nimeäminen
IUserService        // Primary Port (ulkomaailma kutsuu)
IUserRepository     // Secondary Port (sovellus kutsuu)
IEmailService       // Secondary Port (sovellus kutsuu)

// ❌ Huono: Epäselvä nimeäminen
IUserPort
IUserInterface
IUserAdapter
```

### 3. Adaptereita voi vaihtaa helposti

```csharp
// Program.cs
if (builder.Environment.IsDevelopment())
{
    builder.Services.AddScoped<IEmailService, MockEmailAdapter>();
}
else
{
    builder.Services.AddScoped<IEmailService, SendGridEmailAdapter>();
}

// Tai konfiguraation perusteella
string emailProvider = builder.Configuration["EmailProvider"];
switch (emailProvider)
{
    case "SMTP":
        builder.Services.AddScoped<IEmailService, SmtpEmailAdapter>();
        break;
    case "SendGrid":
        builder.Services.AddScoped<IEmailService, SendGridEmailAdapter>();
        break;
    case "Mock":
        builder.Services.AddScoped<IEmailService, MockEmailAdapter>();
        break;
}
```

### 4. Testaa Core erikseen adapterien kautta

```csharp
// Core testi (mock adapterit)
[Fact]
public async Task RegisterUser_SendsWelcomeEmail()
{
    // Arrange
    Mock<IUserRepository> mockRepo = new Mock<IUserRepository>();
    Mock<IEmailService> mockEmail = new Mock<IEmailService>();
    
    UserService service = new UserService(mockRepo.Object, mockEmail.Object);
    
    // Act
    await service.RegisterUserAsync("test@example.com", "John");
    
    // Assert
    mockEmail.Verify(e => e.SendWelcomeEmailAsync("test@example.com", "John"), Times.Once);
}

// Adapter testi (integration test)
[Fact]
public async Task SqlUserRepository_AddAsync_SavesUser()
{
    // Arrange
    DbContextOptions<ApplicationDbContext> options = new DbContextOptionsBuilder<ApplicationDbContext>()
        .UseInMemoryDatabase("TestDatabase")
        .Options;
    
    ApplicationDbContext context = new ApplicationDbContext(options);
    SqlUserRepository repository = new SqlUserRepository(context);
    
    User user = new User { Email = "test@example.com", Name = "John" };
    
    // Act
    int id = await repository.AddAsync(user);
    
    // Assert
    Assert.True(id > 0);
}
```

---

## Yhteenveto

### Hexagonal Architecture sopii kun:

✅ Sovelluksessa on useita ulkoisia integraatioita
✅ Teknologia voi vaihtua (tietokanta, email, jne.)
✅ Mikropalveluarkkitehtuuri
✅ Korkea testattavuus vaaditaan
✅ Useita UI-rajapintoja (Web, Mobile, CLI)

### Haasteet:

❌ Vaatii enemmän rajapintoja
❌ Monimutkaisempi pienissä projekteissa
❌ Mappausta tarvitaan

### Muista:

- **Core määrittelee portit**
- **Adapterit toteuttavat portit**
- **Riippuvuudet osoittavat kohti Core:a**
- **Testattavuus on avainasemassa**

---

## Seuraavaksi

- **[Clean Architecture](Clean-Architecture.md)** - Toinen näkökulma samaan asiaan
- **[Onion Architecture](Onion-Architecture.md)** - Sipulikerrokset
- **[Event-Driven Architecture](Event-Driven-Architecture.md)** - Event:eihin perustuva

### Hyödyllisiä linkkejä

- [Alistair Cockburn: Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/)
- [Netflix Tech Blog: Ready for changes with Hexagonal Architecture](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749)
