# C# App Development Cheat Sheet — When to Use Which Technique?

This is a practical quick guide: when building a C# console application, check here which technique fits which situation.

---

## Decision Tree: "How Do I Model This Data?"

```
Do you need data storage and logic?
│
├── YES → class
│   │
│   ├── Is validation needed (e.g. price cannot be negative)?
│   │   └── Property + private set + validation in constructor or setter
│   │
│   ├── Is it just data without logic (DTO, transfer object)?
│   │   └── record or class with auto-properties only
│   │
│   └── Is it a fixed set of values (e.g. status, type, role)?
│       └── enum
│
└── NO → Is it operations / actions?
    │
    ├── YES → Service class (e.g. PricingService, ReservationService)
    │
    └── NO → No need for a custom class
```

---

## Decision Tree: "When Interface, When Abstract Class?"

```
Do multiple classes need to implement the same contract?
│
├── YES
│   │
│   ├── Is there shared code to reuse?
│   │   └── abstract class (common base + required abstract methods)
│   │
│   └── No shared code, just same interface?
│       └── interface
│           Benefit: mockable in tests, loose coupling
│
└── NO → No need for interface or abstract class
    └── Concrete class is enough
```

**Rule of thumb:** If you want to test a service class without its dependencies → create interfaces for the dependencies.

---

## Decision Tree: "How Do I Organize the Code?"

```
What does the code do?
│
├── Communicate with user (menus, inputs, outputs)?
│   └── UI layer (Program.cs or dedicated UI classes)
│       No business logic here!
│
├── Rules and calculations (validation, pricing, overlap checks)?
│   └── Service layer (e.g. ReservationService, PricingService)
│       All business logic goes here.
│
├── Save and load data?
│   └── Repository/DataStore layer (e.g. JsonRepository, FileDataStore)
│       Only storage and retrieval, no logic.
│
└── Data structure (what data an object contains)?
    └── Model layer (e.g. Room, Guest, Reservation)
        Properties, validation, nothing else.
```

```
Typical layered structure:

  UI (Program.cs)
       │
       ▼
  Service (business logic)
       │
       ▼
  Repository (data save/load)
       │
       ▼
  Models (data structures)
```

---

## Decision Tree: "How Do I Store Data Persistently?"

```
Are you using a database?
│
├── YES → Entity Framework Core / Dapper
│
└── NO → File-based storage
    │
    ├── Does the data need to be human-readable?
    │   └── JSON (System.Text.Json)
    │
    └── Doesn't need to be readable?
        └── JSON still often the simplest option
```

### JSON Save/Load

```csharp
// Saving
var options = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(data, options);
await File.WriteAllTextAsync("data.json", json);

// Loading
string json = await File.ReadAllTextAsync("data.json");
var data = JsonSerializer.Deserialize<List<MyModel>>(json);
```

### When to Use Async in File Operations?

```
Are you reading/writing a file?
│
├── YES → Use async versions (ReadAllTextAsync, WriteAllTextAsync)
│         Releases the thread during the wait
│
└── NO → No need for async
```

---

## LINQ Quick Reference: "Which LINQ Method Do I Use?"

| I want to... | LINQ method | Example |
|--------------|-------------|---------|
| Filter a list | `.Where()` | `items.Where(x => x.IsActive)` |
| Transform list to another form | `.Select()` | `items.Select(x => x.Name)` |
| Sort | `.OrderBy()` / `.OrderByDescending()` | `items.OrderBy(x => x.Price)` |
| Find one | `.FirstOrDefault()` | `items.FirstOrDefault(x => x.Id == id)` |
| Check if any exist | `.Any()` | `items.Any(x => x.Status == "Active")` |
| Check if all satisfy condition | `.All()` | `items.All(x => x.Price > 0)` |
| Count | `.Count()` | `items.Count(x => x.Type == "Suite")` |
| Sum | `.Sum()` | `items.Sum(x => x.TotalPrice)` |
| Average | `.Average()` | `items.Average(x => x.Rating)` |
| Group | `.GroupBy()` | `items.GroupBy(x => x.Type)` |
| Join two lists | `.Join()` | Two lists by a common key |
| Check for overlaps | `.Any()` + condition | `existing.Any(x => x.Start < end && x.End > start)` |
| Take first N | `.Take(n)` | `items.Take(10)` |
| Skip first N | `.Skip(n)` | `items.Skip(20).Take(10)` |

### Chaining

LINQ methods can be chained:

```csharp
var results = items
    .Where(x => x.IsActive)
    .OrderBy(x => x.Name)
    .Select(x => new { x.Name, x.Price })
    .ToList();
```

---

## Validation: "Where Does Validation Belong?"

```
In which layer do I validate?
│
├── Model layer: Data integrity
│   └── "Price cannot be negative", "Name cannot be empty"
│   └── Implementation: constructor or property setter throws ArgumentException
│
├── Service layer: Business rules
│   └── "Overlapping reservations not allowed", "Budget must not be exceeded"
│   └── Implementation: method checks and throws InvalidOperationException
│
└── UI layer: Input format
    └── "Is the date in the correct format?", "Is the field empty?"
    └── Implementation: check before calling the service
```

