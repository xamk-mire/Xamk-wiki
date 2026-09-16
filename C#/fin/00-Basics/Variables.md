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
| `int` | Kokonaisluku | Ikä, lippumäärä |
| `decimal` | Rahasumma, tarkka desimaali | Hinta, välisumma — aina `m`-pääte |
| `string` | Teksti | Nimi, alennuskoodi, syöte |
| `bool` | Kyllä tai ei | `isStudent`, ehdon tulos |
| `const` | Arvo, joka ei muutu | `ChildPrice = 7.50m` |
| `var` | Tyyppi päätellään oikealta | `var age = 20` → silti `int` |
| `null` | "Ei mitään" | Tyhjä viittaus, ei luku nolla |

Syöte konsolista on aina `string`, kunnes muunnat sen — [tyyppimuunnokset](Casting.md). Laskumerkit: [operaattorit](Operators.md).

## Muuttujatyypit C#-kielessä

### string

[Virallinen dokumentaatio - String Class (System) | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/strings/)

`string` on tietotyyppi, jota käytetään merkkijonojen tallentamiseen ja käsittelemiseen. Merkkijono on yksinkertaisesti tekstiä, eli se voi sisältää sanoja, lauseita, numeroita tai muita merkkejä.

#### Esimerkki

```csharp
string tervehdys = "Hei maailma!";
Console.WriteLine(tervehdys);
```

Tässä esimerkissä `tervehdys` on `string`-tyyppinen muuttuja, ja siihen on tallennettu teksti "Hei maailma!". Hipsut `" "` kertovat, että kyseessä on merkkijono.

#### Merkkijonojen yhdistäminen

```csharp
string etuNimi = "Matti";
string sukuNimi = "Meikäläinen";
string kokoNimi = etuNimi + " " + sukuNimi;
Console.WriteLine(kokoNimi); // Tulostaa: Matti Meikäläinen
```

#### Merkkijonon pituus

```csharp
string sana = "Ohjelmointi";
Console.WriteLine(sana.Length); // Tulostaa: 11
```

#### Merkkijonojen vertailu

Merkkijonoja vertaillaan, jotta voidaan tarkistaa ovatko kaksi tekstiä samat – esimerkiksi käyttäjän syöttämä salasana, hakusana, tiedostonimi tai tietokannan avain täsmää tallennettuun arvoon.

**Kirjainkoko.** `"LEFFA10"` ja `"leffa10"` ovat eri merkkijonoja. Yksi tapa tehdä vertailu kirjainkoosta riippumattomaksi:

```csharp
if (code.ToUpper() == "LEFFA10")
{
    // alennus
}
```

`ToUpper()` / `ToLower()` luo uuden merkkijonon (string on *immutable*). Ammattikoodissa kirjainkoosta riippumaton vertailu tehdään usein näin:

```csharp
if (a.Equals(b, StringComparison.OrdinalIgnoreCase)) { /* ... */ }
```

`OrdinalIgnoreCase` ei riipu käyttöjärjestelmän kielestä (esim. turkin I/İ). Tunnisteille ja koodeille se on turvallisempi kuin `ToLower()`. Alussa `.ToUpper()` riittää.

#### Merkkijonon muokkaaminen

```csharp
string lause = "Hei maailma";
Console.WriteLine(lause.ToUpper());   // HEI MAAILMA
Console.WriteLine(lause.ToLower());   // hei maailma
Console.WriteLine(lause.Substring(4)); // maailma
```

#### Merkkijonojen tulostustavat

**1. String interpolation (suositeltu tapa)**

```csharp
string nimi = "Matti";
int ika = 30;

Console.WriteLine($"Hei, nimeni on {nimi} ja olen {ika} vuotta vanha.");
```

**2. String.Format**

```csharp
string tulos = string.Format("Hei, nimeni on {0} ja olen {1} vuotta vanha.", nimi, ika);
Console.WriteLine(tulos);
```

**3. Placeholderit Console.WriteLine:ssa**

