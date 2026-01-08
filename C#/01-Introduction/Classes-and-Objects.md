# Luokat ja Objektit (Classes and Objects)

## Mitä ovat luokat?

Luokka (class) C#-kielessä on malli objektien luomiseen. Se määrittelee tyypin yhdistämällä datan (muuttujat) ja metodit (funktiot), jotka toimivat tällä datalla, yhdeksi yksiköksi. Luokan sisältämät data ja metodit kutsutaan luokan jäseniksi.

### Luokan jäsenet

- **Data Members (Datan jäsenet)**: Yleensä kentät (fields) tai ominaisuudet (properties), jotka tallentavat dataa
- **Methods (Metodit)**: Funktiot, jotka määrittelevät toimintoja, joita luokka voi suorittaa

## Esimerkki: Yksinkertainen luokka

```csharp
public class Person
{
    // Data members (kentät)
    private string name;
    private int age;
    
    // Properties (ominaisuudet)
    public string Name
    {
        get { return name; }
        set { name = value; }
    }
    
    public int Age
    {
        get { return age; }
        set { age = value; }
    }
    
    // Methods (metodit)
    public void Introduce()
    {
        Console.WriteLine($"Hei, olen {name} ja olen {age} vuotta vanha.");
    }
}
```

## Objektin luominen

```csharp
// Luodaan objekti Person-luokasta
Person person1 = new Person();
person1.Name = "Matti";
person1.Age = 25;
person1.Introduce(); // Tulostaa: "Hei, olen Matti ja olen 25 vuotta vanha."
```

## Miksi käytämme luokkia?

### 1. Kapselointi (Encapsulation)
Luokat kapseloivat datan ja metodit yhdeksi yksiköksi. Tämä tarkoittaa, että luokka voi piilottaa sisäiset toteutuksensa ulkomaailmalta ja näyttää vain tarvittavat asiat. Tämä tekee koodista turvallisempaa ja vähemmän virhealtista.

### 2. Jälleenkäytettävyys (Reusability)
Kun luokka on kirjoitettu, sitä voidaan käyttää uudelleen ohjelman eri osissa ilman tarvetta kirjoittaa koodia uudelleen.

### 3. Modulaarisuus (Modularity)
Luokat mahdollistavat monimutkaisen ongelman jakamisen pienempiin, hallittavampiin osiin. Jokainen luokka voidaan kehittää itsenäisesti muista.

### 4. Perintä (Inheritance)
Luokat tukevat perintää, mikä tarkoittaa, että uusi luokka voidaan johtaa olemassa olevasta luokasta, perien sen ominaisuudet ja metodit. Tämä edistää koodin uudelleenkäyttöä ja yksinkertaistaa ylläpitoa.

### 5. Polymorfismi (Polymorphism)
Luokat mahdollistavat polymorfismin, jossa yksi rajapinta voidaan käyttää edustamaan eri taustalla olevia tietotyyppejä.

## Luokkien hyödyt C#-kielessä

### 1. Organisointi
Luokat auttavat koodin organisoinnissa ja rakenteessa, mikä tekee siitä helpommin luettavaa ja ylläpidettävää.

### 2. Tietoturva
Käyttämällä pääsyn muuttujia (access modifiers) kuten `public`, `private`, `protected` jne., luokat voivat hallita, kuka pääsee käsiksi niiden dataan, parantaen turvallisuutta ja datan eheyttä.

### 3. Abstraktio (Abstraction)
Luokat mahdollistavat monimutkaisten ongelmien abstrahoinnin yksinkertaisemmiksi, ymmärrettäviksi komponenteiksi.

### 4. Testattavuus
Luokat tekevät yksikkötestien kirjoittamisesta helpompaa tiettyjä toiminnallisuuksia varten, johtuen vankemmasta ja virheettömämmästä koodista.

## Esimerkki: Täydellisempi luokka

```csharp
public class BankAccount
{
    private decimal balance;
    private string accountNumber;
    
    public BankAccount(string accountNumber, decimal initialBalance)
    {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }
    
    public string AccountNumber
    {
        get { return accountNumber; }
    }
    
    public decimal Balance
    {
        get { return balance; }
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            balance += amount;
            Console.WriteLine($"Talletettu {amount} euroa. Uusi saldo: {balance}");
        }
    }
    
    public bool Withdraw(decimal amount)
    {
        if (amount > 0 && amount <= balance)
        {
            balance -= amount;
            Console.WriteLine($"Nostettu {amount} euroa. Uusi saldo: {balance}");
            return true;
        }
        Console.WriteLine("Nosto epäonnistui: riittämätön saldo tai virheellinen summa.");
        return false;
    }
    
    public void DisplayBalance()
    {
        Console.WriteLine($"Tilin {accountNumber} saldo: {balance} euroa");
    }
}
```

### Käyttöesimerkki:

```csharp
BankAccount account = new BankAccount("FI123456789", 1000.00m);
account.DisplayBalance();  // Tilin FI123456789 saldo: 1000.00 euroa
account.Deposit(500.00m);   // Talletettu 500.00 euroa. Uusi saldo: 1500.00
account.Withdraw(200.00m);  // Nostettu 200.00 euroa. Uusi saldo: 1300.00
account.DisplayBalance();   // Tilin FI123456789 saldo: 1300.00 euroa
```

## Yhteenveto

Luokat ovat C#-ohjelmoinnin perusrakennuspalikoita. Ne mahdollistavat:
- Koodin organisoinnin ja rakenteen
- Tietoturvan ja datan eheyden
- Koodin uudelleenkäytön
- Modulaarisen ohjelmoinnin
- Testattavuuden

Seuraavaksi tutustumme olio-ohjelmoinnin peruskäsitteisiin.

