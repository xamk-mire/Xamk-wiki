# Azure Key Vault - Tuotantotason salaisuuksien hallinta (RBAC)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Key Vaultin luominen](#key-vaultin-luominen)
3. [RBAC vs. Access Policy](#rbac-vs-access-policy)
4. [RBAC-roolien määrittäminen](#rbac-roolien-määrittäminen)
5. [Managed Identity](#managed-identity)
6. [.NET-integraatio](#net-integraatio)
7. [DefaultAzureCredential](#defaultazurecredential)
8. [Käytännön esimerkki](#käytännön-esimerkki)
9. [Key Vault References App Servicessa](#key-vault-references-app-servicessa)
10. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Johdanto

**Azure Key Vault** on Azuren palvelu salaisuuksien, salausavainten ja sertifikaattien turvalliseen tallentamiseen. Se tarjoaa:

- ✅ **HSM-suojattu salaus** - salaisuudet salataan laitteistotasolla
- ✅ **RBAC-pääsynhallinta** - tarkka hallinta kuka pääsee mihinkin
- ✅ **Audit-lokit** - kaikki pääsy kirjataan
- ✅ **Versiointi** - salaisuuksien historia säilyy
- ✅ **Managed Identity** - ei salasanoja palveluiden välillä

### Miksi Key Vault?

```
❌ ILMAN KEY VAULTIA:
┌──────────────┐    salasana     ┌──────────────┐
│  App Service │ ──────────────→ │  Tietokanta  │
│              │  (env muuttuja) │              │
└──────────────┘                 └──────────────┘
  Salasana näkyy portaalissa, ei auditointia

✅ KEY VAULTIN KANSSA:
┌──────────────┐  Managed    ┌──────────────┐   salaisuus   ┌──────────────┐
│  App Service │ ──Identity──│  Key Vault   │ ────────────→ │  Tietokanta  │
│              │  (ei salas.)│  (RBAC)      │               │              │
└──────────────┘             └──────────────┘               └──────────────┘
  Ei salasanoja konfiguraatiossa, kaikki auditoitu
```

---

## Key Vaultin luominen

### Azure Portalissa

1. Avaa [Azure Portal](https://portal.azure.com)
2. Klikkaa **+ Create a resource**
3. Hae **Key Vault** → Klikkaa **Create**
4. Täytä:
   - **Resource group**: Valitse tai luo uusi
   - **Key vault name**: `myapp-kv` (globaalisti uniikki)
   - **Region**: Sama kuin sovelluksesi
   - **Pricing tier**: Standard
5. **Access configuration** -välilehdellä:
   - **Permission model**: ✅ Valitse **Azure role-based access control (recommended)**
6. Klikkaa **Review + create** → **Create**

### Azure CLI:llä

```bash
# 1. Luo Resource Group (jos ei vielä ole)
az group create \
  --name MyResourceGroup \
  --location northeurope

# 2. Luo Key Vault RBAC-mallilla
az keyvault create \
  --name myapp-kv \
  --resource-group MyResourceGroup \
  --location northeurope \
  --enable-rbac-authorization true

# 3. Lisää salaisuus
az keyvault secret set \
  --vault-name myapp-kv \
  --name "DatabaseConnectionString" \
  --value "Server=prod-db.database.windows.net;Database=MyDb;..."

az keyvault secret set \
  --vault-name myapp-kv \
  --name "SendGridApiKey" \
  --value "SG.real-production-key"

az keyvault secret set \
  --vault-name myapp-kv \
  --name "JwtSecret" \
  --value "production-jwt-signing-key-min-32-characters!"
```

### Salaisuuden nimeämiskäytännöt

Key Vault ei tue `:`- tai `__`-merkkejä nimissä. Käytä `--` (kaksi väliviivaa):

| appsettings.json-avain | Key Vault -nimi |
|---|---|
| `ConnectionStrings:Default` | `ConnectionStrings--Default` |
| `ApiKeys:SendGrid` | `ApiKeys--SendGrid` |
| `Jwt:Secret` | `Jwt--Secret` |

> **Huom:** .NET:n Key Vault -provider muuntaa `--` automaattisesti `:`-merkiksi.

---

## RBAC vs. Access Policy

Azure Key Vault tukee kahta pääsynhallintamallia:

| Ominaisuus | RBAC (suositeltu) | Access Policy |
|---|---|---|
| **Hallintamalli** | Azure IAM -roolit | Key Vault -omat käytännöt |
| **Granulariteetti** | Yksittäinen salaisuus | Koko Key Vault |
| **Azure AD -integraatio** | ✅ Natiivi | ⚠️ Rajoitettu |
| **Conditional Access** | ✅ Kyllä | ❌ Ei |
| **Yhdenmukainen** | ✅ Sama malli kuin muissa Azure-palveluissa | ❌ Oma malli |
| **Suositus** | ✅ **Microsoftin suosittelema** | ⚠️ Legacy |

### Miksi RBAC on parempi?

1. **Yhdenmukainen pääsynhallinta** - Sama RBAC-malli kuin muissa Azure-palveluissa
2. **Tarkempi hallinta** - Voit antaa oikeuden yksittäiseen salaisuuteen
3. **Conditional Access** - Voit vaatia MFA:ta tai rajata IP-osoitteen perusteella
4. **Auditointipolku** - Kaikki Azure AD:n kautta, yksi paikka

---

## RBAC-roolien määrittäminen

### Key Vault -roolit

| Rooli | Oikeudet | Käyttökohteet |
|---|---|---|
| **Key Vault Administrator** | Kaikki oikeudet Key Vaultiin | Ylläpitäjät |
| **Key Vault Secrets Officer** | Hallinnoi salaisuuksia (CRUD) | DevOps, CI/CD |
| **Key Vault Secrets User** | Lukee salaisuuksia | Sovellukset (Managed Identity) |
| **Key Vault Reader** | Lukee Key Vaultin metatiedot | Monitorointi |

### Roolin myöntäminen Azure Portalissa

1. Avaa Key Vault → **Access control (IAM)**
2. Klikkaa **+ Add** → **Add role assignment**
3. Valitse rooli: **Key Vault Secrets User**
4. Valitse jäsen:
   - Sovelluksen **Managed Identity** (tuotannossa)
   - Oma käyttäjätilisi (kehityksessä)
5. Klikkaa **Review + assign**

### Roolin myöntäminen Azure CLI:llä

```bash
# 1. Hae App Servicen Managed Identityn Object ID
APP_IDENTITY=$(az webapp identity show \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --query principalId \
  --output tsv)

# 2. Hae Key Vaultin Resource ID
KV_ID=$(az keyvault show \
  --name myapp-kv \
  --query id \
  --output tsv)

# 3. Myönnä Key Vault Secrets User -rooli
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee $APP_IDENTITY \
  --scope $KV_ID
```

### Roolin myöntäminen kehittäjälle (lokaali kehitys)

```bash
# Hae oma käyttäjä-ID
USER_ID=$(az ad signed-in-user show --query id --output tsv)

# Myönnä Key Vault Secrets User -rooli
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee $USER_ID \
  --scope $KV_ID
```

---

## Managed Identity

**Managed Identity** on Azure AD:n identiteetti, joka myönnetään Azure-resurssille (esim. App Service). Sen avulla sovellus voi autentikoitua muihin Azure-palveluihin **ilman salasanoja**.

### System-assigned vs. User-assigned

| Ominaisuus | System-assigned | User-assigned |
|---|---|---|
| **Elinkaari** | Sidottu resurssiin | Itsenäinen resurssi |
| **Luominen** | Automaattinen (resurssin asetuksissa) | Luodaan erikseen |
| **Jakaminen** | Yksi per resurssi | Voidaan jakaa usean resurssin kesken |
| **Käyttökohteet** | Yksinkertaiset tapaukset | Usean sovelluksen jaettu identiteetti |
| **Suositus** | ✅ Yleensä riittävä | Tarvittaessa |

### System-assigned Managed Identity käyttöönotto

**Portalissa:**
1. App Service → **Identity** → **System assigned**
2. Vaihda **Status** → **On**
3. Klikkaa **Save**

**CLI:llä:**
```bash
# Ota Managed Identity käyttöön
az webapp identity assign \
  --resource-group MyResourceGroup \
  --name MyAppService

# Tulostaa:
# {
#   "principalId": "abc12345-...",
#   "tenantId": "def67890-...",
#   "type": "SystemAssigned"
# }
```

---

## .NET-integraatio

### NuGet-paketit

```bash
# Key Vault -konfiguraatioprovider
dotnet add package Azure.Extensions.AspNetCore.Configuration.Secrets

# Azure Identity (DefaultAzureCredential)
dotnet add package Azure.Identity
```

### Program.cs-konfigurointi

```csharp
using Azure.Identity;

var builder = WebApplication.CreateBuilder(args);

// Lisää Azure Key Vault konfiguraatiolähteeksi
var keyVaultUrl = builder.Configuration["KeyVault:Url"];

if (!string.IsNullOrEmpty(keyVaultUrl))
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(keyVaultUrl),
        new DefaultAzureCredential());
}

// Options Pattern - toimii samalla tavalla kuin ennenkin
builder.Services.Configure<DatabaseSettings>(
    builder.Configuration.GetSection("Database"));
builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));

builder.Services.AddScoped<IEmailService, EmailService>();

var app = builder.Build();
app.MapControllers();
app.Run();
```

### appsettings.json

```json
{
  "KeyVault": {
    "Url": ""
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
    "Secret": "",
    "Issuer": "https://myapp.azurewebsites.net",
    "ExpirationMinutes": 60
  }
}
```

### Azure App Service - Environment Variable

```
KeyVault__Url = https://myapp-kv.vault.azure.net/
```

> **Huom:** Key Vault URL asetetaan ympäristömuuttujana. Key Vault itse sisältää varsinaiset salaisuudet. Näin koodissa ei ole mitään salaisuuksia.

---

## DefaultAzureCredential

`DefaultAzureCredential` on Azure Identity -kirjaston luokka, joka yrittää autentikoitua **usealla eri tavalla** järjestyksessä. Tämä mahdollistaa saman koodin toimimisen sekä lokaalisti että Azuressa.

### Autentikoinnin järjestys

```
DefaultAzureCredential yrittää seuraavat järjestyksessä:
───────────────────────────────────────────────────────
 1. EnvironmentCredential         ← Environment variables
 2. WorkloadIdentityCredential    ← Kubernetes
 3. ManagedIdentityCredential     ← Azure App Service ✅
 4. AzureDeveloperCliCredential   ← azd CLI
 5. SharedTokenCacheCredential    ← Visual Studio cache
 6. VisualStudioCredential        ← Visual Studio ✅
 7. VisualStudioCodeCredential    ← VS Code
 8. AzureCliCredential            ← Azure CLI ✅
 9. AzurePowerShellCredential     ← PowerShell
10. InteractiveBrowserCredential  ← Selain
───────────────────────────────────────────────────────
```

### Miten tämä toimii käytännössä?

**Lokaalisti (kehitysympäristö):**
1. Kirjaudu Azure CLI:llä: `az login`
2. `DefaultAzureCredential` käyttää **AzureCliCredential** tai **VisualStudioCredential**
3. Varmista, että käyttäjälläsi on **Key Vault Secrets User** -rooli

**Azuressa (tuotanto):**
1. App Servicellä on **Managed Identity** käytössä
2. `DefaultAzureCredential` käyttää **ManagedIdentityCredential** automaattisesti
3. Managed Identityllä on **Key Vault Secrets User** -rooli

```csharp
// Sama koodi toimii molemmissa ympäristöissä!
var credential = new DefaultAzureCredential();

builder.Configuration.AddAzureKeyVault(
    new Uri("https://myapp-kv.vault.azure.net/"),
    credential);
```

### Lokaalin kehityksen valmistelu

```bash
# 1. Kirjaudu Azureen
az login

# 2. Valitse oikea subscription (jos useita)
az account set --subscription "My Subscription"

# 3. Varmista, että sinulla on oikeudet Key Vaultiin
az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee your.email@company.com \
  --scope /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.KeyVault/vaults/myapp-kv
```

---

## Käytännön esimerkki

### Kokonaisvaltainen esimerkki: ASP.NET Core Web API + Key Vault

#### 1. Asetusluokat

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

#### 2. Program.cs

```csharp
using Azure.Identity;

var builder = WebApplication.CreateBuilder(args);

// ─── Key Vault konfiguraatio ───
var keyVaultUrl = builder.Configuration["KeyVault:Url"];
if (!string.IsNullOrEmpty(keyVaultUrl))
{
    builder.Configuration.AddAzureKeyVault(
        new Uri(keyVaultUrl),
        new DefaultAzureCredential());
}

// ─── Options Pattern ───
builder.Services.Configure<DatabaseSettings>(
    builder.Configuration.GetSection("Database"));
builder.Services.Configure<ApiKeySettings>(
    builder.Configuration.GetSection("ApiKeys"));
builder.Services.Configure<JwtSettings>(
    builder.Configuration.GetSection("Jwt"));

// ─── DbContext ───
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetSection("Database")["ConnectionString"]));

// ─── Palvelut ───
builder.Services.AddScoped<IEmailService, EmailService>();
builder.Services.AddScoped<ITokenService, TokenService>();
builder.Services.AddControllers();

var app = builder.Build();
app.MapControllers();
app.Run();
```

#### 3. Key Vault -salaisuudet (Azure CLI)

```bash
# Luo salaisuudet Key Vaultiin
# Huom: käytä -- erottimena (ei : tai __)
az keyvault secret set --vault-name myapp-kv \
  --name "Database--ConnectionString" \
  --value "Server=prod-db.database.windows.net;Database=MyDb;User Id=admin;Password=SuperS3cret!"

az keyvault secret set --vault-name myapp-kv \
  --name "ApiKeys--SendGrid" \
  --value "SG.real-production-api-key"

az keyvault secret set --vault-name myapp-kv \
  --name "ApiKeys--OpenAI" \
  --value "sk-real-production-api-key"

az keyvault secret set --vault-name myapp-kv \
  --name "Jwt--Secret" \
  --value "production-jwt-signing-key-minimum-32-characters!"
```

#### 4. App Service -konfiguraatio

```bash
# Ota Managed Identity käyttöön
az webapp identity assign \
  --resource-group MyResourceGroup \
  --name MyAppService

# Myönnä Key Vault Secrets User -rooli
APP_IDENTITY=$(az webapp identity show \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --query principalId --output tsv)

KV_ID=$(az keyvault show --name myapp-kv --query id --output tsv)

az role assignment create \
  --role "Key Vault Secrets User" \
  --assignee $APP_IDENTITY \
  --scope $KV_ID

# Aseta Key Vault URL ympäristömuuttujaksi
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --settings KeyVault__Url="https://myapp-kv.vault.azure.net/"
```

#### 5. Konfiguraation hierarkia

```
LOKAALI KEHITYS:
────────────────
appsettings.json          → Rakenne ja oletusarvot
  ↑ ylikirjoitetaan
User Secrets (secrets.json) → Kehittäjän omat salaisuudet
  ↑ ylikirjoitetaan (jos Key Vault URL asetettu)
Key Vault                   → Tuotannon salaisuudet

AZURE (TUOTANTO):
─────────────────
appsettings.json          → Rakenne ja oletusarvot
  ↑ ylikirjoitetaan
Environment Variables      → KeyVault__Url
  ↑ ylikirjoitetaan
Key Vault                  → Kaikki salaisuudet (Managed Identity)
```

---

## Key Vault References App Servicessa

Vaihtoehtoinen tapa käyttää Key Vaultia ilman koodimuutoksia. App Servicen ympäristömuuttujat voivat **viitata suoraan Key Vaultiin**:

### Konfigurointi

```
Application Setting:
────────────────────────────────────────────────────────────────────────────
Name:    Database__ConnectionString
Value:   @Microsoft.KeyVault(SecretUri=https://myapp-kv.vault.azure.net/secrets/DatabaseConnectionString)

Name:    ApiKeys__SendGrid
Value:   @Microsoft.KeyVault(SecretUri=https://myapp-kv.vault.azure.net/secrets/SendGridApiKey)
```

### Azure CLI:llä

```bash
az webapp config appsettings set \
  --resource-group MyResourceGroup \
  --name MyAppService \
  --settings \
    Database__ConnectionString="@Microsoft.KeyVault(SecretUri=https://myapp-kv.vault.azure.net/secrets/DatabaseConnectionString)" \
    ApiKeys__SendGrid="@Microsoft.KeyVault(SecretUri=https://myapp-kv.vault.azure.net/secrets/SendGridApiKey)"
```

### Edut

- ✅ Ei tarvita NuGet-paketteja (`Azure.Identity`, `Azure.Extensions.AspNetCore.Configuration.Secrets`)
- ✅ Ei koodimuutoksia - toimii kuten tavalliset ympäristömuuttujat
- ✅ Key Vaultin turvallisuus ja auditointi

### Rajoitukset

- ❌ Toimii vain Azure App Servicessa (ei lokaalisti)
- ❌ Ei toimi konttisovelluksissa (ACA, AKS) ilman lisäkonfiguraatiota
- ❌ Salaisuuden päivitys vaatii sovelluksen uudelleenkäynnistyksen

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä RBAC:ia** Access Policyn sijaan - se on Microsoftin suosittelema malli
- **Käytä Managed Identity:ä** - ei salasanoja palveluiden välillä
- **Käytä `Key Vault Secrets User` -roolia** sovelluksille - vain lukuoikeus
- **Nimeä salaisuudet johdonmukaisesti** - käytä `--` erottimena (.NET muuntaa automaattisesti)
- **Erota Key Vaultit ympäristöittäin** - `myapp-dev-kv`, `myapp-staging-kv`, `myapp-prod-kv`
- **Kierrätä salaisuudet** - vaihda API-avaimet ja salasanat säännöllisesti
- **Ota Soft Delete käyttöön** - vahingossa poistetut salaisuudet voidaan palauttaa
- **Monitoroi Key Vault** - Azure Monitor ja Diagnostic Settings audit-lokeille

### ❌ Vältä näitä

- Älä anna **Key Vault Administrator** -roolia sovelluksille - käytä **Secrets User**
- Älä tallenna Key Vault URL:ää koodiin - käytä ympäristömuuttujaa tai `appsettings.json`:ia
- Älä luo yhtä Key Vaultia kaikille ympäristöille
- Älä käytä Access Policy -mallia uusissa projekteissa

### Vertailu: Konfiguraatioprovider vs. Key Vault References

| Ominaisuus | AddAzureKeyVault (koodi) | Key Vault References |
|---|---|---|
| **NuGet-paketit** | Tarvitaan | Ei tarvita |
| **Koodimuutokset** | Program.cs muutos | Ei muutoksia |
| **Lokaali kehitys** | ✅ Toimii (DefaultAzureCredential) | ❌ Ei toimi |
| **Kontit (ACA/AKS)** | ✅ Toimii | ⚠️ Rajoitettu |
| **Dynaaminen päivitys** | Konfiguroitavissa | Uudelleenkäynnistys |
| **Suositus** | ✅ Joustavampi | ✅ Yksinkertaisempi |

---

## Seuraavaksi

- [Azure Key Vault pilvipalveluna](../../../../Cloud%20technologies/Azure/Key-Vault.md) - Key Vaultin käsitteet, hinnoittelu ja verkkokonfiguraatio

## Takaisin

- [Azure Environment Variables](Azure-Environment-Variables.md) - Ympäristömuuttujat App Servicessa
- [User Secrets](User-Secrets.md) - Lokaalikehityksen salaisuudet
- [Salaisuuksien hallinta - Yleiskatsaus](README.md)
- [Edistyneet aiheet](../README.md)
