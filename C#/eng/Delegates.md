# Delegates

[Official Microsoft documentation on delegates](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)

## What Is a Delegate?

A **delegate** is a C# type that represents a reference to one or more methods. You can think of a delegate as a variable that can store a function. This allows you to treat methods as data: you can store them in variables and pass them as parameters to other methods.

Delegates are especially useful for:

- **Callback functions** – when you want to pass a method to another method
- **Event handling** – reacting to events (e.g. button clicks)
- **LINQ queries** – filter and transform operations
- **Asynchronous programming** – when you want to execute some logic after an operation completes

## Defining and Using a Delegate

### Basic Syntax

```csharp
// 1. Define a delegate type
delegate void MyDelegate(string message);

// 2. Create a method matching the delegate signature
void PrintMessage(string message)
{
    Console.WriteLine(message);
}

// 3. Create a delegate instance and assign the method to it
MyDelegate del = PrintMessage;

// 4. Invoke the delegate
del("Hello, World!"); // Prints: Hello, World!
```

### Another Example: Math Operations

```csharp
// Delegate that takes two ints and returns an int
delegate int MathOperation(int a, int b);

// Methods matching the delegate signature
int Add(int a, int b) => a + b;
int Multiply(int a, int b) => a * b;

// Usage
MathOperation operation = Add;
Console.WriteLine(operation(5, 3)); // 8

operation = Multiply;
Console.WriteLine(operation(5, 3)); // 15
```

## Built-in Delegates: `Action`, `Func`, and `Predicate`

C# provides generic delegates that cover most use cases, so you rarely need to define your own delegate types.

### `Action<T>`

`Action` is a delegate that **does not return a value** (`void`). It can take 0–16 parameters.

```csharp
// Action without parameters
Action greet = () => Console.WriteLine("Hello!");
greet(); // Hello!

// Action with one parameter
Action<string> printName = name => Console.WriteLine($"Name: {name}");
printName("Alice"); // Name: Alice

// Action with two parameters
Action<int, int> printSum = (a, b) => Console.WriteLine($"Sum: {a + b}");
printSum(5, 3); // Sum: 8
```

### `Func<T, TResult>`

`Func` is a delegate that **returns a value**. The last type parameter is the return type.

```csharp
// Func that takes an int and returns a bool
Func<int, bool> isEven = number => number % 2 == 0;
Console.WriteLine(isEven(4)); // True
Console.WriteLine(isEven(5)); // False

// Func that takes two ints and returns an int
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(10, 5)); // 15

// Func with no parameters, returns a string
Func<string> getMessage = () => "Hello from Func!";
Console.WriteLine(getMessage()); // Hello from Func!
```

### `Predicate<T>`

`Predicate` is a delegate that takes one parameter and **always returns a `bool`**. It is commonly used in conditions and filtering.

```csharp
Predicate<int> isPositive = number => number > 0;
Console.WriteLine(isPositive(5));  // True
Console.WriteLine(isPositive(-3)); // False

// Using with List.FindAll
List<int> numbers = new List<int> { -2, -1, 0, 1, 2, 3 };
List<int> positiveNumbers = numbers.FindAll(isPositive);
// positiveNumbers = [1, 2, 3]
```

> **Note:** LINQ operations typically use `Func<T, bool>` rather than `Predicate<T>`, but `Predicate<T>` is still common with `List` methods and similar APIs.

## Delegates and LINQ

Delegates are at the core of LINQ. Most LINQ methods take a `Func` delegate as a parameter.

### Example: `Where` and `Select`

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Where takes a Func<int, bool>
Func<int, bool> isEven = n => n % 2 == 0;
var evenNumbers = numbers.Where(isEven).ToList();
// evenNumbers = [2, 4, 6]

// Select takes a Func<int, TResult>
Func<int, string> toText = n => $"Number: {n}";
var textNumbers = numbers.Select(toText).ToList();
// textNumbers = ["Number: 1", "Number: 2", ...]
```

### Example: Delegate as a Parameter

```csharp
// Method that takes a delegate as a parameter
void ProcessNumbers(List<int> numbers, Func<int, bool> filter)
{
    var filtered = numbers.Where(filter);
    foreach (var num in filtered)
    {
        Console.WriteLine(num);
    }
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Use different filters
ProcessNumbers(numbers, n => n > 3);       // 4, 5, 6
ProcessNumbers(numbers, n => n % 2 == 0);  // 2, 4, 6
```

> **More LINQ examples:** see [LINQ.md](LINQ.md)

## Multicast Delegates

A delegate can reference multiple methods at once. When the delegate is invoked, all attached methods are executed in order.

```csharp
delegate void Notify(string message);

void SendEmail(string message)
{
    Console.WriteLine($"Email sent: {message}");
}

void SendSMS(string message)
{
    Console.WriteLine($"SMS sent: {message}");
}

void LogMessage(string message)
{
    Console.WriteLine($"Logged: {message}");
}

// Combine multiple methods into the same delegate
Notify notifier = SendEmail;
notifier += SendSMS;      // Add second method
notifier += LogMessage;   // Add third method

// Invoke the delegate – all methods run
notifier("Important notification!");
// Output:
// Email sent: Important notification!
// SMS sent: Important notification!
// Logged: Important notification!

// Remove a method
notifier -= SendSMS;
notifier("Another notification!");
// Output:
// Email sent: Another notification!
// Logged: Another notification!
```

## Delegates and Events

Delegates form the basis of **events** in C#. Events use delegates to define which methods are called when the event is raised.

### Example: Simple Event

```csharp
public class Button
{
    // Delegate for the event
    public delegate void ClickHandler(string message);
    
    // Event
    public event ClickHandler Click;
    
    // Method that raises the event
    public void OnClick()
    {
        Click?.Invoke("Button was clicked!");
    }
}

// Usage
Button button = new Button();

// Attach event handlers
button.Click += message => Console.WriteLine($"Handler 1: {message}");
button.Click += message => Console.WriteLine($"Handler 2: {message}");

// Raise the event
button.OnClick();
// Output:
// Handler 1: Button was clicked!
// Handler 2: Button was clicked!
```

> **Note:** In modern C#, you will often use the built-in `EventHandler` or `EventHandler<T>` delegates instead of defining your own.

## Anonymous Methods and Lambda Expressions

Instead of defining a separate named method, you can use anonymous methods or lambda expressions.

### Anonymous Method (Older Style)

```csharp
delegate int MathOp(int a, int b);

MathOp add = delegate (int a, int b)
{
    return a + b;
};

Console.WriteLine(add(5, 3)); // 8
```

### Lambda Expression (Modern Style)

```csharp
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(5, 3)); // 8

