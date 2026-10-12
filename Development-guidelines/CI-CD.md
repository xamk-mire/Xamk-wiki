# CI/CD — Jatkuva integraatio ja julkaisu

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on CI?](#mikä-on-ci)
3. [Mikä on CD?](#mikä-on-cd)
4. [CI/CD-putki](#cicd-putki)
5. [GitHub Actions](#github-actions)
6. [Käytännön esimerkki: .NET CI/CD](#käytännön-esimerkki-net-cicd)
7. [Secrets ja ympäristömuuttujat](#secrets-ja-ympäristömuuttujat)
8. [Azure-kirjautuminen putkessa: OIDC](#azure-kirjautuminen-putkessa-oidc)
9. [Laatuportit ja branch protection](#laatuportit-ja-branch-protection)
10. [Ilmoitukset epäonnistumisista](#ilmoitukset-epäonnistumisista)
11. [Best Practices](#best-practices)
12. [Yhteenveto](#yhteenveto)

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

> **Huom:** publish profile on **pitkäikäinen salaisuus** — yksinkertainen tapa aloittaa, mutta suositeltu tapa on **OIDC** (`azure/login@v2` + federated identity), jolloin repoon ei tallenneta yhtään salasanaa tai avainta. Katso [OIDC-luku](#azure-kirjautuminen-putkessa-oidc) alempana.

### IaC deploy — Bicep GitHub Actionsilla

```yaml
# .github/workflows/deploy-infra.yml
name: Deploy Infrastructure

on:
  push:
    branches: [main]
    paths:
      - 'infra/**'

permissions:
  id-token: write   # OIDC-token (ks. OIDC-luku alempana)
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Azure Login (OIDC — ei pitkäikäisiä salaisuuksia)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: What-if (esikatselu lokiin)
        run: |
          az deployment group what-if \
            --resource-group my-resource-group \
            --template-file infra/main.bicep \
            --parameters infra/dev.bicepparam

      - name: Deploy Bicep
        run: |
          az deployment group create \
            --resource-group my-resource-group \
            --template-file infra/main.bicep \
            --parameters infra/dev.bicepparam
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

## Azure-kirjautuminen putkessa: OIDC

Putki tarvitsee oikeudet Azureen. Huonoin tapa on tallentaa **pitkäikäinen salaisuus** (service principal -salasana tai publish profile) GitHub Secretsiin: se ei vanhene, se pitää kierrättää käsin, ja vuotaessaan se toimii missä tahansa.

**OIDC (OpenID Connect) / federated identity** poistaa ongelman: GitHub Actions todistaa identiteettinsä Azurelle **lyhytikäisellä tokenilla**, jonka Azure vaihtaa käyttöoikeuteen. Repoon ei tallenneta yhtään salasanaa — vain kolme *tunnistetta* (client id, tenant id, subscription id), jotka eivät ole salaisuuksia vaikka ne secrets-osioon tallennetaankin.

```
Pitkäikäinen salaisuus (❌):              OIDC / federated identity (✅):

GitHub Secrets:                          GitHub Secrets:
  AZURE_CREDENTIALS = {                    AZURE_CLIENT_ID       = <guid>
    "clientSecret": "oikea salasana,       AZURE_TENANT_ID       = <guid>
     joka toimii kaikkialla ja             AZURE_SUBSCRIPTION_ID = <guid>
     ikuisesti" }                          (tunnisteita, ei salaisuuksia)
        │                                      │
        ▼                                      ▼
  Vuotaa → hyökkääjällä                  Workflow saa kertakäyttöisen tokenin,
  pysyvä pääsy Azureen                   joka kelpaa VAIN tästä reposta,
                                         VAIN määritellystä haarasta
```

### Käyttöönotto (Azure CLI)

```bash
# 1. Sovellusrekisteröinti + service principal
az ad app create --display-name "gh-myapp-deploy"
# → ota talteen appId
az ad sp create --id <appId>

# 2. Oikeudet: Contributor VAIN omaan resource groupiin (least privilege)
az role assignment create \
  --assignee <appId> \
  --role Contributor \
  --scope /subscriptions/<sub-id>/resourceGroups/<rg-name>

# 3. Federated credential: luota TÄSMÄLLEEN tähän repoon ja haaraan
az ad app federated-credential create --id <appId> --parameters '{
  "name": "github-main",
  "issuer": "https://token.actions.githubusercontent.com",
  "subject": "repo:<owner>/<repo>:ref:refs/heads/main",
  "audiences": ["api://AzureADTokenExchange"]
}'
```

`subject`-kenttä on turvallisuuden ydin: token kelpaa vain, kun workflow ajaa nimenomaan tästä reposta ja tästä haarasta. Toisen repon (tai forkin) workflow ei saa pääsyä, vaikka tunnisteet vuotaisivat.

### Käyttö workflowssa

```yaml
permissions:
  id-token: write   # ilman tätä OIDC-token ei irtoa
  contents: read

steps:
  - name: Azure Login
    uses: azure/login@v2
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

---

## Laatuportit ja branch protection

CI-tarkistukset ovat hyödyttömiä, jos ne voi ohittaa. **Branch protection** tekee tarkistuksista pakollisia: main-haaraan ei pääse kuin pull requestin kautta, ja PR ei mergeydy ennen kuin kaikki portit ovat vihreällä.

```
Kehittäjä ──► feature-haara ──► Pull Request ──► main ──► automaattinen deploy
                                    │
                          ┌─────────┴──────────┐
                          │  LAATUPORTIT        │
                          │  ✅ Build           │
                          │  ✅ Testit          │
                          │  ✅ Lint/format     │
                          │  ✅ Katselmointi    │
                          │     (ihminen/AI)    │
                          └────────────────────┘
                          Kaikki vihreällä → merge sallittu
                          Yksikin punainen → merge estetty
```

### Käyttöönotto GitHubissa

`Repository → Settings → Branches → Add branch protection rule`:

| Asetus | Vaikutus |
|--------|----------|
| **Require a pull request before merging** | Suoraan mainiin ei voi pushata |
| **Require status checks to pass** | Valitut CI-jobit (esim. `build-and-test`) pakollisia |
| **Require branches to be up to date** | PR testataan mainin uusinta versiota vasten |
| **Do not allow bypassing the above settings** | Säännöt koskevat myös adminia (itseäsi) |

> **Huom:** yksityisissä repoissa branch protection vaatii GitHub Pro -tason (opiskelijat saavat sen [GitHub Student Developer Packista](https://education.github.com/pack)). Julkisissa repoissa se on ilmainen.

### AI-katselmointi porttina

Ihmiskatselmoinnin rinnalle (tai opiskeluprojektissa sen sijaan) voi kytkeä **AI-koodikatselmoinnin** — esim. GitHub Copilot code review — joka kommentoi PR:n muutokset automaattisesti. AI-katselmointi löytää mekaanisia ongelmia (bugiepäilyt, nimeäminen, unohtunut virheenkäsittely), mutta **ei ymmärrä kontekstia**: sen huomautukset ovat ehdotuksia, jotka ihminen hyväksyy tai perustellusti hylkää. Hyvä käytäntö: jokaiseen AI-kommenttiin reagoidaan — joko korjaus tai lyhyt perustelu, miksi ei korjata.

---

## Ilmoitukset epäonnistumisista

Automaattinen putki ilman ilmoituksia on vaarallinen: rikkinäinen deploy voi jäädä huomaamatta päiviksi. Vähimmäistaso on **sähköposti-ilmoitus epäonnistuneesta workflow-ajosta**:

1. GitHub → oma profiili → **Settings → Notifications → Actions**
2. Valitse **Only notify for failed workflows**

Tämän jälkeen jokainen punainen ajo mainissa tuottaa sähköpostin — myös deploy-vaiheen tai deploymentin jälkeisen **smoke testin** epäonnistuminen. Smoke test (esim. `curl /health` deployn jälkeen) kannattaa aina lisätä putken viimeiseksi askeleeksi: se muuttaa "deploy meni läpi" -tiedon muotoon "sovellus oikeasti vastaa".

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
