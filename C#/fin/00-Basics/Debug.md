# Debug (Virheenetsintä) - Visual Studiossa

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/visualstudio/debugger/debugger-feature-tour?view=vs-2022)

**Debuggaus** tarkoittaa virheenetsintää ohjelmistossa. Kun kirjoitat koodia, on melko yleistä, että koodissa on virheitä (bugit), jotka saavat ohjelman käyttäytymään odottamattomalla tavalla. Debuggaus auttaa sinua paikantamaan ja korjaamaan nämä virheet.

C#-ohjelmoinnissa, kuten monissa muissa ohjelmointikielissä, debuggausta tuetaan erilaisilla työkaluilla. Yksi yleisimmin käytetty kehitysympäristö C#-ohjelmointiin on **Visual Studio**, joka sisältää tehokkaat debuggausominaisuudet.

Kuvakaappaukset ovat Microsoftin [Debugger feature tour](https://learn.microsoft.com/en-us/visualstudio/debugger/debugger-feature-tour)-sivulta (Visual Studio 2022).

## 1. Keskeytyspisteet (Breakpoints)

Keskeytyspiste pysäyttää ohjelman suorituksen tietyssä kohdassa. Kun suoritat ohjelman debuggaustilassa, suoritus pysähtyy tälle riville, ja voit tarkastella muuttujien arvoja ja ohjelman tilaa.

### Keskeytyspisteen lisääminen

1. **Hiirellä**: Klikkaa vasemmalla reunalla rivinumeron vieressä olevaa harmaata aluetta. Tämä asettaa punaisen pallon, joka on **breakpoint**.
2. **Näppäimistöllä**: Siirry riville ja paina `F9`
3. **Valikosta**: Debug → Toggle Breakpoint
4. **Oikealla hiiren näppäimellä**: Klikkaa riviä oikealla → Breakpoint

**Muista**: Näitä breakpointteja voi olla niin monta, kuin tarvitset.

![Breakpoint rivin vasemmassa laidassa](images/dbg-tour-set-a-breakpoint.png)

*Punainen pallo rivinumeron vasemmalla puolella merkitsee aktiivista breakpointia. Klikkaa harmaata palkkia tai paina F9.*

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

![Ehdollisen breakpointin asetukset](images/breakpoint-settings.png)

*Breakpoint Settings: rastita **Conditions** ja kirjoita lauseke (esim. `i == 50`). Silmukka pysähtyy vasta kun ehto on tosi.*

### Breakpointin tunnistaminen

- **Harmaalla reunalla**: Breakpoint voidaan asettaa
- **Punainen pallo**: Breakpoint on aktiivinen
- **Keltainen korostus**: Ohjelma on pysähtynyt tälle riville debug-tilassa

![Keltainen nuoli näyttää pysähtyneen rivin](images/dbg-tour-f11.png)

*Keltainen nuoli ja rivin korostus: suoritus on pysähtynyt tälle riville. Riviä ei ole vielä suoritettu — F10 suorittaa sen ja siirtyy eteenpäin.*

## 2. Käynnistä ohjelma debuggaustilassa

Valitse ylävalikosta "Debug" ja sitten "Start Debugging" tai paina **F5**. Ohjelman suoritus alkaa ja pysähtyy, kun se saavuttaa asettamasi katkaisupisteen.

**Tärkeää**: 
- Valitun arvon täytyy olla **Debug**, jotta voit debugata
- **Release on versio, jota ei voi debugata**. Release-versio on aina, joka annetaan asiakkaalle tai ohjelma, joka pyörii oikeassa ympäristössä.

## 3. Debug-ohjaus

### F5 vai Ctrl+F5?

| Näppäin | Mitä tekee |
|---------|-----------|
| **Ctrl+F5** | Ajaa ohjelman **ilman** debuggeria — konsoli jää auki lopuksi. Arjen ajotapa. |
| **F5** | Ajaa **debuggerilla** — pysähtyy breakpointeihin. Kun etsit vikaa. |

### Tärkeimmät komennot

| Näppäin | Toiminto | Kuvaus |
|---------|----------|--------|
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

![Run to Click -painike koodirivin vieressä](images/dbg-tour-run-to-click-2.png)

*Vihreä nuoli rivin vasemmalla (ympyröity): **Run to Click**. Klikkaa sitä, niin suoritus etenee tuohon riviin asti ilman uutta breakpointia.*

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

![Data tip: muuttujan arvo hiiren alla](images/dbg-tour-data-tips.png)

*Vie hiiri muuttujan päälle: data tip näyttää nykyisen arvon (`amount 5.77`). Nasta-ikonilla arvon voi kiinnittää editoriin.*

### Autos Window

Näyttää automaattisesti relevantit muuttujat nykyisessä laajuudessa:

- **Avaa**: `Ctrl+Alt+V, A`
- Visual Studio valitsee automaattisesti tärkeimmät muuttujat (esim. x, y, operation)

![Autos-ikkuna](images/dbg-tour-autos-window.png)

*Autos-ikkuna näyttää nykyisen ja edellisen rivin muuttujat ilman että niitä lisätään käsin.*

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

![Watch-ikkuna](images/dbg-tour-watch-window.png)

*Watch 1: seuraat itse valitsemiasi muuttujia. Kirjoita nimi riville **Add item to watch**.*

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

![Locals-ikkuna](images/dbg-tour-locals-window.png)

*Locals listaa kaikki paikalliset muuttujat: nimi, arvo ja tyyppi. Alareunan välilehdiltä vaihdat Autos / Locals / Watch.*

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

![Call Stack -ikkuna](images/dbg-tour-call-stack.png)

*Ylin rivi on missä olet nyt (keltainen nuoli). Alla on metodit, joista tultiin — tässä `Credit` kutsuttiin `Main`ista.*

## Poikkeus debuggerissa

Kun ohjelma kaatuu debuggauksen aikana, Visual Studio avaa **Exception Helper** -ikkunan suoraan virheen riville — sama tieto kuin konsolin virheilmoituksessa, mutta luettavammassa muodossa.

![Exception Helper NullReferenceException](images/dbg-tour-exception-helper.png)

*Keltainen nuoli osoittaa rivin. Ikkuna kertoo poikkeuksen tyypin (`NullReferenceException`) ja usein syyn (`str was null.`). Lue ensin tyyppi ja viesti — sitten korjaa.*

Lisää poikkeuksista: [Poikkeusten käsittely](Exception-Handling.md).

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
- [Debugger feature tour](https://learn.microsoft.com/en-us/visualstudio/debugger/debugger-feature-tour) — kuvien lähde
- [Using breakpoints](https://learn.microsoft.com/en-us/visualstudio/debugger/using-breakpoints)

