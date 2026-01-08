# Yksikkötestaus (Unit Testing)

## HUOM!

- Esimerkkikoodit löydät esimerkki solutionista UnitTestExamples-projektin alta, ClassLibraryTests-luokasta
- Lisää yksikkötestiesimerkkejä löytyy aina tehtävien yksikkötestiprojekteista, joiden avulla voitte tarkastaa tehtäviä
- [Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test)
- [Miten ajaa yksikkötestejä Visual Studiossa](https://learn.microsoft.com/en-us/visualstudio/test/run-unit-tests-with-test-explorer?view=vs-2022)

## Mikä on yksikkötestaus?

Yksikkötestaus on ohjelmointiprosessi, jossa pieni osa koodista (tyypillisesti yksittäinen funktio tai luokka) testataan erikseen varmistaakseen, että se toimii odotetulla tavalla.

### xUnit

**xUnit** on suosittu yksikkötestaustyökalu C#-ohjelmointikielessä. Se on kirjoitettu .NET-kielellä ja sitä käytetään .NET-sovellusten yksikkötestaukseen. xUnit on erityisen suosittu .NET Core -yhteisössä, ja se on yksi monista testauskehyksistä, kuten MSTest ja NUnit, mutta se on suunniteltu erityisesti modernilla otteella, ottaen huomioon parhaat käytännöt ja oppimukset muista testauskehyksistä.

## Yksikkötestaamisen hyödyt

1. **Varmistaa koodin toiminta**: Voit olla varma, että koodisi tekee sen, mitä sen on tarkoitus tehdä.
2. **Havaitsee virheet aikaisin**: Mahdolliset virheet löydetään ja korjataan ennen kuin ne päätyvät tuotantoon.
3. **Helpottaa muutoksia**: Jos teet muutoksia koodiin, voit ajaa yksikkötestit varmistaaksesi, ettet rikkonut mitään.
4. **Parantaa koodin laatua**: Yksikkötestaus kannustaa suunnittelemaan koodin paremmin ja tekemään se modulaarisemmaksi.

## Perusesimerkki

Oletetaan, että sinulla on seuraava yksinkertainen funktio, joka laskee kahden luvun summan:

```csharp
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
}
```

Tämä yksikkötesti varmistaa, että Add-funktion palauttama tulos on oikea:

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_ShouldReturnSum_WhenGivenTwoNumbers()
    {
        // Arrange
        Calculator calculator = new Calculator();
        int a = 5;
        int b = 3;
        int expected = 8;

        // Act
        int result = calculator.Add(a, b);

        // Assert
        Assert.Equal(expected, result);
    }
}
```

Jos joku muuttaisi Add-funktiota myöhemmin (esim. vahingossa), ja funktio ei enää palauttaisi oikeaa tulosta, tämä testi epäonnistuisi ja ilmoittaisi virheestä.

## Yksikkötestauksen syntaksi

### Arrange-Act-Assert (AAA)

AAA on yleinen malli, jota käytetään yksikkötestauksessa kuvaamaan testin kolmea päävaihetta:

1. **Arrange** (Järjestä)
   - Tässä vaiheessa luodaan testin edellyttämät objektit ja asetetaan niiden alkuarvot.
   - Testin lähtötilanne rakennetaan: luodaan tarvittavat objektit, asetetaan mock-objekteille odotetut arvot ja toiminnot jne.

2. **Act** (Toimi)
   - Testattavaa toimintoa kutsutaan tässä vaiheessa.
   - Yleensä tämä vaihe koostuu yhdestä toimintokutsusta, joka on testin keskeinen osa.

3. **Assert** (Varmista)
   - Tässä vaiheessa testin tulos tarkistetaan.
   - Käytetään yleensä `Assert`-luokan funktioita (kuten `Assert.Equal`, `Assert.True` jne.) varmistaakseen, että testattava koodi toimii odotetusti.
   - Jos jokin `Assert` epäonnistuu, testi katsotaan epäonnistuneeksi.

### [Fact]-attribuutti

`[Fact]`-attribuutti käytetään yksittäisen testin määrittelemiseen. Toisin kuin muissa kehyksissä, joissa saatetaan käyttää esim. `[Test]`-attribuuttia, xUnitissa käytetään `[Fact]`.

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_ShouldReturnSum_WhenGivenTwoNumbers()
    {
        // Arrange
        Calculator calculator = new Calculator();
        int a = 5;
        int b = 3;

        // Act
        int result = calculator.Add(a, b);

        // Assert
        Assert.Equal(8, result);
    }
}
```

