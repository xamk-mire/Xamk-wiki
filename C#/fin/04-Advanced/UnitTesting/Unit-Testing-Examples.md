# Yksikkötestaus - Esimerkit

Tämä tiedosto sisältää kattavat koodiesimerkit yksikkötestauksesta xUnit:illa.

## Sisällysluettelo

1. [Perus Assert-esimerkit](#perus-assert-esimerkit)
2. [Theory ja InlineData](#theory-ja-inlinedata)
3. [Mocking Moq:lla](#mocking-moqlla)
4. [Async-testit](#async-testit)
5. [Exception-testit](#exception-testit)
6. [Kokoelma-testit](#kokoelma-testit)
7. [Kattava esimerkki: UserService](#kattava-esimerkki-userservice)

---

## Perus Assert-esimerkit

### Esimerkki 1: Calculator-luokka

Testattava koodi:

```csharp
public class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    public int Subtract(int a, int b)
    {
        return a - b;
    }

    public int Multiply(int a, int b)
    {
        return a * b;
    }

    public double Divide(int a, int b)
    {
        if (b == 0)
            throw new DivideByZeroException("Cannot divide by zero");
        return (double)a / b;
    }

    public bool IsEven(int number)
    {
        return number % 2 == 0;
    }
}
```

Testit:

```csharp
using Xunit;

public class CalculatorTests
{
    [Fact]
    public void Add_PositiveNumbers_ReturnsSum()
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.Add(5, 3);

        // Assert
        Assert.Equal(8, result);
    }

    [Fact]
    public void Add_NegativeNumbers_ReturnsSum()
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.Add(-5, -3);

        // Assert
        Assert.Equal(-8, result);
    }

    [Fact]
    public void Subtract_ShouldReturnDifference()
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.Subtract(10, 3);

        // Assert
        Assert.Equal(7, result);
    }

    [Fact]
    public void Multiply_ShouldReturnProduct()
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.Multiply(4, 5);

        // Assert
        Assert.Equal(20, result);
    }

    [Fact]
    public void IsEven_EvenNumber_ReturnsTrue()
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        bool result = calculator.IsEven(4);

        // Assert
        Assert.True(result);
    }

    [Fact]
    public void IsEven_OddNumber_ReturnsFalse()
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        bool result = calculator.IsEven(5);

        // Assert
        Assert.False(result);
    }
}
```

### Esimerkki 2: String-käsittely

Testattava koodi:

```csharp
public class StringHelper
{
    public string Reverse(string input)
    {
        if (string.IsNullOrEmpty(input))
            return input;

        char[] chars = input.ToCharArray();
        Array.Reverse(chars);
        return new string(chars);
    }

    public bool IsPalindrome(string input)
    {
        if (string.IsNullOrEmpty(input))
            return false;

        string reversed = Reverse(input);
        return input.Equals(reversed, StringComparison.OrdinalIgnoreCase);
    }

    public int CountWords(string input)
    {
        if (string.IsNullOrWhiteSpace(input))
            return 0;

        return input.Split(new[] { ' ', '\t', '\n' }, 
            StringSplitOptions.RemoveEmptyEntries).Length;
    }
}
```

Testit:

```csharp
public class StringHelperTests
{
    [Fact]
    public void Reverse_ValidString_ReturnsReversed()
    {
        // Arrange
        StringHelper helper = new StringHelper();

        // Act
        string result = helper.Reverse("hello");

        // Assert
        Assert.Equal("olleh", result);
    }

    [Fact]
    public void Reverse_EmptyString_ReturnsEmpty()
    {
        // Arrange
        StringHelper helper = new StringHelper();

        // Act
        string result = helper.Reverse("");

        // Assert
        Assert.Equal("", result);
    }

    [Fact]
    public void IsPalindrome_ValidPalindrome_ReturnsTrue()
    {
        // Arrange
        StringHelper helper = new StringHelper();

        // Act
        bool result = helper.IsPalindrome("racecar");

        // Assert
        Assert.True(result);
    }

    [Fact]
    public void IsPalindrome_NotPalindrome_ReturnsFalse()
    {
        // Arrange
        StringHelper helper = new StringHelper();

        // Act
        bool result = helper.IsPalindrome("hello");

        // Assert
        Assert.False(result);
    }

    [Fact]
    public void CountWords_MultipleWords_ReturnsCount()
    {
        // Arrange
        StringHelper helper = new StringHelper();

        // Act
        int result = helper.CountWords("Hello world from tests");

        // Assert
        Assert.Equal(4, result);
    }

    [Fact]
    public void CountWords_EmptyString_ReturnsZero()
    {
        // Arrange
        StringHelper helper = new StringHelper();

        // Act
        int result = helper.CountWords("");

        // Assert
        Assert.Equal(0, result);
    }
}
```

---

## Theory ja InlineData

### Esimerkki 1: Parametrisoidut Calculator-testit

```csharp
public class CalculatorTheoryTests
{
    [Theory]
    [InlineData(2, 3, 5)]
    [InlineData(0, 0, 0)]
    [InlineData(-1, 1, 0)]
    [InlineData(-5, -3, -8)]
    [InlineData(100, 200, 300)]
    public void Add_VariousInputs_ReturnsCorrectSum(int a, int b, int expected)
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.Add(a, b);

        // Assert
        Assert.Equal(expected, result);
    }

    [Theory]
    [InlineData(10, 2, 5.0)]
    [InlineData(10, 3, 3.333)]
    [InlineData(0, 5, 0.0)]
    [InlineData(-10, 2, -5.0)]
    public void Divide_VariousInputs_ReturnsQuotient(int a, int b, double expected)
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        double result = calculator.Divide(a, b);

        // Assert
        Assert.Equal(expected, result, 3); // 3 desimaalin tarkkuus
    }

    [Theory]
    [InlineData(2, true)]
    [InlineData(3, false)]
    [InlineData(0, true)]
    [InlineData(-4, true)]
    [InlineData(-5, false)]
    public void IsEven_VariousNumbers_ReturnsCorrectResult(int number, bool expected)
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        bool result = calculator.IsEven(number);

        // Assert
        Assert.Equal(expected, result);
    }
}
```

### Esimerkki 2: MemberData

```csharp
public class CalculatorMemberDataTests
{
    public static IEnumerable<object[]> AddTestData()
    {
        yield return new object[] { 2, 3, 5 };
        yield return new object[] { -1, 1, 0 };
        yield return new object[] { 0, 0, 0 };
        yield return new object[] { 100, 200, 300 };
    }

    public static IEnumerable<object[]> ComplexTestData()
    {
        yield return new object[] 
        { 
            new int[] { 1, 2, 3, 4, 5 }, 
            15 
        };
        yield return new object[] 
        { 
            new int[] { }, 
            0 
        };
        yield return new object[] 
        { 
            new int[] { -1, -2, -3 }, 
            -6 
        };
    }

    [Theory]
    [MemberData(nameof(AddTestData))]
    public void Add_MemberData_ReturnsCorrectSum(int a, int b, int expected)
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = calculator.Add(a, b);

        // Assert
        Assert.Equal(expected, result);
    }

    [Theory]
    [MemberData(nameof(ComplexTestData))]
    public void Sum_Array_ReturnsTotal(int[] numbers, int expected)
    {
        // Arrange
        Calculator calculator = new Calculator();

        // Act
        int result = numbers.Sum();

        // Assert
        Assert.Equal(expected, result);
    }
}
```

---

## Mocking Moqlla

### Esimerkki 1: Email Service

Testattava koodi:

```csharp
public interface IEmailService
{
    bool SendEmail(string to, string subject, string body);
    bool SendWelcomeEmail(string email, string name);
}

public interface IUserRepository
{
    void Save(User user);
    User GetById(int id);
    List<User> GetAll();
    void Delete(int id);
}

public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public bool IsActive { get; set; }
}

public class UserService
{
    private readonly IUserRepository _userRepository;
    private readonly IEmailService _emailService;

    public UserService(IUserRepository userRepository, IEmailService emailService)
    {
        _userRepository = userRepository;
        _emailService = emailService;
    }

    public void CreateUser(string name, string email)
    {
        User user = new User
        {
            Name = name,
            Email = email,
            IsActive = true
        };

        _userRepository.Save(user);
        _emailService.SendWelcomeEmail(email, name);
    }

    public User GetUser(int id)
    {
        return _userRepository.GetById(id);
    }

    public int GetActiveUserCount()
    {
        return _userRepository.GetAll().Count(u => u.IsActive);
    }

    public void DeactivateUser(int id)
    {
        User user = _userRepository.GetById(id);
        if (user != null)
        {
            user.IsActive = false;
            _userRepository.Save(user);
        }
    }
}
```

Testit:

```csharp
using Moq;
using Xunit;

public class UserServiceTests
{
    [Fact]
    public void CreateUser_ValidData_SavesUserAndSendsEmail()
    {
        // Arrange
        Mock<IUserRepository> userRepoMock = new Mock<IUserRepository>();
        Mock<IEmailService> emailServiceMock = new Mock<IEmailService>();
        UserService userService = new UserService(userRepoMock.Object, emailServiceMock.Object);

        // Act
        userService.CreateUser("Matti", "matti@example.com");

        // Assert
        userRepoMock.Verify(x => x.Save(It.Is<User>(u => 
            u.Name == "Matti" && 
            u.Email == "matti@example.com" &&
            u.IsActive == true)), 
            Times.Once);

        emailServiceMock.Verify(x => 
            x.SendWelcomeEmail("matti@example.com", "Matti"), 
            Times.Once);
    }

    [Fact]
    public void GetUser_ValidId_ReturnsUser()
    {
        // Arrange
        User expectedUser = new User { Id = 1, Name = "Test", Email = "test@test.com" };
        Mock<IUserRepository> userRepoMock = new Mock<IUserRepository>();
        userRepoMock.Setup(x => x.GetById(1)).Returns(expectedUser);

        Mock<IEmailService> emailServiceMock = new Mock<IEmailService>();
        UserService userService = new UserService(userRepoMock.Object, emailServiceMock.Object);

        // Act
        User result = userService.GetUser(1);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(expectedUser.Id, result.Id);
        Assert.Equal(expectedUser.Name, result.Name);
    }

    [Fact]
    public void GetActiveUserCount_ReturnsCorrectCount()
    {
        // Arrange
        List<User> users = new List<User>
        {
            new User { Id = 1, IsActive = true },
            new User { Id = 2, IsActive = true },
            new User { Id = 3, IsActive = false }
        };

        Mock<IUserRepository> userRepoMock = new Mock<IUserRepository>();
        userRepoMock.Setup(x => x.GetAll()).Returns(users);

        Mock<IEmailService> emailServiceMock = new Mock<IEmailService>();
        UserService userService = new UserService(userRepoMock.Object, emailServiceMock.Object);

        // Act
        int result = userService.GetActiveUserCount();

        // Assert
        Assert.Equal(2, result);
    }

    [Fact]
    public void DeactivateUser_ExistingUser_DeactivatesAndSaves()
    {
        // Arrange
        User user = new User { Id = 1, Name = "Test", IsActive = true };
        Mock<IUserRepository> userRepoMock = new Mock<IUserRepository>();
        userRepoMock.Setup(x => x.GetById(1)).Returns(user);

        Mock<IEmailService> emailServiceMock = new Mock<IEmailService>();
        UserService userService = new UserService(userRepoMock.Object, emailServiceMock.Object);

        // Act
        userService.DeactivateUser(1);

        // Assert
        Assert.False(user.IsActive);
        userRepoMock.Verify(x => x.Save(user), Times.Once);
    }

    [Fact]
    public void DeactivateUser_NonExistingUser_DoesNotSave()
    {
        // Arrange
        Mock<IUserRepository> userRepoMock = new Mock<IUserRepository>();
        userRepoMock.Setup(x => x.GetById(999)).Returns((User)null);

        Mock<IEmailService> emailServiceMock = new Mock<IEmailService>();
        UserService userService = new UserService(userRepoMock.Object, emailServiceMock.Object);

        // Act
        userService.DeactivateUser(999);

        // Assert
        userRepoMock.Verify(x => x.Save(It.IsAny<User>()), Times.Never);
    }
}
```

---

## Async-testit

Testattava koodi:

```csharp
public interface IApiClient
{
    Task<string> GetDataAsync(string url);
}

public class DataService
{
    private readonly IApiClient _apiClient;

    public DataService(IApiClient apiClient)
    {
        _apiClient = apiClient;
    }

    public async Task<string> FetchDataAsync(string url)
    {
        return await _apiClient.GetDataAsync(url);
    }

    public async Task<int> ProcessDataAsync(string data)
    {
        await Task.Delay(100); // Simuloi prosessointia
        return data.Length;
    }
}
```

Testit:

```csharp
public class DataServiceTests
{
    [Fact]
    public async Task FetchDataAsync_ValidUrl_ReturnsData()
    {
        // Arrange
        Mock<IApiClient> apiClientMock = new Mock<IApiClient>();
        apiClientMock.Setup(x => x.GetDataAsync(It.IsAny<string>()))
            .ReturnsAsync("test data");

        DataService service = new DataService(apiClientMock.Object);

        // Act
        string result = await service.FetchDataAsync("http://test.com");

        // Assert
        Assert.Equal("test data", result);
        apiClientMock.Verify(x => x.GetDataAsync("http://test.com"), Times.Once);
    }

    [Fact]
    public async Task ProcessDataAsync_ValidData_ReturnsLength()
    {
        // Arrange
        Mock<IApiClient> apiClientMock = new Mock<IApiClient>();
        DataService service = new DataService(apiClientMock.Object);

        // Act
        int result = await service.ProcessDataAsync("hello");

        // Assert
        Assert.Equal(5, result);
    }

    [Fact]
    public async Task FetchDataAsync_ThrowsException_PropagatesException()
    {
        // Arrange
        Mock<IApiClient> apiClientMock = new Mock<IApiClient>();
        apiClientMock.Setup(x => x.GetDataAsync(It.IsAny<string>()))
            .ThrowsAsync(new HttpRequestException("Network error"));

        DataService service = new DataService(apiClientMock.Object);

        // Act & Assert
        await Assert.ThrowsAsync<HttpRequestException>(
            async () => await service.FetchDataAsync("http://test.com"));
    }
}
```

---

## Exception-testit

```csharp
public class ValidationService
{
    public void ValidateAge(int age)
    {
        if (age < 0)
            throw new ArgumentException("Age cannot be negative", nameof(age));
        if (age > 150)
            throw new ArgumentException("Age is too high", nameof(age));
    }

    public void ValidateEmail(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentNullException(nameof(email));
        if (!email.Contains("@"))
            throw new FormatException("Invalid email format");
    }
}

public class ValidationServiceTests
{
    [Fact]
    public void ValidateAge_NegativeAge_ThrowsArgumentException()
    {
        // Arrange
        ValidationService service = new ValidationService();

        // Act & Assert
        ArgumentException exception = Assert.Throws<ArgumentException>(() => 
            service.ValidateAge(-1));
        
        Assert.Equal("Age cannot be negative (Parameter 'age')", exception.Message);
    }

    [Fact]
    public void ValidateAge_TooHighAge_ThrowsArgumentException()
    {
        // Arrange
        ValidationService service = new ValidationService();

        // Act & Assert
        Assert.Throws<ArgumentException>(() => service.ValidateAge(200));
    }

    [Fact]
    public void ValidateAge_ValidAge_DoesNotThrow()
    {
        // Arrange
        ValidationService service = new ValidationService();

        // Act & Assert - Ei poikkeusta
        Exception exception = Record.Exception(() => service.ValidateAge(25));
        Assert.Null(exception);
    }

    [Fact]
    public void ValidateEmail_NullEmail_ThrowsArgumentNullException()
    {
        // Arrange
        ValidationService service = new ValidationService();

        // Act & Assert
        Assert.Throws<ArgumentNullException>(() => service.ValidateEmail(null));
    }

    [Fact]
    public void ValidateEmail_InvalidFormat_ThrowsFormatException()
    {
        // Arrange
        ValidationService service = new ValidationService();

        // Act & Assert
        Assert.Throws<FormatException>(() => service.ValidateEmail("notanemail"));
    }
}
```

---

## Kokoelma-testit

```csharp
public class ListHelper
{
    public List<int> GetEvenNumbers(List<int> numbers)
    {
        return numbers.Where(n => n % 2 == 0).ToList();
    }

    public List<int> RemoveDuplicates(List<int> numbers)
    {
        return numbers.Distinct().ToList();
    }
}

public class ListHelperTests
{
    [Fact]
    public void GetEvenNumbers_MixedList_ReturnsOnlyEven()
    {
        // Arrange
        ListHelper helper = new ListHelper();
        List<int> numbers = new List<int> { 1, 2, 3, 4, 5, 6 };

        // Act
        List<int> result = helper.GetEvenNumbers(numbers);

        // Assert
        Assert.Equal(3, result.Count);
        Assert.Contains(2, result);
        Assert.Contains(4, result);
        Assert.Contains(6, result);
        Assert.DoesNotContain(1, result);
        Assert.All(result, n => Assert.True(n % 2 == 0));
    }

    [Fact]
    public void GetEvenNumbers_EmptyList_ReturnsEmpty()
    {
        // Arrange
        ListHelper helper = new ListHelper();
        List<int> numbers = new List<int>();

        // Act
        List<int> result = helper.GetEvenNumbers(numbers);

        // Assert
        Assert.Empty(result);
    }

    [Fact]
    public void RemoveDuplicates_ListWithDuplicates_ReturnsUnique()
    {
        // Arrange
        ListHelper helper = new ListHelper();
        List<int> numbers = new List<int> { 1, 2, 2, 3, 3, 3, 4 };

        // Act
        List<int> result = helper.RemoveDuplicates(numbers);

        // Assert
        Assert.Equal(4, result.Count);
        Assert.Equal(new[] { 1, 2, 3, 4 }, result);
    }
}
```

---

## Kattava esimerkki: UserService

Tämä esimerkki yhdistää kaikki opitut asiat.

```csharp
// Domain
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public DateTime CreatedAt { get; set; }
    public bool IsActive { get; set; }
}

// Interfaces
public interface IUserRepository
{
    Task<User> GetByIdAsync(int id);
    Task<List<User>> GetAllAsync();
    Task SaveAsync(User user);
    Task DeleteAsync(int id);
    Task<bool> ExistsAsync(string email);
}

public interface IEmailService
{
    Task<bool> SendWelcomeEmailAsync(string email, string name);
    Task<bool> SendDeactivationEmailAsync(string email);
}

public interface ILogger
{
    void LogInfo(string message);
    void LogError(string message, Exception ex);
}

// Service
public class UserService
{
    private readonly IUserRepository _repository;
    private readonly IEmailService _emailService;
    private readonly ILogger _logger;

    public UserService(IUserRepository repository, IEmailService emailService, ILogger logger)
    {
        _repository = repository;
        _emailService = emailService;
        _logger = logger;
    }

    public async Task<User> CreateUserAsync(string name, string email)
    {
        // Validointi
        if (string.IsNullOrWhiteSpace(name))
            throw new ArgumentException("Name is required", nameof(name));
        if (string.IsNullOrWhiteSpace(email))
            throw new ArgumentException("Email is required", nameof(email));

        // Tarkista duplikaatti
        if (await _repository.ExistsAsync(email))
            throw new InvalidOperationException("User already exists");

        // Luo käyttäjä
        User user = new User
        {
            Name = name,
            Email = email,
            CreatedAt = DateTime.UtcNow,
            IsActive = true
        };

        try
        {
            await _repository.SaveAsync(user);
            await _emailService.SendWelcomeEmailAsync(email, name);
            _logger.LogInfo($"User created: {email}");
            return user;
        }
        catch (Exception ex)
        {
            _logger.LogError("Failed to create user", ex);
            throw;
        }
    }

    public async Task<User> GetUserAsync(int id)
    {
        if (id <= 0)
            throw new ArgumentException("Invalid id", nameof(id));

        return await _repository.GetByIdAsync(id);
    }

    public async Task DeactivateUserAsync(int id)
    {
        User user = await _repository.GetByIdAsync(id);
        if (user == null)
            throw new InvalidOperationException("User not found");

        user.IsActive = false;
        await _repository.SaveAsync(user);
        await _emailService.SendDeactivationEmailAsync(user.Email);
        _logger.LogInfo($"User deactivated: {user.Email}");
    }

    public async Task<int> GetActiveUserCountAsync()
    {
        List<User> users = await _repository.GetAllAsync();
        return users.Count(u => u.IsActive);
    }
}

// Tests
public class UserServiceTests
{
    private readonly Mock<IUserRepository> _repositoryMock;
    private readonly Mock<IEmailService> _emailServiceMock;
    private readonly Mock<ILogger> _loggerMock;
    private readonly UserService _userService;

    public UserServiceTests()
    {
        _repositoryMock = new Mock<IUserRepository>();
        _emailServiceMock = new Mock<IEmailService>();
        _loggerMock = new Mock<ILogger>();
        _userService = new UserService(
            _repositoryMock.Object,
            _emailServiceMock.Object,
            _loggerMock.Object);
    }

    [Fact]
    public async Task CreateUserAsync_ValidData_CreatesUserAndSendsEmail()
    {
        // Arrange
        _repositoryMock.Setup(x => x.ExistsAsync("test@test.com"))
            .ReturnsAsync(false);
        _emailServiceMock.Setup(x => x.SendWelcomeEmailAsync(It.IsAny<string>(), It.IsAny<string>()))
            .ReturnsAsync(true);

        // Act
        User user = await _userService.CreateUserAsync("Test User", "test@test.com");

        // Assert
        Assert.NotNull(user);
        Assert.Equal("Test User", user.Name);
        Assert.Equal("test@test.com", user.Email);
        Assert.True(user.IsActive);

        _repositoryMock.Verify(x => x.SaveAsync(It.IsAny<User>()), Times.Once);
        _emailServiceMock.Verify(x => 
            x.SendWelcomeEmailAsync("test@test.com", "Test User"), Times.Once);
        _loggerMock.Verify(x => 
            x.LogInfo(It.Is<string>(s => s.Contains("User created"))), Times.Once);
    }

    [Theory]
    [InlineData(null, "test@test.com")]
    [InlineData("", "test@test.com")]
    [InlineData("Test", null)]
    [InlineData("Test", "")]
    public async Task CreateUserAsync_InvalidData_ThrowsArgumentException(string name, string email)
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            async () => await _userService.CreateUserAsync(name, email));
    }

    [Fact]
    public async Task CreateUserAsync_DuplicateEmail_ThrowsInvalidOperationException()
    {
        // Arrange
        _repositoryMock.Setup(x => x.ExistsAsync("test@test.com"))
            .ReturnsAsync(true);

        // Act & Assert
        await Assert.ThrowsAsync<InvalidOperationException>(
            async () => await _userService.CreateUserAsync("Test", "test@test.com"));

        _repositoryMock.Verify(x => x.SaveAsync(It.IsAny<User>()), Times.Never);
    }

    [Fact]
    public async Task GetUserAsync_ValidId_ReturnsUser()
    {
        // Arrange
        User expectedUser = new User { Id = 1, Name = "Test", Email = "test@test.com" };
        _repositoryMock.Setup(x => x.GetByIdAsync(1))
            .ReturnsAsync(expectedUser);

        // Act
        User result = await _userService.GetUserAsync(1);

        // Assert
        Assert.NotNull(result);
        Assert.Equal(expectedUser.Id, result.Id);
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-1)]
    public async Task GetUserAsync_InvalidId_ThrowsArgumentException(int id)
    {
        // Act & Assert
        await Assert.ThrowsAsync<ArgumentException>(
            async () => await _userService.GetUserAsync(id));
    }

    [Fact]
    public async Task DeactivateUserAsync_ExistingUser_DeactivatesAndSendsEmail()
    {
        // Arrange
        User user = new User { Id = 1, Name = "Test", Email = "test@test.com", IsActive = true };
        _repositoryMock.Setup(x => x.GetByIdAsync(1))
            .ReturnsAsync(user);

        // Act
        await _userService.DeactivateUserAsync(1);

        // Assert
        Assert.False(user.IsActive);
        _repositoryMock.Verify(x => x.SaveAsync(user), Times.Once);
        _emailServiceMock.Verify(x => 
            x.SendDeactivationEmailAsync("test@test.com"), Times.Once);
        _loggerMock.Verify(x => 
            x.LogInfo(It.Is<string>(s => s.Contains("deactivated"))), Times.Once);
    }

    [Fact]
    public async Task DeactivateUserAsync_NonExistingUser_ThrowsInvalidOperationException()
    {
        // Arrange
        _repositoryMock.Setup(x => x.GetByIdAsync(999))
            .ReturnsAsync((User)null);

        // Act & Assert
        await Assert.ThrowsAsync<InvalidOperationException>(
            async () => await _userService.DeactivateUserAsync(999));
    }

    [Fact]
    public async Task GetActiveUserCountAsync_ReturnsCorrectCount()
    {
        // Arrange
        List<User> users = new List<User>
        {
            new User { Id = 1, IsActive = true },
            new User { Id = 2, IsActive = true },
            new User { Id = 3, IsActive = false },
            new User { Id = 4, IsActive = true }
        };
        _repositoryMock.Setup(x => x.GetAllAsync())
            .ReturnsAsync(users);

        // Act
        int count = await _userService.GetActiveUserCountAsync();

        // Assert
        Assert.Equal(3, count);
    }
}
```

---

## Yhteenveto

Nämä esimerkit kattavat:
- Perus-Assert metodit
- Theory ja InlineData
- Mocking Moq:lla
- Async-testit
- Exception-testit
- Kokoelma-testit
- Kattavan esimerkin kaikilla elementeillä

Palaa teoriaan: [Unit-Testing.md](Unit-Testing.md)

