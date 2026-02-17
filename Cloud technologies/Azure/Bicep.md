# Bicep - Azuren IaC-kieli

## Sisällysluettelo

1. [Mikä on Bicep?](#mikä-on-bicep)
2. [Kehitysympäristön pystytys](#kehitysympäristön-pystytys)
3. [Bicepin syntaksi](#bicepin-syntaksi)
4. [Tyypit ja dekoraattorit](#tyypit-ja-dekoraattorit)
5. [Resurssien väliset riippuvuudet](#resurssien-väliset-riippuvuudet)
6. [Olemassa oleviin resursseihin viittaaminen](#olemassa-oleviin-resursseihin-viittaaminen)
7. [Scope ja deployment-tasot](#scope-ja-deployment-tasot)
8. [Moduulit syventävästi](#moduulit-syventävästi)
9. [Bicep-funktiot](#bicep-funktiot)
10. [User-Defined Types](#user-defined-types)
11. [Testaaminen ja validointi](#testaaminen-ja-validointi)
12. [Yleiset kuviot (patterns)](#yleiset-kuviot-patterns)
13. [Virheenkorjaus (troubleshooting)](#virheenkorjaus-troubleshooting)

---

## Mikä on Bicep?

**Bicep** on Azuren domain-specific language (DSL), joka on kehitetty korvaamaan ARM JSON -templatet helpommin luettavalla ja kirjoitettavalla syntaksilla. Bicep kääntyy taustalla ARM JSON -muotoon.

> Katso IaC:n perusteet ja Bicepin perusesimerkit: [Infrastructure as Code](Infrastructure-as-Code.md)

Tämä sivu keskittyy Bicepin **edistyneempiin ominaisuuksiin** ja käytännön kuvioihin.

---

## Kehitysympäristön pystytys

### Tarvittavat työkalut

```bash
# 1. Asenna Azure CLI
# Windows (winget):
winget install Microsoft.AzureCLI

# macOS:
brew install azure-cli

# 2. Asenna Bicep (tulee Azure CLI:n mukana, mutta varmista uusin versio)
az bicep install
az bicep upgrade

# 3. Tarkista versiot
az --version
az bicep version
```

### VS Code -laajennus

Asenna **Bicep-laajennus** VS Codeen:

- Nimi: **Bicep** (Microsoft)
- Extension ID: `ms-azuretools.vscode-bicep`

Laajennus tarjoaa:

| Ominaisuus | Kuvaus |
|---|---|
| **IntelliSense** | Automaattitäydennys resursseille ja ominaisuuksille |
| **Validointi** | Reaaliaikainen virheiden tarkistus |
| **Hover info** | Tietoa resurssityypeistä hoverin alla |
| **Go to definition** | Navigointi moduuleihin ja parametreihin |
| **Refactoring** | Arvon muuttaminen parametriksi, muuttujaksi tai moduuliksi |
| **Visualisointi** | Graafinen näkymä resursseista ja riippuvuuksista |

---

## Bicepin syntaksi

### Resurssimäärittely yksityiskohtaisesti

```bicep
// Perusresurssi
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stmyapp'               // Resurssin nimi Azuressa (globaalisti uniikki)
  location: resourceGroup().location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {                  // Resurssikohtaiset asetukset
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
  }
  tags: {                        // Metatiedot
    Environment: 'dev'
  }
}
```

Resurssimäärittelyn osat:

```
resource <symbolinenNimi> '<tyyppi>@<apiVersio>' = {
  │         │                │          │
  │         │                │          └─ Azure API -versio (päivämäärä)
  │         │                └─ Resurssin täysi tyyppinimi
  │         └─ Nimi, jolla resurssiin viitataan Bicep-koodissa
  └─ Avainsana
}
```

### Lapsiresurssit (child resources)

Lapsiresursseja voi määritellä kahdella tavalla:

```bicep
// Tapa 1: Sisäkkäin (nested)
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stmyapp'
  location: resourceGroup().location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'

  // Blob-palvelu on Storage Accountin lapsi
  resource blobService 'blobServices' = {
    name: 'default'

    // Container on Blob-palvelun lapsi
    resource container 'containers' = {
      name: 'documents'
      properties: {
        publicAccess: 'None'
      }
    }
  }
}

// Tapa 2: Parent-property (selkeämpi suurissa tiedostoissa)
resource storageAccount2 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'stmyapp2'
  location: resourceGroup().location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount2
  name: 'default'
}

resource container 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobService
  name: 'documents'
  properties: {
    publicAccess: 'None'
  }
}
```

---

## Tyypit ja dekoraattorit

### Parametrityypit

```bicep
// Perustyypit
param myString string
param myInt int
param myBool bool
param myArray array
param myObject object

// Tyypitetty taulukko
param vmNames string[]

// Tyypitetty objekti
param networkConfig {
  vnetName: string
  subnetName: string
  addressPrefix: string
}
```

### Dekoraattorit

Dekoraattorit lisäävät parametreille ja muuttujille sääntöjä ja metatietoja:

```bicep
// Kuvaus (näkyy deploymentissa ja dokumentaatiossa)
@description('Sovelluksen nimi, käytetään resurssien nimeämisessä')
param appName string

// Sallitut arvot
@allowed(['dev', 'staging', 'prod'])
param environment string

// Pituusrajoitukset
@minLength(3)
@maxLength(24)
param storageAccountName string

// Arvorajoitukset
@minValue(1)
@maxValue(10)
param instanceCount int = 1

// Turvallinen parametri (ei näy lokeissa eikä deployment-historiassa)
@secure()
param adminPassword string

// Metadata
@metadata({
  example: 'myapp'
  impact: 'Käytetään kaikkien resurssien nimissä'
})
param projectName string
```

---

## Resurssien väliset riippuvuudet

### Implisiittiset riippuvuudet (suositeltu)

Bicep osaa tunnistaa riippuvuudet automaattisesti, kun viittaat toisen resurssin ominaisuuteen:

```bicep
// App Service Plan luodaan ensin
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'asp-myapp'
  location: resourceGroup().location
  sku: { name: 'S1' }
}

// Web App luodaan vasta kun Plan on valmis (implisiittinen riippuvuus)
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: 'app-myapp'
  location: resourceGroup().location
  properties: {
    serverFarmId: appServicePlan.id    // ← Tämä viittaus luo riippuvuuden
  }
}
```

### Eksplisiittiset riippuvuudet

Joskus riippuvuutta ei voi päätellä viittauksista:

```bicep
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, webApp.id)
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'
    )
    principalId: webApp.identity.principalId
  }
  dependsOn: [
    keyVault        // ← Eksplisiittinen riippuvuus
  ]
}
```

```
Riippuvuusketju:

  App Service Plan ──→ Web App ──→ Role Assignment
                                        │
                       Key Vault ────────┘

  Bicep/ARM ratkaisee oikean luontijärjestyksen automaattisesti.
```

---

## Olemassa oleviin resursseihin viittaaminen

### `existing`-avainsana

Kun haluat viitata resurssiin, joka on jo olemassa Azuressa (etkä luo sitä uudelleen):

```bicep
// Viittaa olemassa olevaan Key Vaultiin samassa resource groupissa
resource existingKeyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: 'kv-myapp-prod'
}

// Käytä sitä toisessa resurssissa
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: 'app-myapp'
  location: resourceGroup().location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'KeyVaultUri'
          value: existingKeyVault.properties.vaultUri   // Lue arvo olemassa olevasta
        }
      ]
    }
  }
}

// Viittaa resurssiin toisessa resource groupissa
resource existingVnet 'Microsoft.Network/virtualNetworks@2023-11-01' existing = {
  name: 'vnet-shared'
  scope: resourceGroup('rg-networking')   // Eri resource group
}
```

---

## Scope ja deployment-tasot

Azure tukee neljää deployment-tasoa:

```
┌─────────────────────────────────────────┐
│  Management Group                       │  targetScope = 'managementGroup'
│  ┌───────────────────────────────────┐  │
│  │  Subscription                     │  │  targetScope = 'subscription'
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Resource Group             │  │  │  targetScope = 'resourceGroup' (oletus)
│  │  │  ┌───────────────────────┐  │  │  │
│  │  │  │  Resources            │  │  │  │
│  │  │  └───────────────────────┘  │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

```bicep
// Subscription-tason deployment (esim. Resource Groupien luonti)
targetScope = 'subscription'

resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-myapp-dev'
  location: 'northeurope'
}

// Moduuli kohdistetaan luotuun Resource Groupiin
module resources 'modules/resources.bicep' = {
  name: 'resourcesDeployment'
  scope: rg    // ← Tärkeä: määrittää kohteen
  params: {
    location: rg.location
  }
}
```

### Deployment-komennot tason mukaan

```bash
# Resource Group -taso (oletus)
az deployment group create \
  --resource-group rg-myapp-dev \
  --template-file main.bicep

# Subscription-taso
az deployment sub create \
  --location northeurope \
  --template-file main.bicep

# Management Group -taso
az deployment mg create \
  --management-group-id myMgGroup \
  --location northeurope \
  --template-file main.bicep
```

---

## Moduulit syventävästi

### Moduulin anatomia

Moduuli on tavallinen `.bicep`-tiedosto, jota kutsutaan toisesta tiedostosta:

```bicep
// modules/appservice.bicep

// SYÖTTEET: Mitä moduuli tarvitsee
param location string
param appName string
param environment string
param appServicePlanId string

// RESURSSIT: Mitä moduuli luo
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: 'app-${appName}-${environment}'
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
  }
}

// TULOSTEET: Mitä moduuli palauttaa kutsujalle
output webAppName string = webApp.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output principalId string = webApp.identity.principalId
```

### Moduulien ketjuttaminen

```bicep
// main.bicep - Moduulit viittaavat toistensa tulosteisiin

module plan 'modules/plan.bicep' = {
  name: 'planDeployment'
  scope: rg
  params: {
    location: location
    appName: appName
  }
}

module app 'modules/appservice.bicep' = {
  name: 'appDeployment'
  scope: rg
  params: {
    location: location
    appName: appName
    environment: environment
    appServicePlanId: plan.outputs.planId   // ← Ketjutus tulosteella
  }
}

module kvAccess 'modules/kv-access.bicep' = {
  name: 'kvAccessDeployment'
  scope: rg
  params: {
    keyVaultName: kv.outputs.keyVaultName
    principalId: app.outputs.principalId   // ← Toinen ketjutus
  }
}
```

### Ehdolliset moduulit

```bicep
param deployRedis bool = false
param deployMonitoring bool = true

module redis 'modules/redis.bicep' = if (deployRedis) {
  name: 'redisDeployment'
  scope: rg
  params: {
    location: location
  }
}

module monitoring 'modules/monitoring.bicep' = if (deployMonitoring) {
  name: 'monitoringDeployment'
  scope: rg
  params: {
    location: location
    webAppName: app.outputs.webAppName
  }
}
```

---

## Bicep-funktiot

### Yleisimmät funktiot

```bicep
// ─── Resurssifunktiot ───

resourceGroup().location        // Resource Groupin sijainti
subscription().subscriptionId   // Subscription ID
subscription().tenantId         // Tenant ID
tenant().tenantId               // Sama kuin yllä (tenant-scopessa)

// ─── Merkkijonofunktiot ───

toLower('MyApp')                        // 'myapp'
toUpper('myapp')                        // 'MYAPP'
replace('hello-world', '-', '_')        // 'hello_world'
substring('hello', 0, 3)               // 'hel'
'${appName}-${environment}'             // Merkkijonointerpolaatio

// ─── Uniikkiarvot ───

uniqueString(resourceGroup().id)        // Deterministinen hash (13 merkkiä)
// Esim: 'a3kxc5m7nop2q'
// Sama input → sama output, aina

guid(resourceGroup().id, 'myApp')       // Deterministinen GUID
// Esim: '8b5a3c7d-1e2f-4a5b-9c8d-0e1f2a3b4c5d'

// ─── Taulukko- ja objektifunktiot ───

length(['a', 'b', 'c'])                // 3
contains(['dev', 'prod'], 'dev')        // true
union({ a: 1 }, { b: 2 })              // { a: 1, b: 2 }
empty([])                               // true

// ─── Resurssi-ID:t ───

// Resurssi-ID samasta scopesta
storageAccount.id

// Subscription-tason resurssi-ID
subscriptionResourceId(
  'Microsoft.Authorization/roleDefinitions',
  '4633458b-17de-408a-b874-0445c86b69e6'
)

// Resurssi-ID toisesta resource groupista
resourceId('rg-shared', 'Microsoft.Network/virtualNetworks', 'vnet-shared')
```

### Ehtolausekkeet

```bicep
// Ternary-operaattori
var skuName = environment == 'prod' ? 'S1' : 'F1'
var replication = environment == 'prod' ? 'Standard_ZRS' : 'Standard_LRS'

// Monivaiheinen ehto
var skuTier = environment == 'prod' ? 'P1v3' : environment == 'staging' ? 'S1' : 'F1'
```

---

## User-Defined Types

Bicep tukee omien tyyppimääritysten luontia, joka parantaa parametrien validointia:

```bicep
// Oma tyyppi: ympäristökonfiguraatio
type environmentConfig = {
  @description('Ympäristön nimi')
  name: 'dev' | 'staging' | 'prod'

  @description('App Service Plan SKU')
  sku: 'F1' | 'B1' | 'S1' | 'P1v3'

  @description('Instanssien määrä')
  @minValue(1)
  @maxValue(10)
  instanceCount: int

  @description('Onko ympäristö tuotantoympäristö')
  isProduction: bool
}

// Käyttö parametrina
param config environmentConfig

// Käyttö resurssissa
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'asp-myapp-${config.name}'
  location: resourceGroup().location
  sku: {
    name: config.sku
    capacity: config.instanceCount
  }
}

// Oma tyyppi: tagi-objekti
type resourceTags = {
  Environment: string
  Application: string
  ManagedBy: 'Bicep' | 'Terraform' | 'Manual'
  CostCenter: string?    // ? = valinnainen
}
```

---

## Testaaminen ja validointi

### Bicep Linter

Bicep sisältää sisäänrakennetun linterin, joka tarkistaa parhaita käytäntöjä:

```bash
# Tarkista tiedoston syntaksi ja best practices
az bicep build --file main.bicep

# Vain validointi (ei luo ARM JSON:ia)
az bicep lint --file main.bicep
```

### Linter-asetukset (`bicepconfig.json`)

```json
{
  "analyzers": {
    "core": {
      "rules": {
        "no-hardcoded-location": {
          "level": "error"
        },
        "no-unused-params": {
          "level": "warning"
        },
        "prefer-interpolation": {
          "level": "warning"
        },
        "secure-parameter-default": {
          "level": "error"
        },
        "use-resource-id-functions": {
          "level": "warning"
        }
      }
    }
  }
}
```

### Preflight-validointi

```bash
# Tarkista template ilman deploymenttia
az deployment group validate \
  --resource-group rg-myapp-dev \
  --template-file main.bicep \
  --parameters main.bicepparam

# What-if: näytä muutokset ilman deploymenttia
az deployment group what-if \
  --resource-group rg-myapp-dev \
  --template-file main.bicep \
  --parameters main.bicepparam
```

---

## Yleiset kuviot (patterns)

### Kuvio 1: Nimeämismoduuli

```bicep
// modules/naming.bicep - Keskitetty nimeäminen

param appName string
param environment string

var sanitizedAppName = toLower(replace(appName, '-', ''))

output names object = {
  resourceGroup: 'rg-${appName}-${environment}'
  appServicePlan: 'asp-${appName}-${environment}'
  webApp: 'app-${appName}-${environment}'
  keyVault: 'kv-${appName}-${environment}'
  storage: 'st${sanitizedAppName}${environment}'
  sqlServer: 'sql-${appName}-${environment}'
  sqlDatabase: 'db-${appName}-${environment}'
  logAnalytics: 'log-${appName}-${environment}'
}
```

```bicep
// main.bicep - Käyttö
module naming 'modules/naming.bicep' = {
  name: 'namingDeployment'
  params: {
    appName: appName
    environment: environment
  }
}

// Käytä nimiä muissa moduuleissa
module kv 'modules/keyvault.bicep' = {
  scope: rg
  name: 'kvDeployment'
  params: {
    keyVaultName: naming.outputs.names.keyVault   // ← Keskitetty nimi
  }
}
```

### Kuvio 2: Tagi-standardi

```bicep
// Yhteiset tagit kaikille resursseille
var commonTags = {
  Application: appName
  Environment: environment
  ManagedBy: 'Bicep'
  DeployedAt: utcNow()   // Deployment-ajankohta (huom: aiheuttaa aina muutoksen)
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: naming.outputs.names.storage
  location: location
  tags: union(commonTags, {
    DataClassification: 'Internal'   // Resurssikohtainen tagi
  })
  // ...
}
```

### Kuvio 3: Ympäristökohtainen konfiguraatio

```bicep
@allowed(['dev', 'staging', 'prod'])
param environment string

// Ympäristökohtaiset asetukset yhdessä paikassa
var envConfig = {
  dev: {
    appServiceSku: 'F1'
    sqlSku: 'Basic'
    storageSku: 'Standard_LRS'
    alwaysOn: false
    minInstances: 1
  }
  staging: {
    appServiceSku: 'S1'
    sqlSku: 'S0'
    storageSku: 'Standard_LRS'
    alwaysOn: true
    minInstances: 1
  }
  prod: {
    appServiceSku: 'P1v3'
    sqlSku: 'S1'
    storageSku: 'Standard_ZRS'
    alwaysOn: true
    minInstances: 2
  }
}

// Käyttö
var config = envConfig[environment]

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'asp-myapp-${environment}'
  location: location
  sku: {
    name: config.appServiceSku
  }
}
```

### Kuvio 4: Monitorointi (Log Analytics + Application Insights)

```bicep
// modules/monitoring.bicep

param location string
param appName string
param environment string

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-${appName}-${environment}'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: environment == 'prod' ? 90 : 30
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'ai-${appName}-${environment}'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
    RetentionInDays: environment == 'prod' ? 90 : 30
  }
}

output logAnalyticsId string = logAnalytics.id
output appInsightsConnectionString string = appInsights.properties.ConnectionString
output appInsightsInstrumentationKey string = appInsights.properties.InstrumentationKey
```

---

## Virheenkorjaus (troubleshooting)

### Yleisimmät virheet

| Virhe | Syy | Ratkaisu |
|---|---|---|
| `InvalidTemplateDeployment` | Resurssin validointi epäonnistui | Tarkista resurssien parametrit ja rajoitukset |
| `DeploymentFailed` | Yksi tai useampi resurssi epäonnistui | Lue tarkat virheviestit `az deployment group show` |
| `ResourceNotFound` | Viitattu resurssia ei löydy | Tarkista `existing`-viittaukset ja riippuvuudet |
| `AuthorizationFailed` | Käyttöoikeus puuttuu | Tarkista RBAC-roolit |
| `AccountNameInvalid` | Nimen formaatti väärä | Tarkista Azuren nimeämissäännöt (esim. storage: vain pienet kirjaimet) |
| `Conflict` | Resurssi on lukittu tai tilassa joka estää muutoksen | Tarkista resource lockit ja resurssin tila |

### Hyödylliset komennot

```bash
# Näytä viimeisen deploymentin tiedot
az deployment group show \
  --resource-group rg-myapp-dev \
  --name myDeployment

# Listaa kaikki deploymentit
az deployment group list \
  --resource-group rg-myapp-dev \
  --output table

# Näytä deployment-operaatiot (yksityiskohtaiset virheet)
az deployment operation group list \
  --resource-group rg-myapp-dev \
  --name myDeployment \
  --output table

# Käännä Bicep ARM JSON:iksi (tarkistaa syntaksin)
az bicep build --file main.bicep --stdout

# Decompile ARM JSON Bicepiksi (migraatio)
az bicep decompile --file template.json
```

---

## Takaisin

- [Infrastructure as Code](Infrastructure-as-Code.md)
- [Azure-palvelut](README.md)

## Hyödyllisiä linkkejä

- [Bicep Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/)
- [Bicep Playground](https://aka.ms/bicepdemo)
- [Bicep Examples (GitHub)](https://github.com/Azure/bicep/tree/main/docs/examples)
- [Azure Verified Modules](https://aka.ms/avm)
- [Bicep VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)
- [Azure Resource Reference](https://learn.microsoft.com/en-us/azure/templates/)
- [Bicep Linter Rules](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/linter)
