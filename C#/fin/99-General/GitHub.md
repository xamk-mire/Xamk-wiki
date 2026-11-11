# GitHub (Git)

**Git** on versionhallintatyökalu omalla koneellasi. Se tallentaa koodin historian **commit** kerrallaan, ja voit palata mihin tahansa aiempaan versioon. **GitHub** on palvelu verkossa, joka säilyttää repon kopion ja jonka kautta jaat koodin. Git ei ole GitHub: työkalu toimii ilman palvelua, palvelu on vain kopio.

Arjen esimerkki: commit on tallennettu pelitila, jolla on nimilappu. Push vie pelitilan pilveen, josta sen saa toiselle koneelle.

Tällä kurssilla Gitiä käytetään Visual Studio Communityn (2022 tai 2026) **Git**-valikosta ja **Git Changes** -ikkunasta. Koko kurssin solution on yhdessä Private-repossa, esimerkiksi `csharp-perusteet`.

**Microsoft:** [Version control with Git in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/version-control/git-with-visual-studio) · **GitHub:** [Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world) — tämä sivu riittää alkuun.

## Kartta

| Käsite | Yhdellä lauseella |
|--------|-------------------|
| **Repositorio** (repo) | Kansio, jonka koko muutoshistorian Git muistaa |
| **Commit** | Tallennettu versio kaikista tiedostoista + viesti, joka kertoo mitä muuttui |
| **Push** | Vie paikalliset commitit GitHubiin |
| **Pull** | Hakee GitHubin uudet commitit paikalliseen repoon |
| **Clone** | Repon kopio GitHubista toiselle koneelle, historia mukana |
| **Branch** (haara) | Erillinen kehityslinja; kurssilla käytössä vain oletushaara `main` |
| **Remote** / `origin` | Paikallisen repon tietämä verkko-osoite; `origin` on sen vakionimi |
| **`.gitignore`** | Tekstitiedosto repon juuressa: lista siitä, mitä Git ei ota mukaan |
| **Private** | Repo, jonka näkevät vain sinä ja kutsumasi henkilöt |

Haarat, pull requestit ja merge-konfliktit tulevat jatkokurssilla. Et törmää niihin, kun olet reposi ainoa kirjoittaja.

## Kolme paikkaa

Koodi on kolmessa paikassa, ja sinä päätät, milloin se siirtyy eteenpäin:

```
  Työkansio                 Paikallinen repo              GitHub
  (tiedostot levyllä)       (historia omalla koneella)    (kopio verkossa)
 ┌──────────────────┐      ┌──────────────────┐         ┌──────────────────┐
 │ Program.cs  (M)  │      │ commit 3: Lisää… │         │ commit 3         │
 │ Movie.cs    (A)  │ ───► │ commit 2: Korjaa…│  ────►  │ commit 2         │
 │ ...              │commit│ commit 1: Alku   │  push   │ commit 1         │
 └──────────────────┘      └──────────────────┘         └──────────────────┘
          ◄──────────── undo                    ◄──────── pull
```

| Toiminto | Mihin vaikuttaa | Mikä on tallessa, jos kone hajoaa |
|----------|-----------------|-----------------------------------|
| **Tallennus** (Ctrl+S) | Vain työkansioon | Ei mikään |
| **Commit** | Paikalliseen repoon (historia) | Ei mikään — historia on samalla levyllä |
| **Push** | GitHubiin | Kaikki pushatut commitit |

Tärkein asia: **tallennus ei ole commit, eikä commit ole push.** Vain push suojaa koneen hajoamiselta. Takaisinpäin: **Undo Changes** palauttaa työkansion viimeisimpään committiin, **pull** tuo GitHubin commitit paikalliseen repoon.

Git ei ole OneDrive: muutokset eivät siirry itsestään. Siksi historiassa on vain nimettyjä, toimivia versioita.

## Tilin yhdistäminen

Visual Studio tekee repon GitHubiin puolestasi, mutta sen pitää ensin tietää, kuka olet. Kaksi asetusta, kerran per kone:

1. **GitHub-tili Visual Studioon:** oikean yläkulman profiilikuvake → **Account settings…** → **All Accounts: Add → GitHub** → kirjaudu selaimessa ja paina **Authorize**. Sen jälkeen push ja pull toimivat ilman salasanoja.
2. **Nimi ja sähköposti commiteille:** **Git → Settings** → **Git Global Settings** (uudemmassa versiossa **Source Control → Git Settings → Git Global Config**) → **User Name** ja **Email**. Käytä samaa sähköpostia kuin GitHub-tilissä, niin commitit yhdistyvät profiiliisi.

