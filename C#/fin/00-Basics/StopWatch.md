# StopWatch

**HUOM! Tämä ei suoraan ole perusteita ja ei tulla kysymään tentissä**

[How to calculate the code execution time in C#? (tutorialsteacher.com)](https://www.tutorialsteacher.com/articles/how-to-calculate-code-execution-time-in-csharp)  
[Stopwatch Class (System.Diagnostics) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.stopwatch?view=net-7.0)

`Stopwatch` on luokka C#-ohjelmointikielessä, joka kuuluu `System.Diagnostics`-nimiavaruuteen. Se tarjoaa yksinkertaisen ja tehokkaan tavan mitata ajan kulumista, esimerkiksi kuinka kauan tietty koodin osa kestää suorittaa. `Stopwatch` on hyödyllinen suorituskyvyn profiloinnissa ja ajoituksen mittauksessa.

## Peruskäyttö

```csharp
using System.Diagnostics;

Stopwatch stopwatch = new Stopwatch();
stopwatch.Start();

// Simuloidaan aikaa vievää toimintoa
Thread.Sleep(1000); // Odota 1 sekunti

stopwatch.Stop();

// Hae kulunut aika
TimeSpan elapsed = stopwatch.Elapsed;
Console.WriteLine($"Kulunut aika: {elapsed.TotalMilliseconds} ms");
```

Selitys:
1. Luodaan uusi `Stopwatch`-olio.
2. Käynnistetään ajanotto `Start`-metodilla.
3. Tässä esimerkissä, simuloimme jonkin aikaa vievää toimintoa `Thread.Sleep`-metodilla, joka odottaa 1 sekunnin.
4. Pysäytämme ajanoton `Stop`-metodilla.
5. Haemme kuluneen ajan `Elapsed`-ominaisuuden avulla, joka palauttaa `TimeSpan`-olion.
6. Tulostamme kuluneen ajan `Console.WriteLine`-metodilla ja näytämme kuluneen ajan millisekuntteina.

## Käyttöesimerkkejä

### 1. Metodin suoritusajan mittaus

```csharp
using System.Diagnostics;

Stopwatch sw = new Stopwatch();
sw.Start();

// Mitataan metodin suoritusaikaa
DoSomething();

sw.Stop();
Console.WriteLine($"Metodi kesti: {sw.ElapsedMilliseconds} ms");
```

### 2. Useita mittauksia

```csharp
using System.Diagnostics;

Stopwatch sw = new Stopwatch();

// Ensimmäinen mittaus
sw.Start();
Method1();
sw.Stop();
Console.WriteLine($"Method1: {sw.ElapsedMilliseconds} ms");

// Nollataan ja aloitetaan uusi mittaus
sw.Reset();
sw.Start();
Method2();
sw.Stop();
Console.WriteLine($"Method2: {sw.ElapsedMilliseconds} ms");
```

### 3. Restart-metodi

```csharp
using System.Diagnostics;

Stopwatch sw = new Stopwatch();

sw.Start();
DoFirstThing();
sw.Restart(); // Nollaa ja käynnistää uudelleen
DoSecondThing();
sw.Stop();

Console.WriteLine($"Toinen operaatio kesti: {sw.ElapsedMilliseconds} ms");
```

### 4. Tarkka ajanmittaus

```csharp
using System.Diagnostics;

Stopwatch sw = Stopwatch.StartNew(); // Luodaan ja käynnistetään samalla

// Koodia mitataan
for (int i = 0; i < 1000000; i++)
{
    // Jotain laskutoimituksia
}

sw.Stop();

Console.WriteLine($"Kulunut aika: {sw.Elapsed}");
Console.WriteLine($"Millisekuntteina: {sw.ElapsedMilliseconds} ms");
Console.WriteLine($"Tikkeinä: {sw.ElapsedTicks}");
```

## Tärkeät ominaisuudet ja metodit

### Ominaisuudet

- `Elapsed`: Palauttaa `TimeSpan`-olion, joka kuvaa kulunutta aikaa
- `ElapsedMilliseconds`: Kulunut aika millisekuntteina (long)
- `ElapsedTicks`: Kulunut aika tikkienä (long)
- `IsRunning`: Totuusarvo, joka kertoo onko stopwatch käynnissä

### Metodit

- `Start()`: Käynnistää ajanoton
- `Stop()`: Pysäyttää ajanoton
- `Reset()`: Nollaa stopwatchin
- `Restart()`: Nollaa ja käynnistää uudelleen

## Yhteenveto

`Stopwatch`-luokka on hyvin suoraviivainen ja helppo käyttää, ja se on erinomainen työkalu suorituskyvyn mittaukseen ja ajoituksen tarkkailuun C#-ohjelmissa.

**Käyttökohteet:**
- Suorituskyvyn profiloinnissa
- Algoritmien nopeuden vertailussa
- Koodin optimoinnissa
- Ajoitusten testauksessa

Seuraavaksi: [Thread.Sleep](Thread-Sleep.md)

