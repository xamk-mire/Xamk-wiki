# Async/Await — Asynchronous Programming

## Table of Contents

1. [Introduction](#introduction)
2. [Why Asynchronous Programming?](#why-asynchronous-programming)
3. [async and await Basics](#async-and-await-basics)
4. [Task and Task\<T\>](#task-and-taskt)
5. [Task.WhenAll and Task.WhenAny](#taskwhenall-and-taskwhenany)
6. [CancellationToken](#cancellationtoken)
7. [ValueTask](#valuetask)
8. [Error Handling in Async Code](#error-handling-in-async-code)
9. [Anti-patterns and Pitfalls](#anti-patterns-and-pitfalls)
10. [Best Practices](#best-practices)
11. [Summary](#summary)
12. [Useful Links](#useful-links)

---

## Introduction

**Asynchronous programming** allows long-running operations (database, HTTP, files) to be performed **without blocking the thread**. C#'s `async`/`await` model makes async code almost as readable as synchronous code.

**Basic idea:**

```
Synchronous (blocks):
  Thread: ████ [waiting for DB 200ms...] ████
                ↑ Thread is blocked!

Asynchronous (doesn't block):
  Thread: ████ → release thread → ████ (continue when DB responds)
               ↑ Thread does other work during wait
```

---

## Why Asynchronous Programming?

### Problem: Synchronous Code Blocks

```csharp
// ❌ Synchronous - blocks the thread
public string GetData()
{
    string result = httpClient.GetStringAsync("https://api.example.com/data").Result; // BLOCKS!
    return result;
}
```

**Problems:**
- Thread is blocked during the wait
- In web apps: fewer concurrent requests
- In UI apps: interface freezes
- Scalability suffers

### Solution: Asynchronous Code

```csharp
// ✅ Asynchronous - doesn't block the thread
public async Task<string> GetDataAsync()
{
    string result = await httpClient.GetStringAsync("https://api.example.com/data");
    return result;
}
```

**Benefits:**
- ✅ Thread is released during the wait
- ✅ Better scalability (more concurrent requests)
- ✅ UI stays responsive
- ✅ More efficient resource use

### Performance Comparison (ASP.NET Core)

| Metric | Synchronous | Asynchronous | Improvement |
|--------|-------------|--------------|-------------|
| Concurrent requests | 100 | 10,000+ | **100×** |
| Thread usage | 1 per request | Shared | **More efficient** |
| Memory usage | High | Low | **Significant** |

---

## async and await Basics

### Syntax

```csharp
// async keyword in method definition
// await keyword before asynchronous operation
public async Task<string> FetchDataAsync()
{
    string result = await FetchFromDatabase();
    return result;
}
```

**Rules:**
1. `async` keyword is added before the return type
2. Return type is `Task`, `Task<T>`, or `ValueTask<T>`
3. `await` can only be used inside an `async` method
4. Method name conventionally ends with `Async`

### Basic Example

```csharp
using System.Net.Http;

public class DataService
{
    private readonly HttpClient _httpClient = new();

    // Async method that returns a string
    public async Task<string> GetWeatherAsync(string city)
    {
        Console.WriteLine("Fetching weather data...");

        // await releases thread during wait
        string response = await _httpClient.GetStringAsync(
            $"https://api.weather.com/{city}");

        Console.WriteLine("Weather data received!");
        return response;
    }
}

// Usage
DataService service = new DataService();
string weather = await service.GetWeatherAsync("Helsinki");
Console.WriteLine(weather);
```

### Task vs Task\<T\> vs void

```csharp
// Task<T> - returns a value
public async Task<int> CalculateAsync()
{
    await Task.Delay(100);
    return 42;
}

// Task - no return value (like void, but awaitable)
public async Task SaveAsync(string data)
{
    await File.WriteAllTextAsync("data.txt", data);
}

// ❌ async void - AVOID! (except event handlers)
// Exceptions cannot be caught!
public async void DangerousMethod()
{
    await Task.Delay(100);
    throw new Exception("This cannot be caught!");
}
```

### How Does async/await Work?

```csharp
public async Task<string> ExampleAsync()
{
    Console.WriteLine("1. Before await");   // Executes on calling thread

    await Task.Delay(1000);                  // Thread released for 1s

    Console.WriteLine("2. After await");    // Executes on (possibly different) thread

    return "Done";
}
```

```
What happens under the hood:

1. Method starts normally
2. At await:
   a. Task not complete → method "pauses"
   b. Thread released back to ThreadPool
   c. Compiler creates state machine (IAsyncStateMachine)
3. When Task completes:
   a. Continue state machine from next state
   b. Thread (possibly different) resumes execution
```

---

## Task and Task\<T\>

### Task — Asynchronous Operation

`Task` represents an operation that is running or will complete in the future.

```csharp
// Task.Run — run CPU work on background thread
Task<int> computationTask = Task.Run(() =>
{
    // Heavy computation
    int sum = 0;
    for (int i = 0; i < 1_000_000; i++)
        sum += i;
    return sum;
});

int result = await computationTask;
Console.WriteLine($"Sum: {result}");
```

### Task.Delay — Asynchronous Wait

```csharp
// ✅ Task.Delay — doesn't block the thread
await Task.Delay(2000); // Wait 2 seconds asynchronously

// ❌ Thread.Sleep — blocks the thread
Thread.Sleep(2000); // Thread blocked for 2 seconds!
```

> **Tip:** See more [Thread.Sleep vs Task.Delay](../../00-Basics/Thread-Sleep.md)

### Task.Run — When to Use?

```csharp
// ✅ GOOD: CPU-intensive work in UI app
int result = await Task.Run(() => HeavyComputation());

// ❌ BAD: I/O operation in Task.Run (redundant)
string data = await Task.Run(() => httpClient.GetStringAsync(url)); // Don't do this!

// ✅ GOOD: I/O operation directly
string data = await httpClient.GetStringAsync(url);
```

**Rule of thumb:**
- `Task.Run` → CPU-intensive work
- Direct `await` → I/O operations (HTTP, database, files)

---

## Task.WhenAll and Task.WhenAny

### Task.WhenAll — Wait for All to Complete

```csharp
// Start three API calls SIMULTANEOUSLY
Task<string> task1 = httpClient.GetStringAsync("https://api.example.com/users");
Task<string> task2 = httpClient.GetStringAsync("https://api.example.com/products");
Task<string> task3 = httpClient.GetStringAsync("https://api.example.com/orders");

// Wait for all to complete
string[] results = await Task.WhenAll(task1, task2, task3);

Console.WriteLine($"Users: {results[0]}");
Console.WriteLine($"Products: {results[1]}");
Console.WriteLine($"Orders: {results[2]}");
```

**Execution time comparison:**

```
Sequentially (await one at a time):
  Task1: ████████ (200ms)
  Task2:         ████████ (200ms)
  Task3:                 ████████ (200ms)
  Total: 600ms

Concurrently (Task.WhenAll):
  Task1: ████████ (200ms)
  Task2: ████████ (200ms)
  Task3: ████████ (200ms)
  Total: 200ms ← 3× faster!
```

### Practical Example: Dashboard Data

```csharp
public async Task<DashboardDto> GetDashboardAsync(int userId)
{
    // Start all fetches AT THE SAME TIME
    Task<User> userTask = _userRepository.GetByIdAsync(userId);
    Task<List<Order>> ordersTask = _orderRepository.GetByUserIdAsync(userId);
    Task<UserStats> statsTask = _statsService.GetUserStatsAsync(userId);

    // Wait for all to complete
    await Task.WhenAll(userTask, ordersTask, statsTask);

    return new DashboardDto
    {
        User = userTask.Result,       // Already complete, doesn't block
        Orders = ordersTask.Result,
        Stats = statsTask.Result
    };
}
```

### Task.WhenAny — Wait for First to Complete

```csharp
// Use fastest API
Task<string> europeTask = httpClient.GetStringAsync("https://eu.api.example.com/data");
Task<string> usaTask = httpClient.GetStringAsync("https://us.api.example.com/data");

// Which responds first?
Task<string> fastest = await Task.WhenAny(europeTask, usaTask);
string result = await fastest;

Console.WriteLine($"Fastest responded: {result}");
```

### Task.WhenAny — Timeout Pattern

```csharp
public async Task<string?> FetchWithTimeoutAsync(string url, int timeoutMs)
{
    Task<string> dataTask = httpClient.GetStringAsync(url);
    Task timeoutTask = Task.Delay(timeoutMs);

    // Which completes first?
    Task completed = await Task.WhenAny(dataTask, timeoutTask);

    if (completed == timeoutTask)
    {
        Console.WriteLine("Timeout! Request took too long.");
        return null;
    }

    return await dataTask;
}
```

---

## CancellationToken

`CancellationToken` enables **cancelling** asynchronous operations.

### Basic Usage

```csharp
public async Task<string> FetchDataAsync(CancellationToken cancellationToken = default)
{
    // Check if cancelled
    cancellationToken.ThrowIfCancellationRequested();

    // Pass token forward
    string response = await httpClient.GetStringAsync(
        "https://api.example.com/data",
        cancellationToken);

    return response;
}
```

### CancellationTokenSource

```csharp
// Create CancellationTokenSource
using CancellationTokenSource cts = new CancellationTokenSource();

// Cancel automatically after 5 seconds
cts.CancelAfter(TimeSpan.FromSeconds(5));

try
{
    string data = await FetchDataAsync(cts.Token);
    Console.WriteLine(data);
}
catch (OperationCanceledException)
{
    Console.WriteLine("Operation cancelled (timeout).");
}
```

### Manual Cancellation

```csharp
using CancellationTokenSource cts = new CancellationTokenSource();

// Start long operation in background
Task task = LongOperationAsync(cts.Token);

// User presses Enter → cancel
Console.WriteLine("Press Enter to cancel...");
Console.ReadLine();
cts.Cancel();

try
{
    await task;
}
catch (OperationCanceledException)
{
    Console.WriteLine("Cancelled!");
}
```

### CancellationToken in ASP.NET Core

```csharp
// ASP.NET Core provides CancellationToken automatically
// which cancels when the user closes the connection
[HttpGet("products")]
public async Task<IActionResult> GetProducts(CancellationToken cancellationToken)
{
    List<Product> products = await _repository.GetAllAsync(cancellationToken);
    return Ok(products);
}

// Repository
public async Task<List<Product>> GetAllAsync(CancellationToken cancellationToken)
{
    return await _db.Products
        .AsNoTracking()
        .ToListAsync(cancellationToken);  // Pass token forward!
}
```

### CancellationToken — Linked Tokens

```csharp
// Combine multiple cancellation conditions
using CancellationTokenSource timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
using CancellationTokenSource linkedCts = CancellationTokenSource.CreateLinkedTokenSource(
    timeoutCts.Token,
    httpContext.RequestAborted  // User closes connection
);

// Cancels IF:
// 1. Timeout (30s) expires OR
// 2. User closes connection
await ProcessAsync(linkedCts.Token);
```

---

## ValueTask

`ValueTask<T>` is an optimized version of `Task<T>` for situations where the result is often **already available**.

### When to Use?

```csharp
// Example: Cache that often returns immediately
public ValueTask<Product?> GetProductAsync(int id)
{
    // 90% of the time: cache hit → no Task allocation needed
    if (_cache.TryGetValue(id, out Product? cached))
        return new ValueTask<Product?>(cached);  // No allocation!

    // 10% of the time: cache miss → fetch async
    return new ValueTask<Product?>(GetFromDatabaseAsync(id));
}

private async Task<Product?> GetFromDatabaseAsync(int id)
{
    Product? product = await _db.Products.FindAsync(id);
    _cache[id] = product;
    return product;
}
```

### Task vs ValueTask

| Property | `Task<T>` | `ValueTask<T>` |
|----------|-----------|----------------|
| **Allocation** | Always (heap) | None if result is immediately ready |
| **Await multiple times** | ✅ Yes | ❌ Only once! |
| **Store in variable** | ✅ Yes | ❌ Risky |
| **Usage** | Default choice | Optimization (hot path) |

**Rule of thumb:**
- Use `Task<T>` by default
- Use `ValueTask<T>` only when profiling shows the need (e.g. cache scenarios)

---

## Error Handling in Async Code

### try/catch Works Normally

```csharp
public async Task<string> FetchDataSafelyAsync()
{
    try
    {
        string data = await httpClient.GetStringAsync("https://api.example.com/data");
        return data;
    }
    catch (HttpRequestException ex)
    {
        Console.WriteLine($"HTTP error: {ex.Message}");
        return "Fallback data";
    }
    catch (TaskCanceledException)
    {
        Console.WriteLine("Request timed out.");
        return "Timeout";
    }
}
```

### Error Handling in Task.WhenAll

```csharp
Task<string> task1 = FetchAsync("https://api1.example.com");
Task<string> task2 = FetchAsync("https://api2.example.com");
Task<string> task3 = FetchAsync("https://api3.example.com");

try
{
    string[] results = await Task.WhenAll(task1, task2, task3);
}
catch (Exception ex)
{
    // NOTE: await throws only the first exception!
    Console.WriteLine($"Error: {ex.Message}");

    // Check all exceptions:
    if (task1.IsFaulted) Console.WriteLine($"Task1: {task1.Exception?.InnerException?.Message}");
    if (task2.IsFaulted) Console.WriteLine($"Task2: {task2.Exception?.InnerException?.Message}");
    if (task3.IsFaulted) Console.WriteLine($"Task3: {task3.Exception?.InnerException?.Message}");
}
```

### AggregateException

```csharp
Task task = Task.WhenAll(
    Task.Run(() => throw new InvalidOperationException("Error 1")),
    Task.Run(() => throw new ArgumentException("Error 2"))
);

try
{
    await task;
}
catch
{
    // task.Exception is AggregateException containing ALL errors
    if (task.Exception != null)
    {
        foreach (Exception ex in task.Exception.InnerExceptions)
        {
            Console.WriteLine($"Error: {ex.GetType().Name}: {ex.Message}");
        }
    }
}

// Output:
// Error: InvalidOperationException: Error 1
// Error: ArgumentException: Error 2
```

---

## Anti-patterns and Pitfalls

### 1. async void — DON'T USE

```csharp
// ❌ DANGEROUS: async void
public async void LoadData()
{
    string data = await httpClient.GetStringAsync(url);
    // If this throws → app crashes!
    // Exception CANNOT be caught in calling code!
}

// ✅ CORRECT: async Task
public async Task LoadDataAsync()
{
    string data = await httpClient.GetStringAsync(url);
}

// ✅ EXCEPTION: Event handlers (only OK use for async void)
button.Click += async (sender, e) =>
{
    await LoadDataAsync();
};
```

### 2. .Result and .Wait() — Deadlock Risk

```csharp
// ❌ DEADLOCK RISK (especially in ASP.NET and WPF)
public string GetData()
{
    // .Result blocks thread AND waits for Task to complete
    // But Task tries to return to the same thread → deadlock!
    string result = GetDataAsync().Result;
    return result;
}

// ❌ Same problem with .Wait()
public void SaveData()
{
    SaveDataAsync().Wait(); // Deadlock!
}

// ✅ CORRECT: async "bubbles up"
public async Task<string> GetDataAsync()
{
    return await httpClient.GetStringAsync(url);
}
```

### 3. Async Doesn't "Bubble Up" — Sync-over-async

```csharp
// ❌ BAD: Synchronous method calls async
public List<Product> GetProducts()
{
    // Blocks and can cause deadlock
    return GetProductsAsync().Result;
}

// ✅ GOOD: Make entire chain async
public async Task<List<Product>> GetProductsAsync()
{
    return await _repository.GetAllAsync();
}
```

**Rule of thumb:** Async bubbles up — when one method is async, the calling methods should also be async.

### 4. Unnecessary async/await

```csharp
// ❌ REDUNDANT: async/await does nothing useful
public async Task<int> GetIdAsync()
{
    return await _repository.GetIdAsync();  // Unnecessary wrapper
}

// ✅ BETTER: Return Task directly
public Task<int> GetIdAsync()
{
    return _repository.GetIdAsync();  // No unnecessary state machine
}

// ⚠️ BUT: If method has try/catch, using or other logic → use async/await
public async Task<int> GetIdSafelyAsync()
{
    try
    {
        return await _repository.GetIdAsync();
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Error!");
        return -1;
    }
}
```

### 5. await in Loop (N+1 Problem)

```csharp
// ❌ SLOW: Sequential calls in loop
foreach (int id in productIds)
{
    Product product = await _repository.GetByIdAsync(id);  // Waits for each!
    products.Add(product);
}

// ✅ FASTER: Concurrent calls
IEnumerable<Task<Product>> tasks = productIds.Select(id => _repository.GetByIdAsync(id));
Product[] products = await Task.WhenAll(tasks);

// ✅ OR: Single query that fetches all at once
List<Product> products = await _repository.GetByIdsAsync(productIds);
```

---

## Best Practices

### 1. Name Async Methods with Async Suffix

```csharp
// ✅ Clear naming
public async Task<User> GetUserAsync(int id) { ... }
public async Task SaveAsync(User user) { ... }
public async Task<List<Order>> GetOrdersAsync() { ... }
```

### 2. Always Pass CancellationToken Forward

```csharp
// ✅ Token flows through entire chain
public async Task<Product> GetProductAsync(int id, CancellationToken ct = default)
{
    Product? dbProduct = await _db.Products.FindAsync(new object[] { id }, ct);
    List<Review> reviews = await _reviewService.GetReviewsAsync(id, ct);
    return MapToProduct(dbProduct, reviews);
}
```

### 3. Use ConfigureAwait(false) in Libraries

```csharp
// In library code: no need for UI context
public async Task<string> GetDataAsync()
{
    string result = await httpClient.GetStringAsync(url)
        .ConfigureAwait(false);  // Don't return to original context
    return result;
}

// In ASP.NET Core: NOT needed (no SynchronizationContext)
// In WPF/WinForms: ConfigureAwait(false) in libraries
```

### 4. Avoid Unnecessary Task.Run Calls

```csharp
// ❌ Unnecessary Task.Run for I/O operation
List<Product> data = await Task.Run(() => _db.Products.ToListAsync());

// ✅ Direct await
List<Product> data = await _db.Products.ToListAsync();

// ✅ Task.Run only for CPU work
string hash = await Task.Run(() => ComputeExpensiveHash(data));
```

### 5. Dispose Resources Properly

```csharp
public async Task ProcessFileAsync(string path)
{
    // ✅ await using - asynchronous disposal
    await using FileStream stream = new FileStream(path, FileMode.Open, FileAccess.Read,
        FileShare.Read, bufferSize: 4096, useAsync: true);
    await using StreamReader reader = new StreamReader(stream);

    string content = await reader.ReadToEndAsync();
    Console.WriteLine(content);
}
```

---

## Summary

### Basics

| Principle | Explanation |
|-----------|-------------|
| `async Task<T>` | Async method that returns a value |
| `async Task` | Async method without return value |
| `await` | Wait for operation to complete, releasing thread |
| `Task.WhenAll` | Run multiple operations concurrently |
| `CancellationToken` | Cancel async operation |

### Checklist

1. **Don't use `async void`** — use `async Task`
2. **Don't use `.Result` or `.Wait()`** — use `await`
3. **Async bubbles up** — make entire call chain async
4. **Pass `CancellationToken`** — enables cancellation
5. **Use `Task.WhenAll`** — concurrent operations in parallel
6. **`Task.Run` only for CPU work** — direct `await` for I/O
7. **Name methods with `Async` suffix** — clear convention

---

## Useful Links

- [Microsoft: Asynchronous programming with async and await](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [Microsoft: Task-based asynchronous pattern (TAP)](https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap)
- [Stephen Cleary: Async Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
- [Microsoft: Cancellation in managed threads](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads)

### Next

- [Synchronization (lock, SemaphoreSlim)](Synchronization.md) — Learn to protect shared data in async code
