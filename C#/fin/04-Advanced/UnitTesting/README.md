# Yksikkötestaus ja TDD

Tervetuloa yksikkötestauksen ja Test-Driven Development (TDD) materiaaleihin!

## Sisältö

### Yksikkötestaus
- **[Unit-Testing.md](Unit-Testing.md)** - Yksikkötestauksen perusteet
  - Mikä on yksikkötestaus?
  - xUnit-framework
  - AAA-malli (Arrange-Act-Assert)
  - Assert-metodit
  - Mocking Moq:lla
  - Parhaat käytännöt

- **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)** - Kattavat koodiesimerkit
  - Perus-Assert esimerkit
  - Theory ja InlineData
  - Mocking-esimerkit
  - Async-testit
  - Exception-testit
  - Kokoelma-testit
  - Kattava esimerkki: UserService

### Test-Driven Development (TDD)
- **[TDD.md](TDD.md)** - TDD teoria ja käytännöt
  - Mikä on TDD?
  - Red-Green-Refactor sykli
  - TDD:n säännöt
  - TDD:n hyödyt
  - Haasteet ja ratkaisut
  - Parhaat käytännöt

- **[TDD-Examples.md](TDD-Examples.md)** - TDD käytännössä
  - FizzBuzz
  - String Calculator
  - Banking System
  - Password Validator
  - Shopping Cart
  - (Jokainen esimerkki askel-askeleelta Red-Green-Refactor syklillä)

## Oppimisjärjestys

Suosittelemme opiskelua seuraavassa järjestyksessä:

### 1. Aloita yksikkötestauksesta
📚 **[Unit-Testing.md](Unit-Testing.md)** - Opi testauksen perusteet
- Mikä on yksikkötestaus?
- xUnit-framework
- AAA-malli
- Assert-metodit
- Mocking

### 2. Harjoittele esimerkeillä
💻 **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)** - Katso koodiesimerkit
- Yksinkertaisista monimutkaisempiin
- Calculator, StringHelper, UserService
- Mocking-esimerkit

### 3. Opi TDD
🔄 **[TDD.md](TDD.md)** - Testivetoinen kehitys
- Red-Green-Refactor sykli
- TDD:n säännöt ja periaatteet
- Milloin ja miten käyttää

### 4. Harjoittele TDD:tä
🚀 **[TDD-Examples.md](TDD-Examples.md)** - TDD käytännössä
- Seuraa askel-askeleelta esimerkkejä
- Ymmärrä prosessi
- Kokeile itse

## Pika-aloitus

### Asennus

1. Luo uusi testi-projekti:
```bash
dotnet new xunit -n MyProject.Tests
cd MyProject.Tests
```

2. Asenna tarvittavat paketit:
```bash
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
dotnet add package Moq
```

3. Aja testit:
```bash
dotnet test
```

### Ensimmäinen testi

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_TwoNumbers_ReturnsSum()
    {
        // Arrange
        Calculator calculator = new Calculator();
        
        // Act
        int result = calculator.Add(2, 3);
        
        // Assert
        Assert.Equal(5, result);
    }
}

public class Calculator
{
    public int Add(int a, int b) => a + b;
}
```

Aja: `dotnet test`

## TDD-sykli pähkinänkuoressa

```
🔴 RED
Kirjoita epäonnistuva testi
    ↓
🟢 GREEN
Kirjoita vähimmäiskoodi (testi läpi)
    ↓
🔵 REFACTOR
Paranna koodia (testit läpi)
    ↓
Toista ↩️
```

## Hyödyllisiä resursseja

### Dokumentaatio
- [xUnit dokumentaatio](https://xunit.net/)
- [Moq dokumentaatio](https://github.com/moq/moq4)
- [Microsoft: Unit testing](https://learn.microsoft.com/en-us/dotnet/core/testing/)

### Kirjat
- **Test-Driven Development: By Example** - Kent Beck
- **Growing Object-Oriented Software, Guided by Tests** - Steve Freeman & Nat Pryce
- **The Art of Unit Testing** - Roy Osherove
- **Working Effectively with Legacy Code** - Michael Feathers

### Harjoitussivustot
- [Code Katas](http://codekata.com/)
- [Cyber Dojo](https://cyber-dojo.org/)
- [Codewars](https://www.codewars.com/)
- [Exercism](https://exercism.org/)

### Videot
- [Uncle Bob: The Three Rules of TDD](https://www.youtube.com/watch?v=AoIfc5NwRks)
- [Ian Cooper: TDD, Where Did It All Go Wrong](https://www.youtube.com/watch?v=EZ05e7EMOLM)

## Vinkkejä

### Yksikkötestaus
✅ Pidä testit nopeina (< 10ms)  
✅ Testit ovat itsenäisiä  
✅ Käytä AAA-mallia  
✅ Yksi Assert per testi (yleensä)  
✅ Testaa myös virhetilanteet  
✅ Käytä kuvaavia nimiä

### TDD
✅ Aloita yksinkertaisesta  
✅ Pienet askeleet (Baby Steps)  
✅ Red → Green → Refactor  
✅ Testit ensin, koodi sitten  
✅ YAGNI - Älä tee ylimääräistä  
✅ Anna testien ohjata suunnittelua

## Seuraavaksi

Kun hallitset yksikkötestauksen ja TDD:n, voit jatkaa:
- **[Design Principles](../Design-Principles.md)** - SOLID-periaatteet
- **[Design Patterns](../Design-Patterns.md)** - Suunnittelumallit
- **[Architecture](../Architecture/)** - Ohjelmistoarkkitehtuuri

---

**Muista:** TDD on taito joka kehittyy harjoittelun myötä. Älä luovuta jos se tuntuu aluksi vaikealta!