```csharp
Console.WriteLine("Hei, nimeni on {0} ja olen {1} vuotta vanha.", nimi, ika);
```

**4. Merkkijonojen yhdistäminen**

```csharp
Console.WriteLine("Hei, nimeni on " + nimi + " ja olen " + ika + " vuotta vanha.");
```

#### Merkkijonon muuntaminen eri tietotyypeiksi (parsiminen)

Tietokoneessa kaikki mitä luetaan käyttäjältä tai vaikka tiedostosta, tulee **tekstinä** eli `string`-muodossa. Jos haluat tehdä laskutoimituksia, päivämäärien käsittelyä tai desimaalilaskentaa, teksti pitää muuttaa **oikeaan tietotyyppiin**. Tätä sanotaan *parsimiseksi* (engl. *parsing*).

**1: string → int (kokonaisluku)**

```csharp
string teksti = "123";
int luku = int.Parse(teksti);
int tulos = luku + 10;
Console.WriteLine(tulos); // 133
```

Selitys:
- `"123"` on teksti (merkkijono), vaikka se näyttää numerolta.
- `int.Parse("123")` muuttaa sen oikeaksi kokonaisluvuksi (`int`).
- Nyt voidaan laskea: 123 + 10 = 133.

Jos käyttäjä syöttäisi jotain muuta kuin numeroita (esim. `"abc"`), ohjelma kaatuisi, koska sitä ei voi muuttaa luvuksi.

**2: string → int turvallisesti TryParse (Tätä kannattaa käyttää lähtökohtaisesti!)**

```csharp
string syote = Console.ReadLine();
if (int.TryParse(syote, out int tulos))
{
    Console.WriteLine($"Luku on: {tulos}");
}
else
{
    Console.WriteLine("Syöte ei ole kelvollinen kokonaisluku.");
}
```

Selitys:
- `TryParse` yrittää muuntaa tekstin luvuksi.
- Jos onnistuu, tulos tallentuu `tulos`-muuttujaan ja ohjelma jatkuu normaalisti.
- Jos epäonnistuu (esim. `"kissa"`), ohjelma **ei kaadu**, vaan menee `else`-haaraan.

Tätä kannattaa käyttää aina, kun syöte tulee käyttäjältä, koska käyttäjä voi kirjoittaa mitä tahansa.

Aluksi syöte muunnetaan usein `Convert.ToInt32(Console.ReadLine())` -kutsulla. Se on yksinkertaisempi, mutta kaatuu väärästä tekstistä (`FormatException`). `TryParse` estää kaatumisen. Molemmat ovat oikein — tiedä ero.

**3: string → double (desimaaliluku)**

```csharp
string teksti = "23.5";
double luku = double.Parse(teksti);
Console.WriteLine(luku); // 23.5
```

Selitys:
- `double.Parse` muuttaa tekstin liukuluvuksi (desimaaliluku).
- Suomessa desimaalierotin on **pilkku (,)**, mutta monessa maassa se on **piste (.)**.
- Jos ohjelma toimii väärällä asetuksella, se voi aiheuttaa virheen.
- Lopulta doublella ja muilla numerotyypeillä on samat parsimismetodit, kuten int:llä, eli Parse ja TryParse.

**4: string → DateTime (päivämäärä)**

```csharp
string paivamaara = "2024-01-15";
DateTime pvm = DateTime.Parse(paivamaara);
Console.WriteLine(pvm);
```

Selitys:
- `DateTime.Parse` muuttaa tekstin päivämääräksi.

**Huomio!** `string` on C#:ssa *immutable* (eli muuttumaton). Kun muokkaat merkkijonoa, C# luo aina uuden merkkijonon eikä muuta alkuperäistä.

---

### int

[Virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/integral-numeric-types)

`int` on tietotyyppi, jota käytetään tallentamaan kokonaislukuja, eli lukuja ilman desimaaleja. `int` tulee sanasta "integer", joka tarkoittaa kokonaislukua.

#### Esimerkki

```csharp
int ika = 25; // ika on int-tyyppinen muuttuja
Console.WriteLine(ika); // Tulostaa 25
```

