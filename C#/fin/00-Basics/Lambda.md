# Lambda-lausekkeet ja Anonyymit funktiot

[Microsoftin virallinen Lambda-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)

## Mikä on Lambda-lauseke?

**Lambda-lauseke** on lyhyt ja tiivis tapa ilmaista anonyymi funktio (eli nimetön funktio). Lambda-lausekkeita käytetään yleisesti:
- LINQ-kyselyissä (`Where`, `Select`, `OrderBy`, jne.)
- Delegaattien luomisessa
- Event handler -metodeissa
- Callback-funktioissa
- Asynkronisessa ohjelmoinnissa

Lambda-lausekkeet tekevät koodista tiiviimpää ja luettavampaa, kun funktio on yksinkertainen ja sitä tarvitaan vain yhdessä paikassa.

## Lambda-lausekkeen syntaksi

### Perussyntaksi

```
(parametrit) => lauseke tai lohko
```

- **Parametrit**: Funktion syötteet (voi olla 0, 1 tai useampia)
- **=>**: "Lambda-operaattori" (luetaan "goes to" tai "becomes")
- **Lauseke tai lohko**: Funktion toteutus

### Esimerkkejä

```csharp
// Ei parametreja
() => Console.WriteLine("Hello!")

// Yksi parametri
x => x * 2

// Useampi parametri
(x, y) => x + y

// Monirivinen lohko
(x, y) => 
{
    int sum = x + y;
    Console.WriteLine($"Sum: {sum}");
    return sum;
}
```

## Expression Lambda vs. Statement Lambda

### Expression Lambda (Lauseke-lambda)

Yksinkertainen, yhden lausekkeen lambda. Palauttaa lausekkeen arvon automaattisesti.

```csharp
Func<int, int> square = x => x * x;
Console.WriteLine(square(5)); // 25

Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(3, 4)); // 7

// LINQ-esimerkki
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var doubled = numbers.Select(n => n * 2).ToList();
// doubled = [2, 4, 6, 8, 10]
```

### Statement Lambda (Lohko-lambda)

Monirivinen lambda, jossa on aaltosulkeet `{}`. Tarvitsee `return`-avainsanan, jos palauttaa arvon.

```csharp
Func<int, int, int> multiply = (a, b) =>
{
    Console.WriteLine($"Multiplying {a} and {b}");
    int result = a * b;
    return result;
};

Console.WriteLine(multiply(3, 4));
// Tulostaa:
// Multiplying 3 and 4
// 12
```

```csharp
// LINQ-esimerkki monirivisen lambdan kanssa
var numbers = new List<int> { 1, 2, 3, 4, 5 };
var filtered = numbers.Where(n =>
{
    bool isEven = n % 2 == 0;
    bool isLarge = n > 2;
    return isEven && isLarge;
}).ToList();
// filtered = [4]
```

## Parametrien käyttö

### Ei parametreja

```csharp
Func<string> getMessage = () => "Hello, World!";
Console.WriteLine(getMessage()); // Hello, World!

Action greet = () => Console.WriteLine("Hi there!");
greet(); // Hi there!
```

### Yksi parametri

Yhden parametrin tapauksessa sulkeet ovat valinnaisia:

```csharp
// Ilman sulkeita (suositeltu yksinkertaisissa tapauksissa)
Func<int, int> square = x => x * x;

// Sulkeiden kanssa (myös toimii)
Func<int, int> squareWithParens = (x) => x * x;

// Tyypin määrittely (harvoin tarvitaan)
Func<int, int> squareWithType = (int x) => x * x;
```

### Useampi parametri

Useamman parametrin tapauksessa sulkeet ovat pakollisia:

```csharp
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(10, 5)); // 15

Func<string, string, string> concat = (first, last) => $"{first} {last}";
Console.WriteLine(concat("John", "Doe")); // John Doe
```

### Tyypitetyt parametrit

Normaalisti C# päättelee tyypit, mutta voit määritellä ne eksplisiittisesti:

```csharp
Func<int, int, double> divide = (int a, int b) => (double)a / b;
Console.WriteLine(divide(10, 3)); // 3.333...
```

## Anonyymit funktiot vs. Nimetyt metodit

### Nimetty metodi

```csharp
bool IsEven(int number)
{
    return number % 2 == 0;
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(IsEven).ToList();
// evenNumbers = [2, 4, 6]
```

### Lambda-lauseke (anonyymi funktio)

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
// evenNumbers = [2, 4, 6]
```

### Milloin käyttää mitä?

| Käyttötilanne | Suositus |
|---------------|----------|
| Yksinkertainen, kertaluonteinen logiikka | Lambda-lauseke |
| Monimutkainen logiikka (>3 riviä) | Nimetty metodi |
| Logiikka käytetään useassa paikassa | Nimetty metodi |
| LINQ-kyselyt | Lambda-lauseke |
| Yksikkötestattava logiikka | Nimetty metodi |

## Käytännön esimerkkejä

### Esimerkki 1: LINQ-suodatus ja projektointi

```csharp
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
}

