# Azure Cost Management — kustannusten seuranta ja hallinta

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

---

## Säästökeinot

Karkea järjestys opiskelu-/pienympäristössä — vaikuttavin ensin:

1. **Poista se, mitä et tarvitse** — nollaa kulun kokonaan
2. **Sammuta, kun et käytä** — tietokannan pysäytys yöksi ja viikonlopuksi poistaa compute-kulun (tallennus jää)
3. **Rightsizing** — pienempi SKU mitatun tarpeen mukaan
4. **Lokikuri** — älä ingestoi dataa, jota kukaan ei kysele
5. **Ilmaistasot** — F1-plan, Log Analyticsin ilmaisraja, opiskelijakrediitit

Tuotantomittakaavassa listaan tulevat lisäksi **varaukset** (Reserved Instances / Savings Plan: sitoudut 1–3 vuodeksi, saat 30–60 % alennuksen) ja **skaalaussäännöt** (maksa ruuhkahuipuista vain silloin kun ne ovat käynnissä) — nämä eivät ole opiskelijaympäristön työkaluja, mutta ne kannattaa tuntea.

---

## Automaattinen sammutus

Ihmismuisti on huono säästömekanismi. Aikataulutettu automaatio ei unohda:

- **GitHub Actions schedule** — sama putki, joka deployaa, voi myös sammuttaa: `on: schedule: cron` + OIDC-kirjautuminen + `az postgres flexible-server stop`. Ei uusia työkaluja, jos CI/CD on jo pystyssä
- **Azure Automation / Logic Apps** — Azure-natiivi vaihtoehto samaan
- **DevTest Labs auto-shutdown** — VM-ympäristöihin sisäänrakennettu

Muista sivuvaikutus: jos ympäristöä valvotaan (availability-testit, hälytykset), aikataulutettu sammutus **laukaisee hälytykset joka ilta**. Suunniteltu katko tarvitsee **hälytysten vaimennuksen** samalle aikaikkunalle (alert processing rule / maintenance window) — muuten koulutat itsesi ohittamaan hälytykset, ja se on monitoroinnin vaarallisin lopputulos (alert fatigue).

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
