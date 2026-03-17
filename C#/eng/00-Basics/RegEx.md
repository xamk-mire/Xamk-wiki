# RegEx (Regular Expressions)

## What is Regex?

**Regular expressions** (regex) are a powerful way to search and process text data programmatically. They can be used to identify specific string patterns, such as email addresses, postal codes, or certain words in text.

Regex is widely used in various programming languages, including **C#**, **Python**, **JavaScript**, and **Java**. It is a useful tool for data validation, text processing, and data filtering.

## Basic Regex Syntax

Regular expressions are made up of **special characters and symbols** that define what kind of characters to search for.

| Character | Description | Example |
|-----------|-------------|---------|
| `.` | Any character (except newline) | `a.b` matches "aab", "axb", but not "ab" |
| `^` | Start of line | `^Hello` matches only "Hello world", but not "world Hello" |
| `$` | End of line | `world$` matches "Hello world", but not "world Hello" |
| `\d` | Digit (0–9) | `\d+` matches "123" |
| `\w` | Alphanumeric character (a-z, A-Z, 0-9, _) | `\w+` matches "text_123" |
| `\|` | Or operator | `cat\|dog` matches "cat" or "dog" |
| `()` | Grouping | `(ab)+` matches "ab", "abab", "ababab" |
| `[]` | Character class | `[aeiou]` matches any vowel |
| `*` | Zero or more | `a*` matches "", "a", "aa", "aaa" |
| `+` | One or more | `a+` matches "a", "aa", "aaa" |
| `?` | Zero or one | `a?` matches "" or "a" |
| `{n}` | Exactly n times | `\d{3}` matches exactly 3 digits |
| `{n,m}` | At least n, at most m times | `\d{2,4}` matches 2–4 digits |

## C# Examples of Using Regex

### 1. Find a Pattern in a String

```csharp
using System;
using System.Text.RegularExpressions;

class Program
{
    static void Main()
    {
        string input = "My phone number is 040-1234567.";
        string pattern = @"\d{3}-\d{7}";

        Match match = Regex.Match(input, pattern);

        if (match.Success)
        {
            Console.WriteLine($"Found phone number: {match.Value}");
            // Output: Found phone number: 040-1234567
        }
    }
}
```

### 2. Check if an Email Address is Valid

```csharp
using System;
using System.Text.RegularExpressions;

string email = "test@example.com";
string pattern = @"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$";

bool isValid = Regex.IsMatch(email, pattern);
Console.WriteLine(isValid ? "Email is valid" : "Invalid email");
```

### 3. Replace a Pattern in Text

```csharp
using System;
using System.Text.RegularExpressions;

string input = "The cat ran after the cat.";
string pattern = "cat";
string replacement = "dog";

string result = Regex.Replace(input, pattern, replacement, RegexOptions.IgnoreCase);
Console.WriteLine(result);
// Output: The dog ran after the dog.
```

### 4. Find All Matches

```csharp
using System;
using System.Text.RegularExpressions;

string input = "Phone numbers: 040-1234567, 050-9876543, 045-1112222";
string pattern = @"\d{3}-\d{7}";

MatchCollection matches = Regex.Matches(input, pattern);

foreach (Match match in matches)
{
    Console.WriteLine($"Found: {match.Value}");
}
```

### 5. Grouping and Using Groups

```csharp
using System;
using System.Text.RegularExpressions;

string input = "Dates: 15.01.2024, 20.02.2024";
string pattern = @"(\d{2})\.(\d{2})\.(\d{4})";

MatchCollection matches = Regex.Matches(input, pattern);

foreach (Match match in matches)
{
    Console.WriteLine($"Full match: {match.Value}");
    Console.WriteLine($"Day: {match.Groups[1].Value}");
    Console.WriteLine($"Month: {match.Groups[2].Value}");
    Console.WriteLine($"Year: {match.Groups[3].Value}");
    Console.WriteLine();
}
```

### 6. Validate Postal Code

```csharp
using System;
using System.Text.RegularExpressions;

string[] postcodes = { "00100", "12345", "ABC12", "99999" };
string pattern = @"^\d{5}$";  // Exactly 5 digits

foreach (string postcode in postcodes)
{
    bool isValid = Regex.IsMatch(postcode, pattern);
    Console.WriteLine($"{postcode}: {(isValid ? "Valid" : "Invalid")}");
}
```

### 7. Find Words of a Specific Length

```csharp
using System;
using System.Text.RegularExpressions;

string input = "cat dog horse bird";
string pattern = @"\b\w{5}\b";  // Words with exactly 5 characters

MatchCollection matches = Regex.Matches(input, pattern);

foreach (Match match in matches)
{
    Console.WriteLine($"Found: {match.Value}");
}
// Output: horse, bird
```

### 8. Using RegexOptions

```csharp
using System;
using System.Text.RegularExpressions;

string input = "HELLO world";
string pattern = "hello";

// Case-insensitive search
bool match1 = Regex.IsMatch(input, pattern, RegexOptions.IgnoreCase);
Console.WriteLine($"IgnoreCase: {match1}");  // true

// Multiline search
string multilineInput = "Line1\nLine2\nLine3";
string multilinePattern = "^Line";
MatchCollection matches = Regex.Matches(multilineInput, multilinePattern, RegexOptions.Multiline);
Console.WriteLine($"Multiline matches: {matches.Count}");  // 3
```

## Common Regex Patterns

### Email Address

```csharp
string emailPattern = @"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$";
```

### Phone Number (Finnish format)

```csharp
string phonePattern = @"^(\+358|0)[0-9]{1,2}-?[0-9]{6,10}$";
```

### Postal Code (Finnish format)

```csharp
string postcodePattern = @"^\d{5}$";
```

### IP Address

```csharp
string ipPattern = @"^(\d{1,3}\.){3}\d{1,3}$";
```

### URL

```csharp
string urlPattern = @"^https?://[^\s/$.?#].[^\s]*$";
```

## Summary

- **Regex is a powerful way to search, filter, and modify text data.**
- **It consists of special characters and symbols that can create complex search conditions.**
- **In C#, the `System.Text.RegularExpressions` library is used for regex processing.**
- **Regex is used for validation, text editing, and data retrieval.**
- **Regex can be complex, but it is a very powerful tool for text processing.**

## Useful Links

- [Microsoft Regex Documentation](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regex)
- [Regex Tester](https://regex101.com/) — Test your regex patterns online
