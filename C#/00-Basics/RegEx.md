# RegEx (Säännölliset lausekkeet)

## Mikä on Regex?

Säännölliset lausekkeet (**regex, regular expressions**) ovat tehokas tapa etsiä ja käsitellä tekstidataa ohjelmallisesti. Niiden avulla voidaan tunnistaa tiettyjä merkkijonokaavoja, kuten sähköpostiosoitteita, postinumeroita tai tiettyjä sanoja tekstistä.

Regexiä käytetään laajasti eri ohjelmointikielissä, kuten **C#**, **Python**, **JavaScript** ja **Java**. Se on hyödyllinen työkalu esimerkiksi tietojen validoinnissa, tekstin käsittelyssä ja tietojen suodattamisessa.

## Regexin perussyntaksi

Säännölliset lausekkeet muodostuvat **erikoismerkeistä ja symboleista**, joiden avulla voidaan määrittää, millaisia merkkejä halutaan etsiä.

| Merkki | Kuvaus | Esimerkki |
|--------|--------|-----------|
| `.` | Mikä tahansa merkki (paitsi rivinvaihto) | `a.b` löytää "aab", "axb", mutta ei "ab" |
| `^` | Rivin alku | `^Hei` löytää vain "Hei maailma", mutta ei "Maailma Hei" |
| `$` | Rivin loppu | `maailma$` löytää "Hei maailma", mutta ei "maailma Hei" |
| `\d` | Numerot (0–9) | `\d+` löytää "123" |
| `\w` | Aakkosnumeerinen merkki (a-z, A-Z, 0-9, _) | `\w+` löytää "teksti_123" |
| `\|` | Tai-operaattori | `cat\|dog` löytää "cat" tai "dog" |
| `()` | Ryhmittely | `(ab)+` löytää "ab", "abab", "ababab" |
| `[]` | Merkkiluokka | `[aeiou]` löytää mitä tahansa vokaalia |
| `*` | Nolla tai useampi | `a*` löytää "", "a", "aa", "aaa" |
| `+` | Yksi tai useampi | `a+` löytää "a", "aa", "aaa" |
| `?` | Nolla tai yksi | `a?` löytää "" tai "a" |
| `{n}` | Täsmälleen n kertaa | `\d{3}` löytää täsmälleen 3 numeroa |
| `{n,m}` | Vähintään n, enintään m kertaa | `\d{2,4}` löytää 2-4 numeroa |

## C#-esimerkkejä regexin käytöstä

### 1. Etsi tietty kuvio merkkijonosta

```csharp
using System;
using System.Text.RegularExpressions;

class Program
{
    static void Main()
    {
        string input = "Minun puhelinnumeroni on 040-1234567.";
        string pattern = @"\d{3}-\d{7}";

        Match match = Regex.Match(input, pattern);

        if (match.Success)
        {
            Console.WriteLine($"Löytyi puhelinnumero: {match.Value}");
            // Tulostaa: Löytyi puhelinnumero: 040-1234567
        }
    }
}
```

### 2. Tarkista, onko annettu sähköpostiosoite kelvollinen

```csharp
using System;
using System.Text.RegularExpressions;

string email = "test@example.com";
string pattern = @"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$";

bool isValid = Regex.IsMatch(email, pattern);
Console.WriteLine(isValid ? "Sähköposti on kelvollinen" : "Virheellinen sähköposti");
```

### 3. Korvaa tietty kuvio tekstissä

```csharp
using System;
using System.Text.RegularExpressions;

string input = "Kissa juoksi kissan perässä.";
string pattern = "kissa";
string replacement = "koira";

string result = Regex.Replace(input, pattern, replacement, RegexOptions.IgnoreCase);
Console.WriteLine(result);
// Tulostaa: Koira juoksi koiran perässä.
```

### 4. Etsi kaikki osumat

```csharp
using System;
using System.Text.RegularExpressions;

string input = "Puhelinnumerot: 040-1234567, 050-9876543, 045-1112222";
string pattern = @"\d{3}-\d{7}";

MatchCollection matches = Regex.Matches(input, pattern);

foreach (Match match in matches)
{
    Console.WriteLine($"Löytyi: {match.Value}");
}
```

