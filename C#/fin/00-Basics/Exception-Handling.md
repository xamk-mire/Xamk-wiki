# Poikkeusten käsittely (Exception Handling)

**Poikkeus** on virhe kesken ajon. Ohjelma kääntyi. Sitten tapahtui jotain, jota koodi ei osannut hoitaa: käyttäjä kirjoitti `abc` iäksi, tiedostoa ei ole, taulukosta haettiin paikkaa jota ei ole.

Jos poikkeusta ei käsitellä, ohjelma **kaatuu**. Kaatuminen ei riko konetta, Visual Studiota eikä koodia. Ohjelma lopettaa ja kertoo miksi.

Ensimmäinen taito ei ole `try-catch`. Ensimmäinen taito on **lukea ilmoitus**.

**Microsoft:** [Exceptions](https://learn.microsoft.com/fi-fi/dotnet/csharp/fundamentals/exceptions/)

## Kartta

| Asia | Yksi lause |
|------|------------|
| Virheilmoitus | Tyyppi + viesti + **oman koodin rivi** |
| Estä etukäteen | Tarkista syöte `TryParse`-metodilla, `if`, `ContainsKey`, `Exists` |
| `try` / `catch` | Yritä, ja jos kaatuu, hoida virhe itse — loput `try`-rivit jäävät ajamatta |
| Monta `catch`-lohkoa | Tarkin tyyppi ensin, `catch (Exception ex)` viimeisenä |
| Sääntö | **Tarkista se, minkä voit — ota kiinni se, mitä et voi** |
| `finally` | Ajetaan aina — myöhemmin, tiedostojen kanssa |
| Tyhjä `catch` | Piilottaa vian — älä tee näin |

## Virheilmoituksen lukeminen

```
Unhandled exception. System.FormatException: The input string 'abc' was not in a correct format.
   at System.Convert.ToInt32(String value)
   at Program.<Main>$(String[] args) in C:\...\MovieTickets\Program.cs:line 10
```

| Osa | Esimerkissä | Mitä kertoo |
|-----|-------------|-------------|
| **Tyyppi** | `System.FormatException` | Vian laatu: "muoto on väärä" |
| **Viesti** | `The input string 'abc' was not in a correct format.` | Mikä syöte epäonnistui |
| **Rivi** | `Program.cs:line 10` | **Oman koodisi** rivi |

Keskimmäiset `System.Number...`-rivit ovat .NET:n sisäisiä. Hyppää niiden yli. Etsi **oman tiedoston** nimi.

Sama pino näkyy debuggerin Call Stack -ikkunassa. F5:n aikana Visual Studio avaa Exception Helper -ikkunan suoraan riville — [debuggaus](Debug.md#poikkeus-debuggerissa).

### Aloittelijan yleisimmät poikkeukset

| Poikkeus | Tyypillinen syy |
|----------|-----------------|
| `FormatException` | `"abc"` annettiin `Convert.ToInt32`-metodille |
| `OverflowException` | Luku ei mahdu `int`-tyyppiin (max n. 2,1 miljardia) |
| `IndexOutOfRangeException` | Taulukosta haettiin indeksiä, jota ei ole (`movies[4]` neljän alkion taulukossa) |
| `KeyNotFoundException` | Dictionarysta haettiin avainta, jota ei ole — käytä `ContainsKey` |
| `FileNotFoundException` | `File.ReadAllText` tiedostolle, jota ei ole |
| `DirectoryNotFoundException` | Polun kansiota ei ole (`data\x.txt`). `catch (FileNotFoundException)` **ei** nappaa tätä; `File.Exists` palauttaa `false` molemmissa |
| `IOException` | Tiedosto on lukittu tai levy täynnä — kirjoitus epäonnistuu. Ei voi tarkistaa etukäteen |
| `DivideByZeroException` | Kokonaisluku jaettiin nollalla |
| `NullReferenceException` | Metodikutsu `null`-viittaukselle (esim. `text.Length` kun `text` on `null`) |

## Estä virhe ennen kuin se syntyy

Poikkeus on **poikkeus** normaaliin kulkuun. Ikä väärässä muodossa ei ole yllätys. Käyttäjä kirjoittaa mitä tahansa.

```csharp
// Parempi syötteelle: ei kaadu
Console.Write("Anna ikä: ");
string? text = Console.ReadLine();

if (int.TryParse(text, out int age))
{
    Console.WriteLine($"Ikä: {age}");
}
else
{
    Console.WriteLine("Kirjoita kokonaisluku.");
}
```

`TryParse` palauttaa `false`, jos teksti ei ole luku. Ohjelma jatkuu. Sama idea silmukalla: kysy uudestaan, kunnes arvo kelpaa — [ohjausrakenteet](Control-Structures.md).

```csharp
// Huonompi syötteelle: käyttää poikkeusta tavallisena haarana
try
{
    int age = int.Parse(userInput);
}
catch (FormatException)
{
    Console.WriteLine("Ei ole luku");
}
```

Molemmat "toimivat". `TryParse` on tarkoitettu tälle tilanteelle. `try-catch` jää tilanteisiin, joita et voi tarkistaa etukäteen: tiedosto katosi, verkko katkesi, JSON on rikki.

Tarkista myös:

- taulukon indeksi ennen hakua
- Dictionaryn avain (`ContainsKey`)
- tiedoston olemassaolo (`File.Exists`)
- ettei merkkijono ole `null` ennen `.Length`

## try-catch — kun virhe on odottamaton

```csharp
try
{
    // Rivit, jotka voivat kaatua
}
catch (FormatException)
{
    // Mitä tehdään, jos muoto on väärä
}
```

C# yrittää `try`-lohkon. Jos poikkeus syntyy, suoritus hyppää **heti** sopivaan `catch`-lohkoon. `try`-lohkon loput rivit jäävät ajamatta. Rakenteen jälkeiset rivit ajetaan normaalisti.

```csharp
try
{
    string json = File.ReadAllText("menu.json");
    Console.WriteLine(json);                 // ei ajeta, jos tiedosto puuttuu
}
catch (FileNotFoundException)
{
    Console.WriteLine("Menu-tiedostoa ei löydy — käytetään oletusvalikkoa.");
}

Console.WriteLine("Ohjelma jatkuu.");        // ajetaan molemmissa tapauksissa
```

### Yksi catch nappaa vain oman tyyppinsä

```csharp
try
{
    int number = int.Parse(Console.ReadLine());   // "abc" → FormatException
    int result = 100 / number;                    // 0 → DivideByZeroException
}
catch (FormatException)
{
    Console.WriteLine("Syöte ei ole luku.");
}
```

`abc` menee `catch`-lohkoon. `0` kaataa ohjelman silti, koska `DivideByZeroException` ei ole `FormatException`. Lohko nappaa vain sen tyypin, jonka nimesit.

### Monta catch-lohkoa

Voit ketjuttaa useita `catch`-lohkoja. Ne käydään läpi ylhäältä alas, ja ensimmäinen sopiva ajetaan. **Tarkin tyyppi ensin**, yleinen `Exception` viimeisenä. Jos `Exception` on ensimmäisenä, tulee käännösvirhe CS0160, koska sen jälkeiset lohkot eivät voisi koskaan ajaa.

```csharp
try
{
    int number = int.Parse(Console.ReadLine());
    int result = 100 / number;
}
catch (FormatException)
{
    Console.WriteLine("Syöte ei ole luku.");
}
catch (DivideByZeroException)
{
    Console.WriteLine("Nollalla ei voi jakaa.");
}
catch (Exception ex)
{
    Console.WriteLine($"Odottamaton virhe: {ex.Message}");
}
```

`ex` on poikkeusolio. `ex.Message` on sama viesti, jonka kaatumisilmoitus näyttäisi. Tulosta se, kun et tiedä tarkemmin, mitä tapahtui.

### try on oma lohko

`try`-lohko on oma näkyvyysalue. Sen sisällä esitelty muuttuja ei näy `catch`-lohkossa eikä rakenteen jälkeen (CS0103). Esittele muuttuja **ennen** `try`-sanaa:

```csharp
Dictionary<string, decimal> codes = new Dictionary<string, decimal>();   // ennen try

try
{
    // täytä codes tiedostosta
}
catch (FileNotFoundException)
{
    Console.WriteLine("Koodilistaa ei löydy — alennuksia ei ole käytössä.");
}

return codes;   // näkyy, koska esiteltiin ennen try-lohkoa
```

Sama sääntö kuin muissa lohkoissa — [näkyvyysalueet](Scopes.md#try-ja-catch-ovat-lohkoja).

### Tyhjä catch on vaarallisempi kuin kaatuminen

Älä jätä `catch`-lohkoa tyhjäksi. Silloin ohjelma "toimii", mutta vika katoaa. Jos kuitin tallennuksen `catch (IOException)` on tyhjä, kassa näyttää koko päivän toimivan — ja omistaja huomaa illalla, että `kuitit.txt` on tyhjä. Kaatuminen olisi kertonut vian ensimmäisellä asiakkaalla. Tulosta aina vähintään `ex.Message`.

### Missä try-catch on

Kun luet tiedostoa rivi riviltä, `try-catch` kuuluu **silmukan sisälle**, rikkinäisen rivin kohdalle. Silloin rivi ohitetaan ja loput käsitellään:

```csharp
for (int i = 0; i < lines.Length; i++)
{
    try
    {
        string[] parts = lines[i].Split(';');
        int score = int.Parse(parts[1]);
    }
    catch (FormatException)
    {
        Console.WriteLine($"Rivi {i + 1} ohitettu: ei ole luku.");
    }
}
```

Jos rakenne on koko silmukan ympärillä, ensimmäinen rikkinäinen rivi lopettaa lukemisen ja loput rivit jäävät käsittelemättä. Koko `Main` yhdessä `try-catch`-rakenteessa on sama virhe isompana: ohjelma ei kaadu, mutta ohjelmointivirheet piiloutuvat `Jokin meni pieleen` -viestin taakse. Älä tee niin.

## Estä vai ota kiinni — sääntö

**Tarkista se, minkä voit — ota kiinni se, mitä et voi.**

| Kysy itseltäsi | Jos kyllä |
|----------------|-----------|
| Tuleeko virhe **käyttäjän syötteestä**? | Estä: `TryParse`, `ReadInt(min, max)`, silmukka — käyttäjä saa uuden yrityksen |
| Voinko tarkistaa tilanteen **yhdellä ehdolla** ennen vaarallista riviä? | Estä: `if`, `ContainsKey`, `Exists`, `parts.Length == 2`, `Count == 0` |
| Onko puuttuminen **normaali tilanne** (ensimmäinen käynnistys, `kuitit.txt`)? | Estä: `File.Exists`, ja ohjelma jatkaa hiljaa |
| Tuleeko virhe **ohjelman ulkopuolelta** tavalla, jota et voi tarkistaa (tiedosto katoaa, levy täynnä, rivin sisältö on mitä sattuu)? | Ota kiinni: `try-catch` **lähellä** kaatuvaa riviä, **tarkka** tyyppi, **viesti** käyttäjälle |

`Exists` voi palauttaa `true`, ja `ReadAllLines` kaatua silti — tiedosto on lukittu toisessa ohjelmassa. Kurssityössä `Exists` riittää. Sama päätös tiedostoille: [`Exists` vai `catch`](File-IO.md#polku-ja-puuttuva-tiedosto).

## throw — heitä itse

Metodi voi ilmoittaa virheestä `throw`-sanalla. Kutsuja päättää, ottaako sen kiinni.

```csharp
static int Divide(int a, int b)
{
    if (b == 0)
    {
        throw new DivideByZeroException("Jakaja ei voi olla nolla.");
    }

    return a / b;
}
```

Alussa tarvitaan tätä harvoin. Riittää, että luet .NET:n heittämät poikkeukset.

Oma poikkeusluokka (`class InvalidAgeException`) kuuluu myöhempään.

## finally ja using — myöhemmin

`finally` ajetaan aina, onnistui `try` tai ei. Sitä käytetään resurssin sulkemiseen. Tiedostoille parempi tapa on `using`, joka sulkee tiedoston automaattisesti. Katso [tiedostot](File-IO.md), kun tallennat dataa.

## Yhteenveto

- Kaatuminen kertoo tyypin, viestin ja oman rivin. Lue ne ensin.
- Tarkista se, minkä voit (`TryParse`, `if`, `ContainsKey`, `Exists`) — ota kiinni se, mitä et voi (tiedosto katoaa, rivi on rikki).
- Poikkeus hyppää heti `catch`-lohkoon, `try`-lohkon loput rivit jäävät ajamatta, rakenteen jälkeen jatketaan.
- Yksi `catch` nappaa vain oman tyyppinsä. Monta lohkoa: tarkin ensin, `Exception ex` viimeisenä (muuten CS0160).
- `try` on oma lohko — esittele muuttuja ennen sitä. `try-catch` silmukan sisälle, ei ympärille, eikä koko `Main`in ympärille.
- Älä nielaise poikkeusta tyhjällä `catch`-lohkolla. Tulosta vähintään `ex.Message`.
- Yleisimmät: `FormatException`, `IndexOutOfRangeException`, `KeyNotFoundException`, `FileNotFoundException`, `DirectoryNotFoundException`.

Seuraavaksi: [Debuggaus](Debug.md) · [Tyyppimuunnokset](Casting.md) · [Tiedostojen luku ja kirjoitus](File-IO.md)
