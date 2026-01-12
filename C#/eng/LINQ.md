# LINQ and Lambda Expressions

[Official Microsoft LINQ documentation](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)

## What Is LINQ?

**LINQ** (Language Integrated Query) is a feature in C# that lets you query data directly inside your code in a unified way, regardless of the data source. You can use LINQ with databases (through ORMs like Entity Framework Core), XML documents, or in-memory collections such as lists.

### Sample LINQ Query

```csharp
using System.Linq;

var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Select all odd numbers
var oddNumbers = numbers.Where(n => n % 2 != 0).ToList();
// oddNumbers = {1, 3, 5}
```

## What Is a Lambda?

**Lambda expressions** are a short-hand way to declare anonymous functions in C#. They are frequently used inside LINQ queries and with [delegates](Delegates.md).

> **Dig deeper:** [Lambda expressions](Lambda.md) – in-depth material on lambdas and anonymous functions

### Lambda Syntax

```
(parameters) => expression
```

### Sample Lambda Expression

```csharp
// Lambda expression that checks if a number is odd
Func<int, bool> isOdd = x => x % 2 != 0;

bool result = isOdd(5);  // true
bool result2 = isOdd(4); // false
```

### Lambda Inside a LINQ Query

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Using a lambda expression
var oddNumbers = numbers.Where(x => x % 2 != 0).ToList();
```

### Naming Parameters

You can name parameters however you like. `x` and `y` are common, but descriptive names improve readability:

```csharp
// Common but vague
var result = numbers.Where(x => x % 2 == 0);

// Clearer
var result = numbers.Where(number => number % 2 == 0);
```

## LINQ vs. Lambda: What Is the Difference?

LINQ (Language Integrated Query) and lambda expressions are related but not identical. LINQ provides a higher-level syntax for asking questions about data structures, while lambda expressions are flexible building blocks that can be part of LINQ queries.

### 1. LINQ Query Syntax

LINQ offers a SQL-like syntax for performing operations on collections.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// LINQ query syntax
var evenNumbers = from num in numbers
                  where num % 2 == 0
                  select num;

foreach (var num in evenNumbers)
{
    Console.WriteLine(num);
}
```

This **query syntax** looks similar to SQL. It is often readable but a bit longer than lambda-based syntax.

### 2. Lambda Method Syntax

Lambda expressions are anonymous functions typically used for short operations, for instance inside LINQ method chains.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Lambda syntax with LINQ methods
var evenNumbersLambda = numbers.Where(num => num % 2 == 0);

foreach (var num in evenNumbersLambda)
{
    Console.WriteLine(num);
}
```

This does the same thing as the previous query, but now uses **method syntax**, which tends to be shorter and more direct.

### 3. Key Differences

| Feature | LINQ Query Syntax | Lambda Method Syntax |
|---------|-------------------|----------------------|
| **Readability** | SQL-like and explicit | More compact but can be harder to read |
| **Flexibility** | Less flexible (some operations are harder) | Allows more complex functions |
| **Ability to use functions** | Limited | Full support for lambda functions |
| **Performance** | Same performance as lambdas | Same performance as LINQ |

### 4. Practical Tip

- **Want an SQL-style, very explicit format?** Use **LINQ query syntax**.
- **Want a shorter and more flexible approach?** Use **lambda expressions with method syntax**.

Most C# developers prefer lambda-based syntax because it is concise and flexible.

## Core LINQ Concepts

### 1. Filtering (`Where`)

Filtering lets you keep only the elements that satisfy a condition.

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
// evenNumbers = {2, 4, 6}
```

### 2. Projection (`Select`)

`Select` transforms each element into a new shape.

```csharp
List<string> names = new List<string> { "Anna", "Ben", "Charlie" };
List<string> upperNames = names.Select(n => n.ToUpper()).ToList();
// upperNames = {"ANNA", "BEN", "CHARLIE"}
```

### 3. Grouping (`GroupBy`)

Grouping splits a collection into buckets based on a key.

```csharp
List<(string Name, int Grade)> students = new List<(string Name, int Grade)>
{
    ("Alice", 10),
    ("Bob", 10),
    ("Charlie", 11)
};

var grouped = students.GroupBy(s => s.Grade);
foreach (var group in grouped)
{
    Console.WriteLine($"Grade {group.Key}:");
    foreach (var student in group)
    {
        Console.WriteLine($"  {student.Name}");
    }
}
```

