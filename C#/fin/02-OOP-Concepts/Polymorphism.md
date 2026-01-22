# Polymorfismi (Polymorphism)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mitä polymorfismi on?](#mitä-polymorfismi-on)
3. [Ongelma joka ratkaistaan](#ongelma-joka-ratkaistaan)
4. [Compile-time Polymorfismi](#compile-time-polymorfismi)
5. [Runtime Polymorfismi](#runtime-polymorfismi)
6. [Abstract Classes ja Polymorfismi](#abstract-classes-ja-polymorfismi)
7. [Interface-pohjainen Polymorfismi](#interface-pohjainen-polymorfismi)
8. [Käytännön esimerkit](#käytännön-esimerkit)
9. [Polymorfismin hyödyt](#polymorfismin-hyödyt)
10. [Best Practices](#best-practices)
11. [Yleiset virheet](#yleiset-virheet)
12. [Yhteenveto](#yhteenveto)

---

## Johdanto

Polymorfismi (kreikaksi "moni muoto") on yksi olio-ohjelmoinnin neljästä peruspilarista. Se mahdollistaa **saman rajapinnan käyttämisen eri objektityypeille**.

**Lyhyesti:** Polymorfismi tarkoittaa että voit käsitellä eri tyyppisiä objekteja yhtenäisellä tavalla.

**Esimerkki:** Kaikki eläimet voivat tehdä ääntä, mutta jokainen eläin tekee oman äänensä.

---

## Mitä polymorfismi on?

Polymorfismi jakautuu kahteen päätyyppiin:

### 1. Compile-time Polymorfismi (Static Polymorfismi)
- **Method Overloading** - Sama metodin nimi, eri parametrit
- **Operator Overloading** - Operaattorien ylikuormitus
- Ratkaistaan **käännösaikana**

### 2. Runtime Polymorfismi (Dynamic Polymorfismi)
- **Method Overriding** - Ylikirjoitus perinnässä
- **Virtual metodit** - virtual/override
- **Abstract metodit** - abstract/override
- **Interface toteutukset** - IInterface
- Ratkaistaan **ajonaikana**

```csharp
// Yksinkertainen esimerkki:
Animal animal1 = new Dog();    // Polymorfismi
Animal animal2 = new Cat();    // Polymorfismi
Animal animal3 = new Bird();   // Polymorfismi

// Sama rajapinta, eri toteutukset:
animal1.MakeSound(); // "Hau hau!"
animal2.MakeSound(); // "Miau!"
animal3.MakeSound(); // "Tsirp tsirp!"
```

---

## Ongelma joka ratkaistaan

### Ilman polymorfismia (ongelma)

```csharp
// ❌ HUONO: Pitää tarkistaa jokainen tyyppi erikseen
public class AnimalHandler
{
    public void HandleAnimal(Animal animal)
    {
        // Joudumme tarkistamaan tyypin...
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
            Console.WriteLine("Tsirp!");
        }
        else if (animal is Horse)
        {
            Console.WriteLine("Hirnuu!");
        }
        else if (animal is Cow)
        {
            Console.WriteLine("Ammuu!");
        }
        // ... Jos meillä on 20 eläintyyppiä, tämä kasvaa valtavaksi!
    }
    
    public void FeedAnimals(List<Animal> animals)
    {
        foreach (Animal animal in animals)
        {
            // Sama ongelma jokaiselle operaatiolle...
            if (animal is Dog)
            {
                Console.WriteLine("Syötä koiraruokaa");
            }
            else if (animal is Cat)
            {
                Console.WriteLine("Syötä kissanruokaa");
            }
            // ... jne
        }
    }
}
```

**Ongelmat:**
- ❌ Paljon if-else lauseita
- ❌ Vaikea ylläpitää
- ❌ Uuden eläimen lisääminen vaatii muutoksia kaikkialle
- ❌ Helppo unohtaa päivittää jokin paikka
- ❌ Rikkoo Open/Closed Principle
- ❌ Ei skaalaudu

### Polymorfismin avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Polymorfismi hoitaa kaiken
public abstract class Animal
{
    public string Name { get; set; }
    
    // Virtual metodi - voidaan ylikirjoittaa
    public abstract void MakeSound();
    public abstract void Eat();
}

public class Dog : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} haukkuu: Hau hau!");
    }
    
    public override void Eat()
    {
        Console.WriteLine($"{Name} syö koiraruokaa");
    }
}

public class Cat : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} naukuu: Miau!");
    }
    
    public override void Eat()
    {
        Console.WriteLine($"{Name} syö kissanruokaa");
    }
}

public class Bird : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine($"{Name} laulaa: Tsirp tsirp!");
    }
    
    public override void Eat()
    {
        Console.WriteLine($"{Name} syö siemeniä");
    }
}

// ✅ Yksinkertainen, skaalautuva koodi
public class AnimalHandler
{
    public void HandleAnimal(Animal animal)
    {
        animal.MakeSound(); // ✅ Ei tyyppitarkistuksia!
    }
    
    public void FeedAnimals(List<Animal> animals)
    {
        foreach (Animal animal in animals)
        {
            animal.Eat(); // ✅ Yksinkertainen!
        }
    }
    
    public void ProcessAnimals(Animal[] animals)
    {
        foreach (Animal animal in animals)
        {
            animal.MakeSound();
            animal.Eat();
        }
    }
}

// Käyttö:
Animal[] animals = new Animal[]
{
    new Dog { Name = "Rex" },
    new Cat { Name = "Whiskers" },
    new Bird { Name = "Tweety" },
    new Dog { Name = "Buddy" }
};

AnimalHandler handler = new AnimalHandler();
handler.ProcessAnimals(animals);
// Tulostaa:
// Rex haukkuu: Hau hau!
// Rex syö koiraruokaa
// Whiskers naukuu: Miau!
// Whiskers syö kissanruokaa
// Tweety laulaa: Tsirp tsirp!
// Tweety syö siemeniä
// Buddy haukkuu: Hau hau!
// Buddy syö koiraruokaa
```

**Hyödyt:**
- ✅ Ei tyyppitarkistuksia
- ✅ Helppo lisätä uusia tyyppejä
- ✅ Koodi pysyy yksinkertaisena
- ✅ Skaalautuva
- ✅ Noudattaa Open/Closed Principle

---

## Compile-time Polymorfismi

### Method Overloading (Metodin ylikuormitus)

Sama metodin nimi, **eri parametrit**. Ratkaistaan **käännösaikana**.

```csharp
public class Calculator
{
    // Sama nimi "Add", eri parametrit
    public int Add(int a, int b)
    {
        Console.WriteLine("Int version");
        return a + b;
    }
    
    public double Add(double a, double b)
    {
        Console.WriteLine("Double version");
        return a + b;
    }
    
    public int Add(int a, int b, int c)
    {
        Console.WriteLine("Three parameters");
        return a + b + c;
    }
    
    public string Add(string a, string b)
    {
        Console.WriteLine("String version");
        return a + b;
    }
}

// Käyttö:
Calculator calc = new Calculator();
calc.Add(5, 3);           // Kutsuu int-versiota → 8
calc.Add(5.5, 3.2);       // Kutsuu double-versiota → 8.7
calc.Add(1, 2, 3);        // Kutsuu three parameter -versiota → 6
calc.Add("Hello", " World"); // Kutsuu string-versiota → "Hello World"
```

### Esimerkkejä Method Overloading:sta

```csharp
public class Printer
{
    // Eri tyyppien tulostus
    public void Print(int value)
    {
        Console.WriteLine($"Numero: {value}");
    }
    
    public void Print(string value)
    {
        Console.WriteLine($"Teksti: {value}");
    }
    
    public void Print(double value)
    {
        Console.WriteLine($"Desimaaliluku: {value:F2}");
    }
    
    public void Print(int[] values)
    {
        Console.WriteLine($"Array: [{string.Join(", ", values)}]");
    }
    
    // Eri määrä parametreja
    public void Print(string value, bool uppercase)
    {
        Console.WriteLine(uppercase ? value.ToUpper() : value);
    }
}

// Käyttö:
Printer printer = new Printer();
printer.Print(42);                    // "Numero: 42"
printer.Print("Hello");               // "Teksti: Hello"
printer.Print(3.14159);               // "Desimaaliluku: 3.14"
printer.Print(new int[] { 1, 2, 3 }); // "Array: [1, 2, 3]"
printer.Print("hello", true);         // "HELLO"
```

### Optional Parameters vs Overloading

```csharp
// Vaihtoehto 1: Overloading
public void Connect(string server)
{
    Connect(server, 80); // Oletusportti
}

public void Connect(string server, int port)
{
    Console.WriteLine($"Yhdistetään: {server}:{port}");
}

// Vaihtoehto 2: Optional parameters (usein parempi)
public void Connect(string server, int port = 80)
{
    Console.WriteLine($"Yhdistetään: {server}:{port}");
}

// Molemmat toimivat:
Connect("example.com");      // Käyttää porttia 80
Connect("example.com", 443); // Käyttää porttia 443
```

---

## Runtime Polymorfismi

### Method Overriding (Virtual/Override)

Aliluokka **ylikirjoittaa** yläluokan metodin. Ratkaistaan **ajonaikana**.

```csharp
// Yläluokka
public class Shape
{
    public string Name { get; set; }
    public string Color { get; set; }
    
    // Virtual - voidaan ylikirjoittaa
    public virtual double CalculateArea()
    {
        return 0;
    }
    
    public virtual void Draw()
    {
        Console.WriteLine($"Piirretään {Name}");
    }
    
    public virtual void DisplayInfo()
    {
        Console.WriteLine($"Muoto: {Name}");
        Console.WriteLine($"Väri: {Color}");
        Console.WriteLine($"Pinta-ala: {CalculateArea():F2}");
    }
}

// Aliluokat ylikirjoittavat metodit
public class Circle : Shape
{
    public double Radius { get; set; }
    
    public override double CalculateArea()
    {
        return Math.PI * Radius * Radius;
    }
    
    public override void Draw()
    {
        Console.WriteLine($"Piirretään ympyrä, säde: {Radius}");
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
    
    public override void Draw()
    {
        Console.WriteLine($"Piirretään suorakulmio, {Width}x{Height}");
    }
}

public class Triangle : Shape
{
    public double Base { get; set; }
    public double Height { get; set; }
    
    public override double CalculateArea()
    {
        return 0.5 * Base * Height;
    }
    
    public override void Draw()
    {
        Console.WriteLine($"Piirretään kolmio, pohja: {Base}, korkeus: {Height}");
    }
}

// ✅ Polymorfismi toiminnassa
public class ShapeProcessor
{
    public void ProcessShapes(Shape[] shapes)
    {
        double totalArea = 0;
        
        foreach (Shape shape in shapes)
        {
            shape.Draw();              // Kutsuu oikeaa versiota
            double area = shape.CalculateArea(); // Kutsuu oikeaa versiota
            Console.WriteLine($"Pinta-ala: {area:F2}\n");
            totalArea += area;
        }
        
        Console.WriteLine($"Kokonaispinta-ala: {totalArea:F2}");
    }
}

// Käyttö:
Shape[] shapes = new Shape[]
{
    new Circle { Name = "Ympyrä", Color = "Punainen", Radius = 5 },
    new Rectangle { Name = "Suorakulmio", Color = "Sininen", Width = 4, Height = 6 },
    new Triangle { Name = "Kolmio", Color = "Vihreä", Base = 4, Height = 3 }
};

ShapeProcessor processor = new ShapeProcessor();
processor.ProcessShapes(shapes);
```

### Runtime Type Resolution

```csharp
// Tärkeä konsepti: Tyyppi ratkaistaan ajonaikana
Shape shape;

if (DateTime.Now.Hour < 12)
{
    shape = new Circle { Radius = 5 };
}
else
{
    shape = new Rectangle { Width = 4, Height = 6 };
}

// Kääntäjä ei tiedä mikä tyyppi, mutta polymorfismi toimii!
shape.CalculateArea(); // Kutsuu oikeaa metodia ajonaikana
```

---

## Abstract Classes ja Polymorfismi

Abstract-luokat pakottavat aliluokat toteuttamaan tiettyjä metodeja.

```csharp
// Abstract yläluokka
public abstract class Vehicle
{
    public string Brand { get; set; }
    public string Model { get; set; }
    public int Year { get; set; }
    
    // Abstract metodit - PAKKO toteuttaa
    public abstract void Start();
    public abstract void Stop();
    public abstract double CalculateFuelConsumption();
    
    // Virtual metodi - voi ylikirjoittaa (ei pakko)
    public virtual void Honk()
    {
        Console.WriteLine("Tööt!");
    }
    
    // Tavallinen metodi - ei voi ylikirjoittaa
    public void DisplayInfo()
    {
        Console.WriteLine($"{Brand} {Model} ({Year})");
        Console.WriteLine($"Kulutus: {CalculateFuelConsumption()} l/100km");
    }
}

public class Car : Vehicle
{
    public int NumberOfDoors { get; set; }
    
    public override void Start()
    {
        Console.WriteLine($"{Brand} {Model} käynnistyy");
    }
    
    public override void Stop()
    {
        Console.WriteLine($"{Brand} {Model} sammuu");
    }
    
    public override double CalculateFuelConsumption()
    {
        return 7.5; // Keskimäärin
    }
    
    public override void Honk()
    {
        Console.WriteLine("Beep beep!");
    }
}

public class Truck : Vehicle
{
    public double LoadCapacity { get; set; }
    
    public override void Start()
    {
        Console.WriteLine($"{Brand} kuorma-auto käynnistyy (raskas)");
    }
    
    public override void Stop()
    {
        Console.WriteLine($"{Brand} kuorma-auto pysähtyy (jarrutusmatka pitkä)");
    }
    
    public override double CalculateFuelConsumption()
    {
        return 25.0 + (LoadCapacity * 0.5); // Riippuu kuormasta
    }
    
    public override void Honk()
    {
        Console.WriteLine("TUUT TUUT! (kova ääni)");
    }
}

public class Motorcycle : Vehicle
{
    public bool HasSidecar { get; set; }
    
    public override void Start()
    {
        Console.WriteLine($"{Brand} moottoripyörä käynnistyy (vruum!)");
    }
    
    public override void Stop()
    {
        Console.WriteLine($"{Brand} moottoripyörä sammuu");
    }
    
    public override double CalculateFuelConsumption()
    {
        return HasSidecar ? 5.0 : 3.5;
    }
}

// Polymorfismi toiminnassa:
public class VehicleFleet
{
    private List<Vehicle> vehicles = new List<Vehicle>();
    
    public void AddVehicle(Vehicle vehicle)
    {
        vehicles.Add(vehicle);
    }
    
    public void StartAll()
    {
        Console.WriteLine("Käynnistetään kaikki ajoneuvot:\n");
        foreach (Vehicle vehicle in vehicles)
        {
            vehicle.Start(); // Polymorfismi!
        }
    }
    
    public void TestHorns()
    {
        Console.WriteLine("\nTorvet:\n");
        foreach (Vehicle vehicle in vehicles)
        {
            vehicle.Honk(); // Polymorfismi!
        }
    }
    
    public double CalculateTotalFuelConsumption()
    {
        double total = 0;
        foreach (Vehicle vehicle in vehicles)
        {
            total += vehicle.CalculateFuelConsumption(); // Polymorfismi!
        }
        return total;
    }
}

// Käyttö:
VehicleFleet fleet = new VehicleFleet();
fleet.AddVehicle(new Car { Brand = "Toyota", Model = "Corolla", Year = 2023, NumberOfDoors = 4 });
fleet.AddVehicle(new Truck { Brand = "Volvo", Model = "FH16", Year = 2022, LoadCapacity = 20 });
fleet.AddVehicle(new Motorcycle { Brand = "Harley", Model = "Davidson", Year = 2023, HasSidecar = false });

fleet.StartAll();
fleet.TestHorns();
Console.WriteLine($"\nKokonaiskulutus: {fleet.CalculateTotalFuelConsumption():F1} l/100km");
```

---

## Interface-pohjainen Polymorfismi

Rajapinnat tarjoavat puhtaan polymorfismin ilman perintähierarkiaa.

```csharp
// Rajapinnat
public interface IDrawable
{
    void Draw();
    void Erase();
}

public interface IResizable
{
    void Resize(double scale);
}

public interface IMovable
{
    void Move(int x, int y);
}

// Luokat voivat toteuttaa useita rajapintoja
public class Circle : IDrawable, IResizable, IMovable
{
    public double Radius { get; set; }
    public int X { get; set; }
    public int Y { get; set; }
    
    public void Draw()
    {
        Console.WriteLine($"Piirretään ympyrä kohtaan ({X}, {Y}), säde: {Radius}");
    }
    
    public void Erase()
    {
        Console.WriteLine("Poistetaan ympyrä");
    }
    
    public void Resize(double scale)
    {
        Radius *= scale;
        Console.WriteLine($"Ympyrän koko muutettu, uusi säde: {Radius}");
    }
    
    public void Move(int x, int y)
    {
        X = x;
        Y = y;
        Console.WriteLine($"Ympyrä siirretty kohtaan ({X}, {Y})");
    }
}

public class TextBox : IDrawable, IMovable
{
    public string Text { get; set; }
    public int X { get; set; }
    public int Y { get; set; }
    
    public void Draw()
    {
        Console.WriteLine($"Piirretään teksti '{Text}' kohtaan ({X}, {Y})");
    }
    
    public void Erase()
    {
        Console.WriteLine("Poistetaan teksti");
    }
    
    public void Move(int x, int y)
    {
        X = x;
        Y = y;
        Console.WriteLine($"Teksti siirretty kohtaan ({X}, {Y})");
    }
}

// Polymorfismi rajapintojen avulla
public class DrawingCanvas
{
    private List<IDrawable> drawables = new List<IDrawable>();
    
    public void Add(IDrawable drawable)
    {
        drawables.Add(drawable);
    }
    
    public void DrawAll()
    {
        foreach (IDrawable drawable in drawables)
        {
            drawable.Draw(); // Polymorfismi!
        }
    }
    
    public void MoveAllDrawables(int deltaX, int deltaY)
    {
        foreach (IDrawable drawable in drawables)
        {
            // Tarkistetaan tukeeko liikkumista
            if (drawable is IMovable movable)
            {
                movable.Move(deltaX, deltaY);
            }
        }
    }
    
    public void ResizeAllResizables(double scale)
    {
        foreach (IDrawable drawable in drawables)
        {
            if (drawable is IResizable resizable)
            {
                resizable.Resize(scale);
            }
        }
    }
}
```

---

## Käytännön esimerkit

### Esimerkki 1: Maksujen käsittely

```csharp
// Abstract base class
public abstract class PaymentMethod
{
    public string AccountHolder { get; set; }
    
    public abstract bool ProcessPayment(decimal amount);
    public abstract string GetPaymentDetails();
    
    public virtual void LogTransaction(decimal amount)
    {
        Console.WriteLine($"[{DateTime.Now}] Maksu käsitelty: {amount:C}");
    }
}

public class CreditCard : PaymentMethod
{
    public string CardNumber { get; set; }
    public DateTime ExpiryDate { get; set; }
    
    public override bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Maksetaan luottokortilla: {amount:C}");
        // Todellinen logiikka tässä...
        LogTransaction(amount);
        return true;
    }
    
    public override string GetPaymentDetails()
    {
        return $"Luottokortti: ****{CardNumber.Substring(CardNumber.Length - 4)}";
    }
}

public class PayPal : PaymentMethod
{
    public string Email { get; set; }
    
    public override bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Maksetaan PayPal:lla ({Email}): {amount:C}");
        LogTransaction(amount);
        return true;
    }
    
    public override string GetPaymentDetails()
    {
        return $"PayPal: {Email}";
    }
}

public class BankTransfer : PaymentMethod
{
    public string BankAccount { get; set; }
    public string BankName { get; set; }
    
    public override bool ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Tilisiirto ({BankName}): {amount:C}");
        LogTransaction(amount);
        return true;
    }
    
    public override string GetPaymentDetails()
    {
        return $"Tilisiirto: {BankName} - {BankAccount}";
    }
}

