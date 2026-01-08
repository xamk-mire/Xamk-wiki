# Staattiset luokat ja metodit (static keyword)

`static`-avainsana C#-kielessä tarkoittaa, että jäsen (muuttuja, metodi, luokka) kuuluu luokkaan itselleen, ei luokan instanssille (oliolle).

## Staattiset metodit

Staattinen metodi kuuluu luokalle, ei olioille. Sitä kutsutaan suoraan luokan nimen kautta.

### Perussyntaksi

```csharp
public class MathHelper
{
    // Staattinen metodi
    public static int Add(int a, int b)
    {
        return a + b;
    }
    
    // Ei-staattinen metodi
    public int Multiply(int a, int b)
    {
        return a * b;
    }
}

// Käyttö
int sum = MathHelper.Add(5, 3);  // ✅ Staattinen - kutsutaan luokan kautta

MathHelper helper = new MathHelper();
int product = helper.Multiply(5, 3);  // ✅ Ei-staattinen - kutsutaan olion kautta
```

### Esimerkki: Utility-luokka

```csharp
public class StringHelper
{
    // Staattinen metodi - ei tarvitse luoda oliota
    public static string Reverse(string text)
    {
        char[] chars = text.ToCharArray();
        Array.Reverse(chars);
        return new string(chars);
    }
    
    public static bool IsEmail(string text)
    {
        return text.Contains("@") && text.Contains(".");
    }
    
    public static string Capitalize(string text)
    {
        if (string.IsNullOrEmpty(text))
            return text;
        
        return char.ToUpper(text[0]) + text.Substring(1).ToLower();
    }
}

// Käyttö - ei tarvitse luoda oliota!
string reversed = StringHelper.Reverse("Hei");
bool isEmail = StringHelper.IsEmail("test@example.com");
string capitalized = StringHelper.Capitalize("matti");
```

## Staattiset muuttujat (Fields)

Staattinen muuttuja on jaettu kaikkien luokan instanssien kesken:

```csharp
public class Counter
{
    // Staattinen muuttuja - jaettu kaikkien instanssien kesken
    private static int totalCount = 0;
    
    // Ei-staattinen muuttuja - jokaisella oliolla oma
    private int instanceCount = 0;
    
    public void Increment()
    {
        totalCount++;      // Kasvattaa kaikkien olioiden yhteistä laskuria
        instanceCount++;   // Kasvattaa vain tämän olion laskuria
    }
    
    public static int GetTotalCount()
    {
        return totalCount;  // Staattinen metodi voi käyttää staattista muuttujaa
    }
    
    public int GetInstanceCount()
    {
        return instanceCount;
    }
}

// Käyttö
Counter counter1 = new Counter();
Counter counter2 = new Counter();

counter1.Increment();
counter2.Increment();
counter2.Increment();

Console.WriteLine(Counter.GetTotalCount());    // 3 (kaikkien olioiden yhteensä)
Console.WriteLine(counter1.GetInstanceCount()); // 1
Console.WriteLine(counter2.GetInstanceCount()); // 2
```

## Staattiset propertyt

```csharp
public class AppConfig
{
    // Staattinen property
    public static string AppName { get; set; } = "MyApp";
    public static string Version { get; set; } = "1.0.0";
    
    // Staattinen readonly property
    public static string Environment { get; } = "Development";
}

// Käyttö
AppConfig.AppName = "NewApp";
Console.WriteLine(AppConfig.AppName);  // "NewApp"
Console.WriteLine(AppConfig.Version);   // "1.0.0"
```

## Staattiset luokat

Staattinen luokka ei voi luoda instansseja. Kaikki jäsenet täytyy olla staattisia:

```csharp
// ✅ HYVÄ: Staattinen utility-luokka
public static class MathUtils
{
    public static double CalculateCircleArea(double radius)
    {
        return Math.PI * radius * radius;
    }
    
    public static double CalculateRectangleArea(double width, double height)
    {
        return width * height;
    }
    
    // Staattinen vakio
    public const double Pi = 3.14159;
}

// Käyttö
double area = MathUtils.CalculateCircleArea(5.0);

// ❌ EI TOIMI: Ei voi luoda instanssia
// MathUtils utils = new MathUtils(); // Virhe!
```

## Staattinen konstruktori

Staattinen konstruktori suoritetaan ennen kuin luokkaa käytetään ensimmäisen kerran:

```csharp
public class Logger
{
    private static string logFile;
    
    // Staattinen konstruktori - suoritetaan automaattisesti
    static Logger()
    {
        logFile = "application.log";
        Console.WriteLine("Logger alustettu");
    }
    
    public static void Log(string message)
    {
        // Kirjoita log-tiedostoon
        File.AppendAllText(logFile, $"{DateTime.Now}: {message}\n");
    }
}

// Ensimmäinen käyttö kutsuu staattisen konstruktorin
Logger.Log("Sovellus käynnistyi"); // "Logger alustettu" tulostetaan ensin
```

## Yleisiä käyttökohteita

### 1. Utility-luokat

