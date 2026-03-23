# Health Checks (Terveystarkistukset)

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Miksi Health Checks?](#miksi-health-checks)
3. [ASP.NET Core Health Checks](#aspnet-core-health-checks)
4. [Custom Health Checks](#custom-health-checks)
5. [Health Check -vastausmuodot](#health-check--vastausmuodot)
6. [Health Checks tuotannossa](#health-checks-tuotannossa)
7. [Best Practices](#best-practices)
8. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Health Check** on HTTP-endpoint, joka kertoo onko sovellus toimintakunnossa. Se vastaa yksinkertaiseen kysymykseen: **"Onko tämä palvelu kunnossa?"**

**Perusidea:**

```
GET /health  →  200 OK   { "status": "Healthy" }     ✅ Kaikki kunnossa
GET /health  →  503      { "status": "Unhealthy" }   ❌ Jokin vialla
GET /health  →  200 OK   { "status": "Degraded" }    ⚠️ Toimii, mutta osittain
```

Health checkit ovat välttämättömiä tuotannossa — ne mahdollistavat automaattisen monitoroinnin, kuormantasauksen ja ongelmien havaitsemisen ennen kuin käyttäjät huomaavat ne.

---

## Miksi Health Checks?

### Tuotantoympäristön haasteet

Sovellus voi olla "käynnissä" mutta silti rikki:

```
✅ Prosessi pyörii               ... mutta tietokanta on alhaalla
✅ HTTP-portti kuuntelee          ... mutta muisti on lopussa
✅ DNS resolvoituu                ... mutta ulkoinen API ei vastaa
```

### Hyödyt

| Hyöty | Selitys |
|-------|---------|
| **Automaattinen monitorointi** | Azure, Docker, Kubernetes tarkistavat sovelluksen tilan säännöllisesti |
| **Kuormantasaus** | Load balancer ohjaa liikenteen pois epäterveistä instansseista |
| **Automaattinen uudelleenkäynnistys** | Kubernetes käynnistää epäterveen podin uudelleen |
| **Nopea vianhaku** | Näet heti mikä komponentti on rikki |
| **Deployment-varmistus** | Uusi versio tarkistetaan ennen liikenteen ohjaamista sille |

### Ilman Health Checkia

```
1. Tietokanta kaatuu
2. Käyttäjät raportoivat ongelmista
3. Kehittäjä tutkii lokeista
4. 30 min myöhemmin ongelma löytyy
```

### Health Checkin kanssa

```
1. Tietokanta kaatuu
2. Health check havaitsee: "Unhealthy - Database connection failed"
3. Load balancer ohjaa liikenteen terveelle instanssille
4. Hälytys kehittäjälle — korjaa ongelma
```

---

## ASP.NET Core Health Checks

ASP.NET Core tarjoaa sisäänrakennetun Health Checks -middlewaren.

### Perusasennus

```csharp
// Program.cs

// 1. Rekisteröi Health Checks -palvelut
builder.Services.AddHealthChecks();

var app = builder.Build();

// 2. Mappaa endpoint
app.MapHealthChecks("/health");

app.Run();
```

Nyt `GET /health` palauttaa:

```
HTTP/1.1 200 OK
Content-Type: text/plain

Healthy
```

### Tietokantatarkistus

EF Core -health check tarkistaa, vastaako tietokanta:

```bash
dotnet add package Microsoft.Extensions.Diagnostics.HealthChecks.EntityFrameworkCore
```

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>("database");
```

Nyt health check testaa automaattisesti tietokantayhteyden. Jos tietokanta on alhaalla, endpoint palauttaa `503 Service Unavailable`.

### Ulkoisten palveluiden tarkistus

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>("database")
    .AddUrlGroup(new Uri("https://api.example.com/health"), "external-api")
    .AddCheck("disk-space", () =>
    {
        var drive = new DriveInfo("C");
        long freeSpaceGB = drive.AvailableFreeSpace / (1024 * 1024 * 1024);

        return freeSpaceGB > 1
            ? HealthCheckResult.Healthy($"Free space: {freeSpaceGB} GB")
            : HealthCheckResult.Unhealthy($"Low disk space: {freeSpaceGB} GB");
    });
```

---

## Custom Health Checks

Voit luoda omia health check -luokkia monimutkaisia tarkistuksia varten.

### IHealthCheck-rajapinta

```csharp
public class DatabaseHealthCheck : IHealthCheck
{
    private readonly AppDbContext _db;

    public DatabaseHealthCheck(AppDbContext db)
    {
        _db = db;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            await _db.Database.CanConnectAsync(cancellationToken);

            int bookingCount = await _db.Bookings.CountAsync(cancellationToken);

            return HealthCheckResult.Healthy(
                $"Database OK. Bookings: {bookingCount}");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy(
                "Database connection failed",
                exception: ex);
        }
    }
}
```

### Rekisteröinti

```csharp
builder.Services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database");
```

### Health Check -tilat

| Tila | HTTP-koodi | Merkitys |
|------|-----------|---------|
| `Healthy` | 200 | Kaikki kunnossa |
| `Degraded` | 200 | Toimii, mutta suorituskyky heikentynyt tai ei-kriittinen komponentti rikki |
| `Unhealthy` | 503 | Palvelu ei toimi kunnolla |

```csharp
public async Task<HealthCheckResult> CheckHealthAsync(
    HealthCheckContext context,
    CancellationToken cancellationToken = default)
{
    double responseTimeMs = await MeasureResponseTimeAsync();

    if (responseTimeMs < 100)
        return HealthCheckResult.Healthy($"Response time: {responseTimeMs}ms");

    if (responseTimeMs < 500)
        return HealthCheckResult.Degraded($"Slow response: {responseTimeMs}ms");

    return HealthCheckResult.Unhealthy($"Too slow: {responseTimeMs}ms");
}
```

---

## Health Check -vastausmuodot

Oletuksena health check palauttaa pelkän tekstin ("Healthy"). JSON-muoto on hyödyllisempi:

### JSON-vastaus

```csharp
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";

        var response = new
        {
            status = report.Status.ToString(),
            totalDuration = report.TotalDuration.TotalMilliseconds + "ms",
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                description = e.Value.Description,
                duration = e.Value.Duration.TotalMilliseconds + "ms"
            })
        };

        await context.Response.WriteAsJsonAsync(response);
    }
});
```

**Vastaus:**

```json
{
  "status": "Healthy",
  "totalDuration": "45ms",
  "checks": [
    {
      "name": "database",
      "status": "Healthy",
      "description": "Database OK. Bookings: 142",
      "duration": "12ms"
    },
    {
      "name": "external-api",
      "status": "Healthy",
      "description": null,
      "duration": "31ms"
    }
  ]
}
```

### Erillisiä endpointeja eri tarkoituksiin

```csharp
// Liveness — "Onko prosessi käynnissä?"
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false  // Ei ajeta mitään tarkistuksia
});

// Readiness — "Onko palvelu valmis vastaanottamaan liikennettä?"
app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

// Täysi tarkistus
app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = WriteJsonResponse
});
```

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>("database", tags: new[] { "ready" })
    .AddCheck("memory", () =>
    {
        long memoryMB = GC.GetTotalMemory(false) / (1024 * 1024);
        return memoryMB < 500
            ? HealthCheckResult.Healthy($"Memory: {memoryMB} MB")
            : HealthCheckResult.Unhealthy($"High memory: {memoryMB} MB");
    }, tags: new[] { "ready" });
```

---

## Health Checks tuotannossa

### Azure App Service

Azure App Service tukee health check -endpointeja natiivisti:

1. **Azure Portal** → App Service → **Health check**
2. Aseta polku: `/health`
3. Azure tarkistaa endpointin minuutin välein
4. Jos endpoint palauttaa 5xx tai ei vastaa → instanssi merkitään epäterveeksi

### Docker / Docker Compose

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

```yaml
# docker-compose.yml
services:
  api:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

### Kubernetes

```yaml
# Liveness probe — käynnistetäänkö pod uudelleen?
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 15

# Readiness probe — ohjataanko liikennettä tälle podille?
readinessProbe:
  httpGet:
    path: /health/ready
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
```

---

## Best Practices

### 1. Pidä health check kevyenä

```csharp
// ✅ Nopea tarkistus — "voiko yhdistää?"
await _db.Database.CanConnectAsync(ct);

// ❌ Raskas operaatio health checkissä
var allOrders = await _db.Orders.Include(o => o.Items).ToListAsync();
```

### 2. Erota liveness ja readiness

- **Liveness**: Onko prosessi elossa? (ei tarvitse tarkistaa riippuvuuksia)
- **Readiness**: Onko palvelu valmis käsittelemään pyyntöjä? (tarkistaa tietokannan ym.)

### 3. Lisää tagit health checkeihin

```csharp
builder.Services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database", tags: new[] { "ready", "critical" })
    .AddCheck<CacheHealthCheck>("cache", tags: new[] { "ready" })
    .AddCheck<EmailHealthCheck>("email", tags: new[] { "non-critical" });
```

### 4. Älä paljasta arkaluonteista tietoa

```csharp
// ❌ Älä paljasta connection stringiä tai sisäisiä virheitä
return HealthCheckResult.Unhealthy($"Failed: {connectionString}");

// ✅ Yleisluontoinen virheilmoitus
return HealthCheckResult.Unhealthy("Database connection failed");
```

### 5. Aseta timeout

```csharp
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>("database",
        timeout: TimeSpan.FromSeconds(5));
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Health Check** | HTTP-endpoint joka kertoo palvelun tilan |
| **Healthy** | 200 — kaikki kunnossa |
| **Degraded** | 200 — toimii mutta heikentynyt |
| **Unhealthy** | 503 — palvelu ei toimi |
| **Liveness** | "Onko prosessi elossa?" — ei tarkistuksia |
| **Readiness** | "Voiko vastaanottaa liikennettä?" — tarkistaa riippuvuudet |
| **IHealthCheck** | Rajapinta custom-tarkistuksille |
| **Tags** | Mahdollistavat endpointtikohtaisen filtteröinnin |

**Muista:**
- Health check on **pakollinen** tuotantosovelluksissa
- Pidä tarkistukset **kevyinä** ja **nopeina**
- Erota **liveness** ja **readiness** -tarkistukset
- Palauta **JSON** yksityiskohtaista diagnostiikkaa varten
- **Älä paljasta** arkaluonteista tietoa vastauksissa

---

## Hyödyllisiä linkkejä

- [Microsoft: Health checks in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/health-checks)
- [Microsoft: Monitor ASP.NET Core apps](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/health-checks)
- [AspNetCore.Diagnostics.HealthChecks (NuGet)](https://github.com/Xabaril/AspNetCore.Diagnostics.HealthChecks) — valmiita health checkejä (SQL Server, Redis, Azure Storage, ym.)
