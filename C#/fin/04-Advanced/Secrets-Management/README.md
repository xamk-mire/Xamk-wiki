# Salaisuuksien hallinta .NET-sovelluksissa

Tervetuloa salaisuuksien hallinnan oppimateriaaliin! Tämä materiaali käsittelee, miten .NET-sovelluksen salaisuuksia (connection stringit, API-avaimet, salasanat) hallitaan turvallisesti lokaalissa kehityksessä ja Azure-ympäristössä.

## .NET Configuration -järjestelmä

ASP.NET Core käyttää **Configuration**-järjestelmää, joka koostuu useista **Configuration Providereista**. Providerit ladataan järjestyksessä, ja myöhemmin ladattu arvo ylikirjoittaa aiemman.

### Configuration Providerin hierarkia

```
Prioriteetti (korkein ylikirjoittaa alemmat):
─────────────────────────────────────────────
 7. Command-line arguments          ← Korkein
 6. Azure Key Vault                 
 5. User Secrets (Development)      
 4. Environment variables           
 3. appsettings.{Environment}.json  
 2. appsettings.json                
 1. Oletusarvot                     ← Matalin
─────────────────────────────────────────────
```

### Miten tämä toimii käytännössä?

```csharp
var builder = WebApplication.CreateBuilder(args);

// CreateBuilder rekisteröi automaattisesti:
// 1. appsettings.json
// 2. appsettings.{Environment}.json
// 3. User Secrets (kun Environment = "Development")
// 4. Environment variables
// 5. Command-line arguments

// Salaisuus haetaan IConfiguration-rajapinnalla
var connectionString = builder.Configuration.GetConnectionString("Default");
var apiKey = builder.Configuration["ApiKeys:SendGrid"];
```

Tämä tarkoittaa, että:
- **Lokaalisti**: `appsettings.json` sisältää oletusarvot, User Secrets ylikirjoittaa salaisuudet
- **Azuressa**: Environment variables tai Key Vault ylikirjoittaa `appsettings.json`-arvot

### Vahvasti tyypitetty konfiguraatio (Options Pattern)

Salaisuuksien käyttö `IOptions<T>`-rajapinnalla on suositeltu tapa:

```csharp
// 1. Määritä asetusluokka
public class DatabaseSettings
{
    public string ConnectionString { get; set; } = string.Empty;
}

public class ApiKeySettings
{
    public string SendGrid { get; set; } = string.Empty;
    public string OpenAI { get; set; } = string.Empty;
}
```

```csharp
// 2. Rekisteröi Program.cs:ssa
builder.Services.Configure<DatabaseSettings>(
    builder.Configuration.GetSection("Database"));

builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));
```

```csharp
// 3. Käytä palvelussa
public class EmailService
{
    private readonly ApiKeySettings _apiKeys;

    public EmailService(IOptions<ApiKeySettings> apiKeys)
    {
        _apiKeys = apiKeys.Value;
    }

    public async Task SendEmail(string to, string subject, string body)
    {
        var client = new SendGridClient(_apiKeys.SendGrid);
        // ...
    }
}
```

---

## Sisältö

### Perusteet
- [ASP.NET Core Configuration](Configuration.md) - Konfiguraatiojärjestelmä ja Options Pattern
  - Konfiguraatiolähteet ja tärkeysjärjestys
  - `appsettings.json` ja ympäristökohtaiset tiedostot
  - `ASPNETCORE_ENVIRONMENT`
  - `IConfiguration` vs. `IOptions<T>` vs. `IOptionsSnapshot<T>`
  - Konfiguraation validointi käynnistyksessä

### Lokaali kehitys
- [User Secrets](User-Secrets.md) - .NET User Secrets -työkalu lokaaliin kehitykseen
  - `dotnet user-secrets` -komennot
  - `secrets.json`-tiedoston rakenne
  - Käyttö `IConfiguration`- ja `IOptions<T>`-rajapinnoilla

### Azure-ympäristö
- [Azure Environment Variables](Azure-Environment-Variables.md) - Ympäristömuuttujat Azure App Servicessa
  - Application Settings ja Connection Strings
  - Azure Portal ja Azure CLI
  - Slot-kohtaiset asetukset
- [Azure Key Vault](Azure-Key-Vault.md) - Azure Key Vault ja RBAC-pääsynhallinta
  - Key Vaultin luominen ja konfigurointi
  - Managed Identity ja RBAC-roolit
  - .NET-integraatio (`DefaultAzureCredential`)

---

## Oppimisjärjestys

Suosittelemme opiskelua seuraavassa järjestyksessä:

1. **Configuration** - Ymmärrä ASP.NET Coren konfiguraatiojärjestelmä ja Options Pattern
2. **User Secrets** - Aloita lokaalista kehityksestä, opettele hallitsemaan salaisuudet kehitysympäristössä
3. **Azure Environment Variables** - Ymmärrä miten Azure App Service hallitsee konfiguraatiota
4. **Azure Key Vault** - Opi tuotantotason salaisuuksien hallinta Managed Identityn ja RBAC:n avulla

## Esitietovaatimukset

- [Dependency Injection](../Dependency-Injection.md) - Ymmärrä DI ja `IOptions<T>` -rajapinta
- [Azure App Service](../../../../Cloud%20technologies/Azure/App-Service.md) - .NET-sovellusten isännöinti Azuressa
- [Managed Identity](../../../../Cloud%20technologies/Azure/Managed-Identity.md) - Autentikointi ilman salasanoja Azuressa

## Hyödyllisiä linkkejä

- [Microsoft: Configuration in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/)
- [Microsoft: Options pattern in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/configuration/options)
- [Microsoft: Safe storage of app secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets)
- [Microsoft: Azure App Service documentation](https://learn.microsoft.com/en-us/azure/app-service/)
- [Microsoft: Managed Identity overview](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)
