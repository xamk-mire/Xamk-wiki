# Pagination (Sivutus)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi paginaatio on tärkeä?](#miksi-paginaatio-on-tärkeä)
3. [Pagination-strategiat](#pagination-strategiat)
4. [Offset-based Pagination](#offset-based-pagination)
5. [Cursor-based Pagination](#cursor-based-pagination)
6. [PagedResult Pattern](#pagedresult-pattern)
7. [Mihin kerrokseen sivutus kuuluu](#mihin-kerrokseen-sivutus-kuuluu)
8. [Milloin sivutusta ei tarvita](#milloin-sivutusta-ei-tarvita)
9. [API Design](#api-design)
10. [Performance-näkökulmat](#performance-näkökulmat)
11. [Best Practices](#best-practices)
12. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Paginaatio** (pagination, sivutus) on tekniikka, jossa suuret tietomäärät jaetaan pienempiin sivuihin (pages). Paginaatio on olennainen osa modernia web- ja API-kehitystä.

---

## Miksi paginaatio on tärkeä?

### Ongelma: Kaikki tulokset kerralla

```http
GET /api/users
```

**Palauttaa:**
```json
[
  { "id": 1, "name": "User 1" },
  { "id": 2, "name": "User 2" },
  ...
  { "id": 10000, "name": "User 10000" }
]
```

**Ongelmia:**

1. **Performance** 🐌
   - 10,000 riviä tietokannasta
   - Sarjallistaminen JSON:ksi
   - Verkon kautta siirtäminen

2. **Muisti** 💾
   - Server: 10,000 oliota muistissa
   - Client: Suuri JSON parseriin
   - Browser: DOM-renderöinti

3. **Käyttökokemus** 😵
   - Käyttäjä ei jaksa selata 10,000 tulosta
   - Pitkä latausaika
   - Huono responssi

4. **Kaistanleveys** 📡
   - Suuri JSON-payload
   - Mobiilikäyttäjät kärsivät
   - Turha datan siirto

### Ratkaisu: Paginaatio

```http
GET /api/users?page=1&pageSize=20
```

**Palauttaa:**
```json
{
  "items": [
    { "id": 1, "name": "User 1" },
    ...
    { "id": 20, "name": "User 20" }
  ],
  "page": 1,
  "pageSize": 20,
  "totalCount": 10000,
  "totalPages": 500
}
```

**Edut:**
- ✅ Nopea vastaus (20 riviä vs. 10,000)
- ✅ Vähän muistia
- ✅ Hyvä UX (käyttäjä näkee tulokset heti)
- ✅ Vähemmän kaistanleveyttä

---

## Pagination-strategiat

### 1. Offset-based Pagination (Skip/Take)

**Yleisin ja yksinkertaisin.**

```sql
SELECT * FROM Users
ORDER BY Id
OFFSET 20 ROWS
FETCH NEXT 20 ROWS ONLY
```

```csharp
var users = _context.Users
    .OrderBy(u => u.Id)
    .Skip(20)      // Skip first 20
    .Take(20)      // Take next 20
    .ToList();
```

**Edut:**
- ✅ Yksinkertainen toteuttaa
- ✅ Voit hypätä mille tahansa sivulle
- ✅ Helppo laskea sivujen määrä
- ✅ Sopii UI:hin jossa on sivunumerot

**Haitat:**
- ❌ Performance heikkenee suurilla offset-arvoilla
- ❌ Epäjohdonmukainen jos data muuttuu (items "liikkuvat")
- ❌ Tietokanta joutuu skannaamaan kaikki skipatut rivit

### 2. Cursor-based Pagination (Keyset Pagination)

**Tehokkaampi suurilla datamäärillä.**

```http
GET /api/users?cursor=123&limit=20
```

```csharp
var users = _context.Users
    .Where(u => u.Id > cursor)
    .OrderBy(u => u.Id)
    .Take(20)
    .ToList();
```

> **Huom:** Cursor-kentän tyyppi riippuu pääavaimen tyypistä. Numeerisilla ID:illä käytetään `>` -vertailua, merkkijonopohjaisilla `CompareTo`:ta.

**Edut:**
- ✅ Parempi performance (ei skannaa ohitettuja rivejä)
- ✅ Johdonmukainen vaikka data muuttuu
- ✅ Sopii infinite scroll -tyyppisiin UI:hin

**Haitat:**
- ❌ Monimutkaisempi toteuttaa
- ❌ Et voi hypätä suoraan sivulle X
- ❌ Vaikea laskea sivujen määrä

### Sivunumero ei ole kolmas strategia

Usein näkee puhuttavan erikseen "page number" -sivutuksesta:

```http
GET /api/users?page=5&pageSize=20
```

Se **ei ole eri strategia** kuin offset-based. Se on sama asia asiakkaan näkökulmasta: asiakas antaa sivun numeron ja sivukoon, ja palvelin laskee niistä offsetin kaavalla `(page - 1) * pageSize`. Tietokantakysely on sama Skip/Take, joten edut ja haitat ovat samat.

Erot ovat vain parametrien nimissä:

| Asiakas lähettää | Palvelin tekee |
|------------------|----------------|
| `page=5&pageSize=20` | `Skip(80).Take(20)` |
| `offset=80&limit=20` | `Skip(80).Take(20)` |

Todellisia strategioita on siis kaksi: offset-based ja cursor-based.

---

## Offset-based Pagination

### Toteutus

**1. Query Parameters:**

```http
GET /api/users?page=2&pageSize=10
```

**2. Laskenta:**

```
page = 2
pageSize = 10

offset = (page - 1) * pageSize = (2 - 1) * 10 = 10
```

**3. SQL:**

```sql
SELECT * FROM Users
ORDER BY Id
OFFSET 10 ROWS
FETCH NEXT 10 ROWS ONLY
```

**4. LINQ:**

```csharp
var page = 2;
var pageSize = 10;

var users = _context.Users
    .OrderBy(u => u.Id)
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToList();
```

### Esimerkki

```csharp
public async Task<PagedResult<UserDto>> GetUsersPagedAsync(
    int page, 
    int pageSize)
{
    // Virheelliset arvot korjataan tässä sallittuun arvoon (clamp).
    // Toinen vaihtoehto on vastata 400 - ks. Best Practices 1.
    if (page < 1) page = 1;
    if (pageSize < 1) pageSize = 10;
    if (pageSize > 100) pageSize = 100; // Max 100 per page
    
    // Get total count (for metadata)
    var totalCount = await _context.Users.CountAsync();
    
    // Get paged data
    var users = await _context.Users
        .OrderBy(u => u.CreatedAt)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(u => new UserDto
        {
            Id = u.Id,
            Name = u.Name,
            Email = u.Email
        })
        .ToListAsync();
    
    // Return paged result
    return new PagedResult<UserDto>(users, page, pageSize, totalCount);
}
```

---

## Cursor-based Pagination

### Toteutus

**1. Request:**

```http
GET /api/users?cursor=20&limit=20
```

`cursor` on edellisen sivun viimeisen rivin Id. Ensimmäisellä pyynnöllä sitä ei anneta.

**2. SQL (periaate):**

```sql
SELECT * FROM Users
WHERE Id > @cursor
ORDER BY Id
FETCH FIRST 20 ROWS ONLY
```

**3. LINQ:**

```csharp
public async Task<CursorPagedResult<UserDto>> GetUsersAsync(
    int? cursor,
    int limit = 20)
{
    IQueryable<User> query = _context.Users;
    
    if (cursor.HasValue)
    {
        query = query.Where(u => u.Id > cursor.Value);
    }
    
    var users = await query
        .OrderBy(u => u.Id)
        .Take(limit + 1) // Take one extra to check if there's more
        .Select(u => new UserDto
        {
            Id = u.Id,
            Name = u.Name,
            Email = u.Email
        })
        .ToListAsync();
    
    var hasMore = users.Count > limit;
    if (hasMore)
        users.RemoveAt(users.Count - 1); // Remove extra
    
    // int? - null tarkoittaa, että seuraavaa sivua ei ole
    int? nextCursor = hasMore ? users.Last().Id : null;
    
    return new CursorPagedResult<UserDto>
    {
        Items = users,
        NextCursor = nextCursor,
        HasMore = hasMore
    };
}
```

**4. Response:**

```json
{
  "items": [
    { "id": 21, "name": "User 21" },
    ...
    { "id": 40, "name": "User 40" }
  ],
  "nextCursor": 40,
  "hasMore": true
}
```

Seuraava sivu haetaan pyynnöllä `GET /api/users?cursor=40&limit=20`.

---

## PagedResult Pattern

Sivutettu vastaus ei ole pelkkä lista. Asiakas tarvitsee rivien lisäksi tiedon siitä, mikä osa kokonaisuudesta sillä on kädessään. `PagedResult` on vastauksen kääre, jossa nämä tiedot kulkevat rivien mukana.

| Kenttä | Mitä se tarkoittaa |
|--------|--------------------|
| **Sivu** (`page`) | Monesko sivu tämä on. Numerointi alkaa yleensä ykkösestä. |
| **Sivukoko** (`pageSize`) | Kuinka monta riviä yhdelle sivulle enintään tulee. Viimeisellä sivulla rivejä voi olla vähemmän. |
| **Kokonaismäärä** (`totalCount`) | Kuinka monta riviä hakuehtoon osuu yhteensä, kaikilla sivuilla. |

Miksi asiakas tarvitsee kokonaismäärän? Ilman sitä asiakas ei tiedä, onko seuraavaa sivua olemassa eikä montako sivua on. Kokonaismäärästä ja sivukoosta lasketaan sivujen määrä, ja käyttöliittymä voi näyttää sivunumerot ja tekstin "näytetään 11–20 / 150". Palvelin on ainoa, joka tietää määrän, koska asiakkaalla on vain yksi sivu.

Sivu ja sivukoko palautetaan vastauksessa, vaikka asiakas lähetti ne itse. Palvelin on voinut käyttää oletusarvoa tai rajata liian suuren sivukoon, ja vastaus kertoo, mitä arvoja oikeasti käytettiin.

### Generic Wrapper

```csharp
public class PagedResult<T>
{
    public List<T> Items { get; set; } = new();
    public int Page { get; set; }
    public int PageSize { get; set; }
    public int TotalCount { get; set; }
    public int TotalPages { get; set; }
    public bool HasPreviousPage => Page > 1;
    public bool HasNextPage => Page < TotalPages;
    
    public PagedResult()
    {
    }
    
    public PagedResult(List<T> items, int page, int pageSize, int totalCount)
    {
        Items = items;
        Page = page;
        PageSize = pageSize;
        TotalCount = totalCount;
        TotalPages = (int)Math.Ceiling(totalCount / (double)pageSize);
    }
}
```

### Käyttö

```csharp
// Service
var result = new PagedResult<UserDto>(
    users,
    page: 2,
    pageSize: 10,
    totalCount: 150
);

// result.TotalPages = Ceiling(150 / 10) = 15
// result.HasPreviousPage = true (page 2 > 1)
// result.HasNextPage = true (page 2 < 15)
```

### API Response

```json
{
  "items": [
    { "id": 11, "name": "User 11" },
    ...
    { "id": 20, "name": "User 20" }
  ],
  "page": 2,
  "pageSize": 10,
  "totalCount": 150,
  "totalPages": 15,
  "hasPreviousPage": true,
  "hasNextPage": true
}
```

---

## Mihin kerrokseen sivutus kuuluu

Sivutus on **lupaus rajapinnan sopimuksessa**: "tämä lista palautetaan sivuina, ja vastaus kertoo sivun, sivukoon ja kokonaismäärän". Lupaus tehdään API-kerroksessa, mutta itse rajaus tehdään tietokannassa.

Parametrit kulkevat kerrosten läpi:

```
API (controller)        Lukee page ja pageSize, tarkistaa ne
      ↓
Application (use case)  Välittää parametrit eteenpäin
      ↓
Repository              Tekee Skip/Take-kyselyn ja laskee kokonaismäärän
      ↓
Tietokanta              Palauttaa vain pyydetyn sivun rivit
```

```csharp
// Repository: rajaus tehdään tietokannassa
public async Task<PagedResult<Match>> GetPagedAsync(int page, int pageSize)
{
    var totalCount = await _context.Matches.CountAsync();

    var items = await _context.Matches
        .OrderBy(m => m.PlayedAt)
        .ThenBy(m => m.Id)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .ToListAsync();

    return new PagedResult<Match>(items, page, pageSize, totalCount);
}
```

**Älä koskaan hae kaikkea ja leikkaa muistissa.** Tämä näyttää toimivalta, mutta kumoaa sivutuksen hyödyn:

```csharp
// ❌ Huono - koko taulu haetaan muistiin, sivu leikataan vasta sitten
var all = await _repository.GetAllAsync();
var pageItems = all.Skip((page - 1) * pageSize).Take(pageSize).ToList();
```

Asiakas saa oikean kokoisen vastauksen, mutta palvelin ja tietokanta tekevät silti koko työn joka pyynnöllä. Sama virhe syntyy, jos `ToListAsync()` kutsutaan ennen `Skip`- ja `Take`-kutsuja.

Katso myös [Repository Pattern](Repository-Pattern.md).

---

## Milloin sivutusta ei tarvita

Sivutus ei kuulu jokaiseen listaan. Sitä ei tarvita, kun lista on **luonnostaan pieni** ja sen rivit **kuuluvat yhteen**.

| Lista | Miksi sivuja ei tarvita |
|-------|-------------------------|
| Juuri nyt vapaana olevat ajat tai tilat | Rivejä on vähän, ja käyttäjä haluaa nähdä ne kaikki kerralla |
| Yhden sarjan joukkueet | Enintään kymmeniä rivejä, ja sarjataulukko näytetään kokonaisena |
| Valintalistan vaihtoehdot (esim. tilatyypit) | Määrä on pieni ja pysyy pienenä |

Näissä sivutus toisi vain lisää edestakaisia pyyntöjä ja lisää koodia asiakkaalle, eikä säästäisi mitään.

Kysy kaksi asiaa:

1. **Voiko lista kasvaa rajatta?** Ottelut, varaukset ja tilaukset kertyvät ajan myötä, joten ne sivutetaan. Yhden sarjan joukkueet eivät kerry.
2. **Tarvitseeko käyttäjä koko listan kerralla?** Jos tarvitsee ja lista on pieni, palauta se kokonaan.

Kun jätät sivutuksen pois, kirjoita syy rajapinnan kuvaukseen. Silloin valinta on päätös eikä unohdus.

---

## API Design

### 1. Query Parameters

**Standard:**

```http
GET /api/users?page=2&pageSize=20
```

**Alternatiivit:**

```http
GET /api/users?page=2&limit=20
GET /api/users?offset=20&limit=20
GET /api/users?skip=20&take=20
```

### 2. Response Headers (GitHub-tyyli)

**Headers:**
```
Link: <https://api.example.com/users?page=3>; rel="next",
      <https://api.example.com/users?page=1>; rel="prev",
      <https://api.example.com/users?page=10>; rel="last",
      <https://api.example.com/users?page=1>; rel="first"
X-Total-Count: 150
X-Page-Count: 15
```

**Body:** Vain items (ei meta-dataa)
```json
[
  { "id": 11, "name": "User 11" },
  ...
]
```

### 3. Envelope Pattern (suositeltu)

**Body:** Sekä items että meta-data

```json
{
  "data": [
    { "id": 11, "name": "User 11" },
    ...
  ],
  "pagination": {
    "page": 2,
    "pageSize": 10,
    "totalCount": 150,
    "totalPages": 15,
    "hasNext": true,
    "hasPrevious": true
  }
}
```

### 4. HATEOAS (Hypermedia)

```json
{
  "items": [...],
  "links": {
    "self": "/api/users?page=2",
    "first": "/api/users?page=1",
    "prev": "/api/users?page=1",
    "next": "/api/users?page=3",
    "last": "/api/users?page=15"
  },
  "page": 2,
  "totalPages": 15
}
```

---

## Performance-näkökulmat

### 1. Offset-based Performance

**Ongelma suurilla offset-arvoilla:**

```sql
SELECT * FROM Users
ORDER BY Id
OFFSET 900000 ROWS
FETCH NEXT 100 ROWS ONLY
```

Tietokanta joutuu **skannaamaan 900,000 riviä** vaikka palauttaa vain 100!

**Ratkaisu:**
- Käytä cursor-based paginationia suurilla datamäärillä
- Rajoita max page-numero (esim. max 100 sivua)
- Lisää indeksi ORDER BY -kenttään

### 2. COUNT(*) Performance

```csharp
var totalCount = await _context.Users.CountAsync();
```

`COUNT(*)` voi olla hidas suurissa tauluissa.

**Optimoinnit:**

**Option 1:** Cache totalCount

```csharp
var totalCount = _cache.GetOrCreate("users_count", entry =>
{
    entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);
    return _context.Users.Count();
});
```

**Option 2:** Approximate count

```sql
-- PostgreSQL
SELECT reltuples::bigint AS estimate
FROM pg_class
WHERE relname = 'users';
```

**Option 3:** Älä näytä totalCount:ia

```json
{
  "items": [...],
  "hasMore": true  // Vain "onko lisää?"
}
```

### 3. N+1 Problem

**Ongelma:**

```csharp
var orders = await _context.Orders
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync();

foreach (var order in orders)
{
    // N queries!
    order.Customer = await _context.Customers.FindAsync(order.CustomerId);
}
```

**Ratkaisu: Eager Loading**

```csharp
var orders = await _context.Orders
    .Include(o => o.Customer)  // ← Single JOIN
    .Skip((page - 1) * pageSize)
    .Take(pageSize)
    .ToListAsync();
```

---

## Best Practices

### 1. Validoi parametrit

Asiakas voi lähettää virheellisen arvon, esimerkiksi `page=0` tai `pageSize=100000`. Vaihtoehtoja on kaksi:

- **Vastaa 400 Bad Request.** Asiakas saa tietää, että pyyntö oli virheellinen.
- **Korjaa arvo sallittuun rajaan (clamp).** Pyyntö onnistuu, ja vastauksen `page` ja `pageSize` kertovat, mitä arvoja käytettiin.

Kumpikin käy. Tärkeää on, että valinta on **tehty tietoisesti ja dokumentoitu** rajapinnan kuvaukseen, ja että se on sama kaikissa listoissa. Alla oleva esimerkki korjaa arvon.

```csharp
public class PaginationRequest
{
    private int _page = 1;
    private int _pageSize = 10;
    
    public int Page
    {
        get => _page;
        set => _page = value < 1 ? 1 : value;
    }
    
    public int PageSize
    {
        get => _pageSize;
        set => _pageSize = value switch
        {
            < 1 => 10,
            > 100 => 100,  // Max 100 items
            _ => value
        };
    }
}
```

### 2. Käytä oletusarvoja

```csharp
[HttpGet]
public async Task<PagedResult<UserDto>> GetUsers(
    [FromQuery] int page = 1,      // ← Default 1
    [FromQuery] int pageSize = 10) // ← Default 10
{
    // ...
}
```

### 3. Dokumentoi rajat

```csharp
/// <summary>
/// Get paginated users
/// </summary>
/// <param name="page">Page number (1-based). Default: 1</param>
/// <param name="pageSize">Items per page. Default: 10, Max: 100</param>
[HttpGet]
public async Task<PagedResult<UserDto>> GetUsers(
    int page = 1, 
    int pageSize = 10)
{
    // ...
}
```

### 4. Palauta aina meta-data

```json
{
  "items": [...],
  "page": 2,
  "pageSize": 10,
  "totalCount": 150,
  "totalPages": 15,
  "hasNext": true,
  "hasPrevious": true
}
```

Client tarvitsee tämän navigointiin!

### 5. Käytä johdonmukaista järjestystä

```csharp
// ❌ Huono - Ei järjestystä
var users = _context.Users
    .Skip(...)
    .Take(...)
    .ToList();  // Random order!

// ✅ Hyvä - Aina sama järjestys
var users = _context.Users
    .OrderByDescending(u => u.CreatedAt)  // Newest first
    .ThenBy(u => u.Id)  // Secondary sort
    .Skip(...)
    .Take(...)
    .ToList();
```

### 6. Indeksoi ORDER BY -kentät

```sql
CREATE INDEX idx_users_created_at ON Users(CreatedAt DESC, Id);
```

Ilman indeksiä paginaatio on hidasta!

---

## Yhteenveto

### Keskeiset opit

**Miksi paginaatio?**
- Performance
- Muisti
- Käyttökokemus
- Kaistanleveys

**Pagination-strategiat:**

| Strategia | Käyttötapaus | Edut | Haitat |
|-----------|--------------|------|--------|
| **Offset-based** | Yleisin, sivunumerot | Yksinkertainen, hyppy mille tahansa sivulle | Performance suurilla offset:illa |
| **Cursor-based** | Infinite scroll, suuret datamäärät | Parempi performance | Ei voi hypätä sivulle |

Sivunumero (`page` + `pageSize`) on offset-based-sivutus asiakkaan näkökulmasta, ei kolmas strategia.

**Kerros ja rajaus:**
- Sivutus on rajapinnan lupaus; Skip/Take tehdään repositoryssä tietokantaa vasten
- Älä hae kaikkea ja leikkaa muistissa
- Luonnostaan pientä, yhteen kuuluvaa listaa ei sivuteta

**Best Practices:**
- Validoi parametrit (page > 0, pageSize <= 100): vastaa 400 tai korjaa arvo, ja dokumentoi valinta
- Käytä oletusarvoja
- Palauta meta-data (page, totalPages, hasNext)
- Indeksoi ORDER BY -kentät
- Dokumentoi rajat

**Performance:**
- Offset-based hidastuu suurilla offset:illa
- COUNT(*) voi olla kallis → cache tai approximate
- Eager load related data (N+1)

### Milloin käyttää mitäkin?

**Offset-based:**
- Pienet-keskisuuret datamäärät (< 100,000 riviä)
- UI jossa sivunumerot
- Tarvitset totalPages-tiedon

**Cursor-based:**
- Suuret datamäärät (> 1M riviä)
- Infinite scroll UI
- Real-time data (chat, feed)

### Seuraavat askeleet

- Kokeile molempia strategioita
- Mittaa performance omassa sovelluksessasi
- Tutustu [Result Pattern](Result-Pattern.md)
- Lue [Clean Architecture](../Architecture/Clean-Architecture.md)

---

**Muista:** Paginaatio on välttämätön suurissa sovelluksissa. Valitse strategia käyttötapauksen mukaan!
