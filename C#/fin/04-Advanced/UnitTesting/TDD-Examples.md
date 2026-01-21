# TDD Esimerkit

Tämä tiedosto sisältää askel-askeleelta esimerkkejä Test-Driven Development:stä. Jokainen esimerkki näyttää Red-Green-Refactor syklin käytännössä.

## Sisällysluettelo

1. [FizzBuzz](#esimerkki-1-fizzbuzz)
2. [String Calculator](#esimerkki-2-string-calculator)
3. [Banking System](#esimerkki-3-banking-system)
4. [Password Validator](#esimerkki-4-password-validator)
5. [Shopping Cart](#esimerkki-5-shopping-cart)

---

## Esimerkki 1: FizzBuzz

FizzBuzz on klassinen TDD-harjoitus. Säännöt:
- Palauta "Fizz" jos luku on jaollinen 3:lla
- Palauta "Buzz" jos luku on jaollinen 5:llä
- Palauta "FizzBuzz" jos luku on jaollinen molemmilla
- Muuten palauta numero string:nä

### Askel 1: 🔴 RED - Ensimmäinen testi

```csharp
using Xunit;

public class FizzBuzzTests
{
    [Fact]
    public void Convert_1_Returns1()
    {
        // Arrange
        FizzBuzz fizzBuzz = new FizzBuzz(); // Ei ole vielä olemassa!
        
        // Act
        string result = fizzBuzz.Convert(1); // Ei ole vielä olemassa!
        
        // Assert
        Assert.Equal("1", result);
    }
}
```

**Tulos:** ❌ Koodi ei käänny - FizzBuzz luokkaa ei ole.

### Askel 2: 🟢 GREEN - Vähimmäiskoodi

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        return "1"; // Yksinkertaisin ratkaisu!
    }
}
```

**Tulos:** ✅ Testi menee läpi!

### Askel 3: 🔴 RED - Toinen testi

```csharp
[Fact]
public void Convert_2_Returns2()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(2);
    Assert.Equal("2", result);
}
```

**Tulos:** ❌ Odotti "2", sai "1"

### Askel 4: 🟢 GREEN - Oikea implementaatio

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        return number.ToString();
    }
}
```

**Tulos:** ✅ Molemmat testit menevät läpi!

### Askel 5: 🔴 RED - Fizz-testi

```csharp
[Fact]
public void Convert_3_ReturnsFizz()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(3);
    Assert.Equal("Fizz", result);
}
```

**Tulos:** ❌ Odotti "Fizz", sai "3"

### Askel 6: 🟢 GREEN - Lisää Fizz-logiikka

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        if (number % 3 == 0)
            return "Fizz";
            
        return number.ToString();
    }
}
```

**Tulos:** ✅ Kaikki testit menevät läpi!

### Askel 7: 🔴 RED - Buzz-testi

```csharp
[Fact]
public void Convert_5_ReturnsBuzz()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(5);
    Assert.Equal("Buzz", result);
}
```

**Tulos:** ❌ Odotti "Buzz", sai "5"

### Askel 8: 🟢 GREEN - Lisää Buzz-logiikka

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        if (number % 3 == 0)
            return "Fizz";
        if (number % 5 == 0)
            return "Buzz";
            
        return number.ToString();
    }
}
```

**Tulos:** ✅ Kaikki testit menevät läpi!

### Askel 9: 🔴 RED - FizzBuzz-testi

```csharp
[Fact]
public void Convert_15_ReturnsFizzBuzz()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(15);
    Assert.Equal("FizzBuzz", result);
}
```

**Tulos:** ❌ Odotti "FizzBuzz", sai "Fizz" (koska 15 % 3 == 0)

### Askel 10: 🟢 GREEN - Korjaa logiikka

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        if (number % 15 == 0)
            return "FizzBuzz";
        if (number % 3 == 0)
            return "Fizz";
        if (number % 5 == 0)
            return "Buzz";
            
        return number.ToString();
    }
}
```

**Tulos:** ✅ Kaikki testit menevät läpi!

### Askel 11: 🔵 REFACTOR - Paranna koodia

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        bool divisibleBy3 = number % 3 == 0;
        bool divisibleBy5 = number % 5 == 0;
        
        if (divisibleBy3 && divisibleBy5)
            return "FizzBuzz";
        if (divisibleBy3)
            return "Fizz";
        if (divisibleBy5)
            return "Buzz";
            
        return number.ToString();
    }
}
```

