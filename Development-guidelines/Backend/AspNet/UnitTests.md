# UnitTest and Testing in .NET

Think of tests as the *user interface* for your code.

If someone new opens your solution, the tests should be the quickest way to learn:

* what matters,
* what’s guaranteed,
* what will break if they touch the wrong wire.

---

## 1. Testing stack: what to use in .NET

The good news: the ecosystem is mature and boring in the best way.

You’ll usually pick:

* **xUnit** (most popular in modern .NET, great for dependency injection, used by ASP.NET team)
* **NUnit** (battle-tested, expressive, still widely used)
* **MSTest** (ships with Visual Studio, fine but less loved)

If you’re starting fresh, choose **xUnit** unless your team standard says otherwise.

Typical solution layout:

```text
MyApp.sln
  src/
    MyApp/
      MyApp.csproj
  tests/
    MyApp.Tests/
      MyApp.Tests.csproj
```

Create the test project:

```bash
dotnet new xunit -n MyApp.Tests
dotnet sln add ./tests/MyApp.Tests/MyApp.Tests.csproj
dotnet add ./tests/MyApp.Tests/MyApp.Tests.csproj reference ./src/MyApp/MyApp.csproj
```

Run:

```bash
dotnet test
```

That’s the skeleton. Now let’s fill it with good habits.

---

## 2. How to structure your tests (mentally and in code)

For each class or behavior, think in **scenarios**, not methods.

Name tests like statements:

```csharp
public class PriceCalculatorTests
{
    [Fact]
    public void Calculates_Discount_For_PremiumCustomer()
    {
        // ...
    }
}
```

Use **Arrange → Act → Assert** as your default rhythm:

```csharp
[Fact]
public void Calculates_Discount_For_PremiumCustomer()
{
    // Arrange
    var calc = new PriceCalculator();
    
    // Act
    var price = calc.Calculate(100m, isPremiumCustomer: true);

    // Assert
    Assert.Equal(90m, price);
}
```

Key habits worth locking in:

* Keep each test **focused**: one scenario, one assertion “theme”.
* Prefer naming that reads like a sentence over cleverness.
* Don’t share too much magic setup across tests; clarity beats DRY here.

---

## 3. Writing your first real tests

### 3.1 Pure logic: easiest wins first

Start with the stuff that doesn’t touch I/O, time, or randomness.

```csharp
public sealed class DamageCalculator
{
    public int Calculate(int attack, int defense, bool critical)
    {
        var baseDamage = Math.Max(0, attack - defense);
        if (critical)
        {
            baseDamage = (int)(baseDamage * 1.5);
        }
        return baseDamage;
    }
}
```

Test:

```csharp
using Xunit;

public class DamageCalculatorTests
{
    [Fact]
    public void Normal_Hit_Subtracts_Defense()
    {
        var calc = new DamageCalculator();

        var result = calc.Calculate(10, 3, critical: false);

        Assert.Equal(7, result);
    }

    [Fact]
    public void Critical_Hit_Multiplies_BaseDamage()
    {
        var calc = new DamageCalculator();

        var result = calc.Calculate(10, 3, critical: true);

        Assert.Equal(10, result); // (10 - 3) * 1.5 = 10.5 => 10
    }
}
```

This is the foundation. Every other kind of test is just this plus some wiring.

---

## 4. Testing code with dependencies (the real game)

Most application code *depends on things*:

* current time,
* random numbers,
* database,
* HTTP clients,
* message buses.

Direct calls to those make tests painful. In .NET, the standard move is:

1. Depend on **interfaces**.
2. Pass them via **constructor injection**.
3. Use **fakes/mocks** in tests.

### 4.1 Injecting dependencies

Production code:

```csharp
public interface IClock
{
    DateTime UtcNow { get; }
}

public sealed class SystemClock : IClock
{
    public DateTime UtcNow => DateTime.UtcNow;
}

public sealed class DailyBonusService
{
    private readonly IClock _clock;

    public DailyBonusService(IClock clock)
    {
        _clock = clock;
    }

    public bool IsBonusAvailable() =>
        _clock.UtcNow.Hour == 0;
}
```

Test:

```csharp
public sealed class FakeClock : IClock
{
    public DateTime UtcNow { get; set; }
}

public class DailyBonusServiceTests
{
    [Fact]
    public void Bonus_Only_Available_At_Midnight()
    {
        var clock = new FakeClock { UtcNow = new DateTime(2025, 11, 10, 00, 00, 00) };
        var svc = new DailyBonusService(clock);

        Assert.True(svc.IsBonusAvailable());
    }

    [Fact]
    public void Bonus_Not_Available_Otherwise()
    {
        var clock = new FakeClock { UtcNow = new DateTime(2025, 11, 10, 13, 15, 00) };
        var svc = new DailyBonusService(clock);

        Assert.False(svc.IsBonusAvailable());
    }
}
```

