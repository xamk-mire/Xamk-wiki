# Attribuutit (Attributes)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mikä on attribuutti](#mikä-on-attribuutti)
3. [Miksi attribuutteja käytetään](#miksi-attribuutteja-käytetään)
4. [Attribuuttien syntaksi](#attribuuttien-syntaksi)
5. [Sisäänrakennetut attribuutit](#sisäänrakennetut-attribuutit)
6. [Omien attribuuttien luominen](#omien-attribuuttien-luominen)
7. [Reflection ja attribuutit](#reflection-ja-attribuutit)
8. [AttributeUsage](#attributeusage)
9. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Johdanto

Attribuutit ovat C#:n metadatamekanismi, joka mahdollistaa deklaratiivisen tiedon liittämisen koodielementteihin. Ne ovat tehokas tapa lisätä informaatiota luokkiin, metodeihin, ominaisuuksiin ja muihin koodielementteihin ilman, että varsinaista logiikkaa tarvitsee muuttaa.

### Materiaalin rakenne

- **Tämä tiedosto**: Teoria ja käsitteet
- **[Attributes-Examples.md](Attributes-Examples.md)**: Kattavat koodiesimerkit

### Hyödyllisiä linkkejä

- [Microsoft: Attributes](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/)
- [Microsoft: Creating Custom Attributes](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/creating-custom-attributes)
- [Microsoft: Reflection](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/accessing-attributes-by-using-reflection)

---

## Mikä on attribuutti

**Attribuutti** on erikoinen luokka, joka lisää metadataa koodielementteihin. Attribuutit eivät muuta koodin toimintaa suoraan, vaan ne tarjoavat lisätietoa, jota voidaan lukea ajonaikana (reflection) tai kääntäjän toimesta.

### Peruskäsite

```csharp
[AttributeName]
public class MyClass
{
    [AttributeName]
    public void MyMethod()
    {
    }
}
```

Attribuutti on:
- Luokka, joka perii `System.Attribute`-luokan
- Kirjoitetaan hakasulkeisiin `[...]`
- Liitetään koodielementtiin (luokka, metodi, ominaisuus, jne.)
- Metadata, joka voidaan lukea reflectionin avulla

---

## Miksi attribuutteja käytetään

### 1. Deklaratiivinen ohjelmointi

Attribuutit mahdollistavat deklaratiivisen tavan ilmaista asioita, jotka muuten vaatisivat imperatiivista koodia.

```csharp
// Ilman attribuuttia
public string Name 
{ 
    get { return _name; }
    set 
    {
        if (string.IsNullOrEmpty(value))
            throw new ValidationException("Name is required");
        _name = value;
    }
}

// Attribuutilla
[Required]
public string Name { get; set; }
```

### 2. Koodin dokumentointi

Attribuutit voivat toimia elävänä dokumentaationa:

```csharp
[Obsolete("Use NewMethod instead", false)]
public void OldMethod()
{
}
```

### 3. Framework-integraatio

Monet frameworkit käyttävät attribuutteja:

```csharp
// ASP.NET
[Route("api/users")]
public class UserController : Controller
{
    [HttpGet]
    public IActionResult GetAll()
    {
    }
}

// Entity Framework
[Table("Users")]
public class User
{
    [Key]
    public int Id { get; set; }
    
    [MaxLength(100)]
    public string Name { get; set; }
}

// Serialization
[Serializable]
public class Person
{
    [JsonProperty("full_name")]
    public string Name { get; set; }
}
```

### 4. Kääntäjän ohjaus

Attribuutit voivat ohjata kääntäjää:

```csharp
[Conditional("DEBUG")]
public void LogDebugInfo()
{
    // Suoritetaan vain DEBUG-moodissa
}
```

---

## Attribuuttien syntaksi

### Perus syntaksi

```csharp
[AttributeName]
public class MyClass { }
```

### Parametrit

Attribuutit voivat ottaa parametreja:

```csharp
[AttributeName("parameter")]
public class MyClass { }

[AttributeName("param1", 42)]
public class MyClass2 { }
```

### Nimetyt parametrit

```csharp
[AttributeName(Name = "John", Age = 30)]
public class MyClass { }
```

### Useita attribuutteja

```csharp
// Useita attribuutteja
[Attribute1]
[Attribute2]
public class MyClass { }

// Sama rivi
[Attribute1, Attribute2]
public class MyClass { }
```

### Attribuutin nimi

Attribuutin nimestä voi jättää `Attribute`-loppuosan pois:

```csharp
// Luokka: ObsoleteAttribute
[Obsolete]  // Toimii
[ObsoleteAttribute]  // Toimii myös
public void OldMethod() { }
```

---

## Sisäänrakennetut attribuutit

.NET tarjoaa monia valmiita attribuutteja.

### [Obsolete] - Vanhentunut koodi

Merkitsee koodin vanhentuneeksi ja varoittaa käyttäjiä.

```csharp
[Obsolete("Use NewMethod instead")]
public void OldMethod()
{
}

[Obsolete("This method is deprecated", true)] // Aiheuttaa virheen
public void VeryOldMethod()
{
}
```

**Parametrit:**
- `message` (string): Varoitusviesti
- `error` (bool): Jos `true`, aiheuttaa kääntäjävirheen varoituksen sijaan

### [Serializable] - Serialisoitavuus

Merkitsee luokan serialisoitavaksi.

```csharp
[Serializable]
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}
```

### [DllImport] - Natiivikirjaston kutsuminen

Mahdollistaa natiivikirjastojen (C/C++) funktioiden kutsumisen.

```csharp
[DllImport("user32.dll")]
public static extern int MessageBox(IntPtr hWnd, string text, string caption, uint type);
```

### [Conditional] - Ehdollinen suoritus

Metodi suoritetaan vain tietyn symbolin ollessa määriteltynä.

```csharp
[Conditional("DEBUG")]
public void LogDebugInfo()
{
    Console.WriteLine("Debug info");
}
```

### [CallerMemberName], [CallerFilePath], [CallerLineNumber]

Automaattisesti syöttävät kutsupaikkatiedot.

```csharp
public void Log(
    string message,
    [CallerMemberName] string memberName = "",
    [CallerFilePath] string filePath = "",
    [CallerLineNumber] int lineNumber = 0)
{
    Console.WriteLine($"{filePath}:{lineNumber} - {memberName}: {message}");
}
```

### [DebuggerDisplay] - Debuggerin näyttö

Määrittää, miten objekti näkytetään debuggerissa.

```csharp
[DebuggerDisplay("Person: {Name}, Age: {Age}")]
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}
```

### [Flags] - Lippu-enum

Merkitsee enumin lipuiksi (bitwise-operaatioita varten).

```csharp
[Flags]
public enum FileAccess
{
    None = 0,
    Read = 1,
    Write = 2,
    ReadWrite = Read | Write
}
```

### [InternalsVisibleTo] - Assembly-näkyvyys

Mahdollistaa `internal`-jäsenten näkyvyyden toiselle assemblylle.

```csharp
[assembly: InternalsVisibleTo("MyProject.Tests")]
```

---

## Omien attribuuttien luominen

Voit luoda omia attribuutteja perimällä `System.Attribute`-luokan.

### Yksinkertainen attribuutti

```csharp
// Attribuutin määrittely
public class AuthorAttribute : Attribute
{
    public string Name { get; }
    
    public AuthorAttribute(string name)
    {
        Name = name;
    }
}

// Käyttö
[Author("Matti Meikäläinen")]
public class MyClass
{
}
```

### Attribuutti useilla ominaisuuksilla

```csharp
public class DocumentationAttribute : Attribute
{
    public string Description { get; }
    public string Version { get; set; }
    public string Author { get; set; }
    public DateTime LastModified { get; set; }
    
    public DocumentationAttribute(string description)
    {
        Description = description;
    }
}

// Käyttö
[Documentation(
    "This class handles user authentication",
    Version = "2.0",
    Author = "Matti",
    LastModified = "2026-01-15")]
public class AuthService
{
}
```

---

## Reflection ja attribuutit

Reflectionin avulla voit lukea attribuutteja ajonaikana.

### Attribuutin lukeminen luokasta

```csharp
Type type = typeof(MyClass);
AuthorAttribute attribute = (AuthorAttribute)Attribute.GetCustomAttribute(
    type, 
    typeof(AuthorAttribute));

if (attribute != null)
{
    Console.WriteLine($"Author: {attribute.Name}");
}
```

### Attribuutin lukeminen metodista

```csharp
MethodInfo method = typeof(MyClass).GetMethod("MyMethod");
ObsoleteAttribute attribute = method.GetCustomAttribute<ObsoleteAttribute>();

if (attribute != null)
{
    Console.WriteLine($"Method is obsolete: {attribute.Message}");
}
```

### Kaikkien attribuuttien lukeminen

```csharp
Type type = typeof(MyClass);
object[] attributes = type.GetCustomAttributes(true);

foreach (Attribute attr in attributes)
{
    Console.WriteLine($"Attribute: {attr.GetType().Name}");
}
```

### Tietyn tyyppisten attribuuttien etsiminen

```csharp
Type type = typeof(MyClass);
IEnumerable<AuthorAttribute> authorAttributes = 
    type.GetCustomAttributes<AuthorAttribute>();

foreach (AuthorAttribute attr in authorAttributes)
{
    Console.WriteLine($"Author: {attr.Name}");
}
```

---

## AttributeUsage

`AttributeUsage`-attribuutti määrittää, miten attribuuttia voidaan käyttää.

### AttributeTargets

Määrittää, mihin koodielementteihin attribuuttia voidaan soveltaa.

```csharp
[AttributeUsage(AttributeTargets.Class)]
public class MyClassOnlyAttribute : Attribute
{
}

[AttributeUsage(AttributeTargets.Method | AttributeTargets.Property)]
public class MyMethodOrPropertyAttribute : Attribute
{
}
```

**Mahdolliset arvot:**
- `Assembly` - Koko assembly
- `Class` - Luokat
- `Constructor` - Konstruktorit
- `Delegate` - Delegaatit
- `Enum` - Enumit
- `Event` - Eventit
- `Field` - Kentät
- `Interface` - Rajapinnat
- `Method` - Metodit
- `Parameter` - Parametrit
- `Property` - Ominaisuudet
- `ReturnValue` - Paluuarvot
- `Struct` - Struktuurit
- `All` - Kaikki (oletus)

### AllowMultiple

Määrittää, voiko samaa attribuuttia käyttää useita kertoja samalla elementillä.

```csharp
[AttributeUsage(AttributeTargets.Class, AllowMultiple = true)]
public class AuthorAttribute : Attribute
{
    public string Name { get; }
    
    public AuthorAttribute(string name)
    {
        Name = name;
    }
}

// Nyt voidaan käyttää useita kertoja
[Author("Matti")]
[Author("Maija")]
public class MyClass
{
}
```

### Inherited

Määrittää, perivätkö aliluokat attribuutin.

```csharp
[AttributeUsage(AttributeTargets.Class, Inherited = true)]
public class MyAttribute : Attribute
{
}

[MyAttribute]
public class BaseClass
{
}

// DerivedClass saa automaattisesti MyAttribute-attribuutin
public class DerivedClass : BaseClass
{
}
```

---

## Parhaat käytännöt

### 1. Nimeä attribuutit selkeästi

✅ **Hyvä:**
```csharp
public class AuthorAttribute : Attribute { }
public class ValidationAttribute : Attribute { }
```

❌ **Huono:**
```csharp
public class AttrAttribute : Attribute { }
public class MyAttr : Attribute { }
```

**Milloin käyttää:** Aina. Attribuutin nimen pitää kuvata sen tarkoitusta.

**Miksi:** Selkeä nimeäminen helpottaa koodin lukemista ja ylläpitoa.

### 2. Käytä AttributeUsage-attribuuttia

✅ **Hyvä:**
```csharp
[AttributeUsage(AttributeTargets.Method, AllowMultiple = false)]
public class HttpGetAttribute : Attribute { }
```

❌ **Huono:**
```csharp
// Ei AttributeUsage-attribuuttia
public class HttpGetAttribute : Attribute { }
```

**Milloin käyttää:** Aina kun luot oman attribuutin.

**Miksi:** Määrittää selkeästi, miten attribuuttia voidaan käyttää ja estää virheellisen käytön.

### 3. Tee attribuuteista muuttumattomia (immutable)

✅ **Hyvä:**
```csharp
public class AuthorAttribute : Attribute
{
    public string Name { get; }  // Vain get
    
    public AuthorAttribute(string name)
    {
        Name = name;
    }
}
```

❌ **Huono:**
```csharp
public class AuthorAttribute : Attribute
{
    public string Name { get; set; }  // Muokattavissa
}
```

**Milloin käyttää:** Aina kun mahdollista. Pakolliset arvot konstruktoriin, valinnaiset set-ominaisuuksiin.

**Miksi:** Attribuutit ovat metadataa, jota ei pitäisi muokata luomisen jälkeen.

### 4. Dokumentoi attribuuttisi

✅ **Hyvä:**
```csharp
/// <summary>
/// Merkitsee metodin HTTP GET -endpointiksi.
/// </summary>
[AttributeUsage(AttributeTargets.Method)]
public class HttpGetAttribute : Attribute
{
}
```

**Milloin käyttää:** Aina.

**Miksi:** Muut kehittäjät ymmärtävät, miten attribuuttia käytetään.

### 5. Älä käytä attribuutteja liikaa

❌ **Huono:**
```csharp
[MyAttribute1]
[MyAttribute2]
[MyAttribute3]
[MyAttribute4]
[MyAttribute5]
public class MyClass
{
}
```

**Milloin käyttää:** Käytä attribuutteja vain kun ne todella tuovat lisäarvoa.

**Miksi:** Liian moni attribuutti tekee koodista vaikealukuista.

### 6. Validoi attribuutin parametrit

✅ **Hyvä:**
```csharp
public class MaxLengthAttribute : Attribute
{
    public int Length { get; }
    
    public MaxLengthAttribute(int length)
    {
        if (length <= 0)
            throw new ArgumentException("Length must be positive", nameof(length));
        
        Length = length;
    }
}
```

**Milloin käyttää:** Aina kun attribuutilla on rajoituksia.

**Miksi:** Estää virheellisten arvojen käytön.

---

## Yhteenveto

### Attribuuttien hyödyt:
✅ Deklaratiivinen ohjelmointi  
✅ Koodin dokumentointi  
✅ Framework-integraatio  
✅ Kääntäjän ohjaus  
✅ Metadata ajonaikana  
✅ Puhdas ja ylläpidettävä koodi

### Muista:
- Attribuutit periytyvät `System.Attribute`-luokasta
- Käytä `AttributeUsage`-attribuuttia määrittelemään käyttö
- Attribuutit luetaan reflectionin avulla ajonaikana
- Tee attribuuteista muuttumattomia
- Dokumentoi attribuuttisi hyvin

### Seuraavaksi:
1. Tutustu esimerkkeihin: [Attributes-Examples.md](Attributes-Examples.md)
2. Harjoittele omilla projekteilla
3. Lue lisää: [Microsoftin dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/advanced-topics/reflection-and-attributes/)

---

**Onnea attribuuttien kanssa!**
