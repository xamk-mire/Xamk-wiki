# Enum (Enumeraatio)

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum)

## Mikä on Enum?

`enum` (lyhenne sanasta "enumeration") on C#:ssa arvotyyppi, joka määritellään nimettyjen vakioiden joukolla, jotka perustuvat kokonaislukutyyppiin. Sitä käytetään symbolisten nimien antamiseen kokonaislukuarvoille, mikä tekee koodista luettavampaa ja ylläpidettävämpää.

## Milloin Enumia kannattaa käyttää?

### 1. Liittyvien vakioiden esittäminen

Käytä enumia, kun sinulla on joukko liittyviä kokonaislukuvakioita, kuten viikonpäivät, kuukaudet tai työnkulun tilat.

### 2. Koodin luettavuuden ja ylläpidettävyyden parantaminen

Enumit tekevät koodista luettavampaa ja ymmärrettävämpää korvaamalla "magia-numerot" merkityksellisillä nimillä.

### 3. Tyypin turvallisuus

Enumit tarjoavat tavan määritellä tyyppi, jolla voi olla vain yksi muutamasta mahdollisesta arvosta, estäen virheellisten arvojen asettamisen.

## Enumien hyödyt

1. **Selkeys**: Enumit tekevät koodista helpommin luettavaa ja ymmärrettävää, koska ne korvaavat kokonaislukuvakiot merkityksellisillä nimillä.
2. **Ylläpidettävyys**: Enum-vakion arvon muuttaminen päivittää automaattisesti kaikki viittaukset, mikä vähentää virheriskiä.
3. **Tyypin turvallisuus**: Enumit varmistavat, että vain kelvollisia arvoja käytetään.

## Milloin Enumia ei kannata käyttää?

### 1. Ei sovellu usein muuttuviin arvojoukkoihin

Jos arvojoukko muuttuu usein, enumin käyttö ei välttämättä ole paras valinta, koska se vaatii koodin uudelleenkäännön.

### 2. Suorituskyky pienissä skenaarioissa

Hyvin yksinkertaisissa tai suorituskykykriittisissä tilanteissa enumin käyttö voi aiheuttaa tarpeetonta ylimääräistä kuormaa.

### 3. Serialisointi ja yhteensopivuus

Hajautetuissa sovelluksissa enum-arvojen muuttaminen voi rikkoa yhteensopivuuden. Ole varovainen serialisoidessasi enumeja.

## Koodiesimerkit

### Perus enum-määrittely

```csharp
enum WeekDay
{
    Monday,
    Tuesday,
    Wednesday,
    Thursday,
    Friday,
    Saturday,
    Sunday
}
```

### Enumien käyttö

```csharp
WeekDay today = WeekDay.Monday;

if (today == WeekDay.Monday)
{
    Console.WriteLine("Aloitetaan uusi viikko!");
}

// Enum-arvo voidaan myös muuntaa kokonaisluvuksi
int dayNumber = (int)today;  // 0 (Monday on ensimmäinen, arvo 0)
```

### Enum eksplisiittisillä arvoilla

```csharp
enum Status
{
    Pending = 0,
    InProgress = 1,
    Completed = 2,
    Cancelled = 3
}

Status currentStatus = Status.InProgress;
int statusValue = (int)currentStatus;  // 1
```

### Enum switch-case-lauseessa

```csharp
enum Priority
{
    Low,
    Medium,
    High,
    Critical
}

void ProcessTask(Priority priority)
{
    switch (priority)
    {
        case Priority.Low:
            Console.WriteLine("Käsitellään hiljaisesti");
            break;
        case Priority.Medium:
            Console.WriteLine("Käsitellään normaalisti");
            break;
        case Priority.High:
            Console.WriteLine("Käsitellään kiireellisesti");
            break;
        case Priority.Critical:
            Console.WriteLine("Käsitellään välittömästi!");
            break;
        default:
            Console.WriteLine("Tuntematon prioriteetti");
            break;
    }
}

// Käyttö
ProcessTask(Priority.High);
```

### Enum merkkijonona

```csharp
enum Color
{
    Red,
    Green,
    Blue
}

Color myColor = Color.Red;

// Muunnetaan merkkijonoksi
string colorName = myColor.ToString();  // "Red"

// Muunnetaan merkkijonosta enumiksi
if (Enum.TryParse<Color>("Green", out Color parsedColor))
{
    Console.WriteLine($"Parsed color: {parsedColor}");  // Green
}
```

### Enum kaikilla arvoilla

```csharp
enum Direction
{
    North,
    South,
    East,
    West
}

// Käydään läpi kaikki enum-arvot
foreach (Direction dir in Enum.GetValues(typeof(Direction)))
{
    Console.WriteLine(dir);
}
```

## Yhteenveto

Enumit ovat C#:ssa tehokas ominaisuus, joka parantaa merkittävästi koodin luettavuutta, ylläpidettävyyttä ja turvallisuutta, kun niitä käytetään asianmukaisesti. Niitä tulisi kuitenkin käyttää harkiten, erityisesti tilanteissa, joissa joustavuus tai suorituskyky on keskeinen huolenaihe.

