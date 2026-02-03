# Result Pattern

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Ongelma: Exception-pohjainen virheenkäsittely](#ongelma-exception-pohjainen-virheenkäsittely)
3. [Ratkaisu: Result Pattern](#ratkaisu-result-pattern)
4. [Railway Oriented Programming](#railway-oriented-programming)
5. [Toteutus C#:ssa](#toteutus-cssa)
6. [Result vs Exceptions](#result-vs-exceptions)
7. [Käytännön esimerkkejä](#käytännön-esimerkkejä)
8. [Result Pattern Libraries](#result-pattern-libraries)
9. [Best Practices](#best-practices)
10. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Result Pattern** on funktionaalisen ohjelmoinnin malli, jossa operaation tulos palautetaan eksplisiittisenä Result-oliona sen sijaan että heitetään exception. Pattern tekee virheenkäsittelystä näkyvän ja kontrolloidun.

---

## Ongelma: Exception-pohjainen virheenkäsittely

### Tyypillinen koodi Exceptioneilla

```csharp
public async Task<Order> CreateOrderAsync(CreateOrderDto dto)
{
    // Validointi
    if (dto.Items.Count == 0)
        throw new ValidationException("Order must have at least one item");
    
    // Business rule
    var customer = await _customerRepository.GetByIdAsync(dto.CustomerId);
    if (customer == null)
        throw new NotFoundException($"Customer {dto.CustomerId} not found");
    
    if (customer.IsBlocked)
        throw new BusinessRuleException("Customer is blocked");
    
    // Luo order
    var order = new Order { ... };
    return await _orderRepository.AddAsync(order);
}
```

**Controller:**

```csharp
[HttpPost]
public async Task<ActionResult<Order>> Create([FromBody] CreateOrderDto dto)
{
    try
    {
        var order = await _service.CreateOrderAsync(dto);
        return CreatedAtAction(nameof(GetById), new { id = order.Id }, order);
    }
    catch (ValidationException ex)
    {
        return BadRequest(new { error = ex.Message });
    }
    catch (NotFoundException ex)
    {
        return NotFound(new { error = ex.Message });
    }
    catch (BusinessRuleException ex)
    {
        return Conflict(new { error = ex.Message });
    }
}
```

### Ongelmat

**1. Ei-eksplisiittinen kontrollivirta**

```csharp
// Signaturesta ei näy että operaatio voi epäonnistua
Task<Order> CreateOrderAsync(CreateOrderDto dto)
```

Kehittäjä ei tiedä mitä exceptioneita voi tulla!

**2. Performance-kustannus**

Exceptionit ovat kalliita:
- Stack trace luodaan
- Exception-olio allokoidaan
- Unwinding stack:ia

**3. Try-catch kaikkialla**

```csharp
try { ... } catch { }
try { ... } catch { }
try { ... } catch { }
```

Controller on täynnä virheenkäsittelyä!

**4. Eri exception-tyyppejä**

```csharp
throw new ValidationException();
throw new NotFoundException();
throw new BusinessRuleException();
throw new UnauthorizedException();
// ... jne.
```

Pitää tietää kaikki mahdolliset exceptionit!

**5. "Goto" moderniksi**

Exceptionit ovat "goto":n tapainen kontrollivirtaus:
```csharp
void MethodA()
{
    try
    {
        MethodB();  // ← Hyppää suoraan catch:iin mistä tahansa!
    }
    catch { ... }
}

void MethodB() { throw new Exception(); }
```

---

## Ratkaisu: Result Pattern

### Perusidea

**Palauta Result-olio joka kertoo:**
- ✅ Onnistuiko operaatio?
- ✅ Jos onnistui → Mikä on tulos?
- ❌ Jos epäonnistui → Mikä on virhe?

### Esimerkki

```csharp
// Sen sijaan että heitetään exception...
if (customer == null)
    throw new NotFoundException("Customer not found");

// ...palautetaan Result
if (customer == null)
    return Result.Failure<Order>("Customer not found");
```

**Signaturesta näkyy että voi epäonnistua:**

```csharp
// ✅ Eksplisiittinen
Task<Result<Order>> CreateOrderAsync(CreateOrderDto dto)

// ❌ Ei-eksplisiittinen
Task<Order> CreateOrderAsync(CreateOrderDto dto)
```

---

## Railway Oriented Programming

**Ajattele koodia kahtena raitioparina:**

```
Success Track:  ────────────────────────────►  Success
                    ↓ (virhe)
Failure Track:  ────────────────────────────►  Failure
```

### Konsepti

**Success path:**
```
Validate → CheckCustomer → CheckStock → CreateOrder → Return Success
```

**Jos jokin epäonnistuu, hypätään failure-raiteelle:**
```
Validate → CheckCustomer → [FAILURE] ───────────────► Return Failure
            ↓ Virhe!
```

### Esimerkki

```csharp
public async Task<Result<Order>> CreateOrderAsync(CreateOrderDto dto)
{
    // Validate
    var validateResult = ValidateOrder(dto);
    if (validateResult.IsFailure)
        return Result.Failure<Order>(validateResult.Error);  // ← Hyppää failure-raiteelle
    
    // Check customer
    var customerResult = await CheckCustomerAsync(dto.CustomerId);
    if (customerResult.IsFailure)
        return Result.Failure<Order>(customerResult.Error);  // ← Hyppää failure-raiteelle
    
    // Check stock
    var stockResult = await CheckStockAsync(dto.Items);
    if (stockResult.IsFailure)
        return Result.Failure<Order>(stockResult.Error);  // ← Hyppää failure-raiteelle
    
    // Create order (success-raiteella)
    var order = new Order { ... };
    await _orderRepository.AddAsync(order);
    
    return Result.Success(order);  // ← Success!
}
```

**Kontrollivirta on selvä ja lineaarinen!**

---

## Toteutus C#:ssa

### Yksinkertainen Result<T>

```csharp
public class Result<T>
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public T Value { get; }
    public string Error { get; }
    
    // Private constructor
    private Result(bool isSuccess, T value, string error)
    {
        if (isSuccess && !string.IsNullOrEmpty(error))
            throw new InvalidOperationException("Success result cannot have error");
        if (!isSuccess && string.IsNullOrEmpty(error))
            throw new InvalidOperationException("Failure result must have error");
        
        IsSuccess = isSuccess;
        Value = value;
        Error = error;
    }
    
    // Factory methods
    public static Result<T> Success(T value)
        => new Result<T>(true, value, string.Empty);
    
    public static Result<T> Failure(string error)
        => new Result<T>(false, default, error);
}
```

### Käyttö

```csharp
// Success
var result = Result<Order>.Success(order);
Console.WriteLine(result.IsSuccess);  // true
Console.WriteLine(result.Value);      // Order object

// Failure
var result = Result<Order>.Failure("Customer not found");
Console.WriteLine(result.IsFailure);  // true
Console.WriteLine(result.Error);      // "Customer not found"
```

### Non-generic Result

```csharp
public class Result
{
    public bool IsSuccess { get; protected set; }
    public bool IsFailure => !IsSuccess;
    public string Error { get; protected set; } = string.Empty;
    
    protected Result(bool isSuccess, string error)
    {
        IsSuccess = isSuccess;
        Error = error;
    }
    
    public static Result Success() 
        => new Result(true, string.Empty);
    
    public static Result Failure(string error) 
        => new Result(false, error);
    
    // For Result<T>
    public static Result<T> Success<T>(T value) 
        => Result<T>.Success(value);
    
    public static Result<T> Failure<T>(string error) 
        => Result<T>.Failure(error);
}
```

**Käyttö operaatioille ilman palautusarvoa:**

```csharp
public async Task<Result> DeleteOrderAsync(int id)
{
    var order = await _repository.GetByIdAsync(id);
    if (order == null)
        return Result.Failure("Order not found");
    
    await _repository.DeleteAsync(id);
    return Result.Success();
}
```

### Paranneltu versio: ErrorType

```csharp
public enum ErrorType
{
    Validation,
    NotFound,
    Conflict,
    Unauthorized,
    Forbidden,
    InternalError
}

public class Result<T>
{
    public bool IsSuccess { get; }
    public bool IsFailure => !IsSuccess;
    public T Value { get; }
    public string Error { get; }
    public ErrorType ErrorType { get; }
    
    // ...
    
    public static Result<T> Failure(string error, ErrorType errorType = ErrorType.Validation)
        => new Result<T>(false, default, error, errorType);
}
```

**Controller:**

```csharp
if (result.IsFailure)
{
    return result.ErrorType switch
    {
        ErrorType.NotFound => NotFound(new { error = result.Error }),
        ErrorType.Conflict => Conflict(new { error = result.Error }),
        ErrorType.Unauthorized => Unauthorized(new { error = result.Error }),
        ErrorType.Validation => BadRequest(new { error = result.Error }),
        _ => StatusCode(500, new { error = result.Error })
    };
}
```

---

## Result vs Exceptions

### Milloin Result?

**✅ Käytä Result kun:**
- Virhe on **odotettavissa** (expected error)
- Virhe on osa normaalia kontrollivirtaa
- Haluat eksplisiittisen virheenkäsittelyn
- Performance on kriittinen

**Esimerkkejä:**
```csharp
Result<User> FindUserByEmail(string email)  // ← Käyttäjä ei välttämättä löydy
Result<Order> CreateOrder(CreateOrderDto)   // ← Validointi voi epäonnistua
Result DeleteResource(int id)               // ← Resurssi ei välttämättä ole olemassa
```

### Milloin Exception?

**✅ Käytä Exception kun:**
- Virhe on **odottamaton** (unexpected error)
- Ohjelmavirhe (bug)
- Infrastruktuuri-ongelma
- Katastrofaalinen virhe

**Esimerkkejä:**
```csharp
throw new ArgumentNullException(nameof(dto));        // ← Programmer error
throw new InvalidOperationException("DB not connected");  // ← System error
throw new OutOfMemoryException();                    // ← Catastrophic
```

### Vertailu

| Kriteeeri | Result | Exception |
|-----------|--------|-----------|
| **Signatointi** | Eksplisiittinen | Implisiittinen |
| **Performance** | Nopea | Hidas |
| **Kontrollivirta** | Lineaarinen | Hyppäävä |
| **Käyttötapaus** | Expected errors | Unexpected errors |
| **Tyypillinen koodi** | if (result.IsFailure) | try-catch |

### Hybrid-lähestymistapa (Suositeltu)

**Result odotettaville virheille:**
```csharp
public async Task<Result<Order>> CreateOrderAsync(CreateOrderDto dto)
{
    // Validointi, business rules → Result
    if (dto.Items.Count == 0)
        return Result.Failure<Order>("Order must have items");
    
    // ...
    
    return Result.Success(order);
}
```

**Exception odottamattomille:**
```csharp
public async Task<Result<Order>> CreateOrderAsync(CreateOrderDto dto)
{
    try
    {
        // ... business logic ...
        return Result.Success(order);
    }
    catch (DbUpdateException ex)  // ← Database error
    {
        _logger.LogError(ex, "Database error creating order");
        throw; // Re-throw - tämä on odottamaton!
    }
}
```

---

## Käytännön esimerkkejä

### Esimerkki 1: Use Case

```csharp
public class CreateBookingUseCase
{
    private readonly IBookingRepository _bookingRepository;
    private readonly IResourceRepository _resourceRepository;
    
    public async Task<Result<BookingResponseDto>> ExecuteAsync(CreateBookingDto dto)
    {
        // Validate
        var booking = new Booking
        {
            ResourceId = dto.ResourceId,
            BookedBy = dto.BookedBy,
            StartTime = dto.StartTime,
            EndTime = dto.EndTime
        };
        
        try
        {
            booking.Validate();
        }
        catch (InvalidOperationException ex)
        {
            return Result.Failure<BookingResponseDto>(ex.Message);
        }
        
        // Check resource exists
        var resource = await _resourceRepository.GetByIdAsync(dto.ResourceId);
        if (resource == null)
            return Result.Failure<BookingResponseDto>(
                $"Resource {dto.ResourceId} not found", 
                ErrorType.NotFound);
        
        if (!resource.IsAvailable)
            return Result.Failure<BookingResponseDto>(
                $"Resource {resource.Name} is not available",
                ErrorType.Conflict);
        
        // Check overlap
        var hasOverlap = await _bookingRepository.HasOverlappingBookingAsync(
            dto.ResourceId, 
            dto.StartTime, 
            dto.EndTime);
        
        if (hasOverlap)
            return Result.Failure<BookingResponseDto>(
                $"Resource {resource.Name} is already booked",
                ErrorType.Conflict);
        
        // Create
        booking.Status = BookingStatus.Confirmed;
        var created = await _bookingRepository.AddAsync(booking);
        
        // Success
        return Result.Success(new BookingResponseDto
        {
            Id = created.Id,
            ResourceName = resource.Name,
            // ...
        });
    }
}
```

### Esimerkki 2: Controller

```csharp
[ApiController]
[Route("api/[controller]")]
public class BookingsController : ControllerBase
{
    private readonly CreateBookingUseCase _createBookingUseCase;
    
    [HttpPost]
    public async Task<ActionResult<BookingResponseDto>> Create(
        [FromBody] CreateBookingDto dto)
    {
        var result = await _createBookingUseCase.ExecuteAsync(dto);
        
        if (result.IsFailure)
        {
            return result.ErrorType switch
            {
                ErrorType.NotFound => NotFound(new { error = result.Error }),
                ErrorType.Conflict => Conflict(new { error = result.Error }),
                _ => BadRequest(new { error = result.Error })
            };
        }
        
        return CreatedAtAction(
            nameof(GetById), 
            new { id = result.Value.Id }, 
            result.Value);
    }
    
    [HttpGet("{id}")]
    public async Task<ActionResult<BookingResponseDto>> GetById(int id)
    {
        var result = await _getBookingByIdUseCase.ExecuteAsync(id);
        
        if (result.IsFailure)
            return NotFound(new { error = result.Error });
        
        return Ok(result.Value);
    }
}
```

**Huomaa:**
- Ei try-catch!
- Selkeä kontrollivirta
- HTTP status code mappaus ErrorType:stä

---

## Result Pattern Libraries

### 1. FluentResults

**NuGet:** `FluentResults`

```csharp
public Result<Order> CreateOrder()
{
    return Result.Ok(order);
    return Result.Fail("Customer not found");
    return Result.Fail(new NotFoundError("Customer not found"));
}

// Chaining
var result = ValidateInput()
    .Bind(() => CheckCustomer())
    .Bind(() => CreateOrder());
```

### 2. LanguageExt (Funktionaalinen C#)

**NuGet:** `LanguageExt.Core`

```csharp
public Either<Error, Order> CreateOrder()
{
    return Right(order);  // Success
    return Left(new Error("Failed"));  // Failure
}

// Pattern matching
result.Match(
    Right: order => Ok(order),
    Left: error => BadRequest(error)
);
```

### 3. CSharpFunctionalExtensions

**NuGet:** `CSharpFunctionalExtensions`

```csharp
public Result<Order> CreateOrder()
{
    return Result.Success(order);
    return Result.Failure<Order>("Error message");
}

// Railway oriented programming
var result = Validate(dto)
    .OnSuccess(() => CheckCustomer())
    .OnSuccess(() => CreateOrder());
```

### Oma vs. Library?

**Oma toteutus:**
- ✅ Yksinkertainen
- ✅ Ei ylimääräisiä riippuvuuksia
- ✅ Täysi kontrolli

**Library:**
- ✅ Paljon valmiita ominaisuuksia
- ✅ Testattu ja bugiraportoitu
- ❌ Oppimiskäyrä

**Suositus:** Aloita omalla toteutuksella. Vaihda library:yn jos tarvitset lisää ominaisuuksia.

---

## Best Practices

### 1. Nimeä selkeästi

```csharp
// ✅ Hyvä
Result<Order> CreateOrder()
Result<User> FindUserByEmail(string email)
Result DeleteResource(int id)

// ❌ Huono (ei palauta Result:ia)
Order CreateOrder()
User? FindUserByEmail(string email)  // Nullable ei ole Result
```

### 2. Älä sekoita Result ja Exception

```csharp
// ❌ Huono - Sekoittaa Result ja Exception
public Result<Order> CreateOrder()
{
    if (validation fails)
        throw new ValidationException();  // ← Miksi ei Result?
    
    return Result.Success(order);
}

// ✅ Hyvä - Johdonmukainen
public Result<Order> CreateOrder()
{
    if (validation fails)
        return Result.Failure<Order>("Validation failed");
    
    return Result.Success(order);
}
```

### 3. Käytä ErrorType:iä

```csharp
Result.Failure<Order>("Not found", ErrorType.NotFound)
Result.Failure<Order>("Already exists", ErrorType.Conflict)
```

Helpottaa HTTP status code mappausta!

### 4. Dokumentoi Result

```csharp
/// <summary>
/// Creates a new order
/// </summary>
/// <returns>
/// Success: Created order
/// Failure: 
///   - "Customer not found" (NotFound)
///   - "Insufficient stock" (Conflict)
///   - "Invalid items" (Validation)
/// </returns>
public async Task<Result<Order>> CreateOrderAsync(CreateOrderDto dto)
{
    // ...
}
```

### 5. Extension methods controllerille

```csharp
public static class ResultExtensions
{
    public static ActionResult<T> ToActionResult<T>(this Result<T> result)
    {
        if (result.IsSuccess)
            return new OkObjectResult(result.Value);
        
        return result.ErrorType switch
        {
            ErrorType.NotFound => new NotFoundObjectResult(new { error = result.Error }),
            ErrorType.Conflict => new ConflictObjectResult(new { error = result.Error }),
            _ => new BadRequestObjectResult(new { error = result.Error })
        };
    }
}

// Controller
[HttpPost]
public async Task<ActionResult<Order>> Create([FromBody] CreateOrderDto dto)
{
    var result = await _useCase.ExecuteAsync(dto);
    return result.ToActionResult();  // ← Yksinkertainen!
}
```

---

## Yhteenveto

### Keskeiset opit

**Mikä on Result Pattern?**
- Funktionaalinen malli virheenkäsittelyyn
- Palauttaa Result<T>-olion (Success/Failure)
- Eksplisiittinen kontrollivirta

**Edut:**
- ✅ Selkeä ja eksplisiittinen
- ✅ Parempi performance
- ✅ Helpompi testata
- ✅ Lineaarinen kontrollivirta

**Haitat:**
- ❌ Enemmän koodia
- ❌ Oppimiskäyrä
- ❌ Ei standardoitu C#:ssa (vielä)

**Result vs Exception:**
- Result = Expected errors (validation, not found, etc.)
- Exception = Unexpected errors (bugs, system errors)

**Railway Oriented Programming:**
- Success-raite: Kaikki OK → jatka
- Failure-raite: Virhe → lopeta ja palauta virhe

### Milloin käyttää?

**Käytä Result kun:**
- Clean Architecture / Domain-Driven Design
- Use Case -pohjainen arkkitehtuuri
- Haluat eksplisiittisen virheenkäsittelyn
- Performance on tärkeä

**Älä käytä jos:**
- Yksinkertainen CRUD-sovellus
- Tiimi ei ole valmis funktionaaliseen ohjelmointiin
- Olemassa oleva codebase käyttää vain Exceptioneja

### Seuraavat askeleet

- Kokeile Result-patternia omassa projektissa
- Tutustu [Railway Oriented Programming](https://fsharpforfunandprofit.com/rop/)
- Kokeile FluentResults-kirjastoa
- Lue [Clean Architecture](../Architecture/Clean-Architecture.md)

---

**Muista:** Result Pattern ei korvaa kaikkia exceptioneita. Käytä molempia oikein!

**Expected errors → Result**  
**Unexpected errors → Exception**
