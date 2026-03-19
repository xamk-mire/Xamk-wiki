# Azure Managed Identity — Autentikointi ilman salasanoja

## Sisällysluettelo

1. [Mikä on Managed Identity?](#mikä-on-managed-identity)
2. [Kolme vaihetta käytännössä](#kolme-vaihetta-käytännössä)
3. [Vaihe 1 — Managed Identityn aktivointi](#vaihe-1--managed-identityn-aktivointi)
4. [Vaihe 2 — RBAC-oikeuksien myöntäminen](#vaihe-2--rbac-oikeuksien-myöntäminen)
5. [Vaihe 3 — DefaultAzureCredential koodissa](#vaihe-3--defaultazurecredential-koodissa)
6. [Paikallinen kehitys](#paikallinen-kehitys)
7. [Miten se toimii taustalla?](#miten-se-toimii-taustalla)
8. [System-assigned vs. User-assigned](#system-assigned-vs-user-assigned)
9. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Mikä on Managed Identity?

Kuvittele, että App Service -sovelluksesi on uusi työntekijä yrityksessä. Ennen kuin se pääsee käsiksi arkaluonteisiin resursseihin — kuten Key Vaultin salaisuuksiin — sillä täytyy olla **henkilöllisyystodistus** ja **kulkuoikeus** oikeisiin paikkoihin.

**Managed Identity** antaa Azure-resurssillesi (kuten App Servicelle) oman henkilöllisyyden Azuressa. Azure luo ja hallitsee tätä identiteettiä automaattisesti — sinun ei tarvitse luoda salasanoja, varmenteita tai API-avaimia.

### Ongelma ilman Managed Identityä

Perinteinen tapa antaa sovellukselle pääsy Key Vaultiin on luoda **rekisteröity sovellus** (App Registration) Azureen ja tallentaa sen `client_id` ja `client_secret` ympäristömuuttujiin:

```
❌ ILMAN MANAGED IDENTITYÄ:

App Service                        Key Vault
──────────────────────────────     ───────────────
AZURE_CLIENT_ID = "abc-123"   ──→  "Kuka sinä olet?"
AZURE_CLIENT_SECRET = "xyz"   ──→  "Onko sinulla oikeudet?"

Ongelma: Key Vaultin salaisuuden lukemiseen tarvitaan
toinen salaisuus (client_secret). Mistä se tallennetaan?
Ympäristömuuttujaan — joka on taas yksi hallittava salaisuus.
```

Tämä on noidankehä. Managed Identity katkaisee sen:

```
✅ MANAGED IDENTITYN KANSSA:

App Service                        Key Vault
──────────────────────────────     ───────────────
(Managed Identity aktivoitu)  ──→  "Kuka sinä olet?"
                                   "Olen app-myapi,
                                    Azure todistaa sen."
                              ──→  "Onko sinulla oikeudet?"
                                   "Tarkistetaan RBAC..."
                              ←──  Salaisuus palautetaan

Ei salasanoja, ei API-avaimia. Azure hoitaa tunnistautumisen.
```

> **Ydin:** Azure tietää, että tietty App Service -instanssi on se mitä väittääkin olevansa — aivan kuten yrityksen kulunvalvontajärjestelmä tietää, kenen henkilökortti on kenen. Sinun ei tarvitse kertoa salasanaa, kortti itsessään on todiste.

---

## Kolme vaihetta käytännössä

Managed Identityn käyttöönotto koostuu aina kolmesta selkeästä vaiheesta:

```
VAIHE 1                    VAIHE 2                    VAIHE 3
─────────────────────      ─────────────────────      ─────────────────────
Aktivoi identiteetti       Myönnä oikeudet            Käytä koodissa

App Service saa            Key Vault saa luvan         .NET-koodi hakee
oman tunnisteen            päästää App Service         salaisuuden
Azuressa.                  lukemaan salaisuuksia.      DefaultAzureCredential
                                                       -luokan avulla.
az webapp                  az role assignment          new SecretClient(
  identity assign            create                      uri,
                               --role                    new DefaultAzureCredential()
                               "Key Vault              )
                               Secrets User"
```

Kaikki kolme vaihetta täytyy tehdä — ilman yhtäkin niistä sovellus ei pysty lukemaan salaisuuksia.

---

## Vaihe 1 — Managed Identityn aktivointi

Tässä vaiheessa App Servicelle luodaan oma identiteetti Azuressa. Tuloksena on **Object ID** (tunnetaan myös nimellä Principal ID) — yksilöllinen tunniste, jota käytetään seuraavassa vaiheessa oikeuksien myöntämiseen.

### Vaihtoehto A: Azure CLI

```bash
# Aktivoi system-assigned Managed Identity
az webapp identity assign \
  --resource-group $RG \
  --name $APP
```

Komento tulostaa JSON-vastauksen, jossa näkyy luotu identiteetti:

```json
{
  "principalId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "tenantId": "...",
  "type": "SystemAssigned"
}
```

`principalId` on App Servicen identiteetin yksilöllinen tunniste. Tallenna se — tarvitset sen vaiheessa 2.

```bash
# Tallenna principalId muuttujaan myöhempää käyttöä varten
$IDENTITY_ID = az webapp identity show \
  --resource-group $RG \
  --name $APP \
  --query principalId \
  --output tsv

# Tulosta arvo tarkistukseksi
Write-Output "Identity ID: $IDENTITY_ID"
```

### Vaihtoehto B: Azure Portal

1. Avaa **App Service** Portalissa
2. Vasemmassa valikossa: **Settings** → **Identity**
3. **System assigned** -välilehdellä vaihda **Status** → **On**
4. Klikkaa **Save** ja vahvista avautuva valintaikkuna
5. Sivulle ilmestyy **Object (principal) ID** — kopioi se talteen

---

## Vaihe 2 — RBAC-oikeuksien myöntäminen

Managed Identity on nyt olemassa, mutta sillä ei vielä ole oikeuksia mihinkään. Oikeudet myönnetään **RBAC:n** (Role-Based Access Control) avulla.

### Mikä on RBAC?

RBAC on Azuren tapa hallita käyttöoikeuksia roolien avulla. Sen sijaan, että antaisit jollekulle "pääsyn kaikkialle", myönnät täsmällisen roolin tiettyyn resurssiin:

```
Kuka saa tehdä mitä mihin:
──────────────────────────────────────────────────────────
  KUKA            ROOLI                    MIHIN
  ─────           ─────────────────────    ─────────────
  App Service  →  Key Vault Secrets User → Vault: my-kv
  App Service  →  Storage Blob Data Reader→ Storage: myfiles
  Kehittäjä    →  Contributor             → Resurssiryhmä: rg-dev
```

### Roolit Key Vault -käyttöön

| Rooli | Mitä sallii | Milloin käytetään |
|-------|-------------|-------------------|
| **Key Vault Secrets User** | Lukea salaisuuksia | Tuotantosovellus — riittää lähes aina |
| **Key Vault Secrets Officer** | Lukea, luoda, päivittää ja poistaa | Sovellus, joka myös tallentaa salaisuuksia |
| **Key Vault Reader** | Lukea metadataa — **ei** salaisuuksien arvoja | Auditointityökalut |
| **Key Vault Administrator** | Kaikki oikeudet | Vain ylläpitäjille |

> **Tärkeä periaate — Least Privilege:** Myönnä aina **pienin mahdollinen oikeus**. Jos sovellus vain lukee salaisuuksia, anna `Key Vault Secrets User` — ei enempää. Jos identiteetti varastetaan tai väärinkäytetään, vahingot jäävät minimaalisiksi.

### Vaihtoehto A: Azure CLI

```bash
# 1. Hae Key Vaultin yksilöllinen resurssi-ID
$KV_ID = az keyvault show \
  --name $KV_NAME \
  --query id \
  --output tsv

# 2. Myönnä Key Vault Secrets User -rooli App Servicen identiteetille
az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

`--scope $KV_ID` tarkoittaa: oikeus myönnetään **vain tähän Key Vaultiin**, ei muihin resursseihin.

### Vaihtoehto B: Azure Portal

1. Avaa **Key Vault** Portalissa
2. Vasemmassa valikossa: **Access control (IAM)**
3. Klikkaa **+ Add** → **Add role assignment**
4. **Role**-välilehdellä:
   - Etsi hakukenttään `Key Vault Secrets User`
   - Valitse se listasta → klikkaa **Next**
5. **Members**-välilehdellä:
   - **Assign access to**: valitse **Managed identity**
   - Klikkaa **+ Select members**
   - **Subscription**: valitse oma tilauksesi
   - **Managed identity**: valitse **App Service**
   - Valitse listasta oma App Servicesi → **Select**
6. Klikkaa **Review + assign** → **Review + assign**

> **Huom:** Roolimuutos ei tule heti voimaan. Odota **1–5 minuuttia** ennen kuin testaat sovellusta.

---

## Vaihe 3 — DefaultAzureCredential koodissa

Kun identiteetti on aktivoitu ja oikeudet myönnetty, koodi voi hakea salaisuuksia. Tähän käytetään `DefaultAzureCredential`-luokkaa `Azure.Identity`-paketista.

### Mitä DefaultAzureCredential tekee?

`DefaultAzureCredential` on älykkäinen luokka, joka **selvittää automaattisesti miten autentikoitua** ympäristön perusteella:

```
Azuressa (App Service):
  → Käyttää Managed Identityä automaattisesti ✅

Kehityskoneella:
  → Käyttää az login -kirjautumistasi ✅

Molemmissa tapauksissa koodi on täsmälleen sama.
```

Tämä tarkoittaa, että kirjoitat koodin kerran — eikä sitä tarvitse muuttaa kehityskoneen ja tuotannon välillä.

### NuGet-paketit

```bash
dotnet add package Azure.Identity
dotnet add package Azure.Security.KeyVault.Secrets
```

### Perusesimerkki — salaisuuden lukeminen

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var client = new SecretClient(
    vaultUri: new Uri("https://my-keyvault.vault.azure.net/"),
    credential: new DefaultAzureCredential());

// Hae salaisuus nimellä
KeyVaultSecret secret = await client.GetSecretAsync("weather-api-secret");

// secret.Value.Value sisältää salaisuuden arvon
Console.WriteLine(secret.Value.Value);
```

### ASP.NET Core -sovelluksessa (IOptions + DI)

Rekisteröi `SecretClient` kerran `Program.cs`:ssä, jolloin se on injektoitavissa kaikkialle:

```csharp
// Program.cs
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using WeatherApi;

var builder = WebApplication.CreateBuilder(args);

// Key Vault URL tulee konfiguraatiosta (User Secrets kehityksessä,
// App Service Application Settings tuotannossa)
builder.Services.Configure<KeyVaultOptions>(
    builder.Configuration.GetSection(KeyVaultOptions.SectionName));

// Rekisteröi SecretClient — luodaan kerran, jaetaan kaikille
builder.Services.AddSingleton(serviceProvider =>
{
    var options = serviceProvider
        .GetRequiredService<IOptions<KeyVaultOptions>>().Value;

    if (string.IsNullOrEmpty(options.VaultUrl))
        throw new InvalidOperationException("KeyVault:VaultUrl ei ole asetettu.");

    return new SecretClient(
        new Uri(options.VaultUrl),
        new DefaultAzureCredential());
});
```

```csharp
// Controller tai palvelu — injektoi SecretClient suoraan
[ApiController]
[Route("[controller]")]
public class KeyVaultController : ControllerBase
{
    private readonly SecretClient _secretClient;

    public KeyVaultController(SecretClient secretClient)
    {
        _secretClient = secretClient;
    }

    [HttpGet("secret")]
    public async Task<IActionResult> GetSecret()
    {
        var secret = await _secretClient.GetSecretAsync("weather-api-secret");

        return Ok(new
        {
            Source = "Azure Key Vault",
            SecretName = secret.Value.Name,
            ValuePreview = secret.Value.Value[..4] + "***",
            Version = secret.Value.Properties.Version
        });
    }
}
```

---

## Paikallinen kehitys

Kehityskoneella ei ole Managed Identityä — mutta `DefaultAzureCredential` osaa käyttää sen sijaan **Azure CLI -kirjautumistasi**. Sama koodi toimii ilman muutoksia.

### 1. Kirjaudu Azure CLI:llä

```bash
az login
# Valitse oikea tilaus jos sinulla on useita
az account set --subscription "<tilauksesi nimi tai ID>"
```

### 2. Myönnä itsellesi Key Vault -oikeudet

Kehityskoneella sinä olet se "identiteetti" joka lukee salaisuuksia — sinulle täytyy myöntää sama rooli kuin App Servicelle on myönnetty Azuressa.

```bash
# Hae oman Azure-tilisi Object ID
$MY_ID = az ad signed-in-user show --query id --output tsv

# Myönnä Key Vault Secrets User -rooli omalle tilillesi
az role assignment create \
  --assignee $MY_ID \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

### 3. Aseta Key Vault URL User Secretsiin

Kehityskoneella Key Vault -URL tulee User Secretsistä, Azuressa se tulee Application Settingsistä:

```bash
dotnet user-secrets set "KeyVault:VaultUrl" "https://my-keyvault.vault.azure.net/"
```

Nyt `DefaultAzureCredential` toimii automaattisesti:

```
Kehityskoneella:   DefaultAzureCredential → az login -identiteetti → Key Vault
Azuressa:          DefaultAzureCredential → Managed Identity        → Key Vault
```

> **Miksi tämä on siisti?** Sinun ei tarvitse ylläpitää kahta eri koodihaaraa — kehitys ja tuotanto käyttävät täsmälleen samaa koodia. Ympäristö ratkaisee autentikointitavan automaattisesti.

---

## Miten se toimii taustalla?

Tämä osio selittää mitä kulissien takana tapahtuu. **Se ei ole pakollista lukemista** — voit käyttää Managed Identityä ilman tätä tietoa — mutta se auttaa ymmärtämään miksi ratkaisu on turvallinen.

### Token-pohjainen autentikointi

Managed Identity perustuu lyhytikäisiin **access tokeneihin** (pääsytokeneihin). Token on digitaalisesti allekirjoitettu todiste siitä, kuka olet ja mitä saat tehdä — kuin digitaalinen kulkulupa.

```
Mitä tapahtuu kun koodi kutsuu GetSecretAsync():

  1. DefaultAzureCredential huomaa olevansa Azure App Servicessa

  2. Se pyytää access tokenin Azuren sisäiseltä palvelulta
     (Azure Instance Metadata Service)

  3. Azure palauttaa lyhytikäisen tokenin (~1 tunti voimassa)
     Token sisältää mm: "Olen App Service X, tenant Y"

  4. SecretClient lähettää pyynnön Key Vaultille tokenin kanssa

  5. Key Vault tarkistaa tokenin aitouden (Azure on allekirjoittanut sen)
     ja tarkistaa RBAC: "Onko tällä identiteetillä Key Vault Secrets User -rooli?"

  6. Jos kaikki ok → salaisuus palautetaan
     Jos ei oikeuksia → 403 Forbidden

  7. DefaultAzureCredential uusii tokenin automaattisesti ennen vanhenemista
```

**Miksi tämä on turvallisempaa kuin salasana:**
- Tokenilla on lyhyt voimassaoloaika — vaikka se vuotaisi, se vanhenee pian
- Tokenia ei tallenneta mihinkään — se haetaan tarvittaessa
- Azure allekirjoittaa tokenin — sitä ei voi väärentää

### DefaultAzureCredentialin autentikointiketju

`DefaultAzureCredential` käy läpi seuraavan listan järjestyksessä ja käyttää ensimmäistä toimivaa tapaa:

```
Järjestys    Tapa                         Milloin aktivoituu
─────────    ────────────────────────     ────────────────────────────────
1.           EnvironmentCredential        Kun AZURE_CLIENT_ID jne. on asetettu
2.           WorkloadIdentityCredential   Kubernetes-ympäristö
3.           ManagedIdentityCredential    ← Azure App Service, VM, Functions
4.           SharedTokenCacheCredential   Visual Studio (Windows)
5.           VisualStudioCodeCredential   VS Code Azure-laajennus
6.           AzureCliCredential           ← az login (kehityskone)
7.           AzurePowerShellCredential    Connect-AzAccount
8.           AzureDeveloperCliCredential  azd login
             ─────────────────────────────────────────────────────────────
             Jos mikään ei onnistu → AuthenticationFailedException
```

Käytännössä sinulle oleelliset ovat **kohta 3** (tuotanto Azuressa) ja **kohta 6** (kehityskone).

---

## System-assigned vs. User-assigned

Managed Identityä on kahta tyyppiä. Aloittelijalle **System-assigned on oikea valinta** — se on yksinkertaisempi ja riittää useimpiin tilanteisiin.

### System-assigned (suositeltu aloittelijoille)

Identiteetti on sidottu yhteen resurssiin ja poistetaan automaattisesti kun resurssi poistetaan.

```
┌──────────────────────────────────┐
│  App Service: my-weatherapi      │
│                                  │
│  System-assigned identity:       │
│  Object ID: a1b2c3d4-e5f6-...   │
│                                  │
│  ✅ Luodaan automaattisesti      │
│  ✅ Poistetaan resurssin mukana  │
│  ✅ Ei erillisiä resursseja      │
└──────────────────────────────────┘
```

**Käytä kun:** Yhdellä sovelluksella on pääsy tiettyihin resursseihin. Tämä kattaa suurimman osan tilanteista.

### User-assigned (edistyneempi)

Identiteetti on itsenäinen Azure-resurssi, jonka voi liittää useampaan sovellukseen.

```
┌─────────────────────────────┐
│  Managed Identity: mi-myapp │  ← Itsenäinen resurssi
│  Object ID: f1e2d3c4-...    │
└──────────┬──────────────────┘
           │ liitetty molempiin
    ┌──────▼──────┐    ┌──────────────┐
    │  App Service│    │  Function App│
    │  my-api     │    │  my-worker   │
    └─────────────┘    └──────────────┘
```

**Käytä kun:** Usealla eri sovelluksella täytyy olla täsmälleen samat oikeudet samoihin resursseihin. Oikeuksia ei tarvitse myöntää erikseen jokaiselle.

| | System-assigned | User-assigned |
|-|-----------------|---------------|
| **Elinkaari** | Sidottu resurssiin | Itsenäinen |
| **Jakaminen** | Ei — yksi per resurssi | Kyllä — useille resursseille |
| **Monimutkaisuus** | Yksinkertainen | Monimutkaisempi |
| **Suositus** | Aloittelijat, yksinkertaiset projektit | Kun identiteetti jaetaan |

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä System-assigned Managed Identityä** yksinkertaisiin projekteihin — se on helppo ottaa käyttöön ja siivoutuu automaattisesti pois
- **Myönnä pienin mahdollinen oikeus** — `Key Vault Secrets User` riittää lukemiseen, älä anna `Key Vault Administrator` -roolia
- **Testaa paikallisesti `az login`-kirjautumisella** ennen kuin viet koodin Azureen — näin varmistat, että DefaultAzureCredential ja RBAC-oikeudet toimivat oikein
- **Käytä `DefaultAzureCredential`** — sama koodi toimii kehityskoneella ja tuotannossa ilman muutoksia
- **Tallenna Key Vault URL konfiguraatioon** (User Secrets kehityksessä, Application Settings Azuressa) — älä kovakoodaa sitä

### ❌ Vältä näitä

- Älä tallenna `client_id` + `client_secret` -pareja ympäristömuuttujiin Key Vault -yhteyttä varten — Managed Identity on juuri tätä varten olemassa
- Älä myönnä laajoja rooleja kuten `Owner` tai `Contributor` sovellukselle — rajoita oikeudet täsmälleen tarvittavaan resurssiin
- Älä unohda odottaa 1–5 minuuttia RBAC-muutosten jälkeen ennen testaamista

---

## Seuraavaksi

- [Azure Key Vault](Key-Vault.md) — Key Vault -palvelu ja sen käsitteet
- [Azure App Service](App-Service.md) — .NET-sovellusten isännöinti Azuressa
- [Azure Key Vault .NET-integraatio](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Key-Vault.md) — Koodiesimerkit Key Vault + Managed Identity

## Takaisin

- [Azure-palvelut — Yleiskatsaus](README.md)
