# Yleisiä vinkkejä Visual Studion käyttöön

Visual Studio on tehokas IDE (Integrated Development Environment) C#-ohjelmointiin. Tässä on hyödyllisiä vinkkejä sen käyttöön.

## Miten ajaa projekteja

Visual Studiossa olevia projekteja voi ajaa muutamalla eri tavalla:

1. **Vihreä ajo-nappi**: Painamalla vihreää ajo-nappia, joka löytyy ylhäältä työkaluriviltä
2. **F5**: Voit myös halutessasi painaa **F5**, joka ajaa saman asian kuin yllä olevan napin painaminen

### Debug vs Release

- **Debug**: Käynnistää ohjelman debug-tilassa (voit debugata)
- **Release**: Versio, jota ei voi debugata. Release-versio on aina, joka annetaan asiakkaalle tai ohjelma joka pyörii oikeassa ympäristössä

Valitse ylhäältä työkaluriviltä Debug tai Release -moodi.

## Ajettavan projektin vaihto

### Mistä tietää mikä projekti on valittu

Visual Studion solutionissa voi olla useampi projekti. Valittu projekti näkyy:
- Projektin nimi on **boldattu** Solution Explorerissa
- Ylhäältä löytyvästä palkista, josta projekteja ajetaan

### Miten vaihtaa projekti

Voit vaihtaa projektin muutamalla eri tavalla:

1. **Vetovalikosta**: Valitse ylhäältä vetovalikosta eri projekti
2. **Oikea hiiren nappi**: Painamalla halutun projektin päällä oikealla hiiren napilla ja valitsemalla **Set as Startup Project**

## Projektin kääntäminen

### Build

Kun suoritat **Build** (kääntäminen) toiminnon tietylle projektille tai ratkaisulle (solution) Visual Studiossa, IDE tarkistaa, onko koodissa tapahtunut muutoksia viimeisen käännöksen jälkeen. Jos muutoksia on tapahtunut, Visual Studio kääntää vain ne tiedostot, jotka ovat muuttuneet (ja mahdollisesti niistä riippuvaiset tiedostot).

**Build vaihtoehdot löydät ylhäältä löytyvästä valikosta nimeltä Build**

- Tämä on tehokasta, koska se nopeuttaa käännösaikaa, erityisesti suurissa projekteissa. Sinun ei tarvitse kääntää koko projektia uudelleen, jos vain yksi tai muutama tiedosto on muuttunut.
- Jos käännöksessä havaitaan virheitä, ne näytetään **Error List** -ikkunassa, ja voit korjata ne ennen ohjelman suorittamista.

### Rebuild All

**Rebuild All** (uudelleenrakennus) toiminto tekee periaatteessa kaksi asiaa:
1. Ensin se suorittaa **Clean** toiminnon, joka poistaa kaikki aikaisemmat käännöstiedostot (kuten objektitiedostot ja lopulliset binääritiedostot)
2. Sen jälkeen se rakentaa koko ratkaisun uudelleen alusta alkaen

Tämä tarkoittaa, että kaikki projektin tiedostot käännetään uudelleen, riippumatta siitä, ovatko ne muuttuneet vai eivät.

Tätä toimintoa voi olla hyvä käyttää, jos kohtaat ongelmia, jotka saattavat johtua vanhoista käännöstiedostoista tai jos haluat varmistaa, että koko projekti on konsistentti ja rakentuu puhtaalta pöydältä.

### Clean Solution

Visual Studiossa **Clean Solution** (puhdista ratkaisu) on toiminto, joka poistaa kaikki käännöksen aikana syntyneet väliaikaiset tiedostot ja lopulliset binääritiedostot (kuten `.exe`, `.dll` ja muut tiedostot) projektista tai koko ratkaisusta (solution).

**Clean Solution** -toiminnon tarkoituksena on:

1. **Levytilan vapauttaminen**: Poistamalla väliaikaiset tiedostot voit vapauttaa levytilaa.
2. **Ongelmien ratkaiseminen**: Joskus käännöksen tai linkityksen aikana voi syntyä ongelmia, jotka johtuvat vanhoista tai korruptoituneista väliaikaistiedostoista. Näissä tapauksissa **Clean Solution** voi auttaa poistamaan vanhat tiedostot, jolloin voit rakentaa ratkaisun uudelleen puhtaalta pöydältä.
3. **Riippuvuuksien varmistaminen**: Joskus on hyödyllistä varmistaa, että kaikki osat ratkaisusta kääntyvät oikein ja riippuvuudet ovat kunnossa. Tämä on helpompi tehdä, kun kaikki vanhat tiedostot on ensin poistettu.

**Huomio**: **Clean Solution** ei tee muutoksia itse lähdekoodiisi tai muihin projektiin kuuluviin resursseihin. Se kohdistuu vain käännöksen ja linkityksen aikana syntyneisiin tiedostoihin.

## IntelliSense

