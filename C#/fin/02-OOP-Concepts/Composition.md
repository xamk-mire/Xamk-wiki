# Yhdistäminen (Composition)

## Yhdistämisen ongelma, joka ratkaistaan

Liian suuri "kaikki yhdessä" -luokka, joka sisältää liikaa vastuita ja tekee koodista vaikeasti ylläpidettävää.

## Ratkaisu

Yhdistäminen (Composition) tarkoittaa, että luokka koostuu muiden luokkien ilmentymistä. Tämä mahdollistaa loogisesti pienempien moduulien käytön, mikä parantaa selkeyttä ja ylläpidettävyyttä.

## Ilman yhdistämistä (ongelma)

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
    
    // Kaikki metodit yhdessä
    public void StartEngine()
    {
        EngineRunning = true;
        Console.WriteLine("Moottori käynnistyy");
    }
    
    public void CheckTirePressure()
    {
        Console.WriteLine($"Renkaiden paine: {TirePressure} PSI");
    }
    
    public void AdjustSeats()
    {
        Console.WriteLine($"Säädetään {NumberOfSeats} istuinta");
    }
    
    // ... ja paljon muuta
}
```

**Ongelmat:**
- Liian monimutkainen luokka
- Vaikea ylläpitää
- Vaikea testata
- Rikoo Single Responsibility Principle -periaatetta

## Yhdistämisen avulla (ratkaisu)

### Perusyhdistäminen

```csharp
// ✅ HYVÄ: Pienet, keskitetyt luokat
public class Engine
{
    public bool IsRunning { get; private set; }
    public int Power { get; set; }
    
    public void Start()
    {
        IsRunning = true;
        Console.WriteLine("Moottori käynnistyy");
    }
    
    public void Stop()
    {
        IsRunning = false;
        Console.WriteLine("Moottori sammuu");
    }
}

public class Tire
{
    public int Pressure { get; set; }
    public string Brand { get; set; }
    
    public void CheckPressure()
    {
        Console.WriteLine($"Renkaan paine: {Pressure} PSI, Merkki: {Brand}");
    }
    
    public void Inflate(int amount)
    {
        Pressure += amount;
        Console.WriteLine($"Renkaita täytetty. Uusi paine: {Pressure} PSI");
    }
}

public class Seat
{
    public bool IsLeather { get; set; }
    public bool IsHeated { get; set; }
    
    public void Adjust()
    {
        Console.WriteLine("Istuin säädetty");
    }
}

// ✅ Yhdistetty luokka
public class Car
{
    // Yhdistäminen: Car koostuu näistä osista
    private Engine engine;
    private Tire[] tires;
    private Seat[] seats;
    
    public Car(Engine engine, Tire[] tires, Seat[] seats)
    {
        this.engine = engine;
        this.tires = tires;
        this.seats = seats;
    }
    
    public void Start()
    {
        engine.Start();
    }
    
    public void CheckAllTires()
    {
        foreach (var tire in tires)
        {
            tire.CheckPressure();
        }
    }
    
    public void AdjustAllSeats()
    {
        foreach (var seat in seats)
        {
            seat.Adjust();
        }
    }
}
```

### Käyttöesimerkki:

```csharp
// Luodaan osat
Engine engine = new Engine { Power = 150 };
Tire[] tires = new Tire[]
{
    new Tire { Pressure = 32, Brand = "Michelin" },
    new Tire { Pressure = 32, Brand = "Michelin" },
    new Tire { Pressure = 32, Brand = "Michelin" },
    new Tire { Pressure = 32, Brand = "Michelin" }
};
Seat[] seats = new Seat[]
{
    new Seat { IsLeather = true, IsHeated = true },
    new Seat { IsLeather = true, IsHeated = true },
    new Seat { IsLeather = true, IsHeated = false },
    new Seat { IsLeather = true, IsHeated = false }
};

// Luodaan auto osista
Car car = new Car(engine, tires, seats);
car.Start();
car.CheckAllTires();
car.AdjustAllSeats();
```

### Kompleksisempi esimerkki: Tietokone

```csharp
public class CPU
{
    public string Model { get; set; }
    public double Speed { get; set; }
    
    public void Process()
    {
        Console.WriteLine($"{Model} prosessoi dataa {Speed} GHz nopeudella");
    }
}

public class RAM
{
    public int Capacity { get; set; }
    
    public void LoadData()
    {
        Console.WriteLine($"Ladataan dataa {Capacity} GB muistiin");
    }
}

public class HardDrive
{
    public int Capacity { get; set; }
    public string Type { get; set; }
    
    public void Read()
    {
        Console.WriteLine($"Luetaan dataa {Type} -kiintolevyltä");
    }
    
    public void Write()
    {
        Console.WriteLine($"Kirjoitetaan dataa {Type} -kiintolevylle");
    }
}

public class Computer
{
    private CPU cpu;
    private RAM ram;
    private HardDrive hardDrive;
    
    public Computer(CPU cpu, RAM ram, HardDrive hardDrive)
    {
        this.cpu = cpu;
        this.ram = ram;
        this.hardDrive = hardDrive;
    }
    
    public void Boot()
    {
        Console.WriteLine("Käynnistetään tietokone...");
        hardDrive.Read();
        ram.LoadData();
        cpu.Process();
        Console.WriteLine("Tietokone käynnistetty!");
    }
    
    public void Shutdown()
    {
        Console.WriteLine("Sammutetaan tietokone...");
        hardDrive.Write();
        Console.WriteLine("Tietokone sammutettu.");
    }
}

// Käyttö
CPU cpu = new CPU { Model = "Intel i7", Speed = 3.5 };
RAM ram = new RAM { Capacity = 16 };
HardDrive hdd = new HardDrive { Capacity = 1000, Type = "SSD" };

Computer computer = new Computer(cpu, ram, hdd);
computer.Boot();
```

## Yhdistämisen hyödyt

1. **Modulaarisuus**: Jokainen osa on itsenäinen ja testattavissa
2. **Joustavuus**: Osia voidaan vaihtaa helposti
3. **Ylläpidettävyys**: Muutokset yhdessä osassa eivät vaikuta muihin
4. **Testattavuus**: Jokainen osa voidaan testata erikseen
5. **Single Responsibility**: Jokainen luokka vastaa yhdestä asiasta

## Yhdistäminen vs. Perintä

- **Perintä**: "on-a" suhde (esim. "Dog on Animal")
- **Yhdistäminen**: "has-a" suhde (esim. "Car has Engine")

Yhdistäminen on usein joustavampi vaihtoehto, koska se mahdollistaa osien vaihtamisen dynaamisesti.

## Yhteenveto

Yhdistäminen on tehokas tapa rakentaa monimutkaisia järjestelmiä yksinkertaisista osista. Se parantaa koodin modulaarisuutta, testattavuutta ja ylläpidettävyyttä.

