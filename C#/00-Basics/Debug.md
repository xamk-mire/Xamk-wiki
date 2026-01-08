# Debug (Virheenetsintä)

Debug-työkalut auttavat löytämään ja korjaamaan virheitä koodissa. Visual Studio tarjoaa tehokkaita debug-ominaisuuksia.

## Keskeytyspisteet (Breakpoints)

Keskeytyspiste pysäyttää ohjelman suorituksen tietyssä kohdassa.

### Keskeytyspisteen lisääminen

1. **Hiirellä**: Klikkaa vasemmalla reunalla rivinumeron vieressä
2. **Näppäimistöllä**: Siirry riville ja paina `F9`
3. **Valikosta**: Debug → Toggle Breakpoint

```csharp
public void ProcessData()
{
    int count = 0;  // ← Keskeytyspiste täällä
    
    for (int i = 0; i < 10; i++)
    {
        count += i;
    }
    
    Console.WriteLine(count);
}
```

### Ehdolliset keskeytyspisteet

Keskeytyspiste, joka aktivoituu vain tietyissä olosuhteissa:

```csharp
for (int i = 0; i < 100; i++)
{
    // Keskeytyspiste, joka aktivoituu vain kun i == 50
    ProcessItem(i);
}
```

**Asetus**: Klikkaa keskeytyspistettä oikealla → Condition → `i == 50`

## Debug-ohjaus

### Tärkeimmät komennot

| Lyöntitaulu | Toiminto | Kuvaus |
|------------|----------|--------|
| `F5` | Continue | Jatkaa suoritusta |
| `F10` | Step Over | Siirtyy seuraavalle riville (ei mene funktioon) |
| `F11` | Step Into | Siirtyy funktioon sisään |
| `Shift+F11` | Step Out | Poistuu funktiosta |
| `Ctrl+Shift+F5` | Restart | Käynnistää debug-tilan uudelleen |
| `Shift+F5` | Stop | Lopettaa debug-tilan |

### Step Over vs Step Into

```csharp
public void Method1()
{
    int x = 5;
    int y = 10;
    int result = Add(x, y);  // ← Keskeytyspiste täällä
    Console.WriteLine(result);
}

public int Add(int a, int b)
{
    return a + b;
}
```

- **F10 (Step Over)**: Siirtyy suoraan `Console.WriteLine`-riville, ei mene `Add`-metodiin
- **F11 (Step Into)**: Siirtyy `Add`-metodin sisään

## Muuttujien tarkastelu

### Hover (Hiiren päällä)

Vie hiiri muuttujan päälle debug-tilassa nähdäksesi sen arvon:

```csharp
int age = 25;  // ← Keskeytyspiste täällä
string name = "Matti";
// Vie hiiri age:n päälle → näet arvon 25
```

### Watch Window

Seuraa muuttujien arvoja:

1. **Avaa**: `Ctrl+Alt+W, 1`
2. **Lisää muuttuja**: Kirjoita muuttujan nimi Watch-ikkunaan

```csharp
int sum = 0;
for (int i = 0; i < 10; i++)
{
    sum += i;  // Lisää sum Watch-ikkunaan
}
```

### Immediate Window

Suorita koodia debug-tilassa:

1. **Avaa**: `Ctrl+Alt+I`
2. **Käyttö**: Kirjoita koodia ja paina Enter

```csharp
int x = 5;
int y = 10;
// Immediate Windowissa:
// x + y  → 15
// x = 20  → Muuttaa x:n arvon
```

### Locals Window

Näyttää kaikki paikalliset muuttujat:

- **Avaa**: `Ctrl+Alt+V, L`
- Näyttää automaattisesti kaikki muuttujat nykyisessä laajuudessa

## Call Stack

Näyttää metodien kutsuketjun:

- **Avaa**: `Ctrl+Alt+C`
- Näyttää miten ohjelma päätyi nykyiseen kohtaan

```csharp
public void Method1()
{
    Method2();  // ← Keskeytyspiste
}

public void Method2()
{
    Method3();  // ← Keskeytyspiste
}

public void Method3()
{
    int x = 5;  // ← Keskeytyspiste
}
// Call Stack näyttää: Method3 → Method2 → Method1
```

## Autos Window

Näyttää automaattisesti relevantit muuttujat:

- **Avaa**: `Ctrl+Alt+V, A`
- Visual Studio valitsee automaattisesti tärkeimmät muuttujat

## Debug Console

Näyttää ohjelman tulosteen:

- **Avaa**: `Ctrl+Alt+O`
- Näyttää `Console.WriteLine`-tulosteen

## Ehdollinen debug-koodi

### Debug.Assert

Tarkistaa ehtoja debug-tilassa:

```csharp
using System.Diagnostics;

int age = -5;
Debug.Assert(age >= 0, "Ikä ei voi olla negatiivinen");
```

### Conditional Compilation

Koodi, joka suoritetaan vain debug-tilassa:

```csharp
#if DEBUG
    Console.WriteLine("Debug-tila aktiivinen");
#endif

// Tai
[Conditional("DEBUG")]
public void DebugLog(string message)
{
    Console.WriteLine($"[DEBUG] {message}");
}
```

## Yhteenveto

- **Keskeytyspisteet**: Pysäyttävät ohjelman tietyssä kohdassa
- **Step Over/Into**: Navigoi koodissa
- **Watch Window**: Seuraa muuttujien arvoja
- **Immediate Window**: Suorita koodia debug-tilassa
- **Call Stack**: Näytä metodien kutsuketju

Lisätietoja: [Visual Studio Debugging](https://learn.microsoft.com/en-us/visualstudio/debugger/)

