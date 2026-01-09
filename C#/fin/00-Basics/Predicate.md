# Predikaatit (Predicates)

[Microsoftin Predicate-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/api/system.predicate-1)

## Mikä on predikaatti?

**Predikaatti** on funktio (tai [lambda-lauseke](Lambda.md)), joka ottaa jonkin arvon sisään ja palauttaa `true` tai `false`. Toisin sanoen: predikaatti on **ehto**, jolla testataan "täyttääkö tämä asia säännön".

Predikaatit ovat keskeinen käsite ohjelmoinnissa, ja niitä käytetään laajasti:
- Kokoelmien suodattamisessa
- Tiedon validoinnissa
- Ehtojen testaamisessa
- LINQ-kyselyissä

## Predikaatin perusidea

```csharp
// Predikaatti: "Onko tämä luku parillinen?"
bool IsEven(int number)
{
    return number % 2 == 0;
}

Console.WriteLine(IsEven(4)); // True
Console.WriteLine(IsEven(7)); // False
```

Tämä on yksinkertainen predikaatti, joka testaa yhden ehdon. Predikaatti voi olla yksinkertainen tai monimutkainen, mutta sen lopputulos on aina `bool`.

## Predicate<T> -delegaatti

C# tarjoaa valmiin `Predicate<T>`-delegaattityypin, joka määrittelee metodin, joka:
- Ottaa yhden parametrin tyyppiä `T`
- Palauttaa `bool`-arvon

```csharp
// Predicate<int>: ottaa int:n, palauttaa bool:n
Predicate<int> isEven = number => number % 2 == 0;

Console.WriteLine(isEven(4)); // True
Console.WriteLine(isEven(7)); // False
```

```csharp
// Predicate<string>: ottaa string:in, palauttaa bool:n
Predicate<string> isLongName = name => name.Length >= 5;

Console.WriteLine(isLongName("Alice"));     // True
Console.WriteLine(isLongName("Bob"));       // False
```

## Predicate<T> vs Func<T, bool>

Sekä `Predicate<T>` että `Func<T, bool>` edustavat funktiota, joka ottaa yhden parametrin ja palauttaa `bool`:n. Käytännössä ne ovat hyvin samankaltaisia, mutta niillä on pieniä eroja:

| Ominaisuus | Predicate&lt;T&gt; | Func&lt;T, bool&gt; |
|------------|-------------|-----------------|
| **Parametrien määrä** | Tasan 1 | 1-16 |
| **Palautustyyppi** | Aina bool | Viimeinen tyyppi |
| **Käyttötarkoitus** | Semanttinen: ehdon testaus | Yleiskäyttöinen funktio |
| **Käytetään** | `List.Find`, `List.FindAll`, jne. | LINQ-metodit |

### Esimerkki: Predicate<T>

```csharp
Predicate<int> isPositive = n => n > 0;

List<int> numbers = new List<int> { -2, -1, 0, 1, 2, 3 };
List<int> positiveNumbers = numbers.FindAll(isPositive);
// positiveNumbers = [1, 2, 3]
```

### Esimerkki: Func<T, bool>

```csharp
Func<int, bool> isPositive = n => n > 0;

var numbers = new List<int> { -2, -1, 0, 1, 2, 3 };
var positiveNumbers = numbers.Where(isPositive).ToList();
// positiveNumbers = [1, 2, 3]
```

> **Käytännön vinkki:** Modernissa C#-koodissa `Func<T, bool>` on yleisempi LINQ-operaatioiden kanssa, kun taas `Predicate<T>` näkyy erityisesti `List`-luokan metodeissa.

## Predikaatit List-metodien kanssa

`List<T>`-luokka tarjoaa useita metodeja, jotka ottavat `Predicate<T>`-parametrin:

### Find - Ensimmäinen ehdon täyttävä

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Etsi ensimmäinen parillinen luku
int firstEven = numbers.Find(n => n % 2 == 0);
Console.WriteLine(firstEven); // 2

