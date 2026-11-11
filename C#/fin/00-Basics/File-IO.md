# Tiedostojen luku ja kirjoitus

Konsolista luettu data katoaa, kun ohjelma suljetaan. **Tiedosto** tallentaa tekstin koneelle. Seuraavana päivänä ohjelma voi lukea menun tai eilisen myynnin.

Arjen esimerkki: kassan päiväkirja. Ilman vihkoa summa on vain muistissa. Vihko jää tiskille yöksi.

Tiedoston voi yhdistää [JSONiin](JSON.md). Ensin opitaan itse tiedosto.

**Microsoft:** [File class](https://learn.microsoft.com/fi-fi/dotnet/api/system.io.file)

## Kartta

| Metodi | Mitä tekee |
|--------|------------|
| `File.WriteAllText(polku, sisältö)` | Kirjoittaa merkkijonon (ylikirjoittaa vanhan) |
| `File.ReadAllText(polku)` | Lukee koko tiedoston merkkijonoksi |
| `File.Exists(polku)` | `true`, jos tiedosto on olemassa |
| `File.AppendAllText(polku, teksti)` | Lisää tekstiä loppuun — rivinvaihto `Environment.NewLine` itse |
| `File.ReadAllLines(polku)` | Lukee rivit `string[]`-taulukoksi |
| `File.WriteAllLines(polku, string[])` | Kirjoittaa taulukon rivit, yksi per rivi (ylikirjoittaa vanhan) |
| `"Anna;87".Split(';')` | Pilkkoo rivin osiin: `["Anna", "87"]` |

## Kolme metodia riittää alkuun

`System.IO.File` käsittelee koko tiedoston kerralla. Kirjoita, lue, tarkista.

```csharp
using System.IO;

string path = "myynti.txt";

File.WriteAllText(path, "Päivän myynti: 33,30 €");

if (File.Exists(path))
{
    string content = File.ReadAllText(path);
    Console.WriteLine(content);
}
```

Tiedosto syntyy projektin ajokansioon (Visual Studiossa yleensä `bin/Debug/net8.0/`), ellei polkuun kirjoita kansiota.

## Lisää rivejä ilman ylikirjoitusta

`WriteAllText` korvaa koko tiedoston. Päiväkirjaan tai lokiin sopii `AppendAllText` — se lisää tekstin loppuun:

```csharp
File.AppendAllText("loki.txt", $"Tilaus {total:F2} €{Environment.NewLine}");
```

`Environment.NewLine` on käyttöjärjestelmän rivinvaihto (Windowsissa `\r\n`). Ilman sitä jokainen `AppendAllText` jatkaa **samaa riviä**: tiedostossa lukee `Tilaus 19,35 €Tilaus 12,00 €`, ja `ReadAllLines` palauttaa yhden rivin, vaikka tallensit kolme.

## Rivien lukeminen taulukkoon

```csharp
string[] lines = File.ReadAllLines("menu.txt");

foreach (string line in lines)
{
    Console.WriteLine(line);
}
```

Jokainen rivi on yksi alkio. Tyhjä tiedosto tuottaa tyhjän taulukon.

`foreach` riittää, kun vain käyt rivit läpi. Käytä `for`-silmukkaa, kun tarvitset **rivinumeron** — esimerkiksi kertoaksesi käyttäjälle, mikä rivi oli rikki. Taulukon indeksi alkaa nollasta, joten käyttäjälle näytetään `i + 1`:

```csharp
string[] lines = File.ReadAllLines("kuitit.txt");

for (int i = 0; i < lines.Length; i++)
{
    Console.WriteLine($"{i + 1}: {lines[i]}");   // 1: ..., 2: ..., 3: ...
}
```

## Rivi osiin: Split

Tiedoston rivillä on usein monta tietoa erottimella: `Anna;87`. `Split` pilkkoo rivin taulukoksi:

```csharp
string[] parts = "Anna;87".Split(';');   // ["Anna", "87"]
string name = parts[0];                  // "Anna"
```

Osat ovat **tekstiä**. `"87"` ei ole luku ennen muunnosta: `int.TryParse(parts[1], out int score)`.

Rivi voi olla rikki kahdella tavalla. `Ville` ilman puolipistettä antaa yhden osan, ja `parts[1]` heittää `IndexOutOfRangeException`. `Pekka;abc` antaa kaksi osaa, mutta `int.Parse("abc")` heittää `FormatException`. Tarkistus tehdään **silmukan sisällä**, jotta rikkinäinen rivi ohitetaan ja loput käsitellään:

```csharp
for (int i = 0; i < lines.Length; i++)
{
    string[] parts = lines[i].Split(';');

    if (parts.Length == 2 && int.TryParse(parts[1], out int score))
    {
        Console.WriteLine($"{parts[0]}: {score}");
    }
    else
    {
        Console.WriteLine($"Rivi {i + 1} ohitettu: {lines[i]}");
    }
}
```

Sama onnistuu `try-catch`-rakenteella silmukan sisällä — [poikkeusten käsittely](Exception-Handling.md#try-catch--kun-virhe-on-odottamaton). Jos rakenne on koko silmukan ympärillä, ensimmäinen rikkinäinen rivi lopettaa lukemisen.

**Desimaalit tiedostossa:** `decimal.Parse("2.50")` ei anna suomalaisella koneella `2,50` — desimaalierotin on pilkku, ei piste, joten tulos on `250` tai `FormatException`. Kurssin sääntö: tallenna tiedostoon **kokonaisluku** (`10`) ja laske ohjelmassa `percent / 100m`. Katso [tyyppimuunnokset](Casting.md#yleisiä-virheitä).

## Polku ja puuttuva tiedosto

Jos tiedostoa ei ole, `ReadAllText` heittää `FileNotFoundException`-poikkeuksen. Tarkista olemassaolo ensin tai käytä `try-catch`-lohkoa:

```csharp
string path = "menu.txt";

if (!File.Exists(path))
{
    Console.WriteLine("Menu-tiedostoa ei löydy — käytetään oletusvalikkoa.");
    return;
}

string json = File.ReadAllText(path);
```

**`Exists` vai `catch`?** Kumpikin hoitaa puuttuvan tiedoston. Valinta riippuu siitä, onko puuttuminen normaalia vai virhe:

| Tilanne | Tapa |
|---------|------|
| Puuttuminen on **normaalia** — ensimmäinen käynnistys, `kuitit.txt` ei ole vielä syntynyt | `File.Exists`, ja ohjelma jatkaa hiljaa |
| Puuttuminen on **virhe** — asetustiedosto tai `alennuskoodit.txt` kuuluu olla paikallaan | `catch (FileNotFoundException)`: kerro käyttäjälle, metodi palauttaa tyhjän kokoelman, kassa jatkaa |

```csharp
static Dictionary<string, decimal> LoadDiscountCodes(string path)
{
    Dictionary<string, decimal> codes = new Dictionary<string, decimal>();   // ennen try

    try
    {
        foreach (string line in File.ReadAllLines(path))
        {
            // Split, tarkistus, codes[parts[0]] = percent / 100m
        }
    }
    catch (FileNotFoundException)
    {
        Console.WriteLine($"Tiedostoa {path} ei löydy — alennuskoodit eivät ole käytössä.");
    }

    return codes;
}
```

Jos polun **kansio** puuttuu (`data\x.txt`), poikkeus on `DirectoryNotFoundException`, eikä `catch (FileNotFoundException)` nappaa sitä. `File.Exists` palauttaa `false` molemmissa tapauksissa. Päätössääntö: [estä vai ota kiinni](Exception-Handling.md#estä-vai-ota-kiinni--sääntö).

**Polku.** Suhteellinen polku `"menu.txt"` tarkoittaa ajokansiota `bin\Debug\net8.0`. `Path.GetFullPath(path)` näyttää koko polun, jos et löydä tiedostoa. Absoluuttinen polku (`C:\kurssi\menu.txt`) on hauras — se ei toimi toisen koneella.

Pidä data-tiedosto projektissa ja käytä lyhyttä nimeä. Projektiin lisätty tiedosto kopioituu ajokansioon **vain**, kun asetat sille Solution Explorerissa Properties → **Copy to Output Directory = Copy if newer**. Muokkaa tiedostoa Solution Explorerin kautta, ei ajokansiossa: ajokansion kopio korvautuu seuraavassa buildissa. Muistio ei päivitä avointa tiedostoa itse — sulje ja avaa uudelleen, kun ohjelma on kirjoittanut siihen.

## Yhdistelmä: tiedosto + JSON

Tyypillinen kuvio: talleta oliot JSONina, lue ne takaisin ohjelman käynnistyessä.

```csharp
using System.IO;
using System.Text.Json;

List<decimal> sales = new List<decimal> { 19.35m, 12.00m };

string json = JsonSerializer.Serialize(sales);
File.WriteAllText("myynti.json", json);

if (File.Exists("myynti.json"))
{
    string loaded = File.ReadAllText("myynti.json");
    List<decimal>? restored = JsonSerializer.Deserialize<List<decimal>>(loaded);
}
```

Syntaksi ja oliot: [JSON](JSON.md). Poikkeukset: [Poikkeusten käsittely](Exception-Handling.md).

## Encoding — skandit

Suomen ääkköset (`ä ö å`) vaativat UTF-8-koodauksen. `WriteAllText` / `ReadAllText` käyttävät sitä oletuksena nykyaikaisessa .NET:issä. Jos tiedosto on luotu Muistiossa "ANSI"-muodossa, ääkköset voivat vääristyä — tallenna UTF-8:na.

## Yleisiä virheitä

| Virhe | Mitä tapahtuu | Korjaus |
|-------|---------------|---------|
| `Environment.NewLine` unohtui `AppendAllText`-kutsusta | Kaikki samalle riville, `ReadAllLines` antaa yhden rivin | Lisää rivinvaihto tekstin perään |
| `WriteAllText` lokiin tai kuitteihin | Vanha sisältö katoaa joka kerta | `AppendAllText` |
| `parts[1]` ilman `Length`-tarkistusta | `IndexOutOfRangeException` rivillä `Ville` | `parts.Length == 2` ennen hakua |
| `decimal.Parse("2.50")` tiedostosta | `250` tai `FormatException` suomalaisella koneella | Kokonaisluku tiedostoon, `/ 100m` koodissa |
| Tiedosto muokattiin ajokansiossa | Muutos katosi Rebuildissa | Muokkaa Solution Explorerissa, Copy if newer |
| `try-catch` koko silmukan ympärillä | Ensimmäinen rikkinäinen rivi lopettaa lukemisen | `try-catch` tai tarkistus silmukan sisälle |

## Yhteenveto

- `WriteAllText` tallentaa (korvaa), `ReadAllText` lukee, `Exists` tarkistaa
- `AppendAllText` lisää loppuun — `Environment.NewLine` itse; `ReadAllLines` palauttaa rivit `string[]`-taulukkona, `for` kun tarvitset rivinumeron `i + 1`
- `Split(';')` pilkkoo rivin tekstiosiin; tarkista `parts.Length` ja muunna `TryParse`-metodilla silmukan sisällä
- Puuttuminen normaalia → `Exists`; puuttuminen virhe → `catch (FileNotFoundException)` ja viesti käyttäjälle
- Data-tiedosto projektiin, Copy to Output Directory = Copy if newer
- JSON + tiedosto = data säilyy ohjelman sulkemisen yli

Seuraavaksi: [JSON](JSON.md) · [Poikkeusten käsittely](Exception-Handling.md)