Nämä ovat eri asiat: tili antaa oikeuden pushata, nimi ja sähköposti leimataan jokaiseen committiin.

Jos **Git**-valikkoa ei ole yläpalkissa, Git for Windows puuttuu: Visual Studio Installer → Modify → Individual components → **Git for Windows**.

## Gitin käyttö Visual Studiossa

Repo luodaan **kerran** koko solutionille: **Git → Create Git Repository…** (sama löytyy oikeasta alareunasta **Add to Source Control**). Ikkunassa:

- vasemmalta **GitHub**
- **Local path:** solutionin kansio (Visual Studio ehdottaa valmiiksi)
- **.gitignore template: Default (VisualStudio)** — pitää `bin/`, `obj/` ja `.vs/` poissa
- **Repository name:** esimerkiksi `csharp-perusteet`
- **Visibility: Private** — koulutehtävässä aina
- **Create and Push**

Yksi nappi tekee paikallisen repon, `.gitignore`-tiedoston, ensimmäisen commitin (`Add project files.`) ja Private-repon GitHubiin. Oikeassa alareunassa näkyy nyt repon nimi ja haara `main`.

Tarkista selaimessa `https://github.com/tunnuksesi/csharp-perusteet`: tiedostot ovat siellä, nimen vieressä lukee **Private**, eikä `bin/`-kansiota ole.

### Git Changes -ikkuna

**View → Git Changes** (Ctrl+0, Ctrl+G). Tämä on arjen työkalu, jonka rakenne ylhäältä alas on: nuolet, viestikenttä, **Commit All** -nappi ja **Changes**-lista.

| Merkki | Tarkoittaa | Milloin |
|--------|------------|---------|
| **M** | Modified — tiedostoa on muokattu | Muutit olemassa olevaa tiedostoa |
| **A** | Added — uusi tiedosto, jota ei vielä ole historiassa | Lisäsit projektin tai luokkatiedoston |
| **D** | Deleted — tiedosto on poistettu | Poistit tiedoston |

Kaksoisklikkaus tiedostolla näyttää rinnakkain, mitä oli ennen ja mitä nyt. Vihreä rivi on lisätty, punainen poistettu.

Rutiini, jonka toistat kymmeniä kertoja viikossa:

1. Muokkaa ja tallenna. Tiedosto ilmestyy **Changes**-listaan.
2. Kirjoita viestikenttään, mitä teit (esimerkiksi `Lisää Movie-luokka`).
3. **Commit All**. Ilmoitus `Commit … created locally` — commit on vain koneellasi.
4. **Nuoli ylös** on push. Sen vieressä lukee **1 outgoing**: yksi commit odottaa viemistä. Pushin jälkeen laskuri on 0.

**Nuoli alas** on pull. Jos sen vieressä lukee **incoming**, GitHubissa on commiteja, joita koneellasi ei ole. Keskimmäinen nuoli on *fetch*: se tarkistaa tilanteen hakematta vielä mitään.

### Muutosten kumoaminen

Oikea nappi tiedostolla **Changes**-listassa → **Undo Changes**. Tiedosto palaa **viimeisimmän commitin** tilaan, ja kaikki sen jälkeen tehdyt muutokset katoavat — myös ne, jotka olisit halunnut pitää.

Siksi commit usein on turvaverkko: kun jokin toimii, committaa, niin Undo palauttaa juuri siihen. Jos commiteja on yksi, Undo palauttaa aamuun.

Kaksi rajoitusta:

- Uudella tiedostolla (**A**) Undo ei ole valittavissa, koska aiempaa versiota ei ole. Poista tiedosto tavallisesti.
- Undo ei tee mitään **jo commitatulle** muutokselle. Commitatun muutoksen peruminen on **Revert** Branch Historyssa (oikea nappi commitilla). Se tekee uuden commitin, joka kumoaa vanhan; historia säilyy. Et tarvitse sitä vielä.

## Git History

**Git → View Branch History** listaa commitit uusin ylinnä: viesti, tekijä, aika ja tunniste. Alimpana on Visual Studion tekemä ensimmäinen commit.

