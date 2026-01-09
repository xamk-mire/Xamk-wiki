# Olio-ohjelmoinnin Tekniikat ja Niiden Ratkaisemat Ongelmat

Olio-ohjelmoinnin (OOP) ytimessä on ajatus jakaa sovellus loogisiin yksiköihin, **olioihin**, jotka kuvaavat todellisen maailman käsitteitä tai sovelluksen osia. Tällä sivulla esittelemme OOP-konsepteja (kapselointi, perintä, polymorfismi, yhdistäminen ja rajapinnat), kerromme mitä ongelmia ne ratkaisevat ja annamme C#-kieliset koodi-esimerkit.

---

## Kapselointi (Encapsulation)

**Kapseloinnin ongelma, joka ratkaistaan:**
Ilman kapselointia luokan sisäisiä tietoja (muuttujia) voidaan lukemattomilla tavoilla lukea ja muokata suoraan ulkopuolelta, mikä voi rikkoa luokan eheyttä ja vaikeuttaa ylläpitoa.

**Ratkaisu:**
*Kapselointi* kätkee luokan toteutuksen yksityiskohdat tarjoamalla julkiset `get`- ja `set`-metodit (tai ominaisuudet) muuttujien käsittelyyn. Näin varmistetaan tietoturva ja selkeä rajapinta ulkoisille käyttäjille.

### Ennen kapselointia (ongelma)

```csharp
// ❌ HUONO: Julkiset kentät, ei kontrollia
public class BankAccount
{
    public decimal balance; // Kuka tahansa voi muuttaa suoraan!
    public string accountNumber;
}

// Käyttö - vaarallista!
BankAccount account = new BankAccount();
account.balance = -1000; // Voimme asettaa negatiivisen saldon!
account.balance = 999999; // Tai liian suuren summan!
```

### Kapseloinnin avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Kapseloitu toteutus
public class BankAccount
{
    private decimal balance; // Yksityinen kenttä
    private string accountNumber;
    
    public string AccountNumber
    {
        get { return accountNumber; }
        private set { accountNumber = value; }
    }
    
    public decimal Balance
    {
        get { return balance; }
        // Ei setteriä - saldoa ei voi muuttaa suoraan!
    }
    
    public BankAccount(string accountNumber, decimal initialBalance)
    {
        this.accountNumber = accountNumber;
        if (initialBalance >= 0)
            this.balance = initialBalance;
        else
            throw new ArgumentException("Alkusaldo ei voi olla negatiivinen");
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            balance += amount;
            Console.WriteLine($"Talletettu {amount} euroa. Uusi saldo: {balance}");
        }
        else
        {
            throw new ArgumentException("Talletussumman täytyy olla positiivinen");
        }
    }
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance)
        {
            balance -= amount;
            Console.WriteLine($"Nostettu {amount} euroa. Uusi saldo: {balance}");
            return true;
        }
        Console.WriteLine("Nosto epäonnistui: riittämätön saldo tai virheellinen summa.");
        return false;
    }
}
```

**Lisätietoja:** Katso [Kapselointi (Encapsulation)](Encapsulation.md)

---

## Perintä (Inheritance)

**Perinnän ongelma, joka ratkaistaan:**
Koodin toistuminen, moninkertainen kopiointi ja hankalasti hallittavat rinnakkaiset luokkien versiot.

**Ratkaisu:**
*Perintä* sallii uuden luokan (aliluokan) periä olemassa olevan luokan (yläluokan) ominaisuudet ja metodit, jolloin koodin uudelleenkäyttö ja ylläpito helpottuvat. Perintä kuvaa usein **"on-suhdetta"** (esim. "Koira on Eläin").

### Ilman perintää (ongelma)

```csharp
// ❌ HUONO: Koodin toistoa
public class Dog
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public void Eat() { Console.WriteLine($"{Name} syö"); }
    public void Sleep() { Console.WriteLine($"{Name} nukkuu"); }
    public void Bark() { Console.WriteLine($"{Name} haukkuu: Hau hau!"); }
}

public class Cat
{
    public string Name { get; set; } // Toistoa!
    public int Age { get; set; }     // Toistoa!
    
    public void Eat() { Console.WriteLine($"{Name} syö"); } // Toistoa!
    public void Sleep() { Console.WriteLine($"{Name} nukkuu"); } // Toistoa!
    public void Meow() { Console.WriteLine($"{Name} naukuu: Miau!"); }
}
```

### Perinnän avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Yläluokka (base class)
public class Animal
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public void Eat()
    {
        Console.WriteLine($"{Name} syö");
    }
    
    public void Sleep()
    {
        Console.WriteLine($"{Name} nukkuu");
    }
    
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} tekee ääntä");
    }
}

// ✅ Aliluokat (derived classes)
public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} naukuu: Miau!");
    }
}
```

**Lisätietoja:** Katso [Perintä (Inheritance)](Inheritance.md)

---

## Polymorfismi (Polymorphism)

**Polymorfismin ongelma, joka ratkaistaan:**
Tarve käsitellä luokkien olioita **yhtenäisellä** tavalla ilman, että kutsujan täytyy tietää tarkka toteutus.

**Ratkaisu:**
*Polymorfismi* mahdollistaa sen, että sama metodikutsu voi toimia eri tavoin riippuen siitä, minkä luokan olio (ylä- vai aliluokka) on kyseessä. C#-kielessä polymorfismin toteuttaa esimerkiksi `virtual`, `override`, `abstract` sekä interfacet.

### Metodin kutsut ilman polymorfismia (ongelma)

