# C# Perusteet

Tervetuloa C#-ohjelmoinnin perusteisiin. Tämä osio käsittelee C#-ohjelmoinnin peruskäsitteitä ja työkaluja.

## Sisältö

### Ensimmäinen ohjelma
- [Visual Studio -vinkit](Visual-Studio-Tips.md) — projektin luonti, Ctrl+F5, IntelliSense
- [Konsolin syöte ja tulostus](Console-IO.md) — Write, WriteLine, ReadLine, interpolaatio, `:F2`
- [Muuttujat](Variables.md) — `int`, `decimal` (raha), `string`, `bool`, `const`
- [Operaattorit](Operators.md) — laskut, vertailu, `&&` / `||`, `+=` / `++`
- [Tyyppimuunnokset](Casting.md) — `Convert.ToInt32`, implisiittinen muunnos
- [Ohjausrakenteet](Control-Structures.md) — `if` / `else if` / `else`, ehtojen järjestys
- [Koodauskonventiot](Coding-Conventions.md) — camelCase, PascalCase
- [Debuggaus](Debug.md) — breakpoint (F9), F5 vs Ctrl+F5, F10, Locals

### Metodit ja näkyvyys
- [Funktiot ja metodit](Functions-and-Methods.md) — parametrit, `return`, `void`, kuormitus, Main
- [Näkyvyysalueet](Scopes.md) — Mainin muuttuja ei näy toiselle metodille
- [Staattiset luokat ja metodit](Static-Classes-and-Methods.md) — `static` ja `const`

### Kokoelmat
- [Tietorakenteet](Data-Structures.md) — taulukko, List, Dictionary, indeksi nollasta

### Tietotyypit ja rakenteet
- [Enum](Enum.md)
- [DateTime](DateTime.md)
- [Properties](Properties.md)
- [Access Modifiers](Access-Modifiers.md)

### Virheet, tiedostot ja data
- [Poikkeusten käsittely](Exception-Handling.md) — virheilmoituksen luku, try-catch
- [Tiedostojen luku ja kirjoitus](File-IO.md)
- [JSON](JSON.md)

### Ajattelu ennen koodia
Materiaalit kansiossa [99-General](../99-General/):
- [Algoritmi](../99-General/Algorithm.md) · [Vuokaaviot](../99-General/Flowchart.md) · [Pseudokoodi](../99-General/Pseudocode.md)
- [Ongelmanratkaisu](../99-General/Problem-Solving.md) · [draw.io](../99-General/DrawIO.md)

## Muut sivut (tarpeen mukaan)

- [Koodin kääntäminen](Code-Compilation.md)
- [DateTime](DateTime.md)
- [Region](Region.md)
- [Satunnaisluvut](Random.md)
- [Rekursio](Recursion.md)
- [StopWatch](StopWatch.md) · [Thread.Sleep](Thread-Sleep.md)
- [RegEx](RegEx.md)

### Funktionaalinen ohjelmointi
- [Lambda](Lambda.md) · [Delegaatit](Delegates.md) · [Predikaatit](Predicate.md) · [Closures](Closures.md) · [LINQ](LINQ.md)

## Oppimisjärjestys

1. Visual Studio + konsoli + muuttujat + `if`
2. Silmukat + debuggeri
3. Metodit + näkyvyysalue
4. Taulukko, List, Dictionary
5. Luokat ja propertyt → kapselointi → perinnän alkeet
6. Enum, try-catch, tiedostot + JSON

## Seuraavaksi

- [OOP-konseptit](../02-OOP-Concepts/) — oliot, kapselointi, perintä
- [Edistyneet aiheet](../04-Advanced/) — Web API, testaus, arkkitehtuuri

## Takaisin

- [C#-materiaalit](../) — Takaisin pääsivulle
