# Rekursio (Recursion)

Rekursio ohjelmoinnissa viittaa toimintatapaan, jossa funktio kutsuu itseään suorituksensa aikana. Tämä mahdollistaa monimutkaisten ongelmien ratkaisemisen jakamalla ne pienempiin, samankaltaisiin osaongelmiin. Rekursiivinen funktio tarvitsee aina ehdon sen suorituksen lopettamiseksi, jotta se ei jää loputtomaan kutsujen ketjuun.

## Perusperiaate

Rekursiivinen funktio koostuu kahdesta osasta:
1. **Perustapaus (Base case)**: Ehto, joka lopettaa rekursion
2. **Rekursiivinen kutsu**: Funktio kutsuu itseään pienemmällä ongelmalla

## Esimerkki: Faktoriaalifunktio

Faktoriaali n! on luku kerrottuna kaikilla positiivisilla kokonaisluvuilla sen alapuolella. Esimerkiksi 5! = 5 × 4 × 3 × 2 × 1 = 120

### Rekursiivinen toteutus

```csharp
public static int Factorial(int n)
{
    // Perustapaus: 0! = 1 ja 1! = 1
    if (n <= 1)
    {
        return 1;
    }
    
    // Rekursiivinen kutsu: n! = n × (n-1)!
    return n * Factorial(n - 1);
}

// Käyttö
int tulos = Factorial(5);
Console.WriteLine(tulos); // 120
```

### Miten se toimii?

```
Factorial(5)
  → 5 * Factorial(4)
    → 4 * Factorial(3)
      → 3 * Factorial(2)
        → 2 * Factorial(1)
          → 1 (perustapaus)
        → 2 * 1 = 2
      → 3 * 2 = 6
    → 4 * 6 = 24
  → 5 * 24 = 120
```

## Esimerkki: Fibonacci-luku

Fibonacci-sekvenssi: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
Jokainen luku on kahden edellisen summa.

```csharp
public static int Fibonacci(int n)
{
    // Perustapaukset
    if (n == 0)
        return 0;
    if (n == 1)
        return 1;
    
    // Rekursiivinen kutsu
    return Fibonacci(n - 1) + Fibonacci(n - 2);
}

// Käyttö
for (int i = 0; i < 10; i++)
{
    Console.Write($"{Fibonacci(i)} ");
}
// Tulostaa: 0 1 1 2 3 5 8 13 21 34
```

## Esimerkki: Potenssiin korotus

```csharp
public static int Power(int baseNum, int exponent)
{
    // Perustapaus: mikä tahansa luku potenssiin 0 = 1
    if (exponent == 0)
        return 1;
    
    // Rekursiivinen kutsu: base^exponent = base × base^(exponent-1)
    return baseNum * Power(baseNum, exponent - 1);
}

// Käyttö
int tulos = Power(2, 8);
Console.WriteLine(tulos); // 256
```

## Esimerkki: Listan summa

```csharp
public static int Sum(List<int> numbers)
{
    // Perustapaus: tyhjä lista
    if (numbers.Count == 0)
        return 0;
    
    // Rekursiivinen kutsu: summa = ensimmäinen + summa(loppu)
    int first = numbers[0];
    List<int> rest = numbers.Skip(1).ToList();
    return first + Sum(rest);
}

// Käyttö
List<int> numerot = new List<int> { 1, 2, 3, 4, 5 };
int summa = Sum(numerot);
Console.WriteLine(summa); // 15
```

## Tärkeät huomiot

### 1. Älä unohda perustapausta!

**❌ HUONO - Loputon silmukka:**

```csharp
public static int BadRecursion(int n)
{
    // EI PERUSTAPAUSTA! Tämä aiheuttaa StackOverflowException
    return n + BadRecursion(n - 1);
}
```

**✅ HYVÄ - Oikea perustapaus:**

```csharp
public static int GoodRecursion(int n)
{
    // Perustapaus
    if (n <= 0)
        return 0;
    
    // Rekursiivinen kutsu
    return n + GoodRecursion(n - 1);
}
```

### 2. Rekursio voi olla hidas

Rekursiivinen toteutus voi olla hitaampi kuin iteratiivinen, koska jokainen funktiokutsu vie muistia ja aikaa.

**Rekursiivinen (hitaampi):**

```csharp
public static int FibonacciRecursive(int n)
{
    if (n <= 1) return n;
    return FibonacciRecursive(n - 1) + FibonacciRecursive(n - 2);
}
```

**Iteratiivinen (nopeampi):**

```csharp
public static int FibonacciIterative(int n)
{
    if (n <= 1) return n;
    
    int prev = 0;
    int current = 1;
    
    for (int i = 2; i <= n; i++)
    {
        int next = prev + current;
        prev = current;
        current = next;
    }
    
    return current;
}
```

### 3. Stack Overflow

Liian syvä rekursio voi aiheuttaa `StackOverflowException`:

```csharp
// ⚠️ Varoitus: Tämä voi aiheuttaa StackOverflowException suurilla arvoilla
public static int DeepRecursion(int n)
{
    if (n <= 0) return 0;
    return 1 + DeepRecursion(n - 1);
}

// Suurilla arvoilla tämä kaatuu
// DeepRecursion(100000); // StackOverflowException!
```

## Milloin käyttää rekursiota?

### ✅ Hyvät käyttökohteet:

- **Puurakenteet**: Puiden läpikäynti (esim. hakemistorakenteet)
- **Jako ja hallitse -algoritmit**: Quicksort, mergesort
- **Matemaattiset ongelmat**: Faktoriaali, Fibonacci, potenssiin korotus
- **Ongelmat, jotka ovat luonteeltaan rekursiivisia**: Hanoi-tornit, permutaatiot

### ❌ Huonot käyttökohteet:

- **Yksinkertaiset toistot**: Käytä silmukoita sen sijaan
- **Suorituskykykriittiset osat**: Iteratiivinen toteutus on yleensä nopeampi
- **Syvät rekursiot**: Voivat aiheuttaa StackOverflowException

## Yhteenveto

- Rekursio on funktio, joka kutsuu itseään
- Tarvitsee aina perustapauksen, joka lopettaa rekursion
- Sopii hyvin ongelmiin, jotka voidaan jakaa pienempiin samankaltaisiin osaongelmiin
- Voi olla hitaampi kuin iteratiivinen toteutus
- Liian syvä rekursio voi aiheuttaa StackOverflowException

**Muista**: Rekursio on työkalu, ei tavoite. Käytä sitä kun se tekee koodista selkeämmän, mutta harkitse iteratiivista toteutusta suorituskyvyn kannalta.

Seuraavaksi: [Funktiot ja Metodit](Functions-and-Methods.md)