IntelliSense on koodin kirjoittamisen avustusominaisuus, joka on integroitu moniin Microsoftin kehitysympäristöihin, kuten Visual Studioon. Se auttaa kehittäjiä kirjoittamaan koodia nopeammin ja virheettömämmin tarjoamalla eri koodiehdotuksia heidän kirjoittaessaan.

**HUOM!** Aina ehdotus ei ole oikea tai paras mahdollinen.

### IntelliSensen pääominaisuudet

1. **Koodin täydennys**: Kun kirjoitat koodia, IntelliSense näyttää ehdotuksia luokista, funktioista, muuttujista ja muista nimetyistä kohteista, jotka voivat täsmätä siihen, mitä olet kirjoittamassa (vähän niinkuin ennakoiva tekstintäyttö). Voit valita ehdotetun kohteen painamalla **Enter** ja se täydentää koodin puolestasi. Ehdotus näkyy aina **harmaana**!

2. **Parametri-informaatio**: Kun kutsut funktiota tai metodia, IntelliSense näyttää saatavilla olevat parametrit ja niiden tyypit, jotta voit tietää mitä argumentteja sille pitäisi antaa.

3. **Quick Info**: Kun viet hiiren koodissa olevan objektin päälle, IntelliSense näyttää pienen infoikkunan, joka sisältää tietoa kyseisestä objektista, kuten sen tyyppi tai kuvaus.

4. **Luettelo jäsenistä**: Kun kirjoitat pistettä objektin jälkeen, IntelliSense näyttää luettelon kyseisen objektin metodeista, ominaisuuksista ja muista jäsenistä.

5. **Värin koodaus ja korostus**: Tämä auttaa erottamaan erilaiset koodin osat toisistaan, kuten muuttujat, luokat ja avainsanat.

## Pikanäppäimet

### Koodin muokkaaminen

- **Ctrl + X** / **Ctrl + C** / **Ctrl + V** - Leikkaa / kopioi / liitä
- **Ctrl + Z** / **Ctrl + Y** - Kumoa / tee uudelleen
- **Ctrl + K** → **Ctrl + C** - Kommentoi valittu koodi
- **Ctrl + K** → **Ctrl + U** - Poista kommentointi valitusta koodista
- **Ctrl + Space** - Koodin täydennys / IntelliSense
- **Ctrl + .** - Näyttää pikatoimenpiteet ja korjaukset

### Navigointi

- **F12** - Siirry määrittelyyn
- **Shift + F12** - Näytä kaikki viittaukset
- **Ctrl + -** / **Ctrl + Shift + -** - Siirry taaksepäin / eteenpäin navigoinnissa
- **Ctrl + T** tai **Ctrl + ,** - Etsi kaikista tiedostoista (Solution Explorerin pikahaku)

### Koodin muotoilu

- **Ctrl + K** → **Ctrl + D** - Muotoile koko tiedosto
- **Ctrl + K** → **Ctrl + F** - Muotoile valittu koodi

### Koodin kääntäminen ja suorittaminen

- **F5** - Aloita (käännä ja suorita)
- **Ctrl + F5** - Aloita ilman virheenkorjausta
- **Shift + F5** - Lopeta virheenkorjaus
- **F9** - Aseta tai poista katkaisupiste (breakpoint)

### Ikkunoiden hallinta

- **Ctrl + M** → **Ctrl + O** - Minimoi tai laajenna kaikki koodilohkot
- **Ctrl + Alt + L** - Siirry Solution Exploreriin
- **Ctrl + W** → **Ctrl + S** - Avaa/halkeama ikkunat

### Tiedostojen hallinta

- **Ctrl + Shift + A** - Lisää uusi tiedosto projektiin
- **Ctrl + O** - Avaa tiedosto
- **Ctrl + S** - Tallenna tiedosto
- **Ctrl + Shift + S** - Tallenna kaikki

### Debuggaus

- **F9** - Lisää breakpoint
- **F10** - Aja ohjelma seuraavalle riville (Step Over)
- **F11** - Hyppää funktion sisälle debuggaamaan (Step Into)
- **Shift + F11** - Hyppää pois suoritettavasta funktiosta (Step Out)
- **Ctrl + F10** - Ajaa ohjelman valitulle riville (Run to cursor)

## Yhteenveto

Visual Studio tarjoaa monia työkaluja, jotka helpottavat ohjelmointia:

- **IntelliSense** auttaa kirjoittamaan koodia nopeammin
- **Pikanäppäimet** nopeuttavat työskentelyä
- **Build/Rebuild/Clean** auttavat projektin hallinnassa
- **Debug-työkalut** auttavat virheiden löytämisessä

## Hyödyllisiä linkkejä

- [Productivity guide - Visual Studio (Windows) | Microsoft Learn](https://learn.microsoft.com/en-us/visualstudio/ide/productivity-features?view=vs-2022)
- [Visual Studio Keyboard Shortcuts Cheat Sheet](https://learn.microsoft.com/en-us/visualstudio/ide/default-keyboard-shortcuts-in-visual-studio)

Seuraavaksi: [Muuttujat](Variables.md)