```csharp
public static class FileHelper
{
    public static bool FileExists(string path)
    {
        return File.Exists(path);
    }
    
    public static string ReadAllText(string path)
    {
        return File.ReadAllText(path);
    }
    
    public static void WriteAllText(string path, string content)
    {
        File.WriteAllText(path, content);
    }
}
```

### 2. Vakioiden säilytys

```csharp
public static class Constants
{
    public const int MaxRetryAttempts = 3;
    public const int TimeoutSeconds = 30;
    public const string DefaultConnectionString = "Server=localhost;";
}
```

### 3. Extension-metodit

```csharp
public static class StringExtensions
{
    public static bool IsValidEmail(this string email)
    {
        return email.Contains("@") && email.Contains(".");
    }
    
    public static string Reverse(this string text)
    {
        char[] chars = text.ToCharArray();
        Array.Reverse(chars);
        return new string(chars);
    }
}

// Käyttö
string email = "test@example.com";
bool isValid = email.IsValidEmail();  // Extension-metodi
string reversed = email.Reverse();
```

## Tärkeät huomiot

1. **Staattiset jäsenet eivät voi käyttää ei-staattisia jäseniä**
   ```csharp
   public class Example
   {
       private int instanceField = 10;
       
       public static void StaticMethod()
       {
           // ❌ Virhe: Ei voi käyttää instanceField
           // Console.WriteLine(instanceField);
       }
   }
   ```

2. **Ei-staattiset jäsenet voivat käyttää staattisia jäseniä**
   ```csharp
   public class Example
   {
       private static int staticField = 10;
       
       public void InstanceMethod()
       {
           // ✅ OK: Voimme käyttää staattista kenttää
           Console.WriteLine(staticField);
       }
   }
   ```

3. **Staattinen luokka ei voi periä tai olla peritty**

## Hyödyt ja milloin käyttää

`static`-avainsanan käyttö C#:ssa tarjoaa useita etuja:

### 1. Muistin säästö

Koska `static`-muuttujat ovat yhteisiä kaikille luokan instansseille, ne vievät muistia vain kerran, riippumatta siitä, kuinka monta instanssia luokasta on luotu. Tämä voi säästää merkittävästi muistia, kun muuttujan arvon on oltava sama kaikissa instansseissa.

### 2. Globaalien arvojen hallinta

`static`-muuttujien avulla voidaan helposti taata, että koko sovellus käyttää samoja arvoja. (Globaali tarkoittaa luokkaa/metodia, joka on saatavilla/näkyvissä koko ohjelmalle)

### 3. Ei tarvetta olion instanssille

`static`-metodeita voidaan kutsua ilman, että luokasta pitäisi tehdä olio. Tämä tekee niistä käteviä toiminnallisuuksille, jotka eivät vaadi pääsyä olion erityiseen tilaan, kuten apufunktioille tai matemaattisille laskutoimituksille.

### 4. Organisointi

`static`-luokat, kuten `System.Math`, voivat ryhmitellä yhteen liittyviä funktioita ja arvoja, jolloin koodista tulee selkeämpää ja helpompaa ylläpitää.

### 5. Suorituskyky

Joissakin tapauksissa `static`-metodien käyttö voi olla hieman nopeampaa kuin ei-static-metodien, koska ei ole tarvetta olion viitteelle tai `this`-avainsanan käytölle. Vaikka tämä ero on usein minimaalinen, se voi olla merkittävä tietyissä suorituskykyherkissä tilanteissa.

### 6. Vältetään virheitä

Kun luokka on merkitty `static`, se ei voi olla instansioitu, mikä tarkoittaa, että kehittäjät eivät voi vahingossa yrittää tehdä siitä instanssia. Tämä voi estää tiettyjä ohjelmointivirheitä.

## Haasteet ja huomiot

Toisaalta `static`-jäsenten käytössä on myös haittapuolia ja haasteita, erityisesti kun puhutaan monisäikeisistä sovelluksista:

- **Monisäikeisyys**: Koska `static`-muuttujat ovat yhteisiä kaikille säikeille, niiden arvojen muuttaminen yhdestä säikeestä voi aiheuttaa odottamattomia tuloksia toisissa säikeissä, ellei asiaa käsitellä asianmukaisesti (esim. käyttämällä `lock`-lauseita tai muita synkronointimekanismeja).

## Yhteenveto

- `static` tarkoittaa, että jäsen kuuluu luokalle, ei olioille
- Staattisia metodeja kutsutaan luokan nimen kautta
- Staattiset muuttujat ovat jaettuja kaikkien instanssien kesken
- Staattiset luokat eivät voi luoda instansseja
- Käytä staattisia jäseniä utility-metodeihin ja vakioihin
- Yleisesti ottaen `static`-avainsana tarjoaa keinoja tehdä koodista tehokkaampaa ja järjestäytyneempää tietyissä tilanteissa, mutta sen käyttöön liittyy myös vastuuta varmistaa, että se ei aiheuta odottamattomia sivuvaikutuksia

Seuraavaksi: [Funktiot ja Metodit](Functions-and-Methods.md)

