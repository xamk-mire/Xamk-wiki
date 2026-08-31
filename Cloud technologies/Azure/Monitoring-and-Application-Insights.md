# Azure Monitor ja Application Insights — sovelluksen näkyvyys

## Sisällysluettelo

1. [Mitä on observability?](#mitä-on-observability)
2. [Azure Monitor -kokonaisuus](#azure-monitor--kokonaisuus)
3. [Application Insights](#application-insights)
4. [Käyttöönotto .NET-sovelluksessa](#käyttöönotto-net-sovelluksessa)
5. [Hyvät lokituskäytännöt](#hyvät-lokituskäytännöt)
6. [KQL — kyselyt telemetriaan](#kql--kyselyt-telemetriaan)
7. [Hälytykset ja Action Groupit](#hälytykset-ja-action-groupit)
8. [Availability-testit](#availability-testit)
9. [Kustannukset](#kustannukset)
10. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Mitä on observability?

**Observability** (havainnoitavuus) tarkoittaa kykyä päätellä järjestelmän sisäinen tila sen tuottamasta datasta — ilman että jokaista vikaa varten tarvitsee lisätä uutta koodia. Kolme peruspilaria:

| Pilari | Mitä se on | Esimerkki | Vastaa kysymykseen |
|--------|------------|-----------|---------------------|
| **Logs** (lokit) | Aikaleimattuja tapahtumia tekstinä/rakenteisena | "Registration created for event X" | *Mitä tapahtui?* |
| **Metrics** (metriikat) | Numeerisia aikasarjoja | Vasteaika, pyyntöjen määrä, 5xx-virheet/min | *Miten paljon ja kuinka nopeasti?* |
| **Traces** (jäljet) | Pyynnön koko polku palvelujen ja riippuvuuksien läpi | HTTP-pyyntö → API → PostgreSQL-kysely | *Missä kohtaa ketjua ongelma on?* |

```
Ilman observabilityä:                Observabilityn kanssa:

Käyttäjä: "Sivu ei toimi!"           Hälytys sähköpostiin klo 14:02
Sinä: "Hmm, toimii mulla..."         → Failures-näkymä: 500-virheet alkoivat 14:00
→ arvailua, ssh, print-debuggausta   → Poikkeus: "connection refused (postgres)"
→ tunteja                            → Juurisyy minuuteissa: tietokanta alhaalla
```

---

## Azure Monitor -kokonaisuus

**Azure Monitor** on kattotermi Azuren monitorointipalveluille. Sen osat liittyvät toisiinsa näin:

```
┌───────────────────────────────────────────────────────────────┐
│  AZURE MONITOR (kattotermi)                                   │
│                                                               │
│  Datan lähteet:              Säilö:                Käyttö:    │
│  ┌─────────────────┐    ┌──────────────────┐   ┌───────────┐ │
│  │ Sovellus         │    │                  │   │ KQL-      │ │
│  │ (App Insights    │───►│  Log Analytics   │──►│ kyselyt   │ │
│  │  SDK)            │    │  Workspace       │   ├───────────┤ │
│  ├─────────────────┤    │                  │   │ Dashboard │ │
│  │ Azure-resurssit  │───►│  (kaikki data    │   │ Workbook  │ │
│  │ (platform-       │    │   yhteen         │   ├───────────┤ │
│  │  metriikat,      │    │   paikkaan)      │──►│ Hälytykset│ │
│  │  esim. Http5xx)  │    │                  │   │ + Action  │ │
│  └─────────────────┘    └──────────────────┘   │   Groups  │ │
│                                                 └───────────┘ │
└───────────────────────────────────────────────────────────────┘
```

| Palvelu | Rooli |
|---------|-------|
| **Log Analytics Workspace** | Keskitetty säilö kaikelle loki- ja telemetriadatalle; KQL-kyselyjen kohde |
| **Application Insights** | Sovellustason telemetria (pyynnöt, riippuvuudet, poikkeukset) — tallentaa Log Analyticsiin |
| **Platform-metriikat** | Azure kerää automaattisesti jokaisesta resurssista (esim. App Servicen `Http5xx`, CPU) — ilmaisia |
| **Alerts + Action Groups** | Sääntö ("5xx > 0") + reaktio ("lähetä sähköposti") |

---

## Application Insights

**Application Insights** on Azure Monitorin sovellusmonitorointiosa (APM). Kun .NET-sovellukseen lisätään App Insights SDK, se kerää **automaattisesti**:

| Telemetriatyyppi | Mitä kerätään | Taulu KQL:ssä |
|-------------------|----------------|----------------|
| **Requests** | Jokainen HTTP-pyyntö: polku, kesto, statuskoodi | `requests` |
| **Dependencies** | Ulkoiset kutsut: tietokantakyselyt, HTTP-kutsut muihin palveluihin | `dependencies` |
| **Exceptions** | Käsittelemättömät poikkeukset stack traceineen | `exceptions` |
| **Traces** | `ILogger`-lokirivit | `traces` |
| **Custom events** | Itse lähetetyt tapahtumat (`TelemetryClient.TrackEvent`) | `customEvents` |

Tärkein ominaisuus on **korrelaatio**: yksittäisen HTTP-pyynnön alta näkee sen aiheuttamat tietokantakyselyt, lokirivit ja poikkeukset yhtenä puuna (end-to-end transaction). Vianselvitys ei ala arvailulla vaan pyynnöstä, joka epäonnistui.

### Keskeiset näkymät portaalissa

| Näkymä | Käyttö |
|--------|--------|
| **Live Metrics** | Reaaliaikainen liikenne (sekunnin viiveellä) — deploy-hetken valvonta |
| **Failures** | Epäonnistuneet pyynnöt ja poikkeukset ryhmiteltyinä — vianselvityksen aloituspiste |
| **Performance** | Vasteajat endpointeittain, hitaimmat riippuvuudet |
| **Transaction search** | Yksittäisten tapahtumien haku ja end-to-end -näkymä |
| **Availability** | Availability-testien tulokset maailmalta |
| **Logs** | KQL-kyselyt kaikkeen dataan |

---

## Käyttöönotto .NET-sovelluksessa

### 1. Infrastruktuuri (Bicep)

Application Insights on **workspace-pohjainen**: ensin Log Analytics, sitten App Insights joka osoittaa siihen.

```bicep
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-myapp-dev'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-myapp-dev'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

output connectionString string = appInsights.properties.ConnectionString
```

### 2. Sovellus liitetään konfiguraatiolla

SDK löytää App Insightsin **ympäristömuuttujasta** — sama backing service -periaate kuin tietokannalla:

```bicep
appSettings: [
  {
    name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
    value: appInsights.properties.ConnectionString
  }
]
```

### 3. SDK sovellukseen

```bash
dotnet add package Microsoft.ApplicationInsights.AspNetCore
```

```csharp
// Program.cs
builder.Services.AddApplicationInsightsTelemetry();
```

Tämä yksi rivi kytkee automaattisen keräyksen (requests, dependencies, exceptions) ja ohjaa `ILogger`-lokit App Insightsiin. Paikallisesti ilman connection stringiä SDK on hiljaa — ei virheitä, ei dataa.

---

## Hyvät lokituskäytännöt

### Rakenteinen loki (structured logging)

Käytä **message templatea** — älä interpoloi arvoja merkkijonoon:

```csharp
// ✅ Rakenteinen: EventId on kyseltävä kenttä KQL:ssä
logger.LogInformation("Registration created for event {EventId}", eventId);

// ❌ Interpoloitu: pelkkää tekstiä, ei kyseltävissä kentittäin
logger.LogInformation($"Registration created for event {eventId}");
```

Rakenteisessa lokissa `{EventId}` tallentuu omana kenttänään (`customDimensions.EventId`), jolloin KQL voi suodattaa ja ryhmitellä sillä.

### PII ja salaisuudet EIVÄT kuulu lokiin

**PII** (personally identifiable information) — nimet, sähköpostit, puhelinnumerot — ja salaisuudet (tokenit, salasanat, yhteysmerkkijonot) eivät koskaan kuulu lokiin:

```csharp
// ❌ PII vuotaa telemetriaan (ja jää sinne retention-ajaksi)
logger.LogInformation("Registration by {Email} for {EventId}", request.AttendeeEmail, id);

// ✅ Tunniste riittää vianselvitykseen — henkilö selviää tietokannasta tarvittaessa
logger.LogInformation("Registration {RegistrationId} created for event {EventId}", reg.Id, id);
```

Miksi tämä on vakavaa: lokidata kopioituu (workspace, exportit, kehittäjien ruudut), sen pääsynhallinta on löyhempi kuin tietokannan, ja GDPR:n poisto-oikeus ei käytännössä ulotu lokeihin. Helpoin ratkaisu: PII ei mene lokiin ollenkaan.

### Lokitasot

| Taso | Käyttö |
|------|--------|
| `LogDebug` | Kehitysaikainen yksityiskohta — ei tuotantoon |
| `LogInformation` | Normaali tapahtuma: "registration created" |
| `LogWarning` | Odotettu poikkeustilanne: "event full", "duplicate email" |
| `LogError` | Virhe joka vaatii huomiota: käsittelemätön poikkeus, riippuvuus alhaalla |

---

## KQL — kyselyt telemetriaan

**KQL** (Kusto Query Language) on Log Analyticsin kyselykieli. Putkimalli: taulu → suodata → muokkaa → tiivistä.

```kusto
// Epäonnistuneet pyynnöt viimeisen tunnin ajalta
requests
| where timestamp > ago(1h)
| where success == false
| order by timestamp desc

// Pyyntömäärät statuskoodeittain
requests
| where timestamp > ago(24h)
| summarize count() by resultCode

// Vasteajan keskiarvo endpointeittain
requests
| where timestamp > ago(24h)
| summarize avg(duration), count() by name
| order by avg_duration desc

// Tuoreimmat poikkeukset
exceptions
| order by timestamp desc
| take 10

// Hitaimmat tietokantakyselyt
dependencies
| where type == "SQL" or type contains "postgres"
| order by duration desc
| take 10

// Omat lokirivit rakenteisella kentällä suodatettuna
traces
| where customDimensions.EventId == "11111111-1111-1111-1111-111111111111"
```

| Operaattori | Merkitys |
|-------------|----------|
| `where` | Suodatus |
| `summarize ... by` | Ryhmittely ja aggregointi (`count()`, `avg()`, `percentile()`) |
| `order by` / `take` | Järjestys ja rajaus |
| `ago(1h)` | Suhteellinen aika |
| `render timechart` | Piirrä tulos kaaviona |

> **AI ja KQL:** kielimallit generoivat KQL:ää hyvin, kun kerrot taulun ja tavoitteen ("App Insights `requests`-taulusta 5xx-määrä 5 min ikkunoissa, timechart"). Tarkista aina kentännimet omaa dataa vasten — AI keksii niitä surutta.

---

## Hälytykset ja Action Groupit

Hälytysjärjestelmässä on kaksi osaa, jotka konfiguroidaan erikseen:

```
┌──────────────────────┐          ┌──────────────────────┐
│  ALERT RULE           │  laukeaa │  ACTION GROUP        │
│  "Http5xx > 0         │ ───────► │  "lähetä sähköposti  │
│   5 min ikkunassa"    │          │   opiskelija@edu.fi" │
└──────────────────────┘          └──────────────────────┘
   MITÄ vahditaan?                    MITEN reagoidaan?
```

Sama Action Group voidaan kytkeä moneen hälytykseen (5xx, availability, budjetti...).

### Luonti CLI:llä

```bash
# Action Group: sähköposti-ilmoitus
az monitor action-group create \
  --resource-group $RG \
  --name ag-myapp-email \
  --short-name myappmail \
  --action email primary-email me@example.com

# Metric alert: App Servicen 5xx-virheet
az monitor metrics alert create \
  --resource-group $RG \
  --name alert-http5xx \
  --scopes $(az webapp show -g $RG -n $APP --query id -o tsv) \
  --condition "total Http5xx > 0" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action ag-myapp-email \
  --description "The app is returning server errors"
```

| Parametri | Merkitys |
|-----------|----------|
| `--condition "total Http5xx > 0"` | Aggregaatio + metriikka + ehto |
| `--window-size 5m` | Tarkasteluikkuna: 5xx-summa viimeisen 5 min ajalta |
| `--evaluation-frequency 1m` | Ehto arvioidaan minuutin välein |
| `--severity 2` | 0 = kriittinen ... 4 = verbose; vaikuttaa vain luokitteluun |

Hälytys myös **palautuu** automaattisesti (resolved), kun ehto ei enää täyty — siitä lähtee oma sähköpostinsa.

> **Huom:** sähköposti tulee osoitteesta `azure-noreply@microsoft.com` ja voi mennä roskapostiin — tarkista sieltä ensin, jos mitään ei kuulu.

---

## Availability-testit

**Availability-testi** kutsuu sovellustasi Azuren datakeskuksista ympäri maailmaa ja hälyttää, kun sovellus ei vastaa — vaikka kukaan käyttäjä ei olisi paikalla huomaamassa.

- **Standard test**: HTTP-kutsu valittuun URL:iin (esim. `/health`) 5–15 min välein useasta sijainnista
- Onnistumisehto: statuskoodi (esim. 200) ja/tai vasteaika
- Kytketään Action Groupiin → sähköposti kun X sijaintia Y:stä epäonnistuu

Luonti: App Insights → **Availability** → **Add Standard test**. Testaa nimenomaan `/health`-tyyppistä endpointtia, joka tarkistaa myös riippuvuudet — silloin testi kertoo "palvelu toimii", ei vain "prosessi on ylhäällä".

---

## Kustannukset

| Erä | Hinta (suuruusluokka) | Huomio |
|-----|------------------------|--------|
| Log Analytics ingestointi | ~2–3 €/GB, **ensimmäiset 5 GB/kk ilmaisia** (per laskutustili) | Pieni kurssisovellus tuottaa megatavuja — käytännössä ilmaista |
| Datan säilytys | 31 pv ilmaista (App Insights -data 90 pv), sen jälkeen ~0,1 €/GB/kk | 30 pv retention riittää kurssille |
| Metric alert -sääntö | ~0,1 €/kk per sääntö | |
| Availability standard test | ~1 €/kk per testi | Poista kurssin päätteeksi |
| Action Group -sähköposti | Ilmainen | |

> **Sampling:** jos dataa syntyisi paljon, App Insights voi ottaa vain otoksen telemetriasta (adaptive sampling on .NET SDK:ssa oletuksena päällä). Kurssisovelluksen liikennemäärillä tällä ei ole merkitystä, mutta tiedä ilmiö: tuotannossa "puuttuva" pyyntö voi olla samplattu pois.

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Workspace-pohjainen App Insights** — kaikki data yhteen Log Analyticsiin
- **Connection string ympäristömuuttujasta** — sama build kaikkiin ympäristöihin
- **Rakenteinen loki message templateilla** — kentät kyseltävissä KQL:llä
- **Ei PII:tä eikä salaisuuksia lokiin** — tunnisteet riittävät
- **Hälytys + Action Group jokaiselle "herätys"-ehdolle**: 5xx, availability, (budjetti)
- **Availability-testi /health-endpointtiin** — testaa palvelua, ei vain prosessia
- **Testaa hälytykset rikkomalla sovellus tahallaan** — hälytys, jota ei ole koskaan nähty laukeavan, ei ole hälytys

### ❌ Vältä näitä

- Älä lokita jokaista pyyntöä itse `LogInformation`illa — requests-telemetria hoitaa sen jo
- Älä tee hälytystä, jolla ei ole selvää reaktiota ("kuka tekee mitä kun tämä laukeaa?")
- Älä jätä hälytysten sähköposteja lukematta "kyllä ne aina huutaa" -tilaan — säädä kynnys mieluummin oikeaksi
- Älä kytke Instrumentation Key -pohjaista (vanhentunut) konfiguraatiota — käytä connection stringiä

---

## Seuraavaksi

- [Azure App Service](App-Service.md) - Sovelluksen isännöinti ja lokit
- [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md) - Riippuvuus, jonka App Insights näkee dependencies-tauluna
- [Infrastructure as Code](Infrastructure-as-Code.md) - Monitorointi-infra Bicepillä

## Takaisin

- [Azure-palvelut — Yleiskatsaus](README.md)
