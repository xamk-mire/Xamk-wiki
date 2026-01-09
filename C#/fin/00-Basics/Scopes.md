# Näkyvyysalueet (Scopes)

C#:ssa on useita erilaisia scopeja eli näkyvyysalueita, jotka määrittävät, missä muuttujia, metodeja ja muita jäseniä voidaan käyttää. Näkyvyysalueet ovat tärkeitä, koska ne auttavat hallitsemaan pääsyä koodin osiin ja parantavat koodin turvallisuutta ja ylläpidettävyyttä.

## Scope-tyypit

### 1. Lokaali scope

Lokaali scope rajoittuu yhteen metodiin tai lohkoon (esim. `if`-lausetta tai silmukkaa käytettäessä). Lokaalit muuttujat ovat käytettävissä vain siinä metodissa tai lohkossa, jossa ne on määritelty. Ne eivät ole käytettävissä metodin tai lohkon ulkopuolella.

```csharp
public void ExampleMethod()
{
    int localVariable = 10;  // Lokaali muuttuja
    
    if (true)
    {
        int blockVariable = 20;  // Lohkon sisäinen muuttuja
        Console.WriteLine(localVariable);  // OK: pääsy lokaaliin muuttujaan
        Console.WriteLine(blockVariable);   // OK: pääsy lohkon muuttujaan
    }
    
    // Console.WriteLine(blockVariable);  // VIRHE: blockVariable ei ole näkyvissä
}

// Console.WriteLine(localVariable);  // VIRHE: localVariable ei ole näkyvissä
```

### 2. Luokan jäsenen scope

Tämä scope koskee muuttujia ja metodeja, jotka on määritelty luokan tasolla. Näitä jäseniä voidaan kutsua minkä tahansa luokan instanssin (eli olion) kautta tai staattisesti, jos jäsen on määritelty staattiseksi. Pääsy näihin jäseniin riippuu niiden määrittelyistä käyttöoikeuksista (kuten `public`, `private` jne.).

```csharp
public class MyClass
{
    private int privateField = 10;      // Näkyy vain luokan sisällä
    public int publicField = 20;        // Näkyy kaikkialle
    internal int internalField = 30;   // Näkyy saman assemblyn sisällä
    
    public void PublicMethod()
    {
        Console.WriteLine(privateField);  // OK: pääsy private-kenttään
        Console.WriteLine(publicField);   // OK: pääsy public-kenttään
    }
    
    private void PrivateMethod()
    {
        Console.WriteLine(privateField);  // OK: pääsy private-kenttään
    }
}

// Käyttö
MyClass obj = new MyClass();
// Console.WriteLine(obj.privateField);  // VIRHE: private ei näy ulkopuolella
Console.WriteLine(obj.publicField);      // OK: public näkyy
obj.PublicMethod();                      // OK: public metodi näkyy
// obj.PrivateMethod();                  // VIRHE: private metodi ei näy
```

### 3. Namespace scope

Namespacet eli nimiavaruudet tarjoavat tavan ryhmitellä luokkia ja muita tietotyyppejä. Namespace-scope sallii jäsenten käytön saman nimiavaruuden sisällä ilman, että niitä täytyy erikseen tuoda esiin. Jäsenten käyttö eri nimiavaruuksista vaatii `using`-direktiivin tai täysin kelpaavan nimen.

```csharp
namespace MyNamespace
{
    public class ClassA
    {
        public void MethodA() { }
    }
    
    public class ClassB
    {
        public void MethodB()
        {
            ClassA a = new ClassA();  // OK: samassa namespace:ssä
            a.MethodA();
        }
    }
}

namespace AnotherNamespace
{
    using MyNamespace;  // Tuodaan MyNamespace käyttöön
    
    public class ClassC
    {
        public void MethodC()
        {
            ClassA a = new ClassA();  // OK: using-direktiivin ansiosta
            // TAI täydellä nimellä:
            MyNamespace.ClassA a2 = new MyNamespace.ClassA();
        }
    }
}
```

### 4. Assembly scope

Assembly (kokoonpano/projekti) on yksi tai useampi tiedosto, joka muodostaa sovelluksen tai kirjaston .NET:ssä. Assembly-scope määrittää, mitkä luokat, metodit ja muut jäsenet ovat näkyvissä muille kokoonpanoille. Tämä näkyvyys määritellään `internal`-avainsanalla, joka sallii jäsenten käytön vain saman kokoonpanon sisällä.

```csharp
// Projektissa A
public class PublicClass
{
    public void PublicMethod() { }
    internal void InternalMethod() { }  // Näkyy vain samassa projektissa
}

internal class InternalClass  // Näkyy vain samassa projektissa
{
    public void Method() { }
}

// Projektissa B (viittaa projektiin A)
// PublicClass ja PublicMethod ovat näkyvissä
// InternalMethod ja InternalClass eivät ole näkyvissä
```

## Scopejen vertailu

| Scope-tyyppi | Näkyvyysalue | Esimerkki |
|--------------|--------------|-----------|
| **Lokaali** | Metodi tai lohko | `int x = 10;` metodin sisällä |
| **Luokan jäsen** | Luokan sisällä (riippuen access modifierista) | `private int field;` |
| **Namespace** | Saman namespace:n sisällä | Luokat samassa `namespace`-lohkossa |
| **Assembly** | Saman projektin/assemblyn sisällä | `internal`-avainsana |

## Yhteenveto

Näiden scopejen väliset erot liittyvät pääasiassa siihen, missä ja miten muuttujia ja metodeja voidaan käyttää. Lokaali scope on rajoittunein, kun taas namespace- ja assembly-scope tarjoavat laajempia näkyvyysalueita. Luokan jäsenen scope puolestaan sallii muuttujien ja metodien käytön luokan instansseissa, riippuen määritellyistä käyttöoikeuksista.

Scopejen oikea ymmärtäminen on tärkeää turvallisen ja ylläpidettävän koodin kirjoittamiseen, koska ne auttavat varmistamaan, että koodin osat ovat saatavilla vain siellä, missä niitä tarvitaan.