**Tulos:** ✅ Kaikki testit menevät edelleen läpi!

### Askel 12: 🔵 REFACTOR - Testit parametrisoiduksi

```csharp
public class FizzBuzzTests
{
    [Theory]
    [InlineData(1, "1")]
    [InlineData(2, "2")]
    [InlineData(3, "Fizz")]
    [InlineData(4, "4")]
    [InlineData(5, "Buzz")]
    [InlineData(6, "Fizz")]
    [InlineData(10, "Buzz")]
    [InlineData(15, "FizzBuzz")]
    [InlineData(30, "FizzBuzz")]
    public void Convert_VariousNumbers_ReturnsExpectedResult(int input, string expected)
    {
        FizzBuzz fizzBuzz = new FizzBuzz();
        string result = fizzBuzz.Convert(input);
        Assert.Equal(expected, result);
    }
}
```

**Tulos:** ✅ Kaikki testit menevät läpi! Valmis!

---

## Esimerkki 2: String Calculator

String Calculator Kata - klassinen TDD harjoitus.

**Vaatimukset:**
1. Tyhjä string palauttaa 0
2. Yksi numero palauttaa sen arvon
3. Kaksi numeroa pilkulla erotettuna palauttaa summan
4. Useita numeroita palauttaa summan
5. Rivinvaihto toimii erottimena

### Askel 1: 🔴 RED - Tyhjä string

```csharp
public class StringCalculatorTests
{
    [Fact]
    public void Add_EmptyString_ReturnsZero()
    {
        StringCalculator calculator = new StringCalculator();
        int result = calculator.Add("");
        Assert.Equal(0, result);
    }
}
```

### Askel 2: 🟢 GREEN - Yksinkertaisin ratkaisu

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        return 0;
    }
}
```

✅ Testi läpi!

### Askel 3: 🔴 RED - Yksi numero

```csharp
[Fact]
public void Add_SingleNumber_ReturnsNumber()
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add("5");
    Assert.Equal(5, result);
}
```

### Askel 4: 🟢 GREEN - Parse numero

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        if (string.IsNullOrEmpty(numbers))
            return 0;
            
        return int.Parse(numbers);
    }
}
```

✅ Molemmat testit läpi!

### Askel 5: 🔴 RED - Kaksi numeroa

```csharp
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add("1,2");
    Assert.Equal(3, result);
}
```

❌ Epäonnistuu (FormatException)

### Askel 6: 🟢 GREEN - Split ja summaa

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        if (string.IsNullOrEmpty(numbers))
            return 0;
        
        if (!numbers.Contains(","))
            return int.Parse(numbers);
        
        string[] parts = numbers.Split(',');
        return int.Parse(parts[0]) + int.Parse(parts[1]);
    }
}
```

✅ Kaikki testit läpi!

### Askel 7: 🔴 RED - Useita numeroita

```csharp
[Theory]
[InlineData("1,2,3", 6)]
[InlineData("1,2,3,4", 10)]
public void Add_MultipleNumbers_ReturnsSum(string input, int expected)
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add(input);
    Assert.Equal(expected, result);
}
```

❌ Epäonnistuu

### Askel 8: 🟢 GREEN - Loop kaikkien yli

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        if (string.IsNullOrEmpty(numbers))
            return 0;
        
        string[] parts = numbers.Split(',');
        int sum = 0;
        
        foreach (string part in parts)
        {
            sum += int.Parse(part);
        }
        
        return sum;
    }
}
```

✅ Kaikki testit läpi!

