# Poikkeusten käsittely (Exception Handling)

**Poikkeus** on virhe kesken ajon. Ohjelma kääntyi. Sitten tapahtui jotain, jota koodi ei osannut hoitaa: käyttäjä kirjoitti `abc` iäksi, tiedostoa ei ole, taulukosta haettiin paikkaa jota ei ole.

Jos poikkeusta ei käsitellä, ohjelma **kaatuu**. Kaatuminen ei riko konetta, Visual Studiota eikä koodia. Ohjelma lopettaa ja kertoo miksi.

Ensimmäinen taito ei ole `try-catch`. Ensimmäinen taito on **lukea ilmoitus**.

**Microsoft:** [Exceptions](https://learn.microsoft.com/fi-fi/dotnet/csharp/fundamentals/exceptions/)

## Kartta

| Asia | Yksi lause |
|------|------------|
| Virheilmoitus | Tyyppi + viesti + **oman koodin rivi** |
| Estä etukäteen | Tarkista syöte silmukalla tai `TryParse` |
| `try` / `catch` | Yritä, ja jos kaatuu, hoida virhe itse |
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

Keskimmäiset `System.Number...`-rivit ovat .NET:n sisäisiä. Hyppää niihin. Etsi **oman tiedoston** nimi.

Sama pino näkyy debuggerin Call Stack -ikkunassa. F5:n aikana Visual Studio avaa Exception Helper -ikkunan suoraan riville — [debuggaus](Debug.md#poikkeus-debuggerissa).

### Aloittelijan yleisimmät poikkeukset

| Poikkeus | Tyypillinen syy |
|----------|-----------------|
| `FormatException` | `"abc"` annettiin `Convert.ToInt32`-metodille |
| `OverflowException` | Luku ei mahdu `int`-tyyppiin (max n. 2,1 miljardia) |
| `IndexOutOfRangeException` | Taulukosta haettiin indeksiä, jota ei ole (`movies[4]` neljän alkion taulukossa) |
| `KeyNotFoundException` | Dictionarysta haettiin avainta, jota ei ole — käytä `ContainsKey` |
| `FileNotFoundException` | `File.ReadAllText` tiedostolle, jota ei ole |
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
    // Rivitat, jotka voivat kaatua
}
catch (FormatException)
{
    // Mitä tehdään, jos muoto on väärä
}
```

C# yrittää `try`-lohkon. Jos poikkeus syntyy, suoritus hyppää sopivaan `catch`-lohkoon. `try`-lohkon loput rivit jäävät ajamatta.

```csharp
try
{
    string json = File.ReadAllText("menu.json");
    Console.WriteLine(json);
}
catch (FileNotFoundException)
{
    Console.WriteLine("Menu-tiedostoa ei löydy — käytetään oletusvalikkoa.");
}
```

Voit ketjuttaa useita `catch`-lohkoja. **Tarkin tyyppi ensin**, yleinen `Exception` viimeisenä.

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

Älä jätä `catch`-lohkoa tyhjäksi. Silloin ohjelma "toimii", mutta vika katoaa. Et tiedä, miksi tulos on väärä.

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
- Estä tavallinen virhe tarkistuksella tai `TryParse`-metodilla.
- `try-catch` odottamattomille tilanteille (tiedosto, verkko, rikki oleva JSON).
- Älä nielaise poikkeusta tyhjällä `catch`-lohkolla.
- Yleisimmät: `FormatException`, `IndexOutOfRangeException`, `KeyNotFoundException`, `FileNotFoundException`.

Seuraavaksi: [Debuggaus](Debug.md) · [Tyyppimuunnokset](Casting.md) · [Tiedostojen luku ja kirjoitus](File-IO.md)
