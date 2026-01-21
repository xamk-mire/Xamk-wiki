# Test-Driven Development (TDD)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on TDD?](#mikä-on-tdd)
3. [TDD:n hyödyt](#tddn-hyödyt)
4. [Red-Green-Refactor sykli](#red-green-refactor-sykli)
5. [TDD:n säännöt](#tddn-säännöt)
6. [TDD käytännössä](#tdd-käytännössä)
7. [TDD vs. Perinteinen kehitys](#tdd-vs-perinteinen-kehitys)
8. [Haasteet ja ratkaisut](#haasteet-ja-ratkaisut)
9. [Parhaat käytännöt](#parhaat-käytännöt)
10. [Esimerkit](#esimerkit)

---

## Johdanto

Test-Driven Development (TDD) on ohjelmistokehityksen lähestymistapa, jossa testit kirjoitetaan **ennen** varsinaista koodia. TDD ei ole pelkkä testausmetodi, vaan **suunnittelutyökalu** joka ohjaa koodin rakennetta ja arkkitehtuuria.

### Materiaalin rakenne

- **Tämä tiedosto**: TDD teoria ja käytännöt
- **[TDD-Examples.md](TDD-Examples.md)**: Askel-askeleelta esimerkit TDD:stä
- **[Unit-Testing.md](Unit-Testing.md)**: Testauksen perusteet
- **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)**: Testausesimerkit

### Hyödyllisiä linkkejä

- [Kent Beck: Test-Driven Development](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Martin Fowler: TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Uncle Bob: The Three Rules of TDD](http://butunclebob.com/ArticleS.UncleBob.TheThreeRulesOfTdd)

---

## Mikä on TDD?

**Test-Driven Development (TDD)** on kehitysmenetelmä, jossa:

1. ✍️ **Kirjoitat testin ensin** - Testi epäonnistuu, koska koodia ei ole vielä
2. ✅ **Kirjoitat vähimmäiskoodin** - Juuri sen verran, että testi menee läpi
3. 🔄 **Refaktoroit koodin** - Parannat koodin laatua testien turvin

### TDD ei ole:

❌ **Pelkkää testausta** - Se on suunnittelutyökalu  
❌ **Testien kirjoittamista jälkikäteen** - Testit tulevat ensin  
❌ **Testien kirjoittamista koodin rinnalla** - Testit tulevat **ennen**

### TDD on:

✅ **Suunnittelumetodi** - Testit pakottavat miettimään rajapintoja  
✅ **Dokumentaatio** - Testit kertovat, miten koodia käytetään  
✅ **Laadunvarmistus** - Testit varmistavat toimivuuden  
✅ **Turvaverkko** - Testit antavat luottamusta refaktorointiin

---

## TDD:n hyödyt

### 1. Parempi suunnittelu

Kun kirjoitat testin ensin, joudut miettimään:
- Mitä luokka/metodi tekee?
- Miten sitä kutsutaan?
- Mitä se palauttaa?
- Mitkä ovat sen riippuvuudet?

**Tämä johtaa:**
- Selkeämpiin rajapintoihin
- Vähempiin riippuvuuksiin
- SOLID-periaatteiden noudattamiseen
- Testattavampaan koodiin

### 2. Vähemmän bugeja

```
Perinteinen: Koodi → Testit → Bugit löydetään myöhemmin
TDD: Testit → Koodi → Bugit havaitaan heti
```

- Virheet havaitaan välittömästi
- Regressiot estetään
- Turvaverkko refaktoroinnille

### 3. Luottamus koodiin

- Uskallat tehdä muutoksia
- Refaktorointi on turvallista
- Voit poistaa vanhaa koodia rohkeasti

### 4. Elävä dokumentaatio

Testit ovat paras dokumentaatio:
- Näyttävät miten koodia käytetään
- Pysyvät aina ajan tasalla
- Ovat ajettavissa

### 5. Nopeampi kehitys pitkällä tähtäimellä

Vaikka TDD tuntuu aluksi hitaalta:
- Vähemmän debuggausta
- Vähemmän regressioita
- Turvallinen refaktorointi
- Parempi koodin laatu

**Kehitysaika:**
```
Perinteinen: ████████████░░░░░░ (12 viikkoa)
              ^koodaus    ^debuggaus

TDD:        ██████████████ (14 viikkoa)
              ^testit+koodi (vähän debuggausta)
```

Vaikka TDD vie aluksi 15-20% enemmän aikaa, säästät:
- 40-80% vähemmän bugeja tuotannossa
- 50% vähemmän aikaa debuggaukseen
- Nopea ja turvallinen refaktorointi

---

## Red-Green-Refactor sykli

TDD perustuu kolmen vaiheen sykliin:

### 🔴 RED - Kirjoita epäonnistuva testi

**Mitä tehdään:**
1. Kirjoita testi uudelle toiminnallisuudelle
2. Aja testi - sen PITÄÄ epäonnistua
3. Varmista että testi epäonnistuu oikeasta syystä

**Miksi:**
- Varmistetaan että testi todella testaa jotain
- Jos testi menee läpi ilman koodia, se on virheellinen

**Esimerkki:**
```csharp
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    // Arrange
    Calculator calculator = new Calculator(); // Ei ole vielä olemassa!
    
    // Act
    int result = calculator.Add(2, 3); // Metodi ei ole vielä olemassa!
    
    // Assert
    Assert.Equal(5, result);
}
```

### 🟢 GREEN - Kirjoita vähimmäiskoodi

**Mitä tehdään:**
1. Kirjoita yksinkertaisin mahdollinen koodi
2. Älä mieti optimointia tai suunnittelua
3. Aja testi - sen pitää mennä läpi

**Miksi:**
- Nopea palaute
- Keskity yhteen asiaan kerrallaan
- Älä "over-engineer"

**Esimerkki:**
```csharp
public class Calculator
{
    public int Add(int a, int b)
    {
        return 5; // "Fake it 'til you make it"
    }
}
```

Tämä tuntuu typeräl tä, mutta seuraava testi pakottaa parantamaan:
```csharp
[Theory]
[InlineData(2, 3, 5)]
[InlineData(1, 1, 2)] // Tämä ei mene läpi!
public void Add_VariousNumbers_ReturnsSum(int a, int b, int expected)
{
    Calculator calculator = new Calculator();
    int result = calculator.Add(a, b);
    Assert.Equal(expected, result);
}
```

Nyt joudut kirjoittamaan oikean toteutuksen:
```csharp
public int Add(int a, int b)
{
    return a + b;
}
```

### 🔵 REFACTOR - Paranna koodia

**Mitä tehdään:**
1. Paranna koodin laatua
2. Poista toistoa (DRY)
3. Paranna luettavuutta
4. Aja testit joka muutoksen jälkeen

**Miksi:**
- Koodi pysyy puhtaana
- Testit varmistavat että mikään ei hajoa
- Tekninen velka ei kasva

**Esimerkki:**
```csharp
// Ennen refaktorointia
[Fact]
public void Test1()
{
    Calculator calculator = new Calculator();
    int result = calculator.Add(2, 3);
    Assert.Equal(5, result);
}

[Fact]
public void Test2()
{
    Calculator calculator = new Calculator();
    int result = calculator.Add(1, 1);
    Assert.Equal(2, result);
}

// Jälkeen refaktoroinnin
public class CalculatorTests
{
    private readonly Calculator _calculator;
    
    public CalculatorTests()
    {
        _calculator = new Calculator(); // Kerran!
    }
    
    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(1, 1, 2)]
    public void Add_VariousNumbers_ReturnsSum(int a, int b, int expected)
    {
        int result = _calculator.Add(a, b);
        Assert.Equal(expected, result);
    }
}
```

### Sykli graafisesti:

```
    🔴 RED
     ↓
Kirjoita
epäonnistuva  ←───────┐
testi              │
     ↓              │
    🟢 GREEN        │
     ↓              │
Kirjoita        Testit
vähimmäis-      läpi?
koodi              │
     ↓              │
Testit          Jatka
läpi?           seuraavaan
     │           ominaisuuteen
     ↓              │
    🔵 REFACTOR     │
     ↓              │
Paranna koodia  ────┘
(testit läpi)
```

---

## TDD:n säännöt

### Uncle Bob:n kolme sääntöä:

Robert C. Martin (Uncle Bob) on määritellyt TDD:lle kolme yksinkertaista sääntöä:

#### 1. Älä kirjoita tuotantokoodia ennen kuin sinulla on epäonnistuva testi

```csharp
// ❌ VÄÄRIN
public class Calculator
{
    public int Add(int a, int b)  // Ei testiä!
    {
        return a + b;
    }
}

// ✅ OIKEIN
// 1. Kirjoita ensin testi
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    Calculator calc = new Calculator();
    Assert.Equal(5, calc.Add(2, 3));
}

// 2. Sitten implementoi
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
}
```

#### 2. Älä kirjoita enempää testiä kuin tarvitaan yhden epäonnistumisen aikaansaamiseksi

Kompiloinnin epäonnistuminen = epäonnistuminen

```csharp
// ❌ VÄÄRIN - liikaa kerralla
[Fact]
public void ComplexTest()
{
    Calculator calc = new Calculator();
    Assert.Equal(5, calc.Add(2, 3));
    Assert.Equal(10, calc.Multiply(2, 5));
    Assert.Equal(1, calc.Subtract(3, 2));
    Assert.Equal(2, calc.Divide(4, 2));
}

// ✅ OIKEIN - yksi asia kerrallaan
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    Calculator calc = new Calculator();
    Assert.Equal(5, calc.Add(2, 3));
}
// Seuraava testi vasta kun tämä toimii!
```

#### 3. Älä kirjoita enempää tuotantokoodia kuin tarvitaan yhden testin läpäisyyn

```csharp
// ❌ VÄÄRIN - liikaa kerralla
[Fact]
public void Add_ReturnsSum()
{
    Assert.Equal(5, new Calculator().Add(2, 3));
}

public class Calculator
{
    public int Add(int a, int b) => a + b;
    public int Subtract(int a, int b) => a - b;  // Ei testiä!
    public int Multiply(int a, int b) => a * b;  // Ei testiä!
}

// ✅ OIKEIN - vain testin vaatima
public class Calculator
{
    public int Add(int a, int b) => a + b;
}
```

### TDD Mantra:

```
RED → GREEN → REFACTOR
RED → GREEN → REFACTOR
RED → GREEN → REFACTOR
...
```

Toistetaan loputtomiin, pienin askelin.

---

## TDD käytännössä

### 1. Aloita yksinkertaisesta

**Älä yritä rakentaa kaikkea kerralla:**

```
❌ VÄÄRIN:
Testi: Calculator joka laskee +, -, *, /, %, ^, sqrt, sin, cos...

✅ OIKEIN:
Testi 1: Calculator.Add(2, 3) = 5
Testi 2: Calculator.Add(0, 0) = 0
Testi 3: Calculator.Add(-1, 1) = 0
...
```

### 2. Baby Steps - Pienet askeleet

Jokainen askel on:
1. Kirjoita yksi pieni testi
2. Aja testi (RED)
3. Kirjoita vähimmäiskoodi (GREEN)
4. Refaktoroi (REFACTOR)
5. **Toista**

**Esimerkki progressio:**
```csharp
// Askel 1: Peruscase
[Fact]
public void Add_PositiveNumbers_ReturnsSum()
{
    Assert.Equal(5, new Calculator().Add(2, 3));
}

// Askel 2: Nollat
[Fact]
public void Add_WithZero_ReturnsOtherNumber()
{
    Assert.Equal(5, new Calculator().Add(5, 0));
}

// Askel 3: Negatiiviset
[Fact]
public void Add_NegativeNumbers_ReturnsSum()
{
    Assert.Equal(-5, new Calculator().Add(-2, -3));
}

// Askel 4: Suuret numerot
[Theory]
[InlineData(1000000, 2000000, 3000000)]
public void Add_LargeNumbers_ReturnsSum(int a, int b, int expected)
{
    Assert.Equal(expected, new Calculator().Add(a, b));
}
```

### 3. YAGNI - You Aren't Gonna Need It

**Älä tee mitään, mitä testit eivät vaadi:**

```csharp
// ❌ VÄÄRIN
public class Calculator
{
    private ILogger _logger;
    private ICache _cache;
    private IValidator _validator;
    
    public int Add(int a, int b)
    {
        _logger.Log("Adding...");
        var cached = _cache.Get(a, b);
        if (cached != null) return cached;
        
        _validator.Validate(a);
        _validator.Validate(b);
        
        var result = a + b;
        _cache.Set(a, b, result);
        return result;
    }
}

// ✅ OIKEIN (jos testit vaativat vain yhteenlaskua)
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
}
```

### 4. Triangulation - Kolmiomittaus

Kun et ole varma implementaatiosta, lisää useampia testejä:

```csharp
// Testi 1
[Fact]
public void Add_2And3_Returns5()
{
    Assert.Equal(5, new Calculator().Add(2, 3));
}

// Yksinkertaisin toteutus:
public int Add(int a, int b) => 5;

// Testi 2 paljastaa ongelman
[Fact]
public void Add_1And1_Returns2()
{
    Assert.Equal(2, new Calculator().Add(1, 1));
}

// Nyt oikea toteutus:
public int Add(int a, int b) => a + b;
```

### 5. Test List - Testilista

Pidä listaa testeistä, jotka pitää kirjoittaa:

```
TODO:
☐ Add positive numbers
☐ Add with zero
☐ Add negative numbers
☐ Add handles overflow?
☐ Subtract positive numbers
☐ Subtract negative numbers
...
```

Tee yksi kerrallaan, rasti kun valmis.

---

## TDD vs. Perinteinen kehitys

### Perinteinen tapa (Test-Last):

```
1. Suunnittele ───┐
2. Kirjoita koodi │  Kehitys
3. Testaa         │
4. Debuggaa      ─┘
5. Toista
```

**Ongelmat:**
- Testit kirjoitetaan "velvollisuudesta"
- Testaamaton koodi jää helposti
- Testit eivät ohjaa suunnittelua
- Vaikea testata koodia jälkikäteen
- Testikattavuus jää alhaiseksi

### TDD tapa (Test-First):

```
1. Kirjoita testi (RED)    ─┐
2. Kirjoita koodi (GREEN)   │ Toistuu
3. Refaktoroi (REFACTOR)   ─┘
```

**Hyödyt:**
- 100% testikattavuus automaattisesti
- Testattava koodi syntyy luonnostaan
- Testit ohjaavat suunnittelua
- Vähemmän bugeja
- Rohkea refaktorointi

### Vertailu taulukossa:

| Ominaisuus | Perinteinen | TDD |
|------------|-------------|-----|
| Testikattavuus | 40-60% | 90-100% |
| Bugien määrä | Keskiarvo | 40-80% vähemmän |
| Suunnittelun laatu | Vaihtelee | Korkeampi |
| Refaktorointi | Pelottavaa | Turvallista |
| Dokumentaatio | Vanhenee | Aina ajan tasalla |
| Kehitysnopeus (aluksi) | Nopeampi | Hitaampi |
| Kehitysnopeus (6kk jälkeen) | Hidastuu | Pysyy hyvänä |

---

## Haasteet ja ratkaisut

### Haaste 1: "TDD on hidasta"

**Ongelma:** TDD tuntuu hidastavan kehitystä.

**Ratkaisu:**
- TDD on investointi tulevaisuuteen
- Säästät aikaa debuggauksessa
- Välttämät regressiot
- Nopea feedback-loop

**Vertailu:**
```
Viikko 1: Perinteinen nopea, TDD hidas
Viikko 4: Perinteinen hidastuu, TDD tasaista
Viikko 12: Perinteinen hyvin hidasta (bugit), TDD tasaista
```

### Haaste 2: "En tiedä mitä testata"

**Ongelma:** En osaa kirjoittaa testiä ennen kuin tiedän ratkaisun.

**Ratkaisu:**
- Aloita vaatimuksista ("mitä tämän pitää tehdä?")
- Kirjoita testi käyttäjän näkökulmasta
- Älä mieti implementaatiota

**Esimerkki:**
```csharp
// Mieti: "Käyttäjä haluaa laskea yhteen kaksi numeroa"
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    // Mitä käyttäjä tekee?
    Calculator calc = new Calculator();
    
    // Mitä käyttäjä odottaa?
    int result = calc.Add(2, 3);
    
    // Mikä on oikea vastaus?
    Assert.Equal(5, result);
}
```

### Haaste 3: "Testit hajoavat kun refaktoroin"

**Ongelma:** Refaktorointi hajottaa testejä.

**Ratkaisu:**
- Testaa julkista rajapintaa, älä implementaatiota
- Älä testaa private-metodeja
- Testaa käyttäytymistä, älä rakennetta

**Esimerkki:**
```csharp
// ❌ Huono - testaa implementaatiota
[Fact]
public void InternalMethod_DoesX()
{
    Assert.Equal(expectedInternalState, obj.InternalState);
}

// ✅ Hyvä - testaa julkista rajapintaa
[Fact]
public void Process_ValidInput_ReturnsExpectedOutput()
{
    string result = processor.Process("input");
    Assert.Equal("expected", result);
}
```

### Haaste 4: "Liian monta testiä"

**Ongelma:** Testejä tulee liikaa.

**Ratkaisu:**
- Käytä `[Theory]` ja `[InlineData]`
- Poista duplikaattitestit
- Keskity edge caseihin

**Esimerkki:**
```csharp
// ❌ Liikaa testejä
[Fact]
public void Add_2And3_Returns5() { ... }
[Fact]
public void Add_1And1_Returns2() { ... }
[Fact]
public void Add_5And7_Returns12() { ... }

// ✅ Yksi testi, monta casea
[Theory]
[InlineData(2, 3, 5)]
[InlineData(1, 1, 2)]
[InlineData(5, 7, 12)]
public void Add_VariousInputs_ReturnsSum(int a, int b, int expected) { ... }
```

### Haaste 5: "Legacy-koodi ei ole testattavissa"

**Ongelma:** Vanha koodi on vaikeaa testata.

**Ratkaisu:**
- Aloita uusista ominaisuuksista
- Refaktoroi vanhaa koodia vähitellen
- Käytä "Characterization Tests"
- Lue: "Working Effectively with Legacy Code" (Michael Feathers)

---

## Parhaat käytännöt

### 1. Pidä testit nopeina

```
⚡ Tavoite: < 1ms per testi
🚀 Hyväksyttävä: < 10ms per testi
⚠️  Hidas: > 100ms per testi
❌ Liian hidas: > 1s per testi
```

**Keinot:**
- Käytä mockeja (ei oikeaa tietokantaa)
- Älä käytä Thread.Sleep()
- Älä tee verkkokutsuja
- Älä käytä tiedostojärjestelmää

### 2. Yksi assert per testi (yleensä)

```csharp
// ❌ Huono
[Fact]
public void ComplexTest()
{
    Assert.Equal(5, result.Count);
    Assert.True(result.IsValid);
    Assert.NotNull(result.Data);
}

// ✅ Hyvä
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

[Fact]
public void Data_ShouldNotBeNull() 
{ 
    Assert.NotNull(result.Data); 
}
```

### 3. Käytä kuvaavia nimiä

```csharp
// ❌ Huono
[Fact]
public void Test1() { ... }

// ⚠️  OK
[Fact]
public void AddTest() { ... }

// ✅ Hyvä
[Fact]
public void Add_TwoPositiveNumbers_ReturnsSum() { ... }

// ✅ Erinomainen
[Fact]
public void Add_WhenBothNumbersArePositive_ShouldReturnTheirSum() { ... }
```

### 4. Järjestä testit AAA-mallin mukaan

```csharp
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    // Arrange - Valmistele
    Calculator calculator = new Calculator();
    int a = 2;
    int b = 3;
    
    // Act - Toimi
    int result = calculator.Add(a, b);
    
    // Assert - Varmista
    Assert.Equal(5, result);
}
```

### 5. Testaa rajatapaukset (Edge Cases)

```csharp
[Theory]
[InlineData(0, 0, 0)]           // Nollat
[InlineData(-1, -1, -2)]        // Negatiiviset
[InlineData(int.MaxValue, 0)]    // Maksimiarvo
[InlineData(int.MinValue, 0)]    // Minimiarvo
public void Add_EdgeCases_HandledCorrectly(int a, int b, int expected)
{
    Assert.Equal(expected, new Calculator().Add(a, b));
}
```

### 6. Älä testaa frameworkia

```csharp
// ❌ Turha - testaa List:in toimintaa
[Fact]
public void List_Add_IncreasesCount()
{
    var list = new List<int>();
    list.Add(5);
    Assert.Equal(1, list.Count);
}

// ✅ Testaa omaa logiikkaa
[Fact]
public void AddItem_ValidItem_IncreasesCount()
{
    var manager = new ItemManager();
    manager.AddItem(new Item());
    Assert.Equal(1, manager.Count);
}
```

### 7. Pidä testit ylläp idettävinä

- DRY (Don't Repeat Yourself) myös testeissä
- Käytä helper-metodeja
- Käytä test fixtures
- Refaktoroi testit säännöllisesti

```csharp
// ❌ Toistetaan koodi
[Fact]
public void Test1()
{
    var repo = new Mock<IRepository>();
    var service = new Mock<IService>();
    var logger = new Mock<ILogger>();
    var sut = new MyClass(repo.Object, service.Object, logger.Object);
    // ...
}

[Fact]
public void Test2()
{
    var repo = new Mock<IRepository>();
    var service = new Mock<IService>();
    var logger = new Mock<ILogger>();
    var sut = new MyClass(repo.Object, service.Object, logger.Object);
    // ...
}

// ✅ Helper-metodi
public class MyClassTests
{
    private readonly Mock<IRepository> _repo;
    private readonly Mock<IService> _service;
    private readonly Mock<ILogger> _logger;
    
    public MyClassTests()
    {
        _repo = new Mock<IRepository>();
        _service = new Mock<IService>();
        _logger = new Mock<ILogger>();
    }
    
    private MyClass CreateSut() => 
        new MyClass(_repo.Object, _service.Object, _logger.Object);
    
    [Fact]
    public void Test1()
    {
        var sut = CreateSut();
        // ...
    }
}
```

---

## Esimerkit

Katso yksityiskohtaiset, askel-askeleelta esimerkit TDD:stä:

### [TDD-Examples.md](TDD-Examples.md)

Esimerkit sisältävät:
1. Yksinkertainen esimerkki: FizzBuzz
2. String Calculator Kata
3. Banking System
4. Shopping Cart
5. Password Validator

Jokainen esimerkki näyttää TDD-prosessin Red-Green-Refactor syklineen.

---

## Yhteenveto

### TDD pähkinänkuoressa:

1. 🔴 **RED** - Kirjoita epäonnistuva testi
2. 🟢 **GREEN** - Kirjoita vähimmäiskoodi
3. 🔵 **REFACTOR** - Paranna koodia
4. **Toista** loputtomiin

### TDD:n hyödyt:

✅ Parempi suunnittelu  
✅ Vähemmän bugeja  
✅ Luottamus koodiin  
✅ Elävä dokumentaatio  
✅ Turvallinen refaktorointi  
✅ Nopeampi kehitys pitkällä tähtäimellä

### Muista:

- Aloita pienistä askelista (Baby Steps)
- Noudata kolmea sääntöä
- Käytä AAA-mallia (Arrange-Act-Assert)
- Pidä testit nopeina
- Testaa julkista rajapintaa
- YAGNI - Älä tee enempää kuin testit vaativat

### Seuraavaksi:

1. Harjoittele esimerkeillä: **[TDD-Examples.md](TDD-Examples.md)**
2. Kokeile Code Kata:ja (FizzBuzz, String Calculator, etc.)
3. Käytä TDD:tä seuraavassa projektissa
4. Lue lisää: [Unit-Testing.md](Unit-Testing.md)

---

**"TDD on kuin ajaminen: Ensin tuntuu vaikealta, mutta pian se tulee automaatiksi ja et voi kuvitella tekemäsi ilman sitä."**

