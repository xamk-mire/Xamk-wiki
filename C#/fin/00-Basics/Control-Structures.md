# Ohjausrakenteet (Control Structures)

Tietokone tekee vain sen, mitä sille kirjoitat. Se lukee ohjelmaa **ylhäältä alas**, yksi rivi kerrallaan.

Pelkkä rivien jono ei riitä oikeaan ohjelmaan. Tarvitset myös päätöksiä ja toistoa:

- **Jos** asiakas on lapsi, lippu maksaa vähemmän.
- Kysy ikää **uudestaan**, kunnes se on järkevä.
- Tulosta kuitti **yksi rivi per lippu**.

Näitä päätöksiä ja toistoja kutsutaan **ohjausrakenteiksi**. Ne kertovat, *mitä* tehdään, *milloin* ja *kuinka monta kertaa*.

Arjen esimerkki: aamu. Nouset sängystä (peräkkäin). Jos sataa, otat sateenvarjon (valinta). Harjaat hampaita, kunnes olet valmis (toisto). Ohjelma toimii samalla idealla.

**Vertailut ja `&&` / `||`:** [Operaattorit](Operators.md).

**Microsoft:** [Valinta](https://learn.microsoft.com/fi-fi/dotnet/csharp/language-reference/statements/selection-statements) · [Toisto](https://learn.microsoft.com/fi-fi/dotnet/csharp/language-reference/statements/iteration-statements)

## Kartta

| Termi | Yksi lause | Missä |
|-------|------------|--------|
| Peräkkäisyys | Rivit ajetaan järjestyksessä | [Peräkkäisyys](#peräkkäisyys--rivit-järjestyksessä) |
| Ehto | Kyllä/ei-kysymys, tulos on `true` tai `false` | [Mikä on ehto](#mikä-on-ehto) |
| `if` / `else` | Valitse yksi polku | [Valinta](#valinta--jos-näin-tee-näin) |
| `else if` | Useita vaihtoehtoja, ensimmäinen tosi voittaa | [Useita vaihtoehtoja](#useita-vaihtoehtoja-if--else-if--else) |
| `while` | Toista **niin kauan kuin** ehto on tosi | [while](#while--toista-niin-kauan-kuin) |
| `do-while` | Kuten `while`, mutta runko ajetaan **ainakin kerran** | [do-while](#do-while--tee-ensin-kysy-sitten) |
| `for` | Toista **tiedetty määrä** kertoja | [for](#for--tiedetty-määrä-kertoja) |
| `foreach` | Käy kokoelma läpi ilman järjestysnumeroa | [foreach](#foreach--käy-kokoelma-läpi) |
| Kertymä | Summa tai laskuri, joka kasvaa silmukassa | [Kertymämuuttuja](#kertymämuuttuja) |

Kolme perusrakennetta riittää lähes kaikkeen:

| Rakenne | Arjen kysymys | C#:ssa |
|---------|----------------|--------|
| Peräkkäisyys | Mitä teen seuraavaksi? | Rivit allekkain |
| Valinta | Teenkö tämän vai tuon? | `if`, `else`, `switch` |
| Toisto | Teenkö tämän uudestaan? | `while`, `for`, `foreach` |

## Peräkkäisyys — rivit järjestyksessä

Ilman valintaa ja silmukkaa ohjelma on kuin resepti ilman haarautumista: ensin rivi 1, sitten rivi 2, sitten rivi 3.

```csharp
Console.WriteLine("Tervetuloa.");
Console.Write("Anna ikäsi: ");
int age = Convert.ToInt32(Console.ReadLine());
Console.WriteLine($"Ikäsi on {age}.");
```

Tämä riittää, kun jokainen ajo tekee samat asiat samassa järjestyksessä. Heti kun vastaus riippuu iästä tai samaa työtä pitää tehdä monta kertaa, tarvitaan valinta tai toisto.

## Valinta — jos näin, tee näin

Valinta on risteys. Ohjelma kysyy kysymyksen. Vastaus on joko **kyllä** (`true`) tai **ei** (`false`). Sen mukaan valitaan, mitä rivejä ajetaan. Muita rivejä ei ajeta.

### Mikä on ehto?

**Ehto** on lauseke suluissa `if`-sanan jälkeen. C# laskee sen totuusarvoksi (`bool`).

```csharp
int age = 20;

bool isAdult = age >= 18;   // true, koska 20 on vähintään 18

if (age >= 18)              // sama kysymys suoraan if-lauseessa
{
    Console.WriteLine("Tervetuloa.");
}
```

Lue ehto ääneen suomeksi: *"Onko ikä vähintään 18?"*

| Kirjoitus | Ääneen |
|-----------|--------|
| `age < 12` | Onko ikä alle 12? |
| `age >= 18` | Onko ikä vähintään 18? |
| `answer == "k"` | Onko vastaus kirjain k? |
| `ticketCount > 0` | Onko lippuja enemmän kuin nolla? |

Vertailumerkit (`==`, `!=`, `<`, `>`, `<=`, `>=`) on selitetty sivulla [Operaattorit](Operators.md). Yksi yhtäläisyysmerkki (`=`) **sijoittaa** arvon. Kaksi (`==`) **vertaa**.

### if — tee jotain vain jos ehto täyttyy

```csharp
if (ehto)
{
    // Nämä rivit ajetaan vain, jos ehto on tosi
}
```

**Aaltosulkeet `{ }`** merkitsevät lohkon: "nämä rivit kuuluvat tähän `if`-lauseeseen". Sisennä lohkon rivit, jotta silmä näkee rakenteen.

```csharp
int age = 20;

if (age < 18)
{
    Console.WriteLine("Olet alaikäinen.");
}

Console.WriteLine("Kiitos käynnistä.");
```

Mitä tapahtuu, kun `age` on `20`:

1. C# kysyy: onko 20 pienempi kuin 18? **Ei** (`false`).
2. Lohkon riviä ei ajeta. "Olet alaikäinen." ei näy.
3. Suoritus jatkuu `if`-lohkon jälkeen. "Kiitos käynnistä." tulostuu aina.

Jos `age` on `15`, ehto on tosi. Molemmat viestit tulostuvat.

Kirjoita aluksi **aina** aaltosulkeet, vaikka lohkossa olisi vain yksi rivi. Ilman sulkeita `if` koskee vain seuraavaa riviä. Se on helppo unohtaa myöhemmin.

### if-else — joko tämä tai tuo

`else` on toinen ovi: "jos ehto ei täyttynyt, tee tämä sen sijaan".

```csharp
if (age >= 18)
{
    Console.WriteLine("Tervetuloa sisään.");
}
else
{
    Console.WriteLine("Valitettavasti et pääse sisään.");
}
```

Täsmälleen **yksi** haara ajetaan. Ikä 18 täyttää ehdon `>= 18` (suurempi **tai yhtä suuri**). Ikä 17 menee `else`-haaraan.

`else` ei tarvitse omaa ehtoa. Se tarkoittaa: "kaikki muut tapaukset".

### Useita vaihtoehtoja: if – else if – else

Kun vaihtoehtoja on enemmän kuin kaksi, ketjuta ne. Elokuvalipun hinta riippuu iästä: lapsi, aikuinen tai seniori.

```csharp
int age = 20;
decimal price;

if (age < 12)
{
    price = 7.50m;
}
else if (age < 65)
{
    price = 12.00m;
}
else
{
    price = 9.00m;
}

Console.WriteLine($"Lipun hinta: {price:F2} €");
```

C# käy ehdot **ylhäältä alas** ja pysähtyy ensimmäiseen, joka on tosi.

| Ikä | `age < 12` | `age < 65` | Tulos |
|-----|------------|------------|--------|
| 8 | tosi | ei tarkisteta | 7,50 € (lapsi) |
| 20 | epätosi | tosi | 12,00 € (aikuinen) |
| 70 | epätosi | epätosi | 9,00 € (seniori) |

Kun suoritus on `else if (age < 65)`-kohdassa, ensimmäinen ehto oli jo epätosi. Ikä ei siis ole alle 12. Siksi tämä haara tarkoittaa **12–64-vuotiaita**, vaikka koodissa lukee vain `< 65`.

`else` on turvaverkko: "mikään edellinen ehto ei täyttynyt". Tässä se tarkoittaa ikää 65 tai enemmän.

### Ehtojen järjestyksellä on väliä

Vain **yksi** haara ajetaan. Laita **kapein** ehto ensin.

```csharp
// Oikein: ensin lapsi, sitten muut alle 65-vuotiaat
if (age < 12) { /* lapsi */ }
else if (age < 65) { /* aikuinen */ }
else { /* seniori */ }

// Väärin: 8-vuotias täyttää jo age < 65
if (age < 65) { /* aikuinen — myös lapset päätyvät tänne */ }
else if (age < 12) { /* tänne ei koskaan päästä */ }
```

Toisessa versiossa lapsen haara on kuollutta koodia. 8 on pienempi kuin 65, joten ensimmäinen ehto nappaa lapsen.

### Testaa raja-arvot

Yhden merkin ero (`<` vai `<=`) vaihtaa luokan. Älä arvaa. Kokeile rajoja.

Esimerkin säännöillä:

| Ikä | Odotettu luokka | Miksi |
|-----|-----------------|-------|
| 11 | lapsi | 11 on alle 12 |
| 12 | aikuinen | 12 ei ole alle 12 |
| 64 | aikuinen | 64 on alle 65 |
| 65 | seniori | 65 ei ole alle 65 |

Jos sääntö olisi "alle 12-vuotias **tai tasan 12** on lapsi", ehto olisi `age <= 12`. Lue tehtävän lause tarkasti ennen kuin kirjoitat merkin.

### Yleisiä virheitä valinnassa

**1. Yksi yhtäläisyysmerkki vertailussa**

```csharp
// Väärä ajatus: "jos ikä on 18"
if (age = 18)   // tämä yrittää SIJOITTAA luvun 18 — C# ei käännä
```

`if` tarvitsee kyllä/ei-vastauksen. Vertailu kirjoitetaan `age == 18`.

**2. Puolipiste heti ehdon jälkeen**

```csharp
if (age < 12);   // tämä if ei tee mitään hyödyllistä
{
    Console.WriteLine("Lapsi");   // tämä rivi ajetaan AINA
}
```

Puolipiste päättää lauseen. Lohko ei enää kuulu `if`-lauseeseen.

**3. Puuttuva puoli yhdistetystä ehdosta**

```csharp
// Ei käänny:
if (age > 12 && < 65)

// Oikein: toista muuttujan nimi
if (age > 12 && age < 65)
```

**4. Merkkijonon TAI väärin**

```csharp
// Ei käänny tai ei tarkoita sitä mitä luulet:
if (answer == "k" || "e")

// Oikein: vertaa molemmat
if (answer == "k" || answer == "e")
```

Loogiset ehdot (`ikä < 0 || ikä > 130`) on selitetty sivulla [Operaattorit](Operators.md).

### switch — yksi muuttuja, monta tarkkaa arvoa

`if` sopii väleille (`age < 12`). `switch` sopii, kun vertaat **samaa** muuttujaa moniin **tarkkoihin** arvoihin: viikonpäivän numero, valikon valinta, alennuskoodi.

```csharp
int weekDay = 1;   // 1 = maanantai, 7 = sunnuntai

switch (weekDay)
{
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
        Console.WriteLine("Arkipäivä");
        break;
    case 6:
    case 7:
        Console.WriteLine("Viikonloppu");
        break;
    default:
        Console.WriteLine("Anna luku 1–7.");
        break;
}
```

| Osa | Merkitys |
|-----|----------|
| `case 1:` | "Jos arvo on tasan 1" |
| Useita `case`-rivejä peräkkäin | Sama toimenpide monelle arvolle (tyhjät `case`-rivit jakavat seuraavan koodin) |
| `break;` | Lopeta `switch` tähän. Jos haarassa on koodia ilman `break`-sanaa, C# ei käännä ohjelmaa |
| `default:` | Mikään `case` ei täsmännyt — vastaava kuin `else` |

Merkkijonoja voi käyttää samalla tavalla (`case "LEFFA10":`). Kirjainkoko ratkaisee: `"k"` ja `"K"` ovat eri arvoja.

Alussa `if` / `else if` riittää. Ota `switch` käyttöön, kun vaihtoehtoja on paljon ja jokainen on tarkka arvo.

### Switch-lauseke (C# 8+)

Lyhyempi kirjoitustapa, joka **palauttaa arvon**. Opettele ensin tavallinen `switch` tai `if`.

```csharp
string kind = weekDay switch
{
    1 or 2 or 3 or 4 or 5 => "Arkipäivä",
    6 or 7 => "Viikonloppu",
    _ => "Tuntematon päivä"
};
```

Alaviiva `_` on sama idea kuin `default`.

## Toisto — tee uudestaan

Silmukka toistaa samoja rivejä. Ilman silmukkaa joutuisit kopioimaan saman koodin monta kertaa. Kolme lippua olisi vielä hallittavissa. Kolmesataa ei.

**Kierros** on yksi läpikäynti silmukan rungosta. **Runko** on aaltosulkeiden sisällä olevat rivit.

### Milloin mitäkin silmukkaa?

| Silmukka | Milloin | Esimerkki |
|----------|---------|-----------|
| `while` | Toista **niin kauan kuin** ehto on tosi. Kierrosmäärää ei tiedetä etukäteen | Kysy ikä uudestaan, kunnes se on 0–130 |
| `do-while` | Kuten `while`, mutta runko ajetaan **ainakin kerran** | Palvele ainakin yksi asiakas, kysy jatkosta vasta sitten |
| `for` | Toista **tietty määrä** kertoja | Yksi kierros per lippu |
| `foreach` | Käy kokoelma läpi ilman järjestysnumeroa | Tulosta nimet listasta |

`for` vai `foreach`: jos tarvitset järjestysnumeron (`1. Margherita`) tai paikan taulukossa (`movies[i]`), käytä `for`. Jos tarvitset vain alkiot, `foreach` on selkeämpi. Kokoelmat: [Tietorakenteet](Data-Structures.md).

### while — toista niin kauan kuin

`while` tarkistaa ehdon **ennen** runkoa. Jos ehto on heti epätosi, runko ei aja kertaakaan.

```csharp
while (ehto)
{
    // Näitä rivejä toistetaan, kun ehto on tosi
}
```

Tyypillinen käyttö on huono syöte. Käyttäjä voi kirjoittaa iän 200. Ohjelman pitää kysyä uudestaan.

```csharp
Console.Write("Anna ikä (0–130): ");
int age = Convert.ToInt32(Console.ReadLine());

while (age < 0 || age > 130)
{
    Console.WriteLine("Ikä ei kelpaa.");
    Console.Write("Anna ikä (0–130): ");
    age = Convert.ToInt32(Console.ReadLine());
}

Console.WriteLine($"Ikä hyväksytty: {age}");
```

Lue ehto: *"niin kauan kuin ikä on alle 0 TAI yli 130"*. Kun käyttäjä antaa 20, ehto on epätosi ja silmukka loppuu.

Jos ensimmäinen syöte on jo 20, silmukkaan ei mennä lainkaan. Siksi `while` sopii tilanteeseen "toista vain jos korjattavaa on".

Väärä teksti (`"abc"`) kaataa ohjelman. Se on eri virhe kuin väärä lukuarvo. Tämän sivun esimerkit lukevat luvun `Convert.ToInt32`-kutsulla **lyhyyden vuoksi** — kun `TryParse` on opittu, käytä omissa ohjelmissasi `TryParse`-silmukkaa, joka ei kaadu vaan kysyy uudelleen. Katso [tyyppimuunnokset](Casting.md) ja [poikkeukset](Exception-Handling.md).

### Ikuinen silmukka

Silmukka ei lopu, jos ehdon käyttämä muuttuja **ei muutu** rungossa.

```csharp
int age = 200;

while (age < 0 || age > 130)
{
    Console.WriteLine("Ikä ei kelpaa.");
    // Puuttuu: age = Convert.ToInt32(Console.ReadLine());
}
```

`age` pysyy lukuna 200. Ehto on joka kerta tosi. Sama viesti tulvii ruudulle.

Pysäytä juokseva ohjelma konsoli-ikkunasta tai **Ctrl+C**. Tunnusmerkki: sama teksti toistuu eikä ohjelma kysy mitään uutta.

Korjaus: lue uusi arvo rungon sisällä, tai muuta ehtoa niin, että se voi muuttua epätodeksi.

### do-while — tee ensin, kysy sitten

`do-while` ajaa rungon **ensin** ja tarkistaa ehdon **jälkeen**. Runko ajetaan aina ainakin kerran.

```csharp
int number;
do
{
    Console.Write("Anna positiivinen luku: ");
    number = Convert.ToInt32(Console.ReadLine());
}
while (number <= 0);
```

Ensimmäistä lukua ei tarvitse lukea ennen silmukkaa. Kysymys on rungossa. Jos käyttäjä antaa `−3`, ehto `number <= 0` on tosi ja kysymys toistuu. Jos käyttäjä antaa `4`, silmukka loppuu.

```
while (ehto)              do
{                         {
    runko                     runko
}                         } while (ehto);

Ehto ENNEN runkoa         Ehto RUNGON JÄLKEEN
→ voi pyöriä 0 kertaa     → pyörii aina vähintään 1 kerran
```

Kassan jatkokysymys sopii `do-while`-rakenteeseen: ensimmäistä asiakasta ei kysytä ("palvellaanko ketään?"), vaan palvelu alkaa heti. Jatko kysytään vasta asiakkaan jälkeen.

Muuttuja, jota ehto käyttää, pitää esitellä **ennen** silmukkaa. Jos `string? continueAnswer` syntyy `do`-lohkon sisällä, `while`-ehto ei näe sitä. Syy on [näkyvyysalue](Scopes.md).

```csharp
string? continueAnswer;   // esittely täällä
do
{
    // ... palvele asiakas ...
    Console.Write("Uusi asiakas (k/e): ");
    continueAnswer = Console.ReadLine();
}
while (continueAnswer == "k");
```

### for — tiedetty määrä kertoja

Kun tiedät kierrosmäärän etukäteen, `for` kokoaa kolme asiaa yhdelle riville: mistä aloitetaan, kuinka kauan jatketaan ja miten laskuri muuttuu.

```csharp
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine($"Kierros {i}");
}
```

Tulostaa:

```
Kierros 1
Kierros 2
Kierros 3
Kierros 4
Kierros 5
```

Kolme osaa puolipisteillä erotettuna:

| Osa | Esimerkissä | Merkitys |
|-----|-------------|----------|
| Alustus | `int i = 1` | Luo laskurin. Ajetaan **kerran**, ennen ensimmäistä kierrosta |
| Ehto | `i <= 5` | Tarkistetaan **jokaisen kierroksen alussa**. Jos epätosi, silmukka loppuu |
| Kasvatus | `i++` | Ajetaan **kierroksen lopussa**. Tässä lisää yhden (`i` kasvaa: 1 → 2 → 3 …) |

Nimi `i` on perinteinen lyhyt laskuri (*index*). Voit käyttää selkeämpää nimeä, esimerkiksi `ticketNumber`.

```csharp
int ticketCount = 3;

for (int ticketNumber = 1; ticketNumber <= ticketCount; ticketNumber++)
{
    Console.WriteLine($"Käsitellään lippu {ticketNumber}/{ticketCount}");
}
```

Jos ehto on `i < 5` ja alustus `i = 0`, kierroksia on silti viisi (0, 1, 2, 3, 4). Taulukon paikat alkavat nollasta — siihen palataan [tietorakenteissa](Data-Structures.md). Lipun numeroinnissa ihmiselle luonteva on `1 … ticketCount`.

### foreach — käy kokoelma läpi

`foreach` antaa yhden alkion kerrallaan. Et tarvitse laskuria.

```csharp
string[] names = { "Matti", "Liisa", "Pekka" };

foreach (string name in names)
{
    Console.WriteLine(name);
}
```

Lue ääneen: *"jokaiselle nimelle listassa names"*. Ensimmäisellä kierroksella `name` on `"Matti"`, sitten `"Liisa"`, sitten `"Pekka"`.

```csharp
foreach (tyyppi alkio in kokoelma)
{
    // käytä muuttujaa alkio
}
```

`foreach` ei anna järjestysnumeroa. Jos tarvitset `1. Matti`, `2. Liisa`, käytä `for`-silmukkaa ja indeksiä.

### Kertymämuuttuja

**Kertymä** on muuttuja, joka kerää summaa tai määrää silmukan aikana: välisumma, päivän myynti, asiakkaiden luku.

Alustus on **aina silmukan ulkopuolella**. Sisällä vain lisätään.

```csharp
int ticketCount = 3;
decimal unitPrice = 12.00m;
decimal subtotal = 0m;              // nollaus ENNEN silmukkaa

for (int i = 1; i <= ticketCount; i++)
{
    subtotal += unitPrice;          // sama kuin: subtotal = subtotal + unitPrice
}

Console.WriteLine($"Välisumma: {subtotal:F2} €");   // 36,00
```

Kolme kierrosta: 0 → 12 → 24 → 36.

Jos `subtotal = 0m` on silmukan sisällä, edelliset kierrokset nollautuvat. Jäljelle jää vain viimeisen lipun hinta.

Sama kaava päivän myynnille: esittely ennen asiakassilmukkaa, `+=` sisällä, tulostus jälkeen.

`+=` ja `++` on selitetty sivulla [Operaattorit](Operators.md).

### break ja continue

Nämä keskeyttävät tavanomaisen kierroksen. Käytä harvoin. Selkeä ehto silmukan päällä on usein helpompi lukea.

**`break`** lopettaa **koko** silmukan heti. Suoritus jatkuu silmukan jälkeen.

```csharp
for (int i = 0; i < 10; i++)
{
    if (i == 5)
    {
        break;
    }

    Console.WriteLine(i);
}
// Tulostaa: 0, 1, 2, 3, 4
```

Kun `i` on 5, `break` hyppää pois. Lukua 5 ei tulosteta, eikä silmukka jatka lukuihin 6–9.

**`continue`** lopettaa **vain tämän kierroksen**. Seuraava kierros alkaa normaalisti.

```csharp
for (int i = 0; i < 10; i++)
{
    if (i % 2 == 0)
    {
        continue;   // parillinen: älä tulosta, siirry seuraavaan i:hin
    }

    Console.WriteLine(i);
}
// Tulostaa: 1, 3, 5, 7, 9
```

`i % 2 == 0` tarkoittaa: jakojäännös kahdella on nolla, eli luku on parillinen. Katso `%` sivulta [Operaattorit](Operators.md).

### Sisäkkäiset silmukat

Silmukan sisällä voi olla toinen silmukka. Ulompi kierros odottaa, kunnes sisempi on käynyt omat kierroksensa loppuun.

Ajattele teatterin salia: kolme riviä, neljä paikkaa rivillä.

```csharp
for (int row = 1; row <= 3; row++)
{
    for (int seat = 1; seat <= 4; seat++)
    {
        Console.Write($"R{row}P{seat}  ");
    }

    Console.WriteLine();   // rivinvaihto, kun rivin paikat on tulostettu
}
```

Tulostaa:

```
R1P1  R1P2  R1P3  R1P4
R2P1  R2P2  R2P3  R2P4
R3P1  R3P2  R3P3  R3P4
```

Kun `row` on 1, sisempi silmukka käy paikat 1–4. Vasta sitten `row` muuttuu 2:ksi. Yhteensä 3 × 4 = 12 tulostusta.

Kertotaulu rakennetaan samalla idealla: ulompi luku, sisempi luku, tulo keskellä.

## Ternary-operaattori — lyhyt if-else

Yksi rivi, joka valitsee arvon. Lue: *"jos ehto, niin tämä, muuten tuo"*.

```csharp
string message = age >= 18 ? "Aikuinen" : "Alaikäinen";
```

Sama ilman lyhennystä:

```csharp
string message;
if (age >= 18)
{
    message = "Aikuinen";
}
else
{
    message = "Alaikäinen";
}
```

Käytä ternaryä vain lyhyeen, selkeään valintaan. Ketjuta mieluummin tavallisia `if`-lauseita. Lukijan pitää ymmärtää rivi vilkaisulla.

## Yhteenveto

- Ohjelma etenee ylhäältä alas. **Valinta** haarauttaa. **Silmukka** toistaa.
- Ehto on kyllä/ei-kysymys. Tulos on `true` tai `false`.
- `if` / `else if` / `else`: vain **yksi** haara. Kapein ehto ensin. Testaa raja-arvot (11, 12, 64, 65).
- `==` vertaa, `=` sijoittaa. Älä laita puolipistettä `if (ehto)`-rivin perään.
- `while`: ehto ensin, voi pyöriä nolla kertaa — syötteen korjaus.
- `do-while`: runko ensin, ainakin yksi kerta — asiakassilmukka. Esittele ehdon muuttuja ennen silmukkaa.
- `for`: tiedetty kierrosmäärä — liput, numerointi.
- `foreach`: kokoelma ilman indeksiä.
- Kertymä (`+=`) nollataan **silmukan ulkopuolella**.
- Ikuinen silmukka: ehdon muuttuja ei muutu. Tunnista tulvasta ja korjaa.

Seuraavaksi: [Operaattorit](Operators.md) · [Debuggaus](Debug.md) · [Tietorakenteet](Data-Structures.md)
