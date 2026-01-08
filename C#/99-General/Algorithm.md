# Algoritmi

## Mikä on algoritmi?

Algoritmi on joukko sääntöjä tai ohjeita, joita noudattamalla voidaan ratkaista jokin tietty ongelma tai tehtävä. Algoritmit voivat olla yksinkertaisia tai monimutkaisia riippuen ongelman luonteesta.

Esimerkiksi resepti ruoan valmistamiseksi voidaan ajatella algoritmina. Siinä on tietty sarja ohjeita, joita noudattamalla saamme lopputulokseksi tietyn ruokalajin.

Tietojenkäsittelyssä algoritmit ovat keskeisessä roolissa. Esimerkiksi hakukoneet käyttävät monimutkaisia algoritmeja etsiessään ja järjestäessään tietoa verkon miljardeista sivuista. Ohjelmointikielet, joilla tietokoneohjelmia kirjoitetaan, ovat työkaluja algoritmien ilmaisemiseen tavalla, jonka tietokone voi ymmärtää ja suorittaa.

Oikein suunnitellut algoritmit tehostavat toimintoja ja mahdollistavat monimutkaisten ongelmien ratkaisun. Huonosti suunnitellut algoritmit voivat sen sijaan kuluttaa paljon aikaa ja resursseja eivätkä välttämättä tuota toivottua lopputulosta.

**Muita lähteitä:**
- [Wikipedia - Algoritmi](https://fi.wikipedia.org/wiki/Algoritmi)

## Mikä on hyvä algoritmi?

Hyvän algoritmin tunnusmerkit voivat vaihdella riippuen kontekstista ja käyttötarkoituksesta. Alla on joitakin yleisiä ominaisuuksia, joita otetaan huomioon. Mitä näistä otetaan huomioon ja mitä näistä painotetaan eniten, riippuu aina kehitettävän ohjelman käyttötarkoituksesta.

### 1. Tehokkuus

Algoritmin tulisi käyttää mahdollisimman vähän resursseja (kuten prosessoriaikaa ja muistia) suhteessa siihen, mitä sen tehtävänä on suorittaa. Aikavaativuus ja tilavaativuus ovat kaksi keskeistä mittaria tehokkuudessa.

**Esimerkki**: Kuvittele, että olet kirjastossa ja etsit tiettyä kirjaa, joka on järjestetty aakkosjärjestyksessä. Jos tiedät, miten aakkoset on järjestetty, voit mennä suoraan oikeaan osaan hyllyä sen sijaan, että kulkisit joka hyllyn läpi alusta loppuun. Binäärihaku toimii samalla tavalla kuin tämä menetelmä: sen sijaan, että tarkastelisi jokaista kirjaa yksi kerrallaan (kuten lineaarisessa haussa), se keskittyy listaan ja tarkastelee vain sitä osaa, jossa haluttu kirja todennäköisesti on. Se tekee etsinnästä huomattavasti nopeamman.

### 2. Selkeys

Algoritmin tulisi olla ymmärrettävä. Selkeästi kuvattu algoritmi on helpompi tarkistaa, ylläpitää ja optimoida.

**Esimerkki**: Kun kokkaat ensimmäistä kertaa, yksinkertainen ja selkeä resepti on helpompi seurata kuin monimutkainen ohjeistus.

### 3. Yleiskäyttöisyys

Joskus algoritmin arvoa mitataan sen perusteella, kuinka monenlaisiin ongelmiin se soveltuu.

**Esimerkki**: Vaate, joka toimii sekä sateella että kuorimiseen tai tehokas järjestelyalgoritmi, joka toimii monenlaisissa tietorakenteissa ja syötteissä (kuten [QuickSort](https://fi.wikipedia.org/wiki/Pikalajittelu)).

### 4. Luotettavuus

Algoritmin tulisi toimia oikein kaikilla mahdollisilla syötteillä ja tuottaa oikea lopputulos.

**Esimerkki**: Kuvitellaan, että sinulla on koululaskin. Kun syötät laskimeen kaksi numeroa ja valitset yhteenlaskutoiminnon, odotat saavasi oikean summan joka kerta. Olipa syötteesi sitten 2 + 2 tai 999 + 1, laskimen tulisi antaa oikea tulos jokaisessa tilanteessa. Jos laskin antaisi erilaisia tuloksia samalle syötteelle tai jos sillä olisi rajat syötteille, jolloin se ei toimisi oikein, se ei olisi luotettava. Luotettavuus tarkoittaa sitä, että algoritmi (tässä tapauksessa yhteenlaskutoiminto) antaa oikean tuloksen johdonmukaisesti kaikille syötteille.

### 5. Stabiilisuus

Joissakin yhteyksissä, kuten numeerisessa analyysissä, algoritmin stabiilisuus (kyky käsitellä epätarkkuuksia ja virheitä) on tärkeää.

**Esimerkki**: Tässä on hyvä reaalimaailman esimerkki, joka toteutui vähän aikaa sitten: [UK Air Traffic Control Chaos Was a '1 in 15 Million' Problem - The New York Times](https://www.nytimes.com/2023/09/06/world/europe/uk-flights-air-traffic-control-chaos.html)

### 6. Skaalautuvuus

Hyvä algoritmi pystyy käsittelemään suuria datamääriä ilman, että suorituskyky romahtaa.

**Esimerkki**: Kuten metro, joka voi kuljettaa tuhansia ihmisiä päivittäin, niinkuin Google pystyy käsittelemään valtavat määrät dataa.

### 7. Joustavuus

Algoritmin kykyä mukautua muuttuviin olosuhteisiin tai vaatimuksiin voidaan pitää arvossa.

**Esimerkki**: Kuten lamppu, jonka kirkkautta voi säätää tai pilvipalveluiden algoritmit voivat skaalautua tarpeen mukaan.

### 8. Turvallisuus

Joissakin sovelluksissa, kuten salauksessa, algoritmin turvallisuus on keskeistä. Tämä tarkoittaa sitä, että ulkopuolisten on vaikea murtaa tai manipuloida sitä.

**Esimerkki**: Kassakaappi, vaikka kaikki tietävät, että kassakaappi lukitsee arvoesineet, vain harva osaa murtaa sellaisen.

### 9. Kustannustehokkuus

Kun otetaan huomioon kaikki resurssit (esim. kehitysaika, suorituskyky, muistin käyttö), algoritmin tulisi tarjota hyvää vastinetta resursseille.

**Esimerkki**: Energiatehokas talo, joka pitää lämmön sisällä talvella ja säästää sähköä. Teollisuudessa esimerkiksi algoritmit optimoivat resurssien käyttöä, jotta tuotanto olisi optimaalista.

### 10. Adaptiivisuus

Jotkut algoritmit pystyvät mukautumaan syötteen ominaisuuksiin parantaen suorituskykyään.

**Esimerkki**: Kuten ilmastointi, joka säätää lämpötilaa ulkoisten olosuhteiden mukaan tai miten suositusalgoritmit mukautuvat käyttäjän toiminnan mukaan.

## Yhteenveto

Hyvä algoritmi on:
- **Tehokas**: Käyttää resursseja tehokkaasti
- **Selkeä**: Helppo ymmärtää ja ylläpitää
- **Luotettava**: Toimii oikein kaikilla syötteillä
- **Skaalautuva**: Toimii myös suurilla datamäärillä
- **Soveltuva**: Sopii käyttötarkoitukseensa

Seuraavaksi: [Pseudokoodaus](Pseudocode.md)