No hacks. No messing with system time. Completely deterministic.

### 4.2 Using mocking frameworks (when helpful)

For simple cases, hand-written fakes are clearer.

For more complex interactions (e.g., “must call repository once with these arguments”), use a mocking library like **Moq** or **NSubstitute**.

Example with Moq:

```csharp
using Moq;
using Xunit;

public interface IEmailSender
{
    Task SendAsync(string to, string subject);
}

public sealed class WelcomeService
{
    private readonly IEmailSender _emails;
    public WelcomeService(IEmailSender emails) { _emails = emails; }

    public Task SendWelcomeAsync(string email) =>
        _emails.SendAsync(email, "Welcome!");
}

public class WelcomeServiceTests
{
    [Fact]
    public async Task Sends_Welcome_Email()
    {
        var sender = new Mock<IEmailSender>();
        var svc = new WelcomeService(sender.Object);

        await svc.SendWelcomeAsync("user@example.com");

        sender.Verify(x => x.SendAsync("user@example.com", "Welcome!"), Times.Once);
    }
}
```

Keep mocks close to the behavior you’re asserting; don’t mock everything by default.

---

## 5. Organizing tests in a .NET solution

A few simple conventions help a lot:

**Folder and class structure**

Mirror production structure:

```text
src/MyApp/Services/PaymentService.cs
tests/MyApp.Tests/Services/PaymentServiceTests.cs
```

**Naming**

Use a consistent pattern:

* `ClassNameTests`
* or `ClassName_Scenario` inside a bigger test class.

**Test data**

For tiny cases, inline literals are fine.
For more complex scenarios, consider:

* private factory methods (`CreateOrder(...)`),
* `[Theory]` + `[InlineData(...)]` / `[MemberData]` in xUnit for variations.

Example:

```csharp
public class DamageCalculatorTheoryTests
{
    [Theory]
    [InlineData(10, 3, false, 7)]
    [InlineData(10, 3, true, 10)]
    [InlineData(5, 10, false, 0)]
    public void Calculates_As_Expected(int atk, int def, bool crit, int expected)
    {
        var calc = new DamageCalculator();

        var result = calc.Calculate(atk, def, crit);

        Assert.Equal(expected, result);
    }
}
```

---

## 6. Integration tests the .NET way (quick overview)

When you need to test how components collaborate (e.g., ASP.NET Core controllers, EF Core, etc.), you can:

* Use `WebApplicationFactory<TEntryPoint>` to spin up an in-memory test server.
* Use in-memory or test containers for databases.
* Hit real endpoints with `HttpClient` against that in-memory host.

Example shape (ASP.NET Core):

```csharp
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc.Testing;
using Xunit;

public class ApiTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public ApiTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Get_Status_ReturnsOk()
    {
        var response = await _client.GetAsync("/status");
        Assert.Equal(HttpStatusCode.OK, response.StatusCode);
    }
}
```

These are heavier than unit tests; keep them targeted.

---

## 7. Common traps (and how to sidestep them)

A few things that quietly ruin test suites:

**Flaky tests**

Timers, threads, random, network. If a test “sometimes fails,” fix the cause or delete it. Unreliable tests train everyone to ignore red.

**Over-mocking**

If your test uses 7 mocks for 1 behavior, your design is shouting for refactoring. Group behavior, pass simpler dependencies.

**Testing implementation instead of behavior**

Asserting “this private method was called” or “it uses a list internally” is brittle. Assert **outcomes**:

* returned values,
* events raised,
* calls made to dependencies (when that’s the contract).

**No tests for the scary parts**

If there’s a file everybody fears touching, that’s where you need tests the most. Wrap current behavior in tests *before* you refactor.

---

## 8. Putting it all together (a simple recipe)

If you’re unsure where to start in a .NET project:

1. **Create a test project** with xUnit alongside your main project.
2. **Pick one nontrivial behavior** (price calc, bonus rule, state machine) and write 3–5 precise unit tests.
3. **Introduce interfaces** for any external stuff (time, HTTP, DB) your tests struggle with.
4. **Use DI** (constructor injection) consistently in your main code so tests can pass fakes.
5. **Add an integration test** for one key end-to-end path (e.g., POST → DB → response).
6. **Run `dotnet test` often**; wire it into CI so nobody can merge red.

Key highlights:

* Tests are design tools, not paperwork.
* Interfaces + DI + small functions make testing natural.
* If writing a test feels impossible, treat that as a design smell worth fixing.
