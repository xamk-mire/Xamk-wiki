# LINQ ja Lambda-lausekkeet

[Microsoftin virallinen LINQ-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)

## Mikä on LINQ?

**LINQ** (Language Integrated Query) on C#-ohjelmointikielessä käytetty tekniikka, joka mahdollistaa tietojen kyselyn suoraan ohjelmointikoodissa yhtenäisellä tavalla riippumatta tietolähteestä. LINQ mahdollistaa tietojen kyselyn niin tietokannoista (ORM kuten Entity Framework Core), XML-dokumenteista kuin kokoelmista (kuten listoista).

### Esimerkki LINQ-kyselystä

```csharp
using System.Linq;

var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Valitsee kaikki parittomat numerot
var oddNumbers = numbers.Where(n => n % 2 != 0).ToList();
// oddNumbers = {1, 3, 5}
```

## Mikä on Lambda?

**Lambda**-lausekkeet ovat lyhyt tapa esittää [anonyymi funktioita](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions) C#:ssa. Ne ovat usein käytettyjä LINQ-kyselyissä ja [delegate](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)-tietotyyppien kanssa.

### Lambda-lausekkeen syntaksi

```
(parametrit) => lauseke
```

### Esimerkki lambda-lausekkeesta

```csharp
// Lambda-lauseke, joka tarkistaa, onko luku pariton
Func<int, bool> isOdd = x => x % 2 != 0;

bool result = isOdd(5);  // true
bool result2 = isOdd(4);  // false
```

### Lambda LINQ-kyselyssä

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Käyttämällä lambda-lauseketta
var oddNumbers = numbers.Where(x => x % 2 != 0).ToList();
```

### Parametrien nimeäminen

Ota huomioon, että parametri voidaan nimetä miksi vaan. `x` ja `y` ovat yleisesti käytettyjä, mutta selkeämmät nimet tekevät koodista luettavampaa:

```csharp
// Yleinen mutta epäselvä
var result = numbers.Where(x => x % 2 == 0);

// Selkeämpi
var result = numbers.Where(number => number % 2 == 0);
```

## LINQ vs. Lambda: Mikä ero niillä on?

LINQ (Language Integrated Query) ja lambda-lausekkeet liittyvät toisiinsa, mutta ne eivät ole sama asia. Käytännössä LINQ tarjoaa korkeamman tason syntaksin tietorakenteiden käsittelyyn, kun taas lambda-lausekkeet ovat joustavia ja voivat olla osa LINQ-kyselyjä.

### 1. LINQ-kyselysyntaksi (Query Syntax)

LINQ on kokoelmapohjaisten operaatioiden kyselykieli, joka tarjoaa SQL-tyylisen syntaksin tietojen käsittelyyn C#:ssa.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// LINQ-kyselysyntaksi
var evenNumbers = from num in numbers
                  where num % 2 == 0
                  select num;

foreach (var num in evenNumbers)
{
    Console.WriteLine(num);
}
```

Tässä LINQ:n **query syntax** muistuttaa SQL-kyselyä. Se on usein selkeälukuinen mutta hieman pidempi kuin lambda-pohjainen syntaksi.

### 2. Lambda-metodisyntaksi (Method Syntax)

Lambda-lausekkeet ovat anonyymejä funktioita, joita käytetään yleensä lyhyisiin operaatioihin esimerkiksi LINQ:n metodiketjusyntaksissa.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Lambda-syntaksi LINQ-metodikutsujen kanssa
var evenNumbersLambda = numbers.Where(num => num % 2 == 0);

