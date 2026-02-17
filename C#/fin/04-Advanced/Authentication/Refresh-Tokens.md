# Refresh Tokens

## Sisällysluettelo

- [Mikä on Refresh Token?](#mikä-on-refresh-token)
- [Miksi Refresh Token tarvitaan?](#miksi-refresh-token-tarvitaan)
- [Access Token vs. Refresh Token](#access-token-vs-refresh-token)
- [Token Rotation](#token-rotation)
- [Tallennusvaihtoehdot](#tallennusvaihtoehdot)
- [Toteutus ASP.NET Coressa](#toteutus-aspnet-coressa)
  - [RefreshToken-entiteetti](#1-refreshtoken-entiteetti)
  - [DbContext](#2-dbcontext)
  - [TokenService laajennus](#3-tokenservice---refresh-tokenin-generointi)
  - [AuthController - Refresh-endpoint](#4-authcontroller---refresh-endpoint)
  - [Token Revocation](#5-token-revocation---tokenin-mitätöinti)
  - [Vanhojen tokenien siivous](#6-vanhojen-tokenien-siivous)
- [Koko flow yhteenveto](#koko-flow-yhteenveto)
- [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Mikä on Refresh Token?

**Refresh Token** on pitkäikäinen token, jota käytetään uuden **Access Tokenin** (JWT) hakemiseen ilman, että käyttäjän tarvitsee kirjautua uudelleen sisään.

```
Refresh Token on kuin avainkortti:
──────────────────────────────────
┌─────────────────────────────────────────┐
│  ACCESS TOKEN (JWT)                     │
│                                         │
│  Lyhytikäinen: 15 minuuttia             │  ← Kuin päiväpassi
│  Sisältää: käyttäjätiedot (claims)      │
│  Käyttö: jokaisessa API-pyynnössä       │
│  Tallennus: muisti / localStorage       │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  REFRESH TOKEN                          │
│                                         │
│  Pitkäikäinen: 7-30 päivää             │  ← Kuin avainkortti
│  Sisältää: satunnainen merkkijono       │
│  Käyttö: vain uuden Access Tokenin haku │
│  Tallennus: tietokanta (palvelin)       │
└─────────────────────────────────────────┘
```

---

## Miksi Refresh Token tarvitaan?

JWT (Access Token) on **tilaton** - palvelin ei voi mitätöidä sitä ennen kuin se vanhenee. Tämä luo ongelman:

```
Ongelma ilman Refresh Tokenia:
──────────────────────────────

Vaihtoehto A: Pitkä Access Token (esim. 24h)
  ✅ Käyttäjä ei joudu kirjautumaan usein
  ❌ Jos token varastetaan, hyökkääjällä on 24h aikaa
  ❌ Tokenia ei voi mitätöidä

Vaihtoehto B: Lyhyt Access Token (esim. 15min)
  ✅ Varastettu token on voimassa vain 15min
  ❌ Käyttäjä joutuu kirjautumaan joka 15. minuutti
  ❌ Huono käyttökokemus

Ratkaisu: Access Token + Refresh Token
  ✅ Lyhyt Access Token (15min) → turvallinen
  ✅ Refresh Token (7-30pv) → hyvä käyttökokemus
  ✅ Refresh Token voidaan mitätöidä tietokannasta
  ✅ Token Rotation havaitsee varkauden
```

---

## Access Token vs. Refresh Token

| Ominaisuus | Access Token (JWT) | Refresh Token |
|---|---|---|
| **Elinkaari** | Lyhyt (5-30 min) | Pitkä (7-30 päivää) |
| **Muoto** | JWT (Header.Payload.Signature) | Satunnainen merkkijono |
| **Sisältö** | Claims (käyttäjätiedot) | Ei sisällä käyttäjätietoja |
| **Tallennus (client)** | Muisti / localStorage | HTTP-only cookie (suositus) |
| **Tallennus (server)** | Ei tallenneta (tilaton) | Tietokanta |
| **Käyttö** | Jokaisessa API-pyynnössä | Vain Access Tokenin uusimisessa |
| **Mitätöinti** | Ei mahdollista (vanhenee itsestään) | Poistetaan/merkitään tietokannasta |
| **Lähetetään** | `Authorization: Bearer ...` -headerissa | POST-pyynnön bodyssa / cookiessa |

---

## Token Rotation

**Token Rotation** tarkoittaa, että joka kerta kun Refresh Tokenia käytetään, vanha Refresh Token mitätöidään ja uusi luodaan. Tämä parantaa turvallisuutta merkittävästi.

```
Token Rotation -prosessi:
─────────────────────────

1. Kirjautuminen
   Käyttäjä ──→ POST /login ──→ Palvelin
                                   │
                                   ├─ Luo Access Token (JWT)
                                   ├─ Luo Refresh Token (RT-1)
                                   └─ Tallenna RT-1 tietokantaan
                                   │
   Käyttäjä ←── { accessToken, refreshToken: RT-1 }

2. Access Token vanhenee (15 min)
   Käyttäjä ──→ POST /refresh { refreshToken: RT-1 } ──→ Palvelin
                                                            │
                                                            ├─ Validoi RT-1 tietokannasta
                                                            ├─ Mitätöi RT-1 (used = true)
                                                            ├─ Luo uusi Access Token
                                                            └─ Luo uusi Refresh Token (RT-2)
                                                            │
   Käyttäjä ←── { accessToken, refreshToken: RT-2 }

3. Jos hyökkääjä yrittää käyttää varastettua RT-1:
   Hyökkääjä ──→ POST /refresh { refreshToken: RT-1 } ──→ Palvelin
                                                             │
                                                             ├─ RT-1 on jo käytetty!
                                                             ├─ Mahdollinen varkaus havaittu
                                                             └─ Mitätöi KAIKKI käyttäjän tokenit
                                                             │
   Hyökkääjä ←── 401 Unauthorized
   Käyttäjä ←── (joutuu kirjautumaan uudelleen, mutta turvallisesti)
```

> 💡 **Token Rotation** on tärkeä turvallisuusmekanismi, koska se havaitsee Refresh Tokenin varkauden automaattisesti. Jos vanhaa, jo käytettyä tokenia yritetään käyttää, kaikki käyttäjän tokenit mitätöidään.

---

## Tallennusvaihtoehdot

### Palvelinpuoli (Refresh Token)

Refresh Token tallennetaan aina palvelimen tietokantaan:

| Vaihtoehto | Hyödyt | Haitat |
|---|---|---|
| **Relaatiotietokanta** (SQL Server, PostgreSQL) | Helppo toteuttaa, transaktiot | Hieman hitaampi |
| **Redis / In-Memory Cache** | Erittäin nopea, TTL-tuki | Monimutkaisempi infrastruktuuri |
| **Molemmat** | Nopea luku + pysyvä tallennus | Monimutkaisin |

### Asiakaspuoli (Client)

| Vaihtoehto | Turvallisuus | Kuvaus |
|---|---|---|
| **HTTP-only Cookie** | ✅ Paras | JavaScript ei pääse käsiksi, CSRF-suojaus tarvitaan |
| **Muisti (RAM)** | ✅ Hyvä | Katoaa sivun uudelleenlatauksen yhteydessä |
| **localStorage** | ❌ Heikompi | Altis XSS-hyökkäyksille, ei suositella Refresh Tokenille |

> ⚠️ **Suositus**: Tallenna Refresh Token **HTTP-only cookieen** tai **muistiin**. Älä tallenna sitä `localStorage`-muistiin.

---

## Toteutus ASP.NET Coressa

Tämä toteutus laajentaa [JWT.md](JWT.md)-materiaalin esimerkkejä.

### 1. RefreshToken-entiteetti

```csharp
// Entity Framework -entiteetti Refresh Tokenille
public class RefreshToken
{
    public int Id { get; set; }

    // Tokenin arvo (satunnainen merkkijono)
    public string Token { get; set; } = string.Empty;

    // Mihin käyttäjään token liittyy
    public int UserId { get; set; }
    public User User { get; set; } = null!;

    // Milloin token luotiin
    public DateTime Created { get; set; } = DateTime.UtcNow;

    // Milloin token vanhenee
    public DateTime Expires { get; set; }

    // Onko token käytetty (Token Rotation)
    public bool IsUsed { get; set; } = false;

    // Onko token mitätöity (esim. uloskirjautuminen)
    public bool IsRevoked { get; set; } = false;

    // Korvaavan tokenin arvo (jäljitettävyys)
    public string? ReplacedByToken { get; set; }

    // Apupropertyt
    public bool IsExpired => DateTime.UtcNow >= Expires;
    public bool IsActive => !IsUsed && !IsRevoked && !IsExpired;
}
```

### 2. DbContext

```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) 
        : base(options) { }

    public DbSet<User> Users { get; set; }
    public DbSet<RefreshToken> RefreshTokens { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // Refresh Token -konfiguraatio
        modelBuilder.Entity<RefreshToken>(entity =>
        {
            // Indeksi nopeaan hakuun tokenin arvolla
            entity.HasIndex(rt => rt.Token).IsUnique();

            // Relaatio: User -> RefreshTokens (1:N)
            entity.HasOne(rt => rt.User)
                  .WithMany()
                  .HasForeignKey(rt => rt.UserId)
                  .OnDelete(DeleteBehavior.Cascade);
        });
    }
}
```

### 3. TokenService - Refresh Tokenin generointi

```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

public interface ITokenService
{
    string GenerateAccessToken(User user);
    Task<RefreshToken> GenerateRefreshTokenAsync(User user);
    Task<(string AccessToken, RefreshToken RefreshToken)?> RefreshAsync(string refreshToken);
    Task RevokeTokenAsync(string refreshToken);
    Task RevokeAllUserTokensAsync(int userId);
}

public class TokenService : ITokenService
{
    private readonly JwtSettings _jwtSettings;
    private readonly AppDbContext _context;

    // Refresh Tokenin elinkaari (päiviä)
    private const int RefreshTokenExpirationDays = 7;

    public TokenService(
        IOptions<JwtSettings> jwtSettings,
        AppDbContext context)
    {
        _jwtSettings = jwtSettings.Value;
        _context = context;
    }

    // Access Token -generointi (sama kuin JWT.md:ssä)
    public string GenerateAccessToken(User user)
    {
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_jwtSettings.Secret));

        var credentials = new SigningCredentials(
            key, SecurityAlgorithms.HmacSha256);

        var claims = new List<Claim>
        {
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new Claim(ClaimTypes.Name, user.UserName),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role)
        };

        var token = new JwtSecurityToken(
            issuer: _jwtSettings.Issuer,
            audience: _jwtSettings.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_jwtSettings.ExpirationMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }

    // Refresh Token -generointi
    public async Task<RefreshToken> GenerateRefreshTokenAsync(User user)
    {
        var refreshToken = new RefreshToken
        {
            // Luo kryptografisesti turvallinen satunnainen merkkijono
            Token = GenerateSecureRandomString(),
            UserId = user.Id,
            Created = DateTime.UtcNow,
            Expires = DateTime.UtcNow.AddDays(RefreshTokenExpirationDays)
        };

        _context.RefreshTokens.Add(refreshToken);
        await _context.SaveChangesAsync();

        return refreshToken;
    }

    // Token Refresh -prosessi (Token Rotation)
    public async Task<(string AccessToken, RefreshToken RefreshToken)?> RefreshAsync(
        string refreshToken)
    {
        // 1. Hae Refresh Token tietokannasta
        var existingToken = await _context.RefreshTokens
            .Include(rt => rt.User)
            .FirstOrDefaultAsync(rt => rt.Token == refreshToken);

        // 2. Tarkista onko token olemassa
        if (existingToken is null)
        {
            return null;
        }

        // 3. Tarkista onko token jo käytetty (mahdollinen varkaus!)
        if (existingToken.IsUsed)
        {
            // Token Rotation: jo käytettyä tokenia yritetään käyttää
            // → Mitätöi KAIKKI käyttäjän tokenit turvallisuussyistä
            await RevokeAllUserTokensAsync(existingToken.UserId);
            return null;
        }

        // 4. Tarkista onko token mitätöity tai vanhentunut
        if (!existingToken.IsActive)
        {
            return null;
        }

        // 5. Merkitse vanha token käytetyksi (Token Rotation)
        existingToken.IsUsed = true;

        // 6. Luo uudet tokenit
        var user = existingToken.User;
        var newAccessToken = GenerateAccessToken(user);
        var newRefreshToken = new RefreshToken
        {
            Token = GenerateSecureRandomString(),
            UserId = user.Id,
            Created = DateTime.UtcNow,
            Expires = DateTime.UtcNow.AddDays(RefreshTokenExpirationDays)
        };

        // 7. Linkitä vanha token uuteen (jäljitettävyys)
        existingToken.ReplacedByToken = newRefreshToken.Token;

        // 8. Tallenna muutokset
        _context.RefreshTokens.Add(newRefreshToken);
        await _context.SaveChangesAsync();

        return (newAccessToken, newRefreshToken);
    }

    // Yksittäisen tokenin mitätöinti (esim. uloskirjautuminen)
    public async Task RevokeTokenAsync(string refreshToken)
    {
        var token = await _context.RefreshTokens
            .FirstOrDefaultAsync(rt => rt.Token == refreshToken);

        if (token is not null)
        {
            token.IsRevoked = true;
            await _context.SaveChangesAsync();
        }
    }

    // Kaikkien käyttäjän tokenien mitätöinti (turvallisuustoimenpide)
    public async Task RevokeAllUserTokensAsync(int userId)
    {
        var tokens = await _context.RefreshTokens
            .Where(rt => rt.UserId == userId && !rt.IsRevoked)
            .ToListAsync();

        foreach (var token in tokens)
        {
            token.IsRevoked = true;
        }

        await _context.SaveChangesAsync();
    }

    // Apumetodi: Luo turvallinen satunnainen merkkijono
    private static string GenerateSecureRandomString()
    {
        var randomBytes = new byte[64];
        using var rng = RandomNumberGenerator.Create();
        rng.GetBytes(randomBytes);
        return Convert.ToBase64String(randomBytes);
    }
}
```

### 4. AuthController - Refresh-endpoint

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly ITokenService _tokenService;
    private readonly AppDbContext _context;

    public AuthController(ITokenService tokenService, AppDbContext context)
    {
        _tokenService = tokenService;
        _context = context;
    }

    // Kirjautuminen - palauttaa Access Token + Refresh Token
    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginRequest request)
    {
        // Validoi käyttäjätunnukset (yksinkertaistettu esimerkki)
        var user = await ValidateCredentialsAsync(request.Email, request.Password);

        if (user is null)
        {
            return Unauthorized(new { message = "Virheellinen sähköposti tai salasana" });
        }

        // Generoi molemmat tokenit
        var accessToken = _tokenService.GenerateAccessToken(user);
        var refreshToken = await _tokenService.GenerateRefreshTokenAsync(user);

        return Ok(new AuthResponse
        {
            AccessToken = accessToken,
            RefreshToken = refreshToken.Token,
            AccessTokenExpiration = DateTime.UtcNow.AddMinutes(15)
        });
    }

    // Refresh - uusi Access Token vanhan Refresh Tokenin avulla
    [HttpPost("refresh")]
    public async Task<IActionResult> Refresh([FromBody] RefreshRequest request)
    {
        var result = await _tokenService.RefreshAsync(request.RefreshToken);

        if (result is null)
        {
            return Unauthorized(new { message = "Virheellinen tai vanhentunut refresh token" });
        }

        var (accessToken, refreshToken) = result.Value;

        return Ok(new AuthResponse
        {
            AccessToken = accessToken,
            RefreshToken = refreshToken.Token,
            AccessTokenExpiration = DateTime.UtcNow.AddMinutes(15)
        });
    }

    // Uloskirjautuminen - mitätöi Refresh Token
    [HttpPost("logout")]
    [Authorize]
    public async Task<IActionResult> Logout([FromBody] LogoutRequest request)
    {
        await _tokenService.RevokeTokenAsync(request.RefreshToken);
        return Ok(new { message = "Uloskirjautuminen onnistui" });
    }

    // Mitätöi kaikki sessiot (esim. "Kirjaudu ulos kaikista laitteista")
    [HttpPost("revoke-all")]
    [Authorize]
    public async Task<IActionResult> RevokeAll()
    {
        var userId = int.Parse(
            User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)!.Value);

        await _tokenService.RevokeAllUserTokensAsync(userId);
        return Ok(new { message = "Kaikki sessiot mitätöity" });
    }

    private async Task<User?> ValidateCredentialsAsync(string email, string password)
    {
        // TODO: Oikeassa sovelluksessa:
        // 1. Hae käyttäjä tietokannasta sähköpostin perusteella
        // 2. Vertaa salasanaa BCrypt.Verify() -metodilla
        // var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == email);
        // if (user != null && BCrypt.Net.BCrypt.Verify(password, user.PasswordHash))
        //     return user;
        // return null;

        if (email == "admin@example.com" && password == "salasana123")
        {
            return new User
            {
                Id = 1,
                UserName = "admin",
                Email = email,
                Role = "Admin"
            };
        }
        return null;
    }
}

// Request/Response-mallit
public class LoginRequest
{
    public string Email { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
}

public class RefreshRequest
{
    public string RefreshToken { get; set; } = string.Empty;
}

public class LogoutRequest
{
    public string RefreshToken { get; set; } = string.Empty;
}

public class AuthResponse
{
    public string AccessToken { get; set; } = string.Empty;
    public string RefreshToken { get; set; } = string.Empty;
    public DateTime AccessTokenExpiration { get; set; }
}
```

### 5. Token Revocation - Tokenin mitätöinti

Tokenien mitätöinti on tärkeää seuraavissa tilanteissa:

```
Milloin mitätöidä tokeneita:
────────────────────────────
1. Uloskirjautuminen
   → Mitätöi kyseinen Refresh Token

2. Salasanan vaihto
   → Mitätöi KAIKKI käyttäjän Refresh Tokenit

3. Epäilyttävä toiminta
   → Mitätöi KAIKKI käyttäjän Refresh Tokenit

4. Token Rotation -rikkomus
   → Jo käytettyä tokenia yritetään käyttää uudelleen
   → Mitätöi KAIKKI käyttäjän Refresh Tokenit

5. Admin poistaa käyttäjän
   → Mitätöi KAIKKI käyttäjän Refresh Tokenit
```

```csharp
// Esimerkki: Salasanan vaihdon yhteydessä mitätöidään kaikki tokenit
[HttpPost("change-password")]
[Authorize]
public async Task<IActionResult> ChangePassword(
    [FromBody] ChangePasswordRequest request)
{
    var userId = int.Parse(
        User.FindFirst(ClaimTypes.NameIdentifier)!.Value);

    // 1. Vaihda salasana (yksinkertaistettu)
    var user = await _context.Users.FindAsync(userId);
    if (user is null) return NotFound();

    // 2. Varmista vanha salasana
    // if (!BCrypt.Net.BCrypt.Verify(request.OldPassword, user.PasswordHash))
    //     return BadRequest("Vanha salasana on virheellinen");

    // 3. Aseta uusi salasana
    // user.PasswordHash = BCrypt.Net.BCrypt.HashPassword(request.NewPassword);

    // 4. Mitätöi KAIKKI Refresh Tokenit → pakottaa uudelleenkirjautumisen
    await _tokenService.RevokeAllUserTokensAsync(userId);

    await _context.SaveChangesAsync();

    return Ok(new { message = "Salasana vaihdettu, kirjaudu uudelleen" });
}

public class ChangePasswordRequest
{
    public string OldPassword { get; set; } = string.Empty;
    public string NewPassword { get; set; } = string.Empty;
}
```

### 6. Vanhojen tokenien siivous

Ajan myötä tietokantaan kertyy vanhentuneita ja mitätöityjä tokeneita. Nämä tulisi siivota säännöllisesti.

```csharp
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;

// Taustapalvelu, joka siivoaa vanhat tokenit automaattisesti
public class TokenCleanupService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<TokenCleanupService> _logger;

    // Siivousväli (esim. kerran päivässä)
    private readonly TimeSpan _cleanupInterval = TimeSpan.FromHours(24);

    public TokenCleanupService(
        IServiceScopeFactory scopeFactory,
        ILogger<TokenCleanupService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await CleanupExpiredTokensAsync();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Virhe tokenien siivouksessa");
            }

            await Task.Delay(_cleanupInterval, stoppingToken);
        }
    }

    private async Task CleanupExpiredTokensAsync()
    {
        using var scope = _scopeFactory.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        // Poista tokenit, jotka ovat:
        // - Vanhentuneet (expired)
        // - Mitätöidyt (revoked)
        // - Käytetyt (used) ja yli 7 päivää vanhoja
        var cutoffDate = DateTime.UtcNow.AddDays(-7);

        var expiredTokens = await context.RefreshTokens
            .Where(rt => rt.Expires < DateTime.UtcNow
                      || rt.IsRevoked
                      || (rt.IsUsed && rt.Created < cutoffDate))
            .ToListAsync();

        if (expiredTokens.Count > 0)
        {
            context.RefreshTokens.RemoveRange(expiredTokens);
            await context.SaveChangesAsync();

            _logger.LogInformation(
                "Siivottu {Count} vanhentunutta refresh tokenia", 
                expiredTokens.Count);
        }
    }
}
```

Rekisteröi taustapalvelu `Program.cs`:ssä:

```csharp
// Program.cs - lisää taustapalvelu
builder.Services.AddHostedService<TokenCleanupService>();
```

---

## Koko flow yhteenveto

```
┌──────────────────────────────────────────────────────────────────────┐
│                    Autentikointi-flow kokonaisuutena                 │
│                                                                      │
│  ┌─────────┐       POST /login            ┌──────────────────────┐  │
│  │ Käyttäjä│ ────────────────────────────→ │ AuthController       │  │
│  │         │ { email, password }           │                      │  │
│  │         │                               │  1. Validoi tunnus   │  │
│  │         │                               │  2. TokenService:    │  │
│  │         │                               │     - Access Token   │  │
│  │         │ ←──────────────────────────── │     - Refresh Token  │  │
│  │         │ { accessToken, refreshToken } │  3. Tallenna RT DB:n │  │
│  │         │                               └──────────────────────┘  │
│  │         │                                                         │
│  │         │  API-pyynnöt (Bearer token)                            │
│  │         │ ────────────────────────────→ [Authorize] Endpoint     │
│  │         │                                                         │
│  │         │  Access Token vanhenee...                               │
│  │         │                                                         │
│  │         │       POST /refresh           ┌──────────────────────┐  │
│  │         │ ────────────────────────────→ │ AuthController       │  │
│  │         │ { refreshToken: RT-1 }        │                      │  │
│  │         │                               │  1. Hae RT-1 DB:stä │  │
│  │         │                               │  2. Merkitse käytetty│  │
│  │         │                               │  3. Luo uudet:      │  │
│  │         │ ←──────────────────────────── │     - Access Token   │  │
│  │         │ { accessToken, RT-2 }         │     - RT-2           │  │
│  │         │                               └──────────────────────┘  │
│  │         │                                                         │
│  │         │       POST /logout            ┌──────────────────────┐  │
│  │         │ ────────────────────────────→ │ AuthController       │  │
│  │         │ { refreshToken: RT-2 }        │                      │  │
│  │         │                               │  Mitätöi RT-2 DB:stä│  │
│  │         │ ←──────────────────────────── │                      │  │
│  └─────────┘ { message: "OK" }             └──────────────────────┘  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │ TokenCleanupService (taustapalvelu)                      │       │
│  │ - Poistaa vanhentuneet tokenit tietokannasta             │       │
│  │ - Ajastettu: kerran päivässä                             │       │
│  └──────────────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Parhaat käytännöt

| Käytäntö | Kuvaus |
|---|---|
| ✅ **Lyhyt Access Token** | 5-30 minuuttia |
| ✅ **Token Rotation** | Uusi Refresh Token joka refreshissä |
| ✅ **Tietokantatallennus** | Refresh Token aina tietokantaan |
| ✅ **HTTP-only Cookie** | Refresh Token asiakaspuolella |
| ✅ **Siivous** | Poista vanhat tokenit säännöllisesti |
| ✅ **Mitätöinti salasanan vaihdossa** | Mitätöi kaikki tokenit |
| ❌ **Pitkä Access Token** | Älä käytä tuntien/päivien Access Tokenia |
| ❌ **localStorage Refresh Tokenille** | Altis XSS-hyökkäyksille |
| ❌ **Claims Refresh Tokenissa** | Refresh Token on vain satunnainen merkkijono |

---

## Hyödyllisiä linkkejä

- [Microsoft: Refresh Tokens in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/)
- [OWASP: Token Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [RFC 6749 - OAuth 2.0 (Refresh Token)](https://datatracker.ietf.org/doc/html/rfc6749#section-1.5)
- [Auth0: Refresh Token Rotation](https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation)

---

## Edellinen materiaali

- [JWT (JSON Web Token)](JWT.md) - JWT:n teoria ja perustoteutus
- [Autentikointi - Yleiskatsaus](README.md) - Autentikoinnin peruskäsitteet