Oikea nappi commitilla → **View Commit Details** näyttää, mitkä tiedostot muuttuivat. Tiedostoa klikkaamalla näet tarkat rivit rinnakkain.

Historia on hyödyllinen vain, jos viestit kertovat jotain. Lista `päivitys`, `päivitys`, `korjaus` ei auta ketään — ei sinua kahden viikon päästä eikä opettajaa palautuksessa.

## Milloin committaat ja millainen on hyvä viesti

**Yksi toimiva osio = yksi commit.** Hyvä hetki on, kun ohjelma kääntyy ja tekee sen, mitä osio pyysi, ja seuraava osio alkaa uudella asialla. Älä committaa rikkinäistä koodia "varmuuden vuoksi": silloin Undo palauttaa rikkinäiseen. Älä myöskään odota koko päivää.

Viesti kertoo **mitä** muuttui ja tarvittaessa **miksi**. Käytäntö: imperatiivi (Lisää, Korjaa, Siirrä, Poista), alle 70 merkkiä, sama kieli koko repossa.

| Huono | Hyvä | Miksi |
|-------|------|-------|
| `päivitys` | `Lisää Movie-luokka ja korvaa string[] movies` | Kertoo *mitä* tehtiin ilman, että pitää avata koodia |
| `korjaus` | `Korjaa alennuksen pyöristys sentteihin` | Kertoo *mikä* korjattiin |
| `Korjasin bugi X:n` | `Korjaa tyhjän alennuskoodin kaatuminen` | Imperatiivi ja nimetty ongelma, ei "bugi X" |
| `asdf` | — | Ei koskaan |

Kenelle hyvästä viestistä on hyötyä:

- **Sinulle kahden viikon päästä**, kun etsit, missä commitissa alennus meni rikki.
- **Opettajalle**, joka näkee historiasta, missä järjestyksessä työ syntyi.
- **Tiimille** jatkokurssilla, kun joku muu lukee muutoksesi ennen yhdistämistä.

## .gitignore — mitä repoon ei laiteta

Repoon kuuluu **lähdekoodi** ja se, mitä ohjelma tarvitsee toimiakseen. Siihen **ei** kuulu se, mitä käännös tai ajo tuottaa — ne syntyvät uudestaan jokaisella koneella.

| Kuuluu repoon | Ei kuulu repoon | Miksi |
|---------------|-----------------|-------|
| `.cs`-tiedostot, `.csproj`, `.sln` / `.slnx` | `bin/`, `obj/` | Käännöksen tulos: `.exe`, `.dll`, välimuistit. Syntyvät uudestaan Ctrl+F5:llä |
| Ohjelman lukemat datatiedostot projektikansiossa (esim. `alennuskoodit.txt`) | `.vs/` | Visual Studion omat asetukset ja välimuistit, eri joka koneella |
| `README.md`, `.gitignore` | Ohjelman ajossa luomat tiedostot (`kuitit.txt` ajokansiossa) | Tuotettu tulos, ei lähde |
| | Salasanat, avaimet, `.env`, `appsettings.Development.json` | Historiasta ei saa pois; Private-repo ei suojaa collaboratoreilta |

**`.gitignore`** on tekstitiedosto repon juuressa. Jokainen rivi on polku tai kuvio, jonka Git ohittaa kokonaan:

```
[Bb]in/
[Oo]bj/
.vs/
```

Hakasulkeet tarkoittavat "iso tai pieni kirjain". Loppukauttaviiva tarkoittaa kansiota.

Visual Studio luo tiedoston valmiiksi, kun pohjaksi valitaan *VisualStudio* repoa luodessa. Tiedosto on pitkä, koska sama pohja kattaa kaikki projektityypit — sinulle tärkeät ovat nuo kolme riviä.

Jos `.gitignore` puuttuu tai siitä puuttuu rivejä, Git Changes -ikkuna näyttää satoja `.dll`-, `.exe`- ja `.json`-tiedostoja `bin\`- ja `obj\`-poluista. Lisää rivit **ennen** committia. Jos kansiot ehtivät jo historiaan, ne pitää poistaa erikseen (`git rm -r --cached bin obj` komentoriviltä) — kysy apua.

Sääntö: **ohjelman tarvitsema syöte kuuluu repoon, ohjelman tuottama tulos ei.** Salaisuuksien käsittely: [Secrets Management](../../../Development-guidelines/Secrets-Management/README.md).

## Clone ja pull — sama repo kahdella koneella

**Clone** tekee repon kopion toiselle koneelle, historia mukana:

1. GitHubissa repon sivulla vihreä **Code**-nappi → **HTTPS** → kopioi osoite (`https://github.com/tunnus/repo.git`).
2. Visual Studiossa **Git → Clone Repository…** (tai aloitusikkunan *Clone a repository*).
3. **Repository location**: liitä osoite. **Path**: kansio, johon kopio tulee. **Clone**.

