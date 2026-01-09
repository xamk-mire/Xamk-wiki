# Lajittelualgoritmit

**Muita materiaaleja:**
- [Ohjelmointiputka: Oppaat: Algoritmien aakkoset](https://www.ohjelmointiputka.net/oppaat/opas.php?tunnus=alg_1#algoritmintilavaativuus)

## Johdanto

Lajittelualgoritmit ovat ohjelmointitekniikoita, joita käytetään tietojen järjestämiseen tietyssä järjestyksessä. Ne ovat olennainen osa tietojenkäsittelyä ja tietojenkäsittelytiedettä, koska ne auttavat tehokkaasti käsittelemään ja hakemaan tietoja suurista tietorakenteista, kuten taulukoista, listoista, tietokannoista ja muista tietolähteistä.

Lajittelualgoritmit voivat järjestää tietoja eri tavoin, kuten numeroiden kasvavaan tai laskevaan järjestykseen, tekstijonojen aakkosjärjestykseen tai muiden kriteerien mukaan. Niitä käytetään monenlaisissa sovelluksissa, kuten hakualgoritmeissa, tietokantojen kyselyissä, aineiston analysoinnissa ja monissa muissa.

## Lajittelualgoritmien luokat

Yleisesti ottaen lajittelualgoritmit voidaan jakaa kahteen pääluokkaan:

### 1. Vertailupohjaiset lajittelualgoritmit

Nämä algoritmit perustuvat vertailuihin tietojen kesken. Ne vertailevat tietoja keskenään ja vaihtavat niitä tarvittaessa järjestääkseen ne oikeaan järjestykseen.

**Esimerkkejä:**
- Quicksort
- Mergesort
- Heapsort
- Selection sort
- Bubble sort

### 2. Vertailuttomat lajittelualgoritmit

Näitä algoritmeja kutsutaan myös radiksilajittelualgoritmeiksi. Ne eivät perustu tietojen suoraan vertailuun keskenään, vaan ne käyttävät muita tekniikoita, kuten bittien kääntämistä tai jakamista, järjestämiseen.

**Esimerkkejä:**
- Counting sort (laskemislajittelu)
- Bucket sort (hajautuslajittelu)
- Radix sort

## Big O -notaatio

**Muita materiaaleja:**
- [Big O Cheat Sheet – Time Complexity Chart](https://www.freecodecamp.org/news/big-o-cheat-sheet-time-complexity-chart/)

Big O on matemaattinen notaatio, jota käytetään algoritmien aikavaativuuden kuvaamiseen. Se auttaa arvioimaan, kuinka algoritmin suoritusaika kasvaa syötteen koon kasvaessa. Big O -notaatio ilmaisee yleisesti suurimman mahdollisen suoritusaikakasvun suhteessa syötteen koon kasvuun.

### Yleisiä Big O -notaation ilmaisuja

1. **O(1) - vakioaikavaativuus**: Algoritmi suorittaa tehtävänsä vakioajassa riippumatta syötteen koosta.

2. **O(log n) - logaritmiaikavaativuus**: Algoritmi suorittaa tehtävänsä nopeammin, kun syöte kasvaa, mutta suoritusaika kasvaa hitaasti logaritmisesti syötteen koossa.

3. **O(n) - lineaariaikavaativuus**: Algoritmin suoritusaika kasvaa suorassa suhteessa syötteen kokoon. Kun syöte kaksinkertaistuu, suoritusaika myös kaksinkertaistuu.

4. **O(n log n) - lineaarilogaritminen aikavaativuus**: Usein tehokas aikavaativuusluokka, joka kasvaa hitaammin kuin lineaarisesti mutta nopeammin kuin pelkkä logaritminen kasvu.

5. **O(n²) - neliöaikavaativuus**: Algoritmin suoritusaika kasvaa neliöllisesti syötteen koossa. Tämä on huomattavan tehoton algoritmi suurille syötteille.

6. **O(2ⁿ) - eksponentiaaliaikavaativuus**: Algoritmin suoritusaika kasvaa eksponentiaalisesti syötteen koossa. Tällaiset algoritmit voivat olla hyvin tehottomia suurilla syötteillä.

## Selection Sort

Selection sort on yksi yksinkertaisimmista ja helpoimmin ymmärrettävistä lajittelualgoritmeista. Sen tarkoitus on järjestää taulukko tai lista numeroita pienimmästä suurimpaan (tai suurimmasta pienimpään).

### Miten Selection Sort toimii?

1. Aluksi se tarkastaa koko taulukon tai listan ja etsii pienimmän numeron
2. Kun pienin numero on löydetty, se vaihdetaan taulukon tai listan ensimmäisen numeron kanssa, jolloin pienin numero siirtyy taulukon alkuun
3. Sitten algoritmi tarkastelee loppuosaa taulukosta tai listasta, etsii sieltä seuraavan pienimmän numeron ja vaihtaa sen taulukon toisen numeron kanssa
4. Tämä prosessi toistetaan, kunnes kaikki numerot ovat järjestyksessä

### Aikavaativuus

- **Aikavaativuus**: O(n²)
- Selection sortin aikavaativuus on aina O(n²), missä "n" on lajiteltavien alkioiden määrä
- Algoritmi suorittaa kaksi sisäkkäistä silmukkaa

### Tilavaativuus

- **Tilavaativuus**: O(1)
- Selection sort on in-place -lajittelualgoritmi, mikä tarkoittaa, että se ei tarvitse ylimääräistä muistia syötteen järjestämiseen

### Yhteenveto

Vaikka selection sort on helppo ymmärtää ja toteuttaa, se ei ole kovin tehokas suurilla taulukoilla. Sen aikavaativuus on O(n²), mikä tarkoittaa, että sen suoritusaika kasvaa neliössä taulukon koon kasvaessa. Tämä tekee siitä hidas verrattuna tehokkaampiin lajittelualgoritmeihin, kuten quicksortiin tai mergesortiin, joilla on parempi aikavaativuus suurille taulukoille.

## Aikavaativuus

Aikavaativuus (englanniksi "time complexity") on käsite, joka liittyy algoritmien tehokkuuden arviointiin. Se kuvaa, kuinka paljon aikaa algoritmi tarvitsee suorittaakseen tehtävänsä tietyn kokoisella syötteellä.

### Tärkeimmät aikavaativuusluokat

1. **O(1) - vakioaikavaativuus**: Algoritmi suorittaa tehtävänsä vakioajassa riippumatta syötteen koosta

2. **O(log n) - logaritmiaikavaativuus**: Algoritmin suoritusaika kasvaa logaritmisesti syötteen koon kanssa. Esimerkiksi binäärihaku on O(log n)

3. **O(n) - lineaariaikavaativuus**: Algoritmi suorittaa tehtävänsä suorassa suhteessa syötteen kokoon

4. **O(n log n) - lineaarilogaritmiaikavaativuus**: Tämä on monissa tehokkaissa lajittelualgoritmeissa, kuten quicksortissa ja mergesortissa, esiintyvä aikavaativuusluokka

5. **O(n²) - neliöaikavaativuus**: Algoritmin suoritusaika kasvaa neliöllisesti syötteen koon suhteen. Tämä on yleensä merkki tehoton algoritmista suurilla syötteillä

6. **O(2ⁿ) - eksponentiaaliaikavaativuus**: Algoritmin suoritusaika kasvaa eksponentiaalisesti syötteen koon kanssa. Tällaiset algoritmit ovat erittäin tehottomia ja käyttökelpoisia vain hyvin pienille syötteille

### Asia kiteytettynä

- **O(1)**: Laskenta ei riipu syötteen koosta
- **O(log n)**: Syötteen koko puolittuu jokaisessa vaiheessa
- **O(n)**: Yksi silmukka
- **O(n²)**: Sisäkkäiset silmukat
- **O(2ⁿ)**: Kasvunopeus kaksinkertaistuu jokaisen syötteen lisäyksen myötä

## Tilavaativuus

Tilavaativuus (englanniksi "space complexity") on käsite, joka liittyy algoritmin muistin käyttöön ja kuinka paljon lisätilaa (muistia) algoritmi tarvitsee suorittaakseen tehtävänsä suhteessa syötteen kokoon.

### Tärkeimmät tilavaativuusluokat

1. **O(1) - vakiotilavaativuus**: Algoritmi käyttää vakio määrän muistia riippumatta syötteen koosta

2. **O(n) - lineaarinen tilavaativuus**: Algoritmi käyttää muistia suorassa suhteessa syötteen kokoon

3. **O(n log n) - lineaarilogaritminen tilavaativuus**: Tämä tilavaativuusluokka on yleinen lajittelualgoritmeissa, kuten mergesortissa tai quicksortissa

4. **O(n²) - neliötilavaativuus**: Algoritmi käyttää muistia, joka kasvaa neliöllisesti syötteen koon kanssa

5. **O(2ⁿ) - eksponentiaalinen tilavaativuus**: Algoritmi käyttää muistia, joka kasvaa eksponentiaalisesti syötteen koon kanssa

## Yhteenveto

Lajittelualgoritmit ovat olennainen osa ohjelmoinnin ja tietojenkäsittelyn opiskelua, ja niiden ymmärtäminen auttaa kehittäjiä tehokkaasti käsittelemään ja analysoimaan dataa monissa eri tilanteissa.

**Tärkeimmät asiat:**
- Valitse oikea algoritmi ongelmalle
- Ymmärrä aikavaativuus ja tilavaativuus
- Tiedä milloin käyttää mitäkin algoritmia

Seuraavaksi: [Ongelman määrittäminen ja ratkominen](Problem-Solving.md)