### Askel 9: 🔵 REFACTOR - LINQ

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        if (string.IsNullOrEmpty(numbers))
            return 0;
        
        return numbers
            .Split(',')
            .Select(int.Parse)
            .Sum();
    }
}
```

✅ Testit läpi ja koodi siistimpi!

### Askel 10: 🔴 RED - Rivinvaihto erottimena

```csharp
[Fact]
public void Add_NewlineDelimiter_ReturnsSum()
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add("1\n2,3");
    Assert.Equal(6, result);
}
```

### Askel 11: 🟢 GREEN - Useampia erottimia

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        if (string.IsNullOrEmpty(numbers))
            return 0;
        
        return numbers
            .Split(new[] { ',', '\n' })
            .Select(int.Parse)
            .Sum();
    }
}
```

✅ Valmis!

---

## Esimerkki 3: Banking System

Rakennetaan yksinkertainen pankkijärjestelmä TDD:llä.

### Askel 1: 🔴 RED - Uusi tili

```csharp
public class BankAccountTests
{
    [Fact]
    public void NewAccount_HasZeroBalance()
    {
        BankAccount account = new BankAccount();
        decimal balance = account.GetBalance();
        Assert.Equal(0, balance);
    }
}
```

### Askel 2: 🟢 GREEN - Toteuta

```csharp
public class BankAccount
{
    private decimal _balance = 0;
    
    public decimal GetBalance()
    {
        return _balance;
    }
}
```

✅ Testi läpi!

### Askel 3: 🔴 RED - Talletus

```csharp
[Fact]
public void Deposit_100_IncreasesBalance()
{
    BankAccount account = new BankAccount();
    account.Deposit(100);
    Assert.Equal(100, account.GetBalance());
}
```

### Askel 4: 🟢 GREEN - Toteuta talletus

```csharp
public class BankAccount
{
    private decimal _balance = 0;
    
    public void Deposit(decimal amount)
    {
        _balance += amount;
    }
    
    public decimal GetBalance()
    {
        return _balance;
    }
}
```

✅ Testit läpi!

### Askel 5: 🔴 RED - Nosto

```csharp
[Fact]
public void Withdraw_50_DecreasesBalance()
{
    BankAccount account = new BankAccount();
    account.Deposit(100);
    account.Withdraw(50);
    Assert.Equal(50, account.GetBalance());
}
```

### Askel 6: 🟢 GREEN - Toteuta nosto

```csharp
public class BankAccount
{
    private decimal _balance = 0;
    
    public void Deposit(decimal amount)
    {
        _balance += amount;
    }
    
    public void Withdraw(decimal amount)
    {
        _balance -= amount;
    }
    
    public decimal GetBalance()
    {
        return _balance;
    }
}
```

✅ Testit läpi!

### Askel 7: 🔴 RED - Ei saa nostaa yli saldon

```csharp
[Fact]
public void Withdraw_MoreThanBalance_ThrowsException()
{
    BankAccount account = new BankAccount();
    account.Deposit(100);
    
    Assert.Throws<InvalidOperationException>(() => 
        account.Withdraw(150));
}
```

### Askel 8: 🟢 GREEN - Lisää validointi

```csharp
public class BankAccount
{
    private decimal _balance = 0;
    
    public void Deposit(decimal amount)
    {
        _balance += amount;
    }
    
    public void Withdraw(decimal amount)
    {
        if (amount > _balance)
            throw new InvalidOperationException("Insufficient funds");
            
        _balance -= amount;
    }
    
    public decimal GetBalance()
    {
        return _balance;
    }
}
```

✅ Testit läpi!

### Askel 9: 🔴 RED - Negatiivinen talletus

```csharp
[Fact]
public void Deposit_NegativeAmount_ThrowsException()
{
    BankAccount account = new BankAccount();
    Assert.Throws<ArgumentException>(() => 
        account.Deposit(-100));
}
```

### Askel 10: 🟢 GREEN - Validoi talletukset

```csharp
public void Deposit(decimal amount)
{
    if (amount <= 0)
        throw new ArgumentException("Amount must be positive");
        
    _balance += amount;
}
```

### Askel 11: 🔵 REFACTOR - Paranna rakennetta

