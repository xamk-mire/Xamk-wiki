# Delegaatit (Delegates)

[Microsoftin virallinen Delegates-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)

## Mikä on delegaatti?

**Delegaatti** on C#-tyyppi, joka edustaa viittausta yhteen tai useampaan metodiin. Voidaan ajatella, että delegaatti on muuttuja, johon voidaan tallentaa funktio. Tämä mahdollistaa metodien käsittelyn muuttujina ja niiden välittämisen parametrina muihin metodeihin.

Delegaatit ovat erityisen hyödyllisiä:
- **Callback-funktioissa**: kun haluat välittää metodin toiselle metodille
- **Event handling**: tapahtumien käsittelyssä (esim. napinpainallukset)
- **LINQ-kyselyissä**: suodatus- ja muunnosoperaatioissa
- **Asynkronisessa ohjelmoinnissa**: kun haluat suorittaa jotain operaation päätyttyä

## Delegaatin määrittely ja käyttö

### Perus syntaksi

```csharp
// 1. Määrittele delegaatti-tyyppi
delegate void MyDelegate(string message);

// 2. Luo metodi, joka vastaa delegaatin allekirjoitusta
void PrintMessage(string message)
{
    Console.WriteLine(message);
}

// 3. Luo delegaatti-instanssi ja liitä metodi siihen
MyDelegate del = PrintMessage;

// 4. Kutsu delegaattia
del("Hello, World!"); // Tulostaa: Hello, World!
```

### Toinen esimerkki: Matematiikka-operaatiot

```csharp
// Delegaatti, joka ottaa kaksi int-arvoa ja palauttaa int-arvon
delegate int MathOperation(int a, int b);

// Metodit, jotka vastaavat delegaatin allekirjoitusta
int Add(int a, int b) => a + b;
int Multiply(int a, int b) => a * b;

// Käyttö
MathOperation operation = Add;
Console.WriteLine(operation(5, 3)); // 8

operation = Multiply;
Console.WriteLine(operation(5, 3)); // 15
```

## Sisäänrakennetut delegaatit: Action, Func ja Predicate

C# tarjoaa valmiit geneerisedelegaatit, jotka kattavat useimmat käyttötapaukset ilman että sinun tarvitsee määritellä omia delegaatteja.

### Action<T>

`Action` on delegaatti, joka **ei palauta arvoa** (void). Se voi ottaa 0-16 parametria.

```csharp
// Action ilman parametreja
Action greet = () => Console.WriteLine("Hello!");
greet(); // Hello!

// Action yhdellä parametrilla
Action<string> printName = name => Console.WriteLine($"Name: {name}");
printName("Alice"); // Name: Alice

// Action kahdella parametrilla
Action<int, int> printSum = (a, b) => Console.WriteLine($"Sum: {a + b}");
printSum(5, 3); // Sum: 8
```

### Func<T, TResult>

`Func` on delegaatti, joka **palauttaa arvon**. Viimeinen tyyppiparametri on palautustyyppi.

```csharp
// Func, joka ottaa int:n ja palauttaa bool:n
Func<int, bool> isEven = number => number % 2 == 0;
Console.WriteLine(isEven(4)); // True
Console.WriteLine(isEven(5)); // False

// Func, joka ottaa kaksi int:ä ja palauttaa int:n
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(10, 5)); // 15

// Func ilman parametreja, palauttaa string:n
Func<string> getMessage = () => "Hello from Func!";
Console.WriteLine(getMessage()); // Hello from Func!
```

### Predicate<T>

`Predicate` on delegaatti, joka ottaa yhden parametrin ja **palauttaa aina bool:n**. Sitä käytetään usein ehtolausekkeissa ja suodatuksessa.

```csharp
Predicate<int> isPositive = number => number > 0;
Console.WriteLine(isPositive(5));  // True
Console.WriteLine(isPositive(-3)); // False

// Käyttö List.FindAll-metodin kanssa
List<int> numbers = new List<int> { -2, -1, 0, 1, 2, 3 };
List<int> positiveNumbers = numbers.FindAll(isPositive);
// positiveNumbers = [1, 2, 3]
```

