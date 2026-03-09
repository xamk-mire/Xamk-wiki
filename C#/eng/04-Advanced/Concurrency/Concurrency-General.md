# Concurrency — Overview

## Table of Contents

1. [What is Concurrency?](#what-is-concurrency)
2. [Why is Concurrency Needed?](#why-is-concurrency-needed)
3. [Concurrency vs Parallelism vs Asynchrony](#concurrency-vs-parallelism-vs-asynchrony)
4. [Challenges of Concurrency](#challenges-of-concurrency)
5. [Concurrency Patterns](#concurrency-patterns)
6. [Concurrency in C# and .NET](#concurrency-in-c-and-net)
7. [When to Use What?](#when-to-use-what)
8. [Summary](#summary)
9. [Further Study](#further-study)

---

## What is Concurrency?

**Concurrency** means a program's ability to handle multiple tasks over overlapping time periods. It does not necessarily mean that tasks execute at exactly the same moment — but that the program can **manage** several things at once.

### Everyday Analogy

Imagine a restaurant kitchen:

**Without concurrency (sequentially):**
```
Chef: [Take order 1] → [Prepare dish 1] → [Serve 1]
      → [Take order 2] → [Prepare dish 2] → [Serve 2]
      → [Take order 3] → [Prepare dish 3] → [Serve 3]

Total time: 30 minutes (each order waits for the previous one)
```

**With concurrency:**
```
Chef: [Put order 1 in oven] → [Start order 2] → [Check order 1]
      → [Order 2 on stove] → [Order 3 start] → [Order 1 ready!]
      → [Check order 2] → ...

Total time: 12 minutes (tasks overlap)
```

Note: **One chef** can handle multiple orders concurrently. They don't clone themselves — they just organize their work smarter.

This is the core idea of concurrency: **organizing work**, not necessarily using more workers.

---

## Why is Concurrency Needed?

### 1. Performance

Modern computers have multiple processor cores. If a program uses only one core, most of the computing power goes unused:

```
4-core processor, single-threaded program:

  Core 1: ████████████████  (100% loaded)
  Core 2: ░░░░░░░░░░░░░░░░  (idle)
  Core 3: ░░░░░░░░░░░░░░░░  (idle)
  Core 4: ░░░░░░░░░░░░░░░░  (idle)

  → 75% of computing power wasted!

4-core processor, parallel program:

  Core 1: ████████████████  (100%)
  Core 2: ████████████████  (100%)
  Core 3: ████████████████  (100%)
  Core 4: ████████████████  (100%)

  → Up to 4x faster!
```

### 2. Responsiveness

In user interface applications (desktop, mobile), one thread handles UI rendering. If that thread does heavy work (database query, file download), the UI **freezes**:

```
Without concurrency:
  UI thread: [Draw button] → [Load 10MB file...............] → [Draw response]
                              ↑ UI frozen for 5 seconds!

With concurrency:
  UI thread:    [Draw button] → [Animation] → [Animation] → [Draw response]
  Background:   [Load 10MB file...............................] → Done!
                ↑ UI stays responsive the whole time!
```

### 3. Efficient Resource Use

Many operations (HTTP requests, database queries, file reads) are **I/O operations** — the program waits for an external system. Without concurrency, the thread sits idle during the wait:

```
Synchronous (wastes time):
  Thread: [Send HTTP request] → [WAIT 200ms.........] → [Process response]
                                ↑ Thread does nothing!

Asynchronous (efficient):
  Thread: [Send HTTP request] → [Do other work] → [Process response]
                                ↑ Thread serves other requests!
```

### 4. Scalability

A web server handles hundreds or thousands of requests simultaneously. Without concurrency, every user would have to wait for all previous requests to complete:

```
Synchronous web server (1 request at a time):
  User 1: [Request] → [Response]
  User 2:                      [Request] → [Response]
  User 3:                                            [Request] → [Response]
  → Everyone waits their turn

Asynchronous web server (many requests simultaneously):
  User 1: [Request] → [Response]
  User 2: [Request] → [Response]
  User 3: [Request] → [Response]
  → All served concurrently
```

---

## Concurrency vs Parallelism vs Asynchrony

These three concepts are often confused. They are different things, though related:

### Concurrency

**Definition:** A program's ability to handle multiple tasks over overlapping time periods.

Concurrency is a **structural** property — a way of organizing a program so it can handle multiple tasks. The tasks do not necessarily run at the same moment.

```
Concurrency on one core (interleaving):

  Thread A: ██░░██░░██░░██
  Thread B: ░░██░░██░░██░░

  → Both "advance" concurrently, but execute in turns
  → Like a chef switching between tasks
```

### Parallelism

**Definition:** Multiple tasks executing **literally at the same time** on different processor cores.

Parallelism is a **special case** of concurrency — it requires physically multiple execution units.

```
Parallelism on two cores:

  Core 1: ████████████████
  Core 2: ████████████████

  → Both execute TRULY simultaneously
  → Like two chefs working at the same time
```

### Asynchrony

**Definition:** Starting a task without waiting for it to complete — continue with other work and return to the result later.

Asynchrony is an **execution style** — it describes how a task is started and how its result is awaited.

```
Asynchronous operation:

  Thread: [Start I/O] → [Do something else] → [I/O done, process result]
                         ↑ Thread is free!

  → Thread doesn't stand still during the wait
  → Like a chef who turns on the oven and makes salad meanwhile
```

### How Do They Relate?

```
                    ┌─────────────────────────────┐
                    │       CONCURRENCY           │
                    │  (managing simultaneous work)│
                    │                             │
                    │  ┌───────────┐ ┌──────────┐ │
                    │  │PARALLELISM│ │ASYNCHRONY│ │
                    │  │(diff cores)│ │(I/O wait)│ │
                    │  └───────────┘ └──────────┘ │
                    └─────────────────────────────┘

Concurrency = umbrella concept (managing multiple tasks)
Parallelism = one way to implement (on different cores at once)
Asynchrony  = another way (release thread during wait)
```

| Concept | Key Idea | Requires multiple cores? | C# Tools |
|---------|----------|--------------------------|----------|
| **Concurrency** | Managing multiple tasks | No | Task, async/await, lock |
| **Parallelism** | Truly simultaneous | Yes | Parallel.ForEach, PLINQ, Task.Run |
| **Asynchrony** | Release thread during wait | No | async/await, Task.Delay |

### Concrete Example

**Situation:** 100 images need to be downloaded from the internet and processed.

```
1. Synchronous (no concurrency):
   Download image 1 → Process 1 → Download image 2 → Process 2 → ...
   Time: 100 x (download + process) = SLOW

2. Asynchronous (async/await):
   Start 100 downloads at once (await Task.WhenAll)
   → Thread released during each download
   → Process each when ready
   Time: longest download + processing

3. Parallel (Parallel.ForEach):
   Process images on 4 cores simultaneously
   → CPU work distributed across cores
   Time: 100 processes / 4 cores = ~25 processes

4. Asynchronous + parallel (best):
   Download all asynchronously (I/O) + process in parallel (CPU)
   → I/O doesn't block, CPU work distributed across cores
   Time: fastest possible
```

---

## Challenges of Concurrency

Concurrency is not free — it brings problems that single-threaded programs don't have.

### 1. Race Condition

When two threads read and write the same data simultaneously, the result is unpredictable:

```
Situation: Two threads increment a counter (_count = 0)

  Expected result:  0 + 1 + 1 = 2
  Possible result:  1 (one increment lost!)

  Thread A: READ (0) → CALCULATE (1) → WRITE (1)
  Thread B:    READ (0) → CALCULATE (1) → WRITE (1)
                                              ↑ Both wrote 1!
```

**Solution:** Synchronization mechanisms (`lock`, `Interlocked`, `SemaphoreSlim`)

> Read more: [Synchronization](Synchronization.md)

### 2. Deadlock

Two threads wait for each other's resources — neither can proceed:

```
  Thread A: Acquire lock 1, tries to acquire lock 2 → WAITING...
  Thread B: Acquire lock 2, tries to acquire lock 1 → WAITING...

  → Both wait forever! Program hangs.

  Analogy: Two cars in a narrow alley facing each other.
  Neither can reverse. Neither can move forward.
```

**Solutions:**
- Always acquire locks in the same order
- Use timeout values when acquiring locks
- Avoid nested locks
- Use higher-level abstractions (Channel, ConcurrentDictionary)

> Read more: [Synchronization — Deadlock](Synchronization.md#deadlock)

### 3. Starvation

A thread never gets to run because other threads keep resources busy:

```
  Thread A (high priority): ████████████████████████████████
  Thread B (high priority): ████████████████████████████████
  Thread C (low priority):  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                             ↑ Thread C never gets to run!
```

**Solution:** .NET's ThreadPool and Task system usually handle priorities correctly automatically.

### 4. Thread Safety

Code is **thread-safe** when it works correctly even when multiple threads use it concurrently. Most ordinary code is NOT thread-safe:

```csharp
// NOT thread-safe:
List<int> list = new List<int>();
// If two threads call Add at the same time → crash or data loss

// Thread-safe alternative:
ConcurrentBag<int> list = new ConcurrentBag<int>();
// Multiple threads can add safely
```

> Read more: [Threads — Thread Safety](Threads.md#thread-safety)

### 5. Complexity

Concurrency code is harder to write, read, test, and debug:

```
Single-threaded bug:
  → Run program again → Same bug every time → Easy to reproduce

Multi-threaded bug (race condition):
  → Run 10 times → Works 9 times → Fails 1 time
  → "Works on my machine!" → Crashes in production every day
```

**Therefore:** Use concurrency only when you need it. Simple code is the best code.

---

## Concurrency Patterns

### 1. Shared State

Threads share the same memory and communicate by modifying shared variables. Requires synchronization.

```
  Thread A ──┐
             ├──→ [Shared memory] ← Needs protection (lock, Interlocked)
  Thread B ──┘

  C# tools: lock, Interlocked, SemaphoreSlim, ConcurrentDictionary
```

**Pros:** Fast communication (memory is fast)
**Cons:** Prone to race conditions and deadlocks

### 2. Message Passing

Threads communicate by sending messages to each other. No shared state — no race conditions.

```
  Producer ──→ [Channel/Queue] ──→ Consumer

  C# tools: Channel<T>, BlockingCollection<T>
```

**Pros:** No race conditions, clear structure
**Cons:** Slightly slower than direct memory access

### 3. Producer-Consumer

One or more producers create data, one or more consumers process it. A queue stands between them.

```
  [Producer 1] ──┐
                 ├──→ [Queue (Channel)] ──→ [Consumer]
  [Producer 2] ──┘

  Restaurant analogy:
  [Waiter 1] ──┐
                ├──→ [Order slip holder] ──→ [Chef]
  [Waiter 2] ──┘
```

> Read more: [Concurrent Collections — Channel](Concurrent-Collections.md#channel)

### 4. Fork-Join

Work is split into parts, parts run in parallel, and results are combined.

```
                 ┌──→ [Part 1] ──┐
  [Work] ──Fork──→├──→ [Part 2] ──├──Join──→ [Result]
                 └──→ [Part 3] ──┘

  C# tools: Task.WhenAll, Parallel.ForEach, PLINQ
```

> Read more: [Parallel Programming](Parallel-Programming.md)

---

## Concurrency in C# and .NET

.NET provides several levels for implementing concurrency. Modern C# favors higher-level abstractions:

### Abstraction Levels (top to bottom)

```
Level 4 (highest): PLINQ, Parallel.ForEachAsync
  → "Process this list in parallel"
  → Easiest to use, least control

Level 3: async/await, Task.WhenAll, Channel<T>
  → "Start this asynchronously, wait later"
  → Foundation of modern C#

Level 2: Task.Run, ConcurrentDictionary, SemaphoreSlim
  → "Run in background thread, protect shared data"
  → More control

Level 1: Thread, lock, Monitor, Interlocked
  → "Create thread, lock resource"
  → Low-level control

Level 0 (lowest): Thread, Mutex, ManualResetEvent
  → Operating system-level synchronization
  → Rarely needed directly
```

**Rule of thumb:** Start at the highest level. Move down only if you need more control.

### C# Concurrency Tools and When to Use Them

| Tool | Purpose | Example |
|------|---------|---------|
| `async/await` | I/O waits (HTTP, DB, files) | `await httpClient.GetAsync(url)` |
| `Task.WhenAll` | Await multiple async operations | Download 10 images at once |
| `Task.Run` | Offload CPU work to background thread | Heavy computation in UI app |
| `Parallel.ForEach` | CPU-intensive list processing | Process 1000 images |
| `Parallel.ForEachAsync` | Asynchronous parallel list processing | 1000 API calls, max 10 at a time |
| `PLINQ` | Parallel LINQ queries | `.AsParallel().Where(...)` |
| `lock` | Protect code block (one thread at a time) | Counter update |
| `Interlocked` | Atomic single-value change | `Interlocked.Increment(ref count)` |
| `SemaphoreSlim` | Limit concurrency (N at a time) | Max 5 DB connections |
| `Channel<T>` | Asynchronous queue between threads | Producer-consumer pipeline |
| `ConcurrentDictionary` | Thread-safe lookup structure | Shared cache |
| `CancellationToken` | Cancellation mechanism | Timeout, user cancellation |

---

## When to Use What?

### Decision Tree

```
Is the task I/O-based (HTTP, DB, file)?
├── YES → Use async/await
│   ├── Single operation → await GetAsync()
│   ├── Multiple operations → await Task.WhenAll(...)
│   └── Multiple + limited → Parallel.ForEachAsync (MaxDegreeOfParallelism)
│
└── NO → Is the task CPU-intensive?
    ├── YES → Use Parallel / Task.Run
    │   ├── List → Parallel.ForEach / PLINQ
    │   └── Single heavy task → Task.Run (in UI apps)
    │
    └── NO → Need to share data between threads?
        ├── YES
        │   ├── Single counter → Interlocked
        │   ├── Multiple variables together → lock
        │   ├── Dictionary → ConcurrentDictionary
        │   └── Queue/pipeline → Channel<T>
        │
        └── NO → No need for concurrency!
```

### I/O-bound vs CPU-bound

This is the most important distinction when choosing concurrency tools:

| | I/O-bound | CPU-bound |
|---|---|---|
| **What happens** | Waiting for external system | Processor computes |
| **Examples** | HTTP request, DB query, file read | Image processing, encryption, calculation |
| **Thread during wait** | Does nothing (can be released) | Computes actively (needs a core) |
| **Right tool** | `async/await` | `Parallel`, `Task.Run` |
| **Why** | Release thread for others | Utilize multiple processor cores |

```
I/O-bound (async/await):
  Thread: [Send] → FREE → [Process response]
                   ↑ Thread serves other requests

CPU-bound (Parallel):
  Core 1: [Compute part 1]
  Core 2: [Compute part 2]   ← All cores computing
  Core 3: [Compute part 3]
  Core 4: [Compute part 4]
```

---

## Summary

### Key Takeaways

1. **Concurrency = managing tasks**, not necessarily simultaneous execution
2. **async/await for I/O**, **Parallel for CPU** — don't mix them
3. **Shared data needs protection** — lock, Interlocked, or thread-safe collections
4. **Use the highest-level abstraction** that suffices
5. **Don't use concurrency unnecessarily** — simple code is the best code

### Overview Map

```
┌─────────────────────────────────────────────────────────────┐
│                    CONCURRENCY IN C#                         │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   ASYNC      │  │ SYNCHRONIZATION│  │  PARALLEL    │      │
│  │              │  │              │  │              │      │
│  │ async/await  │  │ lock         │  │ Parallel.For │      │
│  │ Task.WhenAll │  │ Interlocked  │  │ PLINQ        │      │
│  │ Task.Delay   │  │ SemaphoreSlim│  │ Task.Run     │      │
│  │ Channel<T>   │  │ ConcDictionary│  │              │      │
│  │              │  │              │  │              │      │
│  │ I/O-bound    │  │ Shared data  │  │ CPU-bound    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  Cancellation: CancellationToken                             │
│  Foundation: Thread, ThreadPool                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Further Study

Recommended study order:

1. **[Threads](Threads.md)** — Understand what a thread is and how a program executes
2. **[Async/Await](Async-Await.md)** — Foundation of modern C#, I/O operations
3. **[Synchronization](Synchronization.md)** — Protecting shared data (lock, SemaphoreSlim)
4. **[Concurrent Collections](Concurrent-Collections.md)** — Thread-safe data structures
5. **[Parallel Programming](Parallel-Programming.md)** — CPU-intensive parallelism

### Practical Exercise

Try what you've learned in practice: [Restaurant order system exercise](../../../Assigments/ConcurrencyExercises/README.md)

### External Resources

- [Microsoft: Asynchronous programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [Microsoft: Parallel programming in .NET](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/)
- [Microsoft: Thread-safe collections](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)
- [Stephen Cleary: Async Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
- [Joe Albahari: Threading in C#](https://www.albahari.com/threading/)
