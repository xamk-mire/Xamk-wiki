# Miten C#-koodi käännetään tietokoneelle

[Video: How C# Code Gets Compiled](https://www.youtube.com/watch?v=Ja_uXTw_Ozw)

C#-ohjelmointikieli, kuten muutkin korkean tason ohjelmointikielet, ei ole suoraan tietokoneen ymmärrettävissä. Tietokone ymmärtää vain konekieltä, joka koostuu yksinkertaisista käskyistä, jotka esitetään binaarisina eli nollina ja ykkösinä. C# kaltaiset kielet on suunniteltu helpottamaan ohjelmoijien työtä, sillä ne ovat lähempänä ihmisten luonnollista kieltä ja loogista ajattelua.

## Miten C#-koodi muuttuu tietokoneelle ymmärrettäväksi

### 1. Kääntäminen (Compilation)

Kun kirjoitat ohjelman C#:llä, se täytyy kääntää. Kääntäminen tarkoittaa prosessia, jossa ohjelmakoodi muunnetaan sellaiseksi, että tietokone voi sen suorittaa.

C#-tapauksessa kääntäjä (esim. Visual Studio) muuntaa C#-koodin ensin **välitason koodiksi** (Intermediate Language, IL), joka on vieläkin korkeammalla tasolla kuin konekieli.

### 2. JIT-kääntäminen (Just-In-Time Compilation)

Kun suoritat ohjelman, .NET Framework (tai .NET Core/.NET 5+) käyttää JIT-kääntäjää (Just-In-Time Compiler), joka muuntaa IL-koodin reaaliaikaisesti konekieleksi, jota tietokone voi suorittaa.

## Kääntämisprosessi vaiheittain

```
C#-lähdekoodi (.cs)
    ↓
[C#-kääntäjä (CSC)]
    ↓
IL-koodi (Intermediate Language) (.dll / .exe)
    ↓
[JIT-kääntäjä (Just-In-Time)]
    ↓
Konekieli (Machine Code)
    ↓
[Suoritus]
```

## Esimerkki: C#-koodi → IL-koodi

### C#-lähdekoodi

```csharp
public class Program
{
    public static void Main()
    {
        int x = 10;
        int y = 20;
        int sum = x + y;
        Console.WriteLine(sum);
    }
}
```

### Vastaava IL-koodi (yksinkertaistettu)

IL-koodi on alhaisemman tason kieltä, joka on lähempänä konekieltä mutta vielä ymmärrettävää:

```il
.method public static void Main() cil managed
{
    .entrypoint
    .maxstack 2
    .locals init (int32 x, int32 y, int32 sum)
    
    ldc.i4.s 10      // Lataa vakio 10
    stloc.0          // Tallenna muuttujaan x
    
    ldc.i4.s 20      // Lataa vakio 20
    stloc.1          // Tallenna muuttujaan y
    
    ldloc.0          // Lataa x
    ldloc.1          // Lataa y
    add              // Laske yhteen
    stloc.2          // Tallenna summaan
    
    ldloc.2          // Lataa sum
    call void [System.Console]System.Console::WriteLine(int32)
    ret              // Paluu
}
```

## Intermediate Language (IL)

Intermediate Language (IL) on tietokonekielien välitaso, jota käytetään erityisesti korkean tason ohjelmointikielistä käännettäessä. Se toimii ohjelmakoodin välivaiheena ennen kuin se käännetään suoraan konekielelle, jota suoritettava laite voi ymmärtää.

Yleisimmin käytetty esimerkki Intermediate Languagesta on Microsoftin .NET-alustassa käytettävä Common Intermediate Language (CIL). Kun ohjelmoija kirjoittaa koodia esimerkiksi C#-kielellä, koodi käännetään ensin IL-muotoon. Tämän jälkeen IL käännetään laitteistokohtaiseksi konekieleksi suorituksen aikana.

### IL:n edut

1. **Alustariippumattomuus**: Sama IL-koodi toimii eri alustoilla (Windows, Linux, macOS)
2. **Suorituskyky**: JIT-kääntäjä voi optimoida koodin kohdealustalle
3. **Turvallisuus**: IL voidaan tarkistaa ennen suoritusta

## Kääntämisen vaiheet Visual Studiossa

### 1. Build (Kääntäminen)

Kun painat **F5** tai valitset **Build → Build Solution**, Visual Studio:
1. Tarkistaa syntaksin
2. Kääntää C#-koodin IL-koodiksi
3. Luo .dll tai .exe -tiedoston

### 2. Run (Suoritus)

Kun ajat ohjelman:
1. .NET Runtime lataa IL-koodin
2. JIT-kääntäjä muuntaa IL-koodin konekieleksi
3. Konekieli suoritetaan

## Debug vs Release

### Debug-moodi

- **Optimointi**: Pois päältä
- **Symbolit**: Sisältyvät (helpottaa debuggausta)
- **Koko**: Suurempi
- **Nopeus**: Hitaampi

```csharp
// Debug-moodissa kääntäjä säilyttää enemmän tietoa
int x = 10; // Muuttuja näkyy debuggerissa
```

### Release-moodi

- **Optimointi**: Päällä
- **Symbolit**: Vähäisemmin
- **Koko**: Pienempi
- **Nopeus**: Nopeampi

```csharp
// Release-moodissa kääntäjä optimoi koodia
// Muuttujat voivat olla optimoituja pois
```

## Yhteenveto

1. **C#-koodi** kirjoitetaan ihmisen luettavassa muodossa
2. **C#-kääntäjä** muuntaa koodin **IL-koodiksi** (Intermediate Language)
3. **JIT-kääntäjä** muuntaa IL-koodin **konekieleksi** suorituksen aikana
4. **Tietokone** suorittaa konekielen

Tämä prosessi mahdollistaa sen, että voit kirjoittaa koodia korkean tason kielellä, mutta se suoritetaan tehokkaasti konekielellä.

## Hyödyllisiä linkkejä

- [.NET Compilation Overview](https://learn.microsoft.com/en-us/dotnet/core/introduction)
- [Common Intermediate Language (CIL)](https://learn.microsoft.com/en-us/dotnet/standard/managed-code)

Seuraavaksi: [Luokat ja Objektit](../01-Introduction/Classes-and-Objects.md)

