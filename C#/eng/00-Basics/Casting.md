# Casting (Type Conversion)

## What is Casting?

Casting is the process of converting a variable from one type to another in C#. It is commonly used with different data types, collections, and object hierarchies. There are two main types of casting:

1. **Implicit Casting (Automatic conversion)** – Automatically converts a smaller type to a larger type.
2. **Explicit Casting (Forced conversion)** – Manually converts a larger type to a smaller type, which may result in data loss.

## Casting Types

### 1. Implicit Casting

Implicit casting happens automatically when there is no risk of data loss. This typically occurs when converting a smaller data type to a larger one.

```csharp
// Smaller type -> larger type (automatic)
int smallNumber = 10;
long largeNumber = smallNumber;  // Automatic conversion int -> long

float floatValue = 3.14f;
double doubleValue = floatValue;  // Automatic conversion float -> double

char character = 'A';
int charAsInt = character;  // Automatic conversion char -> int
```

### 2. Explicit Casting

Explicit casting is required when converting a larger type to a smaller type, which requires a manual cast. This can result in data loss or exceptions.

```csharp
// Larger type -> smaller type (forced)
double doubleValue = 3.14;
int intValue = (int)doubleValue;  // 3 (decimal part is lost)

long largeNumber = 1000;
int smallNumber = (int)largeNumber;  // OK if value fits in int

// Warning: data loss
double bigDouble = 999999999999.99;
int result = (int)bigDouble;  // Data is lost
```

### 3. Using the Convert Class

The `Convert` class provides methods for safe conversion between data types, handling edge cases such as null values.

```csharp
string numberString = "123";
int number = Convert.ToInt32(numberString);  // 123

string doubleString = "3.14";
double doubleValue = Convert.ToDouble(doubleString);  // 3.14

// Null value handling
string nullString = null;
int? nullableInt = Convert.ToInt32(nullString);  // 0 (default value)
```

### 4. Using the `as` Operator

The `as` operator attempts to convert an object to a specified type. If the conversion fails, it returns `null` instead of throwing an exception.

```csharp
object obj = "Hello";
string str = obj as string;  // "Hello"

object obj2 = 123;
string str2 = obj2 as string;  // null (conversion failed)

// Check
if (str2 != null)
{
    Console.WriteLine(str2);
}
else
{
    Console.WriteLine("Conversion failed");
}
```

### 5. Using the `is` Operator

The `is` operator checks whether an object is of a certain type before attempting a conversion.

```csharp
object obj = "Hello";

if (obj is string)
{
    string str = (string)obj;  // Safe conversion
    Console.WriteLine(str);
}

// Pattern matching (C# 7.0+)
if (obj is string str2)
{
    Console.WriteLine(str2);  // str2 is automatically defined
}
```

## What is Cast<T>?

In C#, `Cast<T>` is a LINQ method used to convert elements of a non-generic collection (such as `IEnumerable`) to a specified type. It is part of the `System.Linq` namespace and is useful when working with collections that do not have a strongly typed interface.

### Method Signature

```csharp
public static IEnumerable<TResult> Cast<TResult>(this IEnumerable source)
```

This method attempts to convert each element in the source collection to the specified type `TResult`. If an element cannot be converted, an `InvalidCastException` is thrown.

## When is Cast<T> Used?

- When working with **non-generic collections** (e.g. `ArrayList`) that store elements as `object` type, and you need to work with them as a specific type.
- When you have an **IEnumerable** and need to explicitly convert elements to a more specific type.
- When handling **LINQ queries** where the input collection is of type `IEnumerable`.

## Examples of Cast<T> Usage

### Example 1: Converting ArrayList to a List of Integers

```csharp
using System;
using System.Collections;
using System.Linq;

ArrayList arrayList = new ArrayList { 1, 2, 3, 4, 5 };

// Cast<int>() ensures all elements are treated as integers
var intList = arrayList.Cast<int>().ToList();

foreach (int number in intList)
{
    Console.WriteLine(number);
}
```

**Explanation**:

- `ArrayList` stores objects, so when iterating they must be converted to `int`.
- `Cast<int>()` ensures that all elements are treated as integers.

### Example 2: Converting Objects in IEnumerable

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

IEnumerable<object> objects = new List<object> { "Hello", "World", "C#" };

// Convert to strings
var strings = objects.Cast<string>().ToList();

foreach (string str in strings)
{
    Console.WriteLine(str);
}
```

**Explanation**:

- The original collection stores elements as `object` type, so they must be converted to `string`.

### Example 3: Using Cast<T> with LINQ

```csharp
using System;
using System.Collections;
using System.Linq;

ArrayList mixedList = new ArrayList { 1, 2, "three", 4 };

try
{
    // Attempts to convert all to int
    var numbers = mixedList.Cast<int>().ToList();
}
catch (InvalidCastException ex)
{
    Console.WriteLine($"Error: {ex.Message}");
    // "three" cannot be converted to int -> InvalidCastException
}
```

**Explanation**:

- The list contains the string `"three"`, which cannot be converted to `int`.
- This results in an `InvalidCastException`.

## Cast<T> vs. OfType<T>

| Feature            | `Cast<T>`                                                       | `OfType<T>`                                   |
| ------------------ | --------------------------------------------------------------- | --------------------------------------------- |
| **Type safety**    | Assumes all elements can be converted                           | Filters out elements that cannot be converted |
| **Exception risk** | Throws `InvalidCastException` if an element cannot be converted | No exceptions; skips incompatible elements    |
| **Use case**       | Use when you are sure all elements can be converted             | Use when handling mixed-type collections      |

### Example:

```csharp
using System;
using System.Collections;
using System.Linq;

ArrayList mixedList = new ArrayList { 1, 2, "three", 4, 5 };

// Cast<int>() - throws exception
try
{
    var castResult = mixedList.Cast<int>().ToList();
}
catch (InvalidCastException)
{
    Console.WriteLine("Cast<int>() failed");
}

// OfType<int>() - filters out incompatible elements
var ofTypeResult = mixedList.OfType<int>().ToList();
// Result: [1, 2, 4, 5] ("three" filtered out)
foreach (int num in ofTypeResult)
{
    Console.WriteLine(num);
}
```

## Summary

- **Casting** is the process of converting a variable from one type to another.
- **Implicit casting** happens automatically when there is no risk of data loss.
- **Explicit casting** requires a manual cast and may result in data loss.
- **`Cast<T>`** is useful when you need to convert elements in a non-generic `IEnumerable` to a specific type.
- It **throws an exception** if any element cannot be converted.
- If you want to filter out incompatible elements instead of throwing an exception, use **`OfType<T>`**.
