# Algoritmi

**Algoritmi** on askellista, jota tietokone voi seurata sellaisenaan. Tietokone tekee täsmälleen sen, mitä lista sanoo. Se ei arvaa puuttuvaa askelta eikä korjaa epäselvää.

Arjen esimerkki on resepti. Ihmiselle riittää ohje "keitä vettä". Tietokoneelle pitää kertoa, mistä tietää veden kiehuvan ja mitä tehdään, jos vedenkeitin on tyhjä.

Saman askellistan voi esittää [vuokaaviona](Flowchart.md) tai [pseudokoodina](Pseudocode.md). C#-koodi on sama lista kirjoitettuna kielellä, jonka kääntäjä ymmärtää.

**Muita lähteitä:**
- [Wikipedia: Algoritmi](https://fi.wikipedia.org/wiki/Algoritmi)

## Hyvä algoritmi

Tällä kurssilla hyvä algoritmi täyttää kolme ehtoa.

| Ominaisuus | Selitys |
|------------|---------|
| **Yksiselitteinen** | Jokaisen askeleen voi suorittaa vain yhdellä tavalla |
| **Äärellinen** | Algoritmi päättyy joskus eikä jatku ikuisesti |
| **Järjestetty** | Askelten järjestyksellä on väliä |

"Odota" ei ole yksiselitteinen askel. "Odota 3 minuuttia" on. Jos salasanaa kysytään uudelleen eikä yrityksiä rajoiteta, algoritmi ei ole äärellinen: käyttäjä voi vastata väärin loputtomiin.

## Kolme rakennetta

Kolme rakennetta riittää kuvaamaan minkä tahansa ohjelman.

| Rakenne | Mitä tapahtuu | Vuokaaviossa |
|---------|----------------|--------------|
| **Peräkkäisyys** | Askeleet suoritetaan järjestyksessä alusta loppuun | Suora putki, nuolet eteenpäin |
| **Valinta** | Ohjelma haarautuu ehdon mukaan | Salmiakki ja kyllä/ei-nuolet |
| **Toisto** | Sama askel toistuu, kunnes ehto täyttyy | Nuoli takaisin aiempaan kohtaan |

C#:ssa samat rakenteet ovat rivit allekkain, `if` / `else` sekä silmukat `while` ja `for`. Katso [ohjausrakenteet](../00-Basics/Control-Structures.md).

## Tehokkuus — myöhemmin

Myöhemmin algoritmeja vertaillaan myös sen mukaan, kuinka paljon aikaa ja muistia ne käyttävät. Tätä mitataan Big O -notaatiolla. Sitä ei tarvita vielä. Ensin algoritmin pitää olla yksiselitteinen, äärellinen ja järjestetty.

Lisää: [Big O](Big-O.md).

## Yhteenveto

- Algoritmi on askellista, jonka tietokone voi suorittaa sellaisenaan.
- Hyvä algoritmi on yksiselitteinen, äärellinen ja järjestetty.
- Kolme rakennetta riittää: peräkkäisyys, valinta ja toisto.

Seuraavaksi: [Vuokaavio](Flowchart.md) · [Pseudokoodi](Pseudocode.md)
