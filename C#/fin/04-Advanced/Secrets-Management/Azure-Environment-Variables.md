# Azure Environment Variables - Ympäristömuuttujat Azure App Servicessa

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Azure App Service Configuration](#azure-app-service-configuration)
3. [Application Settings vs. Connection Strings](#application-settings-vs-connection-strings)
4. [Ympäristömuuttujien asettaminen Azure Portalissa](#ympäristömuuttujien-asettaminen-azure-portalissa)
5. [Ympäristömuuttujien asettaminen Azure CLI:llä](#ympäristömuuttujien-asettaminen-azure-clillä)
6. [Miten .NET lukee ympäristömuuttujat](#miten-net-lukee-ympäristömuuttujat)
7. [Slot-kohtaiset asetukset](#slot-kohtaiset-asetukset)
8. [Käytännön esimerkki](#käytännön-esimerkki)
9. [Turvallisuusnäkökohdat](#turvallisuusnäkökohdat)
10. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Johdanto

**Azure App Service Configuration** on yksinkertaisin tapa hallita salaisuuksia Azuressa. Ympäristömuuttujat asetetaan Azure-portaalissa tai CLI:llä, ja .NET lukee ne automaattisesti `IConfiguration`-rajapinnan kautta.

### Miten se toimii?

```
┌──────────────────────────────┐
│  Azure App Service           │
│                              │
│  Application Settings:       │
│  ┌────────────────────────┐  │
│  │ ApiKeys__SendGrid =    │  │
│  │   "SG.real-key"        │  │
│  │ Jwt__Secret =          │  │
│  │   "prod-secret-key"    │  │
│  └────────────────────────┘  │
│                              │
│  Connection Strings:         │
│  ┌────────────────────────┐  │
│  │ Default =              │  │
│  │   "Server=prod-db;..." │  │
│  └────────────────────────┘  │
│                              │
│  ┌────────────────────────┐  │
│  │    .NET-sovellus       │  │
│  │                        │  │
│  │  IConfiguration lukee  │  │
│  │  automaattisesti ↑     │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

> **Tärkeää:** Azure App Service -ympäristömuuttujat ylikirjoittavat `appsettings.json`-arvot. Sinun ei tarvitse muuttaa koodia.

---

## Azure App Service Configuration

Azure App Servicessa on kaksi konfiguraatiotyyppiä:

### 1. Application Settings

- Yleiskäyttöisiä avain-arvo -pareja
- Näkyvät sovellukselle ympäristömuuttujina
- Soveltuvat API-avaimille, asetuksille ja salaisuuksille
- Sisäkkäiset avaimet käyttävät `__` (kaksi alaviivaa) erottimena

```
Avain:                    Arvo:
───────────────────────   ─────────────────────────
ApiKeys__SendGrid         SG.real-production-key
ApiKeys__OpenAI           sk-real-production-key
Jwt__Secret               prod-jwt-signing-key-32chars
Jwt__Issuer               https://myapp.azurewebsites.net
```

> **Huom:** JSON:n sisäkkäiset avaimet `ApiKeys:SendGrid` muuttuvat ympäristömuuttujissa muotoon `ApiKeys__SendGrid` (kaksoispiste → kaksi alaviivaa).

### 2. Connection Strings

- Erityisesti tietokantayhteyksille
- .NET lukee ne `ConnectionStrings`-osiosta
- Tukee eri tietokantatyyppejä (SQL Server, MySQL, PostgreSQL, Custom)

```
Nimi:      Arvo:                                              Tyyppi:
─────────  ─────────────────────────────────────────────────   ──────────
Default    Server=prod-db.database.windows.net;Database=...   SQLAzure
Redis      myredis.redis.cache.windows.net:6380,...            Custom
```

---

## Application Settings vs. Connection Strings

| Ominaisuus | Application Settings | Connection Strings |
|---|---|---|
| **Käyttötarkoitus** | API-avaimet, yleiset asetukset | Tietokantayhteydet |
| **Lukeminen koodissa** | `Configuration["Key"]` | `Configuration.GetConnectionString("Name")` |
| **Etuliite env-muuttujassa** | Ei etuliitettä | `CUSTOMCONNSTR_`, `SQLCONNSTR_`, jne. |
| **Slot-kohtaisuus** | Valittavissa | Valittavissa |
| **Salaus levossa** | ✅ Kyllä | ✅ Kyllä |

---

## Ympäristömuuttujien asettaminen Azure Portalissa

### Vaihe 1: Navigoi App Service -resurssiin

1. Avaa [Azure Portal](https://portal.azure.com)
2. Valitse **App Services** → Valitse sovelluksesi
3. Vasemmasta valikosta: **Settings** → **Environment variables**

### Vaihe 2: Lisää Application Settings

1. Klikkaa **+ Add** (App settings -välilehdellä)
2. Syötä:
   - **Name**: `ApiKeys__SendGrid`
   - **Value**: `SG.your-real-api-key`
3. Valitse tarvittaessa **Deployment slot setting** (slot-kohtainen)
4. Klikkaa **Apply**

### Vaihe 3: Lisää Connection String

1. Vaihda **Connection strings** -välilehdelle
2. Klikkaa **+ Add**
3. Syötä:
   - **Name**: `Default`
   - **Value**: `Server=myserver.database.windows.net;Database=MyDb;User Id=admin;Password=...`
   - **Type**: `SQLAzure`
4. Klikkaa **Apply**

### Vaihe 4: Tallenna

- Klikkaa **Apply** sivun alaosassa
- Azure käynnistää sovelluksen uudelleen muutosten jälkeen

---

## Ympäristömuuttujien asettaminen Azure CLI:llä

### Application Settings

```bash
# Yksittäinen asetus
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --settings ApiKeys__SendGrid="SG.real-key"

# Useita asetuksia kerralla
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --settings \
    ApiKeys__SendGrid="SG.real-key" \
    ApiKeys__OpenAI="sk-real-key" \
    Jwt__Secret="prod-jwt-secret-key"

# Slot-kohtainen asetus
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --slot staging \
  --settings ApiKeys__SendGrid="SG.staging-key" \
  --slot-settings ApiKeys__SendGrid="SG.staging-key"
```

### Connection Strings

```bash
# Connection string
az webapp config connection-string set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --connection-string-type SQLAzure \
  --settings Default="Server=myserver.database.windows.net;Database=MyDb;..."
```

### Asetusten listaaminen

```bash
# Application Settings
az webapp config appsettings list \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --output table

# Connection Strings
az webapp config connection-string list \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --output table
```

### Asetuksen poistaminen

```bash
az webapp config appsettings delete \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --setting-names ApiKeys__SendGrid
```

---

## Miten .NET lukee ympäristömuuttujat

### Automaattinen lukeminen

.NET lukee ympäristömuuttujat automaattisesti - **et tarvitse ylimääräistä koodia**:

```csharp
var builder = WebApplication.CreateBuilder(args);

// Nämä toimivat automaattisesti:
// 1. appsettings.json ladataan ensin
// 2. Azure Environment Variables ylikirjoittavat arvot

// Application Settings
var sendGridKey = builder.Configuration["ApiKeys:SendGrid"];
var jwtSecret = builder.Configuration["Jwt:Secret"];

// Connection Strings
var connectionString = builder.Configuration.GetConnectionString("Default");
```

### Sisäkkäisten avainten muunnos

Azure käyttää `__` (kaksi alaviivaa) JSON:n `:` (kaksoispiste) sijasta:

```json
// appsettings.json
{
  "ApiKeys": {
    "SendGrid": ""    // ← tyhjä lokaalisti
  }
}
```

```
// Azure App Service → Environment Variables
ApiKeys__SendGrid = "SG.real-key"    // ← __ vastaa JSON:n sisäkkäisyyttä
```

```csharp
// Koodissa ei tarvitse tietää kumpaa käytetään
var key = builder.Configuration["ApiKeys:SendGrid"]; // Toimii molemmilla!
```

### Options Pattern Azuressa

Sama koodi toimii sekä lokaalisti (User Secrets) että Azuressa (Environment Variables):

```csharp
// Program.cs - tämä koodi on SAMA molemmissa ympäristöissä
builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));

builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));
```

```csharp
// Palvelussa - tämä koodi on SAMA molemmissa ympäristöissä
public class EmailService : IEmailService
{
    private readonly ApiKeySettings _apiKeys;

    public EmailService(IOptions<ApiKeySettings> apiKeys)
    {
        _apiKeys = apiKeys.Value;
    }

    public async Task SendEmailAsync(string to, string subject, string body)
    {
        // Lokaalisti: arvo tulee User Secrets:stä
        // Azuressa: arvo tulee Environment Variables:sta
        var client = new SendGridClient(_apiKeys.SendGrid);
        // ...
    }
}
```

---

## Slot-kohtaiset asetukset

Azure App Servicessa voit luoda **deployment slotteja** (esim. `staging`, `production`). Slot-kohtaiset asetukset pysyvät slotissa, eivätkä vaihdu swapin yhteydessä.

### Miksi slot-kohtaisuus on tärkeää?

```
┌─────────────────────┐     SWAP      ┌─────────────────────┐
│  STAGING SLOT       │  ←────────→   │  PRODUCTION SLOT    │
│                     │               │                     │
│  App Code: v2.0 ────┼──── swap ────→│  App Code: v2.0     │
│                     │               │                     │
│  DB_CONN: staging ──┼── EI swap ──→ │  DB_CONN: prod      │
│  (slot-kohtainen)   │               │  (slot-kohtainen)   │
└─────────────────────┘               └─────────────────────┘
```

### Slot-kohtaisen asetuksen määrittäminen

**Portalissa:**
- Raksita **Deployment slot setting** -valintaruutu asetuksen kohdalla

**CLI:llä:**
```bash
# --slot-settings merkitsee asetuksen slot-kohtaiseksi
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --slot-settings ConnectionStrings__Default="Server=staging-db;..."
```

### Tyypilliset slot-kohtaiset asetukset

| Asetus | Slot-kohtainen? | Miksi? |
|---|---|---|
| **Tietokantayhteys** | ✅ Kyllä | Staging käyttää eri tietokantaa |
| **API-avaimet** | ⚠️ Riippuu | Eri avaimet staging/production |
| **Logging-taso** | ✅ Kyllä | Staging: Debug, Production: Warning |
| **Feature flags** | ✅ Kyllä | Uudet ominaisuudet ensin stagingissa |
| **Sovelluksen nimi** | ❌ Ei | Sama kaikissa sloteissa |

---

## Käytännön esimerkki

### appsettings.json (versionhallinnassa)

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
    "MaxRetries": 3
  },
  "ApiKeys": {
    "SendGrid": "",
    "OpenAI": ""
  },
  "Jwt": {
    "Secret": "",
    "Issuer": "https://myapp.azurewebsites.net",
    "ExpirationMinutes": 60
  }
}
```

### Azure App Service - Application Settings

```
Name                          Value                              Slot Setting
──────────────────────────    ─────────────────────────────────  ────────────
Database__ConnectionString    Server=prod.database.windows.net;  ✅
Database__MaxRetries          5                                  ❌
ApiKeys__SendGrid             SG.prod-real-key                   ✅
ApiKeys__OpenAI               sk-prod-real-key                   ✅
Jwt__Secret                   prod-jwt-secret-32-chars-min!      ✅
ASPNETCORE_ENVIRONMENT        Production                         ✅
```

### Program.cs (sama koodi kaikissa ympäristöissä)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Options Pattern - toimii automaattisesti:
// - Lokaalisti: User Secrets
// - Azuressa: Environment Variables ylikirjoittavat appsettings.json
builder.Services.Configure<DatabaseSettings>(
    builder.Configuration.GetSection("Database"));
builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));

// DbContext
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetSection("Database")["ConnectionString"]));

