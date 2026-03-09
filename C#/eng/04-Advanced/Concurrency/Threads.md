# Threads — Multithreading in C#

## Table of Contents

1. [What is a Thread?](#what-is-a-thread)
2. [Process vs Thread](#process-vs-thread)
3. [How Does a Program Execute?](#how-does-a-program-execute)
4. [One Thread vs Multiple Threads](#one-thread-vs-multiple-threads)
5. [ThreadPool](#threadpool)
6. [Threads and async/await](#threads-and-asyncawait)
7. [Thread Safety](#thread-safety)
8. [Summary](#summary)
9. [Useful Links](#useful-links)

---

## What is a Thread?

A **thread** is the smallest unit of program execution. It is the "path" along which your code proceeds — line by line, top to bottom.

When you start a C# program, the operating system creates **one thread** (main thread) for it. This thread executes the code in `Program.cs` line by line.

```
Simple program — one thread:

Main Thread: [Console.WriteLine("Hello")] → [int x = 5 + 3] → [Console.WriteLine(x)]
             ──────────────────────────────────────────────────────────────────────▶ time
```

### Everyday Analogy

Think of a thread as a **chef in a kitchen**:

- **One chef (one thread)** = One person does everything alone: chop onions, fry meat, cook rice. Sequentially, one thing at a time.
- **Three chefs (three threads)** = Three people work in the same kitchen: one chops, another fries, the third cooks rice. Simultaneously, but coordination is needed to avoid collisions.

```
One chef (one thread):
  Chef: [Onions 5min] → [Meat 10min] → [Rice 8min]
  Total: 23 minutes

Three chefs (three threads):
  Chef 1: [Onions 5min]
  Chef 2: [Meat 10min]
  Chef 3: [Rice 8min]
  Total: 10 minutes (longest time wins)
```

---

## Process vs Thread

### Process

A **process** is a running program. When you open Visual Studio, a browser, or your own C# program, the operating system creates a **process** for each.

Each process has:
- Its own memory space (other processes cannot see it)
- At least one thread
- Its own processor time

### Thread

A **thread** is an execution path within a process. One process can have multiple threads.

Threads in the same process **share the same memory** — they see the same variables. This is both useful (easy to share data) and dangerous (race conditions).

```
┌─────────────────────────────────────────┐
│ PROCESS (e.g. your C# program)          │
│                                         │
│  ┌───────────┐  Shared memory:          │
│  │ Thread 1  │  - variables             │
│  │ (Main)    │  - objects               │
│  └───────────┘  - static fields         │
│  ┌───────────┐                          │
│  │ Thread 2  │  All threads see the     │
│  │ (Background)│  SAME variables!        │
│  └───────────┘                          │
│  ┌───────────┐  → That's why we need    │
│  │ Thread 3  │    lock, Interlocked,    │
│  │ (Background)│    ConcurrentDictionary  │
│  └───────────┘                          │
└─────────────────────────────────────────┘
```

| Property | Process | Thread |
|----------|---------|--------|
| **Memory** | Own, separate | Shared within process |
| **Creation** | Slow (OS creates) | Fast |
| **Communication** | Hard (inter-process) | Easy (same memory) |
| **Crash** | One process doesn't crash another | One thread can crash entire process |
| **Example** | Chrome, Visual Studio, your program | Main thread, background thread, ThreadPool thread |

---

## How Does a Program Execute?

### Single-threaded Execution

A normal C# program runs on **one thread** (main thread):

```csharp
// All of this happens on ONE thread, sequentially:
Console.WriteLine("1. Hello");        // Main thread executes
int result = CalculateSomething();    // Main thread executes
Console.WriteLine($"2. Result: {result}"); // Main thread executes
```

```
Main Thread: [WriteLine] → [CalculateSomething] → [WriteLine]
             ────────────────────────────────────────────▶ time

Everything happens sequentially, one thing at a time.
```

### Multi-threaded Execution

When you use `Task.Run`, `Parallel.ForEach`, or similar, .NET creates **additional threads**:

```csharp
// Start computation on another thread
Task<int> task = Task.Run(() => HeavyComputation());

// Main thread continues AT THE SAME TIME
Console.WriteLine("Computation in progress...");

// Wait for result
int result = await task;
```

```
Main Thread:  [Task.Run] → [WriteLine "in progress"] → ... → [await: get result]
                  │
                  └──▶ Background: [HeavyComputation ████████████]
                       (ThreadPool thread does the heavy work)
```

### What About async/await?

`async/await` **does NOT create a new thread!** It releases the current thread during the wait:

```csharp
// async/await does NOT create a new thread:
string data = await httpClient.GetStringAsync(url);
```

```
Main Thread:  [GetStringAsync] → (thread RELEASED) → ... → [continue when data arrives]
                    │                                              │
                    └── HTTP request sent                          │
                        Operating system handles it                │
                        No thread needed for waiting!  ─────────────┘
```

**Important distinction:**

| Operation | Creates new thread? | Explanation |
|-----------|--------------------|-------------|
| `await httpClient.GetAsync()` | **No** | I/O operation — OS handles it, thread is free |
| `await Task.Delay(1000)` | **No** | Timer — OS handles it, thread is free |
| `Task.Run(() => Compute())` | **Yes** | CPU work moved to ThreadPool thread |
| `Parallel.ForEach(...)` | **Yes** | Multiple ThreadPool threads in parallel |
| `new Thread(() => ...).Start()` | **Yes** | Completely new thread created (rarely needed) |

---

## One Thread vs Multiple Threads

### When Does One Thread Suffice?

In simple programs, one thread (main thread) is enough:

```csharp
// Simple program — one thread is enough
Console.Write("Your name: ");
string name = Console.ReadLine()!;
Console.WriteLine($"Hello {name}!");
```

### When Are Multiple Threads Needed?

**1. Long operation would freeze the program:**

```csharp
// ❌ One thread: program "freezes" for 5 seconds
Thread.Sleep(5000);  // Main thread blocked!
Console.WriteLine("This prints only after 5s");

// ✅ Asynchronous: program doesn't freeze
await Task.Delay(5000);  // Main thread free for other work!
Console.WriteLine("5s passed");
```

**2. Heavy computation benefits from multiple cores:**

```csharp
// ❌ One thread: uses one core
foreach (string image in images)
    ResizeImage(image);  // Sequentially, slow

// ✅ Multiple threads: uses all cores
Parallel.ForEach(images, image =>
    ResizeImage(image));  // In parallel, fast!
```

**3. Web app serves multiple users:**

```
ASP.NET Core server:

  User A → [Thread 1: Process request A]
  User B → [Thread 2: Process request B]  ← Simultaneously!
  User C → [Thread 3: Process request C]

  Without threads: A waits → B waits → C waits (slow!)
  With threads: A, B, C processed simultaneously (fast!)
```

---

## ThreadPool

### What is the ThreadPool?

.NET maintains a **thread pool** — a set of ready threads waiting for work. This is an important concept to understand, because `Task.Run`, `Parallel.ForEach`, and many others use it.

```
ThreadPool (thread reservoir):

  ┌─────────────────────────────────────────┐
  │  [Thread 1: free]  [Thread 2: BUSY]     │
  │  [Thread 3: free]  [Thread 4: BUSY]     │
  │  [Thread 5: free]  [Thread 6: free]     │
  │  [Thread 7: free]  [Thread 8: BUSY]     │
  └─────────────────────────────────────────┘
       ↑                     ↑
       │                     │
  Task.Run(() => ...)   Parallel.ForEach(...)
  "Give me a free       "Give me MULTIPLE
   thread to do          threads in parallel!"
   this work!"
```

### Why ThreadPool Instead of New Threads?

```csharp
// ❌ BAD: Creating new threads is slow and heavy
for (int i = 0; i < 100; i++)
{
    new Thread(() => Work(i)).Start();  // 100 new threads! Slow!
}

// ✅ GOOD: ThreadPool reuses threads
for (int i = 0; i < 100; i++)
{
    Task.Run(() => Work(i));  // Uses ThreadPool's ready threads
}
```

| Property | `new Thread()` | `Task.Run` (ThreadPool) |
|----------|----------------|------------------------|
| **Thread creation** | New each time (slow) | Reuses ready ones (fast) |
| **Resource use** | Heavy (~1MB memory/thread) | Light (shared pool) |
| **Management** | Manual | Automatic |
| **Usage** | Rarely needed | ✅ Recommended |

### How Does async/await Use the ThreadPool?

```csharp
public async Task<string> FetchDataAsync()
{
    // 1. Main thread calls this
    Console.WriteLine($"Thread: {Thread.CurrentThread.ManagedThreadId}"); // e.g. "Thread: 1"

    // 2. await releases thread (thread 1 returns to ThreadPool)
    string data = await httpClient.GetStringAsync(url);

    // 3. Some ThreadPool thread continues from here (might be different thread!)
    Console.WriteLine($"Thread: {Thread.CurrentThread.ManagedThreadId}"); // e.g. "Thread: 7"

    return data;
}
```

```
Before await:
  Thread 1 (Main): [FetchDataAsync starts] → [GetStringAsync starts] → thread released
                                                                         ↓
During wait:                                                         Thread 1 free!
  OS handles HTTP request                                             Does other work
                                                                         ↓
After await:
  Thread 7 (Pool): [data arrived] → [continue FetchDataAsync] → [return data]
```

**Important:**
- After `await`, the code may continue on a **different thread** than before `await`
- This is normal and safe
- That's why shared data must be protected (lock, Interlocked, ConcurrentDictionary)

---

## Threads and async/await

### async/await is Not the Same as Multithreading

This is a common misconception. Clarification:

```csharp
// This does NOT create a new thread:
await Task.Delay(1000);

// This DOES create a new thread (ThreadPool):
await Task.Run(() => HeavyComputation());
```

**What's the difference?**

- `Task.Delay`, `httpClient.GetAsync`, `stream.ReadAsync` — **I/O operations**. The OS handles the wait, no thread needed.
- `Task.Run` — **moves CPU work** to a ThreadPool thread. Creates a new thread.

### Visualization: async/await vs Thread

```
async/await (I/O):
  Thread 1: [Start HTTP request] → FREE → [Receive response, continue]
                                   ↑
                          No thread for waiting!
                          OS handles it.

Task.Run (CPU work):
  Thread 1: [Task.Run] → FREE → [await: get result]
               │
               └──▶ Thread 2 (ThreadPool): [████ Heavy computation ████]
                    Separate thread does the work.
```

### Why Is This Important?

In a web app (ASP.NET Core), the server serves **thousands of requests** simultaneously. If every request held a thread during the wait, threads would run out quickly:

```
❌ Synchronous (Thread.Sleep / .Result):
  1000 requests = 1000 blocked threads = out of memory!

✅ Asynchronous (async/await):
  1000 requests = a few threads interleaving = scales!
```

---

## Thread Safety

### Why Is Shared Data Dangerous?

Because threads in the same process **share memory**, two threads can try to modify the same variable at the same time:

```csharp
int counter = 0;

// Two threads increment the same counter:
Task.Run(() => { for (int i = 0; i < 1000; i++) counter++; });
Task.Run(() => { for (int i = 0; i < 1000; i++) counter++; });

// Result: counter < 2000! (should be 2000)
```

```
Why is the result wrong?

  Thread A: Read counter (5) → Compute 5+1=6 → Write 6
  Thread B:    Read counter (5) → Compute 5+1=6 → Write 6

  Both read 5 → both wrote 6
  One increment LOST! Should be 7.
```

### Solutions

| Problem | Solution | When to use |
|---------|----------|-------------|
| Single value update | `Interlocked` | Counters (int, long) |
| Multiple values together | `lock` | More complex logic |
| Asynchronous locking | `SemaphoreSlim` | In async code, capacity limiting |
| Thread-safe collection | `ConcurrentDictionary` | Shared data between threads |

> 📚 In detail: [Synchronization](Synchronization.md) and [Concurrent Collections](Concurrent-Collections.md)

---

## Summary

### Basics

| Concept | Explanation |
|---------|-------------|
| **Thread** | Program execution path — code proceeding line by line |
| **Main Thread** | Program's main thread — created automatically at startup |
| **ThreadPool** | .NET-maintained pool of ready threads — Task.Run uses this |
| **Process** | Running program — contains one or more threads |
| **Shared memory** | Threads in the same process see the same variables |
| **Race condition** | Two threads modify the same data at once → errors |

### Checklist

1. **One thread** executes code sequentially, line by line
2. **Multiple threads** can execute code simultaneously
3. **async/await** does not create new threads — it releases the thread during I/O wait
4. **Task.Run** moves CPU work to a ThreadPool thread
5. **ThreadPool** reuses threads — use Task.Run, not `new Thread()`
6. **Shared data** must be protected (lock, Interlocked, ConcurrentDictionary)
7. **After await** code may continue on a different thread — this is normal

### Restaurant Analogy Recap

| Programming concept | Restaurant equivalent |
|--------------------|------------------------|
| Thread | Chef |
| Main Thread | Head chef who starts the shift |
| ThreadPool | Chef break room (chefs ready and waiting) |
| Task.Run | "Hey, we need a chef to do this!" |
| async/await | Chef turns on the oven and does something else while waiting |
| lock | "Only one chef at a time may use the knife" |
| SemaphoreSlim | "Max 3 chefs in the kitchen at once" |
| Race condition | Two chefs try to season the same pot → too much salt |

---

## Useful Links

- [Microsoft: Threads and threading](https://learn.microsoft.com/en-us/dotnet/standard/threading/threads-and-threading)
- [Microsoft: The managed thread pool](https://learn.microsoft.com/en-us/dotnet/standard/threading/the-managed-thread-pool)
- [Microsoft: Managed threading best practices](https://learn.microsoft.com/en-us/dotnet/standard/threading/managed-threading-best-practices)
- [Thread.Sleep](../../00-Basics/Thread-Sleep.md) — Basic introduction to pausing a thread

### Next

- [Async/Await](Async-Await.md) — Learn asynchronous programming (most important skill!)
- [Synchronization](Synchronization.md) — Learn to protect shared data