// Payment Processor - polymorfismi!
public class PaymentProcessor
{
    public void ProcessPayments(List<PaymentMethod> payments, decimal amount)
    {
        foreach (PaymentMethod payment in payments)
        {
            Console.WriteLine($"Maksutapa: {payment.GetPaymentDetails()}");
            payment.ProcessPayment(amount);
            Console.WriteLine();
        }
    }
}

// Käyttö:
List<PaymentMethod> paymentMethods = new List<PaymentMethod>
{
    new CreditCard { AccountHolder = "Matti", CardNumber = "1234567890123456", ExpiryDate = DateTime.Now.AddYears(2) },
    new PayPal { AccountHolder = "Liisa", Email = "liisa@example.com" },
    new BankTransfer { AccountHolder = "Pekka", BankAccount = "FI1234567890", BankName = "Nordea" }
};

PaymentProcessor processor = new PaymentProcessor();
processor.ProcessPayments(paymentMethods, 99.99m);
```

### Esimerkki 2: Dokumenttien käsittely

```csharp
public interface IDocument
{
    string Title { get; set; }
    void Open();
    void Save();
    void Print();
}

public class WordDocument : IDocument
{
    public string Title { get; set; }
    public string Content { get; set; }
    
    public void Open()
    {
        Console.WriteLine($"Avataan Word-dokumentti: {Title}");
    }
    
