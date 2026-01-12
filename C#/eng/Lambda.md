# Lambda Expressions and Anonymous Functions

[Official Microsoft documentation on lambda expressions](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)

## What Is a Lambda Expression?

A **lambda expression** is a short and concise way to define an anonymous function (a function without a name). Lambda expressions are commonly used in:

- LINQ queries (`Where`, `Select`, `OrderBy`, etc.)
- Creating delegates
- Event handler methods
- Callback functions
- Asynchronous programming

Lambda expressions make code more compact and readable when the function is simple and only needed in a single place.

## Lambda Expression Syntax

### Basic Syntax

```
(parameters) => expression or block
```

- **Parameters**: The function inputs (can be 0, 1, or many)
- **`=>`**: The “lambda operator” (read as “goes to” or “becomes”)
- **Expression or block**: The body (implementation) of the function

### Examples

```csharp
// No parameters
() => Console.WriteLine("Hello!")

// One parameter
x => x * 2

// Multiple parameters
(x, y) => x + y

// Multi-line block
(x, y) =>
{
    int sum = x + y;
    Console.WriteLine($"Sum: {sum}");
    return sum;
}
```

## Expression Lambdas vs. Statement Lambdas

### Expression Lambda

An expression lambda is a simple, single-expression lambda. The result of the expression is returned automatically.

```csharp
Func<int, int> square = x => x * x;
Console.WriteLine(square(5)); // 25

Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(3, 4)); // 7

// LINQ example
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var doubled = numbers.Select(n => n * 2).ToList();
// doubled = [2, 4, 6, 8, 10]
```

### Statement Lambda

A statement lambda is a multi-line lambda that uses curly braces `{ }`. If it returns a value, it must use the `return` keyword.

```csharp
Func<int, int, int> multiply = (a, b) =>
{
    Console.WriteLine($"Multiplying {a} and {b}");
    int result = a * b;
    return result;
};

Console.WriteLine(multiply(3, 4));
// Output:
// Multiplying 3 and 4
// 12
```

```csharp
// LINQ example with a multi-line lambda
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var filtered = numbers.Where(n =>
{
    bool isEven = n % 2 == 0;
    bool isLarge = n > 2;
    return isEven && isLarge;
}).ToList();
// filtered = [4]
```

## Working with Parameters

### No Parameters

```csharp
Func<string> getMessage = () => "Hello, World!";
Console.WriteLine(getMessage()); // Hello, World!

Action greet = () => Console.WriteLine("Hi there!");
greet(); // Hi there!
```

### One Parameter

For a single parameter, parentheses are optional:

```csharp
// Without parentheses (recommended in simple cases)
Func<int, int> square = x => x * x;

// With parentheses (also valid)
Func<int, int> squareWithParens = (x) => x * x;

// Explicit type (rarely needed)
Func<int, int> squareWithType = (int x) => x * x;
```

### Multiple Parameters

For multiple parameters, parentheses are required:

```csharp
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(10, 5)); // 15

Func<string, string, string> concat = (first, last) => $"{first} {last}";
Console.WriteLine(concat("John", "Doe")); // John Doe
```

### Explicitly Typed Parameters

Normally C# infers parameter types, but you can specify them explicitly:

```csharp
Func<int, int, double> divide = (int a, int b) => (double)a / b;
Console.WriteLine(divide(10, 3)); // 3.333...
```

## Anonymous Functions vs. Named Methods

### Named Method

```csharp
bool IsEven(int number)
{
    return number % 2 == 0;
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(IsEven).ToList();
// evenNumbers = [2, 4, 6]
```

### Lambda Expression (Anonymous Function)

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
// evenNumbers = [2, 4, 6]
```

### When to Use Which?

| Scenario                         | Recommendation    |
| -------------------------------- | ----------------- |
| Simple, one-off logic            | Lambda expression |
| Complex logic (> 3 lines)        | Named method      |
| Logic reused in multiple places  | Named method      |
| LINQ queries                     | Lambda expression |
| Logic that should be unit-tested | Named method      |

## Practical Examples

### Example 1: LINQ Filtering and Projection

```csharp
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}

