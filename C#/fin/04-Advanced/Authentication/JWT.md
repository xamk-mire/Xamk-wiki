# JWT (JSON Web Token)

## Sisällysluettelo

- [Mikä on JWT?](#mikä-on-jwt)
- [JWT:n rakenne](#jwtn-rakenne)
  - [Header](#1-header-otsikko)
  - [Payload](#2-payload-hyötykuorma)
  - [Signature](#3-signature-allekirjoitus)
- [Claims](#claims)
- [JWT:n elinkaari](#jwtn-elinkaari)
- [Symmetrinen vs. asymmetrinen allekirjoitus](#symmetrinen-vs-asymmetrinen-allekirjoitus)
- [JWT:n hyödyt ja rajoitukset](#jwtn-hyödyt-ja-rajoitukset)
- [Toteutus ASP.NET Coressa](#toteutus-aspnet-coressa)
  - [NuGet-paketit](#1-nuget-paketit)
  - [Asetukset](#2-asetukset-appsettingsjson)
  - [Asetusluokka](#3-asetusluokka)
  - [TokenService](#4-tokenservice---tokenin-generointi)
  - [Program.cs konfigurointi](#5-programcs---jwt-autentikoinnin-konfigurointi)
  - [Kontrollerit](#6-kontrollerit)
  - [Claims-tietojen lukeminen](#7-claims-tietojen-lukeminen)
- [Hyödyllisiä linkkejä](#hyödyllisiä-linkkejä)

---

## Mikä on JWT?

**JWT (JSON Web Token)** on avoin standardi ([RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)), joka määrittelee kompaktin ja itsenäisen tavan siirtää tietoa osapuolten välillä JSON-muodossa. Tieto on digitaalisesti allekirjoitettu, joten sen eheys voidaan varmistaa.

```
JWT on kuin digitaalinen henkilökortti:
──────────────────────────────────────
┌─────────────────────────────────────────┐
│  HENKILÖKORTTI (JWT)                    │
│                                         │
│  Nimi: Matti Meikäläinen                │  ← Payload (käyttäjätiedot)
│  Rooli: Admin                           │
│  Voimassa: 17.2.2026 klo 15:00 asti    │
│                                         │
│  Allekirjoitus: a8f3k2...               │  ← Signature (eheyden varmistus)
│  Myöntäjä: my-api.example.com          │  ← Issuer
└─────────────────────────────────────────┘

- Kuka tahansa voi LUKEA kortin tiedot (Base64-dekoodaus)
- Kukaan ei voi MUOKATA tietoja ilman allekirjoitusavainta
- Palvelin voi VARMISTAA kortin aitouden allekirjoituksen avulla
```

---

## JWT:n rakenne

JWT koostuu kolmesta osasta, jotka on eroteltu pisteillä (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ik1hdHRpIn0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
└──────────── Header ────────────┘ └──────────── Payload ─────────────┘ └──────────── Signature ──────────┘
```

### 1. Header (Otsikko)

Header kertoo tokenin tyypin ja allekirjoitusalgoritmin:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

| Kenttä | Kuvaus |
|---|---|
| `alg` | Allekirjoitusalgoritmi (esim. `HS256`, `RS256`) |
| `typ` | Tokenin tyyppi (aina `JWT`) |

### 2. Payload (Hyötykuorma)

Payload sisältää **claims**-tiedot eli väittämät käyttäjästä:

```json
{
  "sub": "user-123",
  "name": "Matti Meikäläinen",
  "email": "matti@example.com",
  "role": "Admin",
  "iat": 1708200000,
  "exp": 1708203600
}
```

> ⚠️ **Huom!** Payload on vain Base64-koodattu, **ei salattu**. Älä koskaan tallenna salasanoja tai arkaluontoisia tietoja payloadiin!

### 3. Signature (Allekirjoitus)

Allekirjoitus luodaan yhdistämällä Header, Payload ja salainen avain:

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

```
Allekirjoituksen tarkoitus:
───────────────────────────
1. Eheys (Integrity)
   → Varmistaa, että tokenin sisältöä ei ole muutettu

2. Aitous (Authenticity)  
   → Varmistaa, että token on luotu luotetun palvelimen toimesta

3. EI salaa dataa
   → Kuka tahansa voi lukea headerin ja payloadin
   → Allekirjoitus estää vain muokkaamisen
```

---

## Claims

Claims ovat avain-arvo-pareja JWT:n payloadissa. Ne jaetaan kolmeen kategoriaan:

### Registered Claims (Rekisteröidyt)

Standardoidut claims, jotka on määritelty [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) -standardissa:

| Claim | Nimi | Kuvaus | Esimerkki |
|---|---|---|---|
| `sub` | Subject | Käyttäjän tunniste | `"user-123"` |
| `iss` | Issuer | Tokenin myöntäjä | `"my-api.example.com"` |
| `aud` | Audience | Tokenin vastaanottaja | `"my-app.example.com"` |
| `exp` | Expiration | Vanhenemisaika (Unix timestamp) | `1708203600` |
| `iat` | Issued At | Luontiaika (Unix timestamp) | `1708200000` |
| `nbf` | Not Before | Token ei ole voimassa ennen tätä | `1708200000` |
| `jti` | JWT ID | Tokenin yksilöllinen tunniste | `"abc-123-def"` |

### Public Claims (Julkiset)

Vapaasti määriteltäviä claims-kenttiä, jotka ovat yleisesti tunnettuja:

```json
{
  "name": "Matti Meikäläinen",
  "email": "matti@example.com",
  "role": "Admin"
}
```

### Private Claims (Yksityiset)

Sovelluksen omia claims-kenttiä, joista lähettäjä ja vastaanottaja ovat sopineet:

```json
{
  "department": "IT",
  "employee_id": "EMP-456",
  "permissions": ["read", "write", "delete"]
}
```

---

## JWT:n elinkaari

```
┌──────────┐                                    ┌──────────┐
│  Käyttäjä │                                    │ Palvelin │
└─────┬────┘                                    └─────┬────┘
      │                                               │
      │  1. POST /api/auth/login                      │
      │  { "email": "...", "password": "..." }        │
      │ ─────────────────────────────────────────────→ │
      │                                               │
      │                          2. Validoi tunnukset │
      │                          3. Luo JWT-token     │
      │                                               │
      │  4. 200 OK                                    │
      │  { "token": "eyJhbG...", "expiration": "..." }│
      │ ←───────────────────────────────────────────── │
      │                                               │
      │  5. GET /api/users (suojattu endpoint)        │
      │  Headers: Authorization: Bearer eyJhbG...     │
      │ ─────────────────────────────────────────────→ │
      │                                               │
      │                    6. Validoi token:           │
      │                       - Allekirjoitus OK?     │
      │                       - Vanhentunut?          │
      │                       - Issuer/Audience OK?   │
      │                                               │
      │  7. 200 OK (data) tai 401 Unauthorized        │
      │ ←───────────────────────────────────────────── │
      │                                               │
```

---

## Symmetrinen vs. asymmetrinen allekirjoitus

| Ominaisuus | Symmetrinen (HS256) | Asymmetrinen (RS256) |
|---|---|---|
| **Avaimet** | Yksi jaettu salainen avain | Avainpari: yksityinen + julkinen |
| **Allekirjoitus** | Sama avain allekirjoittaa ja validoi | Yksityinen avain allekirjoittaa |
| **Validointi** | Sama avain validoi | Julkinen avain validoi |
| **Käyttökohde** | Yksittäinen palvelin / monoliitti | Mikropalvelut, useat palvelimet |
| **Turvallisuus** | Avain täytyy jakaa kaikille validoijille | Vain julkinen avain jaetaan |
| **Suorituskyky** | Nopeampi | Hitaampi (mutta silti nopea) |

```
Symmetrinen (HS256):
────────────────────
Palvelin A (sama avain)          Palvelin B (sama avain)
   ┌──────┐                         ┌──────┐
   │ 🔑   │  ← Sama salainen  →    │ 🔑   │
   │ Luo  │     avain molemmilla    │Validoi│
   └──────┘                         └──────┘

Asymmetrinen (RS256):
─────────────────────
Palvelin A (yksityinen avain)    Palvelin B (julkinen avain)
   ┌──────┐                         ┌──────┐
   │ 🔐   │  Yksityinen avain      │ 🔓   │  Julkinen avain
   │ Luo  │  (vain tällä)           │Validoi│  (jaettu kaikille)
   └──────┘                         └──────┘
```

> 💡 **Yksinkertaisissa sovelluksissa** (yksi palvelin) `HS256` on riittävä ja helpompi toteuttaa. **Mikropalveluarkkitehtuurissa** `RS256` on turvallisempi, koska yksityinen avain pysyy yhdellä palvelimella.

---

## JWT:n hyödyt ja rajoitukset

### ✅ Hyödyt

| Hyöty | Kuvaus |
|---|---|
| **Tilaton (Stateless)** | Palvelimen ei tarvitse tallentaa sessiotietoja |
| **Skaalautuva** | Mikä tahansa palvelin voi validoida tokenin |
| **Itsenäinen** | Token sisältää kaikki tarvittavat tiedot (claims) |
| **Standardoitu** | Avoin standardi (RFC 7519), laaja tuki |
| **Cross-platform** | Toimii eri ohjelmointikielillä ja alustoilla |

### ❌ Rajoitukset

| Rajoitus | Kuvaus | Ratkaisu |
|---|---|---|
| **Ei voi mitätöidä** | Token on voimassa kunnes vanhenee | Lyhyt elinkaari + Refresh Token |
| **Koko kasvaa** | Mitä enemmän claimeja, sitä suurempi token | Tallenna vain välttämättömät tiedot |
| **Ei salattu** | Payload on Base64-koodattu, luettavissa | Älä tallenna arkaluontoista dataa |
| **Avainten hallinta** | Salainen avain täytyy pitää turvassa | Käytä [Secrets Management](../Secrets-Management/) |

---

## Toteutus ASP.NET Coressa

### 1. NuGet-paketit

```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package System.IdentityModel.Tokens.Jwt
```

### 2. Asetukset (appsettings.json)

```json
{
  "JwtSettings": {
    "Secret": "TÄMÄ-ON-VAIN-KEHITYSTÄ-VARTEN-KÄYTÄ-USER-SECRETS-TAI-KEY-VAULTIA-TUOTANNOSSA-vähintään-32-merkkiä",
    "Issuer": "my-api.example.com",
    "Audience": "my-app.example.com",
    "ExpirationMinutes": 15
  }
}
```

> ⚠️ **Älä koskaan tallenna oikeaa Secret-avainta `appsettings.json`-tiedostoon!** Käytä [User Secrets](../Secrets-Management/User-Secrets.md) lokaalissa kehityksessä ja [Azure Key Vault](../Secrets-Management/Azure-Key-Vault.md) tuotannossa.

### 3. Asetusluokka

```csharp
// Vahvasti tyypitetty konfiguraatio JWT-asetuksille
public class JwtSettings
{
    public string Secret { get; set; } = string.Empty;
    public string Issuer { get; set; } = string.Empty;
    public string Audience { get; set; } = string.Empty;
    public int ExpirationMinutes { get; set; } = 15;
}
```

### 4. TokenService - Tokenin generointi

```csharp
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using Microsoft.Extensions.Options;
using Microsoft.IdentityModel.Tokens;

public interface ITokenService
{
    string GenerateAccessToken(User user);
}

public class TokenService : ITokenService
{
    private readonly JwtSettings _jwtSettings;

    public TokenService(IOptions<JwtSettings> jwtSettings)
    {
        _jwtSettings = jwtSettings.Value;
    }

    public string GenerateAccessToken(User user)
    {
        // 1. Luodaan salainen avain tavumuodossa
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_jwtSettings.Secret));

        // 2. Luodaan allekirjoitustiedot (avain + algoritmi)
        var credentials = new SigningCredentials(
            key, SecurityAlgorithms.HmacSha256);

        // 3. Määritellään tokenin claims (käyttäjätiedot)
        var claims = new List<Claim>
        {
            // Rekisteröidyt claims
            new Claim(JwtRegisteredClaimNames.Sub, user.Id.ToString()),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new Claim(JwtRegisteredClaimNames.Iat, 
                DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString(),
                ClaimValueTypes.Integer64),

            // Omat claims
            new Claim(ClaimTypes.Name, user.UserName),
            new Claim(ClaimTypes.Email, user.Email),
            new Claim(ClaimTypes.Role, user.Role)
        };

        // 4. Luodaan JWT-token
        var token = new JwtSecurityToken(
            issuer: _jwtSettings.Issuer,
            audience: _jwtSettings.Audience,
            claims: claims,
            expires: DateTime.UtcNow.AddMinutes(_jwtSettings.ExpirationMinutes),
            signingCredentials: credentials
        );

        // 5. Serialisoidaan token merkkijonoksi
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

### User-luokka (esimerkki)

```csharp
// Yksinkertainen käyttäjäluokka
public class User
{
    public int Id { get; set; }
    public string UserName { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;
    public string PasswordHash { get; set; } = string.Empty;
    public string Role { get; set; } = "User";
}
```

### 5. Program.cs - JWT-autentikoinnin konfigurointi

```csharp
using System.Text;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

var builder = WebApplication.CreateBuilder(args);

// 1. Rekisteröi JWT-asetukset (Options Pattern)
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("JwtSettings"));

// 2. Rekisteröi TokenService
builder.Services.AddScoped<ITokenService, TokenService>();

// 3. Konfiguroi JWT-autentikointi
var jwtSettings = builder.Configuration
    .GetSection("JwtSettings")
    .Get<JwtSettings>()!;

builder.Services
    .AddAuthentication(options =>
    {
        // Oletusautentikointi on JWT Bearer
        options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
    })
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            // Validoi allekirjoitus
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwtSettings.Secret)),

            // Validoi myöntäjä (issuer)
            ValidateIssuer = true,
            ValidIssuer = jwtSettings.Issuer,

            // Validoi vastaanottaja (audience)
            ValidateAudience = true,
            ValidAudience = jwtSettings.Audience,

            // Validoi vanhenemisaika
            ValidateLifetime = true,

            // Sallittu aikaero kellon synkronoinnissa (oletus 5 min)
            ClockSkew = TimeSpan.Zero
        };
    });

builder.Services.AddAuthorization();
builder.Services.AddControllers();

var app = builder.Build();

// 4. Lisää middleware OIKEASSA JÄRJESTYKSESSÄ
app.UseAuthentication();  // ← Ensin: "Kuka olet?"
app.UseAuthorization();   // ← Sitten: "Mitä saat tehdä?"

app.MapControllers();
app.Run();
```

```
Middleware-järjestys on tärkeä:
──────────────────────────────
Pyyntö → UseAuthentication() → UseAuthorization() → Controller
                │                       │
                │                       └─ Tarkistaa onko oikeus
                └─ Lukee ja validoi JWT-tokenin
```

### 6. Kontrollerit

#### AuthController - Kirjautuminen

```csharp
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly ITokenService _tokenService;

    public AuthController(ITokenService tokenService)
    {
        _tokenService = tokenService;
    }

    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginRequest request)
    {
        // 1. Validoi käyttäjätunnukset (tässä yksinkertaistettu esimerkki)
        //    Oikeassa sovelluksessa: hae käyttäjä tietokannasta ja
        //    vertaa salasanan hashia (esim. BCrypt)
        var user = ValidateCredentials(request.Email, request.Password);

        if (user is null)
        {
            return Unauthorized(new { message = "Virheellinen sähköposti tai salasana" });
        }

        // 2. Generoi JWT-token
        var token = _tokenService.GenerateAccessToken(user);

        // 3. Palauta token
        return Ok(new LoginResponse
        {
            Token = token,
            Expiration = DateTime.UtcNow.AddMinutes(15)
        });
    }

    private User? ValidateCredentials(string email, string password)
    {
        // TODO: Oikeassa sovelluksessa hae tietokannasta
        // ja käytä BCrypt.Verify() salasanan tarkistukseen
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

public class LoginResponse
{
    public string Token { get; set; } = string.Empty;
    public DateTime Expiration { get; set; }
}
```

#### Suojattu kontrolleri - [Authorize]-attribuutti

```csharp
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

[ApiController]
[Route("api/[controller]")]
[Authorize] // ← Kaikki endpointit vaativat autentikoinnin
public class UsersController : ControllerBase
{
    // Kaikki kirjautuneet käyttäjät pääsevät tähän
    [HttpGet("profile")]
    public IActionResult GetProfile()
    {
        return Ok(new { message = "Tämä on suojattu endpoint!" });
    }

    // Vain Admin-roolissa olevat pääsevät tähän
    [HttpGet("admin")]
    [Authorize(Roles = "Admin")]
    public IActionResult AdminOnly()
    {
        return Ok(new { message = "Tervetuloa, admin!" });
    }

    // Tämä endpoint on julkinen (ei vaadi tokenia)
    [HttpGet("public")]
    [AllowAnonymous]
    public IActionResult PublicEndpoint()
    {
        return Ok(new { message = "Tämä on julkinen endpoint" });
    }
}
```

```
[Authorize]-attribuutin käyttö:
───────────────────────────────
[Authorize]              → Vaatii kirjautumisen (mikä tahansa rooli)
[Authorize(Roles = "Admin")]  → Vaatii Admin-roolin
[Authorize(Roles = "Admin,Manager")] → Admin TAI Manager
[AllowAnonymous]         → Ohittaa autentikoinnin (julkinen)

Attribuutti voidaan asettaa:
- Kontrolleri-tasolle   → Kaikki endpointit suojataan
- Metodi-tasolle        → Vain kyseinen endpoint suojataan
```

### 7. Claims-tietojen lukeminen

Kun JWT on validoitu, voit lukea claims-tiedot `HttpContext.User`-objektista:

```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class ProfileController : ControllerBase
{
    [HttpGet]
    public IActionResult GetMyProfile()
    {
        // Lue claims JWT-tokenista
        var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        var userName = User.FindFirst(ClaimTypes.Name)?.Value;
        var email = User.FindFirst(ClaimTypes.Email)?.Value;
        var role = User.FindFirst(ClaimTypes.Role)?.Value;

        // Vaihtoehtoinen tapa lukea Sub-claim
        var sub = User.FindFirst(JwtRegisteredClaimNames.Sub)?.Value;

        return Ok(new
        {
            UserId = userId,
            UserName = userName,
            Email = email,
            Role = role
        });
    }

    // Esimerkki: hae vain kirjautuneen käyttäjän omat tiedot
    [HttpGet("orders")]
    public IActionResult GetMyOrders()
    {
        var userId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;

        if (userId is null)
        {
            return Unauthorized();
        }

        // Hae tilaukset tietokannasta käyttäjän ID:n perusteella
        // var orders = _orderService.GetByUserId(int.Parse(userId));

        return Ok(new { message = $"Käyttäjän {userId} tilaukset" });
    }
}
```

```
Claims-tietojen lukeminen kontrollerissa:
─────────────────────────────────────────
User.FindFirst(ClaimTypes.NameIdentifier) → Käyttäjän ID (sub)
User.FindFirst(ClaimTypes.Name)           → Käyttäjänimi
User.FindFirst(ClaimTypes.Email)          → Sähköposti
User.FindFirst(ClaimTypes.Role)           → Rooli
User.IsInRole("Admin")                    → Onko Admin-roolissa? (bool)

Huom: "User" on ControllerBase-luokan property,
joka palauttaa ClaimsPrincipal-objektin.
```

---

## Koko autentikoinnin flow yhteenveto

```
┌─────────────────────────────────────────────────────────────────┐
│                        ASP.NET Core API                        │
│                                                                 │
│  appsettings.json ──→ JwtSettings ──→ Options Pattern          │
│       (asetukset)      (luokka)       (IOptions<JwtSettings>)  │
│                                                                 │
│  ┌────────────────┐    ┌──────────────┐    ┌────────────────┐  │
│  │ AuthController │───→│ TokenService │───→│ JwtSecurityToken│  │
│  │ POST /login    │    │ GenerateToken│    │ (token luodaan) │  │
│  └────────────────┘    └──────────────┘    └────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Middleware Pipeline                                      │   │
│  │                                                          │   │
│  │ Request → UseAuthentication() → UseAuthorization()       │   │
│  │              │                       │                   │   │
│  │              │ Validoi JWT            │ Tarkistaa roolit │   │
│  │              │ (TokenValidation-      │ ([Authorize])    │   │
│  │              │  Parameters)           │                  │   │
│  │              ↓                       ↓                   │   │
│  │          ClaimsPrincipal ──→ Controller (User.Claims)    │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hyödyllisiä linkkejä

- [Microsoft: JWT Bearer Authentication in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/jwt)
- [JWT.io - Token Debugger](https://jwt.io/) - Testaa ja debuggaa JWT-tokeneita
- [RFC 7519 - JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
- [Microsoft: Claims-based Authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/claims)
- [Microsoft: Role-based Authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles)

---

## Seuraavaksi

Opi turvallinen tokenien uusimisstrategia:
- [Refresh Tokens](Refresh-Tokens.md) - Access Token + Refresh Token -malli