// Etsi ensimmäinen luku > 4
int firstLarge = numbers.Find(n => n > 4);
Console.WriteLine(firstLarge); // 5
```

### FindAll - Kaikki ehdon täyttävät

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Etsi kaikki parilliset luvut
List<int> evenNumbers = numbers.FindAll(n => n % 2 == 0);
// evenNumbers = [2, 4, 6]

// Etsi kaikki luvut välillä 2-5
List<int> inRange = numbers.FindAll(n => n >= 2 && n <= 5);
// inRange = [2, 3, 4, 5]
```

### FindLast - Viimeinen ehdon täyttävä

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Etsi viimeinen parillinen luku
int lastEven = numbers.FindLast(n => n % 2 == 0);
Console.WriteLine(lastEven); // 6
```

### FindIndex - Ensimmäisen ehdon täyttävän indeksi

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Etsi ensimmäisen parillisen luvun indeksi
int index = numbers.FindIndex(n => n % 2 == 0);
Console.WriteLine(index); // 1 (luku 2 on indeksissä 1)
```

### Exists - Tarkista, löytyykö ehdon täyttävä

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Onko listassa parillisia lukuja?
bool hasEven = numbers.Exists(n => n % 2 == 0);
Console.WriteLine(hasEven); // True

// Onko listassa negatiivisia lukuja?
bool hasNegative = numbers.Exists(n => n < 0);
Console.WriteLine(hasNegative); // False
```

### TrueForAll - Tarkista, täyttävätkö kaikki ehdon

```csharp
List<int> numbers = new List<int> { 2, 4, 6, 8 };

// Ovatko kaikki luvut parillisia?
bool allEven = numbers.TrueForAll(n => n % 2 == 0);
Console.WriteLine(allEven); // True

// Ovatko kaikki luvut positiivisia?
List<int> mixed = new List<int> { -1, 2, 3 };
bool allPositive = mixed.TrueForAll(n => n > 0);
Console.WriteLine(allPositive); // False
```

### RemoveAll - Poista kaikki ehdon täyttävät

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Poista kaikki parilliset luvut
int removedCount = numbers.RemoveAll(n => n % 2 == 0);
Console.WriteLine(removedCount); // 3 (poistettiin 2, 4, 6)
Console.WriteLine(string.Join(", ", numbers)); // 1, 3, 5
```

## Predikaatit LINQ:n kanssa

LINQ-metodit käyttävät `Func<T, bool>` -muotoa, mutta konsepti on täsmälleen sama kuin predikaateissa.

### Where - Suodatus

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Suodata parilliset luvut
var evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
// evenNumbers = [2, 4, 6]
```

### Any - Onko jotain

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Onko listassa parillisia?
bool hasEven = numbers.Any(n => n % 2 == 0); // True

// Onko listassa lukuja > 10?
bool hasLarge = numbers.Any(n => n > 10); // False
```

### All - Täyttävätkö kaikki

```csharp
var numbers = new List<int> { 2, 4, 6, 8 };

// Ovatko kaikki parilliset?
bool allEven = numbers.All(n => n % 2 == 0); // True
```

### Count - Laske ehdon täyttävät

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Kuinka monta parillista?
int evenCount = numbers.Count(n => n % 2 == 0); // 3
```

> **Lisää LINQ-esimerkkejä:** [LINQ.md](LINQ.md)

## Käytännön esimerkkejä

### Esimerkki 1: Henkilöiden suodatus

```csharp
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string City { get; set; }
}

List<Person> people = new List<Person>
{
    new Person { Name = "Alice", Age = 25, City = "Helsinki" },
    new Person { Name = "Bob", Age = 30, City = "Tampere" },
    new Person { Name = "Charlie", Age = 20, City = "Helsinki" },
    new Person { Name = "David", Age = 35, City = "Turku" }
};

// Predikaatti: aikuinen (yli 21v)
Predicate<Person> isAdult = p => p.Age >= 21;
List<Person> adults = people.FindAll(isAdult);
// adults = [Alice, Bob, David]