List<Person> people = new List<Person>
{
    new Person { Name = "Alice", Age = 25 },
    new Person { Name = "Bob", Age = 30 },
    new Person { Name = "Charlie", Age = 20 }
};

// Filter adults (over 21) and get their names
var adultNames = people
    .Where(p => p.Age > 21)
    .Select(p => p.Name)
    .ToList();
// adultNames = ["Alice", "Bob"]

// Order by age and create a summary
var summary = people
    .OrderBy(p => p.Age)
    .Select(p => $"{p.Name} is {p.Age} years old")
    .ToList();
```

### Example 2: Event Handling

```csharp
public class Button
{
    public event EventHandler Clicked;

    public void Click()
    {
        Clicked?.Invoke(this, EventArgs.Empty);
    }
}

Button button = new Button();

// Lambda expression as an event handler
button.Clicked += (sender, e) => Console.WriteLine("Button clicked!");

// Multi-line event handler
button.Clicked += (sender, e) =>
{
    Console.WriteLine("Processing click...");
    Console.WriteLine("Click handled!");
};

button.Click();
// Output:
// Button clicked!
// Processing click...
// Click handled!
```

### Example 3: Callback Functions

```csharp
void ProcessData(List<int> data, Action<int> callback)
{
    foreach (var item in data)
    {
        callback(item);
    }
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// Simple callback
ProcessData(numbers, n => Console.WriteLine(n));

// More complex callback
ProcessData(numbers, n =>
{
    int squared = n * n;
    Console.WriteLine($"{n}² = {squared}");
});
```

### Example 4: Custom Sorting Logic

```csharp
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
}

List<Product> products = new List<Product>
{
    new Product { Name = "Laptop", Price = 999.99m },
    new Product { Name = "Mouse", Price = 25.50m },
    new Product { Name = "Keyboard", Price = 79.99m }
};

// Sort by price (cheapest first)
var sortedByPrice = products.OrderBy(p => p.Price).ToList();

// Sort by name length
var sortedByNameLength = products.OrderBy(p => p.Name.Length).ToList();

// More complex sort: first by price, then by name
var complexSort = products
    .OrderBy(p => p.Price)
    .ThenBy(p => p.Name)
    .ToList();
```

### Example 5: Aggregation and Calculations

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// Sum of even numbers
int evenSum = numbers.Where(n => n % 2 == 0).Sum();
// evenSum = 30

// Largest even number
int maxEven = numbers.Where(n => n % 2 == 0).Max();
// maxEven = 10

// Count numbers greater than 5
int count = numbers.Count(n => n > 5);
// count = 5

// Average of numbers between 3 and 7 (inclusive)
double average = numbers.Where(n => n >= 3 && n <= 7).Average();
// average = 5.0
```

## Lambdas and Delegates

Lambda expressions work together with delegates. Every lambda expression is compatible with some delegate type.

```csharp
// Action: no return value
Action<string> print = message => Console.WriteLine(message);
print("Hello!"); // Hello!

// Func: returns a value
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(5, 3)); // 8

// Predicate: returns bool
Predicate<int> isPositive = number => number > 0;
Console.WriteLine(isPositive(5)); // True
```

> **More info:** [Delegates](Delegates.md), [Predicates](Predicate.md)

## Old-Style Anonymous Methods (C# 2.0)

