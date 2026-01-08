# Access Modifiers (Käyttöoikeusmääreet)

[Microsoftin virallinen dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers)

C#:ssa access modifierit ovat avainsanoja, joita käytetään määrittämään luokkien, metodien ja muiden jäsenten näkyvyys. Ne hallitsevat, mistä näitä jäseniä voidaan käyttää, ja niillä on keskeinen rooli datan kapseloinnissa ja suojauksessa.

## Access Modifierit

### 1. Public

`public`-määre sallii pääsyn luokan jäseneen mistä tahansa koodista samassa assemblyssä tai toisessa assemblyssä, joka viittaa siihen. Esimerkiksi julkinen luokka tai metodi voidaan käyttää mistä tahansa ohjelman osasta.

```csharp
public class PublicClass
{
    public string Name { get; set; }
    public void PublicMethod()
    {
        Console.WriteLine("Tämä metodi on julkinen");
    }
}

// Käyttö mistä tahansa
PublicClass obj = new PublicClass();
obj.Name = "Test";
obj.PublicMethod();
```

**Reaalimaailman analogia**: Julkinen kirjasto. Kuka tahansa voi mennä sisään ja käyttää sen resursseja.

### 2. Private

`private`-määre rajoittaa pääsyn luokan jäseneen vain luokkaan itseensä. Se on rajoittunein näkyvyystaso ja sitä käytetään kapseloimaan luokan sisäisiä toimintoja. Esimerkiksi yksityinen kenttä tai metodi ei ole käytettävissä sen sisältävän luokan ulkopuolelta.

```csharp
public class MyClass
{
    private string secret;  // Näkyy vain tämän luokan sisällä
    
    private void PrivateMethod()
    {
        Console.WriteLine("Tämä on yksityinen metodi");
    }
    
    public void PublicMethod()
    {
        secret = "Salaisuus";  // OK: pääsy private-kenttään luokan sisällä
        PrivateMethod();        // OK: pääsy private-metodiin luokan sisällä
    }
}

// Käyttö
MyClass obj = new MyClass();
// obj.secret = "Test";        // VIRHE: private ei näy ulkopuolella
// obj.PrivateMethod();        // VIRHE: private ei näy ulkopuolella
obj.PublicMethod();            // OK: public metodi näkyy
```

**Reaalimaailman analogia**: Henkilökohtainen päiväkirja. Vain sinä voit lukea ja kirjoittaa siihen.

### 3. Protected

`protected`-määre sallii luokan jäsenen olla käytettävissä luokan sisällä ja johdetuissa luokissa. Tämä tarkoittaa, että jos sinulla on perusluokka, jossa on suojattu jäsen, mikä tahansa aliluokka voi käyttää sitä jäsentä, mutta muut luokat (jotka eivät ole aliluokkia) eivät voi.

```csharp
public class BaseClass
{
    protected int protectedField = 10;
    
    protected void ProtectedMethod()
    {
        Console.WriteLine("Tämä on suojattu metodi");
    }
}

public class DerivedClass : BaseClass
{
    public void UseProtected()
    {
        Console.WriteLine(protectedField);  // OK: pääsy protected-kenttään
        ProtectedMethod();                   // OK: pääsy protected-metodiin
    }
}

// Käyttö
DerivedClass derived = new DerivedClass();
derived.UseProtected();  // OK
// derived.protectedField = 20;  // VIRHE: protected ei näy ulkopuolella
```

**Reaalimaailman analogia**: Perheen perintöesine kotona. Se on saatavilla sinulle ja perheenjäsenillesi, mutta ei ulkopuolisille.

### 4. Internal

`internal`-määre rajoittaa pääsyn jäseniin saman assemblyn sisällä. Tämä on hyödyllistä, kun haluat sallia pääsyn tiettyihin kirjaston osiin saman kirjaston muissa osissa, mutta et ulkopuolella.

