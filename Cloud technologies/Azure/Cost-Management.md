# Azure Cost Management — kustannusten seuranta ja hallinta
> 🇬🇧 English version: [Cost-Management.md](../eng/Azure/Cost-Management.md)

## Sisällysluettelo

1. [CapEx vs. OpEx — miksi pilvilasku on erilainen](#capex-vs-opex--miksi-pilvilasku-on-erilainen)
2. [Miten Azure-lasku syntyy: mittarit](#miten-azure-lasku-syntyy-mittarit)
3. [Cost Management -työkalut](#cost-management--työkalut)
4. [Budjetit ja hälytykset](#budjetit-ja-hälytykset)
5. [Tagit kustannusten kohdistamisessa](#tagit-kustannusten-kohdistamisessa)
6. [Rightsizing — oikea SKU oikeaan tarpeeseen](#rightsizing--oikea-sku-oikeaan-tarpeeseen)
7. [Piilokustannukset](#piilokustannukset)
8. [Säästökeinot](#säästökeinot)
9. [Automaattinen sammutus](#automaattinen-sammutus)
10. [AI kustannusanalyysissä](#ai-kustannusanalyysissä)
11. [Parhaat käytännöt](#parhaat-käytännöt)

---

## CapEx vs. OpEx — miksi pilvilasku on erilainen

| | **CapEx** (investointi) | **OpEx** (käyttökulu) |
|--|--------------------------|------------------------|
| Malli | Osta palvelin etukäteen | Maksa käytöstä jälkikäteen |
| Kustannus | Suuri kertasumma, poistot vuosille | Juokseva kuukausilasku |
| Riski | Yli-/alimitoitus lukittu vuosiksi | Mitoitusta voi muuttaa tänään |
| Kenen ongelma | Talousosasto budjetoi kerran | **Jokainen kehittäjä vaikuttaa laskuun joka päivä** |

Pilvessä arkkitehtuuripäätökset **ovat** kustannuspäätöksiä: SKU-valinta, skaalaussäännöt, lokien määrä ja unohtunut testiympäristö näkyvät suoraan seuraavan kuun laskulla. Siksi kustannusosaaminen kuuluu kehittäjälle, ei vain taloushallinnolle — tätä ajattelua kutsutaan nimellä **FinOps**.

Kääntöpuoli: OpEx-lasku voi myös **yllättää**. CapEx-palvelin ei maksa enempää, vaikka sitä käyttäisi väärin — pilviresurssi maksaa tasan niin kauan ja niin paljon kuin se on olemassa ja mitä se tekee.

---

## Miten Azure-lasku syntyy: mittarit

Azure laskuttaa **mittareilla** (meter). Yksi resurssi tuottaa tyypillisesti useita mittareita — ja osa niistä juoksee, vaikka kukaan ei käyttäisi palvelua:

| Resurssi | Mittarit (esimerkkejä) | Juokseeko idlenä? |
|----------|--------------------------|--------------------|
| App Service Plan | Instanssitunnit SKU:n mukaan | **Kyllä** — plan maksaa, vaikka appi ei saisi yhtään pyyntöä |
| PostgreSQL Flexible Server | vCore-tunnit + tallennustila (GB/kk) + varmuuskopiot | Compute **kyllä** kun käynnissä; **tallennus aina**, myös pysäytettynä |
| Log Analytics | Ingestoitu data (GB) + säilytys yli ilmaisrajan | Ei — vain datasta |
| Availability test (standard) | Testiajot | Kyllä — testaa aikataululla |
| Metric alert -säännöt | Kiinteä kk-hinta per sääntö | Kyllä (senttejä) |
| Kaista (egress) | Ulos lähtevä data (GB) | Ei |

Kaksi seurausta:

1. **"En käyttänyt sitä" ei tarkoita "se ei maksanut".** Provisioitu kapasiteetti (App Service plan, tietokannan compute) laskuttaa ajasta, ei käytöstä.
2. **Poistaminen ja pysäyttäminen ovat eri asioita.** Pysäytetty PostgreSQL ei laskuta computesta, mutta tallennustila laskuttaa edelleen. Vain poistettu resurssi on ilmainen.

### SKU, mittari ja mittayksikkö

Kolme sanaa, joilla hinnasto puhuu:

| Termi | Mikä se on | Esimerkki |
|-------|------------|-----------|
| **SKU** (stock keeping unit) | Tuotteen *kokoluokka*, jonka valitset: nimi, jolla Azure tietää mitä kapasiteettia annat | App Service `F1`, `B1`, `S1`; PostgreSQL `Standard_B1ms`; Storage `Standard_LRS` |
| **Mittari** (meter) | Yksi laskutettava asia SKU:n sisällä. Yhdellä resurssilla on tyypillisesti useita | B1ms-palvelin: *compute-tunnit*, *tallennus GB/kk*, *varmuuskopiotallennus GB/kk* |
| **Mittayksikkö** (unit of measure) | Missä yksikössä mittari laskee | `1 Hour`, `1 GB/Month`, `10K` (operaatiota), `1/Execution` |

Lasku on siis summa riveistä *mittari × käytetyt yksiköt × yksikköhinta*. Kun ennustat omaa laskuasi, aloita SKU:sta, listaa sen mittarit ja arvioi jokaiselle yksiköt — se on tämän sivun ensimmäisen taulukon sarake "Mittarit".

### Listahinta vs. lasku: Retail Prices API

Hinnoittelulaskuri on yksi lähde listahinnoille. Toinen on **Retail Prices API**: julkinen, kirjautumaton rajapinta, joka palauttaa saman hinnaston JSON:na.

```powershell
$Filter = "armRegionName eq 'francecentral' and priceType eq 'Consumption' and serviceName eq 'Azure Database for PostgreSQL'"
(Invoke-RestMethod "https://prices.azure.com/api/retail/prices?currencyCode=EUR&`$filter=$Filter").Items |
  Select-Object skuName, meterName, retailPrice, unitOfMeasure | Format-Table
```

| Parametri | Merkitys |
|-----------|----------|
| `armRegionName` | Alue — sama SKU maksaa eri alueilla eri verran |
| `priceType eq 'Consumption'` | Käytön mukaan laskutettava hinta (vaihtoehdot: `Reservation`, `DevTestConsumption`) |
| `currencyCode=EUR` | Valuutta; oletus USD |
| `NextPageLink` | Vastaus on sivutettu (100 riviä) — seuraava sivu tästä kentästä |

**Listahinta on ennuste, lasku on totuus.** Toteutunut lasku poikkeaa listahinnasta ainakin näistä syistä: ilmaistasot (Log Analyticsin 5 GB, App Servicen F1), opiskelija- ja sponsorikrediitit, mittari joka ei kyseisessä tilauksessa ole käytössä tai näkyy viiveellä, ja pyöristys mittayksikön tarkkuuteen. Siksi arvio tehdään API:sta tai laskurista, mutta **tarkistetaan Cost analysisistä** muutaman päivän kuluttua.

---

## Cost Management -työkalut

Portal → resurssiryhmä (tai tilaus) → **Cost Management**:

| Työkalu | Mihin |
|---------|-------|
| **Cost analysis** | Toteutunut kulutus: päivittäin, resurssikohtaisesti, tageittain, palveluittain; myös ennuste (forecast) |
| **Budgets** | Kulutusrajat + hälytykset (ks. alla) |
| **Cost alerts** | Lauenneiden budjettihälytysten lista |
| **Advisor recommendations** | Azuren omat säästösuositukset (mm. vajaakäyttöiset resurssit) |

### Cost analysis -näkymän tehokäyttö

- **Scope** ensin oikein: resurssiryhmä = projektin kulut, tilaus = kaikki
- **Group by: Resource** — mikä maksaa eniten?
- **Group by: Tag → Environment** — dev vs. test vs. prod (edellyttää, että tagit ovat kunnossa!)
- **Granularity: Daily** — milloin kulutus muuttui? (Piikin päivämäärä + `git log` = syyllinen löytyy usein heti)
- **Download** — CSV ulos analyysiä tai AI:ta varten

> **Viive:** kulutusdata **ei ole reaaliaikaista** — se päivittyy tyypillisesti 8–24 tunnin viiveellä. Tänään luotu resurssi näkyy kuluissa aikaisintaan huomenna. Tämä on yleisin hämmennyksen aihe.

### Accumulated, Daily ja kaksi ennustetta

Cost analysisin kaaviolla on kaksi perusmuotoa. **Accumulated** piirtää kuukauden kertymän nousevana viivana — "paljonko tähän mennessä, ja mihin ollaan menossa"; budjetti näkyy samassa kuvassa katkoviivana. **Daily** piirtää jokaisen päivän omana pylväänään — "milloin jokin muuttui": päivä, jona plan skaalattiin tai tietokanta luotiin, erottuu heti, ja `git log` kertoo loput.

Ennusteita on **kaksi erilaista**, ja ne eivät näytä samaa lukua:

| Ennuste | Missä | Miten lasketaan | Milloin näkyy |
|---------|-------|------------------|---------------|
| Kaavion *Forecast* | Cost analysis | Mallinnetaan kuukauden trendistä | Vasta kun dataa on useita päiviä — uudessa resurssiryhmässä *"Forecast unavailable"* on normaalia |
| Budjetin `forecastSpend` | Budgets-lista, budjetin API | Karkeampi arvio nykyisestä päivätasosta | Jo ensimmäisinä päivinä, ennen kuin `currentSpend` edes päivittyy |

**Untagged-kori.** Kun ryhmittelet tagilla, näet usein siivun *Untagged*, vaikka Bicep tagittaa kaiken minkä luot. Syy: Azure luo resursseja *puolestasi* — availability-testin, smart detection -säännön, Portal-wizardin tekemät hälytyssäännöt — eivätkä ne peri tageja. Pienessä ympäristössä harmiton; isossa organisaatiossa syy ottaa käyttöön Azure Policy, joka kieltää tagittomat resurssit.

### Sama data komentoriviltä: Cost Management API ja az rest

Cost analysis on käyttöliittymä **Cost Management query API:lle** — samaa rajapintaa voi kutsua itse, kun tarvitset luvut skriptiin tai kuvakaappaukseen:

```powershell
$Body = @{
  type      = "ActualCost"          # toteutunut; "AmortizedCost" jakaa varausten hinnan käyttöpäiville
  timeframe = "MonthToDate"         # tai Custom + timePeriod
  dataset   = @{
    granularity = "None"            # tai "Daily"
    aggregation = @{ totalCost = @{ name = "Cost"; function = "Sum" } }
    grouping    = @(@{ type = "Dimension"; name = "ResourceId" })   # tai TagKey + tagin nimi
  }
} | ConvertTo-Json -Depth 5 -Compress

az rest --method post `
  --url "https://management.azure.com$Scope/providers/Microsoft.CostManagement/query?api-version=2023-11-01" `
  --body $Body --query "properties.rows" --output table
```

**`az rest`** lähettää allekirjoitetun HTTP-kutsun mihin tahansa Azure Resource Manager -rajapintaan kirjautuneen käyttäjän tokenilla. Sitä tarvitaan, kun CLI-komento puuttuu tai elää preview-laajennuksessa (budjetit, alert processing rules, kustannuskyselyt) — ja sama kutsu on dokumentti siitä, mitä Portal tekee napin takana.

**`--query`** on JMESPath-lauseke, joka suodattaa ja muotoilee vastauksen JSON:n ennen tulostusta. Perusmuodot:

| Lauseke | Tekee |
|---------|-------|
| `properties.rows` | Poimii polun |
| `[].{name:name, state:properties.state}` | Projisoi jokaisesta taulukon alkiosta uuden olion valituilla kentillä |
| `[?average != null]` | Suodattaa alkiot ehdolla |
| `value[0].timeseries[0].data` | Indeksit taulukkoon |
| `--output table` / `tsv` / `json` | Tulostusmuoto; `tsv` sopii muuttujaan tallennukseen |

> **Throttlaus:** kyselyrajapinta vastaa `429 Too many requests`, jos kutsuja tulee enemmän kuin muutama minuutissa samaan scopeen. Odota minuutti (`Retry-After`-otsake kertoo kauanko) äläkä laita kyselyä silmukkaan.

---

## Budjetit ja hälytykset

**Budjetti** on valvontaraja, ei katkaisija: se **hälyttää** sähköpostilla, mutta **ei pysäytä** kulutusta eikä poista resursseja.

| Asetus | Suositus opiskeluympäristöön |
|--------|------------------------------|
| Scope | Kurssin resurssiryhmä (+ halutessa toinen budjetti koko tilaukselle) |
| Reset period | Monthly |
| Hälytysrajat | **Actual** 50 % / 80 % / 100 % + **Forecasted** 100 % |

**Actual vs. Forecasted:**

- **Actual** laukeaa, kun toteutunut kulutus ylittää rajan — vahinko on jo (osin) tapahtunut
- **Forecasted** laukeaa, kun Azuren ennuste kuun loppusummasta ylittää rajan — **ennakkovaroitus**, ehdit reagoida ennen kuin raja oikeasti ylittyy

Budjettien arviointi tapahtuu jaksoittain (tunneissa, ei minuuteissa) — budjetti ei korvaa metriikkahälytyksiä, eikä metriikkahälytys budjettia. Eri työkalut eri aikaskaaloille.

---

## Tagit kustannusten kohdistamisessa

Cost analysis osaa ryhmitellä kulut **tageilla** — mutta vain, jos tagit on asetettu johdonmukaisesti. Ilman tageja tilauksen lasku on yksi iso möykky, josta kukaan ei tiedä, kenen projekti sen aiheutti.

Suositeltu perussetti (sama kuin kurssin Bicep-pohjissa):

| Tagi | Esimerkki | Vastaa kysymykseen |
|------|-----------|---------------------|
| `Environment` | `dev` / `test` / `prod` | Minkä ympäristön kulu? |
| `Project` / `Course` | `cloud26` | Minkä hankkeen kulu? |
| `Owner` | `etunimi.sukunimi@edu.xamk.fi` | Keneltä kysytään "tarvitaanko tätä vielä?" |
| `CostCenter` | `IT-1234` | Mille kustannuspaikalle lasku kohdistetaan? |

Käytännöt, jotka tekevät tageista luotettavia:

- Tagit tulevat **IaC:stä** (Bicep `tags`-objekti) — käsin lisätyt unohtuvat
- Huom: resurssiryhmän tagit **eivät periydy** resursseille automaattisesti — siksi tagit asetetaan jokaiselle resurssille (tai perintä pakotetaan Azure Policyllä)

---

## Rightsizing — oikea SKU oikeaan tarpeeseen

**Rightsizing** = kapasiteetin sovittaminen todelliseen, mitattuun tarpeeseen — ei arvaukseen eikä "varmuuden vuoksi" -kertoimeen.

Prosessi:

1. **Mittaa** todellinen käyttö: App Servicen CPU/muisti, tietokannan CPU/yhteydet, vasteajat (Application Insights / Metrics)
2. **Vertaa** varattuun kapasiteettiin: jos B1-plan käy 3 % CPU:lla, maksat 97 % tyhjästä
3. **Pienennä** yksi porras kerrallaan ja seuraa vaikutusta — monitorointi kertoo, menikö liian pieneksi
4. **Toista** — tarve muuttuu ajan myötä

Muista SKU-portaiden **ominaisuuskynnykset**: halvempi porras voi pudottaa pois ominaisuuksia, ei vain tehoa (esim. App Service F1: ei Always On -toimintoa eikä skaalausta; Basic: ei staging slotteja). Rightsizing-päätös on siis ominaisuus- **ja** kapasiteettipäätös.

Vastakkainen suunta on yhtä tärkeä: jos mittarit näyttävät jatkuvaa 80 %+ kuormaa tai jonoutumista, SKU on **alimitoitettu** — se maksaa vasteajoissa ja virheinä.

### Todisteet: planin CPU- ja muistimetriikat

Rightsizing-päätöksen luvut ovat **platform-metriikoita**: Azure kerää ne jokaisesta resurssista ilmaiseksi ja ilman SDK:ta. App Servicessä ne luetaan **planin** tasolta (`Microsoft.Web/serverfarms`), koska plan on se, minkä koosta maksat: `CpuPercentage` ja `MemoryPercentage`.

Kaksi aggregaatiota kertovat eri asian: **Avg** on taso, jolla sovellus elää, **Max** on piikit — tyypillisesti deployt ja uudelleenkäynnistykset, eivät käyttäjät. Päätös tehdään keskiarvosta, mutta piikit kertovat, mahtuuko huippu pienempään SKU:hun.

```powershell
az monitor metrics list `
  --resource plan-myapp-dev --resource-group $RG --resource-type Microsoft.Web/serverfarms `
  --metric CpuPercentage --offset 7d --interval PT6H --aggregation Average Maximum `
  --query "value[0].timeseries[0].data[?average != null].{time:timeStamp, avg:average, max:maximum}" --output table
# sama --metric MemoryPercentage
```

`--interval` hyväksyy vain tietyt arvot (`PT1M`, `PT5M`, `PT15M`, `PT30M`, `PT1H`, `PT6H`, `PT12H`, `P1D`); viikon jaksolle `PT6H` tai `P1D` on luettava. Katso **molemmat** mittarit: kurssisovelluksella CPU on yksinumeroinen, mutta muisti voi olla 70 % B1:n 1,75 GB:stä — ja F1 antaa 1 GB. Rightsizing päätetään siitä mittarista, joka on lähimpänä kattoaan.

### Ominaisuuskynnykset: Always On ja F1:n kiintiö

Halvempi porras pudottaa ominaisuuksia, ei vain tehoa. Kaksi App Servicen esimerkkiä, jotka näkyvät vasta kun ne puuttuvat:

- **Always On** (Basic ja ylemmät): App Service pitää prosessin lämpimänä myös ilman liikennettä. Ilman sitä (F1, Shared) sovellus nukahtaa ~20 minuutin hiljaisuuden jälkeen, ja seuraava pyyntö kestää sekunteja — availability-testille se näyttää katkolta, ja hälytykset *läpättävät*. Bicepissä `siteConfig.alwaysOn`; skaalattaessa alaspäin se pitää kytkeä pois **ennen** planin vaihtoa (`az webapp config set --always-on false`), muuten deploy kaatuu `Conflict … AlwaysOn … not allowed in the target compute mode`.
- **F1:n päiväkiintiö**: 60 CPU-minuuttia vuorokaudessa. Kun se täyttyy, App Service pysäyttää sovelluksen: `/health` vastaa HTML-sivulla *Error 403 - This web app is stopped*, `az webapp show` näyttää `state: QuotaExceeded`, deploy kaatuu `Site Disabled (CODE: 403)`, ja kiintiö nollautuu keskiyöllä UTC. Huomaa, että **monitorointi itse kuluttaa kiintiötä**: viidestä sijainnista viiden minuutin välein käyvä availability-testi on 1 440 kutsua päivässä, jokainen avaa tietokantayhteyden.

Rightsizing-kysymys ei siis ole "riittääkö F1 käyttäjilleni" vaan "riittääkö F1 käyttäjilleni *ja kaikelle muulle, mikä sovellusta kutsuu*".

---

## Piilokustannukset

Erät, jotka eivät näy arkkitehtuurikaaviossa mutta näkyvät laskulla:

| Piilokustannus | Mistä syntyy | Vastalääke |
|-----------------|---------------|-------------|
| **Idle-resurssit** | Unohtunut testiympäristö, POC, "katson tätä myöhemmin" | Tagit (Owner!), säännöllinen siivous, automaattinen sammutus |
| **Egress** | Azuresta ulos lähtevä data | Pidä data ja compute samassa regionissa; huomioi suurissa datamäärissä |
| **Diagnostiikka ja lokit** | Log Analytics -ingestointi GB-hinnalla; runsas debug-loki tuotannossa | Lokitasot kuntoon, sampling, retention järkeväksi |
| **Ylimitoitettu tallennus** | Tietokannan levykokoa ei voi pienentää jälkikäteen (kasvattaa voi) | Aloita pienestä |
| **Varmuuskopiot ja säilytys** | Yli ilmaisrajan menevä backup-tila ja pitkä retention | Tarkista oletukset — älä säilö "ikuisesti" tottumuksesta |
| **Pysäytetyn resurssin tallennus** | Pysäytetty VM/tietokanta laskuttaa levystä | Poista, jos et oikeasti tarvitse |
| **Availability-testin suoritukset** | Listahinta per suoritus: 5 sijaintia × 5 min välein ≈ 43 000 suoritusta/kk | Tarkista oma lasku; harvempi väli tai vähemmän sijainteja pudottaa suoraan; poista kurssin päätteeksi |

---

## Säästökeinot

Karkea järjestys opiskelu-/pienympäristössä — vaikuttavin ensin:

1. **Poista se, mitä et tarvitse** — nollaa kulun kokonaan
2. **Sammuta, kun et käytä** — tietokannan pysäytys yöksi ja viikonlopuksi poistaa compute-kulun (tallennus jää)
3. **Rightsizing** — pienempi SKU mitatun tarpeen mukaan
4. **Lokikuri** — älä ingestoi dataa, jota kukaan ei kysele
5. **Ilmaistasot** — F1-plan, Log Analyticsin ilmaisraja, opiskelijakrediitit

Tuotantomittakaavassa listaan tulevat lisäksi **varaukset** (Reserved Instances / Savings Plan: sitoudut 1–3 vuodeksi, saat 30–60 % alennuksen) ja **skaalaussäännöt** (maksa ruuhkahuipuista vain silloin kun ne ovat käynnissä) — nämä eivät ole opiskelijaympäristön työkaluja, mutta ne kannattaa tuntea.

### Tuotannon hintatekijät: HA, varaukset ja säästösuunnitelmat

Kun sama arkkitehtuuri hinnoitellaan tuotantoon, lasku moninkertaistuu muutamasta syystä, jotka kannattaa osata nimetä:

| Tekijä | Mitä maksat | Miksi |
|--------|-------------|-------|
| **PostgreSQL High Availability** | Compute **×2** | HA = *toinen, valmiiksi käynnissä oleva palvelin* (standby) toisessa saatavuusvyöhykkeessä (*zone-redundant*) tai samassa (*same-zone*); failover minuutissa ilman datan menetystä. Yksittäinen kurssipalvelin ei ole HA |
| **App Service Standard / Premium** | Instanssihinta 5–10× Basic | Deployment slotit, autoscale, useampi instanssi, parempi SLA |
| **Isommat SKU:t ja useampi instanssi** | Lineaarisesti | Skaalaus ulos kertoo planin hinnan instanssimäärällä |

Vastapainona tuotannolla on **sitoumusalennukset**, joita opiskelijaympäristössä ei ole:

| | **Reserved Instance** | **Savings Plan** |
|--|----------------------|------------------|
| Sitoudut | Tiettyyn SKU:hun ja alueeseen 1 tai 3 vuodeksi | Tuntihintaan (esim. 5 €/h compute-kulua) 1 tai 3 vuodeksi |
| Alennus | Suurin (jopa 60–70 %) | Pienempi (jopa ~65 % laskennallisesti, käytännössä vähemmän) |
| Joustavuus | Vähäinen — SKU:n vaihto on vaihto-operaatio | Kattaa minkä tahansa SKU:n ja alueen sitoumukseen asti |
| Kannattaa kun | Peruskuorma on tasainen ja tiedossa vuosiksi | Kuorma on tasainen mutta muoto muuttuu |

Molemmissa luovut siitä, mikä OpEx-mallissa oli etu: kyvystä pienentää tänään. Siksi sitoumus tehdään vasta mitatun peruskuorman mukaan — ei koko kapasiteetille.

---

## Automaattinen sammutus

Ihmismuisti on huono säästömekanismi. Aikataulutettu automaatio ei unohda:

- **GitHub Actions schedule** — sama putki, joka deployaa, voi myös sammuttaa: `on: schedule: cron` + OIDC-kirjautuminen + `az postgres flexible-server stop`. Ei uusia työkaluja, jos CI/CD on jo pystyssä
- **Azure Automation / Logic Apps** — Azure-natiivi vaihtoehto samaan
- **DevTest Labs auto-shutdown** — VM-ympäristöihin sisäänrakennettu

Muista sivuvaikutus: jos ympäristöä valvotaan (availability-testit, hälytykset), aikataulutettu sammutus **laukaisee hälytykset joka ilta**. Suunniteltu katko tarvitsee **hälytysten vaimennuksen** samalle aikaikkunalle (alert processing rule / maintenance window, ks. alla) — muuten koulutat itsesi ohittamaan hälytykset, ja se on monitoroinnin vaarallisin lopputulos ([alert fatigue](Monitoring-and-Application-Insights.md#hälytysväsymys-alert-fatigue-ja-resolved-ilmoitus)).

### GitHub Actions schedule: cron, UTC ja best effort

```yaml
on:
  schedule:
    - cron: '0 18 * * *'   # minuutti tunti päivä kuukausi viikonpäivä
  workflow_dispatch:       # manuaalinen ajo: testaus ja todiste
```

| Kenttä | Arvo | Esimerkkejä |
|--------|------|-------------|
| minuutti, tunti | `0 18` | `30 5` = 05:30; `*/15 * * * *` = 15 min välein |
| päivä, kuukausi | `* *` | `1 *` = joka kuun 1. |
| viikonpäivä | `*` | `1-5` = ma–pe (0 = sunnuntai) |

Neljä sääntöä, jotka yllättävät:

1. **Cron on aina UTC.** `0 18` on Helsingissä 20:00 talvella ja 21:00 kesällä — kesäaika siirtää kellosi, ei cronia.
2. **Ajo on best effort.** GitHub käynnistää ajon "joskus slotin jälkeen": ruuhkassa minuuteista tunteihin myöhässä (kurssin testissä 5 h), ja juuri mergetty aikataulu voi ohittaa ensimmäisen slottinsa kokonaan. Minuutilleen tärkeä ajastus kuuluu Azure-natiiville ajastimelle (Logic Apps, Automation).
3. **Vain oletushaara.** Aikataulu luetaan `main`-haaran tiedostosta — PR-haarassa se ei laukea koskaan.
4. **60 päivän sääntö.** Jos repositoriossa ei ole aktiivisuutta 60 päivään, GitHub kytkee aikataulut pois.

`workflow_dispatch` samassa tiedostossa antaa *Run workflow* -napin: sillä testataan heti ja todistetaan OIDC-kirjautuminen. Aikataulun todiste on silti vasta ajo, jonka tapahtuma on `schedule` (`gh run list --event schedule`). Tee stop-askeleesta **idempotentti** — tarkista tila ennen komentoa — niin manuaaliajo jo pysäytetyn palvelimen päälle ei kaadu ([idempotenssi](Infrastructure-as-Code.md#idempotenssi)).

### Hälytysten vaimennus: alert processing rule

**Alert processing rule** on Azure Monitorin sääntö, joka muokkaa laukeavien hälytysten käsittelyä scopen (esim. resurssiryhmä) sisällä. Vaimennusmuoto `RemoveAllActionGroups` tarkoittaa: hälytys **laukeaa ja kirjautuu** historiaan normaalisti, mutta Action Groupia ei kutsuta — sähköposti jää tulematta. Totuus säilyy, postilaatikko säästyy. Aikataulu voi olla kertaluonteinen (huoltoikkuna) tai toistuva (Daily, Weekly), ja keskiyön ylittävä ikkuna 20:00 → 08:00 on yksi Daily-toisto.

```powershell
$Body = @{
  location   = "Global"
  properties = @{
    scopes   = @($Scope)
    enabled  = $true
    actions  = @(@{ actionType = "RemoveAllActionGroups" })
    schedule = @{
      timeZone    = "FLE Standard Time"
      recurrences = @(@{ recurrenceType = "Daily"; startTime = "20:00:00"; endTime = "08:00:00" })
    }
  }
} | ConvertTo-Json -Depth 6 -Compress
az rest --method put --body $Body `
  --url "https://management.azure.com$Scope/providers/Microsoft.AlertsManagement/actionRules/apr-quiet-hours?api-version=2021-08-08"
```

**Aikavyöhykkeet** annetaan Windowsin aikavyöhyke-ID:inä, eivät IANA-niminä: Helsinki on `FLE Standard Time` (Finland, Lithuania, Estonia), Keski-Eurooppa `W. Europe Standard Time`, UTC `UTC`. ID kattaa kesäajan automaattisesti — sääntö seuraa seinäkelloa. Cron ei seuraa, joten UTC-aikataulun ja paikallisen ikkunan on katettava toisensa **sekä talvi- että kesäajassa** (18:00 UTC = 20:00 tai 21:00 Helsinki → ikkuna 20:00–08:00 riittää molemmissa). CLI-komento `az monitor alert-processing-rule` on preview-laajennuksessa; REST-kutsu on vakaa ja sama resurssi on kirjoitettavissa Bicepillä (`Microsoft.AlertsManagement/actionRules`).

---

## AI kustannusanalyysissä

Kulutusdata on taulukkomuotoista ja selitettävää — AI:lle luontevaa maastoa:

| Käyttö | Miten |
|--------|-------|
| **Kulutusraportin tulkinta** | Vie Cost analysis CSV:nä → pyydä AI:ta erittelemään suurimmat ajurit ja poikkeamat |
| **Säästöehdotukset** | Pyydä 2–3 konkreettista toimenpidettä €-arvioineen omasta datastasi |
| **SKU-vertailut** | "App Service B1 vs. F1 vs. Container Apps tälle kuormalle" — vaihtoehtojen kartoitus |
| **Copilot in Azure** | Kustannuskysymykset suoraan portaalissa luonnollisella kielellä |

**Kriittisyys kuuluu kuvaan:** AI:n hintatiedot voivat olla vanhentuneita tai väärän regionin/valuutan mukaisia. Tarkista €-väitteet aina [hinnoittelulaskurista](https://azure.microsoft.com/en-us/pricing/calculator/) tai omasta kulutusdatastasi ennen kuin teet päätöksiä. AI on hyvä *analyysin jäsentäjä* ja huono *hinnaston muistaja*.

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Budjetti + hälytykset ennen ensimmäistäkään maksullista resurssia** — Actual 50/80/100 % + Forecasted 100 %
- **Tagit kaikkiin resursseihin IaC:n kautta** — kustannukset kohdistuvat itsestään
- **Katso Cost analysis viikoittain** — pienet yllätykset eivät ehdi kasvaa isoiksi
- **Sammuta ja siivoa automaattisesti** — äläkä unohda hälytysten vaimennusta katkon ajaksi
- **Rightsizing mittausten perusteella** — monitorointidata on jo olemassa, käytä sitä
- **Poistettu > pysäytetty > pienennetty** — vaikuttavuusjärjestys

### ❌ Vältä näitä

- Älä luota siihen, että "huomaan kyllä laskusta" — data tulee 8–24 h viiveellä ja lasku kerran kuussa
- Älä jätä resurssia "varalta" käyntiin — tagaa Owner ja poista, kun omistaja ei enää tarvitse
- Älä valitse SKU:ta arvaamalla ylöspäin "ettei vaan lopu kesken" — mittaa ja säädä
- Älä tee kustannuspäätöksiä pelkän AI:n hintamuistin varassa — laskuri ja oma data ratkaisevat

---

## Seuraavaksi

- [Azure Monitor ja Application Insights](Monitoring-and-Application-Insights.md) - Mittausdata, johon rightsizing perustuu
- [Azure App Service](App-Service.md) - SKU-portaat ja niiden ominaisuudet
- [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md) - Stop/start ja tallennuskustannus
- [Infrastructure as Code](Infrastructure-as-Code.md) - Tagit ja SKU:t koodissa

## Takaisin

- [Azure-palvelut — Yleiskatsaus](README.md)