### 4. Ordering (`OrderBy`, `OrderByDescending`)

Use these to sort a collection.

```csharp
List<int> numbers = new List<int> { 5, 2, 8, 1 };
List<int> orderedNumbers = numbers.OrderBy(n => n).ToList();
// orderedNumbers = {1, 2, 5, 8}

// Descending order
List<int> descendingNumbers = numbers.OrderByDescending(n => n).ToList();
// descendingNumbers = {8, 5, 2, 1}
```

### 5. Aggregation (`Sum`, `Average`, `Count`)

These methods perform calculations over the collection.

```csharp
List<decimal> sales = new List<decimal> { 100.0m, 200.0m, 50.0m };
decimal totalSales = sales.Sum();        // 350.0m
decimal averageSales = sales.Average();  // 116.67m
int count = sales.Count();               // 3
```

### 6. `Single` vs. `SingleOrDefault`

- `Single()`: Returns the only element in the sequence; throws if there are zero or more than one.
- `SingleOrDefault()`: Returns the single element or the default value (`null` for reference types) if the sequence is empty; throws if there is more than one element.

```csharp
var numbers = new List<int> { 5 };

int single = numbers.Single();                  // 5
int? singleOrDefault = numbers.SingleOrDefault(); // 5

var empty = new List<int>();
// int result = empty.Single();                // Throws
int? result2 = empty.SingleOrDefault();        // null
```

### 7. `First` vs. `FirstOrDefault`

- `First()`: Returns the first element; throws if the sequence is empty.
- `FirstOrDefault()`: Returns the first element or the default value if the sequence is empty.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

int first = numbers.First();                     // 1
int? firstOrDefault = numbers.FirstOrDefault();  // 1

