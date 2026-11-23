# Ohjelmistoarkkitehtuuri - Johdanto

## Sisällysluettelo

1. [Mikä on ohjelmistoarkkitehtuuri?](#mikä-on-ohjelmistoarkkitehtuuri)
2. [Historia](#historia)
3. [Miksi arkkitehtuuria tarvitaan?](#miksi-arkkitehtuuria-tarvitaan)
4. [Arkkitehtuurin evoluutio](#arkkitehtuurin-evoluutio)
5. [Yleiset käsitteet](#yleiset-käsitteet)
6. [Arkkitehdin rooli](#arkkitehdin-rooli)
7. [Yhteenveto](#yhteenveto)

---

## Mikä on ohjelmistoarkkitehtuuri?

**Ohjelmistoarkkitehtuuri** on sovelluksen **rakenteen** ja **organisoinnin** määrittely. Se on kuin rakennuksen pohjapiirustus - se kertoo miten osat liittyvät toisiinsa ja miten kokonaisuus toimii.

### Määritelmä

> "Ohjelmistoarkkitehtuuri on sovelluksen rakenne, joka koostuu ohjelmistokomponenteista, niiden välisistä suhteista ja periaatteista, jotka ohjaavat niiden suunnittelua ja kehitystä."
> 
> — IEEE 1471-2000

Käytännössä hyödyllisempi määritelmä on tämä: **arkkitehtuuri on niiden päätösten joukko, joita on kallista muuttaa myöhemmin.**

| Päätös | Onko arkkitehtuuria? | Miksi |
|---|---|---|
| Muuttujan nimi | Ei | Sen voi vaihtaa minuutissa |
| Missä kerroksessa liiketoimintasäännöt ovat | Kyllä | Muutos koskee kymmeniä tiedostoja |
| Mihin suuntaan riippuvuudet osoittavat | Kyllä | Muutos koskee koko projektirakennetta |
| Käytetäänkö yhtä sovellusta vai monta palvelua | Kyllä | Muutos koskee myös julkaisua ja tiimien työtä |

Arkkitehtuurin tehtävä on tehdä nämä kalliit päätökset harkiten ja pitää muut päätökset halpoina muuttaa.

### Toimiva koodi ja hyvä koodi

**Toimiva koodi** tekee oikean asian tänään. **Hyvä koodi** tekee oikean asian tänään, ja lisäksi sitä voi huomenna muuttaa, testata ja ymmärtää.

Ero ei näy, kun ohjelmaa ajetaan. Molemmat palauttavat saman tuloksen. Ero näkyy vasta, kun jotain pitää muuttaa:

| Kysymys | Vain toimiva koodi | Hyvä koodi |
|---|---|---|
| Voiko sitä muuttaa? | Yksi muutos rikkoo jotain muualta | Muutos osuu yhteen paikkaan |
| Voiko sitä testata? | Vain käynnistämällä koko sovellus | Sääntö testataan erikseen ilman tietokantaa |
| Voiko sen ymmärtää? | Vain kirjoittaja tietää, missä mikin on | Rakenne kertoo, mistä asia löytyy |

Arkkitehtuuri on keino päästä toimivasta koodista hyvään koodiin. Pienessä kertakäyttöisessä ohjelmassa toimiva koodi riittää.

### Mitä arkkitehtuuri sisältää?

**1. Rakenne (Structure)**
- Miten sovellus on jaettu osiin?
- Mitkä ovat pääkomponentit?
- Miten komponentit on organisoitu?

**2. Suhteet (Relationships)**
- Miten komponentit kommunikoivat keskenään?
- Mitkä komponentit riippuvat toisistaan?
- Mikä on tiedonkulku?

**3. Periaatteet (Principles)**
- Mitkä säännöt ohjaavat kehitystä?
- Miten tehdään päätöksiä?
- Mitä rajoituksia on?

### Esimerkki

Ajattele verkkokauppaa:

```
┌─────────────────────────────────────┐
│         Verkkokauppa                │
├─────────────────────────────────────┤
│  UI Layer                           │  ← Käyttöliittymä
│  ┌──────────┐  ┌──────────┐        │
│  │ Tuotteet │  │ Ostoskori│        │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│  Business Logic Layer               │  ← Liiketoimintalogiikka
│  ┌──────────┐  ┌──────────┐        │
│  │ Hinnoittelu│ │Varasto   │       │
│  └──────────┘  └──────────┘        │
├─────────────────────────────────────┤
│  Data Layer                         │  ← Tietokanta
│  ┌──────────────────────┐           │
│  │     SQL Database     │           │
│  └──────────────────────┘           │
└─────────────────────────────────────┘
```

Tämä on yksinkertainen **kerrosarkkitehtuuri**.

---

## Historia

Ohjelmistoarkkitehtuurin historia kulkee käsi kädessä ohjelmistokehityksen historian kanssa.

### 1950-1960: Alkuaika - Ei arkkitehtuuria

**Ongelma:** Ohjelmat olivat pieniä ja yksinkertaisia.

- Kaikki koodi yhdessä tiedostossa
- Ei modulaarisuutta
- Ei suunnittelua

```
┌───────────────┐
│  Kaikki koodi │
│  yhdessä      │
│  massassa     │
└───────────────┘
```

**Esimerkki:** 1000-rivinen FORTRAN-ohjelma ilman funktioita.

### 1970: Rakenteellinen ohjelmointi

**Innovaatio:** Dijkstra esitteli **strukturoidun ohjelmoinnin** (Structured Programming).

**Idea:**
- Jaa ohjelma funktioihin
- Käytä selkeitä rakenteita (if, while, for)
- Vältä GOTO-lauseita

```
┌─────────────────────┐
│  Main Program       │
│  ├─ Function A      │
│  ├─ Function B      │
│  └─ Function C      │
└─────────────────────┘
```

### 1980: Kerrosarkkitehtuuri

**Innovaatio:** **Layered Architecture** (N-tier Architecture)

**Idea:**
- Jaa sovellus kerroksiin
- Jokainen kerros vastaa yhdestä asiasta
- Ylemmät kerrokset käyttävät alempia kerroksia

```
┌─────────────┐
│  UI Layer   │
├─────────────┤
│ Logic Layer │
├─────────────┤
│ Data Layer  │
└─────────────┘
```

**Esimerkkejä:**
- Verkkoprotokollien kerrosmallit: OSI-malli (7 kerrosta) ja TCP/IP-malli (4 kerrosta)
- Tietokantasovellukset (Presentation, Business, Data)

### 1990: Olio-ohjelmointi ja Design Patterns

**Innovaatio:** Gang of Four julkaisi **Design Patterns** -kirjan (1994).

**Idea:**
- Tunnista yleisiä ongelmia
- Luo uudelleenkäytettäviä ratkaisuja
- Nimeä mallit (Singleton, Factory, Observer, jne.)

**Vaikutus:**
- Yhteinen kieli kehittäjien välillä
- Todistetusti toimivat ratkaisut
- Koodin laatu parani

### 2000: Service-Oriented Architecture (SOA)

**Innovaatio:** **SOA** (Palvelukeskeinen arkkitehtuuri)

**Idea:**
- Jaa sovellus palveluihin
- Palvelut kommunikoivat verkon yli
- Löyhä kytkös

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│Service A│◄──►│Service B│◄──►│Service C│
└─────────┘    └─────────┘    └─────────┘
```

**Esimerkkejä:**
- Web Services (SOAP, REST)
- Enterprise Service Bus (ESB)

### 2010: Domain-Driven Design ja Clean Architecture

**Innovaatio:** Robert C. Martin esitteli **Clean Architecture** (2012).

**Idea:**
- Domain (liiketoimintalogiikka) on keskiössä
- Riippuvuudet osoittavat sisäänpäin
- Teknologia on vaihdettavissa

```
┌────────────────────────┐
│    Infrastructure      │
│  ┌──────────────────┐  │
│  │  Use Cases       │  │
│  │  ┌────────────┐  │  │
│  │  │  Domain    │  │  │
│  │  └────────────┘  │  │
│  └──────────────────┘  │
└────────────────────────┘
```

**Muut mallit:**
- Hexagonal Architecture (Alistair Cockburn, 2005)
- Onion Architecture (Jeffrey Palermo, 2008)

### 2010-luku: Mikropalvelut

**Innovaatio:** **Microservices Architecture**

**Idea:**
- Jaa sovellus pieniin, itsenäisiin palveluihin
- Jokainen palvelu on oma prosessi
- Kommunikaatio HTTP:n tai viestien kautta

```
┌────────┐  ┌────────┐  ┌────────┐
│Service │  │Service │  │Service │
│   A    │  │   B    │  │   C    │
│  DB    │  │  DB    │  │  DB    │
└────────┘  └────────┘  └────────┘
```

**Esimerkkejä:**
- Netflix
- Amazon
- Uber

### 2020-luku: Cloud-Native ja Serverless

**Innovaatio:** **Cloud-Native Architecture** ja **Serverless**

**Idea:**
- Rakennettu pilvelle (AWS, Azure, GCP)
- Automaattinen skaalautuvuus
- Serverless Functions (AWS Lambda, Azure Functions)

```
┌──────────────────────────┐
│   API Gateway            │
├──────────────────────────┤
│ ┌────┐ ┌────┐ ┌────┐    │
│ │Func│ │Func│ │Func│    │
│ │ A  │ │ B  │ │ C  │    │
│ └────┘ └────┘ └────┘    │
└──────────────────────────┘
```

---

## Miksi arkkitehtuuria tarvitaan?

### 1. Hallittavuus

**Ongelma ilman arkkitehtuuria:**

Kuvittele 100,000 riviä koodia yhdessä tiedostossa ilman jakoa:

```csharp
// Program.cs (100,000 riviä)
class Program
{
    static void Main()
    {
        // UI koodi
        Console.WriteLine("Tervetuloa!");
        
        // Liiketoimintalogiikka
        if (user.Age > 18) { ... }
        
        // Tietokantakoodi
        SqlConnection conn = new SqlConnection(...);
        
        // Email-lähetys
        SmtpClient smtp = new SmtpClient(...);
        
        // ... 99,900 riviä lisää ...
    }
}
```

**Ongelmat:**
- ❌ Vaikea löytää mitään
- ❌ Vaikea ymmärtää kokonaisuutta
- ❌ Muutokset rikkovat kaiken
- ❌ Testaaminen mahdotonta

**Ratkaisu arkkitehtuurilla:**

```
MyApp/
├── UI/               ← Käyttöliittymä
├── Business/         ← Liiketoimintalogiikka
├── Data/             ← Tietokanta
└── Infrastructure/   ← Email, logging, jne.
```

**Hyödyt:**
- ✅ Helppo löytää oikea paikka
- ✅ Selkeä kokonaisuus
- ✅ Muutokset eristetty
- ✅ Testattavissa osissa

### 2. Ylläpidettävyys

**Tilastot:**
- 70-80% ohjelmiston kustannuksista tulee ylläpidosta
- Uuden kehittäjän perehdyttäminen vie 3-6 kuukautta

**Hyvä arkkitehtuuri:**
- ✅ Uusi kehittäjä ymmärtää rakenteen nopeasti
- ✅ Bugien korjaaminen on helpompaa
- ✅ Uusien ominaisuuksien lisääminen on turvallista

**Esimerkki:**

```csharp
// ❌ Huono: Kaikki sekaisin
public void ProcessOrder(Order order)
{
    // Validointi
    if (order.Total < 0) throw new Exception();
    
    // Tietokantatallennus
    SqlConnection conn = new SqlConnection("...");
    conn.Open();
    
    // Email-lähetys
    SmtpClient smtp = new SmtpClient();
    smtp.Send(...);
    
    // Logging
    File.AppendAllText("log.txt", "Order processed");
}

// ✅ Hyvä: Selkeä jako
public void ProcessOrder(Order order)
{
    _validator.Validate(order);
    _orderRepository.Save(order);
    _emailService.SendConfirmation(order);
    _logger.Log("Order processed");
}
```

### 3. Skaalautuvuus

**Tekninen skaalautuvuus:**

```
// Ilman arkkitehtuuria: Koko sovellus yhdessä
┌─────────────────────┐
│  Koko sovellus      │ ← Jos kuormitus kasvaa,
│  (1 server)         │   pitää ostaa isompi server
└─────────────────────┘

// Arkkitehtuurilla: Komponentit erikseen
┌────────┐  ┌────────┐  ┌────────┐
│  UI    │  │Business│  │Database│
│(3 srv) │  │(2 srv) │  │(1 srv) │
└────────┘  └────────┘  └────────┘
         ↑ Vain UI:ta skaalataan
```

**Huomaa:** kuvassa osat on ajettu eri palvelimille. Silloin puhutaan **tasoista** (tier), ei kerroksista (layer). Koodin jako kerroksiin ei vielä tarkoita, että osat ajetaan eri palvelimilla. Selkeä kerrosjako kuitenkin helpottaa osien erottamista omille palvelimilleen myöhemmin. Ero selitetään kohdassa [Kerros ja taso](#3-kerros-layer--tier).

**Tiimin skaalautuvuus:**

```
// Ilman arkkitehtuuria
Kaikki 20 kehittäjää muokkaavat samaa tiedostoa → Konfliktit

// Arkkitehtuurilla
┌───────┐  ┌───────┐  ┌───────┐
│ Tim 1 │  │ Tiimi2│  │ Tiimi3│
│  UI   │  │Logic  │  │ Data  │
└───────┘  └───────┘  └───────┘
      ↑ Itsenäistä työskentelyä
```

### 4. Testattavuus

**Ilman arkkitehtuuria:**

```csharp
// Vaikea testata - riippuu tietokannasta
public void CreateUser(string name)
{
    SqlConnection conn = new SqlConnection("...");
    // Testaaminen vaatii oikean tietokannan!
}
```

**Arkkitehtuurilla:**

```csharp
// Helppo testata - mock riippuvuudet
public class UserService
{
    private IUserRepository _repository;
    
    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }
    
    public void CreateUser(string name)
    {
        // Testeissä: mock repository
    }
}

// Testi
[Fact]
public void CreateUser_ValidName_Succeeds()
{
    Mock<IUserRepository> mock = new Mock<IUserRepository>();
    UserService service = new UserService(mock.Object);
    // Ei tarvita tietokantaa!
}
```

### 5. Teknologian vaihdettavuus

**Esimerkki: Tietokannan vaihto**

```
// Ilman arkkitehtuuria
Kaikki koodi käyttää suoraan SQL Server:ia
→ Vaihto PostgreSQL:ään: Muuta 10,000 riviä koodia

// Arkkitehtuurilla
Business Logic → IRepository (interface)
                       ↓
                 SqlRepository (implementation)

→ Vaihto PostgreSQL:ään:
  Luo PostgresRepository, vaihda 1 rivi (DI-rekisteröinti)
```

### 6. Selkeä rakenne auttaa myös tekoälyagenttia

**Tekoälyagentti** on työkalu, joka lukee projektin tiedostoja ja kirjoittaa koodia pyynnön perusteella. Agentti ei tunne projektin historiaa. Se päättelee asiayhteyden siitä, mitä se näkee: kansioista, nimistä ja rajapinnoista.

| Agentti näkee | Mitä se siitä päättelee |
|---|---|
| Kansiot `Domain/`, `Application/`, `Infrastructure/` | Mihin kerrokseen uusi luokka kuuluu |
| Rajapinnan `IMatchRepository` | Mitä tallennukselta saa pyytää |
| Nimen `RecordResultUseCase` | Mistä muut käyttötapaukset löytyvät ja miltä ne näyttävät |

Jos kaikki koodi on yhdessä tiedostossa tai kerrokset ovat sekaisin, agentilla ei ole näitä vihjeitä. Silloin se laittaa uuden koodin sinne, mihin se sattuu sopimaan. Usein sääntö päätyy controlleriin tai tietokantakoodiin.

Selkeä rakenne kertoo siis sekä ihmiselle että agentille, mihin uusi koodi kuuluu. Rakenne ei korvaa tarkistamista: ihminen lukee agentin tekemät muutokset ja päättää, hyväksytäänkö ne. Katso [Haarat ja pull request](../../99-General/Git-Haarat-ja-Pull-Request.md).

---

## Arkkitehtuurin evoluutio

### Vaihe 1: Monolittiset sovellukset (1950-2000)

Kaikki koodi yhdessä:

```
┌──────────────────────┐
│                      │
│   Koko sovellus      │
│   yhdessä            │
│                      │
└──────────────────────┘
```

**Edut:**
- ✅ Yksinkertainen kehittää
- ✅ Helppo deployata

**Haitat:**
- ❌ Vaikea skaalata
- ❌ Vaikea ylläpitää
- ❌ Muutokset riskialttiita

### Vaihe 2: Kerrosarkkitehtuuri (1980-2010)

Jako kerroksiin:

```
┌──────────────┐
│  UI          │
├──────────────┤
│  Business    │
├──────────────┤
│  Data        │
└──────────────┘
```

**Edut:**
- ✅ Selkeämpi jako
- ✅ Helpompi ylläpitää

**Haitat:**
- ❌ Edelleen yhdessä deployattava
- ❌ Riippuvuudet alaspäin

### Vaihe 3: Domain-Driven Design (2000-luku)

Domain keskiössä:

```
┌────────────────┐
│ Infrastructure │
│  ┌──────────┐  │
│  │ Domain   │  │
│  └──────────┘  │
└────────────────┘
```

**Edut:**
- ✅ Liiketoimintalogiikka eristetty
- ✅ Testattava
- ✅ Teknologiariippumaton

### Vaihe 4: Mikropalvelut (2010-luku)

Pienet, itsenäiset palvelut:

```
┌────┐ ┌────┐ ┌────┐
│ A  │ │ B  │ │ C  │
└────┘ └────┘ └────┘
```

**Edut:**
- ✅ Itsenäisesti skaalautuva
- ✅ Teknologiavalinnat per palvelu
- ✅ Itsenäinen deployaus

**Haitat:**
- ❌ Monimutkainen infrastruktuuri
- ❌ Hajautetun järjestelmän ongelmat

### Vaihe 5: Serverless (2020-luku)

Funktioita ilman palvelimia:

```
┌────────────────────┐
│  Function 1        │
│  Function 2        │
│  Function 3        │
└────────────────────┘
     ↑ Cloud provider hallinnoi
```

**Edut:**
- ✅ Automaattinen skaalautuvuus
- ✅ Maksat vain käytöstä
- ✅ Ei infrastruktuurin ylläpitoa

---

## Yleiset käsitteet

### 1. Komponentti (Component)

Sovelluksen itsenäinen osa, jolla on selkeä vastuu.

```csharp
public class UserService  // Komponentti
{
    public void CreateUser() { }
    public void DeleteUser() { }
}
```

### 2. Moduuli (Module)

Kokoelma toisiinsa liittyviä komponentteja.

```
UserManagement/        ← Moduuli
├── UserService.cs
├── UserRepository.cs
└── User.cs
```

### 3. Kerros (Layer / Tier)

**Kerros (layer)** on koodin looginen jako vastuualueittain. Kerrokset voivat olla kansioita tai projekteja samassa sovelluksessa.

```
UI Layer        ← Kerros 1
Business Layer  ← Kerros 2
Data Layer      ← Kerros 3
```

**Taso (tier)** on fyysinen yksikkö, joka ajetaan omana prosessinaan tai omalla palvelimellaan. Esimerkiksi selain, API-palvelin ja tietokantapalvelin ovat kolme tasoa.

| | Kerros (layer) | Taso (tier) |
|---|---|---|
| Mitä jaetaan | Koodi | Ajoympäristö |
| Missä näkyy | Kansiot, projektit, riippuvuudet | Palvelimet, prosessit, verkko |
| Esimerkki | Controller, service, repository | Selain, API-palvelin, tietokanta |

Sanat menevät usein sekaisin, koska niitä käytetään arkikielessä samasta asiasta. Ne ovat silti eri asioita: kolmen kerroksen sovellus voi pyöriä yhdellä palvelimella, eli yhdellä tasolla.

### 4. Rajapinta (Interface)

Sopimus siitä, mitä komponentti tarjoaa.

```csharp
public interface IUserRepository  // Rajapinta
{
    User GetById(int id);
    void Save(User user);
}

public class SqlUserRepository : IUserRepository  // Toteutus
{
    // Konkreettinen toteutus
}
```

### 5. Riippuvuus (Dependency)

Komponentti A tarvitsee komponenttia B.

```csharp
public class UserService
{
    private IUserRepository _repository;  // Riippuvuus
    
    public UserService(IUserRepository repository)
    {
        _repository = repository;
    }
}
```

### 6. Kytkös (Coupling)

Kuinka vahvasti komponentit riippuvat toisistaan.

```csharp
// ❌ Vahva kytkös (tight coupling)
public class UserService
{
    private SqlUserRepository _repo = new SqlUserRepository();
}

// ✅ Löyhä kytkös (loose coupling)
public class UserService
{
    private IUserRepository _repo;
    
    public UserService(IUserRepository repo)
    {
        _repo = repo;
    }
}
```

### 7. Koheesio (Cohesion)

Kuinka hyvin komponentin osat kuuluvat yhteen.

```csharp
// ✅ Korkea koheesio - kaikki liittyy käyttäjiin
public class UserService
{
    public void CreateUser() { }
    public void DeleteUser() { }
    public void UpdateUser() { }
}

// ❌ Matala koheesio - ei liity toisiinsa
public class MixedService
{
    public void CreateUser() { }
    public void SendEmail() { }
    public void CalculateTax() { }
}
```

---

## Arkkitehdin rooli

### Mitä arkkitehti tekee?

**1. Suunnittelee rakenteen**
- Päättää arkkitehtuurimallin (Layered, Clean, Microservices)
- Jakaa sovelluksen komponentteihin
- Määrittelee komponenttien väliset suhteet

**2. Tekee teknologiavalintoja**
- Ohjelmointikieli (C#, Java, Python)
- Framework (ASP.NET Core, Spring Boot)
- Tietokanta (SQL Server, PostgreSQL, MongoDB)
- Infrastruktuuri (Azure, AWS, on-premise)

**3. Määrittelee standardit ja periaatteet**
- Koodausstandardit
- Nimeämiskäytännöt
- Testausstrategiat
- Dokumentointikäytännöt

**4. Ohjaa tiimiä**
- Code review
- Tekninen mentorointi
- Arkkitehtuuripäätösten perusteleminen

**5. Hallitsee teknistä velkaa**
- Tunnistaa arkkitehtuuriongelmat
- Priorisoi refaktoroinnit
- Tasapainottaa lyhyen ja pitkän aikavälin tarpeet

### Esimerkkipäätös

**Tilanne:** Rakennetaan verkkokauppaa

**Arkkitehdin päätökset:**

1. **Arkkitehtuurimalli:** Clean Architecture
   - **Miksi:** Sovellus on monimutkainen, vaatii testattavuutta

2. **Teknologiat:**
   - Backend: ASP.NET Core Web API
   - Frontend: React
   - Tietokanta: PostgreSQL
   - Cache: Redis

3. **Projektijako:**
   ```
   Domain/           ← Liiketoimintalogiikka
   Application/      ← Use cases
   Infrastructure/   ← Tietokanta, email
   Web/             ← API controllers
   ```

4. **Periaatteet:**
   - SOLID-periaatteet
   - Dependency Injection kaikkialla
   - Repository pattern tietokannalle
   - DTO:t API:ssa

---

## Yhteenveto

### Tärkeimmät oivallukset

**1. Arkkitehtuuri on suunnittelua**
- Ei tapahdu itsestään
- Vaatii ajattelua ja päätöksiä
- Parempi suunnitella kuin korjata myöhemmin

**2. Arkkitehtuuri kehittyy ajan myötä**
- 1950: Ei arkkitehtuuria
- 1980: Kerrosarkkitehtuuri
- 2000: Domain-Driven Design
- 2010: Mikropalvelut
- 2020: Cloud-Native

**3. Arkkitehtuuri on väline, ei päämäärä**
- Valitse projektin mukaan
- Älä ylisuunnittele
- Refaktoroi kun tarve tulee

**4. Hyvä arkkitehtuuri:**
- ✅ On helppo ymmärtää
- ✅ On helppo ylläpitää
- ✅ On helppo testata
- ✅ On helppo laajentaa
- ✅ Skaalautuu (teknisesti ja tiimin koon mukaan)

### Aloita tästä

Jos olet uusi arkkitehtuurien parissa:

1. **Aloita yksinkertaisesta**
   - [Layered Architecture](Layered-Architecture.md)

2. **Opettele periaatteet**
   - SOLID-periaatteet
   - Dependency Inversion

3. **Etene monimutkaisempiin**
   - [Clean Architecture](Clean-Architecture.md)
   - [Hexagonal Architecture](Hexagonal-Architecture.md)

4. **Käytä oikein**
   - Valitse projektin mukaan
   - Älä ylisuunnittele
   - Opi kokemuksesta

---

## Hyödyllisiä linkkejä

### Kirjat
- **Clean Architecture** by Robert C. Martin (2017)
- **Domain-Driven Design** by Eric Evans (2003)
- **Building Microservices** by Sam Newman (2015)
- **Patterns of Enterprise Application Architecture** by Martin Fowler (2002)

### Verkkomateriaali
- [Martin Fowler's Software Architecture Guide](https://martinfowler.com/architecture/)
- [Microsoft: .NET Architecture Guides](https://learn.microsoft.com/en-us/dotnet/architecture/)
- [The Twelve-Factor App](https://12factor.net/)

### Videot
- [GOTO Conferences - Software Architecture](https://www.youtube.com/c/GotoConferences)
- [Martin Fowler - Software Architecture](https://www.youtube.com/results?search_query=martin+fowler+architecture)

---

## Seuraavaksi

Kun ymmärrät arkkitehtuurin perusteet, tutustu eri malleihin:

- **[README](README.md)** - Yleiskatsaus arkkitehtuurimalleihin
- **[Layered Architecture](Layered-Architecture.md)** - Aloita tästä!
- **[Clean Architecture](Clean-Architecture.md)** - Domain-keskinen malli
- **[Hexagonal Architecture](Hexagonal-Architecture.md)** - Portit ja adapterit

**Muista:** Arkkitehtuuri on matka, ei päämäärä. Opi jatkuvasti ja sovella oppimaasi!