Before lambda expressions (introduced in C# 3.0), C# used the `delegate` keyword to create anonymous functions. You may still see this syntax in older code.

```csharp
// Old style (C# 2.0)
Func<int, int, int> oldAdd = delegate (int a, int b)
{
    return a + b;
};

// Modern style (C# 3.0+)
Func<int, int, int> modernAdd = (a, b) => a + b;
```

**Recommendation:** Always use lambda expressions in new code. They are shorter and easier to read.

## Discard Parameters

If you don’t need all parameters, you can use `_` (a discard):

```csharp
// Event handler that doesn’t use parameters
button.Click += (_, _) => Console.WriteLine("Clicked!");

// LINQ example: index not used
var items = new[] { "a", "b", "c" };
var withIndex = items.Select((item, _) => item.ToUpper()).ToList();
```

## Async Lambdas

Lambda expressions can also be asynchronous:

```csharp
Func<Task<string>> fetchData = async () =>
{
    await Task.Delay(1000);
    return "Data loaded!";
};

string result = await fetchData();
Console.WriteLine(result); // Data loaded! (after ~1 second delay)
```

```csharp
// With LINQ
List<int> ids = new List<int> { 1, 2, 3 };
var tasks = ids.Select(async id =>
{
    await Task.Delay(100);
    return $"Processed {id}";
});

var results = await Task.WhenAll(tasks);
// results = ["Processed 1", "Processed 2", "Processed 3"]
```

> **Note:** Using async lambdas in LINQ requires care. Use `Task.WhenAll` or similar methods when you need to await all asynchronous operations.

## Common Mistakes with Lambda Expressions

### Mistake 1: Forgetting Parentheses with Multiple Parameters

```csharp
// ❌ Error
Func<int, int, int> add = a, b => a + b; // Compilation error!

// ✅ Correct
Func<int, int, int> add = (a, b) => a + b;
```

### Mistake 2: Forgetting `return` in a Statement Lambda

```csharp
// ❌ Error
Func<int, int> square = x =>
{
    x * x; // No return!
};

// ✅ Correct
Func<int, int> square = x =>
{
    return x * x;
};

// ✅ Even better (expression lambda)
Func<int, int> square = x => x * x;
```

### Mistake 3: Overly Complex Lambdas

```csharp
// ❌ Hard to read
var result = data
    .Where(x =>
    {
        var isValid = x.Status == "Active" && x.Date > DateTime.Now.AddDays(-30);
        var hasItems = x.Items != null && x.Items.Count > 0;
        var isApproved = x.ApprovedBy != null;
        return isValid && hasItems && isApproved;
    })
    .ToList();

// ✅ Better: use a named method
bool IsValidRecord(Record x)
{
    var isValid = x.Status == "Active" && x.Date > DateTime.Now.AddDays(-30);
    var hasItems = x.Items != null && x.Items.Count > 0;
    var isApproved = x.ApprovedBy != null;
    return isValid && hasItems && isApproved;
}

var result = data.Where(IsValidRecord).ToList();
```

## Best Practices

1. **Keep lambdas simple**: If a lambda is more than about 3 lines, consider using a named method.
2. **Use clear parameter names**: `x` and `y` are fine for simple cases, but more descriptive names improve readability.
3. **Avoid side effects**: A lambda should not normally modify external variables (see [Closures](Closures.md)).
4. **Prefer expression lambdas over statement lambdas** when possible.
5. **Think about testability**: If the logic is complex or critical, move it into a named method that can be unit-tested.

## Summary

- A **lambda expression** is a concise way to define an anonymous function.
- Syntax: `(parameters) => expression or block`.
- **Expression lambda**: single-line expression; result is returned automatically.
- **Statement lambda**: multi-line block; uses `{}` and may require `return`.
- Lambdas work with **delegates** (`Action`, `Func`, `Predicate`).
- Widely used in **LINQ**, **event handling**, and **callback** functions.
- Keep lambdas **simple and clear** for better readability and maintainability.

## Useful Links

### Official Documentation

- [Lambda Expressions (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)
- [Expression-bodied members (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/statements-expressions-operators/expression-bodied-members)
- [Anonymous Functions (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-operator)

### Tutorials

- [C# Lambda Expressions (w3schools)](https://www.w3schools.com/cs/cs_lambda.php)
- [Lambda Tutorial (TutorialsTeacher)](https://www.tutorialsteacher.com/linq/linq-lambda-expression)
- [Lambda Expressions in C# (C# Corner)](https://www.c-sharpcorner.com/UploadFile/bd6c67/lambda-expressions-in-C-Sharp/)

### Video Tutorials

- [Lambda Expressions in C# (YouTube)](https://www.youtube.com/watch?v=j02HKEgIlV0)
- [C# Lambda Expressions Tutorial (YouTube)](https://www.youtube.com/watch?v=o8LWnwmHnXo)

### Related Material

- [LINQ and Lambda Expressions](LINQ.md)
- [Delegates](Delegates.md)
- [Predicates](Predicate.md)
- [Closures](Closures.md)