#### Muutamia keskeisiä asioita int-tyypistä

**1. Arvon rajat**: `int` voi tallentaa arvoja välillä -2,147,483,648 ja 2,147,483,647, koska se on 32-bittinen kokonaisluku.

**2. Yksinkertaiset laskutoimitukset**: `int`-muuttujilla voi suorittaa peruslaskuja:

```csharp
int a = 10;
int b = 3;

int summa = a + b;       // 13
int erotus = a - b;      // 7
int tulo = a * b;        // 30
int jako = a / b;        // 3 (kokonaislukuosuus!, jos haluat että luvussa on desimaaleja käytä double/decimal muuttujaa)
int jakoJäännös = a % b; // 1

Console.WriteLine($"Summa: {summa}, Erotus: {erotus}, Tulo: {tulo}");
Console.WriteLine($"Jakolasku: {jako}, Jakojäännös: {jakoJäännös}");
```

**3. Kokonaislukuosuus ja jakojäännös**: Kun jaetaan kokonaislukuja, tuloksena saadaan vain kokonaisluku. Jakojäännöksen saa `%`-operaattorilla.

```csharp
int x = 17;
int y = 5;

Console.WriteLine(x / y); // 3
Console.WriteLine(x % y); // 2
```

**4. Käyttö ohjelmoinnissa**: `int`-tyyppi on yleisin muuttujaohjelmoinnissa. Esimerkiksi laskureissa ja silmukoissa käytetään usein int-muuttujia:

```csharp
for (int i = 1; i <= 5; i++)
{
    Console.WriteLine($"Kierros {i}");
}
```

**5. Muunnokset**: Jos haluat muuttaa kokonaisluvun desimaaliluvuksi, voit muuntaa sen `double`-tyypiksi:

```csharp
int kokonaisluku = 7;
double desimaali = (double)kokonaisluku / 2;
Console.WriteLine(desimaali); // 3.5
```

**6. Inkrementti ja dekrementti**: Int-muuttujan arvoa voi kasvattaa tai vähentää yhdellä käyttämällä `++` ja `--`.

```csharp
int luku = 10;
luku++; // nyt 11
luku--; // takaisin 10
```

**7. Oletusarvo**: Jos luot int-muuttujan ilman arvoa, sen oletusarvo on 0 (kun se on olion kenttä).

```csharp
int oletus;
Console.WriteLine(default(int)); // 0
```

#### Yhteenveto

`int` on erittäin yleinen tietotyyppi, jota käytetään kokonaislukujen käsittelyyn. Sen avulla voidaan tehdä peruslaskuja, hallita silmukoita, laskea summia ja monia muita toimintoja.

---

### double

`double` on tietotyyppi, jota käytetään tallentamaan desimaalilukuja, eli lukuja, joissa voi olla murtolukuosa. Se on nimensä mukaisesti lyhenne sanasta "double precision floating point number", mikä viittaa sen kykyyn tallentaa lukuja suuremmalla tarkkuudella kuin esimerkiksi `float`-tyyppi.

#### Esimerkki

```csharp
double lampotila = 23.5;
Console.WriteLine(lampotila); // 23.5
```

Tässä esimerkissä `lampotila` on `double`-tyyppinen muuttuja, ja siihen on tallennettu arvo 23.5.

#### Muutamia keskeisiä asioita double-tyypistä

**1. Arvon rajat ja tarkkuus**: `double` voi tallentaa hyvin suuria tai hyvin pieniä lukuja, ja sen tarkkuus on 15–16 desimaalin tarkkuudella. Se voi tallentaa arvoja välillä noin ±5.0 × 10^−324 ja ±1.7 × 10^308.

**2. Laskutoimitukset**: `double`-tyyppisillä muuttujilla voit suorittaa erilaisia laskutoimituksia, kuten yhteenlaskua, vähennyslaskua, kertolaskua ja jakolaskua aivan kuten `int`-muuttujilla, mutta se tukee myös murtolukuja.

