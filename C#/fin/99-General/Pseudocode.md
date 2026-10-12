# Pseudokoodaus

## Mikä on pseudokoodaus?

Pseudokoodaus tarkoittaa algoritmin tai ohjelman rakenteen kirjoittamista yksinkertaistetussa muodossa, joka muistuttaa ohjelmointikieltä mutta on vapaamuotoisempi ja ymmärrettävämpi ihmisille, jotka eivät ole ohjelmointikielten asiantuntijoita. Pseudokoodi ei ole suoritettavaa koodia, vaan se on tarkoitettu ohjelman tai algoritmin logiikan ja toiminnallisuuden kuvaamiseen.

Saman ratkaisun voi piirtää [vuokaaviona](Flowchart.md). Pseudokoodin `JOS` on vuokaavion salmiakki, ja `NIIN KAUAN KUIN` on nuoli, joka palaa taaksepäin. Kumpikin kuvaa saman algoritmin: toinen tekstinä, toinen kuvana.

## Pseudokoodauksen hyödyt

### 1. Yksinkertaistaminen

Pseudokoodi auttaa kehittäjiä keskittymään algoritmin logiikkaan ilman että heidän tarvitsee huolehtia syntaksista tai kielispesifisistä rakenteista.

### 2. Selkeys

Pseudokoodi on yleensä selkeämpää ja helpommin ymmärrettävää kuin varsinainen koodi, mikä tekee siitä tehokkaan työkalun ideoiden ja ratkaisujen kommunikointiin tiimien sisällä.

### 3. Yleispätevyys

Pseudokoodi ei ole sidottu mihinkään tiettyyn ohjelmointikieleen, joten se on ymmärrettävää kaikille ohjelmoijille riippumatta heidän taustastaan.

### 4. Suunnittelun tukeminen

Pseudokoodi on erinomainen työkalu algoritmien ja ohjelmien suunnitteluvaiheessa, sillä se auttaa hahmottamaan ohjelman rakennetta ja toimintalogiikkaa ennen varsinaisen koodin kirjoittamista.

### 5. Opetuksellinen väline

Pseudokoodia käytetään usein opetuksessa algoritmien ja ohjelmoinnin peruskäsitteiden selittämiseen, koska se keskittyy logiikkaan ja suunnitteluun teknisten yksityiskohtien sijaan.

## Esimerkki pseudokoodista

### Esimerkki 1: Tervehdys

```
ALOITA
  LUE käyttäjän_nimi
  TULOSTA "Hei, " + käyttäjän_nimi + "!"
LOPPU
```

### Esimerkki 2: Yksinkertainen laskin

```
ALOITA
  LUE luku1
  LUE luku2
  LUE operaatio
  
  JOS operaatio == "+" NIIN
    tulos = luku1 + luku2
  MUUTEN JOS operaatio == "-" NIIN
    tulos = luku1 - luku2
  MUUTEN JOS operaatio == "*" NIIN
    tulos = luku1 * luku2
  MUUTEN JOS operaatio == "/" NIIN
    tulos = luku1 / luku2
  LOPPU JOS
  
  TULOSTA tulos
LOPPU
```

### Esimerkki 3: Pariton vai parillinen

```
ALOITA
  LUE luku
  
  JOS luku % 2 == 0 NIIN
    TULOSTA "Luku on parillinen"
  MUUTEN
    TULOSTA "Luku on pariton"
  LOPPU JOS
LOPPU
```

### Esimerkki 4: Alennusprosentti

```
ALOITA
  LUE ikä
  
  JOS ikä < 10 NIIN
    alennusProsentti = 10
  MUUTEN JOS ikä >= 10 JA ikä <= 60 NIIN
    alennusProsentti = 0
  MUUTEN
    alennusProsentti = 5
  LOPPU JOS
  
  TULOSTA "Alennusprosenttisi on " + alennusProsentti + "%"
LOPPU
```

### Esimerkki 5: Alennusprosentti laajennettu

```
ALOITA
  LUE ikä
  LUE onko_opiskelija
  
  JOS onko_opiskelija == TOSI NIIN
    alennusProsentti = 15
  MUUTEN JOS ikä < 10 NIIN
    alennusProsentti = 10
  MUUTEN JOS ikä >= 10 JA ikä <= 60 NIIN
    alennusProsentti = 0
  MUUTEN
    alennusProsentti = 5
  LOPPU JOS
  
  TULOSTA "Alennusprosenttisi on " + alennusProsentti + "%"
LOPPU
```

### Esimerkki 6: Toisto — salasana

```
ALOITA
  LUE salasana

  NIIN KAUAN KUIN salasana on väärä
    TULOSTA "Väärä salasana, yritä uudelleen"
    LUE salasana

  TULOSTA "Tervetuloa"
LOPPU
```

Sisennetyt rivit toistuvat niin kauan kuin ehto on tosi. Kun salasana on oikein, suoritus jatkuu sisennyksen jälkeiseltä riviltä. Vuokaaviossa sama kohta on salmiakki, jonka ei-nuoli palaa kysymykseen.

Kurssin tehtävissä syötteen lukeminen kirjoitetaan usein sanalla `KYSY`. `LUE` ja `KYSY` tarkoittavat samaa asiaa.

## Harjoitustehtäviä

1. **Tervehdys**
   - Pyydä käyttäjältä nimeä
   - Tulosta "Hei, [käyttäjän nimi]!"

2. **Yksinkertainen laskin**
   - Pyydä käyttäjältä kaksi lukua
   - Kysy käyttäjältä, haluaako hän laskea lukujen summan, eron, tulon vai osamäärän
   - Tulosta valitun operaation tulos

3. **Pariton vai parillinen**
   - Pyydä käyttäjältä kokonaisluku
   - Tarkista onko luku pariton vai parillinen
   - Tulosta "Luku on pariton" tai "Luku on parillinen" sen mukaan, kumpi se on

4. **Alennusprosentti**
   - Kysy käyttäjältä ikää
   - Jos ikä on pienempi kuin 10-vuotta on alennusprosentti 10%
   - Jos ikä on 10-60 on alennusprosentti 0%
   - Jos ikä on yli 60 on alennusprosentti 5%
   - Tulosta "Alennusprosenttisi on [alennusProsentti]"

5. **Laajenna alennusprosenttialgoritmiä**
   - Kysy käyttäjältä onko hän opiskelija
   - Jos käyttäjä on opiskelija on alennusprosentti 15%
   - Tulosta "Alennusprosenttisi on [alennusProsentti]"

6. **Salasana enintään kolmella yrityksellä**
   - Kysy salasanaa niin kauan, kunnes se on oikein
   - Laske yritykset. Kolmannen väärän yrityksen jälkeen tulosta "Liian monta yritystä" ja lopeta
   - Tähän tarvitset toiston, laskurin ja kaksi ehtoa

## Yhteenveto

Pseudokoodi on:
- **Yksinkertaista**: Keskittyy logiikkaan, ei syntaksiin
- **Selkeää**: Helppo ymmärtää kaikille
- **Yleispätevää**: Ei riippuvaista ohjelmointikielestä
- **Hyödyllistä**: Auttaa suunnittelussa ja kommunikoinnissa

Seuraavaksi: [Vuokaavio](Flowchart.md) · [Algoritmi](Algorithm.md)

