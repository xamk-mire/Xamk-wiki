# Entity Framework Core — Tietokannan käyttö .NET:ssä

## Sisällysluettelo

1. [Mikä on ORM?](#mikä-on-orm)
2. [Mikä on Entity Framework Core?](#mikä-on-entity-framework-core)
3. [Entiteetti — tietokantataulun malli](#entiteetti---tietokantataulun-malli)
4. [DbContext — yhteys tietokantaan](#dbcontext---yhteys-tietokantaan)
5. [DbSet — taulun edustaja koodissa](#dbset---taulun-edustaja-koodissa)
6. [Migraatiot](#migraatiot)
7. [Async-metodit](#async-metodit)
8. [Rekisteröinti Program.cs:ssä](#rekisteröinti-programcsssä)
9. [CRUD tietokannalla](#crud-tietokannalla)
10. [Tietokannan valinta](#tietokannan-valinta)
11. [Yhteenveto](#yhteenveto)

---

## Mikä on ORM?

**ORM** (Object-Relational Mapper) on kirjasto, joka **muuntaa C#-luokat tietokantatauluiksi** — ja toisin päin. Ilman ORM:ia pitäisi kirjoittaa SQL-kyselyjä käsin.

```
Ilman ORM:ia (SQL käsin):
──────────────────────────────────────────────────────────
string sql = "SELECT * FROM Products WHERE Id = @id";
using var cmd = new SqlCommand(sql, connection);
cmd.Parameters.AddWithValue("@id", id);
var reader = cmd.ExecuteReader();
// ... manuaalinen muuntaminen C#-olioksi

ORM:n kanssa (EF Core):
──────────────────────────────────────────────────────────
var product = await _context.Products.FindAsync(id);
// Valmis — EF Core hoitaa SQL:n automaattisesti
```

**ORM:n hyödyt:**

| Ilman ORM | ORM:n kanssa |
|-----------|--------------|
| SQL-kyselyt käsin | EF Core generoi SQL:n |
| Manuaalinen muunnos C#-olioksi | Automaattinen muunnos |
| Eri koodi eri tietokannoille | Sama koodi, vaihda vain provider |
| Helposti SQL injection -haavoittuvuus | Parameterized queries automaattisesti |

---

## Mikä on Entity Framework Core?

**Entity Framework Core** (EF Core) on Microsoftin ORM-kirjasto .NET:lle. Se on osa ASP.NET Core -ekosysteemiä ja yleisin tapa käsitellä tietokantaa .NET-projekteissa.

EF Core tukee monia tietokantoja:

| Tietokanta | NuGet-paketti |
|------------|---------------|
| **SQLite** | `Microsoft.EntityFrameworkCore.Sqlite` |
| **SQL Server** | `Microsoft.EntityFrameworkCore.SqlServer` |
| **PostgreSQL** | `Npgsql.EntityFrameworkCore.PostgreSQL` |
| **MySQL** | `Pomelo.EntityFrameworkCore.MySql` |
| **In-Memory** (testaus) | `Microsoft.EntityFrameworkCore.InMemory` |

> **Kehityksessä käytetään yleensä SQLiteä** — se on tiedostopohjainen tietokanta, joka ei vaadi erillistä palvelinta. Tuotannossa vaihdetaan SQL Serveriin tai PostgreSQL:ään.

---

## Entiteetti — tietokantataulun malli

**Entiteetti** (entity) on C#-luokka, joka kuvaa yhtä tietokantataulua. Se näyttää samalta kuin tavallinen model-luokka:

```csharp
public class Product
{
    public int Id { get; set; }           // Ensisijaisavain (primary key)
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public string? Description { get; set; }
}
```

EF Core tunnistaa automaattisesti:
- `Id`-nimisen kentän **ensisijaisavaimeksi** (primary key)
- `string`-kentät `NULL`-sallittaviksi tietokannassa
- `string?`-kentät (nullable) `NULL`-sallittaviksi

### Taulun nimeäminen

Oletuksena EF Core käyttää `DbSet`-ominaisuuden nimeä taulun nimenä (esim. `Products`). Nimeä voi muuttaa attribuutilla:

```csharp
[Table("tuotteet")]
public class Product { ... }
```

---

## DbContext — yhteys tietokantaan

**DbContext** on luokka, joka edustaa **yhteyttä tietokantaan**. Se on ikään kuin portti, jonka kautta kaikki tietokantaoperaatiot tehdään.

```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options)
        : base(options)
    {
    }

    // Jokainen DbSet vastaa yhtä tietokantataulua
    public DbSet<Product> Products { get; set; }
    public DbSet<Category> Categories { get; set; }
}
```

### Mitä DbContext tekee?

- Pitää kirjaa siitä, mitä entiteettejä on haettu, lisätty tai muutettu (**Change Tracking**)
- Generoi ja ajaa SQL-kyselyt automaattisesti
- Hallinnoi tietokantayhteyttä

---

## DbSet — taulun edustaja koodissa

**DbSet** edustaa yhtä tietokantataulua. Se tarjoaa metodit CRUD-operaatioihin:

```csharp
// Haku
_context.Products.ToListAsync()           // SELECT * FROM Products
_context.Products.FindAsync(id)           // SELECT * FROM Products WHERE Id = @id
_context.Products.FirstOrDefaultAsync(p => p.Name == "Kahvi")

// Lisäys
_context.Products.Add(product)            // INSERT INTO Products ...
// tai
await _context.Products.AddAsync(product)

// Poisto
_context.Products.Remove(product)         // DELETE FROM Products WHERE Id = @id

// Haku ehdolla
_context.Products
    .Where(p => p.Price > 10)
    .ToListAsync()                         // SELECT * FROM Products WHERE Price > 10

// Tallenna muutokset tietokantaan
await _context.SaveChangesAsync()
```

> **Tärkeää:** `Add()` ja `Remove()` eivät heti muuta tietokantaa. Muutokset tallennetaan vasta kun kutsutaan `SaveChangesAsync()`.

---

## Migraatiot

**Migraatiot** (migrations) ovat EF Coren tapa pitää tietokannan rakenne synkronoituna koodin kanssa. Kun muutat entiteettiluokkaa, luot uuden migraation, joka päivittää tietokannan.

### Migraatiotyönkulku

```
1. Muutat C#-luokkaa (lisäät kentän, luokat uuden entiteetin...)
       ↓
2. Luot migraation: dotnet ef migrations add NimiMigraaatiolle
       ↓
3. EF Core generoi migraatiotiedoston (C#-koodi SQL-muutoksista)
       ↓
4. Ajat migraation: dotnet ef database update
       ↓
5. Tietokanta päivittyy
```

### Komennot

Ensin asenna EF Core Tools (kerran):

```bash
dotnet tool install --global dotnet-ef
```

Migraatiokomennot:

```bash
# Luo uusi migraatio (kun muutat entiteettejä)
dotnet ef migrations add InitialCreate

# Aja migraatiot (päivitä tietokanta)
dotnet ef database update

# Listaa kaikki migraatiot
dotnet ef migrations list

# Peru viimeisin migraatio (ennen kuin se on ajettu)
dotnet ef migrations remove

# Nollaa tietokanta takaisin tiettyyn migraatioon
dotnet ef database update MigraationNimi
```

### Migraatiotiedosto

Kun luot migraation, EF Core generoi automaattisesti tiedoston `Migrations/`-kansioon:

```csharp
// Migrations/20240301120000_InitialCreate.cs (generoitu automaattisesti)
public partial class InitialCreate : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.CreateTable(
            name: "Products",
            columns: table => new
            {
                Id = table.Column<int>(nullable: false)
                    .Annotation("Sqlite:Autoincrement", true),
                Name = table.Column<string>(nullable: false),
                Price = table.Column<decimal>(nullable: false),
                Description = table.Column<string>(nullable: true)
            },
            constraints: table =>
            {
                table.PrimaryKey("PK_Products", x => x.Id);
            });
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.DropTable(name: "Products");
    }
}
```

`Up()`-metodi ajaa migraation eteenpäin (lisää taulun), `Down()` peruu sen.

---

## Async-metodit

Tietokantaoperaatiot ovat hitaita (verkon yli, levyltä), joten ne tehdään aina **asynkronisesti** `async/await`-avainsanojen kanssa.

### Sync vs. Async

```csharp
// Synkroninen — HUONO (estää muut pyynnöt)
var products = _context.Products.ToList();

// Asynkroninen — HYVÄ
var products = await _context.Products.ToListAsync();
```

### Yleiset async-metodit

| Metodi | Toiminto |
|--------|----------|
| `ToListAsync()` | Hae kaikki tulokset listaksi |
| `FindAsync(id)` | Hae ensisijaisavaimella |
| `FirstOrDefaultAsync(ehto)` | Hae ensimmäinen ehdon täyttävä tai null |
| `AnyAsync(ehto)` | Onko yhtään ehdon täyttävää? |
| `CountAsync()` | Laske rivien määrä |
| `AddAsync(entity)` | Lisää entiteetti (valinnainen async-versio) |
| `SaveChangesAsync()` | Tallenna kaikki muutokset tietokantaan |

### Esimerkki: täydellinen async-metodi

```csharp
[HttpGet("{id}")]
public async Task<IActionResult> GetById(int id)
{
    var product = await _context.Products.FindAsync(id);

    if (product == null)
        return NotFound();

    return Ok(product);
}
```

Huomaa:
- Metodi on `async` — se voi odottaa asynkronisia operaatioita
- Paluutyyppi on `Task<IActionResult>` — `Task` käärii paluuarvon asynkroniselle metodille
- `await` odottaa tietokantahaun valmistumista ennen kuin jatkaa

---

## Rekisteröinti Program.cs:ssä

EF Core rekisteröidään DI-konttiin `Program.cs`:ssä:

```csharp
// SQLite-tietokanta
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite("Data Source=productapi.db"));
```

Tietokantayhteys (`Data Source=productapi.db`) kertoo SQLitelle, mihin tiedostoon tietokanta tallennetaan. Tiedosto luodaan automaattisesti projektin juureen.

### Connection string appsettings.json:ssa

Parempi tapa on tallentaa yhteysmäärittely `appsettings.json`-tiedostoon:

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Data Source=productapi.db"
  }
}
```

```csharp
// Program.cs
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlite(builder.Configuration.GetConnectionString("DefaultConnection")));
```

---

## CRUD tietokannalla

Tässä täydellinen esimerkki CRUD-operaatioista EF Coren kanssa:

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly AppDbContext _context;

    // AppDbContext injektoidaan konstruktorilla
    public ProductsController(AppDbContext context)
    {
        _context = context;
    }

    // GET api/products
    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var products = await _context.Products.ToListAsync();
        return Ok(products);
    }

    // GET api/products/5
    [HttpGet("{id}")]
    public async Task<IActionResult> GetById(int id)
    {
        var product = await _context.Products.FindAsync(id);

        if (product == null)
            return NotFound();

        return Ok(product);
    }

    // POST api/products
    [HttpPost]
    public async Task<IActionResult> Create(Product product)
    {
        _context.Products.Add(product);
        await _context.SaveChangesAsync();  // ID asetetaan automaattisesti tietokannassa

        return CreatedAtAction(nameof(GetById), new { id = product.Id }, product);
    }

    // PUT api/products/5
    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, Product product)
    {
        var existing = await _context.Products.FindAsync(id);

        if (existing == null)
            return NotFound();

        existing.Name = product.Name;
        existing.Price = product.Price;
        existing.Description = product.Description;

        await _context.SaveChangesAsync();

        return Ok(existing);
    }

    // DELETE api/products/5
    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        var product = await _context.Products.FindAsync(id);

        if (product == null)
            return NotFound();

        _context.Products.Remove(product);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}
```

### Ero staattiseen listaan verrattuna

| Staattinen lista | EF Core + SQLite |
|-----------------|------------------|
| Data häviää sovelluksen käynnistyessä | Data säilyy tiedostossa |
| `_products.Add(product)` | `_context.Products.Add(product)` + `SaveChangesAsync()` |
| ID pitää asettaa manuaalisesti | Tietokanta asettaa ID:n automaattisesti |
| Kaikki metodit synkronisia | Kaikki metodit asynkronisia (`async/await`) |
| `FirstOrDefault(...)` | `FindAsync(id)` tai `FirstOrDefaultAsync(...)` |

---

## Tietokannan valinta

### SQLite — kehitykseen

```
Hyödyt:
+ Ei erillistä palvelinta
+ Tietokanta on yksi .db-tiedosto
+ Helppo jakaa ja siirtää

Rajoitukset:
- Ei sovellu monelle yhtäaikaiselle käyttäjälle tuotannossa
- Ei tue kaikkia SQL Serverin ominaisuuksia
```

### SQL Server / PostgreSQL — tuotantoon

```
Hyödyt:
+ Kestää tuhansia yhtäaikaisia yhteyksiä
+ Kaikki SQL-ominaisuudet
+ Azure SQL (SQL Server) tai Azure Database for PostgreSQL

Vaihto on helppoa: vain connection string ja NuGet-paketti muuttuvat,
muu koodi pysyy täysin samana.
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **ORM** | Kirjasto joka muuntaa C#-luokat tietokantatauluiksi |
| **EF Core** | Microsoftin ORM .NET:lle |
| **Entiteetti** | C#-luokka joka vastaa tietokantataulua |
| **DbContext** | Yhteys tietokantaan, hallinnoi operaatiot |
| **DbSet** | Taulun edustaja koodissa (CRUD-metodit) |
| **Migraatio** | Tietokannan rakenteen versiointi koodissa |
| **SaveChangesAsync()** | Tallentaa muutokset tietokantaan |
| **async/await** | Asynkroniset tietokantakutsut — ei estä muita pyyntöjä |

### Seuraavaksi

- [Services-and-DI](Services-and-DI.md) — Siirretään tietokantalogiikka pois controllerista service-luokkaan
- [Database-harjoitus](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Database) — Käytännön harjoitus
- [Dependency Injection](../Dependency-Injection.md) — DI:n teoria syvemmin