```csharp
public class BankAccount
{
    private decimal _balance = 0;
    
    public void Deposit(decimal amount)
    {
        ValidatePositiveAmount(amount);
        _balance += amount;
    }
    
    public void Withdraw(decimal amount)
    {
        ValidatePositiveAmount(amount);
        ValidateSufficientFunds(amount);
        _balance -= amount;
    }
    
    public decimal GetBalance() => _balance;
    
    private void ValidatePositiveAmount(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Amount must be positive", nameof(amount));
    }
    
    private void ValidateSufficientFunds(decimal amount)
    {
        if (amount > _balance)
            throw new InvalidOperationException("Insufficient funds");
    }
}
```

✅ Testit läpi ja koodi siistimpi!

---

## Esimerkki 4: Password Validator

Rakennetaan salasanan validaattori TDD:llä.

**Vaatimukset:**
- Vähintään 8 merkkiä
- Sisältää isoja kirjaimia
- Sisältää pieniä kirjaimia
- Sisältää numeroita
- Sisältää erikoismerkkejä

### Askel 1: 🔴 RED - Liian lyhyt

```csharp
public class PasswordValidatorTests
{
    [Fact]
    public void Validate_TooShort_ReturnsFalse()
    {
        PasswordValidator validator = new PasswordValidator();
        bool result = validator.Validate("short");
        Assert.False(result);
    }
}
```

### Askel 2: 🟢 GREEN - Yksinkertainen implementaatio

```csharp
public class PasswordValidator
{
    public bool Validate(string password)
    {
        return password.Length >= 8;
    }
}
```

✅ Testi läpi!

### Askel 3: 🔴 RED - Kelvollinen salasana

```csharp
[Fact]
public void Validate_ValidPassword_ReturnsTrue()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("Valid123!");
    Assert.True(result);
}
```

✅ Testi läpi heti (8 merkkiä)!

### Askel 4: 🔴 RED - Pitää sisältää isoja kirjaimia

```csharp
[Fact]
public void Validate_NoUppercase_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("lowercase123!");
    Assert.False(result);
}
```

❌ Testi epäonnistuu

### Askel 5: 🟢 GREEN - Tarkista isot kirjaimet

```csharp
public class PasswordValidator
{
    public bool Validate(string password)
    {
        if (password.Length < 8)
            return false;
            
        if (!password.Any(char.IsUpper))
            return false;
            
        return true;
    }
}
```

✅ Testit läpi!

### Askel 6: 🔴 RED - Pitää sisältää pieniä kirjaimia

```csharp
[Fact]
public void Validate_NoLowercase_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("UPPERCASE123!");
    Assert.False(result);
}
```

### Askel 7: 🟢 GREEN - Tarkista pienet kirjaimet

```csharp
public class PasswordValidator
{
    public bool Validate(string password)
    {
        if (password.Length < 8)
            return false;
        if (!password.Any(char.IsUpper))
            return false;
        if (!password.Any(char.IsLower))
            return false;
            
        return true;
    }
}
```

✅ Testit läpi!

### Askel 8: 🔴 RED - Pitää sisältää numeroita

```csharp
[Fact]
public void Validate_NoDigits_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("Password!");
    Assert.False(result);
}
```

### Askel 9: 🟢 GREEN - Tarkista numerot

```csharp
public bool Validate(string password)
{
    if (password.Length < 8)
        return false;
    if (!password.Any(char.IsUpper))
        return false;
    if (!password.Any(char.IsLower))
        return false;
    if (!password.Any(char.IsDigit))
        return false;
        
    return true;
}
```

✅ Testit läpi!

### Askel 10: 🔴 RED - Pitää sisältää erikoismerkkejä

```csharp
[Fact]
public void Validate_NoSpecialChars_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("Password123");
    Assert.False(result);
}
```

### Askel 11: 🟢 GREEN - Tarkista erikoismerkit

```csharp
public bool Validate(string password)
{
    if (password.Length < 8)
        return false;
    if (!password.Any(char.IsUpper))
        return false;
    if (!password.Any(char.IsLower))
        return false;
    if (!password.Any(char.IsDigit))
        return false;
    if (!password.Any(c => !char.IsLetterOrDigit(c)))
        return false;
        
    return true;
}
```

