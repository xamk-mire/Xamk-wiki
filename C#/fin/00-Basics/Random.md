# Random (Satunnaislukujen generointi)

`Random`-luokka C#-kielessä mahdollistaa satunnaislukujen generoinnin.

## Random-luokan käyttö

### Peruskäyttö

```csharp
Random random = new Random();

// Generoi satunnaisen kokonaisluvun 0 ja int.MaxValue välillä
int number = random.Next();
Console.WriteLine(number);

// Generoi satunnaisen kokonaisluvun 0 ja 10 välillä (10 ei sisälly)
int number1 = random.Next(10);
Console.WriteLine(number1);  // 0-9

// Generoi satunnaisen kokonaisluvun määritellyllä välillä
int number2 = random.Next(1, 11);
Console.WriteLine(number2);  // 1-10

// Generoi satunnaisen desimaaliluvun 0.0 ja 1.0 välillä
double doubleValue = random.NextDouble();
Console.WriteLine(doubleValue);  // 0.0 - 1.0
```

## Yleisiä käyttökohteita

### Satunnaisen luvun generointi välillä

```csharp
Random random = new Random();

// Luku 1-100 välillä
int number = random.Next(1, 101);

// Luku 0-50 välillä
int number2 = random.Next(0, 51);
```

### Satunnaisen desimaaliluvun generointi välillä

```csharp
Random random = new Random();

// Desimaaliluku 0.0 - 100.0 välillä
double value = random.NextDouble() * 100;

// Desimaaliluku 10.0 - 20.0 välillä
double value2 = 10 + (random.NextDouble() * 10);
```

### Satunnaisen totuusarvon generointi

```csharp
Random random = new Random();

bool randomBool = random.Next(2) == 0;  // true tai false
// Tai
bool randomBool2 = random.NextDouble() < 0.5;
```

### Satunnaisen merkin generointi

```csharp
Random random = new Random();

// Satunnainen iso kirjain A-Z
char randomChar = (char)random.Next('A', 'Z' + 1);

// Satunnainen pieni kirjain a-z
char randomLower = (char)random.Next('a', 'z' + 1);
```

### Satunnaisen merkkijonon generointi

```csharp
Random random = new Random();
string chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
int length = 10;

string randomString = new string(
    Enumerable.Repeat(chars, length)
              .Select(s => s[random.Next(s.Length)])
              .ToArray()
);

Console.WriteLine(randomString);  // Esim. "A3B7C2D9E1"
```

### Satunnaisen värin generointi

```csharp
Random random = new Random();

// RGB-väri
int red = random.Next(0, 256);
int green = random.Next(0, 256);
int blue = random.Next(0, 256);

Console.WriteLine($"RGB({red}, {green}, {blue})");
```

## Satunnaisen elementin valinta taulukosta

```csharp
Random random = new Random();
string[] names = { "Matti", "Liisa", "Pekka", "Anna", "Jukka" };

// Valitse satunnainen nimi
string randomName = names[random.Next(names.Length)];
Console.WriteLine(randomName);
```

## Satunnaisen elementin valinta listasta

```csharp
Random random = new Random();
List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };

// Valitse satunnainen numero
int randomNumber = numbers[random.Next(numbers.Count)];
Console.WriteLine(randomNumber);
```

## Satunnaisen järjestyksen luominen (Shuffle)

```csharp
Random random = new Random();
List<int> numbers = new List<int> { 1, 2, 3, 4, 5 };

// Sekoita lista
for (int i = numbers.Count - 1; i > 0; i--)
{
    int j = random.Next(i + 1);
    int temp = numbers[i];
    numbers[i] = numbers[j];
    numbers[j] = temp;
}

// numbers on nyt sekoitettu
```

## Seed-arvo (Alkuarvo)

Random-luokka käyttää oletuksena kellonaikaa seed-arvona. Voit antaa oman seed-arvon:

```csharp
// Sama seed tuottaa samat satunnaisluvut
Random random1 = new Random(12345);
Random random2 = new Random(12345);

int num1 = random1.Next(100);
int num2 = random2.Next(100);

Console.WriteLine(num1 == num2);  // true - samat luvut!
```

**Huomio**: Sama seed-arvo on hyödyllinen testauksessa, mutta tuotannossa käytä oletusarvoa.

## Yleisiä virheitä

### ❌ Luodaan uusi Random-olio liian usein

```csharp
// ❌ HUONO: Uusi Random-olio jokaisella kutsulla
for (int i = 0; i < 10; i++)
{
    Random random = new Random();  // Sama seed → samat luvut!
    Console.WriteLine(random.Next(100));
}
```

### ✅ Luodaan Random-olio kerran

```csharp
// ✅ HYVÄ: Yksi Random-olio
Random random = new Random();
for (int i = 0; i < 10; i++)
{
    Console.WriteLine(random.Next(100));
}
```

## Yhteenveto

- `Random`-luokka generoi satunnaislukuja
- `Next()` generoi kokonaislukuja
- `NextDouble()` generoi desimaalilukuja
- Luodaan yleensä yksi Random-olio ja käytetään sitä useita kertoja
- Seed-arvo määrittää satunnaislukujen sekvenssin

Seuraavaksi: [Tietorakenteet](Data-Structures.md)

