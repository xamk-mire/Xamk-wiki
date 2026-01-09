# Polymorfismi (Polymorphism)

## Polymorfismin ongelma, joka ratkaistaan

Tarve käsitellä luokkien olioita **yhtenäisellä** tavalla ilman, että kutsujan täytyy tietää tarkka toteutus.

## Ratkaisu

Polymorfismi mahdollistaa sen, että sama metodikutsu voi toimia eri tavoin riippuen siitä, minkä luokan olio (ylä- vai aliluokka) on kyseessä. C#-kielessä polymorfismin toteuttaa esimerkiksi `virtual`, `override`, `abstract` sekä interfacet.

## Metodin kutsut ilman polymorfismia (ongelma)

```csharp
// ❌ HUONO: Jokainen eläintyyppi käsitellään erikseen
public class Animal
{
    public string Name { get; set; }
}

public class Dog : Animal { }
public class Cat : Animal { }
public class Bird : Animal { }

// Ongelma: Pitää tarkistaa tyyppi ja kutsua eri metodia
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

// Käyttö
Dog dog = new Dog { Name = "Rex" };
Cat cat = new Cat { Name = "Whiskers" };
MakeAnimalSound(dog);
MakeAnimalSound(cat);
```

**Ongelmat:**
- Pitää tietää jokainen tyyppi erikseen
- Koodi monimutkaistuu uusien tyyppien lisätessä
- Vaikea ylläpitää

## Polymorfismin avulla (ratkaisu)

### Vaihtoehto 1: Virtual ja Override

```csharp
// ✅ HYVÄ: Polymorfismi virtual/override -avainsanoilla
public class Animal
{
    public string Name { get; set; }
    
    // Virtual-metodi, joka voidaan ylikirjoittaa
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} tekee ääntä");
    }
}

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

public class Bird : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} laulaa: Tsirp tsirp!");
    }
}

// ✅ Yhtenäinen käsittely - ei tarvitse tietää tarkkaa tyyppiä!
public void MakeAnimalSound(Animal animal)
{
    animal.MakeSound(); // Kutsutaan oikea versio automaattisesti
}

// Käyttö
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

### Vaihtoehto 2: Abstract-luokat

```csharp
// ✅ Abstract-luokka - ei voi luoda suoraan instanssia
public abstract class Shape
{
    public string Name { get; set; }
    
    // Abstract-metodi - täytyy toteuttaa aliluokissa
    public abstract double CalculateArea();
    
    // Tavallinen metodi - voidaan käyttää suoraan
    public virtual void DisplayInfo()
    {
        Console.WriteLine($"Muoto: {Name}, Pinta-ala: {CalculateArea()}");
    }
}

public class Circle : Shape
{
    public double Radius { get; set; }
    
    public Circle(double radius)
    {
        Name = "Ympyrä";
        Radius = radius;
    }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }
    
    public Rectangle(double width, double height)
    {
        Name = "Suorakulmio";
        Width = width;
        Height = height;
    }
    
    public override double CalculateArea()
    {
        return Width * Height;
    }
}

// Käyttö
Shape[] shapes = new Shape[]
{
    new Circle(5.0),
    new Rectangle(4.0, 6.0)
};

foreach (Shape shape in shapes)
{
    shape.DisplayInfo(); // Kutsutaan oikea CalculateArea() automaattisesti
}
```

### Vaihtoehto 3: Metodin ylikuormitus (Method Overloading)

```csharp
// ✅ Polymorfismi metodin ylikuormituksella
public class Calculator
{
    // Sama metodi, eri parametrit
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
    
    public string Summa(string a, string b)
    {
        return a + b; // Yhdistää merkkijonot
    }
}

// Käyttö
Calculator calc = new Calculator();
int result1 = calc.Summa(5, 3);           // 8
double result2 = calc.Summa(5.5, 3.2);    // 8.7
int result3 = calc.Summa(1, 2, 3);        // 6
string result4 = calc.Summa("Hei", " maailma"); // "Hei maailma"
```

## Polymorfismin hyödyt

1. **Joustavuus**: Sama koodi toimii eri tyyppisille olioille
2. **Laajennettavuus**: Uusia tyyppejä voidaan lisätä helposti
3. **Ylläpidettävyys**: Vähemmän ehdollisia lauseita
4. **Luettavuus**: Koodi on selkeämpää ja helpommin ymmärrettävää

## Yhteenveto

Polymorfismi on olio-ohjelmoinnin keskeinen konsepti, joka mahdollistaa joustavan ja laajennettavan koodin. Se vähentää koodin monimutkaisuutta ja parantaa ylläpidettävyyttä.

