# Thread.Sleep — tauko ohjelmaan

**`Thread.Sleep(ms)`** pysäyttää ohjelman annetuksi ajaksi millisekunteina. `Thread.Sleep(1000)` on sekunnin tauko. `Thread` on nimiavaruudessa `System.Threading`, joka on .NET 8 -projektipohjassa valmiina käytössä (implicit usings).

Arjen esimerkki: latauspalkki. Ilman taukoa 0–100 % vilahtaa ohi ennen kuin ehdit nähdä. Pieni tauko joka askeleella tekee siitä seurattavan.

Tyypillinen tilanne: jatkuva peli, jossa kierroslaskuri päivittyy samalle riville ja käyttäjä lopettaa näppäimellä. Tauko kierrosten välissä on 10–100 ms, ei sekuntia.

**Microsoft:** [Thread.Sleep](https://learn.microsoft.com/fi-fi/dotnet/api/system.threading.thread.sleep)

## Kartta

| Asia | Yksi lause |
|------|------------|
| `Thread.Sleep(1000)` | Sekunnin tauko; ohjelma ei tee tauon aikana mitään |
| `Thread.Sleep(10)` … `Thread.Sleep(100)` | Sopiva tauko jatkuvan silmukan kierrosten väliin |
| `Thread.Sleep(random.Next(1000, 5001))` | Satunnainen odotus 1–5 s |
| `Console.Write($"\r...")` + `Sleep` | Laskuri, joka päivittyy samalle riville |

## Ohjelma seisoo tauon ajan

```csharp
Console.WriteLine("Arvotaan...");
Thread.Sleep(2000);                 // 2 sekuntia: mitään ei tapahdu
Console.WriteLine("Valmis.");
```

Tauon aikana ohjelma **ei lue näppäimistöä eikä tulosta** mitään. Painallus jää puskuriin ja huomataan vasta tauon jälkeen. Siksi jatkuvassa silmukassa tauko on lyhyt, 10–100 ms: silmukka ehtii tarkistaa näppäimen monta kertaa sekunnissa, eikä peli tunnu jumilta.

```csharp
while (!stop)
{
    // yksi kierros: arvonta, tulostus, näppäimen tarkistus
    Thread.Sleep(50);               // ei 1000
}
```

Näppäimen tarkistus ilman odotusta: [KeyAvailable ja ReadKey](Console-IO.md#näppäin-ilman-enteriä-readkey-ja-keyavailable).

## Laskuri samalla rivillä

```csharp
for (int percent = 0; percent <= 100; percent += 5)
{
    Console.Write($"\rLadataan... {percent} %");
    Thread.Sleep(100);
}

Console.WriteLine();                // uusi rivi vasta lopuksi
```

`\r` siirtää kohdistimen rivin alkuun, `Write` kirjoittaa vanhan päälle, ja `Sleep` antaa silmälle aikaa nähdä välivaiheet. Ilman `Sleep`-kutsua näkyisi vain `100 %`. Katso [sama rivi uudelleen](Console-IO.md#sama-rivi-uudelleen-r).

## Satunnainen odotus pelissä

```csharp
static Random random = new Random();

Console.WriteLine("Odota...");
Thread.Sleep(random.Next(1000, 5001));   // 1–5 s
Console.WriteLine("Nyt!");
```

Reaktiopeli tai arvonta tuntuu aidommalta, kun odotus vaihtelee. `Next(1000, 5001)` antaa 1000–5000 ms — katso [Random](Random.md).

## Myöhemmin

`Thread.Sleep` pysäyttää koko ohjelman. Ohjelmissa, joiden pitää tehdä useaa asiaa samaan aikaan (verkko, käyttöliittymä), käytetään `Task.Delay`-metodia ja `async`-koodia. Ne tulevat jatkokurssilla. `Sleep` hyväksyy myös `TimeSpan`-arvon (`TimeSpan.FromSeconds(2)`), mutta tällä kurssilla millisekunnit riittävät.

## Yleisiä virheitä

**1. Pitkä `Sleep` jatkuvassa pelissä**

`Thread.Sleep(1000)` joka kierroksella: peli tuntuu jumilta, ja näppäinpainallus huomataan sekunnin myöhässä. Pidä tauko 10–100 ms.

**2. `Sleep` ei odota näppäintä**

`Sleep` odottaa vain aikaa. Jos haluat odottaa, että käyttäjä painaa jotain, käytä `Console.ReadLine()` tai `Console.ReadKey()`.

**3. `Sleep` silmukassa ilman tulostusta**

Jos silmukka nukkuu eikä tulosta mitään, käyttäjä näkee tyhjän ruudun ja luulee ohjelman kaatuneen. Tulosta jotain joka kierroksella, vaikka samalle riville.

## Yhteenveto

- `Thread.Sleep(ms)` pysäyttää ohjelman millisekunneiksi. Tauon aikana ei lueta näppäimistöä eikä tulosteta.
- Jatkuvassa silmukassa tauko on 10–100 ms, ei sekuntia.
- Laskuri samalle riville: `Console.Write($"\r...")` + `Sleep`, `WriteLine()` kerran lopuksi.
- Satunnainen odotus: `Thread.Sleep(random.Next(1000, 5001))`.
- `Task.Delay` ja `async` ovat jatkokurssin asiaa.

Seuraavaksi: [Konsolin syöte ja tulostus](Console-IO.md) · [Random](Random.md) · [StopWatch](StopWatch.md)
