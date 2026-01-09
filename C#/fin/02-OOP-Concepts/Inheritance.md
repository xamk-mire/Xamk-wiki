# Perintä (Inheritance)

## Perinnän ongelma, joka ratkaistaan

Koodin toistuminen, moninkertainen kopiointi ja hankalasti hallittavat rinnakkaiset luokkien versiot.

## Ratkaisu

Perintä sallii uuden luokan (aliluokan) periä olemassa olevan luokan (yläluokan) ominaisuudet ja metodit, jolloin koodin uudelleenkäyttö ja ylläpito helpottuvat. Perintä kuvaa usein **"on-suhdetta"** (esim. "Koira on Eläin").

## Ilman perintää (ongelma)

```csharp
// ❌ HUONO: Koodin toistoa
public class Dog
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
    
    public void Bark()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
}

public class Cat
{
    public string Name { get; set; } // Toistoa!
    public int Age { get; set; }     // Toistoa!
    
    public void Eat()                 // Toistoa!
    {
        Console.WriteLine($"{Name} syö");
    }
    
    public void Sleep()               // Toistoa!
    {
        Console.WriteLine($"{Name} nukkuu");
    }
    
    public void Meow()
    {
        Console.WriteLine($"{Name} naukuu: Miau!");
    }
}
```

**Ongelmat:**
- Sama koodi toistuu useassa luokassa
- Muutokset täytyy tehdä useassa paikassa
- Vaikea ylläpitää

## Perinnän avulla (ratkaisu)

### Perussyntaksi

```csharp
// Yläluokka (base/parent class)
public class BaseClass
{
    // Yläluokan jäsenet
}

// Aliluokka (derived/child class) - perii yläluokan
public class DerivedClass : BaseClass
{
    // Aliluokan jäsenet
    // Voi käyttää yläluokan jäseniä
    // Voi ylikirjoittaa yläluokan metodeja
}
```

### Perusperintä

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
    
    // Virtual-metodi, joka voidaan ylikirjoittaa
    public virtual void MakeSound()
    {
        Console.WriteLine($"{Name} tekee ääntä");
    }
}

// ✅ Aliluokka (derived class) - perii Animal-luokan
public class Dog : Animal
{
    // Ylikirjoitetaan MakeSound-metodi
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
    
    // Uusi metodi, joka on vain Dog-luokassa
    public void Fetch()
    {
        Console.WriteLine($"{Name} hakee pallon");
    }
}

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
```

### Käyttöesimerkki:

```csharp
Dog dog = new Dog { Name = "Rex", Age = 3 };
dog.Eat();        // Peritty Animal-luokasta
dog.Sleep();      // Peritty Animal-luokasta
dog.MakeSound();  // Ylikirjoitettu versio: "Rex haukkuu: Hau hau!"
dog.Fetch();      // Vain Dog-luokassa

Cat cat = new Cat { Name = "Whiskers", Age = 2 };
cat.Eat();        // Peritty Animal-luokasta
cat.MakeSound();  // Ylikirjoitettu versio: "Whiskers naukuu: Miau!"
cat.Climb();      // Vain Cat-luokassa
```

## Base-luokan konstruktorin kutsuminen

```csharp
public class Vehicle
{
    public string Brand { get; set; }
    public int Year { get; set; }
    
    public Vehicle(string brand, int year)
    {
        Brand = brand;
        Year = year;
    }
    
    public virtual void Start()
    {
        Console.WriteLine($"{Brand} käynnistyy");
    }
}

public class Car : Vehicle
{
    public int NumberOfDoors { get; set; }
    
    // base-käsky kutsuu yläluokan konstruktoria
    public Car(string brand, int year, int numberOfDoors) 
        : base(brand, year)
    {
        NumberOfDoors = numberOfDoors;
    }
    
    public override void Start()
    {
        base.Start(); // Kutsutaan yläluokan metodia
        Console.WriteLine($"Autossa on {NumberOfDoors} ovea");
    }
}

// Käyttö
Car car = new Car("Toyota", 2023, 4);
car.Start();
// Tulostaa:
// Toyota käynnistyy
// Autossa on 4 ovea
```

## Perinnän hyödyt

1. **Koodin uudelleenkäyttö**: Yhteinen toiminnallisuus määritellään kerran
2. **Hierarkkinen rakenne**: Luokkien väliset suhteet selkeämpiä
3. **Ylläpidettävyys**: Muutokset yläluokassa vaikuttavat automaattisesti aliluokkiin
4. **Polymorfismi**: Aliluokkia voidaan käsitellä yläluokan kautta

## Tärkeät huomiot

- C# tukee vain **yksittäistä perintää** luokkien välillä (yksi yläluokka)
- **Rajapinnat** mahdollistavat moniperinnän kaltaisen toiminnallisuuden
- `virtual`-avainsana yläluokassa sallii metodin ylikirjoittamisen
- `override`-avainsana aliluokassa ylikirjoittaa yläluokan metodin
- `base`-avainsana viittaa yläluokkaan

## Yhteenveto

Perintä on tehokas työkalu koodin organisoimiseen ja uudelleenkäyttöön. Se mahdollistaa luokkien hierarkkisen rakenteen ja vähentää koodin toistoa merkittävästi.