✅ Testit läpi!

### Askel 12: 🔵 REFACTOR - Paranna rakennetta

```csharp
public class PasswordValidator
{
    private const int MinLength = 8;
    
    public bool Validate(string password)
    {
        return HasMinimumLength(password) &&
               HasUppercase(password) &&
               HasLowercase(password) &&
               HasDigit(password) &&
               HasSpecialCharacter(password);
    }
    
    private bool HasMinimumLength(string password) => 
        password.Length >= MinLength;
    
    private bool HasUppercase(string password) => 
        password.Any(char.IsUpper);
    
    private bool HasLowercase(string password) => 
        password.Any(char.IsLower);
    
    private bool HasDigit(string password) => 
        password.Any(char.IsDigit);
    
    private bool HasSpecialCharacter(string password) => 
        password.Any(c => !char.IsLetterOrDigit(c));
}
```

✅ Testit läpi ja koodi paljon luettavampi!

### Askel 13: 🔵 REFACTOR - Parametrisoi testit

```csharp
public class PasswordValidatorTests
{
    [Theory]
    [InlineData("short", false)]          // Liian lyhyt
    [InlineData("lowercase123!", false)]  // Ei isoja
    [InlineData("UPPERCASE123!", false)]  // Ei pieniä
    [InlineData("Password!", false)]      // Ei numeroita
    [InlineData("Password123", false)]    // Ei erikoismerkkejä
    [InlineData("Valid123!", true)]       // Kelvollinen
    [InlineData("MyP@ssw0rd", true)]     // Kelvollinen
    public void Validate_VariousPasswords_ReturnsExpected(string password, bool expected)
    {
        PasswordValidator validator = new PasswordValidator();
        bool result = validator.Validate(password);
        Assert.Equal(expected, result);
    }
}
```

✅ Valmis!

---

## Esimerkki 5: Shopping Cart

Rakennetaan ostoskori TDD:llä.

### Askel 1: 🔴 RED - Tyhjä ostoskori

```csharp
public class ShoppingCartTests
{
    [Fact]
    public void NewCart_IsEmpty()
    {
        ShoppingCart cart = new ShoppingCart();
        Assert.Equal(0, cart.ItemCount);
    }
}
```

### Askel 2: 🟢 GREEN - Toteuta

```csharp
public class ShoppingCart
{
    public int ItemCount => 0;
}
```

✅ Testi läpi!

### Askel 3: 🔴 RED - Lisää tuote

```csharp
[Fact]
public void AddItem_SingleItem_IncreasesCount()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 1.5m, 1));
    Assert.Equal(1, cart.ItemCount);
}
```

### Askel 4: 🟢 GREEN - Toteuta AddItem

```csharp
public class CartItem
{
    public string Name { get; }
    public decimal Price { get; }
    public int Quantity { get; }
    
    public CartItem(string name, decimal price, int quantity)
    {
        Name = name;
        Price = price;
        Quantity = quantity;
    }
}

public class ShoppingCart
{
    private readonly List<CartItem> _items = new();
    
    public int ItemCount => _items.Count;
    
    public void AddItem(CartItem item)
    {
        _items.Add(item);
    }
}
```

✅ Testit läpi!

### Askel 5: 🔴 RED - Laske kokonaishinta

```csharp
[Fact]
public void GetTotal_SingleItem_ReturnsPrice()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 1.5m, 2));
    Assert.Equal(3.0m, cart.GetTotal());
}
```

### Askel 6: 🟢 GREEN - Toteuta GetTotal

```csharp
public decimal GetTotal()
{
    return _items.Sum(item => item.Price * item.Quantity);
}
```

✅ Testit läpi!

### Askel 7: 🔴 RED - Useita tuotteita

```csharp
[Fact]
public void GetTotal_MultipleItems_ReturnsSumOfPrices()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 1.5m, 2));   // 3.0
    cart.AddItem(new CartItem("Banana", 0.5m, 3));  // 1.5
    Assert.Equal(4.5m, cart.GetTotal());
}
```

✅ Testi läpi heti!

