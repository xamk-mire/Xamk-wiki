# Test-Driven Development (TDD)

## Table of Contents

1. [Introduction](#introduction)
2. [What is TDD?](#what-is-tdd)
3. [Benefits of TDD](#benefits-of-tdd)
4. [Red-Green-Refactor Cycle](#red-green-refactor-cycle)
5. [Rules of TDD](#rules-of-tdd)
6. [TDD in Practice](#tdd-in-practice)
7. [TDD vs. Traditional Development](#tdd-vs-traditional-development)
8. [Challenges and Solutions](#challenges-and-solutions)
9. [Best Practices](#best-practices)
10. [Examples](#examples)

---

## Introduction

Test-Driven Development (TDD) is a software development approach where tests are written **before** the actual code. TDD is not just a testing method, but a **design tool** that guides code structure and architecture.

### Material Structure

- **This file**: TDD theory and practices
- **[TDD-Examples.md](TDD-Examples.md)**: Step-by-step examples of TDD
- **[Unit-Testing.md](Unit-Testing.md)**: Testing fundamentals
- **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)**: Testing examples

### Useful Links

- [Kent Beck: Test-Driven Development](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Martin Fowler: TDD](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Uncle Bob: The Three Rules of TDD](http://butunclebob.com/ArticleS.UncleBob.TheThreeRulesOfTdd)

---

## What is TDD?

**Test-Driven Development (TDD)** is a development method where:

1. ✍️ **Write the test first** - The test fails because the code doesn't exist yet
2. ✅ **Write the minimum code** - Just enough to make the test pass
3. 🔄 **Refactor the code** - Improve code quality with tests as safety net

### TDD is NOT:

❌ **Just testing** - It's a design tool  
❌ **Writing tests afterward** - Tests come first  
❌ **Writing tests alongside code** - Tests come **before**

### TDD is:

✅ **A design method** - Tests force you to think about interfaces  
✅ **Documentation** - Tests show how code is used  
✅ **Quality assurance** - Tests verify behavior  
✅ **Safety net** - Tests give confidence to refactor

---

## Benefits of TDD

### 1. Better Design

When you write the test first, you have to think about:

- What does the class/method do?
- How is it called?
- What does it return?
- What are its dependencies?

**This leads to:**

- Clearer interfaces
- Fewer dependencies
- Adherence to SOLID principles
- More testable code

### 2. Fewer Bugs

```
Traditional: Code → Tests → Bugs found later
TDD: Tests → Code → Bugs found immediately
```

- Errors are found immediately
- Regressions are prevented
- Safety net for refactoring

### 3. Confidence in Code

- You dare to make changes
- Refactoring is safe
- You can remove old code confidently

### 4. Living Documentation

Tests are the best documentation:

- Show how code is used
- Always up to date
- Executable

### 5. Faster Development in the Long Run

Even if TDD feels slow at first:

- Less debugging
- Fewer regressions
- Safe refactoring
- Better code quality

**Development time:**

```
Traditional: ████████████░░░░░░ (12 weeks)
              ^coding     ^debugging

TDD:        ██████████████ (14 weeks)
              ^tests+code (less debugging)
```

Even if TDD takes 15-20% more time initially, you save:

- 40-80% fewer bugs in production
- 50% less time debugging
- Fast and safe refactoring

---

## Red-Green-Refactor Cycle

TDD is based on a three-phase cycle:

### 🔴 RED - Write a Failing Test

**What to do:**

1. Write a test for new functionality
2. Run the test - it MUST fail
3. Make sure the test fails for the right reason

**Why:**

- Ensures the test actually tests something
- If the test passes without code, the test is wrong

**Example:**

```csharp
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    // Arrange
    Calculator calculator = new Calculator(); // Doesn't exist yet!

    // Act
    int result = calculator.Add(2, 3); // Method doesn't exist yet!

    // Assert
    Assert.Equal(5, result);
}
```

### 🟢 GREEN - Write the Minimum Code

**What to do:**

1. Write the simplest possible code
2. Don't think about optimization or design
3. Run the test - it should pass

**Why:**

- Fast feedback
- Focus on one thing at a time
- Don't over-engineer

**Example:**

```csharp
public class Calculator
{
    public int Add(int a, int b)
    {
        return 5; // "Fake it 'til you make it"
    }
}
```

This feels silly, but the next test forces improvement:

```csharp
[Theory]
[InlineData(2, 3, 5)]
[InlineData(1, 1, 2)] // This won't pass!
public void Add_VariousNumbers_ReturnsSum(int a, int b, int expected)
{
    Calculator calculator = new Calculator();
    int result = calculator.Add(a, b);
    Assert.Equal(expected, result);
}
```

Now you must write the real implementation:

```csharp
public int Add(int a, int b)
{
    return a + b;
}
```

### 🔵 REFACTOR - Improve the Code

**What to do:**

1. Improve code quality
2. Remove duplication (DRY)
3. Improve readability
4. Run tests after each change

**Why:**

- Code stays clean
- Tests ensure nothing breaks
- Technical debt doesn't grow

**Example:**

```csharp
// Before refactoring
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

// After refactoring
public class CalculatorTests
{
    private readonly Calculator _calculator;

    public CalculatorTests()
    {
        _calculator = new Calculator(); // Once!
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

### Cycle in a Diagram:

```
    🔴 RED
     ↓
Write
failing     ←───────┐
test                │
     ↓              │
    🟢 GREEN        │
     ↓              │
Write           Tests
minimum         pass?
code                │
     ↓              │
Tests          Continue
pass?          to next
     │           feature
     ↓              │
    🔵 REFACTOR     │
     ↓              │
Improve code    ────┘
(tests pass)
```

---

## Rules of TDD

### Uncle Bob's three rules:

Robert C. Martin (Uncle Bob) defined three simple rules for TDD:

#### 1. Don't write production code before you have a failing test

```csharp
// ❌ WRONG
public class Calculator
{
    public int Add(int a, int b)  // No test!
    {
        return a + b;
    }
}

// ✅ RIGHT
// 1. Write the test first
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    Calculator calc = new Calculator();
    Assert.Equal(5, calc.Add(2, 3));
}

// 2. Then implement
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
}
```

#### 2. Don't write more test than needed to make one failure

Compilation failure = failure

```csharp
// ❌ WRONG - too much at once
[Fact]
public void ComplexTest()
{
    Calculator calc = new Calculator();
    Assert.Equal(5, calc.Add(2, 3));
    Assert.Equal(10, calc.Multiply(2, 5));
    Assert.Equal(1, calc.Subtract(3, 2));
    Assert.Equal(2, calc.Divide(4, 2));
}

// ✅ RIGHT - one thing at a time
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    Calculator calc = new Calculator();
    Assert.Equal(5, calc.Add(2, 3));
}
// Next test only when this works!
```

#### 3. Don't write more production code than needed to pass one test

```csharp
// ❌ WRONG - too much at once
[Fact]
public void Add_ReturnsSum()
{
    Assert.Equal(5, new Calculator().Add(2, 3));
}

public class Calculator
{
    public int Add(int a, int b) => a + b;
    public int Subtract(int a, int b) => a - b;  // No test!
    public int Multiply(int a, int b) => a * b;  // No test!
}

// ✅ RIGHT - only what's needed by the test
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

Repeat forever, in small steps.

---

## TDD in Practice

### 1. Start Simple

**Don't try to build everything at once:**

```
❌ WRONG:
Test: Calculator that calculates +, -, *, /, %, ^, sqrt, sin, cos...

✅ RIGHT:
Test 1: Calculator.Add(2, 3) = 5
Test 2: Calculator.Add(0, 0) = 0
Test 3: Calculator.Add(-1, 1) = 0
...
```

### 2. Baby Steps - Small Steps

Each step is:

1. Write one small test
2. Run the test (RED)
3. Write the minimum code (GREEN)
4. Refactor (REFACTOR)
5. **Repeat**

**Example progression:**

```csharp
// Step 1: Base case
[Fact]
public void Add_PositiveNumbers_ReturnsSum()
{
    Assert.Equal(5, new Calculator().Add(2, 3));
}

// Step 2: Zeros
[Fact]
public void Add_WithZero_ReturnsOtherNumber()
{
    Assert.Equal(5, new Calculator().Add(5, 0));
}

// Step 3: Negatives
[Fact]
public void Add_NegativeNumbers_ReturnsSum()
{
    Assert.Equal(-5, new Calculator().Add(-2, -3));
}

// Step 4: Large numbers
[Theory]
[InlineData(1000000, 2000000, 3000000)]
public void Add_LargeNumbers_ReturnsSum(int a, int b, int expected)
{
    Assert.Equal(expected, new Calculator().Add(a, b));
}
```

### 3. YAGNI - You Aren't Gonna Need It

**Don't do anything the tests don't require:**

```csharp
// ❌ WRONG
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

// ✅ RIGHT (if tests only require addition)
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
}
```

### 4. Triangulation

When you are not sure about the implementation, add more tests:

```csharp
// Test 1
[Fact]
public void Add_2And3_Returns5()
{
    Assert.Equal(5, new Calculator().Add(2, 3));
}

// Simplest implementation:
public int Add(int a, int b) => 5;

// Test 2 reveals the problem
[Fact]
public void Add_1And1_Returns2()
{
    Assert.Equal(2, new Calculator().Add(1, 1));
}

// Now the correct implementation:
public int Add(int a, int b) => a + b;
```

### 5. Test List

Keep a list of tests you need to write:

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

Do one at a time, check off when done.

---

## TDD vs. Traditional Development

### Traditional way (Test-Last):

```
1. Design    ───┐
2. Write code   │  Development
3. Test         │
4. Debug       ─┘
5. Repeat
```

**Problems:**

- Tests are written "by obligation"
- Untested code easily remains
- Tests do not guide design
- Hard to test code afterward
- Test coverage remains low

### TDD way (Test-First):

```
1. Write test (RED)    ─┐
2. Write code (GREEN)   │ Repeats
3. Refactor (REFACTOR) ─┘
```

**Benefits:**

- 100% test coverage automatically
- Testable code emerges naturally
- Tests guide design
- Fewer bugs
- Bold refactoring

### Comparison Table:

| Feature                            | Traditional      | TDD               |
| ---------------------------------- | ---------------- | ----------------- |
| Test coverage                      | 40-60%           | 90-100%           |
| Bug count                          | Average          | 40-80% fewer      |
| Design quality                     | Varies           | Higher            |
| Refactoring                        | Scary            | Safe              |
| Documentation                      | Becomes outdated | Always up to date |
| Development speed (initially)      | Faster           | Slower            |
| Development speed (after 6 months) | Slows down       | Stays good        |

---

## Challenges and Solutions

### Challenge 1: "TDD is slow"

**Problem:** TDD feels like it slows development.

**Solution:**

- TDD is an investment in the future
- You save time debugging
- Fewer regressions
- Fast feedback loop

**Comparison:**

```
Week 1: Traditional fast, TDD slow
Week 4: Traditional slows down, TDD steady
Week 12: Traditional very slow (bugs), TDD steady
```

### Challenge 2: "I don't know what to test"

**Problem:** I can't write a test before I know the solution.

**Solution:**

- Start from requirements ("what should this do?")
- Write tests from the user's perspective
- Don't think about implementation

**Example:**

```csharp
// Think: "User wants to add two numbers"
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    // What does the user do?
    Calculator calc = new Calculator();

    // What does the user expect?
    int result = calc.Add(2, 3);

    // What is the correct answer?
    Assert.Equal(5, result);
}
```

### Challenge 3: "Tests break when I refactor"

**Problem:** Refactoring breaks tests.

**Solution:**

- Test the public interface, not implementation
- Don't test private methods
- Test behavior, not structure

**Example:**

```csharp
// ❌ Bad - tests implementation
[Fact]
public void InternalMethod_DoesX()
{
    Assert.Equal(expectedInternalState, obj.InternalState);
}

// ✅ Good - tests public interface
[Fact]
public void Process_ValidInput_ReturnsExpectedOutput()
{
    string result = processor.Process("input");
    Assert.Equal("expected", result);
}
```

### Challenge 4: "Too many tests"

**Problem:** There are too many tests.

**Solution:**

- Use `[Theory]` and `[InlineData]`
- Remove duplicate tests
- Focus on edge cases

**Example:**

```csharp
// ❌ Too many tests
[Fact]
public void Add_2And3_Returns5() { ... }
[Fact]
public void Add_1And1_Returns2() { ... }
[Fact]
public void Add_5And7_Returns12() { ... }

// ✅ One test, many cases
[Theory]
[InlineData(2, 3, 5)]
[InlineData(1, 1, 2)]
[InlineData(5, 7, 12)]
public void Add_VariousInputs_ReturnsSum(int a, int b, int expected) { ... }
```

### Challenge 5: "Legacy code is not testable"

**Problem:** Old code is hard to test.

**Solution:**

- Start with new features
- Refactor legacy code gradually
- Use "Characterization Tests"
- Read: "Working Effectively with Legacy Code" (Michael Feathers)

---

## Best Practices

### 1. Keep tests fast

```
⚡ Target: < 1ms per test
🚀 Acceptable: < 10ms per test
⚠️  Slow: > 100ms per test
❌ Too slow: > 1s per test
```

**Ways:**

- Use mocks (no real database)
- Don't use Thread.Sleep()
- Don't make network calls
- Don't use the file system

### 2. One assert per test (usually)

```csharp
// ❌ Bad
[Fact]
public void ComplexTest()
{
    Assert.Equal(5, result.Count);
    Assert.True(result.IsValid);
    Assert.NotNull(result.Data);
}

// ✅ Good
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

### 3. Use descriptive names

```csharp
// ❌ Bad
[Fact]
public void Test1() { ... }

// ⚠️  OK
[Fact]
public void AddTest() { ... }

// ✅ Good
[Fact]
public void Add_TwoPositiveNumbers_ReturnsSum() { ... }

// ✅ Excellent
[Fact]
public void Add_WhenBothNumbersArePositive_ShouldReturnTheirSum() { ... }
```

### 4. Organize tests with the AAA pattern

```csharp
[Fact]
public void Add_TwoNumbers_ReturnsSum()
{
    // Arrange - Prepare
    Calculator calculator = new Calculator();
    int a = 2;
    int b = 3;

    // Act - Act
    int result = calculator.Add(a, b);

    // Assert - Assert
    Assert.Equal(5, result);
}
```

### 5. Test edge cases

```csharp
[Theory]
[InlineData(0, 0, 0)]           // Zeros
[InlineData(-1, -1, -2)]        // Negatives
[InlineData(int.MaxValue, 0)]   // Max value
[InlineData(int.MinValue, 0)]   // Min value
public void Add_EdgeCases_HandledCorrectly(int a, int b, int expected)
{
    Assert.Equal(expected, new Calculator().Add(a, b));
}
```

### 6. Don't test the framework

```csharp
// ❌ Unnecessary - tests List behavior
[Fact]
public void List_Add_IncreasesCount()
{
    var list = new List<int>();
    list.Add(5);
    Assert.Equal(1, list.Count);
}

// ✅ Test your own logic
[Fact]
public void AddItem_ValidItem_IncreasesCount()
{
    var manager = new ItemManager();
    manager.AddItem(new Item());
    Assert.Equal(1, manager.Count);
}
```

### 7. Keep tests maintainable

- DRY (Don't Repeat Yourself) also applies to tests
- Use helper methods
- Use test fixtures
- Refactor tests regularly

```csharp
// ❌ Repeated code
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

// ✅ Helper method
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

## Examples

See detailed, step-by-step examples of TDD:

### [TDD-Examples.md](TDD-Examples.md)

Examples include:

1. Simple example: FizzBuzz
2. String Calculator Kata
3. Banking System
4. Shopping Cart
5. Password Validator

Each example shows the TDD process with the Red-Green-Refactor cycle.

---

## Summary

### TDD in a nutshell:

1. 🔴 **RED** - Write a failing test
2. 🟢 **GREEN** - Write the minimum code
3. 🔵 **REFACTOR** - Improve the code
4. **Repeat** endlessly

### Benefits of TDD:

✅ Better design  
✅ Fewer bugs  
✅ Confidence in code  
✅ Living documentation  
✅ Safe refactoring  
✅ Faster development in the long run

### Remember:

- Start with small steps (Baby Steps)
- Follow the three rules
- Use the AAA pattern (Arrange-Act-Assert)
- Keep tests fast
- Test the public interface
- YAGNI - Don't do more than tests require

### Next:

1. Practice with examples: **[TDD-Examples.md](TDD-Examples.md)**
2. Try Code Katas (FizzBuzz, String Calculator, etc.)
3. Use TDD in your next project
4. Read more: [Unit-Testing.md](Unit-Testing.md)

---

**"TDD is like driving: at first it feels difficult, but soon it becomes automatic and you can't imagine doing it without it."**
