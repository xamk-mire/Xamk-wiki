# Enum (enumeraatio)

**Enum** on nimetty lista sallituista arvoista. Kirjoitat `Size.Large` etkä merkkijonoa `"iso"` tai lukua `2`.

Merkkijono `"iso"` voi olla `"Iso"`, `"ISO"` tai kirjoitusvirhe `"is o"`. Enumissa väärää kokoa ei ole, ellei sitä lisätä tyyppiin.

Pizzan koko, lipun ikäluokka ja tilauksen tila ovat tyypillisiä enumeja: arvoja on vähän ja ne tunnetaan etukäteen.

**Microsoft:** [Enumeration types](https://learn.microsoft.com/fi-fi/dotnet/csharp/language-reference/builtin-types/enum)

## Kartta

| Asia | Yksi lause |
|------|------------|
| Määrittely | `enum Size { Normal, Large, Family }` |
| Käyttö | `Size size = Size.Large;` |
| Vertailu | `if (size == Size.Large)` |
| `switch` | Yksi haara per arvo — usein selkeämpi kuin merkkijonot |
| `ToString()` | Nimi tekstinä: `"Large"` |

## Määrittely ja käyttö

Enum määritellään yleensä luokan ulkopuolella tai luokan sisällä, ei metodin sisällä.

```csharp
enum Size
{
    Normal,
    Large,
    Family
}
```

```csharp
Size size = Size.Large;

if (size == Size.Large)
{
    price += 3.00m;
}
```

Nimet ovat PascalCase. Pisteen jälkeen IntelliSense näyttää vaihtoehdot. Et joudu muistamaan merkkijonoja.

Ikäluokka samalla idealla:

```csharp
enum AgeCategory
{
    Child,
    Adult,
    Senior
}

static AgeCategory GetCategory(int age)
{
    if (age < 12) return AgeCategory.Child;
    if (age < 65) return AgeCategory.Adult;
    return AgeCategory.Senior;
}
```

## switch sopii enumille

`switch` vertaa tarkkoja arvoja. Enum on juuri sitä.

```csharp
switch (size)
{
    case Size.Normal:
        price = 10.00m;
        break;
    case Size.Large:
        price = 13.00m;
        break;
    case Size.Family:
        price = 18.00m;
        break;
}
```

Jos lisäät myöhemmin uuden koon, kääntäjä voi varoittaa puuttuvasta haarasta. Merkkijono-`if` ei varoita.

Lisää `switch`-lauseesta: [ohjausrakenteet](Control-Structures.md#switch--yksi-muuttuja-monta-tarkkaa-arvoa).

## Numero taustalla

C# tallentaa enumin kokonaislukuna. Ensimmäinen nimi on `0`, seuraava `1`, ja niin edelleen. Voit antaa luvut itse, mutta alussa oletus riittää.

```csharp
Size size = Size.Large;
int number = (int)size;          // 1, jos Large on toinen
string name = size.ToString();   // "Large"
```

Tekstistä enumiksi:

```csharp
if (Enum.TryParse("Large", out Size parsed))
{
    Console.WriteLine(parsed);
}
```

Älä käytä enumia, jos lista muuttuu joka päivä tai tulee tiedostosta (kaupungin nimet, elokuvien otsikot). Siihen sopii [taulukko tai List](Data-Structures.md).

Kaikkien arvojen läpikäynti (`Enum.GetValues`) ja liput (`[Flags]`) ovat myöhempää.

## Yhteenveto

- Enum on suljettu lista nimistä. Parempi kuin taikanumero tai merkkijono.
- Vertaa `==` tai `switch`.
- Sopii kokoon, tilaan, ikäluokkaan. Ei sovi avoimeen listaan.
- Kirjoitusvirhe nimessä on käännösvirhe — hyvä asia.

Seuraavaksi: [Ohjausrakenteet](Control-Structures.md) · [Luokat ja oliot](../02-OOP-Concepts/Classes-and-Objects.md) · [Propertyt](Properties.md)
