# Casting (Tyyppimuunnos)

## Mikä on Casting?

Casting on prosessi, jossa muuttuja muunnetaan yhdestä tyypistä toiseen C#:ssa. Sitä käytetään yleisesti eri tietotyyppien, kokoelmien ja oliohierarkioiden kanssa. Castingia on kaksi päätyyppiä:

1. **Implicit Casting (Automaattinen muunnos)** – Muuntaa automaattisesti pienemmän tyypin suuremmaksi tyypiksi.
2. **Explicit Casting (Pakotettu muunnos)** – Muuntaa manuaalisesti suuremman tyypin pienemmäksi tyypiksi, mikä voi johtaa tietojen menetykseen.

## Casting-tyypit

### 1. Implicit Casting

Implicit casting tapahtuu automaattisesti, kun tietojen menetystä ei ole riskiä. Tämä tapahtuu yleensä, kun muunnetaan pienempi tietotyyppi suuremmaksi.

```csharp
// Pienempi tyyppi -> suurempi tyyppi (automaattinen)
int smallNumber = 10;
long largeNumber = smallNumber;  // Automaattinen muunnos int -> long

float floatValue = 3.14f;
double doubleValue = floatValue;  // Automaattinen muunnos float -> double

char character = 'A';
int charAsInt = character;  // Automaattinen muunnos char -> int
```

### 2. Explicit Casting

Explicit casting tarvitaan, kun muunnetaan suurempi tyyppi pienemmäksi tyypiksi, mikä vaatii manuaalisen castin. Tämä voi johtaa tietojen menetykseen tai poikkeuksiin.

```csharp
// Suurempi tyyppi -> pienempi tyyppi (pakotettu)
double doubleValue = 3.14;
int intValue = (int)doubleValue;  // 3 (desimaaliosa menetetään)

long largeNumber = 1000;
int smallNumber = (int)largeNumber;  // OK, jos arvo mahtuu int:ään

// Varoitus: tietojen menetys
double bigDouble = 999999999999.99;
int result = (int)bigDouble;  // Tietoja menetetään
```

### 3. Convert-luokan käyttö

`Convert`-luokka tarjoaa metodeja tietotyyppien turvalliseen muuntamiseen, käsitellen reunatapauksia, kuten null-arvot.

```csharp
string numberString = "123";
int number = Convert.ToInt32(numberString);  // 123

string doubleString = "3.14";
double doubleValue = Convert.ToDouble(doubleString);  // 3.14

// Null-arvon käsittely
string nullString = null;
int? nullableInt = Convert.ToInt32(nullString);  // 0 (oletusarvo)
```

### 4. `as`-operaattorin käyttö

`as`-operaattori yrittää muuntaa objektin tiettyyn tyyppiin. Jos muunnos epäonnistuu, se palauttaa `null` poikkeuksen sijaan.

```csharp
object obj = "Hello";
string str = obj as string;  // "Hello"

object obj2 = 123;
string str2 = obj2 as string;  // null (muunnos epäonnistui)

// Tarkistus
if (str2 != null)
{
    Console.WriteLine(str2);
}
else
{
    Console.WriteLine("Muunnos epäonnistui");
}
```

### 5. `is`-operaattorin käyttö

`is`-operaattori tarkistaa, onko objekti tiettyä tyyppiä ennen muunnoksen yrittämistä.

```csharp
object obj = "Hello";

if (obj is string)
{
    string str = (string)obj;  // Turvallinen muunnos
    Console.WriteLine(str);
}

// Pattern matching (C# 7.0+)
if (obj is string str2)
{
    Console.WriteLine(str2);  // str2 on automaattisesti määritelty
}
```

## Mikä on Cast<T>?

C#:ssa `Cast<T>` on LINQ-metodi, jota käytetään muuntamaan ei-geneerisen kokoelman (kuten `IEnumerable`) elementit määriteltyyn tyyppiin. Se on osa `System.Linq`-nimiavaruutta ja on hyödyllinen, kun työskennellään kokoelmien kanssa, joilla ei ole vahvasti tyypitettyä rajapintaa.

### Metodin allekirjoitus

```csharp
public static IEnumerable<TResult> Cast<TResult>(this IEnumerable source)
```

Tämä metodi yrittää muuntaa jokaisen elementin lähdekokoelmassa määriteltyyn tyyppiin `TResult`. Jos elementtiä ei voi muuntaa, heitetään `InvalidCastException`.

## Milloin Cast<T> käytetään?

