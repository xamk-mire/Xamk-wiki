# Funktiot ja Metodit (Functions and Methods)

C#-kielessä termit "funktio" ja "metodi" viittaavat samaan asiaan: koodilohkoon, joka suorittaa tietyn tehtävän ja voidaan kutsua uudelleen.

## Mitä ovat metodit?

Metodi on nimetty koodilohko, joka suorittaa tietyn tehtävän. Metodit auttavat:
- **Koodin uudelleenkäytössä**: Sama koodi voidaan käyttää useita kertoja
- **Modulaarisuudessa**: Koodi jaetaan pieniin, hallittaviin osiin
- **Luettavuudessa**: Metodit tekevät koodista selkeämpää

## Metodin määrittely

### Perussyntaksi

```csharp
[access-modifier] [return-type] MethodName([parameters])
{
    // Metodin runko
    return value; // Jos palauttaa arvon
}
```

### Esimerkkejä

```csharp
// Metodi ilman parametreja ja palautusarvoa
public void Greet()
{
    Console.WriteLine("Hei maailma!");
}

// Metodi parametreilla
public void Greet(string name)
{
    Console.WriteLine($"Hei {name}!");
}

// Metodi palautusarvolla
public int Add(int a, int b)
{
    return a + b;
}

// Metodi useilla parametreilla
public string CreateFullName(string firstName, string lastName)
{
    return $"{firstName} {lastName}";
}
```

## Metodin kutsuminen

```csharp
// Kutsu metodia ilman palautusarvoa
Greet();

// Kutsu metodia parametreilla
Greet("Matti");

// Kutsu metodia ja tallenna palautusarvo
int sum = Add(5, 3);
Console.WriteLine(sum);  // 8

// Kutsu metodia suoraan ilman tallennusta
Console.WriteLine(Add(10, 20));  // 30
```

## Parametrit

### Arvoparametrit (Value Parameters)

Parametri kopioidaan metodin kutsuessa:

```csharp
public void Increment(int number)
{
    number++;  // Muuttaa vain kopiota
    Console.WriteLine($"Metodissa: {number}");
}

int x = 5;
Increment(x);
Console.WriteLine($"Kutsujan jälkeen: {x}");  // x on edelleen 5
```

### Viittausparametrit (Reference Parameters)

`ref`-avainsana antaa metodin muuttaa alkuperäistä muuttujaa:

```csharp
public void Increment(ref int number)
{
    number++;  // Muuttaa alkuperäistä muuttujaa
}

int x = 5;
Increment(ref x);
Console.WriteLine(x);  // x on nyt 6
```

### Output-parametrit

`out`-avainsana pakottaa metodin asettamaan arvon:

```csharp
public bool TryDivide(int dividend, int divisor, out int result)
{
    if (divisor == 0)
    {
        result = 0;
        return false;
    }
    
    result = dividend / divisor;
    return true;
}

// Käyttö
if (TryDivide(10, 2, out int result))
{
    Console.WriteLine($"Tulos: {result}");  // 5
}
```

### Valinnaiset parametrit (Optional Parameters)

Parametrille voidaan antaa oletusarvo:

```csharp
public void Greet(string name, string greeting = "Hei")
{
    Console.WriteLine($"{greeting} {name}!");
}

Greet("Matti");              // "Hei Matti!"
Greet("Matti", "Moro");      // "Moro Matti!"
```

### Nimetty parametrit (Named Parameters)

Parametrit voidaan nimetä kutsuessa:

```csharp
public void CreateUser(string firstName, string lastName, int age = 0)
{
    Console.WriteLine($"{firstName} {lastName}, {age} vuotta");
}

// Käyttö
CreateUser("Matti", "Meikäläinen", 25);
CreateUser(firstName: "Matti", lastName: "Meikäläinen", age: 25);
CreateUser(lastName: "Meikäläinen", firstName: "Matti");  // Järjestys ei merkitse
```

## Palautusarvot

### Void-metodit

Metodit, jotka eivät palauta arvoa:

```csharp
public void DisplayMessage(string message)
{
    Console.WriteLine(message);
}
```

### Palautusarvon tyyppi

```csharp
// Palauttaa int
public int GetAge()
{
    return 25;
}

// Palauttaa string
public string GetName()
{
    return "Matti";
}

// Palauttaa bool
public bool IsAdult(int age)
{
    return age >= 18;
}

// Palauttaa objektin
public Person CreatePerson(string name, int age)
{
    return new Person { Name = name, Age = age };
}
```

### Useita palautusarvoja (Tuples)

```csharp
public (int sum, int product) Calculate(int a, int b)
{
    return (a + b, a * b);
}

// Käyttö
var result = Calculate(5, 3);
Console.WriteLine($"Summa: {result.sum}, Tulo: {result.product}");

// Tai hajotetaan suoraan
(int sum, int product) = Calculate(5, 3);
```

## Metodin ylikuormitus (Method Overloading)

Sama metodi voidaan määritellä useilla eri parametreilla:

```csharp
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }
    
    public double Add(double a, double b)
    {
        return a + b;
    }
    
    public int Add(int a, int b, int c)
    {
        return a + b + c;
    }
}

// Käyttö
Calculator calc = new Calculator();
int result1 = calc.Add(5, 3);        // 8
double result2 = calc.Add(5.5, 3.2); // 8.7
int result3 = calc.Add(1, 2, 3);     // 6
```

## Rekursio

Metodi voi kutsua itseään:

```csharp
public int Factorial(int n)
{
    if (n <= 1)
        return 1;
    
    return n * Factorial(n - 1);
}

// Käyttö
int result = Factorial(5);  // 5 * 4 * 3 * 2 * 1 = 120
```

## Lambda-lausekkeet (Lambda Expressions)

Lyhyt tapa määritellä metodit:

```csharp
// Perinteinen metodi
public int Add(int a, int b)
{
    return a + b;
}

// Lambda-lauseke
Func<int, int, int> add = (a, b) => a + b;

// Käyttö
int result = add(5, 3);  // 8

// Lambda-lauseke ilman parametreja
Action greet = () => Console.WriteLine("Hei!");

// Lambda-lauseke yhdellä parametrilla
Func<int, int> square = x => x * x;
```

## Extension-metodit

Metodit, jotka voidaan lisätä olemassa oleviin luokkiin:

```csharp
public static class StringExtensions
{
    public static bool IsValidEmail(this string email)
    {
        return email.Contains("@") && email.Contains(".");
    }
    
    public static string Reverse(this string text)
    {
        char[] chars = text.ToCharArray();
        Array.Reverse(chars);
        return new string(chars);
    }
}

// Käyttö
string email = "test@example.com";
bool isValid = email.IsValidEmail();  // Extension-metodi
string reversed = email.Reverse();
```

## Yhteenveto

- Metodit ovat nimettyjä koodilohkoja, jotka suorittavat tehtävän
- Parametrit välittävät dataa metodeihin
- Palautusarvot palauttavat tuloksen
- Metodin ylikuormitus mahdollistaa useita versioita
- Lambda-lausekkeet ovat lyhyitä tapoja määritellä metodeja

Seuraavaksi: [Ohjausrakenteet](Control-Structures.md)

