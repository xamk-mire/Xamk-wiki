# Koodauskäytännöt (Coding Conventions)

Kenelle kirjoitamme koodia? Nopeasti tähän saattaisi vastata, että kirjoitamme koodia tietokoneelle, jotta se osaa tehdä asiat joita me sille käsketään tekemään. Tämä on toki totta, mutta tästä jää erittäin tärkeä aspekti kokonaan puuttumaan, eli ihminen. Koodia aina lukee siis kaksi tahoa, ihminen ja tietokone.

Tietokone lopulta aina ymmärtää mitä haluat saada kirjoitetulla koodilla aikaiseksi, mutta koodi ei välttämättä avaudu toiselle ihmiselle (erillainen muotoilu, nimeäminen jne.). Tätä varten ohjelmistoalalla ollaan kehitetty eri ohjelmointikonventioita, jotka yhtenäistää kehittäjien koodaustyyli samanlaiseksi.

## Mitä on koodauskäytäntö?

"Coding convention" tai koodauskäytäntö/konventio tarkoittaa joukkoa sääntöjä tai ohjeita, jotka määrittelevät koodin ulkoasun ja rakenteen. Se voi kattaa monia asioita, kuten:

1. **Muotoilu**: Esimerkiksi kuinka monta välilyöntiä tai sarkainta (tab) pitäisi käyttää sisennyksessä, kuinka aukot ja rivinvaihdot sijoitetaan tai kuinka kommentteja tulisi käyttää.
2. **Nimeäminen**: Miten muuttujia, funktioita, luokkia jne. tulisi nimetä. Esimerkiksi, voitaisiin päättää, että muuttujien nimet kirjoitetaan pienellä alkukirjaimella ja funktioiden nimet isolla alkukirjaimella.
3. **Komenttien käyttö**: Milloin ja miten lisätä kommentteja koodiin niin, että muut kehittäjät ymmärtävät, mitä koodi tekee.
4. **Ohjelmointikäytännöt**: Kuinka tietyt ohjelmointiongelmat tulisi ratkaista, esim. miten virheidenkäsittelyä pitäisi käyttää.

## Miksi konventioita käytetään?

1. **Luettavuus**: Kun kaikki kehittäjät noudattavat samoja sääntöjä, koodista tulee yhtenäisempää ja helpommin ymmärrettävää. Tämä tekee koodin tarkistamisesta, korjaamisesta ja laajentamisesta helpompaa.
2. **Ylläpidettävyys**: Kun koodi on johdonmukainen ja helppo ymmärtää, sen ylläpitäminen ja päivittäminen tulevaisuudessa on helpompaa.
3. **Virheiden välttäminen**: Jotkut käytännöt voivat auttaa välttämään yleisiä virheitä.
4. **Tiimityö**: Kun useampi kehittäjä työskentelee samassa projektissa, yhtenäiset käytännöt tekevät yhteistyöstä sujuvampaa.

## C#-koodauskäytännöt

Tällä kurssilla käytämme ohjelmointikielenä C#, joten käytämme näissä harjoituksissa Microsoftin luomia konventioita:

- [C# identifier names - rules and conventions | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names)
- [.NET documentation C# Coding Conventions | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)

Näistä teille tärkeämpi näin aluksi on sisäistää **identifier names - rules and conventions**. Voitte esimerkiksi kirjoittaa koodin ensin puhtaaksi ihan omalla tavalla ja sen jälkeen katsoa tuolta, että olette kirjoittaneet koodin tyylillisesti oikein.

## Nimeäminen (Naming Conventions)

### Luokat (Classes)

Käytä **PascalCase**-kirjoitustapaa:

```csharp
// ✅ HYVÄ
public class BankAccount { }
public class UserService { }
public class DataProcessor { }

// ❌ HUONO
public class bankAccount { }
public class user_service { }
public class DataProcessorClass { }
```

### Muuttujat ja metodit

- **Public** jäsenet: PascalCase
- **Private** jäsenet: camelCase

```csharp
public class Person
{
    // Public property - PascalCase
    public string FirstName { get; set; }
    public string LastName { get; set; }
    
    // Private field - camelCase
    private int age;
    
    // Public method - PascalCase
    public void DisplayInfo()
    {
        // Local variable - camelCase
        string fullName = $"{FirstName} {LastName}";
        Console.WriteLine(fullName);
    }
}
```

### Vakiot (Constants)

Käytä **PascalCase**-kirjoitustapaa:

```csharp
// ✅ HYVÄ
public const int MaxRetryAttempts = 3;
public const double Pi = 3.14159;
public const string AppName = "MyApp";

// ❌ HUONO
public const int max_retry_attempts = 3;
public const double PI = 3.14159;
```

## Muotoilu (Formatting)

### Sisennykset

Käytä **4 välilyöntiä** sisennykseen (ei tab-merkkejä):

```csharp
// ✅ HYVÄ
public void Method()
{
    if (condition)
    {
        DoSomething();
    }
}

// ❌ HUONO (väärä sisennyksen määrä)
public void Method()
{
  if (condition)
  {
    DoSomething();
  }
}
```

### Aaltosulkeet (Braces)

Aaltosulkeet omalla rivillään:

```csharp
// ✅ HYVÄ
public void Method()
{
    // Koodi
}

// ❌ HUONO
public void Method() {
    // Koodi
}
```

### Rivinvaihdot

Lisää tyhjä rivi metodien, luokkien ja muiden suurten rakenteiden väliin:

```csharp
// ✅ HYVÄ
public class Person
{
    public string Name { get; set; }
    
    public void DisplayInfo()
    {
        Console.WriteLine(Name);
    }
    
    public void UpdateName(string newName)
    {
        Name = newName;
    }
}
```

## Kommentit

### Yksiriviset kommentit

```csharp
// Tämä on yksirivinen kommentti
int age = 25;
```

### Moniriviset kommentit

```csharp
/*
 * Tämä on monirivinen kommentti
 * joka voi kattaa useita rivejä
 */
```

### XML-dokumentointi

```csharp
/// <summary>
/// Laskee kahden luvun summan.
/// </summary>
/// <param name="a">Ensimmäinen luku</param>
/// <param name="b">Toinen luku</param>
/// <returns>Lukujen summa</returns>
public int Add(int a, int b)
{
    return a + b;
}
```

## Yleisiä käytäntöjä

### 1. Selkeät muuttujan nimet

```csharp
// ✅ HYVÄ - selkeä ja kuvaava
int userAge = 25;
string customerName = "Matti";
bool isActive = true;

// ❌ HUONO - epäselvä
int a = 25;
string n = "Matti";
bool flag = true;
```

### 2. Vältä lyhenteitä

```csharp
// ✅ HYVÄ
string customerName = "Matti";
int numberOfItems = 10;

// ❌ HUONO
string custName = "Matti";
int numItems = 10;
```

### 3. Totuusarvojen nimeäminen

```csharp
// ✅ HYVÄ - alkaa "is", "has", "can" jne.
bool isActive = true;
bool hasPermission = false;
bool canEdit = true;

// ❌ HUONO
bool active = true;
bool permission = false;
```

### 4. Metodien nimeäminen

```csharp
// ✅ HYVÄ - verbi + substantiivi
public void CalculateTotal() { }
public string GetUserName() { return ""; }
public void SaveData() { }

// ❌ HUONO
public void Total() { }
public string UserName() { return ""; }
```

## Yhteenveto

- **Nimeäminen**: PascalCase luokille ja public jäsenille, camelCase private jäsenille ja paikallisille muuttujille
- **Muotoilu**: 4 välilyöntiä sisennykseen, aaltosulkeet omalla rivillään
- **Kommentit**: Selkeät ja hyödylliset kommentit, XML-dokumentointi julkisille metodeille
- **Selkeys**: Selkeät ja kuvaavat nimet, vältä lyhenteitä

Noudattamalla näitä käytäntöjä koodistasi tulee selkeämpää, ylläpidettävämpää ja helpommin ymmärrettävää sekä ihmisille että tietokoneille.

## Hyödyllisiä linkkejä

- [C# identifier names - rules and conventions | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/identifier-names)
- [.NET documentation C# Coding Conventions | Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)

Seuraavaksi: [Visual Studio -vinkit](Visual-Studio-Tips.md)