> **Huom!** LINQ-operaatioissa käytetään yleensä `Func<T, bool>` -muotoa, mutta `Predicate<T>` on yhä yleinen esim. `List`-metodien kanssa.

## Delegaatit ja LINQ

Delegaatit ovat LINQ:n ytimessä. Useimmat LINQ-metodit ottavat parametrina `Func`-delegaatin.

### Esimerkki: Where ja Select

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Where ottaa Func<int, bool>
Func<int, bool> isEven = n => n % 2 == 0;
var evenNumbers = numbers.Where(isEven).ToList();
// evenNumbers = [2, 4, 6]

// Select ottaa Func<int, TResult>
Func<int, string> toText = n => $"Number: {n}";
var textNumbers = numbers.Select(toText).ToList();
// textNumbers = ["Number: 1", "Number: 2", ...]
```

### Esimerkki: Delegaatti parametrina

```csharp
// Metodi, joka ottaa delegaatin parametrina
void ProcessNumbers(List<int> numbers, Func<int, bool> filter)
{
    var filtered = numbers.Where(filter);
    foreach (var num in filtered)
    {
        Console.WriteLine(num);
    }
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Käytä eri suodattimia
ProcessNumbers(numbers, n => n > 3);        // 4, 5, 6
ProcessNumbers(numbers, n => n % 2 == 0);   // 2, 4, 6
```

> **Lisäesimerkkejä LINQ:sta:** [LINQ.md](LINQ.md)

## Multicast-delegaatit

Delegaattiin voidaan liittää useita metodeja. Kun delegaattia kutsutaan, kaikki metodit suoritetaan järjestyksessä.

```csharp
delegate void Notify(string message);

void SendEmail(string message)
{
    Console.WriteLine($"Email sent: {message}");
}

void SendSMS(string message)
{
    Console.WriteLine($"SMS sent: {message}");
}

void LogMessage(string message)
{
    Console.WriteLine($"Logged: {message}");
}

// Yhdistä useita metodeja samaan delegaattiin
Notify notifier = SendEmail;
notifier += SendSMS;      // Lisää toinen metodi
notifier += LogMessage;   // Lisää kolmas metodi

// Kutsu delegaattia - kaikki metodit suoritetaan
notifier("Important notification!");
// Tulostaa:
// Email sent: Important notification!
// SMS sent: Important notification!
// Logged: Important notification!

// Poista metodi
notifier -= SendSMS;
notifier("Another notification!");
// Tulostaa vain:
// Email sent: Another notification!
// Logged: Another notification!
```

## Delegaatit ja Tapahtumat (Events)

Delegaatit ovat tapahtumien (events) perusta C#:ssa. Tapahtumat käyttävät delegaatteja määrittääkseen, mitä metodeja kutsutaan kun tapahtuma laukeaa.

### Esimerkki: Yksinkertainen tapahtuma

```csharp
public class Button
{
    // Delegaatti tapahtumalle
    public delegate void ClickHandler(string message);
    
    // Tapahtuma
    public event ClickHandler Click;
    
    // Metodi, joka laukaisee tapahtuman
    public void OnClick()
    {
        Click?.Invoke("Button was clicked!");
    }
}

// Käyttö
Button button = new Button();

// Liitä tapahtumankäsittelijät
button.Click += message => Console.WriteLine($"Handler 1: {message}");
button.Click += message => Console.WriteLine($"Handler 2: {message}");

// Laukaise tapahtuma
button.OnClick();
// Tulostaa:
// Handler 1: Button was clicked!
// Handler 2: Button was clicked!
```

> **Huom!** Modernissa C#:ssa käytetään usein `EventHandler` tai `EventHandler<T>` valmiita delegaatteja omien delegaattien sijaan.

## Anonyymit metodit ja Lambda-lausekkeet

Sen sijaan että määrittelisit erillisen metodin, voit käyttää anonyymeja metodeja tai lambda-lausekkeita.

### Anonyymi metodi (vanha tapa)

```csharp
delegate int MathOp(int a, int b);

MathOp add = delegate (int a, int b)
{
    return a + b;
};

Console.WriteLine(add(5, 3)); // 8
```

### Lambda-lauseke (moderni tapa)

```csharp
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(5, 3)); // 8