---

## Unit Testing: "What Do I Test and How?"

```
What are you testing?
│
├── Business logic (service)?
│   │
│   ├── Are there dependencies on other classes?
│   │   └── YES → Mock dependencies (Moq)
│   │       Requirement: dependencies are interfaces
│   │
│   └── No dependencies?
│       └── Test directly: new MyService() + call + Assert
│
├── Model validation?
│   └── Test: valid values → object is created, invalid → exception
│
└── UI logic / Program.cs?
    └── DON'T test UI with unit tests.
        Only test business logic through the service.
```

### Test Naming

```
MethodName_Scenario_ExpectedResult

Examples:
  CalculatePrice_ThreeNights_ReturnsCorrectTotal
  CreateReservation_OverlappingDates_ThrowsException
  FindByEmail_NonExistent_ReturnsNull
```

### Test Structure (AAA)

```csharp
[Fact]
public void MethodName_Scenario_ExpectedResult()
{
    // Arrange - prepare
    var mock = new Mock<IRepository>();
    mock.Setup(x => x.GetAll()).Returns(testData);
    var service = new MyService(mock.Object);

    // Act - execute
    var result = service.Calculate(input);

    // Assert - verify
    Assert.Equal(expected, result);
}
```

### When Fact, When Theory?

| Situation | Use | Example |
|-----------|-----|---------|
| Single scenario | `[Fact]` | "Cancellation works" |
| Same logic, different values | `[Theory]` + `[InlineData]` | "Price calculated correctly for 1, 3, 7 nights" |

```csharp
[Theory]
[InlineData(1, 89)]
[InlineData(3, 267)]
[InlineData(7, 623)]
public void CalculatePrice_DifferentNights_ReturnsCorrectTotal(int nights, decimal expected)
{
    // ...
}
```

---

## Dependency Injection: "Why and How?"

```
Class A uses class B.
│
├── A creates B itself: new B()
│   └── PROBLEM: A cannot be tested without the real B
│
└── A receives B in constructor: A(IB b)
    └── SOLUTION: In tests you can provide a mock B, in production the real B
```

```csharp
// BAD — tight coupling
public class OrderService
{
    private DatabaseRepository _repo = new DatabaseRepository();
}

// GOOD — loose coupling
public class OrderService
{
    private readonly IRepository _repo;

    public OrderService(IRepository repo)
    {
        _repo = repo;
    }
}
```

---

## Exception Handling: "Which Exceptions Do I Throw?"

| Situation | Exception | Example |
|-----------|-----------|---------|
| Invalid parameter | `ArgumentException` | Empty name, negative price |
| Null parameter | `ArgumentNullException` | `email` is null |
| Value out of range | `ArgumentOutOfRangeException` | Amount is -1 |
| Business rule prevents operation | `InvalidOperationException` | Overlapping reservation, closed project |
| Data not found | Return `null` or throw `KeyNotFoundException` | No record with that ID |

```csharp
// Validation in service
public Reservation Create(int roomId, DateTime start, DateTime end)
{
    if (end <= start)
        throw new ArgumentException("End must be after start.");

    if (HasOverlap(roomId, start, end))
        throw new InvalidOperationException("Overlapping reservation.");

    // ... create reservation
}
```

---

## Quick Reference: Building the Whole Application

| Step | What to do | Technique |
|------|------------|-----------|
| 1. Models | Create data classes with properties and validation | `class`, `enum`, encapsulation |
| 2. Interfaces | Define contracts for services | `interface` |
| 3. Repository | Implement data save and load | `System.Text.Json`, `async/await`, `File.ReadAllTextAsync` |
| 4. Services | Implement business logic | Service classes, LINQ, DI in constructor |
| 5. UI | Build UI that calls services | `Console.ReadLine`, `Console.WriteLine` |
| 6. Tests | Test service logic | xUnit, Moq, `[Fact]`, `[Theory]` |

---

## 10 Golden Rules

1. **UI contains no logic** — UI reads inputs and displays results, service decides what happens.
2. **Service knows nothing of UI** — Service returns data, does not write to console.
3. **Validate in two places** — Model ensures data integrity, service ensures business rules.
4. **Interfaces for dependencies** — If class A uses class B, give A `IB` not `B`.
5. **One responsibility per class** — `PricingService` calculates prices, `ReservationService` manages reservations.
6. **LINQ before foreach** — If you filter, sort, or group, use LINQ.
7. **Async for files** — `File.ReadAllTextAsync` / `WriteAllTextAsync`, not synchronous versions.
8. **Test logic, not UI** — Test services directly, mock dependencies.
9. **Name clearly** — `SearchAvailableRooms`, not `GetRooms2` or `DoStuff`.
10. **Throw exception for invalid input** — `ArgumentException` for invalid data, `InvalidOperationException` for business rule violations.
