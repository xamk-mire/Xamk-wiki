# Concurrency and Asynchrony in C#

Welcome to the C# concurrency and asynchrony materials! This section covers multithreading, asynchronous programming, synchronization mechanisms, thread-safe collections, and parallel programming.

## Contents

### Overview
- [Concurrency General](Concurrency-General.md) - What is concurrency, why it's needed, concurrency vs parallelism vs asynchrony, challenges and patterns — **Read first!**
- [Cheat Sheet — Quick Reference](Cheat-Sheet.md) - Decision tree, quick lookup table, 10 golden rules, common mistakes — **Keep at hand!**

### Fundamentals
- [Threads](Threads.md) - What is a thread, process vs thread, ThreadPool, thread safety

### Asynchronous Programming
- [Async/Await](Async-Await.md) - Fundamentals of asynchronous programming, Task, CancellationToken, error handling

### Synchronization Mechanisms
- [Synchronization](Synchronization.md) - lock, Monitor, SemaphoreSlim, Mutex, Interlocked, deadlock

### Thread-Safe Collections
- [Concurrent Collections](Concurrent-Collections.md) - ConcurrentDictionary, ConcurrentQueue, Channel, BlockingCollection

### Parallel Programming
- [Parallel Programming](Parallel-Programming.md) - Parallel.ForEach, PLINQ, Task.Run, parallelization

---

## Key Concepts

### Concurrency vs Parallelism vs Asynchrony

These three concepts are often confused:

| Concept | Explanation | Example |
|---------|-------------|---------|
| **Concurrency** | Managing multiple tasks at overlapping times — not necessarily executing at the same time | One chef prepares three dishes by alternating |
| **Parallelism** | Multiple tasks executing literally at the same time on different processors | Three chefs each prepare their own dish |
| **Asynchrony** | Starting a task without waiting — continue other work until the result is ready | Chef turns on the oven and makes salad while waiting |

```
Concurrency (simultaneity):
  Thread 1: ████░░░░████░░░░████
  Thread 2: ░░░░████░░░░████░░░░
  → Alternation on one core

Parallelism:
  Core 1: ████████████████████
  Core 2: ████████████████████
  → Truly simultaneous on different cores

Asynchrony:
  Thread:  ████──────████──────████
                ↑ I/O wait    ↑ I/O wait
  → Thread released during wait
```

### When to Use What?

| Situation | Solution | Example |
|-----------|----------|---------|
| **I/O operations** (database, HTTP, files) | `async/await` | API calls, DB queries |
| **CPU-intensive computation** | `Parallel` / `Task.Run` | Image processing, data processing |
| **Shared data across threads** | `lock` / `ConcurrentDictionary` | Shared counter, shared cache |
| **Limited resource usage** | `SemaphoreSlim` | Max 5 concurrent API calls |
| **Producer-Consumer** | `Channel<T>` / `BlockingCollection` | Message queues, background processing |

---

## Learning Order

We recommend studying in the following order:

1. **[Concurrency General](Concurrency-General.md)** - Start here! Understand the big picture: what concurrency is, why it's needed, and how different approaches differ
2. **[Threads](Threads.md)** - Understand what a thread is and how a program executes
   - What is a thread and process
   - ThreadPool
   - How async/await relates to threads
3. **[Async/Await](Async-Await.md)** - Asynchronous programming is the foundation of modern C#
   - async/await syntax
   - Task and Task<T>
   - CancellationToken
   - Error handling and anti-patterns
4. **[Synchronization](Synchronization.md)** - Learn to protect shared data
   - lock statement
   - SemaphoreSlim
   - Avoiding deadlock
5. **[Concurrent Collections](Concurrent-Collections.md)** - Thread-safe data structures
   - ConcurrentDictionary
   - Channel
   - Producer-Consumer pattern
6. **[Parallel Programming](Parallel-Programming.md)** - Leverage multiple cores
   - Parallel.ForEach
   - PLINQ
   - When to parallelize

---

## Prerequisites

Before this section, it's good to master:
- [C# basics](../../00-Basics/) - Variables, functions, data structures
- [Delegates and Lambda](../../00-Basics/Delegates.md) - Delegates and lambda expressions
- [LINQ](../../00-Basics/LINQ.md) - LINQ queries (for PLINQ)
- [Thread.Sleep](../../00-Basics/Thread-Sleep.md) - Basic thread concepts

---

## Useful Links

- [Microsoft: Asynchronous programming](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/)
- [Microsoft: Parallel programming in .NET](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/)
- [Microsoft: Thread-safe collections](https://learn.microsoft.com/en-us/dotnet/standard/collections/thread-safe/)
- [Stephen Cleary: Async Best Practices](https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming)
