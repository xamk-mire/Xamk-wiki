# Poikkeusten käsittely (Exception Handling)

Poikkeukset (exceptions) ovat virhetilanteita, jotka tapahtuvat ohjelman suorituksen aikana. C#-kielessä poikkeukset käsitellään `try-catch`-lohkoilla.

## Mitä ovat poikkeukset?

Poikkeus on erityinen olio, joka heitetään kun virhetilanne tapahtuu. Jos poikkeusta ei käsitellä, ohjelma kaatuu.

## Try-Catch-lohko

### Perussyntaksi

```csharp
try
{
    // Koodi, joka voi aiheuttaa poikkeuksen
}
catch (ExceptionType ex)
{
    // Koodi, joka suoritetaan jos poikkeus tapahtuu
}
finally
{
    // Koodi, joka suoritetaan aina (valinnainen)
}
```

### Yksinkertainen esimerkki

```csharp
try
{
    int number = int.Parse("123");
    Console.WriteLine($"Numero: {number}");
}
catch (FormatException ex)
{
    Console.WriteLine($"Virhe: {ex.Message}");
}
```

## Yleisimmät poikkeustyypit

### 1. FormatException

Tapahtuu kun merkkijonoa ei voida muuntaa numeroksi:

```csharp
try
{
    int number = int.Parse("abc");  // ❌ Virhe!
}
catch (FormatException ex)
{
    Console.WriteLine($"Muunnosvirhe: {ex.Message}");
}
```

### 2. NullReferenceException

Tapahtuu kun yritetään käyttää null-viittausta:

```csharp
string text = null;
try
{
    int length = text.Length;  // ❌ Virhe! text on null
}
catch (NullReferenceException ex)
{
    Console.WriteLine($"Null-viittaus: {ex.Message}");
}
```

### 3. ArgumentNullException

Tapahtuu kun null-arvo annetaan parametrina:

```csharp
public void ProcessUser(User user)
{
    if (user == null)
        throw new ArgumentNullException(nameof(user), "Käyttäjä ei voi olla null");
    
    // Käsittele käyttäjää
}
```

### 4. IndexOutOfRangeException

Tapahtuu kun yritetään käyttää taulukon ulkopuolella olevaa indeksiä:

```csharp
int[] numbers = { 1, 2, 3 };
try
{
    int value = numbers[10];  // ❌ Virhe! Indeksi 10 ei ole olemassa
}
catch (IndexOutOfRangeException ex)
{
    Console.WriteLine($"Indeksivirhe: {ex.Message}");
}
```

### 5. DivideByZeroException

Tapahtuu kun yritetään jakaa nollalla:

```csharp
try
{
    int result = 10 / 0;  // ❌ Virhe!
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Jako nollalla: {ex.Message}");
}
```

## Useita catch-lohkoja

Voit käsitellä eri poikkeustyypit erikseen:

```csharp
try
{
    int number = int.Parse(Console.ReadLine());
    int result = 100 / number;
    Console.WriteLine($"Tulos: {result}");
}
catch (FormatException ex)
{
    Console.WriteLine("Syöte ei ole kelvollinen numero");
}
catch (DivideByZeroException ex)
{
    Console.WriteLine("Ei voi jakaa nollalla");
}
catch (Exception ex)
{
    Console.WriteLine($"Odottamaton virhe: {ex.Message}");
}
```

## Finally-lohko

`finally`-lohko suoritetaan aina, riippumatta siitä tapahtuiko poikkeus vai ei:

```csharp
FileStream file = null;
try
{
    file = File.Open("data.txt", FileMode.Open);
    // Käsittele tiedostoa
}
catch (FileNotFoundException ex)
{
    Console.WriteLine($"Tiedostoa ei löytynyt: {ex.Message}");
}
finally
{
    // Varmista että tiedosto suljetaan aina
    if (file != null)
        file.Close();
}
```

### Using-lause (parempi tapa)

`using`-lause sulkee automaattisesti resurssit:

```csharp
// ✅ HYVÄ: using-lause sulkee automaattisesti
using (FileStream file = File.Open("data.txt", FileMode.Open))
{
    // Käsittele tiedostoa
    // Tiedosto suljetaan automaattisesti
}

// ✅ HYVÄ: using-lause ilman aaltosulkeita (C# 8.0+)
using var file = File.Open("data.txt", FileMode.Open);
// Tiedosto suljetaan automaattisesti lohkon lopussa
```

## Poikkeuksen heittäminen

Voit heittää poikkeuksen itse `throw`-avainsanalla:

```csharp
public int Divide(int a, int b)
{
    if (b == 0)
        throw new DivideByZeroException("Jakaja ei voi olla nolla");
    
    return a / b;
}

// Käyttö
try
{
    int result = Divide(10, 0);
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Virhe: {ex.Message}");
}
```

## Mukautettu poikkeusluokka

Voit luoda oman poikkeusluokan:

```csharp
public class InvalidAgeException : Exception
{
    public InvalidAgeException(string message) : base(message)
    {
    }
    
    public InvalidAgeException(string message, Exception innerException) 
        : base(message, innerException)
    {
    }
}

// Käyttö
public void SetAge(int age)
{
    if (age < 0 || age > 150)
        throw new InvalidAgeException($"Ikä {age} ei ole kelvollinen");
    
    this.age = age;
}

try
{
    person.SetAge(-5);
}
catch (InvalidAgeException ex)
{
    Console.WriteLine($"Ikävirhe: {ex.Message}");
}
```

## Poikkeusten käsittelyn best practices

### 1. Käsittele spesifiset poikkeukset ensin

```csharp
// ✅ HYVÄ
try
{
    // Koodi
}
catch (FormatException ex)
{
    // Spesifinen käsittely
}
catch (Exception ex)
{
    // Yleinen käsittely viimeisenä
}
```

### 2. Älä jätä catch-lohkoa tyhjäksi

```csharp
// ❌ HUONO
try
{
    DoSomething();
}
catch (Exception ex)
{
    // Tyhjä - virhe piilotetaan!
}

// ✅ HYVÄ
try
{
    DoSomething();
}
catch (Exception ex)
{
    // Logita virhe
    Logger.LogError(ex);
    // Tai heitä eteenpäin
    throw;
}
```

### 3. Käytä using-lausetta resursseille

```csharp
// ✅ HYVÄ
using (var connection = new SqlConnection(connectionString))
{
    // Käytä yhteyttä
}

// ❌ HUONO
SqlConnection connection = null;
try
{
    connection = new SqlConnection(connectionString);
    // Käytä yhteyttä
}
finally
{
    if (connection != null)
        connection.Close();
}
```

### 4. Tarkista null-arvoja ennen käyttöä

```csharp
// ✅ HYVÄ
if (user != null)
{
    Console.WriteLine(user.Name);
}

// ❌ HUONO
try
{
    Console.WriteLine(user.Name);  // Voit aiheuttaa NullReferenceException
}
catch (NullReferenceException)
{
    // Käsittele virhe
}
```

## Yhteenveto

- Poikkeukset käsitellään `try-catch`-lohkoilla
- `finally`-lohko suoritetaan aina
- Käytä `using`-lausetta resursseille
- Käsittele spesifiset poikkeukset ensin
- Älä piilota poikkeuksia tyhjällä catch-lohkolla

Seuraavaksi: [Funktiot ja Metodit](Functions-and-Methods.md)