```csharp
double a = 10.5;
double b = 3.2;

double summa = a + b;       // 13.7
double erotus = a - b;      // 7.3
double tulo = a * b;        // 33.6
double jako = a / b;        // 3.28125

Console.WriteLine($"Summa: {summa}, Erotus: {erotus}, Tulo: {tulo}, Jako: {jako}");
```

**3. Tarkkuus ja virheet**: Koska `double` on liukulukutyyppi, se ei aina voi tallentaa desimaalilukuja täydellisen tarkasti. Tämä voi johtaa pieniin pyöristysvirheisiin, erityisesti kun käsitellään hyvin pieniä tai hyvin suuria lukuja.

**Älä käytä `double`-tyyppiä rahalle.** `0.1 + 0.2` ei ole tietokoneessa täsmälleen `0.3`. Lipun hinnassa, kuitissa ja päivän myynnissä käytetään aina `decimal`-tyyppiä — katso seuraava osio.

**4. Muunnokset**: Joskus saatat haluta muuntaa `double`-arvon esimerkiksi `int`-arvoksi. Tämä onnistuu käyttämällä tyyppimuunnosta, mutta huomaa, että tällöin desimaaliosa katkaistaan pois.

```csharp
double desimaali = 3.7;
int kokonaisluku = (int)desimaali;
Console.WriteLine(kokonaisluku); // 3 (desimaaliosa katkaistu)
```

**5. Oletusarvo**: Jos luot `double`-muuttujan ilman, että annat sille aluksi arvoa, sen oletusarvo on 0.0.

```csharp
double oletus;
Console.WriteLine(default(double)); // 0.0
```

**6. Käyttö ohjelmoinnissa**: `double` sopii mittauksiin, lämpötiloihin, koordinaatteihin ja tieteellisiin laskuihin. **Rahalaskut kuuluvat `decimal`-tyypille**, ei `double`:lle.

#### Yhteenveto

`double` on liukuluku desimaaleille, kun pieni pyöristysvirhe ei haittaa. Rahaan, hintoihin ja kuitteihin käytä `decimal`.

---

### decimal — raha

[Virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/floating-point-numeric-types)

`decimal` on desimaaliluku, joka on suunniteltu **tarkkaan** laskentaan. Rahat (`hinta`, `välisumma`, `alennus`, `myynti`) kannattaa pitää `decimal`-tyyppinä.

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

**Miksi ei `double`?** Liukuluku tallentaa luvun kaksikantaisena approksimaationa. Sentit voivat "valua":

```csharp
double a = 0.1;
double b = 0.2;
Console.WriteLine(a + b);          // 0.30000000000000004
Console.WriteLine(0.1m + 0.2m);    // 0.3
```

Yhdessä laskussa virhe on mitätön; sadassa kuitissa se kertyy. Siksi nyrkkisääntö: **raha = `decimal`**.

Vakiohinnat kannattaa merkitä `const`-sanalla, kun arvo ei muutu ohjelman aikana:

```csharp
const decimal ChildPrice = 7.50m;
```

---

### bool (Boolean)

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/bool)

C#-ohjelmointikielessä `boolean` (tai lyhyemmin `bool`) on tietotyyppi, joka voi saada kaksi arvoa: `true` (tosi) tai `false` (epätosi). Tätä tietotyyppiä käytetään yleensä ehtojen arvioinnissa ja logiikan hallinnassa.

#### Esimerkki bool-muuttujan käytöstä

```csharp
bool onkoTosi = true;

if (onkoTosi)
{
    Console.WriteLine("Muuttuja on tosi.");
}
else
{
    Console.WriteLine("Muuttuja on epätosi.");
}
```

Tässä esimerkissä, koska `onkoTosi`-muuttujan arvo on `true`, ohjelma tulostaa "Muuttuja on tosi."

#### Boolean-arvoja tuotetaan usein vertailuoperaatioiden yhteydessä

