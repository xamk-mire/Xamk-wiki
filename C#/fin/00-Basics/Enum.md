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
| `switch` | Yksi `case` per arvo plus `default` — kääntäjä ei varoita puuttuvasta haarasta |
| Numero taustalla | `(int)Size.Large` on `1`, `(Size)1` on `Large` |
| Teksti enumiksi | `Enum.TryParse(text, true, out Size size)` + `Enum.IsDefined` |
| `ToString()` | Nimi tekstinä: `"Large"`. Suomenkielinen nimi tulee metodista |
| Valikko | `enum MenuChoice { Exit = 0, SellTickets = 1, … }` — numerot auki, cast ei tarkista arvoa |

## Määrittely ja käyttö

Enum kirjoitetaan omaan tiedostoon kuten luokka: **Add → Class…** → `Size.cs`, ja sisällä `class` vaihdetaan sanaksi `enum`. Metodin sisällä enumia ei voi määritellä.

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
    default:
        Console.WriteLine($"Tuntematon koko: {size}");
        break;
}
```

Kääntäjä **ei varoita** puuttuvasta haarasta. Jos lisäät myöhemmin koon `Jumbo` etkä muista tätä `switch`-lausetta, `Jumbo` menisi hiljaa ohi ilman hintaa. `default` ottaa sen kiinni ja kertoo siitä — siksi `default` kirjoitetaan, vaikka kaikki nykyiset arvot on käsitelty.

Jokainen haara päättyy `break`- tai `return`-riviin. Ilman sitä käännös pysähtyy virheeseen **CS0163** (*Control cannot fall through from one case label to another*).

Suomenkielinen näyttönimi tulee samalla tavalla olion metodista, ei `ToString()`-kutsusta:

```csharp
public string GetCategoryName()
{
    switch (Category)
    {
        case AgeCategory.Child:  return "Lapsi";
        case AgeCategory.Adult:  return "Aikuinen";
        case AgeCategory.Senior: return "Seniori";
        default:                 return "Tuntematon";
    }
}
```

`Category` pysyy enumina (`AgeCategory.Child`), ja teksti on käyttöliittymän asia. `ToString()`-ylikirjoitus on jatkokurssin aihe.

Lisää `switch`-lauseesta: [ohjausrakenteet](Control-Structures.md#switch--yksi-muuttuja-monta-tarkkaa-arvoa).

## Numero taustalla

C# tallentaa enumin kokonaislukuna. Ensimmäinen nimi on `0`, seuraava `1`, ja niin edelleen. Voit antaa luvut itse, mutta alussa oletus riittää.

```csharp
Size size = Size.Large;
int number = (int)size;          // 1
Size fromNumber = (Size)1;       // Large — luvusta enumiksi, tätä käytät valikossa
string name = size.ToString();   // "Large"
```

Tekstistä enumiksi, kun käyttäjä kirjoittaa nimen:

```csharp
string text = Console.ReadLine();

if (Enum.TryParse(text, true, out Size parsed) && Enum.IsDefined(typeof(Size), parsed))
{
    Console.WriteLine(parsed);
}
```

`true` sallii `family` ja `FAMILY`. `Enum.IsDefined` tarvitaan, koska `TryParse` hyväksyy myös luvun `"7"` ja tekee siitä arvon `(Size)7`, jota ei ole määritelty.

Kaikki arvot silmukkaan: `foreach (Size s in Enum.GetValues(typeof(Size)))` — hyvä valikon tulostukseen.

Kaksi käännösvirhettä, jotka enum antaa puolestasi:

- `Size.Larg` → **CS0117** (*'Size' does not contain a definition for 'Larg'*). Merkkijono `"larg"` olisi kääntynyt ja hinta olisi väärä ajossa.
- `category == "Lapsi"` → **CS0019** (*Operator '==' cannot be applied to 'AgeCategory' and 'string'*). Enumia verrataan enumiin: `== AgeCategory.Child`.

Älä käytä enumia, jos lista muuttuu joka päivä tai tulee tiedostosta (kaupungin nimet, elokuvien otsikot). Siihen sopii [taulukko tai List](Data-Structures.md). Liput (`[Flags]`) ovat myöhempää.

## Valikko enumina

Konsolivalikko kysyy numeron, mutta koodissa valinnan pitäisi olla nimi, ei taikanumero `case 2:`. Numerot kirjoitetaan auki, koska ne ovat sopimus käyttäjän kanssa: valikossa lukee "1 Myy liput". Ilman numeroita ensimmäinen nimi olisi 0, ja rivien järjestys enumissa muuttaisi valikon toiminnan.

```csharp
enum MenuChoice
{
    Exit = 0,
    SellTickets = 1,
    ShowReceipts = 2,
    Report = 3
}
```

```csharp
int choice = ReadInt("Valinta: ", 0, 3);

