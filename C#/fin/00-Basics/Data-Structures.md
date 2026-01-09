# Tietorakenteet (Data Structures)

Tietorakenteet ovat tapoja organisoida ja tallentaa dataa. C# tarjoaa monia valmiita tietorakenteita.

## Taulukot (Arrays)

Taulukko on kiinteän kokoinen kokoelma samantyyppisiä elementtejä.

### Yksiulotteinen taulukko

```csharp
// Määrittele ja alusta
int[] numbers = new int[5];
numbers[0] = 1;
numbers[1] = 2;
numbers[2] = 3;
numbers[3] = 4;
numbers[4] = 5;

// Tai lyhyemmin
int[] numbers2 = { 1, 2, 3, 4, 5 };

// Käyttö
Console.WriteLine(numbers[0]);  // 1
Console.WriteLine(numbers.Length);  // 5
```

### Moniulotteinen taulukko

```csharp
// 2D-taulukko (matriisi)
int[,] matrix = new int[3, 3];

// Alusta arvot
matrix[0, 0] = 1;
matrix[0, 1] = 2;
matrix[0, 2] = 3;
matrix[1, 0] = 4;
matrix[1, 1] = 5;
matrix[1, 2] = 6;
matrix[2, 0] = 7;
matrix[2, 1] = 8;
matrix[2, 2] = 9;

// Tai lyhyemmin
int[,] matrix2 = { { 1, 2, 3 }, { 4, 5, 6 }, { 7, 8, 9 } };
```

## Listat (Lists)

Lista on dynaaminen kokoelma, joka voi kasvaa ja pienentyä.

```csharp
using System.Collections.Generic;

// Luodaan lista
List<int> numbers = new List<int>();

// Lisää elementtejä
numbers.Add(1);
numbers.Add(2);
numbers.Add(3);

// Tai alusta heti
List<string> names = new List<string> { "Matti", "Liisa", "Pekka" };

// Käyttö
Console.WriteLine(names[0]);  // "Matti"
Console.WriteLine(names.Count);  // 3

// Poista elementti
names.Remove("Liisa");

// Tarkista onko elementti listassa
bool exists = names.Contains("Matti");
```

## Sanakirjat (Dictionaries)

Sanakirja tallentaa avain-arvo-pareja.

```csharp
using System.Collections.Generic;

// Luodaan sanakirja
Dictionary<string, int> ages = new Dictionary<string, int>();

// Lisää arvoja
ages["Matti"] = 25;
ages["Liisa"] = 30;
ages["Pekka"] = 28;

// Tai alusta heti
Dictionary<string, string> countries = new Dictionary<string, string>
{
    { "FI", "Suomi" },
    { "SE", "Ruotsi" },
    { "NO", "Norja" }
};

// Käyttö
Console.WriteLine(ages["Matti"]);  // 25

// Tarkista onko avain olemassa
if (ages.ContainsKey("Matti"))
{
    Console.WriteLine(ages["Matti"]);
}

// Iteroi läpi
foreach (var pair in ages)
{
    Console.WriteLine($"{pair.Key}: {pair.Value}");
}
```

## Joukot (Sets)

Joukko tallentaa uniikkeja elementtejä.

```csharp
using System.Collections.Generic;

// HashSet - nopea etsintä
HashSet<int> numbers = new HashSet<int> { 1, 2, 3, 4, 5 };

// Lisää elementti (jos ei jo ole)
numbers.Add(6);

// Tarkista onko elementti joukossa
bool exists = numbers.Contains(3);

// Poista elementti
numbers.Remove(3);
```

## Jono (Queue)

Jono on FIFO (First In, First Out) -rakenne.

```csharp
using System.Collections.Generic;

Queue<string> queue = new Queue<string>();

// Lisää jonoon
queue.Enqueue("Ensimmäinen");
queue.Enqueue("Toinen");
queue.Enqueue("Kolmas");

// Poista jonosta (ensimmäinen)
string first = queue.Dequeue();  // "Ensimmäinen"

// Katso seuraavaa ilman poistamista
string next = queue.Peek();  // "Toinen"
```

## Pino (Stack)

Pino on LIFO (Last In, First Out) -rakenne.

```csharp
using System.Collections.Generic;

Stack<string> stack = new Stack<string>();

// Lisää pinoon
stack.Push("Ensimmäinen");
stack.Push("Toinen");
stack.Push("Kolmas");

// Poista pinosta (viimeisin)
string last = stack.Pop();  // "Kolmas"

// Katso seuraavaa ilman poistamista
string next = stack.Peek();  // "Toinen"
```

## Vertailu

| Tietorakenne | Käyttö | Etsintä | Lisäys | Poisto |
|-------------|--------|---------|--------|--------|
| Array | Kiinteä koko | O(1) | - | - |
| List | Dynaaminen lista | O(n) | O(1) | O(n) |
| Dictionary | Avain-arvo-pari | O(1) | O(1) | O(1) |
| HashSet | Uniikit elementit | O(1) | O(1) | O(1) |
| Queue | FIFO-jono | - | O(1) | O(1) |
| Stack | LIFO-pino | - | O(1) | O(1) |

## Yhteenveto

- **Taulukot**: Kiinteän kokoinen kokoelma
- **Listat**: Dynaaminen kokoelma
- **Sanakirjat**: Avain-arvo-pareja
- **Joukot**: Uniikit elementit
- **Jonot**: FIFO-rakenne
- **Pinot**: LIFO-rakenne

Valitse oikea tietorakenne tarpeen mukaan!

Seuraavaksi: [Thread.Sleep](Thread-Sleep.md)