Boolean-arvoja tuotetaan usein vertailuoperaatioiden yhteydessä, kuten:
- `==` (yhtä suuri kuin)
- `!=` (ei yhtä suuri kuin)
- `<` (pienempi kuin)
- `>` (suurempi kuin)
- `<=` (pienempi tai yhtä suuri kuin)
- `>=` (suurempi tai yhtä suuri kuin)

#### Esimerkkejä

```csharp
int ika = 20;
bool onTaysiIkanen = ika >= 18;
bool onAlaIkanen = ika < 18;

Console.WriteLine($"On täysi-ikäinen: {onTaysiIkanen}"); // true
Console.WriteLine($"On alaikäinen: {onAlaIkanen}"); // false

// Loogiset operaattorit
bool ehto1 = true;
bool ehto2 = false;

bool ja = ehto1 && ehto2;  // false (molempien pitää olla true)
bool tai = ehto1 || ehto2; // true (jompikumpi riittää)
bool ei = !ehto1;          // false (kääntää arvon)
```

---

### null

#### Mitä tarkoittaa null?

Vertaus reaalimaailmasta voi auttaa hahmottamaan `null`-konseptia.

Kuvittele, että sinulla on autonavainnipussa paikka talosi avaimelle.

1. **Avain paikallaan**: Tämä vastaisi tilannetta, jossa muuttujalla on viittaus johonkin arvoon. Talosi avaimenippusi paikassa on konkreettinen avain.
2. **Ei avainta**: Jos avainnipussa ei ole avainta talosi avainpaikassa, se vastaa `null`-viittausta. Se tarkoittaa, että olet tietoinen avaimen pitämisestä tuossa paikassa, mutta juuri nyt siinä ei ole avainta. Jos yrittäisit avata ovea tuolla "ei olemassa olevalla" avaimella, kohtaisit ongelman - vastaavasti kuin jos yrittäisit käyttää `null`-viittausta koodissa.
3. **Tässä kontekstissa**:
   - Avain = todellinen olio tai arvo koodissa.
   - Avaimen paikka = muuttuja tai viittaustyyppi koodissa.
   - Ei avainta = `null` viittaus.

Reaalimaailmassa `null`-tilanne voi vastata monia asioita: tyhjä laatikko, postilaatikko ilman postia, kirjahylly ilman kirjoja jne. Se kuvaa tilaa, jossa odotettu asia tai esine puuttuu.

#### null C#-ohjelmointikielessä

C#-ohjelmointikielessä "null" tarkoittaa arvoa tai viittausta, joka ei osoita mihinkään. Se on tyypillisesti tapa ilmaista, että muuttuja ei osoita mihinkään olemassa olevaan objektiin tai muistialueeseen.

#### Esimerkkejä

**1. Referenssityypit**: Muuttujan (kuten luokan instanssin) viittaus voi olla `null`, mikä tarkoittaa, että se ei viittaa mihinkään olion esiintymään.

```csharp
string teksti = null;

if (teksti == null)
{
    Console.WriteLine("Teksti on null");
}
else
{
    Console.WriteLine(teksti);
}
```

**2. Nullable-arvotyypit**: C# tukee nullable-versioita arvotyypeistä, kuten int, float, ja bool. Tämä tarkoittaa, että voit asettaa näiden tyyppien muuttujia arvoon `null` erityisen syntaksin avulla laittamalla muuttujan perään **?**

```csharp
int? numero = null; // nullable int

if (numero.HasValue)
{
    Console.WriteLine($"Numero on: {numero.Value}");
}
else
{
    Console.WriteLine("Numero on null");
}

// Tai lyhyemmin:
int? ika = null;
Console.WriteLine(ika ?? 0); // Jos ika on null, käytetään 0
```

**3. Tyypillinen käyttö**: `null`-arvoa käytetään usein ilmaisemaan, että jotain ei ole määritelty tai että jokin ei ole saatavilla. Esimerkiksi, jos yrität hakea tietokannasta tietoa, joka ei ole olemassa, saattaisit palauttaa `null`.

On tärkeää huomata, että arvotyypeillä (kuten int, float, bool) ei ole oletusarvoisesti `null`-arvoa, ellei niitä tehdä nullable-tyyppiseksi. Tämän takia `int?` voi olla `null`, mutta pelkkä `int` ei voi.

