# Konsolin syöte ja tulostus (Console I/O)

Konsolisovellus keskustelee käyttäjän kanssa tekstillä: se **tulostaa** viestejä ja **lukee** vastauksia. C#:ssa tähän käytetään `Console`-luokkaa.

Arjen esimerkki: kassan näyttö ja näppäimistö. Ohjelma kirjoittaa kysymyksen. Ihminen vastaa. Vastaus on aina tekstiä, kunnes muutat sen luvuksi.

**Microsoft:** [Console class](https://learn.microsoft.com/fi-fi/dotnet/api/system.console)

## Kolme metodia, jotka riittävät pitkälle

| Metodi | Mitä tekee | Rivinvaihto |
|--------|------------|-------------|
| `Console.WriteLine("teksti")` | Tulostaa tekstin ja siirtyy seuraavalle riville | Kyllä |
| `Console.Write("teksti")` | Tulostaa tekstin ja jättää kursorin samalle riville | Ei |
| `Console.ReadLine()` | Lukee käyttäjän kirjoittaman rivin **tekstinä** (`string`) | — |
| `Console.ReadKey(true)` | Lukee yhden näppäimen ilman Enteriä (myöhemmin tällä sivulla) | — |
| `Console.KeyAvailable` | `true`, jos näppäintä on painettu; ei odota | — |

```csharp
Console.WriteLine("=== Elokuvateatteri Tähti ===");
Console.WriteLine();                          // tyhjä rivi
Console.Write("Anna ikäsi: ");                // kursori jää odottamaan samalle riville
string? input = Console.ReadLine();
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

Jos syöte ei ole luku, `Convert.ToInt32` kaataa ohjelman `FormatException`-poikkeukseen. `int.TryParse` palauttaa sen sijaan `false`, ja `while`-silmukka kysyy luvun uudelleen: [TryParse](Casting.md#tryparse--kysy-uudelleen).

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

`:F2` pyöristää vain **tulostuksen** — muuttujan arvo ei muutu. Jos arvo pitää pyöristää oikeasti (tallennus, yhteenlasku), käytä `Math.Round` — katso [Math-luokka](Math.md).

### Erikoismerkit

Kenoviiva aloittaa merkin, jota ei voi kirjoittaa suoraan:

| Merkki | Mitä tekee |
|--------|------------|
| `\n` | Rivinvaihto |
| `\t` | Sarkain (tabulaattori) |
| `\r` | Kohdistin rivin alkuun, rivi ei vaihdu |
| `\"` | Lainausmerkki merkkijonon sisällä |
| `\\` | Kenoviiva itse (polut: `"C:\\temp"`) |

`Console.WriteLine($"Nimi:\t{name}")` tasaa sarakkeet. `\r` on hyödyllinen laskurissa — katso alla.

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

## Sama rivi uudelleen: \r

Laskuri, joka päivittyy paikallaan sen sijaan, että konsoli täyttyisi sadoista riveistä:

```csharp
for (int percent = 0; percent <= 100; percent += 5)
{
    Console.Write($"\rLadataan... {percent} %");
    Thread.Sleep(100);
}

Console.WriteLine();   // vasta lopuksi uudelle riville
```

`\r` siirtää kohdistimen rivin alkuun vaihtamatta riviä. `Write` ei vaihda riviä, toisin kuin `WriteLine`. Yhdessä ne kirjoittavat uuden tekstin vanhan päälle. `WriteLine` silmukan sisällä tekisi joka kierroksesta uuden rivin. Tauko: [Thread.Sleep](Thread-Sleep.md).

`\r` **ei tyhjennä riviä**. Jos uusi teksti on lyhyempi kuin edellinen, vanhan rivin häntä jää näkyviin: `Ladataan... 100 %` ja sen päälle `Ladataan... 5 %` näyttää `Ladataan... 5 % %`. Korjaus on tasata teksti samanmittaiseksi:

```csharp
Console.Write($"\rKierros {round}, voitot {wins} €".PadRight(30));
```

`PadRight(30)` täyttää lopun välilyönneillä 30 merkkiin asti, jolloin vanha teksti peittyy kokonaan.

## Näppäin ilman Enteriä: ReadKey ja KeyAvailable

`ReadLine` pysähtyy odottamaan Enteriä. Jatkuva peli tai sekuntikello ei voi pysähtyä joka kierroksella, joten näppäin tarkistetaan odottamatta:

```csharp
bool stop = false;

while (!stop)
{
    // yksi kierros: tulosta aika tai arvo, pieni tauko

    if (Console.KeyAvailable)                        // onko näppäintä painettu? ei odota
    {
        ConsoleKeyInfo key = Console.ReadKey(true);  // true = merkkiä ei tulosteta
        if (key.Key == ConsoleKey.Q)
        {
            stop = true;
        }
    }
}
```

`Console.KeyAvailable` on `true`, jos näppäimistöpuskurissa on painallus. Se ei jää odottamaan. `ReadKey(true)` ottaa painalluksen pois puskurista ja palauttaa `ConsoleKeyInfo`-arvon. `key.Key` on näppäin (`ConsoleKey.Q`, `ConsoleKey.Enter`), `key.KeyChar` on sama merkkinä (`'q'`).

Helpompi, myös sallittu tapa: kysy `Console.ReadLine()` jokaisen kierroksen jälkeen ja lopeta, jos vastaus on `x`. Silloin ohjelma pysähtyy odottamaan Enteriä joka kierroksella.

## Yhteenveto

- `WriteLine` tulostaa rivin, `Write` jättää kursorin samalle riville, `ReadLine` lukee tekstin
- Syöte on aina `string` — luvuksi tarvitaan `Convert.ToInt32` tai vastaava
- `$"...{muuttuja:F2}..."` upottaa arvot ja muotoilee desimaalit
- Merkkijonoja verrataan `==`-operaattorilla; kirjainkoko merkitsee
- `Console.Write($"\r...")` päivittää saman rivin; `PadRight` peittää vanhan hännän
- `Console.KeyAvailable` + `ReadKey(true)` lukee näppäimen ilman Enteriä ja odottamatta

Seuraavaksi: [Muuttujat](Variables.md) · [Tyyppimuunnokset](Casting.md) · [Ohjausrakenteet](Control-Structures.md)
