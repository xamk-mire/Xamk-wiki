# DateTime (päivämäärä ja kellonaika)

`DateTime` on tyyppi yhdelle ajanhetkelle: päivä, ja tarvittaessa kello.

Arjen esimerkki: lipun ostopäivä, näytöksen kellonaika, "onko syntymäpäivä jo tänä vuonna".

**Microsoft:** [DateTime](https://learn.microsoft.com/fi-fi/dotnet/api/system.datetime)

## Kartta

| Kirjoitus | Merkitys |
|-----------|----------|
| `DateTime.Now` | Tämä hetki, kello mukana |
| `DateTime.Today` | Tämä päivä, kello 00:00 |
| `new DateTime(2024, 1, 15)` | Vuosi, kuukausi, päivä |
| `AddDays(7)` | Uusi hetki viikon päästä (alkuperäinen ei muutu) |
| `ToString("dd.MM.yyyy")` | Suomalainen päivämäärä tekstinä |

## Luonti

```csharp
DateTime now = DateTime.Now;
DateTime today = DateTime.Today;
DateTime premiere = new DateTime(2024, 1, 15);
DateTime showtime = new DateTime(2024, 1, 15, 18, 30, 0);   // 15.1.2024 18:30
```

Järjestys konstruktorissa on vuosi, kuukausi, päivä. Sitten tunti, minuutti, sekunti.

Osia voi lukea erikseen: `now.Year`, `now.Month`, `now.Day`, `now.Hour`, `now.DayOfWeek`.

## Laskenta ja vertailu

`AddDays`, `AddMonths` ja `AddYears` palauttavat **uuden** arvon. Vanha muuttuja ei muutu, ellet sijoita tulosta.

```csharp
DateTime today = DateTime.Today;
DateTime nextWeek = today.AddDays(7);
DateTime lastWeek = today.AddDays(-7);
```

Vertailu samoilla merkeillä kuin luvuilla:

```csharp
DateTime start = new DateTime(2024, 1, 15);
DateTime end = new DateTime(2024, 1, 20);

if (start < end)
{
    TimeSpan length = end - start;
    Console.WriteLine($"{length.Days} päivää");   // 5
}
```

`TimeSpan` on kesto, ei kellonaika. Siinä on `Days`, `Hours`, `TotalHours`.

## Tulostus

Suomalaisessa Windowsissa oletus voi näyttää pilkkuja ja pisteitä eri tavalla. Kuitissa ja otsikossa kannattaa antaa muoto itse.

```csharp
DateTime day = new DateTime(2024, 1, 15, 14, 30, 0);

Console.WriteLine(day.ToString("dd.MM.yyyy"));         // 15.01.2024
Console.WriteLine(day.ToString("dd.MM.yyyy HH:mm"));   // 15.01.2024 14:30
Console.WriteLine(day.ToString("yyyy-MM-dd"));         // 2024-01-15
```

| Koodi | Merkitys |
|-------|----------|
| `dd` | Päivä kahdella numerolla |
| `MM` | Kuukausi kahdella numerolla (`mm` on minuutti) |
| `yyyy` | Vuosi neljällä numerolla |
| `HH` | Tunti 24-tuntisena |
| `mm` | Minuutti |

`MM` ja `mm` menevät usein sekaisin. Kuukausi on isoilla.

## Iän laskeminen syntymäpäivästä

```csharp
DateTime birth = new DateTime(1990, 5, 15);
DateTime today = DateTime.Today;

int age = today.Year - birth.Year;
if (birth.Date > today.AddYears(-age))
{
    age--;   // syntymäpäivä ei ole vielä tänä vuonna
}
```

Pelkkä vuosien erotus valehtelisi joulukuussa, jos syntymäpäivä on vasta tammikuussa.

Tekstistä päivämääräksi: `DateTime.Parse` / `TryParse`. Sama varoitus kuin luvuissa — väärä muoto kaataa `Parse`-kutsun. Katso [muuttujat](Variables.md) ja [tyyppimuunnokset](Casting.md).

UTC ja aikavyöhykkeet kuuluvat myöhempään. Alussa `DateTime.Now` ja `Today` riittävät yhden koneen ohjelmaan.

## Yhteenveto

- `Now` = nyt. `Today` = tämä päivä ilman kelloa.
- `AddDays` palauttaa uuden arvon — sijoita se muuttujaan.
- Vertaa `<` / `>`. Erotus on `TimeSpan`.
- Muotoile itse: `dd.MM.yyyy`. `MM` = kuukausi, `mm` = minuutti.

Seuraavaksi: [Muuttujat](Variables.md) · [Enum](Enum.md) · [Tiedostojen luku ja kirjoitus](File-IO.md)
