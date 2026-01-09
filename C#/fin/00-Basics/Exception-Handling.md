# Poikkeusten käsittely (Exception Handling)

**Microsoftin virallinen dokumentaatio:**
- [Exception Handling in C#](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/exceptions/)

Poikkeukset (exceptions) ovat virhetilanteita, jotka tapahtuvat ohjelman suorituksen aikana. C#-kielessä poikkeukset käsitellään `try-catch`-lohkoilla.

## Mitä ovat poikkeukset?

Poikkeus on erityinen olio, joka heitetään kun virhetilanne tapahtuu. Jos poikkeusta ei käsitellä, ohjelma kaatuu.

Poikkeuskäsittely on ohjelmointikäsite, jota käytetään odottamattomien virhetilanteiden käsittelyyn ohjelman suorituksen aikana. Kun ohjelmaa suoritetaan ja siinä tapahtuu virhe, se saattaa aiheuttaa ohjelman kaatumisen tai toimimattomuuden. Poikkeuskäsittelyn tarkoitus on antaa ohjelmalle mahdollisuus käsitellä näitä virheitä hallitusti ilman, että ohjelma kaatuu.

## Keskeiset käsitteet

1. **Poikkeukset**: Nämä ovat ohjelman suorituksen aikana tapahtuvia virheitä. Esimerkiksi, jaettuna nollalla, tiedoston avaaminen, jota ei ole olemassa, tai yritys muuttaa merkkijonoa numeroksi, kun se ei ole mahdollista.

2. **Heittäminen (throw)**: Kun virhe tapahtuu, ohjelma "heittää" poikkeuksen. Tämä tarkoittaa, että se ilmoittaa virheestä ja siirtää ohjauksen poikkeuskäsittelijälle, jos sellainen on määritetty.

3. **Kiinniottaminen (catch)**: Ohjelmassa voi olla koodilohko, joka "ottaa kiinni" heitetyn poikkeuksen. Tämä on se paikka, jossa virhe käsitellään. Esimerkiksi, voit näyttää virheilmoituksen käyttäjälle tai yrittää korjata virheen ja jatkaa ohjelman suorittamista. Näitä catch-lohkoja voi olla myös useampi peräkkäin. Jokaisen catch-lohkon tarkoitus on käsitellä tiettyä virhetilannetta.

4. **Finally-lohko**: Tämä on koodilohko, joka suoritetaan riippumatta siitä, tapahtuiko virhe vai ei. Se on hyvä paikka resurssien vapauttamiseen tai muunlaisille lopetusoperaatioille.

## Try-Catch-lohko

### Perussyntaksi

```csharp
try
{
    // Koodi, joka voi aiheuttaa poikkeuksen
}
catch (ExceptionType ex)
{
    // Koodi, joka suoritetaan jos poikkeus tapahtuu
}
finally
{
    // Koodi, joka suoritetaan aina (valinnainen)
}
```

### Yksinkertainen esimerkki

```csharp
try
{
    int number = int.Parse("123");
    Console.WriteLine($"Numero: {number}");
}
catch (FormatException ex)
{
    Console.WriteLine($"Virhe: {ex.Message}");
}
```

## Yleisimmät poikkeustyypit

### 1. FormatException

Tapahtuu kun merkkijonoa ei voida muuntaa numeroksi:

```csharp
try
{
    int number = int.Parse("abc");  // ❌ Virhe!
}
catch (FormatException ex)
{
    Console.WriteLine($"Muunnosvirhe: {ex.Message}");
}
```

### 2. NullReferenceException

Tapahtuu kun yritetään käyttää null-viittausta:

```csharp
string text = null;
try
{
    int length = text.Length;  // ❌ Virhe! text on null
}
catch (NullReferenceException ex)
{
    Console.WriteLine($"Null-viittaus: {ex.Message}");
}
```

### 3. ArgumentNullException

Tapahtuu kun null-arvo annetaan parametrina:

```csharp
public void ProcessUser(User user)
{
    if (user == null)
        throw new ArgumentNullException(nameof(user), "Käyttäjä ei voi olla null");
    
    // Käsittele käyttäjää
}
```

### 4. IndexOutOfRangeException

Tapahtuu kun yritetään käyttää taulukon ulkopuolella olevaa indeksiä:

```csharp
int[] numbers = { 1, 2, 3 };
try
{
    int value = numbers[10];  // ❌ Virhe! Indeksi 10 ei ole olemassa
}
catch (IndexOutOfRangeException ex)
{
    Console.WriteLine($"Indeksivirhe: {ex.Message}");
}
```

### 5. DivideByZeroException

Tapahtuu kun yritetään jakaa nollalla:

```csharp
try
{
    int result = 10 / 0;  // ❌ Virhe!
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Jako nollalla: {ex.Message}");
}
```

## Useita catch-lohkoja

Voit käsitellä eri poikkeustyypit erikseen:

```csharp
try
{
    int number = int.Parse(Console.ReadLine());
    int result = 100 / number;
    Console.WriteLine($"Tulos: {result}");
}
catch (FormatException ex)
{
    Console.WriteLine("Syöte ei ole kelvollinen numero");
}
catch (DivideByZeroException ex)
{
    Console.WriteLine("Ei voi jakaa nollalla");
}
catch (Exception ex)
{
    Console.WriteLine($"Odottamaton virhe: {ex.Message}");
}
```

## Finally-lohko

`finally`-lohko suoritetaan aina, riippumatta siitä tapahtuiko poikkeus vai ei:

```csharp
FileStream file = null;
try
{
    file = File.Open("data.txt", FileMode.Open);
    // Käsittele tiedostoa
}
catch (FileNotFoundException ex)
{
    Console.WriteLine($"Tiedostoa ei löytynyt: {ex.Message}");
}
finally
{
    // Varmista että tiedosto suljetaan aina
    if (file != null)
        file.Close();
}
```

### Using-lause (parempi tapa)

`using`-lause sulkee automaattisesti resurssit:

```csharp
// ✅ HYVÄ: using-lause sulkee automaattisesti
using (FileStream file = File.Open("data.txt", FileMode.Open))
{
    // Käsittele tiedostoa
    // Tiedosto suljetaan automaattisesti
}

// ✅ HYVÄ: using-lause ilman aaltosulkeita (C# 8.0+)
using var file = File.Open("data.txt", FileMode.Open);
// Tiedosto suljetaan automaattisesti lohkon lopussa
```

## Poikkeuksen heittäminen

Voit heittää poikkeuksen itse `throw`-avainsanalla:

```csharp
public int Divide(int a, int b)
{
    if (b == 0)
        throw new DivideByZeroException("Jakaja ei voi olla nolla");
    
    return a / b;
}

// Käyttö
try
{
    int result = Divide(10, 0);
}
catch (DivideByZeroException ex)
{
    Console.WriteLine($"Virhe: {ex.Message}");
}
```

## Mukautettu poikkeusluokka

Voit luoda oman poikkeusluokan:

```csharp
public class InvalidAgeException : Exception
{
    public InvalidAgeException(string message) : base(message)
    {
    }
    
    public InvalidAgeException(string message, Exception innerException) 
        : base(message, innerException)
    {
    }
}

// Käyttö
public void SetAge(int age)
{
    if (age < 0 || age > 150)
        throw new InvalidAgeException($"Ikä {age} ei ole kelvollinen");
    
    this.age = age;
}

try
{
    person.SetAge(-5);
}
catch (InvalidAgeException ex)
{
    Console.WriteLine($"Ikävirhe: {ex.Message}");
}
```

## Poikkeusten käsittelyn best practices

### 1. Käsittele spesifiset poikkeukset ensin

```csharp
// ✅ HYVÄ
try
{
    // Koodi
}
catch (FormatException ex)
{
    // Spesifinen käsittely
}
catch (Exception ex)
{
    // Yleinen käsittely viimeisenä
}
```

### 2. Älä jätä catch-lohkoa tyhjäksi

```csharp
// ❌ HUONO
try
{
    DoSomething();
}
catch (Exception ex)
{
    // Tyhjä - virhe piilotetaan!
}

// ✅ HYVÄ
try
{
    DoSomething();
}
catch (Exception ex)
{
    // Logita virhe
    Logger.LogError(ex);
    // Tai heitä eteenpäin
    throw;
}
```

### 3. Käytä using-lausetta resursseille

```csharp
// ✅ HYVÄ
using (var connection = new SqlConnection(connectionString))
{
    // Käytä yhteyttä
}

// ❌ HUONO
SqlConnection connection = null;
try
{
    connection = new SqlConnection(connectionString);
    // Käytä yhteyttä
}
finally
{
    if (connection != null)
        connection.Close();
}
```

### 4. Tarkista null-arvoja ennen käyttöä

```csharp
// ✅ HYVÄ
if (user != null)
{
    Console.WriteLine(user.Name);
}

// ❌ HUONO
try
{
    Console.WriteLine(user.Name);  // Voit aiheuttaa NullReferenceException
}
catch (NullReferenceException)
{
    // Käsittele virhe
}
```

## Milloin käyttää poikkeusten hallintaa?

Käytä poikkeusten käsittelyä silloin, kun virhe on **odottamaton** ja estää normaalin etenemisen. Älä käytä poikkeuksia silloin, kun voit estää virheen etukäteen, kuten tarkistamalla, että arvo ei ole null tai esim. syöte ei ole numero.

**Esimerkki - älä käytä poikkeuksia:**

```csharp
// ❌ HUONO: Käyttää poikkeusta normaaliin kontrolliin
try
{
    int number = int.Parse(userInput);
}
catch (FormatException)
{
    // Käsittele virheellinen syöte
}

// ✅ HYVÄ: Tarkista etukäteen
if (int.TryParse(userInput, out int number))
{
    // Käytä numeroa
}
else
{
    // Käsittele virheellinen syöte
}
```

Eli poikkeukset eivät ole osa ohjelman normaalia kulkua – ne ovat **poikkeuksia normaaliin toimintaan**.

**Esimerkkejä tilanteista, joissa poikkeukset ovat oikein:**
- Tiedostoa ei löydy
- Yhteys verkkoon katkeaa
- Käyttäjällä ei ole oikeuksia
- Muisti loppuu
- JSON-tiedosto on virheellinen

## Poikkeustilanteiden oikeanlainen käyttö

Poikkeuskäsittelyn käyttö on välttämätöntä virhetilanteiden käsittelyssä, mutta se ei ole "ilmaista" suorituskyvyn näkökulmasta, ja väärin käytettynä se voi tehdä koodista sekavan ja vaikeasti ylläpidettävän. Tässä on muutamia syitä siihen, miksi poikkeuskäsittely tulisi rajata vain tietylle koodille:

### 1. Suorituskyky

Poikkeusten heittäminen ja niiden käsittely voi olla kallista suorituskyvyn kannalta verrattuna tavalliseen ohjaukseen. Vaikka modernit järjestelmät ja kielet ovat tehokkaita, poikkeusten liiallinen käyttö voi silti aiheuttaa suorituskykyongelmia, erityisesti tiukoissa suorituskyvyn vaatimuksissa, kuten reaaliaikaisissa järjestelmissä.

### 2. Lukemisen helppous

Jos jokaista pientä virhetilannetta käsitellään poikkeuksena, koodi voi tulla vaikealukuiseksi. Selkeän virhekoodin palauttaminen tai ehtolauseen käyttäminen voi olla helpompi ymmärtää tietyissä tilanteissa.

### 3. Hallinta

Poikkeusten heittämistä pitkin poikki voi tehdä virheiden lähteen jäljittämisen vaikeammaksi. On tärkeää ymmärtää, mistä ja miksi poikkeus heitetään. Rajoittamalla poikkeusten käyttöä tietyille kriittisille koodin osille, voit olla varma, että vain todella odottamattomat virheet aiheuttavat poikkeuksia.

### 4. Resurssien vapauttaminen

Jos heität poikkeuksen keskellä koodia, joka käyttää resursseja (kuten tiedostoja tai tietokantayhteyksiä), sinun on oltava varovainen, että vapautat nämä resurssit oikein. Muuten saatat aiheuttaa resurssivuotoja. Tämä on erityinen syy käyttää `finally`-lohkoa, joka varmistaa, että resurssit vapautetaan asianmukaisesti.

### 5. Semantiikka

Poikkeusten tulisi kuvata poikkeuksellisia olosuhteita, ei normaalia ohjelman toimintaa. Jos esimerkiksi tietyssä tilanteessa jotain ei löydy tietokannasta, se ei välttämättä ole "poikkeus", vaan normaali osa sovelluksen toimintaa, ja se tulisi käsitellä sellaisena.

**Tiivistettynä**: Poikkeuskäsittely on tehokas työkalu odottamattomien virhetilanteiden käsittelyssä, mutta sen pitäisi kuvata nimensä mukaisesti "poikkeuksellisia" olosuhteita. Sen liiallinen tai väärä käyttö voi aiheuttaa suorituskykyongelmia, tehdä koodista sekavan ja lisätä ylläpidon haasteita. Siksi on tärkeää käyttää poikkeuskäsittelyä harkitusti ja rajoittaa se niihin koodin osiin, joissa se on todella tarpeellista.

## Yhteenveto

- Poikkeukset käsitellään `try-catch`-lohkoilla
- `finally`-lohko suoritetaan aina
- Käytä `using`-lausetta resursseille
- Käsittele spesifiset poikkeukset ensin
- Älä piilota poikkeuksia tyhjällä catch-lohkolla
- Käytä poikkeuksia vain odottamattomille virhetilanteille, ei normaaliin kontrolliin
- Rajoita poikkeuskäsittely kriittisille koodin osille

Seuraavaksi: [Funktiot ja Metodit](Functions-and-Methods.md)

