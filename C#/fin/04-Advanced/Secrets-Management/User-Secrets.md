# User Secrets - Lokaalikehityksen salaisuudet

## Sisällysluettelo

1. [Mikä on User Secrets?](#mikä-on-user-secrets)
2. [Asennus ja käyttöönotto](#asennus-ja-käyttöönotto)
3. [Salaisuuksien hallinta](#salaisuuksien-hallinta)
4. [Secrets.json-tiedoston rakenne](#secretsjson-tiedoston-rakenne)
5. [Käyttö .NET-sovelluksessa](#käyttö-net-sovelluksessa)
6. [Options Pattern - vahvasti tyypitetty konfiguraatio](#options-pattern---vahvasti-tyypitetty-konfiguraatio)
7. [Käytännön esimerkki](#käytännön-esimerkki)
8. [Parhaat käytännöt](#parhaat-käytännöt)
9. [Rajoitukset](#rajoitukset)

---

## Mikä on User Secrets?

**User Secrets** on .NET:n sisäänrakennettu työkalu, joka tallentaa kehitysvaiheen salaisuudet **käyttäjäprofiilin alle** - ei projektikansioon. Tämä tarkoittaa, että:

- ✅ Salaisuudet eivät koskaan päädy versionhallintaan
- ✅ Jokaisella kehittäjällä voi olla omat arvonsa
- ✅ Salaisuudet ylikirjoittavat `appsettings.json`-arvot automaattisesti

### Miten se toimii?

```
┌─────────────────────────────────┐
│  Projektikansio (Git-repo)      │
│                                 │
│  appsettings.json               │
│  {                              │
│    "Database": {                │
│      "ConnectionString": ""     │  ← Tyhjä tai placeholder
│    }                            │
│  }                              │
└──────────────┬──────────────────┘
               │ ylikirjoitetaan
┌──────────────▼──────────────────┐
│  User Secrets (käyttäjäprofiili)│
│                                 │
│  secrets.json                   │
│  {                              │
│    "Database": {                │
│      "ConnectionString":        │  ← Oikea arvo
│        "Server=localhost;..."   │
│    }                            │
│  }                              │
└─────────────────────────────────┘
```

### Missä secrets.json sijaitsee?

| Käyttöjärjestelmä | Sijainti |
|---|---|
| **Windows** | `%APPDATA%\Microsoft\UserSecrets\<UserSecretsId>\secrets.json` |
| **macOS/Linux** | `~/.microsoft/usersecrets/<UserSecretsId>/secrets.json` |

> **Huom:** `<UserSecretsId>` on GUID, joka generoidaan projektikohtaisesti `.csproj`-tiedostoon.

---

## Asennus ja käyttöönotto

### 1. Alusta User Secrets projektissa

```bash
# Navigoi projektikansioon (.csproj-tiedoston sijainti)
cd MyApi

# Alusta User Secrets
dotnet user-secrets init
```

Tämä lisää `.csproj`-tiedostoon `UserSecretsId`-elementin:

```xml
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
  <!-- Tämä lisätään automaattisesti -->
  <UserSecretsId>a1b2c3d4-e5f6-7890-abcd-ef1234567890</UserSecretsId>
</PropertyGroup>
```

### 2. Varmista, että NuGet-paketti on asennettu

ASP.NET Core -projekteissa (`WebApplication.CreateBuilder`) User Secrets toimii automaattisesti. Konsolisovelluksissa tarvitset paketin:

```bash
dotnet add package Microsoft.Extensions.Configuration.UserSecrets
```

---

## Salaisuuksien hallinta

### Salaisuuden asettaminen

```bash
# Yksinkertainen arvo
dotnet user-secrets set "ApiKeys:SendGrid" "SG.your-real-api-key-here"

# Connection string
dotnet user-secrets set "ConnectionStrings:Default" "Server=localhost;Database=MyDb;User=sa;Password=MyP@ssw0rd"

# Sisäkkäinen arvo (käytä kaksoispistettä : erottimena)
dotnet user-secrets set "Database:ConnectionString" "Server=localhost;Database=MyDb;User=sa;Password=MyP@ssw0rd"
dotnet user-secrets set "Database:MaxRetries" "3"
```

### Salaisuuksien listaaminen

```bash
dotnet user-secrets list
```

Tulostaa:

```
Database:ConnectionString = Server=localhost;Database=MyDb;User=sa;Password=MyP@ssw0rd
Database:MaxRetries = 3
ApiKeys:SendGrid = SG.your-real-api-key-here
```

### Yksittäisen salaisuuden poistaminen

```bash
dotnet user-secrets remove "ApiKeys:SendGrid"
```

### Kaikkien salaisuuksien poistaminen

```bash
dotnet user-secrets clear
```

---

## Secrets.json-tiedoston rakenne

Voit myös muokata `secrets.json`-tiedostoa suoraan. Se on tavallinen JSON-tiedosto:

```json
{
  "ConnectionStrings": {
    "Default": "Server=localhost;Database=MyDb;User=sa;Password=MyP@ssw0rd"
  },
  "Database": {
    "ConnectionString": "Server=localhost;Database=MyDb;User=sa;Password=MyP@ssw0rd",
    "MaxRetries": 3
  },
  "ApiKeys": {
    "SendGrid": "SG.your-real-api-key-here",
    "OpenAI": "sk-your-openai-key-here"
  },
  "Jwt": {
    "Secret": "my-super-secret-jwt-signing-key-min-32-chars!",
    "Issuer": "https://localhost:5001"
  }
}
```

> **Vinkki:** Visual Studiossa voit avata `secrets.json`-tiedoston klikkaamalla projektia hiiren oikealla ja valitsemalla **"Manage User Secrets"**.

---

## Käyttö .NET-sovelluksessa

### ASP.NET Core (WebApplication)

User Secrets ladataan automaattisesti kun `ASPNETCORE_ENVIRONMENT` on `Development`:

```csharp
var builder = WebApplication.CreateBuilder(args);

// User Secrets ladataan automaattisesti Development-ympäristössä!
// Ei tarvita ylimääräistä konfiguraatiota.

// Hae salaisuus suoraan
var connectionString = builder.Configuration.GetConnectionString("Default");
var sendGridKey = builder.Configuration["ApiKeys:SendGrid"];

// Tai käytä GetSection
var jwtSecret = builder.Configuration.GetSection("Jwt")["Secret"];
```

### Konsolisovellus

Konsolisovelluksessa User Secrets pitää rekisteröidä erikseen:

```csharp
using Microsoft.Extensions.Configuration;

var configuration = new ConfigurationBuilder()
    .SetBasePath(Directory.GetCurrentDirectory())
    .AddJsonFile("appsettings.json", optional: true)
    .AddUserSecrets<Program>()  // ← Lisää User Secrets
    .Build();

var apiKey = configuration["ApiKeys:SendGrid"];
```

---

## Options Pattern - vahvasti tyypitetty konfiguraatio

**Options Pattern** on suositeltu tapa käyttää konfiguraatioarvoja. Sen sijaan, että hakisit arvoja merkkijonoilla, luot tyypitetyn luokan.

### 1. Määritä asetusluokat

```csharp
public class DatabaseSettings
{
    public string ConnectionString { get; set; } = string.Empty;
    public int MaxRetries { get; set; } = 3;
}

public class ApiKeySettings
{
    public string SendGrid { get; set; } = string.Empty;
    public string OpenAI { get; set; } = string.Empty;
}

public class JwtSettings
{
    public string Secret { get; set; } = string.Empty;
    public string Issuer { get; set; } = string.Empty;
    public int ExpirationMinutes { get; set; } = 60;
}
```

### 2. Rekisteröi Options

```csharp
var builder = WebApplication.CreateBuilder(args);

// Sido konfiguraatio-osiot asetusluokkiin
builder.Services.Configure<DatabaseSettings>(
    builder.Configuration.GetSection("Database"));

builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));

builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));
```

### 3. Käytä palveluissa

```csharp
public class EmailService : IEmailService
{
    private readonly ApiKeySettings _apiKeys;
    private readonly ILogger<EmailService> _logger;

    public EmailService(
        IOptions<ApiKeySettings> apiKeys,
        ILogger<EmailService> logger)
    {
        _apiKeys = apiKeys.Value;
        _logger = logger;
    }

    public async Task SendEmailAsync(string to, string subject, string body)
    {
        var client = new SendGridClient(_apiKeys.SendGrid);
        _logger.LogInformation("Lähetetään sähköposti osoitteeseen {To}", to);
        // ...
    }
}
```

```csharp
public class TokenService : ITokenService
{
    private readonly JwtSettings _jwtSettings;

    public TokenService(IOptions<JwtSettings> jwtSettings)
    {
        _jwtSettings = jwtSettings.Value;
    }

    public string GenerateToken(User user)
    {
        var key = new SymmetricSecurityKey(
            Encoding.UTF8.GetBytes(_jwtSettings.Secret));
        
        var credentials = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            issuer: _jwtSettings.Issuer,
            expires: DateTime.UtcNow.AddMinutes(_jwtSettings.ExpirationMinutes),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
```

---

## Käytännön esimerkki

Koko sovelluksen konfiguraatio yhdistettynä:

### appsettings.json (versionhallinnassa - EI salaisuuksia)

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  },
  "Database": {
    "ConnectionString": "",
    "MaxRetries": 3
  },
  "ApiKeys": {
    "SendGrid": "",
    "OpenAI": ""
  },
  "Jwt": {
    "Issuer": "https://myapp.azurewebsites.net",
    "ExpirationMinutes": 60,
    "Secret": ""
  }
}
```

### secrets.json (User Secrets - EI versionhallinnassa)

```json
{
  "Database": {
    "ConnectionString": "Server=localhost;Database=MyDb;User=sa;Password=DevP@ss123"
  },
  "ApiKeys": {
    "SendGrid": "SG.dev-key-for-testing",
    "OpenAI": "sk-dev-key-for-testing"
  },
  "Jwt": {
    "Secret": "my-local-dev-jwt-secret-key-min-32-characters!"
  }
}
```

### Program.cs

```csharp
var builder = WebApplication.CreateBuilder(args);

// Konfiguraatio (User Secrets ladataan automaattisesti Development-ympäristössä)
builder.Services.Configure<DatabaseSettings>(
    builder.Configuration.GetSection("Database"));
builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));

// Palvelut
builder.Services.AddScoped<IEmailService, EmailService>();
builder.Services.AddScoped<ITokenService, TokenService>();

// Tietokantayhteys
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetSection("Database")["ConnectionString"]));

var app = builder.Build();
// ...
```

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä Options Pattern:ia** tyypitetyn konfiguraation sijaan merkkijonoavaimia
- **Pidä `appsettings.json` puhtaana** - ei salaisuuksia, vain rakenne ja oletusarvot
- **Dokumentoi tarvittavat salaisuudet** - kerro README:ssä tai CONTRIBUTING:ssa mitä User Secrets -avaimia projekti tarvitsee
- **Käytä `dotnet user-secrets` -komentoja** eikä muokkaa `secrets.json`:ia suoraan (vähemmän virhealtista)

### ❌ Vältä näitä

- Älä luota User Secrets:iin tuotannossa - se on **vain kehityskäyttöön**
- Älä jaa `secrets.json`-tiedostoa tiimin kesken - jokaisella kehittäjällä on omat arvonsa
- Älä tallenna User Secrets ID:tä `.gitignore`-tiedostoon - se on osa projektin konfiguraatiota ja kuuluu `.csproj`-tiedostoon

---

## Rajoitukset

| Rajoitus | Kuvaus |
|---|---|
| **Ei salausta** | `secrets.json` tallennetaan selkotekstinä levylle |
| **Vain kehityskäyttöön** | Ei sovellu tuotantoon tai staging-ympäristöön |
| **Ei keskitettyä hallintaa** | Jokainen kehittäjä hallitsee omia salaisuuksiaan |
| **Ei versiointia** | Ei audit-lokia tai muutoshistoriaa |
| **Projektikohtainen** | Salaisuudet on sidottu `UserSecretsId`-arvoon |

> **Tuotantokäyttöön** katso [Azure Environment Variables](Azure-Environment-Variables.md) tai [Azure Key Vault](Azure-Key-Vault.md).

---

## Seuraavaksi

- [Azure Environment Variables](Azure-Environment-Variables.md) - Ympäristömuuttujat Azure App Servicessa
- [Azure Key Vault](Azure-Key-Vault.md) - Tuotantotason salaisuuksien hallinta

## Takaisin

- [Salaisuuksien hallinta - Yleiskatsaus](README.md)
- [Edistyneet aiheet](../README.md)