foreach (var num in evenNumbersLambda)
{
    Console.WriteLine(num);
}
```

Tämä tekee saman asian kuin edellinen LINQ-kysely, mutta nyt käytetään **method syntax** -tyyliä, joka on tyypillisesti lyhyempi ja suoraviivaisempi.

### 3. Keskeiset erot

| Ominaisuus | LINQ-kyselysyntaksi | Lambda-metodisyntaksi |
|------------|---------------------|----------------------|
| **Lukukelpoisuus** | Selkeä ja SQL-tyylinen | Tiiviimpi mutta voi olla vaikealukuisempi |
| **Joustavuus** | Vähemmän joustava (tietyt operaatiot vaikeampia) | Mahdollistaa monimutkaisempia funktioita |
| **Mahdollisuus käyttää funktioita** | Rajallinen | Täysi tuki lambda-funktioille |
| **Suorituskyky** | Sama suorituskyky kuin lambdoilla | Sama suorituskyky kuin LINQ:llä |

### 4. Käytännön vinkki

- **Jos haluat SQL-tyyppisen selkeän lukumuodon**, käytä **LINQ-kyselysyntaksia**.
- **Jos haluat tiiviimmän ja joustavamman tavan kirjoittaa kyselyitä**, käytä **lambda-lausekkeita ja metodisyntaksia**.

Useimmiten C#-kehittäjät suosivat lambda-pohjaista metodisyntaksia sen lyhyyden ja joustavuuden vuoksi.

## LINQ-peruskäsitteet

### 1. Suodatus (Where)

Suodatuksella voidaan poimia tietystä kokoelmasta vain tietyt ehdot täyttävät alkiot.

```csharp
List<int> numbers = new List<int> {1, 2, 3, 4, 5, 6};
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
// evenNumbers = {2, 4, 6}
```

### 2. Projektointi (Select)

`Select`-metodilla voidaan muuntaa tietueita uuteen muotoon.

```csharp
List<string> names = new List<string> {"Anna", "Ben", "Charlie"};
List<string> upperNames = names.Select(n => n.ToUpper()).ToList();
// upperNames = {"ANNA", "BEN", "CHARLIE"}
```

### 3. Ryhmittely (GroupBy)

Ryhmittelyn avulla voidaan jakaa kokoelman alkioita tietyn avaimen mukaan ryhmiin.

```csharp
List<(string Name, int Grade)> students = new List<(string Name, int Grade)>
{
    ("Alice", 10),
    ("Bob", 10),
    ("Charlie", 11)
};

var grouped = students.GroupBy(s => s.Grade);
foreach (var group in grouped)
{
    Console.WriteLine($"Grade {group.Key}:");
    foreach (var student in group)
    {
        Console.WriteLine($"  {student.Name}");
    }
}
```

### 4. Järjestäminen (OrderBy, OrderByDescending)

Kokoelman elementtejä voidaan järjestää nousevaan tai laskevaan järjestykseen.

```csharp
List<int> numbers = new List<int> {5, 2, 8, 1};
List<int> orderedNumbers = numbers.OrderBy(n => n).ToList();
// orderedNumbers = {1, 2, 5, 8}

// Laskeva järjestys
List<int> descendingNumbers = numbers.OrderByDescending(n => n).ToList();
// descendingNumbers = {8, 5, 2, 1}
```

### 5. Aggregointi (Sum, Average, Count)

Näillä metodeilla voidaan suorittaa laskutoimituksia kokoelman alkioille.

```csharp
List<decimal> sales = new List<decimal> {100.0m, 200.0m, 50.0m};
decimal totalSales = sales.Sum();        // 350.0m
decimal averageSales = sales.Average();  // 116.67m
int count = sales.Count();               // 3
```

### 6. Single vs SingleOrDefault

- `Single()`: Palauttaa ainoan alkion sekvenssissä. Heittää poikkeuksen, jos alkioita on useampia tai ei yhtään.
- `SingleOrDefault()`: Palauttaa ainoan alkion sekvenssissä tai `null` (oletusarvo), jos alkioita ei ole. Heittää poikkeuksen, jos alkioita on useampia.

```csharp
var numbers = new List<int> { 5 };

int single = numbers.Single();           // 5
int? singleOrDefault = numbers.SingleOrDefault(); // 5

var empty = new List<int>();
// int result = empty.Single();          // Heittää poikkeuksen
int? result2 = empty.SingleOrDefault(); // null
```

### 7. First vs FirstOrDefault

- `First()`: Palauttaa ensimmäisen alkion sekvenssissä. Heittää poikkeuksen, jos alkioita ei ole.
- `FirstOrDefault()`: Palauttaa ensimmäisen alkion tai `null` (oletusarvo), jos alkioita ei ole.

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5 };

int first = numbers.First();            // 1
int? firstOrDefault = numbers.FirstOrDefault(); // 1

var empty = new List<int>();
// int result = empty.First();          // Heittää poikkeuksen
int? result2 = empty.FirstOrDefault(); // null
```

