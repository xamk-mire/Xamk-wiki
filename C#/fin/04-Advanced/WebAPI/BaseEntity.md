# BaseEntity — Yhteiset kentät ja automaattiset aikaleimat

## Sisällysluettelo

1. [Miksi yhteinen kantaluokka?](#miksi-yhteinen-kantaluokka)
2. [BaseEntity-luokka](#baseentity-luokka)
3. [Periminen — entiteetti perii BaseEntityn](#periminen---entiteetti-perii-baseentityn)
4. [SaveChangesAsync-ylikirjoitus](#savechangesasync-ylikirjoitus)
5. [ChangeTracker ja EntityState](#changetracker-ja-entitystate)
6. [Yhteenveto](#yhteenveto)

---

## Miksi yhteinen kantaluokka?

Kun sovelluksessa on useampi entiteetti, huomaat nopeasti, että jokaisella on samat peruskentät:

```csharp
public class Product
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    // ... tuotekohtaiset kentät
}

public class Category
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
    // ... kategoriakohtaiset kentät
}
```

`Id`, `CreatedAt` ja `UpdatedAt` toistuvat **jokaisessa luokassa**. Tämä rikkoo **DRY-periaatetta** (Don't Repeat Yourself): jos haluat lisätä yhteisen kentän (esim. `CreatedBy`), joudut muuttamaan jokaisen entiteetin erikseen.

Ratkaisu: luodaan **yksi kantaluokka** (`BaseEntity`), josta kaikki entiteetit perivät yhteiset kentät.

---

## BaseEntity-luokka

```csharp
public abstract class BaseEntity
{
    public int Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime? UpdatedAt { get; set; }
}
```

### Kentät

| Kenttä | Tyyppi | Tarkoitus |
|--------|--------|-----------|
| `Id` | `int` | Yksilöivä tunniste (primary key) — EF Core tunnistaa `Id`-nimisen kentän automaattisesti |
| `CreatedAt` | `DateTime` | Milloin rivi luotiin tietokantaan |
| `UpdatedAt` | `DateTime?` | Milloin riviä viimeksi muutettiin — `null` jos ei ole vielä muutettu |

### Miksi `abstract`?

`abstract`-avainsana tarkoittaa, että `BaseEntity`-luokasta **ei voi luoda olioita suoraan**:

```csharp
var entity = new BaseEntity();  // ❌ Käännösvirhe — abstract-luokkaa ei voi instansoida
var product = new Product();    // ✅ Product perii BaseEntityn ja sitä voi käyttää
```

`BaseEntity` on tarkoitettu **vain kantaluokaksi** — se ei edusta mitään konkreettista tietokantataulua.

### Miksi `CreatedAt` ja `UpdatedAt`?

Nämä kentät ovat hyödyllisiä lähes kaikissa sovelluksissa:

- **`CreatedAt`** — lajittelu ("uusimmat ensin"), auditointi ("milloin tämä data syntyi?"), debuggaus
- **`UpdatedAt`** — muutoshistorian seuraaminen, välimuistin hallinta (cache invalidation), debuggaus

Ilman aikaleimakenttiä et pysty jälkikäteen selvittämään, milloin data on luotu tai muuttunut.

> **`int Id` vs. `Guid Id`**
>
> Tässä käytämme `int Id`:tä yksinkertaisuuden vuoksi. Tuotantosovelluksissa `Guid` on usein parempi valinta, koska se on maailmanlaajuisesti yksilöllinen eikä riipu tietokannan laskurista. `Guid` on kuitenkin edistynyt aihe.

---

## Periminen — entiteetti perii BaseEntityn

Kun `BaseEntity` on olemassa, entiteetit perivät siitä C#:n perintämekanismilla (`:` -merkki):

```csharp
public class Product : BaseEntity
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
}
```

`Product` saa nyt **automaattisesti** kentät `Id`, `CreatedAt` ja `UpdatedAt` — niitä ei tarvitse kirjoittaa uudelleen.

Uuden entiteetin lisääminen on yhtä helppoa:

```csharp
public class Category : BaseEntity
{
    public string Name { get; set; } = string.Empty;
}
```

`Category` saa samat yhteiset kentät ilman yhtään toistoa.

---

## SaveChangesAsync-ylikirjoitus

`CreatedAt` ja `UpdatedAt` pitäisi asettua **automaattisesti** — ilman, että kehittäjän tarvitsee muistaa tehdä se jokaisessa controllerissa tai servicessä. Tämä onnistuu ylikirjoittamalla EF Coren `SaveChangesAsync`-metodi `DbContext`:issa.

```csharp
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options) { }

    public DbSet<Product> Products { get; set; }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        var now = DateTime.UtcNow;

        foreach (var entry in ChangeTracker.Entries<BaseEntity>())
        {
            if (entry.State == EntityState.Added)
                entry.Entity.CreatedAt = now;

            if (entry.State == EntityState.Modified)
                entry.Entity.UpdatedAt = now;
        }

        return await base.SaveChangesAsync(cancellationToken);
    }
}
```

### Mitä tapahtuu?

1. **`ChangeTracker.Entries<BaseEntity>()`** — hakee kaikki entiteetit, jotka perivät `BaseEntity`:n ja joita ollaan tallentamassa
2. **`EntityState.Added`** — rivi on uusi → asetetaan `CreatedAt`
3. **`EntityState.Modified`** — riviä on muutettu → asetetaan `UpdatedAt`
4. **`DateTime.UtcNow`** — UTC-aika on aikavyöhykkeestä riippumaton ja suositeltava valinta palvelinsovelluksissa
5. **`base.SaveChangesAsync()`** — kutsuu EF Coren alkuperäistä tallennuslogiikkaa

Tämän ansiosta aikaleimat asettuvat **automaattisesti yhdessä paikassa** — riippumatta siitä, kutsuuko `SaveChangesAsync`:ia controller, service vai mikä tahansa muu osa koodia.

---

## ChangeTracker ja EntityState

EF Coren **ChangeTracker** seuraa kaikkien ladattujen entiteettien tilaa. Jokaisella entiteetillä on tila (`EntityState`), joka kertoo mitä sille on tapahtunut:

| EntityState | Merkitys | Mitä EF Core tekee? |
|-------------|----------|---------------------|
| `Added` | Uusi entiteetti lisätty (`_context.Products.Add(...)`) | `INSERT INTO` |
| `Modified` | Olemassa olevan entiteetin kenttää muutettu | `UPDATE` |
| `Deleted` | Entiteetti poistettu (`_context.Products.Remove(...)`) | `DELETE FROM` |
| `Unchanged` | Ladattu tietokannasta, ei muutoksia | Ei SQL-operaatiota |
| `Detached` | Ei seurannassa | Ei SQL-operaatiota |

`SaveChangesAsync`-ylikirjoituksessa hyödynnämme tilaa selvittääksemme, onko rivi uusi (`Added`) vai muokattu (`Modified`), ja asetamme aikaleiman sen mukaan.

### Esimerkki: mitä tapahtuu kulissien takana

```csharp
// 1. Luodaan uusi tuote
var product = new Product { Name = "Kahvi", Price = 3.50m };
_context.Products.Add(product);
// → ChangeTracker: product.State = EntityState.Added

// 2. Kutsutaan SaveChangesAsync
await _context.SaveChangesAsync();
// → Ylikirjoitus asettaa: product.CreatedAt = DateTime.UtcNow
// → EF Core generoi: INSERT INTO Products (Name, Price, CreatedAt) VALUES ...
```

```csharp
// 1. Haetaan olemassa oleva tuote
var product = await _context.Products.FindAsync(1);
// → ChangeTracker: product.State = EntityState.Unchanged

// 2. Muutetaan kenttää
product.Price = 4.00m;
// → ChangeTracker: product.State = EntityState.Modified

// 3. Kutsutaan SaveChangesAsync
await _context.SaveChangesAsync();
// → Ylikirjoitus asettaa: product.UpdatedAt = DateTime.UtcNow
// → EF Core generoi: UPDATE Products SET Price = 4.00, UpdatedAt = ... WHERE Id = 1
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **BaseEntity** | Abstrakti kantaluokka, joka sisältää yhteiset kentät (`Id`, `CreatedAt`, `UpdatedAt`) |
| **`abstract`** | Luokasta ei voi luoda instanssia — vain periminen on sallittu |
| **Periminen (`:`)** | `Product : BaseEntity` — Product saa kaikki BaseEntityn kentät automaattisesti |
| **DRY-periaate** | Yhteiset kentät yhdessä paikassa, ei kopioita jokaisessa entiteetissä |
| **ChangeTracker** | EF Coren mekanismi, joka seuraa entiteettien muutoksia |
| **EntityState** | Kertoo onko entiteetti `Added`, `Modified`, `Deleted`, `Unchanged` vai `Detached` |
| **SaveChangesAsync-ylikirjoitus** | Asettaa `CreatedAt`/`UpdatedAt` automaattisesti ennen tallennusta |
| **`DateTime.UtcNow`** | Aikavyöhykkeestä riippumaton aika — suositeltava palvelinsovelluksissa |

### Seuraavaksi

- [Entity Framework Core](Entity-Framework.md) — DbContext, DbSet ja migraatiot
- [DTO:t ja Mapping](DTOs-and-Mapping.md) — API-rajapinnan erottaminen tietokannasta
- [Service-kerros ja DI](Services-and-DI.md) — Liiketoimintalogiikan erottaminen controllerista
