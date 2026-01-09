# C# Properties (Ominaisuudet)

## Mikä on Property?

C#:ssa property on luokan jäsen, joka tarjoaa joustavan mekanismin päästä käsiksi yksityisiin kenttiin (field). Property toimii ikään kuin yleisenä porttina luokan sisäisiin tietoihin, mahdollistaen arvojen asettamisen (setter) ja hakemisen (getter) määritellyllä tavalla. Propertyjen avulla voidaan suorittaa tietojen validointi, logiikan suorittaminen arvojen asettamisen tai hakemisen yhteydessä, ja ne auttavat varmistamaan, että luokan tila pysyy hallinnassa ja johdonmukaisena.

## Miksi Propertyjä käytetään?

### 1. Kapselointi

Suojataan luokan sisäinen tila ja varmistetaan, että vain sallitut toiminnot voivat muuttaa sitä.

### 2. Validointi

Kun asetat arvon propertyn kautta, voit varmistaa, että arvo täyttää tietyt ehdot ennen sen tallentamista.

### 3. Helppous ja luettavuus

Propertyjen avulla voit käsitellä luokan sisäisiä arvoja kuin julkisia kenttiä, mutta samalla hallita tarkasti, miten niitä käytetään.

## Koodiesimerkit

### Perusproperty

```csharp
public class Person
{
    private string name;

    // Property getterillä ja setterillä
    public string Name
    {
        get { return name; }
        set { name = value; }
    }
}

// Käyttö
Person person = new Person();
person.Name = "Matti";  // setter kutsutaan
string name = person.Name;  // getter kutsutaan
```

### Auto-implemented property

```csharp
public class Person
{
    // Auto-implemented property (C# luo automaattisesti taustakentän)
    public string Name { get; set; }
    public int Age { get; set; }
}

// Käyttö
Person person = new Person();
person.Name = "Matti";
person.Age = 25;
```

### Property validoinnilla

```csharp
public class Employee
{
    private int age;

    public int Age
    {
        get { return age; }
        set
        {
            if (value < 0)
            {
                throw new ArgumentException("Ikä ei voi olla negatiivinen");
            }
            age = value;
        }
    }
}

// Käyttö
Employee employee = new Employee();
employee.Age = 30;  // OK
// employee.Age = -5;  // Heittää poikkeuksen
```

### Read-only property

```csharp
public class Circle
{
    private double radius;

    public Circle(double radius)
    {
        this.radius = radius;
    }

    // Read-only property (vain getter)
    public double Area
    {
        get { return Math.PI * radius * radius; }
    }
}

// Käyttö
Circle circle = new Circle(5);
double area = circle.Area;  // Lasketaan automaattisesti
// circle.Area = 10;  // Virhe: ei setteriä
```

### Write-only property

```csharp
public class Logger
{
    private string logFile;

    // Write-only property (vain setter)
    public string LogFile
    {
        set { logFile = value; }
    }

    public void WriteLog(string message)
    {
        // Käyttää logFile-kenttää
    }
}
```

### Property ilman taustakenttää (laskettu arvo)

```csharp
public class Rectangle
{
    public double Width { get; set; }
    public double Height { get; set; }

    // Property, joka lasketaan muista propertyistä
    public double Area
    {
        get { return Width * Height; }
    }

    public double Perimeter
    {
        get { return 2 * (Width + Height); }
    }
}

// Käyttö
Rectangle rect = new Rectangle { Width = 5, Height = 3 };
Console.WriteLine($"Pinta-ala: {rect.Area}");        // 15
Console.WriteLine($"Piiri: {rect.Perimeter}");      // 16
```

### Property init-only (C# 9.0+)

```csharp
public class Person
{
    // Init-only property (voidaan asettaa vain objektin luonnin yhteydessä)
    public string Name { get; init; }
    public int Age { get; init; }
}

// Käyttö
Person person = new Person { Name = "Matti", Age = 25 };
// person.Name = "Liisa";  // Virhe: ei voi muuttaa init-only propertyä
```

### Property private setterillä

```csharp
public class BankAccount
{
    private decimal balance;

    public decimal Balance
    {
        get { return balance; }
        private set { balance = value; }  // Vain luokan sisällä muutettavissa
    }

    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            Balance += amount;  // OK: käytetään luokan sisällä
        }
    }

    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && Balance >= amount)
        {
            Balance -= amount;  // OK: käytetään luokan sisällä
            return true;
        }
        return false;
    }
}

// Käyttö
BankAccount account = new BankAccount();
account.Deposit(100);
Console.WriteLine($"Saldo: {account.Balance}");  // 100
// account.Balance = 200;  // Virhe: Balance on private set
```

### Property default-arvolla

```csharp
public class Settings
{
    // Property default-arvolla
    public string Theme { get; set; } = "Light";
    public int MaxItems { get; set; } = 10;
    public bool NotificationsEnabled { get; set; } = true;
}

// Käyttö
Settings settings = new Settings();
Console.WriteLine(settings.Theme);  // "Light" (oletusarvo)
```

## Reaalimaailman esimerkki

```csharp
public class Employee
{
    private int age;
    private string email;

    public string Name { get; set; }

    public int Age
    {
        get { return age; }
        set
        {
            if (value < 0)
            {
                throw new ArgumentException("Ikä ei voi olla negatiivinen");
            }
            if (value > 150)
            {
                throw new ArgumentException("Ikä ei voi olla yli 150");
            }
            age = value;
        }
    }

    public string Email
    {
        get { return email; }
        set
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                throw new ArgumentException("Sähköposti ei voi olla tyhjä");
            }
            if (!value.Contains("@"))
            {
                throw new ArgumentException("Sähköpostin täytyy sisältää @-merkki");
            }
            email = value;
        }
    }
}

// Käyttö
Employee employee = new Employee
{
    Name = "Matti Meikäläinen",
    Age = 30,
    Email = "matti@example.com"
};
```

## Yhteenveto

Propertyjen käyttö C#-ohjelmoinnissa on erittäin hyödyllistä, koska se lisää koodin turvallisuutta, luettavuutta ja ylläpidettävyyttä, samalla kun se tarjoaa kehittäjille mahdollisuuden hallita tarkasti, miten luokan tilaa muokataan ja käytetään. Propertyt mahdollistavat kapseloinnin, validoinnin ja joustavan datan käsittelyn ilman, että tarvitsee paljastaa luokan sisäisiä toteutusyksityiskohtia.

