# Unit Testing and TDD

Welcome to the unit testing and Test-Driven Development (TDD) materials!

## Contents

### Unit Testing

- **[Unit-Testing.md](Unit-Testing.md)** - Unit testing fundamentals
  - What is unit testing?
  - xUnit framework
  - AAA pattern (Arrange-Act-Assert)
  - Assert methods
  - Mocking with Moq
  - Best practices

- **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)** - Comprehensive code examples
  - Basic Assert examples
  - Theory and InlineData
  - Mocking examples
  - Async tests
  - Exception tests
  - Collection tests
  - Comprehensive example: UserService

### Test-Driven Development (TDD)

- **[TDD.md](TDD.md)** - TDD theory and practices
  - What is TDD?
  - Red-Green-Refactor cycle
  - Rules of TDD
  - Benefits of TDD
  - Challenges and solutions
  - Best practices

- **[TDD-Examples.md](TDD-Examples.md)** - TDD in practice
  - FizzBuzz
  - String Calculator
  - Banking System
  - Password Validator
  - Shopping Cart
  - (Each example step-by-step with the Red-Green-Refactor cycle)

## Learning Order

We recommend studying in the following order:

### 1. Start with Unit Testing

📚 **[Unit-Testing.md](Unit-Testing.md)** - Learn the basics of testing

- What is unit testing?
- xUnit framework
- AAA pattern
- Assert methods
- Mocking

### 2. Practice with Examples

💻 **[Unit-Testing-Examples.md](Unit-Testing-Examples.md)** - Review code examples

- From simple to more complex
- Calculator, StringHelper, UserService
- Mocking examples

### 3. Learn TDD

🔄 **[TDD.md](TDD.md)** - Test-driven development

- Red-Green-Refactor cycle
- TDD rules and principles
- When and how to use it

### 4. Practice TDD

🚀 **[TDD-Examples.md](TDD-Examples.md)** - TDD in practice

- Follow step-by-step examples
- Understand the process
- Try it yourself

## Quick Start

### Setup

1. Create a new test project:

```bash
dotnet new xunit -n MyProject.Tests
cd MyProject.Tests
```

2. Install required packages:

```bash
dotnet add package xunit
dotnet add package xunit.runner.visualstudio
dotnet add package Microsoft.NET.Test.Sdk
dotnet add package Moq
```

3. Run tests:

```bash
dotnet test
```

### First Test

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

Run: `dotnet test`

## TDD Cycle in a Nutshell

```
🔴 RED
Write a failing test
    ↓
🟢 GREEN
Write the minimum code (test passes)
    ↓
🔵 REFACTOR
Improve the code (tests pass)
    ↓
Repeat ↩️
```

## Useful Resources

### Documentation

- [xUnit documentation](https://xunit.net/)
- [Moq documentation](https://github.com/moq/moq4)
- [Microsoft: Unit testing](https://learn.microsoft.com/en-us/dotnet/core/testing/)

### Books

- **Test-Driven Development: By Example** - Kent Beck
- **Growing Object-Oriented Software, Guided by Tests** - Steve Freeman & Nat Pryce
- **The Art of Unit Testing** - Roy Osherove
- **Working Effectively with Legacy Code** - Michael Feathers

### Practice Sites

- [Code Katas](http://codekata.com/)
- [Cyber Dojo](https://cyber-dojo.org/)
- [Codewars](https://www.codewars.com/)
- [Exercism](https://exercism.org/)

### Videos

- [Uncle Bob: The Three Rules of TDD](https://www.youtube.com/watch?v=AoIfc5NwRks)
- [Ian Cooper: TDD, Where Did It All Go Wrong](https://www.youtube.com/watch?v=EZ05e7EMOLM)

## Tips

### Unit Testing

✅ Keep tests fast (< 10ms)  
✅ Tests are independent  
✅ Use the AAA pattern  
✅ One Assert per test (usually)  
✅ Test error scenarios too  
✅ Use descriptive names

### TDD

✅ Start simple  
✅ Small steps (Baby Steps)  
✅ Red → Green → Refactor  
✅ Tests first, code second  
✅ YAGNI - Don't do extra work  
✅ Let tests guide design

---

**Remember:** TDD is a skill that improves with practice. Don't give up if it feels difficult at first!