```csharp
// ❌ HUONO: Pitää tarkistaa tyyppi
public void MakeAnimalSound(Animal animal)
{
    if (animal is Dog)
    {
        Console.WriteLine("Hau hau!");
    }
    else if (animal is Cat)
    {
        Console.WriteLine("Miau!");
    }
    else if (animal is Bird)
    {
        Console.WriteLine("Tsirp tsirp!");
    }
    // Mutta jos meillä on 10 eläintyyppiä, koodi monimutkaistuu...
}
```

### Polymorfismin avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Yhtenäinen käsittely
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex" },
    new Cat { Name = "Whiskers" },
    new Bird { Name = "Tweety" }
};

foreach (Animal animal in animals)
{
    animal.MakeSound(); // Jokainen kutsuu oman versionsa!
}
// Tulostaa:
// Rex haukkuu: Hau hau!
// Whiskers naukuu: Miau!
// Tweety laulaa: Tsirp tsirp!
```

**Lisätietoja:** Katso [Polymorfismi (Polymorphism)](Polymorphism.md)

---

## Yhdistäminen (Composition)

**Yhdistämisen ongelma, joka ratkaistaan:**
Liian suuri "kaikki yhdessä" -luokka, joka sisältää liikaa vastuita ja tekee koodista vaikeasti ylläpidettävää.

**Ratkaisu:**
*Yhdistäminen (Composition)* tarkoittaa, että luokka koostuu muiden luokkien ilmentymistä. Tämä mahdollistaa loogisesti pienempien moduulien käytön, mikä parantaa selkeyttä ja ylläpidettävyyttä.

### Ilman yhdistämistä (ongelma)

```csharp
// ❌ HUONO: Kaikki yhdessä luokassa
public class Car
{
    // Moottorin ominaisuudet
    public bool EngineRunning { get; set; }
    public int EnginePower { get; set; }
    
    // Renkaiden ominaisuudet
    public int TirePressure { get; set; }
    public string TireBrand { get; set; }
    
    // Istuinten ominaisuudet
    public int NumberOfSeats { get; set; }
    public bool HasLeatherSeats { get; set; }
    
    // ... ja paljon muuta - liian monimutkainen!
}
```

### Yhdistämisen avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Pienet, keskitetyt luokat
public class Engine
{
    public bool IsRunning { get; private set; }
    public int Power { get; set; }
    
    public void Start() { IsRunning = true; Console.WriteLine("Moottori käynnistyy"); }
    public void Stop() { IsRunning = false; Console.WriteLine("Moottori sammuu"); }
}

public class Tire
{
    public int Pressure { get; set; }
    public string Brand { get; set; }
    
    public void CheckPressure() { Console.WriteLine($"Renkaan paine: {Pressure} PSI"); }
}

// ✅ Yhdistetty luokka
public class Car
{
    private Engine engine;      // Yhdistäminen
    private Tire[] tires;       // Yhdistäminen
    
    public Car(Engine engine, Tire[] tires)
    {
        this.engine = engine;
        this.tires = tires;
    }
    
    public void Start() { engine.Start(); }
    public void CheckAllTires() { foreach (var tire in tires) tire.CheckPressure(); }
}
```

**Lisätietoja:** Katso [Yhdistäminen (Composition)](Composition.md)

---

## Rajapinnat (Interfaces)

**Rajapintojen ongelma, joka ratkaistaan:**
Tarve sitoutua tiettyyn "sopimukseen" useissa luokissa ilman, että käytetään moniperintää. Lisäksi on tarve määritellä yhteisiä metodeja, joita eri luokat voivat toteuttaa omilla tavoillaan.

**Ratkaisu:**
*Rajapinta (interface)* määrittelee joukon metodeja (ja/tai ominaisuuksia), jotka luokan on toteutettava, jos se haluaa "noudattaa" rajapintaa. Tämä antaa joustavuutta, sillä yksi luokka voi toteuttaa useita rajapintoja.

### Rajapinnan avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Rajapinta määrittelee sopimuksen
public interface IFlyable
{
    void Fly();
}

public interface ISwimmable
{
    void Swim();
}

// ✅ Luokka voi toteuttaa useita rajapintoja
public class Duck : IFlyable, ISwimmable
{
    public void Fly()
    {
        Console.WriteLine("Ankka lentää");
    }
    
    public void Swim()
    {
        Console.WriteLine("Ankka ui");
    }
}

// ✅ Yhtenäinen käsittely
IFlyable[] flyables = new IFlyable[] { new Duck(), new Airplane() };
foreach (var flyable in flyables)
{
    flyable.Fly(); // Jokainen toteuttaa oman versionsa
}
```

**Lisätietoja:** Katso [Rajapinnat (Interfaces)](Interfaces.md)

---

## Yhteenveto

Nämä tekniikat—kapselointi, perintä, polymorfismi, yhdistäminen ja rajapinnat—muodostavat olio-ohjelmoinnin perustan. Jokainen niistä ratkaisee tietyn luonteisen ongelman, mutta yhdessä ne luovat kokonaisuuden, jolla saadaan koodista **selkeämpää, ylläpidettävämpää ja joustavampaa**.

### Suositus: Opiskele järjestyksessä

1. **Kapselointi** - Perusta datan suojaukselle
2. **Perintä** - Koodin uudelleenkäyttö
3. **Polymorfismi** - Joustava käsittely
4. **Yhdistäminen** - Modulaarinen rakenne
5. **Rajapinnat** - Sopimukset ja moniperintä

Jokainen konsepti rakentaa edellisen päälle ja yhdessä ne muodostavat vahvan perustan olio-ohjelmoinnille.

