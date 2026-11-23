# MediatR

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Mediator Pattern - Tausta](#mediator-pattern---tausta)
3. [MediatR-kirjaston asennus](#mediatr-kirjaston-asennus)
4. [Request ja Handler](#request-ja-handler)
5. [CQRS MediatR:llä](#cqrs-mediatrllä)
6. [Notifications](#notifications)
7. [Pipeline Behaviors](#pipeline-behaviors)
8. [Validointi FluentValidationilla](#validointi-fluentvalidationilla)
9. [Käytännön esimerkki: ASP.NET Core + MediatR](#käytännön-esimerkki-aspnet-core--mediatr)
10. [MediatR ja Clean Architecture](#mediatr-ja-clean-architecture)
11. [MediatR:n hinta ja handlerin testaus](#mediatrn-hinta-ja-handlerin-testaus)
12. [Best Practices](#best-practices)
13. [Anti-patterns](#anti-patterns)
14. [Yhteenveto](#yhteenveto)

---

## Johdanto

**MediatR** on kevyt kirjasto .NET-sovelluksiin, joka toteuttaa **Mediator-suunnittelumallin**. Se mahdollistaa komponenttien välisen kommunikaation ilman suoria riippuvuuksia, käyttäen viestipohjaista (message-based) arkkitehtuuria.

**Miksi MediatR?**

- Vähentää komponenttien välistä kytkentää (loose coupling)
- Mahdollistaa CQRS-mallin (Command Query Responsibility Segregation) helpon toteutuksen
- Tarjoaa pipeline-mekanismin cross-cutting concerns -toiminnallisuuksille (logging, validointi, caching)
- On yleisesti käytetty ASP.NET Core -projekteissa, joten siihen törmää usein valmiissa koodissa

> **Lisenssi:** MediatR muuttui kesällä 2025 kaupalliseksi. Versiosta 13.0.0 alkaen kirjastolla on kaksoislisenssi (RPL-1.5 tai kaupallinen lisenssi, josta on ehdoiltaan rajattu ilmainen Community-versio). Versiot 12.x ja vanhemmat pysyvät Apache 2.0 -lisenssillä. Tarkista lisenssi ennen kuin otat kirjaston projektiin: [Lucky Penny Software: FAQ](https://luckypennysoftware.com/faq). Tämän sivun esimerkit toimivat versiolla 12.

**Perusidea:**

```
Ilman MediatR:ia:
Controller → Service → Repository
     ↓
Controller tuntee Servicen suoraan (tight coupling)

MediatR:n kanssa:
Controller → IMediator → Handler → Repository
     ↓
Controller lähettää viestin, ei tiedä kuka käsittelee (loose coupling)
```

---

## Mediator Pattern - Tausta

### Ongelma: Spagettikytkennät

Kun komponentit kommunikoivat suoraan toistensa kanssa, syntyy monimutkainen riippuvuusverkko:

```
❌ Ilman Mediatoria:

    ComponentA ←→ ComponentB
        ↕           ↕
    ComponentC ←→ ComponentD

Jokainen komponentti tuntee muut → N*(N-1) riippuvuutta
```

### Ratkaisu: Mediator

Mediator toimii välittäjänä, joka ohjaa viestit oikeille vastaanottajille:

```
✅ Mediatorin kanssa:

    ComponentA → Mediator ← ComponentB
                   ↕
    ComponentC → Mediator ← ComponentD

Jokainen komponentti tuntee vain Mediatorin → N riippuvuutta
```

### Gang of Four määritelmä

> "Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly."

---

## MediatR-kirjaston asennus

### NuGet-paketin asennus

```bash
# ASP.NET Core -projektissa: lukitse versio
dotnet add package MediatR --version 12.5.0
```

Versio kannattaa kirjoittaa näkyviin. Ilman `--version`-valitsinta komento asentaa uusimman version, jolla on eri lisenssi kuin 12.x-versioilla (katso [Johdanto](#johdanto)). 12.5.0 on viimeinen Apache 2.0 -lisenssillä julkaistu versio.

### Rekisteröinti DI-containeriin

**Program.cs (ASP.NET Core):**

```csharp
var builder = WebApplication.CreateBuilder(args);

// Rekisteröi MediatR ja skannaa handlerit automaattisesti
builder.Services.AddMediatR(cfg => 
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly));

var app = builder.Build();
```

> **Huom:** `RegisterServicesFromAssembly` skannaa automaattisesti kaikki `IRequestHandler`- ja `INotificationHandler`-toteutukset annetusta assemblysta.

**Useamman assemblyn rekisteröinti (esim. Clean Architecture):**

```csharp
builder.Services.AddMediatR(cfg => 
    cfg.RegisterServicesFromAssemblies(
        typeof(Program).Assembly,              // API-kerros
        typeof(CreateProductCommand).Assembly   // Application-kerros
    ));
```

---

## Request ja Handler

MediatR:n ydin perustuu kahteen käsitteeseen: **Request** (viesti) ja **Handler** (käsittelijä).

### IRequest - Viesti joka palauttaa arvon

```csharp
// Request: "Hae tuote ID:llä"
public record GetProductByIdQuery(int Id) : IRequest<ProductDto>;

// Response-tyyppi
public class ProductDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
}
```

### IRequestHandler - Viestin käsittelijä

```csharp
// Handler: Käsittelee GetProductByIdQuery-viestin
public class GetProductByIdQueryHandler 
    : IRequestHandler<GetProductByIdQuery, ProductDto>
{
    private readonly AppDbContext _context;

    public GetProductByIdQueryHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<ProductDto> Handle(
        GetProductByIdQuery request, 
        CancellationToken cancellationToken)
    {
        var product = await _context.Products
            .Where(p => p.Id == request.Id)
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .FirstOrDefaultAsync(cancellationToken);

        return product ?? throw new NotFoundException($"Product {request.Id} not found");
    }
}
```

### IRequest ilman paluuarvoa

Kun viesti ei palauta arvoa (esim. delete-operaatio):

```csharp
// Request ilman paluuarvoa
public record DeleteProductCommand(int Id) : IRequest;

// Handler
public class DeleteProductCommandHandler : IRequestHandler<DeleteProductCommand>
{
    private readonly AppDbContext _context;

    public DeleteProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task Handle(
        DeleteProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = await _context.Products.FindAsync(
            new object[] { request.Id }, cancellationToken);

        if (product is null)
            throw new NotFoundException($"Product {request.Id} not found");

        _context.Products.Remove(product);
        await _context.SaveChangesAsync(cancellationToken);
    }
}
```

### Viestin lähettäminen

```csharp
// Controllerissa tai missä tahansa
public class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;

    public ProductsController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        // Lähetä viesti → MediatR löytää oikean handlerin automaattisesti
        var product = await _mediator.Send(new GetProductByIdQuery(id));
        return Ok(product);
    }
}
```

**`ISender` riittää controllerille.** `IMediator` koostuu kahdesta rajapinnasta: `ISender` (metodi `Send`) ja `IPublisher` (metodi `Publish`). Controller vain lähettää viestejä, joten sille riittää kapeampi `ISender`. Silloin konstruktorista näkee, ettei controller julkaise tapahtumia.

```csharp
public class ProductsController : ControllerBase
{
    private readonly ISender _sender;

    public ProductsController(ISender sender)
    {
        _sender = sender;
    }
}
```

### Miten MediatR löytää handlerin?

```
1. Controller kutsuu: _mediator.Send(new GetProductByIdQuery(42))

2. MediatR katsoo viestin tyypin: GetProductByIdQuery

3. MediatR etsii DI-containerista handlerin:
   IRequestHandler<GetProductByIdQuery, ProductDto>

4. MediatR kutsuu handlerin Handle()-metodia

5. Handler palauttaa tuloksen → Controller saa ProductDto:n
```

Uusi toiminto on siis uusi viesti ja uusi handler. Vanhoihin luokkiin ei kosketa.

### Handler on use case

Handler on sama asia kuin Clean Architecturen **use case** (käyttötapaus), vain uudessa muodossa. Se ohjaa yhden toiminnon alusta loppuun: **hae, kutsu domainia, tallenna**. Liiketoimintasääntö pysyy entiteetissä. Handler ei tarkista sitä itse.

Esimerkki sarjataulukkosovelluksesta, jossa otteluun kirjataan tulos:

```csharp
public record RecordResultCommand(int MatchId, int HomeGoals, int AwayGoals) : IRequest;

public class RecordResultCommandHandler : IRequestHandler<RecordResultCommand>
{
    private readonly IMatchRepository _matches;

    public RecordResultCommandHandler(IMatchRepository matches)
    {
        _matches = matches;
    }

    public async Task Handle(RecordResultCommand request, CancellationToken cancellationToken)
    {
        // 1. Hae
        var match = await _matches.GetByIdAsync(request.MatchId, cancellationToken)
            ?? throw new NotFoundException($"Match {request.MatchId} not found");

        // 2. Kutsu domainia: sääntö "tuloksen voi kirjata vain kerran" on entiteetissä
        match.RecordResult(request.HomeGoals, request.AwayGoals);

        // 3. Tallenna
        await _matches.SaveAsync(match, cancellationToken);
    }
}
```

Jos handleriin alkaa kertyä `if`-lauseita, jotka tarkistavat liiketoimintasääntöjä, ne kuuluvat entiteettiin. Tämän sivun muut esimerkit käyttävät yksinkertaista `Product`-luokkaa ilman sääntöjä, jotta MediatR:n omat osat näkyvät selvästi.

---

## CQRS MediatR:llä

**CQRS (Command Query Responsibility Segregation)** erottaa luku- ja kirjoitusoperaatiot toisistaan. MediatR on luonnollinen tapa toteuttaa CQRS, koska jokainen viesti on joko **Query** (lukuoperaatio) tai **Command** (kirjoitusoperaatio).

### CQRS:n perusidea

```
Perinteinen malli:
ProductService
  - GetAll()         ← Luku
  - GetById()        ← Luku
  - Create()         ← Kirjoitus
  - Update()         ← Kirjoitus
  - Delete()         ← Kirjoitus

CQRS-malli:
Queries (luku):
  - GetAllProductsQuery        → GetAllProductsQueryHandler
  - GetProductByIdQuery        → GetProductByIdQueryHandler

Commands (kirjoitus):
  - CreateProductCommand       → CreateProductCommandHandler
  - UpdateProductCommand       → UpdateProductCommandHandler
  - DeleteProductCommand       → DeleteProductCommandHandler
```

### Kansiorakenne

```
Features/
├── Products/
│   ├── Commands/
│   │   ├── CreateProduct/
│   │   │   ├── CreateProductCommand.cs
│   │   │   └── CreateProductCommandHandler.cs
│   │   ├── UpdateProduct/
│   │   │   ├── UpdateProductCommand.cs
│   │   │   └── UpdateProductCommandHandler.cs
│   │   └── DeleteProduct/
│   │       ├── DeleteProductCommand.cs
│   │       └── DeleteProductCommandHandler.cs
│   └── Queries/
│       ├── GetAllProducts/
│       │   ├── GetAllProductsQuery.cs
│       │   └── GetAllProductsQueryHandler.cs
│       └── GetProductById/
│           ├── GetProductByIdQuery.cs
│           └── GetProductByIdQueryHandler.cs
```

### Query-esimerkki

```csharp
// === Query ===
public record GetAllProductsQuery : IRequest<List<ProductDto>>;

// === Handler ===
public class GetAllProductsQueryHandler 
    : IRequestHandler<GetAllProductsQuery, List<ProductDto>>
{
    private readonly AppDbContext _context;

    public GetAllProductsQueryHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<List<ProductDto>> Handle(
        GetAllProductsQuery request, 
        CancellationToken cancellationToken)
    {
        return await _context.Products
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Price = p.Price
            })
            .ToListAsync(cancellationToken);
    }
}
```

### Command-esimerkki

```csharp
// === Command ===
public record CreateProductCommand(
    string Name, 
    decimal Price, 
    string Description) : IRequest<int>;

// === Handler ===
public class CreateProductCommandHandler 
    : IRequestHandler<CreateProductCommand, int>
{
    private readonly AppDbContext _context;

    public CreateProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<int> Handle(
        CreateProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = new Product
        {
            Name = request.Name,
            Price = request.Price,
            Description = request.Description
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync(cancellationToken);

        return product.Id; // Palauttaa luodun tuotteen ID:n
    }
}
```

### Command-esimerkki Update-operaatiolle

```csharp
// === Command ===
public record UpdateProductCommand(
    int Id, 
    string Name, 
    decimal Price) : IRequest;

// === Handler ===
public class UpdateProductCommandHandler : IRequestHandler<UpdateProductCommand>
{
    private readonly AppDbContext _context;

    public UpdateProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task Handle(
        UpdateProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = await _context.Products.FindAsync(
            new object[] { request.Id }, cancellationToken);

        if (product is null)
            throw new NotFoundException($"Product {request.Id} not found");

        product.Name = request.Name;
        product.Price = request.Price;

        await _context.SaveChangesAsync(cancellationToken);
    }
}
```

### Miksi CQRS + MediatR?

| Ominaisuus | Perinteinen Service | CQRS + MediatR |
|---|---|---|
| **Single Responsibility** | Service sisältää kaiken | Jokainen handler = yksi operaatio |
| **Testattavuus** | Koko service mockattava | Yksi handler kerrallaan |
| **Skaalautuvuus** | Service kasvaa isoksi | Pienet, itsenäiset handlerit |
| **Löysä kytkentä** | Controller → Service | Controller → IMediator |
| **Cross-cutting** | Manuaalinen | Pipeline Behaviors |

---

## Notifications

**Notification** on viesti, joka lähetetään **monelle** vastaanottajalle (one-to-many). Toisin kuin Request, jolla on yksi handler, Notificationilla voi olla monta handleria.

### Milloin käyttää?

- **Domainin tapahtumat** (Domain Events): "Tilaus luotiin" → lähetä sähköposti, päivitä varasto, kirjaa loki
- **Sivuvaikutukset**: Operaation jälkeen tapahtuvat asiat
- **Irtikytkentä**: Pääoperaation ei tarvitse tietää sivuvaikutuksista

### INotification ja INotificationHandler

```csharp
// === Notification (tapahtuma) ===
public record ProductCreatedNotification(
    int ProductId, 
    string ProductName, 
    decimal Price) : INotification;

// === Handler 1: Lähetä sähköposti ===
public class SendEmailOnProductCreated 
    : INotificationHandler<ProductCreatedNotification>
{
    private readonly IEmailService _emailService;

    public SendEmailOnProductCreated(IEmailService emailService)
    {
        _emailService = emailService;
    }

    public async Task Handle(
        ProductCreatedNotification notification, 
        CancellationToken cancellationToken)
    {
        await _emailService.SendAsync(
            to: "admin@company.com",
            subject: $"New product: {notification.ProductName}",
            body: $"Product {notification.ProductName} created with price {notification.Price:C}");
    }
}

// === Handler 2: Kirjaa tapahtuma lokiin ===
public class LogProductCreated 
    : INotificationHandler<ProductCreatedNotification>
{
    private readonly ILogger<LogProductCreated> _logger;

    public LogProductCreated(ILogger<LogProductCreated> logger)
    {
        _logger = logger;
    }

    public Task Handle(
        ProductCreatedNotification notification, 
        CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "Product created: {ProductId} - {ProductName} ({Price:C})",
            notification.ProductId,
            notification.ProductName,
            notification.Price);

        return Task.CompletedTask;
    }
}

// === Handler 3: Päivitä hakuindeksi ===
public class UpdateSearchIndexOnProductCreated 
    : INotificationHandler<ProductCreatedNotification>
{
    private readonly ISearchService _searchService;

    public UpdateSearchIndexOnProductCreated(ISearchService searchService)
    {
        _searchService = searchService;
    }

    public async Task Handle(
        ProductCreatedNotification notification, 
        CancellationToken cancellationToken)
    {
        await _searchService.IndexProductAsync(notification.ProductId);
    }
}
```

### Notificationin julkaisu

```csharp
public class CreateProductCommandHandler 
    : IRequestHandler<CreateProductCommand, int>
{
    private readonly AppDbContext _context;
    private readonly IMediator _mediator;

    public CreateProductCommandHandler(
        AppDbContext context, IMediator mediator)
    {
        _context = context;
        _mediator = mediator;
    }

    public async Task<int> Handle(
        CreateProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = new Product
        {
            Name = request.Name,
            Price = request.Price
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync(cancellationToken);

        // Julkaise notification → kaikki handlerit suoritetaan
        await _mediator.Publish(
            new ProductCreatedNotification(product.Id, product.Name, product.Price),
            cancellationToken);

        return product.Id;
    }
}
```

### Send vs Publish

| | `Send` | `Publish` |
|---|---|---|
| **Tyyppi** | `IRequest<T>` | `INotification` |
| **Handlereita** | Täsmälleen 1 | 0...N |
| **Palauttaa** | `Task<T>` | `Task` |
| **Käyttötarkoitus** | Komennot ja kyselyt | Tapahtumat ja sivuvaikutukset |

---

## Pipeline Behaviors

**Pipeline Behavior** on luokka, joka tekee saman työn jokaisen pyynnön ympärillä. Se toimii kuin ASP.NET Core:n middleware, mutta MediatR-viesteille. Behavior suoritetaan **ennen ja/tai jälkeen** jokaisen handlerin.

Rakenteeltaan behavior on [Decorator-suunnittelumalli](Decorator-Pattern.md) valmiissa muodossa: se kääritään jokaisen handlerin ympärille, kutsuu handleria ja lisää jotain kutsun ympärille.

### Perusidea

```
Request saapuu:

  [Logging Behavior]
      ↓
  [Validation Behavior]
      ↓
  [Caching Behavior]
      ↓
  [Handler]
      ↓
  Response palautuu (käänteisessä järjestyksessä behaviorien läpi)
```

Kuvan `[Caching Behavior]` on esimerkki siitä, mitä ketjuun voi lisätä. Behavior koskee kuitenkin kaikkia pyyntöjä. Kun välimuistiin halutaan vain yhden kyselyn tulos, se tehdään yleensä decoratorilla, joka kääritään sen yhden rajapinnan ympärille (katso [Caching: Decorator Pattern cachingille](Caching.md#decorator-pattern-cachingille)).

### Mikä kuuluu behavioriin ja mikä ei

Behavioriin kuuluu työ, joka on **sama jokaiselle pyynnölle** eikä riipu siitä, mitä pyyntö tekee.

| Kuuluu behavioriin | Ei kuulu behavioriin |
|---|---|
| Lokitus: mikä pyyntö tuli ja onnistuiko se | Liiketoimintasääntö ("tuloksen voi kirjata vain kerran") |
| Ajanmittaus: kauanko käsittely kesti | Päätös, joka vaatii entiteetin tilan |
| Syötteen muodon tarkistus: kenttä ei ole tyhjä, teksti ei ole liian pitkä | Yhden toiminnon oma logiikka |

**Miksi liiketoimintasääntö ei kuulu behavioriin?** Behavior näkee vain viestin, eli sen kentät. Se ei näe entiteettiä eikä tiedä, missä tilassa se on. Sääntö "tuloksen voi kirjata vain kerran" vaatii tiedon siitä, onko tulos jo kirjattu. Sen tiedon omistaa entiteetti, joten sääntö kuuluu sinne.

**Kerros:** behaviorit ovat Application-kerroksessa. **Milloin behavioria ei kannata tehdä:** kun työ koskee vain yhtä tai kahta pyyntöä. Silloin se kirjoitetaan handleriin tai decoratoriin.

### IPipelineBehavior

```csharp
public class LoggingBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly ILogger<LoggingBehavior<TRequest, TResponse>> _logger;

    public LoggingBehavior(ILogger<LoggingBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        var requestName = typeof(TRequest).Name;

        _logger.LogInformation("Handling {RequestName}: {@Request}", 
            requestName, request);

        var stopwatch = Stopwatch.StartNew();

        // Kutsu seuraava behavior tai handler
        var response = await next();

        stopwatch.Stop();

        _logger.LogInformation("Handled {RequestName} in {ElapsedMs}ms", 
            requestName, stopwatch.ElapsedMilliseconds);

        return response;
    }
}
```

### Behaviorin rekisteröinti

```csharp
// Program.cs
builder.Services.AddMediatR(cfg => 
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
    
    // Lisää pipeline behaviors (suoritusjärjestys = rekisteröintijärjestys)
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
});
```

### Performance Behavior -esimerkki

```csharp
public class PerformanceBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly ILogger<PerformanceBehavior<TRequest, TResponse>> _logger;
    private readonly Stopwatch _timer;

    public PerformanceBehavior(
        ILogger<PerformanceBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
        _timer = new Stopwatch();
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        _timer.Start();

        var response = await next();

        _timer.Stop();

        var elapsedMs = _timer.ElapsedMilliseconds;

        // Varoita jos operaatio kestää yli 500ms
        if (elapsedMs > 500)
        {
            _logger.LogWarning(
                "Long running request: {RequestName} ({ElapsedMs}ms) {@Request}",
                typeof(TRequest).Name, elapsedMs, request);
        }

        return response;
    }
}
```

### Unhandled Exception Behavior

```csharp
public class UnhandledExceptionBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly ILogger<UnhandledExceptionBehavior<TRequest, TResponse>> _logger;

    public UnhandledExceptionBehavior(
        ILogger<UnhandledExceptionBehavior<TRequest, TResponse>> logger)
    {
        _logger = logger;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        try
        {
            return await next();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, 
                "Unhandled exception for request {RequestName}: {@Request}",
                typeof(TRequest).Name, request);
            throw;
        }
    }
}
```

---

## Validointi FluentValidationilla

Yksi MediatR:n yleisimmistä käyttötavoista on **automaattinen validointi** Pipeline Behaviorin avulla. FluentValidation-kirjasto sopii tähän erinomaisesti.

### Asennus

```bash
dotnet add package FluentValidation
dotnet add package FluentValidation.DependencyInjectionExtensions
```

### Validator-luokka

```csharp
public class CreateProductCommandValidator 
    : AbstractValidator<CreateProductCommand>
{
    public CreateProductCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty().WithMessage("Product name is required")
            .MaximumLength(200).WithMessage("Product name must not exceed 200 characters");

        RuleFor(x => x.Description)
            .MaximumLength(2000).WithMessage("Description must not exceed 2000 characters");
    }
}
```

> **Huom:** Validator tarkistaa syötteen **muodon**: onko kenttä täytetty ja mahtuuko se sarakkeeseen. Sääntö "hinnan pitää olla positiivinen" on liiketoimintasääntö, joten se kuuluu `Product`-entiteettiin eikä validatoriin. Jos sama sääntö kirjoitetaan molempiin, ne ajautuvat ennen pitkää erilleen. Katso [Mikä kuuluu behavioriin ja mikä ei](#mikä-kuuluu-behavioriin-ja-mikä-ei).

### Validation Pipeline Behavior

```csharp
public class ValidationBehavior<TRequest, TResponse> 
    : IPipelineBehavior<TRequest, TResponse>
    where TRequest : notnull
{
    private readonly IEnumerable<IValidator<TRequest>> _validators;

    public ValidationBehavior(IEnumerable<IValidator<TRequest>> validators)
    {
        _validators = validators;
    }

    public async Task<TResponse> Handle(
        TRequest request,
        RequestHandlerDelegate<TResponse> next,
        CancellationToken cancellationToken)
    {
        // Jos validaattoreita ei ole, jatka suoraan handleriin
        if (!_validators.Any())
            return await next();

        // Suorita kaikki validaattorit
        var context = new ValidationContext<TRequest>(request);

        var validationResults = await Task.WhenAll(
            _validators.Select(v => v.ValidateAsync(context, cancellationToken)));

        // Kerää virheet
        var failures = validationResults
            .SelectMany(r => r.Errors)
            .Where(f => f != null)
            .ToList();

        // Jos virheitä löytyy, heitä poikkeus
        if (failures.Count > 0)
            throw new ValidationException(failures);

        // Ei virheitä → jatka handleriin
        return await next();
    }
}
```

### Rekisteröinti

```csharp
// Program.cs
builder.Services.AddMediatR(cfg =>
{
    cfg.RegisterServicesFromAssembly(typeof(Program).Assembly);
    cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
});

// Rekisteröi kaikki validaattorit automaattisesti
builder.Services.AddValidatorsFromAssembly(typeof(Program).Assembly);
```

### Miten se toimii?

```
1. Controller: _mediator.Send(new CreateProductCommand("", 10, ""))

2. ValidationBehavior aktivoituu:
   → Löytää CreateProductCommandValidator:n DI:stä
   → Suorittaa validoinnin
   → Virhe: "Product name is required"
   → Heittää ValidationException

3. Handler EI suoritu ollenkaan → virheellinen data ei pääse läpi!

4. Global Exception Handler muuntaa ValidationExceptionin HTTP 400 -vastaukseksi
```

---

## Käytännön esimerkki: ASP.NET Core + MediatR

### Täydellinen CRUD-esimerkki

**1. Domain-malli:**

```csharp
public class Product
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
}
```

**2. DTO:**

```csharp
public class ProductDto
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public decimal Price { get; set; }
}
```

**3. Queries:**

```csharp
// GetAll
public record GetAllProductsQuery : IRequest<List<ProductDto>>;

public class GetAllProductsQueryHandler 
    : IRequestHandler<GetAllProductsQuery, List<ProductDto>>
{
    private readonly AppDbContext _context;

    public GetAllProductsQueryHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<List<ProductDto>> Handle(
        GetAllProductsQuery request, 
        CancellationToken cancellationToken)
    {
        return await _context.Products
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Price = p.Price
            })
            .ToListAsync(cancellationToken);
    }
}

// GetById
public record GetProductByIdQuery(int Id) : IRequest<ProductDto?>;

public class GetProductByIdQueryHandler 
    : IRequestHandler<GetProductByIdQuery, ProductDto?>
{
    private readonly AppDbContext _context;

    public GetProductByIdQueryHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<ProductDto?> Handle(
        GetProductByIdQuery request, 
        CancellationToken cancellationToken)
    {
        return await _context.Products
            .Where(p => p.Id == request.Id)
            .Select(p => new ProductDto
            {
                Id = p.Id,
                Name = p.Name,
                Description = p.Description,
                Price = p.Price
            })
            .FirstOrDefaultAsync(cancellationToken);
    }
}
```

**4. Commands:**

```csharp
// Create
public record CreateProductCommand(
    string Name, 
    string Description, 
    decimal Price) : IRequest<int>;

public class CreateProductCommandHandler 
    : IRequestHandler<CreateProductCommand, int>
{
    private readonly AppDbContext _context;

    public CreateProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task<int> Handle(
        CreateProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = new Product
        {
            Name = request.Name,
            Description = request.Description,
            Price = request.Price
        };

        _context.Products.Add(product);
        await _context.SaveChangesAsync(cancellationToken);

        return product.Id;
    }
}

// Update
public record UpdateProductCommand(
    int Id, 
    string Name, 
    string Description, 
    decimal Price) : IRequest;

public class UpdateProductCommandHandler 
    : IRequestHandler<UpdateProductCommand>
{
    private readonly AppDbContext _context;

    public UpdateProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task Handle(
        UpdateProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = await _context.Products
            .FindAsync(new object[] { request.Id }, cancellationToken)
            ?? throw new NotFoundException($"Product {request.Id} not found");

        product.Name = request.Name;
        product.Description = request.Description;
        product.Price = request.Price;

        await _context.SaveChangesAsync(cancellationToken);
    }
}

// Delete
public record DeleteProductCommand(int Id) : IRequest;

public class DeleteProductCommandHandler 
    : IRequestHandler<DeleteProductCommand>
{
    private readonly AppDbContext _context;

    public DeleteProductCommandHandler(AppDbContext context)
    {
        _context = context;
    }

    public async Task Handle(
        DeleteProductCommand request, 
        CancellationToken cancellationToken)
    {
        var product = await _context.Products
            .FindAsync(new object[] { request.Id }, cancellationToken)
            ?? throw new NotFoundException($"Product {request.Id} not found");

        _context.Products.Remove(product);
        await _context.SaveChangesAsync(cancellationToken);
    }
}
```

**5. Controller:**

```csharp
[ApiController]
[Route("api/[controller]")]
public class ProductsController : ControllerBase
{
    private readonly IMediator _mediator;

    public ProductsController(IMediator mediator)
    {
        _mediator = mediator;
    }

    [HttpGet]
    public async Task<ActionResult<List<ProductDto>>> GetAll()
    {
        var products = await _mediator.Send(new GetAllProductsQuery());
        return Ok(products);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<ProductDto>> GetById(int id)
    {
        var product = await _mediator.Send(new GetProductByIdQuery(id));
        
        if (product is null)
            return NotFound();

        return Ok(product);
    }

    [HttpPost]
    public async Task<ActionResult<int>> Create(CreateProductCommand command)
    {
        var productId = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetById), new { id = productId }, productId);
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> Update(int id, UpdateProductCommand command)
    {
        if (id != command.Id)
            return BadRequest("ID mismatch");

        await _mediator.Send(command);
        return NoContent();
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(int id)
    {
        await _mediator.Send(new DeleteProductCommand(id));
        return NoContent();
    }
}
```

**Huomaa kuinka ohut controller on!** Se ei sisällä mitään liiketoimintalogiikkaa, vain:
1. Vastaanottaa HTTP-pyynnön
2. Lähettää viestin MediatR:lle
3. Palauttaa HTTP-vastauksen

---

## MediatR ja Clean Architecture

MediatR sopii erinomaisesti Clean Architecture -arkkitehtuuriin. Application-kerros sisältää kaikki Commands, Queries ja niiden Handlerit.

### Projektirakenne

```
Solution/
├── Domain/                          (Entities, Value Objects)
│   └── Entities/
│       └── Product.cs
├── Application/                     (MediatR Commands, Queries, Behaviors)
│   ├── Common/
│   │   ├── Behaviors/
│   │   │   ├── LoggingBehavior.cs
│   │   │   └── ValidationBehavior.cs
│   │   ├── Exceptions/
│   │   │   ├── NotFoundException.cs
│   │   │   └── ValidationException.cs
│   │   └── Interfaces/
│   │       └── IAppDbContext.cs
│   └── Features/
│       └── Products/
│           ├── Commands/
│           │   ├── CreateProduct/
│           │   │   ├── CreateProductCommand.cs
│           │   │   ├── CreateProductCommandHandler.cs
│           │   │   └── CreateProductCommandValidator.cs
│           │   └── DeleteProduct/
│           │       ├── DeleteProductCommand.cs
│           │       └── DeleteProductCommandHandler.cs
│           ├── Queries/
│           │   ├── GetAllProducts/
│           │   │   ├── GetAllProductsQuery.cs
│           │   │   └── GetAllProductsQueryHandler.cs
│           │   └── GetProductById/
│           │       ├── GetProductByIdQuery.cs
│           │       └── GetProductByIdQueryHandler.cs
│           └── Notifications/
│               ├── ProductCreatedNotification.cs
│               └── Handlers/
│                   ├── SendEmailOnProductCreated.cs
│                   └── LogProductCreated.cs
├── Infrastructure/                  (DbContext, External Services)
│   ├── Data/
│   │   └── AppDbContext.cs
│   └── Services/
│       └── EmailService.cs
└── WebApi/                          (Controllers, Program.cs)
    ├── Controllers/
    │   └── ProductsController.cs
    └── Program.cs
```

### Riippuvuuksien suunta

```
WebApi → Application → Domain
  ↓
Infrastructure → Application → Domain

✅ Application-kerros EI riipu Infrastructuresta tai WebApista
✅ Domain-kerros EI riipu mistään
✅ MediatR on Application-kerroksessa
```

### Application-kerroksen DI-rekisteröinti

```csharp
// Application/DependencyInjection.cs
public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        var assembly = typeof(DependencyInjection).Assembly;

        services.AddMediatR(cfg =>
        {
            cfg.RegisterServicesFromAssembly(assembly);
            cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>));
            cfg.AddBehavior(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>));
        });

        services.AddValidatorsFromAssembly(assembly);

        return services;
    }
}

// WebApi/Program.cs
builder.Services.AddApplication();      // Application-kerroksen palvelut
builder.Services.AddInfrastructure();   // Infrastructure-kerroksen palvelut
```

---

## MediatR:n hinta ja handlerin testaus

### Hinta: kutsusta ei näe käsittelijää

MediatR:n hyöty on, että controller ei tiedä, mikä luokka viestin käsittelee. Sama asia on myös sen hinta.

```csharp
await _sender.Send(new RecordResultCommand(matchId, 2, 1));
```

Tältä riviltä ei näe, mihin luokkaan suoritus jatkuu. Editorin "siirry määrittelyyn" vie `Send`-metodiin, ei handleriin. Lukijan pitää tietää nimeämiskäytäntö: `RecordResultCommand` → `RecordResultCommandHandler`, samassa kansiossa.

Tästä seuraa kaksi asiaa:

- **Nimeämiskäytännön pitää pitää.** Jos handlerin nimi tai paikka poikkeaa käytännöstä, sitä ei löydä.
- **Virhe näkyy vasta ajon aikana.** Jos handler puuttuu tai sitä ei ole rekisteröity, koodi kääntyy silti. Virhe tulee vasta, kun viesti lähetetään.

Pienessä sovelluksessa, jossa on muutama toiminto, suora kutsu use case -luokkaan on helpompi lukea. MediatR maksaa itsensä takaisin, kun toimintoja on paljon ja niiden ympärille halutaan sama työ (lokitus, muodon tarkistus).

### Handlerin testaus

Handler on tavallinen luokka. Sen voi testata kutsumalla `Handle`-metodia suoraan. Testi ei tarvitse HTTP:tä, controlleria eikä MediatR:ia. Riippuvuuksien tilalle annetaan tekaistut toteutukset (fake).

```csharp
// Tekaistu repository: pitää ottelun muistissa
public class FakeMatchRepository : IMatchRepository
{
    private readonly Match _match;
    public bool SaveWasCalled { get; private set; }

    public FakeMatchRepository(Match match)
    {
        _match = match;
    }

    public Task<Match?> GetByIdAsync(int id, CancellationToken ct)
        => Task.FromResult<Match?>(_match);

    public Task SaveAsync(Match match, CancellationToken ct)
    {
        SaveWasCalled = true;
        return Task.CompletedTask;
    }
}

public class RecordResultCommandHandlerTests
{
    [Fact]
    public async Task Handle_RecordsResultAndSaves()
    {
        var match = new Match(homeTeamId: 1, awayTeamId: 2);
        var repository = new FakeMatchRepository(match);
        var handler = new RecordResultCommandHandler(repository);

        await handler.Handle(
            new RecordResultCommand(match.Id, HomeGoals: 2, AwayGoals: 1),
            CancellationToken.None);

        Assert.Equal(2, match.HomeGoals);
        Assert.True(repository.SaveWasCalled);
    }
}
```

**Mitä tämä testi todistaa?** Handlerin oman logiikan: se hakee ottelun, kutsuu entiteettiä ja tallentaa.

**Mitä se ei todista?** Sitä, että osoite ohjautuu oikeaan controlleriin, että handler on rekisteröity DI-containeriin tai että behaviorit ajetaan. Ne näkyvät vasta testissä, joka käynnistää koko sovelluksen ja lähettää oikean HTTP-pyynnön (integraatiotesti).

---

## Best Practices

### 1. Nimeä Commands ja Queries selkeästi

```csharp
// ✅ HYVÄ: Selkeä nimeäminen
public record CreateProductCommand(...) : IRequest<int>;
public record GetProductByIdQuery(int Id) : IRequest<ProductDto>;
public record UpdateProductPriceCommand(int Id, decimal NewPrice) : IRequest;

// ❌ HUONO: Epäselvä nimeäminen
public record ProductRequest(...) : IRequest<int>;
public record GetProduct(int Id) : IRequest<ProductDto>;
public record UpdateRequest(...) : IRequest;
```

### 2. Käytä record-tyyppejä viesteille

```csharp
// ✅ HYVÄ: record on immutable ja kompakti
public record CreateProductCommand(string Name, decimal Price) : IRequest<int>;

// ❌ HUONO: class on mutable ja verbose
public class CreateProductCommand : IRequest<int>
{
    public string Name { get; set; }
    public decimal Price { get; set; }
}
```

### 3. Yksi Handler = Yksi vastuu

```csharp
// ✅ HYVÄ: Handler tekee yhden asian
public class CreateProductCommandHandler : IRequestHandler<CreateProductCommand, int>
{
    public async Task<int> Handle(CreateProductCommand request, CancellationToken ct)
    {
        // Vain tuotteen luominen
    }
}

// ❌ HUONO: Handler tekee liikaa
public class ProductHandler : IRequestHandler<CreateProductCommand, int>
{
    public async Task<int> Handle(CreateProductCommand request, CancellationToken ct)
    {
        // Luominen + sähköpostin lähetys + loggaus + cachen päivitys...
        // → Siirrä sivuvaikutukset pois handlerin rungosta (katso alla)
    }
}
```

Sivuvaikutukselle on kaksi tapaa:

- **Yksinkertaisempi: handler kutsuu rajapintaa.** Handler saa konstruktorissa esimerkiksi rajapinnan, jolla sarjataulukon välimuisti tyhjennetään, ja kutsuu sitä tallennuksen jälkeen. Kutsu näkyy handlerissa, ja järjestys on selvä. Tämä riittää, kun sivuvaikutuksia on yksi tai kaksi.
- **Notification.** Handler julkaisee tapahtuman, ja erilliset handlerit reagoivat siihen. Tämä kannattaa, kun samaan tapahtumaan reagoi monta toisistaan riippumatonta osaa tai kun reagoijia lisätään usein. Hinta on, että handlerista ei enää näe, mitä tallennuksen jälkeen tapahtuu ja missä järjestyksessä.

### 4. Käytä CancellationToken aina

```csharp
// ✅ HYVÄ: Välittää CancellationTokenin
public async Task<ProductDto> Handle(
    GetProductByIdQuery request, 
    CancellationToken cancellationToken)
{
    return await _context.Products
        .FirstOrDefaultAsync(p => p.Id == request.Id, cancellationToken);
}

// ❌ HUONO: Ei käytä CancellationTokenia
public async Task<ProductDto> Handle(
    GetProductByIdQuery request, 
    CancellationToken cancellationToken)
{
    return await _context.Products
        .FirstOrDefaultAsync(p => p.Id == request.Id);
}
```

### 5. Käytä Pipeline Behaviors cross-cutting concerneille

```csharp
// ✅ HYVÄ: Validointi Pipeline Behaviorissa
// → Kaikki commands validoidaan automaattisesti

// ❌ HUONO: Validointi jokaisessa handlerissa erikseen
public async Task<int> Handle(CreateProductCommand request, CancellationToken ct)
{
    // Manuaalinen validointi jokaisessa handlerissa...
    if (string.IsNullOrEmpty(request.Name))
        throw new ValidationException("Name is required");
    // ...
}
```

### 6. Pidä Command/Query ja Handler samassa tiedostossa tai kansiossa

```csharp
// ✅ Vaihtoehto 1: Samassa tiedostossa (pienille projekteille)
// CreateProduct.cs
public record CreateProductCommand(string Name, decimal Price) : IRequest<int>;

public class CreateProductCommandHandler 
    : IRequestHandler<CreateProductCommand, int>
{
    // ...
}

// ✅ Vaihtoehto 2: Samassa kansiossa (isommille projekteille)
// Features/Products/Commands/CreateProduct/
//   ├── CreateProductCommand.cs
//   ├── CreateProductCommandHandler.cs
//   └── CreateProductCommandValidator.cs
```

---

## Anti-patterns

### 1. Älä injektoi IMediator Handleriin ilman syytä

```csharp
// ❌ HUONO: Handler kutsuu toista handleria MediatR:n kautta
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, int>
{
    private readonly IMediator _mediator;

    public async Task<int> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // Tämä luo piilotetun riippuvuuden!
        var product = await _mediator.Send(new GetProductByIdQuery(request.ProductId));
        // ...
    }
}

// ✅ HYVÄ: Käytä suoraa riippuvuutta
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, int>
{
    private readonly AppDbContext _context;

    public async Task<int> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        var product = await _context.Products.FindAsync(request.ProductId, ct);
        // ...
    }
}

// ✅ OK: IMediator Handlerissa Notificationien julkaisemiseen
public class CreateOrderCommandHandler : IRequestHandler<CreateOrderCommand, int>
{
    private readonly IMediator _mediator;
    private readonly AppDbContext _context;

    public async Task<int> Handle(CreateOrderCommand request, CancellationToken ct)
    {
        // ... luo tilaus ...
        
        // Notificationien julkaisu ON ok
        await _mediator.Publish(new OrderCreatedNotification(order.Id), ct);
        
        return order.Id;
    }
}
```

### 2. Älä käytä MediatR:ia kaikkeen

```csharp
// ❌ HUONO: MediatR yksinkertaiseen datahakuun
public record GetCurrentTimeQuery : IRequest<DateTime>;

public class GetCurrentTimeQueryHandler : IRequestHandler<GetCurrentTimeQuery, DateTime>
{
    public Task<DateTime> Handle(GetCurrentTimeQuery request, CancellationToken ct)
    {
        return Task.FromResult(DateTime.UtcNow);
    }
}

// ✅ HYVÄ: Yksinkertaiset asiat suoraan
var currentTime = DateTime.UtcNow;
```

### 3. Vältä liian isoja Handlereita

```csharp
// ❌ HUONO: Handler sisältää liikaa logiikkaa
public async Task<int> Handle(CreateOrderCommand request, CancellationToken ct)
{
    // 200 riviä validointia, liiketoimintalogiikkaa, 
    // sähköpostin lähetystä, loggausta...
}

// ✅ HYVÄ: Jaa vastuut
// - Syötteen muodon tarkistus → Validator + ValidationBehavior
// - Liiketoimintasääntö → entiteetti
// - Sivuvaikutukset → rajapinta tai Notifications
// - Handler: hae, kutsu domainia, tallenna
```

---

## Yhteenveto

### MediatR:n keskeiset käsitteet

| Käsite | Tarkoitus | Interface |
|---|---|---|
| **Request** | Viesti (command/query) | `IRequest<T>` |
| **Handler** | Viestin käsittelijä | `IRequestHandler<TRequest, TResponse>` |
| **Notification** | Tapahtuma (one-to-many) | `INotification` |
| **NotificationHandler** | Tapahtuman käsittelijä | `INotificationHandler<T>` |
| **PipelineBehavior** | Sama työ jokaisen pyynnön ympärillä | `IPipelineBehavior<TRequest, TResponse>` |
| **Sender** | Kapea rajapinta viestin lähettämiseen | `ISender` |

### Milloin käyttää MediatR:ia?

**Käytä kun:**
- ✅ Haluat toteuttaa CQRS-mallin
- ✅ Tarvitset pipeline-mekanismia (validointi, logging, caching)
- ✅ Rakennat Clean Architecture -sovellusta
- ✅ Haluat ohuen controllerin
- ✅ Projektissa on useita kehittäjiä (vähemmän merge-konflikteja)

**Älä käytä kun:**
- ❌ Projekti on hyvin pieni ja yksinkertainen
- ❌ Tiimillä ei ole kokemusta CQRS-mallista
- ❌ Ei tarvetta cross-cutting concerneille

### Hyödyllisiä linkkejä

- [MediatR GitHub](https://github.com/LuckyPennySoftware/MediatR) - Virallinen repository
- [MediatR Wiki](https://github.com/LuckyPennySoftware/MediatR/wiki) - Dokumentaatio
- [Lucky Penny Software: FAQ](https://luckypennysoftware.com/faq) - Lisenssiehdot versiosta 13 alkaen
- [Decorator Pattern](Decorator-Pattern.md) - Malli, jonka valmis muoto Pipeline Behavior on
- [CQRS Pattern - Microsoft Docs](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) - CQRS-malli
- [Mediator Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/mediator) - Mediator-suunnittelumalli

---

[Takaisin: Edistyneet aiheet](../README.md)
