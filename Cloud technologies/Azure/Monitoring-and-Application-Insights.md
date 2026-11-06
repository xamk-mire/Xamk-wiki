# Azure Monitor ja Application Insights — sovelluksen näkyvyys
> 🇬🇧 English version: [Monitoring-and-Application-Insights.md](../eng/Azure/Monitoring-and-Application-Insights.md)

## Sisällysluettelo

1. [Mitä on observability?](#mitä-on-observability)
2. [Azure Monitor -kokonaisuus](#azure-monitor--kokonaisuus)
3. [Application Insights](#application-insights)
4. [Käyttöönotto .NET-sovelluksessa](#käyttöönotto-net-sovelluksessa)
5. [Hyvät lokituskäytännöt](#hyvät-lokituskäytännöt)
6. [KQL — kyselyt telemetriaan](#kql--kyselyt-telemetriaan)
7. [Hälytykset ja Action Groupit](#hälytykset-ja-action-groupit)
8. [Availability-testit](#availability-testit)
9. [Dashboardit ja workbookit](#dashboardit-ja-workbookit)
10. [Kustannukset](#kustannukset)
11. [Parhaat käytännöt](#parhaat-käytännöt)

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

### Korrelaatio: operation_Id

Korrelaatio ei ole taikaa vaan yksi sarake. Kun pyyntö saapuu, SDK antaa sille tunnisteen **`operation_Id`** ja leimaa sillä kaiken, mitä pyynnön käsittely tuottaa: `requests`-rivin, jokaisen `dependencies`-rivin (SQL-kyselyt), `traces`-rivit (`ILogger`) ja `exceptions`-rivit. Transaction searchin "end-to-end transaction" -puu on vain nämä taulut yhdistettynä tällä sarakkeella.

```kusto
// Yksi pyyntö ja kaikki, mitä se aiheutti
requests
| where name startswith "POST /api/events"
| take 1
| join kind=inner (dependencies) on operation_Id
| project timestamp, name, duration, dependency = name1, sql = data, dependencyDuration = duration1
```

Kun kirjoitat KQL:ää, joka yhdistää tauluja, `operation_Id` on aina avain — ei `id`, `session_Id` eikä mikään AI:n ehdottama `correlationId`. Pyynnön sisällä riippuvuuksilla on lisäksi oma `id` ja vanhemman tunniste, joista puu rakentuu; kurssilla riittää `operation_Id`.

### Keskeiset näkymät portaalissa

| Näkymä | Käyttö |
|--------|--------|
| **Live Metrics** | Reaaliaikainen liikenne (sekunnin viiveellä) — deploy-hetken valvonta |
| **Failures** | Epäonnistuneet pyynnöt ja poikkeukset ryhmiteltyinä — vianselvityksen aloituspiste |
| **Performance** | Vasteajat endpointeittain, hitaimmat riippuvuudet |
| **Transaction search** | Yksittäisten tapahtumien haku ja end-to-end -näkymä |
| **Application map** | Kartta sovelluksesta ja sen riippuvuuksista (PostgreSQL, Storage, muut API:t) kutsumäärineen ja virheprosentteineen — "mikä laatikko on punainen?" |
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
using OpenTelemetry.Trace;

if (builder.Configuration["APPLICATIONINSIGHTS_CONNECTION_STRING"] is not null)
{
    builder.Services.AddApplicationInsightsTelemetry();

    // Npgsql (PostgreSQL) julkaisee omat jäljet "Npgsql"-lähteen alla —
    // ilman tätä riviä dependencies-taulu jää tyhjäksi.
    builder.Services.ConfigureOpenTelemetryTracerProvider(t => t.AddSource("Npgsql"));
}
```

`AddApplicationInsightsTelemetry()` kytkee automaattisen keräyksen (requests, exceptions, HttpClient- ja SqlClient-riippuvuudet) ja ohjaa `ILogger`-lokit App Insightsiin.

**OpenTelemetry** (OTel) on toimittajariippumaton standardi sille, miten sovellus tuottaa jälkiä, metriikoita ja lokeja — sama koodi voi lähettää dataa App Insightsiin, Grafanaan tai Jaegeriin. .NET:ssä jälki syntyy `ActivitySource`-oliosta: kirjasto (ASP.NET Core, HttpClient, Npgsql) luo `Activity`-olion jokaiselle operaatiolle ja julkaisee sen nimetyn lähteen alla. SDK **tilaa** lähteitä: oletuksena vain Microsoftin omat, ja `AddSource("Npgsql")` lisää PostgreSQL-ajurin lähteen tilaukseen. Siksi rivi puuttuessaan ei kaada mitään — `dependencies`-taulu jää vain hiljaa tyhjäksi.

Kaksi asiaa, jotka SDK:n **versio 3** (OpenTelemetry-pohjainen) muutti:

| Asia | Ennen (2.x) | Nyt (3.x) |
|------|-------------|-----------|
| Ei connection stringiä | SDK oli hiljaa | SDK **kaataa käynnistyksen**: `A connection string was not found` → rekisteröi SDK vain, kun asetus on olemassa (`if` yllä) |
| PostgreSQL-riippuvuudet | – | Vain ASP.NET Core, HttpClient ja SqlClient kuunnellaan oletuksena. Npgsql:n jäljet saa tilaamalla `AddSource("Npgsql")` |
| Sampling | adaptiivinen | **rate limiting** (jälkiä/sekunti); säilytetyt rivit saavat `microsoft.sample_rate`-kentän, `sum(itemCount)` arvioi todellisen määrän |

> **Huom (Bicep + putki):** Log Analytics ja App Insights vaativat, että tilauksessa on rekisteröity resource providerit `Microsoft.OperationalInsights`, `Microsoft.Insights` ja `Microsoft.AlertsManagement`. Omalla CLI:llä Owner-roolissa ARM tekee sen automaattisesti, mutta putken identiteetti (Contributor yhteen resurssiryhmään) ei saa — deploy kaatuu virheeseen `MissingSubscriptionRegistration`. Rekisteröi kerran käsin: `az provider register --namespace Microsoft.OperationalInsights --wait` (ja samoin kaksi muuta).

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
| `LogTrace` | Kaikkein yksityiskohtaisin (muuttujien arvot, silmukan kierrokset) — vain hetkellisesti päällä |
| `LogDebug` | Kehitysaikainen yksityiskohta — ei tuotantoon |
| `LogInformation` | Normaali tapahtuma: "registration created" |
| `LogWarning` | Odotettu poikkeustilanne: "event full", "duplicate email" |
| `LogError` | Virhe joka vaatii huomiota: käsittelemätön poikkeus, riippuvuus alhaalla |
| `LogCritical` | Sovellus ei voi jatkaa: käynnistys epäonnistui, levy täynnä |

Taso valitaan sen mukaan, **mitä lukija tekee rivin nähdessään**: Information on tilastoa, Warning on "katso jos toistuu", Error on "joku korjaa tämän". Jos jokainen rivi on Error, mikään ei ole.

### Lokitasot konfiguraatiossa (appsettings)

Koodi ei päätä, mitä lokista tallennetaan — konfiguraatio päättää. `appsettings.json`:n `Logging`-osio asettaa **kynnyksen kategorioittain**; kategoria on loggerin tyyppinimi (`ILogger<Program>` → `Program`) tai kirjaston nimiavaruus:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning"
    }
  }
}
```

| Rivi | Vaikutus |
|------|----------|
| `Default` | Kynnys kaikille kategorioille, joita ei erikseen mainita |
| `Microsoft.AspNetCore: Warning` | Kehyksen omat Information-rivit (jokainen pyyntö) pois |
| `Microsoft.EntityFrameworkCore.Database.Command: Warning` | EF Coren `Executed DbCommand` -rivit (jokainen SQL-lause) pois — telemetrian meluisin kategoria, mutta vianselvityksessä joskus ainoa todiste siitä, mitä kanta sai |

Tarkin osuma voittaa: `Microsoft.EntityFrameworkCore.Database.Command` ohittaa `Microsoft.EntityFrameworkCore`-rivin, joka ohittaa `Default`-rivin. Ympäristökohtainen tiedosto (`appsettings.Development.json`) ylikirjoittaa perustiedoston, ja App Servicessä sama asetus annetaan ympäristömuuttujana `Logging__LogLevel__Microsoft.EntityFrameworkCore=Warning` (kaksoisalaviiva = `:`). Suodatus tapahtuu **sovelluksessa ennen lähetystä**, joten se säästää myös ingestointikustannusta — toisin kuin KQL-suodatin, joka toimii vasta tallennetulle datalle.

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
| `where` | Suodatus. Tekstiin: `==` tarkka, `startswith`, `has` (kokonainen sana, nopea), `contains` (osajono, hidas) |
| `project` | Valitse ja nimeä sarakkeet (`project timestamp, name, ms = duration`) |
| `extend` | Lisää laskettu sarake (`extend slow = duration > 1000`) |
| `summarize ... by` | Ryhmittely ja aggregointi (`count()`, `avg()`, `percentile(duration, 95)`, `sum(itemCount)`) |
| `bin(timestamp, 5m)` | Pyöristä aika ikkunoihin — `summarize count() by bin(timestamp, 5m)` on aikasarja |
| `order by` / `take` | Järjestys ja rajaus |
| `ago(1h)` | Suhteellinen aika |
| `join kind=inner (taulu) on operation_Id` | Yhdistä kaksi taulua yhteisellä sarakkeella (ks. [Korrelaatio](#korrelaatio-operation_id)) |
| `tostring(customDimensions.X)` | `customDimensions` on `dynamic`-tyyppinen JSON — muunna ennen `by`-ryhmittelyä tai vertailua |
| `render timechart` | Piirrä tulos kaaviona |

Putki luetaan ylhäältä alas: jokainen `|` ottaa edellisen rivin tuloksen ja antaa seuraavalle. `summarize` tuottaa sarakkeita, joiden nimet ovat `count_`, `avg_duration` jne. — niihin viitataan `order by`:ssa.

### Taulut ja sarakkeet

| Taulu | Yksi rivi on | Sarakkeet, joita kysyt useimmin |
|-------|--------------|----------------------------------|
| `requests` | yksi HTTP-pyyntö sovellukseesi | `name` (`GET /api/events`), `resultCode` (`"200"`, teksti), `success`, `duration` (ms), `operation_Id` |
| `dependencies` | yksi lähtevä kutsu: SQL-lause, HTTP-kutsu | `type` (`postgresql`, `Http`), `name` (PostgreSQL: vain `postgresql`), `target` (palvelimen nimi), `data` (SQL-teksti), `success`, `duration` |
| `traces` | yksi `ILogger`-rivi | `message`, `severityLevel` (1 = Information, 2 = Warning, 3 = Error), `customDimensions` (template-kentät, `CategoryName`, `EventId`) |
| `exceptions` | yksi poikkeus | `type` (`Npgsql.NpgsqlException`), `outerMessage`, `innermostMessage`, `details[0].rawStack` |
| `availabilityResults` | yksi availability-testin ajo yhdestä sijainnista | `name`, `location`, `success`, `duration` |
| `customMetrics` | yksi mittauspiste | `name`, `value` |

Kaksi yllätystä, jotka kannattaa tietää etukäteen: `resultCode` on **teksti** (`resultCode == "500"`), ja PostgreSQL-riippuvuuden SQL on sarakkeessa `data`, ei `name`. Kun et tiedä sarakkeita, katso yksi raaka rivi: `dependencies | take 1`.

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
>
> **Vahvista osoite:** kun sähköposti lisätään Action Groupiin, Azure lähettää viestin *"Verify your email address"* kertakäyttökoodilla. Ennen vahvistusta vastaanottaja ei saa yhtään hälytystä, vaikka sääntö näkyy Portalissa *Fired*-tilassa. Koodi vanhenee 30 minuutissa.

### Metric alert vs. log alert

Azure Monitorissa on kaksi hälytyslajia, ja ero on signaalissa:

| | **Metric alert** | **Log alert** (scheduled query) |
|---|---|---|
| Signaali | Numeerinen aikasarja: platform-metriikka (`Http5xx`, CPU) tai App Insights -metriikka | KQL-kysely, jonka tulos ylittää kynnyksen |
| Esimerkki | "`Http5xx` summa > 0 viiden minuutin ikkunassa" | "`exceptions \| where type has 'Npgsql'` palauttaa > 5 riviä 15 minuutissa" |
| Viive | Noin minuutti (metriikat ovat lähes reaaliaikaisia) | Ingestoinnin viive (minuutteja) + arviointiväli |
| Hinta | Ensimmäiset 10 aikasarjaa ilmaisia | Per sääntö ja arviointiväli, kalliimpi |
| Käytä kun | Ehto on numero, joka on jo olemassa | Ehto tarvitsee suodattimen tai yhdistelmän, jota mikään metriikka ei anna |

Kolme lukua määräävät metric alertin käytöksen: **kynnys** (`> 0`), **ikkuna** (`--window-size 5m`: mitä aikaväliä aggregaatti koskee) ja **arviointiväli** (`--evaluation-frequency 1m`: kuinka usein ikkunaa katsotaan). Ikkuna > arviointiväli tarkoittaa, että sama virhe näkyy useassa peräkkäisessä arvioinnissa — hälytys pysyy *Fired*-tilassa kunnes ikkuna on puhdas.

### Hälytysväsymys (alert fatigue) ja resolved-ilmoitus

**Hälytysväsymys** on monitoroinnin oma vikatila: kun hälytyksiä tulee enemmän kuin niihin ehditään reagoida, ihminen oppii ohittamaan ne — myös sen oikean. Kurssin `Http5xx > 0` on opetuskynnys; tuotannossa yksi 5xx tuhannesta on kohinaa. Kolme säädintä:

1. **Kynnys** normaalin liikenteen mukaan (esim. 5xx-osuus > 2 % eikä absoluuttinen määrä)
2. **Ikkuna** niin pitkä, että hetkellinen piikki ei laukaise (5 → 15 min)
3. **Alert processing rule** suunniteltuihin katkoihin — yöllinen pysäytys ei ole häiriö (ks. [Cost Management](Cost-Management.md#automaattinen-sammutus))

Ja jokaisella hälytyksellä pitää olla **reaktio**: jos kukaan ei tee mitään sen lauetessa, se on dashboardin paikka, ei hälytys.

**Resolved-ilmoitus** on sama hälytys toiseen suuntaan: kun ehto ei enää täyty, tila vaihtuu *Fired* → *Resolved* ja Action Group lähettää uuden viestin. Se ei ole roskapostia: päivystäjä tietää, että korjaus purki, tilat voi laskea hälytysten kestosta (mean time to recovery), ja hälytys, joka ei koskaan resolvoidu, kertoo rikkinäisestä säännöstä. Portalin Alerts-sivulla sarake on *Monitor condition*; käyttäjän oma *Alert state* (New / Acknowledged / Closed) on eri asia ja vaihdetaan käsin.

### Smart detection (Failure Anomalies)

Kun App Insights -resurssi luodaan, Azure luo sen viereen automaattisesti **Smart detection** -säännön *Failure Anomalies* ja sille oman Action Groupin (*Application Insights Smart Detection*). Sääntö oppii sovelluksen normaalin virhetason ja hälyttää, kun epäonnistuneiden pyyntöjen osuus **poikkeaa** siitä äkillisesti — ilman kynnystä, jonka sinä asetat. Se täydentää omia sääntöjäsi, ei korvaa niitä: se tarvitsee liikennettä oppiakseen, ja sen viesti on "jotain muuttui", ei "mikä".

Käytännön seuraukset: resurssiryhmässä on resursseja, joita Bicep ei luonut (`microsoft.alertsmanagement/smartDetectorAlertRules/...` ja kaksi ylimääräistä Action Groupia), ja what-if listaa ne `* Ignore` -riveinä — se on oikein, ei virhe. Säännön voi poistaa käytöstä Portalissa (App Insights → Smart detection), mutta kurssilla se saa olla.

### Hälytykset taskussa: Azure-mobiilisovellus

Päivystäjä ei istu sähköpostin ääressä. [Azure mobile app](https://azure.microsoft.com/en-us/get-started/azure-portal/mobile-app/) (Android/iOS) kirjautuu samalla tilillä ja näyttää samat hälytykset **push-ilmoituksina** heti kun ne laukeavat. Lisäksi sovelluksesta näkee resurssien tilan (esim. PostgreSQL-palvelin *Stopped*), voi **käynnistää tai pysäyttää** resurssin, vaihtaa hälytyksen käsittelytilan (*Acknowledged* / *Closed*), seurata Service Healthia ja kuluvan kuun kustannuksia — ja Cloud Shell antaa `az`-komennot käyttöön ilman läppäriä. Sovellus on ikkuna, ei korvike: KQL, dashboardit ja Bicep tehdään edelleen portaalissa ja putkessa.

---

## Availability-testit

**Availability-testi** (saatavuustesti) kutsuu sovellustasi Azuren datakeskuksista ympäri maailmaa ja hälyttää, kun sovellus ei vastaa — vaikka kukaan käyttäjä ei olisi paikalla huomaamassa.

- **Standard test**: HTTP-kutsu valittuun URL:iin (esim. `/health`) 5–15 min välein useasta sijainnista
- Onnistumisehto: statuskoodi (esim. 200) ja/tai vasteaika
- Kytketään Action Groupiin → sähköposti kun X sijaintia Y:stä epäonnistuu

Testi luo itselleen metric alert -säännön (`availabilityResults/availabilityPercentage`), jonka ehto on **"X of Y locations failed"**. Useampi sijainti on olennaista: yksi datakeskus voi epäonnistua verkkosyistä, jotka eivät koske sovellustasi, ja "2 of 5" erottaa sovelluksen vian yhden reitin viasta. Jokainen ajo on yksi rivi `availabilityResults`-taulussa, ja jokainen ajo on laskutettava suoritus (ks. [Kustannukset](#kustannukset)).

Luonti: App Insights → **Availability** → **Add Standard test**. Testaa nimenomaan `/health`-tyyppistä endpointtia, joka tarkistaa myös riippuvuudet — silloin testi kertoo "palvelu toimii", ei vain "prosessi on ylhäällä".

---

## Dashboardit ja workbookit

Hälytys herättää; **dashboard** vastaa kysymykseen "onko kaikki kunnossa?" yhdellä silmäyksellä, ilman että kukaan kirjoittaa KQL:ää muistista keskellä häiriötä.

| | **Dashboard** | **Workbook** |
|---|---|---|
| Mikä | Ruudukko pinnattuja ruutuja: kaavioita, KQL-tuloksia, resurssilistoja | Interaktiivinen raportti: tekstiä, parametreja (aikaväli, ympäristö) ja KQL-kaavioita samassa dokumentissa |
| Miten syntyy | Portalin näkymästä **pin**-kuvakkeella (Failures, Performance, Availability, Logs) | App Insights → **Workbooks** → mallista tai tyhjästä |
| Jakaminen | *Share* julkaisee resurssiryhmään — tiimi näkee saman ruudun; yksityinen oletuksena | Tallentuu resurssina, aina jaettu |
| Käytä kun | "Tilannekuva seinälle": päivystäjän ensimmäinen katse | Toistuva analyysi parametreilla: viikkoraportti, post mortem, kapasiteettikatsaus |

Hyvä aloitusdashboard on neljä ruutua: epäonnistuneet pyynnöt ajan funktiona (Failures), vasteaika (Performance), availability-testin tulokset sijainneittain (Availability) ja yksi oma KQL-kaavio. Dashboard kertoo *että* jokin on vialla; tarkempi *miksi* selviää Failures-näkymästä ja KQL:stä.

---

## Kustannukset

| Erä | Hinta (suuruusluokka) | Huomio |
|-----|------------------------|--------|
| Log Analytics ingestointi | ~2–3 €/GB, **ensimmäiset 5 GB/kk ilmaisia** (per laskutustili) | Pieni kurssisovellus tuottaa megatavuja — käytännössä ilmaista |
| Datan säilytys | 31 pv ilmaista (App Insights -data 90 pv), sen jälkeen ~0,1 €/GB/kk | 30 pv retention riittää kurssille |
| Metric alert -sääntö | ~0,1 €/kk per valvottu aikasarja, **ensimmäiset 10 ilmaisia** | Kurssin kaksi sääntöä: 0 € |
| Availability standard test | Listahinta **~0,0006 € per suoritus** — 5 sijaintia × 5 min välein ≈ 43 000 suoritusta/kk ≈ 25 €/kk | Tarkista omasta Cost analysisista: kurssin testiajon ensimmäisen päivän laskussa riviä ei näkynyt. Jos näkyy, harvempi väli tai vähemmän sijainteja pudottaa suoraan. Poista kurssin päätteeksi |
| Action Group -sähköposti | Ilmainen | |
| Päivittäinen ingestointikatto (*daily cap*, workspace → Usage and estimated costs) | Ilmainen asetus | Suojaa laskua, jos jokin alkaa lokittaa silmukassa; katon ylityksen jälkeen data **hylätään** loppupäiväksi — myös hälytysten tarvitsema |

> **Sampling:** jos dataa syntyy paljon, App Insights ottaa vain otoksen telemetriasta (.NET SDK 3.x rajoittaa jälkien määrää sekunnissa oletuksena). Jo muutaman pyynnön sekuntivauhti merkitsee osan riveistä 50 %:n otokseksi. Tiedä ilmiö: tuotannossa "puuttuva" pyyntö voi olla samplattu pois, ja `count()` laskee tallennetut rivit — `sum(itemCount)` arvioi todellisen määrän.

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
