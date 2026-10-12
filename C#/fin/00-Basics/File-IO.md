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
| `File.AppendAllText` | Lisää tekstiä loppuun |
| `File.ReadAllLines` | Lukee rivit taulukoksi |

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

`Environment.NewLine` on käyttöjärjestelmän rivinvaihto (Windowsissa `\r\n`).

## Rivien lukeminen taulukkoon

```csharp
string[] lines = File.ReadAllLines("menu.txt");

foreach (string line in lines)
{
    Console.WriteLine(line);
}
```

Jokainen rivi on yksi alkio. Tyhjä tiedosto tuottaa tyhjän taulukon.

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

Suhteellinen polku `"menu.txt"` tarkoittaa ajokansiota. Absoluuttinen polku (`C:\kurssi\menu.txt`) on hauras — se ei toimi toisen koneella. Pidä data tiedostot projektissa ja käytä lyhyttä nimeä.

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

## Yhteenveto

- `WriteAllText` tallentaa, `ReadAllText` lukee, `Exists` tarkistaa
- `AppendAllText` lisää loppuun, `ReadAllLines` palauttaa rivit taulukkona
- Puuttuva tiedosto kaataa ohjelman — tarkista `Exists` tai käytä `try-catch`
- JSON + tiedosto = data säilyy ohjelman sulkemisen yli

Seuraavaksi: [JSON](JSON.md) · [Poikkeusten käsittely](Exception-Handling.md)
