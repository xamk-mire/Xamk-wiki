# Math-luokka (Math class)

**`Math`** on valmis staattinen luokka, jossa on laskennan apumetodit: pyöristys, ylös- ja alaspyöristys, suurin ja pienin, itseisarvo, potenssi ja neliöjuuri. Sitä ei luoda `new`-sanalla — metodit kutsutaan luokan nimellä: `Math.Round(x, 2)`.

Arjen esimerkki: kassakone näyttää hinnan kahdella desimaalilla, mutta sen muistissa alennus voi olla `2,475 €`. Jos kuitille tulostetaan `2,48` ja tiedostoon tallennetaan `2,475`, huomisen raportti ei täsmää senttiin. `Math.Round` pyöristää **arvon**, ei vain näyttöä.

Tyypillinen tilanne: keskihinta `19,50 / 3 = 6,5`, mutta `10 / 3 = 3,3333…`. `:F2` näyttää `3,33`, mutta muuttuja on yhä `3,3333…`. `Math.Round(x, 2)` tekee siitä oikeasti `3,33`.

**Microsoft:** [Math class](https://learn.microsoft.com/en-us/dotnet/api/system.math) — kaikki metodit listana; tämä sivu kattaa ne, joita tarvitset alussa.

## Kartta

| Kutsu | Mitä tekee | Esimerkki |
|-------|------------|-----------|
| `Math.Round(x)` | Lähimpään kokonaislukuun | `Math.Round(3.7)` → `4` |
| `Math.Round(x, 2)` | Kahteen desimaaliin | `Math.Round(3.3333m, 2)` → `3,33` |
| `Math.Round(x, 2, MidpointRounding.AwayFromZero)` | Puolikas aina pois nollasta ("koulupyöristys") | `Math.Round(2.5, …)` → `3` |
| `Math.Ceiling(x)` | Ylöspäin lähimpään kokonaislukuun | `Math.Ceiling(1.2)` → `2` |
| `Math.Floor(x)` | Alaspäin lähimpään kokonaislukuun | `Math.Floor(1.8)` → `1` |
| `Math.Max(a, b)` / `Math.Min(a, b)` | Suurempi / pienempi | `Math.Max(3, 8)` → `8` |
| `Math.Abs(x)` | Itseisarvo (etumerkki pois) | `Math.Abs(-5)` → `5` |
| `Math.Pow(a, b)` / `Math.Sqrt(x)` | Potenssi / neliöjuuri (`double`) | `Math.Sqrt(16)` → `4` |

Kaikki metodit ovat `static`: `Math` on luokka, josta ei tehdä olioita. Sama idea kuin omassa `ReadInt`-metodissa — katso [Staattiset luokat ja metodit](Static-Classes-and-Methods.md).

## Pyöristys — Math.Round

```csharp
decimal third = 10m / 3;                    // 3,3333333333333333333333333333
decimal rounded = Math.Round(third, 2);     // 3,33

Console.WriteLine(third);                   // 3,3333333333333333333333333333
Console.WriteLine(rounded);                 // 3,33
```

Toinen parametri on desimaalien määrä. Ilman sitä pyöristetään kokonaislukuun. `Math.Round` **palauttaa uuden arvon** — alkuperäinen muuttuja ei muutu, ellet sijoita tulosta takaisin:

```csharp
decimal price = 12.345m;
Math.Round(price, 2);          // tulos heitetään pois — price on yhä 12,345
price = Math.Round(price, 2);  // nyt price on 12,34
```

`Math.Round` toimii sekä `decimal`- että `double`-tyypillä. Rahalle käytä `decimal`-tyyppiä — katso [muuttujat](Variables.md#decimal--raha).

## Puoliväli — pankkiiripyöristys

Tämä yllättää kaikki kerran:

```csharp
Console.WriteLine(Math.Round(2.5));   // 2
Console.WriteLine(Math.Round(3.5));   // 4
Console.WriteLine(Math.Round(4.5));   // 4
```

Kun luku on **tasan puolivälissä**, `Math.Round` pyöristää **parilliseen** kokonaislukuun. Tätä sanotaan pankkiiripyöristykseksi (banker's rounding). Syy: pitkässä sarjassa puolikkaat eivät pyöristy aina ylös, joten summan virhe ei kasva yhteen suuntaan. Sama koskee desimaaleja: `Math.Round(2.345m, 2)` on `2,34` (4 on parillinen), `Math.Round(2.355m, 2)` on `2,36`.

Koulussa opittu tapa "puolikas aina ylös" on `MidpointRounding.AwayFromZero`:

```csharp
Console.WriteLine(Math.Round(2.5, MidpointRounding.AwayFromZero));        // 3
Console.WriteLine(Math.Round(2.345m, 2, MidpointRounding.AwayFromZero));  // 2,35
```

Kumpi on oikein? Rahassa kumpikin käy, kunhan **sama tapa on koko ohjelmassa**. Jos kuitti pyöristää yhdellä tavalla ja raportti toisella, sentit eroavat.

## :F2 vai Math.Round?

| | `{x:F2}` | `Math.Round(x, 2)` |
|--|----------|---------------------|
| Mitä muuttaa | Vain tulostettavan **merkkijonon** | **Arvon** |
| Muuttuja jälkeen | Ennallaan (`3,3333…`) | Pyöristetty (`3,33`), jos sijoitat tuloksen |
| Puoliväli | Pois nollasta: `2,345` → `2,35` | Parilliseen: `2,345` → `2,34` |
| Milloin | Kun näytät käyttäjälle | Kun arvo tallennetaan, lasketaan yhteen tai verrataan |

Sääntö: **pyöristä kerran, siinä kohdassa missä arvo syntyy, ja käytä pyöristettyä arvoa kaikkialla.** Kassassa alennus pyöristetään `Math.Round`-kutsulla heti, ja sama arvo menee kuitille, tiedostoon ja raporttiin. `:F2` on sen jälkeen vain varmistus, että näytöllä on kaksi desimaalia.

Jos pyöristät vain `:F2`-muotoilulla, kaksi erikseen pyöristettyä lukua voivat summautua väärin: `4,125` → `4,13` ja `12,375` → `12,38`, yhteensä `16,51`, vaikka alkuperäinen summa oli `16,50`.

## Ylös ja alas — Ceiling ja Floor

`Ceiling` pyöristää aina ylöspäin, `Floor` aina alaspäin — riippumatta desimaaleista.

```csharp
int minutes = 95;
double hours = minutes / 60.0;              // 1,5833…
Console.WriteLine(Math.Ceiling(hours));     // 2 — kaksi täyttä tuntia varataan
Console.WriteLine(Math.Floor(hours));       // 1 — yksi kokonainen tunti kului
Console.WriteLine(Math.Round(hours));       // 2
```

Tyypillisiä käyttöjä: montako sivua tarvitaan 23 tulokselle, kun sivulla on 10 (`Ceiling(23 / 10.0)` = 3); montako kokonaista pakettia saldosta riittää (`Floor`).

Paluutyyppi on `double` (tai `decimal`), vaikka arvo on kokonainen. Jos tarvitset `int`-tyypin, muunna: `int pages = (int)Math.Ceiling(23 / 10.0);` — cast on turvallinen, koska desimaaleja ei enää ole. Katso [tyyppimuunnokset](Casting.md).

## Kokonaislukujako ennen pyöristystä

Yleisin virhe `Math`-luokan kanssa ei ole `Math`-luokassa:

```csharp
int minutes = 95;
Console.WriteLine(Math.Ceiling(minutes / 60));     // 1 — väärin!
Console.WriteLine(Math.Ceiling(minutes / 60.0));   // 2 — oikein
```

`95 / 60` on kokonaislukujako ja antaa `1` jo ennen kuin `Ceiling` näkee mitään. Vähintään toisen luvun pitää olla desimaaliluku (`60.0` tai `60m`). Sama asia [tyyppimuunnoksissa](Casting.md#yleisiä-virheitä).

Myös `(int)3.9` ei ole pyöristys — cast **katkaisee** desimaalit (`3`). Pyöristys on aina `Math.Round`.

## Max, Min ja Abs

```csharp
int bigger = Math.Max(3, 8);        // 8
int smaller = Math.Min(3, 8);       // 3
int distance = Math.Abs(-5);        // 5

// Saldo ei saa mennä miinukselle: valitse suurempi nollasta ja laskusta
int stock = Math.Max(0, stock - sold);
```

`Max` ja `Min` korvaavat usein pienen `if`-rakenteen. Kahta useamman luvun suurin lasketaan silmukalla — katso [ennätys](Control-Structures.md#ennätys--suurin-arvo).

## Yhteenveto

- `Math` on staattinen luokka: `Math.Round(x)`, ei `new Math()`.
- `Math.Round(x, 2)` palauttaa pyöristetyn arvon. Sijoita se muuttujaan.
- Puoliväli pyöristyy parilliseen (`2,5` → `2`). `MidpointRounding.AwayFromZero` pyöristää pois nollasta.
- `:F2` muuttaa vain tulostuksen. Tallennettava tai yhteenlaskettava arvo pyöristetään `Math.Round`-kutsulla, kerran.
- `Ceiling` ylös, `Floor` alas, `Max`/`Min` valitsee. Cast `(int)` katkaisee, ei pyöristä.
- Tee jako desimaaliluvulla (`/ 60.0`) ennen pyöristystä.

Seuraavaksi: [Tyyppimuunnokset](Casting.md) · [Staattiset luokat ja metodit](Static-Classes-and-Methods.md) · [Konsolin syöte ja tulostus](Console-IO.md)

## Hyödyllisiä linkkejä

- [Microsoft: Math.Round](https://learn.microsoft.com/en-us/dotnet/api/system.math.round) — kaikki kuormitukset ja esimerkit puolivälistä
- [Microsoft: MidpointRounding](https://learn.microsoft.com/en-us/dotnet/api/system.midpointrounding) — `ToEven`, `AwayFromZero` ja muut tavat
- [Microsoft: Standard numeric format strings](https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-numeric-format-strings) — `F2`, `N2`, `C` ja muut muotoilukoodit
- [Microsoft: decimal](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/floating-point-numeric-types) — miksi raha on `decimal` eikä `double`
- [Wikipedia: Rounding — round half to even](https://en.wikipedia.org/wiki/Rounding#Rounding_half_to_even) — miksi pankkiiripyöristys on olemassa
