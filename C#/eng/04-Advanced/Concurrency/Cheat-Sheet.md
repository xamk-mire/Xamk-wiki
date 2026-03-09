# Concurrency Cheat Sheet — Quick Reference and Tips

This is a practical quick guide: when you encounter a situation, check here which tool is the right one.

---

## Decision Tree: "What Should I Use?"

```
1. Are you waiting for something external? (HTTP, database, file, API)
   │
   ├── YES → async/await
   │   │
   │   ├── Single operation?
   │   │   └── await GetAsync(url)
   │   │
   │   ├── Multiple operations simultaneously?
   │   │   └── await Task.WhenAll(task1, task2, task3)
   │   │
   │   ├── Multiple operations, but limit the count?
   │   │   └── Parallel.ForEachAsync + MaxDegreeOfParallelism
   │   │
   │   └── Want to be able to cancel?
   │       └── Pass CancellationToken to every method
   │
   └── NO → Is the processor doing heavy computation?
       │
       ├── YES
       │   ├── Large list to process?
       │   │   └── Parallel.ForEach or PLINQ (.AsParallel())
       │   │
       │   └── Single heavy task (UI must not freeze)?
       │       └── await Task.Run(() => HeavyComputation())
       │
       └── NO → Is data shared between threads?
           │
           ├── YES → See "Protecting data" below
           │
           └── NO → No need for concurrency!
```

---

## Protecting Data: "How Do I Protect Shared Data?"

```
How many variables are modified at once?
│
├── ONE number (int, long)?
│   └── Interlocked.Increment / Interlocked.Add
│       Fastest option. No locks.
│
├── SEVERAL variables together (e.g. sum + count)?
│   │
│   ├── Synchronous code?
│   │   └── lock (_lock) { variable1++; variable2 += value; }
│   │
│   └── Asynchronous code (need await)?
│       └── SemaphoreSlim(1, 1) + WaitAsync/Release
│           (Cannot use await inside lock!)
│
├── Dictionary / lookup structure?
│   └── ConcurrentDictionary<TKey, TValue>
│       GetOrAdd, AddOrUpdate, TryAdd — atomic operations
│
├── Queue between threads (producer-consumer)?
│   │
│   ├── Asynchronous code?
│   │   └── Channel<T> (modern, recommended)
│   │
│   └── Synchronous code?
│       └── BlockingCollection<T> (older)
│
└── Want to limit how many threads can run simultaneously?
    └── SemaphoreSlim(N, N)
        E.g. SemaphoreSlim(5, 5) = max 5 at a time
```

---

## 10 Golden Rules

### 1. async for I/O, Parallel for CPU

```
I/O (HTTP, DB, file)  →  async/await
CPU (computation, images)  →  Parallel.ForEach / Task.Run
```

Don't mix these. `Task.Run` for I/O operations is redundant. `Thread.Sleep` in async code is a mistake.

### 2. Never Use Thread.Sleep in Async Code

```csharp
// WRONG — blocks the thread
async Task DoSomethingAsync()
{
    Thread.Sleep(1000);     // Thread stuck!
}

// RIGHT — releases the thread
async Task DoSomethingAsync()
{
    await Task.Delay(1000); // Thread free!
}
```

### 3. Async Bubbles Upward

When one method is async, all its callers must be async. Don't break the chain with `.Result` or `.Wait()`.

```csharp
// WRONG — deadlock risk
string data = GetDataAsync().Result;

// RIGHT
string data = await GetDataAsync();
```

### 4. Task.WhenAll When You Want Speed

If you have multiple independent operations, start them all and wait together:

```csharp
// SLOW (sequentially):
string a = await FetchA();    // 2s
string b = await FetchB();    // 2s
// Total: 4s

// FAST (concurrently):
Task<string> taskA = FetchA();
Task<string> taskB = FetchB();
string[] results = await Task.WhenAll(taskA, taskB);
// Total: 2s (longest one wins)
```

### 5. CancellationToken ALWAYS Included

Pass CancellationToken to every async method. Otherwise the operation cannot be cancelled.

```csharp
// Method accepts the token
public async Task<string> FetchAsync(CancellationToken ct = default)
{
    return await _http.GetStringAsync(url, ct);  // Pass it forward!
}
```

### 6. Interlocked for One, lock for Many

```csharp
// Single value → Interlocked (fast)
Interlocked.Increment(ref _counter);

// Multiple values together → lock (safe)
lock (_lock)
{
    _totalTime += duration;
    _count++;
}
```

### 7. SemaphoreSlim.Release() ALWAYS in a finally Block

```csharp
await _semaphore.WaitAsync(ct);
try
{
    await DoSomethingAsync(ct);
}
finally
{
    _semaphore.Release();  // Always released, even on error
}
```

If you forget `finally` and the operation throws an exception, the slot stays reserved forever.

### 8. Don't Use async void

```csharp
// WRONG — exceptions cannot be handled
async void DoSomething() { ... }

// RIGHT
async Task DoSomethingAsync() { ... }

// ONLY exception: event handlers
button.Click += async (s, e) => { await DoSomethingAsync(); };
```

### 9. Don't Use Plain List/Dictionary in Parallel Code

```csharp
// WRONG — crashes or corrupts data
List<int> list = new List<int>();
Parallel.For(0, 1000, i => list.Add(i));

// RIGHT — thread-safe
ConcurrentBag<int> bag = new ConcurrentBag<int>();
Parallel.For(0, 1000, i => bag.Add(i));
```

