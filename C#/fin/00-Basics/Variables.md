# Muuttujat (Variables)

**Muuttuja** on nimetty säilö. Annat sille nimen ja tyypin. Ohjelma laittaa säilöön arvon, lukee sen myöhemmin ja voi vaihtaa arvon.

Arjen esimerkki: lipun hintalappu. Lappuun kirjoitetaan `12.00`. Nimi voisi olla `unitPrice`. Tyyppi kertoo, että kyse on rahasta (`decimal`), ei tekstistä.

```csharp
int age = 20;
decimal unitPrice = 12.00m;
string category = "Aikuinen";
```

Lue rivi vasemmalta: tyyppi, nimi, arvo. `int age = 20` tarkoittaa: "luo kokonaislukusäilö nimeltä age ja laita siihen 20".

**Microsoft:** [Built-in types](https://learn.microsoft.com/fi-fi/dotnet/csharp/language-reference/builtin-types/built-in-types)

## Kartta

| Tyyppi | Mitä säilyttää | Esimerkki kurssilla |
|--------|----------------|---------------------|
| `int` | Kokonaisluku | Ikä, lippumäärä, saldo |
| `decimal` | Rahasumma, tarkka desimaali | Hinta, välisumma. Aina `m`-pääte |
| `string` | Teksti | Nimi, alennuskoodi, syöte |
| `bool` | Kyllä tai ei | `isStudent`, ehdon tulos |
| `const` | Arvo, joka ei muutu | `ChildPrice = 7.50m` |
| `double`, `var`, `null` | Myöhemmin | [Lyhyesti sivun lopussa](#double-var-ja-null--myöhemmin) |

Syöte konsolista on aina `string`, kunnes muunnat sen: [tyyppimuunnokset](Casting.md). Laskumerkit: [operaattorit](Operators.md).

## Muuttujan määrittely

```csharp
tyyppi nimi = arvo;
```

```csharp
int balance = 200;            // kokonaisluku
decimal price = 7.50m;        // raha, m-pääte
string name = "Matti";        // teksti hipsuissa
bool isStudent = true;        // tosi tai epätosi
```

Muuttujan voi esitellä ensin ja antaa arvon myöhemmin. Lukeminen ennen arvon antamista ei käänny.

```csharp
int ticketCount;              // esittely: säilö on olemassa, mutta tyhjä
ticketCount = 2;              // sijoitus: säilöön laitetaan 2
```

Arvoa voi vaihtaa niin monta kertaa kuin haluat. Nimi ja tyyppi pysyvät.

```csharp
int balance = 200;
balance = balance - 50;       // lue vanha arvo, laske, laita tulos samaan säilöön
Console.WriteLine(balance);   // 150
```

Rivi `balance = balance - 50` ei ole yhtälö. Se luetaan oikealta vasemmalle: laske ensin `balance - 50`, sijoita sitten tulos säilöön `balance`. Laskuri `count++` toimii samalla idealla: [sijoitus ja lyhenteet](Operators.md#sijoitus-ja-lyhenteet).

Tyyppi ei vaihdu. `int`-säilöön ei mahdu tekstiä:

```csharp
int age = 20;
// age = "kaksikymmentä";     // ei käänny: Cannot implicitly convert type 'string' to 'int'
```

## Tyypit

### int

[Microsoft: Integral numeric types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types)

`int` (*integer*) on kokonaisluku: ilman desimaaleja, positiivinen tai negatiivinen. Ikä, lippumäärä, valikon numero ja silmukan laskuri ovat `int`-tyyppisiä.

```csharp
int age = 25;
int ticketCount = 3;
int attempts = 0;

attempts = attempts + 1;      // 1
attempts++;                   // 2
```

Kahden `int`-luvun jako on kokonaislukujako. Desimaalit katkaistaan pois:

```csharp
int result = 17 / 5;          // 3, ei 3.4
int remainder = 17 % 5;       // 2 (jakojäännös)
```

Jos tarvitset desimaalit, laske `decimal`-tyypillä. Katso [aritmeettiset operaattorit](Operators.md#aritmeettiset-operaattorit).

`int` mahtuu välille −2 147 483 648 … 2 147 483 647. Kurssin luvut mahtuvat siihen. Konsolista luettu liian iso luku kaataa ohjelman `OverflowException`-poikkeukseen: [tyyppimuunnokset](Casting.md).

### decimal — raha

[Microsoft: Floating-point numeric types](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/floating-point-numeric-types)

`decimal` on desimaaliluku, joka on suunniteltu **tarkkaan** laskentaan. Rahat (`price`, `subtotal`, `discount`, `dailySales`) pidetään `decimal`-tyyppinä.

```csharp
decimal childPrice = 7.50m;
decimal adultPrice = 12.00m;
decimal subtotal = adultPrice * 2;   // 24.00
```

| Asia | Selitys |
|------|---------|
| `m`-pääte | Ilman `m`:ää luku `7.50` on `double`. C# ei sijoita `double`-arvoa `decimal`-muuttujaan automaattisesti |
| Piste koodissa | Kirjoita `7.50m`, vaikka konsoli näyttäisi `7,50` |
| Tulostus | `{price:F2}` antaa kaksi desimaalia: `12,00` |

```csharp
decimal total = 21.6m;
Console.WriteLine($"Maksettavaa: {total:F2} €");
// Maksettavaa: 21,60 €
```

`int` kertaa `decimal` onnistuu ilman muunnosta. Lippumäärä kertaa hinta on `decimal`:

```csharp
int ticketCount = 2;
decimal unitPrice = 12.00m;
decimal subtotal = unitPrice * ticketCount;   // 24.00
```

**Miksi ei `double`?** Liukuluku tallentaa luvun likiarvona. Sentit voivat "valua":

```csharp
Console.WriteLine(0.1 + 0.2);      // 0.30000000000000004
Console.WriteLine(0.1m + 0.2m);    // 0.3
```

Yhdessä laskussa virhe on mitätön. Sadassa kuitissa se kertyy. Nyrkkisääntö: **raha = `decimal`**.

### string

[Microsoft: Strings](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)

`string` on merkkijono eli tekstiä: sanoja, lauseita, myös numeroita merkkeinä. Teksti kirjoitetaan hipsuihin `" "`. Hipsut kertovat kääntäjälle, että kyseessä on teksti, eivätkä ne tulostu.

```csharp
string greeting = "Hei maailma!";
Console.WriteLine(greeting);           // Hei maailma!
```

Ilman hipsuja `Hei` olisi muuttujan nimi, jota ei ole olemassa, ja koodi ei käänny.

`"200"` ja `200` ovat eri asia. Ensimmäinen on kolme merkkiä, toinen on luku. Merkeillä ei voi laskea:

```csharp
string text = "200";
int number = 200;
// int sum = text + 1;          // ei käänny: teksti + luku ei ole lasku
int sum = number + 1;           // 201
```

Merkkijonoja yhdistetään `+`-merkillä. Selkeämpi tapa on **interpolointi**: `$`-alkuinen merkkijono, jossa muuttuja on aaltosulkeissa.

```csharp
string firstName = "Matti";
int age = 30;

Console.WriteLine("Hei, " + firstName + "! Olet " + age + " vuotta.");   // yhdistäminen
Console.WriteLine($"Hei, {firstName}! Olet {age} vuotta.");              // interpolointi
```

Ilman `$`-merkkiä aaltosulkeet tulostuvat sellaisenaan: `Hei, {firstName}!`. Lisää: [merkkijonointerpolaatio](Console-IO.md#merkkijonointerpolaatio).

Kaksi metodia, joita tarvitset alussa:

```csharp
string code = "leffa10";

Console.WriteLine(code.Length);        // 7 (merkkien määrä)
Console.WriteLine(code.ToUpper());     // LEFFA10
```

Vertailu `==` on **kirjainkokoherkkä**: `"LEFFA10"` ja `"leffa10"` ovat eri merkkijonoja. Jos kirjainkoolla ei saa olla väliä, muunna syöte ensin isoiksi kirjaimiksi: `code.ToUpper() == "LEFFA10"`. Katso [vertailuoperaattorit](Operators.md#vertailuoperaattorit).

### bool (Boolean)

[Microsoft: bool](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/bool)

`bool` voi saada vain kaksi arvoa: `true` (tosi) tai `false` (epätosi). Sitä käytetään ehdoissa.

```csharp
bool isStudent = true;

if (isStudent)
{
    Console.WriteLine("Opiskelija-alennus");
}
```

Vertailun tulos on `bool`. Siksi vertailun voi tallentaa muuttujaan ja käyttää myöhemmin:

```csharp
int age = 20;
bool isAdult = age >= 18;       // true
bool isChild = age < 12;        // false

Console.WriteLine(isAdult);     // True
```

Nimeä `bool`-muuttuja kysymykseksi, johon vastataan kyllä tai ei: `isStudent`, `hasDiscount`, `canContinue`.

Ehtoja yhdistetään operaattoreilla `&&` (ja), `||` (tai) ja `!` (ei): [loogiset operaattorit](Operators.md#loogiset-operaattorit). `int.TryParse` palauttaa `bool`-arvon, joka kertoo, onnistuiko muunnos: [TryParse](Casting.md#tryparse--kysy-uudelleen).

### const — arvo, joka ei muutu

`const` on vakio. Arvo annetaan kerran, eikä sitä voi vaihtaa. Lippujen hinnat ja PIN-koodi ovat vakioita.

```csharp
const decimal ChildPrice = 7.50m;
const decimal AdultPrice = 12.00m;
const int CorrectPin = 1234;

// ChildPrice = 8.00m;         // ei käänny: The left-hand side of an assignment must be a variable
```

Vakion nimi on PascalCase, muuttujan camelCase. Kun vakio tarvitaan useassa metodissa, se kirjoitetaan luokan tasolle `Main`-metodin ulkopuolelle: [luokan taso](Scopes.md#luokan-taso--jaettu-tieto).

Vakio korvaa "taikaluvun". Rivi `price = 7.50m` ei kerro, mikä hinta on kyseessä. Rivi `price = ChildPrice` kertoo. Kun hinta muuttuu, korjaat yhden rivin.

## Syöte on tekstiä

`Console.ReadLine()` palauttaa aina `string`-arvon, vaikka käyttäjä kirjoittaisi numeroita. Luvuksi se muunnetaan erikseen:

```csharp
Console.Write("Anna ikäsi: ");
string? input = Console.ReadLine();
int age = Convert.ToInt32(input);
```

`Convert.ToInt32("abc")` kaataa ohjelman `FormatException`-poikkeukseen. `int.TryParse` ei kaada, vaan palauttaa `false`, ja ohjelma voi kysyä uudelleen. Molemmat selitetään sivulla [tyyppimuunnokset](Casting.md).

## Muuttujan nimeäminen

Säännöt, jotka kääntäjä vaatii:

1. Nimi alkaa kirjaimella tai alaviivalla `_`.
2. Nimi saa sisältää kirjaimia, numeroita ja alaviivoja. Ei välilyöntiä, ei viivaa.
3. Nimi ei saa olla varattu sana (`int`, `class`, `void`).
4. Nimi on kirjainkokoherkkä: `age` ja `Age` ovat eri muuttujat.

```csharp
int age = 25;              // hyvä
string firstName = "Matti";
bool isActive = true;

// int 2age = 25;          // ei voi alkaa numerolla
// string first-name = ""; // viiva ei käy
// int class = 5;          // varattu sana
```

Käytännöt, joita kurssilla noudatetaan:

| Käytäntö | Esimerkki |
|----------|-----------|
| camelCase muuttujille | `ticketCount`, `unitPrice` |
| PascalCase vakioille | `ChildPrice` |
| Englanti | `age`, ei `ika` |
| Kuvaava nimi | `ticketCount`, ei `n` tai `x` |

Lisää: [koodauskäytännöt](Coding-Conventions.md).

## Yleisiä virheitä

**1. `m`-pääte puuttuu**

```csharp
// decimal price = 7.50;     // ei käänny: Cannot implicitly convert type 'double' to 'decimal'
decimal price = 7.50m;
```

**2. Muuttujaa luetaan ennen arvon antamista**

```csharp
int total;
// Console.WriteLine(total); // ei käänny: Use of unassigned local variable 'total'
total = 0;
Console.WriteLine(total);    // 0
```

Kertymämuuttuja alustetaan aina: `decimal total = 0m;`.

**3. Sama nimi kahdesti**

```csharp
int age = 20;
// int age = 25;             // ei käänny: A local variable named 'age' is already defined
age = 25;                    // oikein: sijoitus ilman tyyppiä
```

Tyyppi kirjoitetaan vain esittelyssä. Sijoituksessa riittää nimi.

**4. Teksti ja luku sekaisin**

```csharp
string input = "200";
// if (input == 200)          // ei käänny: string ja int eivät ole vertailukelpoisia
if (Convert.ToInt32(input) == 200)
{
    Console.WriteLine("Sama luku");
}
```

**5. Sijoitus vertailun paikalla**

`age = 18` sijoittaa, `age == 18` vertaa. `if (age = 18)` ei käänny. Katso [yleisiä virheitä valinnassa](Control-Structures.md#yleisiä-virheitä-valinnassa).

## double, var ja null — myöhemmin

Näitä ei tarvita kurssin ensimmäisissä ohjelmissa. Lyhyt esittely riittää, jotta tunnistat ne, kun näet ne.

### double

`double` on liukuluku: desimaaliluku, joka sopii mittauksiin, lämpötiloihin ja koordinaatteihin. Pieni pyöristysvirhe ei haittaa niissä.

```csharp
double temperature = 23.5;
double average = 17 / 5.0;    // 3.4
```

Rahaan `double` ei sovi, koska `0.1 + 0.2` ei ole tasan `0.3`. Käytä rahalle `decimal`-tyyppiä.

### var

`var` antaa kääntäjän päätellä tyypin oikealta puolelta. `var age = 20` on silti `int`-muuttuja, ja tyyppi ei voi vaihtua myöhemmin.

```csharp
var age = 20;                  // int
var name = "Matti";            // string
var price = 7.50m;             // decimal
```

Alussa kirjoita tyyppi näkyviin. Silloin rivi kertoo lukijalle, onko kyseessä luku vai teksti, ja opit tyypit.

### null

`null` tarkoittaa "ei mitään": säilö on olemassa, mutta siinä ei ole arvoa. Se ei ole sama kuin luku `0` tai tyhjä teksti `""`.

`Console.ReadLine()` on määritelty palauttamaan `string?`. Kysymysmerkki kertoo, että arvo voi olla myös `null`. Siksi syötteen muuttuja kirjoitetaan usein muodossa `string? input`. Tavallinen Enter-painallus tuottaa tyhjän merkkijonon `""`, ei `null`-arvoa.

`int?` ja `HasValue` kuuluvat olio-ohjelmoinnin jälkeen. Niitä ei tarvita vielä.

## Yhteenveto

- Muuttujalla on tyyppi, nimi ja arvo: `int age = 20;`. Arvo voi vaihtua, tyyppi ei.
- `int` kokonaisluvuille, `decimal` rahalle (`m`-pääte, tulostus `:F2`), `string` tekstille, `bool` kyllä/ei-arvoille.
- `"200"` on tekstiä, `200` on luku. Syöte on aina tekstiä, kunnes muunnat sen.
- `const` on vakio: arvo annetaan kerran, nimi PascalCase.
- Nimet englanniksi ja camelCase. Nimen pitää kertoa, mitä säilö sisältää.
- Näkyvyysalue eli missä muuttujan nimeä saa käyttää: [Näkyvyysalueet](Scopes.md).

Seuraavaksi: [Konsolin syöte ja tulostus](Console-IO.md) · [Operaattorit](Operators.md) · [Ohjausrakenteet](Control-Structures.md)
