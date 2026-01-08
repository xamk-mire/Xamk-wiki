# Kapselointi (Encapsulation)

## Kapseloinnin ongelma, joka ratkaistaan

Ilman kapselointia luokan sisäisiä tietoja (muuttujia) voidaan lukemattomilla tavoilla lukea ja muokata suoraan ulkopuolelta, mikä voi rikkoa luokan eheyttä ja vaikeuttaa ylläpitoa.

## Ratkaisu

Kapselointi kätkee luokan toteutuksen yksityiskohdat tarjoamalla julkiset `get`- ja `set`-metodit (tai ominaisuudet) muuttujien käsittelyyn. Näin varmistetaan tietoturva ja selkeä rajapinta ulkoisille käyttäjille.

## Ennen kapselointia (ongelma)

```csharp
// ❌ HUONO: Julkiset kentät, ei kontrollia
public class BankAccount
{
    public decimal balance; // Kuka tahansa voi muuttaa suoraan!
    public string accountNumber;
}

// Käyttö - vaarallista!
BankAccount account = new BankAccount();
account.balance = -1000; // Voimme asettaa negatiivisen saldon!
account.balance = 999999; // Tai liian suuren summan!
```

**Ongelmat:**
- Ei validointia
- Ei kontrollia datan eheydestä
- Helppo tehdä virheitä
- Vaikea ylläpitää

## Kapseloinnin avulla (ratkaisu)

### Vaihtoehto 1: Properties (Ominaisuudet)

```csharp
// ✅ HYVÄ: Kapseloitu toteutus
public class BankAccount
{
    private decimal balance; // Yksityinen kenttä
    private string accountNumber;
    
    public string AccountNumber
    {
        get { return accountNumber; }
        private set { accountNumber = value; } // Vain luokka voi asettaa
    }
    
    public decimal Balance
    {
        get { return balance; }
        // Ei setteriä - saldoa ei voi muuttaa suoraan!
    }
    
    public BankAccount(string accountNumber, decimal initialBalance)
    {
        this.accountNumber = accountNumber;
        if (initialBalance >= 0)
            this.balance = initialBalance;
        else
            throw new ArgumentException("Alkusaldo ei voi olla negatiivinen");
    }
    
    public void Deposit(decimal amount)
    {
        if (amount > 0)
        {
            balance += amount;
            Console.WriteLine($"Talletettu {amount} euroa. Uusi saldo: {balance}");
        }
        else
        {
            throw new ArgumentException("Talletussumman täytyy olla positiivinen");
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
}
```

### Vaihtoehto 2: Auto-Properties (Automaattiset ominaisuudet)

```csharp
// ✅ HYVÄ: Auto-property validointilla
public class Person
{
    private string name;
    private int age;
    
    public string Name
    {
        get { return name; }
        set
        {
            if (string.IsNullOrWhiteSpace(value))
                throw new ArgumentException("Nimi ei voi olla tyhjä");
            name = value;
        }
    }
    
    public int Age
    {
        get { return age; }
        set
        {
            if (value < 0 || value > 150)
                throw new ArgumentException("Ikä täytyy olla välillä 0-150");
            age = value;
        }
    }
}
```

### Käyttöesimerkki:

```csharp
// ✅ Turvallinen käyttö
BankAccount account = new BankAccount("FI123456789", 1000.00m);
account.Deposit(500.00m);   // OK
account.Withdraw(200.00m);  // OK
// account.balance = -1000; // ❌ Ei toimi - balance on yksityinen!
// account.Balance = 5000;  // ❌ Ei toimi - ei setteriä!

Console.WriteLine($"Saldo: {account.Balance}"); // ✅ Vain luku
```

## Kapseloinnin hyödyt

1. **Tietoturva**: Datan eheys varmistetaan validointilla
2. **Joustavuus**: Voimme muuttaa toteutusta ilman, että ulkopuolinen koodi rikkoontuu
3. **Ylläpidettävyys**: Muutokset tehdään yhdessä paikassa
4. **Testattavuus**: Helpompi testata, kun logiikka on keskitetty

## Yhteenveto

Kapselointi on olio-ohjelmoinnin perusta, joka varmistaa että luokan sisäinen toteutus pysyy piilotettuna ja datan käsittely tapahtuu kontrolloidusti julkisten metodien kautta.