    public void Save()
    {
        Console.WriteLine($"Tallennetaan Word-dokumentti: {Title}");
    }
    
    public void Print()
    {
        Console.WriteLine($"Tulostetaan Word-dokumentti: {Title}");
        Console.WriteLine($"Sisältö: {Content}");
    }
}

public class ExcelSpreadsheet : IDocument
{
    public string Title { get; set; }
    public int Rows { get; set; }
    public int Columns { get; set; }
    
    public void Open()
    {
        Console.WriteLine($"Avataan Excel-taulukko: {Title}");
    }
    
    public void Save()
    {
        Console.WriteLine($"Tallennetaan Excel-taulukko: {Title}");
    }
    
    public void Print()
    {
        Console.WriteLine($"Tulostetaan Excel-taulukko: {Title}");
        Console.WriteLine($"Koko: {Rows} riviä x {Columns} saraketta");
    }
}

public class PdfDocument : IDocument
{
    public string Title { get; set; }
    public int PageCount { get; set; }
    
    public void Open()
    {
        Console.WriteLine($"Avataan PDF-dokumentti: {Title}");
    }
    
    public void Save()
    {
        Console.WriteLine("PDF on read-only, ei voi tallentaa");
    }
    
    public void Print()
    {
        Console.WriteLine($"Tulostetaan PDF: {Title} ({PageCount} sivua)");
    }
}

