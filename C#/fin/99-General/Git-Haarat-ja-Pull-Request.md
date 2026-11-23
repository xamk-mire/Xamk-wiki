# Haarat ja pull request (Branches and Pull Requests)

**Haara** (branch) on erillinen kehityslinja samassa repossa. Voit tehdä muutoksen haarassa rikkomatta sitä versiota, jota muut käyttävät. **Pull request** (PR) on pyyntö yhdistää haaran muutokset toiseen haaraan. Sen kautta joku lukee muutoksen ennen kuin se hyväksytään.

Arjen esimerkki: kirjoitat yhteiseen raporttiin uuden luvun omaan kopioosi. Kun luku on valmis, pyydät toista lukemaan sen. Vasta hyväksynnän jälkeen luku liitetään yhteiseen raporttiin.

Tämä sivu jatkaa siitä, mihin [GitHub (Git)](GitHub.md) päättyy. Commit, push ja pull oletetaan tutuiksi.

**GitHub:** [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) · [About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

## Kartta

| Käsite | Yhdellä lauseella |
|--------|-------------------|
| **Haara** (branch) | Erillinen kehityslinja, jolla on oma commit-historiansa |
| **`master`** | Julkaistu ja hyväksytty tila (uusissa repoissa nimi on usein `main`) |
| **`development`** | Integraatiohaara: valmiit muutokset kootaan tänne |
| **`feature/*`** | Yhden muutoksen haara, esimerkiksi `feature/tuloksen-kirjaus` |
| **Pull request** (PR) | Pyyntö yhdistää haara toiseen; sisältää muutosten vertailun ja keskustelun |
| **Diff** | Vertailu, joka näyttää lisätyt ja poistetut rivit |
| **Merge** | Yhdistäminen: haaran commitit tulevat osaksi kohdehaaraa |
| **Haaran suojaus** (branch protection) | GitHubin asetus, joka estää suorat pushit haaraan |

## Pitkäikäiset haarat ja feature-haarat

Repossa on kaksi haaraa, jotka ovat olemassa koko ajan, ja lyhytikäisiä haaroja yksittäisille muutoksille.

| Haara | Mitä se tarkoittaa | Kuinka kauan elää |
|-------|--------------------|-------------------|
| `master` | Se, mikä on julkaistu tai hyväksytty. Tämän version pitää aina toimia. | Aina |
| `development` | Se, mikä on valmista mutta ei vielä julkaistu. Muutokset kootaan ja testataan täällä yhdessä. | Aina |
| `feature/nimi` | Yksi keskeneräinen muutos. Saa olla rikki, koska se ei haittaa muita. | Muutoksen ajan |

Feature-haara **lähtee `development`-haarasta ja palaa sinne**. Kun `development` on testattu ja valmis julkaistavaksi, se yhdistetään `master`-haaraan.

```
master       ●───────────────────────────────●──────►   julkaistu tila
              \                             ╱
development    ●──────●───────────●────────●─────────►   integraatio
                       \         ╱ ▲
feature/tulos           ●───●───●  │
                                   pull request:
                                   lue diff, aja tarkistukset, yhdistä
```

Miksi kolme tasoa eikä yksi?

- **Keskeneräinen työ ei riko muiden työtä.** Feature-haarassa saa olla koodia, joka ei vielä käänny.
- **Yksi haara = yksi muutos.** Muutoksen voi lukea, hyväksyä tai hylätä kokonaisuutena.
- **`master` on aina tunnetussa tilassa.** Siitä tiedetään, mitä on hyväksytty.

**Milloin tätä ei tarvita:** kun olet reposi ainoa kirjoittaja ja teet harjoitustehtäviä, yksi haara riittää. Haarat alkavat hyödyttää, kun kirjoittajia on useita tai kun muutokset halutaan tarkistaa ennen hyväksymistä.

## Peruskomennot

Neljä komentoa riittää feature-haaran tekemiseen ja viemiseen GitHubiin:

```bash
git switch development              # siirry integraatiohaaraan
git pull                            # hae uusin tila
git switch -c feature/tuloksen-kirjaus   # tee uusi haara ja siirry siihen
# ... muokkaa, git add ., git commit -m "Lisää tuloksen kirjaus" ...
git push -u origin feature/tuloksen-kirjaus   # vie haara GitHubiin
```

Pull request avataan ja yhdistetään GitHubin verkkosivulla. Visual Studiossa samat toiminnot löytyvät **Git**-valikosta (**New Branch…**) ja oikean alareunan haaravalitsimesta.

## Pull request on kaksi eri tekoa

Pull requestissa on kaksi erillistä tekoa. Ne menevät helposti sekaisin, koska ne tehdään samalla sivulla.

| Teko | Mitä se tarkoittaa | Mitä se muuttaa |
|------|--------------------|-----------------|
| **Avaaminen** (open) | "Katsoisitko tämän." Pyyntö, ei päätös. | Ei mitään kohdehaarassa |
| **Yhdistäminen** (merge) | "Tämä hyväksytään." Päätös. | Muutokset tulevat kohdehaaraan |

Näiden kahden välissä tehdään varsinainen työ:

1. **Lue diff.** Avaa PR:n **Files changed** -välilehti ja lue jokainen muuttunut rivi. Kysy itseltäsi: ymmärränkö, mitä tämä tekee? Onko tässä jotain, mitä ei pyydetty?
2. **Aja tarkistukset.** Vähintään: koodi kääntyy ja testit menevät läpi (`dotnet build`, `dotnet test`). Jos repossa on automaattiset tarkistukset, niiden tulos näkyy PR:n sivulla.
3. **Päätä.** Yhdistä, pyydä korjauksia tai sulje PR yhdistämättä.

```
avaa PR  ──►  lue diff  ──►  aja tarkistukset  ──►  merge
"katsoisitko"                                       päätös
```

PR:n avaaminen ei siis tarkoita, että muutos on hyväksytty. Suljettu PR, jota ei yhdistetty, on täysin tavallinen lopputulos.

## Miksi yhdistäminen on ihmisen päätös

Tekoälyagentti voi kirjoittaa koodin, tehdä commitit feature-haaraan ja jopa avata pull requestin. **Yhdistämisen tekee silti ihminen.**

| Vaihe | Kuka tekee |
|-------|-----------|
| Kirjoittaa koodin ja committaa feature-haaraan | Ihminen tai agentti |
| Avaa pull requestin | Ihminen tai agentti |
| Lukee diffin | Ihminen |
| Ajaa tarkistukset ja katsoo tuloksen | Ihminen |
| Yhdistää (merge) | Ihminen |

Syyt:

- **Vastuu on sillä, joka hyväksyy.** Kun muutos on `master`-haarassa, se on osa tuotetta. Agentti ei vastaa siitä, ihminen vastaa.
- **Agentti voi olla väärässä vakuuttavasti.** Koodi voi kääntyä ja näyttää siistiltä, mutta tehdä eri asian kuin pyydettiin. Tai se voi muuttaa tiedostoja, joihin ei pitänyt koskea. Tämä näkyy vain diffistä.
- **Kirjoittaja ei tarkista omaa työtään.** Sama pätee ihmisiin: siksi toinen henkilö lukee muutoksen. Agentin oma arvio "kaikki toimii" ei ole tarkistus.

Feature-haara on agentille turvallinen paikka työskennellä juuri siksi, että mikään siellä ei ole vielä hyväksyttyä. Raja kulkee yhdistämisessä.

## Haaran suojaus (branch protection)

**Haaran suojaus** on GitHubin asetus (repo → **Settings** → **Branches** tai **Rules**), jolla haaralle asetetaan sääntöjä. Tavallisin sääntö: haaraan ei voi pushata suoraan, vaan muutokset tulevat vain pull requestin kautta.

**Mitä se estää:**

| Tilanne | Ilman suojausta | Suojauksen kanssa |
|---------|-----------------|-------------------|
| Joku pushaa suoraan `master`-haaraan | Onnistuu, kukaan ei lukenut muutosta | Push hylätään |
| Sinä itse unohdat vaihtaa haaraa ja pushaat | Keskeneräinen koodi on `master`-haarassa | Push hylätään, huomaat virheen |
| Agentti yrittää pushata `master`-haaraan | Onnistuu, jos sillä on kirjoitusoikeus | Push hylätään |

Suojaus ei siis ole epäluottamusta muita kohtaan. Se suojaa myös omilta vahingoilta. Sääntö, joka on vain sovittu, unohtuu kiireessä. Sääntö, jonka GitHub valvoo, ei unohdu.

**Mitä suojatun haaran historiasta voi sanoa:** jokainen muutos `master`-haarassa on tullut pull requestin kautta. Jokaisella muutoksella on siis PR, josta näkee, mitä muutettiin, kuka sen hyväksyi ja milloin. Ilman suojausta tätä ei voi väittää, vaikka kaikki olisivat yrittäneet toimia oikein.

**Milloin sitä ei tarvita:** omassa harjoitusrepossa, jossa on yksi haara ja yksi kirjoittaja, suojaus vain hidastaa.

## Yleisiä virheitä

| Virhe | Mitä tapahtuu | Korjaus |
|-------|---------------|---------|
| Feature-haara tehdään `master`-haarasta | Haarasta puuttuvat `development`-haaran uudet muutokset | Siirry ensin `development`-haaraan ja tee `git pull` |
| Yksi haara, monta eri muutosta | Diffiä on vaikea lukea, eikä osaa voi hyväksyä erikseen | Yksi haara = yksi muutos |
| PR yhdistetään lukematta diffiä | Hyväksyt koodia, jota et ole nähnyt | Lue **Files changed** aina, myös omissa PR:issä |
| "Agentti sanoi, että testit menevät läpi" | Et tiedä, ajettiinko testejä oikeasti | Aja `dotnet test` itse ja katso tulos |

## Yhteenveto

- `master` on julkaistu ja hyväksytty tila, `development` on integraatiohaara ja `feature/*` on yhden muutoksen haara.
- Feature-haara lähtee `development`-haarasta ja palaa sinne pull requestin kautta.
- Pull requestin avaaminen on pyyntö ("katsoisitko"). Yhdistäminen on päätös.
- Avaamisen ja yhdistämisen välissä luetaan diff ja ajetaan tarkistukset.
- Agentti saa committata feature-haaraan. Ihminen lukee diffin, ajaa tarkistuksen ja yhdistää.
- Haaran suojaus estää suorat pushit `master`-haaraan, myös omat vahingot ja agentin virheet.
- Suojatun haaran historiasta tiedetään, että jokainen muutos on tullut tarkistetun pull requestin kautta.

## Takaisin

- [GitHub (Git)](GitHub.md) — commit, push, pull ja `.gitignore`
- [Git and GitHub Usage Guidelines](../../../Development-guidelines/Git-and-Github.md) — komentorivi ja haarakäytännöt laajemmin (englanniksi)

## Hyödyllisiä linkkejä

- [GitHub Docs: About branches](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches) — haarat GitHubissa
- [GitHub Docs: About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) — pull requestin osat
- [GitHub Docs: About protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) — haaran suojauksen säännöt
- [Microsoft: Create a branch in Visual Studio](https://learn.microsoft.com/en-us/visualstudio/version-control/git-create-branch) — haaran luonti Visual Studiossa
- [Learn Git Branching](https://learngitbranching.js.org/) — selaimessa pelattava harjoitus haaroista
