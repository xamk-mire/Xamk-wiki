# Closures (Sulkeumat)

[Microsoftin dokumentaatio Closures-aiheesta](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions#capture-of-outer-variables-and-variable-scope-in-lambda-expressions)

## Mikä on Closure?

**Closure** (sulkeuma) on ohjelmointikonsepti, jossa funktio (esim. [lambda-lauseke](Lambda.md)) "kaappaa" tai "muistaa" muuttujat sen ympäristöstä, jossa se määriteltiin. Toisin sanoen, lambda voi käyttää muuttujia, jotka eivät ole sen parametreja, vaan ulkoisesta scopesta.

Closure mahdollistaa sen, että funktio säilyttää viittauksen ulkoisiin muuttujiin senkin jälkeen, kun varsinainen koodi on jo suoritettu.

## Yksinkertainen esimerkki

```csharp
void Example()
{
    int multiplier = 3; // Ulkoinen muuttuja
    
    Func<int, int> multiplyByThree = x => x * multiplier;
    // Lambda "kaappaa" multiplier-muuttujan
    
    Console.WriteLine(multiplyByThree(5)); // 15
    Console.WriteLine(multiplyByThree(10)); // 30
}
```

Tässä esimerkissä:
- `multiplier` on ulkoinen muuttuja
- Lambda-lauseke `x => x * multiplier` käyttää tätä ulkoista muuttujaa
- Lambda "kaappaa" `multiplier`:n → **Closure**

## Miten Closure toimii?

Kun lambda-lauseke viittaa ulkoiseen muuttujaan, C# **ei kopioi** sen arvoa, vaan **säilyttää viittauksen** siihen muuttujaan. Tämä tarkoittaa, että:
1. Lambda näkee muuttujaan tehdyt muutokset
2. Lambda voi myös muuttaa muuttujaa

### Esimerkki: Muuttujan muuttaminen

```csharp
void Example()
{
    int counter = 0; // Ulkoinen muuttuja
    
    Action increment = () => counter++; // Lambda kaappaa counter:n
    
    Console.WriteLine($"Counter: {counter}"); // 0
    increment();
    Console.WriteLine($"Counter: {counter}"); // 1
    increment();
    Console.WriteLine($"Counter: {counter}"); // 2
}
```

Lambda ei vain lue `counter`:a, vaan myös muuttaa sitä!

## Closures ja muuttuvat arvot

Koska closure viittaa itse muuttujaan (ei sen arvoon), muutokset muuttujaan heijastuvat lambdassa:

```csharp
void Example()
{
    int multiplier = 2;
    
    Func<int, int> multiply = x => x * multiplier;
    
    Console.WriteLine(multiply(5)); // 10 (5 * 2)
    
    multiplier = 3; // Muutetaan multiplier:a
    
    Console.WriteLine(multiply(5)); // 15 (5 * 3)
    // Lambda näkee uuden arvon!
}
```

## Yleinen sudoku: Loop-muuttuja

Yksi klassisin closure-virhe C#:ssa liittyy loop-muuttujiin:

### ❌ Väärä tapa (ennen C# 5.0)

```csharp
void Example()
{
    var actions = new List<Action>();
    
    for (int i = 0; i < 5; i++)
    {
        actions.Add(() => Console.WriteLine(i));
        // Lambda kaappaa i-muuttujan, ei sen ARVON!
    }
    
    foreach (var action in actions)
    {
        action(); // Tulostaa: 5, 5, 5, 5, 5 (ei 0, 1, 2, 3, 4!)
    }
}
```

**Miksi?** Kaikki lambdat viittaavat **samaan** `i`-muuttujaan. Kun loop päättyy, `i`:n arvo on 5, ja siksi kaikki lambdat tulostavat 5.

### ✅ Oikea tapa: Kopioi arvo paikalliseen muuttujaan

```csharp
void Example()
{
    var actions = new List<Action>();
    
    for (int i = 0; i < 5; i++)
    {
        int localI = i; // Kopioi i:n arvo paikalliseen muuttujaan
        actions.Add(() => Console.WriteLine(localI));
        // Lambda kaappaa localI:n, joka on uniikki jokaisella iteraatiolla
    }
    
    foreach (var action in actions)
    {
        action(); // Tulostaa: 0, 1, 2, 3, 4
    }
}
```

### ✅ C# 5.0+: foreach on turvallinen

C# 5.0:sta lähtien `foreach`-loopin muuttuja käyttäytyy kuin paikallinen muuttuja:

```csharp
void Example()
{
    var numbers = new[] { 1, 2, 3, 4, 5 };
    var actions = new List<Action>();
    
    foreach (var num in numbers)
    {
        actions.Add(() => Console.WriteLine(num));
        // foreach luo uuden muuttujan jokaiselle iteraatiolle
    }
    
    foreach (var action in actions)
    {
        action(); // Tulostaa: 1, 2, 3, 4, 5
    }
}
```

## Closures käytännössä

### Esimerkki 1: Counter Factory

```csharp
Func<int> CreateCounter()
{
    int count = 0; // Tämä muuttuja "elää" lambdan sisällä
    
    return () =>
    {
        count++;
        return count;
    };
}

var counter1 = CreateCounter();
var counter2 = CreateCounter();

Console.WriteLine(counter1()); // 1
Console.WriteLine(counter1()); // 2
Console.WriteLine(counter1()); // 3

Console.WriteLine(counter2()); // 1 (eri instanssi!)
Console.WriteLine(counter2()); // 2
```

Jokainen `CreateCounter()`-kutsu luo **oman** `count`-muuttujansa, joka "kaapautuu" lambdaan.

### Esimerkki 2: Multiplier Factory

```csharp
Func<int, int> CreateMultiplier(int factor)
{
    return x => x * factor; // factor kaapautuu
}

var double = CreateMultiplier(2);
var triple = CreateMultiplier(3);

Console.WriteLine(double(5));  // 10
Console.WriteLine(triple(5));  // 15
```

### Esimerkki 3: Event Handler -kaappaus

```csharp
void SetupButtons()
{
    var buttons = new List<Button>();
    
    for (int i = 0; i < 5; i++)
    {
        int buttonId = i; // Tärkeä: kopioi paikalliseen muuttujaan
        var button = new Button();
        
        button.Click += (sender, e) =>
        {
            Console.WriteLine($"Button {buttonId} clicked!");
        };
        
        buttons.Add(button);
    }
}
```

### Esimerkki 4: LINQ ja Closures

```csharp
void FilterByMinimum(List<int> numbers, int minimum)
{
    // Lambda kaappaa minimum-parametrin
    var filtered = numbers.Where(n => n >= minimum).ToList();
    
    Console.WriteLine(string.Join(", ", filtered));
}

var numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

FilterByMinimum(numbers, 5); // 5, 6, 7, 8, 9, 10
FilterByMinimum(numbers, 8); // 8, 9, 10
```

### Esimerkki 5: Closure ja tilanhallinta

```csharp
class Validator
{
    public Func<string, bool> CreateLengthValidator(int minLength, int maxLength)
    {
        // minLength ja maxLength kaapautuvat
        return text =>
        {
            return text.Length >= minLength && text.Length <= maxLength;
        };
    }
}

var validator = new Validator();
var passwordValidator = validator.CreateLengthValidator(8, 20);
var usernameValidator = validator.CreateLengthValidator(3, 15);

Console.WriteLine(passwordValidator("abc123")); // False (liian lyhyt)
Console.WriteLine(passwordValidator("StrongPassword123")); // True
Console.WriteLine(usernameValidator("Bob")); // True
```

## Closures ja muisti

Closure pitää kaapattuja muuttujia muistissa niin kauan kuin lambda itse on muistissa. Tämä voi aiheuttaa **muistivuotoja**, jos et ole varovainen.

### Huomioon otettavaa:

```csharp
class DataProcessor
{
    private List<Action> handlers = new List<Action>();
    
    public void AddHandler(string data)
    {
        // ⚠️ Varoitus: data-muuttuja pysyy muistissa niin kauan kuin handler on listassa
        handlers.Add(() => Console.WriteLine(data));
    }
    
    public void Clear()
    {
        handlers.Clear(); // Vapauta lambdat ja niiden kaappamat muuttujat
    }
}
```

Jos `AddHandler` kutsutaan tuhansia kertoja suurilla `data`-arvoilla, ne kaikki pysyvät muistissa!

### Ratkaisu: Vapauta resurssit

```csharp
class DataProcessor
{
    private List<Action> handlers = new List<Action>();
    
    public void AddHandler(string data)
    {
        handlers.Add(() => Console.WriteLine(data));
    }
    
    public void ProcessAndClear()
    {
        foreach (var handler in handlers)
        {
            handler();
        }
        handlers.Clear(); // Vapauta lambdat
    }
}
```

## Closures ja monisäikeistys

Closures voivat aiheuttaa **race condition** -ongelmia monisäikeisissä ohjelmissa, koska useampi säie voi käyttää samaa kaapattua muuttujaa samanaikaisesti.

### ❌ Ongelma: Race condition

```csharp
void Example()
{
    int counter = 0; // Jaettu muuttuja
    
    var tasks = new List<Task>();
    
    for (int i = 0; i < 10; i++)
    {
        tasks.Add(Task.Run(() =>
        {
            for (int j = 0; j < 1000; j++)
            {
                counter++; // ⚠️ EI turvallista monisäikeisessä ympäristössä
            }
        }));
    }
    
    Task.WaitAll(tasks.ToArray());
    Console.WriteLine(counter); // Voi olla alle 10000!
}
```

### ✅ Ratkaisu: Lock tai Interlocked

```csharp
void Example()
{
    int counter = 0;
    object lockObj = new object();
    
    var tasks = new List<Task>();
    
    for (int i = 0; i < 10; i++)
    {
        tasks.Add(Task.Run(() =>
        {
            for (int j = 0; j < 1000; j++)
            {
                lock (lockObj) // Suojaa kriittinen osio
                {
                    counter++;
                }
            }
        }));
    }
    
    Task.WaitAll(tasks.ToArray());
    Console.WriteLine(counter); // 10000
}
```

## Closures ja puhdas funktionaalinen ohjelmointi

Puhtaassa funktionaalisessa ohjelmoinnissa lambdat **eivät saa muuttaa** ulkoisia muuttujia (ei sivuvaikutuksia). Tämä tekee koodista helpommin testattavaa ja ennustettavaa.

### ❌ Ei-puhdas (mutoi tilaa)

```csharp
int total = 0;
var numbers = new List<int> { 1, 2, 3, 4, 5 };

numbers.ForEach(n => total += n); // Sivuvaikutus: muuttaa total:a
Console.WriteLine(total); // 15
```

### ✅ Puhdas (ei sivuvaikutuksia)

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

int total = numbers.Sum(); // Ei sivuvaikutuksia
Console.WriteLine(total); // 15
```

## Parhaat käytännöt

1. **Ymmärrä, että closure viittaa muuttujaan, ei arvoon**
   - Lambda näkee muuttujaan tehdyt muutokset

2. **Varo loop-muuttujia**
   - Kopioi loop-muuttuja paikalliseen muuttujaan ennen lambdan luomista (`for`-loop)
   - `foreach` on turvallinen C# 5.0+

3. **Vältä sivuvaikutuksia**
   - Älä muuta ulkoisia muuttujia lambdan sisällä, jos mahdollista
   - Pidä lambdat "puhtaina" funktioina

4. **Huomioi muistinkäyttö**
   - Closures pitävät kaapattuja muuttujia muistissa
   - Vapauta lambdat, kun niitä ei enää tarvita

5. **Monisäikeisyys**
   - Suojaa jaetut muuttujat `lock`:lla tai käytä `Interlocked`
   - Harkitse `ThreadLocal<T>`-muuttujia

6. **Testattavuus**
   - Monimutkaiset closures voivat tehdä koodista vaikeasti testattavaa
   - Harkitse nimettyä metodia, jos logiikka on monimutkainen

## Yhteenveto

- **Closure** = lambda "kaappaa" ulkoisia muuttujia
- Lambda viittaa **muuttujaan**, ei sen arvoon
- **Loop-muuttuja**: varo `for`-looppia, käytä paikallista kopiota
- **Muisti**: Closures pitävät kaapattuja muuttujia muistissa
- **Monisäikeisyys**: Suojaa jaetut muuttujat
- **Sivuvaikutukset**: Vältä muuttamasta ulkoisia muuttujia

## Hyödyllisiä linkkejä

### Viralliset dokumentaatiot
- [Lambda Expressions - Capture of Outer Variables (Microsoft)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions#capture-of-outer-variables-and-variable-scope-in-lambda-expressions)
- [Closures (Eric Lippert's Blog)](https://learn.microsoft.com/en-us/archive/blogs/ericlippert/closures-are-not-complicated)
- [Captured Variables (C# Programming Guide)](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)

### Tutoriaalit
- [Understanding Closures in C#](https://www.c-sharpcorner.com/article/closures-in-c-sharp/)
- [C# Closures Explained](https://www.tutorialsteacher.com/csharp/csharp-closures)

### Videomuotoinen oppimateriaali
- [C# Closures Explained (YouTube)](https://www.youtube.com/results?search_query=c%23+closures+explained)

### Liittyvät materiaalit
- [Lambda-lausekkeet](Lambda.md)
- [Delegaatit](Delegates.md)
- [LINQ](LINQ.md)
- [Scopes](Scopes.md)

