# OOP-konseptit (Object-Oriented Programming)

Tervetuloa olio-ohjelmoinnin (OOP) syvälliseen tutustumiseen! Tämä osio käsittelee kaikki keskeiset OOP-konseptit, jotka ovat välttämättömiä modernin ohjelmistokehityksen hallitsemiseksi.

## Mikä on OOP?

**Olio-ohjelmointi (OOP)** on ohjelmointiparadigma, joka organisoi koodin **objektien** ja **luokkien** ympärille. Se on yksi eniten käytetyistä paradigmoista modernissa ohjelmistokehityksessä, ja se on C#:n ytimessä.

### OOP:n neljä pilaria:
1. **Kapselointi** - Datan piilottaminen ja suojaaminen
2. **Perintä** - Koodin uudelleenkäyttö luokka hierarchioiden avulla
3. **Polymorfismi** - Yhtenäinen käsittely eri objekteille
4. **Abstraktio** - Monimutkaisten yksityiskohtien piilottaminen

## Sisältö

### Aloita tästä:
0. **[OOP-tekniikat - Yleiskuvaus](OOP-Techniques-Overview.md)**  
   Nopea katsaus kaikkiin tekniikoihin - aloita tästä saadaksesi kokonaiskuvan!

### OOP:n neljä pilaria:

1. **[Kapselointi (Encapsulation)](Encapsulation.md)**
   - Datan ja metodien yhdistäminen
   - Tietoturva ja validointi
   - Properties ja access modifiers
   - Information hiding

2. **[Perintä (Inheritance)](Inheritance.md)**
   - Luokkien hierarkiat
   - Koodin uudelleenkäyttö
   - virtual, override, base-avainsanat
   - Milloin käyttää ja milloin välttää

3. **[Polymorfismi (Polymorphism)](Polymorphism.md)**
   - Compile-time polymorfismi (overloading)
   - Runtime polymorfismi (overriding)
   - Abstract luokat
   - Yhtenäinen käsittely

4. **[Rajapinnat (Interfaces)](Interfaces.md)**
   - Sopimukset luokkien välillä
   - Moniperintä rajapinnoilla
   - Dependency Injection
   - Interface Segregation

### Lisätekniikat:

5. **[Yhdistäminen (Composition)](Composition.md)**
   - "Has-a" vs. "Is-a" suhteet
   - Composition over Inheritance
   - Aggregation vs. Composition
   - Modulaarinen suunnittelu

## Oppimisjärjestys

Suosittelemme opiskelua **tässä järjestyksessä**, koska jokainen konsepti rakentuu edellisen päälle:

### Vaihe 1: Perusta (Aloita tästä!)
**[OOP-tekniikat - Yleiskuvaus](OOP-Techniques-Overview.md)**  
↓  
Saat nopean käsityksen kaikista tekniikoista

### Vaihe 2: Peruspilarit (Opiskele järjestyksessä)
1. **[Kapselointi](Encapsulation.md)** - Perusta kaikelle  
   *Miksi?* Opettaa datan suojaamisen ja luokkien suunnittelun perusteet

2. **[Perintä](Inheritance.md)** - Rakenna hierarkioita  
   *Miksi?* Ymmärrät koodin uudelleenkäytön perusteet

3. **[Polymorfismi](Polymorphism.md)** - Joustava käsittely  
   *Miksi?* Vaatii perinnän ymmärtämistä

4. **[Rajapinnat](Interfaces.md)** - Sopimukset  
   *Miksi?* Rakentuu polymorfismin päälle

5. **[Yhdistäminen](Composition.md)** - Vaihtoehtoja perinnälle  
   *Miksi?* Ymmärrät milloin käyttää perintää ja milloin yhdistämistä

### Vaihe 3: Syventyminen
Kun hallitset perusteet, jatka:
- **[Design Principles](../04-Advanced/Design-Principles.md)** - SOLID-periaatteet
- **[Design Patterns](../04-Advanced/Design-Patterns.md)** - Suunnittelumallit