### [Theory] ja [InlineData]

`Theory` on attribuutti, jota käytetään ilmoittamaan, että testausmetodi on tarkoitettu suoritettavaksi useilla eri syötedataseteillä. Toisin kuin `Fact`-attribuutti, joka osoittaa, että metodi on testi, joka suoritetaan tarkalleen yhdellä määritellyllä tavalla, `Theory`-attribuutti kertoo, että testi odottaa syötettä.

Kun merkitset testausmetodin `Theory`-attribuutilla, sinun on yhdistettävä se johonkin datalähteen attribuuttiin, joka toimittaa syötedatan.

`InlineData` on atribuutti parametrisoiduille testausmetodeille. Se mahdollistaa eri syötedatojen syöttämisen samaan testausmetodiin. Tämän avulla voit suorittaa saman testin useilla eri syötearvoilla ilman, että sinun tarvitsee kirjoittaa useita erillisiä testejä.

**HUOM!** Voit käyttää vain jompaa kumpaa attributeja, joko `Theory`:a tai `Fact`:a, koska ne sulkevat toisensa pois (toimivat eri logiikalla).

```csharp
using Xunit;

public class WordCounterTests
{
    [Theory]
    [InlineData("Hello World", 2)]
    [InlineData("", 0)]
    [InlineData("One", 1)]
    public void CountWords_ShouldReturnCorrectCount_WhenGivenString(string input, int expected)
    {
        // Arrange
        WordCounter counter = new WordCounter();

        // Act
        int result = counter.CountWords(input);

        // Assert
        Assert.Equal(expected, result);
    }
}
```

Tässä esimerkissä `WordCounterTheoryTest` -testi suoritetaan kolme kertaa eri syötedataarvoilla:
1. `input` = "Hello World", `expected` = 2
2. `input` = "", `expected` = 0
3. `input` = "One", `expected` = 1

**Syntaksi**: `[InlineData(value1, expected)]`

Jos testi-metodissa olisi useampi parametri, niin silloin InlineData attribuutin parametrien määrä pitää täsmätä. Alla olevassa esimerkissä on testi, joka ottaa kaksi parametria:

```csharp
[Theory]
[InlineData(2, 3, 5)]
[InlineData(10, 20, 30)]
[InlineData(-5, 5, 0)]
public void Add_ShouldReturnSum_WhenGivenTwoNumbers(int a, int b, int expected)
{
    // Arrange
    Calculator calculator = new Calculator();

    // Act
    int result = calculator.Add(a, b);

    // Assert
    Assert.Equal(expected, result);
}
```

## Mocking testauksessa

### Mitä on mocking?

Mocking eli "mock-olioiden" (tai testidummyjen) käyttäminen on tekniikka, jossa luodaan "teko-olioita" (mockkeja) korvaamaan sovelluksen oikeat riippuvuudet testin ajaksi. Tarkoituksena on testata **yhtä koodin osaa** kerrallaan eristettynä muista osista. Näin ulkoinen tai monimutkainen riippuvuus (kuten tietokanta, API-kutsu tai sähköpostipalvelu) korvataan mockilla, joka joko antaa ennalta määritellyt tulokset tai jonka metodeja voidaan seurata ja varmistaa, että niitä kutsutaan oikeilla parametreilla.

