# Ohjausrakenteet (Control Structures)

Ohjausrakenteet ohjaavat ohjelman suoritusta. Ne määrittävät, mitä koodia suoritetaan ja milloin.

## Ehdolliset lauseet (Conditional Statements)

### If-lause

```csharp
if (condition)
{
    // Koodi suoritetaan jos ehto on tosi
}
```

### If-else-lause

```csharp
if (condition)
{
    // Koodi jos ehto on tosi
}
else
{
    // Koodi jos ehto on epätosi
}
```

### If-else if-else-lause

```csharp
if (condition1)
{
    // Koodi jos ehto1 on tosi
}
else if (condition2)
{
    // Koodi jos ehto2 on tosi
}
else
{
    // Koodi jos mikään ehto ei ole tosi
}
```

### Esimerkki

```csharp
int age = 20;

if (age < 18)
{
    Console.WriteLine("Olet alaikäinen");
}
else if (age < 65)
{
    Console.WriteLine("Olet aikuinen");
}
else
{
    Console.WriteLine("Olet eläkeläinen");
}
```

### Switch-lause

```csharp
switch (variable)
{
    case value1:
        // Koodi
        break;
    case value2:
        // Koodi
        break;
    default:
        // Koodi jos mikään case ei täsmää
        break;
}
```

### Esimerkki switch-lauseesta

```csharp
string day = "Monday";

switch (day)
{
    case "Monday":
    case "Tuesday":
    case "Wednesday":
    case "Thursday":
    case "Friday":
        Console.WriteLine("Työpäivä");
        break;
    case "Saturday":
    case "Sunday":
        Console.WriteLine("Viikonloppu");
        break;
    default:
        Console.WriteLine("Tuntematon päivä");
        break;
}
```

### Switch-lauseke (C# 8.0+)

```csharp
string result = day switch
{
    "Monday" or "Tuesday" or "Wednesday" or "Thursday" or "Friday" => "Työpäivä",
    "Saturday" or "Sunday" => "Viikonloppu",
    _ => "Tuntematon päivä"
};
```

## Silmukat (Loops)

### For-silmukka

```csharp
for (initialization; condition; increment)
{
    // Koodi
}
```

### Esimerkki

```csharp
// Tulosta numerot 1-10
for (int i = 1; i <= 10; i++)
{
    Console.WriteLine(i);
}

// Taulukon läpikäynti
int[] numbers = { 1, 2, 3, 4, 5 };
for (int i = 0; i < numbers.Length; i++)
{
    Console.WriteLine(numbers[i]);
}
```

### Foreach-silmukka

```csharp
foreach (type variable in collection)
{
    // Koodi
}
```

### Esimerkki

```csharp
int[] numbers = { 1, 2, 3, 4, 5 };

foreach (int number in numbers)
{
    Console.WriteLine(number);
}

// Listan läpikäynti
List<string> names = new List<string> { "Matti", "Liisa", "Pekka" };
foreach (string name in names)
{
    Console.WriteLine(name);
}
```

### While-silmukka

```csharp
while (condition)
{
    // Koodi
}
```

### Esimerkki

```csharp
int count = 0;
while (count < 5)
{
    Console.WriteLine(count);
    count++;
}
```

### Do-while-silmukka

```csharp
do
{
    // Koodi
}
while (condition);
```

### Esimerkki

```csharp
int number;
do
{
    Console.Write("Anna positiivinen luku: ");
    number = int.Parse(Console.ReadLine());
}
while (number <= 0);
```

## Silmukoiden ohjaus

### Break

Keskeyttää silmukan suorituksen:

```csharp
for (int i = 0; i < 10; i++)
{
    if (i == 5)
        break;  // Lopettaa silmukan
    
    Console.WriteLine(i);
}
// Tulostaa: 0, 1, 2, 3, 4
```

### Continue

Siirtyy seuraavalle iteraatiolle:

```csharp
for (int i = 0; i < 10; i++)
{
    if (i % 2 == 0)
        continue;  // Ohita parilliset luvut
    
    Console.WriteLine(i);
}
// Tulostaa: 1, 3, 5, 7, 9
```

## Sisäkkäiset silmukat

```csharp
// Tulosta kertotaulu
for (int i = 1; i <= 10; i++)
{
    for (int j = 1; j <= 10; j++)
    {
        Console.Write($"{i * j,4}");
    }
    Console.WriteLine();
}
```

## Ternary-operaattori (Kolmioperoattori)

Lyhyt tapa kirjoittaa if-else-lause:

```csharp
// Perinteinen tapa
string message;
if (age >= 18)
{
    message = "Aikuinen";
}
else
{
    message = "Alaikäinen";
}

// Ternary-operaattori
string message = age >= 18 ? "Aikuinen" : "Alaikäinen";
```

## Yhteenveto

- **If-lauseet**: Ehdollinen suoritus
- **Switch-lauseet**: Monivalinta
- **For-silmukka**: Tiedetty määrä iteraatioita
- **Foreach-silmukka**: Kokoelman läpikäynti
- **While-silmukka**: Ehdollinen toisto
- **Break/Continue**: Silmukan ohjaus

Seuraavaksi: [Debug](Debug.md)

