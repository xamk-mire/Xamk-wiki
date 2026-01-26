# Mitä on OOP? (Object-Oriented Programming)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi OOP syntyi?](#miksi-oop-syntyi)
3. [OOP:n neljä pilaria](#oopn-neljä-pilaria)
4. [OOP:n lisätekniikat](#oopn-lisätekniikat)
5. [OOP vs muut paradigmat](#oop-vs-muut-paradigmat)
6. [OOP:n edut ja haitat](#oopn-edut-ja-haitat)
7. [Milloin käyttää OOP:ta?](#milloin-käyttää-oopta)
8. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Olio-ohjelmointi** (OOP, eli Object-Oriented Programming) on ohjelmoinnin paradigma, jossa **ohjelmat rakennetaan objekteista**, jotka yhdistävät datan ja toiminnallisuuden yhteen.

**Yksinkertaisesti:** Sen sijaan että kirjoittaisit koodia joka käsittelee dataa ja funktiota erikseen, OOP yhdistää ne **objekteiksi** jotka edustavat todellisen maailman asioita.

### Lyhyt esimerkki:

```csharp
// ❌ Ilman OOP:ta (Proseduraalinen tyyli)
string dogName = "Rex";
int dogAge = 3;
void MakeDogSound(string name)
{
    Console.WriteLine($"{name} haukkuu!");
}
MakeDogSound(dogName);

// ✅ OOP:lla
public class Dog
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu!");
    }
}

Dog dog = new Dog { Name = "Rex", Age = 3 };
dog.MakeSound();
```

**Hyödyt:**
- ✅ Data ja toiminnallisuus yhdessä
- ✅ Helpompi ymmärtää (edustaa todellista koiraa)
- ✅ Helppo luoda useita koiria
- ✅ Voi lisätä uusia ominaisuuksia helposti

---

## Miksi OOP syntyi?

### Ongelma: Proseduraalinen ohjelmointi kasvoi liian monimutkaiseksi

**1960-70-luvuilla** ohjelmat kirjoitettiin **proseduraalisesti**:
- Funktioita jotka käsittelevät dataa
- Data ja logiikka erillään
- Kun ohjelmat kasvoivat, niistä tuli vaikeita hallita

```csharp
// Proseduraalinen esimerkki (1970-luku tyyli)
string[] studentNames = new string[100];
int[] studentAges = new int[100];
double[] studentGrades = new double[100];

void AddStudent(int index, string name, int age, double grade)
{
    studentNames[index] = name;
    studentAges[index] = age;
    studentGrades[index] = grade;
}

void PrintStudent(int index)
{
    Console.WriteLine($"{studentNames[index]}, {studentAges[index]}, {studentGrades[index]}");
}

// Ongelmat:
// - Kaikki taulukot pitää ylläpitää erikseen
// - Helppo sekoittaa indeksit
// - Vaikea laajentaa (lisää kenttä → muuta kaikkea)
```

### Ratkaisu: Olio-ohjelmointi

**1980-luvulla** OOP yleistyi (C++, Smalltalk):
- Data ja logiikka yhdistetty **objekteiksi**
- Objektit edustavat todellisia asioita
- Helpompi hallita monimutkaisuutta

```csharp
// OOP-esimerkki (moderni tyyli)
public class Student
{
    public string Name { get; set; }
    public int Age { get; set; }
    public double Grade { get; set; }
    
    public void Print()
    {
        Console.WriteLine($"{Name}, {Age} vuotta, Arvosana: {Grade}");
    }
    
    public bool IsPassing()
    {
        return Grade >= 1.0;
    }
}

List<Student> students = new List<Student>();
students.Add(new Student { Name = "Matti", Age = 20, Grade = 4.5 });
students.Add(new Student { Name = "Liisa", Age = 22, Grade = 3.8 });

foreach (Student student in students)
{
    student.Print();
}

// Hyödyt:
// ✅ Kaikki opiskelijan data yhdessä paikassa
// ✅ Helppo lisätä uusia kenttiä
// ✅ Metodeita voi kutsua luonnollisesti: student.Print()
```

---

## OOP:n neljä pilaria

OOP perustuu **neljään keskeiseen periaatteeseen**:

### 1. 🔒 Kapselointi (Encapsulation)

**"Piilota sisäiset yksityiskohdat, näytä vain olennainen"**

Kapselointi tarkoittaa datan ja metodien yhdistämistä, ja **pääsyn rajoittamista** niihin.

```csharp
public class BankAccount
{
    private decimal balance; // ❌ Ei pääsyä ulkopuolelta!
    
    public decimal Balance
    {
        get { return balance; }
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0) // ✅ Validointi
        {
            balance += amount;
            Console.WriteLine($"Talletettu: {amount:C}");
        }
    }
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance) // ✅ Turvallisuus
        {
            balance -= amount;
            Console.WriteLine($"Nostettu: {amount:C}");
            return true;
        }
        Console.WriteLine("Ei tarpeeksi rahaa!");
        return false;
    }
}

// Käyttö:
BankAccount account = new BankAccount();
account.Deposit(100);
account.Withdraw(30);
// account.balance = 1000000; // ❌ EI TOIMI - suojattu!
```

**Miksi tärkeää?**
- ✅ Estää virheellisen datan
- ✅ Voi muuttaa sisäistä toteutusta
- ✅ Parempi turvallisuus

**Lue lisää:** [Kapselointi (Encapsulation)](Encapsulation.md)

---

### 2. 👪 Perintä (Inheritance)

**"Luo uusia luokkia olemassa olevien pohjalta"**

Perintä mahdollistaa **"is-a"** (on) -suhteen: "Koira ON eläin".

```csharp
// Yläluokka (parent/base class)
public class Animal
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} tekee äänen");
    }
    
    public void Eat()
    {
        Console.WriteLine($"{Name} syö");
    }
}

// Aliluokat (child/derived classes)
public class Dog : Animal
{
    public string Breed { get; set; }
    
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
    
    public void Fetch()
    {
        Console.WriteLine($"{Name} noutaa pallon");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} naukuu: Miau!");
    }
    
    public void Scratch()
    {
        Console.WriteLine($"{Name} raapii");
    }
}

// Käyttö:
Dog dog = new Dog { Name = "Rex", Age = 3, Breed = "Labrador" };
dog.MakeSound(); // "Rex haukkuu: Hau hau!"
dog.Eat();       // Peritty Animal:sta
dog.Fetch();     // Vain Dog:lla

Cat cat = new Cat { Name = "Whiskers", Age = 2 };
cat.MakeSound(); // "Whiskers naukuu: Miau!"
cat.Eat();       // Peritty Animal:sta
cat.Scratch();   // Vain Cat:lla
```

**Miksi tärkeää?**
- ✅ Vältytään koodin toistolta
- ✅ Yhteinen toiminnallisuus yhdessä paikassa
- ✅ Hierarkia pysyy selkeänä

**Lue lisää:** [Perintä (Inheritance)](Inheritance.md)

---

### 3. 🎭 Polymorfismi (Polymorphism)

**"Sama rajapinta, eri toteutukset"**

Polymorfismi tarkoittaa että **voit käsitellä eri tyyppisiä objekteja samalla tavalla**.

```csharp
// Polymorfismi toiminnassa
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex", Age = 3 },
    new Cat { Name = "Whiskers", Age = 2 },
    new Dog { Name = "Buddy", Age = 5 },
    new Cat { Name = "Fluffy", Age = 1 }
};

// Käsittele kaikkia samalla tavalla!
foreach (Animal animal in animals)
{
    animal.MakeSound(); // ✅ Kutsuu oikeaa versiota!
    animal.Eat();
    Console.WriteLine();
}

// Output:
// Rex haukkuu: Hau hau!
// Rex syö
//
// Whiskers naukuu: Miau!
// Whiskers syö
//
// ... jne
```

**Miksi tärkeää?**
- ✅ Ei if-else lauseita tyyppitarkistuksiin
- ✅ Koodi pysyy yksinkertaisena
- ✅ Helppo lisätä uusia tyyppejä

**Lue lisää:** [Polymorfismi (Polymorphism)](Polymorphism.md)

---

### 4. 🎨 Abstraktio (Abstraction)

**"Piilota monimutkaisuus, näytä vain olennainen"**

Abstraktio tarkoittaa että **keskityt MITÄ tehdään, ei MITEN**.

```csharp
// Abstrakti luokka - ei voi luoda suoraan
public abstract class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    // Abstrakti metodi - PAKKO toteuttaa aliluokissa
    public abstract double CalculateArea();
    
    // Tavallinen metodi - voi käyttää suoraan
    public void Display()
    {
        Console.WriteLine($"{Color} {Name}, Pinta-ala: {CalculateArea():F2}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }
    
    public override double CalculateArea()
    {
        return Width * Height;
    }
}

// Käyttö:
Shape[] shapes = new Shape[]
{
    new Circle { Name = "Ympyrä", Color = "Punainen", Radius = 5 },
    new Rectangle { Name = "Suorakulmio", Color = "Sininen", Width = 4, Height = 6 }
};

foreach (Shape shape in shapes)
{
    shape.Display(); // ✅ Polymorfismi + Abstraktio!
}
```

**Miksi tärkeää?**
- ✅ Pakottaa yhtenäisen rakenteen
- ✅ Piilottaa monimutkaisuuden
- ✅ Helppo laajentaa

**Lue lisää:** [Rajapinnat (Interfaces)](Interfaces.md) ja [Polymorfismi](Polymorphism.md)

---

## OOP:n lisätekniikat

### 5. 🧩 Yhdistäminen (Composition)

**"Rakenna monimutkaiset objektit yksinkertaisista osista"**

Composition kuvaa **"has-a"** (omistaa) -suhdetta: "Autolla ON moottori".

```csharp
// Osat
public class Engine
{
    public void Start() => Console.WriteLine("Moottori käynnistyy");
    public void Stop() => Console.WriteLine("Moottori sammuu");
}

public class Wheel
{
    public string Brand { get; set; }
    public void Rotate() => Console.WriteLine($"{Brand} rengas pyörii");
}

// Auto koostuu osista
public class Car
{
    private Engine engine;    // Car HAS-A Engine
    private Wheel[] wheels;   // Car HAS-A Wheels
    
    public string Brand { get; set; }
    
    public Car(string brand)
    {
        Brand = brand;
        engine = new Engine();
        wheels = new Wheel[4]
        {
            new Wheel { Brand = "Michelin" },
            new Wheel { Brand = "Michelin" },
            new Wheel { Brand = "Michelin" },
            new Wheel { Brand = "Michelin" }
        };
    }
    
    public void Start()
    {
        Console.WriteLine($"{Brand} käynnistyy");
        engine.Start();
        foreach (Wheel wheel in wheels)
        {
            wheel.Rotate();
        }
    }
    
    public void Stop()
    {
        Console.WriteLine($"{Brand} pysähtyy");
        engine.Stop();
    }
}

// Käyttö:
Car car = new Car("Toyota");
car.Start();
car.Stop();
```

**Miksi tärkeää?**
- ✅ Joustavampi kuin perintä
- ✅ Voit vaihtaa osia ajonaikana
- ✅ Välttää syvän perinnän hierarkian

**"Composition over Inheritance"** - suosi yhdistämistä perinnän sijaan!

**Lue lisää:** [Yhdistäminen (Composition)](Composition.md)

---

### 6. 🔌 Rajapinnat (Interfaces)

**"Määrittele 'sopimus' mitä luokan pitää toteuttaa"**

Rajapinnat määrittelevät **MITÄ** pitää tehdä, mutta ei **MITEN**.

```csharp
// Rajapinta - "sopimus"
public interface IFlyable
{
    void TakeOff();
    void Fly();
    void Land();
}

// Luokat toteuttavat sopimuksen
public class Airplane : IFlyable
{
    public void TakeOff() => Console.WriteLine("Lentokone nousee kiitotieltä");
    public void Fly() => Console.WriteLine("Lentokone lentää");
    public void Land() => Console.WriteLine("Lentokone laskeutuu");
}

public class Bird : IFlyable
{
    public void TakeOff() => Console.WriteLine("Lintu lähtee lentoon");
    public void Fly() => Console.WriteLine("Lintu lentää");
    public void Land() => Console.WriteLine("Lintu laskeutuu");
}

// Käyttö - polymorfismi rajapintojen kanssa
IFlyable[] flyers = new IFlyable[]
{
    new Airplane(),
    new Bird()
};

foreach (IFlyable flyer in flyers)
{
    flyer.TakeOff();
    flyer.Fly();
    flyer.Land();
    Console.WriteLine();
}
```

**Miksi tärkeää?**
- ✅ Luokka voi toteuttaa **useita** rajapintoja (vs yksi yläluokka)
- ✅ Löyhä kytkentä (loose coupling)
- ✅ Helppo testata (mock-objektit)

**Lue lisää:** [Rajapinnat (Interfaces)](Interfaces.md)

---

## OOP vs muut paradigmat

### Proseduraalinen ohjelmointi (C, Pascal)

```csharp
// Proseduraalinen tyyli
string[] names = new string[100];
int[] ages = new int[100];

void PrintPerson(int index)
{
    Console.WriteLine($"{names[index]}, {ages[index]}");
}
```

**Ominaisuudet:**
- ✅ Yksinkertainen pieniin ohjelmiin
- ❌ Vaikea hallita suuria ohjelmia
- ❌ Data ja logiikka erillään

### Funktionaalinen ohjelmointi (F#, Haskell)

```csharp
// Funktionaalinen tyyli C#:ssa
var adults = people
    .Where(p => p.Age >= 18)
    .Select(p => p.Name)
    .ToList();
```

**Ominaisuudet:**
- ✅ Immutable data
- ✅ Puhdas funktiot (ei sivuvaikutuksia)
- ⚠️ Voi olla vaikea ymmärtää

### Olio-ohjelmointi (C#, Java, Python)

```csharp
// OOP tyyli
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    
    public bool IsAdult() => Age >= 18;
}

List<Person> adults = people.Where(p => p.IsAdult()).ToList();
```

**Ominaisuudet:**
- ✅ Selkeä rakenne
- ✅ Helppo mallintaa todellista maailmaa
- ✅ Hyvä suuriin projekteihin

**Todellisuudessa:** Moderni C# yhdistää kaikkia paradigmoja!

---

## OOP:n edut ja haitat

### ✅ Edut:

1. **Uudelleenkäytettävyys**
```csharp
// Luo kerran, käytä monesti
public class Logger
{
    public void Log(string message) { }
}

// Käytetään monessa projektissa
```

2. **Modulaarisuus**
```csharp
// Jaa iso ongelma pienempiin osiin
public class Car
{
    private Engine engine;
    private GPS gps;
    private Radio radio;
}
```

3. **Ylläpidettävyys**
```csharp
// Muutokset paikallisia
public class BankAccount
{
    // Muuta vain tätä luokkaa, ei kaikkea koodia
}
```

4. **Skaalautuvuus**
```csharp
// Helppo lisätä uusia ominaisuuksia
public class NewAnimal : Animal { }
```

5. **Testattavuus**
```csharp
// Testaa luokat erikseen
[Test]
public void BankAccount_Deposit_IncreasesBalance()
{
    BankAccount account = new BankAccount();
    account.Deposit(100);
    Assert.AreEqual(100, account.Balance);
}
```

### ❌ Haitat:

1. **Monimutkaisuus**
- Voi olla liian monimutkaista pieniin ohjelmiin
- Oppimiskäyrä jyrkempi

2. **Suorituskyky**
- Hieman hitaampi kuin proseduraalinen (mutta harvoin ongelma)
- Enemmän muistia

3. **Ylitutkittu**
- Helppo tehdä liian monimutkainen rakenne
- "God objects" - liian isot luokat

**Ratkaisu:** Käytä OOP:ta **järkevästi** - älä pakota kaikkea objekteihin.

---

## Milloin käyttää OOP:ta?

### ✅ Käytä OOP:ta kun:

- ✅ Suuret projektit (1000+ riviä)
- ✅ Tiimi kehittää yhdessä
- ✅ Haluat uudelleenkäyttää koodia
- ✅ Mallinnat todellista maailmaa (auto, tili, käyttäjä)
- ✅ Projekti kasvaa ajan myötä

### ⚠️ Harkitse vaihtoehtoja kun:

- ⚠️ Pieni skripti (<100 riviä)
- ⚠️ Yksinkertainen data-käsittely
- ⚠️ Suorituskyky on kriittinen (game loop, reaaliaikainen)

**Muista:** C# tukee useita paradigmoja - käytä parasta työkalua työhön!

---

## Yhteenveto

### OOP:n neljä pilaria:

| Pilari | Kuvaus | Avain |
|--------|--------|-------|
| **Kapselointi** | Piilota sisäiset yksityiskohdat | Data + Metodit yhdessä |
| **Perintä** | Jaa yhteinen toiminnallisuus | "Is-a" suhde |
| **Polymorfismi** | Käsittele eri objekteja samalla tavalla | Sama rajapinta |
| **Abstraktio** | Piilota monimutkaisuus | MITÄ, ei MITEN |

### Lisätekniikat:

- **Composition** - Rakenna osista ("has-a")
- **Interfaces** - Määrittele sopimuksia

### Miksi OOP?

- ✅ Helppo mallintaa todellista maailmaa
- ✅ Selkeä rakenne suuriin projekteihin
- ✅ Uudelleenkäytettävä ja ylläpidettävä koodi
- ✅ Helppo testata
- ✅ Tiimityöhön sopiva

---

## Seuraavat askeleet

### 1. **Syvenny yksittäisiin konsepteihin:**

Suositeltu oppimisjärjestys:

1. [Kapselointi (Encapsulation)](Encapsulation.md) - Aloita tästä!
2. [Perintä (Inheritance)](Inheritance.md)
3. [Polymorfismi (Polymorphism)](Polymorphism.md)
4. [Rajapinnat (Interfaces)](Interfaces.md)
5. [Yhdistäminen (Composition)](Composition.md)

### 2. **Katso yleiskuvaus:**

- [OOP-tekniikat - Yleiskuvaus](OOP-Techniques-Overview.md) - Kaikkien tekniikoiden yhteenveto

### 3. **Jatka edistyneisiin aiheisiin:**

- [Design Principles](../04-Advanced/Design-Principles.md) - SOLID-periaatteet
- [Design Patterns](../04-Advanced/Design-Patterns.md) - Valmiit ratkaisumallit

---

**Valmis aloittamaan?** Aloita [Kapselointi (Encapsulation)](Encapsulation.md) materiaalista ja etene järjestyksessä!