// Document Manager
public class DocumentManager
{
    public void ProcessDocuments(IDocument[] documents)
    {
        foreach (IDocument doc in documents)
        {
            doc.Open();
            doc.Print();
            doc.Save();
            Console.WriteLine();
        }
    }
}
```

---

## Polymorfismin hyödyt

### 1. Joustavuus
```csharp
// Voit lisätä uusia tyyppejä ilman että olemassa oleva koodi hajoaa
public class NewAnimal : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Uusi ääni!");
    }
}
// Kaikki olemassa oleva koodi toimii heti!
```

### 2. Laajennettavuus (Open/Closed Principle)
```csharp
// Luokat ovat avoimia laajennuksille, mutta suljettuja muutoksille
// Ei tarvitse muuttaa AnimalHandler-luokkaa kun lisäät uuden eläimen
```

### 3. Vähemmän koodia
```csharp
// Ilman polymorfismia: 50 riviä if-else lauseita
// Polymorfismilla: 5 riviä selkeää koodia
```

### 4. Helppo testata
```csharp
// Voit luoda mock-objekteja rajapinnoista
public class MockAnimal : Animal
{
    public override void MakeSound()
    {
        Console.WriteLine("Test sound");
    }
}
```

---

## Best Practices

### ✅ DO (Tee näin):

1. **Käytä polymorfismia välttääksesi tyyppitarkistuksia**
```csharp
// ✅ HYVÄ
animal.MakeSound();

