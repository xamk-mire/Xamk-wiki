# Konsolin syöte ja tulostus (Console I/O)

Konsolisovellus keskustelee käyttäjän kanssa tekstillä: se **tulostaa** viestejä ja **lukee** vastauksia. C#:ssa tähän käytetään `Console`-luokkaa.

**Microsoftin dokumentaatio:** [Console class](https://learn.microsoft.com/en-us/dotnet/api/system.console)

## Kolme metodia, jotka riittävät pitkälle

| Metodi | Mitä tekee | Rivinvaihto |
|--------|------------|-------------|
| `Console.WriteLine("teksti")` | Tulostaa tekstin ja siirtyy seuraavalle riville | Kyllä |
| `Console.Write("teksti")` | Tulostaa tekstin ja jättää kursorin samalle riville | Ei |
| `Console.ReadLine()` | Lukee käyttäjän kirjoittaman rivin **tekstinä** (`string`) | — |

```csharp
Console.WriteLine("=== Elokuvateatteri Tähti ===");
Console.WriteLine();                          // tyhjä rivi
Console.Write("Anna ikäsi: ");                // kursori jää odottamaan samalle riville
string? syote = Console.ReadLine();
```

`Write` sopii kysymyksiin (`Anna ikäsi: `), `WriteLine` otsikoihin ja valmiisiin riveihin.

## Syöte on aina tekstiä

`Console.ReadLine()` palauttaa `string?` — ei lukua. Käyttäjä voi kirjoittaa `20` tai `abc`; molemmat ovat merkkijonoja, kunnes muunnat ne.

```
Käyttäjä kirjoittaa:  2 0 ↵
        ↓
Console.ReadLine()  →  "20"   (string — tällä ei voi laskea)
        ↓
Convert.ToInt32()   →   20    (int — tällä voi laskea)
```

```csharp
Console.Write("Kuinka monta lippua ostat? ");
int ticketCount = Convert.ToInt32(Console.ReadLine());
```

Jos syöte ei ole luku, ohjelma kaatuu `FormatException`-poikkeukseen. Se on normaalia — lue [poikkeuksen tyyppi ja rivinumero](Exception-Handling.md#virheilmoituksen-lukeminen). Turvallinen vaihtoehto (`TryParse`) opitaan myöhemmin.

> **Miksi `string?`?** Kysymysmerkki tarkoittaa, että arvo voi olla myös `null` ("ei mitään"). `ReadLine` on määritelty näin. Tyhjä Enter tuottaa tyhjän merkkijonon `""`.

Lisää muunnoksista: [Tyyppimuunnokset](Casting.md).

## Merkkijonointerpolaatio

`$`-alkuisessa merkkijonossa aaltosulkeisiin voi upottaa muuttujia:

```csharp
string category = "Aikuinen";
decimal unitPrice = 12.00m;
int ticketCount = 2;

Console.WriteLine($"Ikäluokka: {category}");
Console.WriteLine($"Liput: {ticketCount} x {unitPrice:F2} €");
```

### Numeroiden muotoilu: `:F2`

Rahasummat tulostetaan kahdella desimaalilla. Muotoilukoodi `:F2` tekee sen:

```csharp
decimal total = 21.6m;
Console.WriteLine($"Maksettavaa: {total:F2} €");
// Tulostaa: Maksettavaa: 21,60 €
```

| Koodi | Merkitys | Esimerkki (`12.5`) |
|-------|----------|---------------------|
| `{arvo}` | Oletusmuoto | `12,5` |
| `{arvo:F2}` | Kaksi desimaalia | `12,50` |
| `{arvo:F0}` | Ei desimaaleja | `13` (pyöristetty) |

Suomalaisessa Windowsissa desimaalierotin on **pilkku** konsolissa. Koodissa käytetään aina **pistettä**: `12.50m`.

## Tyhjä syöte ja merkkijonovertailu

Alennuskoodi on valinnainen — tyhjä rivi tarkoittaa "ei koodia":

```csharp
Console.Write("Anna alennuskoodi (tyhjä = ei koodia): ");
string? code = Console.ReadLine();

if (code == "LEFFA10")
{
    Console.WriteLine("Alennus myönnetty.");
}
else if (code != "")
{
    Console.WriteLine("Tuntematon koodi.");
}
```

Vertailu `==` on **kirjainkoosta riippuvainen**: `"LEFFA10"` ja `"leffa10"` ovat eri merkkijonoja. Kirjainkoosta riippumaton vertailu onnistuu esimerkiksi muuttamalla merkkijonon isoiksi kirjaimiksi: `code.ToUpper()`.

## Kyllä/ei-kysymys

```csharp
Console.Write("Palvellaanko seuraava asiakas (k/e)? ");
string? answer = Console.ReadLine();

if (answer == "k")
{
    // jatka
}
```

Hyväksy vain `k` tai `e` [while-silmukalla](Control-Structures.md) — muuten vastaus `x` tulkitaan helposti "ei".

## Yhteenveto

- `WriteLine` tulostaa rivin, `Write` jättää kursorin samalle riville, `ReadLine` lukee tekstin
- Syöte on aina `string` — luvuksi tarvitaan `Convert.ToInt32` tai vastaava
- `$"...{muuttuja:F2}..."` upottaa arvot ja muotoilee desimaalit
- Merkkijonoja verrataan `==`-operaattorilla; kirjainkoko merkitsee

Seuraavaksi: [Muuttujat](Variables.md) · [Tyyppimuunnokset](Casting.md) · [Ohjausrakenteet](Control-Structures.md)