List<Person> people = new List<Person>
{
    new Person { Name = "Alice", Age = 25 },
    new Person { Name = "Bob", Age = 30 },
    new Person { Name = "Charlie", Age = 20 }
};

// Suodata aikuiset (yli 21v) ja hae heidän nimensä
var adultNames = people
    .Where(p => p.Age > 21)
    .Select(p => p.Name)
    .ToList();
// adultNames = ["Alice", "Bob"]

// Järjestä iän mukaan ja luo yhteenveto
var summary = people
    .OrderBy(p => p.Age)
    .Select(p => $"{p.Name} is {p.Age} years old")
    .ToList();
```

### Esimerkki 2: Event handling

```csharp
public class Button
{
    public event EventHandler Clicked;
    
    public void Click()
    {
        Clicked?.Invoke(this, EventArgs.Empty);
    }
}

Button button = new Button();

// Lambda-lauseke event handlerille
button.Clicked += (sender, e) => Console.WriteLine("Button clicked!");

// Monirivinen event handler
button.Clicked += (sender, e) =>
{
    Console.WriteLine("Processing click...");
    Console.WriteLine("Click handled!");
};

button.Click();
// Tulostaa:
// Button clicked!
// Processing click...
// Click handled!
```

### Esimerkki 3: Callback-funktiot

```csharp
void ProcessData(List<int> data, Action<int> callback)
{
    foreach (var item in data)
    {
        callback(item);
    }
}

List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// Yksinkertainen callback
ProcessData(numbers, n => Console.WriteLine(n));

// Monimutkaisempi callback
ProcessData(numbers, n =>
{
    int squared = n * n;
    Console.WriteLine($"{n}² = {squared}");
});
```

### Esimerkki 4: Järjestäminen custom-logiikalla

```csharp
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
}

List<Product> products = new List<Product>
{
    new Product { Name = "Laptop", Price = 999.99m },
    new Product { Name = "Mouse", Price = 25.50m },
    new Product { Name = "Keyboard", Price = 79.99m }
};

// Järjestä hinnan mukaan (halvin ensin)
var sortedByPrice = products.OrderBy(p => p.Price).ToList();

// Järjestä nimen pituuden mukaan
var sortedByNameLength = products.OrderBy(p => p.Name.Length).ToList();

// Monimutkainen järjestys: ensin hinnan mukaan, sitten nimen mukaan
var complexSort = products
    .OrderBy(p => p.Price)
    .ThenBy(p => p.Name)
    .ToList();
```

### Esimerkki 5: Aggregointi ja laskenta

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// Laske parillisten numeroiden summa
int evenSum = numbers.Where(n => n % 2 == 0).Sum();
// evenSum = 30

// Etsi suurin parillinen luku
int maxEven = numbers.Where(n => n % 2 == 0).Max();
// maxEven = 10

// Laske kuinka monta numeroa on yli 5
int count = numbers.Count(n => n > 5);
// count = 5

// Keskiarvo numeroista, jotka ovat välillä 3-7
double average = numbers.Where(n => n >= 3 && n <= 7).Average();
// average = 5.0
```

## Lambda ja Delegaatit

Lambda-lausekkeet toimivat delegaattien kanssa. Jokainen lambda-lauseke on yhteensopiva jonkin delegaattityypin kanssa.

```csharp
// Action: ei palautusarvoa
Action<string> print = message => Console.WriteLine(message);
print("Hello!"); // Hello!

// Func: palauttaa arvon
Func<int, int, int> add = (a, b) => a + b;
Console.WriteLine(add(5, 3)); // 8

// Predicate: palauttaa bool
Predicate<int> isPositive = number => number > 0;
Console.WriteLine(isPositive(5)); // True
```

> **Lisätietoja:** [Delegaatit](Delegates.md), [Predikaatit](Predicate.md)

## Vanhat Anonyymit metodit (C# 2.0)

