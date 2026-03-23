# Azure App Service — .NET-sovellusten isännöinti

## Sisällysluettelo

1. [Mikä on Azure App Service?](#mikä-on-azure-app-service)
2. [App Service Plan — hintataso ja resurssit](#app-service-plan--hintataso-ja-resurssit)
3. [Web Appin luominen](#web-appin-luominen)
4. [NET-sovelluksen julkaisu](#net-sovelluksen-julkaisu)
5. [Ympäristömuuttujat ja konfiguraatio](#ympäristömuuttujat-ja-konfiguraatio)
6. [Deployment Slots](#deployment-slots)
7. [Lokit ja monitorointi](#lokit-ja-monitorointi)
8. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Mikä on Azure App Service?

**Azure App Service** on Azuren täysin hallittu (PaaS) alusta web-sovellusten, REST API:en ja mobiilitaustajärjestelmien isännöintiin. Se huolehtii infrastruktuurista — palvelimista, käyttöjärjestelmäpäivityksistä ja kuormantasauksesta — joten kehittäjä voi keskittyä koodiin.

### Tuetut runtimet

| Runtime | Versiot |
|---------|---------|
| .NET | 6, 7, 8 (LTS) |
| Node.js | 18, 20 |
| Python | 3.9, 3.10, 3.11, 3.12 |
| Java | 8, 11, 17, 21 |
| PHP | 8.0, 8.1, 8.2 |

### App Servicen arkkitehtuuri

```
┌─────────────────────────────────────────────┐
│  Azure-infrastruktuuri (hallittu)            │
│                                             │
│  ┌─────────────────────────────────────┐    │
│  │  App Service Plan (resurssit)        │    │
│  │                                     │    │
│  │  ┌──────────────┐ ┌──────────────┐  │    │
│  │  │  Web App 1   │ │  Web App 2   │  │    │
│  │  │  (myapi)     │ │  (myfrontend)│  │    │
│  │  │              │ │              │  │    │
│  │  │  .NET 8      │ │  Node.js 20  │  │    │
│  │  └──────────────┘ └──────────────┘  │    │
│  │                                     │    │
│  │  CPU: 1 core  RAM: 1.75 GB          │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
         ↑
  Internet-liikenne ohjataan automaattisesti
  HTTPS-päätepiste: myapi.azurewebsites.net
```

Sama App Service Plan voi isännöidä useita Web App -resursseja — ne jakavat suorittimen ja muistin.

---

## App Service Plan — hintataso ja resurssit

App Service Plan määrittää fyysiseti resurssit ja hinnan. Valitse taso projektin tarpeiden mukaan.

### Kehitys ja opiskelu

| Taso | CPU | RAM | Hinta/kk | Huomioitavaa |
|------|-----|-----|----------|--------------|
| **F1** (Free) | Jaettu | 1 GB | 0 € | Nukahtaa 20 min passiivisuuden jälkeen, ei custom domain |
| **D1** (Shared) | Jaettu | 1 GB | ~1 € | Custom domain, mutta ei SSL |
| **B1** (Basic) | 1 core | 1.75 GB | ~12 € | Ei deployment sloteja, ei autoskaalautumista |

### Tuotanto

| Taso | CPU | RAM | Hinta/kk | Huomioitavaa |
|------|-----|-----|----------|--------------|
| **S1** (Standard) | 1 core | 1.75 GB | ~60 € | 5 deployment slotia, autoskaalautuminen |
| **P1v3** (Premium) | 2 cores | 8 GB | ~130 € | Optimoitu suorituskyky, VNet-integraatio |

> **Opiskeluprojekteissa** käytä **F1** (ilmainen). Muista, että F1 nukahtaa passiivisuuden jälkeen — ensimmäinen pyyntö voi kestää 10–30 sekuntia (cold start).

---

## Web Appin luominen

### Vaihtoehto A: Azure CLI

```bash
# 1. Muuttujat
$RG = "rg-myapp-dev"
$LOCATION = "swedencentral"
$PLAN = "asp-myapp"
$APP = "app-myapp-<uniikki-tunniste>"

# 2. Resurssiryhmä
az group create --name $RG --location $LOCATION

# 3. App Service Plan (Linux, Free F1)
az appservice plan create \
  --name $PLAN \
  --resource-group $RG \
  --sku F1 \
  --is-linux

# 4. Web App (.NET 8)
az webapp create \
  --name $APP \
  --resource-group $RG \
  --plan $PLAN \
  --runtime "DOTNETCORE:8.0"

# 5. Tarkista URL
az webapp show \
  --name $APP \
  --resource-group $RG \
  --query defaultHostName \
  --output tsv
```

Sovellus on heti käytettävissä osoitteessa `https://<nimi>.azurewebsites.net`.

### Vaihtoehto B: Azure Portal

1. Avaa [portal.azure.com](https://portal.azure.com)
2. Klikkaa **+ Create a resource** → **Web App**
3. Täytä perustiedot:
   - **Resource Group**: Luo uusi tai valitse olemassa oleva
   - **Name**: Globaalisti uniikki nimi (esim. `myapp-opiskelija01`)
   - **Publish**: Code
   - **Runtime stack**: .NET 8 (LTS)
   - **Operating System**: Linux
   - **Region**: Sweden Central
4. **App Service Plan** -kohdassa:
   - Klikkaa **Create new**
   - Valitse **Free F1** -taso
5. Klikkaa **Review + create** → **Create**

---

## .NET-sovelluksen julkaisu

### Tapa 1: ZIP-deploy (Azure CLI)

Nopein tapa yksittäiselle deploylle:

```bash
# 1. Julkaise projekti Release-konfiguraatiolla
dotnet publish -c Release -o ./publish

# 2. Pakkaa ZIP-tiedostoksi (PowerShell)
Compress-Archive -Path ./publish/* -DestinationPath ./publish.zip -Force

# 3. Lähetä Azureen
az webapp deploy \
  --resource-group $RG \
  --name $APP \
  --src-path ./publish.zip \
  --type zip

# 4. Seuraa lokeja
az webapp log tail --resource-group $RG --name $APP
```

### Tapa 2: Visual Studio Publish

1. Klikkaa projektia Solution Explorerissa hiiren **oikealla** → **Publish**
2. Valitse **Azure** → **Azure App Service (Linux)** → **Next**
3. Kirjaudu Azure-tilillesi
4. Valitse olemassa oleva App Service tai luo uusi
5. Klikkaa **Finish** → **Publish**

Visual Studio rakentaa projektin, julkaisee sen Azureen ja avaa selaimen automaattisesti.

### Tapa 3: GitHub Actions (CI/CD)

Tuotantoon suositellaan automatisoitua putkea. Hae julkaisuprofiilin salaisuus:

```bash
az webapp deployment list-publishing-profiles \
  --resource-group $RG \
  --name $APP \
  --xml
```

Luo tiedosto `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure App Service

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Build and publish
        run: dotnet publish -c Release -o ./publish

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ secrets.AZURE_APP_NAME }}
          publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
          package: ./publish
```

Lisää repositoryn Secrets-asetuksiin (`Settings → Secrets → Actions`):
- `AZURE_APP_NAME`: Web Appin nimi
- `AZURE_PUBLISH_PROFILE`: julkaisuprofiilin XML-sisältö

---

## Ympäristömuuttujat ja konfiguraatio

App Service injektoi **Application Settings** -arvot automaattisesti sovelluksen ympäristömuuttujiksi. ASP.NET Core lukee ne osana konfiguraatiojärjestelmää — koodi pysyy muuttumattomana:

```
appsettings.json:          Azure App Service:
──────────────────         ──────────────────────────────────
"ApiKeys": {               Application Settings:
  "SendGrid": ""    →      ApiKeys__SendGrid = "SG.prod-key"
}
```

> **Sisäkkäiset avaimet:** JSON:n `:` muuttuu ympäristömuuttujissa `__` (kahdella alaviivalla).

### Asettaminen CLI:llä

```bash
az webapp config appsettings set \
  --resource-group $RG \
  --name $APP \
  --settings \
    ApiKeys__SendGrid="SG.prod-key" \
    Jwt__Secret="prod-secret-min-32-chars"
```

> Lisätietoja: [Azure Environment Variables](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Environment-Variables.md)
> Tuotantotason salaisuuksille: [Azure Key Vault](Key-Vault.md) ja [Managed Identity](Managed-Identity.md)

---

## Deployment Slots

**Deployment Slots** ovat erillisiä ympäristöjä saman App Service Plan -suunnitelman sisällä. Tyypillisin käyttötapa on `staging → production` -swap.

> Deployment Slots vaatii **Standard S1** -tason tai korkeamman.

```
┌──────────────────────┐            ┌──────────────────────┐
│  STAGING SLOT         │   SWAP →   │  PRODUCTION SLOT     │
│                      │            │                      │
│  Koodi: v2.0         │ ─────────→ │  Koodi: v2.0         │
│  URL: myapp-staging  │            │  URL: myapp          │
│  DB: staging-db      │ (pysyy)    │  DB: prod-db         │
└──────────────────────┘            └──────────────────────┘
```

```bash
# Luo staging-slot
az webapp deployment slot create \
  --name $APP \
  --resource-group $RG \
  --slot staging

# Deploy stagingiin
az webapp deploy \
  --resource-group $RG \
  --name $APP \
  --slot staging \
  --src-path ./publish.zip \
  --type zip

# Swap staging → production
az webapp deployment slot swap \
  --resource-group $RG \
  --name $APP \
  --slot staging \
  --target-slot production
```

---

## Lokit ja monitorointi

### Reaaliaikaiset lokit (Log Stream)

```bash
# Seuraa sovelluksen lokeja reaaliajassa
az webapp log tail --resource-group $RG --name $APP
```

### Lokien lataaminen

```bash
az webapp log download \
  --resource-group $RG \
  --name $APP \
  --log-file ./app-logs.zip
```

### Azure Portal

1. App Service → **Monitoring** → **Log stream** — reaaliaikaiset lokit selaimessa
2. App Service → **Diagnose and solve problems** — automaattiset diagnoosit

### Sovelluksen käynnistyksen tarkistaminen

```bash
# Tarkista App Servicen tila
az webapp show \
  --name $APP \
  --resource-group $RG \
  --query state \
  --output tsv

# Käynnistä uudelleen
az webapp restart --name $APP --resource-group $RG
```

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Aseta `ASPNETCORE_ENVIRONMENT`** App Servicen Application Settingsissa arvoksi `Production`
- **Merkitse salaisuudet slot-kohtaisiksi** — tietokantayhteydet ja API-avaimet eivät saa vaihtua swapin mukana
- **Käytä Managed Identityä** Key Vault -yhteyksiin sen sijaan, että tallentaisit yhteysstringin Application Settingsiin
- **Käytä ZIP-deployta kehityksessä** ja GitHub Actionsia tuotantoon
- **Poista resurssit harjoitusten jälkeen**: `az group delete --name $RG --yes`

### ❌ Vältä näitä

- Älä laita salaisuuksia `appsettings.json`-tiedostoon — ne päätyvät versionhallintaan
- Älä käytä F1-tasoa tuotannossa — se nukahtaa passiivisuuden jälkeen eikä tue custom domainia/SSL:ää
- Älä unohda asettaa `ASPNETCORE_ENVIRONMENT=Production` — muuten sovellus käynnistyy Development-tilassa

---

## Seuraavaksi

- [Managed Identity](Managed-Identity.md) - Autentikointi ilman salasanoja
- [Azure Key Vault](Key-Vault.md) - Tuotantotason salaisuuksien hallinta
- [Azure Environment Variables .NET-koodissa](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Environment-Variables.md)

## Takaisin

- [Azure-palvelut — Yleiskatsaus](README.md)
