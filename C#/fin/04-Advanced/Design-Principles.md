# Suunnitteluperiaatteet (Design Principles)

Suunnitteluperiaatteet ovat ohjeita ja käytäntöjä, jotka auttavat kirjoittamaan **luettavaa, ylläpidettävää ja laadukasta** koodia. Ne eivät ole jäykkiä sääntöjä, vaan työkaluja — opi ne, ymmärrä miksi ne ovat olemassa, ja sovella niitä tilanteen mukaan.

Tämä materiaali käy läpi tärkeimmät periaatteet käytännön C#-esimerkein. Tavoite on, että tämän luettuasi osaat tunnistaa huonoa koodia ja kirjoittaa parempaa.

**Muita materiaaleja:**
- [SOLID-periaatteet (kattava materiaali)](SOLID.md)
- [Dependency Injection](Dependency-Injection.md)
- [Suunnittelumallit (Design Patterns)](Design-Patterns.md)
- [Koodauskäytännöt (nimeäminen, muotoilu)](../00-Basics/Coding-Conventions.md)
- [Clean Code - Robert C. Martin (kirja)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

---

## Sisällysluettelo

1. [Perusperiaatteet](#perusperiaatteet) — DRY, KISS, YAGNI
2. [Puhtaan koodin periaatteet](#puhtaan-koodin-periaatteet) — Guard clauses, magic numbers, nesting, pienet metodit
3. [SOLID-periaatteet](#solid-periaatteet) — Yhteenveto + linkki
4. [Arkkitehtuuriperiaatteet](#arkkitehtuuriperiaatteet) — SoC, loose coupling, composition, LoD
5. [Defensiivinen ohjelmointi](#defensiivinen-ohjelmointi) — Null-turvallisuus, validointi, fail fast
6. [Koodihajut (Code Smells)](#koodihajut-code-smells) — Tunnista ongelmia koodissa
7. [Tarkistuslista](#tarkistuslista) — Nopea checklist ennen koodin palautusta

---

## Perusperiaatteet

### 1. DRY (Don't Repeat Yourself)

> *"Jokainen tieto tulisi ilmaista vain yhdessä paikassa."*

Kun sama logiikka toistuu useissa paikoissa, muutos yhdessä kohdassa vaatii muutoksen kaikkialle — ja jossain se unohtuu aina.

**Huono — sama validointi kolmessa paikassa:**

```csharp
public void CreateUser(string email)
{
    if (string.IsNullOrEmpty(email) || !email.Contains("@"))
        throw new ArgumentException("Invalid email");
    // ...
}

public void UpdateEmail(string email)
{
    if (string.IsNullOrEmpty(email) || !email.Contains("@"))
        throw new ArgumentException("Invalid email");
    // ...
}

public void SendInvitation(string email)
{
    if (string.IsNullOrEmpty(email) || !email.Contains("@"))
        throw new ArgumentException("Invalid email");
    // ...
}
```

**Hyvä — validointi yhdessä paikassa:**

```csharp
public static class EmailValidator
{
    public static void Validate(string email)
    {
        if (string.IsNullOrEmpty(email) || !email.Contains("@"))
            throw new ArgumentException("Invalid email");
    }
}

public void CreateUser(string email)
{
    EmailValidator.Validate(email);
    // ...
}

public void UpdateEmail(string email)
{
    EmailValidator.Validate(email);
    // ...
}

public void SendInvitation(string email)
{
    EmailValidator.Validate(email);
    // ...
}
```

Nyt jos sähköpostivalidointi muuttuu (esim. lisätään regex-tarkistus), muutat vain yhden paikan.

**Toinen yleinen DRY-ongelma — toistetut "magic strings":**

```csharp
// Huono: sama merkkijono monessa paikassa
if (user.Role == "Admin") { /* ... */ }
// ... 200 riviä myöhemmin ...
if (user.Role == "Admin") { /* ... */ }
// ... toisessa tiedostossa ...
if (user.Role == "admin") { /* ... */ }  // Hupsista, pieni alkukirjain!

// Hyvä: vakio yhdessä paikassa
public static class Roles
{
    public const string Admin = "Admin";
    public const string User = "User";
    public const string Manager = "Manager";
}

if (user.Role == Roles.Admin) { /* ... */ }
```

---

### 2. KISS (Keep It Simple, Stupid)

> *"Yksinkertaisuus on äärimmäisen monimutkaista." — Leonardo da Vinci*

Kirjoita koodi niin yksinkertaisesti kuin mahdollista. Liian "fiksu" koodi on usein virhealtista ja vaikea ymmärtää.

**Huono — turhan monimutkainen:**

```csharp
public string GetUserDisplayName(User user)
{
    return user != null
        ? (user.FirstName != null && user.LastName != null
            ? $"{user.FirstName} {user.LastName}"
            : (user.FirstName != null
                ? user.FirstName
                : (user.LastName != null
                    ? user.LastName
                    : (user.Email != null
                        ? user.Email
                        : "Unknown"))))
        : "Unknown";
}
```

**Hyvä — selkeä ja luettava:**

```csharp
public string GetUserDisplayName(User user)
{
    if (user is null)
        return "Unknown";

    if (!string.IsNullOrEmpty(user.FirstName) && !string.IsNullOrEmpty(user.LastName))
        return $"{user.FirstName} {user.LastName}";

    if (!string.IsNullOrEmpty(user.FirstName))
        return user.FirstName;

    if (!string.IsNullOrEmpty(user.LastName))
        return user.LastName;

    return user.Email ?? "Unknown";
}
```

**Toinen esimerkki — turha abstraktio:**

```csharp
// Huono: tehdas-malli yhdelle luokalle, jolla ei ole variaatioita
public interface IGreeterFactory
{
    IGreeter Create();
}

public interface IGreeter
{
    string Greet(string name);
}

public class SimpleGreeter : IGreeter
{
    public string Greet(string name) => $"Hello, {name}!";
}

public class GreeterFactory : IGreeterFactory
{
    public IGreeter Create() => new SimpleGreeter();
}

// Hyvä: yksinkertainen metodi riittää
public string Greet(string name) => $"Hello, {name}!";
```

Älä lisää rajapintoja, abstrakteja luokkia tai design pattern -rakenteita, jos niille ei ole oikeaa tarvetta juuri nyt.

---

### 3. YAGNI (You Aren't Gonna Need It)

> *"Älä rakenna sitä, ennen kuin tarvitset."*

Koodaa vain se, mitä **juuri nyt** tarvitaan. "Varmuuden vuoksi" lisätyt ominaisuudet tuovat monimutkaisuutta, jota joudut ylläpitämään — vaikka niitä ei koskaan käytettäisi.

**Huono — "tulevaisuuden varalle" rakennettu:**

```csharp
public class UserService
{
    public void CreateUser(User user) { /* toteutus */ }
    public void UpdateUser(User user) { /* toteutus */ }
    public void DeleteUser(int id) { /* toteutus */ }

    // "Ehkä tarvitaan joskus..."
    public void ExportUsersToXml() { throw new NotImplementedException(); }
    public void ImportUsersFromCsv() { throw new NotImplementedException(); }
    public void SyncWithExternalApi() { throw new NotImplementedException(); }
    public void GenerateUserStatistics() { throw new NotImplementedException(); }
    public void SendBulkNotifications() { throw new NotImplementedException(); }
}
```

**Hyvä — vain se mitä tarvitaan:**

```csharp
public class UserService
{
    public void CreateUser(User user) { /* toteutus */ }
    public void UpdateUser(User user) { /* toteutus */ }
    public void DeleteUser(int id) { /* toteutus */ }
}
```

Kun XML-export tarvitaan, sille luodaan oma luokka siinä vaiheessa. YAGNI ei tarkoita, ettei koodin rakennetta kannata miettiä — se tarkoittaa, ettei rakenneta tyhjää "tulossa"-koodia.

---

## Puhtaan koodin periaatteet

### 4. Guard Clauses (vartiolausekkeet) ja Early Return

Yksi tehokkaimmista tavoista tehdä koodista luettavaa. Sen sijaan, että kirjoitat syvään sisäkkäisiä if-lauseita, tarkista virhetilanteet **heti alussa** ja palaa niistä.

**Huono — syvä sisäkkäisyys (Arrow Anti-Pattern):**

```csharp
public decimal CalculateDiscount(Order order)
{
    if (order != null)
    {
        if (order.Customer != null)
        {
            if (order.Items.Count > 0)
            {
                if (order.Customer.IsPremium)
                {
                    decimal total = order.Items.Sum(i => i.Price);
                    if (total > 100)
                    {
                        return total * 0.15m;
                    }
                    else
                    {
                        return total * 0.10m;
                    }
                }
                else
                {
                    return order.Items.Sum(i => i.Price) * 0.05m;
                }
            }
        }
    }
    return 0;
}
```

**Hyvä — guard clauses:**

```csharp
public decimal CalculateDiscount(Order order)
{
    if (order is null)
        return 0;

    if (order.Customer is null)
        return 0;

    if (order.Items.Count == 0)
        return 0;

    decimal total = order.Items.Sum(i => i.Price);

    if (!order.Customer.IsPremium)
        return total * 0.05m;

    return total > 100 ? total * 0.15m : total * 0.10m;
}
```

Guard clausesin avulla:
- Virhetilanteet käsitellään heti
- Sisennystaso pysyy matalana
- "Happy path" (onnistunut suoritus) on selkeästi näkyvissä

---

### 5. Vältä taikanumeroita ja taikamerkkijonoja (Magic Numbers / Magic Strings)

"Taikanumero" on numero koodissa, jonka merkitystä ei voi päätellä ilman kontekstia. Käytä vakioita tai enumeja.

**Huono:**

```csharp
if (user.Age >= 18)
{
    // ...
}

if (order.Status == 3)
{
    // Mikä on 3? Shipped? Cancelled? Pending?
}

Thread.Sleep(86400000);
// Kuinka monta millisekuntia on 86400000?
```

**Hyvä:**

```csharp
const int LegalAge = 18;

if (user.Age >= LegalAge)
{
    // ...
}

public enum OrderStatus
{
    Pending = 1,
    Processing = 2,
    Shipped = 3,
    Delivered = 4,
    Cancelled = 5
}

if (order.Status == OrderStatus.Shipped)
{
    // Selkeä!
}

var oneDay = TimeSpan.FromDays(1);
Thread.Sleep(oneDay);
```

---

### 6. Pidä metodit pieninä

Hyvä metodi tekee **yhden asian** ja tekee sen hyvin. Jos metodi on yli 20-30 riviä pitkä, se todennäköisesti tekee liikaa.

**Huono — "jumbo-metodi":**

```csharp
public void ProcessOrder(Order order)
{
    // Validoi tilaus (10 riviä)
    if (order == null) throw new ArgumentNullException();
    if (order.Items.Count == 0) throw new InvalidOperationException("No items");
    if (order.Customer == null) throw new InvalidOperationException("No customer");
    // ... lisää validointeja ...

    // Laske hinta (15 riviä)
    decimal subtotal = 0;
    foreach (var item in order.Items)
    {
        subtotal += item.Price * item.Quantity;
    }
    decimal tax = subtotal * 0.24m;
    decimal total = subtotal + tax;
    // ... lisää laskentoja ...

    // Päivitä varasto (10 riviä)
    foreach (var item in order.Items)
    {
        var product = GetProduct(item.ProductId);
        product.Stock -= item.Quantity;
        SaveProduct(product);
    }

    // Tallenna tilaus (5 riviä)
    order.Total = total;
    order.Status = OrderStatus.Confirmed;
    SaveOrder(order);

    // Lähetä vahvistus (10 riviä)
    var emailBody = $"Dear {order.Customer.Name}, your order #{order.Id} ...";
    SendEmail(order.Customer.Email, "Order Confirmation", emailBody);
}
```

**Hyvä — jaettu pieniin metodeihin:**

```csharp
public void ProcessOrder(Order order)
{
    ValidateOrder(order);

    decimal total = CalculateTotal(order);

    UpdateInventory(order);

    SaveConfirmedOrder(order, total);

    SendOrderConfirmation(order);
}

private void ValidateOrder(Order order)
{
    if (order is null)
        throw new ArgumentNullException(nameof(order));

    if (order.Items.Count == 0)
        throw new InvalidOperationException("Order has no items");

    if (order.Customer is null)
        throw new InvalidOperationException("Order has no customer");
}

private decimal CalculateTotal(Order order)
{
    decimal subtotal = order.Items.Sum(i => i.Price * i.Quantity);
    decimal tax = subtotal * 0.24m;
    return subtotal + tax;
}

private void UpdateInventory(Order order)
{
    foreach (var item in order.Items)
    {
        var product = GetProduct(item.ProductId);
        product.Stock -= item.Quantity;
        SaveProduct(product);
    }
}

private void SaveConfirmedOrder(Order order, decimal total)
{
    order.Total = total;
    order.Status = OrderStatus.Confirmed;
    SaveOrder(order);
}

private void SendOrderConfirmation(Order order)
{
    var emailBody = $"Dear {order.Customer.Name}, your order #{order.Id} " +
                    $"has been confirmed. Total: {order.Total:C}";
    SendEmail(order.Customer.Email, "Order Confirmation", emailBody);
}
```

Nyt `ProcessOrder`-metodi on kuin lyhyt "sisällysluettelo" — näet yhdellä silmäyksellä, mitä tilauksen käsittelyssä tapahtuu. Yksityiskohdat löytyvät omista metodeistaan.

---

### 7. Vältä syvää sisäkkäisyyttä (Max 2-3 tasoa)

Jos koodissasi on yli kolme sisennystasoa, se on merkki ongelmasta. Käytä guard clauseeja, pieniin metodeihin jakamista tai LINQ:ia.

**Huono — 5 sisennystasoa:**

```csharp
public void ProcessStudents(List<Student> students)
{
    if (students != null)
    {
        foreach (var student in students)
        {
            if (student.IsActive)
            {
                foreach (var course in student.Courses)
                {
                    if (course.Grade >= 1)
                    {
                        Console.WriteLine($"{student.Name}: {course.Name} = {course.Grade}");
                    }
                }
            }
        }
    }
}
```

**Hyvä — matala ja selkeä:**

```csharp
public void ProcessStudents(List<Student> students)
{
    if (students is null)
        return;

    foreach (var student in students.Where(s => s.IsActive))
    {
        PrintPassedCourses(student);
    }
}

private void PrintPassedCourses(Student student)
{
    var passedCourses = student.Courses.Where(c => c.Grade >= 1);

    foreach (var course in passedCourses)
    {
        Console.WriteLine($"{student.Name}: {course.Name} = {course.Grade}");
    }
}
```

---

### 8. Hyvä nimeäminen

Koodi on kommunikaatiota. Hyvä nimi kertoo **mitä** ja **miksi** — ei **miten**.

```csharp
// Huono — mitä nämä ovat?
var d = GetData();
var x = d.Where(i => i.A > 5).ToList();
var res = Calc(x);

// Hyvä — ymmärrät ilman kommentteja
var activeOrders = GetOrdersByStatus(OrderStatus.Active);
var largeOrders = activeOrders.Where(order => order.Total > 500).ToList();
var monthlyRevenue = CalculateRevenue(largeOrders);
```

**Nimeämisen nyrkkisäännöt:**

| Kohde | Sääntö | Esimerkki |
|-------|--------|-----------|
| Luokka | Substantiivi | `OrderService`, `PriceCalculator` |
| Metodi | Verbi + substantiivi | `CalculateTotal()`, `SendEmail()` |
| Boolean | `is`, `has`, `can` -alkuinen | `isActive`, `hasPermission` |
| Kokoelma | Monikko | `orders`, `activeUsers` |
| Yksittäinen alkio | Yksikkö | `order`, `user` |

**Kommenttien suhteen:** Jos koodi tarvitsee kommentin selittämään *mitä* se tekee, koodi on liian monimutkainen. Hyvä koodi ei tarvitse kommentteja — se selittää itsensä nimeämisellä. Kommentit ovat hyödyllisiä selittämään **miksi** jokin tehdään tietyllä tavalla.

```csharp
// Huono kommentti — kertoo saman mitä koodi
// Lisää tuote listaan
products.Add(product);

// Hyvä kommentti — selittää miksi
// Käytetään 24h välimuistia, koska API:n rate limit on 100 kutsua/tunti
var cacheExpiration = TimeSpan.FromHours(24);
```

Katso myös: [Koodauskäytännöt](../00-Basics/Coding-Conventions.md)

---

### 9. Yhden tason abstraktio (Single Level of Abstraction)

Metodin sisällä kaiken koodin tulisi olla **samalla abstraktiotasolla**. Älä sekoita korkean tason logiikkaa matalan tason yksityiskohtiin.

**Huono — sekaisin eri abstraktiotasoja:**

```csharp
public void RegisterUser(string name, string email, string password)
{
    // Korkea taso: validointi
    if (string.IsNullOrEmpty(name))
        throw new ArgumentException("Name required");

    // Matala taso: salasanan hashays
    using var sha256 = SHA256.Create();
    var bytes = Encoding.UTF8.GetBytes(password);
    var hash = sha256.ComputeHash(bytes);
    var hashedPassword = Convert.ToBase64String(hash);

    // Korkea taso: luo käyttäjä
    var user = new User { Name = name, Email = email, Password = hashedPassword };

    // Matala taso: SQL-kysely
    using var connection = new SqlConnection(_connectionString);
    connection.Open();
    var cmd = new SqlCommand("INSERT INTO Users ...", connection);
    cmd.Parameters.AddWithValue("@name", name);
    cmd.ExecuteNonQuery();

    // Korkea taso: lähetä sähköposti
    SendWelcomeEmail(email);
}
```

**Hyvä — yksi abstraktiotaso:**

```csharp
public void RegisterUser(string name, string email, string password)
{
    ValidateInput(name, email, password);

    var hashedPassword = HashPassword(password);

    var user = new User { Name = name, Email = email, Password = hashedPassword };

    _userRepository.Save(user);

    SendWelcomeEmail(email);
}
```

---

## SOLID-periaatteet

SOLID on viiden suunnitteluperiaatteen kokoelma, joka on yksi tärkeimmistä aiheista olio-ohjelmoinnissa. Tässä lyhyt yhteenveto — **kattava materiaali löytyy täältä: [SOLID-periaatteet](SOLID.md).**

| Periaate | Lyhenne | Ydinsanoma |
|----------|---------|------------|
| **S**ingle Responsibility | SRP | Luokalla yksi syy muuttua |
| **O**pen/Closed | OCP | Avoin laajennuksille, suljettu muutoksille |
| **L**iskov Substitution | LSP | Aliluokka korvaa yläluokan ongelmitta |
| **I**nterface Segregation | ISP | Pienet, kohdennetut rajapinnat |
| **D**ependency Inversion | DIP | Riippu abstraktioista, ei konkreettisista luokista |

**Nopea esimerkki — SRP käytännössä:**

```csharp
// Huono: luokka tekee kaiken
public class User
{
    public string Name { get; set; }
    public string Email { get; set; }

    public void SaveToDatabase() { /* ... */ }
    public void SendEmail() { /* ... */ }
    public string GenerateReport() { return ""; }
}

// Hyvä: jokaisella luokalla yksi tehtävä
public class User { public string Name { get; set; } public string Email { get; set; } }
public class UserRepository { public void Save(User user) { /* ... */ } }
public class EmailService { public void SendEmail(string to, string msg) { /* ... */ } }
public class ReportGenerator { public string Generate(User user) { return ""; } }
```

---

## Arkkitehtuuriperiaatteet

### 10. Separation of Concerns (SoC) — Vastuualueiden erottaminen

Jokainen osa ohjelmaa käsittelee **yhtä huolenaihetta** (concern). Käyttöliittymälogiikka, liiketoimintalogiikka ja tiedon tallennus pidetään erillään.

```csharp
// Huono: Controller tekee kaiken
[HttpPost]
public IActionResult CreateUser(CreateUserRequest request)
{
    // Validointi (UI concern)
    if (string.IsNullOrEmpty(request.Email))
        return BadRequest("Email required");

    // Liiketoimintalogiikka (Business concern)
    var hashedPassword = BCrypt.HashPassword(request.Password);
    var user = new User
    {
        Email = request.Email,
        Password = hashedPassword,
        CreatedAt = DateTime.UtcNow
    };

    // Tietokanta (Data concern)
    _context.Users.Add(user);
    _context.SaveChanges();

    // Sähköposti (Infrastructure concern)
    var smtp = new SmtpClient("smtp.server.com");
    smtp.Send(new MailMessage("noreply@app.com", request.Email, "Welcome!", "..."));

    return Ok(user);
}

// Hyvä: jokainen vastuu omassa paikassaan
[HttpPost]
public IActionResult CreateUser(CreateUserRequest request)
{
    var result = _userService.CreateUser(request.Email, request.Password);

    if (!result.IsSuccess)
        return BadRequest(result.Error);

    return Ok(result.Value);
}
```

SoC toteutuu käytännössä mm. **kerrosarkkitehtuurin** avulla:
- **Controller** — vastaanottaa HTTP-pyynnöt ja palauttaa vastaukset
- **Service** — liiketoimintalogiikka
- **Repository** — tiedon tallennus ja haku

Katso: [Ohjelmistoarkkitehtuuri](Architecture/README.md)

---

### 11. Composition Over Inheritance — Suosi koostumusta perimisen sijaan

Perintä luo **tiukan siteen** yläluokan ja aliluokan välille. Koostumus (composition) on joustavampi — voit yhdistellä toimintoja vapaasti.

**Perintä — jäykkä hierarkia:**

```csharp
public class Animal
{
    public void Eat() { /* ... */ }
}

public class Dog : Animal
{
    public void Bark() { /* ... */ }
}

// Entä jos tarvitaan robotti-koira, joka haukkuu mutta ei syö?
// Perintähierarkia ei taivu tähän helposti.
```

**Koostumus — joustava yhdistely:**

```csharp
public interface IMovable
{
    void Move();
}

public interface IFeedable
{
    void Feed();
}

public interface IVoice
{
    void MakeSound();
}

public class Dog : IMovable, IFeedable, IVoice
{
    public void Move() => Console.WriteLine("Dog runs");
    public void Feed() => Console.WriteLine("Dog eats kibble");
    public void MakeSound() => Console.WriteLine("Woof!");
}

public class RobotDog : IMovable, IVoice
{
    public void Move() => Console.WriteLine("Robot dog walks");
    public void MakeSound() => Console.WriteLine("Woof! (synthetic)");
}
```

**Nyrkkisääntö:** Käytä perintää vain silloin kun aliluokka todella **on** yläluokan erikoistapaus (esim. `Koira on Eläin`). Käytä koostumusta kun luokka **käyttää** toisen luokan toimintoja.

---

### 12. Loose Coupling — Löysä kytkentä

Luokat eivät saa olla liian riippuvaisia toistensa sisäisistä yksityiskohdista. Löysästi kytketty koodi on helppo testata, muuttaa ja laajentaa.

**Tiukka kytkentä:**

```csharp
public class OrderService
{
    // Sidottu suoraan SqlServeriin ja SmtpClientiin
    private readonly SqlServerDatabase _database = new SqlServerDatabase();
    private readonly SmtpEmailClient _emailClient = new SmtpEmailClient();

    public void PlaceOrder(Order order)
    {
        _database.Save(order);
        _emailClient.Send(order.Customer.Email, "Order confirmed");
    }
}
```

**Löysä kytkentä:**

```csharp
public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly INotificationService _notificationService;

    public OrderService(IOrderRepository repository, INotificationService notificationService)
    {
        _repository = repository;
        _notificationService = notificationService;
    }

    public void PlaceOrder(Order order)
    {
        _repository.Save(order);
        _notificationService.Notify(order.Customer.Email, "Order confirmed");
    }
}
```

Hyödyt:
- Tietokannan voi vaihtaa (SQL Server -> PostgreSQL) muuttamatta `OrderService`-luokkaa
- Yksikkötesteissä voidaan käyttää mock-toteutuksia
- Sähköpostipalvelun voi vaihtaa push-notifikaatioksi

Katso: [Dependency Injection](Dependency-Injection.md)

---

### 13. Law of Demeter — "Puhu vain lähimmille ystävillesi"

Luokan ei pidä "kaivella" syvälle toisten olioiden rakenteisiin. Jos näet pitkiä pisteketjuja, se on merkki ongelmasta.

**Huono — pisteketjut:**

```csharp
// OrderService tietää liikaa Order → Customer → Address → City -rakenteesta
var city = order.Customer.Address.City;
var country = order.Customer.Address.Country;
var discount = order.Customer.MembershipPlan.DiscountPercentage;

string shippingLabel = $"{order.Customer.FirstName} {order.Customer.LastName}\n" +
                       $"{order.Customer.Address.Street}\n" +
                       $"{order.Customer.Address.ZipCode} {city}, {country}";
```

**Hyvä — kysy vain mitä tarvitset:**

```csharp
// Order-luokka tarjoaa suoraan tarvittavat tiedot
string shippingLabel = order.GetShippingLabel();
decimal discount = order.GetCustomerDiscount();

// Order-luokan sisällä:
public class Order
{
    public Customer Customer { get; set; }

    public string GetShippingLabel() => Customer.GetShippingLabel();
    public decimal GetCustomerDiscount() => Customer.GetDiscount();
}
```

**Nyrkkisääntö:** Jos pisteketjussa on enemmän kuin kaksi pistettä (esim. `a.B.C.D`), mieti onko vastuu oikeassa paikassa.

---

### 14. Boy Scout Rule — "Jätä koodi parempaan kuntoon kuin löysit"

Kun muokkaat koodia, paranna samalla pieniä asioita: nimeä muuttuja paremmin, poista kuollut koodi, lisää puuttuva validointi. Ajan myötä koodi paranee jatkuvasti.

```csharp
// Löysit tämän koodin:
public void Proc(List<object> d)
{
    for(int i=0;i<d.Count;i++){
        var x = (Customer)d[i];
        if(x.a == true){
            Console.WriteLine(x.n);
        }
    }
}

// Parannettu versio:
public void PrintActiveCustomers(List<Customer> customers)
{
    foreach (var customer in customers.Where(c => c.IsActive))
    {
        Console.WriteLine(customer.Name);
    }
}
```

Ei tarvitse uudelleenkirjoittaa koko sovellusta — **pienet parannukset** kerääntyvät ajan myötä suuriksi.

---

## Defensiivinen ohjelmointi

### 15. Fail Fast — Epäonnistu aikaisin

Tarkista syötteet ja edellytykset **heti metodin alussa**. Mitä aikaisemmin virhe löytyy, sitä helpompi se on korjata.

```csharp
// Huono: virhe löytyy vasta 50 rivin jälkeen
public void TransferMoney(Account from, Account to, decimal amount)
{
    // ... 50 riviä muuta logiikkaa ...
    from.Balance -= amount; // NullReferenceException, jos from == null
    to.Balance += amount;   // Hupsista, rahat katosivat!
}

// Hyvä: tarkista heti
public void TransferMoney(Account from, Account to, decimal amount)
{
    ArgumentNullException.ThrowIfNull(from);
    ArgumentNullException.ThrowIfNull(to);

    if (amount <= 0)
        throw new ArgumentOutOfRangeException(nameof(amount), "Amount must be positive");

    if (from.Balance < amount)
        throw new InvalidOperationException("Insufficient funds");

    from.Balance -= amount;
    to.Balance += amount;
}
```

---

### 16. Null-turvallisuus

`NullReferenceException` on yksi yleisimmistä virheistä C#-ohjelmoinnissa. Suojaudu siltä.

```csharp
// Huono: toivotaan parasta
string name = user.Name.ToUpper();

// Hyvä: null-tarkistukset
string name = user?.Name?.ToUpper() ?? "UNKNOWN";

// Hyvä: pattern matching
if (user is { Name: not null } u)
{
    Console.WriteLine(u.Name.ToUpper());
}

// Hyvä: guard clause
public void ProcessUser(User user)
{
    if (user is null)
        throw new ArgumentNullException(nameof(user));

    // Turvallisesti eteenpäin...
}
```

**Nullable reference types** (C# 8+) auttavat kääntäjätasolla varoittamaan null-ongelmista:

```csharp
// Kertoo kääntäjälle, että Name voi olla null
public string? Name { get; set; }

// Kertoo kääntäjälle, että Email ei saa olla null
public string Email { get; set; } = string.Empty;
```

---

### 17. Syötteiden validointi

Älä luota koskaan ulkoiseen dataan — käyttäjän syötteet, API-vastaukset ja tiedostot voivat sisältää mitä tahansa.

```csharp
public class UserValidator
{
    public static void Validate(CreateUserRequest request)
    {
        if (string.IsNullOrWhiteSpace(request.Name))
            throw new ArgumentException("Name is required");

        if (request.Name.Length > 100)
            throw new ArgumentException("Name too long (max 100 characters)");

        if (string.IsNullOrWhiteSpace(request.Email))
            throw new ArgumentException("Email is required");

        if (!request.Email.Contains('@'))
            throw new ArgumentException("Invalid email format");

        if (request.Age < 0 || request.Age > 150)
            throw new ArgumentOutOfRangeException(nameof(request.Age));
    }
}
```

---

## Koodihajut (Code Smells)

"Koodihaju" on merkki siitä, että koodissa voi olla suunnitteluongelma. Koodihajut eivät välttämättä ole bugeja, mutta ne tekevät koodista vaikeammin ylläpidettävää.

### Yleisimmät koodihajut

| Koodihaju | Kuvaus | Ratkaisu |
|-----------|--------|----------|
| **Pitkä metodi** | Yli 20-30 riviä | Jaa pienempiin metodeihin |
| **Suuri luokka** | Luokka tekee liian montaa asiaa | SRP — jaa useampaan luokkaan |
| **Pitkä parametrilista** | Metodi ottaa 5+ parametriä | Luo parametriolio |
| **Toistuva koodi** | Sama logiikka monessa paikassa | DRY — erota yhteinen koodi |
| **Syvä sisäkkäisyys** | 4+ sisennystasoa | Guard clauses, pienemmät metodit |
| **Kommentit joka rivillä** | Koodi vaatii selitystä toimiakseen | Nimeä koodi paremmin |
| **Kuollut koodi** | Kommentoitu koodi tai käyttämättömät metodit | Poista se (Git muistaa) |
| **Boolean-parametrit** | `DoThing(true, false, true)` | Käytä enum-arvoja tai erillisiä metodeja |
| **Kateelliset metodit** | Metodi käyttää enemmän toisen luokan dataa kuin omaansa | Siirrä metodi oikeaan luokkaan |
| **Primitiiviobsessio** | `string email` kaikkialla luokan sijaan | Luo `Email`-arvo-olio |

### Esimerkkejä

**Pitkä parametrilista → Parametriolio:**

```csharp
// Huono: liian monta parametriä
public void CreateUser(string firstName, string lastName, string email,
    string phone, string address, string city, string zipCode, string country)
{
    // ...
}

// Hyvä: parametriolio
public class CreateUserRequest
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Email { get; set; }
    public string Phone { get; set; }
    public Address Address { get; set; }
}

public void CreateUser(CreateUserRequest request)
{
    // ...
}
```

**Boolean-parametrit → Selkeät metodit:**

```csharp
// Huono: mitä true ja false tarkoittavat?
SendNotification(user, "Welcome!", true, false);

// Hyvä: erilliset metodit tai nimetyt parametrit
SendEmailNotification(user, "Welcome!");
SendPushNotification(user, "Welcome!");

// Tai nimetyt parametrit:
SendNotification(user, "Welcome!", urgent: true, silent: false);
```

**Kuollut koodi — poista se:**

```csharp
// Huono: kommentoitua koodia
public void ProcessOrder(Order order)
{
    // var oldPrice = CalculateOldPrice(order);
    // if (oldPrice > 100) { ApplyOldDiscount(order); }
    // var legacyResult = LegacyProcessor.Process(order);
    // logger.Log("Old processing done");

    var price = CalculatePrice(order);
    ApplyDiscount(order);
}

// Hyvä: vain toimiva koodi
public void ProcessOrder(Order order)
{
    var price = CalculatePrice(order);
    ApplyDiscount(order);
}
```

Älä pidä vanhaa koodia kommentoituna "varmuuden vuoksi" — Git-versionhallinta muistaa kaiken. Jos tarvitset vanhaa koodia, löydät sen commitin historiasta.

---

## Tarkistuslista

Käy tämä lista läpi ennen kuin palautat koodin tai teet commitin:

### Nimeäminen
- [ ] Muuttujilla on kuvaavat nimet (`customerAge`, ei `x` tai `a`)
- [ ] Metodien nimet kertovat mitä ne tekevät (`CalculateTotal`, ei `DoWork`)
- [ ] Boolean-muuttujat alkavat `is`, `has`, `can`, `should` -sanalla
- [ ] Luokkien nimet ovat substantiiveja (`OrderService`, ei `ProcessOrder`)

### Rakenne
- [ ] Jokainen metodi tekee yhden asian
- [ ] Metodit ovat alle 20-30 riviä
- [ ] Sisäkkäisyys on korkeintaan 2-3 tasoa
- [ ] Guard clauseita käytetään syvälle menemisen sijaan

### Periaatteet
- [ ] Ei toistettua logiikkaa (DRY)
- [ ] Ei turhaa monimutkaisuutta (KISS)
- [ ] Ei "tulevaisuuden varalle" kirjoitettua koodia (YAGNI)
- [ ] Ei taikanumeroita — vakiot tai enumit käytössä

### Turvallisuus
- [ ] Null-tarkistukset kriittisessä koodissa
- [ ] Syötteiden validointi
- [ ] Poikkeukset käsitelty järkevästi

### Siisteys
- [ ] Ei kommentoitua koodia
- [ ] Ei käyttämättömiä muuttujia tai using-lauseita
- [ ] Tyhjät rivit erottelevat loogiset kokonaisuudet
- [ ] Koodi noudattaa [koodauskäytäntöjä](../00-Basics/Coding-Conventions.md)

---

## Yhteenveto

| Periaate | Ydinsanoma |
|----------|------------|
| **DRY** | Älä toista itseäsi — erota yhteinen logiikka |
| **KISS** | Pidä yksinkertaisena — älä ylimonimutkaistu |
| **YAGNI** | Koodaa vain se mitä nyt tarvitaan |
| **Guard Clauses** | Käsittele virhetilanteet heti alussa |
| **Small Methods** | Yksi metodi = yksi asia |
| **Good Naming** | Koodi selittää itse itsensä |
| **SOLID** | Viisi periaatetta laadukkaaseen olio-ohjelmointiin |
| **SoC** | Pidä vastuualueet erillään |
| **Loose Coupling** | Riippu rajapinnoista, ei toteutuksista |
| **Composition** | Suosi koostumusta perimisen sijaan |
| **Fail Fast** | Tarkista edellytykset alussa |
| **Boy Scout Rule** | Jätä koodi parempaan kuntoon kuin löysit |

### Muista

Nämä ovat **ohjeita**, eivät lakeja. Joskus paras ratkaisu rikkoo jotain periaatetta — ja se on ok, kunhan tiedät miksi. Tärkeintä on, että **ymmärrät** periaatteet ja **tietoisesti** päätät milloin niistä poiketa.

## Hyödyllisiä linkkejä

- [SOLID-periaatteet (kattava materiaali)](SOLID.md)
- [Dependency Injection](Dependency-Injection.md)
- [Suunnittelumallit (Design Patterns)](Design-Patterns.md)
- [Koodauskäytännöt](../00-Basics/Coding-Conventions.md)
- [Clean Code - Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [SOLID Principles in C#](https://www.c-sharpcorner.com/UploadFile/damubetha/solid-principles-in-C-Sharp/)
- [Microsoft - Architectural Principles](https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles)
- [Refactoring Guru - Code Smells](https://refactoring.guru/refactoring/smells)

Seuraavaksi: [SOLID-periaatteet (syvempi materiaali)](SOLID.md)