## Anonyymit funktiot ja delegaatit

### Mikä on anonyymi funktio?

Anonyymi funktio on nimettömänä määritelty funktio, jota voidaan käyttää ilman erillistä metodia. Se on erityisen hyödyllinen tilanteissa, joissa funktiota tarvitaan vain kerran, esimerkiksi LINQ-operaatioiden yhteydessä. C# tukee anonyymejä funktioita lambda-ilmaisujen (`=>`) avulla.

### Esimerkki: Anonyymi funktio vs. erillinen metodi

```csharp
// Erillinen metodi
bool IsEven(int number)
{
    return number % 2 == 0;
}

List<int> numbers = new List<int> {1, 2, 3, 4, 5, 6};
List<int> evenNumbers = numbers.Where(IsEven).ToList();
// evenNumbers = {2, 4, 6}
```

```csharp
// Sama anonyymillä funktiolla (lambda-ilmaisulla)
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
```

### Mikä on delegaatti?

Delegaatit ovat erityisiä C#-tyyppejä, jotka edustavat viittausta yhteen tai useampaan metodiin. Voidaan ajatella, että delegaatti on muuttuja, johon voidaan tallentaa funktio. Tämä mahdollistaa metodien käsittelyn muuttujina ja niiden välittämisen parametrina muihin metodeihin.

### Esimerkki: Delegaatin käyttö

```csharp
delegate bool NumberPredicate(int number);

bool IsOdd(int number)
{
    return number % 2 != 0;
}

NumberPredicate predicate = IsOdd;
List<int> oddNumbers = numbers.Where(predicate).ToList();
// oddNumbers = {1, 3, 5}
```

### Delegaatin korvaaminen lambda-funktiolla

```csharp
List<int> oddNumbers = numbers.Where(n => n % 2 != 0).ToList();
```

### Esimerkki: Ravintolan tilausten käsittely

```csharp
// Delegaatin käyttö tilausten suodattamisessa
delegate bool OrderFilter(Order order);

bool ExpensiveOrders(Order order)
{
    return order.Price > 50;
}

List<Order> orders = GetOrders();
List<Order> expensiveOrders = orders.Where(ExpensiveOrders).ToList();
```

```csharp
// Sama toteutus anonyymillä funktiolla
List<Order> expensiveOrders = orders.Where(order => order.Price > 50).ToList();
```

## Predikaatti

### Mikä on predikaatti C#:ssa?

**Predikaatti** on funktio (tai lambda), joka ottaa jonkin arvon sisään ja palauttaa `true` tai `false`. Toisin sanoen: predikaatti on *ehto*, jolla testataan "täyttääkö tämä asia säännön".

### Milloin predikaattia käytetään?

Predikaatteja käytetään usein, kun:

- etsitään listasta alkioita (`Find`, `FindAll`)
- tarkistetaan löytyykö jotain (`Any`)
- lasketaan montako ehtoa täyttävää on (`Count`)
- suodatetaan dataa (`Where`)
- tarkistetaan täyttävätkö kaikki ehdon (`All`)

### Predicate<T> ja Func<T, bool>

C#:ssa predikaatti näkyy usein kahdessa muodossa:

- **`Predicate<T>`** — delegaatti, joka tarkoittaa "metodi joka ottaa T:n ja palauttaa bool". Esim. `Predicate<int>` on "ottaa int → palauttaa bool".
- **`Func<T, bool>`** — yleisempi versio, toimii myös predikaattina. Esim. `Func<string, bool>` on "ottaa string → palauttaa bool".

Käytännössä monet listametodit käyttävät `Predicate<T>`-tyyppiä, ja LINQ usein käyttää `Func<T, bool>`-muotoa. Molempien idea on sama: **sisään arvo → ulos true/false**.