// Multi-line lambda
Func<int, int, int> multiply = (a, b) =>
{
    Console.WriteLine($"Multiplying {a} and {b}");
    return a * b;
};
Console.WriteLine(multiply(4, 5)); // 20
```

> **More about lambda expressions:** see [Lambda.md](Lambda.md)

## Practical Examples

### Example 1: Callback Function

```csharp
void DownloadFile(string url, Action<string> onComplete)
{
    Console.WriteLine($"Downloading {url}...");
    // Simulate download
    System.Threading.Thread.Sleep(1000);
    string result = "File content";
    
    // Call the callback function
    onComplete(result);
}

// Usage
DownloadFile("http://example.com/file.txt", content =>
{
    Console.WriteLine($"Download complete! Content: {content}");
});
```

### Example 2: Strategy Pattern

```csharp
public class Calculator
{
    public int Calculate(int a, int b, Func<int, int, int> strategy)
    {
        return strategy(a, b);
    }
}

Calculator calc = new Calculator();

int sum = calc.Calculate(10, 5, (a, b) => a + b);        // 15
int difference = calc.Calculate(10, 5, (a, b) => a - b); // 5
int product = calc.Calculate(10, 5, (a, b) => a * b);    // 50
```

### Example 3: Validation

```csharp
public class Validator
{
    public bool Validate<T>(T value, Predicate<T> validationRule)
    {
        return validationRule(value);
    }
}

Validator validator = new Validator();

// Different validation rules
bool isValidAge = validator.Validate(25, age => age >= 18 && age <= 100);
bool isValidEmail = validator.Validate("test@example.com",
    email => email.Contains("@") && email.Contains("."));

Console.WriteLine($"Valid age: {isValidAge}");     // True
Console.WriteLine($"Valid email: {isValidEmail}"); // True
```

## When Should You Use Delegates?

| Use Case                 | Description                                 | Example                              |
|--------------------------|---------------------------------------------|--------------------------------------|
| **Callback functions**   | Run code when an operation completes        | File download, API calls             |
| **Event handling**       | UI events, notifications                    | Button clicks, data changes          |
| **LINQ operations**      | Filtering, mapping, aggregation             | `Where`, `Select`, `OrderBy`         |
| **Strategy pattern**     | Switch algorithms at runtime                | Sorting algorithms, payment methods  |
| **Dependency Injection** | Pass behavior as a dependency               | Testing, modular design              |

## Summary

- A **delegate** is a type that represents a reference to a method.
- **`Action`** = no return value (`void`).
- **`Func`** = returns a value.
- **`Predicate`** = returns a `bool`.
- Delegates allow you to **pass methods as parameters**.
- Delegates are the foundation of **events** in C#.
- **Lambda expressions** are the modern, concise way to create delegates.

## Useful Links

### Official Documentation

- [Delegates (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)
- [Using Delegates (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/using-delegates)
- [Events (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/)

### Tutorials

- [C# Delegates (w3schools)](https://www.w3schools.com/cs/cs_delegates.php)
- [Delegates Tutorial (TutorialsTeacher)](https://www.tutorialsteacher.com/csharp/csharp-delegates)
- [Action, Func, and Predicate (dotnettutorials.net)](https://dotnettutorials.net/lesson/action-func-predicate-delegates-csharp/)

### Video Resources

- [C# Delegates Explained (YouTube)](https://www.youtube.com/watch?v=jQgwEsJISy0)
- [Events and Delegates (YouTube)](https://www.youtube.com/watch?v=OuZrhykVytg)

### Related Material

- [Lambda Expressions](Lambda.md) – in-depth material on lambda expressions
- [Predicates](Predicate.md) – predicate usage and examples
- [Closures](Closures.md) – capturing variables and closures
- [LINQ](LINQ.md) – LINQ queries and data processing
- [Exception Handling](Exception-Handling.md) – working with exceptions