### Askel 8: 🔴 RED - Poista tuote

```csharp
[Fact]
public void RemoveItem_ExistingItem_DecreasesCount()
{
    ShoppingCart cart = new ShoppingCart();
    CartItem item = new CartItem("Apple", 1.5m, 1);
    cart.AddItem(item);
    cart.RemoveItem(item);
    Assert.Equal(0, cart.ItemCount);
}
```

### Askel 9: 🟢 GREEN - Toteuta RemoveItem

```csharp
public void RemoveItem(CartItem item)
{
    _items.Remove(item);
}
```

✅ Testit läpi!

### Askel 10: 🔴 RED - Alennus

```csharp
[Fact]
public void ApplyDiscount_10Percent_ReducesTotal()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 10m, 1));
    cart.ApplyDiscount(0.10m); // 10% alennus
    Assert.Equal(9m, cart.GetTotal());
}
```

### Askel 11: 🟢 GREEN - Toteuta alennus

```csharp
public class ShoppingCart
{
    private readonly List<CartItem> _items = new();
    private decimal _discount = 0;
    
    public int ItemCount => _items.Count;
    
    public void AddItem(CartItem item)
    {
        _items.Add(item);
    }
    
    public void RemoveItem(CartItem item)
    {
        _items.Remove(item);
    }
    
    public void ApplyDiscount(decimal discount)
    {
        _discount = discount;
    }
    
    public decimal GetTotal()
    {
        decimal subtotal = _items.Sum(item => item.Price * item.Quantity);
        return subtotal * (1 - _discount);
    }
}
```

✅ Testit läpi!

### Askel 12: 🔵 REFACTOR - Paranna rakennetta

```csharp
public class ShoppingCart
{
    private readonly List<CartItem> _items = new();
    private decimal _discount = 0;
    
    public int ItemCount => _items.Count;
    
    public IReadOnlyList<CartItem> Items => _items.AsReadOnly();
    
    public void AddItem(CartItem item)
    {
        if (item == null)
            throw new ArgumentNullException(nameof(item));
            
        _items.Add(item);
    }
    
    public void RemoveItem(CartItem item)
    {
        if (item == null)
            throw new ArgumentNullException(nameof(item));
            
        _items.Remove(item);
    }
    
    public void ApplyDiscount(decimal discount)
    {
        if (discount < 0 || discount > 1)
            throw new ArgumentOutOfRangeException(nameof(discount), 
                "Discount must be between 0 and 1");
                
        _discount = discount;
    }
    
    public decimal GetSubtotal()
    {
        return _items.Sum(item => item.Price * item.Quantity);
    }
    
    public decimal GetDiscountAmount()
    {
        return GetSubtotal() * _discount;
    }
    
    public decimal GetTotal()
    {
        return GetSubtotal() - GetDiscountAmount();
    }
    
    public void Clear()
    {
        _items.Clear();
    }
}
```

✅ Testit läpi, koodi parempi!

---

## Yhteenveto

Näissä esimerkeissä olemme nähneet:

### TDD-prosessi käytännössä:
1. 🔴 **RED** - Kirjoita epäonnistuva testi
2. 🟢 **GREEN** - Kirjoita yksinkertaisin koodi
3. 🔵 **REFACTOR** - Paranna koodia
4. **Toista**

### Opittua:
- Aloita yksinkertaisesta
- Pienet askeleet (Baby Steps)
- Yksi testi kerrallaan
- Testit ohjaavat suunnittelua
- Refaktoroi säännöllisesti
- Testit ovat turvaverkko

### Vinkkejä:
- Älä suunnittele liikaa etukäteen
- Anna testien ohjata suunnittelua
- Älä pelkää yksinkertaisia ratkaisuja
- Refaktoroi kun testit ovat vihreät
- Pidä testit nopeina
- Testaa rajatapaukset

### Harjoittele lisää:
- [Code Katas](http://codekata.com/)
- [Cyber Dojo](https://cyber-dojo.org/)
- [Codewars](https://www.codewars.com/)

Palaa teoriaan: [TDD.md](TDD.md)

