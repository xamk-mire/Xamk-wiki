# Thread-Safe Collections (Concurrent Collections)

## Table of Contents

1. [Introduction](#introduction)
2. [Why Concurrent Collections?](#why-concurrent-collections)
3. [ConcurrentDictionary](#concurrentdictionary)
4. [ConcurrentQueue and ConcurrentStack](#concurrentqueue-and-concurrentstack)
5. [ConcurrentBag](#concurrentbag)
6. [BlockingCollection](#blockingcollection)
7. [Channel](#channel)
8. [Comparison Table](#comparison-table)
9. [Summary](#summary)
10. [Useful Links](#useful-links)

---

## Introduction

The `System.Collections.Concurrent` namespace contains **thread-safe collections** designed for multithreading. They are safe to use from multiple threads **without separate locking**.

```csharp
using System.Collections.Concurrent;
```

---

## Why Concurrent Collections?

### Problem: Regular Collections Are Not Thread-Safe

```csharp
// ❌ DANGEROUS: Dictionary in multiple threads
Dictionary<int, string> dictionary = new Dictionary<int, string>();

// Parallel writes → InvalidOperationException or corrupted data!
Parallel.For(0, 1000, i =>
{
    dictionary[i] = $"Value {i}";  // ❌ Crashes!
});
```

### Solution 1: Dictionary + lock

```csharp
// ✅ Works, but slow (everyone waits for same lock)
Dictionary<int, string> dictionary = new Dictionary<int, string>();
object lockObj = new object();

Parallel.For(0, 1000, i =>
{
    lock (lockObj)
    {
        dictionary[i] = $"Value {i}";
    }
});
```

### Solution 2: ConcurrentDictionary (Better!)

```csharp
// ✅ Fast and safe (internal partitioned locking)
ConcurrentDictionary<int, string> dictionary = new ConcurrentDictionary<int, string>();

Parallel.For(0, 1000, i =>
{
    dictionary[i] = $"Value {i}";  // No lock needed!
});
```

### Performance Comparison

| Method | 1M operations (4 threads) | Safety |
|--------|---------------------------|--------|
| `Dictionary` (no lock) | ⚡ Fastest, but... | ❌ Crashes! |
| `Dictionary` + `lock` | ~300ms | ✅ Safe |
| `ConcurrentDictionary` | ~150ms | ✅ Safe |

---

## ConcurrentDictionary

`ConcurrentDictionary<TKey, TValue>` is the **most common concurrent collection**. It uses internal partitioned locking, so multiple threads can read and write different partitions simultaneously.

### Basic Usage

```csharp
ConcurrentDictionary<string, int> cache = new ConcurrentDictionary<string, int>();

// Add or update
cache["key1"] = 42;
cache.TryAdd("key2", 100);  // Add only if key doesn't exist

// Read
if (cache.TryGetValue("key1", out int value))
{
    Console.WriteLine($"Value: {value}");
}

// Remove
cache.TryRemove("key1", out _);
```

### GetOrAdd — Get or Add

```csharp
ConcurrentDictionary<string, List<string>> cache = new ConcurrentDictionary<string, List<string>>();

// If key exists → return value
// If not found → create new value, store and return
List<string> cities = cache.GetOrAdd("finland", key => new List<string>
{
    "Helsinki", "Tampere", "Turku"
});

Console.WriteLine($"Cities: {string.Join(", ", cities)}");
```

**Important note:** The `GetOrAdd` lambda may be called multiple times in parallel (factory is not locked), but only one result is stored.

```csharp
// ⚠️ Warning: Factory may be called multiple times!
List<string> result = cache.GetOrAdd("key", key =>
{
    Console.WriteLine("Factory called!");  // May print many times!
    return ExpensiveOperation(key);
});

// ✅ If factory is expensive, use Lazy<T>
ConcurrentDictionary<string, Lazy<ExpensiveResult>> lazyCache = new ConcurrentDictionary<string, Lazy<ExpensiveResult>>();

Lazy<ExpensiveResult> result = lazyCache.GetOrAdd("key",
    key => new Lazy<ExpensiveResult>(() => ExpensiveOperation(key)));

ExpensiveResult actualResult = result.Value;  // Factory called only once
```

### AddOrUpdate — Add or Update

```csharp
ConcurrentDictionary<string, int> wordCount = new ConcurrentDictionary<string, int>();

string[] words = { "cat", "dog", "cat", "bird", "cat", "dog" };

foreach (string word in words)
{
    wordCount.AddOrUpdate(
        word,
        addValue: 1,                       // If key doesn't exist → add with 1
        updateValueFactory: (key, old) => old + 1  // If key exists → increment
    );
}

// Output:
foreach (KeyValuePair<string, int> pair in wordCount)
{
    Console.WriteLine($"{pair.Key}: {pair.Value}");
}
// cat: 3
// dog: 2
// bird: 1
```

### ConcurrentDictionary — Practical Example: Rate Limiter

```csharp
public class SimpleRateLimiter
{
    private readonly ConcurrentDictionary<string, RequestInfo> _requests = new();
    private readonly int _maxRequests;
    private readonly TimeSpan _window;

    public SimpleRateLimiter(int maxRequests, TimeSpan window)
    {
        _maxRequests = maxRequests;
        _window = window;
    }

    public bool IsAllowed(string clientId)
    {
        DateTime now = DateTime.UtcNow;

        RequestInfo info = _requests.AddOrUpdate(
            clientId,
            // New client
            _ => new RequestInfo { Count = 1, WindowStart = now },
            // Existing client
            (_, existing) =>
            {
                if (now - existing.WindowStart > _window)
                {
                    // New time window
                    return new RequestInfo { Count = 1, WindowStart = now };
                }
                existing.Count++;
                return existing;
            });

        return info.Count <= _maxRequests;
    }

    private class RequestInfo
    {
        public int Count { get; set; }
        public DateTime WindowStart { get; set; }
    }
}

// Usage: max 100 requests per minute
SimpleRateLimiter limiter = new SimpleRateLimiter(100, TimeSpan.FromMinutes(1));

if (limiter.IsAllowed("client-123"))
    Console.WriteLine("Allowed");
else
    Console.WriteLine("Rate limit exceeded!");
```

---

## ConcurrentQueue and ConcurrentStack

### ConcurrentQueue\<T\> — FIFO (First In, First Out)

```csharp
ConcurrentQueue<string> queue = new ConcurrentQueue<string>();

// Add to queue (multiple threads can add simultaneously)
queue.Enqueue("Task 1");
queue.Enqueue("Task 2");
queue.Enqueue("Task 3");

// Take from queue (safe parallel use)
if (queue.TryDequeue(out string? task))
{
    Console.WriteLine($"Processing: {task}");
}

// Peek at next (doesn't remove)
if (queue.TryPeek(out string? next))
{
    Console.WriteLine($"Next: {next}");
}

Console.WriteLine($"In queue: {queue.Count}");
```

### Practical Example: Log Queue

```csharp
public class AsyncLogger
{
    private readonly ConcurrentQueue<string> _logQueue = new();
    private readonly CancellationTokenSource _cts = new();

    public AsyncLogger()
    {
        // Background thread processes log messages
        Task.Run(ProcessLogsAsync);
    }

    public void Log(string message)
    {
        _logQueue.Enqueue($"[{DateTime.Now:HH:mm:ss}] {message}");
    }

    private async Task ProcessLogsAsync()
    {
        while (!_cts.IsCancellationRequested)
        {
            while (_logQueue.TryDequeue(out string? message))
            {
                await File.AppendAllTextAsync("app.log", message + "\n");
            }

            await Task.Delay(100);  // Wait before next check
        }
    }

    public void Stop() => _cts.Cancel();
}
```

### ConcurrentStack\<T\> — LIFO (Last In, First Out)

```csharp
ConcurrentStack<int> stack = new ConcurrentStack<int>();

// Push onto stack
stack.Push(1);
stack.Push(2);
stack.Push(3);

// Pop from stack (latest first)
if (stack.TryPop(out int value))
{
    Console.WriteLine($"From stack: {value}");  // 3
}

// Pop multiple at once
int[] results = new int[2];
int popped = stack.TryPopRange(results);
Console.WriteLine($"Got {popped} items: {string.Join(", ", results.Take(popped))}");
```

---

## ConcurrentBag

`ConcurrentBag<T>` is an **unordered collection** optimized for scenarios where the same thread both adds and removes items.

```csharp
ConcurrentBag<string> bag = new ConcurrentBag<string>();

// Add (from multiple threads)
Parallel.For(0, 100, i =>
{
    bag.Add($"Item {i}");
});

Console.WriteLine($"Bag contains {bag.Count} items");

// Take one (order not guaranteed!)
if (bag.TryTake(out string? item))
{
    Console.WriteLine($"Took: {item}");
}
```

### When to Use ConcurrentBag?

- ✅ Same thread adds and removes (e.g. object pool)
- ✅ Order doesn't matter
- ❌ **Don't use** if you need FIFO order → `ConcurrentQueue`
- ❌ **Don't use** if different threads add and remove → `ConcurrentQueue`

### Example: Object Pool

```csharp
public class SimpleObjectPool<T>
{
    private readonly ConcurrentBag<T> _pool = new();
    private readonly Func<T> _factory;

    public SimpleObjectPool(Func<T> factory)
    {
        _factory = factory;
    }

    public T Rent()
    {
        return _pool.TryTake(out T? item) ? item : _factory();
    }

    public void Return(T item)
    {
        _pool.Add(item);
    }
}

// Usage: StringBuilder pool
SimpleObjectPool<StringBuilder> pool = new SimpleObjectPool<StringBuilder>(() => new StringBuilder());

StringBuilder sb = pool.Rent();
sb.Append("Hello");
string result = sb.ToString();
sb.Clear();
pool.Return(sb);  // Return to pool for reuse
```

---

## BlockingCollection

`BlockingCollection<T>` is a **higher-level producer-consumer collection**. It blocks the consumer until data is available and supports capacity limits.

### Basic Usage

```csharp
// Capacity: max 10 items at a time
using BlockingCollection<string> collection = new BlockingCollection<string>(boundedCapacity: 10);

// Producer (different thread)
Task producer = Task.Run(() =>
{
    for (int i = 0; i < 20; i++)
    {
        collection.Add($"Message {i}");  // Blocks if full!
        Console.WriteLine($"Produced: Message {i}");
    }
    collection.CompleteAdding();  // Mark complete
});

// Consumer (different thread)
Task consumer = Task.Run(() =>
{
    // GetConsumingEnumerable blocks and waits for new data
    foreach (string message in collection.GetConsumingEnumerable())
    {
        Console.WriteLine($"Consumed: {message}");
        Thread.Sleep(100);  // Simulate processing
    }
});

await Task.WhenAll(producer, consumer);
```

### Producer-Consumer Pattern with Multiple Consumers

```csharp
using BlockingCollection<WorkItem> workQueue = new BlockingCollection<WorkItem>(boundedCapacity: 100);

// Multiple producers
Task[] producers = Enumerable.Range(0, 3).Select(id =>
    Task.Run(() =>
    {
        for (int i = 0; i < 10; i++)
        {
            workQueue.Add(new WorkItem { Id = id * 10 + i, Data = $"Data-{id}-{i}" });
        }
    })).ToArray();

// Multiple consumers
Task[] consumers = Enumerable.Range(0, 2).Select(id =>
    Task.Run(() =>
    {
        foreach (WorkItem item in workQueue.GetConsumingEnumerable())
        {
            Console.WriteLine($"Worker {id}: Processing {item.Id}");
            Thread.Sleep(50);
        }
    })).ToArray();

await Task.WhenAll(producers);
workQueue.CompleteAdding();  // All produced
await Task.WhenAll(consumers);

record WorkItem { public int Id { get; init; } public string Data { get; init; } = ""; }
```

### BlockingCollection — Limitations

- **Blocks the thread** — no async support (`Add` and `Take` are synchronous)
- **Legacy practice** — `Channel<T>` is the modern replacement

---

## Channel

`Channel<T>` is **.NET's modern producer-consumer** solution. It supports `async/await` and is designed for asynchronous scenarios.

```csharp
using System.Threading.Channels;
```

### Basic Usage

```csharp
// Create bounded channel (max 100 messages)
Channel<string> channel = Channel.CreateBounded<string>(new BoundedChannelOptions(100)
{
    FullMode = BoundedChannelFullMode.Wait  // Wait if full
});

// Producer
Task producer = Task.Run(async () =>
{
    for (int i = 0; i < 50; i++)
    {
        await channel.Writer.WriteAsync($"Message {i}");
        Console.WriteLine($"Written: Message {i}");
    }
    channel.Writer.Complete();  // No more messages
});

// Consumer
Task consumer = Task.Run(async () =>
{
    await foreach (string message in channel.Reader.ReadAllAsync())
    {
        Console.WriteLine($"Read: {message}");
        await Task.Delay(50);
    }
});

await Task.WhenAll(producer, consumer);
```

### Channel — Unbounded vs Bounded

```csharp
// Unbounded: no upper limit (warning: memory can run out!)
Channel<string> unbounded = Channel.CreateUnbounded<string>();

// Bounded: max N items
Channel<string> bounded = Channel.CreateBounded<string>(new BoundedChannelOptions(100)
{
    // What to do when channel is full?
    FullMode = BoundedChannelFullMode.Wait,        // Wait (default)
    // FullMode = BoundedChannelFullMode.DropOldest,  // Drop oldest
    // FullMode = BoundedChannelFullMode.DropNewest,  // Drop newest
    // FullMode = BoundedChannelFullMode.DropWrite,   // Drop write

    SingleReader = true,   // Optimization: only one reader
    SingleWriter = false   // Multiple writers
});
```

### Channel — Practical Example: Background Processing

```csharp
public class BackgroundJobProcessor
{
    private readonly Channel<JobRequest> _channel;

    public BackgroundJobProcessor()
    {
        _channel = Channel.CreateBounded<JobRequest>(new BoundedChannelOptions(1000)
        {
            SingleReader = true
        });
    }

    // API calls this — returns immediately
    public async Task<bool> EnqueueJobAsync(JobRequest job, CancellationToken ct = default)
    {
        return _channel.Writer.TryWrite(job);
    }

    // Background process handles queue
    public async Task ProcessJobsAsync(CancellationToken ct)
    {
        await foreach (JobRequest job in _channel.Reader.ReadAllAsync(ct))
        {
            try
            {
                Console.WriteLine($"Processing: {job.Name}");
                await ProcessJobAsync(job, ct);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error: {ex.Message}");
            }
        }
    }

    private async Task ProcessJobAsync(JobRequest job, CancellationToken ct)
    {
        // Simulate work
        await Task.Delay(1000, ct);
        Console.WriteLine($"Done: {job.Name}");
    }
}

public record JobRequest(string Name, string Payload);
```

### Channel — ASP.NET Core Background Service

```csharp
// 1. Register in DI
builder.Services.AddSingleton(Channel.CreateBounded<EmailRequest>(100));
builder.Services.AddHostedService<EmailSenderService>();

// 2. Controller writes to channel
[ApiController]
[Route("api/[controller]")]
public class EmailController : ControllerBase
{
    private readonly Channel<EmailRequest> _channel;

    public EmailController(Channel<EmailRequest> channel)
    {
        _channel = channel;
    }

    [HttpPost]
    public async Task<IActionResult> SendEmail(EmailRequest request)
    {
        await _channel.Writer.WriteAsync(request);
        return Accepted();  // 202 — processing in background
    }
}

// 3. BackgroundService reads from channel
public class EmailSenderService : BackgroundService
{
    private readonly Channel<EmailRequest> _channel;

    public EmailSenderService(Channel<EmailRequest> channel)
    {
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        await foreach (EmailRequest request in _channel.Reader.ReadAllAsync(ct))
        {
            await SendEmailAsync(request);
        }
    }

    private async Task SendEmailAsync(EmailRequest request)
    {
        Console.WriteLine($"Sending email: {request.To}");
        await Task.Delay(500);  // Simulate sending
    }
}

public record EmailRequest(string To, string Subject, string Body);
```

### BlockingCollection vs Channel

| Property | `BlockingCollection<T>` | `Channel<T>` |
|----------|------------------------|--------------|
| **Async support** | ❌ Synchronous | ✅ Full async |
| **Performance** | Good | ⚡ Better |
| **Capacity handling** | Bounded | Flexible (Wait, Drop) |
| **Modern .NET** | Legacy | ✅ Recommended |
| **`await foreach`** | ❌ | ✅ |
| **Single reader/writer optimization** | ❌ | ✅ |

---

## Comparison Table

| Collection | Order | Duplicates | Async | Use case |
|------------|-------|------------|-------|----------|
| `ConcurrentDictionary<K,V>` | No | Key unique | No | Cache, lookup, counters |
| `ConcurrentQueue<T>` | FIFO | ✅ | No | Task queues, logging |
| `ConcurrentStack<T>` | LIFO | ✅ | No | Undo, redo stacks |
| `ConcurrentBag<T>` | No | ✅ | No | Object pool, same thread adds/removes |
| `BlockingCollection<T>` | FIFO* | ✅ | ❌ | Producer-consumer (synchronous) |
| `Channel<T>` | FIFO | ✅ | ✅ | Producer-consumer (asynchronous) |

\* BlockingCollection can use any `IProducerConsumerCollection<T>` underneath.

### Selection Guide

```
Need thread-safe collection?
│
├─ Key-value pairs?
│  └─ → ConcurrentDictionary<K,V>
│
├─ Producer-consumer?
│  ├─ Asynchronous (async/await)?
│  │  └─ → Channel<T>
│  └─ Synchronous?
│     └─ → BlockingCollection<T>
│
├─ FIFO queue?
│  └─ → ConcurrentQueue<T>
│
├─ LIFO stack?
│  └─ → ConcurrentStack<T>
│
└─ Object pool / order doesn't matter?
   └─ → ConcurrentBag<T>
```

---

## Summary

### Checklist

1. **`ConcurrentDictionary`** — Most common: cache, counters, lookup
2. **`ConcurrentQueue`** — FIFO queue for multiple threads
3. **`Channel<T>`** — Modern producer-consumer (prefer this!)
4. **`BlockingCollection`** — Older producer-consumer (synchronous)
5. **`ConcurrentBag`** — Object pool scenarios

### Key Rules

- ✅ Use `Concurrent*` collections with multiple threads
- ✅ Use `Channel<T>` for async producer-consumer needs
- ✅ `GetOrAdd` + `Lazy<T>` when factory is expensive
- ❌ Don't use plain `Dictionary` without locking in multithreading
- ❌ Don't assume order from `ConcurrentBag`

---

## Useful Links

- [Microsoft: System.Collections.Concurrent](https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent)
- [Microsoft: ConcurrentDictionary](https://learn.microsoft.com/en-us/dotnet/api/system.collections.concurrent.concurrentdictionary-2)
- [Microsoft: System.Threading.Channels](https://learn.microsoft.com/en-us/dotnet/core/extensions/channels)
- [Microsoft: Producer-consumer patterns](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)
- [Stephen Toub: Channels](https://devblogs.microsoft.com/dotnet/an-introduction-to-system-threading-channels/)

### Next

- [Parallel Programming](Parallel-Programming.md) — Leverage multiple cores with parallel execution
