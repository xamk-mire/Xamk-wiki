# Attribuutit - Esimerkit

Tämä tiedosto sisältää kattavat koodiesimerkit attribuuteista C#:ssa.

## Sisällysluettelo

1. [Sisäänrakennetut attribuutit](#sisäänrakennetut-attribuutit)
2. [Omien attribuuttien luominen](#omien-attribuuttien-luominen)
3. [Reflection ja attribuutit](#reflection-ja-attribuutit)
4. [Validointi attribuuteilla](#validointi-attribuuteilla)
5. [Routing-attribuutit](#routing-attribuutit)
6. [Serialization-attribuutit](#serialization-attribuutit)
7. [Kattava esimerkki: Plugin-järjestelmä](#kattava-esimerkki-plugin-järjestelmä)

---

## Sisäänrakennetut attribuutit

### Esimerkki 1: Obsolete-attribuutti

```csharp
public class Calculator
{
    [Obsolete("Use AddNumbers instead")]
    public int Add(int a, int b)
    {
        return a + b;
    }
    
    public int AddNumbers(int a, int b)
    {
        return a + b;
    }
    
    [Obsolete("This method will be removed in version 3.0", true)]
    public int OldCalculation(int x)
    {
        return x * 2;
    }
}

// Käyttö
public class Program
{
    public static void Main()
    {
        Calculator calc = new Calculator();
        
        // Varoitus: 'Calculator.Add(int, int)' is obsolete: 'Use AddNumbers instead'
        int result1 = calc.Add(5, 3);
        
        // OK - Ei varoitusta
        int result2 = calc.AddNumbers(5, 3);
        
        // Virhe: 'Calculator.OldCalculation(int)' is obsolete: 
        // 'This method will be removed in version 3.0'
        // int result3 = calc.OldCalculation(10);
    }
}
```

### Esimerkki 2: Conditional-attribuutti

```csharp
using System.Diagnostics;

public class Logger
{
    [Conditional("DEBUG")]
    public static void LogDebug(string message)
    {
        Console.WriteLine($"[DEBUG] {message}");
    }
    
    [Conditional("TRACE")]
    public static void LogTrace(string message)
    {
        Console.WriteLine($"[TRACE] {message}");
    }
    
    public static void LogAlways(string message)
    {
        Console.WriteLine($"[LOG] {message}");
    }
}

public class Program
{
    public static void Main()
    {
        Logger.LogDebug("This is debug info");  // Näkyy vain DEBUG-moodissa
        Logger.LogTrace("This is trace info");  // Näkyy vain TRACE-moodissa
        Logger.LogAlways("This always shows");  // Näkyy aina
    }
}
```

### Esimerkki 3: Flags-attribuutti

```csharp
[Flags]
public enum FilePermissions
{
    None = 0,
    Read = 1,
    Write = 2,
    Execute = 4,
    Delete = 8,
    
    ReadWrite = Read | Write,
    All = Read | Write | Execute | Delete
}

public class FileSystem
{
    public void SetPermissions(string fileName, FilePermissions permissions)
    {
        Console.WriteLine($"Setting permissions for {fileName}:");
        
        if (permissions.HasFlag(FilePermissions.Read))
            Console.WriteLine("  - Read access");
        
        if (permissions.HasFlag(FilePermissions.Write))
            Console.WriteLine("  - Write access");
        
        if (permissions.HasFlag(FilePermissions.Execute))
            Console.WriteLine("  - Execute access");
        
        if (permissions.HasFlag(FilePermissions.Delete))
            Console.WriteLine("  - Delete access");
    }
}

// Käyttö
FileSystem fs = new FileSystem();

// Yksittäinen oikeus
fs.SetPermissions("file1.txt", FilePermissions.Read);

// Useita oikeuksia
fs.SetPermissions("file2.txt", FilePermissions.Read | FilePermissions.Write);

// Ennalta määritelty yhdistelmä
fs.SetPermissions("file3.txt", FilePermissions.ReadWrite);

// Kaikki oikeudet
fs.SetPermissions("file4.txt", FilePermissions.All);
```

### Esimerkki 4: CallerMemberName ja kumppanit

```csharp
using System.Runtime.CompilerServices;

public class DebugLogger
{
    public static void Log(
        string message,
        [CallerMemberName] string memberName = "",
        [CallerFilePath] string filePath = "",
        [CallerLineNumber] int lineNumber = 0)
    {
        string fileName = Path.GetFileName(filePath);
        Console.WriteLine($"[{fileName}:{lineNumber}] {memberName}(): {message}");
    }
}

public class UserService
{
    public void CreateUser(string name)
    {
        DebugLogger.Log("Creating user");  
        // Output: [UserService.cs:45] CreateUser(): Creating user
        
        // Logiikka...
        
        DebugLogger.Log("User created successfully");
        // Output: [UserService.cs:49] CreateUser(): User created successfully
    }
    
    public void DeleteUser(int id)
    {
        DebugLogger.Log($"Deleting user {id}");
        // Output: [UserService.cs:55] DeleteUser(): Deleting user 123
    }
}
```

### Esimerkki 5: DebuggerDisplay-attribuutti

```csharp
[DebuggerDisplay("Person: {Name}, Age: {Age}, City: {Address.City}")]
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public Address Address { get; set; }
    
    public override string ToString()
    {
        return $"{Name} ({Age})";
    }
}

public class Address
{
    public string Street { get; set; }
    public string City { get; set; }
    public string PostalCode { get; set; }
}

// Käyttö debuggerissa
Person person = new Person
{
    Name = "Matti Meikäläinen",
    Age = 30,
    Address = new Address
    {
        Street = "Keskuskatu 1",
        City = "Helsinki",
        PostalCode = "00100"
    }
};

// Debuggerissa näkyy: "Person: Matti Meikäläinen, Age: 30, City: Helsinki"
// Sen sijaan että näkyisi vain "ConsoleApp.Person"
```

---

## Omien attribuuttien luominen

### Esimerkki 1: Yksinkertainen Author-attribuutti

```csharp
// Attribuutin määrittely
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method, AllowMultiple = true)]
public class AuthorAttribute : Attribute
{
    public string Name { get; }
    public string Email { get; set; }
    public string Date { get; set; }
    
    public AuthorAttribute(string name)
    {
        Name = name;
    }
}

// Käyttö
[Author("Matti Meikäläinen", Email = "matti@example.com", Date = "2026-01-15")]
[Author("Maija Mehiläinen", Email = "maija@example.com", Date = "2026-01-16")]
public class UserService
{
    [Author("Pekka Puupää", Date = "2026-01-17")]
    public void CreateUser(string name)
    {
        // Logiikka
    }
}
```

### Esimerkki 2: Version-attribuutti

```csharp
[AttributeUsage(AttributeTargets.Class | AttributeTargets.Method)]
public class VersionAttribute : Attribute
{
    public int Major { get; }
    public int Minor { get; }
    public int Patch { get; }
    
    public VersionAttribute(int major, int minor, int patch)
    {
        if (major < 0 || minor < 0 || patch < 0)
            throw new ArgumentException("Version numbers must be non-negative");
        
        Major = major;
        Minor = minor;
        Patch = patch;
    }
    
    public override string ToString()
    {
        return $"{Major}.{Minor}.{Patch}";
    }
}

// Käyttö
[Version(2, 1, 0)]
public class ApiController
{
    [Version(1, 0, 0)]
    [Obsolete("Use GetUsersV2 instead")]
    public List<User> GetUsers()
    {
        return new List<User>();
    }
    
    [Version(2, 0, 0)]
    public List<User> GetUsersV2()
    {
        return new List<User>();
    }
}
```

### Esimerkki 3: Description-attribuutti

```csharp
[AttributeUsage(AttributeTargets.All, AllowMultiple = false, Inherited = true)]
public class DescriptionAttribute : Attribute
{
    public string Description { get; }
    public string Category { get; set; }
    public string[] Tags { get; set; }
    
    public DescriptionAttribute(string description)
    {
        Description = description ?? throw new ArgumentNullException(nameof(description));
    }
}

// Käyttö
[Description(
    "Manages user authentication and authorization",
    Category = "Security",
    Tags = new[] { "auth", "security", "users" })]
public class AuthService
{
    [Description("Authenticates a user with username and password")]
    public bool Login(string username, string password)
    {
        return true;
    }
    
    [Description("Logs out the current user")]
    public void Logout()
    {
    }
}
```

---

## Reflection ja attribuutit

### Esimerkki 1: Attribuutin lukeminen luokasta

```csharp
public class AttributeReader
{
    public static void ReadClassAttributes()
    {
        Type type = typeof(UserService);
        
        // Lue kaikki Author-attribuutit
        AuthorAttribute[] authors = (AuthorAttribute[])Attribute.GetCustomAttributes(
            type, 
            typeof(AuthorAttribute));
        
        Console.WriteLine($"Class: {type.Name}");
        Console.WriteLine($"Authors: {authors.Length}");
        
        foreach (AuthorAttribute author in authors)
        {
            Console.WriteLine($"  - {author.Name}");
            if (!string.IsNullOrEmpty(author.Email))
                Console.WriteLine($"    Email: {author.Email}");
            if (!string.IsNullOrEmpty(author.Date))
                Console.WriteLine($"    Date: {author.Date}");
        }
    }
}
```

### Esimerkki 2: Metodien attribuuttien lukeminen

```csharp
public class MethodAttributeReader
{
    public static void ReadMethodAttributes(Type type)
    {
        Console.WriteLine($"\nMethods in {type.Name}:");
        
        MethodInfo[] methods = type.GetMethods(
            BindingFlags.Public | 
            BindingFlags.Instance | 
            BindingFlags.DeclaredOnly);
        
        foreach (MethodInfo method in methods)
        {
            Console.WriteLine($"\n  Method: {method.Name}");
            
            // Tarkista onko Obsolete
            ObsoleteAttribute obsolete = method.GetCustomAttribute<ObsoleteAttribute>();
            if (obsolete != null)
            {
                Console.WriteLine($"    [OBSOLETE] {obsolete.Message}");
            }
            
            // Tarkista Version
            VersionAttribute version = method.GetCustomAttribute<VersionAttribute>();
            if (version != null)
            {
                Console.WriteLine($"    Version: {version}");
            }
            
            // Tarkista Description
            DescriptionAttribute description = method.GetCustomAttribute<DescriptionAttribute>();
            if (description != null)
            {
                Console.WriteLine($"    Description: {description.Description}");
            }
        }
    }
}

// Käyttö
MethodAttributeReader.ReadMethodAttributes(typeof(ApiController));
```

### Esimerkki 3: Ominaisuuksien attribuuttien lukeminen

```csharp
public class PropertyAttributeReader
{
    public static void ReadPropertyAttributes<T>()
    {
        Type type = typeof(T);
        PropertyInfo[] properties = type.GetProperties();
        
        Console.WriteLine($"Properties in {type.Name}:");
        
        foreach (PropertyInfo property in properties)
        {
            Console.WriteLine($"\n  {property.Name} ({property.PropertyType.Name})");
            
            // Lue kaikki attribuutit
            Attribute[] attributes = Attribute.GetCustomAttributes(property);
            
            foreach (Attribute attr in attributes)
            {
                Console.WriteLine($"    [{attr.GetType().Name}]");
                
                // Tarkista tietyt attribuutit
                if (attr is RequiredAttribute)
                {
                    Console.WriteLine("      - This property is required");
                }
                else if (attr is MaxLengthAttribute maxLength)
                {
                    Console.WriteLine($"      - Max length: {maxLength.Length}");
                }
            }
        }
    }
}
```

---

## Validointi attribuuteilla

### Esimerkki: Validointi-attribuutit

```csharp
// Omat validointi-attribuutit
[AttributeUsage(AttributeTargets.Property)]
public class RequiredAttribute : Attribute
{
    public string ErrorMessage { get; set; } = "This field is required";
}

[AttributeUsage(AttributeTargets.Property)]
public class MaxLengthAttribute : Attribute
{
    public int Length { get; }
    public string ErrorMessage { get; set; }
    
    public MaxLengthAttribute(int length)
    {
        Length = length;
        ErrorMessage = $"Maximum length is {length}";
    }
}

[AttributeUsage(AttributeTargets.Property)]
public class RangeAttribute : Attribute
{
    public int Min { get; }
    public int Max { get; }
    public string ErrorMessage { get; set; }
    
    public RangeAttribute(int min, int max)
    {
        Min = min;
        Max = max;
        ErrorMessage = $"Value must be between {min} and {max}";
    }
}

[AttributeUsage(AttributeTargets.Property)]
public class EmailAttribute : Attribute
{
    public string ErrorMessage { get; set; } = "Invalid email format";
}

// Käyttö
public class User
{
    [Required]
    [MaxLength(50)]
    public string Name { get; set; }
    
    [Required]
    [Email]
    public string Email { get; set; }
    
    [Range(18, 120)]
    public int Age { get; set; }
    
    [MaxLength(200)]
    public string Bio { get; set; }
}

// Validaattori
public class Validator
{
    public static List<string> Validate<T>(T obj)
    {
        List<string> errors = new List<string>();
        Type type = typeof(T);
        PropertyInfo[] properties = type.GetProperties();
        
        foreach (PropertyInfo property in properties)
        {
            object value = property.GetValue(obj);
            
            // Tarkista Required
            RequiredAttribute required = property.GetCustomAttribute<RequiredAttribute>();
            if (required != null && value == null)
            {
                errors.Add($"{property.Name}: {required.ErrorMessage}");
                continue;
            }
            
            if (value != null)
            {
                // Tarkista MaxLength
                MaxLengthAttribute maxLength = property.GetCustomAttribute<MaxLengthAttribute>();
                if (maxLength != null && value is string strValue)
                {
                    if (strValue.Length > maxLength.Length)
                    {
                        errors.Add($"{property.Name}: {maxLength.ErrorMessage}");
                    }
                }
                
                // Tarkista Range
                RangeAttribute range = property.GetCustomAttribute<RangeAttribute>();
                if (range != null && value is int intValue)
                {
                    if (intValue < range.Min || intValue > range.Max)
                    {
                        errors.Add($"{property.Name}: {range.ErrorMessage}");
                    }
                }
                
                // Tarkista Email
                EmailAttribute email = property.GetCustomAttribute<EmailAttribute>();
                if (email != null && value is string emailValue)
                {
                    if (!emailValue.Contains("@"))
                    {
                        errors.Add($"{property.Name}: {email.ErrorMessage}");
                    }
                }
            }
        }
        
        return errors;
    }
}

// Käyttö
User user = new User
{
    Name = "Matti",
    Email = "invalid-email",
    Age = 15
};

List<string> errors = Validator.Validate(user);
if (errors.Count > 0)
{
    Console.WriteLine("Validation errors:");
    foreach (string error in errors)
    {
        Console.WriteLine($"  - {error}");
    }
}
// Output:
// Validation errors:
//   - Email: Invalid email format
//   - Age: Value must be between 18 and 120
```

---

## Routing-attribuutit

### Esimerkki: HTTP-routing attribuutit

```csharp
// Route-attribuutit
[AttributeUsage(AttributeTargets.Class)]
public class RouteAttribute : Attribute
{
    public string Template { get; }
    
    public RouteAttribute(string template)
    {
        Template = template;
    }
}

[AttributeUsage(AttributeTargets.Method)]
public class HttpMethodAttribute : Attribute
{
    public string Method { get; }
    public string Route { get; set; }
    
    public HttpMethodAttribute(string method)
    {
        Method = method;
    }
}

public class HttpGetAttribute : HttpMethodAttribute
{
    public HttpGetAttribute() : base("GET") { }
}

public class HttpPostAttribute : HttpMethodAttribute
{
    public HttpPostAttribute() : base("POST") { }
}

public class HttpPutAttribute : HttpMethodAttribute
{
    public HttpPutAttribute() : base("PUT") { }
}

public class HttpDeleteAttribute : HttpMethodAttribute
{
    public HttpDeleteAttribute() : base("DELETE") { }
}

// Käyttö
[Route("api/users")]
public class UserController
{
    [HttpGet]
    public List<User> GetAll()
    {
        return new List<User>();
    }
    
    [HttpGet]
    [Route("{id}")]
    public User GetById(int id)
    {
        return new User();
    }
    
    [HttpPost]
    public void Create(User user)
    {
    }
    
    [HttpPut]
    [Route("{id}")]
    public void Update(int id, User user)
    {
    }
    
    [HttpDelete]
    [Route("{id}")]
    public void Delete(int id)
    {
    }
}

// Route-resolver
public class RouteResolver
{
    public static void PrintRoutes(Type controllerType)
    {
        RouteAttribute classRoute = controllerType.GetCustomAttribute<RouteAttribute>();
        string baseRoute = classRoute?.Template ?? "";
        
        Console.WriteLine($"Controller: {controllerType.Name}");
        Console.WriteLine($"Base route: /{baseRoute}");
        Console.WriteLine("\nEndpoints:");
        
        MethodInfo[] methods = controllerType.GetMethods(BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly);
        
        foreach (MethodInfo method in methods)
        {
            HttpMethodAttribute httpMethod = method.GetCustomAttribute<HttpMethodAttribute>();
            if (httpMethod != null)
            {
                string methodRoute = "";
                RouteAttribute methodRouteAttr = method.GetCustomAttribute<RouteAttribute>();
                if (methodRouteAttr != null)
                {
                    methodRoute = "/" + methodRouteAttr.Template;
                }
                
                string fullRoute = $"/{baseRoute}{methodRoute}";
                Console.WriteLine($"  {httpMethod.Method,-6} {fullRoute} -> {method.Name}()");
            }
        }
    }
}

// Käyttö
RouteResolver.PrintRoutes(typeof(UserController));
// Output:
// Controller: UserController
// Base route: /api/users
//
// Endpoints:
//   GET    /api/users -> GetAll()
//   GET    /api/users/{id} -> GetById()
//   POST   /api/users -> Create()
//   PUT    /api/users/{id} -> Update()
//   DELETE /api/users/{id} -> Delete()
```

---

## Serialization-attribuutit

### Esimerkki: JSON-serialization attribuutit

```csharp
[AttributeUsage(AttributeTargets.Property)]
public class JsonPropertyAttribute : Attribute
{
    public string Name { get; }
    public bool Ignore { get; set; }
    
    public JsonPropertyAttribute(string name = null)
    {
        Name = name;
    }
}

[AttributeUsage(AttributeTargets.Class)]
public class JsonObjectAttribute : Attribute
{
    public string Description { get; set; }
}

// Käyttö
[JsonObject(Description = "Represents a user in the system")]
public class User
{
    [JsonProperty("id")]
    public int UserId { get; set; }
    
    [JsonProperty("full_name")]
    public string Name { get; set; }
    
    [JsonProperty("email_address")]
    public string Email { get; set; }
    
    [JsonProperty(Ignore = true)]
    public string Password { get; set; }
    
    public DateTime CreatedAt { get; set; }
}

// Yksinkertainen JSON-serializer
public class SimpleJsonSerializer
{
    public static string Serialize<T>(T obj)
    {
        Type type = typeof(T);
        PropertyInfo[] properties = type.GetProperties();
        
        List<string> jsonPairs = new List<string>();
        
        foreach (PropertyInfo property in properties)
        {
            JsonPropertyAttribute jsonProp = property.GetCustomAttribute<JsonPropertyAttribute>();
            
            // Ohita jos Ignore = true
            if (jsonProp?.Ignore == true)
                continue;
            
            string propertyName = jsonProp?.Name ?? property.Name;
            object value = property.GetValue(obj);
            
            string jsonValue;
            if (value == null)
            {
                jsonValue = "null";
            }
            else if (value is string)
            {
                jsonValue = $"\"{value}\"";
            }
            else if (value is DateTime dateTime)
            {
                jsonValue = $"\"{dateTime:yyyy-MM-dd HH:mm:ss}\"";
            }
            else
            {
                jsonValue = value.ToString();
            }
            
            jsonPairs.Add($"\"{propertyName}\": {jsonValue}");
        }
        
        return "{\n  " + string.Join(",\n  ", jsonPairs) + "\n}";
    }
}

// Käyttö
User user = new User
{
    UserId = 123,
    Name = "Matti Meikäläinen",
    Email = "matti@example.com",
    Password = "secret123",
    CreatedAt = new DateTime(2026, 1, 15)
};

string json = SimpleJsonSerializer.Serialize(user);
Console.WriteLine(json);
// Output:
// {
//   "id": 123,
//   "full_name": "Matti Meikäläinen",
//   "email_address": "matti@example.com",
//   "CreatedAt": "2026-01-15 00:00:00"
// }
// Huomaa: Password jätetty pois (Ignore = true)
```

---

## Kattava esimerkki: Plugin-järjestelmä

Tämä esimerkki yhdistää kaikki opitut asiat luomalla yksinkertaisen plugin-järjestelmän.

```csharp
// Plugin-attribuutit
[AttributeUsage(AttributeTargets.Class)]
public class PluginAttribute : Attribute
{
    public string Name { get; }
    public string Version { get; }
    public string Description { get; set; }
    public string Author { get; set; }
    
    public PluginAttribute(string name, string version)
    {
        Name = name ?? throw new ArgumentNullException(nameof(name));
        Version = version ?? throw new ArgumentNullException(nameof(version));
    }
}

[AttributeUsage(AttributeTargets.Method)]
public class PluginCommandAttribute : Attribute
{
    public string Command { get; }
    public string Description { get; set; }
    public string[] Aliases { get; set; }
    
    public PluginCommandAttribute(string command)
    {
        Command = command ?? throw new ArgumentNullException(nameof(command));
    }
}

// Plugin-rajapinta
public interface IPlugin
{
    void Initialize();
}

// Plugin-esimerkit
[Plugin("FileManager", "1.0.0", 
    Description = "Manages files and directories", 
    Author = "Matti")]
public class FileManagerPlugin : IPlugin
{
    public void Initialize()
    {
        Console.WriteLine("FileManagerPlugin initialized");
    }
    
    [PluginCommand("list", Description = "Lists files in directory", Aliases = new[] { "ls", "dir" })]
    public void ListFiles(string path)
    {
        Console.WriteLine($"Listing files in: {path}");
    }
    
    [PluginCommand("delete", Description = "Deletes a file", Aliases = new[] { "del", "rm" })]
    public void DeleteFile(string fileName)
    {
        Console.WriteLine($"Deleting file: {fileName}");
    }
}

[Plugin("Calculator", "2.1.0",
    Description = "Performs calculations",
    Author = "Maija")]
public class CalculatorPlugin : IPlugin
{
    public void Initialize()
    {
        Console.WriteLine("CalculatorPlugin initialized");
    }
    
    [PluginCommand("add", Description = "Adds two numbers")]
    public void Add(int a, int b)
    {
        Console.WriteLine($"{a} + {b} = {a + b}");
    }
    
    [PluginCommand("multiply", Description = "Multiplies two numbers", Aliases = new[] { "mul" })]
    public void Multiply(int a, int b)
    {
        Console.WriteLine($"{a} * {b} = {a * b}");
    }
}

// Plugin-järjestelmä
public class PluginSystem
{
    private List<IPlugin> _plugins = new List<IPlugin>();
    
    public void LoadPlugins(Assembly assembly)
    {
        Type[] types = assembly.GetTypes();
        
        foreach (Type type in types)
        {
            PluginAttribute pluginAttr = type.GetCustomAttribute<PluginAttribute>();
            
            if (pluginAttr != null && typeof(IPlugin).IsAssignableFrom(type))
            {
                IPlugin plugin = (IPlugin)Activator.CreateInstance(type);
                _plugins.Add(plugin);
                
                Console.WriteLine($"\nLoaded plugin: {pluginAttr.Name} v{pluginAttr.Version}");
                Console.WriteLine($"  Description: {pluginAttr.Description}");
                Console.WriteLine($"  Author: {pluginAttr.Author}");
                
                plugin.Initialize();
                
                // Listaa komennot
                ListCommands(type);
            }
        }
    }
    
    private void ListCommands(Type pluginType)
    {
        Console.WriteLine("  Commands:");
        
        MethodInfo[] methods = pluginType.GetMethods(
            BindingFlags.Public | 
            BindingFlags.Instance | 
            BindingFlags.DeclaredOnly);
        
        foreach (MethodInfo method in methods)
        {
            PluginCommandAttribute cmdAttr = method.GetCustomAttribute<PluginCommandAttribute>();
            
            if (cmdAttr != null)
            {
                Console.Write($"    - {cmdAttr.Command}");
                
                if (cmdAttr.Aliases != null && cmdAttr.Aliases.Length > 0)
                {
                    Console.Write($" (aliases: {string.Join(", ", cmdAttr.Aliases)})");
                }
                
                Console.WriteLine();
                
                if (!string.IsNullOrEmpty(cmdAttr.Description))
                {
                    Console.WriteLine($"      {cmdAttr.Description}");
                }
            }
        }
    }
    
    public void ExecuteCommand(string pluginName, string command, params object[] args)
    {
        foreach (IPlugin plugin in _plugins)
        {
            Type pluginType = plugin.GetType();
            PluginAttribute pluginAttr = pluginType.GetCustomAttribute<PluginAttribute>();
            
            if (pluginAttr.Name.Equals(pluginName, StringComparison.OrdinalIgnoreCase))
            {
                MethodInfo[] methods = pluginType.GetMethods();
                
                foreach (MethodInfo method in methods)
                {
                    PluginCommandAttribute cmdAttr = method.GetCustomAttribute<PluginCommandAttribute>();
                    
                    if (cmdAttr != null)
                    {
                        bool isMatch = cmdAttr.Command.Equals(command, StringComparison.OrdinalIgnoreCase);
                        
                        if (!isMatch && cmdAttr.Aliases != null)
                        {
                            isMatch = cmdAttr.Aliases.Any(alias => 
                                alias.Equals(command, StringComparison.OrdinalIgnoreCase));
                        }
                        
                        if (isMatch)
                        {
                            method.Invoke(plugin, args);
                            return;
                        }
                    }
                }
            }
        }
        
        Console.WriteLine($"Command not found: {pluginName}.{command}");
    }
    
    public void ListAllPlugins()
    {
        Console.WriteLine("\n=== Installed Plugins ===");
        
        foreach (IPlugin plugin in _plugins)
        {
            Type pluginType = plugin.GetType();
            PluginAttribute pluginAttr = pluginType.GetCustomAttribute<PluginAttribute>();
            
            if (pluginAttr != null)
            {
                Console.WriteLine($"\n{pluginAttr.Name} v{pluginAttr.Version}");
                Console.WriteLine($"  {pluginAttr.Description}");
                Console.WriteLine($"  By: {pluginAttr.Author}");
            }
        }
    }
}

// Käyttö
public class Program
{
    public static void Main()
    {
        PluginSystem system = new PluginSystem();
        
        // Lataa pluginit nykyisestä assemblysta
        system.LoadPlugins(Assembly.GetExecutingAssembly());
        
        Console.WriteLine("\n=== Testing Commands ===");
        
        // Suorita komentoja
        system.ExecuteCommand("FileManager", "list", "C:\\Temp");
        system.ExecuteCommand("FileManager", "ls", "C:\\Documents");  // Alias
        system.ExecuteCommand("Calculator", "add", 10, 20);
        system.ExecuteCommand("Calculator", "mul", 5, 7);  // Alias
        
        // Listaa kaikki pluginit
        system.ListAllPlugins();
    }
}

/* Output:

Loaded plugin: FileManager v1.0.0
  Description: Manages files and directories
  Author: Matti
FileManagerPlugin initialized
  Commands:
    - list (aliases: ls, dir)
      Lists files in directory
    - delete (aliases: del, rm)
      Deletes a file

Loaded plugin: Calculator v2.1.0
  Description: Performs calculations
  Author: Maija
CalculatorPlugin initialized
  Commands:
    - add
      Adds two numbers
    - multiply (aliases: mul)
      Multiplies two numbers

=== Testing Commands ===
Listing files in: C:\Temp
Listing files in: C:\Documents
10 + 20 = 30
5 * 7 = 35

=== Installed Plugins ===

FileManager v1.0.0
  Manages files and directories
  By: Matti

Calculator v2.1.0
  Performs calculations
  By: Maija
*/
```

---

## Yhteenveto

Nämä esimerkit kattavat:
- Sisäänrakennetut attribuutit (Obsolete, Conditional, Flags, jne.)
- Omien attribuuttien luominen
- Reflection ja attribuuttien lukeminen
- Validointi attribuuteilla
- Routing-järjestelmä attribuuteilla
- Serialization-attribuutit
- Kattavan plugin-järjestelmän

Palaa teoriaan: [Attributes.md](Attributes.md)
