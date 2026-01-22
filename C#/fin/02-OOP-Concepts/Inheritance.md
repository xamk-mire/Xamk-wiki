# Perintä (Inheritance)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mitä perintä on?](#mitä-perintä-on)
3. [Ongelma joka ratkaistaan](#ongelma-joka-ratkaistaan)
4. [Perussyntaksi](#perussyntaksi)
5. [Virtual, Override ja Base](#virtual-override-ja-base)
6. [Abstract-luokat](#abstract-luokat)
7. [Sealed-luokat](#sealed-luokat)
8. [Perint hierarkiat](#perintähierarkiat)
9. [Milloin käyttää perintää?](#milloin-käyttää-perintää)
10. [Sudenkuopat ja varoitukset](#sudenkuopat-ja-varoitukset)
11. [Best Practices](#best-practices)
12. [Yhteenveto](#yhteenveto)

---

## Johdanto

Perintä on yksi olio-ohjelmoinnin neljästä peruspilarista. Se mahdollistaa **koodin uudelleenkäytön** ja **hierarkkisten rakenteiden** luomisen.

**Lyhyesti:** Perintä kuvaa **"is-a"** (on) -suhdetta: "Koira ON eläin", "Auto ON ajoneuvo".

---

## Mitä perintä on?

Perintä on mekanismi, jossa **uusi luokka (aliluokka/derived class)** voi periä **olemassa olevan luokan (yläluokka/base class)** ominaisuudet ja metodit.

```csharp
// Yläluokka (base class, parent class, superclass)
public class Animal
{
    public string Name { get; set; }
    public void Eat() => Console.WriteLine($"{Name} syö");
}

// Aliluokka (derived class, child class, subclass)
public class Dog : Animal  // Dog perii Animalin
{
    public void Bark() => Console.WriteLine($"{Name} haukkuu");
}

// Käyttö:
Dog dog = new Dog { Name = "Rex" };
dog.Eat();  // ✅ Peritty Animalista
dog.Bark(); // ✅ Dog:n oma metodi
```

**Perinnän hyödyt:**
- ✅ Välttää koodin toistoa (DRY - Don't Repeat Yourself)
- ✅ Luo loogisia hierarkioita
- ✅ Mahdollistaa polymorfismin
- ✅ Helpottaa ylläpitoa

---

## Ongelma joka ratkaistaan

### Ilman perintää (ongelma)

```csharp
// ❌ HUONO: Sama koodi toistuu useassa luokassa
public class Dog
{
    public string Name { get; set; }      // Toistoa!
    public int Age { get; set; }          // Toistoa!
    public string Species { get; set; }   // Toistoa!
    
    public void Eat()                     // Toistoa!
    {
        Console.WriteLine($"{Name} syö");
    }
    
    public void Sleep()                   // Toistoa!
    {
        Console.WriteLine($"{Name} nukkuu");
    }
    
    public void Bark()                    // Vain Dog:ssa
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
}

public class Cat
{
    public string Name { get; set; }      // Toistoa!
    public int Age { get; set; }          // Toistoa!
    public string Species { get; set; }   // Toistoa!
    
    public void Eat()                     // Toistoa!
    {
        Console.WriteLine($"{Name} syö");
    }
    
    public void Sleep()                   // Toistoa!
    {
        Console.WriteLine($"{Name} nukkuu");
    }
    
    public void Meow()                    // Vain Cat:ssa
    {
        Console.WriteLine($"{Name} naukuu: Miau!");
    }
}

public class Bird
{
    // ... sama toisto jatkuu...
}
```

**Ongelmat:**
- ❌ Koodi toistuu
- ❌ Muutokset pitää tehdä useassa paikassa
- ❌ Helppo unohtaa päivittää jotain luokkaa
- ❌ Vaikea ylläpitää
- ❌ Ei skaalaudu (10+ eläintä = paljon toistoa)

### Perinnän avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Yhteinen toiminnallisuus yläluokassa
public class Animal
{
    // Yhteiset ominaisuudet
    public string Name { get; set; }
    public int Age { get; set; }
    public string Species { get; set; }
    
    // Yhteiset metodit
    public void Eat()
    {
        Console.WriteLine($"{Name} syö");
    }
    
    public void Sleep()
    {
        Console.WriteLine($"{Name} nukkuu");
    }
    
    // Virtual-metodi, jonka aliluokat voivat ylikirjoittaa
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} tekee ääntä");
    }
}

// ✅ Dog perii Animalin - ei toistoa!
public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
    
    public void Fetch()
    {
        Console.WriteLine($"{Name} hakee pallon");
    }
}

// ✅ Cat perii Animalin - ei toistoa!
public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} naukuu: Miau!");
    }
    
    public void Climb()
    {
        Console.WriteLine($"{Name} kiipeää puuhun");
    }
}

// ✅ Bird perii Animalin - ei toistoa!
public class Bird : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} laulaa: Tsirp tsirp!");
    }
    
    public void Fly()
    {
        Console.WriteLine($"{Name} lentää");
    }
}
```

**Hyödyt:**
- ✅ Yhteinen koodi yhdessä paikassa
- ✅ Muutokset tehdään kerran
- ✅ Helppo lisätä uusia eläimiä
- ✅ Selkeä rakenne

---

## Perussyntaksi

### Yksinkertainen perintä

```csharp
// Perusmuoto:
public class BaseClass
{
    // Yläluokan jäsenet
}

public class DerivedClass : BaseClass
{
    // Aliluokan jäsenet + perityt jäsenet
}
```

### Esimerkki: Ajoneuvo-hierarkia

```csharp
// Yläluokka
public class Vehicle
{
    public string Brand { get; set; }
    public int Year { get; set; }
    public string Color { get; set; }
    
    public void Start()
    {
        Console.WriteLine($"{Brand} käynnistyy");
    }
    
    public void Stop()
    {
        Console.WriteLine($"{Brand} sammuu");
    }
    
    public virtual void Honk()
    {
        Console.WriteLine("Tööt!");
    }
}

// Aliluokka: Car
public class Car : Vehicle
{
    public int NumberOfDoors { get; set; }
    public string BodyType { get; set; } // Sedan, SUV, Coupe...
    
    public override void Honk()
    {
        Console.WriteLine("Beep beep!");
    }
    
    public void OpenTrunk()
    {
        Console.WriteLine("Tavaratila avattu");
    }
}

// Aliluokka: Motorcycle
public class Motorcycle : Vehicle
{
    public bool HasSidecar { get; set; }
    
    public override void Honk()
    {
        Console.WriteLine("Vruum vruum!");
    }
    
    public void DoWheelie()
    {
        Console.WriteLine("Takapyörä ilmassa!");
    }
}

// Käyttö:
Car car = new Car 
{ 
    Brand = "Toyota", 
    Year = 2023, 
    Color = "Sininen",
    NumberOfDoors = 4,
    BodyType = "Sedan"
};

car.Start();        // Peritty Vehicle:sta
car.Honk();         // Ylikirjoitettu versio
car.OpenTrunk();    // Car:n oma metodi
```

---

## Virtual, Override ja Base

### Virtual - Metodi joka voidaan ylikirjoittaa

```csharp
public class Animal
{
    // Virtual - aliluokat VOIVAT ylikirjoittaa (mutta eivät pakko)
    public virtual void MakeSound()
    {
        Console.WriteLine("Joku ääni");
    }
    
    // Tavallinen metodi - EI VOI ylikirjoittaa
    public void Breathe()
    {
        Console.WriteLine("Hengittää");
    }
}
```

### Override - Ylikirjoita yläluokan metodi

```csharp
public class Dog : Animal
{
    // Override - ylikirjoittaa yläluokan virtual-metodin
    public override void MakeSound()
    {
        Console.WriteLine("Hau hau!");
    }
}
```

### Base - Viittaa yläluokkaan

```csharp
public class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    public Shape(string name, string color)
    {
        Name = name;
        Color = color;
        Console.WriteLine($"Shape luotu: {name}");
    }
    
    public virtual double CalculateArea()
    {
        return 0;
    }
    
    public virtual void Display()
    {
        Console.WriteLine($"Muoto: {Name}, Väri: {Color}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    // Konstruktori kutsuu yläluokan konstruktoria
    public Circle(string name, string color, double radius) 
        : base(name, color)  // ← Kutsuu Shape konstruktoria
    {
        Radius = radius;
        Console.WriteLine($"Circle luotu, säde: {radius}");
    }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public override void Display()
    {
        base.Display();  // ← Kutsuu yläluokan Display-metodia
        Console.WriteLine($"Säde: {Radius}, Pinta-ala: {CalculateArea():F2}");
    }
}

// Käyttö:
Circle circle = new Circle("Ympyrä", "Punainen", 5.0);
circle.Display();
// Tulostaa:
// Shape luotu: Ympyrä
// Circle luotu, säde: 5
// Muoto: Ympyrä, Väri: Punainen
// Säde: 5, Pinta-ala: 78.54
```

### New - Piilottaa yläluokan metodi (harvoin käytetty)

```csharp
public class Base
{
    public void Method()
    {
        Console.WriteLine("Base method");
    }
}

public class Derived : Base
{
    // new - piilottaa yläluokan metodin (EI ylikirjoita!)
    public new void Method()
    {
        Console.WriteLine("Derived method");
    }
}

// Käyttö:
Derived d = new Derived();
d.Method(); // "Derived method"

Base b = d;
b.Method(); // "Base method" ← Huomaa! Eri kuin override
```

⚠️ **Varoitus:** `new` on erilainen kuin `override`. Yleensä `override` on parempi valinta.

---

## Abstract-luokat

**Abstract-luokka** on luokka, josta **ei voi luoda suoraa instanssia**. Se on tarkoitettu vain yläluokaksi.

### Milloin käyttää?
- Kun haluat määritellä yhteisen perustan, mutta ei ole järkevää luoda sen instanssia
- Kun haluat pakottaa aliluokat toteuttamaan tiettyjä metodeja

### Esimerkki: Muodot

```csharp
// ❌ Ei voi luoda instanssia: new Shape() ei toimi
public abstract class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    // Abstract-metodi - PAKKO toteuttaa aliluokissa
    public abstract double CalculateArea();
    public abstract double CalculatePerimeter();
    
    // Tavallinen metodi - voidaan käyttää suoraan
    public virtual void Display()
    {
        Console.WriteLine($"Muoto: {Name}, Väri: {Color}");
        Console.WriteLine($"Pinta-ala: {CalculateArea():F2}");
        Console.WriteLine($"Ympärysmitta: {CalculatePerimeter():F2}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    // PAKKO toteuttaa abstract-metodit
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public override double CalculatePerimeter()
    {
        return 2 * Math.PI * Radius;
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
    
    public override double CalculatePerimeter()
    {
        return 2 * (Width + Height);
    }
}

public class Triangle : Shape
{
    public double Base { get; set; }
    public double Height { get; set; }
    public double SideA { get; set; }
    public double SideB { get; set; }
    public double SideC { get; set; }
    
    public override double CalculateArea()
    {
        return 0.5 * Base * Height;
    }
    
    public override double CalculatePerimeter()
    {
        return SideA + SideB + SideC;
    }
}

// Käyttö:
// Shape shape = new Shape(); // ❌ EI TOIMI - abstract!

Shape circle = new Circle { Name = "Ympyrä", Color = "Sininen", Radius = 5 };
Shape rectangle = new Rectangle { Name = "Suorakulmio", Color = "Punainen", Width = 4, Height = 6 };

circle.Display();
rectangle.Display();

// Polymorfismi:
Shape[] shapes = { circle, rectangle };
foreach (Shape shape in shapes)
{
    shape.Display(); // Jokainen käyttää omaa toteutustaan
}
```

### Abstract vs Virtual

| Ominaisuus | Abstract | Virtual |
|------------|----------|---------|
| Toteutus | Ei toteutusta | On toteutus |
| Ylikirjoitus | PAKKO ylikirjoittaa | Voi ylikirjoittaa (ei pakko) |
| Luokka | Vain abstract-luokissa | Missä tahansa luokassa |
| Instanssi | Ei voi luoda | Voi luoda |

---

## Sealed-luokat

**Sealed-luokka** on luokka, josta **ei voi periä**.

### Milloin käyttää?
- Kun haluat estää perinnän
- Turvallisuussyistä
- Suorituskyky (pieni optimointi)

```csharp
// ✅ Sealed - ei voi periä
public sealed class FinalClass
{
    public void DoSomething()
    {
        Console.WriteLine("Tämä toimii");
    }
}

// ❌ EI TOIMI - ei voi periä sealed-luokasta
// public class DerivedClass : FinalClass
// {
// }
```

### Sealed-metodit

```csharp
public class Base
{
    public virtual void Method()
    {
        Console.WriteLine("Base");
    }
}

public class Middle : Base
{
    // Sealed - estää lisäylikirjoituksen
    public sealed override void Method()
    {
        Console.WriteLine("Middle");
    }
}

public class Final : Middle
{
    // ❌ EI TOIMI - Method on sealed
    // public override void Method() { }
}
```

---

## Perintähierarkiat

### Syvyys vs. Leveys

```csharp
// ❌ HUONO: Liian syv perinnähierarkia
Animal
  ↓
Mammal
  ↓
Carnivore
  ↓
Canine
  ↓
Dog
  ↓
Labrador  // 6 tasoa!

// ✅ HYVÄ: Matalampi hierarkia
Animal
  ↓
Dog (sisältää rodun propertyna, ei perintänä)
```

**Suositus:** Pidä perintähierarkia matalana (max 2-3 tasoa).

### Esimerkki: Työntekijät

```csharp
// Perushierarkia
public abstract class Employee
{
    public string Name { get; set; }
    public int Id { get; set; }
    public decimal BaseSalary { get; set; }
    
    public abstract decimal CalculateSalary();
    
    public virtual void Display()
    {
        Console.WriteLine($"ID: {Id}, Nimi: {Name}, Palkka: {CalculateSalary():C}");
    }
}

public class FullTimeEmployee : Employee
{
    public decimal MonthlyBonus { get; set; }
    
    public override decimal CalculateSalary()
    {
        return BaseSalary + MonthlyBonus;
    }
}

public class PartTimeEmployee : Employee
{
    public int HoursWorked { get; set; }
    public decimal HourlyRate { get; set; }
    
    public override decimal CalculateSalary()
    {
        return HoursWorked * HourlyRate;
    }
}

public class Contractor : Employee
{
    public decimal ProjectFee { get; set; }
    
    public override decimal CalculateSalary()
    {
        return ProjectFee;
    }
}

// Käyttö:
Employee[] employees =
{
    new FullTimeEmployee { Name = "Matti", Id = 1, BaseSalary = 3000, MonthlyBonus = 500 },
    new PartTimeEmployee { Name = "Liisa", Id = 2, HoursWorked = 80, HourlyRate = 25 },
    new Contractor { Name = "Pekka", Id = 3, ProjectFee = 5000 }
};

foreach (Employee emp in employees)
{
    emp.Display(); // Polymorfismi toiminnassa
}
```

---

## Milloin käyttää perintää?

### ✅ Käytä perintää kun:

1. **"Is-a" suhde on todella selvä**
```csharp
Dog is Animal  // ✅ Selvä
Car is Vehicle // ✅ Selvä
```

2. **Haluat jakaa yhteistä toiminnallisuutta**
```csharp
public abstract class Animal
{
    public void Eat() { ... }     // Kaikki eläimet syövät
    public void Sleep() { ... }   // Kaikki eläimet nukkuvat
}
```

3. **Haluat käyttää polymorfismia**
```csharp
Animal[] animals = { new Dog(), new Cat(), new Bird() };
foreach (Animal animal in animals)
{
    animal.MakeSound(); // Jokainen tekee oman äänensä
}
```

### ❌ ÄLÄ käytä perintää kun:

1. **Suhde on "has-a" eikä "is-a"**
```csharp
// ❌ HUONO - Auto ei OLE moottori!
public class Car : Engine { }

// ✅ HYVÄ - Autolla ON moottori
public class Car
{
    private Engine engine;
}
```

2. **Haluat vain jakaa metodeja**
```csharp
// ❌ HUONO - väärinkäytä perintää jakamiseen
public class Logger
{
    public void Log(string msg) { ... }
}
public class UserService : Logger { } // ← Väärin!

// ✅ HYVÄ - käytä compositionia
public class UserService
{
    private Logger logger;
    public UserService(Logger logger) { this.logger = logger; }
}
```

3. **Luokka on jo liian monimutkainen**
```csharp
// ❌ Jos yläluokka on jo valtava, perintä tekee siitä vielä monimutkaisemman
```

---

## Sudenkuopat ja varoitukset

### 1. Fragile Base Class Problem

```csharp
// Yläluokan muutos voi rikkoa aliluokat
public class Base
{
    public virtual void Method()
    {
        Console.WriteLine("Base");
        Helper(); // Sisäinen kutsu
    }
    
    protected virtual void Helper()
    {
        Console.WriteLine("Helper");
    }
}

public class Derived : Base
{
    public override void Helper()
    {
        Console.WriteLine("Derived Helper");
        // Voi aiheuttaa yllätyksiä jos Base muuttuu
    }
}
```

**Ratkaisu:** Dokumentoi selkeästi mitä metodeja voi ylikirjoittaa ja miten.

### 2. Liskov Substitution Principle rikkominen

```csharp
// ❌ HUONO: Aliluokka rikkoo yläluokan sopimuksen
public class Bird
{
    public virtual void Fly()
    {
        Console.WriteLine("Lentää");
    }
}

public class Penguin : Bird
{
    public override void Fly()
    {
        throw new NotSupportedException("Pingviini ei voi lentää!");
    }
}

// Ongelma:
Bird bird = new Penguin();
bird.Fly(); // ❌ Heittää poikkeuksen - yllättävää!
```

**Ratkaisu:** Suunnittele hierarkia paremmin:
```csharp
// ✅ HYVÄ: Erota lentävät ja ei-lentävät
public abstract class Bird { }
public abstract class FlyingBird : Bird
{
    public abstract void Fly();
}
public class Sparrow : FlyingBird
{
    public override void Fly() { ... }
}
public class Penguin : Bird
{
    // Ei Fly-metodia!
}
```

### 3. Liian syvä hierarkia

```csharp
// ❌ HUONO: 6 tasoa perinnässä
GameObject → Entity → LivingEntity → Animal → Mammal → Dog

// ✅ HYVÄ: Matala hierarkia + composition
GameObject → Entity (sisältää komponentteja)
```

### 4. Yo-Yo Problem

```csharp
// Vaikea seurata mitä tapahtuu kun pitää hyppiä ylös alas hierarkiassa
public class A
{
    public virtual void Method() { B(); }
    protected virtual void B() { }
}

public class C : A
{
    protected override void B() { D(); }
    protected virtual void D() { }
}

public class E : C
{
    protected override void D() { }
}

// Vaikea ymmärtää mitä E.Method() tekee!
```

---

## Best Practices

### ✅ DO (Tee näin):

1. **Käytä perintää "is-a" suhteisiin**
```csharp
public class Dog : Animal { } // ✅ Koira ON eläin
```

2. **Pidä hierarkiat matalina (2-3 tasoa max)**
```csharp
Animal → Dog // ✅ Hyvä
```

3. **Käytä abstract-luokkia yhteiseen toiminnallisuuteen**
```csharp
public abstract class Shape
{
    public abstract double Area();
}
```

4. **Dokumentoi virtual-metodit**
```csharp
/// <summary>
/// Laskee muodon pinta-alan.
/// Aliluokkien TÄYTYY ylikirjoittaa tämä metodi.
/// </summary>
public virtual double CalculateArea() { ... }
```

5. **Käytä sealed estääksesi perinnän jos tarpeen**
```csharp
public sealed class SecurityCriticalClass { }
```

### ❌ DON'T (Älä tee näin):

1. **Älä käytä perintää vain jakamiseen**
```csharp
// ❌ UserService ei OLE Logger
public class UserService : Logger { }
```

2. **Älä tee liian syviä hierarkioita**
```csharp
// ❌ 6+ tasoa on liikaa
```

3. **Älä riko Liskov Substitution Principle**
```csharp
// ❌ Aliluokka ei saa rikkoa yläluokan sopimusta
```

4. **Älä käytä new piilottaaksesi metodeja**
```csharp
// ❌ Käytä override:a, ei new:ta
public new void Method() { }
```

---

## Yhteenveto

Perintä on voimakas työkalu, mutta sitä pitää käyttää viisaasti.

### Muista:
- ✅ Käytä "is-a" suhteisiin
- ✅ Pidä hierarkiat matalina
- ✅ Käytä abstract-luokkia sopivasti
- ✅ Dokumentoi virtual-metodit
- ✅ Mieti onko composition parempi vaihtoehto
- ✅ Noudata Liskov Substitution Principle

### Milloin perintä vs. composition?
- **Perintä**: Selkeä "is-a" suhde, yhteinen toiminnallisuus
- **Composition**: "Has-a" suhde, joustavuus, vähemmän kytkentää

**Seuraava askel:** Kun hallitset perinnän, jatka [Polymorfismi (Polymorphism)](Polymorphism.md) materiaaliin, joka rakentuu perinnän päälle.

---