### Esimerkki: Predikaatti lambdana

```csharp
// Predicate<int>: int -> bool
Predicate<int> isEven = n => n % 2 == 0;

bool a = isEven(4); // true
bool b = isEven(7); // false
```

### Esimerkki: List.Find ja List.FindAll

```csharp
var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Find: palauttaa ensimmäisen alkion, joka täyttää ehdon
int firstEven = numbers.Find(n => n % 2 == 0); // 2

// FindAll: palauttaa kaikki alkiot, jotka täyttää ehdon
List<int> allEven = numbers.FindAll(n => n % 2 == 0); // [2, 4, 6]
```

### Sama ajatus LINQ:lla (Where käyttää ehtoa)

```csharp
using System.Linq;

var numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

// Where suodattaa: pitää mukana vain ne, joille ehto palauttaa true
var evens = numbers.Where(n => n % 2 == 0).ToList(); // [2, 4, 6]
```

### Muistisääntö

Predikaatti on kuin "kyllä/ei-kysymys", jonka esität jokaiselle alkiolle:

- "Onko tämä luku parillinen?"
- "Onko tämän henkilön ikä vähintään 18?"
- "Sisältääkö tämä teksti sanan 'error'?"

### Harjoitus

```csharp
var names = new List<string> { "Ari", "Tuomas", "Liisa", "Annika" };

Predicate<string> longName = name => name.Length >= 5;

var result1 = names.FindAll(longName);                 // FindAll + Predicate<T>
var result2 = names.Where(n => n.Length >= 5).ToList(); // LINQ Where + lambda

// result1 ja result2: ["Tuomas", "Liisa", "Annika"]
```

## LINQ ja parametrit

LINQ-metodit ottavat parametrina yleensä `Func<T, bool>`- tai `Func<T, TResult>`-tyyppisiä delegateja, jotka määrittävät, mitä operaatiota suoritetaan jokaiselle kokoelman alkioille.

### Esimerkki: LINQ ja oma predicate-funktio

```csharp
bool IsEven(int number)
{
    return number % 2 == 0;
}

List<int> numbers = new List<int> {1, 2, 3, 4, 5, 6};
List<int> evenNumbers = numbers.Where(IsEven).ToList();
// evenNumbers = {2, 4, 6}
```

### Esimerkki: LINQ ja anonyymi funktio

Sama voidaan tehdä anonyymilla funktiolla ilman erillistä metodia:

```csharp
List<int> evenNumbers = numbers.Where(n => n % 2 == 0).ToList();
```

## Kyselyoperaattorit

Kyselyoperaattorit (Query operators) ovat metodeja, joita voidaan käyttää C#-kielessä kyselyjen tekemiseen kokoelmista.

Näitä kyselyoperaattoreita on monia erilaisia ja löydät [täältä](https://www.tutorialsteacher.com/linq/linq-standard-query-operators) listan eri operaattoreista ja esimerkin, kuinka niitä käytetään.

Esimerkkikoodia löytyy myös [CollectionExamples](https://github.com/xamk-ture/AdvancedExamples/blob/master/CollectionExamples/Program.cs)-projektista.

## Yhteenveto

- **LINQ** tarjoaa yhtenäisen tavan kysyä tietoja eri lähteistä
- **Lambda-lausekkeet** ovat lyhyt tapa määritellä anonyymejä funktioita
- **Delegaatit** mahdollistavat metodien käsittelyn muuttujina
- **Predikaatit** ovat funktioita, jotka palauttavat `true` tai `false`
- **LINQ ja lambda** tekevät C#-koodista tiiviimpää ja luettavampaa, erityisesti kun käsitellään kokoelmia tai tietolähteitä

## Hyödyllisiä linkkejä

- [Microsoftin LINQ-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/linq/)
- [Lambda-lausekkeet](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)
- [Delegaatit](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/delegates/)
- [LINQ Standard Query Operators](https://www.tutorialsteacher.com/linq/linq-standard-query-operators)
- [Esimerkkikoodit](https://github.com/xamk-ture/OOP_Examples/blob/master/LinqExamples/Program.cs)

