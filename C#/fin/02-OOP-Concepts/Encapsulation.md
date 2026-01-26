# Kapselointi (Encapsulation)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mitä kapselointi on?](#mitä-kapselointi-on)
3. [Ongelma joka ratkaistaan](#ongelma-joka-ratkaistaan)
4. [Access Modifiers](#access-modifiers)
5. [Properties (Ominaisuudet)](#properties-ominaisuudet)
6. [Readonly ja Const](#readonly-ja-const)
7. [Käytännön esimerkit](#käytännön-esimerkit)
8. [Best Practices](#best-practices)
9. [Yleiset virheet](#yleiset-virheet)
10. [Yhteenveto](#yhteenveto)

---

## Johdanto

Kapselointi on **olio-ohjelmoinnin tärkein periaate**. Se on perusta kaikelle muulle - ilman kapselointia emme voisi rakentaa turvallisia ja ylläpidettäviä järjestelmiä.

**Lyhyesti:** Kapselointi tarkoittaa datan (fields) piilottamista ja kontrolloidun pääsyn tarjoamista julkisten metodien ja propertyjen kautta.

---

## Mitä kapselointi on?

Kapselointi koostuu kahdesta pääperiaatteesta:

### 1. Data Hiding (Tiedon piilottaminen)
Luokan sisäinen tila (data) piilotetaan ulkopuolelta käyttämällä `private` avainsanaa.

### 2. Information Hiding (Informaation piilottaminen)
Toteutuksen yksityiskohdat piilotetaan ja tarjotaan vain tarvittava julkinen rajapinta.

```csharp
// Yksinkertainen vertailu:

// ❌ Ilman kapselointia - kaikki näkyvissä
public class BadPerson
{
    public string name;
    public int age;
}

// ✅ Kapselointi - kontrolloitu pääsy
public class GoodPerson
{
    private string name;
    private int age;
    
    public string Name 
    { 
        get { return name; } 
        set 
        { 
            if (!string.IsNullOrWhiteSpace(value))
                name = value;
            else
                throw new ArgumentException("Nimi ei voi olla tyhjä");
        }
    }
    
    public int Age 
    { 
        get { return age; } 
        set 
        { 
            if (value >= 0 && value <= 150)
                age = value;
            else
                throw new ArgumentException("Ikä on virheellinen");
        }
    }
}
```

---

## Ongelma joka ratkaistaan

### Ilman kapselointia (ongelma)

```csharp
// ❌ HUONO: Julkiset kentät
public class BankAccount
{
    public decimal balance; // Kuka tahansa voi muuttaa!
    public string accountNumber;
    public string ownerName;
}

// Käyttö - VAARALLISTA!
BankAccount account = new BankAccount();
account.balance = -1000;     // ❌ Negatiivinen saldo
account.balance = 999999999; // ❌ Realistoimaton summa
account.accountNumber = "";  // ❌ Tyhjä tilinumero
```

**Ongelmat:**
- ❌ Ei validointia
- ❌ Ei kontrollia datan eheydestä
- ❌ Helppo tehdä virheitä
- ❌ Vaikea ylläpitää
- ❌ Ei voi lisätä logiikkaa myöhemmin
- ❌ Rikkoo Single Responsibility Principle

### Kapseloinnin avulla (ratkaisu)

```csharp
// ✅ HYVÄ: Kapseloitu toteutus
public class BankAccount
{
    // Private kentät - piilotettu ulkopuolelta
    private decimal balance;
    private readonly string accountNumber;
    private string ownerName;
    private readonly DateTime createdAt;
    private readonly List<Transaction> transactions;
    
    // Julkinen, read-only property
    public string AccountNumber => accountNumber;
    
    // Julkinen property validoinnilla
    public string OwnerName
    {
        get => ownerName;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Omistajan nimi on pakollinen");
            if (value.Length < 2)
                throw new ArgumentException("Nimen täytyy olla vähintään 2 merkkiä");
            ownerName = value;
        }
    }
    
    // Read-only property - ei voi muuttaa ulkopuolelta
    public decimal Balance => balance;
    
    // Read-only property
    public DateTime CreatedAt => createdAt;
    
    // Read-only kokoelma
    public IReadOnlyList<Transaction> Transactions => transactions.AsReadOnly();
    
    // Konstruktori
    public BankAccount(string accountNumber, string ownerName, decimal initialBalance)
    {
        if (string.IsNullOrWhiteSpace(accountNumber))
            throw new ArgumentException("Tilinumero on pakollinen");
        if (initialBalance < 0)
            throw new ArgumentException("Alkusaldo ei voi olla negatiivinen");
            
        this.accountNumber = accountNumber;
        this.OwnerName = ownerName; // Käyttää property validointia!
        this.balance = initialBalance;
        this.createdAt = DateTime.UtcNow;
        this.transactions = new List<Transaction>();
        
        if (initialBalance > 0)
        {
            transactions.Add(new Transaction(initialBalance, "Initial deposit"));
        }
    }
    
    // Julkinen metodi validoinnilla
    public void Deposit(decimal amount)
    {
        if (amount <= 0)
            throw new ArgumentException("Talletussumman täytyy olla positiivinen");
        if (amount > 1000000)
            throw new ArgumentException("Liian suuri talletussumma kerralla");
            
        balance += amount;
        transactions.Add(new Transaction(amount, "Deposit"));
        Console.WriteLine($"Talletettu {amount:C}. Uusi saldo: {balance:C}");
    }
    
    // Julkinen metodi validoinnilla
    public bool Withdraw(decimal amount)
    {
        if (amount <= 0)
        {
            Console.WriteLine("Nostosumman täytyy olla positiivinen");
            return false;
        }
        
        if (amount > balance)
        {
            Console.WriteLine("Riittämätön saldo");
            return false;
        }
        
        if (amount > 5000)
        {
            Console.WriteLine("Nostoraja ylitetty (max 5000€ kerralla)");
            return false;
        }
        
        balance -= amount;
        transactions.Add(new Transaction(-amount, "Withdrawal"));
        Console.WriteLine($"Nostettu {amount:C}. Uusi saldo: {balance:C}");
        return true;
    }
    
    // Julkinen metodi
    public void Transfer(BankAccount target, decimal amount)
    {
        if (target == null)
            throw new ArgumentNullException(nameof(target));
        if (target == this)
            throw new InvalidOperationException("Ei voi siirtää itselleen");
            
        if (Withdraw(amount))
        {
            target.Deposit(amount);
            Console.WriteLine($"Siirretty {amount:C} tilille {target.AccountNumber}");
        }
    }
    
    // Private helper metodi - ei näy ulospäin
    private void LogTransaction(string description)
    {
        Console.WriteLine($"[{DateTime.Now}] {description}");
    }
}

// Transaction-luokka
public class Transaction
{
    public decimal Amount { get; }
    public string Description { get; }
    public DateTime Timestamp { get; }
    
    public Transaction(decimal amount, string description)
    {
        Amount = amount;
        Description = description;
        Timestamp = DateTime.UtcNow;
    }
}
```

**Hyödyt:**
- ✅ Validointi automaattisesti
- ✅ Datan eheys varmistettu
- ✅ Ei mahdollista tehdä virheellisiä operaatioita
- ✅ Helppo muuttaa toteutusta myöhemmin
- ✅ Selkeä rajapinta ulkopuolelle

---

## Access Modifiers

C# tarjoaa useita access modifierejä kontrolloimaan näkyvyyttä:

### Taulukko: Access Modifiers

| Modifier | Näkyvyys | Käyttötarkoitus |
|----------|----------|-----------------|
| `public` | Kaikkialla | Julkinen rajapinta |
| `private` | Vain luokassa | Sisäinen toteutus (oletus) |
| `protected` | Luokka + aliluokat | Perinnässä jaettu |
| `internal` | Sama assembly | Saman projektin sisällä |
| `protected internal` | Sama assembly TAI aliluokat | Harvoin käytetty |
| `private protected` | Sama assembly JA aliluokat | Hyvin rajoitettu |

### Esimerkit:

```csharp
public class AccessModifiersDemo
{
    // PUBLIC - Näkyy kaikkialle
    public string PublicField = "Näkyy kaikkialle";
    
    // PRIVATE - Näkyy vain tässä luokassa (oletus)
    private string privateField = "Vain tässä luokassa";
    
    // PROTECTED - Näkyy tässä luokassa ja aliluokissa
    protected string protectedField = "Tässä ja aliluokissa";
    
    // INTERNAL - Näkyy samassa assemblyssa (projektissa)
    internal string internalField = "Samassa projektissa";
    
    // PRIVATE metodi - vain sisäinen käyttö
    private void PrivateMethod()
    {
        Console.WriteLine("Sisäinen metodi");
    }
    
    // PUBLIC metodi - julkinen rajapinta
    public void PublicMethod()
    {
        PrivateMethod(); // ✅ Voi kutsua private-metodia
        Console.WriteLine(privateField); // ✅ Voi käyttää private-kenttää
    }
}

public class DerivedClass : AccessModifiersDemo
{
    public void TestAccess()
    {
        Console.WriteLine(PublicField);      // ✅ OK
        Console.WriteLine(protectedField);   // ✅ OK - peri juttua
        Console.WriteLine(internalField);    // ✅ OK - sama assembly
        // Console.WriteLine(privateField);  // ❌ EI OLE - private!
        
        PublicMethod();  // ✅ OK
        // PrivateMethod(); // ❌ EI TOIMI - private!
    }
}
```

### Suositukset:

```csharp
public class BestPracticeExample
{
    // ✅ HYVÄ: Private field, public property
    private string name;
    public string Name
    {
        get => name;
        set => name = value;
    }
    
    // ✅ HYVÄ: Auto-property (suositeltu yksinkertaisille)
    public int Age { get; set; }
    
    // ✅ HYVÄ: Read-only property
    public DateTime CreatedAt { get; }
    
    // ✅ HYVÄ: Private setter
    public decimal Balance { get; private set; }
    
    // ❌ HUONO: Public field
    public string BadField; // Älä koskaan!
}
```

---

## Properties (Ominaisuudet)

Properties ovat C#:n keskeinen ominaisuus kapseloinnissa.

### Auto-Properties (Suositeltu)

```csharp
public class Person
{
    // ✅ Auto-property - yksinkertaisin tapa
    public string Name { get; set; }
    
    // ✅ Read-only auto-property
    public DateTime BirthDate { get; }
    
    // ✅ Private setter
    public int Age { get; private set; }
    
    // ✅ Init-only (C# 9+) - vain konstruktorissa tai object initializerissa
    public string Id { get; init; }
    
    public Person(DateTime birthDate)
    {
        BirthDate = birthDate;
        Age = CalculateAge();
    }
    
    private int CalculateAge()
    {
        return DateTime.Now.Year - BirthDate.Year;
    }
}

// Käyttö:
Person person = new Person(new DateTime(1990, 5, 15))
{
    Name = "Matti",
    Id = "12345" // ✅ Voi asettaa init-only propertyssa
};
// person.Id = "67890"; // ❌ Ei voi muuttaa enää!
```

### Properties validoinnilla

```csharp
public class Product
{
    private decimal price;
    private int stockQuantity;
    
    public string Name { get; set; }
    
    // Property validoinnilla
    public decimal Price
    {
        get => price;
        set
        {
            if (value < 0)
                throw new ArgumentException("Hinta ei voi olla negatiivinen");
            if (value > 1000000)
                throw new ArgumentException("Hinta on epärealistisen suuri");
            price = value;
        }
    }
    
    public int StockQuantity
    {
        get => stockQuantity;
        set
        {
            if (value < 0)
                throw new ArgumentException("Varastomäärä ei voi olla negatiivinen");
            stockQuantity = value;
        }
    }
    
    // Computed property - lasketaan lennossa
    public decimal TotalValue => Price * StockQuantity;
    
    // Property joka käyttää muita propertyjä
    public bool IsInStock => StockQuantity > 0;
    public bool IsLowStock => StockQuantity > 0 && StockQuantity < 10;
}
```

### Expression-bodied properties

```csharp
public class Circle
{
    public double Radius { get; set; }
    
    // ✅ Expression-bodied property (suositeltu yksinkertaisille)
    public double Diameter => Radius * 2;
    public double Area => Math.PI * Radius * Radius;
    public double Circumference => 2 * Math.PI * Radius;
}
```

---

## Readonly ja Const

### Const - Kääntöaikainen vakio

```csharp
public class MathConstants
{
    // ✅ const - arvo ei voi muuttua koskaan
    public const double PI = 3.14159265359;
    public const int MaxIterations = 1000;
    public const string Version = "1.0.0";
    
    // ❌ const ei voi olla objekti
    // public const Person DefaultPerson = new Person(); // EI TOIMI!
}

// Käyttö:
double area = MathConstants.PI * radius * radius;
```

### Readonly - Ajonaikainen vakio

```csharp
public class Configuration
{
    // ✅ readonly - voidaan asettaa vain konstruktorissa
    public readonly string DatabaseConnection;
    public readonly DateTime StartTime;
    public readonly List<string> AllowedUsers;
    
    public Configuration(string dbConnection)
    {
        DatabaseConnection = dbConnection;
        StartTime = DateTime.UtcNow;
        AllowedUsers = new List<string> { "admin", "user" };
    }
    
    public void Test()
    {
        // DatabaseConnection = "new value"; // ❌ EI TOIMI readonly!
        AllowedUsers.Add("guest"); // ✅ TOIMI - lista itsessään ei muutu, sisältö voi
    }
}
```

### Vertailu:

| Ominaisuus | const | readonly |
|------------|-------|----------|
| Arvo asetetaan | Kääntöaikana | Ajonaikana (konstruktorissa) |
| Tyyppi | Vain value types + string | Kaikki tyypit |
| Static | Aina implisiittisesti | Voi olla instance tai static |
| Käyttö | `ClassName.ConstName` | `instance.ReadonlyField` |

---

## Käytännön esimerkit

### Esimerkki 1: Email-validointi

```csharp
public class User
{
    private string email;
    
    public string Email
    {
        get => email;
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Sähköposti on pakollinen");
            if (!value.Contains("@"))
                throw new ArgumentException("Virheellinen sähköpostiosoite");
            if (value.Length > 100)
                throw new ArgumentException("Sähköpostiosoite on liian pitkä");
                
            email = value.ToLower().Trim(); // Normalisoi
        }
    }
}
```

### Esimerkki 2: Luottokortti

```csharp
public class CreditCard
{
    private string cardNumber;
    private string cvv;
    private DateTime expiryDate;
    
    public string CardNumber
    {
        get => MaskCardNumber(cardNumber);
        set
        {
            if (!IsValidCardNumber(value))
                throw new ArgumentException("Virheellinen korttinumero");
            cardNumber = value;
        }
    }
    
    public string CVV
    {
        set // Vain write-only!
        {
            if (value?.Length != 3)
                throw new ArgumentException("CVV:n täytyy olla 3 numeroa");
            cvv = value;
        }
    }
    
    public DateTime ExpiryDate
    {
        get => expiryDate;
        set
        {
            if (value <= DateTime.Now)
                throw new ArgumentException("Kortti on vanhentunut");
            expiryDate = value;
        }
    }
    
    public bool IsValid => expiryDate > DateTime.Now;
    
    private string MaskCardNumber(string number)
    {
        if (string.IsNullOrEmpty(number) || number.Length < 4)
            return "****";
        return "**** **** **** " + number.Substring(number.Length - 4);
    }
    
    private bool IsValidCardNumber(string number)
    {
        // Yksinkertainen tarkistus (oikeassa sovelluksessa Luhn-algoritmi)
        return !string.IsNullOrWhiteSpace(number) && 
               number.Length >= 13 && 
               number.Length <= 19;
    }
}
```

### Esimerkki 3: Temperature-luokka

```csharp
public class Temperature
{
    private double celsius;
    
    public double Celsius
    {
        get => celsius;
        set
        {
            if (value < -273.15)
                throw new ArgumentException("Lämpötila ei voi olla alle absoluuttisen nollan");
            celsius = value;
        }
    }
    
    // Muut yksiköt computed propertiesina
    public double Fahrenheit
    {
        get => (Celsius * 9 / 5) + 32;
        set => Celsius = (value - 32) * 5 / 9;
    }
    
    public double Kelvin
    {
        get => Celsius + 273.15;
        set => Celsius = value - 273.15;
    }
}

// Käyttö:
Temperature temp = new Temperature { Celsius = 25 };
Console.WriteLine($"{temp.Celsius}°C = {temp.Fahrenheit}°F = {temp.Kelvin}K");
```

---

## Best Practices

### ✅ DO (Tee näin):

1. **Käytä aina private fieldsejä**
```csharp
private string name; // ✅
public string Name { get; set; } // ✅
```

2. **Käytä auto-propertyja yksinkertaisissa tapauksissa**
```csharp
public string Name { get; set; } // ✅ Yksinkertainen
public int Age { get; private set; } // ✅ Kontrolloitu
```

3. **Validoi aina setter:ssä**
```csharp
public int Age
{
    get => age;
    set
    {
        if (value < 0 || value > 150)
            throw new ArgumentException("Invalid age");
        age = value;
    }
}
```

4. **Käytä expression-bodied membereitä yksinkertaisille**
```csharp
public double Area => Width * Height; // ✅
public bool IsValid => Age >= 18; // ✅
```

5. **Piiloita arkaluontoiset tiedot**
```csharp
public string Password
{
    set => passwordHash = HashPassword(value); // Vain write
}

public string CardNumber => MaskCard(cardNumber); // Peitetty
```

### ❌ DON'T (Älä tee näin):

1. **Älä käytä public fieldejä**
```csharp
public string Name; // ❌ HUONO!
```

2. **Älä jätä validointia pois**
```csharp
public int Age { get; set; } // ❌ Ei validointia - voisi olla negatiivinen!
```

3. **Älä paljasta sisäisiä kokoelmia**
```csharp
// ❌ HUONO
public List<string> Items { get; set; }

// ✅ HYVÄ
private List<string> items;
public IReadOnlyList<string> Items => items.AsReadOnly();
```

4. **Älä tee propertyjä jotka tekevät raskaita operaatioita**
```csharp
// ❌ HUONO - property ei pitäisi olla raskas
public List<User> AllUsers => database.LoadAllUsers();

// ✅ HYVÄ - käytä metodia
public List<User> GetAllUsers() => database.LoadAllUsers();
```

---

## Yleiset virheet

### Virhe 1: Public fields

```csharp
// ❌ HUONO
public class BadUser
{
    public string name;
    public int age;
}

// ✅ HYVÄ
public class GoodUser
{
    private string name;
    private int age;
    
    public string Name { get; set; }
    public int Age { get; set; }
}
```

### Virhe 2: Ei validointia

```csharp
// ❌ HUONO
public int Age { get; set; } // Voi olla -1000!

// ✅ HYVÄ
private int age;
public int Age
{
    get => age;
    set
    {
        if (value < 0 || value > 150)
            throw new ArgumentException("Invalid age");
        age = value;
    }
}
```

### Virhe 3: Mutable collections

```csharp
// ❌ HUONO
public List<string> Names { get; set; } // Kuka tahansa voi muokata!

// ✅ HYVÄ
private List<string> names = new();
public IReadOnlyList<string> Names => names.AsReadOnly();
public void AddName(string name) => names.Add(name);
```

### Virhe 4: Raskas property

```csharp
// ❌ HUONO - property tekee raskaan operaation
public List<User> AllUsers => LoadUsersFromDatabase();

// ✅ HYVÄ - metodi ilmaisee että tämä on raskas
public List<User> GetAllUsers() => LoadUsersFromDatabase();
```

---

## Yhteenveto

Kapselointi on olio-ohjelmoinnin perusta ja tärkein periaate.

### Muista:
- ✅ Käytä aina `private` fieldejä
- ✅ Tarjoa `public` propertyjä ja metodeja
- ✅ Validoi aina settersissä
- ✅ Piilota toteutuksen yksityiskohdat
- ✅ Käytä `readonly` muuttumattomille arvoille
- ✅ Palauta kopioita tai read-only viittauksia

### Hyödyt:
1. **Tietoturva** - Data on suojattu virheiltä
2. **Joustavuus** - Toteutusta voi muuttaa
3. **Ylläpidettävyys** - Muutokset yhdessä paikassa
4. **Testattavuus** - Helpompi testata
5. **Dokumentointi** - Propertyjen nimet kertovat tarkoituksen

**Seuraava askel:** Kun hallitset kapseloinnin, jatka [Perintä (Inheritance)](Inheritance.md) materiaaliin.

---