// ❌ HUONO
if (animal is Dog) { ... }
```

2. **Käytä rajapintoja joustavuuteen**
```csharp
// ✅ HYVÄ
public void ProcessPayment(IPaymentMethod payment) { }

// ❌ HUONO
public void ProcessPayment(CreditCard card) { } // Rajoittunut
```

3. **Suunnittele rajapinnat huolella**
```csharp
// ✅ HYVÄ - Pieni, keskittynyt rajapinta
public interface IDrawable
{
    void Draw();
}

// ❌ HUONO - Liian iso rajapinta
public interface IEverything
{
    void Draw();
    void Save();
    void Load();
    void Print();
    void Email();
    void Export();
    // ... 20 metodia ...
}
```

4. **Dokumentoi virtual-metodit**
```csharp
/// <summary>
/// Laskee eläimen päivittäisen ruoan tarpeen kilogrammoina.
/// Aliluokkien tulisi ylikirjoittaa tämä metodi eläimen koon mukaan.
/// </summary>
public virtual double CalculateDailyFood() { return 1.0; }
```

### ❌ DON'T (Älä tee näin):

1. **Älä tarkista tyyppiä polymorfismin sijaan**
```csharp
// ❌ HUONO
if (shape is Circle)
{
    ((Circle)shape).DrawCircle();
}

