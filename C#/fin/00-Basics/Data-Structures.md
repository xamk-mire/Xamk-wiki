# Tietorakenteet (Data Structures)

**Tietorakenne** on tapa pitää monta arvoa yhdessä paikassa. Yksi muuttuja, monta arvoa, käsittely silmukalla.

Neljä elokuvaa neljässä muuttujassa (`movie1` … `movie4`) ei skaalaudu. Viides elokuva vaatii uuden muuttujan ja uuden rivin joka paikkaan. Taulukossa lisäät yhden nimen.

Aloita kolmesta: **taulukko**, **List** ja **Dictionary**. HashSet, jono ja pino ovat lisätietoa.

**Microsoft:** [Collections](https://learn.microsoft.com/fi-fi/dotnet/csharp/language-reference/builtin-types/collections)

## Kartta

| Kokoelma | Koko | Käyttö | Esimerkki |
|----------|------|--------|-----------|
| Taulukko `string[]` | Kiinteä — päätetään luodessa | Tunnettu, muuttumaton joukko | Päivän elokuvat |
| `List<decimal>` | Kasvaa `Add`-kutsuilla | Kertyvä data, jonka määrää ei tiedetä | Päivän ostokset |
| `Dictionary<string, decimal>` | Kasvaa | Avain → arvo | Alennuskoodi → prosentti |

Silmukat: [Ohjausrakenteet](Control-Structures.md).

## Indeksi alkaa nollasta

Jokaisella alkiolla on **indeksi** — järjestysnumero, joka alkaa **nollasta**. Neljän elokuvan taulukossa viimeinen indeksi on `3`.

```
movies[0]  →  "Avaruusseikkailu 3D"
movies[3]  →  "Animaatio: Metsän väki"
movies.Length  →  4
```

`movies[4]` heittää `IndexOutOfRangeException`-poikkeuksen — paikkaa ei ole.

Valikossa käyttäjä näkee numerot 1–4. Koodissa valinta muutetaan indeksiksi: `movies[choice - 1]`. Jos käyttäjä kirjoittaa `1`, haetaan `movies[0]`.

| | Taulukko | List |
|--|----------|------|
| Alkioiden määrä | `Length` | `Count` |
| Indeksi | `items[i]` | `items[i]` |

## Taulukko — koko päätetään heti

Taulukkoon mahtuu vain saman tyyppisiä arvoja. Kokoa ei voi kasvattaa myöhemmin.

```csharp
string[] movies =
{
    "Avaruusseikkailu 3D",
    "Komedia: Kahvia ja kaaosta",
    "Draama: Hiljainen joki",
    "Animaatio: Metsän väki"
};

Console.WriteLine(movies[0]);        // ensimmäinen
Console.WriteLine(movies.Length);    // 4

for (int i = 0; i < movies.Length; i++)
{
    Console.WriteLine($"{i + 1}. {movies[i]}");   // 1. Avaruusseikkailu 3D
}
```

`i + 1` on ihmisen numero. `movies[i]` on koneen paikka.

Tyhjä taulukko tietylle koolle: `int[] numbers = new int[5];` — viisi paikkaa, arvot nollia kunnes asetat ne.

Kaksiulotteinen taulukko (`int[,]`) on ruudukko. Alussa yksi rivi riittää. Sisäkkäiset silmukat: [ohjausrakenteet](Control-Structures.md#sisäkkäiset-silmukat).

## Rinnakkainen taulukko

**Rinnakkaiset taulukot** ovat kaksi samanpituista taulukkoa, joissa sama indeksi tarkoittaa samaa asiaa. `movies[1]` on elokuvan nimi, ja `ticketsPerMovie[1]` on sen myytyjen lippujen määrä.

```csharp
string[] movies = { "Avaruus", "Komedia", "Draama" };
int[] ticketsPerMovie = new int[movies.Length];   // yhtä monta laskuria kuin elokuvaa

ticketsPerMovie[choice] += ticketCount;           // choice on elokuvan indeksi
```

`movies.Length` pitää taulukot samankokoisina. Kun lisäät neljännen elokuvan, laskureitakin syntyy neljä ilman muuta muutosta. Kiinteä `new int[4]` hajoaa heti, kun elokuvien määrä muuttuu.

## List — koko kasvaa

Listaan lisätään alkioita ohjelman aikana. Päivän ostosten määrää ei tiedetä aamulla.

```csharp
List<decimal> sales = new List<decimal>();

sales.Add(12.00m);
sales.Add(7.50m);
sales.Add(19.35m);

Console.WriteLine(sales[0]);     // 12.00
Console.WriteLine(sales.Count);  // 3
```

`List<decimal>` luetaan: "lista desimaalilukuja". Hakasulkeiden väliin tulee alkion tyyppi.

```csharp
List<string> names = new List<string> { "Matti", "Liisa", "Pekka" };

names.Remove("Liisa");
bool exists = names.Contains("Matti");
```

Tarvitset `using System.Collections.Generic;` tiedoston alkuun, jos Visual Studio ei lisää sitä itse. **Ctrl+.** ehdottaa korjausta.

`foreach` kun et tarvitse numeroa. `for` kun tarvitset indeksin tai järjestysnumeron.

Kokoelma, jonka pitää kertyä kierrosten yli, luodaan silmukan **ulkopuolella**. Jos `List<decimal> purchases = new List<decimal>();` on `do-while`-silmukan sisällä, joka kierroksella syntyy uusi tyhjä lista ja edellisten asiakkaiden ostokset katoavat. Sama sääntö kuin [kertymämuuttujalla](Control-Structures.md#kertymämuuttuja).

Älä kutsu `Remove`-metodia `foreach`-silmukan sisällä. Lista muuttuu kesken läpikäynnin, ja ohjelma kaatuu `InvalidOperationException`-poikkeukseen. Etsi poistettava alkio silmukassa, mutta tee `Remove` vasta silmukan jälkeen.

## Dictionary — avain avaa arvon

Sanakirja etsii **avaimella**, ei järjestyksellä. Alennuskoodi `LEFFA10` avaa prosentin `0.10`. If-ketju jokaiseen koodiin ei skaalaudu. Uusi koodi on yksi rivi.

```csharp
Dictionary<string, decimal> discounts = new Dictionary<string, decimal>
{
    { "LEFFA10", 0.10m },
    { "KESA20", 0.20m }
};

string code = "leffa10";
string key = code.ToUpper();

if (discounts.ContainsKey(key))
{
    decimal percent = discounts[key];
    decimal discount = subtotal * percent;
}
```

Ilman `ContainsKey`-tarkistusta tuntematon avain kaataa ohjelman (`KeyNotFoundException`). Sama turvallisesti: `TryGetValue`.

```csharp
if (discounts.TryGetValue(key, out decimal percent))
{
    Console.WriteLine(percent);
}
```

Kaikki parit silmukassa:

```csharp
foreach (var pair in discounts)
{
    Console.WriteLine($"{pair.Key}: {pair.Value}");
}
```

`Key` on avain, `Value` on arvo. Avaimen pitää olla uniikki. Samaa koodia ei voi lisätä kahdesti.

Avain huomioi kirjainkoon: `"koira"` ja `"Koira"` ovat eri avaimia. Siksi esimerkissä käyttäjän syöte muutetaan `ToUpper()`-kutsulla isoiksi kirjaimiksi ennen hakua. Avaimet on tallennettu isoilla kirjaimilla, eikä `"leffa10"` löytäisi avainta `"LEFFA10"` ilman muunnosta.

## Pienin arvo listasta

Suurimman ostoksen voi alustaa nollalla, koska jokainen ostos on nollaa suurempi ja ylittää alkuarvon. Pienimmän kanssa sama ei toimi: nolla on pienempi kuin jokainen hinta, joten ehto `price < smallest` ei toteudu koskaan ja tulos jää nollaksi.

Aloita sen sijaan listan ensimmäisestä alkiosta. Silloin listassa pitää olla vähintään yksi alkio.

```csharp
decimal smallest = prices[0];

foreach (decimal price in prices)
{
    if (price < smallest)
    {
        smallest = price;
    }
}
```

Tyhjässä listassa ei ole alkiota `prices[0]`, ja haku kaatuu `ArgumentOutOfRangeException`-poikkeukseen. Tarkista `prices.Count == 0` ennen laskentaa ja tulosta silloin esimerkiksi "Ei ostoksia".

## Yleisiä virheitä

**1. Indeksi 4 neljän alkion kokoelmassa**

Pituus 4, lailliset indeksit 0–3.

**2. `Length` ja `Count` sekaisin**

Taulukolla `Length`. Listalla ja Dictionarylla `Count`.

**3. Valikon numero suoraan indeksiksi**

Käyttäjän `1` ei ole `movies[1]` (toinen elokuva). Vähennä yksi.

**4. Dictionary ilman tarkistusta**

`discounts["TUNTEMATON"]` kaatuu. Tarkista avain ensin.

## HashSet, jono ja pino — myöhemmin

| Rakenne | Idea | Milloin |
|---------|------|---------|
| `HashSet<T>` | Jokainen arvo vain kerran | "Onko tämä jo lisätty?" |
| `Queue<T>` | Ensimmäinen sisään, ensimmäinen ulos | Jonotus |
| `Stack<T>` | Viimeinen sisään, ensimmäinen ulos | Peruutuspino |

Aloita taulukosta, Listasta ja Dictionarysta. Big O -ajat ovat [omalla sivullaan](../99-General/Big-O.md) — älä opettele niitä ennen kuin kokoelma on tuttu.

## Yhteenveto

- Yksi muuttuja, monta arvoa. Indeksi alkaa nollasta.
- Taulukko: kiinteä koko, `Length`. Rinnakkainen taulukko luodaan muodossa `new int[toinen.Length]`.
- List: `Add`, `Count`, koko kasvaa. Luo lista silmukan ulkopuolelle, jos sen pitää kertyä. Ei `Remove`-kutsua `foreach`-silmukan sisällä.
- Dictionary: avain → arvo, tarkista `ContainsKey`. Avain huomioi kirjainkoon.
- `foreach` lukee. `for` kun tarvitset indeksin tai kirjoitat lokeroon.
- Pienimmän arvon haku alkaa ensimmäisestä alkiosta, ei nollasta.

Seuraavaksi: [Ohjausrakenteet](Control-Structures.md) · [Funktiot ja metodit](Functions-and-Methods.md) · [JSON](JSON.md)
