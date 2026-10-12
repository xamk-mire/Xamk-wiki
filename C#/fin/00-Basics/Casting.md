# Tyyppimuunnokset (Casting)

C# pitää tyypit erillään. Teksti `"20"` ei ole sama asia kuin luku `20`. **Tyyppimuunnos** vaihtaa arvon toiseen tyyppiin, jotta sillä voi laskea, vertailla tai tallentaa.

Arjen esimerkki: kassalla ikä kysytään kirjoittamalla. Näppäimistö antaa merkkejä. Hintaa ei voi kertoa merkeillä. Merkit pitää ensin muuttaa luvuksi.

**Microsoft:** [Casting and conversions](https://learn.microsoft.com/fi-fi/dotnet/csharp/programming-guide/types/casting-and-type-conversions)

## Kartta

| Tilanne | Mitä käytät |
|---------|-------------|
| Käyttäjä kirjoitti iän tai lippumäärän | `Convert.ToInt32(...)` |
| Käyttäjä kirjoitti rahasumman | `Convert.ToDecimal(...)` |
| `int` kerrotaan `decimal`-hinnalla | Ei muunnosta — C# tekee sen itse |
| Desimaalit pois (`3.9` → `3`) | `(int)arvo` — tieto katoaa |
| Syöte voi olla mitä tahansa tekstiä | [`int.TryParse`](#tryparse--kysy-uudelleen) — palauttaa `bool`, kysy uudelleen |

## Konsolin syöte on aina tekstiä

`Console.ReadLine()` palauttaa `string?`. Käyttäjä voi kirjoittaa `20` tai `abc`. Molemmat ovat merkkijonoja, kunnes muunnat ne.

```
Käyttäjä kirjoittaa:  2 0 ↵
        ↓
Console.ReadLine()  →  "20"   (string — tällä ei voi laskea)
        ↓
Convert.ToInt32()   →   20    (int — tällä voi kertoa hinnan)
```

```csharp
Console.Write("Anna ikäsi: ");
int age = Convert.ToInt32(Console.ReadLine());
```

| Metodi | Käyttö |
|--------|--------|
| `Convert.ToInt32(teksti)` | Kokonaisluku: ikä, lippumäärä, valikon numero |
| `Convert.ToDecimal(teksti)` | Rahasumma, jos käyttäjä syöttää hinnan |
| `int.Parse` / `decimal.Parse` | Sama idea, hieman tiukempi `null`-käsittely |
| `int.TryParse` | Ei kaada ohjelmaa — palauttaa `false`, jos teksti ei ole luku |

Väärä teksti (`"abc"`) → `FormatException`. Liian iso luku (`9999999999`) → `OverflowException`. Lue virheilmoituksesta **tyyppi** ja **oman koodin rivi** — [poikkeusten käsittely](Exception-Handling.md#virheilmoituksen-lukeminen).

`Convert.ToInt32` on lyhyempi kirjoittaa, mutta se kaatuu väärästä tekstistä. `TryParse` ei kaadu. Molemmat ovat oikein, kunhan tiedät eron.

## TryParse — kysy uudelleen

`int.TryParse` yrittää muuntaa tekstin luvuksi. Paluuarvo on `bool`: onnistuiko muunnos. Itse luku tallentuu `out`-muuttujaan.

| Syöte | Paluuarvo | `out`-muuttuja |
|-------|-----------|----------------|
| `"20"` | `true` | `20` |
| `"abc"` | `false` | `0` |
| `""` | `false` | `0` |

`Convert.ToInt32("abc")` kaataa ohjelman. `int.TryParse("abc", out age)` palauttaa `false`, ja ohjelma jatkaa.

Yksi kutsu ei riitä, kun ohjelma tarvitsee kelvollisen luvun jatkaakseen. `while`-silmukka kysyy uudelleen, kunnes muunnos onnistuu:

```csharp
Console.Write("Anna ikä: ");
string? text = Console.ReadLine();
int age;
bool ok = int.TryParse(text, out age);

while (!ok)
{
    Console.WriteLine("Anna kokonaisluku.");
    Console.Write("Anna ikä: ");
    text = Console.ReadLine();
    ok = int.TryParse(text, out age);
}
```

Pidä tulos omassa `ok`-muuttujassaan. Ehto `while (!ok)` luetaan silloin: "niin kauan kuin muunnos ei onnistunut".

Huomaa, että `0` on kelvollinen kokonaisluku, joten `TryParse` palauttaa sille `true`. Rajojen tarkistus (`age < 0 || age > 130`) on eri asia kuin muunnoksen onnistuminen, ja se tehdään erikseen. Katso [while](Control-Structures.md#while--toista-niin-kauan-kuin).

## Automaattinen muunnos — pienempi mahtuu isompaan

Kun tietoja ei katoa, C# muuntaa itse. Tätä kutsutaan **implisiittiseksi** muunnokseksi.

`int` mahtuu `decimal`-laskuun. Lippujen määrä kertaa hinta ei vaadi sulkeita eikä `Convert`-kutsua:

```csharp
decimal unitPrice = 12.00m;
int ticketCount = 2;
decimal subtotal = unitPrice * ticketCount;   // 24.00 — C# laajentaa intin
```

Sama suunta numeroissa: `int` mahtuu `long`-tyyppiin, `float` mahtuu `double`-tyyppiin.

```csharp
int small = 10;
long large = small;   // OK, 10 mahtuu
```

Toiseen suuntaan C# **ei** muunna itse. Iso tyyppi ei mahdu pieneen ilman että jotain voi kadota.

## Pakotettu muunnos — sulkeet tyypin edessä

**Eksplisiittinen** muunnos kirjoitetaan `(tyyppi)arvo`. Sinä vastaat seurauksista.

```csharp
double measure = 3.9;
int whole = (int)measure;   // 3 — desimaalit katkaistaan, ei pyöristetä
```

`3.9` ei ole `4`. Cast katkaisee. Jos tarvitset pyöristyksen, käytä `Math.Round`.

Rahasta kokonaislukuun tarvitaan tietoinen muunnos, koska sentit katoaisivat:

```csharp
decimal total = 21.60m;
int eurosOnly = (int)total;   // 21 — sentit pois
```

Älä tee tätä kuitissa. Pidä raha `decimal`-tyypissä. Katso [muuttujat](Variables.md#decimal--raha).

Jos luku ei mahdu kohdetyyppiin, tulos voi olla väärä tai tulla poikkeus. Älä arvaa — kokeile debuggerilla.

## Yleisiä virheitä

**1. Lasku merkkijonolla**

```csharp
string text = "20";
// int next = text + 1;          // ei käänny tai tekee väärin
int next = Convert.ToInt32(text) + 1;   // 21
```

**2. Kokonaislukujako ennen muunnosta**

```csharp
int a = 7;
int b = 2;
double wrong = a / b;           // 3  — jako tapahtuu ensin intteinä
double right = (double)a / b;   // 3.5
```

**3. Suomen pilkku ja `Convert.ToDecimal`**

Koodissa desimaali on piste: `12.50m`. Konsolissa suomalainen Windows odottaa usein pilkkua. Jos käyttäjä kirjoittaa `12.50` suomalaisessa koneessa, muunnos voi kaatua. Tämä on kulttuuriasetus, ei C#:n bugi.

## `as` ja `is` — myöhemmin

Kun käsittelet olioita, `is` kysyy tyyppiä ja `as` yrittää muuntaa ilman kaatumista (`null` jos ei onnistu). Näitä ei tarvita konsoliohjelman alussa. Niihin palataan olio-ohjelmoinnissa.

`Cast<T>` ja `OfType<T>` kuuluvat LINQ-kokoelmiin. Aloita [tietorakenteista](Data-Structures.md), LINQ myöhemmin.

## Yhteenveto

- Syöte on `string`. Luvuksi: `Convert.ToInt32` tai `Convert.ToDecimal`.
- `Convert.ToInt32("abc")` kaataa ohjelman. `TryParse` palauttaa `false`, ja `while (!ok)` -silmukka kysyy uudelleen.
- `int` × `decimal` toimii ilman erillistä muunnosta.
- `(int)3.9` on `3`. Tieto katoaa tahallaan.
- Raha pysyy `decimal`-tyypissä.

Seuraavaksi: [Konsolin syöte ja tulostus](Console-IO.md) · [Muuttujat](Variables.md) · [Poikkeusten käsittely](Exception-Handling.md)