```csharp
// Projektissa A
internal class InternalClass
{
    internal void InternalMethod()
    {
        Console.WriteLine("Tämä on sisäinen metodi");
    }
}

public class PublicClass
{
    public void UseInternal()
    {
        InternalClass obj = new InternalClass();  // OK: samassa projektissa
        obj.InternalMethod();
    }
}

// Projektissa B (viittaa projektiin A)
// InternalClass ja InternalMethod eivät ole näkyvissä
```

**Reaalimaailman analogia**: Toimistorakennus, jossa vain yrityksen työntekijät voivat mennä tiettyihin alueisiin.

### 5. Protected Internal

Tämä `protected`- ja `internal`-yhdistelmä sallii pääsyn jäseneen mistä tahansa luokasta samassa assemblyssä tai mistä tahansa johdetusta luokasta missä tahansa assemblyssä. Se on vähemmän yleinen, mutta hyödyllinen tietyissä skenaarioissa, joissa tarvitset laajemman pääsyn kuin `internal`, mutta rajoitetumman kuin `public`.

```csharp
public class BaseClass
{
    protected internal int protectedInternalField = 10;
}

// Samassa projektissa
public class SameProjectClass
{
    public void UseProtectedInternal()
    {
        BaseClass obj = new BaseClass();
        obj.protectedInternalField = 20;  // OK: samassa projektissa
    }
}

// Eri projektissa, mutta perii BaseClassin
public class DerivedClass : BaseClass
{
    public void UseProtectedInternal()
    {
        protectedInternalField = 30;  // OK: johdettu luokka
    }
}
```

**Reaalimaailman analogia**: Yhteisökeskus, jossa kaikki paikalliset asukkaat ja tiettyjen yhteisöjen jäsenet (riippumatta asuinpaikasta) voivat mennä sisään.

### 6. Private Protected

C# 7.2:ssa esitelty tämä yhdistelmä `private`- ja `protected`-määreistä sallii pääsyn vain sisältävän luokan sisällä tai johdetussa luokassa samassa assemblyssä. Se on rajoittuneampi kuin `protected internal`.

```csharp
public class BaseClass
{
    private protected int privateProtectedField = 10;
}

// Samassa projektissa ja perii BaseClassin
public class DerivedClass : BaseClass
{
    public void UsePrivateProtected()
    {
        privateProtectedField = 20;  // OK: johdettu luokka samassa projektissa
    }
}
```

**Reaalimaailman analogia**: Yksityinen perhetapahtuma paikallisessa yhteisöhallissa. Vain perheesi (johdettu luokka) ja tietty yhteisö (sama assembly) voivat osallistua.

## Oletusnäkyvyys

### Luokat

- **Ei määreitä**: `internal` (näkyy vain samassa projektissa)
- **Nested luokat** (sisäluokat): `private` (näkyy vain ulomman luokan sisällä)

```csharp
// Oletuksena internal
class DefaultClass  // Sama kuin: internal class DefaultClass
{
}

// Nested luokka on oletuksena private
public class OuterClass
{
    class NestedClass  // Sama kuin: private class NestedClass
    {
    }
}
```

### Luokan jäsenet

- **Kentät ja metodit**: `private` (näkyvät vain luokan sisällä)

```csharp
public class MyClass
{
    int field;           // Sama kuin: private int field;
    void Method()        // Sama kuin: private void Method()
    {
    }
}
```

## Yhteenveto

Access modifierit ovat keskeinen osa C#:n kapselointia ja ne auttavat varmistamaan, että koodin osat ovat saatavilla vain siellä, missä niitä tarvitaan. Oikea access modifierin valinta parantaa koodin turvallisuutta, ylläpidettävyyttä ja selkeyttä.

| Access Modifier | Näkyvyys |
|----------------|----------|
| `public` | Kaikkialla |
| `private` | Vain luokan sisällä |
| `protected` | Luokan sisällä ja johdetuissa luokissa |
| `internal` | Saman assemblyn/projektin sisällä |
| `protected internal` | Saman assemblyn sisällä TAI johdetuissa luokissa |
| `private protected` | Vain luokan sisällä TAI johdetuissa luokissa samassa assemblyssä |

