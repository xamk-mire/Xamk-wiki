# Kuvauksesta koodiksi tekoälyagentin kanssa (Spec-Driven Development)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi kuvaus ohjaa agenttia](#miksi-kuvaus-ohjaa-agenttia)
3. [Vaiheet ja tiedostot](#vaiheet-ja-tiedostot)
4. [Tarkenna ennen kuin mallinnat](#tarkenna-ennen-kuin-mallinnat)
5. [Specin viisi osaa](#specin-viisi-osaa)
6. [Hyväksymiskriteeri vai toive](#hyväksymiskriteeri-vai-toive)
7. [Ei-tavoitteet](#ei-tavoitteet)
8. [ADR: miksi näin eikä toisin](#adr-miksi-näin-eikä-toisin)
9. [Agentin ohjetiedosto (AGENTS.md)](#agentin-ohjetiedosto-agentsmd)
10. [Tehtävälista](#tehtävälista)
11. [Suunnitelma ennen toteutusta](#suunnitelma-ennen-toteutusta)
12. [Rajatussa promptissa on neljä asiaa](#rajatussa-promptissa-on-neljä-asiaa)
13. [Prompti vai tiedosto?](#prompti-vai-tiedosto)
14. [Työjärjestys ja työnjako](#työjärjestys-ja-työnjako)
15. [Käytä tekoälyä oman version jälkeen](#käytä-tekoälyä-oman-version-jälkeen)
16. [Milloin tämä on liikaa](#milloin-tämä-on-liikaa)
17. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Tekoälyagentti** on työkalu, joka lukee repon tiedostoja, muokkaa niitä ja ajaa komentoja puolestasi. **Spec** (specification, määrittely) on tiedosto, joka kuvaa yhden ominaisuuden: mitä tehdään ja mistä tiedetään, että se on valmis.

**Spec-driven development** tarkoittaa työtapaa, jossa päätökset kirjoitetaan tiedostoiksi ennen koodia. Agentti toteuttaa niitä vasten yhden rajatun askeleen kerrallaan, ja ihminen tarkistaa jokaisen askeleen.

Työtapa ratkaisee yhden ongelman: agentti tuottaa aina jotain, mutta ilman kuvausta se tuottaa yleisimmän ratkaisun, ei sinun järjestelmäsi ratkaisua. Koodirivit voi tuottaa avustettuna. Päätöksiä ei voi, koska agentti ei tiedä, mitä sinä ja asiakas tarkoitatte.

Esimerkkinä tällä sivulla on pieni **varausjärjestelmä**, jossa käyttäjät varaavat kokoustiloja.

---

## Miksi kuvaus ohjaa agenttia

Agentti ei lue ajatuksia. Se päättelee **kontekstin** eli tilanteen siitä, mitä se näkee: kansioista, tiedostojen nimistä, rajapinnoista ja kuvauksista. Kun jotain ei ole kerrottu, se valitsee ratkaisun, jonka se on nähnyt useimmin. Esimerkiksi liiketoimintasääntö päätyy silloin helposti controlleriin, koska opetusesimerkeissä se on usein siellä.

Tästä seuraa kolme sääntöä.

**1. Se mikä ei ole repossa, ei ole olemassa.** Uusi istunto ei muista eilistä keskustelua. Jos säännön paikka on vain sinun päässäsi, agentti valitsee paikan itse. Siksi paikka kirjoitetaan tiedostoon.

**2. Kuvaus ilman rajaa on toive.** "Tee tilojen varaus" tuottaa jotain. "Tee tilojen varaus, älä lisää kirjautumista äläkä palauta domain-oliota sellaisenaan" tuottaa sen, mitä tilattiin.

**3. Tarkistus kuuluu sille, joka ajaa sen.** Agentti sanoo "valmis" aina. Siksi kuvaus päättyy tarkistukseen, jonka ihminen voi ajaa itse ja jonka tulos näkyy tulosteesta tai vastauksesta.

Sama pätee ihmistiimiin. Uusi kehittäjä ei muista keskustelua, jossa hän ei ollut mukana. Agentti vain paljastaa puuttuvan kuvauksen nopeammin, koska se ei kysy käytävällä.

---

## Vaiheet ja tiedostot

Vaiheet ovat eri työkaluissa samat, vaikka nimet vaihtelevat.

| Vaihe | Kysymys, johon se vastaa | Tiedosto | Muuttuu |
|-------|--------------------------|----------|---------|
| **Perussäännöt** | Mistä aloitetaan, mitä ei tehdä, milloin pysähdytään | `AGENTS.md`, `docs/arkkitehtuuri.md` | Harvoin |
| **Tarkennus** | Mitä tilaus jätti sanomatta | `docs/tilaus.md` | Kun asiakkaalta kysytään |
| **Kieli ja säännöt** | Mitkä sanat ja säännöt, ja missä kukin sääntö tarkistetaan | `docs/domain.md` | Kun sääntö muuttuu |
| **Spec** | Mitä tehdään ja mistä tiedetään, että se on valmis | `specs/001-varaa-tila.md` | Uusi tiedosto per ominaisuus |
| **Suunnitelma** | Miten ominaisuus sijoittuu rakenteeseen; miksi näin | `docs/rajapinta.md`, `docs/adr/` | Kun rakenne muuttuu |
| **Tehtävät** | Missä järjestyksessä ja miten askel todetaan valmiiksi | specin Tehtävät-osio | Per spec |
| **Toteutus** | Agentti tekee yhden askeleen, ihminen tarkistaa | koodi ja testit | Joka askeleella |

Tiedostot jaetaan sen mukaan, **kuinka usein tieto muuttuu**. Pysyvä ja yleinen tieto on `docs/`-kansiossa. Yksittäinen muutos on `specs/`-kansiossa.

Ominaisuuden spec **viittaa** arkkitehtuurikuvaukseen eikä toista sitä. Jos sama lause on kahdessa tiedostossa, toinen niistä vanhenee huomaamatta. Silloin agentti lukee kaksi eri ohjetta eikä tiedä, kumpi on voimassa.

---

## Tarkenna ennen kuin mallinnat

Asiakkaan tilauksessa on aina aukkoja. **Kysymys, jota et kysy, on arvaus, jonka agentti tekee puolestasi.**

Hyvä kysymys on sellainen, johon vastaus on arvo tai sääntö:

- Kuinka pitkä varaus saa enintään olla?
- Saako samalla käyttäjällä olla kaksi varausta yhtä aikaa?
- Mitä tapahtuu varaukselle, jos tila poistetaan käytöstä?

Kirjaa vastaus asiakkaan sanoin. Jos vastausta ei saada, tee **oletus** ja kirjoita se näkyviin oletuksena: "Oletus: varauksen voi perua, kunnes se alkaa." Agentti ei lue merkintää "jäi auki". Se lukee oletuksen tai keksii oman.

Sanasto otetaan asiakkaan kielestä. Jos asiakas puhuu tilasta, koodissa on `Tila`, ei `Resource`. Sama sana on kuvauksessa, koodissa ja testeissä. Tätä kutsutaan nimellä **Ubiquitous Language**, ja se on selitetty sivulla [Domain-Driven Design](Domain-Driven-Design.md#ubiquitous-language-yhteinen-kieli).

---

## Specin viisi osaa

Spec kuvaa yhden ominaisuuden. Siinä on viisi osaa.

| Osa | Mitä siinä on |
|-----|---------------|
| **Käsitteet** | Sanat, joita ominaisuus käyttää. Yleensä viittaus sanastoon, ei uusia sanoja. |
| **Tekemiset** | Mitä käyttäjä voi tehdä. Jokaiselle onnistumisen ja epäonnistumisen lopputulos sanoina. |
| **Säännöt ja Paikka** | Jokainen sääntö omalla rivillään, sen paikka ja syy paikalle. |
| **Hyväksymiskriteerit** | Tarkistukset, jotka voi ajaa. |
| **Ei-tavoitteet** | Mitä tämä muutos ei tee. |

**Paikka** tarkoittaa kerrosta tai luokkaa, jossa sääntö tarkistetaan. Paikan ratkaisee yksi kysymys: *mitä tietoa tarkistus tarvitsee?* Jos tarkistus tarvitsee vain yhden olion omat tiedot, sääntö kuuluu siihen olioon. Jos se tarvitsee haun tai toisen olion, sääntö kuuluu use caseen eli luokkaan, joka ohjaa yhden toiminnon kulun.

| Sääntö | Paikka | Miksi |
|--------|--------|-------|
| Varauksen loppu on alun jälkeen | `Varaus` (Domain) | Tarkistus tarvitsee vain varauksen omat ajat |
| Varaus kestää enintään neljä tuntia | `Varaus` (Domain) | Sama syy |
| Samaa tilaa ei varata päällekkäin | Varaa tila -use case (Application) | Tarkistus tarvitsee haun tilan muista varauksista |
| Puuttuva kenttä hylätään | API:n raja | Kyse on syötteen muodosta, ei liiketoimintasäännöstä |

Ilman Paikka-saraketta agentti päättää paikan itse. Sarakkeen avulla voit myös lukea valmiin muutoksen: onko jokainen sääntö siellä, missä spec sanoo?

**Spec viedään versionhallintaan ennen koodia.** Silloin historia näyttää, mitä tilattiin ennen kuin mitään rakennettiin. Jos spec kirjoitetaan koodin jälkeen, se kuvaa sen mitä syntyi, ei sitä mitä haluttiin.

Kerroksista kerrotaan sivulla [Clean Architecture](Clean-Architecture.md).

---

## Hyväksymiskriteeri vai toive

**Hyväksymiskriteeri** on lause, jonka voi todeta ajamalla tai yhdellä katseella vastaukseen. Toive on lause, jota ei voi todeta mistään.

| Toive | Hyväksymiskriteeri |
|-------|--------------------|
| Varaus toimii oikein | Toinen varaus samalle tilalle samalle ajalle hylätään ja vastaus kertoo syyn |
| Koodi on siistiä | Testit menevät läpi, ja Domain-projektissa ei ole viittausta tietokantakirjastoon |
| Arkkitehtuuria on noudatettu | Päällekkäisyys tarkistetaan use casessa, ei controllerissa |

Yleinen muoto on **Given–When–Then**: *Given* on lähtötila, *When* on yksi tekeminen ja *Then* on lopputulos, jonka voi todeta. Kirjoita jokaiselle säännölle vähintään yksi hyväksytty tapaus ja yksi hylkäys.

```text
Hyväksytty tapaus
Given: tila A on vapaa torstaina klo 14–16.
When:  käyttäjä varaa tilan A torstaiksi klo 14–16.
Then:  varaus syntyy, eikä tila A ole enää vapaa sillä välillä.

Hylkäys
Given: tilalla A on varaus torstaina klo 14–16.
When:  toinen käyttäjä varaa tilan A torstaiksi klo 15–17.
Then:  varaus hylätään, vastaus kertoo syyn ja tilalla A on edelleen yksi varaus.
```

Hylkäystapaukset ovat tärkeimmät. Ne sanovat, missä järjestelmän rajat ovat. Ne ovat myös se osa, jonka agentti jättää helpoimmin pois, koska onnistuva polku näyttää valmiilta ilman niitä.

**Definition of Done** on lista siitä, milloin mikä tahansa muutos on valmis: kriteerit on ajettu itse, muutos on luettu Paikka-saraketta vasten, säännöllä on testi, eikä repoon tullut mitään kiellettyä. Lista on sama joka muutokselle. Kirjoita se kerran yhteen paikkaan, älä jokaiseen speciin.

---

## Ei-tavoitteet

**Ei-tavoite** on asia, jota tämä muutos ei tee. Ei-tavoitteet eivät ole pessimismiä. Ne ovat se osa tilausta, jonka agentti muuten päättää itse.

```text
Ei-tavoitteet
- Ei kirjautumista. Varaaja tunnistetaan nimellä.
- Ei toistuvia varauksia.
- Ei sähköposti-ilmoituksia.
- Käynnistys ei lisää esimerkkidataa tietokantaan.
```

Ilman tätä listaa agentti lisää helposti asioita, jotka kuuluvat "tavalliseen" varausjärjestelmään. Jokainen ylimääräinen osa on koodia, jota kukaan ei tilannut mutta joku joutuu ylläpitämään.

---

## ADR: miksi näin eikä toisin

**ADR** (Architecture Decision Record) on lyhyt tiedosto, johon kirjataan yksi rakennepäätös. Siinä on neljä otsikkoa:

- **Tilanne**: mikä ongelma piti ratkaista.
- **Vaihtoehdot**: vähintään kaksi.
- **Päätös**: yksi valittu vaihtoehto.
- **Seuraukset**: mikä helpottuu, mikä vaikeutuu.

```text
ADR 0001: Koko kerroksen sulkeminen huollon ajaksi

Tilanne:      Huolto sulkee kaikki kerroksen tilat. Samalle ajalle voi jo olla varauksia.
Vaihtoehdot:  A) Huolto on oma käsite, joka estää uudet varaukset.
              B) Huolto tehdään varauksena jokaiseen tilaan.
Päätös:       A.
Seuraukset:   Varaa tila -use case tarkistaa myös huollot. Vanhat varaukset pitää
              perua erikseen. Huollon peruminen on yksi muutos, ei monta.
```

Spec sanoo, **mitä** rakennetaan. ADR sanoo, **miksi näin eikä toisin**. Ilman ADR:ää seuraava kehittäjä tai seuraava istunto voi "korjata" ratkaisun takaisin vaihtoehtoon, joka jo hylättiin.

Kaikkea ei kirjata ADR:ksi. Se on tarkoitettu päätöksille, joita on vaikea perua tai joiden syy ei näy koodista.

---

## Agentin ohjetiedosto (AGENTS.md)

`AGENTS.md` on repon juuressa oleva ohje agentille. Moni työkalu lukee sen istunnon alussa. Jos työkalu ei lue, tiedoston voi liittää viestiin itse.

Tiedostossa on neljä asiaa:

1. **Lukujärjestys**: mitkä tiedostot luetaan ja missä järjestyksessä.
2. **Rajat**: mitä ei tehdä. Rajat kirjoitetaan kieltoina, jotka voi tarkistaa.
3. **Tarkistus, jonka ihminen ajaa**: komento ja mitä sen pitää tulostaa.
4. **Pysähtymissääntö**: "Jos tieto puuttuu, pysähdy ja kysy. Älä arvaa."

```markdown
# Ohje agentille

## Lue ensin
1. docs/domain.md, docs/arkkitehtuuri.md, docs/rajapinta.md
2. Se specs-kansion tiedosto, jota muutos koskee. Jos sitä ei ole, pysähdy.

## Rajat
- Domain ei viittaa muihin projekteihin eikä tietokantakirjastoon.
- Nykyhetki annetaan parametrina. Domain-koodi ei lue kelloa itse.
- Älä lisää käsitettä, reittiä tai kirjastoa, jota kuvaus ei nimeä.

## Tarkistus, jonka ihminen ajaa
- Testit ajetaan, ja kaikkien pitää mennä läpi.
- Specin hyväksymiskriteerit todetaan käynnissä olevaa rajapintaa vasten.

## Pysähdy
Jos tieto puuttuu tai tiedostot ovat ristiriidassa, pysähdy ja kysy. Älä arvaa.
```

Rivi "nykyhetki annetaan parametrina" on esimerkki konkreettisesta rajasta. Sääntö "menneisyyteen ei voi varata" riippuu ajasta. Jos domain-koodi lukee kellon itse, sääntöä ei voi testata luotettavasti. Kun aika annetaan parametrina, testi voi antaa minkä tahansa hetken.

Pysähtymissääntö on tiedoston tärkein rivi. Ilman sitä agentti täyttää aukon arvauksella, ja arvaus näyttää aivan tavalliselta koodilta.

`AGENTS.md` **ei toista speciä** eikä muita tiedostoja. Se viittaa niihin. Kopio vanhenee heti, kun alkuperäinen muuttuu.

---

## Tehtävälista

Spec pilkotaan 6–10 askeleeksi. Jokaisella askeleella on oma **valmis kun** -ehto. Lista ei kerro, miten askel toteutetaan. Se kertoo, mistä tiedät askeleen olevan valmis.

| # | Askel | Valmis kun |
|---|-------|------------|
| 1 | Domain: `Varaus` ja sen säännöt | Sääntöjen testit menevät läpi ilman web-palvelinta |
| 2 | Application: Varaa tila -use case | Päällekkäisen varauksen testi menee läpi muistissa toimivalla tallennuksella |
| 3 | Infrastructure: tallennus tietokantaan | Varaus säilyy sovelluksen uudelleenkäynnistyksen yli |
| 4 | API: reitit ja DTO:t | Hyväksymiskriteerit toteutuvat HTTP-kutsuilla |

Miksi kaikkea ei anneta yhdessä viestissä?

- Eri osilla on eri tarkistus. Domainin säännöt todetaan testeillä, rajapinta HTTP-kutsuilla.
- Yhdessä isossa viestissä agentti on tehnyt paljon ennen ensimmäistä tarkistusta.
- Varhainen virhe on halpa korjata. Myöhään löytynyt virhe on kallis, koska sen päälle on jo rakennettu.

---

## Suunnitelma ennen toteutusta

Ennen yhtäkään muutosta agentti lukee kuvauksen ja **ehdottaa suunnitelman muuttamatta tiedostoja**. Näet agentin tulkinnan ennen kuin siitä tulee koodia. Väärän tulkinnan korjaaminen on tässä vaiheessa yhden lauseen työ.

Pyydä suunnitelmaan ainakin nämä:

- mitkä tiedostot agentti luki
- mitä se aikoo luoda tai muuttaa
- missä kerroksessa kukin sääntö tarkistetaan
- miten sinä voit tarkistaa askeleen
- mitkä kohdat kuvauksesta puuttuvat

Lue suunnitelma specin **Paikka-saraketta vasten**. Onko jokaisella säännöllä sama paikka kuin specissä? Pysyykö suunnitelma pyydetyssä askeleessa? Onko mukana jotain, mitä kuvaus ei nimeä?

Agentti kysyy usein jotain. Jos vastaus on tieto, joka puuttui kuvauksesta, **korjaa ensin tiedosto** ja pyydä sitten uusi suunnitelma. Vastaus, joka annetaan vain keskustelussa, katoaa istunnon mukana. Seuraava istunto arvaa saman kohdan uudestaan.

---

## Rajatussa promptissa on neljä asiaa

**Prompti** on viesti, jonka kirjoitat agentille. Rajatussa promptissa on neljä asiaa:

1. **Tehtävä ja lähde**: mitä tehdään ja mihin speciin se perustuu.
2. **Mihin saa koskea**: tiedostot tai projektit, joita saa muuttaa.
3. **Mihin ei saa koskea**: tiedostot, kerrokset ja asiat, jotka jäävät ennalleen.
4. **Miten valmius todetaan**: tarkistus ja sen odotettu tulos.

**Heikko prompti:**

```text
Lisää varauksen peruminen.
```

**Rajattu prompti:**

```text
Toteuta specs/003-peru-varaus.md:n tehtävälistan askel 2 ja vain se.

Saat muuttaa: Application-projektin use caset ja niiden testit.
Älä muuta: Domain-projektia, tietokannan rakennetta äläkä rajapinnan reittejä.
Älä lisää kirjastoja.

Valmis, kun testit menevät läpi ja mukana on testi, jossa jo alkaneen
varauksen peruminen hylätään.
Kerro lopuksi haara, commitit ja testien tuloste.
```

Mitä agentti todennäköisesti tekee heikolla promptilla? Se päättää itse kaiken, mitä viesti ei sano. Se valitsee säännön paikan, usein controllerin. Se päättää, poistetaanko varaus vai merkitäänkö se perutuksi. Se voi muuttaa rajapintaa ja tietokantaa samalla kertaa. Lopputulos voi toimia, mutta et tiedä, vastaako se tilausta, koska tilausta ei kirjoitettu.

**Hyvä prompti on spec-tiedosto ja rajaus, ei pitkä viesti.** Säännöt ovat jo specissä. Promptin tehtävä on osoittaa oikea tiedosto ja rajata tämä yksi askel.

---

## Prompti vai tiedosto?

| Tieto | Minne se kuuluu | Esimerkki |
|-------|-----------------|-----------|
| Pysyvä sääntö tai puuttuva tieto | Kuvaukseen (tiedosto) | "Varauksen voi perua, kunnes se alkaa." |
| Kertaluonteinen rajaus | Promptiin | "Tee vain askel 2." |

Prompti katoaa istunnon mukana. Tiedosto jää, ja seuraava istunto ja seuraava kehittäjä lukevat sen.

Hyvä testi: jos joudut kirjoittamaan saman lauseen toiseen promptiin, se kuuluu tiedostoon.

---

## Työjärjestys ja työnjako

Järjestys on aina sama:

1. **Spec ennen koodia.** Kuvaus on versionhallinnassa ennen muutosta.
2. **Suunnitelma ennen toteutusta.** Agentti ehdottaa, ihminen hyväksyy.
3. **Yksi askel kerrallaan.** Jokaisen askeleen jälkeen tarkistus.

| Kuka | Mitä tekee |
|------|------------|
| **Agentti** | Tekee suunnitelman. Toteuttaa yhden askeleen. Saa tehdä commitit feature-haaraan. Kertoo lopuksi haaran, commitit ja tarkistusten tulosteen. |
| **Ihminen** | Kirjoittaa kuvauksen ja tekee päätökset. Lukee muutoksen (diff) Paikka-saraketta vasten. Ajaa hyväksymistarkistuksen itse. Yhdistää pull requestin. |

Agentin sana "valmis" ei riitä. Aja tarkistus itse ja katso tuloste. Älä yhdistä muutosta, jos et osaa selittää, miksi jokin rivi on juuri siinä tiedostossa.

Haaroista ja pull requesteista kerrotaan sivulla [Git-haarat ja pull request](../../99-General/Git-Haarat-ja-Pull-Request.md).

---

## Käytä tekoälyä oman version jälkeen

Tekoäly kirjoittaa tyhjästä aina uskottavan, yleisen kuvauksen. Se ei ole puhunut asiakkaasi kanssa, joten kuvaus on väärä juuri niissä kohdissa, joilla on merkitystä.

Kirjoita siksi ensin oma versio. **Oma versio näyttää, missä yleinen vastaus on väärässä.** Jos et ole miettinyt asiaa itse, et huomaa virhettä.

Oman version jälkeen tekoäly on hyvä tarkistaja. Pyydä kysymyksiä, älä korjauksia:

```text
Tässä on spec. Mitkä hylkäystapaukset puuttuvat? Missä kohdassa joutuisit
arvaamaan, jos toteuttaisit tämän? Kysy minulta, älä korjaa tiedostoa.
```

Jos tekoäly ehdottaa arvoa, jonka vain asiakas voi tietää, se on oletus. Kirjaa se oletuksena tai kysy asiakkaalta.

---

## Milloin tämä on liikaa

Kuvausten kirjoittaminen vie aikaa. Se ei kannata aina.

- **Kertakäyttöinen skripti.** Ajat sen kerran ja näet tuloksen heti. Tarkistus on tulos itse.
- **Heitettävä prototyyppi.** Tarkoitus on oppia jotain, ja koodi poistetaan sen jälkeen.
- **Yhden rivin korjaus.** Muutos on pienempi kuin sen kuvaus.

Kuvaus kannattaa, kun koodia ylläpidetään, kun siinä on liiketoimintasääntöjä tai kun työtä tekee useampi ihminen tai istunto. Pienessäkin työssä kaksi asiaa säilyy: sano, mihin ei kosketa, ja aja tarkistus itse.

---

## Yhteenveto

| Käsite | Mitä se on | Miksi |
|--------|------------|-------|
| **Spec** | Yhden ominaisuuden kuvaus: käsitteet, tekemiset, säännöt ja Paikka, hyväksymiskriteerit, ei-tavoitteet | Agentti rakentaa sen, mitä tilattiin |
| **Paikka** | Kerros tai luokka, jossa sääntö tarkistetaan, ja syy | Muuten agentti valitsee paikan itse |
| **Hyväksymiskriteeri** | Lause, jonka voi todeta ajamalla | "Valmis" ei ole todiste |
| **Hylkäystapaus** | Kriteeri, jossa pyyntö hylätään | Kertoo rajat; jää helpoimmin pois |
| **Ei-tavoite** | Asia, jota muutos ei tee | Laajuus ei kasva huomaamatta |
| **ADR** | Yksi rakennepäätös: tilanne, vaihtoehdot, päätös, seuraukset | Syy säilyy, vaikka tekijä vaihtuu |
| **AGENTS.md** | Lukujärjestys, rajat, tarkistus ja pysähtymissääntö | Jokainen istunto alkaa samasta tiedosta |
| **Tehtävälista** | 6–10 askelta, jokaisella "valmis kun" | Virhe löytyy aikaisin |
| **Suunnitelma** | Agentin ehdotus ennen muutoksia | Tulkinnan voi korjata ennen koodia |
| **Rajattu prompti** | Tehtävä ja lähde, mihin saa koskea, mihin ei, miten valmius todetaan | Agentti ei päätä puolestasi |

### Muista

- Se mikä ei ole repossa, ei ole olemassa.
- Pysyvä tieto kuuluu tiedostoon, kertaluonteinen rajaus promptiin.
- Tarkistuksen ajaa ihminen.

---

## Seuraavaksi

- **[Clean Architecture](Clean-Architecture.md)** - Kerrokset, joihin Paikka-sarake viittaa
- **[Domain-Driven Design](Domain-Driven-Design.md)** - Sanasto, entiteetit ja säännöt
- **[DTO:t](DTOs.md)** - Rajapinnan oma muoto ja muotovirheen ero sääntövirheeseen
- **[Result Pattern](../Patterns/Result-Pattern.md)** - Odotettu epäonnistuminen paluuarvona
- **[Git-haarat ja pull request](../../99-General/Git-Haarat-ja-Pull-Request.md)** - Feature-haara ja muutoksen yhdistäminen

### Hyödyllisiä linkkejä

- [Microsoft: Architecture decision record](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [Architectural Decision Records (adr.github.io)](https://adr.github.io/)
- [Martin Fowler: Given When Then](https://martinfowler.com/bliki/GivenWhenThen.html)
- [AGENTS.md - avoin muoto agentin ohjetiedostolle](https://agents.md/)
