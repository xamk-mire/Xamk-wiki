# Yhdistäminen (Composition)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mitä yhdistäminen on?](#mitä-yhdistäminen-on)
3. [Ongelma joka ratkaistaan](#ongelma-joka-ratkaistaan)
4. [Composition vs Inheritance](#composition-vs-inheritance)
5. [Composition vs Aggregation](#composition-vs-aggregation)
6. ["Composition over Inheritance"](#composition-over-inheritance)
7. [Käytännön esimerkit](#käytännön-esimerkit)
8. [Design Patterns compositiolla](#design-patterns-compositiolla)
9. [Best Practices](#best-practices)
10. [Yleiset virheet](#yleiset-virheet)
11. [Yhteenveto](#yhteenveto)

---

## Johdanto

Yhdistäminen (Composition) on tekniikka, jossa **monimutkainen olio rakennetaan yksinkertaisemmista osista**. Se on yksi tärkeimmistä ohjelmistokehityksen periaatteista.

**Lyhyesti:** Composition kuvaa **"has-a"** (omistaa) -suhdetta: "Autolla ON moottori", "Tietokoneella ON CPU".

**Analogia:** Auto ei OLE moottori, vaan autossa ON moottori. Auto koostuu osista: moottori, renkaat, ohjaus, jne.

---

## Mitä yhdistäminen on?

Yhdistäminen tarkoittaa että luokka **sisältää** toisia luokkia jäsenmuuttujina.

```csharp
// Yksinkertainen esimerkki:
public class Engine
{
    public void Start()
    {
        Console.WriteLine("Moottori käynnistyy");
    }
}

public class Car
{
    private Engine engine; // Car "has-a" Engine (composition)
    
    public Car()
    {
        engine = new Engine(); // Auto luo moottorin
    }
    
    public void Start()
    {
        engine.Start(); // Auto käyttää moottoria
    }
}
```

**Keskeistä:**
- Car **omistaa** Engine:n
- Car **luo** Engine:n
- Kun Car tuhoutuu, myös Engine tuhoutuu
- Car **delegoi** työtä Engine:lle

---

## Ongelma joka ratkaistaan

### Ilman yhdistämistä (ongelma)

```csharp
// ❌ HUONO: Kaikki yhdessä luokassa - "God Object"
public class Car
{
    // Moottorin logiikka
    private bool engineRunning;
    private int enginePower;
    private string engineType;
    
    public void StartEngine()
    {
        engineRunning = true;
        Console.WriteLine($"Käynnistetään {engineType} moottori, {enginePower} HP");
    }
    
    public void StopEngine()
    {
        engineRunning = false;
        Console.WriteLine("Moottori sammuu");
    }
    
    // Renkaiden logiikka
    private int tirePressure;
    private string tireBrand;
    private int numberOfTires;
    
    public void CheckTirePressure()
    {
        Console.WriteLine($"Renkaiden paine: {tirePressure} PSI");
    }
    
    public void InflateTires(int pressure)
    {
        tirePressure = pressure;
    }
    
    // Istuinten logiikka
    private int numberOfSeats;
    private bool hasLeatherSeats;
    private bool seatsHeated;
    
    public void AdjustSeats()
    {
        Console.WriteLine("Säädetään istuimia");
    }
    
    // GPS-logiikka
    private double latitude;
    private double longitude;
    private string destination;
    
    public void Navigate(string dest)
    {
        destination = dest;
        Console.WriteLine($"Navigoidaan: {destination}");
    }
    
    // ... ja niin edelleen - luokka kasvaa valtavaksi!
}
```

**Ongelmat:**
- ❌ Liian suuri luokka (100+ riviä → 1000+ riviä)
- ❌ Vaikea ylläpitää
- ❌ Vaikea testata
- ❌ Vaikea uudelleenkäyttää
- ❌ Rikkoo Single Responsibility Principle
- ❌ Tight coupling - kaikki riippuu kaikesta

### Yhdistämisen avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Pienet, keskitetyt luokat
public class Engine
{
    public string Type { get; set; }
    public int Power { get; set; }
    private bool isRunning;
    
    public void Start()
    {
        isRunning = true;
        Console.WriteLine($"Käynnistetään {Type} moottori, {Power} HP");
    }
    
    public void Stop()
    {
        isRunning = false;
        Console.WriteLine("Moottori sammuu");
    }
    
    public bool IsRunning => isRunning;
}

public class Tire
{
    public string Brand { get; set; }
    public int Pressure { get; private set; }
    
    public void CheckPressure()
    {
        Console.WriteLine($"Renkaan paine: {Pressure} PSI, Merkki: {Brand}");
    }
    
    public void Inflate(int pressure)
    {
        Pressure = pressure;
        Console.WriteLine($"Rengas täytetty: {Pressure} PSI");
    }
}

public class Seat
{
    public bool IsLeather { get; set; }
    public bool IsHeated { get; set; }
    private int position;
    
    public void Adjust(int newPosition)
    {
        position = newPosition;
        Console.WriteLine($"Istuin säädetty asentoon: {position}");
    }
}

public class GPS
{
    private double latitude;
    private double longitude;
    private string currentDestination;
    
    public void Navigate(string destination)
    {
        currentDestination = destination;
        Console.WriteLine($"Navigoidaan: {destination}");
        Console.WriteLine($"Nykyinen sijainti: {latitude}, {longitude}");
    }
    
    public void UpdateLocation(double lat, double lon)
    {
        latitude = lat;
        longitude = lon;
    }
}

// ✅ Auto koostuu osista (Composition)
public class Car
{
    // Composition - auto OMISTAA nämä osat
    private readonly Engine engine;
    private readonly Tire[] tires;
    private readonly Seat[] seats;
    private readonly GPS gps;
    
    public string Brand { get; set; }
    public string Model { get; set; }
    
    public Car(string brand, string model)
    {
        Brand = brand;
        Model = model;
        
        // Auto luo ja omistaa osat
        engine = new Engine { Type = "V6", Power = 250 };
        tires = new Tire[4]
        {
            new Tire { Brand = "Michelin", Pressure = 32 },
            new Tire { Brand = "Michelin", Pressure = 32 },
            new Tire { Brand = "Michelin", Pressure = 32 },
            new Tire { Brand = "Michelin", Pressure = 32 }
        };
        seats = new Seat[5]
        {
            new Seat { IsLeather = true, IsHeated = true },
            new Seat { IsLeather = true, IsHeated = true },
            new Seat { IsLeather = true, IsHeated = false },
            new Seat { IsLeather = true, IsHeated = false },
            new Seat { IsLeather = true, IsHeated = false }
        };
        gps = new GPS();
    }
    
    // Auto delegoi työt osille
    public void Start()
    {
        Console.WriteLine($"Käynnistetään {Brand} {Model}");
        engine.Start();
    }
    
    public void Stop()
    {
        Console.WriteLine($"Sammutetaan {Brand} {Model}");
        engine.Stop();
    }
    
    public void CheckAllTires()
    {
        Console.WriteLine("Tarkistetaan kaikki renkaat:");
        foreach (Tire tire in tires)
        {
            tire.CheckPressure();
        }
    }
    
    public void AdjustDriverSeat(int position)
    {
        seats[0].Adjust(position); // Kuljettajan istuin
    }
    
    public void NavigateTo(string destination)
    {
        gps.Navigate(destination);
    }
}

// Käyttö:
Car car = new Car("Toyota", "Corolla");
car.Start();
car.CheckAllTires();
car.NavigateTo("Helsinki");
car.Stop();
```

**Hyödyt:**
- ✅ Pienet, hallittavat luokat
- ✅ Helppo ylläpitää
- ✅ Helppo testata (testaa Engine erikseen)
- ✅ Uudelleenkäytettävä (Engine voidaan käyttää muuallakin)
- ✅ Noudattaa Single Responsibility
- ✅ Loose coupling

---

## Composition vs Inheritance

### Perinnän ongelma

```csharp
// ❌ Perinnän väärinkäyttö
public class Engine
{
    public void Start() { }
    public void Stop() { }
}

// ❌ VÄÄRIN: Auto ei OLE moottori!
public class Car : Engine
{
    // Nyt Car:lla on Start() ja Stop() mutta...
    // Tämä on semanttisesti väärin!
}
```

### Composition vs Inheritance vertailu

| Ominaisuus | Composition | Inheritance |
|------------|-------------|-------------|
| **Suhde** | "Has-a" (omistaa) | "Is-a" (on) |
| **Joustavuus** | ✅ Erittäin joustava | ⚠️ Jäykkä |
| **Ajonaikainen muutos** | ✅ Voi vaihtaa osia | ❌ Ei voi vaihtaa yläluokkaa |
| **Moniperintä** | ✅ Rajaton määrä osia | ❌ Yksi yläluokka |
| **Kytkentä** | ✅ Löyhä (loose) | ⚠️ Tiukka (tight) |
| **Testattavuus** | ✅ Helppo testata osia | ⚠️ Vaikeampi testata |
| **Esimerkki** | Car has Engine | Dog is Animal |

### Milloin käyttää mitäkin?

```csharp
// ✅ Käytä COMPOSITION kun:
// - "Has-a" suhde
// - Haluat joustavuutta
// - Haluat vaihtaa osia ajonaikana

public class Car
{
    private IEngine engine; // Voidaan vaihtaa!
    
    public void SetEngine(IEngine newEngine)
    {
        engine = newEngine; // Vaihdetaan moottoria
    }
}

// ✅ Käytä INHERITANCE kun:
// - "Is-a" suhde on todella selvä
// - Haluat jakaa yhteistä toiminnallisuutta
// - Polymorfismi on tärkeää

public abstract class Animal
{
    public abstract void MakeSound();
}

public class Dog : Animal // Dog IS AN Animal ✅
{
    public override void MakeSound()
    {
        Console.WriteLine("Hau!");
    }
}
```

### Esimerkki: "Composition over Inheritance"

```csharp
// ❌ HUONO: Perintähierarkia muuttuu monimutkaiseksi
public class Vehicle { }
public class LandVehicle : Vehicle { }
public class WaterVehicle : Vehicle { }
public class AirVehicle : Vehicle { }
public class AmphibiousVehicle : LandVehicle { } // Mutta se ui myös! Ongelma!

// ✅ HYVÄ: Composition
public interface IMovementMethod
{
    void Move();
}

public class WheelMovement : IMovementMethod
{
    public void Move() => Console.WriteLine("Liikkuu pyörillä");
}

public class PropellerMovement : IMovementMethod
{
    public void Move() => Console.WriteLine("Liikkuu potkurilla");
}

public class WingMovement : IMovementMethod
{
    public void Move() => Console.WriteLine("Liikkuu siivillä");
}

public class Vehicle
{
    private List<IMovementMethod> movementMethods = new List<IMovementMethod>();
    
    public void AddMovementMethod(IMovementMethod method)
    {
        movementMethods.Add(method);
    }
    
    public void Move()
    {
        foreach (var method in movementMethods)
        {
            method.Move();
        }
    }
}

// Käyttö:
Vehicle car = new Vehicle();
car.AddMovementMethod(new WheelMovement());

Vehicle boat = new Vehicle();
boat.AddMovementMethod(new PropellerMovement());

Vehicle amphibious = new Vehicle();
amphibious.AddMovementMethod(new WheelMovement());
amphibious.AddMovementMethod(new PropellerMovement());
// Nyt amfibio voi liikkua molemmilla tavoilla!
```

---

## Composition vs Aggregation

### Composition (vahva omistus)

- **Omistaja luo** komponentin
- **Komponentin elinaika** riippuu omistajasta
- Kun omistaja tuhoutuu, komponentti tuhoutuu

```csharp
// ✅ COMPOSITION: Auto omistaa ja luo moottorin
public class Car
{
    private Engine engine; // Car OMISTAA Engine:n
    
    public Car()
    {
        engine = new Engine(); // Car LÄHETTÄÄ Engine:n
    }
    // Kun Car tuhoutuu, myös Engine tuhoutuu
}
```

### Aggregation (heikko omistus)

- **Omistaja saa** komponentin ulkopuolelta
- **Komponentin elinaika** ei riipu omistajasta
- Kun omistaja tuhoutuu, komponentti voi elää

```csharp
// ✅ AGGREGATION: Auto käyttää kuljettajaa, mutta ei omista
public class Driver
{
    public string Name { get; set; }
}

public class Car
{
    private Driver driver; // Car KÄYTTÄÄ Driver:ia, mutta ei omista
    
    public void SetDriver(Driver d)
    {
        driver = d; // Driver tulee ulkopuolelta
    }
    // Kun Car tuhoutuu, Driver elää edelleen
}

// Käyttö:
Driver matti = new Driver { Name = "Matti" };
Car car1 = new Car();
car1.SetDriver(matti);

Car car2 = new Car();
car2.SetDriver(matti); // Sama kuljettaja, eri auto!
```

### Vertailu:

| Ominaisuus | Composition | Aggregation |
|------------|-------------|-------------|
| **Omistus** | Vahva | Heikko |
| **Luonti** | Omistaja luo | Tulee ulkopuolelta |
| **Elinaika** | Riippuvainen | Riippumaton |
| **Esimerkki** | Car-Engine | Car-Driver |
| **UML-merkintä** | Täytetty vinoneliö | Tyhjä vinoneliö |

---

## "Composition over Inheritance"

Yksi tärkeimmistä ohjelmistokehityksen periaatteista: **"Suosi yhdistämistä perinnän sijaan"**.

### Miksi?

1. **Joustavuus** - Voit vaihtaa osia ajonaikana
2. **Välttää hierarkia-ongelmia** - Ei syvä perinnän sykerö
3. **Parempi uudelleenkäyttö** - Osat toimivat monessa kontekstissa
4. **Helpompi testata** - Testaa osat erikseen

### Esimerkki: Pelihahmo

```csharp
// ❌ HUONO: Perintähierarkia
public abstract class Character { }
public class Warrior : Character { }
public class Mage : Character { }
public class Archer : Character { }
public class WarriorMage : ??? { } // Ongelma! Ei voi periä molemmista!

// ✅ HYVÄ: Composition (Component Pattern)
public interface IAbility
{
    void Use();
    string Name { get; }
}

public class MeleeAttack : IAbility
{
    public string Name => "Lähitaistelu";
    public void Use() => Console.WriteLine("Iskee miekalla!");
}

public class MagicSpell : IAbility
{
    public string Name => "Taikaiskument";
    public void Use() => Console.WriteLine("Heittää tulipallo!");
}

public class RangedAttack : IAbility
{
    public string Name => "Kaukotaistelu";
    public void Use() => Console.WriteLine("Ampuu nuolen!");
}

public class Healing : IAbility
{
    public string Name => "Parantaminen";
    public void Use() => Console.WriteLine("Parantaa haavoja!");
}

// Character koostuu kyvyistä
public class Character
{
    public string Name { get; set; }
    private List<IAbility> abilities = new List<IAbility>();
    
    public void AddAbility(IAbility ability)
    {
        abilities.Add(ability);
        Console.WriteLine($"{Name} oppi kyvyn: {ability.Name}");
    }
    
    public void UseAllAbilities()
    {
        Console.WriteLine($"\n{Name} käyttää kaikki kyvyt:");
        foreach (var ability in abilities)
        {
            ability.Use();
        }
    }
}

// Käyttö - täysi joustavuus!
Character warrior = new Character { Name = "Soturi" };
warrior.AddAbility(new MeleeAttack());

Character mage = new Character { Name = "Velho" };
mage.AddAbility(new MagicSpell());
mage.AddAbility(new Healing());

Character battlemage = new Character { Name = "Taisteluvelho" };
battlemage.AddAbility(new MeleeAttack());
battlemage.AddAbility(new MagicSpell());
battlemage.AddAbility(new Healing());
// Voi yhdistää mitä tahansa kykyjä!

warrior.UseAllAbilities();
mage.UseAllAbilities();
battlemage.UseAllAbilities();
```

---

## Käytännön esimerkit

### Esimerkki 1: Tietokone

```csharp
public class CPU
{
    public string Model { get; set; }
    public double Speed { get; set; }
    public int Cores { get; set; }
    
    public void Process()
    {
        Console.WriteLine($"CPU: {Model} ({Cores} cores @ {Speed}GHz) prosessoi dataa");
    }
}

public class RAM
{
    public int Capacity { get; set; }
    public string Type { get; set; }
    
    public void LoadData()
    {
        Console.WriteLine($"RAM: Ladataan dataa {Capacity}GB {Type} muistiin");
    }
}

public class Storage
{
    public int Capacity { get; set; }
    public string Type { get; set; } // SSD, HDD
    
    public void Read()
    {
        Console.WriteLine($"Storage: Luetaan {Type}:ltä ({Capacity}GB)");
    }
    
    public void Write()
    {
        Console.WriteLine($"Storage: Kirjoitetaan {Type}:lle ({Capacity}GB)");
    }
}

public class GPU
{
    public string Model { get; set; }
    public int VRAM { get; set; }
    
    public void Render()
    {
        Console.WriteLine($"GPU: {Model} ({VRAM}GB) renderöi grafiikkaa");
    }
}

// Computer koostuu osista
public class Computer
{
    private readonly CPU cpu;
    private readonly RAM ram;
    private readonly Storage storage;
    private readonly GPU gpu; // Optional
    
    public string Brand { get; set; }
    public string Model { get; set; }
    
    // Composition - tietokone luo osat
    public Computer(string brand, string model, bool hasGPU = false)
    {
        Brand = brand;
        Model = model;
        
        cpu = new CPU { Model = "Intel i7-12700K", Speed = 3.6, Cores = 12 };
        ram = new RAM { Capacity = 32, Type = "DDR5" };
        storage = new Storage { Capacity = 1000, Type = "NVMe SSD" };
        
        if (hasGPU)
        {
            gpu = new GPU { Model = "RTX 4080", VRAM = 16 };
        }
    }
    
    public void Boot()
    {
        Console.WriteLine($"\n═══ Käynnistetään {Brand} {Model} ═══");
        storage.Read();
        ram.LoadData();
        cpu.Process();
        if (gpu != null)
        {
            gpu.Render();
        }
        Console.WriteLine("Tietokone käynnistetty!\n");
    }
    
    public void RunApplication(string appName)
    {
        Console.WriteLine($"\n═══ Käynnistetään sovellus: {appName} ═══");
        storage.Read();
        ram.LoadData();
        cpu.Process();
        if (gpu != null && appName.Contains("Game"))
        {
            gpu.Render();
        }
    }
}

// Käyttö:
Computer gamingPC = new Computer("Custom", "Gaming PC", hasGPU: true);
gamingPC.Boot();
gamingPC.RunApplication("Cyberpunk 2077 Game");

Computer officePC = new Computer("Dell", "OptiPlex", hasGPU: false);
officePC.Boot();
officePC.RunApplication("Microsoft Word");
```

### Esimerkki 2: Ravintola (Component Pattern)

```csharp
public class Kitchen
{
    public void PrepareFood(string dish)
    {
        Console.WriteLine($"Keittiö valmistaa: {dish}");
    }
}

public class WaitingStaff
{
    public void ServeFood(string dish, int tableNumber)
    {
        Console.WriteLine($"Tarjoilija tuo ruoan: {dish} pöytään {tableNumber}");
    }
    
    public void TakeOrder(string order)
    {
        Console.WriteLine($"Tarjoilija ottaa tilauksen: {order}");
    }
}

public class Bar
{
    public void PrepareDrink(string drink)
    {
        Console.WriteLine($"Baari valmistaa juoman: {drink}");
    }
}

public class CashRegister
{
    public void ProcessPayment(decimal amount)
    {
        Console.WriteLine($"Kassa käsittelee maksun: {amount:C}");
    }
}

// Restaurant koostuu osista
public class Restaurant
{
    private readonly Kitchen kitchen;
    private readonly WaitingStaff staff;
    private readonly Bar bar;
    private readonly CashRegister cashRegister;
    
    public string Name { get; set; }
    
    public Restaurant(string name)
    {
        Name = name;
        kitchen = new Kitchen();
        staff = new WaitingStaff();
        bar = new Bar();
        cashRegister = new CashRegister();
    }
    
    public void ServeCustomer(int tableNumber, string food, string drink, decimal price)
    {
        Console.WriteLine($"\n═══ {Name} - Pöytä {tableNumber} ═══");
        
        staff.TakeOrder($"{food} ja {drink}");
        kitchen.PrepareFood(food);
        bar.PrepareDrink(drink);
        staff.ServeFood(food, tableNumber);
        cashRegister.ProcessPayment(price);
        
        Console.WriteLine("Asiakas palveltu!\n");
    }
}

// Käyttö:
Restaurant restaurant = new Restaurant("Pikku Poro");
restaurant.ServeCustomer(5, "Poro pihvi", "Coca-Cola", 25.50m);
restaurant.ServeCustomer(12, "Lohi pasta", "Olut", 18.90m);
```

---

## Design Patterns compositiolla

### 1. Composite Pattern

```csharp
// Component
public interface IGraphic
{
    void Draw();
}

// Leaf
public class Circle : IGraphic
{
    public void Draw()
    {
        Console.WriteLine("Piirretään ympyrä");
    }
}

// Leaf
public class Rectangle : IGraphic
{
    public void Draw()
    {
        Console.WriteLine("Piirretään suorakulmio");
    }
}

// Composite
public class Group : IGraphic
{
    private List<IGraphic> children = new List<IGraphic>();
    
    public void Add(IGraphic graphic)
    {
        children.Add(graphic);
    }
    
    public void Draw()
    {
        Console.WriteLine("Piirretään ryhmä:");
        foreach (var child in children)
        {
            child.Draw();
        }
    }
}

// Käyttö:
Circle circle = new Circle();
Rectangle rect = new Rectangle();

Group group = new Group();
group.Add(circle);
group.Add(rect);
group.Add(new Circle());

group.Draw(); // Piirtää kaikki
```

### 2. Decorator Pattern

```csharp
public interface ICoffee
{
    string GetDescription();
    decimal GetCost();
}

// Base
public class SimpleCoffee : ICoffee
{
    public string GetDescription() => "Kahvi";
    public decimal GetCost() => 2.00m;
}

// Decorator Base
public abstract class CoffeeDecorator : ICoffee
{
    protected ICoffee coffee;
    
    public CoffeeDecorator(ICoffee coffee)
    {
        this.coffee = coffee;
    }
    
    public virtual string GetDescription() => coffee.GetDescription();
    public virtual decimal GetCost() => coffee.GetCost();
}

// Concrete Decorators
public class Milk : CoffeeDecorator
{
    public Milk(ICoffee coffee) : base(coffee) { }
    
    public override string GetDescription() => coffee.GetDescription() + ", Maito";
    public override decimal GetCost() => coffee.GetCost() + 0.50m;
}

public class Sugar : CoffeeDecorator
{
    public Sugar(ICoffee coffee) : base(coffee) { }
    
    public override string GetDescription() => coffee.GetDescription() + ", Sokeri";
    public override decimal GetCost() => coffee.GetCost() + 0.25m;
}

// Käyttö:
ICoffee coffee = new SimpleCoffee();
coffee = new Milk(coffee);
coffee = new Sugar(coffee);

Console.WriteLine($"{coffee.GetDescription()}: {coffee.GetCost():C}");
// Output: "Kahvi, Maito, Sokeri: 2.75€"
```

---

## Best Practices

### ✅ DO (Tee näin):

1. **Suosi composition over inheritance**
```csharp
// ✅ HYVÄ
public class Car
{
    private Engine engine; // Has-a
}
```

2. **Käytä rajapintoja joustavuuteen**
```csharp
// ✅ HYVÄ
public class Car
{
    private IEngine engine; // Voidaan vaihtaa!
}
```

3. **Dependency Injection**
```csharp
// ✅ HYVÄ - Injektoi riippuvuudet
public class Car
{
    private IEngine engine;
    
    public Car(IEngine engine)
    {
        this.engine = engine;
    }
}
```

4. **Pidä luokat pieniä**
```csharp
// ✅ HYVÄ - Yksi vastuualue per luokka
public class Engine { } // Vain moottori
public class Tire { }   // Vain rengas
```

### ❌ DON'T (Älä tee näin):

1. **Älä tee God Objects**
```csharp
// ❌ HUONO - Liian monimutkainen
public class Car
{
    // 500 riviä koodia kaikesta...
}
```

2. **Älä käytä perintää "has-a" suhteisiin**
```csharp
// ❌ HUONO - Car ei OLE Engine!
public class Car : Engine { }
```

3. **Älä paljasta sisäisiä osia**
```csharp
// ❌ HUONO
public class Car
{
    public Engine Engine { get; set; } // Paljastaa sisäisen osan!
}

// ✅ HYVÄ
public class Car
{
    private Engine engine; // Piilotettu
    
    public void Start()
    {
        engine.Start(); // Delegointi
    }
}
```

---

## Yleiset virheet

### Virhe 1: Väärä suhde

```csharp
// ❌ VÄÄRIN - Käyttää perintää väärään suhteeseen
public class Car : Engine { } // Car ei ole Engine!

// ✅ OIKEIN
public class Car
{
    private Engine engine; // Car has an Engine
}
```

### Virhe 2: Liian tiukka kytkentä

```csharp
// ❌ HUONO - Sidottu konkreettiseen luokkaan
public class Car
{
    private PetrolEngine engine; // Vain bensa-moottori!
}

// ✅ HYVÄ - Rajapinta
public class Car
{
    private IEngine engine; // Mikä tahansa moottori
}
```

### Virhe 3: Ei delegointia

```csharp
// ❌ HUONO - Car päästää Engine:n ulos
public class Car
{
    public Engine Engine { get; set; }
}

// Ulkopuolelta:
car.Engine.Start(); // Ei pitäisi näkyä!

// ✅ HYVÄ - Delegointi
public class Car
{
    private Engine engine;
    
    public void Start()
    {
        engine.Start(); // Car delegoi Engine:lle
    }
}

// Ulkopuolelta:
car.Start(); // Selkeä!
```

---

## Yhteenveto

Composition on yksi tärkeimmistä ohjelmistokehityksen periaatteista.

### Muista:
- ✅ **"Has-a"** suhde - omistaa osia
- ✅ **Composition over Inheritance** - suosi yhdistämistä
- ✅ **Joustavuus** - voit vaihtaa osia
- ✅ **Modulaarisuus** - pienet, itsenäiset osat
- ✅ **Testattavuus** - testaa osat erikseen
- ✅ **Uudelleenkäyttö** - osat toimivat monessa kontekstissa

### Composition vs:
- **Inheritance**: Has-a vs Is-a
- **Aggregation**: Vahva omistus vs Heikko omistus

### Composition mahdollistaa:
- 🧩 Modulaarisen rakenteen
- 🔄 Osien vaihtamisen ajonaikana
- 🧪 Helpon testattavuuden
- 📦 Paremman uudelleenkäytön
- 🎯 Single Responsibility -periaatteen

**Seuraava askel:** Olet nyt käynyt läpi kaikki OOP:n keskeiset konseptit! Jatka [Design Principles](../04-Advanced/Design-Principles.md) ja [Design Patterns](../04-Advanced/Design-Patterns.md) materiaaleihin.

---