**Muita materiaaleja**:
- [How to use Moq for mocking objects with xUnit and .NET](https://www.roundthecode.com/dotnet-tutorials/moq-mocking-objects-xunit-dotnet)
- [Moq Mocking Framework With xUnit.net Unit Test In C#](https://www.csharp.com/article/moq-mocking-framework-with-xunit-net-testing-fr/)

### Mihin mockingia käytetään?

1. **Eristämään testattava koodi ulkoisista riippuvuuksista**
   - Voit testata metodisi logiikkaa ilman, että kutsut oikeaa tietokantaa, ulkoista palvelua tai sähköpostijärjestelmää.

2. **Hallitsemaan testin olosuhteet**
   - Mock-palvelu voi palauttaa tai tehdä juuri sen, mitä testitilanteessa halutaan tarkastella. Esim. voit testata, miten metodi reagoi, jos riippuvuus heittää poikkeuksen.

3. **Varmistamaan tiettyjen metodikutsujen toteutuminen**
   - Voit testata esimerkiksi, että `SendEmail`-metodia on varmasti kutsuttu, kun luot uuden käyttäjän.

### Milloin mockingia kannattaa käyttää?

1. **Riippuvuus on hidas tai epävakaa**
   - Testien ajaminen on nopeampaa ja luotettavampaa, kun et oikeasti kutsu ulkoisia palveluita tai käytä tietokantaa.

2. **Riippuvuus on vaikea tai raskas konfiguroida**
   - Paljon asetuksia tai iso testidata voidaan välttää käyttämällä mockia, joka antaa suoraan halutun vastauksen.

3. **Tarve testata virhetilanteita**
   - Voit pakottaa mock-olion heittämään poikkeuksia ja varmistaa, miten koodisi toimii niissä tilanteissa.

4. **Tahdot varmistaa spesifin metodikutsun**
   - Useimmissa mocking-kehyksissä voit helposti seurata, onko metodia kutsuttu, kuinka monta kertaa ja millä parametreilla.

**Huomaa**: Ettei kaikkea kannata välttämättä mockata. Jos riippuvuuden toteutus on yksinkertainen eikä aiheuta hidastuksia tai hankaluuksia, voi olla helpompaa käyttää oikeaa toteutusta myös testissä.

### Mitä ongelmia mocking ratkaisee?

1. **Hitaat testit**: Testit pysyvät nopeina, koska vältytään oikeilta verkko- tai tietokantakutsuilta.
2. **Epävakaat testit**: Kun riippuvuus on mockattu, testin tulos ei muutu ulkoisten häiriöiden takia.
3. **Monimutkaiset riippuvuudet**: Testit säilyvät selkeinä, koska monimutkainen "oikea" riippuvuus voidaan korvata yksinkertaisella mockilla.
4. **Kattavuuden lisääminen**: Voit hallita tarkasti mockin palauttamat arvot ja virhetilanteet, jolloin testaat kattavasti erilaiset skenaariot.

### Mitä mocking vaatii ja miksi rajapinnat (interface) ovat tässä hyödyllisiä?

1. **Mitä mocking vaatii?**
   - Usein mocking-työkalut (esim. Moq C#-kielessä) tarvitsevat, että testattavan luokan riippuvuus on tarjolla **rajapintana** (interface) tai vähintäänkin *virtual-metodeina*. Ilman rajapintaa tai virtual-metodeja mocking-framework ei saa luotua "teko-oliota", joka toteuttaa tai yliajaa tarvittavia metodeja.

2. **Miksi rajapinnat (interface) ovat hyvä asia?**
   - Kun käytät luokan sijaan **rajapintaa**, sen toteutus on helppo vaihtaa: joko oikeaan toteutukseen tuotantokoodissa tai mock-olioihin testikoodissa. Koko järjestelmä pysyy modulaarisempana ja testausystävällisempänä, koska luokka riippuu ainoastaan rajapinnasta (eli metodeista, ei konkreettisesta toteutuksesta). Tämä tukee parempaa arkkitehtuuria ja koodin ylläpidettävyyttä.

### Esimerkki xUnit-testeistä (C# + Moq)

Alla yksinkertainen esimerkki siitä, miten mocking tehdään C#:ssa käyttäen [Moq-kirjastoa](https://github.com/moq/moq). Testaamme luokkaa, joka luo käyttäjän ja lähettää tervetulotoivotuksen sähköpostilla.

#### 1. Rajapinta (IEmailService)

```csharp
public interface IEmailService
{
    void SendEmail(string to, string subject, string body);
}
```

#### 2. Testattava luokka (UserService)

```csharp
public class UserService
{
    private readonly IEmailService _emailService;

    public UserService(IEmailService emailService)
    {
        _emailService = emailService;
    }

    public void CreateUser(string username, string email)
    {
        // Luodaan käyttäjä...
        
        // Lähetetään tervetuloviesti
        _emailService.SendEmail(email, "Tervetuloa!", $"Hei {username}!");
    }
}
```

#### 3. Testi (xUnit + Moq)

```csharp
using Xunit;
using Moq;

public class UserServiceTests
{
    [Fact]
    public void CreateUser_ShouldSendWelcomeEmail_WhenUserIsCreated()
    {
        // Arrange
        var emailServiceMock = new Mock<IEmailService>();
        var userService = new UserService(emailServiceMock.Object);

        // Act
        userService.CreateUser("matti", "matti@example.com");

        // Assert
        emailServiceMock.Verify(
            x => x.SendEmail("matti@example.com", "Tervetuloa!", "Hei matti!"),
            Times.Once
        );
    }
}
```

**Mitä testissä tapahtuu?**

1. **Luodaan mock-olio**: `new Mock<IEmailService>()` luo dynaamisen "teko-olion", joka toteuttaa `IEmailService`:n.
2. **Injektoidaan mock**: `userService` käyttää `emailServiceMock.Object`-olioa sähköpostin lähetykseen.
3. **Kutsutaan testattavaa metodia**: `userService.CreateUser("matti", "matti@example.com")`.
4. **Tarkistetaan metodikutsu**: `Verify`-metodi varmistaa, että `SendEmail`-metodia kutsuttiin **täsmälleen kerran** annetuille parametreille.

### Yhteenveto mockingista

- **Mocking** tarkoittaa ulkoisten tai monimutkaisten riippuvuuksien "feikkaamista" testikoodissa.
- Se pitää testit **nopeina**, **luotettavina** ja **selkeinä**, keskittyen vain testattavan koodipalan logiikkaan.
- **Rajapinnat (interface)** helpottavat mockin käyttöä: mocking-framework pystyy helposti luomaan dynaamisia olioita rajapintojen pohjalta.
- Mocking säästää aikaa, vaivaa ja estää ulkoisten ja monimutkaisten elementtien sotkemasta yksikkötestejä.
- Kokonaisuudessaan mocking on keskeinen työkalu yksikkötestauksessa ja kannustaa koodin palasteluun, mikä johtaa parempaan arkkitehtuuriseen suunnitteluun ja ylläpidettävyyteen.

## Attribuutit (Attributes)

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/)

C#-kielellä attribuutit (Attributes) ovat erityisiä deklaraatioita, jotka voidaan liittää koodi-elementteihin (esim. luokkiin, menetelmiin, ominaisuuksiin) ja jotka määrittelevät lisätietoja tai ohjeita kääntäjälle. Attribuutteja käytetään usein määrittämään metatietoja koodista tai ohjaamaan tiettyjä toimintoja, kuten sarjoittamista tai yksikkötestausta.

### Esimerkki attribuutin käytöstä

```csharp
public class MyClass
{
    [Obsolete("Käytä NewMethod() sen sijaan")]
    public void OldMethod()
    {
        // Vanha toteutus
    }

    public void NewMethod()
    {
        // Uusi toteutus
    }
}

// Käyttö
MyClass obj = new MyClass();
obj.OldMethod();  // Varoitus: metodi on vanhentunut
```

Tässä `Obsolete` on attribuutti, joka merkitsee `OldMethod`-metodin vanhentuneeksi. Kun kehittäjä yrittää kutsua tätä metodia, hän saa varoituksen siitä, että metodi on vanhentunut ja että hänen pitäisi käyttää jotain muuta metodia sen sijaan.

### Yksikkötestauksessa käytetyt attribuutit

```csharp
using Xunit;

public class MyTests
{
    [Fact]  // Yksittäinen testi
    public void Test1()
    {
        // Testin toteutus
    }

    [Theory]  // Parametrisoitu testi
    [InlineData(1, 2, 3)]
    [InlineData(5, 5, 10)]
    public void Test2(int a, int b, int expected)
    {
        Assert.Equal(expected, a + b);
    }
}
```

## Yhteenveto

Yksikkötestaus on keskeinen osa laadukkaan ohjelmiston kehitystä. Se auttaa varmistamaan, että koodi toimii oikein, havaitsee virheet aikaisin ja helpottaa koodin ylläpitoa. Mocking ja attribuutit ovat tärkeitä työkaluja tehokkaan yksikkötestauksen toteuttamiseen.

