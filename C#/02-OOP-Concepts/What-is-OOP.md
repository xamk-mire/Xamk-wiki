# Mitä on OOP? (Object-Oriented Programming)

## Johdanto

Olio-ohjelmointi (OOP, eli Object-Oriented Programming) on ohjelmoinnin paradigma, joka keskittyy objektien ja luokkien käyttöön ohjelmistosuunnittelussa. OOP:n tavoitteena on parantaa ohjelmiston modulaarisuutta, jälleenkäytettävyyttä ja ylläpidettävyyttä.

**Tämä sivu antaa lyhyen yleiskuvan OOP:sta. Yksityiskohtaisempi materiaali löytyy [OOP-konseptit](../02-OOP-Concepts/) -osiosta.**

## OOP:n Keskeiset Konseptit

Olio-ohjelmoinnissa on neljä peruskäsitettä, jotka muodostavat OOP:n perustan:

### 1. Kapselointi (Encapsulation)

Kapselointi tarkoittaa datan (muuttujat) ja siihen liittyvän toiminnallisuuden (metodit) yhdistämistä yhdeksi yksiköksi (objektiksi tai luokaksi). Kapseloinnin avulla voimme piilottaa yksityiskohdat ja näyttää vain olennaiset ominaisuudet.

**Yksinkertainen esimerkki:**

```csharp
public class BankAccount
{
    private decimal balance; // Piilotettu ulkopuolelta
    
    public decimal Balance
    {
        get { return balance; }
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0)
            balance += amount;
    }
}
```

**Lisätietoja:** [Kapselointi (Encapsulation)](../02-OOP-Concepts/Encapsulation.md)

### 2. Perintä (Inheritance)

Perintä mahdollistaa olemassa olevan luokan ominaisuuksien ja toimintojen perimisen, jolloin voidaan luoda uusi luokka ilman tarvetta kirjoittaa samoja toimintoja uudestaan.

**Yksinkertainen esimerkki:**

```csharp
// Yläluokka (base class)
public class Animal
{
    public string Name { get; set; }
    
    public virtual void MakeSound()
    {
        Console.WriteLine("Eläin tekee ääntä");
    }
}

// Aliluokka (derived class)
public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Hau hau!");
    }
}
```

**Lisätietoja:** [Perintä (Inheritance)](../02-OOP-Concepts/Inheritance.md)

### 3. Polymorfismi (Polymorphism)

Polymorfismi tarkoittaa, että samaa rajapintaa voidaan käyttää eri objektityyppien kanssa. Aliluokat voivat määrittää oman yksilöllisen toimintansa ja silti jakaa saman toiminnallisuuden yläluokan kanssa.

**Yksinkertainen esimerkki:**

```csharp
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex" },
    new Cat { Name = "Whiskers" }
};

foreach (Animal animal in animals)
{
    animal.MakeSound(); // Kukin eläin tekee oman äänensä
}
```

**Lisätietoja:** [Polymorfismi (Polymorphism)](../02-OOP-Concepts/Polymorphism.md)

### 4. Abstraktio (Abstraction)

Abstraktio tarkoittaa monimutkaisten ongelmien yksinkertaistamista piilottamalla tarpeettomat yksityiskohdat ja keskittymällä olennaisiin asioihin.

**Lisätietoja:** Abstraktio toteutetaan usein [rajapintojen (Interfaces)](../02-OOP-Concepts/Interfaces.md) avulla.

## Yhdistäminen (Composition)

Yhdistäminen on tapa yhdistää useita yksinkertaisia osia yhteen monimutkaisempaan kokonaisuuteen. Se on vaihtoehto perinnälle tietyissä tilanteissa.

**Yksinkertainen esimerkki:**

```csharp
public class Engine
{
    public void Start()
    {
        Console.WriteLine("Moottori käynnistyy");
    }
}

public class Car
{
    private Engine engine; // Yhdistäminen
    
    public Car()
    {
        engine = new Engine();
    }
    
    public void Start()
    {
        engine.Start();
    }
}
```

**Lisätietoja:** [Yhdistäminen (Composition)](../02-OOP-Concepts/Composition.md)

## Perintä vs. Rajapinnat

### Perintä

Perinnällä uusi luokka voi hyödyntää ja laajentaa olemassa olevan luokan toimintoja. Perintä kuvaa usein **"on"** -suhdetta, esimerkiksi "Koira on eläin".

```csharp
public class Animal { }
public class Dog : Animal { } // Koira ON eläin
```

### Rajapinnat

Rajapinnat antavat mahdollisuuden määritellä "sopimus", jonka toteuttavat luokat on täytettävä. Rajapinnat usein kuvaavat **"voi tehdä"** -suhteita, esimerkiksi "Lentokone voi lentää".

```csharp
public interface IFlyable
{
    void Fly();
}

public class Airplane : IFlyable // Lentokone VOI lentää
{
    public void Fly()
    {
        Console.WriteLine("Lentokone lentää");
    }
}
```

**Lisätietoja:** [Rajapinnat (Interfaces)](../02-OOP-Concepts/Interfaces.md)

## Miksi käyttää OOP:ta?

Olio-ohjelmoinnin käyttö tarjoaa useita etuja:

1. **Koodin uudelleenkäytettävyys**: Luokkia voidaan käyttää uudelleen eri projekteissa
2. **Modulaarisuus**: Monimutkaiset ongelmat voidaan jakaa pienempiin osiin
3. **Ylläpidettävyys**: Koodi on helpompi ylläpitää ja muokata
4. **Skaalautuvuus**: Ohjelmisto on helpompi laajentaa uusilla ominaisuuksilla
5. **Testattavuus**: Luokat tekevät yksikkötestien kirjoittamisesta helpompaa

## Seuraavat askeleet

Nyt kun ymmärrät OOP:n peruskäsitteet, voit syventää tietämystäsi:

1. **Tutustu luokkiin ja objekteihin**: [Luokat ja Objektit](Classes-and-Objects.md)
2. **Syvenny OOP-konsepteihin**: [OOP-konseptit](../02-OOP-Concepts/)
   - [OOP-tekniikat - Yleiskuvaus](../02-OOP-Concepts/OOP-Techniques-Overview.md) - Kaikkien tekniikoiden yhteenveto
   - [Kapselointi](../02-OOP-Concepts/Encapsulation.md)
   - [Perintä](../02-OOP-Concepts/Inheritance.md)
   - [Polymorfismi](../02-OOP-Concepts/Polymorphism.md)
   - [Yhdistäminen](../02-OOP-Concepts/Composition.md)
   - [Rajapinnat](../02-OOP-Concepts/Interfaces.md)

## Yhteenveto

Olio-ohjelmointi perustuu neljään keskeiseen konseptiin:
- **Kapselointi**: Datan ja metodien yhdistäminen
- **Perintä**: Olemassa olevan luokan laajentaminen
- **Polymorfismi**: Samaa rajapintaa eri objektityypeillä
- **Abstraktio**: Monimutkaisten ongelmien yksinkertaistaminen

Nämä konseptit yhdessä muodostavat vahvan perustan modernille ohjelmistokehitykselle.

**Seuraava askel:** Tutustu [Luokat ja Objektit](Classes-and-Objects.md) -materiaaliin, jotta ymmärrät, miten luokat ja objektit toimivat käytännössä.