if (Enum.IsDefined(typeof(MenuChoice), choice))
{
    MenuChoice menu = (MenuChoice)choice;

    switch (menu)
    {
        case MenuChoice.SellTickets:
            SellTickets();
            break;
        case MenuChoice.ShowReceipts:
            ShowReceipts();
            break;
        case MenuChoice.Report:
            PrintReport();
            break;
        case MenuChoice.Exit:
            running = false;
            break;
        default:
            Console.WriteLine("Tuntematon valinta.");
            break;
    }
}
```

Cast ei tarkista arvoa: `(MenuChoice)7` kääntyy ja ajaa, vaikka arvoa ei ole. Siksi luku rajataan `ReadInt`-kutsussa ja varmistetaan `Enum.IsDefined`-kutsulla ennen castia.

Käyttäjä ei huomaa eroa `case 2:`-riviin. Hyöty on koodissa: kirjoitusvirhe `MenuChoice.Raportti` on käännösvirhe (CS0117), ja uusi valinta lisätään yhteen paikkaan — yksi rivi enumiin ja yksi `case`-haara `switch`-lauseeseen.

## Yhteenveto

- Enum on suljettu lista nimistä omassa tiedostossaan. Parempi kuin taikanumero tai merkkijono.
- Vertaa `==` tai `switch`. `switch`-lauseeseen aina `default`: kääntäjä ei varoita puuttuvasta haarasta.
- Sopii kokoon, tilaan, ikäluokkaan. Ei sovi avoimeen listaan.
- Kirjoitusvirhe nimessä on käännösvirhe (CS0117), vertailu merkkijonoon on käännösvirhe (CS0019) — hyvä asia.
- Numero taustalla: `(int)size` ja `(Size)1`. Teksti enumiksi: `Enum.TryParse` + `Enum.IsDefined`.
- Valikko: numerot auki (`Quit = 0`), luku castilla enumiksi, `switch` nimillä. Rajaa ja tarkista luku ennen castia.
- Suomenkielinen nimi tulee metodista (`GetCategoryName`), ei enumista.

Seuraavaksi: [Ohjausrakenteet](Control-Structures.md) · [Luokat ja oliot](../02-OOP-Concepts/Classes-and-Objects.md) · [Propertyt](Properties.md)

## Hyödyllisiä linkkejä

- [Microsoft: Enumeration types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/enum) — määrittely, numerot, muunnokset
- [Microsoft: Enum.TryParse](https://learn.microsoft.com/en-us/dotnet/api/system.enum.tryparse) — teksti enumiksi; huomaa, että luku `"7"` hyväksytään
- [Microsoft: Enum.IsDefined](https://learn.microsoft.com/en-us/dotnet/api/system.enum.isdefined) — onko arvo oikeasti määritelty
- [Microsoft: Enum.GetValues](https://learn.microsoft.com/en-us/dotnet/api/system.enum.getvalues) — kaikki arvot silmukkaan
- [Microsoft: The switch statement](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/statements/selection-statements#the-switch-statement)
