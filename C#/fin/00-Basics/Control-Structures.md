# Ohjausrakenteet (Control Structures)

Ohjausrakenteet ohjaavat ohjelman suoritusta: **mitä** tehdään ja **kuinka monta kertaa**. Kolme perusrakennetta riittää kuvaamaan minkä tahansa ohjelman: peräkkäisyys (rivit järjestyksessä), valinta (`if`) ja toisto (silmukat).

Vertailut ja `&&` / `||`: [Operaattorit](Operators.md).

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

Vain **yksi** haara suoritetaan — ensimmäinen, jonka ehto on tosi. Siksi `else if (age < 65)` tarkoittaa "12–64-vuotias": jos suoritus pääsi tähän asti, ikä oli jo vähintään 18 (esimerkin ensimmäisen ehdon jälkeen).

### Ehtojen järjestyksellä on väliä

```csharp
// ✅ Oikea järjestys: kapein ehto ensin
if (age < 12) { /* Lapsi */ }
else if (age < 65) { /* Aikuinen */ }
else { /* Seniori */ }

// ❌ Väärä järjestys: 5-vuotias täyttää age < 65 ja saa aikuisen hinnan
if (age < 65) { /* Aikuinen */ }
else if (age < 12) { /* Lapsi — tänne ei koskaan päästä */ }
```

Testaa aina **raja-arvot**: 11, 12, 64 ja 65. Yhden merkin ero (`<` vs `<=`) vaihtaa luokan.

Loogiset ehdot (`ikä < 0 || ikä > 130`, `vastaus != "k" && vastaus != "e"`) on selitetty sivulla [Operaattorit](Operators.md).

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

### Milloin mitäkin silmukkaa?

| Silmukka | Milloin | Esimerkki |
|----------|---------|---------------------|
| `while` | Toistetaan **niin kauan kuin** ehto on tosi — kierrosmäärää ei tiedetä | Kysy ikä uudelleen, kunnes se on 0–130 |
| `for` | Toistetaan **tietty määrä** kertoja | Yksi kierros per lippu (`i = 1; i <= ticketCount; i++`) |
| `do-while` | Kuten while, mutta runko ajetaan **vähintään kerran** | Kassa palvelee ainakin yhden asiakkaan |
| `foreach` | Käydään kokoelma läpi ilman indeksiä | Päivän ostokset, menun tulostus ilman numeroita |

`for` vs `foreach`: jos tarvitset järjestysnumeron (`1. Margherita`) tai indeksin (`movies[i]`), käytä `for`. Jos tarvitset vain alkiot, `foreach` on selkeämpi.

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

### while vs do-while

```
while (ehto)          do
{                     {
    runko                 runko
}                     } while (ehto);

Ehto ENNEN runkoa     Ehto RUNGON JÄLKEEN
→ voi pyöriä 0 krt    → pyörii aina vähintään 1 krt
```

Kassan jatkokysymys sopii `do-while`-rakenteeseen: ensimmäistä asiakasta ei kysytä ("palvellaanko ketään?"), vaan palvelu alkaa heti.

Muuttuja, jota ehto käyttää, pitää esitellä **ennen** silmukkaa. Jos `string? continueAnswer` on `do`-lohkon sisällä, `while`-ehto ei näe sitä — [näkyvyysalue](Scopes.md).

### Ikuinen silmukka

Silmukka ei pääty, jos ehdon muuttujaa ei muuteta rungossa:

```csharp
int age = 200;
while (age < 0 || age > 130)
{
    Console.WriteLine("Virheellinen ikä.");
    // age = Convert.ToInt32(Console.ReadLine());  ← ilman tätä silmukka ei lopu
}
```

Pysäytä juokseva ohjelma sulkemalla konsoli tai **Ctrl+C**. Tunnistaminen: sama viesti tulvii ruudulle eikä kysymys etene.

### Kertymämuuttuja

Summa kerätään silmukan aikana. Alustus on **aina silmukan ulkopuolella**:

```csharp
decimal subtotal = 0m;          // ennen for-silmukkaa

for (int i = 1; i <= ticketCount; i++)
{
    decimal unitPrice = GetUnitPrice(age);
    subtotal += unitPrice;      // sama kuin subtotal = subtotal + unitPrice
}
```

Jos `subtotal = 0m` on silmukan sisällä, jäljelle jää vain viimeisen kierroksen hinta.

Sama kaava päivän myynnille: esittely ennen asiakassilmukkaa, `+=` sisällä, käyttö jälkeen (raportti).

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

- **If / else if / else**: yksi haara — ehtojen järjestyksellä on väliä, testaa raja-arvot
- **while**: ehto ensin, voi pyöriä 0 kertaa — syötteen tarkistus
- **do-while**: runko ensin, vähintään yksi kerta — asiakassilmukka
- **for**: tiedetty kierrosmäärä — liput, valikon numerointi
- **foreach**: kokoelma ilman indeksiä
- **Kertymä** (`+=`) alustetaan silmukan ulkopuolella
- **Ikuinen silmukka**: ehdon muuttuja ei muutu — tunnista ja korjaa

Seuraavaksi: [Operaattorit](Operators.md) · [Debuggaus](Debug.md) · [Tietorakenteet](Data-Structures.md)

