# Access Modifiers

[Microsoft Official Documentation](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers)

In C#, access modifiers are keywords used to define the visibility of classes, methods, and other members. They control where these members can be accessed from and play a central role in data encapsulation and security.

## Access Modifiers

### 1. Public

The `public` modifier allows access to a class member from any code in the same assembly or in another assembly that references it. For example, a public class or method can be used from any part of the program.

```csharp
public class PublicClass
{
    public string Name { get; set; }
    public void PublicMethod()
    {
        Console.WriteLine("This method is public");
    }
}

// Usage from anywhere
PublicClass obj = new PublicClass();
obj.Name = "Test";
obj.PublicMethod();
```

**Real-world analogy**: A public library. Anyone can go in and use its resources.

### 2. Private

The `private` modifier restricts access to a class member to only the class itself. It is the most restrictive visibility level and is used to encapsulate a class's internal operations. For example, a private field or method is not accessible from outside the containing class.

```csharp
public class MyClass
{
    private string secret;  // Visible only inside this class
    
    private void PrivateMethod()
    {
        Console.WriteLine("This is a private method");
    }
    
    public void PublicMethod()
    {
        secret = "Secret";  // OK: access to private field within class
        PrivateMethod();    // OK: access to private method within class
    }
}

// Usage
MyClass obj = new MyClass();
// obj.secret = "Test";        // ERROR: private not visible outside
// obj.PrivateMethod();        // ERROR: private not visible outside
obj.PublicMethod();            // OK: public method is visible
```

**Real-world analogy**: A personal diary. Only you can read and write to it.

### 3. Protected

The `protected` modifier allows a class member to be accessible within the class and in derived classes. This means that if you have a base class with a protected member, any derived class can use that member, but other classes (that are not derived classes) cannot.

```csharp
public class BaseClass
{
    protected int protectedField = 10;
    
    protected void ProtectedMethod()
    {
        Console.WriteLine("This is a protected method");
    }
}

public class DerivedClass : BaseClass
{
    public void UseProtected()
    {
        Console.WriteLine(protectedField);  // OK: access to protected field
        ProtectedMethod();                   // OK: access to protected method
    }
}

// Usage
DerivedClass derived = new DerivedClass();
derived.UseProtected();  // OK
// derived.protectedField = 20;  // ERROR: protected not visible outside
```

**Real-world analogy**: A family heirloom at home. It's available to you and your family members, but not to outsiders.

### 4. Internal

The `internal` modifier restricts access to members within the same assembly. This is useful when you want to allow access to certain parts of a library from other parts of the same library, but not from outside.

```csharp
// In Project A
internal class InternalClass
{
    internal void InternalMethod()
    {
        Console.WriteLine("This is an internal method");
    }
}

public class PublicClass
{
    public void UseInternal()
    {
        InternalClass obj = new InternalClass();  // OK: in same project
        obj.InternalMethod();
    }
}

// In Project B (references Project A)
// InternalClass and InternalMethod are not visible
```

**Real-world analogy**: An office building where only the company's employees can access certain areas.

### 5. Protected Internal

This combination of `protected` and `internal` allows access to a member from any class in the same assembly or from any derived class in any assembly. It is less common but useful in certain scenarios where you need broader access than `internal`, but more restricted than `public`.

```csharp
public class BaseClass
{
    protected internal int protectedInternalField = 10;
}

// In same project
public class SameProjectClass
{
    public void UseProtectedInternal()
    {
        BaseClass obj = new BaseClass();
        obj.protectedInternalField = 20;  // OK: in same project
    }
}

// In different project, but inherits BaseClass
public class DerivedClass : BaseClass
{
    public void UseProtectedInternal()
    {
        protectedInternalField = 30;  // OK: derived class
    }
}
```

**Real-world analogy**: A community center where all local residents and members of certain communities (regardless of location) can enter.

### 6. Private Protected

Introduced in C# 7.2, this combination of `private` and `protected` modifiers allows access only within the containing class or in a derived class in the same assembly. It is more restrictive than `protected internal`.

```csharp
public class BaseClass
{
    private protected int privateProtectedField = 10;
}

// In same project and inherits BaseClass
public class DerivedClass : BaseClass
{
    public void UsePrivateProtected()
    {
        privateProtectedField = 20;  // OK: derived class in same project
    }
}
```

**Real-world analogy**: A private family event at a local community hall. Only your family (derived class) and a specific community (same assembly) can participate.

## Default Visibility

### Classes

- **No modifier**: `internal` (visible only within the same project)
- **Nested classes** (inner classes): `private` (visible only within the outer class)

```csharp
// Default is internal
class DefaultClass  // Same as: internal class DefaultClass
{
}

// Nested class is private by default
public class OuterClass
{
    class NestedClass  // Same as: private class NestedClass
    {
    }
}
```

### Class Members

- **Fields and methods**: `private` (visible only within the class)

```csharp
public class MyClass
{
    int field;           // Same as: private int field;
    void Method()        // Same as: private void Method()
    {
    }
}
```

## Summary

Access modifiers are a central part of C#'s encapsulation and help ensure that parts of code are available only where they are needed. Choosing the right access modifier improves code security, maintainability, and clarity.

| Access Modifier | Visibility |
|----------------|------------|
| `public` | Everywhere |
| `private` | Only within the class |
| `protected` | Within the class and in derived classes |
| `internal` | Within the same assembly/project |
| `protected internal` | Within the same assembly OR in derived classes |
| `private protected` | Only within the class OR in derived classes in the same assembly |
