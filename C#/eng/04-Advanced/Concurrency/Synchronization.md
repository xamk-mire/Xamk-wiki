# Synchronization Mechanisms

## Table of Contents

1. [Introduction](#introduction)
2. [Why Synchronization?](#why-synchronization)
3. [lock](#lock)
4. [Monitor](#monitor)
5. [SemaphoreSlim](#semaphoreslim)
6. [Mutex](#mutex)
7. [ReaderWriterLockSlim](#readerwriterlockslim)
8. [Interlocked](#interlocked)
9. [Double-checked Locking](#double-checked-locking)
10. [Deadlock](#deadlock)
11. [Comparison Table](#comparison-table)
12. [Summary](#summary)
13. [Useful Links](#useful-links)

---

## Introduction

When multiple threads use **the same data**, **synchronization mechanisms** are needed to prevent race conditions and ensure data integrity.

**Problem without synchronization:**

```
Thread 1: Read counter (value: 10)
Thread 2: Read counter (value: 10)
Thread 1: Write counter (10 + 1 = 11)
Thread 2: Write counter (10 + 1 = 11)  ← Should be 12!
```

---

## Why Synchronization?

### Race Condition Example

```csharp
// ❌ DANGEROUS: No synchronization
public class Counter
{
    private int _value = 0;

    public void Increment()
    {
        _value++;  // NOT an atomic operation!
        // Behind the scenes: 1) Read _value  2) Add 1  3) Write _value
    }

    public int Value => _value;
}

// Test race condition
Counter counter = new Counter();
IEnumerable<Task> tasks = Enumerable.Range(0, 1000).Select(_ =>
    Task.Run(() => counter.Increment()));

await Task.WhenAll(tasks);
Console.WriteLine($"Expected: 1000, Actual: {counter.Value}");
// Output: Expected: 1000, Actual: 987 (or some other value <1000)
```

---

## lock

`lock` is the **simplest synchronization mechanism**. It ensures that only one thread at a time executes the protected code block.

### Basic Usage

```csharp
public class ThreadSafeCounter
{
    private int _value = 0;
    private readonly object _lock = new();  // Lock object

    public void Increment()
    {
        lock (_lock)  // Only one thread at a time
        {
            _value++;  // Now safe!
        }
    }

    public int Value
    {
        get
        {
            lock (_lock)
            {
                return _value;
            }
        }
    }
}

// Now it works correctly!
ThreadSafeCounter counter = new ThreadSafeCounter();
IEnumerable<Task> tasks = Enumerable.Range(0, 1000).Select(_ =>
    Task.Run(() => counter.Increment()));

await Task.WhenAll(tasks);
Console.WriteLine($"Value: {counter.Value}");
// Output: Value: 1000 ✅
```

### How Does lock Work?

```
Thread 1: lock(_lock) → Acquire lock → Execute code → Release lock
Thread 2: lock(_lock) → WAITING... → Acquire lock → Execute code → Release
Thread 3: lock(_lock) → WAITING.............. → Acquire lock → Execute → Release
```

### lock Rules

```csharp
// ✅ GOOD: Use private readonly object
private readonly object _lock = new();

// ❌ BAD: Lock on this
lock (this)  // Anyone can lock the same object from outside!
{
    // ...
}

// ❌ BAD: Lock on type
lock (typeof(MyClass))  // Global lock, affects all instances!
{
    // ...
}

// ❌ BAD: Lock on string
lock ("myLock")  // String interning: same "myLock" is same object!
{
    // ...
}
```

### lock C# 13 (.NET 9) — System.Threading.Lock

```csharp
// C# 13 introduces dedicated Lock type
public class ModernCounter
{
    private int _value = 0;
    private readonly Lock _lock = new();  // System.Threading.Lock

    public void Increment()
    {
        lock (_lock)  // Compiler optimizes automatically
        {
            _value++;
        }
    }

    // Can also use Scope syntax
    public void IncrementScope()
    {
        using (_lock.EnterScope())
        {
            _value++;
        }
    }
}
```

### lock Limitations

- **Does not support `await`** — cannot use `await` inside lock block
- **Blocks the thread** — waiting thread does nothing else
- **Within single process only** — does not work across processes

```csharp
// ❌ DOESN'T WORK: await inside lock
lock (_lock)
{
    await Task.Delay(100);  // Compile error!
}

// ✅ Use SemaphoreSlim for asynchronous locking
await _semaphore.WaitAsync();
try
{
    await Task.Delay(100);  // Works!
}
finally
{
    _semaphore.Release();
}
```

---

## Monitor

`lock` is syntactic sugar for the `Monitor` class. `Monitor` provides more control.

### lock vs Monitor

```csharp
// These are identical:

// lock version
lock (_lock)
{
    // Critical section
}

// Monitor version (what the compiler does)
Monitor.Enter(_lock);
try
{
    // Critical section
}
finally
{
    Monitor.Exit(_lock);
}
```

### Monitor.TryEnter — Timeout

```csharp
private readonly object _lock = new();

public bool TryIncrement(int timeoutMs = 1000)
{
    // Try to acquire lock within given time
    if (Monitor.TryEnter(_lock, TimeSpan.FromMilliseconds(timeoutMs)))
    {
        try
        {
            _value++;
            return true;
        }
        finally
        {
            Monitor.Exit(_lock);
        }
    }

    Console.WriteLine("Could not acquire lock — timeout!");
    return false;
}
```

### Monitor.Wait and Monitor.Pulse — Producer-Consumer

```csharp
public class SimpleQueue<T>
{
    private readonly Queue<T> _queue = new();
    private readonly object _lock = new();

    public void Add(T item)
    {
        lock (_lock)
        {
            _queue.Enqueue(item);
            Monitor.Pulse(_lock);  // Wake waiting thread
        }
    }

    public T Take()
    {
        lock (_lock)
        {
            // Wait until queue has something
            while (_queue.Count == 0)
            {
                Monitor.Wait(_lock);  // Release lock and wait
            }

            return _queue.Dequeue();
        }
    }
}
```

---

## SemaphoreSlim

`SemaphoreSlim` is the **most versatile synchronization mechanism**:
- Supports `await` (asynchronous locking)
- Limits number of concurrent accesses
- Lighter than `Semaphore`

### Asynchronous Locking (Replaces lock in async code)

```csharp
public class ThreadSafeCache
{
    private readonly Dictionary<string, string> _cache = new();
    private readonly SemaphoreSlim _semaphore = new(1, 1);  // Max 1 at a time

    public async Task<string> GetOrAddAsync(string key, Func<Task<string>> factory)
    {
        await _semaphore.WaitAsync();  // ✅ Asynchronous locking!
        try
        {
            if (_cache.TryGetValue(key, out string? cached))
                return cached;

            string value = await factory();  // ✅ Can use await!
            _cache[key] = value;
            return value;
        }
        finally
        {
            _semaphore.Release();
        }
    }
}
```

### Limited Concurrency

```csharp
// Limit: max 5 concurrent HTTP calls
private readonly SemaphoreSlim _httpThrottle = new(5, 5);

public async Task<string[]> FetchAllAsync(string[] urls)
{
    IEnumerable<Task<string>> tasks = urls.Select(async url =>
    {
        await _httpThrottle.WaitAsync();  // Wait for turn
        try
        {
            Console.WriteLine($"Fetching: {url}");
            return await httpClient.GetStringAsync(url);
        }
        finally
        {
            _httpThrottle.Release();  // Release slot for next
        }
    });

    return await Task.WhenAll(tasks);
}

// Example: 20 URLs, max 5 concurrently
string[] urls = Enumerable.Range(1, 20)
    .Select(i => $"https://api.example.com/item/{i}")
    .ToArray();

string[] results = await FetchAllAsync(urls);
```

```
Execution (max 5 concurrent):
  Batch 1: [1] [2] [3] [4] [5]  ← 5 concurrent
  Batch 2: [6] [7] [8] [9] [10] ← Next 5
  Batch 3: [11][12][13][14][15]
  Batch 4: [16][17][18][19][20]
```

### SemaphoreSlim — Timeout and CancellationToken

```csharp
private readonly SemaphoreSlim _semaphore = new(1, 1);

public async Task<bool> TryLockAsync(CancellationToken ct)
{
    // Try to acquire lock within 5 seconds, respect cancellation
    bool acquired = await _semaphore.WaitAsync(
        TimeSpan.FromSeconds(5),
        ct);

    if (!acquired)
    {
        Console.WriteLine("Timeout — could not acquire lock!");
        return false;
    }

    try
    {
        await DoWorkAsync(ct);
        return true;
    }
    finally
    {
        _semaphore.Release();
    }
}
```

### SemaphoreSlim — Cache Stampede Protection

```csharp
// Prevent "cache stampede": only one fetch at a time per key
public class StampedeGuardedCache
{
    private readonly IMemoryCache _cache;
    private readonly ConcurrentDictionary<string, SemaphoreSlim> _locks = new();

    public async Task<T> GetOrCreateAsync<T>(
        string key,
        Func<Task<T>> factory,
        TimeSpan expiration)
    {
        if (_cache.TryGetValue(key, out T? cached))
            return cached!;

        // Own semaphore per key
        SemaphoreSlim semaphore = _locks.GetOrAdd(key, _ => new SemaphoreSlim(1, 1));
        await semaphore.WaitAsync();
        try
        {
            // Double-check: someone else might have already fetched
            if (_cache.TryGetValue(key, out cached))
                return cached!;

            T value = await factory();
            _cache.Set(key, value, expiration);
            return value;
        }
        finally
        {
            semaphore.Release();
        }
    }
}
```

---

## Mutex

`Mutex` is a synchronization mechanism that works **across processes**. Used less often than `lock` or `SemaphoreSlim`.

### Use Case: Only One Instance of Application

```csharp
// Prevent multiple instances of the same application
using Mutex mutex = new Mutex(false, "Global\\MyApp_UniqueId");

if (!mutex.WaitOne(0))
{
    Console.WriteLine("Application is already running!");
    return;
}

try
{
    Console.WriteLine("Application started.");
    // Normal application execution...
    Console.ReadLine();
}
finally
{
    mutex.ReleaseMutex();
}
```

### Mutex vs lock vs SemaphoreSlim

| Property | `lock` | `SemaphoreSlim` | `Mutex` |
|----------|--------|-----------------|---------|
| **Async support** | ❌ | ✅ | ❌ |
| **Cross-process** | ❌ | ❌ | ✅ |
| **Max concurrent** | 1 | N (configurable) | 1 |
| **Performance** | ⚡ Fastest | ⚡ Fast | 🐢 Slow |
| **Use case** | Simple locking | Async + throttling | Cross-process |

---

## ReaderWriterLockSlim

`ReaderWriterLockSlim` **separates readers and writers**: multiple threads can read simultaneously, but writes are exclusive.

### Basic Usage

```csharp
public class ThreadSafeRegistry
{
    private readonly Dictionary<string, string> _data = new();
    private readonly ReaderWriterLockSlim _rwLock = new();

    // Multiple threads can read SIMULTANEOUSLY
    public string? Read(string key)
    {
        _rwLock.EnterReadLock();
        try
        {
            return _data.TryGetValue(key, out string? value) ? value : null;
        }
        finally
        {
            _rwLock.ExitReadLock();
        }
    }

    // Only ONE thread at a time can write
    public void Write(string key, string value)
    {
        _rwLock.EnterWriteLock();
        try
        {
            _data[key] = value;
        }
        finally
        {
            _rwLock.ExitWriteLock();
        }
    }

    // Upgradeable: Read first, write if needed
    public string ReadAndUpdate(string key, string defaultValue)
    {
        _rwLock.EnterUpgradeableReadLock();
        try
        {
            if (_data.TryGetValue(key, out string? value))
                return value;

            // Need to write
            _rwLock.EnterWriteLock();
            try
            {
                _data[key] = defaultValue;
                return defaultValue;
            }
            finally
            {
                _rwLock.ExitWriteLock();
            }
        }
        finally
        {
            _rwLock.ExitUpgradeableReadLock();
        }
    }
}
```

### When to Use ReaderWriterLockSlim?

```
Many reads, few writes:
  Reader 1: ████ ████ ████ ████  (simultaneously!)
  Reader 2: ████ ████ ████ ████
  Writer:        ██                (exclusive)
  Reader 3: ████      ████ ████

→ Readers don't block each other
→ Writer blocks everyone
```

**Use when:**
- Reads far outnumber writes (e.g. 90% read, 10% write)
- Read operations are fast

**Don't use when:**
- Read/write ratio is balanced → use `lock`
- Need async support → use `SemaphoreSlim`

---

## Interlocked

The `Interlocked` class provides **atomic operations** for simple values. No locks needed!

### Basic Usage

```csharp
public class AtomicCounter
{
    private int _value = 0;

    // ✅ Atomic increment (no lock needed!)
    public void Increment()
    {
        Interlocked.Increment(ref _value);
    }

    // ✅ Atomic decrement
    public void Decrement()
    {
        Interlocked.Decrement(ref _value);
    }

    // ✅ Atomic add
    public void Add(int amount)
    {
        Interlocked.Add(ref _value, amount);
    }

    // ✅ Atomic read
    public int Value => Interlocked.CompareExchange(ref _value, 0, 0);
}
```

### CompareExchange — Conditional Update

```csharp
// "If value is X, change it to Y"
// Atomic operation, no lock needed

public class AtomicMax
{
    private int _max = int.MinValue;

    public void UpdateMax(int newValue)
    {
        int current;
        do
        {
            current = _max;
            if (newValue <= current)
                return;  // No need to update
        }
        while (Interlocked.CompareExchange(ref _max, newValue, current) != current);
        // If someone else changed _max in between → retry
    }

    public int Max => _max;
}
```

### Interlocked — Use Cases

```csharp
// Concurrent request counter
public class RequestCounter
{
    private long _totalRequests = 0;
    private int _activeRequests = 0;

    public async Task<T> TrackRequestAsync<T>(Func<Task<T>> handler)
    {
        Interlocked.Increment(ref _totalRequests);
        Interlocked.Increment(ref _activeRequests);
        try
        {
            return await handler();
        }
        finally
        {
            Interlocked.Decrement(ref _activeRequests);
        }
    }

    public long TotalRequests => Interlocked.Read(ref _totalRequests);
    public int ActiveRequests => _activeRequests;
}
```

### Interlocked vs lock

| Property | `Interlocked` | `lock` |
|----------|---------------|--------|
| **Performance** | ⚡⚡ Very fast | ⚡ Fast |
| **Use case** | Single values (int, long) | Complex logic |
| **Complexity** | Simple | Simple |
| **Multiple operations** | ❌ Only one at a time | ✅ Multiple operations |

---

## Double-checked Locking

**Double-checked locking** is an optimization technique that avoids unnecessary locking.

### Typical Example: Lazy Initialization

```csharp
public class SingletonService
{
    private static SingletonService? _instance;
    private static readonly object _lock = new();

    // ❌ BAD: Locks on EVERY call
    public static SingletonService InstanceBad
    {
        get
        {
            lock (_lock)
            {
                if (_instance == null)
                    _instance = new SingletonService();
                return _instance;
            }
        }
    }

    // ✅ GOOD: Double-checked locking
    public static SingletonService Instance
    {
        get
        {
            if (_instance == null)  // 1st check (no lock)
            {
                lock (_lock)
                {
                    if (_instance == null)  // 2nd check (inside lock)
                    {
                        _instance = new SingletonService();
                    }
                }
            }
            return _instance;
        }
    }

    // ✅ BEST: Use Lazy<T>
    private static readonly Lazy<SingletonService> _lazy =
        new(() => new SingletonService());

    public static SingletonService InstanceBest => _lazy.Value;
}
```

### Lazy\<T\> — Easiest Way

```csharp
public class AppConfig
{
    // Lazy<T> handles thread safety automatically
    private static readonly Lazy<AppConfig> _instance =
        new(() => new AppConfig());

    public static AppConfig Instance => _instance.Value;

    // Also in async context
    private readonly Lazy<Task<List<string>>> _cities;

    public AppConfig()
    {
        _cities = new Lazy<Task<List<string>>>(
            () => FetchCitiesAsync());
    }

    public Task<List<string>> Cities => _cities.Value;

    private async Task<List<string>> FetchCitiesAsync()
    {
        // Fetch only once
        return await httpClient.GetFromJsonAsync<List<string>>(
            "https://api.example.com/cities") ?? new();
    }
}
```

---

## Deadlock

**Deadlock** occurs when two (or more) threads wait for each other forever.

### Classic Deadlock

```csharp
// ❌ DEADLOCK!
private readonly object _lockA = new();
private readonly object _lockB = new();

// Thread 1
public void Method1()
{
    lock (_lockA)           // 1. Acquire lock A
    {
        Thread.Sleep(100);   // Simulate work
        lock (_lockB)       // 3. Wait for lock B... (Thread 2 has it!)
        {
            Console.WriteLine("Method1 done");
        }
    }
}

// Thread 2
public void Method2()
{
    lock (_lockB)           // 2. Acquire lock B
    {
        Thread.Sleep(100);   // Simulate work
        lock (_lockA)       // 4. Wait for lock A... (Thread 1 has it!)
        {
            Console.WriteLine("Method2 done");
        }
    }
}

// Run → DEADLOCK!
Task.Run(() => Method1());
Task.Run(() => Method2());
```

```
Deadlock situation:

  Thread 1: Owns A, waiting for B ──────┐
                                        │
  Thread 2: Owns B, waiting for A ──┐   │
                                    │   │
            ┌───────────────────────┘   │
            │  ┌────────────────────────┘
            ▼  ▼
         INFINITE WAIT!
```

### Avoiding Deadlock

```csharp
// ✅ Solution 1: Always acquire locks in SAME order
public void Method1Fixed()
{
    lock (_lockA)       // Always A first
    {
        lock (_lockB)   // Then B
        {
            Console.WriteLine("Method1 done");
        }
    }
}

public void Method2Fixed()
{
    lock (_lockA)       // Always A first (same order!)
    {
        lock (_lockB)   // Then B
        {
            Console.WriteLine("Method2 done");
        }
    }
}
```

```csharp
// ✅ Solution 2: Use Monitor.TryEnter with timeout
public bool SaferMethod()
{
    lock (_lockA)
    {
        if (Monitor.TryEnter(_lockB, TimeSpan.FromSeconds(5)))
        {
            try
            {
                Console.WriteLine("Done!");
                return true;
            }
            finally
            {
                Monitor.Exit(_lockB);
            }
        }
        else
        {
            Console.WriteLine("Could not acquire lock B — possible deadlock!");
            return false;
        }
    }
}
```

```csharp
// ✅ Solution 3: Use single lock
private readonly object _commonLock = new();

public void Method1Simple()
{
    lock (_commonLock)
    {
        // All critical code under one lock
        Console.WriteLine("Done");
    }
}
```

### async/await Deadlock

```csharp
// ❌ DEADLOCK (WPF/WinForms, legacy ASP.NET)
public void Button_Click(object sender, EventArgs e)
{
    // .Result blocks UI thread
    // GetDataAsync tries to return to UI thread → deadlock!
    string data = GetDataAsync().Result;
}

// ✅ SOLUTION 1: Use async/await
public async void Button_Click(object sender, EventArgs e)
{
    string data = await GetDataAsync();
}

// ✅ SOLUTION 2: ConfigureAwait(false) in library
public async Task<string> GetDataAsync()
{
    return await httpClient.GetStringAsync(url)
        .ConfigureAwait(false);  // Don't require UI thread
}
```

---

## Comparison Table

| Mechanism | Async | Cross-process | Max concurrent | Performance | Use case |
|-----------|-------|---------------|----------------|-------------|----------|
| `lock` | ❌ | ❌ | 1 | ⚡⚡⚡ | Simple locking |
| `Monitor` | ❌ | ❌ | 1 | ⚡⚡⚡ | lock + timeout + Wait/Pulse |
| `SemaphoreSlim` | ✅ | ❌ | N | ⚡⚡ | Async locking, throttling |
| `Mutex` | ❌ | ✅ | 1 | ⚡ | Cross-process locking |
| `ReaderWriterLockSlim` | ❌ | ❌ | N readers / 1 writer | ⚡⚡ | Read-heavy scenarios |
| `Interlocked` | - | ❌ | - | ⚡⚡⚡⚡ | Atomic single values |
| `Lazy<T>` | ✅ | ❌ | - | ⚡⚡⚡ | Lazy initialization |

### Selection Guide

```
Need synchronization?
│
├─ Single value (int, long)?
│  └─ → Interlocked
│
├─ Need await inside lock?
│  └─ → SemaphoreSlim(1, 1)
│
├─ Limited concurrency (max N)?
│  └─ → SemaphoreSlim(N, N)
│
├─ Many reads, few writes?
│  └─ → ReaderWriterLockSlim
│
├─ Cross-process locking?
│  └─ → Mutex
│
├─ Lazy initialization?
│  └─ → Lazy<T>
│
└─ Other simple locking?
   └─ → lock
```

---

## Summary

### Checklist

1. **`lock`** — Simple, fast, use by default for synchronous code
2. **`SemaphoreSlim`** — Asynchronous locking and throttling (`WaitAsync`)
3. **`Interlocked`** — Atomic operations for single values (fastest)
4. **`Mutex`** — Cross-process locking (rarely needed)
5. **`ReaderWriterLockSlim`** — Read-heavy scenarios
6. **`Lazy<T>`** — Thread-safe lazy initialization

### Key Rules

- ✅ Keep locked section as **short as possible**
- ✅ Acquire locks **always in the same order** (deadlock prevention)
- ✅ Use `SemaphoreSlim` when you need `await` inside the lock
- ✅ Release lock **always** (use `try/finally`)
- ❌ Don't call **external code** inside lock
- ❌ Don't lock on `this`, types, or strings

---

## Useful Links

- [Microsoft: lock statement](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/lock)
- [Microsoft: SemaphoreSlim](https://learn.microsoft.com/en-us/dotnet/api/system.threading.semaphoreslim)
- [Microsoft: Interlocked](https://learn.microsoft.com/en-us/dotnet/api/system.threading.interlocked)
- [Microsoft: ReaderWriterLockSlim](https://learn.microsoft.com/en-us/dotnet/api/system.threading.readerwriterlockslim)
- [Microsoft: Managed threading best practices](https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-best-practices)

### Next

- [Concurrent Collections](Concurrent-Collections.md) — Thread-safe collections that don't need manual locking