// Monirivinen lambda
Func<int, int, int> multiply = (a, b) =>
{
    Console.WriteLine($"Multiplying {a} and {b}");
    return a * b;
};
Console.WriteLine(multiply(4, 5)); // 20
```

> **Lisää Lambda-lausekkeista:** [LINQ.md](LINQ.md)

## Käytännön esimerkkejä

### Esimerkki 1: Callback-funktio

```csharp
void DownloadFile(string url, Action<string> onComplete)
{
    Console.WriteLine($"Downloading {url}...");
    // Simuloi lataus
    System.Threading.Thread.Sleep(1000);
    string result = "File content";
    
    // Kutsu callback-funktiota
    onComplete(result);
}

// Käyttö
DownloadFile("http://example.com/file.txt", content =>
{
    Console.WriteLine($"Download complete! Content: {content}");
});
```

### Esimerkki 2: Strategiasuunnittelumalli (Strategy Pattern)

```csharp
public class Calculator
{
    public int Calculate(int a, int b, Func<int, int, int> strategy)
    {
        return strategy(a, b);
    }
}

Calculator calc = new Calculator();

int sum = calc.Calculate(10, 5, (a, b) => a + b);           // 15
int difference = calc.Calculate(10, 5, (a, b) => a - b);    // 5
int product = calc.Calculate(10, 5, (a, b) => a * b);       // 50
```

### Esimerkki 3: Validointi

```csharp
public class Validator
{
    public bool Validate<T>(T value, Predicate<T> validationRule)
    {
        return validationRule(value);
    }
}

Validator validator = new Validator();

// Eri validointisäännöt
bool isValidAge = validator.Validate(25, age => age >= 18 && age <= 100);
bool isValidEmail = validator.Validate("test@example.com", 
    email => email.Contains("@") && email.Contains("."));

Console.WriteLine($"Valid age: {isValidAge}");     // True
Console.WriteLine($"Valid email: {isValidEmail}"); // True
```

## Milloin käyttää delegaatteja?

| Käyttötapaus | Kuvaus | Esimerkki |
|--------------|--------|-----------|
| **Callback-funktiot** | Kun haluat suorittaa koodia operaation päätyttyä | Tiedoston lataus, API-kutsut |
| **Event handling** | Käyttöliittymätapahtumat, notifikaatiot | Napinpainallukset, datan muutokset |
| **LINQ-operaatiot** | Suodatus, muunnos, aggregointi | `Where`, `Select`, `OrderBy` |
| **Strategiasuunnittelumalli** | Vaihda algoritmi ajonaikaisesti | Eri lajittelualgoritmit, maksutavat |
| **Dependency Injection** | Välitä toiminnallisuus riippuvuutena | Testaus, modulaarisuus |

## Yhteenveto

- **Delegaatti** on tyyppi, joka edustaa viittausta metodiin
- **Action** = ei palautusarvoa (void)
- **Func** = palauttaa arvon
- **Predicate** = palauttaa bool:n
- Delegaatit mahdollistavat **metodien välittämisen parametrina**
- Delegaatit ovat **tapahtumien (events) perusta**
- **Lambda-lausekkeet** ovat moderni tapa luoda delegaatteja

## Hyödyllisiä linkkejä

### Viralliset dokumentaatiot
- [Delegates (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)
- [Using Delegates (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/using-delegates)
- [Events (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/events/)

### Tutoriaalit
- [C# Delegates (w3schools)](https://www.w3schools.com/cs/cs_delegates.php)
- [Delegates Tutorial (TutorialsTeacher)](https://www.tutorialsteacher.com/csharp/csharp-delegates)
- [Action, Func, and Predicate (dotnettutorials.net)](https://dotnettutorials.net/lesson/action-func-predicate-delegates-csharp/)

### Videomuotoinen oppimateriaali
- [C# Delegates Explained (YouTube)](https://www.youtube.com/watch?v=jQgwEsJISy0)
- [Events and Delegates (YouTube)](https://www.youtube.com/watch?v=OuZrhykVytg)

### Liittyvät materiaalit
- [LINQ ja Lambda-lausekkeet](LINQ.md)
- [Exception Handling](Exception-Handling.md)

