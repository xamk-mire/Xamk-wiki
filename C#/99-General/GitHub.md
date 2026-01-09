# GitHub (Git)

## Mikä on Git?

Git on järjestelmä, joka tallentaa tiedostojen muutoshistorian. Sitä käytetään pääasiassa koodin versionhallintaan, mutta sitä voidaan käyttää minkä tahansa tekstipohjaisen tiedoston, kuten dokumenttien tai konfiguraatiotiedostojen, hallintaan.

## Mihin Git:iä käytetään?

### 1. Versionhallinta

Voit tallentaa projektisi eri versiot ja palata tarvittaessa aiempaan versioon. Tämä on hyödyllistä esimerkiksi silloin, kun uusi koodimuutos aiheuttaa odottamattomia ongelmia.

### 2. Yhteistyö

Git mahdollistaa sen, että useat kehittäjät voivat työskennellä samassa projektissa samanaikaisesti. Kukin kehittäjä voi tehdä muutoksia omassa paikallisessa kopiossaan ja yhdistää ne myöhemmin yhteiseen päähaaraan.

### 3. Haarautuminen ja yhdistäminen

Voit luoda haarautumia (branches) koodissasi, mikä mahdollistaa erilaisten ominaisuuksien tai korjausten kehittämisen erillään pääkoodista. Kun olet valmis, voit yhdistää (merge) haaran takaisin päähaaraan.

## Mikä on Gitin hyöty aloittelijalle?

### 1. Turvallisuus

Voit kokeilla uusia ideoita ja tehdä muutoksia koodiin tietäen, että voit aina palata toimivaan versioon, jos jokin menee pieleen.

### 2. Oppiminen

Versionhallinta on olennainen taito ohjelmistokehityksessä, ja Git on alan standardi. Sen oppiminen antaa sinulle tärkeän taidon ja tekee yhteistyöstä muiden kanssa helpompaa.

### 3. Yhteistyö

Jos aiot työskennellä muiden kanssa tai osallistua avoimen lähdekoodin projekteihin, Gitin tunteminen on välttämätöntä.

### 4. Historian seuraaminen

Voit nähdä, mitä muutoksia olet tehnyt, milloin ja miksi. Tämä auttaa ymmärtämään projektisi kehityskaarta ja oppimaan omista virheistäsi.

### 5. Portfolio

GitHubin ja muiden Git-pohjaisten palveluiden avulla voit näyttää projektisi mahdollisille työnantajille tai tiimikavereille.

## Terminologia

Gitin sanasto voi tuntua monimutkaiselta aloittelijalle, mutta kun ymmärtää peruskäsitteet, Gitin käyttö alkaa tuntua loogisemmalta. Tässä on lista yleisimmistä Git-käsitteistä:

### Tärkeimmät aluksi (kohdat 1, 2, 5, 7, 8)

1. **Repository (Repositorio)**: Tämä on perusyksikkö Gitissä ja se tarkoittaa koodivarastoa, joka sisältää kaikki tiedostosi sekä koko muutoshistoriasi.

2. **Commit**: Yksittäinen muutos tai joukko muutoksia, jotka olet tallentanut repositorioosi. Jokaisella commitilla on yksilöllinen tunniste ja viesti, joka kuvaa tehdyt muutokset.

3. **Branch (Haara)**: Versio projektistasi. Voit tehdä uusia haarautumia, jotta voit kehittää uusia ominaisuuksia erillään pääkoodistasi. "Master" tai nykyään usein "Main" on usein oletushaara.

4. **Merge (Yhdistäminen)**: Prosessi, jossa yhdistät yhden haaran muutokset toiseen haaraan.

5. **Clone**: Kopio repositoriosta, yleensä paikalliselle koneelle.

6. **Fork**: Kopio toisen käyttäjän repositoriosta omaan tilillesi, yleensä käytetty avoimen lähdekoodin projekteissa.