// ✅ HYVÄ
shape.Draw();
```

2. **Älä riko Liskov Substitution Principle**
```csharp
// ❌ HUONO - Square ei käyttäydy oikein Rectangle:nä
public class Square : Rectangle
{
    public override void SetWidth(int width)
    {
        base.SetWidth(width);
        base.SetHeight(width); // Muuttaa myös korkeuden!
    }
}
```

3. **Älä ylikuormita väärin**
```csharp
// ❌ Hämmentävää - eri toiminnallisuus samalla nimellä
public int Calculate(int a, int b)
{
    return a + b; // Yhteenlasku
}

public int Calculate(int a, int b, int c)
{
    return a * b * c; // Kertolasku? Miksi?
}
```

---

## Yleiset virheet

### Virhe 1: Väärä casting

```csharp
// ❌ HUONO
Animal animal = new Dog();
Cat cat = (Cat)animal; // ❌ Runtime error!

// ✅ HYVÄ - tarkista ensin
if (animal is Cat cat)
{
    cat.Meow();
}

// TAI
Cat cat = animal as Cat;
if (cat != null)
{
    cat.Meow();
}
```

### Virhe 2: Unohtaa override

```csharp
// ❌ HUONO - ei override
public class Dog : Animal
{
    public void MakeSound() // Ei ylikirjoita!
    {
        Console.WriteLine("Hau!");
    }
}

