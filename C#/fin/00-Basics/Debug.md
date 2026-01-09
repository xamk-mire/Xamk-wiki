# Debug (Virheenetsintä) - Visual Studiossa

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/visualstudio/debugger/debugger-feature-tour?view=vs-2022)

**Debuggaus** tarkoittaa virheenetsintää ohjelmistossa. Kun kirjoitat koodia, on melko yleistä, että koodissa on virheitä (bugit), jotka saavat ohjelman käyttäytymään odottamattomalla tavalla. Debuggaus auttaa sinua paikantamaan ja korjaamaan nämä virheet.

C#-ohjelmoinnissa, kuten monissa muissa ohjelmointikielissä, debuggausta tuetaan erilaisilla työkaluilla. Yksi yleisimmin käytetty kehitysympäristö C#-ohjelmointiin on **Visual Studio**, joka sisältää tehokkaat debuggausominaisuudet.

## 1. Keskeytyspisteet (Breakpoints)

Keskeytyspiste pysäyttää ohjelman suorituksen tietyssä kohdassa. Kun suoritat ohjelman debuggaustilassa, suoritus pysähtyy tälle riville, ja voit tarkastella muuttujien arvoja ja ohjelman tilaa.

### Keskeytyspisteen lisääminen

1. **Hiirellä**: Klikkaa vasemmalla reunalla rivinumeron vieressä olevaa harmaata aluetta. Tämä asettaa punaisen pallon, joka on **breakpoint**.
2. **Näppäimistöllä**: Siirry riville ja paina `F9`
3. **Valikosta**: Debug → Toggle Breakpoint
4. **Oikealla hiiren näppäimellä**: Klikkaa riviä oikealla → Breakpoint

**Muista**: Näitä breakpointteja voi olla niin monta, kuin tarvitset.

### Breakpointin poistaminen

- Paina punaista palloa uudelleen
- Tai paina `F9` rivillä, jossa on breakpoint
- Tai Debug-valikosta: Delete/Disable All Breakpoints (poistaa kaikki kerralla)

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

**Asetus**: 
1. Klikkaa keskeytyspistettä oikealla hiiren näppäimellä
2. Valitse "Condition" tai "Conditions"
3. Kirjoita ehto, esim. `i == 50`

### Breakpointin tunnistaminen

- **Harmaalla reunalla**: Breakpoint voidaan asettaa
- **Punainen pallo**: Breakpoint on aktiivinen
- **Keltainen korostus**: Ohjelma on pysähtynyt tälle riville debug-tilassa

## 2. Käynnistä ohjelma debuggaustilassa

Valitse ylävalikosta "Debug" ja sitten "Start Debugging" tai paina **F5**. Ohjelman suoritus alkaa ja pysähtyy, kun se saavuttaa asettamasi katkaisupisteen.

**Tärkeää**: 
- Valitun arvon täytyy olla **Debug**, jotta voit debugata
- **Release on versio, jota ei voi debugata**. Release-versio on aina, joka annetaan asiakkaalle tai ohjelma, joka pyörii oikeassa ympäristössä.

## 3. Debug-ohjaus

### Tärkeimmät komennot

| Lyöntitaulu | Toiminto | Kuvaus |
|------------|----------|--------|
| Lyöntitaulu | Toiminto | Kuvaus |
|------------|----------|--------|
| `F5` | Continue | Jatkaa suoritusta seuraavaan breakpointtiin |
| `F10` | Step Over | Siirtyy seuraavalle riville (ei mene funktioon) |
| `F11` | Step Into | Mene metodiin ja näe sen sisäinen toteutus |
| `Shift+F11` | Step Out | Poistu metodista ja palaa siihen kohtaan, josta metodia kutsuttiin |
| `Ctrl+Shift+F5` | Restart | Käynnistää debug-tilan uudelleen |
| `Shift+F5` | Stop Debugging | Lopettaa debug-tilan |

### Run To Cursor

Voit myös ajaa debug-tilassa haluttuun kohtaan (riviin) kahdella tavalla:

1. **Vihreä nuoli**: Vie hiiri halutulle riville, ja klikkaa vihreää nuolta, joka ilmestyy rivin kohdalle
2. **Oikea hiiren näppäin**: Klikkaa riviä oikealla → "Run To Cursor"

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

## 4. Tarkasta muuttujat

Kun ohjelma on pysäytetty katkaisupisteeseen, voit tarkastella muuttujien arvoja useilla tavoilla.

### Hover (Hiiren päällä)

Vie hiiri muuttujan päälle debug-tilassa nähdäksesi sen arvon:

```csharp
int age = 25;  // ← Keskeytyspiste täällä
string name = "Matti";
// Vie hiiri age:n päälle → näet arvon 25
```

### Autos Window

Näyttää automaattisesti relevantit muuttujat nykyisessä laajuudessa:

- **Avaa**: `Ctrl+Alt+V, A`
- Visual Studio valitsee automaattisesti tärkeimmät muuttujat (esim. x, y, operation)

### Watch Window

Seuraa muuttujien arvoja:

1. **Avaa**: `Ctrl+Alt+W, 1`
2. **Lisää muuttuja**: 
   - Klikkaa muuttujaa oikealla hiiren näppäimellä → "Add Watch"
   - TAI kirjoita muuttujan nimi Watch-ikkunaan

```csharp
int sum = 0;
for (int i = 0; i < 10; i++)
{
    sum += i;  // Lisää sum Watch-ikkunaan
}
```

**Watch-ikkunan hallinta**:
- **Poista muuttuja**: Klikkaa oikealla hiiren näppäimellä → "Delete Watch"
- **Poista kaikki**: "Clear All"

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

## 5. Debug-valikko

Löydät ylhäältä Debug-nimisen valikon, jonka avaamalla näet myös monia debuggaukseen liittyviä toimintoja. Voit myös täältä ajaa komentoja tarvittaessa.

**Hyödyllisiä toimintoja**:
- **Delete/Disable All Breakpoints**: Poistaa kaikki breakpointit kerralla
- **Windows**: Avaa eri debug-ikkunoita (Watch, Locals, Call Stack, jne.)

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

Debuggaus on taito, joka paranee ajan myötä ja kokemuksen karttuessa. Aluksi se saattaa tuntua hankalalta, mutta käytännön kautta opit tunnistamaan yleisiä ongelmia ja löytämään ratkaisuja niihin nopeammin.

### Keskeiset asiat:

- **Keskeytyspisteet**: Pysäyttävät ohjelman tietyssä kohdassa
- **Debug vs Release**: Debug-tila vaaditaan debuggaukseen
- **Step Over/Into/Out**: Navigoi koodissa
- **Watch Window**: Seuraa muuttujien arvoja
- **Autos Window**: Näyttää automaattisesti relevantit muuttujat
- **Immediate Window**: Suorita koodia debug-tilassa
- **Call Stack**: Näytä metodien kutsuketju
- **Run To Cursor**: Aja haluttuun kohtaan

### Hyödyllisiä linkkejä:

- [Visual Studio Debugging](https://learn.microsoft.com/en-us/visualstudio/debugger/)
- [Run unit tests with Test Explorer](https://learn.microsoft.com/en-us/visualstudio/test/run-unit-tests-with-test-explorer?view=vs-2022)

