# JSON (JavaScript Object Notation)

**JSON** on tekstimuoto datalle. Ihminen voi lukea sen. Kone voi lukea sen. C#-olio ei säily tiedostossa sellaisenaan. JSON on silta: olio → teksti → tiedosto, ja takaisin.

Arjen esimerkki: ostoslista paperilla. Rivillä on nimi ja määrä. JSON on sama idea merkeillä, joita ohjelma ymmärtää.

Kurssilla JSON + [tiedosto](File-IO.md) tarkoittaa: eilisen myynti on vielä tallella, kun ohjelma avataan uudestaan.

**Microsoft:** [System.Text.Json](https://learn.microsoft.com/fi-fi/dotnet/api/system.text.json)

## Kartta

| Termi | Yksi lause |
|-------|------------|
| JSON-objekti | Aaltosulkeet `{ }`, avain–arvo-pareja |
| Avain | Aina lainausmerkeissä: `"Nimi"` |
| Serialisointi | C#-olio → JSON-teksti |
| Deserialisointi | JSON-teksti → C#-olio |
| Tiedosto | `File.WriteAllText` / `File.ReadAllText` |

## Miltä JSON näyttää?

```json
{
  "Nimi": "Matti",
  "Ika": 30,
  "Harrastukset": [ "jalkapallo", "koodaus" ]
}
```

| Sääntö | Esimerkki |
|--------|-----------|
| Avain lainausmerkeissä | `"Nimi"` |
| Kaksoispiste avaimen ja arvon välissä | `"Ika": 30` |
| Pilkku parien väliin, ei viimeisen perään | `"Nimi": "Matti",` |
| Teksti lainausmerkeissä, numero ilman | `"Matti"` ja `30` |
| Lista hakasulkeissa | `[ "a", "b" ]` |
| Totuusarvo | `true` / `false` |
| Tyhjä | `null` |

Puuttuva pilkku tai extra pilkku viimeisen parin jälkeen rikkoo tiedoston. C# ei lue rikkinäistä JSONia.

JSON ei ole C#-koodia. Tiedostossa ei ole `decimal` eikä `m`-päätettä. Numerot kirjoitetaan kuten `12.5`.

## C# → JSON ja takaisin

Tarvitset `using System.Text.Json;` ja luokan, jonka propertyjen **nimet täsmäävät** JSON-avaimiin.

```csharp
using System.Text.Json;

public class Person
{
    public string Nimi { get; set; }
    public int Ika { get; set; }
}

Person person = new Person { Nimi = "Maija", Ika = 25 };

string json = JsonSerializer.Serialize(person);
// {"Nimi":"Maija","Ika":25}

Person? copy = JsonSerializer.Deserialize<Person>(json);
Console.WriteLine(copy?.Nimi);   // Maija
```

**Serialisointi** pakkaa olion tekstiksi. **Deserialisointi** rakentaa olion tekstistä.

Jos JSON-avain on `nimi` ja property on `Nimi`, arvo voi jäädä `null` tai nollaksi. Kirjoitusvirhe ei aina kaada ohjelmaa. Tarkista nimet.

Luettava tiedosto: `WriteIndented = true` lisää rivinvaihdot.

```csharp
var options = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(person, options);
```

## Tallennus tiedostoon

```csharp
using System.IO;
using System.Text.Json;

List<decimal> sales = new List<decimal> { 19.35m, 12.00m };

var options = new JsonSerializerOptions { WriteIndented = true };
string json = JsonSerializer.Serialize(sales, options);
File.WriteAllText("myynti.json", json);

if (File.Exists("myynti.json"))
{
    string loaded = File.ReadAllText("myynti.json");
    List<decimal>? restored = JsonSerializer.Deserialize<List<decimal>>(loaded);
}
```

Puuttuva tiedosto: [tiedostot](File-IO.md). Rikkinäinen JSON heittää poikkeuksen — [poikkeukset](Exception-Handling.md).

Sisäkkäiset oliot (osoite henkilön sisällä) toimivat samalla tavalla: tee luokka per taso, propertyjen nimet täsmäävät.

Web-API, MongoDB ja camelCase-nimeäminen (`PropertyNamingPolicy`) tulevat vastaan myöhemmin. Alussa riittää: serialize, kirjoita tiedostoon, lue, deserialize.

## Yhteenveto

- JSON on tekstiä: avaimet lainausmerkeissä, pilkut paikoillaan.
- `Serialize` tekee tekstin. `Deserialize` tekee olion.
- Propertyn nimi = JSON-avain, tai arvo katoaa hiljaa.
- `File.WriteAllText` säilyttää datan ohjelman sulkemisen yli.

Seuraavaksi: [Tiedostojen luku ja kirjoitus](File-IO.md) · [Propertyt](Properties.md) · [Tietorakenteet](Data-Structures.md)
