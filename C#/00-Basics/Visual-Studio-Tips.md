# Yleisiä vinkkejä Visual Studion käyttöön

Visual Studio on tehokas IDE (Integrated Development Environment) C#-ohjelmointiin. Tässä on hyödyllisiä vinkkejä sen käyttöön.

## Peruslyöntitaulut (Keyboard Shortcuts)

### Tärkeimmät lyöntitaulut

| Lyöntitaulu | Toiminto | Kuvaus |
|------------|----------|--------|
| `F5` | Käynnistä debug | Käynnistää sovelluksen debug-tilassa |
| `Ctrl+F5` | Käynnistä ilman debug | Käynnistää sovelluksen ilman debug-ominaisuuksia |
| `F9` | Toggle Breakpoint | Lisää/poistaa keskeytyspisteen |
| `F10` | Step Over | Siirtyy seuraavalle riville (ei mene funktioon) |
| `F11` | Step Into | Siirtyy funktioon sisään |
| `Shift+F11` | Step Out | Poistuu funktiosta |
| `Ctrl+K, Ctrl+C` | Kommentoi | Kommentoi valitut rivit |
| `Ctrl+K, Ctrl+U` | Poista kommentit | Poistaa kommentit valituilta riveiltä |
| `Ctrl+.` | Quick Actions | Näyttää nopeat toiminnot (esim. using-lause) |
| `Ctrl+Shift+B` | Build | Kääntää projektin |
| `Ctrl+F` | Etsi | Etsii tekstiä tiedostosta |
| `Ctrl+Shift+F` | Etsi kaikista | Etsii tekstiä koko projektista |
| `Ctrl+R, Ctrl+R` | Nimeä uudelleen | Nimeää muuttujan/metodin uudelleen |
| `Ctrl+.` | Quick Fix | Korjaa virheet automaattisesti |

## Koodin automaattinen muotoilu

### Format Document
- **Lyöntitaulu**: `Ctrl+K, Ctrl+D`
- Muotoilee koko dokumentin automaattisesti

```csharp
// Ennen muotoilua:
public class Example{public void Method(){if(true){DoSomething();}}}

// Muotoilun jälkeen:
public class Example
{
    public void Method()
    {
        if (true)
        {
            DoSomething();
        }
    }
}
```

## IntelliSense

Visual Studio tarjoaa automaattisen täydennyksen kirjoitettaessa:

```csharp
// Kirjoita "Con" ja Visual Studio ehdottaa:
// - Console
// - Convert
// - Configuration
// - jne.

Console.WriteLine("Hei maailma!");
```

### IntelliSense-komennot
- `Ctrl+Space`: Pakota IntelliSense-näkyviin
- `Tab`: Hyväksy ehdotus
- `Esc`: Sulje IntelliSense

## Snippetit (Code Snippets)

Snippetit ovat valmiita koodipohjia:

### Yleisimmät snippetit

| Snippet | Lyöntitaulu | Tulos |
|---------|------------|-------|
| `for` | `for` + Tab + Tab | For-silmukka |
| `foreach` | `foreach` + Tab + Tab | Foreach-silmukka |
| `if` | `if` + Tab + Tab | If-lause |
| `try` | `try` + Tab + Tab | Try-catch-lohko |
| `prop` | `prop` + Tab + Tab | Auto-property |
| `propfull` | `propfull` + Tab + Tab | Property get/set |
| `ctor` | `ctor` + Tab + Tab | Konstruktori |

### Esimerkki: for-silmukka

```csharp
// Kirjoita "for" ja paina Tab kahdesti
for (int i = 0; i < length; i++)
{
    // Koodi täällä
}
```

## Debug-ominaisuudet

### Keskeytyspisteet (Breakpoints)

1. **Lisää keskeytyspiste**: Klikkaa vasemmalla reunalla tai paina `F9`
2. **Ehdollinen keskeytyspiste**: Klikkaa oikealla hiiren napilla → Condition

```csharp
// Keskeytyspiste, joka aktivoituu vain kun i == 5
for (int i = 0; i < 10; i++)
{
    Console.WriteLine(i); // Breakpoint täällä, condition: i == 5
}
```

### Immediate Window
- **Avaa**: `Ctrl+Alt+I`
- Voit suorittaa koodia debug-tilassa

### Watch Window
- **Avaa**: `Ctrl+Alt+W, 1`
- Seuraa muuttujien arvoja debug-tilassa

## Projektin hallinta

### Solution Explorer
- **Avaa**: `Ctrl+Alt+L`
- Näyttää projektin rakenteen

### NuGet Package Manager
- **Avaa**: Tools → NuGet Package Manager → Manage NuGet Packages
- Asenna kirjastoja projektiin

### Add Reference
- Klikkaa projektia oikealla → Add → Reference
- Lisää viittauksia muihin projekteihin

## Koodin navigointi

### Go to Definition
- **Lyöntitaulu**: `F12`
- Siirtyy muuttujan/metodin määrittelyyn

### Find All References
- **Lyöntitaulu**: `Shift+F12`
- Näyttää kaikki kohdat, joissa muuttujaa/metodia käytetään

### Navigate Back/Forward
- **Takaisin**: `Ctrl+-`
- **Eteenpäin**: `Ctrl+Shift+-`

## Koodin refaktorointi

### Extract Method
1. Valitse koodi
2. Klikkaa oikealla → Quick Actions → Extract Method

```csharp
// Ennen:
public void ProcessOrder()
{
    // Pitkä koodi...
    decimal total = 0;
    foreach (var item in items)
    {
        total += item.Price * item.Quantity;
    }
    // ...
}

// Jälkeen:
public void ProcessOrder()
{
    decimal total = CalculateTotal(items);
    // ...
}

private decimal CalculateTotal(List<Item> items)
{
    decimal total = 0;
    foreach (var item in items)
    {
        total += item.Price * item.Quantity;
    }
    return total;
}
```

### Rename
- **Lyöntitaulu**: `Ctrl+R, Ctrl+R`
- Nimeää muuttujan/metodin uudelleen kaikkialla

## Hyödyllisiä asetuksia

### Fontin suuruus
- **Suurennus**: `Ctrl+Shift+.`
- **Pienennys**: `Ctrl+Shift+,`

### Dark/Light Theme
- Tools → Options → Environment → General → Color theme

### Line Numbers
- Tools → Options → Text Editor → C# → General → Line numbers

## Yhteenveto

Nämä vinkit auttavat työskentelemään tehokkaammin Visual Studiossa:
- Opi tärkeimmät lyöntitaulut
- Käytä IntelliSensea ja snippettejä
- Hyödynnä debug-ominaisuuksia
- Refaktoroi koodia automaattisesti

Lisätietoja: [Visual Studio Documentation](https://learn.microsoft.com/en-us/visualstudio/)

