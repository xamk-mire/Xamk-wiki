# DateTime

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/api/system.datetime?view=net-8.0)

## Mikä on DateTime?

`DateTime` on osa `System`-nimiavaruutta C#:ssa. Sitä käytetään päivämäärien ja kellonaikojen käsittelyyn C#:ssa. `DateTime`-rakenne tarjoaa metodeja ja ominaisuuksia erilaisten päivämäärä- ja kellonaikaoperaatioiden suorittamiseen, kuten päivien lisäämiseen päivämäärään, päivämäärien vertailuun tai päivämäärien muotoiluun näyttöä varten.

## Milloin DateTimeia kannattaa käyttää?

### 1. Päivämäärien ja kellonaikojen esittäminen

Aina kun sinun täytyy esittää tietty hetki, olipa kyseessä sitten nykyinen aika, syntymäpäivä tai tulevaisuudessa tapahtuva tapahtuma.

### 2. Aikavälien laskeminen

`DateTime`-rakennetta voidaan käyttää päivämäärien välien laskemiseen (esim. päivien määrän löytäminen tapahtumaan asti tai henkilön iän laskeminen).

### 3. Tietojen tallennus ja haku

Päivämäärien ja kellonaikojen tallentaminen tietokantoihin, tiedostoihin tai muihin tallennusjärjestelmiin ja niiden hakeminen ja käsittely.

### 4. Päivämäärien ja kellonaikojen muotoilu näyttöä varten

Päivämäärien ja kellonaikojen muotoilu käyttöliittymässä käyttäjäystävälliseen muotoon.

### 5. Ajoitus ja aikaperusteiset operaatiot

Tilanteissa, joissa toiminnot on ajoitettava tapahtumaan tiettynä ajankohtana tai tietyn keston jälkeen.

## DateTimein hyödyt

1. **Helppous**: `DateTime` tarjoaa suoraviivaisen ja intuitiivisen tavan käsitellä päivämääriä ja kellonaikoja koodissasi.
2. **Vankkuus**: Se käsittelee erilaisia päivämäärä- ja kellonaikalaskennan monimutkaisuuksia, kuten karkausvuodet, aikavyöhykkeet, kesäaika jne.
3. **Joustavuus ja toiminnallisuus**: Tarjoaa lukuisia metodeja ja ominaisuuksia erityyppisiin päivämäärä- ja kellonaikamanipulaatioihin.
4. **Kulttuuritietoinen muotoilu**: Tukee kulttuuritietoista muotoilua, mikä tekee siitä hyödyllisen globaaleissa sovelluksissa.
5. **Yhteentoimivuus**: Helppo yhteentoimivuus tietokantojen ja muiden tietolähteiden kanssa, jotka tallentavat päivämäärä- ja kellonaikatietoja.
6. **Standardisointi**: Tarjoaa standardoidun lähestymistavan päivämäärien ja kellonaikojen käsittelyyn sovelluksen eri osissa.

## Koodiesimerkit

### Peruskäyttö

```csharp
using System;

// Nykyinen päivämäärä ja aika
DateTime now = DateTime.Now;
Console.WriteLine($"Nykyinen aika: {now}");

// Tänään (ilman kellonaikaa)
DateTime today = DateTime.Today;
Console.WriteLine($"Tänään: {today}");

// Tietty päivämäärä
DateTime specificDate = new DateTime(2024, 1, 15);
Console.WriteLine($"Tietty päivämäärä: {specificDate}");

// Päivämäärä ja kellonaika
DateTime dateTime = new DateTime(2024, 1, 15, 14, 30, 0);
Console.WriteLine($"Päivämäärä ja aika: {dateTime}");
```

### Päivämäärien laskeminen

```csharp
DateTime today = DateTime.Today;

// Lisätään päiviä
DateTime nextWeek = today.AddDays(7);
Console.WriteLine($"Viikon päästä: {nextWeek}");

// Vähennetään päiviä
DateTime lastWeek = today.AddDays(-7);
Console.WriteLine($"Viikko sitten: {lastWeek}");

// Lisätään kuukausia
DateTime nextMonth = today.AddMonths(1);
Console.WriteLine($"Kuukauden päästä: {nextMonth}");

// Lisätään vuosia
DateTime nextYear = today.AddYears(1);
Console.WriteLine($"Vuoden päästä: {nextYear}");
```

### Päivämäärien vertailu

```csharp
DateTime date1 = new DateTime(2024, 1, 15);
DateTime date2 = new DateTime(2024, 1, 20);

// Vertailu
if (date1 < date2)
{
    Console.WriteLine($"{date1} on ennen {date2}");
}

// Aikavälin laskeminen
TimeSpan difference = date2 - date1;
Console.WriteLine($"Aikaväli: {difference.Days} päivää");
```

### Päivämäärien muotoilu

```csharp
DateTime now = DateTime.Now;

// Eri muotoiluja
Console.WriteLine(now.ToString("dd.MM.yyyy"));        // 15.01.2024
Console.WriteLine(now.ToString("yyyy-MM-dd"));      // 2024-01-15
Console.WriteLine(now.ToString("dd.MM.yyyy HH:mm")); // 15.01.2024 14:30
Console.WriteLine(now.ToString("dddd, MMMM dd"));   // Monday, January 15

// Enkoodattu muotoilu
Console.WriteLine(now.ToShortDateString());  // 15.1.2024
Console.WriteLine(now.ToLongDateString());   // Monday, January 15, 2024
Console.WriteLine(now.ToShortTimeString()); // 14:30
Console.WriteLine(now.ToLongTimeString());   // 14:30:00
```

### Iän laskeminen

```csharp
DateTime birthDate = new DateTime(1990, 5, 15);
DateTime today = DateTime.Today;

int age = today.Year - birthDate.Year;

// Tarkistetaan, onko syntymäpäivä jo tullut tänä vuonna
if (birthDate.Date > today.AddYears(-age))
{
    age--;
}

Console.WriteLine($"Ikä: {age} vuotta");
```

### Päivämääräkomponentit

```csharp
DateTime now = DateTime.Now;

Console.WriteLine($"Vuosi: {now.Year}");
Console.WriteLine($"Kuukausi: {now.Month}");
Console.WriteLine($"Päivä: {now.Day}");
Console.WriteLine($"Tunti: {now.Hour}");
Console.WriteLine($"Minuutti: {now.Minute}");
Console.WriteLine($"Sekunti: {now.Second}");
Console.WriteLine($"Viikonpäivä: {now.DayOfWeek}");
Console.WriteLine($"Vuoden päivä: {now.DayOfYear}");
```

### UTC (Coordinated Universal Time)

```csharp
// Paikallinen aika
DateTime localTime = DateTime.Now;
Console.WriteLine($"Paikallinen aika: {localTime}");

// UTC-aika
DateTime utcTime = DateTime.UtcNow;
Console.WriteLine($"UTC-aika: {utcTime}");

// Muunnos UTC:ksi
DateTime toUtc = localTime.ToUniversalTime();
Console.WriteLine($"Muunnettu UTC:ksi: {toUtc}");

// Muunnos paikalliseksi ajaksi
DateTime toLocal = utcTime.ToLocalTime();
Console.WriteLine($"Muunnettu paikalliseksi: {toLocal}");
```

## Yhteenveto

`DateTime` on keskeinen työkalu päivämäärien ja kellonaikojen käsittelyyn C#:ssa. Se tarjoaa monipuoliset toiminnot päivämäärien luomiseen, muokkaamiseen, vertailuun ja muotoiluun, mikä tekee siitä välttämättömän osan useimpia C#-sovelluksia.

