# Visual Studio -vinkit

**Visual Studio Community** on ohjelma, jossa kirjoitat, ajat ja korjaat C#-koodia. Sitä kutsutaan IDE:ksi (*Integrated Development Environment*): editori, kääntäjä ja debuggeri ovat samassa ikkunassa.

Tämä sivu on Visual Studiota varten. Markdown-tiedostoja luet **VS Codessa** tai **Cursorissa**. Älä sekoita näitä.

**Microsoft:** [Visual Studio -tuottavuus](https://learn.microsoft.com/fi-fi/visualstudio/ide/productivity-features?view=vs-2022)

## Kartta

| Asia | Yksi lause |
|------|------------|
| Console App | Uuden konsoliohjelman malli |
| **Ctrl+F5** | Aja ilman debuggeria — konsoli jää auki |
| **F5** | Aja debuggerilla — pysähtyy punaisiin palloihin |
| Error List | Käännösvirheet ennen ajoa |
| IntelliSense | Lista nimistä, kun kirjoitat `Console.` |
| Solution Explorer | Projektin tiedostot vasemmalla |

## Uuden konsoliprojektin luonti

1. **Create a new project** → hae **Console App**. Kieli on **C#**, ei C++ eikä Visual Basic.
2. Anna nimi, esimerkiksi `MovieTickets`. Frameworkiksi uusin **.NET** (esim. .NET 8).
3. Jätä **"Do not use top-level statements"** tyhjäksi. `Main` voidaan avata myöhemmin itse.
4. Aja **Ctrl+F5** (*Start Without Debugging*). Konsoli jää auki, jotta ehdit lukea tulosteen.

Jos painat pelkkää F5:ttä ilman breakpointia, konsoli voi sulkeutua heti ohjelman lopussa. Siksi arjen ajotapa on Ctrl+F5.

| Näppäin | Käyttö |
|---------|--------|
| **Ctrl+F5** | Normaali ajo — konsoli ei sulkeudu heti |
| **F5** | Debuggeri — breakpointit, F10. Katso [Debuggaus](Debug.md) |

## Punainen alleviivaus ja Error List

Jos koodissa on virhe, Visual Studio näyttää punaisen aaltoviivan. Sama tieto on ikkunassa **View → Error List**.

Käännösvirhe estää ajon. Ohjelma ei käynnisty, ennen kuin Error List on tyhjä. Lue viesti ja rivinumero. Älä arvaa.

Yleisiä ensimmäisiä virheitä: puuttuva `;`, väärin kirjoitettu nimi (`Consol` vs `Console`), sulkeet eri määrässä.

## IntelliSense saa jäädä, tekoäly pois

Kun kirjoitat `Console.` (piste lopussa), aukeaa lista metodeista. Se on **IntelliSense**. Se näyttää nimet. Se ei kirjoita kokonaisia rivejä puolestasi. Pidä se päällä. Avaa lista myös **Ctrl+välilyönti**.

Harmaa "haamuteksti" rivillä on eri asia (IntelliCode / Copilot). Oppimisen ajaksi kytke se pois — kirjoita koodi itse.

- **IntelliCode:** Tools → Options → IntelliCode → poista "Automatically generate code completions"
- **Copilot:** Tools → Options → GitHub → Copilot — vain jos olet kirjautunut GitHubiin

## Solution Explorer ja startup-projekti

Vasemmalla on **Solution Explorer**. Siinä näkyvät projektin tiedostot. `Program.cs` on yleensä se tiedosto, johon kirjoitat ensimmäisen ohjelman.

Solutionissa voi olla useita projekteja. **Lihavoitu** nimi on startup-projekti: se käynnistyy, kun painat Ctrl+F5.

Vaihda startup-projekti näin: klikkaa projektia oikealla → **Set as Startup Project**. Yhdellä projektilla tätä ei tarvita.

## Debug vai Release?

Yläpalkissa on valinta **Debug** / **Release**.

| Tila | Milloin |
|------|---------|
| **Debug** | Harjoittelu ja virheenetsintä. Pidä tämä kurssilla. |
| **Release** | Valmis versio asiakkaalle. Breakpointit eivät toimi samalla tavalla. |

Jos F5 ei pysähdy breakpointtiin, tarkista että tila on Debug.

## Build, Rebuild, Clean — lyhyesti

**Build** kääntää muuttuneet tiedostot. Ctrl+F5 tekee tämän automaattisesti.

Jos ajo käyttäytyy oudosti vanhan käännöksen takia:

1. **Build → Clean Solution** poistaa vanhat `.exe`-tiedostot.
2. **Build → Rebuild Solution** kääntää kaiken uudestaan.

Lähdekoodiisi nämä eivät koske. Älä siivoa, jos Error List jo kertoo oikean rivin.

## Hyödylliset pikanäppäimet alkuun

Älä opettele kaikkia kerralla. Nämä riittävät ensimmäisiin viikkoihin.

| Näppäin | Mitä tekee |
|---------|------------|
| **Ctrl+S** | Tallenna |
| **Ctrl+Z** | Kumoa |
| **Ctrl+K**, sitten **Ctrl+D** | Muotoile koko tiedosto (sisennys kuntoon) |
| **Ctrl+K**, sitten **Ctrl+C** | Kommentoi valitut rivit |
| **Ctrl+K**, sitten **Ctrl+U** | Poista kommentointi |
| **Ctrl+välilyönti** | Avaa IntelliSense |
| **F9** | Lisää tai poista breakpoint |
| **F12** | Siirry metodin määrittelyyn |
| **Ctrl+.** | Ehdota korjausta (esim. puuttuva `using`) |

Debuggauksen F10 / F11: [Debuggaus](Debug.md).

Lisää näppäimiä: [Visual Studion pikanäppäimet](https://learn.microsoft.com/fi-fi/visualstudio/ide/default-keyboard-shortcuts-in-visual-studio).

## Yhteenveto

- Uusi ohjelma: **Console App**, kieli C#, ajo **Ctrl+F5**.
- Punainen viiva = käännösvirhe. Lue Error List.
- IntelliSense auttaa nimissä. Haamutäydennys pois oppimisen ajaksi.
- Debug-tila päälle, kun etsit vikaa. Clean/Rebuild vain jos vanha käännös häiritsee.

Seuraavaksi: [Konsolin syöte ja tulostus](Console-IO.md) · [Muuttujat](Variables.md) · [Debuggaus](Debug.md)
