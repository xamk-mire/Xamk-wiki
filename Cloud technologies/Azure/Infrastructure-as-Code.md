# Infrastructure as Code (IaC)

## Sisällysluettelo

1. [Mikä on Infrastructure as Code?](#mikä-on-infrastructure-as-code)
2. [Miksi IaC?](#miksi-iac)
3. [IaC-lähestymistavat](#iac-lähestymistavat)
4. [IaC-työkalut Azuressa](#iac-työkalut-azuressa)
5. [Mikä on Bicep?](#mikä-on-bicep)
6. [Bicep vs. ARM-template](#bicep-vs-arm-template)
7. [Bicepin perusteet](#bicepin-perusteet)
8. [Käytännön esimerkit Bicepillä](#käytännön-esimerkit-bicepillä)
9. [Parametrit ja muuttujat](#parametrit-ja-muuttujat)
10. [Moduulit](#moduulit)
11. [IaC:n parhaat käytännöt](#iacn-parhaat-käytännöt)
12. [Deployment (käyttöönotto)](#deployment-käyttöönotto)

---

## Mikä on Infrastructure as Code?

**Infrastructure as Code (IaC)** tarkoittaa infrastruktuurin (palvelimet, verkot, tietokannat, jne.) hallintaa ja provisiointia kooditiedostojen avulla, manuaalisten prosessien sijaan.

Perinteisesti infrastruktuuri luotiin käsin portaalin kautta tai suorittamalla komentoja yksitellen. IaC:n avulla koko ympäristö kuvataan koodina, jota voidaan **versioida**, **toistaa** ja **automatisoida**.

```
PERINTEINEN TAPA (❌):
┌─────────────┐     Klikkaa portaalissa      ┌──────────────┐
│  Kehittäjä  │ ──────────────────────────→  │ Azure Portal │
└─────────────┘   Manuaalinen, virhealtis    └──────────────┘
                  Ei toistettava
                  Ei versionhallinnassa

IaC-TAPA (✅):
┌─────────────┐     main.bicep      ┌─────────────┐     Deploy      ┌───────────┐
│  Kehittäjä  │ ─────────────────→ │     Git     │ ─────────────→ │   Azure   │
└─────────────┘  Koodi = Totuus     └─────────────┘  Automaattinen  └───────────┘
                 Versioitu                            Toistettava
                 Katselmoitava                        Luotettava
```

---

## Miksi IaC?

### Ongelmat ilman IaC:tä

| Ongelma | Kuvaus |
|---|---|
| **Konfiguraation ajautuminen (drift)** | Ympäristöt eroavat toisistaan, koska muutoksia on tehty käsin |
| **Dokumentaation puute** | Kukaan ei tiedä tarkalleen, mitä infrastruktuuri sisältää |
| **Ei toistettavuutta** | Uuden ympäristön luominen on työlästä ja virhealtista |
| **Ei auditointipolkua** | Ei tiedetä kuka muutti mitä ja milloin |
| **Hitaus** | Manuaalinen provisiointi kestää tuntikausia |

### IaC:n hyödyt

| Hyöty | Kuvaus |
|---|---|
| **Toistettavuus** | Sama koodi tuottaa aina saman ympäristön |
| **Versionhallinta** | Infrastruktuurin muutoshistoria Gitissä |
| **Automatisointi** | CI/CD-putki hoitaa käyttöönoton |
| **Itsepalveludokumentaatio** | Koodi on dokumentaatio |
| **Nopeus** | Ympäristö pystyssä minuuteissa |
| **Kustannuskontrolli** | Koodista näkee mitä resursseja on käytössä |
| **Katselmointi** | Infrastruktuurimuutokset pull requestiin kuin mikä tahansa koodimuutos |

---

## IaC-lähestymistavat

### Deklaratiivinen vs. imperatiivinen

IaC-työkaluissa on kaksi perustavaa lähestymistapaa:

```
DEKLARATIIVINEN ("Mitä haluan"):
─────────────────────────────────
"Haluan web-sovelluksen, jossa on App Service Plan (S1)
 ja Storage Account (LRS)"

→ Työkalu laskee itse mitä pitää tehdä

IMPERATIIVINEN ("Miten teen"):
──────────────────────────────
1. Luo Resource Group
2. Luo App Service Plan
3. Aseta SKU S1
4. Luo Web App
5. Luo Storage Account
6. Aseta replication LRS

→ Sinä kerrot jokaisen askeleen
```

| Ominaisuus | Deklaratiivinen | Imperatiivinen |
|---|---|---|
| **Kuvaa** | Halutun lopputilan | Askeleet tavoitteeseen |
| **Idempotenssi** | Sisäänrakennettu | Pitää toteuttaa itse |
| **Esimerkkityökalut** | Bicep, Terraform, ARM | Azure CLI -skriptit, Pulumi |
| **Oppimiskynnys** | Matalampi | Korkeampi |
| **Joustavuus** | Rajoitetumpi | Täysin vapaa |

> **Suositus:** Deklaratiivinen lähestymistapa (kuten Bicep) on suositeltava useimmissa tilanteissa. Se on yksinkertaisempi, turvallisempi ja helpompi ylläpitää.

### Idempotenssi

**Idempotenssi** on IaC:n keskeinen käsite: saman koodin suorittaminen useita kertoja tuottaa aina saman lopputuloksen.

```
1. suoritus: Luo Storage Account → ✅ Luotu
2. suoritus: Storage Account on jo olemassa → ✅ Ei muutoksia
3. suoritus: Storage Account on jo olemassa → ✅ Ei muutoksia

→ Turvallista ajaa uudelleen milloin tahansa!
```

---

## IaC-työkalut Azuressa

| Työkalu | Tyyppi | Kuvaus | Suositus |
|---|---|---|---|
| **Bicep** | Deklaratiivinen | Azuren oma DSL, kääntyy ARM-templateksi | ✅ Azure-natiivi valinta |
| **ARM Templates** | Deklaratiivinen | JSON-pohjainen, Azuren alkuperäinen IaC | ⚠️ Vanhentunut, käytä Bicepiä |
| **Terraform** | Deklaratiivinen | HashiCorpin monipilvityökalu (HCL-kieli) | ✅ Monipilvi-ympäristöt |
| **Pulumi** | Imperatiivinen | IaC oikeilla ohjelmointikielillä (C#, TS, Python) | ✅ Kehittäjäystävällinen |
| **Azure CLI** | Imperatiivinen | Komentorivityökalu, skriptattava | ⚠️ Ad hoc -tehtäviin |

> **Suositus:** Jos käytät pelkästään Azurea, **Bicep** on paras valinta. Jos käytät useita pilvipalveluita, harkitse **Terraformia**.

---

## Mikä on Bicep?

**Bicep** on Azuren oma **domain-specific language (DSL)** infrastruktuurin kuvaamiseen. Se on ARM-templatejen seuraaja, joka tarjoaa selkeämmän ja lyhyemmän syntaksin.

### Bicepin ominaisuudet

- **Azuren natiivi tuki** - tukee kaikkia Azure-resurssityyppejä heti niiden julkaisun jälkeen
- **Tyyppiturvallisuus** - IntelliSense ja validointi VS Code -laajennuksella
- **Moduulit** - Koodin uudelleenkäyttö moduuleilla
- **Ei tilanhallintatiedostoa (state)** - Toisin kuin Terraform, Bicep vertaa suoraan Azure-ympäristöön
- **Ilmainen ja avoimen lähdekoodin** - Microsoftin ylläpitämä

### Miten Bicep toimii?

```
┌──────────────┐    Käännös     ┌──────────────┐    Deploy     ┌───────────┐
│  main.bicep  │ ────────────→ │  ARM JSON    │ ──────────→  │   Azure   │
│  (helppo     │  bicep build   │  (Azure      │  Resource    │ Resources │
│   syntaksi)  │               │   ymmärtää)  │  Manager     │           │
└──────────────┘               └──────────────┘              └───────────┘
```

Bicep on **transpilaatiokieli**: kirjoitat Bicepiä, joka käännetään ARM JSON -templateksi. Azure Resource Manager vastaanottaa aina ARM JSON:n.

---

## Bicep vs. ARM-template

### Vertailu: Storage Account

**ARM Template (JSON) - 22 riviä:**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": {
      "type": "string",
      "defaultValue": "[resourceGroup().location]"
    }
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "apiVersion": "2023-01-01",
      "name": "myappstorage",
      "location": "[parameters('location')]",
      "sku": { "name": "Standard_LRS" },
      "kind": "StorageV2"
    }
  ]
}
```

**Bicep - 7 riviä:**

```bicep
param location string = resourceGroup().location

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: 'myappstorage'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}
```

| Ominaisuus | ARM Template | Bicep |
|---|---|---|
| **Syntaksi** | JSON (verbose) | Siisti DSL |
| **Rivimäärä** | ~3x enemmän | ~3x vähemmän |
| **IntelliSense** | Rajallinen | Erinomainen |
| **Moduulit** | Linked templates (monimutkainen) | Natiivit moduulit |
| **Oppimiskynnys** | Korkea | Matala |
| **Tuki** | Kaikki Azure-resurssit | Kaikki Azure-resurssit |

---

## Bicepin perusteet

### Resurssimäärittely

Bicepin perusyksikkö on **resurssi** (`resource`):

```bicep
resource <symbolinen-nimi> '<resurssi-tyyppi>@<api-versio>' = {
  name: '<resurssin-nimi-azuressa>'
  location: '<sijainti>'
  properties: {
    // Resurssikohtaiset asetukset
  }
}
```

### Parametrit (`param`)

Parametrit tekevät templatesta uudelleenkäytettävän:

```bicep
// Pakollinen parametri
param appName string

// Parametri oletusarvolla
param location string = resourceGroup().location

// Parametri rajoituksilla
@allowed(['dev', 'staging', 'prod'])
param environment string

// Parametri kuvauksella
@description('Storage Accountin SKU')
param storageSku string = 'Standard_LRS'

// Turvallinen parametri (ei näy lokeissa)
@secure()
param adminPassword string
```

### Muuttujat (`var`)

Muuttujat auttavat välttämään toistoa:

```bicep
param appName string
param environment string

// Muuttujat lasketaan parametreista
var resourceGroupName = 'rg-${appName}-${environment}'
var storageAccountName = 'st${appName}${environment}'
var tags = {
  Application: appName
  Environment: environment
  ManagedBy: 'Bicep'
}
```

### Tulosteet (`output`)

Tulosteet välittävät tietoa deploymentista:

```bicep
output storageAccountId string = storageAccount.id
output storageAccountName string = storageAccount.name
output primaryEndpoint string = storageAccount.properties.primaryEndpoints.blob
```

### Ehdollinen resurssien luonti

```bicep
param deployRedis bool = false

resource redis 'Microsoft.Cache/redis@2023-08-01' = if (deployRedis) {
  name: 'myapp-redis'
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0
    }
  }
}
```

### Silmukat (loops)

```bicep
param storageNames array = ['docs', 'images', 'backups']

resource storageAccounts 'Microsoft.Storage/storageAccounts@2023-01-01' = [
  for name in storageNames: {
    name: 'st${name}${uniqueString(resourceGroup().id)}'
    location: resourceGroup().location
    sku: { name: 'Standard_LRS' }
    kind: 'StorageV2'
  }
]
```

---

## Käytännön esimerkit Bicepillä

### Esimerkki 1: Resource Group + Storage Account

```bicep
// Tiedosto: main.bicep
// Kuvaus: Luo Resource Groupin ja Storage Accountin
targetScope = 'subscription'

param location string = 'northeurope'
param environment string = 'dev'

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-myapp-${environment}'
  location: location
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

// Storage Account (moduulina Resource Groupin sisällä)
module storage 'modules/storage.bicep' = {
  name: 'storageDeployment'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

output storageAccountName string = storage.outputs.storageAccountName
```

### Esimerkki 2: Key Vault + Salaisuudet

```bicep
// Tiedosto: keyvault.bicep
// Kuvaus: Luo Key Vaultin RBAC-tuella ja esimerkkisalaisuuden

param location string = resourceGroup().location
param environment string = 'dev'
param keyVaultName string = 'kv-myapp-${environment}'

@description('Pääkäyttäjän Object ID Azure AD:ssa')
param adminObjectId string

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      family: 'A'
      name: 'standard'
    }
    enableRbacAuthorization: true    // Käytä RBAC:ia Access Policyn sijaan
    enableSoftDelete: true
    softDeleteRetentionInDays: 90
    enablePurgeProtection: true      // Estä lopullinen poisto
    networkAcls: {
      defaultAction: 'Deny'
      bypass: 'AzureServices'        // Salli Azure-palveluiden pääsy
    }
  }
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

// Anna admin-käyttäjälle Key Vault Administrator -rooli
resource adminRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, adminObjectId, 'Key Vault Administrator')
  scope: keyVault
  properties: {
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '00482a5a-887f-4fb3-b363-3b7fe8e74483' // Key Vault Administrator
    )
    principalId: adminObjectId
    principalType: 'User'
  }
}

output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
```

### Esimerkki 3: App Service + App Service Plan

```bicep
// Tiedosto: appservice.bicep
// Kuvaus: Luo App Service Planin ja Web Appin .NET-sovellukselle

param location string = resourceGroup().location
param appName string
param environment string = 'dev'

@allowed(['F1', 'B1', 'S1', 'P1v3'])
@description('App Service Planin hintataso')
param skuName string = 'F1'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: 'asp-${appName}-${environment}'
  location: location
  sku: {
    name: skuName
  }
  kind: 'linux'
  properties: {
    reserved: true    // Linux
  }
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

// Web App
resource webApp 'Microsoft.Web/sites@2023-12-01' = {
  name: 'app-${appName}-${environment}'
  location: location
  identity: {
    type: 'SystemAssigned'  // Managed Identity Key Vaultia varten
  }
  properties: {
    serverFarmId: appServicePlan.id
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'DOTNETCORE|8.0'
      alwaysOn: skuName != 'F1'      // AlwaysOn ei tuettu ilmaisella tasolla
      minTlsVersion: '1.2'
      ftpsState: 'Disabled'
      appSettings: [
        {
          name: 'ASPNETCORE_ENVIRONMENT'
          value: environment == 'prod' ? 'Production' : 'Development'
        }
      ]
    }
  }
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

// Diagnostiikkalokit
resource webAppDiagnostics 'Microsoft.Web/sites/config@2023-12-01' = {
  parent: webApp
  name: 'logs'
  properties: {
    applicationLogs: {
      fileSystem: {
        level: 'Information'
      }
    }
    httpLogs: {
      fileSystem: {
        retentionInMb: 35
        retentionInDays: 3
        enabled: true
      }
    }
  }
}

output webAppName string = webApp.name
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output managedIdentityId string = webApp.identity.principalId
```

### Esimerkki 4: Kokonainen ympäristö (päätemplate)

```bicep
// Tiedosto: main.bicep
// Kuvaus: Kokonainen sovellusympäristö: App Service + Key Vault + Storage + SQL
targetScope = 'subscription'

@description('Sovelluksen nimi')
param appName string

@allowed(['dev', 'staging', 'prod'])
param environment string = 'dev'

param location string = 'northeurope'

@secure()
@description('SQL-tietokannan ylläpitäjän salasana')
param sqlAdminPassword string

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'rg-${appName}-${environment}'
  location: location
}

// Key Vault
module keyVault 'modules/keyvault.bicep' = {
  name: 'keyVaultDeployment'
  scope: rg
  params: {
    location: location
    environment: environment
    keyVaultName: 'kv-${appName}-${environment}'
    adminObjectId: '' // Täytä oma Object ID
  }
}

// Storage Account
module storage 'modules/storage.bicep' = {
  name: 'storageDeployment'
  scope: rg
  params: {
    location: location
    environment: environment
    storageAccountName: 'st${appName}${environment}'
  }
}

// App Service
module appService 'modules/appservice.bicep' = {
  name: 'appServiceDeployment'
  scope: rg
  params: {
    location: location
    appName: appName
    environment: environment
    skuName: environment == 'prod' ? 'S1' : 'F1'
  }
}

// Anna App Servicen Managed Identitylle Key Vault -lukuoikeus
module kvAccess 'modules/kv-role-assignment.bicep' = {
  name: 'kvAccessDeployment'
  scope: rg
  params: {
    keyVaultName: keyVault.outputs.keyVaultName
    principalId: appService.outputs.managedIdentityId
    roleName: 'Key Vault Secrets User'
  }
}

// Tulosteet
output resourceGroupName string = rg.name
output webAppUrl string = appService.outputs.webAppUrl
output keyVaultName string = keyVault.outputs.keyVaultName
```

### Esimerkki 5: SQL-tietokanta

```bicep
// Tiedosto: sql.bicep
// Kuvaus: Azure SQL Server + Database

param location string = resourceGroup().location
param appName string
param environment string = 'dev'

@secure()
param adminLogin string

@secure()
param adminPassword string

@allowed(['Basic', 'S0', 'S1', 'P1'])
param skuName string = 'Basic'

// SQL Server
resource sqlServer 'Microsoft.Sql/servers@2023-08-01-preview' = {
  name: 'sql-${appName}-${environment}'
  location: location
  properties: {
    administratorLogin: adminLogin
    administratorLoginPassword: adminPassword
    minimalTlsVersion: '1.2'
    publicNetworkAccess: environment == 'prod' ? 'Disabled' : 'Enabled'
  }
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

// SQL Database
resource sqlDatabase 'Microsoft.Sql/servers/databases@2023-08-01-preview' = {
  parent: sqlServer
  name: 'db-${appName}-${environment}'
  location: location
  sku: {
    name: skuName
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    maxSizeBytes: 2147483648 // 2 GB
    zoneRedundant: environment == 'prod'
  }
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

// Firewall: Salli Azure-palveluiden pääsy
resource firewallRule 'Microsoft.Sql/servers/firewallRules@2023-08-01-preview' = {
  parent: sqlServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
output databaseName string = sqlDatabase.name
```

---

## Parametrit ja muuttujat

### Parametritiedosto (`bicepparam`)

Parametrit voidaan erottaa erilliseen tiedostoon ympäristökohtaisesti:

```bicep
// Tiedosto: main.bicepparam (dev-ympäristö)
using 'main.bicep'

param appName = 'myapp'
param environment = 'dev'
param location = 'northeurope'
param sqlAdminPassword = readEnvironmentVariable('SQL_ADMIN_PASSWORD')
```

```bicep
// Tiedosto: main.prod.bicepparam (tuotantoympäristö)
using 'main.bicep'

param appName = 'myapp'
param environment = 'prod'
param location = 'northeurope'
param sqlAdminPassword = readEnvironmentVariable('SQL_ADMIN_PASSWORD')
```

### Nimeämisstrategia

Hyvä nimeämiskäytäntö helpottaa resurssien tunnistamista:

```bicep
// Nimeämismuuttujat
var naming = {
  resourceGroup: 'rg-${appName}-${environment}'
  appServicePlan: 'asp-${appName}-${environment}'
  webApp: 'app-${appName}-${environment}'
  keyVault: 'kv-${appName}-${environment}'
  storage: 'st${appName}${environment}'    // Ei väliviivoja (Azure-rajoitus)
  sqlServer: 'sql-${appName}-${environment}'
  sqlDatabase: 'db-${appName}-${environment}'
}
```

| Resurssi | Formaatti | Esimerkki |
|---|---|---|
| Resource Group | `rg-<app>-<env>` | `rg-myapp-dev` |
| App Service Plan | `asp-<app>-<env>` | `asp-myapp-dev` |
| Web App | `app-<app>-<env>` | `app-myapp-dev` |
| Key Vault | `kv-<app>-<env>` | `kv-myapp-dev` |
| Storage Account | `st<app><env>` | `stmyappdev` |
| SQL Server | `sql-<app>-<env>` | `sql-myapp-dev` |

> Nimeäminen perustuu [Azuren virallisiin suosituksiin](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming).

---

## Moduulit

### Moduulien rakenne

Moduulit mahdollistavat Bicep-koodin uudelleenkäytön ja organisoinnin:

```
infra/
├── main.bicep              # Päätemplate
├── main.bicepparam         # Dev-parametrit
├── main.prod.bicepparam    # Prod-parametrit
└── modules/
    ├── appservice.bicep    # App Service -moduuli
    ├── keyvault.bicep      # Key Vault -moduuli
    ├── storage.bicep       # Storage -moduuli
    ├── sql.bicep           # SQL -moduuli
    └── kv-role-assignment.bicep  # Roolimääritys-moduuli
```

### Moduulin kutsuminen

```bicep
// Päätemplatessa (main.bicep)
module storage 'modules/storage.bicep' = {
  name: 'storageDeployment'          // Deploymentin nimi
  scope: rg                          // Kohde-resource group
  params: {                          // Parametrit moduulille
    location: location
    environment: environment
    storageAccountName: naming.storage
  }
}

// Moduulin tulosteen käyttö
output storageName string = storage.outputs.storageAccountName
```

### Esimerkki moduulista: Storage Account

```bicep
// Tiedosto: modules/storage.bicep

param location string
param environment string
param storageAccountName string

@allowed(['Standard_LRS', 'Standard_GRS', 'Standard_ZRS'])
param skuName string = environment == 'prod' ? 'Standard_ZRS' : 'Standard_LRS'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: { name: skuName }
  kind: 'StorageV2'
  properties: {
    minimumTlsVersion: 'TLS1_2'
    allowBlobPublicAccess: false
    supportsHttpsTrafficOnly: true
    accessTier: 'Hot'
  }
  tags: {
    Environment: environment
    ManagedBy: 'Bicep'
  }
}

output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
output primaryBlobEndpoint string = storageAccount.properties.primaryEndpoints.blob
```

---

## IaC:n parhaat käytännöt

### ✅ Hyvät käytännöt

- **Versionhallinta** - Pidä kaikki IaC-koodi Gitissä
- **Ympäristökohtaiset parametrit** - Käytä eri parametritiedostoja (dev, staging, prod)
- **Moduulit** - Jaa koodi uudelleenkäytettäviin moduuleihin
- **Nimeämiskäytännöt** - Noudata yhdenmukaista nimeämistä (ks. yllä)
- **Tagit** - Lisää resursseihin tagit (Environment, ManagedBy, Owner)
- **Tarkista ennen deploymenttia** - Käytä `what-if`-komentoa muutosten esikatseluun
- **CI/CD** - Automatisoi käyttöönotto (GitHub Actions, Azure DevOps)
- **Älä muokkaa resursseja käsin** - Kaikki muutokset IaC:n kautta

### ❌ Vältä näitä

- Älä kovakoodaa arvoja - käytä parametreja ja muuttujia
- Älä ohita `what-if`-tarkistusta tuotannossa
- Älä säilytä salaisuuksia IaC-koodissa - käytä Key Vaultia tai ympäristömuuttujia
- Älä luo resursseja ilman tageja
- Älä tee suuria muutoksia kerralla - pienemmät muutokset ovat turvallisempia

---

## Deployment (käyttöönotto)

### Azure CLI

```bash
# 1. Kirjaudu sisään
az login

# 2. Valitse subscription
az account set --subscription "My Subscription"

# 3. Tarkista muutokset (what-if) - AINA ENSIN!
az deployment sub what-if \
  --location northeurope \
  --template-file main.bicep \
  --parameters main.bicepparam

# 4. Suorita deployment
az deployment sub create \
  --location northeurope \
  --template-file main.bicep \
  --parameters main.bicepparam \
  --name "deploy-$(date +%Y%m%d-%H%M%S)"
```

### Resource Group -tason deployment

```bash
# Jos targetScope on 'resourceGroup' (oletus)
az deployment group create \
  --resource-group rg-myapp-dev \
  --template-file appservice.bicep \
  --parameters appName='myapp' environment='dev'
```

### What-if -tarkistus

`what-if` näyttää mitä muutoksia deployment tekisi **ilman, että mitään oikeasti muutetaan**:

```bash
az deployment group what-if \
  --resource-group rg-myapp-dev \
  --template-file main.bicep \
  --parameters main.bicepparam
```

```
Tulostus:
  + Microsoft.Storage/storageAccounts  stmyappdev        [Luodaan]
  ~ Microsoft.Web/sites               app-myapp-dev      [Muokataan]
    - Microsoft.Cache/redis            myapp-redis        [Poistetaan]
```

### GitHub Actions -esimerkki

```yaml
# .github/workflows/deploy-infra.yml
name: Deploy Infrastructure

on:
  push:
    branches: [main]
    paths: ['infra/**']

permissions:
  id-token: write    # OIDC-autentikointi
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: What-If
        uses: azure/arm-deploy@v2
        with:
          scope: subscription
          region: northeurope
          template: infra/main.bicep
          parameters: infra/main.bicepparam
          additionalArguments: --what-if

      - name: Deploy
        uses: azure/arm-deploy@v2
        with:
          scope: subscription
          region: northeurope
          template: infra/main.bicep
          parameters: infra/main.bicepparam
          deploymentName: deploy-${{ github.run_number }}
```

---

## Yhteenveto

| Käsite | Kuvaus |
|---|---|
| **IaC** | Infrastruktuurin hallinta koodina |
| **Deklaratiivinen** | Kuvaa halutun lopputilan (Bicep, Terraform) |
| **Imperatiivinen** | Kuvaa askeleet tavoitteeseen (CLI-skriptit, Pulumi) |
| **Idempotenssi** | Sama koodi = sama tulos, aina |
| **Bicep** | Azuren oma IaC-kieli, ARM-templatejen seuraaja |
| **Moduulit** | Koodin uudelleenkäyttö ja organisointi |
| **What-if** | Muutosten esikatselu ennen käyttöönottoa |
| **Parametritiedosto** | Ympäristökohtaiset asetukset erillisessä tiedostossa |

---

## Takaisin

- [Azure-palvelut](README.md)

## Hyödyllisiä linkkejä

- [Bicep Documentation](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/)
- [Bicep Playground](https://aka.ms/bicepdemo) - Kokeile Bicepiä selaimessa
- [Azure Verified Modules](https://aka.ms/avm) - Valmiita, testattuja Bicep-moduuleja
- [Bicep VS Code Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-bicep)
- [Azure Naming Conventions](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-naming)
- [ARM Template Reference](https://learn.microsoft.com/en-us/azure/templates/)