7. **Pull**: Toiminto, jolla haet ja yhdistät muutokset etä-repositoriosta paikalliseen versioosi.

8. **Push**: Toiminto, jolla lähetät paikalliset commitisi etä-repositorioon.

9. **Pull Request (PR)**: Ehdotus muutoksista, jotka olet tehnyt forkatussa repositoriossa, ja haluaisit yhdistää ne alkuperäiseen repositorioon. Yleinen käytäntö avoimen lähdekoodin projekteissa.

10. **Remote**: Viittaa etä-repositorioon, yleensä internetissä sijaitsevaan palveluun kuten GitHub, GitLab tai Bitbucket.

11. **Staging Area (Lavastusalue)**: Paikka, jossa valmistellaan muutoksia ennen niiden commitoimista. Täällä määrität, mitkä muutokset haluat sisällyttää seuraavaan commitiisi.

12. **Checkout**: Toiminto, jolla voit siirtyä eri committien, tagien tai haarautumien välillä.

13. **Tag**: Merkki, joka viittaa tiettyyn commitiin, yleensä käytetty versioiden merkitsemiseen.

14. **Stash**: Toiminto, jolla voit tilapäisesti tallentaa muutokset, jotka et ole vielä commitoinut, jotta voit siirtyä toiseen tehtävään.

## Gitin käyttö Visual Studiossa

### Kuinka laittaa koodit GitHubiin?

Visual Studion oikeasta alareunasta löytyy kohta **Add to Source Control**

Tai työkaluvalikosta löytyy Git ja sieltä voi valita **Create Git Repository**

Tämän jälkeen tulee ikkuna, jossa voit valita:
- **Mihin koodi ollaan laittamassa**: Valitse **GitHub** tai valitse **Local only**, jos haluat vain tallentaa omalle tietokoneellesi
- **Mikä on repositoryn nimi**: Anna repositorylle nimi
- **Haluatko, että repository on kaikille nähtävissä vai vain itsellesi**: **HUOM!** Jos olet koodaamassa koulutehtävää, sen täytyy olla **Private!!!!!**
- **Luo repository**: Painamalla tätä, ohjelma luo uuden repositoryn tilillesi ja laittaa koodit sinne

### Git Changes -ikkuna

**Commit-viesti**: Viesti jossa kerrotaan, että mitä muutoksia tehtiin tässä commitissa. Commit-viestissä kannattaa aina kertoa tarkasti, että mitä on tehnyt, jotta muut kehittäjät tietävät commitin syyn ja se on myös itsellesi hyödyllinen, jos joskus kuukausien päästä joudut jostain syystä katsomaan commit-historiaa.

**Commit**: Tämän avulla voit commitoida muutokset. Nuolta painamalla avautuu valikko, josta voit tehdä lisätoimintoja.

### git commit

Kun olet tehnyt muutoksia paikallisessa työtilassasi, sinun täytyy "commitoida" nämä muutokset, jotta ne kirjataan Git-historiaan. Commitilla on viesti, joka kuvailee tehdyt muutokset.

Esimerkki: `"Korjasin bugi X:n"`

Commit-toiminto tallentaa muutokset vain **paikallisesti**, eli ne eivät ole vielä siirretty etävarastoon (esim. GitHubiin tai GitLabiin).

### git push

Kun olet tehnyt yhden tai useamman commitin paikallisesti ja haluat siirtää (tai "pushata") nämä muutokset etävarastoon, käytät `git push`-komentoa.

Esimerkki: `git push origin master`, missä "origin" on oletusetävaraston nimi ja "master" on haaran nimi (nykyään monissa projekteissa käytetään termiä "main" päähaaralle).

### Muutosten näkeminen

**Muutokset**: Tässä kohdassa näet kaikki muutokset, joita olet tehnyt. Tiedostot merkitään:
- **M** (Modified) - Muokattu tiedosto
- **A** (Added) - Lisätty tiedosto
- **D** (Deleted) - Poistettu tiedosto (yliviivattu)

