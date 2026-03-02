# Unit Testing

## Table of Contents

1. [Introduction](#introduction)
2. [What is Unit Testing?](#what-is-unit-testing)
3. [Why is Unit Testing Important?](#why-is-unit-testing-important)
4. [xUnit - Testing Framework](#xunit---testing-framework)
5. [Test Anatomy - AAA Pattern](#test-anatomy---aaa-pattern)
6. [xUnit Attributes](#xunit-attributes)
7. [Assert Methods](#assert-methods)
8. [Mocking](#mocking)
9. [Test Organization](#test-organization)
10. [Best Practices](#best-practices)
11. [Examples](#examples)

---

## Introduction

Unit testing is a crucial part of software development that ensures code quality and functionality. This material covers unit testing in C# using the xUnit framework.

### Material Structure

- **This file**: Theory and concepts
- **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)**: Comprehensive code examples
- **Exercises**: Practical exercises can be found in course exercise repositories

### Useful Links

- [Official Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-with-dotnet-test)
- [xUnit documentation](https://xunit.net/)
- [How to run tests in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/test/run-unit-tests-with-test-explorer?view=vs-2022)

---

## What is Unit Testing?

**Unit Testing** is an automated test that tests **a small part of code** in isolation from the rest of the system. Typically, a unit test tests:
- One method
- One class
- One functionality

### Unit Test Characteristics

✅ **Fast** - Execution takes milliseconds  
✅ **Isolated** - Does not depend on external resources (database, network)  
✅ **Repeatable** - Always produces the same result with the same inputs  
✅ **Independent** - Does not depend on other tests  
✅ **Clear** - Tests one thing at a time

### What Unit Testing is NOT

❌ **Integration Test** - Tests multiple components together

Integration tests test how different parts of the system work together. For example, testing that the application can actually save data to a database, not mocked. These tests are slower and more complex than unit tests.

**Example:** Testing the interaction between UserService and a real database.

❌ **End-to-End Test (E2E)** - Tests the entire system

E2E tests test the entire application's functionality from the user's perspective, from start to finish. They simulate real user actions (e.g., in a browser), including the user interface, backend, database, and all intermediate components.

**Example:** User logs in, creates a product, adds it to the shopping cart, and pays for the order.

❌ **Manual Test** - Tested manually

In manual testing, a person performs tests manually, not automatically. This is slow, error-prone, and difficult to repeat systematically.

---

## Why is Unit Testing Important?

### 1. Ensures Code Functionality

Unit tests ensure that your code does what it's supposed to do. When you write a test before or immediately after the code, you are forced to think about what the code should do.

### 2. Detects Errors Early

Errors are found immediately in the development phase, not in production. The earlier an error is found, the cheaper it is to fix.

**Error Fix Cost:**
- In development phase: 1x
- In testing phase: 10x
- In production: 100x

### 3. Facilitates Refactoring

When you have comprehensive tests, you can confidently make changes to the code. If you break something, the tests will tell you immediately.

```
Without tests: You're afraid to change code → Code becomes legacy code
With tests: Changes are safe → Code stays clean
```

### 4. Documents Code

Good tests tell you how to use the code. They are "living documentation" that stays up to date.

### 5. Improves Architecture

Testable code is usually better designed:
- Modular (small, independent parts)
- Dependencies are injected
- Clear interfaces
- Single Responsibility Principle

### 6. Saves Time in the Long Run

Although writing tests takes time initially, it saves time:
- Fewer bugs
- Fast debugging
- Safe refactoring
- Fewer regressions

---

## xUnit - Testing Framework

**xUnit** is a modern, open-source testing framework for .NET applications. It is the most popular testing framework in the .NET Core community.

### Why xUnit?

✅ **Modern** - Designed for the .NET Core era  
✅ **Popular** - Widely used, good support  
✅ **Simple** - Easy to learn and use  
✅ **Flexible** - Supports different testing patterns  
✅ **Performant** - Fast test execution

### Other Alternatives

- **NUnit** - Older, also popular
- **MSTest** - Microsoft's own framework
- **xUnit** - Recommended for new projects

### xUnit Installation

**NuGet Packages:**
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

## Test Anatomy - AAA Pattern

AAA (Arrange-Act-Assert) is a common pattern in unit testing. It divides the test into three clear parts.

### 1. Arrange (Set Up)

**Prepare the test:**
- Create necessary objects
- Set initial values
- Configure mock objects

```csharp
// Arrange
Calculator calculator = new Calculator();
int a = 5;
int b = 3;
int expected = 8;
```

### 2. Act (Execute)

**Execute the operation being tested:**
- Call the method being tested
- Usually just one line
- Store the result in a variable

```csharp
// Act
int result = calculator.Add(a, b);
```

### 3. Assert (Verify)

**Check the result:**
- Compare the result to the expectation
- Use Assert methods
- If Assert fails, the test fails

```csharp
// Assert
Assert.Equal(expected, result);
```

### Complete Example

```csharp
[Fact]
public void Add_ShouldReturnSum_WhenGivenTwoNumbers()
{
    // Arrange - Prepare
    Calculator calculator = new Calculator();
    int a = 5;
    int b = 3;
    int expected = 8;

    // Act - Execute
    int result = calculator.Add(a, b);

    // Assert - Verify
    Assert.Equal(expected, result);
}
```

---

## xUnit Attributes

xUnit uses attributes to define and configure tests.

### [Fact] - Single Test

`[Fact]` is the basic attribute for a single test. It does not take parameters.

**Usage:**
```csharp
[Fact]
public void TestMethodName()
{
    // Test
}
```

**Examples:**
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

### [Theory] and [InlineData] - Parameterized Tests

`[Theory]` allows running the same test with multiple different inputs.

**Usage:**
```csharp
[Theory]
[InlineData(param1, param2, expected)]
[InlineData(param1, param2, expected)]
public void TestMethodName(Type param1, Type param2, Type expected)
{
    // Test
}
```

**Example:**
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

**Benefits:**
- Less repetition
- Easy to add new test scenarios
- Clear and compact

### [MemberData] - Complex Test Data

When test data is too complex for `InlineData`, use `MemberData`.

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
    // Test
}
```

### [Skip] - Skip Test

Sometimes you want to temporarily skip a test.

```csharp
[Fact(Skip = "Not yet implemented")]
public void FutureTest()
{
    // ...
}
```

---

## Assert Methods

xUnit provides many `Assert` methods for checking results.

### Basic Checks

```csharp
// Equality
Assert.Equal(expected, actual);
Assert.NotEqual(expected, actual);

// True/False
Assert.True(condition);
Assert.False(condition);

// Null checks
Assert.Null(object);
Assert.NotNull(object);

// Same object
Assert.Same(expected, actual);
Assert.NotSame(expected, actual);
```

### Numeric Checks

```csharp
// Range
Assert.InRange(actual, low, high);
Assert.NotInRange(actual, low, high);

// Decimal comparison
Assert.Equal(expected, actual, precision: 2);
```

### String Checks

```csharp
// Content
Assert.Contains("sub", "substring");
Assert.DoesNotContain("x", "string");

// Start/End
Assert.StartsWith("Hello", "Hello world");
Assert.EndsWith("world", "Hello world");

// Empty
Assert.Empty(collection);
Assert.NotEmpty(collection);

// Regex
Assert.Matches(@"\d+", "123");
```

### Collections

```csharp
// Single element
Assert.Single(collection);

// Content
Assert.Contains(item, collection);
Assert.DoesNotContain(item, collection);

// All elements satisfy condition
Assert.All(collection, item => Assert.True(item > 0));

// Empty
Assert.Empty(collection);
Assert.NotEmpty(collection);
```

### Exceptions

```csharp
// Expect exception
Assert.Throws<ArgumentException>(() => 
{
    method.Call();
});

// More detailed exception test
ArgumentException exception = Assert.Throws<ArgumentException>(() => 
{
    method.Call();
});
Assert.Equal("Parameter cannot be null", exception.Message);

// Async exceptions
await Assert.ThrowsAsync<InvalidOperationException>(async () => 
{
    await method.CallAsync();
});
```

### Type Checks

```csharp
// Type
Assert.IsType<MyClass>(object);
Assert.IsNotType<OtherClass>(object);

// Inherited type
Assert.IsAssignableFrom<BaseClass>(object);
```

---

## Mocking

### What is Mocking?

**Mocking** is a technique where "fake objects" (mocks) are created to replace real dependencies in tests. This allows you to test code in isolation from external dependencies.

### Why Mock?

#### 1. Isolation

```
Without mocking:
YourClass → RealDatabase → Network → Database Server
  ↓
Test depends on all of this

With mocking:
YourClass → MockDatabase
  ↓
Test depends only on YourClass
```

#### 2. Speed

- Real database call: 100-1000ms
- Mock call: <1ms
- Test suite with 1000 tests: hour → second

#### 3. Control

You can define exactly what the mock returns:
- Normal result
- Error situation
- Null value
- Exception

#### 4. Testability

You can test situations that would be difficult or impossible with real objects:
- Network error
- Database full
- Time-related problems

### Moq Library

**Moq** is the most popular mocking library for C#.

**Installation:**
```bash
dotnet add package Moq
```

**Basic Example:**
```csharp
using Moq;

// 1. Create mock object
Mock<IEmailService> mock = new Mock<IEmailService>();

// 2. Define what the mock returns
mock.Setup(x => x.SendEmail(It.IsAny<string>()))
    .Returns(true);

// 3. Use the mock
UserService service = new UserService(mock.Object);

// 4. Verify that the method was called
mock.Verify(x => x.SendEmail("test@example.com"), Times.Once);
```

### When to Mock?

✅ **Mock:**
- Databases
- External APIs
- File system
- Email/SMS
- Time (DateTime.Now)
- Randomness (Random)

❌ **Don't Mock:**
- Simple data classes
- Value Objects
- Your own simple classes
- .NET base classes (String, List, etc.)

### Interfaces and Mocking

Mocking works best with **interfaces**:

```csharp
// ❌ Hard to mock - concrete class
public class UserService
{
    private EmailService _emailService; // Concrete class
}

// ✅ Easy to mock - interface
public class UserService
{
    private IEmailService _emailService; // Interface
}
```

**Benefits:**
- Mock can be created automatically
- Dependency can be easily swapped
- Better architecture (Dependency Inversion)

---

## Test Organization

### Naming Conventions

#### Test Naming

Use a descriptive name that tells:
1. What is being tested
2. With what input
3. What is expected

**Formula:**
```
MethodName_Scenario_ExpectedBehavior
```

**Examples:**
```csharp
Add_PositiveNumbers_ReturnsSum
Add_NegativeNumbers_ReturnsSum
Add_ZeroAndNumber_ReturnsNumber
Divide_ByZero_ThrowsException
GetUser_ValidId_ReturnsUser
GetUser_InvalidId_ReturnsNull
```

#### Project Naming

```
ProjectName → ProjectName.Tests
MyApp → MyApp.Tests
MyApp.Core → MyApp.Core.Tests
```

### Organizing Tests into Folders

```
MyApp.Tests/
├── Unit/              # Unit tests
│   ├── Services/
│   ├── Controllers/
│   └── Helpers/
├── Integration/       # Integration tests
└── Fixtures/          # Shared test data
```

### Test Class per Class

Create one test class for each class being tested:

```
Calculator.cs → CalculatorTests.cs
UserService.cs → UserServiceTests.cs
```

---

## Best Practices

### 1. One Assert per Test (usually)

**When to use:** Usually always. One test tests one thing.

**Why:** When a test fails, you immediately know what went wrong. If a test has multiple Asserts, the first failure stops the test and other checks are not executed.

**Exception:** You can use multiple Asserts when testing multiple properties of the same object that belong together (e.g., coordinates x and y).

```csharp
// ❌ Bad - multiple asserts for different things
[Fact]
public void BadTest()
{
    Assert.Equal(5, result.Count);
    Assert.True(result.IsValid);
    Assert.Equal("OK", result.Status);
}

// ✅ Good - one thing at a time
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

### 2. Tests are Independent

**When to use:** Always. Each test is completely independent of others.

**Why:** Tests can be run in any order and in parallel. If tests depend on each other, one failed test can break all others.

```csharp
// ❌ Bad - depends on another test
private static int sharedCounter = 0;

[Fact]
public void Test1() 
{ 
    sharedCounter++; 
}

[Fact]
public void Test2() 
{ 
    Assert.Equal(1, sharedCounter); // Fails if Test1 doesn't run first
}

// ✅ Good - independent
[Fact]
public void Test2() 
{ 
    int counter = 0;
    counter++;
    Assert.Equal(1, counter);
}
```

### 3. Test Error Cases Too

**When to use:** Always when your method can fail or throw an exception.

**Why:** Most bugs occur in error situations. Testing only "happy path" cases is not enough.

```csharp
// Test normal case
[Fact]
public void Divide_ValidNumbers_ReturnsQuotient()
{
    // ...
}

// Test error case
[Fact]
public void Divide_ByZero_ThrowsException()
{
    Assert.Throws<DivideByZeroException>(() => 
    {
        calculator.Divide(10, 0);
    });
}

// Test edge cases
[Fact]
public void Divide_ZeroDividedByNumber_ReturnsZero()
{
    // ...
}
```

### 4. Use Descriptive Variable Names

**When to use:** Always.

**Why:** Tests are documentation. They must be easy to read and understand.

```csharp
// ❌ Bad
[Fact]
public void Test1()
{
    Thing x = new Thing();
    int y = x.Do(5);
    Assert.Equal(10, y);
}

// ✅ Good
[Fact]
public void Double_ShouldReturnTwiceTheInput()
{
    Calculator calculator = new Calculator();
    int result = calculator.Double(5);
    Assert.Equal(10, result);
}
```

### 5. Don't Test .NET Base Features

**When to use:** Never test framework or library functionality.

**Why:** Microsoft has already tested .NET base classes. Focus on your own logic.

```csharp
// ❌ Unnecessary - tests List functionality
[Fact]
public void List_Add_IncreasesCount()
{
    List<int> list = new List<int>();
    list.Add(5);
    Assert.Equal(1, list.Count);
}

// ✅ Good - tests your own logic
[Fact]
public void AddUser_ShouldIncreaseUserCount()
{
    UserService userService = new UserService();
    userService.AddUser(new User());
    Assert.Equal(1, userService.GetUserCount());
}
```

### 6. FIRST Principles

**When to use:** Keep these principles in mind whenever you write tests.

Good tests are:

- **F**ast - Milliseconds, not seconds
- **I**ndependent - Don't depend on other tests
- **R**epeatable - Same result always
- **S**elf-validating - Pass/Fail, no manual checking
- **T**imely - Write before or immediately after code

---

## Examples

See comprehensive code examples in the file:

### [Unit-Testing-Examples.md](Unit-Testing-Examples.md)

Examples include:
1. Basic Assert examples
2. Theory and InlineData
3. Mocking with Moq
4. Async tests
5. Exception tests
6. Collection tests
7. Comprehensive example: UserService

---

## Summary

### Benefits of Unit Testing:
✅ Ensures code functionality  
✅ Detects errors early  
✅ Facilitates refactoring  
✅ Documents code  
✅ Improves architecture  
✅ Saves time in the long run

### Remember:
- Use AAA pattern (Arrange-Act-Assert)
- Write clear and descriptive names
- Tests are independent
- Mock external dependencies
- Test error cases too
- Follow FIRST principles

### Next Steps:
1. Review examples: [Unit-Testing-Examples.md](Unit-Testing-Examples.md)
2. Practice with your own projects
3. Read more: [Microsoft documentation](https://learn.microsoft.com/en-us/dotnet/core/testing/)

---
