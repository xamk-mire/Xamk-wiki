# Operaattorit

**Operaattori** on merkki, joka tekee laskun, vertailun tai sijoituksen. Ikäluokan päättely, syötteen tarkistus ja kertymämuuttujat rakentuvat näistä.

Lue ehto ääneen: `age < 12` on *"onko ikä alle 12?"*. Tulos on `true` tai `false`. Sitä käytetään [ohjausrakenteissa](Control-Structures.md).

## Kartta

| Laji | Merkit | Käyttö |
|------|--------|--------|
| Lasku | `+ - * / %` | Hinta, määrä, jakojäännös |
| Vertailu | `== != < > <= >=` | `if` ja silmukan ehto |
| Logiikka | `&&` `\|\|` `!` | Yhdistä ehdot |
| Sijoitus | `=` `+=` `++` | Arvo, kertymä, laskuri |

## Aritmeettiset operaattorit

| Operaattori | Merkitys | Esimerkki | Tulos |
|-------------|----------|-----------|-------|
| `+` | Yhteenlasku | `12.00m + 7.50m` | `19.50` |
| `-` | Vähennys | `24.00m - 2.40m` | `21.60` |
| `*` | Kertolasku | `12.00m * 2` | `24.00` |
| `/` | Jakolasku | `17 / 5` | `3` (`int`) tai `3.4` (`double`) |
| `%` | Jakojäännös | `17 % 5` | `2` |

### Kokonaislukujako

Kun molemmat puolet ovat `int`, jako katkaisee desimaalit:

```csharp
int jako = 17 / 5;      // 3  — ei 3.4
int jaannos = 17 % 5;   // 2  — 5*3 + 2 = 17
```

Parillisuus testataan jakojäännöksellä: `luku % 2 == 0` on parillinen.

Rahalaskuissa käytä `decimal`-tyyppiä, jotta `12.00m * 2` pysyy tarkkana. Katso [muuttujat](Variables.md#decimal--raha).

## Vertailuoperaattorit

Vertailu tuottaa `bool`-arvon (`true` tai `false`). Sitä käytetään `if`-ehdoissa ja silmukoissa.

| Operaattori | Merkitys | `age = 12` |
|-------------|----------|------------|
| `==` | Yhtä suuri | `age == 12` → `true` |
| `!=` | Erisuuri | `age != 12` → `false` |
| `<` | Pienempi | `age < 12` → `false` |
| `>` | Suurempi | `age > 12` → `false` |
| `<=` | Pienempi tai yhtä suuri | `age <= 12` → `true` |
| `>=` | Suurempi tai yhtä suuri | `age >= 12` → `true` |

**Raja-arvot:** ehto `age < 12` tekee 11-vuotiaasta lapsen ja 12-vuotiaasta aikuisen. Yhden merkin ero (`<` vs `<=`) vaihtaa rajan.

Merkkijonoja verrataan samalla `==`-operaattorilla:

```csharp
if (code == "LEFFA10") { /* alennus */ }
```

Vertailu on **kirjainkokoherkkä**: `"k" == "K"` on `false`, joten jatkokysymykseen vastattu iso `K` ei jatka silmukkaa, joka odottaa pientä `k`-kirjainta. Sama koskee alennuskoodia: `"leffa10"` ei ole `"LEFFA10"`.

## Loogiset operaattorit

Yhdistävät ehtoja.

| Operaattori | Nimi | Tosi kun |
|-------------|------|----------|
| `&&` | JA | **Molemmat** ehdot ovat tosia |
| `\|\|` | TAI | **Vähintään yksi** ehto on tosi |
| `!` | EI | Ehto on epätosi (kääntää arvon) |

```csharp
// Ikä kelpaa, jos se on 0–130
while (age < 0 || age > 130)
{
    Console.WriteLine("Virheellinen ikä.");
}

// Jatketaan, kunnes vastaus on k TAI e — eli kun se EI ole k JA EI ole e
while (answer != "k" && answer != "e")
{
    Console.Write("Vastaa k tai e: ");
    answer = Console.ReadLine();
}

bool isStudent = answer == "k";   // vertailun tulos on suoraan bool
```

| `a` | `b` | `a && b` | `a \|\| b` |
|-----|-----|----------|------------|
| true | true | true | true |
| true | false | false | true |
| false | true | false | true |
| false | false | false | false |

## Sijoitus ja lyhenteet

| Kirjoitus | Sama kuin | Käyttö |
|-----------|-----------|--------|
| `x = 5` | — | Aseta arvo |
| `x += 3` | `x = x + 3` | Kertymä (välisumma, myynti) |
| `x -= 1` | `x = x - 1` | Vähennä |
| `x++` | `x = x + 1` | Laskuri (asiakkaat, kierrokset) |
| `x--` | `x = x - 1` | Laskuri alaspäin |

```csharp
decimal subtotal = 0m;          // alustus ENNEN silmukkaa
subtotal += unitPrice;          // lisää yksi lippu

int customersServed = 0;
customersServed++;              // yksi asiakas lisää
```

Kertymämuuttuja nollataan **silmukan ulkopuolella**. Jos nollaus on sisällä, edelliset kierrokset katoavat.

## Operaattoreiden järjestys

Kertolasku ja jako suoritetaan ennen yhteen- ja vähennyslaskua. Sulut muuttavat järjestyksen:

```csharp
decimal total = subtotal - subtotal * 0.10m;   // ensin kerto, sitten vähennys
decimal total2 = (subtotal - 5m) * 0.10m;      // ensin sulut
```

Vertailut tehdään ennen `&&` / `||`. Kirjoita silti sulut, jos ehto on pitkä — luettavuus voittaa.

## Yhteenveto

- Laskut: `+ - * / %` — `int`-jako katkaisee desimaalit
- Vertailu (`== != < > <= >=`) tuottaa `bool`-arvon
- `&&` vaatii molemmat, `||` riittää yksi
- `+=` kerää summaa, `++` kasvattaa laskuria — alusta ennen silmukkaa

Seuraavaksi: [Ohjausrakenteet](Control-Structures.md) · [Muuttujat](Variables.md)