Kloonattu repo on täysi repo: sama historia, samat tiedostot. `bin/`- ja `obj/`-kansiot puuttuvat — ne syntyvät, kun käännät.

**Pull** hakee GitHubista commitit, joita koneellasi ei vielä ole: **Git → Pull** tai Git Changes -ikkunan **nuoli alas**. Jos nuolen vieressä lukee *incoming*, GitHubissa on jotain uutta.

Kun työskentelet kahdella koneella (koulu ja koti), rutiini on sama molemmilla:

```
pull → työtä → commit → push
```

Jos unohdat pullata ja yrität pushata, GitHub hylkää pushin (*rejected*): siellä on commiteja, joita sinulla ei ole. Ratkaisu: pull ensin, sitten push. Git yhdistää commitit automaattisesti, jos eri rivejä muutettiin. Jos **sama rivi** muutettiin molemmilla koneilla, syntyy *merge-konflikti*, jossa valitset kumpi versio jää. Vältä se pullaamalla aina ennen työn aloitusta.

## Private vai Public ja collaborator

Repo on joko **Public** (kuka tahansa näkee) tai **Private** (vain sinä ja kutsumasi). Koulutehtävä on aina **Private**, koska

- koodi on keskeneräistä ja sisältää kokeiluja, joita ei ole tarkoitettu julkaistaviksi
- tehtävien ratkaisut eivät saa levitä muille opiskelijoille
- portfolio julkaistaan valmiina — kun projekti on kunnossa, näkyvyyden voi vaihtaa.

Jos rasti jäi pois, korjaa GitHubissa: repo → **Settings** → **Danger Zone** → **Change repository visibility** → Private.

Private-repoon annetaan pääsy toiselle lisäämällä hänet **collaboratoriksi**: repo → **Settings** → **Collaborators** → **Add people** → GitHub-tunnus. Hän saa kutsun sähköpostiin.

| Collaborator voi | Collaborator ei voi |
|------------------|---------------------|
| Lukea repon ja historian | Muuttaa näkyvyyttä (Private/Public) |
| Committata ja pushata | Poistaa repoa |
| | Lisätä muita collaboratoreita |

Tällä kurssilla opettajaa **ei** lisätä collaboratoriksi. Opettaja kertoo Learnissa, miten Private-repon sisältö tarkistetaan. Jokainen kutsu lähettää sähköpostin, joten tee lisäys vasta, kun kurssin ohje erikseen pyytää.

## Komentorivi — sama asia terminaalissa

Kurssilla käytetään Visual Studiota. Komennot ovat se, mitä näet ohjeissa, Stack Overflow'ssa ja työpaikalla, ja ne muokkaavat samaa `.git`-kansiota kuin napit. Tämä taulukko on kartta, ei opeteltava lista.

| Visual Studio | Komentorivi |
|---------------|-------------|
| Git → Settings (nimi, sähköposti) | `git config --global user.name "…"` ja `user.email` |
| Git → Create Git Repository | `git init`, `dotnet new gitignore`, `git remote add origin …`, `git push -u origin main` |
| Git Changes -lista (M / A / D) | `git status` |
| Kaksoisklikkaus tiedostolla (vertailu) | `git diff` |
| Commit All | `git add .` ja `git commit -m "viesti"` |
| Nuoli ylös (push) | `git push` |
| View Branch History | `git log --oneline` |
| View Commit Details | `git show <tunniste>` |
| Undo Changes | `git restore <tiedosto>` |
| Clone a repository | `git clone <osoite>` |
| Nuoli alas (pull) | `git pull` |
| Fetch-nuoli | `git fetch` |

Terminaali avautuu Visual Studiossa **View → Terminal** solutionin kansioon. Arjen rutiini on neljä riviä: `git status`, `git add .`, `git commit -m "Mitä tein"`, `git push`. Laajemmin: [Git and GitHub Usage Guidelines](../../../Development-guidelines/Git-and-Github.md) (englanniksi).