Ennen lambda-lausekkeita (C# 3.0), C# käytti `delegate`-avainsanaa anonyymien funktioiden luomiseen. Tätä syntaksia näkyy vanhemmassa koodissa.

```csharp
// Vanha tapa (C# 2.0)
Func<int, int, int> oldAdd = delegate(int a, int b)
{
    return a + b;
};

// Moderni tapa (C# 3.0+)
Func<int, int, int> modernAdd = (a, b) => a + b;
```

**Suositus:** Käytä aina lambda-lausekkeita uudessa koodissa. Ne ovat lyhyempiä ja luettavampia.

## Discard-parametrit

Jos et tarvitse kaikkia parametreja, voit käyttää `_` (discard):

```csharp
// Event handler, joka ei käytä parametreja
button.Click += (_, _) => Console.WriteLine("Clicked!");

// LINQ-esimerkki: indeksi ei käytössä
var items = new[] { "a", "b", "c" };
var withIndex = items.Select((item, _) => item.ToUpper()).ToList();
```

## Async Lambda

Lambda-lausekkeet voivat olla asynkronisia:

```csharp
Func<Task<string>> fetchData = async () =>
{
    await Task.Delay(1000);
    return "Data loaded!";
};

string result = await fetchData();
Console.WriteLine(result); // Data loaded! (1 sekunnin viiveen jälkeen)
```

```csharp
// LINQ:n kanssa
List<int> ids = new List<int> { 1, 2, 3 };
var tasks = ids.Select(async id =>
{
    await Task.Delay(100);
    return $"Processed {id}";
});

var results = await Task.WhenAll(tasks);
// results = ["Processed 1", "Processed 2", "Processed 3"]
```

> **Huom!** Async lambda -funktioiden käyttö LINQ:ssä vaatii huolellisuutta. Muista käyttää `Task.WhenAll` tai vastaavia, kun haluat odottaa kaikkia asynkronisia operaatioita.

## Yhteisest sudokset Lambda-lausekkeissa

### Virhe 1: Unohtaa sulkeet monen parametrin tapauksessa

```csharp
// ❌ Virhe
Func<int, int, int> add = a, b => a + b; // Käännösvirhe!

// ✅ Oikein
Func<int, int, int> add = (a, b) => a + b;
```

### Virhe 2: Unohtaa return statement Lambda-lohkossa

```csharp
// ❌ Virhe
Func<int, int> square = x =>
{
    x * x; // Ei return!
};

// ✅ Oikein
Func<int, int> square = x =>
{
    return x * x;
};

// ✅ Tai vielä parempi (expression lambda)
Func<int, int> square = x => x * x;
```

### Virhe 3: Liian monimutkainen lambda

```csharp
// ❌ Vaikealukuinen
var result = data
    .Where(x => 
    {
        var isValid = x.Status == "Active" && x.Date > DateTime.Now.AddDays(-30);
        var hasItems = x.Items != null && x.Items.Count > 0;
        var isApproved = x.ApprovedBy != null;
        return isValid && hasItems && isApproved;
    })
    .ToList();

// ✅ Parempi: käytä nimettyä metodia
bool IsValidRecord(Record x)
{
    var isValid = x.Status == "Active" && x.Date > DateTime.Now.AddDays(-30);
    var hasItems = x.Items != null && x.Items.Count > 0;
    var isApproved = x.ApprovedBy != null;
    return isValid && hasItems && isApproved;
}

var result = data.Where(IsValidRecord).ToList();
```

## Parhaat käytännöt

1. **Pidä lambdat yksinkertaisina**: Jos lambda on yli 3 riviä, harkitse nimettyä metodia
2. **Käytä selkeitä parametrinimiä**: `x`, `y` ovat OK yksinkertaisissa tapauksissa, mutta selkeämmät nimet parantavat luettavuutta
3. **Vältä sivuvaikutuksia**: Lambdan ei pitäisi muuttaa ulkoisia muuttujia (katso [Closures](Closures.md))
4. **Expression lambda > Statement lambda**: Kun mahdollista, käytä expression lambda -muotoa
5. **Testattavuus**: Jos logiikka on monimutkainen, tee siitä nimetty metodi, jota voi testata

## Yhteenveto

- **Lambda-lauseke** on lyhyt tapa ilmaista anonyymi funktio
- Syntaksi: `(parametrit) => lauseke tai lohko`
- **Expression lambda**: yksinkertainen, yhden rivin lauseke
- **Statement lambda**: monirivinen, vaatii `{}`-sulkeet ja `return`:n
- Lambda-lausekkeet toimivat **delegaattien** kanssa (Action, Func, Predicate)
- Käytetään laajasti **LINQ**:ssa, **event handling**:ssa ja **callback**-funktioissa
- Pidä lambdat **yksinkertaisina** ja **selkeinä**

## Hyödyllisiä linkkejä

### Viralliset dokumentaatiot
- [Lambda Expressions (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)
- [Expression-bodied members (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/statements-expressions-operators/expression-bodied-members)
- [Anonymous Functions (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-operator)

### Tutoriaalit
- [C# Lambda Expressions (w3schools)](https://www.w3schools.com/cs/cs_lambda.php)
- [Lambda Tutorial (TutorialsTeacher)](https://www.tutorialsteacher.com/linq/linq-lambda-expression)
- [Lambda Expressions in C# (C# Corner)](https://www.c-sharpcorner.com/UploadFile/bd6c67/lambda-expressions-in-C-Sharp/)

### Videomuotoinen oppimateriaali
- [Lambda Expressions in C# (YouTube)](https://www.youtube.com/watch?v=j02HKEgIlV0)
- [C# Lambda Expressions Tutorial (YouTube)](https://www.youtube.com/watch?v=o8LWnwmHnXo)

### Liittyvät materiaalit
- [LINQ ja Lambda-lausekkeet](LINQ.md)
- [Delegaatit](Delegates.md)
- [Predikaatit](Predicate.md)
- [Closures](Closures.md)