var empty = new List<int>();
// int result = empty.First();                  // Throws
int? result2 = empty.FirstOrDefault();           // null
```

## Anonymous Functions

### What Is an Anonymous Function?

An anonymous function is a function defined without a name and used without creating a separate method. This is convenient when you only need the function once, for instance inside LINQ operations. C# supports anonymous functions through lambda expressions (`=>`).

### Example: Anonymous Function vs. Separate Method

```csharp
// Separate method
bool IsEven(int number)
{
    return number % 2 == 0;
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(IsEven).ToList();
// evenNumbers = {2, 4, 6}
```

```csharp
// Same with an anonymous function (lambda expression)
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
```

> **Note:** LINQ often also relies on [delegates](Delegates.md). See how they integrate with LINQ operations.

## Predicate

> **Explore more:** [Predicates](Predicate.md) – comprehensive material about predicates

### What Is a Predicate in C#?

A **predicate** is a function (or lambda) that takes a value and returns `true` or `false`. In other words, it is a *condition* that checks whether “this thing matches the rule.”

### When Do You Use Predicates?

Predicates are common when you:

- search a list (`Find`, `FindAll`)
- check if something exists (`Any`)
- count how many items satisfy a condition (`Count`)
- filter data (`Where`)
- ensure everything matches a condition (`All`)

### `Predicate<T>` vs. `Func<T, bool>`

In C#, predicates usually appear in two forms:

- **`Predicate<T>`** — delegate meaning “method that accepts T and returns bool.” Example: `Predicate<int>` is “takes an int → returns bool.”
- **`Func<T, bool>`** — a generic delegate that can also represent a predicate. Example: `Func<string, bool>` is “takes a string → returns bool.”

Many list methods use `Predicate<T>`, whereas LINQ usually expects a `Func<T, bool>`. Same idea: **input → `true` / `false`**.

### Example: Predicate as a Lambda

```csharp
// Predicate<int>: int -> bool
Predicate<int> isEven = n => n % 2 == 0;

bool a = isEven(4); // true
bool b = isEven(7); // false
```

### Example: `List.Find` and `List.FindAll`

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Find: returns the first element that matches
int firstEven = numbers.Find(n => n % 2 == 0); // 2

// FindAll: returns all matching elements
List<int> allEven = numbers.FindAll(n => n % 2 == 0); // [2, 4, 6]
```

### Same Idea with LINQ (`Where` uses a predicate)

```csharp
using System.Linq;

var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Where keeps only the items where the predicate returns true
var evens = numbers.Where(n => n % 2 == 0).ToList(); // [2, 4, 6]
```

### Memory Trick

A predicate is like asking every item a yes/no question:

- “Is this number even?”
- “Is this person at least 18 years old?”
- “Does this text contain the word 'error'?”

### Exercise

```csharp
var names = new List<string> { "Ari", "Tuomas", "Liisa", "Annika" };

Predicate<string> longName = name => name.Length >= 5;

var result1 = names.FindAll(longName);                  // FindAll + Predicate<T>
var result2 = names.Where(n => n.Length >= 5).ToList(); // LINQ Where + lambda

// result1 and result2: ["Tuomas", "Liisa", "Annika"]
```

## LINQ and Parameters

LINQ methods usually take parameters of type `Func<T, bool>` or `Func<T, TResult>` that define what operation to run for each element.

### Example: LINQ with Your Own Predicate Function

```csharp
bool IsEven(int number)
{
    return number % 2 == 0;
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(IsEven).ToList();
// evenNumbers = {2, 4, 6}
```

### Example: LINQ with an Anonymous Function

The same can be done with an anonymous function and no separate method:

```csharp
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
```

## Practical Examples

### Example 1: Filter and Sort Students

```csharp
public class Student
{
    public string Name { get; set; }
    public int Age { get; set; }
    public double Grade { get; set; }
}

List<Student> students = new List<Student>
{
    new Student { Name = "Anna", Age = 20, Grade = 4.5 },
    new Student { Name = "Mikko", Age = 22, Grade = 3.8 },
    new Student { Name = "Laura", Age = 19, Grade = 4.9 },
    new Student { Name = "Jari", Age = 21, Grade = 3.5 }
};

// Get students with grade > 4.0 and sort by age
var topStudents = students
    .Where(s => s.Grade > 4.0)
    .OrderBy(s => s.Age)
    .Select(s => s.Name)
    .ToList();
// topStudents = ["Laura", "Anna"]
```

> **More examples:** [LINQ Tutorial - 101 LINQ Samples](https://www.tutorialsteacher.com/linq/sample-linq-queries)

### Example 2: Filter Products and Calculate Price

```csharp
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
    public string Category { get; set; }
}

List<Product> products = new List<Product>
{
    new Product { Name = "Laptop", Price = 999.99m, Category = "Electronics" },
    new Product { Name = "Mouse", Price = 25.50m, Category = "Electronics" },
    new Product { Name = "Desk", Price = 299.00m, Category = "Furniture" },
    new Product { Name = "Chair", Price = 149.99m, Category = "Furniture" }
};

// Get electronics and sum their price
var electronicsTotal = products
    .Where(p => p.Category == "Electronics")
    .Sum(p => p.Price);
// electronicsTotal = 1025.49

// Get the most expensive product in each category
var mostExpensiveByCategory = products
    .GroupBy(p => p.Category)
    .Select(g => new
    {
        Category = g.Key,
        MostExpensive = g.OrderByDescending(p => p.Price).First()
    })
    .ToList();
```

> **More examples:** [C# LINQ Examples](https://dotnettutorials.net/lesson/linq-examples/)

### Example 3: Chain Multiple Operations

```csharp
// Find the squares of odd numbers that are below 100 and sort them
var numbers = Enumerable.Range(1, 20); // 1-20

var result = numbers
    .Where(n => n % 2 != 0)       // Odd numbers
    .Select(n => n * n)           // Squares
    .Where(n => n < 100)          // Less than 100
    .OrderByDescending(n => n)    // Largest first
    .ToList();
// result = [81, 49, 25, 9, 1]
```

> **More chaining examples:** [LINQ Method Chaining](https://www.c-sharpcorner.com/article/method-chaining-in-linq/)

### Example 4: Join Operation

```csharp
public class Department
{
    public int Id { get; set; }
    public string Name { get; set; }
}

public class Employee
{
    public string Name { get; set; }
    public int DepartmentId { get; set; }
}

List<Department> departments = new List<Department>
{
    new Department { Id = 1, Name = "IT" },
    new Department { Id = 2, Name = "HR" }
};

List<Employee> employees = new List<Employee>
{
    new Employee { Name = "Alice", DepartmentId = 1 },
    new Employee { Name = "Bob", DepartmentId = 2 },
    new Employee { Name = "Charlie", DepartmentId = 1 }
};

// Join employees and departments
var employeeDepartments = employees
    .Join(departments,
          employee => employee.DepartmentId,
          department => department.Id,
          (employee, department) => new
          {
              EmployeeName = employee.Name,
              DepartmentName = department.Name
          })
    .ToList();
```

> **More join examples:** [LINQ Join Operations](https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/join-operations)

### Example 5: `Any`, `All`, and `Contains`

```csharp
List<int> numbers = new List<int> { 2, 4, 6, 8, 10 };

// Are there any even numbers?
bool hasEven = numbers.Any(n => n % 2 == 0); // true

// Are all numbers even?
bool allEven = numbers.All(n => n % 2 == 0); // true

// Does the list contain 5?
bool containsFive = numbers.Contains(5);     // false

// Are there numbers greater than 100?
bool hasLarge = numbers.Any(n => n > 100);   // false
```

> **More quantifier examples:** [LINQ Quantifier Operations](https://learn.microsoft.com/en-us/dotnet/csharp/linq/standard-query-operators/quantifier-operations)

## Query Operators

Query operators are the methods you use in C# to build queries over collections.

There are many different operators, and you can find a list plus examples [here](https://www.tutorialsteacher.com/linq/linq-standard-query-operators).

Sample code is also available in the [CollectionExamples](https://github.com/xamk-ture/AdvancedExamples/blob/master/CollectionExamples/Program.cs) project.

## Summary

- **LINQ** offers a unified way to query data from different sources.
- **Lambda expressions** are a concise way to define anonymous functions (see [Lambda.md](Lambda.md)).
- **Delegates** let you treat methods as variables (see [Delegates.md](Delegates.md)).
- **Predicates** are functions that return `true` or `false` (see [Predicate.md](Predicate.md)).
- **Closures** allow lambdas to capture external variables (see [Closures.md](Closures.md)).
- **LINQ and lambdas** make C# code more concise and readable, especially when working with collections or data sources.

## Recommended Exercises

1. **Try different LINQ operators** with your own lists.
2. **Chain multiple operations** together and see how they interact.
3. **Compare Query Syntax vs. Method Syntax** and pick what fits your style.
4. **Use the debugger** to inspect how LINQ expressions are evaluated step by step.
5. **Try LINQPad**: [LINQPad](https://www.linqpad.net/) (free version available).

## Helpful Links and Extra Material

### Official Documentation
- [Microsoft LINQ documentation](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)
- [Lambda expressions](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)
- [LINQ query syntax vs. method syntax](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/linq/query-syntax-and-method-syntax-in-linq)

### Tutorials and Examples
- [LINQ Standard Query Operators](https://www.tutorialsteacher.com/linq/linq-standard-query-operators)
- [101 LINQ Samples](https://www.tutorialsteacher.com/linq/sample-linq-queries)
- [C# LINQ Tutorial (w3schools)](https://www.w3schools.com/cs/cs_linq.php)
- [LINQ Tutorial (dotnettutorials.net)](https://dotnettutorials.net/course/linq/)

### Video Resources
- [LINQ Tutorial for Beginners (YouTube)](https://www.youtube.com/watch?v=z3PowDJKOSA)
- [C# LINQ Tutorial (Programming with Mosh)](https://www.youtube.com/watch?v=yClSNQdVD7g)

### Sample Code
- [Sample code (XAMK)](https://github.com/xamk-ture/OOP_Examples/blob/master/LinqExamples/Program.cs)
- [CollectionExamples (XAMK)](https://github.com/xamk-ture/AdvancedExamples/blob/master/CollectionExamples/Program.cs)

### Interactive Exercises
- [LINQPad](https://www.linqpad.net/) – free tool for testing LINQ queries
- [.NET Fiddle](https://dotnetfiddle.net/) – browser-based C# editor for LINQ experimentation

### Related Material
- [Lambda expressions](Lambda.md) – deep dive into lambda expressions
- [Delegates](Delegates.md) – how to use delegates and built-in delegate types
- [Predicates](Predicate.md) – predicate usage and examples
- [Closures](Closures.md) – variable capture and closures

