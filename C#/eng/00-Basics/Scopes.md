# Scopes

In C#, there are several different scopes (visibility regions) that determine where variables, methods, and other members can be used. Scopes are important because they help control access to parts of the code and improve code security and maintainability.

## Scope Types

### 1. Local Scope

Local scope is limited to a single method or block (e.g. when using an `if` statement or loop). Local variables are only accessible within the method or block where they are defined. They are not accessible outside that method or block.

```csharp
public void ExampleMethod()
{
    int localVariable = 10;  // Local variable

    if (true)
    {
        int blockVariable = 20;  // Block-scoped variable
        Console.WriteLine(localVariable);  // OK: access to local variable
        Console.WriteLine(blockVariable);   // OK: access to block variable
    }

    // Console.WriteLine(blockVariable);  // ERROR: blockVariable is not visible
}

// Console.WriteLine(localVariable);  // ERROR: localVariable is not visible
```

### 2. Class Member Scope

This scope applies to variables and methods defined at the class level. These members can be accessed through any instance of the class (i.e. object) or statically if the member is defined as static. Access to these members depends on their access modifiers (such as `public`, `private`, etc.).

```csharp
public class MyClass
{
    private int privateField = 10;      // Visible only inside the class
    public int publicField = 20;        // Visible everywhere
    internal int internalField = 30;   // Visible within the same assembly

    public void PublicMethod()
    {
        Console.WriteLine(privateField);  // OK: access to private field
        Console.WriteLine(publicField);   // OK: access to public field
    }

    private void PrivateMethod()
    {
        Console.WriteLine(privateField);  // OK: access to private field
    }
}

// Usage
MyClass obj = new MyClass();
// Console.WriteLine(obj.privateField);  // ERROR: private not visible outside
Console.WriteLine(obj.publicField);      // OK: public is visible
obj.PublicMethod();                      // OK: public method is visible
// obj.PrivateMethod();                  // ERROR: private method not visible
```

### 3. Namespace Scope

Namespaces provide a way to group classes and other types. Namespace scope allows members to be used within the same namespace without having to qualify them explicitly. Using members from other namespaces requires a `using` directive or the fully qualified name.

```csharp
namespace MyNamespace
{
    public class ClassA
    {
        public void MethodA() { }
    }

    public class ClassB
    {
        public void MethodB()
        {
            ClassA a = new ClassA();  // OK: in same namespace
            a.MethodA();
        }
    }
}

namespace AnotherNamespace
{
    using MyNamespace;  // Bring MyNamespace into scope

    public class ClassC
    {
        public void MethodC()
        {
            ClassA a = new ClassA();  // OK: thanks to using directive
            // OR with full name:
            MyNamespace.ClassA a2 = new MyNamespace.ClassA();
        }
    }
}
```

### 4. Assembly Scope

An assembly is one or more files that make up an application or library in .NET. Assembly scope determines which classes, methods, and other members are visible to other assemblies. This visibility is defined by the `internal` keyword, which allows members to be used only within the same assembly.

```csharp
// In Project A
public class PublicClass
{
    public void PublicMethod() { }
    internal void InternalMethod() { }  // Visible only within same project
}

internal class InternalClass  // Visible only within same project
{
    public void Method() { }
}

// In Project B (references Project A)
// PublicClass and PublicMethod are visible
// InternalMethod and InternalClass are not visible
```

## Scope Comparison

| Scope Type       | Visibility                                    | Example                               |
| ---------------- | --------------------------------------------- | ------------------------------------- |
| **Local**        | Method or block                               | `int x = 10;` inside a method         |
| **Class member** | Within the class (depends on access modifier) | `private int field;`                  |
| **Namespace**    | Within the same namespace                     | Classes in the same `namespace` block |
| **Assembly**     | Within the same project/assembly              | `internal` keyword                    |

## Summary

The differences between these scopes relate mainly to where and how variables and methods can be used. Local scope is the most restricted, while namespace and assembly scope provide broader visibility. Class member scope, in turn, allows variables and methods to be used on class instances, depending on the defined access modifiers.

Understanding scopes correctly is important for writing secure and maintainable code, because they help ensure that parts of the code are available only where they are needed.
