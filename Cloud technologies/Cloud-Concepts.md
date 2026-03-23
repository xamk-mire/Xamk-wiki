# Pilvipalvelukonseptit (Cloud Concepts)

## Sisällysluettelo

1. [Mikä on pilvipalvelu?](#mikä-on-pilvipalvelu)
2. [Jaetun vastuun malli](#jaetun-vastuun-malli)
3. [Pilvipalvelumallit: IaaS, PaaS, SaaS](#pilvipalvelumallit-iaas-paas-saas)
4. [Käyttöönottomallit](#käyttöönottomallit)
5. [Pilvipalvelun hyödyt](#pilvipalvelun-hyödyt)
6. [Skaalautuvuus](#skaalautuvuus)
7. [CapEx vs. OpEx](#capex-vs-opex)
8. [Yhteenveto](#yhteenveto)

---

## Mikä on pilvipalvelu?

**Pilvipalvelu** (cloud computing) tarkoittaa IT-resurssien — palvelimien, tallennustilan, tietokantojen, verkkojen ja ohjelmistojen — tarjoamista internetin kautta. Sen sijaan, että ostat ja ylläpidät omia palvelimia, vuokraat niitä pilvipalveluntarjoajalta (esim. Microsoft Azure, AWS, Google Cloud).

**Perusidea:**

```
Perinteinen malli (On-Premises):
┌──────────────────────────────────────────┐
│  Oma palvelinhuone                       │
│  → Ostat palvelimet                      │
│  → Asennat käyttöjärjestelmän            │
│  → Hallinnoit verkon, sähkön, jäähdytys  │
│  → Ylläpidät 24/7                        │
│  → Skaalaat ostamalla lisää laitteita    │
└──────────────────────────────────────────┘

Pilvipalvelu (Cloud):
┌──────────────────────────────────────────┐
│  Pilvipalveluntarjoaja (Azure, AWS...)   │
│  → Vuokraat resursseja tarpeen mukaan    │
│  → Maksat vain käytöstä                  │
│  → Skaalaat nappia painamalla            │
│  → Tarjoaja huolehtii infrastruktuurista │
└──────────────────────────────────────────┘
```

### Miksi pilvipalvelut?

- **Ei suuria alkuinvestointeja** — ei tarvitse ostaa palvelimia
- **Joustavuus** — resursseja voi lisätä ja vähentää tarpeen mukaan
- **Globaali saavutettavuus** — palvelut ovat käytettävissä kaikkialta
- **Automaattiset päivitykset** — pilvipalveluntarjoaja huolehtii ylläpidosta
- **Korkea saatavuus** — palveluntarjoajan datakeskukset ovat vikasietoisia

---

## Jaetun vastuun malli

**Shared Responsibility Model** määrittää, kuka vastaa mistäkin: pilvipalveluntarjoaja vai asiakas. Vastuu jakautuu eri tavalla riippuen palvelumallista.

```
On-Premises     IaaS            PaaS            SaaS
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│ Data     │ A │ Data     │ A │ Data     │ A │ Data     │ A
│ Sovellus │ A │ Sovellus │ A │ Sovellus │ A │ Sovellus │ T
│ Runtime  │ A │ Runtime  │ A │ Runtime  │ T │ Runtime  │ T
│ OS       │ A │ OS       │ A │ OS       │ T │ OS       │ T
│ Virtuali-│ A │ Virtuali-│ T │ Virtuali-│ T │ Virtuali-│ T
│ sointi   │   │ sointi   │   │ sointi   │   │ sointi   │
│ Palvelin │ A │ Palvelin │ T │ Palvelin │ T │ Palvelin │ T
│ Tallennus│ A │ Tallennus│ T │ Tallennus│ T │ Tallennus│ T
│ Verkko   │ A │ Verkko   │ T │ Verkko   │ T │ Verkko   │ T
└──────────┘   └──────────┘   └──────────┘   └──────────┘

A = Asiakas (sinä)    T = Tarjoaja (Azure/AWS/GCP)
```

**Pääsääntö:** Mitä korkeampi abstraktiotaso (IaaS → PaaS → SaaS), sitä enemmän vastuu siirtyy tarjoajalle.

**Asiakas vastaa aina:**
- Omasta datasta ja sen suojaamisesta
- Käyttäjätunnuksista ja pääsynhallinnasta
- Laitteista, joilla palvelua käytetään

**Tarjoaja vastaa aina:**
- Fyysisestä datakeskuksesta (tilat, sähkö, jäähdytys)
- Fyysisestä verkosta
- Fyysisistä palvelimista

---

## Pilvipalvelumallit: IaaS, PaaS, SaaS

### IaaS — Infrastructure as a Service

**IaaS** tarjoaa perus IT-infrastruktuurin: virtuaalikoneet, verkot ja tallennustilan. Asiakas hallinnoi käyttöjärjestelmästä ylöspäin.

```
Sinä hallinnoit:          Azure tarjoaa:
┌─────────────────┐      ┌─────────────────┐
│ Sovellus        │      │                 │
│ Runtime (.NET)  │      │ Virtuaalikone   │
│ Käyttöjärjest.  │      │ Verkko          │
│ Tietoturva      │      │ Tallennustila   │
└─────────────────┘      │ Fyysinen infra  │
                         └─────────────────┘
```

**Esimerkkejä:**
- Azure Virtual Machines
- Azure Virtual Network
- Azure Disk Storage

**Sopii kun:** Tarvitset täyden hallinnan käyttöjärjestelmästä, asennat erikoisohjelmistoja, migroit olemassa olevia palvelimia pilveen.

### PaaS — Platform as a Service

**PaaS** tarjoaa valmiin alustan sovellusten kehittämiseen ja julkaisemiseen. Sinun ei tarvitse huolehtia käyttöjärjestelmästä, ajonaikaisesta ympäristöstä tai infrastruktuurista.

```
Sinä hallinnoit:          Azure tarjoaa:
┌─────────────────┐      ┌─────────────────┐
│ Sovellus        │      │ Runtime (.NET)  │
│ Data            │      │ Käyttöjärjest.  │
│                 │      │ Verkko/skaalaus  │
└─────────────────┘      │ Fyysinen infra  │
                         └─────────────────┘
```

**Esimerkkejä:**
- **Azure App Service** — Web-sovellusten isännöinti
- **Azure SQL Database** — Hallittu tietokanta
- **Azure Functions** — Serverless-funktiot

**Sopii kun:** Haluat keskittyä koodiin, et infrastruktuuriin. Yleisin malli sovelluskehittäjille.

### SaaS — Software as a Service

**SaaS** tarjoaa valmiin ohjelmiston, jota käytetään selaimen tai sovelluksen kautta. Tarjoaja huolehtii kaikesta.

```
Sinä käytät:              Azure/tarjoaja tarjoaa:
┌─────────────────┐      ┌─────────────────┐
│ Selain / app    │      │ Koko sovellus   │
│ Omat tiedot     │      │ Infra, runtime  │
│ Käyttäjätilit   │      │ Päivitykset     │
└─────────────────┘      │ Ylläpito        │
                         └─────────────────┘
```

**Esimerkkejä:**
- Microsoft 365 (Word, Excel, Teams)
- GitHub
- Slack, Salesforce

**Sopii kun:** Tarvitset valmiin ohjelmiston, et halua kehittää itse.

### Vertailutaulukko

| Ominaisuus | IaaS | PaaS | SaaS |
|-----------|------|------|------|
| **Joustavuus** | Korkein | Keskiverto | Vähäisin |
| **Hallinta** | Eniten sinulla | Jaettu | Eniten tarjoajalla |
| **Ylläpito** | Sinä (OS, runtime) | Tarjoaja (OS, runtime) | Tarjoaja (kaikki) |
| **Käyttöönotto** | Hidas (asennus) | Nopea (deploy) | Välitön (kirjaudu) |
| **Esimerkki** | Azure VM | Azure App Service | Microsoft 365 |
| **Kohderyhmä** | IT-ylläpitäjät | Kehittäjät | Loppukäyttäjät |

---

## Käyttöönottomallit

### Public Cloud (Julkinen pilvi)

Resurssit ovat pilvipalveluntarjoajan datakeskuksissa, jaettuna kaikkien asiakkaiden kesken. Yleisin malli.

- ✅ Ei alkuinvestointeja
- ✅ Nopea käyttöönotto
- ✅ Skaalautuu rajattomasti
- ❌ Vähemmän hallintaa fyysisestä infrastruktuurista

**Esimerkkejä:** Azure, AWS, Google Cloud

### Private Cloud (Yksityinen pilvi)

Resurssit ovat omassa datakeskuksessa tai dedikoidussa ympäristössä. Vain yhden organisaation käytössä.

- ✅ Täysi hallinta infrastruktuurista
- ✅ Tiukempi tietoturva ja compliance
- ❌ Kalliimpi (CapEx)
- ❌ Vaatii oman IT-henkilöstön

**Esimerkkejä:** Azure Stack, VMware-ympäristöt

### Hybrid Cloud (Hybridipilvi)

Yhdistää julkisen ja yksityisen pilven. Osa resursseista on omassa datakeskuksessa, osa julkisessa pilvessä.

- ✅ Joustavuus — voit valita missä mikäkin pyörii
- ✅ Compliance — arkaluonteiset tiedot omassa datakeskuksessa
- ✅ "Burst to cloud" — lisäkapasiteettia pilvesta ruuhkahuippuihin
- ❌ Monimutkaisempi hallinta

### Vertailu

| Malli | Hallinta | Kustannukset | Joustavuus | Tietoturva |
|-------|---------|-------------|------------|-----------|
| **Public** | Vähäisin | OpEx, edullinen | Korkein | Tarjoajan vastuulla |
| **Private** | Korkein | CapEx, kallis | Rajoitettu | Oma hallinta |
| **Hybrid** | Jaettu | Yhdistelmä | Korkea | Voit valita |

---

## Pilvipalvelun hyödyt

### High Availability (Korkea saatavuus)

Palvelut ovat käytettävissä lähes 100% ajasta. Azure tarjoaa SLA-takuun (Service Level Agreement), esim. 99.95% App Servicelle.

```
99.9%  = ~8.7h downtime/vuosi
99.95% = ~4.4h downtime/vuosi
99.99% = ~52 min downtime/vuosi
```

### Scalability (Skaalautuvuus)

Resursseja voidaan lisätä kysynnän kasvaessa ja vähentää kysynnän laskiessa. Katso [Skaalautuvuus](#skaalautuvuus).

### Reliability (Luotettavuus)

Pilvipalvelut on hajautettu useisiin datakeskuksiin (regions). Jos yksi datakeskus kaatuu, toinen ottaa liikenteen vastaan.

### Predictability (Ennustettavuus)

- **Suorituskyvyn ennustettavuus** — autoscaling, kuormantasaus
- **Kustannusten ennustettavuus** — seuranta, budjetit, hälytykset

### Security (Tietoturva)

Pilvipalveluntarjoaja investoi tietoturvaan enemmän kuin yksittäinen yritys. Azure tarjoaa DDoS-suojauksen, palomuurit, salauksen, identiteetinhallinnan.

### Governance (Hallinta)

Standardoidut mallit (templates, policies) varmistavat, että resurssit noudattavat organisaation sääntöjä. Azure Policy ja Blueprints automatisoivat tämän.

### Manageability (Hallittavuus)

Resursseja hallitaan useilla tavoilla:

- **Azure Portal** — graafinen käyttöliittymä
- **Azure CLI** — komentoriviltä
- **Azure PowerShell** — skriptaus
- **ARM/Bicep-templatet** — Infrastructure as Code
- **REST API** — ohjelmalliset operaatiot

---

## Skaalautuvuus

### Vertical Scaling (Scale Up / Scale Down)

Lisätään resursseja **samaan koneeseen**: enemmän CPU:ta, muistia, levytilaa.

```
Scale Up:
┌──────────┐        ┌──────────────┐
│ 1 CPU    │   →    │ 4 CPU        │
│ 2 GB RAM │   →    │ 16 GB RAM    │
│ Palvelin │        │ Sama palvelin│
└──────────┘        └──────────────┘
```

- ✅ Yksinkertaista — ei arkkitehtuurimuutoksia
- ❌ Fyysinen yläraja (ei voi skaalata rajattomasti)
- **Esimerkki:** App Service Plan B1 → S3

### Horizontal Scaling (Scale Out / Scale In)

Lisätään **enemmän koneita** jakamaan kuormaa.

```
Scale Out:
┌──────────┐        ┌──────────┐ ┌──────────┐ ┌──────────┐
│ 1 instans│   →    │ Instans 1│ │ Instans 2│ │ Instans 3│
│          │        │          │ │          │ │          │
└──────────┘        └──────────┘ └──────────┘ └──────────┘
                          ↑           ↑           ↑
                    ┌─────────────────────────────────┐
                    │       Load Balancer              │
                    └─────────────────────────────────┘
```

- ✅ Rajaton skaalautuvuus (lisää koneita tarpeen mukaan)
- ✅ Vikasietoisuus (yksi kaatuu → muut jatkavat)
- ❌ Sovelluksen pitää olla stateless
- **Esimerkki:** App Service autoscale 1 → 10 instanssia

### Vertailu

| Ominaisuus | Vertical (Scale Up) | Horizontal (Scale Out) |
|-----------|--------------------|-----------------------|
| Miten | Suurempi kone | Lisää koneita |
| Yläraja | Fyysinen raja | Käytännössä rajaton |
| Downtime | Usein tarvitsee uudelleenkäynnistyksen | Ei downtime |
| Monimutkaisuus | Yksinkertainen | Vaatii stateless-suunnittelun |
| Kustannukset | Eksponentiaalinen (isompi = kalliimpi) | Lineaarinen (lisää = lisää) |

---

## CapEx vs. OpEx

### CapEx — Capital Expenditure (pääomakustannukset)

Suuria etukäteisinvestointeja fyysiseen infrastruktuuriin.

- Ostat palvelimet, lisenssit, verkkoyhteydet
- Kustannus syntyy **hankintahetkellä**
- Arvo laskee ajan myötä (poistot)
- **Esimerkki:** 50 000€ palvelinhuone

### OpEx — Operational Expenditure (käyttökustannukset)

Juoksevia kustannuksia palveluiden käytöstä.

- Maksat kuukausittain käytön mukaan
- Kustannus syntyy **kulutuksen mukaan**
- Ei sitoutunutta pääomaa
- **Esimerkki:** 200€/kk Azure-tilaus

### Pilvipalvelu = OpEx

```
Perinteinen (CapEx):
Kuukausi 1: ████████████████████ 50 000€ (investointi)
Kuukausi 2: ██ 500€ (sähkö, ylläpito)
Kuukausi 3: ██ 500€
...

Pilvipalvelu (OpEx):
Kuukausi 1: ███ 200€ (käyttö)
Kuukausi 2: █████ 350€ (enemmän käyttöä)
Kuukausi 3: ██ 150€ (vähemmän käyttöä)
...
```

**Consumption-based model:** Pilvipalveluissa maksat vain siitä mitä käytät (pay-as-you-go). Ei käyttöä = ei kustannuksia.

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Cloud Computing** | IT-resurssien tarjoaminen internetin kautta |
| **Shared Responsibility** | Vastuu jaetaan tarjoajan ja asiakkaan kesken |
| **IaaS** | Infrastruktuuri palveluna — VM, verkot, tallennus (esim. Azure VM) |
| **PaaS** | Alusta palveluna — kehitysalusta ilman infrahallintaa (esim. App Service) |
| **SaaS** | Ohjelmisto palveluna — valmis sovellus (esim. Microsoft 365) |
| **Public Cloud** | Jaetut resurssit tarjoajan datakeskuksissa |
| **Private Cloud** | Dedikoitu ympäristö yhdelle organisaatiolle |
| **Hybrid Cloud** | Yhdistelmä julkista ja yksityistä pilveä |
| **High Availability** | Palvelut käytettävissä lähes aina (SLA) |
| **Scalability** | Resursseja voidaan lisätä/vähentää kysynnän mukaan |
| **Vertical Scaling** | Suurempi kone (Scale Up) |
| **Horizontal Scaling** | Lisää koneita (Scale Out) |
| **CapEx** | Pääomakustannukset — suuri etukäteisinvestointi |
| **OpEx** | Käyttökustannukset — maksat kulutuksen mukaan |
| **Consumption-based** | Pay-as-you-go — ei käyttöä, ei kustannuksia |

**Muista:**
- Pilvipalvelut siirtävät vastuuta tarjoajalle — mitä korkeampi abstraktio (IaaS → PaaS → SaaS), sitä vähemmän sinun tarvitsee hallita
- **PaaS** (kuten Azure App Service) on yleisin malli sovelluskehittäjille
- Pilvipalvelut ovat **OpEx-mallisia** — maksat käytöstä, et laitteista
- **Horizontal scaling** on pilvipalveluiden vahvuus — skaalaa rajattomasti

---

## Hyödyllisiä linkkejä

- [Microsoft Learn: Describe Cloud Concepts (AZ-900)](https://learn.microsoft.com/en-us/training/paths/microsoft-azure-fundamentals-describe-cloud-concepts/)
- [Microsoft Learn: Describe Azure Architecture and Services](https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-azure-architecture-services/)
- [Microsoft: Shared Responsibility Model](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility)
- [Azure-palvelut (wiki)](Azure/README.md)