// Predikaatti: asuu Helsingissä
Predicate<Person> livesInHelsinki = p => p.City == "Helsinki";
List<Person> helsinkiPeople = people.FindAll(livesInHelsinki);
// helsinkiPeople = [Alice, Charlie]

// Yhdistetty predikaatti: aikuinen JA asuu Helsingissä
Predicate<Person> adultInHelsinki = p => p.Age >= 21 && p.City == "Helsinki";
List<Person> result = people.FindAll(adultInHelsinki);
// result = [Alice]
```

### Esimerkki 2: Tuotteiden validointi

```csharp
public class Product
{
    public string Name { get; set; }
    public decimal Price { get; set; }
    public int Stock { get; set; }
}

// Predikaatit validointiin
Predicate<Product> isValidPrice = p => p.Price > 0;
Predicate<Product> isInStock = p => p.Stock > 0;
Predicate<Product> isExpensive = p => p.Price > 100;

Product laptop = new Product { Name = "Laptop", Price = 999, Stock = 5 };
Product brokenItem = new Product { Name = "Broken", Price = -10, Stock = 0 };

Console.WriteLine(isValidPrice(laptop));    // True
Console.WriteLine(isInStock(laptop));       // True
Console.WriteLine(isExpensive(laptop));     // True

Console.WriteLine(isValidPrice(brokenItem)); // False
Console.WriteLine(isInStock(brokenItem));    // False
```

### Esimerkki 3: Merkkijonojen käsittely

```csharp
List<string> words = new List<string> 
{ 
    "apple", "banana", "cherry", "date", "elderberry" 
};

// Predikaatti: pitkät sanat (yli 5 kirjainta)
Predicate<string> isLongWord = word => word.Length > 5;
List<string> longWords = words.FindAll(isLongWord);
// longWords = ["banana", "cherry", "elderberry"]

// Predikaatti: alkaa a-kirjaimella
Predicate<string> startsWithA = word => word.StartsWith("a");
List<string> aWords = words.FindAll(startsWithA);
// aWords = ["apple"]

// Predikaatti: sisältää "er"
Predicate<string> containsEr = word => word.Contains("er");
List<string> erWords = words.FindAll(containsEr);
// erWords = ["cherry", "elderberry"]
```

### Esimerkki 4: Numeerinen validointi

```csharp
// Predikaatit numeroiden validointiin
Predicate<int> isEven = n => n % 2 == 0;
Predicate<int> isPositive = n => n > 0;
Predicate<int> isInRange = n => n >= 1 && n <= 100;
Predicate<int> isPrime = n =>
{
    if (n < 2) return false;
    for (int i = 2; i <= Math.Sqrt(n); i++)
    {
        if (n % i == 0) return false;
    }
    return true;
};

int number = 7;
Console.WriteLine($"Even: {isEven(number)}");       // False
Console.WriteLine($"Positive: {isPositive(number)}"); // True
Console.WriteLine($"In range: {isInRange(number)}"); // True
Console.WriteLine($"Prime: {isPrime(number)}");     // True
```

### Esimerkki 5: Monimutkainen suodatus

```csharp
public class Student
{
    public string Name { get; set; }
    public double Grade { get; set; }
    public int Absences { get; set; }
}

List<Student> students = new List<Student>
{
    new Student { Name = "Alice", Grade = 4.5, Absences = 2 },
    new Student { Name = "Bob", Grade = 3.2, Absences = 8 },
    new Student { Name = "Charlie", Grade = 4.8, Absences = 1 },
    new Student { Name = "David", Grade = 2.5, Absences = 12 }
};

// Monimutkainen predikaatti: hyvä opiskelija
Predicate<Student> isGoodStudent = s =>
{
    bool hasGoodGrade = s.Grade >= 4.0;
    bool hasLowAbsences = s.Absences < 5;
    return hasGoodGrade && hasLowAbsences;
};

