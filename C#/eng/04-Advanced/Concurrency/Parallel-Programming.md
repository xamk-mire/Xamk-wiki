# Parallel Programming

## Table of Contents

1. [Introduction](#introduction)
2. [When to Parallelize?](#when-to-parallelize)
3. [Parallel.For and Parallel.ForEach](#parallelfor-and-parallelforeach)
4. [Parallel.ForEachAsync](#parallelforeachasync)
5. [PLINQ (Parallel LINQ)](#plinq-parallel-linq)
6. [Task.Run and Manual Parallelization](#taskrun-and-manual-parallelization)
7. [Thread Safety in Parallel Code](#thread-safety-in-parallel-code)
8. [Best Practices](#best-practices)
9. [Summary](#summary)
10. [Useful Links](#useful-links)

---

## Introduction

**Parallel programming** means distributing work across **multiple processor cores** for simultaneous execution. This significantly speeds up **CPU-intensive** operations.

```
Sequential execution (1 core):
  Core 1: [Task 1][Task 2][Task 3][Task 4]
  Time: ████████████████████████ (4 seconds)

Parallel execution (4 cores):
  Core 1: [Task 1]
  Core 2: [Task 2]
  Core 3: [Task 3]
  Core 4: [Task 4]
  Time: ██████ (1 second) ← 4× faster!
```

---

## When to Parallelize?

### CPU-bound vs I/O-bound

| Type | Description | Solution | Example |
|------|-------------|----------|---------|
| **CPU-bound** | Processor does heavy work | `Parallel` / `Task.Run` | Image processing, calculation, compression |
| **I/O-bound** | Waiting for external resource | `async/await` | HTTP, database, files |

```csharp
// CPU-bound → Parallel
string[] images = Directory.GetFiles("images", "*.jpg");
Parallel.ForEach(images, image => ResizeImage(image));

// I/O-bound → async/await + Task.WhenAll
string[] urls = new[] { "https://api1.com", "https://api2.com", "https://api3.com" };
IEnumerable<Task<string>> tasks = urls.Select(url => httpClient.GetStringAsync(url));
string[] results = await Task.WhenAll(tasks);
```

### When NOT to Parallelize?

```csharp
// ❌ Too small work — parallelization overhead exceeds benefit
Parallel.For(0, 10, i =>
{
    int result = i * 2;  // Operation too fast!
});

// ✅ Sufficiently heavy work — parallelization pays off
Parallel.For(0, 10, i =>
{
    string hash = ComputeExpensiveHash(data[i]);  // Heavy computation
});
```

**Rules of thumb:**
- ✅ Parallelize when a single iteration takes **over 1ms**
- ✅ Parallelize when there are **hundreds or thousands** of elements
- ❌ Don't parallelize **a few fast operations**
- ❌ Don't parallelize **I/O operations** (use async/await)

---

## Parallel.For and Parallel.ForEach

### Parallel.For

```csharp
// Parallel for loop
Parallel.For(0, 1000, i =>
{
    int result = HeavyComputation(i);
    Console.WriteLine($"Done: {i}, result: {result}");
});

Console.WriteLine("All done!"); // Waits for all to complete
```

### Parallel.ForEach

```csharp
string[] files = Directory.GetFiles("data", "*.csv");

// Process files in parallel
Parallel.ForEach(files, file =>
{
    string data = File.ReadAllText(file);
    List<string[]> result = ParseCsv(data);
    Console.WriteLine($"Processed: {Path.GetFileName(file)}, rows: {result.Count}");
});
```

### ParallelOptions — Tune Parallelism

```csharp
ParallelOptions options = new ParallelOptions
{
    // Limit number of concurrent threads
    MaxDegreeOfParallelism = 4,  // Max 4 cores

    // CancellationToken for cancellation
    CancellationToken = cancellationToken
};

try
{
    Parallel.ForEach(data, options, item =>
    {
        ProcessItem(item);
    });
}
catch (OperationCanceledException)
{
    Console.WriteLine("Parallel execution cancelled.");
}
```

### MaxDegreeOfParallelism — Guidelines

```csharp
// CPU-intensive work: use all cores
MaxDegreeOfParallelism = Environment.ProcessorCount  // e.g. 8

// Leave room for other processes
MaxDegreeOfParallelism = Environment.ProcessorCount - 1  // 7

// Mixed I/O work: fewer
MaxDegreeOfParallelism = Environment.ProcessorCount / 2  // 4

// Test and measure! Default (-1) lets .NET decide
MaxDegreeOfParallelism = -1  // Default, usually good
```

### Parallel — Return Results

```csharp
// Parallel.ForEach doesn't return results directly
// Use ConcurrentBag or thread-local variables

ConcurrentBag<ProcessingResult> results = new ConcurrentBag<ProcessingResult>();

Parallel.ForEach(data, item =>
{
    ProcessingResult result = Process(item);
    results.Add(result);  // Thread-safe!
});

Console.WriteLine($"Processed {results.Count} items");
```

### Parallel — Local State (Thread-Local)

```csharp
// More efficient: thread-local sum (avoids unnecessary locking)
long totalSum = 0;

Parallel.For(0, 1_000_000,
    // Initialize thread-local variable
    () => 0L,

    // Execute (each thread computes into its own sum)
    (i, state, localSum) =>
    {
        return localSum + HeavyComputation(i);
    },

    // Combine thread-local sums
    localSum =>
    {
        Interlocked.Add(ref totalSum, localSum);
    }
);

Console.WriteLine($"Sum: {totalSum}");
```

---

## Parallel.ForEachAsync

.NET 6+ introduced `Parallel.ForEachAsync` which combines parallel execution with **async/await**.

### Basic Usage

```csharp
List<string> urls = Enumerable.Range(1, 100)
    .Select(i => $"https://api.example.com/items/{i}")
    .ToList();

await Parallel.ForEachAsync(urls, async (url, ct) =>
{
    string data = await httpClient.GetStringAsync(url, ct);
    Console.WriteLine($"Fetched: {url}, length: {data.Length}");
});
```

### ParallelOptions

```csharp
ParallelOptions options = new ParallelOptions
{
    MaxDegreeOfParallelism = 10,  // Max 10 concurrent
    CancellationToken = cancellationToken
};

await Parallel.ForEachAsync(urls, options, async (url, ct) =>
{
    HttpResponseMessage response = await httpClient.GetAsync(url, ct);
    response.EnsureSuccessStatusCode();
    string content = await response.Content.ReadAsStringAsync(ct);
    await ProcessContentAsync(content, ct);
});
```

### Practical Example: Bulk API Calls

```csharp
public class BulkApiProcessor
{
    private readonly HttpClient _httpClient;
    private readonly ConcurrentBag<ApiResult> _results = new();
    private int _processed = 0;

    public async Task<List<ApiResult>> ProcessBulkAsync(
        List<int> ids,
        int maxConcurrency = 20,
        CancellationToken ct = default)
    {
        ParallelOptions options = new ParallelOptions
        {
            MaxDegreeOfParallelism = maxConcurrency,
            CancellationToken = ct
        };

        await Parallel.ForEachAsync(ids, options, async (id, ct) =>
        {
            try
            {
                ApiResponse? response = await _httpClient.GetFromJsonAsync<ApiResponse>(
                    $"api/items/{id}", ct);

                _results.Add(new ApiResult(id, true, response));
            }
            catch (Exception ex)
            {
                _results.Add(new ApiResult(id, false, null, ex.Message));
            }
            finally
            {
                int count = Interlocked.Increment(ref _processed);
                if (count % 100 == 0)
                    Console.WriteLine($"Processed: {count}/{ids.Count}");
            }
        });

        return _results.ToList();
    }
}

public record ApiResult(int Id, bool Success, ApiResponse? Data, string? Error = null);
public record ApiResponse(string Name, decimal Value);
```

### Parallel.ForEachAsync vs Other Approaches

```csharp
List<int> items = Enumerable.Range(1, 100).ToList();

// ❌ Sequential — slow
foreach (int item in items)
{
    await ProcessAsync(item);
}
// → 100 × 100ms = 10,000ms

// ❌ Task.WhenAll all at once — may overload
IEnumerable<Task> tasks = items.Select(i => ProcessAsync(i));
await Task.WhenAll(tasks);
// → 100 concurrent! May be too much

// ✅ Parallel.ForEachAsync — controlled parallelism
await Parallel.ForEachAsync(items,
    new ParallelOptions { MaxDegreeOfParallelism = 10 },
    async (item, ct) => await ProcessAsync(item));
// → Max 10 concurrent, controlled load
```

---

## PLINQ (Parallel LINQ)

PLINQ (Parallel Language-Integrated Query) enables **automatic parallelization** of LINQ queries.

### Basic Usage — AsParallel()

```csharp
IEnumerable<int> numbers = Enumerable.Range(1, 1_000_000);

// Normal LINQ (sequential)
List<int> results = numbers
    .Where(n => IsPrime(n))
    .ToList();

// PLINQ (parallel) — just add AsParallel()!
List<int> parallelResults = numbers
    .AsParallel()
    .Where(n => IsPrime(n))
    .ToList();
```

### AsOrdered — Preserve Order

```csharp
// By default PLINQ does NOT guarantee order
List<int> results = data
    .AsParallel()
    .Select(x => Process(x))
    .ToList();  // Order may be arbitrary!

// AsOrdered preserves order
List<int> ordered = data
    .AsParallel()
    .AsOrdered()            // Preserve original order
    .Select(x => Process(x))
    .ToList();              // Same order as input
```

**Note:** `AsOrdered()` slows things down slightly because results must be ordered.

### WithDegreeOfParallelism — Limit Parallelism

```csharp
List<int> results = data
    .AsParallel()
    .WithDegreeOfParallelism(4)  // Max 4 threads
    .Select(x => HeavyComputation(x))
    .ToList();
```

### PLINQ — Aggregate Operations

```csharp
IEnumerable<int> numbers = Enumerable.Range(1, 10_000_000);

// Parallel sum
long sum = numbers
    .AsParallel()
    .Sum(n => (long)n);

// Parallel average
double average = numbers
    .AsParallel()
    .Average();

// Parallel grouping
Dictionary<string, int> groups = data
    .AsParallel()
    .GroupBy(x => x.Category)
    .ToDictionary(g => g.Key, g => g.Count());
```

### PLINQ — ForAll (Side Effects)

```csharp
// ForAll is faster than foreach for parallel results
data.AsParallel()
    .Where(x => x.IsActive)
    .ForAll(x =>
    {
        // ⚠️ Thread-safe operation!
        ProcessItem(x);
    });
```

### PLINQ — When to Use?

```csharp
// ✅ GOOD: Heavy computation on large dataset
List<int> primes = Enumerable.Range(2, 1_000_000)
    .AsParallel()
    .Where(n => IsPrime(n))  // CPU-intensive
    .ToList();

// ❌ BAD: Light operation (overhead > benefit)
List<int> doubled = Enumerable.Range(1, 100)
    .AsParallel()
    .Select(n => n * 2)  // Too fast!
    .ToList();

// ❌ BAD: I/O operations (use async)
List<string> results = urls
    .AsParallel()
    .Select(url => httpClient.GetStringAsync(url).Result)  // Blocks threads!
    .ToList();
```

### PLINQ — Exceptions

```csharp
try
{
    List<double> results = data
        .AsParallel()
        .Select(x =>
        {
            if (x < 0) throw new ArgumentException($"Negative: {x}");
            return Math.Sqrt(x);
        })
        .ToList();
}
catch (AggregateException ae)
{
    // PLINQ wraps exceptions in AggregateException
    foreach (Exception ex in ae.InnerExceptions)
    {
        Console.WriteLine($"Error: {ex.Message}");
    }
}
```

---

## Task.Run and Manual Parallelization

### Multiple Task.Run Calls in Parallel

```csharp
// Start multiple CPU tasks in parallel
Task<string> task1 = Task.Run(() => ComputeHash("data1"));
Task<string> task2 = Task.Run(() => ComputeHash("data2"));
Task<string> task3 = Task.Run(() => ComputeHash("data3"));

string[] results = await Task.WhenAll(task1, task2, task3);

Console.WriteLine($"Hash 1: {results[0]}");
Console.WriteLine($"Hash 2: {results[1]}");
Console.WriteLine($"Hash 3: {results[2]}");
```

### Task.Run — Long-Running Background Task

```csharp
// TaskCreationOptions.LongRunning — own thread for long task
Task task = Task.Factory.StartNew(() =>
{
    while (!cancellationToken.IsCancellationRequested)
    {
        ProcessQueue();
        Thread.Sleep(100);
    }
}, cancellationToken, TaskCreationOptions.LongRunning, TaskScheduler.Default);
```

### Task.Run vs Parallel vs PLINQ

| Method | Use case | Strength |
|--------|----------|----------|
| `Task.Run` + `WhenAll` | Few separate tasks | Simple, flexible |
| `Parallel.ForEach` | Large collection, CPU work | Automatic partitioning |
| `Parallel.ForEachAsync` | Large collection, async work | Controlled async parallelism |
| `PLINQ` | LINQ queries, aggregates | Declarative, easy |

---

## Thread Safety in Parallel Code

### Problem: Shared Mutable Data

```csharp
// ❌ DANGEROUS: Shared list
List<int> results = new List<int>();

Parallel.For(0, 1000, i =>
{
    results.Add(i * 2);  // Race condition! List is not thread-safe
});
// → IndexOutOfRangeException or corrupted data
```

### Solution 1: ConcurrentBag

```csharp
// ✅ Thread-safe collection
ConcurrentBag<int> results = new ConcurrentBag<int>();

Parallel.For(0, 1000, i =>
{
    results.Add(i * 2);  // Safe!
});
```

### Solution 2: Thread-Local + Combine

```csharp
// ✅ More efficient: Each thread collects its own results
ConcurrentBag<List<int>> allResults = new ConcurrentBag<List<int>>();

Parallel.ForEach(
    Partitioner.Create(0, 1000),
    () => new List<int>(),  // Thread-local list
    (range, state, localList) =>
    {
        for (int i = range.Item1; i < range.Item2; i++)
        {
            localList.Add(i * 2);  // No locking!
        }
        return localList;
    },
    localList => allResults.Add(localList)  // Combine at end
);

List<int> result = allResults.SelectMany(l => l).ToList();
```

### Solution 3: Interlocked for Single Values

```csharp
// ✅ Atomic counter
long sum = 0;

Parallel.For(0, 1_000_000, i =>
{
    Interlocked.Add(ref sum, i);
});

Console.WriteLine($"Sum: {sum}");
```

### Common Mistake: UI Update from Background Thread

```csharp
// ❌ WPF/WinForms: Cannot update UI from background thread
Parallel.ForEach(data, item =>
{
    string result = Process(item);
    label.Text = result;  // Crashes! Wrong thread!
});

// ✅ Return results and update UI on main thread
ConcurrentBag<string> results = new ConcurrentBag<string>();
await Task.Run(() =>
{
    Parallel.ForEach(data, item =>
    {
        results.Add(Process(item));
    });
});
// Now we're on UI thread
label.Text = string.Join(", ", results);
```

---

## Best Practices

### 1. Measure Before Parallelizing

```csharp
using System.Diagnostics;

Stopwatch sw = Stopwatch.StartNew();

// Sequential
foreach (object item in data)
    Process(item);
Console.WriteLine($"Sequential: {sw.ElapsedMilliseconds}ms");

sw.Restart();

// Parallel
Parallel.ForEach(data, item => Process(item));
Console.WriteLine($"Parallel: {sw.ElapsedMilliseconds}ms");

// Compare — parallelism is not always faster!
```

### 2. Use Partitioner for Large Collections

```csharp
// Partitioner splits data into larger chunks
// → Less overhead than one element at a time
Parallel.ForEach(
    Partitioner.Create(0, data.Length, data.Length / Environment.ProcessorCount),
    range =>
    {
        for (int i = range.Item1; i < range.Item2; i++)
        {
            Process(data[i]);
        }
    });
```

### 3. Avoid Excessive Parallelism

```csharp
// ❌ Too much: Nested parallelization
Parallel.ForEach(categories, category =>
{
    Parallel.ForEach(category.Products, product =>  // ❌ Too many threads!
    {
        Process(product);
    });
});

// ✅ Better: Parallelize only outer loop
Parallel.ForEach(categories, category =>
{
    foreach (Product product in category.Products)  // Sequential inside
    {
        Process(product);
    }
});
```

### 4. Support Cancellation

```csharp
CancellationTokenSource cts = new CancellationTokenSource();
ParallelOptions options = new ParallelOptions { CancellationToken = cts.Token };

try
{
    Parallel.ForEach(data, options, (item, state) =>
    {
        if (ShouldStop(item))
        {
            state.Stop();   // Stop soon (no new iterations)
            // OR
            state.Break();  // Stop after certain index
            return;
        }

        Process(item);
    });
}
catch (OperationCanceledException)
{
    Console.WriteLine("Cancelled.");
}
```

### 5. Choose the Right Tool

```
I/O operations (HTTP, DB, files)?
│
├─ Single calls? → async/await + Task.WhenAll
├─ Many calls? → Parallel.ForEachAsync
└─ Queue/stream? → Channel<T>

CPU computation?
│
├─ Large collection? → Parallel.ForEach
├─ LINQ query? → PLINQ (.AsParallel())
└─ Few tasks? → Task.Run + Task.WhenAll
```

---

## Summary

### Checklist

1. **`Parallel.ForEach`** — CPU-intensive parallel loop
2. **`Parallel.ForEachAsync`** — Asynchronous parallel loop (.NET 6+)
3. **`PLINQ` (AsParallel)** — Parallelizing LINQ queries
4. **`Task.Run` + `WhenAll`** — Parallelizing a few tasks
5. **`MaxDegreeOfParallelism`** — Limit concurrent threads

### Key Rules

- ✅ Parallelize **CPU-intensive work** (computation, image processing)
- ✅ Use **async/await** for I/O operations
- ✅ **Always measure** — parallelism is not always faster
- ✅ Use **ConcurrentBag** or **Interlocked** for shared data
- ✅ **Limit parallelism** (MaxDegreeOfParallelism)
- ❌ Don't parallelize **trivial work** (overhead > benefit)
- ❌ Don't use **nested Parallel loops**
- ❌ Don't use **plain List** in parallel code

---

## Useful Links

- [Microsoft: Parallel programming in .NET](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/)
- [Microsoft: Parallel.ForEach](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreach)
- [Microsoft: Parallel.ForEachAsync](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel.foreachasync)
- [Microsoft: Introduction to PLINQ](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/introduction-to-plinq)
- [Microsoft: Potential pitfalls in data and task parallelism](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/potential-pitfalls-in-data-and-task-parallelism)

### Related Topics

- [Async/Await](Async-Await.md) — Asynchronous programming
- [Synchronization](Synchronization.md) — lock, SemaphoreSlim, Interlocked
- [Concurrent Collections](Concurrent-Collections.md) — Thread-safe collections