- Kun työskennellään **ei-geneeristen kokoelmien** kanssa (esim. `ArrayList`), jotka tallentavat elementit `object`-tyyppinä, ja sinun täytyy työskennellä niiden kanssa tiettynä tyyppinä.
- Kun sinulla on **IEnumerable** ja sinun täytyy eksplisiittisesti muuntaa elementit tarkempaan tyyppiin.
- Kun käsitellään **LINQ-kyselyitä**, joissa syötekokoelma on tyyppiä `IEnumerable`.

## Esimerkkejä Cast<T> käytöstä

### Esimerkki 1: ArrayListin muuntaminen kokonaislukulistaksi

```csharp
using System;
using System.Collections;
using System.Linq;

ArrayList arrayList = new ArrayList { 1, 2, 3, 4, 5 };

// Cast<int>() varmistaa, että kaikki elementit käsitellään kokonaislukuina
var intList = arrayList.Cast<int>().ToList();

foreach (int number in intList)
{
    Console.WriteLine(number);
}
```

**Selitys**:
- `ArrayList` tallentaa objekteja, joten iteroinnin yhteydessä ne täytyy muuntaa `int`:ksi.
- `Cast<int>()` varmistaa, että kaikki elementit käsitellään kokonaislukuina.

### Esimerkki 2: Objektien muuntaminen IEnumerable:ssä

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

IEnumerable<object> objects = new List<object> { "Hello", "World", "C#" };

// Muunnetaan stringeiksi
var strings = objects.Cast<string>().ToList();

foreach (string str in strings)
{
    Console.WriteLine(str);
}
```

**Selitys**:
- Alkuperäinen kokoelma tallentaa elementit `object`-tyyppinä, joten ne täytyy muuntaa `string`:iksi.

### Esimerkki 3: Cast<T> käyttö LINQ:n kanssa

```csharp
using System;
using System.Collections;
using System.Linq;

ArrayList mixedList = new ArrayList { 1, 2, "three", 4 };

try
{
    // Yrittää muuntaa kaikki int:iksi
    var numbers = mixedList.Cast<int>().ToList();
}
catch (InvalidCastException ex)
{
    Console.WriteLine($"Virhe: {ex.Message}");
    // "three" ei voi muuntaa int:iksi -> InvalidCastException
}
```

**Selitys**:
- Lista sisältää merkkijonon `"three"`, jota ei voi muuntaa `int`:ksi.
- Tämä johtaa `InvalidCastException`-poikkeukseen.

## Cast<T> vs. OfType<T>

| Ominaisuus | `Cast<T>` | `OfType<T>` |
|------------|-----------|-------------|
| **Tyypin turvallisuus** | Oletetaan, että kaikki elementit voidaan muuntaa | Suodattaa pois elementit, joita ei voi muuntaa |
| **Poikkeuksen riski** | Heittää `InvalidCastException`, jos elementtiä ei voi muuntaa | Ei poikkeuksia; ohittaa yhteensopimattomat elementit |
| **Käyttötapaus** | Käytä, kun olet varma, että kaikki elementit voidaan muuntaa | Käytä, kun käsittelet sekatyppisiä kokoelmia |

### Esimerkki:

```csharp
using System;
using System.Collections;
using System.Linq;

ArrayList mixedList = new ArrayList { 1, 2, "three", 4, 5 };

// Cast<int>() - heittää poikkeuksen
try
{
    var castResult = mixedList.Cast<int>().ToList();
}
catch (InvalidCastException)
{
    Console.WriteLine("Cast<int>() epäonnistui");
}

// OfType<int>() - suodattaa pois yhteensopimattomat
var ofTypeResult = mixedList.OfType<int>().ToList();
// Tulos: [1, 2, 4, 5] ("three" suodatettu pois)
foreach (int num in ofTypeResult)
{
    Console.WriteLine(num);
}
```

## Yhteenveto

- **Casting** on prosessi muuttujan muuntamiseksi yhdestä tyypistä toiseen.
- **Implicit casting** tapahtuu automaattisesti, kun tietojen menetystä ei ole riskiä.
- **Explicit casting** vaatii manuaalisen castin ja voi johtaa tietojen menetykseen.
- **`Cast<T>`** on hyödyllinen, kun sinun täytyy muuntaa elementit ei-geneerisessä `IEnumerable`:ssä tiettyyn tyyppiin.
- Se **heittää poikkeuksen**, jos jokin elementti ei voi muuntaa.
- Jos haluat suodattaa pois yhteensopimattomat elementit poikkeuksen sijaan, käytä **`OfType<T>`**.