// Palvelut
builder.Services.AddScoped<IEmailService, EmailService>();
builder.Services.AddScoped<ITokenService, TokenService>();

var app = builder.Build();
app.MapControllers();
app.Run();
```

---

## Turvallisuusnäkökohdat

### Huomioitavaa

| Riski | Kuvaus | Ratkaisu |
|---|---|---|
| **Portalin käyttöoikeudet** | Kuka tahansa Contributor-roolissa näkee arvot | Rajaa pääsy RBAC:lla |
| **Arvot näkyvissä portaalissa** | Salaisuudet näkyvät selkotekstinä asetuksissa | Käytä Key Vault -viittauksia |
| **Ei audit-lokia** | Ei tiedetä kuka muutti tai luki asetuksen | Käytä Key Vault -viittauksia |
| **Ei versiointia** | Vanha arvo häviää kun päivität | Käytä Key Vault:ia versiointiin |
| **ARM-templatessa** | Arvot voivat näkyä deployment-templatessa | Käytä Key Vault -referenssejä |

### Key Vault -viittaukset (Key Vault References)

Voit yhdistää Environment Variables:n ja Key Vaultin käyttämällä **Key Vault -viittauksia**:

```
Application Setting:
────────────────────────────────────────────────────────────
Name:   ApiKeys__SendGrid
Value:  @Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/SendGridApiKey)
```

Tämä tarjoaa parhaat puolet molemmista:
- ✅ Yksinkertainen konfiguraatio (Environment Variables)
- ✅ Turvallinen tallennus (Key Vault)
- ✅ Audit-lokit ja versiointi (Key Vault)

> Lisätietoja Key Vault -integraatiosta: [Azure Key Vault](Azure-Key-Vault.md)

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä `__` (kaksi alaviivaa)** sisäkkäisten avainten erottimena ympäristömuuttujissa
- **Merkitse salaisuudet slot-kohtaisiksi** erityisesti tietokantayhteydet ja API-avaimet
- **Aseta `ASPNETCORE_ENVIRONMENT`** jokaiselle slotille (Production, Staging)
- **Käytä Azure CLI:tä** skriptattaviin deployauksiin (toistettavuus)
- **Harkitse Key Vault -viittauksia** tuotannon salaisuuksille

### ❌ Vältä näitä

- Älä tallenna ympäristömuuttujia lähdekoodiin tai ARM-templateihin selkotekstinä
- Älä käytä samoja salaisuuksia staging- ja production-ympäristössä
- Älä jätä slot-kohtaisuutta merkitsemättä - swapin yhteydessä salaisuudet voivat vaihtaa paikkaa

---

## Seuraavaksi

- [Azure Key Vault](Azure-Key-Vault.md) - Tuotantotason salaisuuksien hallinta RBAC:n ja Managed Identityn avulla

## Takaisin

- [User Secrets](User-Secrets.md) - Lokaalikehityksen salaisuudet
- [Salaisuuksien hallinta - Yleiskatsaus](README.md)
- [Edistyneet aiheet](../README.md)