// ✅ HYVÄ
public class Dog : Animal
{
    public override void MakeSound() // Ylikirjoittaa!
    {
        Console.WriteLine("Hau!");
    }
}
```

### Virhe 3: Ylitörmäävät parametrit

```csharp
// ❌ Hämmentävää
public void Process(int value) { }
public void Process(long value) { }

Process(10); // Kumpi kutsutaan? int (mutta ei selvää)
```

---

## Yhteenveto

Polymorfismi on tehokas työkalu, joka tekee koodista joustavaa ja ylläpidettävää.

### Muista:
- ✅ **Compile-time**: Method overloading, operator overloading
- ✅ **Runtime**: Method overriding, virtual/abstract/interface
- ✅ Välty tyyppitarkistuksilta (is, as)
- ✅ Käytä rajapintoja joustavuuteen
- ✅ Noudata Liskov Substitution Principle
- ✅ Pidä rajapinnat pieninä ja keskittyneinä

### Polymorfismi mahdollistaa:
- 🎯 Yhtenäisen käsittelyn eri objekteille
- 🔧 Helpon laajennettavuuden
- 📦 Puhtaan koodin ilman if-else lauseita
- ✨ Open/Closed Principle noudattamisen

**Seuraava askel:** Kun hallitset polymorfismin, jatka [Rajapinnat (Interfaces)](Interfaces.md) ja [Yhdistäminen (Composition)](Composition.md) materiaaleihin.

---