---

### var

`var` on avainsana, jota käytetään muuttujan tyypin automaattiseen päätteleminen sen perusteella, mikä arvo sille annetaan. Tämä tarkoittaa, että kun käytät `var`-avainsanaa, sinun ei tarvitse määrittää tarkkaa tietotyyppiä, vaan C# tekee sen puolestasi. Tämä voi tehdä koodin kirjoittamisesta hieman nopeampaa ja luettavampaa tietyissä tilanteissa.

#### Esimerkki

```csharp
var ika = 25; // ika on automaattisesti tyypiltään int
Console.WriteLine(ika.GetType()); // System.Int32
```

Tässä esimerkissä `ikä`-muuttuja on automaattisesti tyypiltään `int`, koska sille annettu arvo 25 on kokonaisluku.

#### Muutamia keskeisiä asioita var-avainsanasta

**1. Tyypin päättely**: C# päättää muuttujan tyypin automaattisesti annettavan arvon perusteella. Esimerkiksi, jos annat muuttujalle merkkijonon, siitä tulee `string`, ja jos annat desimaaliluvun, siitä tulee `double`.

```csharp
var nimi = "Matti";        // string
var ika = 25;             // int
var hinta = 19.99;        // double
var onkoAktiivinen = true; // bool
```

**2. Koodin luettavuus**: `var` voi tehdä koodista helpommin luettavaa, erityisesti kun tyyppi on ilmeinen tai kun käytetään monimutkaisia tyyppinimiä.

```csharp
// Ilman var - pitkä tyyppinimi
Dictionary<string, List<int>> data = new Dictionary<string, List<int>>();

// Var-avainsanalla - lyhyempi
var data = new Dictionary<string, List<int>>();
```

**3. Rajoitukset**: `var`-avainsanaa voi käyttää vain, kun muuttuja alustetaan samalla rivillä, eli sille annetaan heti arvo. Ilman arvoa C# ei pysty päättelemään tyyppiä.

```csharp
// ✅ HYVÄ
var luku = 10;

// ❌ HUONO - ei voi käyttää var ilman arvoa
var luku; // Virhe!
luku = 10;
```

**4. Yleiskäyttöisyys**: Vaikka `var` helpottaa tiettyjen asioiden kirjoittamista, sen käyttö voi joskus tehdä koodista vähemmän selkeää, jos tyypin päätteleminen ei ole ilmeistä koodin lukijalle. Tällaisissa tilanteissa on parempi käyttää suoraan tietotyyppiä.

```csharp
// ✅ HYVÄ - tyyppi on ilmeinen
var nimi = "Matti";
var ika = 25;

// ❌ HUONO - tyyppi ei ole selvä
var tulos = ProcessData(); // Mikä tyyppi?
```

**5. Käyttö tapauksissa, joissa tarkka tyyppi ei ole heti ilmeinen**: `var` voi olla erityisen hyödyllinen silloin, kun käytät pitkiä tyyppinimiä tai kun tarkka tyyppi ei ole yhtä tärkeä koodin toiminnan ymmärtämisen kannalta.

```csharp
// Pitkä tyyppinimi - var tekee koodista luettavampaa
var kayttajat = new List<Dictionary<string, object>>();

// Sama ilman var - vähemmän luettavaa
List<Dictionary<string, object>> kayttajat = new List<Dictionary<string, object>>();
```

#### Yhteenveto

`var` on kätevä työkalu, joka voi tehdä koodin kirjoittamisesta ja lukemisesta sujuvampaa, kun sitä käytetään oikein. Se on kuitenkin hyvä käyttää harkiten, jotta koodin luettavuus ja ymmärrettävyys säilyy.

---

## Muuttujan määrittely

### Perussyntaksi

```csharp
tyyppi muuttujanNimi = arvo;
```

### Esimerkkejä

