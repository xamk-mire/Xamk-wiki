# Mitä on OOP? (Object-Oriented Programming)

## Johdanto

Olio-ohjelmointi (OOP, eli Object-Oriented Programming) on ohjelmoinnin paradigma, joka keskittyy objektien ja luokkien käyttöön ohjelmistosuunnittelussa. OOP perustuu useisiin keskeisiin konsepteihin, joista **perintä (inheritance)** ja **rajapinnat (interfaces)** ovat kaksi merkittävintä.

OOP:n tavoitteena on parantaa ohjelmiston modulaarisuutta, jälleenkäytettävyyttä ja ylläpidettävyyttä kapseloinnin, perinnän, polymorfismin ja yhdistämisen avulla.

## OOP:n Keskeiset Konseptit

### 1. Kapselointi (Encapsulation)

Kapselointi tarkoittaa datan (muuttujat) ja siihen liittyvän toiminnallisuuden (metodit) yhdistämistä yhdeksi yksiköksi (objektiksi tai luokaksi). Kapseloinnin avulla voimme piilottaa yksityiskohdat ja näyttää vain olennaiset ominaisuudet.

**Esimerkki:**

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
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance)
        {
            balance -= amount;
            return true;
        }
        return false;
    }
}
```

### 2. Perintä (Inheritance)

Perintä mahdollistaa olemassa olevan luokan ominaisuuksien ja toimintojen perimisen, jolloin voidaan luoda uusi luokka ilman tarvetta kirjoittaa samoja toimintoja uudestaan. Se edistää koodin uudelleenkäytettävyyttä ja hierarkkista luokkarakennetta.

**Esimerkki:**

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

// Käyttö
Dog dog = new Dog { Name = "Rex" };
dog.MakeSound(); // Tulostaa: "Hau hau!"
```

### 3. Polymorfismi (Polymorphism)

Polymorfismi on olio-ohjelmoinnissa esiintyvä käsite, jonka mukaan aliluokat voivat määrittää oman yksilöllisen toimintansa ja silti jakaa saman toiminnallisuuden yläluokan kanssa. Se voidaan toteuttaa monin eri tavoin, kuten metodin ylikuormituksen ja ylikirjoituksen avulla.

**Esimerkki:**

```csharp
public class Calculator
{
    // Metodin ylikuormitus (method overloading)
    public int Summa(int a, int b)
    {
        return a + b;
    }
    
    public double Summa(double a, double b)
    {
        return a + b;
    }
    
    public int Summa(int a, int b, int c)
    {
        return a + b + c;
    }
}

// Käyttö
Calculator calc = new Calculator();
int result1 = calc.Summa(5, 3);        // 8
double result2 = calc.Summa(5.5, 3.2); // 8.7
int result3 = calc.Summa(1, 2, 3);    // 6
```

### 4. Yhdistäminen (Composition)

Yhdistäminen tarkoittaa, että yksi luokka sisältää toisen luokan ilmentymiä. Se on tapa yhdistää useita yksinkertaisia osia yhteen monimutkaisempaan kokonaisuuteen.

**Esimerkki:**

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
        Console.WriteLine("Auto on valmis ajamaan");
    }
}
```

## Perintä vs. Rajapinnat

### Perintä

Kuten aiemmin mainittiin, perinnällä uusi luokka voi hyödyntää ja laajentaa olemassa olevan luokan toimintoja. Tämä mahdollistaa koodin jälleenkäytettävyyden ja vähentää toistoa. Perintä kuvaa usein **"on"** -suhdetta, esimerkiksi "Koira on eläin".

```csharp
public class Animal { }
public class Dog : Animal { } // Koira ON eläin
```

### Rajapinnat

Rajapinnat antavat mahdollisuuden määritellä "sopimus", jonka toteuttavat luokat on täytettävä. Toisin kuin perintä, joka kuvaa "on" -suhdetta, rajapinnat usein kuvaavat **"voi tehdä"** -suhteita, esimerkiksi "Lentokone voi lentää". Rajapinnat antavat luokille mahdollisuuden toteuttaa useita toimintoja ilman monen perinnän monimutkaisuutta.

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

## Yhteenveto

Nämä kaksi konseptia—perintä ja rajapinnat—ovat olennaisia olio-ohjelmoinnin ymmärtämisessä, ja ne tarjoavat kehittäjille tehokkaita välineitä ohjelmiston suunnitteluun ja toteutukseen.

Seuraavaksi syvennymme näihin konsepteihin yksityiskohtaisemmin.

