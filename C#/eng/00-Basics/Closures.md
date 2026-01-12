# Closures

[Microsoft documentation on closures in lambda expressions](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions#capture-of-outer-variables-and-variable-scope-in-lambda-expressions)

## What Is a Closure?

A **closure** is a programming concept where a function (for example, a [lambda expression](Lambda.md)) *captures* or *remembers* variables from the environment in which it was defined. In other words, a lambda can use variables that are not its parameters, but come from an outer scope.

A closure allows a function to keep a reference to external variables even after the surrounding code has finished executing.

## Simple Example

```csharp
void Example()
{
    int multiplier = 3; // Outer variable
    
    Func<int, int> multiplyByThree = x => x * multiplier;
    // The lambda "captures" the multiplier variable
    
    Console.WriteLine(multiplyByThree(5));  // 15
    Console.WriteLine(multiplyByThree(10)); // 30
}
```

In this example:

- `multiplier` is an outer variable.
- The lambda expression `x => x * multiplier` uses this external variable.
- The lambda *captures* `multiplier` → **closure**.

## How Does a Closure Work?

When a lambda expression refers to an external variable, C# **does not copy** its value; instead it **keeps a reference** to that variable. This means:

1. The lambda sees changes made to the variable.
2. The lambda can also modify the variable.

### Example: Modifying a Variable

```csharp
void Example()
{
    int counter = 0; // Outer variable
    
    Action increment = () => counter++; // The lambda captures counter
    
    Console.WriteLine($"Counter: {counter}"); // 0
    increment();
    Console.WriteLine($"Counter: {counter}"); // 1
    increment();
    Console.WriteLine($"Counter: {counter}"); // 2
}
```

The lambda not only reads `counter`, it also modifies it.

## Closures and Changing Values

Because a closure points to the variable itself (not just its value), changes to the variable are visible inside the lambda:

```csharp
void Example()
{
    int multiplier = 2;
    
    Func<int, int> multiply = x => x * multiplier;
    
    Console.WriteLine(multiply(5)); // 10 (5 * 2)
    
    multiplier = 3; // Change multiplier
    
    Console.WriteLine(multiply(5)); // 15 (5 * 3)
    // The lambda sees the new value!
}
```

## Classic Pitfall: Loop Variable

One of the most common closure bugs in C# involves loop variables.

### ❌ Wrong Way (pre–C# 5.0)

```csharp
void Example()
{
    var actions = new List<Action>();
    
    for (int i = 0; i < 5; i++)
    {
        actions.Add(() => Console.WriteLine(i));
        // The lambda captures the variable i itself, not its VALUE!
    }
    
    foreach (var action in actions)
    {
        action(); // Prints: 5, 5, 5, 5, 5 (not 0, 1, 2, 3, 4!)
    }
}
```

**Why?** All lambdas refer to the **same** variable `i`. When the loop ends, `i` has the value 5, so all lambdas print 5.

### ✅ Correct Way: Copy Value to a Local Variable

```csharp
void Example()
{
    var actions = new List<Action>();
    
    for (int i = 0; i < 5; i++)
    {
        int localI = i; // Copy the value of i into a local variable
        actions.Add(() => Console.WriteLine(localI));
        // The lambda captures localI, which is unique for each iteration
    }
    
    foreach (var action in actions)
    {
        action(); // Prints: 0, 1, 2, 3, 4
    }
}
```

### ✅ C# 5.0+: `foreach` Is Safe

Starting from C# 5.0, the `foreach` loop variable behaves like a separate local variable per iteration:

```csharp
void Example()
{
    var numbers = new[] { 1, 2, 3, 4, 5 };
    var actions = new List<Action>();
    
    foreach (var num in numbers)
    {
        actions.Add(() => Console.WriteLine(num));
        // foreach creates a new variable for each iteration
    }
    
    foreach (var action in actions)
    {
        action(); // Prints: 1, 2, 3, 4, 5
    }
}
```

## Closures in Practice

### Example 1: Counter Factory

```csharp
Func<int> CreateCounter()
{
    int count = 0; // This variable "lives" inside the lambda
    
    return () =>
    {
        count++;
        return count;
    };
}

var counter1 = CreateCounter();
var counter2 = CreateCounter();

Console.WriteLine(counter1()); // 1
Console.WriteLine(counter1()); // 2
Console.WriteLine(counter1()); // 3

Console.WriteLine(counter2()); // 1 (different instance!)
Console.WriteLine(counter2()); // 2
```

Each call to `CreateCounter()` creates its own `count` variable which is captured by the lambda.

### Example 2: Multiplier Factory

```csharp
Func<int, int> CreateMultiplier(int factor)
{
    return x => x * factor; // factor is captured
}

var doubleValue = CreateMultiplier(2);
var tripleValue = CreateMultiplier(3);

Console.WriteLine(doubleValue(5));  // 10
Console.WriteLine(tripleValue(5));  // 15
```

### Example 3: Event Handler Capture

```csharp
void SetupButtons()
{
    var buttons = new List<Button>();
    
    for (int i = 0; i < 5; i++)
    {
        int buttonId = i; // Important: copy to local variable
        var button = new Button();
        
        button.Click += (sender, e) =>
        {
            Console.WriteLine($"Button {buttonId} clicked!");
        };
        
        buttons.Add(button);
    }
}
```

### Example 4: LINQ and Closures

```csharp
void FilterByMinimum(List<int> numbers, int minimum)
{
    // The lambda captures the minimum parameter
    var filtered = numbers.Where(n => n >= minimum).ToList();
    
    Console.WriteLine(string.Join(", ", filtered));
}

var numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

FilterByMinimum(numbers, 5); // 5, 6, 7, 8, 9, 10
FilterByMinimum(numbers, 8); // 8, 9, 10
```

### Example 5: Closure and State Management

```csharp
class Validator
{
    public Func<string, bool> CreateLengthValidator(int minLength, int maxLength)
    {
        // minLength and maxLength are captured
        return text =>
        {
            return text.Length >= minLength && text.Length <= maxLength;
        };
    }
}

var validator = new Validator();
var passwordValidator = validator.CreateLengthValidator(8, 20);
var usernameValidator = validator.CreateLengthValidator(3, 15);

Console.WriteLine(passwordValidator("abc123"));           // False (too short)
Console.WriteLine(passwordValidator("StrongPassword123")); // True
Console.WriteLine(usernameValidator("Bob"));               // True
```

## Closures and Memory

A closure keeps captured variables in memory as long as the lambda itself is alive. This can cause **memory leaks** if you are not careful.

### Things to Watch Out For

```csharp
class DataProcessor
{
    private List<Action> handlers = new List<Action>();
    
    public void AddHandler(string data)
    {
        // ⚠ Warning: the data variable stays in memory as long as the handler is in the list
        handlers.Add(() => Console.WriteLine(data));
    }
    
    public void Clear()
    {
        handlers.Clear(); // Release lambdas and captured variables
    }
}
```

If `AddHandler` is called thousands of times with large `data` values, they all stay in memory.

### Solution: Release Resources

```csharp
class DataProcessor
{
    private List<Action> handlers = new List<Action>();
    
    public void AddHandler(string data)
    {
        handlers.Add(() => Console.WriteLine(data));
    }
    
    public void ProcessAndClear()
    {
        foreach (var handler in handlers)
        {
            handler();
        }
        handlers.Clear(); // Release lambdas
    }
}
```

## Closures and Multithreading

Closures can cause **race conditions** in multithreaded programs, because multiple threads may access the same captured variable at the same time.

### ❌ Problem: Race Condition

```csharp
void Example()
{
    int counter = 0; // Shared variable
    
    var tasks = new List<Task>();
    
    for (int i = 0; i < 10; i++)
    {
        tasks.Add(Task.Run(() =>
        {
            for (int j = 0; j < 1000; j++)
            {
                counter++; // ⚠ Not thread-safe
            }
        }));
    }
    
    Task.WaitAll(tasks.ToArray());
    Console.WriteLine(counter); // May be less than 10000!
}
```

### ✅ Solution: `lock` or `Interlocked`

```csharp
void Example()
{
    int counter = 0;
    object lockObj = new object();
    
    var tasks = new List<Task>();
    
    for (int i = 0; i < 10; i++)
    {
        tasks.Add(Task.Run(() =>
        {
            for (int j = 0; j < 1000; j++)
            {
                lock (lockObj) // Protect critical section
                {
                    counter++;
                }
            }
        }));
    }
    
    Task.WaitAll(tasks.ToArray());
    Console.WriteLine(counter); // 10000
}
```

## Closures and Pure Functional Programming

In pure functional programming, lambdas **must not modify** external variables (no side effects). This makes code easier to test and reason about.

### ❌ Not Pure (Mutates State)

```csharp
int total = 0;
var numbers = new List<int> { 1, 2, 3, 4, 5 };

numbers.ForEach(n => total += n); // Side effect: modifies total
Console.WriteLine(total); // 15
```

### ✅ Pure (No Side Effects)

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

int total = numbers.Sum(); // No side effects
Console.WriteLine(total); // 15
```

## Best Practices

1. **Remember that a closure captures the variable, not its value**
   - The lambda sees changes to the variable.

2. **Be careful with loop variables**
   - Copy the loop variable to a local variable before creating a lambda (`for` loops).
   - `foreach` is safe starting with C# 5.0.

3. **Avoid side effects**
   - Avoid modifying external variables inside lambdas when possible.
   - Prefer lambdas that are “pure” functions.

4. **Watch memory usage**
   - Closures keep captured variables alive.
   - Release lambdas when they are no longer needed.

5. **Multithreading**
   - Protect shared variables with `lock` or `Interlocked`.
   - Consider using `ThreadLocal<T>` for thread-specific data.

6. **Testability**
   - Complex closures can make code harder to test.
   - Consider using named methods if the logic is complex.

## Summary

- A **closure** occurs when a lambda captures external variables.
- A lambda refers to the **variable**, not just its current value.
- **Loop variables**: be careful with `for` loops; use a local copy.
- **Memory**: closures keep captured variables in memory.
- **Multithreading**: protect shared captured variables.
- **Side effects**: avoid mutating external variables where possible.

## Useful Links

### Official Documentation

- [Lambda Expressions – Capture of Outer Variables (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions#capture-of-outer-variables-and-variable-scope-in-lambda-expressions)
- [Closures (Eric Lippert's Blog)](https://learn.microsoft.com/en-us/archive/blogs/ericlippert/closures-are-not-complicated)
- [Captured Variables (C# Programming Guide)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)

### Tutorials

- [Understanding Closures in C#](https://www.c-sharpcorner.com/article/closures-in-c-sharp/)
- [C# Closures Explained](https://www.tutorialsteacher.com/csharp/csharp-closures)

### Video Resources

- [C# Closures Explained (YouTube)](https://www.youtube.com/results?search_query=c%23+closures+explained)

### Related Material

- [Lambda Expressions](Lambda.md)
- [Delegates](Delegates.md)
- [LINQ](LINQ.md)
- [Scopes](Scopes.md)