### 5. Ryhmittely ja ryhmien käyttö

```csharp
using System;
using System.Text.RegularExpressions;

string input = "Päivämäärät: 15.01.2024, 20.02.2024";
string pattern = @"(\d{2})\.(\d{2})\.(\d{4})";

MatchCollection matches = Regex.Matches(input, pattern);

foreach (Match match in matches)
{
    Console.WriteLine($"Koko osuma: {match.Value}");
    Console.WriteLine($"Päivä: {match.Groups[1].Value}");
    Console.WriteLine($"Kuukausi: {match.Groups[2].Value}");
    Console.WriteLine($"Vuosi: {match.Groups[3].Value}");
    Console.WriteLine();
}
```

### 6. Validoi postinumero

```csharp
using System;
using System.Text.RegularExpressions;

string[] postcodes = { "00100", "12345", "ABC12", "99999" };
string pattern = @"^\d{5}$";  // Täsmälleen 5 numeroa

foreach (string postcode in postcodes)
{
    bool isValid = Regex.IsMatch(postcode, pattern);
    Console.WriteLine($"{postcode}: {(isValid ? "Kelvollinen" : "Virheellinen")}");
}
```

### 7. Etsi sanoja tietyllä pituudella

```csharp
using System;
using System.Text.RegularExpressions;

string input = "Kissa koira hevonen lintu";
string pattern = @"\b\w{5}\b";  // Sanat, joissa on täsmälleen 5 merkkiä

MatchCollection matches = Regex.Matches(input, pattern);

foreach (Match match in matches)
{
    Console.WriteLine($"Löytyi: {match.Value}");
}
// Tulostaa: koira, lintu
```

### 8. RegexOptions-käyttö

```csharp
using System;
using System.Text.RegularExpressions;

string input = "HELLO world";
string pattern = "hello";

// Case-insensitive haku
bool match1 = Regex.IsMatch(input, pattern, RegexOptions.IgnoreCase);
Console.WriteLine($"IgnoreCase: {match1}");  // true

// Multiline-haku
string multilineInput = "Line1\nLine2\nLine3";
string multilinePattern = "^Line";
MatchCollection matches = Regex.Matches(multilineInput, multilinePattern, RegexOptions.Multiline);
Console.WriteLine($"Multiline matches: {matches.Count}");  // 3
```

## Yleisiä regex-kuvioita

### Sähköpostiosoite

```csharp
string emailPattern = @"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$";
```

### Puhelinnumero (suomalainen)

```csharp
string phonePattern = @"^(\+358|0)[0-9]{1,2}-?[0-9]{6,10}$";
```

### Postinumero (suomalainen)

```csharp
string postcodePattern = @"^\d{5}$";
```

### IP-osoite

```csharp
string ipPattern = @"^(\d{1,3}\.){3}\d{1,3}$";
```

### URL

```csharp
string urlPattern = @"^https?://[^\s/$.?#].[^\s]*$";
```

## Yhteenveto

- **Regex on tehokas tapa etsiä, suodattaa ja muokata tekstidataa.**
- **Se koostuu erikoismerkeistä ja symboleista, joiden avulla voidaan luoda monimutkaisia hakuehtoja.**
- **C#:ssa regexin käsittelyyn käytetään `System.Text.RegularExpressions` -kirjastoa.**
- **Regexiä käytetään esimerkiksi validointiin, tekstin muokkaamiseen ja tiedon hakemiseen.**
- **Regex voi olla monimutkainen, mutta se on erittäin tehokas työkalu tekstin käsittelyyn.**

## Hyödyllisiä linkkejä

- [Microsoftin Regex-dokumentaatio](https://learn.microsoft.com/en-us/dotnet/api/system.text.regularexpressions.regex)
- [Regex-testeri](https://regex101.com/) - Testaa regex-kuvioitasi verkossa