### Muutosten kumoaminen

Voit kumota muutoksia viemällä hiiren halutun muutoksen kohdalle ja painamalla kumoa-nuolta tai painamalla tiedoston kohdalta oikeaa hiiren nappia ja valitsemalla **Undo Changes**.

**HUOM!** Uutta lisättyä tiedostoa ei voi kumota, koska siinä ei ole mitään muutoksia joita kumota. Tämän muutoksen saa pois valitsemalla delete.

## Git History

Kun projekti on liitetty johonkin repositoryyn, voit sen jälkeen tarkastella sen historiaa, eli mitä muutoksia milloinkin on tehty siihen repositoryyn.

Saat historian näkyviin menemällä Git-valikkoon ja valitsemalla sieltä **View Branch History**.

Voit halutessasi tarkastella commitin yksityiskohtia painamalla oikeaa hiiren nappia halutun commitin kohdalla ja valitsemalla **View Commit Details**.

## Tilin yhdistäminen

Jotta voit käyttää GitHubia ja gittiä Visual Studiosta suoraan, täytyy sinun ensin linkittää tili. Se tapahtuu seuraavanlaisesti:

1. Paina oikeasta yläkulmasta löytyvää ikonia
2. Valitse Account Settings
3. Paina Add ja valitse GitHub
4. Valitse Authorize

## Muutokset ja niiden tallentaminen (Commit)

Visual Studio sisältää sisäänrakennetun tuen Git-versionhallinnalle, mikä tekee siitä helppoa seurata, tehdä ja kumota muutoksia suoraan IDE:ssa.

### Miten Git seuraa muutoksia Visual Studiossa?

Kun olet kloonannut Git-repositorion tai aloittanut uuden Git-repositorion Visual Studiossa, Visual Studio alkaa automaattisesti seurata tiedostomuutoksia.

Pääset näkemään, että mitä muutoksia olet tehnyt painamalla keltaisella ympyröityä kynää, joka löytyy oikeasta alareunasta. Tai sitten menemällä **Git Changes** -välilehdelle (sinisellä ympyröity).

Vihreällä ympyröidyt tiedostot ovat tiedostoja, joihin on tullut muutoksia edelliseen versioon verrattuna.

### Miten muutokset voidaan laittaa?

1. Avaa "Team Explorer" (joukkueentutkija) -näkymä Visual Studiossa
2. Valitse "Changes" (muutokset) -välilehti. Tässä näkyy kaikki tekemäsi muutokset
3. Syötä commit-viesti, joka kuvailee tekemäsi muutokset
4. Paina "Commit" (tallenna) -painiketta tallentaaksesi muutokset paikallisesti
5. Jos haluat lähettää muutokset etärepositorioon (kuten GitHubiin), valitse "Sync" (synkronoi) ja sitten "Push" (lähetä)

### Miten muutokset voidaan kumota?

- Jos haluat kumota tekemäsi muutokset ennen niiden tallentamista (commit), voit valita "Undo" (kumoa) "Changes"-näkymässä tietylle tiedostolle
- Jos olet jo tehnyt commitin ja haluat kumota sen, siirry "History" (historia) -välilehteen, löydä haluamasi commit ja valitse "Revert" (palauta) kumotaksesi sen muutokset

## Yhteenveto

Vaikka Gitin oppimiskäyrä voi tuntua jyrkältä aluksi, sen hallitseminen on palkitsevaa. Se ei ainoastaan tee koodaamisesta ja yhteistyöstä muiden kanssa helpompaa, vaan se myös avaa ovia moniin mahdollisuuksiin ohjelmistokehityksen maailmassa.

**Tärkeimmät komennot:**
- `git commit` - Tallenna muutokset paikallisesti
- `git push` - Lähetä muutokset etärepositorioon
- `git pull` - Hae muutokset etärepositoriosta

Seuraavaksi: [IDE](IDE.md)