### 10. Measure Before Parallelizing

Parallelism is not always faster — there's overhead. Measure first:

```csharp
Stopwatch sw = Stopwatch.StartNew();
// ... code ...
Console.WriteLine($"Duration: {sw.ElapsedMilliseconds}ms");
```

Only parallelize when a single iteration takes over 1ms or there are hundreds/thousands of elements.

---

## Quick Reference Table

| Situation | Tool | Example |
|-----------|------|---------|
| HTTP request | `await httpClient.GetAsync()` | API fetch |
| Database query | `await db.ToListAsync(ct)` | EF Core |
| Multiple I/O operations | `await Task.WhenAll(...)` | 10 API calls at once |
| Multiple I/O + limit | `Parallel.ForEachAsync` + `MaxDegreeOfParallelism` | 1000 calls, max 20 at a time |
| Heavy CPU computation | `await Task.Run(() => ...)` | Hash computation in UI app |
| Large list + CPU work | `Parallel.ForEach` | Processing 10,000 images |
| LINQ + CPU work | `.AsParallel().Where(...)` | Filtering a million rows |
| Counter (int) | `Interlocked.Increment` | Order count |
| Multiple variables together | `lock` | Average calculation (sum + count) |
| Locking in async code | `SemaphoreSlim(1,1)` | Asynchronous critical section |
| Max N concurrent | `SemaphoreSlim(N,N)` | Max 3 chefs in kitchen |
| Shared key-value data | `ConcurrentDictionary` | Cache, order tracking |
| Producer-consumer queue | `Channel<T>` | Order queue, background processing |
| Delay in async code | `await Task.Delay(ms)` | Simulated wait |
| Cancellation mechanism | `CancellationToken` | Timeout, user cancellation |
| Lazy initialization | `Lazy<T>` | Singleton, data fetched once |

---

## Common Mistakes and Fixes

| Mistake | Why wrong | Fix |
|---------|-----------|-----|
| `Thread.Sleep(1000)` in async method | Blocks the thread | `await Task.Delay(1000)` |
| `GetAsync().Result` | Deadlock risk | `await GetAsync()` |
| `async void Method()` | Exceptions cannot be handled | `async Task MethodAsync()` |
| `_counter++` in parallel code | Race condition | `Interlocked.Increment(ref _counter)` |
| `lock` + `await` inside | Compile error / deadlock | `SemaphoreSlim(1,1).WaitAsync()` |
| `List.Add()` in parallel | Crash / data loss | `ConcurrentBag` or `lock` |
| `Dictionary[key] = x` in parallel | Crash | `ConcurrentDictionary` |
| `SemaphoreSlim.Release()` without `finally` | Slot stays reserved on error | Put in `try/finally` block |
| `Task.Run(() => httpClient.GetAsync(...))` | Unnecessary thread for I/O | Directly `await httpClient.GetAsync(...)` |
| Nested `Parallel.ForEach` | Too many threads, slow | Parallelize only the outer loop |

---

## Restaurant Analogy Quick Guide

| C# Concept | Restaurant |
|------------|------------|
| **Thread** | Chef |
| **async/await** | Chef sets timer and does something else meanwhile |
| **Thread.Sleep** | Chef stands still and stares at the clock |
| **Task.WhenAll** | "Order ready when ALL dishes are done" |
| **Task.Run** | "Hey, we need a chef to do this!" |
| **CancellationToken** | Customer cancels order |
| **lock** | Only one chef may update the blackboard at a time |
| **Interlocked** | Quick counter click (atomic) |
| **SemaphoreSlim(3,3)** | Kitchen fits max 3 chefs |
| **Channel** | Order slip holder on the counter |
| **ConcurrentDictionary** | Wall board with order status |
| **Parallel.ForEach** | Split 100 dish preparations among 4 chefs |
| **Race condition** | Two chefs seasoning the same pot → too much salt |
| **Deadlock** | Two chefs in a narrow corridor face to face — neither can pass |

---

## Mnemonic Rules in Sentences

1. **"Does the code wait for something?"** → async/await
2. **"Does the code compute something heavy?"** → Parallel / Task.Run
3. **"Do multiple threads modify the same data?"** → Protect it (lock, Interlocked, Concurrent*)
4. **"How many variables change at once?"** → One = Interlocked, many = lock
5. **"Need await inside the lock?"** → SemaphoreSlim, not lock
6. **"Need to limit concurrency?"** → SemaphoreSlim(N, N)
7. **"Need to pass data from thread to thread?"** → Channel\<T\>
8. **"Can this be cancelled?"** → CancellationToken
9. **"Does this work correctly if 1000 threads do the same at once?"** → If unsure, protect it
10. **"Is this faster when parallel?"** → Measure, don't guess

---

## Additional Material

- [Concurrency General](Concurrency-General.md) — Overview and concepts
- [Threads](Threads.md) — What is a thread and how a program executes
- [Async/Await](Async-Await.md) — Fundamentals of asynchronous programming
- [Synchronization](Synchronization.md) — lock, SemaphoreSlim, Interlocked
- [Concurrent Collections](Concurrent-Collections.md) — ConcurrentDictionary, Channel
- [Parallel Programming](Parallel-Programming.md) — Parallel.ForEach, PLINQ
