# CI/CD — Jatkuva integraatio ja julkaisu

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on CI?](#mikä-on-ci)
3. [Mikä on CD?](#mikä-on-cd)
4. [CI/CD-putki](#cicd-putki)
5. [GitHub Actions](#github-actions)
6. [Käytännön esimerkki: .NET CI/CD](#käytännön-esimerkki-net-cicd)
7. [Secrets ja ympäristömuuttujat](#secrets-ja-ympäristömuuttujat)
8. [Best Practices](#best-practices)
9. [Yhteenveto](#yhteenveto)

---

## Johdanto

**CI/CD** (Continuous Integration / Continuous Delivery) on joukko käytäntöjä, joiden tarkoituksena on automatisoida koodin rakentaminen, testaaminen ja julkaiseminen. Se poistaa manuaalisen työn ja vähentää inhimillisten virheiden riskiä.

**Perusidea:**

```
Ilman CI/CD:
1. Kehittäjä kirjoittaa koodia
2. Kehittäjä muistaa ehkä ajaa testit
3. Kehittäjä rakentaa sovelluksen käsin
4. Kehittäjä kopioi tiedostot palvelimelle FTP:llä
5. Jotain menee rikki — ei tiedetä missä vaiheessa
6. Virheen etsintä kestää tunteja

CI/CD:llä:
1. Kehittäjä pushaa koodin GitHubiin
2. Automaattinen putki:
   ✅ Rakentaa sovelluksen
   ✅ Ajaa testit
   ✅ Julkaisee tuotantoon
3. Jos jokin vaihe epäonnistuu → välitön ilmoitus
```

---

## Mikä on CI?

**Continuous Integration** (jatkuva integraatio) tarkoittaa, että kehittäjien koodimuutokset yhdistetään päähaaraan usein (päivittäin tai useammin), ja jokainen yhdistäminen laukaisee automaattisen rakennus- ja testiprosessin.

### CI:n vaiheet

```
Kehittäjä pushaa koodin
        │
        ▼
┌──────────────────┐
│  1. Build        │  Käännä sovellus (dotnet build)
├──────────────────┤
│  2. Test         │  Aja yksikkötestit (dotnet test)
├──────────────────┤
│  3. Analyze      │  Koodin laadun tarkistus (valinainen)
└──────────────────┘
        │
        ▼
   ✅ Onnistui → Koodi on integroitavissa
   ❌ Epäonnistui → Kehittäjä korjaa ennen kuin muut hakevat koodin
```

### CI ratkaisee

| Ongelma | CI:n ratkaisu |
|---------|-------------|
| "Toimii minun koneellani" | Rakennetaan puhtaassa ympäristössä |
| Rikkinäinen koodi päähaarassa | Testit ajetaan automaattisesti ennen merge |
| Merge conflict -kasaumat | Pienet, usein tehtävät muutokset |
| Manuaalinen testaus unohtuu | Automaattiset testit jokaisessa pushissa |

---

## Mikä on CD?

**CD** voi tarkoittaa kahta asiaa:

### Continuous Delivery (jatkuva toimitus)

Koodi on **aina julkaisuvalmiissa tilassa**. Julkaisu tuotantoon tapahtuu manuaalisella hyväksynnällä (nappia painamalla).

```
CI → Build → Test → ✅ → Artifakti valmis → [Manuaalinen hyväksyntä] → Tuotanto
```

### Continuous Deployment (jatkuva käyttöönotto)

Jokainen onnistunut CI-putki julkaisee automaattisesti tuotantoon — ilman manuaalista väliaskelta.

```
CI → Build → Test → ✅ → Automaattinen julkaisu → Tuotanto
```

### Vertailu

| Ominaisuus | Continuous Delivery | Continuous Deployment |
|-----------|-------------------|---------------------|
| Tuotantojulkaisu | Manuaalinen hyväksyntä | Automaattinen |
| Riski | Matalampi (ihminen tarkistaa) | Vaatii erittäin hyvät testit |
| Nopeus | Nopeampi kuin manuaalinen | Nopein mahdollinen |
| Sopii kun | Kriittiset järjestelmät | Nopea iteraatio, hyvä testikattavuus |

---

## CI/CD-putki

**Pipeline** (putki) on automatisoitu prosessi, joka suorittaa sarjan vaiheita koodin pushista tuotantojulkaisuun.

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Source  │ →  │  Build  │ →  │   Test   │ →  │  Deploy  │ →  │  Prod    │
│  (Git)  │    │ (dotnet │    │ (dotnet  │    │ (Azure)  │    │ (Live)   │
│         │    │  build) │    │  test)   │    │          │    │          │
└─────────┘    └─────────┘    └──────────┘    └──────────┘    └──────────┘
     │              │              │                │
     │              │         ❌ Fail?             │
     │              │         → STOP               │
     │              │         → Ilmoitus           │
```

### CI/CD-työkalut

| Työkalu | Tarjoaja | Käyttö |
|---------|---------|-------|
| **GitHub Actions** | GitHub | Yleisin, integroituu suoraan repoon |
| Azure DevOps Pipelines | Microsoft | Enterprise, Azure-integraatio |
| GitLab CI/CD | GitLab | GitLab-repot |
| Jenkins | Open Source | Itse isännöity, konfiguroitava |
| CircleCI | CircleCI | SaaS-pohjainen |

Tällä kurssilla keskitytään **GitHub Actionsiin**.

---

## GitHub Actions

**GitHub Actions** on GitHubin sisäänrakennettu CI/CD-alusta. Workflow-tiedostot määrittävät mitä tehdään ja milloin.

### Käsitteet

```
Repository
└── .github/
    └── workflows/
        └── ci.yml          ← Workflow-tiedosto

Workflow (ci.yml)
├── Trigger (milloin ajetaan?)     → push, pull_request, schedule
├── Job 1: "build"                  → Ajetaan Ubuntu-koneella
│   ├── Step 1: Checkout code       → actions/checkout@v4
│   ├── Step 2: Setup .NET          → actions/setup-dotnet@v4
│   ├── Step 3: dotnet restore
│   ├── Step 4: dotnet build
│   └── Step 5: dotnet test
└── Job 2: "deploy"                 → Ajetaan build-jobin jälkeen
    ├── Step 1: Download artifact
    └── Step 2: Deploy to Azure
```

| Käsite | Selitys |
|--------|---------|
| **Workflow** | YAML-tiedosto `.github/workflows/`-kansiossa — määrittelee koko putken |
| **Trigger** | Tapahtuma joka käynnistää workflown (`push`, `pull_request`, `schedule`) |
| **Job** | Joukko vaiheita, jotka ajetaan samalla koneella |
| **Step** | Yksittäinen toiminto jobissa (komento tai valmis action) |
| **Runner** | Kone joka suorittaa jobin (GitHubin tarjoama tai oma) |
| **Action** | Uudelleenkäytettävä komponentti (esim. `actions/checkout@v4`) |
| **Artifact** | Rakennettu tiedosto joka siirretään jobien välillä |

### Triggerit

```yaml
on:
  push:
    branches: [main]          # Ajetaan kun pushataan main-haaraan
  pull_request:
    branches: [main]          # Ajetaan kun PR avataan main-haaraan
  schedule:
    - cron: '0 2 * * 1'       # Joka maanantai klo 02:00 UTC
  workflow_dispatch:           # Manuaalinen käynnistys GitHubista
```

---

## Käytännön esimerkki: .NET CI/CD

### CI — Build ja testit

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Restore dependencies
        run: dotnet restore

      - name: Build
        run: dotnet build --configuration Release --no-restore

      - name: Test
        run: dotnet test --configuration Release --no-build --verbosity normal
```

### CD — Deploy Azure App Serviceen

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Build and publish
        run: dotnet publish --configuration Release --output ./publish

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: app
          path: ./publish

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: app

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: my-app-name
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

### IaC deploy — Bicep GitHub Actionsilla

```yaml
# .github/workflows/deploy-infra.yml
name: Deploy Infrastructure

on:
  push:
    branches: [main]
    paths:
      - 'infra/**'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Deploy Bicep
        uses: azure/arm-deploy@v2
        with:
          resourceGroupName: my-resource-group
          template: ./infra/main.bicep
          parameters: environment=production
```

---

## Secrets ja ympäristömuuttujat

### GitHub Actions Secrets

Arkaluonteiset arvot (API-avaimet, salasanat, yhteysmerkkijonot) tallennetaan **GitHub Secrets** -osioon, josta ne ovat käytettävissä workfloweissa.

```
GitHub → Repository → Settings → Secrets and variables → Actions → New repository secret
```

```yaml
# Secretin käyttö workflowssa
steps:
  - name: Deploy
    env:
      CONNECTION_STRING: ${{ secrets.DB_CONNECTION_STRING }}
    run: echo "Deploying with secret..."
```

**Sääntöjä:**
- Secretit eivät näy lokeissa (GitHub piilottaa ne automaattisesti)
- Secretejä ei voi lukea takaisin — vain ylikirjoittaa
- Secretit ovat repositoriokohtaisia (tai organisaatiotasoisia)

### Ympäristömuuttujat

```yaml
env:
  DOTNET_VERSION: '8.0.x'
  CONFIGURATION: Release

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: dotnet build --configuration ${{ env.CONFIGURATION }}
```

---

## Best Practices

### 1. Aja CI jokaisessa pull requestissa

```yaml
on:
  pull_request:
    branches: [main]
```

PR ei saa mergettävissä ennen kuin CI on vihreä.

### 2. Pidä putket nopeina

- Käytä välimuistia (cache) riippuvuuksille
- Aja vain oleelliset testit PR:ssä, kaikki testit mergessä

```yaml
- name: Cache NuGet packages
  uses: actions/cache@v4
  with:
    path: ~/.nuget/packages
    key: ${{ runner.os }}-nuget-${{ hashFiles('**/*.csproj') }}
```

### 3. Erota build ja deploy

```yaml
jobs:
  build:    # Rakennetaan aina
    ...
  deploy:   # Julkaistaan vain main-haarasta
    needs: build
    if: github.ref == 'refs/heads/main'
```

### 4. Älä tallenna secretejä koodiin

```yaml
# ✅ GitHub Secretsistä
${{ secrets.API_KEY }}

# ❌ Koodissa tai YAML:ssä
API_KEY: "sk-1234567890abcdef"
```

### 5. Käytä versioltuja actioneja

```yaml
# ✅ Kiinnitetty versio — turvallinen ja toistettava
uses: actions/checkout@v4

# ❌ Viittaa haaraan — voi muuttua
uses: actions/checkout@main
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **CI** | Continuous Integration — automaattinen build + testit jokaisessa pushissa |
| **CD** | Continuous Delivery/Deployment — automaattinen julkaisu tuotantoon |
| **Pipeline** | Automatisoitu prosessi: Source → Build → Test → Deploy |
| **GitHub Actions** | GitHubin sisäänrakennettu CI/CD-alusta |
| **Workflow** | YAML-tiedosto joka määrittelee putken |
| **Trigger** | Tapahtuma joka käynnistää workflown (push, PR, schedule) |
| **Job** | Joukko vaiheita samalla runner-koneella |
| **Step** | Yksittäinen toiminto (komento tai action) |
| **Runner** | Kone joka suorittaa jobin |
| **Action** | Uudelleenkäytettävä komponentti |
| **Secrets** | Arkaluonteiset arvot GitHubissa — eivät näy lokeissa |
| **Artifact** | Rakennettu tiedosto jobien välillä |

**Muista:**
- CI/CD **automatisoi** rakennus-, testaus- ja julkaisuprosessin
- **CI** varmistaa, ettei rikkinäinen koodi päädy päähaaraan
- **CD** vie toimivan koodin tuotantoon nopeasti ja turvallisesti
- **GitHub Actions** on yleisin työkalu GitHub-projekteissa
- **Secretit** tallennetaan GitHubin Secrets-osioon — ei koskaan koodiin

---

## Hyödyllisiä linkkejä

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions: Quickstart](https://docs.github.com/en/actions/quickstart)
- [Microsoft: Deploy to Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions)
- [Azure App Service -materiaali (wiki)](../Cloud%20technologies/Azure/App-Service.md)
- [Infrastructure as Code -materiaali (wiki)](../Cloud%20technologies/Azure/Infrastructure-as-Code.md)
