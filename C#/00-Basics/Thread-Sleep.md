# Thread.Sleep

`Thread.Sleep`-metodi pausettaa nykyisen säikeen (thread) suorituksen määritellyksi ajaksi.

## Peruskäyttö

### Syntaksi

```csharp
Thread.Sleep(millisekuntia);
```

### Esimerkki

```csharp
using System.Threading;

Console.WriteLine("Aloitus");
Thread.Sleep(2000);  // Odota 2 sekuntia (2000 millisekuntia)
Console.WriteLine("2 sekuntia myöhemmin");
```

## Yleisiä käyttökohteita

### 1. Simuloidaan viivettä

```csharp
Console.WriteLine("Lataa...");
Thread.Sleep(1000);
Console.WriteLine("Valmis!");
```

### 2. Animaatiot ja visuaaliset efektit

```csharp
for (int i = 0; i < 10; i++)
{
    Console.Write(".");
    Thread.Sleep(200);  // 200ms viive pisteiden välillä
}
Console.WriteLine();
```

### 3. Retry-logiikka

```csharp
int maxRetries = 3;
int retryCount = 0;

while (retryCount < maxRetries)
{
    try
    {
        // Yritä tehdä jotain
        DoSomething();
        break;  // Onnistui, poistu silmukasta
    }
    catch (Exception)
    {
        retryCount++;
        if (retryCount < maxRetries)
        {
            Console.WriteLine($"Yritetään uudelleen {retryCount}/{maxRetries}...");
            Thread.Sleep(1000);  // Odota 1 sekunti ennen uutta yritystä
        }
    }
}
```

### 4. Rate limiting

```csharp
for (int i = 0; i < 100; i++)
{
    ProcessItem(i);
    Thread.Sleep(100);  // Rajoita käsittelynopeutta (10 kpl/sekunti)
}
```

## Aikayksiköt

### Millisekunnit

```csharp
Thread.Sleep(1000);  // 1 sekunti
Thread.Sleep(500);   // 0.5 sekuntia
Thread.Sleep(100);   // 0.1 sekuntia
```

### TimeSpan (Suositeltu tapa)

```csharp
using System;

// Selkeämpi tapa
Thread.Sleep(TimeSpan.FromSeconds(2));      // 2 sekuntia
Thread.Sleep(TimeSpan.FromMilliseconds(500)); // 0.5 sekuntia
Thread.Sleep(TimeSpan.FromMinutes(1));     // 1 minuutti
```

## Tärkeät huomiot

### 1. Thread.Sleep pausettaa koko säikeen

```csharp
// ❌ HUOMIO: Pausettaa koko ohjelman
Console.WriteLine("Ennen");
Thread.Sleep(2000);
Console.WriteLine("Jälkeen");
```

### 2. Async/await on parempi vaihtoehto

```csharp
// ✅ HYVÄ: Ei pauseta koko säiettä
using System.Threading.Tasks;

public async Task DoSomethingAsync()
{
    Console.WriteLine("Ennen");
    await Task.Delay(2000);  // Ei pauseta koko säiettä
    Console.WriteLine("Jälkeen");
}
```

### 3. Thread.Sleep(0) antaa muille säikeille tilaa

```csharp
// Antaa muille säikeille mahdollisuuden suorittua
Thread.Sleep(0);
```

## Esimerkki: Laskuri viiveellä

```csharp
Console.WriteLine("Laskuri alkaa:");
for (int i = 10; i > 0; i--)
{
    Console.WriteLine(i);
    Thread.Sleep(1000);  // Odota 1 sekunti
}
Console.WriteLine("Valmis!");
```

## Esimerkki: Progress bar

```csharp
Console.Write("Lataa: [");
for (int i = 0; i < 20; i++)
{
    Console.Write("#");
    Thread.Sleep(100);  // 100ms viive
}
Console.WriteLine("] Valmis!");
```

## Yhteenveto

- `Thread.Sleep` pausettaa säikeen suorituksen
- Parametri on millisekunteina
- Käytä `TimeSpan`-luokkaa selkeämpään koodiin
- Async/await on parempi vaihtoehto modernissa koodissa
- Hyödyllinen simulointiin, animaatioihin ja retry-logiikkaan

**Huomio**: Tuotannossa harkitse `Task.Delay`-metodia async-koodissa sen sijaan, että käytät `Thread.Sleep`-metodia.

