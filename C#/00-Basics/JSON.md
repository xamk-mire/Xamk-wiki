# JSON (JavaScript Object Notation)

## Mikä on JSON?

JSON (JavaScript Object Notation) on kevyt, ihmisen luettavissa oleva tiedonvälitysformaatti, jota käytetään laajalti modernissa web-kehityksessä. Alun perin se perustui JavaScriptin oliorakenteeseen, mutta nykyään JSONia tuetaan käytännössä kaikilla ohjelmointikielillä ja alustoilla.

JSONin avulla data voidaan mallintaa selkeänä avain-arvo- tai listarakenteena. Syntaksi on yksinkertainen, ja se on helposti luettavissa sekä ihmisille että koneille. Sen vuoksi JSON on suosittu erityisesti rajapintojen (API:en) ja sovellusten välisessä tiedonsiirrossa.

## JSONin rakenne ja syntaksi

### Esimerkki JSON-tiedosta

```json
{
  "etunimi": "Matti",
  "sukunimi": "Meikäläinen",
  "ika": 30,
  "harrastukset": [
    "jalkapallo",
    "valokuvaus",
    "koodaus"
  ],
  "osoite": {
    "katu": "Esimerkkikatu 1",
    "kaupunki": "Helsinki",
    "postinumero": 00100
  }
}
```

Tässä esimerkissä JSON kuvaa yhtä henkilö-oliota (object). Se sisältää useita avaimia (kuten `etunimi`, `sukunimi` ja `ika`), joilla on arvoja (esim. `"Matti"`, `"Meikäläinen"`, `30`). JSON voi myös sisältää listoja (arrays), kuten `harrastukset`, sekä sisäkkäisiä objekteja, kuten `osoite`.

## JSONin keskeiset piirteet

### 1. Avaimien ja arvojen käyttö

- JSON-objekti on suljettu aaltosulkeisiin (`{ ... }`).
- Avaimet ovat merkkijonoja, jotka kirjoitetaan aina lainausmerkeissä (esim. `"etunimi"`).
- Arvot voivat olla merkkijonoja (string), numeroita, taulukoita (array) tai muita objekteja.

### 2. Taulukot (Arrays)

- Merkitään hakasulkeilla (`[ ... ]`).
- Esimerkiksi `["omena", "banaani", "appelsiini"]` on taulukko, joka sisältää kolme merkkijonoalkiota.

### 3. Datatyypit

- **String (merkkijono)**: `"teksti"`
- **Number (luku)**: `10`, `3.14` jne. (ilman lainausmerkkejä)
- **Boolean (totuusarvo)**: `true` tai `false`
- **Object (objekti)**: `{ "avain": "arvo" }`
- **Array (taulukko)**: `[ 1, 2, 3 ]`
- **Null**: `null`

### 4. Pilkut ja kaksoispisteet

- Yhtä avain-arvo -paria erotetaan toisesta pilkulla `,`.
- Avaimen ja arvon välissä on kaksoispiste `:`.

### 5. Syntaksin säännöt

- Merkittävimmät säännöt liittyvät sulkuihin, pilkkuihin ja lainausmerkkeihin.
- Huolimattomat pilkun tai lainausmerkkien virheet rikkovat JSON-rakenteen ja estävät sen lukemisen.

## Missä JSONia käytetään?

### 1. Sovellusten välisessä tiedonsiirrossa

- REST-rajapinnat (API) palauttavat ja vastaanottavat dataa usein JSON-muodossa.
- Esimerkiksi selain saa palvelimelta tiedon JSON-muodossa ja näyttää sen käyttäjälle sopivassa muodossa.

### 2. Konfiguraatiotiedostoissa

- Monissa ohjelmistokehityksen työkaluissa ja kirjastoissa konfiguraatio voidaan määritellä JSONin avulla.

### 3. Tietokannoissa

- Jotkin NoSQL-tietokannat, kuten MongoDB, tallentavat dataa JSON-tyyppisessä muodossa (BSON).

### 4. Modernit rajapinnat ja integraatiot

- Melkein kaikki uudet ohjelmistot tarjoavat jonkin rajapinnan JSON:ia käyttäen, koska se on selkeä, kevyt ja helposti käsiteltävä formaatti.

## C# Esimerkki: JSON-muotoisen merkkijonon muuntaminen olioksi

