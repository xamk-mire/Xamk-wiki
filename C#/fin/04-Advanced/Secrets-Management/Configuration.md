# ASP.NET Core Configuration — Konfiguraatiojärjestelmä

## Sisällysluettelo

1. [Mikä on konfiguraatiojärjestelmä?](#mikä-on-konfiguraatiojärjestelmä)
2. [Konfiguraatiolähteet ja tärkeysjärjestys](#konfiguraatiolähteet-ja-tärkeysjärjestys)
3. [appsettings.json](#appssettingsjson)
4. [Ympäristökohtaiset tiedostot](#ympäristökohtaiset-tiedostot)
5. [ASPNETCORE_ENVIRONMENT](#aspnetcore_environment)
6. [IConfiguration — arvojen lukeminen](#iconfiguration--arvojen-lukeminen)
7. [Options Pattern — IOptions](#options-pattern--ioptions)
8. [IOptions vs. IOptionsSnapshot vs. IOptionsMonitor](#ioptions-vs-ioptionssnapshot-vs-ioptionsmonitor)
9. [Konfiguraation validointi](#konfiguraation-validointi)
10. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Mikä on konfiguraatiojärjestelmä?

ASP.NET Core käyttää **yhtenäistä konfiguraatiojärjestelmää**, joka kokoaa asetukset useista lähteistä yhteen `IConfiguration`-rajapintaan. Sovellus lukee arvot aina `IConfiguration`-rajapinnan kautta — eikä sen tarvitse tietää mistä lähteestä arvo oikeasti tulee.

```
┌────────────────────────────────────────┐
│  Konfiguraatiolähteet                  │
│                                        │
│  appsettings.json          ──┐         │
│  appsettings.Development.json─┤         │
│  User Secrets              ──┼──→  IConfiguration  →  Sovellus
│  Environment Variables     ──┤         │
│  Command-line args         ──┘         │
│                                        │
└────────────────────────────────────────┘
```

Tämä rakenne mahdollistaa sen, että **sama koodi toimii kehitys-, staging- ja tuotantoympäristöissä** ilman muutoksia — vain konfiguraatiolähteet vaihtuvat.

---

## Konfiguraatiolähteet ja tärkeysjärjestys

ASP.NET Core lataa lähteet järjestyksessä. **Myöhemmin ladattu ylikirjoittaa aiemman** — korkein prioriteetti voittaa.

```
Prioriteetti (korkein ylikirjoittaa alemmat):
─────────────────────────────────────────────────
 8. Komentoriviargumentit                ← Korkein
 7. Ympäristömuuttujat
 6. User Secrets (vain Development)
 5. appsettings.{Environment}.json
 4. appsettings.json
 3. Oletusarvot (AddInMemoryCollection)
─────────────────────────────────────────────────
```

### Käytännön esimerkki

Jos `appsettings.json` sisältää `"ApiKey": "default-key"` ja ympäristömuuttuja `ApiKey=real-key` on asetettu, sovellus lukee arvon `real-key` — ympäristömuuttuja ylikirjoittaa JSON-tiedoston.

```csharp
// WebApplication.CreateBuilder rekisteröi lähteet automaattisesti
var builder = WebApplication.CreateBuilder(args);

// builder.Configuration sisältää jo kaikki lähteet yhdistettynä:
// appsettings.json + appsettings.Development.json + User Secrets + env vars
var apiKey = builder.Configuration["ApiKey"]; // "real-key"
```

---

## appsettings.json

`appsettings.json` on projektin peruskonfiguraatiotiedosto. Se tallennetaan versionhallintaan ja sisältää **ei-salaiset** asetukset.

### Rakenne

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  },
  "AllowedHosts": "*",
  "Database": {
    "ConnectionString": "",
    "MaxRetries": 3,
    "CommandTimeoutSeconds": 30
  },
  "ApiKeys": {
    "SendGrid": "",
    "OpenAI": ""
  },
  "Jwt": {
    "Issuer": "https://myapp.example.com",
    "ExpirationMinutes": 60,
    "Secret": ""
  },
  "Features": {
    "EnableDarkMode": true,
    "MaxUploadSizeMb": 10
  }
}
```

### Tärkeimmät säännöt

- **Tyhjä merkkijono** (`""`) tarkoittaa: *"tämä arvo tarvitaan, aseta se User Secretsiin tai ympäristömuuttujiin"*
- **Salaisuudet eivät kuulu tähän tiedostoon** — niitä ei saa koskaan tallentaa versionhallintaan
- Rakenne voi olla sisäkkäinen — sisäkkäisten avainten lukeminen tapahtuu `:` -erottimella: `"Database:MaxRetries"`

---

## Ympäristökohtaiset tiedostot

`appsettings.{Environment}.json` -tiedostot mahdollistavat ympäristökohtaiset ylikirjoitukset. Ne ladataan `appsettings.json`:n jälkeen — vain muuttuneet arvot täytyy kirjoittaa.

```
Projektin kansio:
├── appsettings.json                  ← Peruskonfiguraatio (kaikki ympäristöt)
├── appsettings.Development.json      ← Kehitysympäristö (ylikirjoittaa)
├── appsettings.Staging.json          ← Staging (ylikirjoittaa)
└── appsettings.Production.json       ← Tuotanto (ylikirjoittaa)
```

### Esimerkki

`appsettings.json` (kaikille ympäristöille):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information"
    }
  },
  "Database": {
    "MaxRetries": 3
  }
}
```

`appsettings.Development.json` (vain kehitysympäristöön):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Debug",
      "Microsoft.AspNetCore": "Information"
    }
  }
}
```

`appsettings.Production.json` (vain tuotantoon):
```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft.AspNetCore": "Error"
    }
  },
  "Database": {
    "MaxRetries": 5
  }
}
```

> **Huom:** `appsettings.Development.json` tallennetaan tyypillisesti versionhallintaan (ei sisällä salaisuuksia). `appsettings.Production.json` tallennetaan myös versionhallintaan, mutta salaisuudet asetetaan ympäristömuuttujilla tai Key Vaultilla.

---

## ASPNETCORE_ENVIRONMENT

`ASPNETCORE_ENVIRONMENT` -ympäristömuuttuja kertoo sovellukselle missä ympäristössä se pyörii. Se määrää mm. mitä `appsettings.{Environment}.json` -tiedostoa ladataan ja toimiiko kehittäjäpoikkeussivu (`Developer Exception Page`).

### Arvot

| Arvo | Merkitys |
|------|----------|
| `Development` | Kehitys — User Secrets ladataan, yksityiskohtaiset virhesivut |
| `Staging` | Testaus/staging — ei kehitysominaisuuksia |
| `Production` | Tuotanto — minimaaliset lokitiedot, ei yksityiskohtaisia virheitä |

### Asettaminen

**Paikallisesti (Visual Studio)** — `Properties/launchSettings.json`:
```json
{
  "profiles": {
    "MyApp": {
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

**Paikallisesti (komentorivi)**:
```bash
# PowerShell
$env:ASPNETCORE_ENVIRONMENT = "Development"
dotnet run

# bash/macOS
ASPNETCORE_ENVIRONMENT=Development dotnet run
```

**Azure App Servicessa** (Application Settings):
```
ASPNETCORE_ENVIRONMENT = Production
```

### Ympäristön tarkistaminen koodissa

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
    app.UseSwagger();
    app.UseSwaggerUI();
}

if (app.Environment.IsProduction())
{
    app.UseHsts();
}
```

---

## IConfiguration — arvojen lukeminen

`IConfiguration` on matalan tason rajapinta arvojen suoraan lukemiseen merkkijono-avaimilla.

### Eri lukutavat

```csharp
var builder = WebApplication.CreateBuilder(args);
var config = builder.Configuration;

// 1. Indeksointisyntaksi — palauttaa null jos ei löydy
string? apiKey = config["ApiKeys:SendGrid"];

// 2. GetValue — oletusarvo jos ei löydy
int maxRetries = config.GetValue<int>("Database:MaxRetries", defaultValue: 3);
bool featureEnabled = config.GetValue<bool>("Features:EnableDarkMode", false);

// 3. GetSection — hakee osion omaksi IConfiguration-instanssiksi
IConfigurationSection dbSection = config.GetSection("Database");
string? connStr = dbSection["ConnectionString"];
int retries = dbSection.GetValue<int>("MaxRetries", 3);

// 4. GetConnectionString — lyhenne tietokantayhteyksiä varten
string? connString = config.GetConnectionString("Default");
// Vastaa: config["ConnectionStrings:Default"]

// 5. Bind — kopioi osion arvot olioon
var dbSettings = new DatabaseSettings();
config.GetSection("Database").Bind(dbSettings);
```

### IConfiguration-injektio kontrolleriin

```csharp
[ApiController]
[Route("[controller]")]
public class WeatherController : ControllerBase
{
    private readonly IConfiguration _configuration;

    public WeatherController(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    [HttpGet]
    public IActionResult Get()
    {
        var apiKey = _configuration["WeatherApi:ApiKey"]
            ?? throw new InvalidOperationException("WeatherApi:ApiKey ei ole asetettu.");

        return Ok(new { ApiKeyPrefix = apiKey[..4] + "***" });
    }
}
```

> **Rajoite:** `IConfiguration`-avaimet ovat merkkijonoja — kirjoitusvirheet löytyvät vasta ajon aikana. Options Pattern on parempi vaihtoehto.

---

## Options Pattern — IOptions

**Options Pattern** on suositeltu tapa käyttää konfiguraatiota ASP.NET Core -sovelluksissa. Sen sijaan, että käyttäisit merkkijono-avaimia, sitot konfiguraatio-osion suoraan tyypitettyyn C#-luokkaan.

### Edut IConfigurationiin verrattuna

| | `IConfiguration["avain"]` | `IOptions<T>` |
|-|---------------------------|---------------|
| **Tyyppiturvallisuus** | ❌ merkkijono | ✅ oikea tyyppi |
| **IntelliSense** | ❌ ei | ✅ kyllä |
| **Kirjoitusvirhe** | Löytyy ajon aikana | Löytyy käännösaikana |
| **Testattavuus** | Hankalampaa | Helppo mockata |
| **Uudelleenkäyttö** | Avain kopioitava kaikkialle | Yksi luokka kaikkialle |

### 1. Määrittele Options-luokka

```csharp
public class WeatherApiOptions
{
    // SectionName-vakio sitoo nimen yhteen paikkaan
    public const string SectionName = "WeatherApi";

    public string ApiKey { get; set; } = string.Empty;
    public string BaseUrl { get; set; } = string.Empty;
    public int TimeoutSeconds { get; set; } = 30;
}

public class DatabaseOptions
{
    public const string SectionName = "Database";

    public string ConnectionString { get; set; } = string.Empty;
    public int MaxRetries { get; set; } = 3;
    public int CommandTimeoutSeconds { get; set; } = 30;
}

public class JwtOptions
{
    public const string SectionName = "Jwt";

    public string Secret { get; set; } = string.Empty;
    public string Issuer { get; set; } = string.Empty;
    public int ExpirationMinutes { get; set; } = 60;
}
```

### 2. Rekisteröi Program.cs:ssä

```csharp
var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<WeatherApiOptions>(
    builder.Configuration.GetSection(WeatherApiOptions.SectionName));

builder.Services.Configure<DatabaseOptions>(
    builder.Configuration.GetSection(DatabaseOptions.SectionName));

builder.Services.Configure<JwtOptions>(
    builder.Configuration.GetSection(JwtOptions.SectionName));
```

### 3. Käytä injektiolla

```csharp
[ApiController]
[Route("[controller]")]
public class WeatherController : ControllerBase
{
    private readonly WeatherApiOptions _options;

    public WeatherController(IOptions<WeatherApiOptions> options)
    {
        _options = options.Value;
    }

    [HttpGet]
    public IActionResult GetForecast()
    {
        if (string.IsNullOrEmpty(_options.ApiKey))
            return Problem("WeatherApi:ApiKey ei ole asetettu.", statusCode: 500);

        return Ok(new
        {
            ServiceUrl = _options.BaseUrl,
            KeyPrefix = _options.ApiKey[..4] + "***"
        });
    }
}
```

```csharp
public class EmailService : IEmailService
{
    private readonly WeatherApiOptions _options;
    private readonly ILogger<EmailService> _logger;

    public EmailService(
        IOptions<WeatherApiOptions> options,
        ILogger<EmailService> logger)
    {
        _options = options.Value;
        _logger = logger;
    }

    public async Task SendAsync(string to, string subject)
    {
        _logger.LogInformation(
            "Lähetetään viesti palveluun {Url}", _options.BaseUrl);
        // ...
    }
}
```

---

## IOptions vs. IOptionsSnapshot vs. IOptionsMonitor

Kolme rajapintaa eri tarpeisiin:

| Rajapinta | Päivittyy | Elinkaari | Käyttötapaus |
|-----------|-----------|-----------|--------------|
| `IOptions<T>` | Kerran käynnistyksessä | Singleton | Staattiset arvot, useimmat tilanteet |
| `IOptionsSnapshot<T>` | Per HTTP-pyyntö | Scoped | Arvot voivat muuttua ajon aikana |
| `IOptionsMonitor<T>` | Reaaliajassa | Singleton | Singleton-palvelut, jotka tarvitsevat päivitettyjä arvoja |

### Milloin käyttää mitäkin?

```csharp
// IOptions<T> — yleisin tapaus
// Arvot luetaan kerran sovelluksen käynnistyksessä
public class StaticService
{
    private readonly MyOptions _options;

    public StaticService(IOptions<MyOptions> options)
    {
        _options = options.Value; // Lukee kerran
    }
}

// IOptionsSnapshot<T> — kun appsettings.json voi muuttua ajon aikana
// Uusi instanssi per HTTP-pyyntö
public class DynamicController : ControllerBase
{
    private readonly MyOptions _options;

    public DynamicController(IOptionsSnapshot<MyOptions> options)
    {
        _options = options.Value; // Uusi arvo per pyyntö
    }
}

// IOptionsMonitor<T> — Singleton-palveluissa, kun arvot voivat muuttua
public class BackgroundWorker : BackgroundService
{
    private readonly IOptionsMonitor<MyOptions> _optionsMonitor;

    public BackgroundWorker(IOptionsMonitor<MyOptions> optionsMonitor)
    {
        _optionsMonitor = optionsMonitor;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        while (!stoppingToken.IsCancellationRequested)
        {
            var currentOptions = _optionsMonitor.CurrentValue; // Aina ajantasainen
            await DoWork(currentOptions);
            await Task.Delay(TimeSpan.FromMinutes(1), stoppingToken);
        }
    }
}
```

> **Käytännössä:** `IOptions<T>` riittää lähes aina. User Secretsit ja ympäristömuuttujat eivät muutu sovelluksen ollessa käynnissä.

---

## Konfiguraation validointi

Voit validoida konfiguraation käynnistyksen yhteydessä Data Annotations -attribuuteilla:

```csharp
using System.ComponentModel.DataAnnotations;

public class WeatherApiOptions
{
    public const string SectionName = "WeatherApi";

    [Required(ErrorMessage = "WeatherApi:ApiKey on pakollinen")]
    [MinLength(10, ErrorMessage = "ApiKey on liian lyhyt")]
    public string ApiKey { get; set; } = string.Empty;

    [Required]
    [Url(ErrorMessage = "BaseUrl täytyy olla kelvollinen URL")]
    public string BaseUrl { get; set; } = string.Empty;

    [Range(1, 120)]
    public int TimeoutSeconds { get; set; } = 30;
}
```

```csharp
// Program.cs — validoi käynnistyksen yhteydessä
builder.Services
    .AddOptions<WeatherApiOptions>()
    .Bind(builder.Configuration.GetSection(WeatherApiOptions.SectionName))
    .ValidateDataAnnotations()
    .ValidateOnStart(); // ← Kaataa sovelluksen heti jos validointi epäonnistuu
```

Nyt sovellus ei käynnisty lainkaan jos pakollinen arvo puuttuu — parempi kuin virheen havaitseminen vasta ensimmäisellä API-kutsulla.

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä Options Patternia** `IConfiguration`-suoralukemisen sijaan — parempi tyyppiturvallisuus ja testattavuus
- **Pidä `appsettings.json` puhtaana** — rakenne ja oletusarvot kyllä, salaisuudet ei
- **Käytä `SectionName`-vakiota** Options-luokassa — nimen muuttaminen on helppoa kun se on yhdessä paikassa
- **Validoi käynnistyksessä** `ValidateOnStart()` — virheelliset asetukset havaitaan ennen kuin niistä aiheutuu ongelmia tuotannossa
- **Käytä tyhjää merkkijonoa placeholderina** salaisuuksille `appsettings.json`:ssa — tiimin jäsenet tietävät mitä täytyy asettaa

### ❌ Vältä näitä

- Älä tallenna salaisuuksia `appsettings.json`:iin tai muihin versionhallintaan meneviin tiedostoihin
- Älä käytä `IConfiguration`-merkkijono-avaimia suoraan koodissa useissa paikoissa — avain leviää kaikkialle ja on vaikea muuttaa
- Älä jätä `ASPNETCORE_ENVIRONMENT` asettamatta tuotannossa — sovellus käynnistyy Development-tilassa, mikä voi paljastaa yksityiskohtia virheistä

---

## Seuraavaksi

- [User Secrets](User-Secrets.md) - Salaisuuksien hallinta lokaalikehityksessä
- [Azure Environment Variables](Azure-Environment-Variables.md) - Konfiguraatio Azure App Servicessa
- [Azure Key Vault](Azure-Key-Vault.md) - Tuotantotason salaisuuksien hallinta

## Takaisin

- [Salaisuuksien hallinta — Yleiskatsaus](README.md)
- [Edistyneet aiheet](../README.md)