## Yleisiä virheitä

| Virhe | Mitä tapahtuu | Korjaus |
|-------|---------------|---------|
| Commit ilman pushia, kone hajoaa | Commit oli vain paikallisessa repossa — se on poissa | Pushaa aina työrupeaman lopuksi; **outgoing**-laskuri pitää olla 0 |
| `bin/` tai `obj/` repossa | Satoja tiedostoja Git Changes -ikkunassa, jokainen käännös tekee "muutoksen" | `.gitignore`-rivit `[Bb]in/`, `[Oo]bj/`, `.vs/` ennen committia; jo commitatut poistetaan erikseen |
| Viesti `päivitys` | Historia ei kerro mitään | Imperatiivi + mitä muuttui: `Lisää Movie-luokka` |
| File → New → Project uudelle viikolle | Syntyy uusi solution ja uusi repo | Lisää projekti olemassa olevaan solutioniin: Solution → **Add → New Project** |
| Push ennen pullia toisella koneella | Push hylätään (*rejected*) | Pull ensin, sitten push |
| Opettaja lisätty collaboratoriksi vahingossa | Opettaja saa sähköpostin, pääsy jää voimaan | Settings → Collaborators → poista; tällä kurssilla ei lisätä |

## Yhteenveto

- Git on työkalu koneellasi, GitHub on kopio verkossa.
- Tallennus (Ctrl+S) ei ole commit, commit ei ole push. Vain push suojaa koneen hajoamiselta.
- Yksi toimiva osio = yksi commit. Viesti imperatiivissa ja kertoo, mitä muuttui.
- Undo Changes palauttaa viimeisimpään committiin — committaa usein, niin turvaverkko on lähellä.
- `.gitignore` pitää `bin/`, `obj/` ja `.vs/` poissa reposta. Datatiedosto, jonka ohjelma lukee, kuuluu repoon.
- Kahdella koneella: pull → työtä → commit → push.
- Koulutehtävät ovat **Private**. Opettajaa ei lisätä collaboratoriksi, ellei kurssin ohje pyydä.

Seuraavaksi: [IDE](IDE.md) · [Markdown](Markdown.md) (repon `README.md`) · [Git and GitHub Usage Guidelines](../../../Development-guidelines/Git-and-Github.md) (komentorivi, englanniksi)

## Hyödyllisiä linkkejä

- [Microsoft: Create a Git repository from Visual Studio](https://learn.microsoft.com/en-us/visualstudio/version-control/git-create-repository) — Create Git Repository -ikkuna kuvineen
- [Microsoft: Make a commit](https://learn.microsoft.com/en-us/visualstudio/version-control/git-make-commit) — Git Changes -ikkuna, staged vs kaikki muutokset
- [Microsoft: Fetch, pull, push and sync](https://learn.microsoft.com/en-us/visualstudio/version-control/git-fetch-pull-sync) — nuolet ja outgoing/incoming
- [Microsoft: Clone a repository](https://learn.microsoft.com/en-us/visualstudio/version-control/git-clone-repository) — Clone-ikkuna kuvineen
- [Microsoft: Browse repository history](https://learn.microsoft.com/en-us/visualstudio/version-control/git-browse-repository) — Branch History ja Commit Details
- [GitHub Docs: Hello World](https://docs.github.com/en/get-started/start-your-journey/hello-world) — GitHubin oma aloitusopas
- [GitHub Docs: Inviting collaborators](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository) — mistä collaborator lisätään ja poistetaan (tällä kurssilla vain tiedoksi)
- [GitHub: gitignore-pohjat](https://github.com/github/gitignore) — `VisualStudio.gitignore` on sama, jonka Visual Studio luo
- [Git-komentojen pikaopas (GitHub, PDF)](https://education.github.com/git-cheat-sheet-education.pdf) — yhden sivun lunttilappu komentoriville
- [Pro Git -kirja](https://git-scm.com/book/en/v2) — ilmainen, luvut 1–2 riittävät pitkälle; myös [suomeksi](https://git-scm.com/book/fi/v2) (osittain)
- [Learn Git Branching](https://learngitbranching.js.org/) — selaimessa pelattava harjoitus haaroista, kun ne tulevat ajankohtaisiksi