## Nopea vertailu tekniikoista

| Tekniikka | Tarkoitus | Milloin käyttää | Esimerkki |
|-----------|-----------|-----------------|-----------|
| **Kapselointi** | Suojaa dataa | Aina! | `private` kentät, `public` propertyt |
| **Perintä** | Koodin uudelleenkäyttö | "Is-a" suhteet | `Dog : Animal` |
| **Polymorfismi** | Yhtenäinen käsittely | Eri objektit samalla tavalla | `Animal[]` sisältää `Dog` ja `Cat` |
| **Rajapinnat** | Sopimukset | "Can-do" suhteet | `IFlyable`, `ISwimmable` |
| **Yhdistäminen** | Modulaarisuus | "Has-a" suhteet | `Car` sisältää `Engine` |

## Käytännön vinkkejä

### ✅ Hyvät käytännöt:
- **Aloita kapseloinnista** - Käytä aina `private` kenttiä ja `public` propertyjä
- **Suosi composition over inheritance** - Yhdistäminen on usein joustavampi kuin perintä
- **Käytä rajapintoja** - Ne tekevät koodista testattavampaa ja joustavampaa
- **Pidä luokat pieniä** - Single Responsibility Principle
- **Käytä polymorfismia** - Vältä tyyppitarkistuksia (`is`, `as`)

### ❌ Yleisiä virheitä:
- Julkiset kentät (`public` fields)
- Liian syvälle menevä perintähierarkia (> 3 tasoa)
- Perintä kun yhdistäminen olisi parempi
- "God Objects" - luokat jotka tekevät liikaa
- Rajapintojen rikkominen muutoksilla

## Miksi OOP?

### Hyödyt:
1. **Modulaarisuus** - Koodi on jaoteltu loogisiin osiin
2. **Uudelleenkäytettävyys** - DRY (Don't Repeat Yourself)
3. **Ylläpidettävyys** - Helppo ymmärtää ja muokata
4. **Laajennettavuus** - Uusia ominaisuuksia helppo lisätä
5. **Testattavuus** - Yksikkötestit helpompia
6. **Abstraktio** - Piilottaa monimutkaisuuden

### Todellisen maailman analogia:
```
Auto (luokka)
├── Moottori (kapselointi - sisäinen toiminta piilotettu)
├── Rengas (yhdistäminen - auto koostuu osista)
├── Perintä: Katumaasturi perii Auton
└── Rajapinta: IDriveable (auto voi ajaa)
```

## Resurssit

### Dokumentaatio:
- [Microsoft C# OOP dokumentaatio](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/tutorials/oop)
- [C# Programming Guide](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/)

### Kirjat:
- **"Head First Object-Oriented Analysis and Design"** - Rebecca Riordan
- **"Object-Oriented Programming in C#"** - Simon Kendal
- **"C# 12 and .NET 8 – Modern Cross-Platform Development"** - Mark J. Price

### Videot:
- [Microsoft Learn: C# OOP](https://learn.microsoft.com/en-us/training/paths/csharp-object-oriented-programming/)


OOP ei ole vain syntaksia - se on **ajattelutapa**. Se opettaa:
- Miten organisoida koodia loogisesti
- Miten rakentaa ylläpidettäviä järjestelmiä
- Miten välttää yleisiä sudenkuoppia
- Miten tehdä koodista joustavaa ja laajennettavaa

**Seuraava askel:** Aloita [OOP-tekniikat - Yleiskuvaus](OOP-Techniques-Overview.md) sivusta saadaksesi kokonaiskuvan, ja jatka sitten järjestyksessä [Kapselointi](Encapsulation.md) → [Perintä](Inheritance.md) → [Polymorfismi](Polymorphism.md) → [Rajapinnat](Interfaces.md) → [Yhdistäminen](Composition.md).

---