```csharp
// Kokonaisluku
int age = 25;

// Desimaaliluku
double price = 19.99;
decimal salary = 5000.50m;

// Merkkijono
string name = "Matti";

// Totuusarvo
bool isActive = true;

// Merkki
char grade = 'A';
```

## Muuttujan nimeäminen

### Säännöt

1. Nimi voi alkaa kirjaimella tai alaviivalla (`_`)
2. Nimi voi sisältää kirjaimia, numeroita ja alaviivoja
3. Nimi ei voi olla varattu sana (esim. `int`, `class`, `void`)
4. Nimi on kirjainkokoherkkä (`age` ≠ `Age`)

```csharp
// ✅ HYVÄ
int age = 25;
string firstName = "Matti";
bool isActive = true;
int _count = 0;

// ❌ HUONO
int 2age = 25;        // Ei voi alkaa numerolla
string first-name = "Matti";  // Ei voi sisältää viivaa
int class = 5;        // Varattu sana
```

### Nimeämiskäytännöt

- **camelCase**: Paikalliset muuttujat ja private-kentät
- **PascalCase**: Public-kentät ja propertyt

```csharp
public class Person
{
    // Private field - camelCase
    private string firstName;
    private int age;
    
    // Public property - PascalCase
    public string FirstName { get; set; }
    public int Age { get; set; }
    
    public void DisplayInfo()
    {
        // Local variable - camelCase
        string fullName = $"{FirstName} {Age}";
        Console.WriteLine(fullName);
    }
}
```

## Muuttujan käyttö

### Arvon lukeminen

```csharp
int x = 10;
int y = 20;
int sum = x + y;  // Lukee x:n ja y:n arvot
Console.WriteLine(sum);  // Tulostaa: 30
```

### Arvon muuttaminen

```csharp
int count = 0;
count = 5;        // Muuttaa arvon
count = count + 1; // Kasvattaa arvoa yhdellä
count++;          // Sama kuin yllä (lyhennysmerkintä)
```

## Vakiot (Constants)

Vakio on muuttuja, jonka arvoa ei voi muuttaa:

```csharp
// const - kääntöaikainen vakio
const int MaxRetryAttempts = 3;
const double Pi = 3.14159;
const string AppName = "MyApp";

// readonly - suoritusaikainen vakio (vain luokassa)
public class Config
{
    public readonly string ConnectionString;
    
    public Config()
    {
        ConnectionString = "Server=localhost;"; // Asetetaan konstruktorissa
    }
}
```

## Muuttujien laajuus (Scope)

Muuttujan laajuus määrittää, missä muuttujaa voidaan käyttää:

```csharp
public class Example
{
    // Luokan taso - näkyy koko luokassa
    private int classLevel = 10;
    
    public void Method1()
    {
        // Metodin taso - näkyy vain metodissa
        int methodLevel = 20;
        
        if (true)
        {
            // Lohkon taso - näkyy vain lohkossa
            int blockLevel = 30;
            
            // Voimme käyttää kaikkia
            Console.WriteLine(classLevel);   // OK
            Console.WriteLine(methodLevel);  // OK
            Console.WriteLine(blockLevel);   // OK
        }
        
        // blockLevel ei ole näkyvissä täällä
        // Console.WriteLine(blockLevel); // ❌ Virhe!
    }
}
```

## Yhteenveto

- Muuttujat tallentavat dataa
- Tyyppi määrittää, millaista dataa muuttuja voi sisältää
- Nimeä muuttujat selkeästi ja noudata käytäntöjä
- Käytä `var`-avainsanaa kun tyyppi on ilmeinen
- Vakiot (`const`) eivät voi muuttua
- `string` on immutable - muutokset luovat uuden merkkijonon
- Rahalaskut: aina `decimal` ja `m`-pääte, tulostus `{summa:F2}`
- Syöte: `Convert.ToInt32` on yksinkertainen; `TryParse` ei kaada ohjelmaa väärästä tekstistä

Seuraavaksi: [Konsolin syöte ja tulostus](Console-IO.md) · [Operaattorit](Operators.md) · [Ohjausrakenteet](Control-Structures.md)
