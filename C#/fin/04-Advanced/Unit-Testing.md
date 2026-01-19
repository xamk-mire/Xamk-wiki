# Yksikkötestaus (Unit Testing)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on yksikkötestaus?](#mikä-on-yksikkötestaus)
3. [Miksi yksikkötestaus on tärkeää?](#miksi-yksikkötestaus-on-tärkeää)
4. [xUnit - Testausframework](#xunit---testausframework)
5. [Testien anatomia - AAA-malli](#testien-anatomia---aaa-malli)
6. [xUnit Attribuutit](#xunit-attribuutit)
7. [Assert-metodit](#assert-metodit)
8. [Mocking](#mocking)
9. [Testien organisointi](#testien-organisointi)
10. [Parhaat käytännöt](#parhaat-käytännöt)
11. [Esimerkit](#esimerkit)

---

## Johdanto

Yksikkötestaus on ohjelmistokehityksen keskeinen osa, joka varmistaa koodin laadun ja toimivuuden. Tämä materiaali käsittelee yksikkötestausta C#-kielessä käyttäen xUnit-frameworkia.

### Materiaalin rakenne

- **Tämä tiedosto**: Teoria ja käsitteet
- **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)**: Kattavat koodiesimerkit
- **Tehtävät**: Käytännön harjoitukset löytyvät kurssin tehtävärepositorioista

### Hyödyllisiä linkkejä

- [Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test)
- [xUnit dokumentaatio](https://xunit.net/)
- [Miten ajaa testejä Visual Studiossa](https://learn.microsoft.com/en-us/visualstudio/test/run-unit-tests-with-test-explorer?view=vs-2022)

---

## Mikä on yksikkötestaus?

**Yksikkötestaus** (Unit Testing) on automaattinen testi, joka testaa **pienen osan koodista** eristettynä muusta järjestelmästä. Tyypillisesti yksikkötesti testaa:
- Yhtä metodia
- Yhtä luokkaa
- Yhden toiminnallisuuden

### Yksikkötestin ominaisuudet

✅ **Nopea** - Suoritus kestää millisekunteja  
✅ **Eristetty** - Ei riipu ulkoisista resursseista (tietokanta, verkko)  
✅ **Toistettava** - Antaa aina saman tuloksen samoilla syötteillä  
✅ **Itsenäinen** - Ei riipu muista testeistä  
✅ **Selkeä** - Testaa yhtä asiaa kerrallaan

### Mitä yksikkötesti EI ole

❌ **Integraatiotesti** - Testaa useita komponentteja yhdessä

Integraatiotestit testaavat, miten eri osat järjestelmästä toimivat yhdessä. Esimerkiksi testataan, että sovellus pystyy tallentamaan datan oikeasti tietokantaan, ei mockattuna. Nämä testit ovat hitaampia ja monimutkaisempia kuin yksikkötestit.

**Esimerkki:** Testataan UserService:n ja oikean tietokannan yhteistoimintaa.

❌ **End-to-End testi (E2E)** - Testaa koko järjestelmää

E2E-testit testaavat koko sovelluksen toimintaa käyttäjän näkökulmasta, alusta loppuun. Ne simuloivat oikean käyttäjän toimintaa (esim. selaimessa), sisältäen käyttöliittymän, backendin, tietokannan ja kaikki välikomponentit.

**Esimerkki:** Käyttäjä kirjautuu sisään, luo tuotteen, lisää sen ostoskoriin ja maksaa tilauksen.

❌ **Manuaalinen testi** - Testataan käsin

Manuaalisessa testauksessa ihminen suorittaa testit käsin, ei automaattisesti. Tämä on hidasta, altista virheille ja vaikeaa toistaa systemaattisesti.  

---

## Miksi yksikkötestaus on tärkeää?

### 1. Varmistaa koodin toiminnan

Yksikkötestit varmistavat, että koodisi tekee sen, mitä sen pitää tehdä. Kun kirjoitat testin ennen tai heti koodin jälkeen, olet pakotettuna miettimään, mitä koodin pitää tehdä.

### 2. Havaitsee virheet aikaisin

Virheet löydetään heti kehitysvaiheessa, ei tuotannossa. Mitä aikaisemmin virhe löydetään, sitä halvempaa on korjata se.

**Virheen korjauksen hinta:**
- Kehitysvaiheessa: 1x
- Testausvaiheessa: 10x
- Tuotannossa: 100x

### 3. Helpottaa refaktorointia

Kun sinulla on kattavat testit, voit rohkeasti tehdä muutoksia koodiin. Jos rikot jotain, testit kertovat sen heti.

```
Ilman testejä: Pelkäät muuttaa koodia → Koodi muuttuu legacy-koodiksi
Testien kanssa: Muutokset ovat turvallisia → Koodi pysyy puhtaana
```

### 4. Dokumentoi koodia

Hyvät testit kertovat, miten koodia pitää käyttää. Ne ovat "elävää dokumentaatiota" joka pysyy ajan tasalla.

### 5. Parantaa arkkitehtuuria

Testattava koodi on yleensä paremmin suunniteltua:
- Modulaarinen (pienet, itsenäiset osat)
- Riippuvuudet injektoidaan
- Selkeät rajapinnat
- Single Responsibility Principle

### 6. Säästää aikaa pitkällä tähtäimellä

Vaikka testien kirjoittaminen vie aikaa alussa, se säästää aikaa:
- Vähemmän bugeja
- Nopea debuggaus
- Turvallinen refaktorointi
- Vähemmän regressioita

---

## xUnit - Testausframework

**xUnit** on moderni, avoimen lähdekoodin testausframework .NET-sovelluksille. Se on suosituin testausframework .NET Core -yhteisössä.

### Miksi xUnit?

✅ **Moderni** - Suunniteltu .NET Core -ajalle  
✅ **Suosittu** - Laajasti käytetty, hyvä tuki  
✅ **Yksinkertainen** - Helppo oppia ja käyttää  
✅ **Joustava** - Tukee erilaisia testausmalleja  
✅ **Suorituskykyinen** - Nopea testien suoritus

### Muita vaihtoehtoja

- **NUnit** - Vanhempi, myös suosittu
- **MSTest** - Microsoftin oma framework
- **xUnit** - Suositeltu uusiin projekteihin

### xUnit:n asennus

**NuGet-paketit:**
```xml
<PackageReference Include="xunit" Version="2.6.0" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.5.0" />
<PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
```

**dotnet CLI:**
```bash
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
```

---

## Testien anatomia - AAA-malli

AAA (Arrange-Act-Assert) on yleinen malli yksikkötestauksessa. Se jakaa testin kolmeen selkeään osaan.

### 1. Arrange (Järjestä)

**Valmistele testi:**
- Luo tarvittavat objektit
- Aseta alkuarvot
- Konfiguroi mock-objektit

```csharp
// Arrange
Calculator calculator = new Calculator();
int a = 5;
int b = 3;
int expected = 8;
```

### 2. Act (Toimi)

**Suorita testattava toiminto:**
- Kutsu testattavaa metodia
- Yleensä vain yksi rivi
- Tallenna tulos muuttujaan

```csharp
// Act
int result = calculator.Add(a, b);
```

### 3. Assert (Varmista)

**Tarkista tulos:**
- Vertaa tulosta odotukseen
- Käytä Assert-metodeja
- Jos Assert epäonnistuu, testi epäonnistuu

```csharp
// Assert
Assert.Equal(expected, result);
```

### Täydellinen esimerkki

```csharp
[Fact]
public void Add_ShouldReturnSum_WhenGivenTwoNumbers()
{
    // Arrange - Valmistele
    Calculator calculator = new Calculator();
    int a = 5;
    int b = 3;
    int expected = 8;

    // Act - Toimi
    int result = calculator.Add(a, b);

    // Assert - Varmista
    Assert.Equal(expected, result);
}
```

---

## xUnit Attribuutit

xUnit käyttää attribuutteja testin määrittelyyn ja konfigurointiin.

### [Fact] - Yksittäinen testi

`[Fact]` on perus-attribuutti yksittäiselle testille. Se ei ota parametreja.

**Käyttö:**
```csharp
[Fact]
public void TestMethodName()
{
    // Testi
}
```

**Esimerkkejä:**
```csharp
[Fact]
public void IsEven_ShouldReturnTrue_WhenNumberIsEven()
{
    // ...
}

[Fact]
public void GetUser_ShouldReturnNull_WhenUserNotFound()
{
    // ...
}
```

### [Theory] ja [InlineData] - Parametrisoidut testit

`[Theory]` mahdollistaa saman testin suorittamisen useilla eri syötteillä.

**Käyttö:**
```csharp
[Theory]
[InlineData(param1, param2, expected)]
[InlineData(param1, param2, expected)]
public void TestMethodName(Type param1, Type param2, Type expected)
{
    // Testi
}
```

**Esimerkki:**
```csharp
[Theory]
[InlineData(2, 3, 5)]
[InlineData(0, 0, 0)]
[InlineData(-1, 1, 0)]
[InlineData(100, 200, 300)]
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

**Hyödyt:**
- Vähemmän toistoa
- Helppo lisätä uusia testausskenaarioita
- Selkeä ja kompakti

### [MemberData] - Monimutkainen testdata

Kun testdata on liian monimutkaista `InlineData`:lle, käytä `MemberData`:a.

```csharp
public static IEnumerable<object[]> GetTestData()
{
    yield return new object[] { 2, 3, 5 };
    yield return new object[] { -1, -1, -2 };
    yield return new object[] { 0, 0, 0 };
}

[Theory]
[MemberData(nameof(GetTestData))]
public void Add_ShouldReturnSum(int a, int b, int expected)
{
    // Testi
}
```

### [Skip] - Ohita testi

Välillä haluat tilapäisesti ohittaa testin.

```csharp
[Fact(Skip = "Ei vielä toteutettu")]
public void FutureTest()
{
    // ...
}
```

---

## Assert-metodit

xUnit tarjoaa monia `Assert`-metodeja tulosten tarkistamiseen.

### Perustarkistukset

```csharp
// Yhtäsuuruus
Assert.Equal(expected, actual);
Assert.NotEqual(expected, actual);

// True/False
Assert.True(condition);
Assert.False(condition);

// Null-tarkistukset
Assert.Null(object);
Assert.NotNull(object);

// Sama objekti
Assert.Same(expected, actual);
Assert.NotSame(expected, actual);
```

### Numeeriset tarkistukset

```csharp
// Väli
Assert.InRange(actual, low, high);
Assert.NotInRange(actual, low, high);

// Desimaalien vertailu
Assert.Equal(expected, actual, precision: 2);
```

### String-tarkistukset

```csharp
// Sisältö
Assert.Contains("sub", "substring");
Assert.DoesNotContain("x", "string");

// Alku/Loppu
Assert.StartsWith("Hei", "Hei maailma");
Assert.EndsWith("ma", "Hei maailma");

// Tyhjyys
Assert.Empty(collection);
Assert.NotEmpty(collection);

// Regex
Assert.Matches(@"\d+", "123");
```

### Kokoelmat

```csharp
// Yksittäinen alkio
Assert.Single(collection);

// Sisältö
Assert.Contains(item, collection);
Assert.DoesNotContain(item, collection);

// Kaikki alkiot täyttävät ehdon
Assert.All(collection, item => Assert.True(item > 0));

// Tyhjyys
Assert.Empty(collection);
Assert.NotEmpty(collection);
```

### Poikkeukset

```csharp
// Odota poikkeusta
Assert.Throws<ArgumentException>(() => 
{
    method.Call();
});

// Tarkempi poikkeustesti
ArgumentException exception = Assert.Throws<ArgumentException>(() => 
{
    method.Call();
});
Assert.Equal("Parameter cannot be null", exception.Message);

// Async-poikkeukset
await Assert.ThrowsAsync<InvalidOperationException>(async () => 
{
    await method.CallAsync();
});
```

### Tyyppi-tarkistukset

```csharp
// Tyyppi
Assert.IsType<MyClass>(object);
Assert.IsNotType<OtherClass>(object);

// Peritty tyyppi
Assert.IsAssignableFrom<BaseClass>(object);
```

---

## Mocking

### Mitä on mocking?

**Mocking** on tekniikka, jossa luodaan "teko-objekteja" (mockeja) korvaamaan oikeat riippuvuudet testeissä. Näin voit testata koodia eristettynä ulkoisista riippuvuuksista.

### Miksi mockata?

#### 1. Eristäminen

```
Ilman mockausta:
YourClass → RealDatabase → Network → Database Server
  ↓
Testi riippuu kaikesta tästä

Mockauksen kanssa:
YourClass → MockDatabase
  ↓
Testi riippuu vain YourClass:sta
```

#### 2. Nopeus

- Oikea tietokantakutsu: 100-1000ms
- Mock-kutsu: <1ms
- Testisarja 1000 testillä: tunti → sekunti

#### 3. Kontrolli

Voit määrittää tarkalleen mitä mock palauttaa:
- Normaali tulos
- Virhetilanne
- Null-arvo
- Poikkeus

#### 4. Testattavuus

Voit testata tilanteita, jotka olisivat vaikeita tai mahdottomia oikeilla objekteilla:
- Verkkovirhe
- Tietokannan täyttyminen
- Aikaleimaan liittyvät ongelmat

### Moq-kirjasto

**Moq** on suosituin mocking-kirjasto C#:lle.

**Asennus:**
```bash
dotnet add package Moq
```

**Perusesimerkki:**
```csharp
using Moq;

// 1. Luo mock-olio
Mock<IEmailService> mock = new Mock<IEmailService>();

// 2. Määrittele mitä mock palauttaa
mock.Setup(x => x.SendEmail(It.IsAny<string>()))
    .Returns(true);

// 3. Käytä mockia
UserService service = new UserService(mock.Object);

// 4. Varmista että metodia kutsuttiin
mock.Verify(x => x.SendEmail("test@example.com"), Times.Once);
```

### Milloin mockata?

✅ **Mockata:**
- Tietokannat
- Ulkoiset API:t
- Tiedostojärjestelmä
- Sähköposti/SMS
- Aika (DateTime.Now)
- Satunnaisuus (Random)

❌ **Älä mockata:**
- Yksinkertaiset data-luokat
- Value Objects
- Omia yksinkertaisia luokkia
- .NET:n perusluokat (String, List, etc.)

### Rajapinnat (Interface) ja mocking

Mocking toimii parhaiten **rajapintojen** kanssa:

```csharp
// ❌ Vaikea mockata - konkreettinen luokka
public class UserService
{
    private EmailService _emailService; // Konkreettinen luokka
}

// ✅ Helppo mockata - rajapinta
public class UserService
{
    private IEmailService _emailService; // Rajapinta
}
```

**Hyödyt:**
- Mock voidaan luoda automaattisesti
- Riippuvuuden voi vaihtaa helposti
- Parempi arkkitehtuuri (Dependency Inversion)

---

## Testien organisointi

### Nimeämiskäytännöt

#### Testien nimeäminen

Käytä kuvaavaa nimeä, joka kertoo:
1. Mitä testataan
2. Millä syötteellä
3. Mitä odotetaan

**Kaava:**
```
MethodName_Scenario_ExpectedBehavior
```

**Esimerkkejä:**
```csharp
Add_PositiveNumbers_ReturnsSum
Add_NegativeNumbers_ReturnsSum
Add_ZeroAndNumber_ReturnsNumber
Divide_ByZero_ThrowsException
GetUser_ValidId_ReturnsUser
GetUser_InvalidId_ReturnsNull
```

#### Projektin nimeäminen

```
ProjectName → ProjectName.Tests
MyApp → MyApp.Tests
MyApp.Core → MyApp.Core.Tests
```

### Testien organisointi kansioihin

```
MyApp.Tests/
├── Unit/              # Yksikkötestit
│   ├── Services/
│   ├── Controllers/
│   └── Helpers/
├── Integration/       # Integraatiotestit
└── Fixtures/          # Yhteiset testidatat
```

### Test Class per Class

Luo yksi testiluokka jokaiselle testattavalle luokalle:

```
Calculator.cs → CalculatorTests.cs
UserService.cs → UserServiceTests.cs
```

---

## Parhaat käytännöt

### 1. Yksi Assert per testi (yleensä)

**Milloin käyttää:** Yleensä aina. Yksi testi testaa yhtä asiaa.

**Miksi:** Kun testi epäonnistuu, tiedät heti mikä meni pieleen. Jos testissä on monta Assertia, ensimmäinen epäonnistuminen pysäyttää testin eikä muita tarkistuksia suoriteta.

**Poikkeus:** Voit käyttää useampaa Assertia, kun testataan saman objektin useita ominaisuuksia, jotka kuuluvat yhteen (esim. koordinaatit x ja y).

```csharp
// ❌ Huono - useita asserteja eri asioista
[Fact]
public void BadTest()
{
    Assert.Equal(5, result.Count);
    Assert.True(result.IsValid);
    Assert.Equal("OK", result.Status);
}

// ✅ Hyvä - yksi asia kerrallaan
[Fact]
public void Count_ShouldBeFive()
{
    Assert.Equal(5, result.Count);
}

[Fact]
public void IsValid_ShouldBeTrue()
{
    Assert.True(result.IsValid);
}
```

### 2. Testit ovat itsenäisiä

**Milloin käyttää:** Aina. Jokainen testi on täysin riippumaton muista.

**Miksi:** Testit voidaan ajaa missä tahansa järjestyksessä ja rinnakkain. Jos testit riippuvat toisistaan, yksi epäonnistunut testi voi kaataa kaikki muut.

```csharp
// ❌ Huono - riippuu toisesta testistä
private static int sharedCounter = 0;

[Fact]
public void Test1() 
{ 
    sharedCounter++; 
}

[Fact]
public void Test2() 
{ 
    Assert.Equal(1, sharedCounter); // Epäonnistuu jos Test1 ei aja ensin
}

// ✅ Hyvä - itsenäinen
[Fact]
public void Test2() 
{ 
    int counter = 0;
    counter++;
    Assert.Equal(1, counter);
}
```

### 3. Testaa myös virhetilanteet

**Milloin käyttää:** Aina kun metodisi voi epäonnistua tai heittää poikkeuksen.

**Miksi:** Suurin osa bugeista tapahtuu virhetilanteissa. Pelkkien "happy path" -tapausten testaaminen ei riitä.

```csharp
// Testaa normaali tapaus
[Fact]
public void Divide_ValidNumbers_ReturnsQuotient()
{
    // ...
}

// Testaa virhetilanne
[Fact]
public void Divide_ByZero_ThrowsException()
{
    Assert.Throws<DivideByZeroException>(() => 
    {
        calculator.Divide(10, 0);
    });
}

// Testaa rajatapaukset
[Fact]
public void Divide_ZeroDividedByNumber_ReturnsZero()
{
    // ...
}
```

### 4. Käytä kuvaavia muuttujanimiä

**Milloin käyttää:** Aina.

**Miksi:** Testit ovat dokumentaatiota. Niiden pitää olla helppo lukea ja ymmärtää.

```csharp
// ❌ Huono
[Fact]
public void Test1()
{
    Thing x = new Thing();
    int y = x.Do(5);
    Assert.Equal(10, y);
}

// ✅ Hyvä
[Fact]
public void Double_ShouldReturnTwiceTheInput()
{
    Calculator calculator = new Calculator();
    int result = calculator.Double(5);
    Assert.Equal(10, result);
}
```

### 5. Älä testaa .NET:n perusominaisuuksia

**Milloin käyttää:** Älä koskaan testaa framework:n tai kirjastojen toimintaa.

**Miksi:** Microsoft on jo testannut .NET:n perusluokat. Keskity omaan logiikkaasi.

```csharp
// ❌ Turha - testaa List:in toimintaa
[Fact]
public void List_Add_IncreasesCount()
{
    List<int> list = new List<int>();
    list.Add(5);
    Assert.Equal(1, list.Count);
}

// ✅ Hyvä - testaa omaa logiikkaa
[Fact]
public void AddUser_ShouldIncreaseUserCount()
{
    UserService userService = new UserService();
    userService.AddUser(new User());
    Assert.Equal(1, userService.GetUserCount());
}
```

### 6. FIRST-periaatteet

**Milloin käyttää:** Pidä nämä periaatteet mielessä aina kun kirjoitat testejä.

Hyvät testit ovat:

- **F**ast (Nopeat) - Millisekunteja, ei sekunteja
- **I**ndependent (Riippumattomat) - Ei riipu toisista testeistä
- **R**epeatable (Toistettavat) - Sama tulos aina
- **S**elf-validating (Itsevalidoivat) - Pass/Fail, ei manuaalista tarkistusta
- **T**imely (Ajoissa) - Kirjoita ennen tai heti koodin jälkeen

---

## Esimerkit

Katso kattavat koodiesimerkit tiedostosta:

### [Unit-Testing-Examples.md](Unit-Testing-Examples.md)

Esimerkit sisältävät:
1. Perus-Assert esimerkit
2. Theory ja InlineData
3. Mocking Moq:lla
4. Async-testit
5. Exception-testit
6. Kokoelma-testit
7. Kattava esimerkki: UserService

---

## Yhteenveto

### Yksikkötestauksen hyödyt:
✅ Varmistaa koodin toiminnan  
✅ Havaitsee virheet aikaisin  
✅ Helpottaa refaktorointia  
✅ Dokumentoi koodia  
✅ Parantaa arkkitehtuuria  
✅ Säästää aikaa pitkällä tähtäimellä

### Muista:
- Käytä AAA-mallia (Arrange-Act-Assert)
- Kirjoita selkeät ja kuvaavat nimet
- Testit ovat itsenäisiä
- Mockkaa ulkoiset riippuvuudet
- Testaa myös virhetilanteet
- Noudata FIRST-periaatteita

### Seuraavaksi:
1. Tutustu esimerkkeihin: [Unit-Testing-Examples.md](Unit-Testing-Examples.md)
2. Harjoittele omilla projekteilla
3. Lue lisää: [Microsoftin dokumentaatio](https://learn.microsoft.com/en-us/dotnet/core/testing/)

---