Tässä muutamme JSON-muotoisen merkkijonon C#-olioksi (`Person`-luokaksi).

```csharp
using System;
using System.Text.Json;

public class Person
{
    public string Nimi { get; set; }
    public int Ika { get; set; }
}

class Program
{
    static void Main()
    {
        string jsonString = "{\"Nimi\":\"Matti\",\"Ika\":25}";
        
        Person person = JsonSerializer.Deserialize<Person>(jsonString);
        
        if (person != null)
        {
            Console.WriteLine($"Nimi: {person.Nimi}");
            Console.WriteLine($"Ikä: {person.Ika}");
        }
    }
}
```

**Selitys**:
- `JsonSerializer.Deserialize<T>(jsonString)` muuntaa JSON-muotoisen merkkijonon C#-olioksi.
- Tarkistamme, ettei deserialisoitu objekti ole `null`, ennen kuin käytämme sen ominaisuuksia.
- Lopuksi tulostamme `Nimi` ja `Ika` -kentät.

## C# Esimerkki: C#-olion muuntaminen JSONiksi

Tässä muutamme C#-olion JSON-muotoiseksi merkkijonoksi.

```csharp
using System;
using System.Text.Json;

public class Person
{
    public string Nimi { get; set; }
    public int Ika { get; set; }
}

class Program
{
    static void Main()
    {
        Person person = new Person
        {
            Nimi = "Maija",
            Ika = 25
        };
        
        string jsonString = JsonSerializer.Serialize(person);
        Console.WriteLine(jsonString);
        // Tulostaa: {"Nimi":"Maija","Ika":25}
    }
}
```

**Selitys**:
- `JsonSerializer.Serialize(object)` muuntaa C#-olion JSON-muotoiseksi merkkijonoksi.
- Lopputuloksena saamme merkkijonon: `{"Nimi":"Maija","Ika":25}`

## Monimutkaisempi esimerkki

```csharp
using System;
using System.Collections.Generic;
using System.Text.Json;

public class Address
{
    public string Katu { get; set; }
    public string Kaupunki { get; set; }
    public int Postinumero { get; set; }
}

public class Person
{
    public string Etunimi { get; set; }
    public string Sukunimi { get; set; }
    public int Ika { get; set; }
    public List<string> Harrastukset { get; set; }
    public Address Osoite { get; set; }
}

class Program
{
    static void Main()
    {
        Person person = new Person
        {
            Etunimi = "Matti",
            Sukunimi = "Meikäläinen",
            Ika = 30,
            Harrastukset = new List<string> { "jalkapallo", "valokuvaus", "koodaus" },
            Osoite = new Address
            {
                Katu = "Esimerkkikatu 1",
                Kaupunki = "Helsinki",
                Postinumero = 00100
            }
        };
        
        // Serialisointi
        var options = new JsonSerializerOptions { WriteIndented = true };
        string json = JsonSerializer.Serialize(person, options);
        Console.WriteLine(json);
        
        // Deserialisointi
        Person deserializedPerson = JsonSerializer.Deserialize<Person>(json);
        Console.WriteLine($"\nDeserialisoitu: {deserializedPerson.Etunimi} {deserializedPerson.Sukunimi}");
    }
}
```

## JSON-muotoilu (Pretty Print)

```csharp
using System.Text.Json;

var options = new JsonSerializerOptions
{
    WriteIndented = true,  // Lisää sisennystä
    PropertyNamingPolicy = JsonNamingPolicy.CamelCase  // camelCase nimeäminen
};

string json = JsonSerializer.Serialize(person, options);
```

## Yhteenveto

- **JSON** on kevyt ja luettava tiedonvälitysformaatti.
- **Syntaksi** on yksinkertainen: avaimet lainausmerkeissä, arvot eri tyyppejä.
- **C#:ssa** käytetään `System.Text.Json`-nimiavaruutta JSONin käsittelyyn.
- **Serialisointi** muuntaa C#-olion JSONiksi.
- **Deserialisointi** muuntaa JSON-merkkijonon C#-olioksi.
- **JSON** on laajalti käytetty API:en ja sovellusten välisessä tiedonsiirrossa.

## Hyödyllisiä linkkejä

- [Microsoftin JSON-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/api/system.text.json)
- [JSON.org](https://www.json.org/) - JSONin virallinen dokumentaatio