List<Student> goodStudents = students.FindAll(isGoodStudent);
// goodStudents = [Alice, Charlie]
```

## Predikaattien yhdistäminen

Voit yhdistää useita predikaatteja loogisilla operaattoreilla (`&&`, `||`, `!`):

```csharp
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// Yksittäiset predikaatit
Predicate<int> isEven = n => n % 2 == 0;
Predicate<int> isLarge = n => n > 5;

// Yhdistetyt predikaatit
Predicate<int> isEvenAndLarge = n => isEven(n) && isLarge(n);
Predicate<int> isOddOrSmall = n => !isEven(n) || !isLarge(n);

var evenAndLarge = numbers.FindAll(isEvenAndLarge);
// evenAndLarge = [6, 8, 10]

var oddOrSmall = numbers.FindAll(isOddOrSmall);
// oddOrSmall = [1, 2, 3, 4, 5, 7, 9]
```

Tai suoraan inline:

```csharp
// AND-operaatio
var result1 = numbers.FindAll(n => n % 2 == 0 && n > 5);
// result1 = [6, 8, 10]

// OR-operaatio
var result2 = numbers.FindAll(n => n < 3 || n > 8);
// result2 = [1, 2, 9, 10]

// NOT-operaatio
var result3 = numbers.FindAll(n => !(n % 2 == 0));
// result3 = [1, 3, 5, 7, 9]
```

## Muistisääntö

Predikaatti on kuin **"kyllä/ei-kysymys"**, jonka esität jokaiselle alkiolle:

- "Onko tämä luku parillinen?" → `n => n % 2 == 0`
- "Onko tämän henkilön ikä vähintään 18?" → `p => p.Age >= 18`
- "Sisältääkö tämä teksti sanan 'error'?" → `s => s.Contains("error")`
- "Onko tämä tuote saatavilla?" → `p => p.Stock > 0`

Jokainen predikaatti palauttaa **true** tai **false**, ei mitään muuta.

## Parhaat käytännöt

1. **Nimeä predikaatit selkeästi**: `isValid`, `hasItems`, `isAdult` on parempia kuin `check`, `test`
2. **Pidä predikaatit yksinkertaisina**: Jos predikaatti on monimutkainen, jaa se pienempiin osiin
3. **Käytä nimettyä predikaattia, jos käytät samaa ehtoa useassa paikassa**
4. **Inline-predikaatti on OK yksinkertaisissa tapauksissa**: `numbers.Where(n => n > 0)`
5. **Testaa predikaatit**: Predikaatit ovat yksikötestattavia funktioita

## Yhteenveto

- **Predikaatti** on funktio, joka ottaa arvon ja palauttaa `true` tai `false`
- `Predicate<T>` = delegaatti, joka ottaa `T`:n ja palauttaa `bool`:n
- `Func<T, bool>` = yleisempi versio, käytetään LINQ:ssä
- Predikaatteja käytetään **List-metodeissa** (`Find`, `FindAll`, `Exists`, jne.)
- Predikaatteja käytetään **LINQ:ssä** (`Where`, `Any`, `All`, `Count`)
- Predikaatit ovat **yhdistettävissä** loogisilla operaattoreilla (`&&`, `||`, `!`)

## Hyödyllisiä linkkejä

### Viralliset dokumentaatiot
- [Predicate Delegate (Microsoft)](https://learn.microsoft.com/en-us/dotnet/api/system.predicate-1)
- [List.Find Method (Microsoft)](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.find)
- [List.FindAll Method (Microsoft)](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.list-1.findall)

### Tutoriaalit
- [Predicate in C# (TutorialsTeacher)](https://www.tutorialsteacher.com/csharp/csharp-predicate)
- [Predicate Delegate (dotnettutorials.net)](https://dotnettutorials.net/lesson/predicate-delegate-csharp/)
- [C# Predicate (C# Corner)](https://www.c-sharpcorner.com/article/predicate-delegate-in-c-sharp/)

### Liittyvät materiaalit
- [Lambda-lausekkeet](Lambda.md)
- [Delegaatit](Delegates.md)
- [LINQ ja Lambda](LINQ.md)
- [Functions and Methods](Functions-and-Methods.md)

