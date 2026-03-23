# Azure Functions — Serverless-sovellukset

## Sisällysluettelo

1. [Mikä on Serverless?](#mikä-on-serverless)
2. [Mikä on Azure Functions?](#mikä-on-azure-functions)
3. [Hosting-mallit](#hosting-mallit)
4. [Triggerit](#triggerit)
5. [Bindings — Input ja Output](#bindings--input-ja-output)
6. [Azure Functions .NET:llä](#azure-functions-netllä)
7. [Paikallinen kehitys](#paikallinen-kehitys)
8. [Julkaisu Azureen](#julkaisu-azureen)
9. [Durable Functions](#durable-functions)
10. [Azure Functions vs. App Service](#azure-functions-vs-app-service)
11. [Best Practices](#best-practices)
12. [Yhteenveto](#yhteenveto)

---

## Mikä on Serverless?

**Serverless** ei tarkoita, ettei palvelimia ole — vaan sitä, ettei kehittäjän tarvitse huolehtia niistä. Pilvipalvelu hallinnoi palvelimia, skaalautumista ja resursseja automaattisesti.

### Perinteinen vs. Serverless

```
Perinteinen (App Service / VM):
┌────────────────────────────────────────┐
│  Palvelin pyörii 24/7                  │
│  → Maksat koko ajan                    │
│  → Skaalaat manuaalisesti              │
│  → Hallinnoit infrastruktuuria         │
└────────────────────────────────────────┘

Serverless (Azure Functions):
┌────────────────────────────────────────┐
│  Funktio suoritetaan vain tarvittaessa │
│  → Maksat vain suorituksista           │
│  → Skaalautuu automaattisesti          │
│  → Ei infrastruktuuria hallinnoitavana │
└────────────────────────────────────────┘
```

### Serverlessin ominaisuudet

| Ominaisuus | Selitys |
|-----------|---------|
| **Event-driven** | Koodi suoritetaan vain kun jotain tapahtuu (HTTP-pyyntö, ajastin, viesti jonossa) |
| **Pay-per-execution** | Maksat vain suoritusten määrästä ja kestosta |
| **Auto-scaling** | Skaalautuu nollasta tuhansiin instansseihin automaattisesti |
| **Ei palvelinhallintaa** | Azure huolehtii kaikesta infrastruktuurista |
| **Stateless** | Funktiot eivät säilytä tilaa suoritusten välillä |

---

## Mikä on Azure Functions?

**Azure Functions** on Microsoftin serverless-laskenta-alusta. Se mahdollistaa pienten koodipalojen (funktioiden) suorittamisen ilman sovelluksen tai infrastruktuurin hallintaa.

### Arkkitehtuuri

```
┌─────────────────────────────────────────────────────┐
│  Azure Functions -sovellus (Function App)           │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  Function 1  │  │  Function 2  │                │
│  │  HTTP Trigger │  │  Timer       │                │
│  │              │  │  Trigger     │                │
│  │  GET /api/   │  │  Joka 5 min  │                │
│  │  products    │  │  → siivous   │                │
│  └──────┬───────┘  └──────┬───────┘                │
│         │                 │                         │
│         ▼                 ▼                         │
│  ┌──────────────────────────────┐                  │
│  │  Jaetut palvelut:            │                  │
│  │  - DI Container              │                  │
│  │  - Konfiguraatio             │                  │
│  │  - Logging                   │                  │
│  └──────────────────────────────┘                  │
└─────────────────────────────────────────────────────┘
```

**Function App** = kokoelma funktioita, jotka jakavat saman konfiguraation, hostingin ja skaalauksen.

---

## Hosting-mallit

Azure Functions tarjoaa kolme hosting-mallia:

| Malli | Skaalautuvuus | Hinta | Sopii... |
|-------|--------------|-------|----------|
| **Consumption** | 0 → ∞ automaattisesti | Maksat vain suorituksista | Useimmat käyttötapaukset, prototyypit |
| **Premium** | Esilämmitetyt instanssit | Korkeampi, mutta ei cold startia | Tuotanto, matala latenssi |
| **Dedicated (App Service Plan)** | App Service Plan -resurssit | App Service -hinnoittelu | Kun App Service Plan on jo käytössä |

### Consumption Plan — yksityiskohdat

```
Ilmainen kuukausittainen kiintiö:
- 1 000 000 suoritusta/kk         (ilmainen)
- 400 000 GB-s laskenta-aikaa/kk  (ilmainen)

Sen jälkeen:
- ~0.17 € / miljoona suoritusta
- ~0.000014 € / GB-s
```

**Cold start:** Consumption-mallissa funktio voi olla "nukkumassa" ja ensimmäinen kutsu kestää 1–3 sekuntia ylimääräistä (cold start). Premium-malli eliminoi tämän.

---

## Triggerit

**Trigger** määrittää mikä käynnistää funktion. Jokaisella funktiolla on tasan yksi trigger.

### HTTP Trigger

Funktio suoritetaan kun HTTP-pyyntö saapuu:

```csharp
[Function("GetProducts")]
public async Task<HttpResponseData> GetProducts(
    [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "products")]
    HttpRequestData req)
{
    var products = await _productService.GetAllAsync();

    var response = req.CreateResponse(HttpStatusCode.OK);
    await response.WriteAsJsonAsync(products);
    return response;
}
```

```
GET https://myapp.azurewebsites.net/api/products
```

### Timer Trigger

Funktio suoritetaan ajastimen mukaan (CRON-syntaksi):

```csharp
[Function("CleanupExpiredBookings")]
public async Task CleanupExpired(
    [TimerTrigger("0 0 2 * * *")] TimerInfo timer)
{
    // Suoritetaan joka yö klo 02:00
    await _bookingService.DeleteExpiredAsync();
    _logger.LogInformation("Expired bookings cleaned at {Time}", DateTime.UtcNow);
}
```

**CRON-syntaksi:** `{sekunnit} {minuutit} {tunnit} {päivä} {kuukausi} {viikonpäivä}`

| Lauseke | Merkitys |
|---------|---------|
| `0 */5 * * * *` | Joka 5 minuutti |
| `0 0 * * * *` | Joka tunti |
| `0 0 2 * * *` | Joka yö klo 02:00 |
| `0 0 9 * * 1-5` | Arkipäivinä klo 09:00 |
| `0 30 9 1 * *` | Joka kuun 1. päivä klo 09:30 |

### Queue Trigger

Funktio suoritetaan kun viesti saapuu Azure Storage Queueen:

```csharp
[Function("ProcessOrder")]
public async Task ProcessOrder(
    [QueueTrigger("order-queue")] OrderMessage message)
{
    _logger.LogInformation("Processing order {OrderId}", message.OrderId);
    await _orderService.ProcessAsync(message.OrderId);
}
```

### Blob Trigger

Funktio suoritetaan kun tiedosto lisätään Blob Storageen:

```csharp
[Function("ResizeImage")]
public async Task ResizeImage(
    [BlobTrigger("uploads/{name}")] Stream imageStream,
    string name)
{
    _logger.LogInformation("New image uploaded: {Name}", name);
    await _imageService.ResizeAndSaveAsync(imageStream, name);
}
```

### Triggerien yhteenveto

| Trigger | Käynnistyy kun... | Tyypillinen käyttö |
|---------|-------------------|-------------------|
| **HTTP** | HTTP-pyyntö saapuu | REST API, webhookit |
| **Timer** | Ajastin laukeaa (CRON) | Siivous, raportit, synkronointi |
| **Queue** | Viesti saapuu jonoon | Asynkroninen prosessointi |
| **Blob** | Tiedosto luodaan/muuttuu | Kuvankäsittely, tiedostojen prosessointi |
| **Service Bus** | Viesti Service Bus -jonoon | Mikropalvelukommunikaatio |
| **Cosmos DB** | Dokumentti muuttuu | Change feed -käsittely |
| **Event Hub** | Tapahtuma saapuu | IoT, telemetria, streaming |

---

## Bindings — Input ja Output

**Bindings** yksinkertaistavat Azure-palveluiden käyttöä ilman SDK-koodia.

```
Trigger         →  [Funktio]  →  Output Binding
(mikä käynnistää)  (logiikka)    (minne tulos menee)
```

### Output Binding -esimerkki

Funktio vastaanottaa HTTP-pyynnön ja tallentaa tuloksen jonoon:

```csharp
[Function("CreateOrder")]
[QueueOutput("order-queue")]
public async Task<OrderMessage> CreateOrder(
    [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "orders")]
    HttpRequestData req)
{
    var order = await req.ReadFromJsonAsync<CreateOrderDto>();

    // Paluuarvo menee automaattisesti jonoon (output binding)
    return new OrderMessage
    {
        OrderId = Guid.NewGuid(),
        CustomerEmail = order.Email,
        CreatedAt = DateTime.UtcNow
    };
}
```

### Useita output bindingeja

```csharp
public class MultiOutput
{
    [QueueOutput("notification-queue")]
    public string? QueueMessage { get; set; }

    public HttpResponseData? HttpResponse { get; set; }
}

[Function("CreateAndNotify")]
public async Task<MultiOutput> CreateAndNotify(
    [HttpTrigger(AuthorizationLevel.Anonymous, "post")]
    HttpRequestData req)
{
    var response = req.CreateResponse(HttpStatusCode.Created);
    await response.WriteAsJsonAsync(new { status = "created" });

    return new MultiOutput
    {
        HttpResponse = response,
        QueueMessage = "New order created — send notification"
    };
}
```

---

## Azure Functions .NET:llä

### Isolated Worker Model (suositeltu)

.NET 8+ käyttää **Isolated Worker Model** -mallia, jossa funktiot suoritetaan omassa prosessissaan:

```
┌──────────────────────┐    ┌──────────────────────┐
│  Azure Functions Host │ ←→ │  Worker Process      │
│  (runtime)           │    │  (.NET 8 sovellus)   │
│                      │    │                      │
│  Trigger handling    │    │  Omat funktiot       │
│  Scaling             │    │  DI Container        │
│  Monitoring          │    │  Middleware           │
└──────────────────────┘    └──────────────────────┘
```

### Projektin luominen

```bash
# Luo uusi Azure Functions -projekti
func init MyFunctionApp --worker-runtime dotnet-isolated --target-framework net8.0

# Lisää HTTP-trigger-funktio
func new --name GetProducts --template "HTTP trigger"
```

### Program.cs

```csharp
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = new HostBuilder()
    .ConfigureFunctionsWebApplication()
    .ConfigureServices(services =>
    {
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();

        // Omat palvelut — sama DI kuin ASP.NET Coressa
        services.AddScoped<IProductService, ProductService>();
        services.AddDbContext<AppDbContext>(options =>
            options.UseSqlServer(
                Environment.GetEnvironmentVariable("SqlConnectionString")));
    })
    .Build();

host.Run();
```

### Funktio DI:llä

```csharp
public class ProductFunctions
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductFunctions> _logger;

    public ProductFunctions(
        IProductService productService,
        ILogger<ProductFunctions> logger)
    {
        _productService = productService;
        _logger = logger;
    }

    [Function("GetProducts")]
    public async Task<HttpResponseData> GetAll(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "products")]
        HttpRequestData req)
    {
        _logger.LogInformation("Getting all products");

        var products = await _productService.GetAllAsync();

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(products);
        return response;
    }

    [Function("GetProductById")]
    public async Task<HttpResponseData> GetById(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "products/{id:int}")]
        HttpRequestData req,
        int id)
    {
        var product = await _productService.GetByIdAsync(id);

        if (product is null)
        {
            return req.CreateResponse(HttpStatusCode.NotFound);
        }

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(product);
        return response;
    }

    [Function("CreateProduct")]
    public async Task<HttpResponseData> Create(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "products")]
        HttpRequestData req)
    {
        var dto = await req.ReadFromJsonAsync<CreateProductDto>();
        var product = await _productService.CreateAsync(dto!);

        var response = req.CreateResponse(HttpStatusCode.Created);
        await response.WriteAsJsonAsync(product);
        return response;
    }
}
```

### Konfiguraatio

Azure Functionsin konfiguraatio on `local.settings.json`-tiedostossa (paikallisesti) ja **Application Settings** -asetuksissa (Azuressa):

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "SqlConnectionString": "Server=localhost;Database=MyDb;..."
  }
}
```

> **Huomio:** `local.settings.json` ei lähetetä Azureen — se on vain paikalliseen kehitykseen. Azuressa asetukset asetetaan Application Settings -kohdasta.

---

## Paikallinen kehitys

### Azure Functions Core Tools

```bash
# Asenna Core Tools
npm install -g azure-functions-core-tools@4

# Käynnistä paikallisesti
func start
```

```
Azure Functions Core Tools
Host started, listening on http://localhost:7071

Functions:
    GetProducts: [GET] http://localhost:7071/api/products
    GetProductById: [GET] http://localhost:7071/api/products/{id}
    CreateProduct: [POST] http://localhost:7071/api/products
```

### Azurite — paikallinen Storage-emulaattori

Queue, Blob ja Table trigger vaativat Storage-yhteyden. **Azurite** emuloi Azure Storagea paikallisesti:

```bash
# Asenna
npm install -g azurite

# Käynnistä
azurite --silent --location ./azurite-data
```

`local.settings.json`:ssä `"AzureWebJobsStorage": "UseDevelopmentStorage=true"` ohjaa Azuriteen.

---

## Julkaisu Azureen

### Azure CLI

```bash
# 1. Luo Function App
az functionapp create \
    --resource-group mygroup \
    --consumption-plan-location westeurope \
    --runtime dotnet-isolated \
    --functions-version 4 \
    --name myfunctionapp \
    --storage-account mystorageaccount

# 2. Julkaise
func azure functionapp publish myfunctionapp
```

### Visual Studio / VS Code

- **Visual Studio**: Right-click → Publish → Azure → Function App
- **VS Code**: Azure Functions -laajennus → Deploy to Function App

### GitHub Actions

```yaml
name: Deploy Azure Functions

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '8.0.x'

      - name: Build
        run: dotnet build --configuration Release

      - name: Publish
        run: dotnet publish --configuration Release --output ./publish

      - name: Deploy to Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: myfunctionapp
          package: ./publish
          publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}
```

---

## Durable Functions

**Durable Functions** laajentavat Azure Functionsia mahdollistamalla tilallisia työnkulkuja (workflows). Ne ratkaisevat ongelman: "Miten teen monivaiheisen prosessin serverless-ympäristössä?"

### Function Chaining

Suorita funktiot peräkkäin, jossa edellisen tulos on seuraavan syöte:

```csharp
[Function("OrderOrchestrator")]
public async Task<string> RunOrchestrator(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    // Vaihe 1: Validoi tilaus
    var order = await context.CallActivityAsync<Order>("ValidateOrder", orderId);

    // Vaihe 2: Veloita maksu
    var payment = await context.CallActivityAsync<Payment>("ProcessPayment", order);

    // Vaihe 3: Lähetä vahvistus
    await context.CallActivityAsync("SendConfirmation", payment);

    return "Order processed successfully";
}

[Function("ValidateOrder")]
public async Task<Order> ValidateOrder(
    [ActivityTrigger] string orderId)
{
    // Validointilogiikka...
    return order;
}
```

### Fan-out / Fan-in

Suorita useita tehtäviä rinnakkain ja odota kaikkien valmistumista:

```csharp
[Function("ParallelProcessing")]
public async Task<int[]> RunParallel(
    [OrchestrationTrigger] TaskOrchestrationContext context)
{
    var tasks = new List<Task<int>>();

    // Käynnistä 10 rinnakkaista tehtävää
    for (int i = 0; i < 10; i++)
    {
        tasks.Add(context.CallActivityAsync<int>("ProcessItem", i));
    }

    // Odota kaikkien valmistumista
    int[] results = await Task.WhenAll(tasks);
    return results;
}
```

---

## Azure Functions vs. App Service

| Ominaisuus | Azure Functions | App Service |
|-----------|----------------|-------------|
| **Malli** | Serverless / event-driven | PaaS / always-on |
| **Skaalaus** | 0 → N automaattisesti | Manuaalinen tai autoscale-säännöt |
| **Hinta** | Maksat vain suorituksista | Maksat 24/7 |
| **Cold start** | Kyllä (Consumption) | Ei |
| **Pitkäkestoiset prosessit** | Rajattu (5–10 min) | Ei rajaa |
| **HTTP API** | Yksittäiset endpointit | Täysi MVC/Web API -sovellus |
| **Taustatyöt** | Timer, Queue, Blob trigger | Background services |
| **Monimutkaisuus** | Yksittäiset funktiot | Koko sovellus |

### Milloin Azure Functions?

- ✅ Event-driven -tehtävät (kuva ladattu → pienennä, tilaus luotu → lähetä email)
- ✅ Ajastetut tehtävät (siivous, raportit, synkronointi)
- ✅ Vähäinen liikenne — maksat vain käytöstä
- ✅ Mikropalveluiden yksittäiset operaatiot
- ✅ Webhookit ja integraatiot

### Milloin App Service?

- ✅ Perinteinen REST API kymmenillä endpointeilla
- ✅ Sovellus joka tarvitsee jatkuvaa yhteyttä (WebSocket, SignalR)
- ✅ Pitkäkestoiset prosessit
- ✅ Tasainen, korkea liikenne 24/7
- ✅ Monimutkainen middleware-ketju

---

## Best Practices

### 1. Pidä funktiot pieninä ja fokusoituina

```csharp
// ✅ Yksi funktio, yksi tehtävä
[Function("SendWelcomeEmail")]
public async Task SendWelcomeEmail(
    [QueueTrigger("new-users")] NewUserMessage message) { ... }

// ❌ Yksi funktio tekee kaiken
[Function("HandleEverything")]
public async Task HandleEverything(
    [QueueTrigger("events")] EventMessage message)
{
    if (message.Type == "NewUser") { /* ... */ }
    else if (message.Type == "Order") { /* ... */ }
    else if (message.Type == "Payment") { /* ... */ }
}
```

### 2. Käytä Dependency Injectionia

```csharp
// ✅ Palvelut DI:n kautta
public class OrderFunctions
{
    private readonly IOrderService _orderService;

    public OrderFunctions(IOrderService orderService)
    {
        _orderService = orderService;
    }
}
```

### 3. Käsittele virheet

```csharp
[Function("ProcessOrder")]
public async Task ProcessOrder(
    [QueueTrigger("orders")] OrderMessage message)
{
    try
    {
        await _orderService.ProcessAsync(message.OrderId);
    }
    catch (Exception ex)
    {
        _logger.LogError(ex, "Failed to process order {OrderId}", message.OrderId);
        throw; // Queue trigger yrittää uudelleen automaattisesti
    }
}
```

### 4. Älä tallenna tilaa funktioon

```csharp
// ❌ Staattinen tila — ei toimi skaalatessa
private static List<Order> _cache = new();

// ✅ Käytä ulkoista palvelua (Redis, tietokanta)
private readonly ICacheService _cache;
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Serverless** | Pilvipalvelu hallinnoi infrastruktuuria — maksat vain käytöstä |
| **Azure Functions** | Microsoftin serverless-alusta yksittäisille funktioille |
| **Function App** | Kokoelma funktioita, jotka jakavat konfiguraation ja hostingin |
| **Trigger** | Tapahtuma joka käynnistää funktion (HTTP, Timer, Queue, Blob) |
| **Binding** | Deklaratiivinen yhteys Azure-palveluihin (input/output) |
| **Consumption Plan** | Maksat vain suorituksista, automaattinen skaalaus |
| **Isolated Worker** | .NET 8+ suositteltu malli — oma prosessi, täysi DI-tuki |
| **Durable Functions** | Tilalliset työnkulut serverless-ympäristössä |
| **Cold start** | Ensimmäisen kutsun viive Consumption-mallissa |

**Muista:**
- Azure Functions sopii **event-driven** ja **lyhytkestoisiin** tehtäviin
- Käytä **Consumption Plan** -mallia aloittaessa — se on ilmainen pienillä volyymeilla
- **Isolated Worker Model** on suositeltu .NET 8+:ssa
- Pidä funktiot **stateless** — käytä ulkoisia palveluita tilan tallentamiseen
- Harkitse **Durable Functions** -laajennusta monivaihaisille prosesseille

---

## Hyödyllisiä linkkejä

- [Microsoft: Azure Functions Overview](https://learn.microsoft.com/en-us/azure/azure-functions/functions-overview)
- [Microsoft: Azure Functions .NET Isolated](https://learn.microsoft.com/en-us/azure/azure-functions/dotnet-isolated-process-guide)
- [Microsoft: Triggers and Bindings](https://learn.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)
- [Microsoft: Durable Functions](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [Azure Functions Pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)
