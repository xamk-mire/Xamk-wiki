# TDD Examples

This file contains step-by-step examples of Test-Driven Development. Each example shows the Red-Green-Refactor cycle in practice.

## Table of Contents

1. [FizzBuzz](#example-1-fizzbuzz)
2. [String Calculator](#example-2-string-calculator)
3. [Banking System](#example-3-banking-system)
4. [Password Validator](#example-4-password-validator)
5. [Shopping Cart](#example-5-shopping-cart)

---

## Example 1: FizzBuzz

FizzBuzz is a classic TDD exercise. Rules:
- Return "Fizz" if the number is divisible by 3
- Return "Buzz" if the number is divisible by 5
- Return "FizzBuzz" if the number is divisible by both
- Otherwise return the number as a string

### Step 1: 🔴 RED - First Test

```csharp
using Xunit;

public class FizzBuzzTests
{
    [Fact]
    public void Convert_1_Returns1()
    {
        // Arrange
        FizzBuzz fizzBuzz = new FizzBuzz(); // Doesn't exist yet!
        
        // Act
        string result = fizzBuzz.Convert(1); // Doesn't exist yet!
        
        // Assert
        Assert.Equal("1", result);
    }
}
```

**Result:** ❌ Code doesn't compile - FizzBuzz class doesn't exist.

### Step 2: 🟢 GREEN - Minimum Code

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        return "1"; // Simplest solution!
    }
}
```

**Result:** ✅ Test passes!

### Step 3: 🔴 RED - Second Test

```csharp
[Fact]
public void Convert_2_Returns2()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(2);
    Assert.Equal("2", result);
}
```

**Result:** ❌ Expected "2", got "1"

### Step 4: 🟢 GREEN - Correct Implementation

```csharp
public class FizzBuzz
{
    public string Convert(int number)
    {
        return number.ToString();
    }
}
```

**Result:** ✅ Both tests pass!

### Step 5: 🔴 RED - Fizz Test

```csharp
[Fact]
public void Convert_3_ReturnsFizz()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(3);
    Assert.Equal("Fizz", result);
}
```

**Result:** ❌ Expected "Fizz", got "3"

### Step 6: 🟢 GREEN - Add Fizz Logic

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

**Result:** ✅ All tests pass!

### Step 7: 🔴 RED - Buzz Test

```csharp
[Fact]
public void Convert_5_ReturnsBuzz()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(5);
    Assert.Equal("Buzz", result);
}
```

**Result:** ❌ Expected "Buzz", got "5"

### Step 8: 🟢 GREEN - Add Buzz Logic

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

**Result:** ✅ All tests pass!

### Step 9: 🔴 RED - FizzBuzz Test

```csharp
[Fact]
public void Convert_15_ReturnsFizzBuzz()
{
    FizzBuzz fizzBuzz = new FizzBuzz();
    string result = fizzBuzz.Convert(15);
    Assert.Equal("FizzBuzz", result);
}
```

**Result:** ❌ Expected "FizzBuzz", got "Fizz" (since 15 % 3 == 0)

### Step 10: 🟢 GREEN - Fix Logic

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

**Result:** ✅ All tests pass!

### Step 11: 🔵 REFACTOR - Improve Code

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

**Result:** ✅ All tests still pass!

### Step 12: 🔵 REFACTOR - Parameterize Tests

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

**Result:** ✅ All tests pass! Done!

---

## Example 2: String Calculator

String Calculator Kata - a classic TDD exercise.

**Requirements:**
1. Empty string returns 0
2. One number returns its value
3. Two numbers separated by comma return the sum
4. Multiple numbers return the sum
5. Newline works as a delimiter

### Step 1: 🔴 RED - Empty String

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

### Step 2: 🟢 GREEN - Simplest Solution

```csharp
public class StringCalculator
{
    public int Add(string numbers)
    {
        return 0;
    }
}
```

✅ Test passes!

### Step 3: 🔴 RED - Single Number

```csharp
[Fact]
public void Add_SingleNumber_ReturnsNumber()
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add("5");
    Assert.Equal(5, result);
}
```

### Step 4: 🟢 GREEN - Parse Number

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

✅ Both tests pass!

### Step 5: 🔴 RED - Two Numbers

```csharp
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add("1,2");
    Assert.Equal(3, result);
}
```

❌ Fails (FormatException)

### Step 6: 🟢 GREEN - Split and Sum

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

✅ All tests pass!

### Step 7: 🔴 RED - Multiple Numbers

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

❌ Fails

### Step 8: 🟢 GREEN - Loop Through All

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

✅ All tests pass!

### Step 9: 🔵 REFACTOR - LINQ

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

✅ Tests pass and code is cleaner!

### Step 10: 🔴 RED - Newline Delimiter

```csharp
[Fact]
public void Add_NewlineDelimiter_ReturnsSum()
{
    StringCalculator calculator = new StringCalculator();
    int result = calculator.Add("1\n2,3");
    Assert.Equal(6, result);
}
```

### Step 11: 🟢 GREEN - Multiple Delimiters

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

✅ Done!

---

## Example 3: Banking System

Build a simple banking system with TDD.

### Step 1: 🔴 RED - New Account

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

### Step 2: 🟢 GREEN - Implement

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

✅ Test passes!

### Step 3: 🔴 RED - Deposit

```csharp
[Fact]
public void Deposit_100_IncreasesBalance()
{
    BankAccount account = new BankAccount();
    account.Deposit(100);
    Assert.Equal(100, account.GetBalance());
}
```

### Step 4: 🟢 GREEN - Implement Deposit

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

✅ Tests pass!

### Step 5: 🔴 RED - Withdrawal

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

### Step 6: 🟢 GREEN - Implement Withdraw

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

✅ Tests pass!

### Step 7: 🔴 RED - Can't Withdraw More Than Balance

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

### Step 8: 🟢 GREEN - Add Validation

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

✅ Tests pass!

### Step 9: 🔴 RED - Negative Deposit

```csharp
[Fact]
public void Deposit_NegativeAmount_ThrowsException()
{
    BankAccount account = new BankAccount();
    Assert.Throws<ArgumentException>(() => 
        account.Deposit(-100));
}
```

### Step 10: 🟢 GREEN - Validate Deposits

```csharp
public void Deposit(decimal amount)
{
    if (amount <= 0)
        throw new ArgumentException("Amount must be positive");
        
    _balance += amount;
}
```

### Step 11: 🔵 REFACTOR - Improve Structure

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

✅ Tests pass and code is cleaner!

---

## Example 4: Password Validator

Build a password validator with TDD.

**Requirements:**
- At least 8 characters
- Contains uppercase letters
- Contains lowercase letters
- Contains digits
- Contains special characters

### Step 1: 🔴 RED - Too Short

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

### Step 2: 🟢 GREEN - Simple Implementation

```csharp
public class PasswordValidator
{
    public bool Validate(string password)
    {
        return password.Length >= 8;
    }
}
```

✅ Test passes!

### Step 3: 🔴 RED - Valid Password

```csharp
[Fact]
public void Validate_ValidPassword_ReturnsTrue()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("Valid123!");
    Assert.True(result);
}
```

✅ Test passes immediately (8 characters)!

### Step 4: 🔴 RED - Must Contain Uppercase

```csharp
[Fact]
public void Validate_NoUppercase_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("lowercase123!");
    Assert.False(result);
}
```

❌ Test fails

### Step 5: 🟢 GREEN - Check Uppercase

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

✅ Tests pass!

### Step 6: 🔴 RED - Must Contain Lowercase

```csharp
[Fact]
public void Validate_NoLowercase_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("UPPERCASE123!");
    Assert.False(result);
}
```

### Step 7: 🟢 GREEN - Check Lowercase

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

✅ Tests pass!

### Step 8: 🔴 RED - Must Contain Digits

```csharp
[Fact]
public void Validate_NoDigits_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("Password!");
    Assert.False(result);
}
```

### Step 9: 🟢 GREEN - Check Digits

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

✅ Tests pass!

### Step 10: 🔴 RED - Must Contain Special Characters

```csharp
[Fact]
public void Validate_NoSpecialChars_ReturnsFalse()
{
    PasswordValidator validator = new PasswordValidator();
    bool result = validator.Validate("Password123");
    Assert.False(result);
}
```

### Step 11: 🟢 GREEN - Check Special Characters

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

✅ Tests pass!

### Step 12: 🔵 REFACTOR - Improve Structure

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

✅ Tests pass and code is much more readable!

### Step 13: 🔵 REFACTOR - Parameterize Tests

```csharp
public class PasswordValidatorTests
{
    [Theory]
    [InlineData("short", false)]          // Too short
    [InlineData("lowercase123!", false)]  // No uppercase
    [InlineData("UPPERCASE123!", false)]  // No lowercase
    [InlineData("Password!", false)]      // No digits
    [InlineData("Password123", false)]    // No special chars
    [InlineData("Valid123!", true)]       // Valid
    [InlineData("MyP@ssw0rd", true)]      // Valid
    public void Validate_VariousPasswords_ReturnsExpected(string password, bool expected)
    {
        PasswordValidator validator = new PasswordValidator();
        bool result = validator.Validate(password);
        Assert.Equal(expected, result);
    }
}
```

✅ Done!

---

## Example 5: Shopping Cart

Build a shopping cart with TDD.

### Step 1: 🔴 RED - Empty Cart

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

### Step 2: 🟢 GREEN - Implement

```csharp
public class ShoppingCart
{
    public int ItemCount => 0;
}
```

✅ Test passes!

### Step 3: 🔴 RED - Add Item

```csharp
[Fact]
public void AddItem_SingleItem_IncreasesCount()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 1.5m, 1));
    Assert.Equal(1, cart.ItemCount);
}
```

### Step 4: 🟢 GREEN - Implement AddItem

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

✅ Tests pass!

### Step 5: 🔴 RED - Calculate Total

```csharp
[Fact]
public void GetTotal_SingleItem_ReturnsPrice()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 1.5m, 2));
    Assert.Equal(3.0m, cart.GetTotal());
}
```

### Step 6: 🟢 GREEN - Implement GetTotal

```csharp
public decimal GetTotal()
{
    return _items.Sum(item => item.Price * item.Quantity);
}
```

✅ Tests pass!

### Step 7: 🔴 RED - Multiple Items

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

✅ Test passes immediately!

### Step 8: 🔴 RED - Remove Item

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

### Step 9: 🟢 GREEN - Implement RemoveItem

```csharp
public void RemoveItem(CartItem item)
{
    _items.Remove(item);
}
```

✅ Tests pass!

### Step 10: 🔴 RED - Discount

```csharp
[Fact]
public void ApplyDiscount_10Percent_ReducesTotal()
{
    ShoppingCart cart = new ShoppingCart();
    cart.AddItem(new CartItem("Apple", 10m, 1));
    cart.ApplyDiscount(0.10m); // 10% discount
    Assert.Equal(9m, cart.GetTotal());
}
```

### Step 11: 🟢 GREEN - Implement Discount

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

✅ Tests pass!

### Step 12: 🔵 REFACTOR - Improve Structure

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

✅ Tests pass, code is better!

---

## Summary

In these examples we saw:

### TDD process in practice:
1. 🔴 **RED** - Write a failing test
2. 🟢 **GREEN** - Write the simplest code
3. 🔵 **REFACTOR** - Improve the code
4. **Repeat**

### Learnings:
- Start simple
- Small steps (Baby Steps)
- One test at a time
- Tests guide design
- Refactor regularly
- Tests are a safety net

### Tips:
- Don't design too much up front
- Let tests guide design
- Don't fear simple solutions
- Refactor when tests are green
- Keep tests fast
- Test edge cases

### Practice more:
- [Code Katas](http://codekata.com/)
- [Cyber Dojo](https://cyber-dojo.org/)
- [Codewars](https://www.codewars.com/)

Back to theory: [TDD.md](TDD.md)

