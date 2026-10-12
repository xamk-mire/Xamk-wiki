# Vuokaavio (Flow chart)

**Muita materiaaleja:**
- [Vuokaavio (omaantahtiin.com)](https://matikka.omaantahtiin.com/pitkamatikka/maa11/vuokaavio)

## Mikä on vuokaavio?

Vuokaavio (flowchart) on graafinen esitys, joka kuvaa prosessin vaiheet ja niiden väliset suhteet sekä mahdolliset päätöksentekopisteet. Ohjelmoinnissa vuokaaviota voidaan käyttää algoritmin tai ohjelman logiikan kuvaamiseen visuaalisessa muodossa ennen koodin kirjoittamista.

## Vuokaavion hyötyjä ohjelmoinnissa

### 1. Algoritmien suunnittelu

- Vuokaavio auttaa ohjelmoijia suunnittelemaan ja jäsentämään algoritmin logiikan ennen koodin kirjoittamista
- Se auttaa visualisoimaan prosessin kulun ja havaitsemaan mahdolliset ongelmat tai puutteet suunnitteluvaiheessa

### 2. Selkeys ja ymmärrettävyys

- Vuokaavio tekee ohjelmiston toiminnasta helpommin ymmärrettävää, erityisesti niille, jotka eivät ole koodaajia
- Se on tehokas väline kommunikointiin tiimin jäsenten tai sidosryhmien välillä

### 3. Dokumentointi

- Vuokaavioita voidaan käyttää ohjelmistoprojektien dokumentoinnissa, mikä helpottaa tulevaa viittauskäyttöä ja mahdollistaa paremman ymmärryksen ohjelmiston toiminnasta

### 4. Vianmääritys (Debugging)

- Vuokaavio voi helpottaa virheiden löytämistä ja korjaamista, koska se antaa visuaalisen esityksen siitä, miten ohjelma toimii ja missä mahdolliset ongelmat saattavat olla

### 5. Oppiminen ja koulutus

- Vuokaavioiden laatiminen ja lukeminen on arvokas taito, erityisesti ohjelmoinnin oppimisessa, koska se auttaa ymmärtämään loogista ajattelua ja prosessin hallintaa

### 6. Ajansäästö

- On usein nopeampaa ja helpompaa tehdä muutoksia vuokaaviossa kuin koodissa, erityisesti monimutkaisissa projekteissa

## Vuokaavion symbolit

Viisi symbolia riittää tällä kurssilla.

| Symboli | Muoto | Käyttö |
|---------|-------|--------|
| **Aloitus / Lopetus** | Soikio | Ohjelman alku- ja loppupiste |
| **Prosessi** | Suorakulmio | Toimenpide, esimerkiksi laskutoimitus tai arvon asetus |
| **Valinta** | Salmiakki | Kyllä/ei-kysymys, jonka kohdalla kaavio haarautuu kahtia |
| **Syöte / Tuloste** | Suunnikas | Tiedon lukeminen käyttäjältä tai tulostaminen ruudulle |
| **Nuoli** | Viiva | Suoritusjärjestys: mihin mennään seuraavaksi |

Nimeä valinnan molemmat nuolet: toinen on **kyllä**, toinen **ei**. Ilman nimiä lukija ei tiedä, kumpaan haaraan mennään.

## Kolme rakennetta vuokaaviossa

Jokainen vuokaavio rakentuu kolmesta peruskuviosta. Ne vastaavat [algoritmin kolmea rakennetta](Algorithm.md#kolme-rakennetta).

**Peräkkäisyys** on suora putki: soikio, sitten suorakulmioita ja suunnikkaita, lopuksi soikio. Nuolet kulkevat vain eteenpäin.

**Valinta** on salmiakki keskellä putkea. Kyllä-nuoli vie yhteen haaraan, ei-nuoli toiseen. Haarat yhtyvät taas, jos ohjelma jatkuu yhteistä polkua.

**Toisto** on nuoli, joka palaa taaksepäin. Salmiakki kysyy esimerkiksi "Onko salasana oikein?". Ei-nuoli palaa kysymykseen, kyllä-nuoli jatkaa eteenpäin. Ilman paluunuolta kaavio ei toista mitään.

Saman kuvion voi kirjoittaa [pseudokoodina](Pseudocode.md): salmiakki on `JOS`, paluunuoli on `NIIN KAUAN KUIN`.

## Vuokaavion laatiminen vaiheittain

Vuokaavion laatiminen vaatii huolellista suunnittelua ja jäsennystä. Seuraavat vaiheet voivat auttaa laatimaan hyvän vuokaavion:

### 1. Määrittele tavoite

Määritä selkeästi, mitä prosessia tai algoritmia aiot kuvata vuokaaviossa.

### 2. Tutki prosessi

Tutki ja ymmärrä prosessi perusteellisesti. Kerää kaikki tarvittavat tiedot ja resurssit, jotka auttavat sinua kuvaamaan prosessin vaiheet ja loogisen kulun.

### 3. Luonnostele

Aloita tekemällä karkea luonnos prosessista paperille tai digitaalisesti. Tämä auttaa sinua järjestämään ajatuksesi ja tunnistamaan prosessin eri vaiheet ja päätöskohdat.

### 4. Valitse työkalut

Valitse työkalu, jolla aiot laatia vuokaavion. On olemassa monia ohjelmistoja ja online-työkaluja, kuten:
- **Draw.io** (ilmainen, online)
- **Microsoft Visio** (maksullinen)
- **Lucidchart** (maksullinen, online)

### 5. Laadi vuokaavio

Aloita vuokaavion laatiminen valitulla työkalulla. Käytä oikeita symboleita eri vaiheiden ja päätösten kuvaamiseen.

### 6. Tarkista looginen kulku

Tarkista vuokaavion looginen kulku varmistaaksesi, että kaikki vaiheet ja päätökset on kuvattu oikein ja että vuokaavio johtaa haluttuun lopputulokseen.

### 7. Pyydä palautetta

Pyydä palautetta muilta tiimin jäseniltä tai sidosryhmiltä varmistaaksesi, että vuokaavio on ymmärrettävä ja että se kuvaa prosessia oikein.

### 8. Tee tarvittavat muutokset

Perustuen saatuun palautteeseen, tee tarvittavat korjaukset ja päivitykset vuokaavioon.

### 9. Dokumentoi ja jaa

Dokumentoi vuokaavio ja jaa se muiden kanssa. Selitä tarvittaessa vuokaavion tärkeät kohdat ja varmista, että kaikki sidosryhmät ymmärtävät sen.

### 10. Päivitä tarvittaessa

Kun prosessi muuttuu tai kun saat lisätietoa, päivitä vuokaavio vastaamaan uusia tietoja ja vaatimuksia.

## Yhteenveto

Olemalla taitava vuokaavion laatimisessa, ohjelmoija pystyy suunnittelemaan ja kommunikoimaan ohjelmiston rakenteen ja toiminnallisuuden tehokkaammin, mikä voi johtaa korkealaatuisempaan ja virheettömämpään koodiin. Vuokaaviot auttavat myös ohjelmoijia ja tiimejä pysymään järjestäytyneinä ja keskittyneinä projektin eri vaiheissa, mikä voi olla erityisen hyödyllistä monimutkaisissa tai laajoissa ohjelmistoprojekteissa.

Seuraavaksi: [draw.io](DrawIO.md)

