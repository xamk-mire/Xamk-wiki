# Suunnittelumallit (Design Patterns)

## Materiaalit

Näistä design pattern:sta löydät erittäin hyvät materiaalit **[TÄÄLTÄ](https://refactoring.guru/design-patterns/csharp)**! Tuo materiaali kuvaa hyvin, että mikä on aina ongelma ja mikä malli ratkaisee sen ongelman. Siellä esimerkki ongelmat ja koodiesimerkit. Alla on joka tapauksessa suomeksi lyhyt kuvaus yleisimmistä patterneista.

## Mitä ovat suunnittelumallit (Design Patterns)?

Suunnittelumallit ovat testattuja ratkaisuja tietyille ohjelmointiongelmille. Ne eivät ole riippuvaisia tietystä ohjelmointikielestä, kuten C#:sta, mutta joitakin niistä käytetään laajasti monissa C#-sovelluksissa .NET-alustan luonteen vuoksi.

## Yleisimmät suunnittelumallit

### Singleton Pattern

Tätä mallia käytetään, kun luokalla pitäisi olla vain yksi ilmentymä koko sovelluksen ajan. Sitä käytetään usein asioihin kuten tietokantayhteydet tai lokitus, missä ei ole järkevää olla useita ilmentymiä.

**Esimerkki**: Kun kirjaudut johonkin puhelinsovellukseen, on kirjautunut käyttäjä yleensä singleton-tyyppinen muuttuja.

```csharp
public class Logger
{
    private static Logger _instance;

    private Logger() { }  // Yksityinen konstruktori

    public static Logger Instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = new Logger();
            }
            return _instance;
        }
    }

    public void Log(string message)
    {
        Console.WriteLine($"[LOG] {message}");
    }
}

// Käyttö
Logger.Instance.Log("Tämä on lokiviesti");
```

### Factory Method Pattern

Tätä käytetään, kun haluat luoda olion, mutta et tiedä olion tarkkaa tyyppiä käännösaikana. Factory Method Pattern käyttää metodia olioiden luomisen abstrahoimiseksi, joten olion tyyppi voidaan määrittää suorituksen aikana.

```csharp
public abstract class Animal
{
    public abstract void MakeSound();
}

public class Dog : Animal
{
    public override void MakeSound() => Console.WriteLine("Woof!");
}

public class Cat : Animal
{
    public override void MakeSound() => Console.WriteLine("Meow!");
}

public class AnimalFactory
{
    public static Animal CreateAnimal(string type)
    {
        return type.ToLower() switch
        {
            "dog" => new Dog(),
            "cat" => new Cat(),
            _ => throw new ArgumentException("Unknown animal type")
        };
    }
}

// Käyttö
Animal animal = AnimalFactory.CreateAnimal("dog");
animal.MakeSound();  // "Woof!"
```

### Builder Pattern

Jos olio on monimutkainen ja vaatii paljon asetusta tai konfigurointia, builder-mallia voidaan käyttää. Tämä tarkoittaa erillisen "builder"-olion luomista, joka on vastuussa pääolion asettamisesta vaiheittain.

```csharp
public class Pizza
{
    public string Dough { get; set; }
    public string Sauce { get; set; }
    public List<string> Toppings { get; set; } = new List<string>();
}

public class PizzaBuilder
{
    private Pizza _pizza = new Pizza();

    public PizzaBuilder WithDough(string dough)
    {
        _pizza.Dough = dough;
        return this;
    }

    public PizzaBuilder WithSauce(string sauce)
    {
        _pizza.Sauce = sauce;
        return this;
    }

    public PizzaBuilder AddTopping(string topping)
    {
        _pizza.Toppings.Add(topping);
        return this;
    }

    public Pizza Build() => _pizza;
}

// Käyttö
Pizza pizza = new PizzaBuilder()
    .WithDough("Thin")
    .WithSauce("Tomato")
    .AddTopping("Cheese")
    .AddTopping("Pepperoni")
    .Build();
```

### Observer Pattern

Tunnetaan myös nimellä Publish-Subscribe -malli, sitä käytetään luomaan yksi-moneen riippuvuus olioiden välillä, joten kun yksi olio muuttaa tilaansa, kaikki sen riippuvaiset ilmoitetaan ja päivitetään automaattisesti.

**Esimerkki**: Viestisovellukset toimivat tällä patternilla, kuten WhatsApp.

```csharp
public interface IObserver
{
    void Update(string message);
}

public class Subject
{
    private List<IObserver> _observers = new List<IObserver>();

    public void Attach(IObserver observer)
    {
        _observers.Add(observer);
    }

    public void Notify(string message)
    {
        foreach (var observer in _observers)
        {
            observer.Update(message);
        }
    }
}

public class ConcreteObserver : IObserver
{
    private string _name;

    public ConcreteObserver(string name)
    {
        _name = name;
    }

    public void Update(string message)
    {
        Console.WriteLine($"{_name} received: {message}");
    }
}

// Käyttö
Subject subject = new Subject();
subject.Attach(new ConcreteObserver("Observer 1"));
subject.Attach(new ConcreteObserver("Observer 2"));
subject.Notify("Hello!");
```

### Strategy Pattern

Tätä mallia käytetään, kun haluat valita algoritmin suorituksen aikana. Se sisältää yhteisen rajapinnan algoritmiperheelle ja sitten jokaisen algoritmin kapseloi omaan luokkaansa.

```csharp
public interface IPaymentStrategy
{
    void Pay(decimal amount);
}

public class CreditCardPayment : IPaymentStrategy
{
    public void Pay(decimal amount)
    {
        Console.WriteLine($"Paid {amount} using Credit Card");
    }
}

public class PayPalPayment : IPaymentStrategy
{
    public void Pay(decimal amount)
    {
        Console.WriteLine($"Paid {amount} using PayPal");
    }
}

public class PaymentContext
{
    private IPaymentStrategy _strategy;

    public PaymentContext(IPaymentStrategy strategy)
    {
        _strategy = strategy;
    }

    public void ExecutePayment(decimal amount)
    {
        _strategy.Pay(amount);
    }
}

// Käyttö
PaymentContext context = new PaymentContext(new CreditCardPayment());
context.ExecutePayment(100.00m);
```

### Decorator Pattern

Tämä malli mahdollistaa käyttäytymisen lisäämisen yksittäiseen olioon, joko staattisesti tai dynaamisesti, vaikuttamatta muiden samasta luokasta olevien olioiden käyttäytymiseen. Se sisältää joukon koriste-luokkia, joita käytetään betonikomponenttien ympäröimiseen.

```csharp
public interface ICoffee
{
    string GetDescription();
    decimal GetCost();
}

public class SimpleCoffee : ICoffee
{
    public string GetDescription() => "Simple Coffee";
    public decimal GetCost() => 2.00m;
}

public class CoffeeDecorator : ICoffee
{
    protected ICoffee _coffee;

    public CoffeeDecorator(ICoffee coffee)
    {
        _coffee = coffee;
    }

    public virtual string GetDescription() => _coffee.GetDescription();
    public virtual decimal GetCost() => _coffee.GetCost();
}

public class MilkDecorator : CoffeeDecorator
{
    public MilkDecorator(ICoffee coffee) : base(coffee) { }

    public override string GetDescription() => _coffee.GetDescription() + ", Milk";
    public override decimal GetCost() => _coffee.GetCost() + 0.50m;
}

// Käyttö
ICoffee coffee = new MilkDecorator(new SimpleCoffee());
Console.WriteLine($"{coffee.GetDescription()}: {coffee.GetCost()}");
```

### Facade Pattern

Tätä käytetään tarjoamaan yksinkertaistettu rajapinta monimutkaiseen järjestelmään. Se sisältää luokan, joka piilottaa järjestelmän monimutkaisuuden ja tarjoaa yksinkertaisemman API:n asiakkaalle.

```csharp
public class SubsystemA
{
    public void OperationA() => Console.WriteLine("SubsystemA: OperationA");
}

public class SubsystemB
{
    public void OperationB() => Console.WriteLine("SubsystemB: OperationB");
}

public class Facade
{
    private SubsystemA _subsystemA;
    private SubsystemB _subsystemB;

    public Facade()
    {
        _subsystemA = new SubsystemA();
        _subsystemB = new SubsystemB();
    }

    public void SimpleOperation()
    {
        _subsystemA.OperationA();
        _subsystemB.OperationB();
    }
}

// Käyttö
Facade facade = new Facade();
facade.SimpleOperation();  // Piilottaa monimutkaisuuden
```

### Adapter Pattern

Tätä käytetään, kun haluat kahden yhteensopimattoman rajapinnan toimivan yhdessä. Sovitin käärii toisen rajapinnan ja tekee sen yhteensopivaksi toisen kanssa.

```csharp
public interface ITarget
{
    string Request();
}

public class Adaptee
{
    public string SpecificRequest() => "Specific request";
}

public class Adapter : ITarget
{
    private Adaptee _adaptee;

    public Adapter(Adaptee adaptee)
    {
        _adaptee = adaptee;
    }

    public string Request()
    {
        return $"Adapter: {_adaptee.SpecificRequest()}";
    }
}

// Käyttö
Adaptee adaptee = new Adaptee();
ITarget target = new Adapter(adaptee);
Console.WriteLine(target.Request());
```

### Prototype Pattern

Tätä mallia käytetään, kun luotavien olioiden tyyppi määräytyy prototyyppiesimerkin perusteella, joka kloonataan tuottamaan uusia olioita. Tämä on erityisen hyödyllistä, kun yksittäisten identtisten olioiden luominen on kallista.

```csharp
public interface IPrototype
{
    IPrototype Clone();
}

public class ConcretePrototype : IPrototype
{
    public string Property { get; set; }

    public IPrototype Clone()
    {
        return new ConcretePrototype { Property = this.Property };
    }
}

// Käyttö
ConcretePrototype original = new ConcretePrototype { Property = "Original" };
ConcretePrototype clone = (ConcretePrototype)original.Clone();
```

### Mediator Pattern

Mediator-mallia käytetään, kun useat oliot kommunikoivat toistensa kanssa ja syntyy monimutkainen riippuvuusverkko. Mediator toimii **keskitetyn välittäjän** roolissa: sen sijaan, että oliot kutsuvat toisiaan suoraan, ne lähettävät viestejä Mediatorille, joka ohjaa viestin oikealle vastaanottajalle.

**Gang of Four määritelmä:**
> "Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly."

**Ongelma ilman Mediatoria:**

```
❌ Suorat riippuvuudet (tight coupling):

    ComponentA ←→ ComponentB
        ↕           ↕
    ComponentC ←→ ComponentD

Jokainen komponentti tuntee muut → riippuvuudet kasvavat räjähdysmäisesti
```

**Ratkaisu Mediatorilla:**

```
✅ Keskitetty kommunikaatio (loose coupling):

    ComponentA → Mediator ← ComponentB
                   ↕
    ComponentC → Mediator ← ComponentD

Jokainen komponentti tuntee vain Mediatorin
```

**Esimerkki: Chat-huone**

Chatissa käyttäjät eivät lähetä viestejä suoraan toisilleen, vaan **chat-huone** (Mediator) välittää viestit kaikille osallistujille:

```csharp
// Mediator-rajapinta
public interface IChatRoom
{
    void SendMessage(string message, IUser sender);
    void AddUser(IUser user);
}

// Käyttäjä-rajapinta
public interface IUser
{
    string Name { get; }
    void ReceiveMessage(string message, string senderName);
    void SendMessage(string message);
}

// Konkreettinen Mediator
public class ChatRoom : IChatRoom
{
    private readonly List<IUser> _users = new();

    public void AddUser(IUser user)
    {
        _users.Add(user);
        Console.WriteLine($"*** {user.Name} liittyi huoneeseen ***");
    }

    public void SendMessage(string message, IUser sender)
    {
        // Välittää viestin kaikille PAITSI lähettäjälle
        foreach (var user in _users)
        {
            if (user != sender)
            {
                user.ReceiveMessage(message, sender.Name);
            }
        }
    }
}

// Konkreettinen käyttäjä
public class ChatUser : IUser
{
    private readonly IChatRoom _chatRoom;

    public string Name { get; }

    public ChatUser(string name, IChatRoom chatRoom)
    {
        Name = name;
        _chatRoom = chatRoom;
    }

    public void SendMessage(string message)
    {
        Console.WriteLine($"{Name} lähettää: {message}");
        _chatRoom.SendMessage(message, this);  // Lähettää Mediatorille, EI suoraan toisille
    }

    public void ReceiveMessage(string message, string senderName)
    {
        Console.WriteLine($"{Name} vastaanotti [{senderName}]: {message}");
    }
}

// Käyttö
IChatRoom chatRoom = new ChatRoom();

var matti = new ChatUser("Matti", chatRoom);
var liisa = new ChatUser("Liisa", chatRoom);
var pekka = new ChatUser("Pekka", chatRoom);

chatRoom.AddUser(matti);
chatRoom.AddUser(liisa);
chatRoom.AddUser(pekka);

matti.SendMessage("Moi kaikille!");
// Liisa vastaanotti [Matti]: Moi kaikille!
// Pekka vastaanotti [Matti]: Moi kaikille!

liisa.SendMessage("Moi Matti!");
// Matti vastaanotti [Liisa]: Moi Matti!
// Pekka vastaanotti [Liisa]: Moi Matti!
```

**Esimerkki: Lennonjohtotorni**

Lentokoneet eivät kommunikoi suoraan toistensa kanssa, vaan lennonjohtotorni (Mediator) koordinoi kaiken:

```csharp
// Mediator
public interface IControlTower
{
    void RequestLanding(Aircraft aircraft);
    void RequestTakeoff(Aircraft aircraft);
}

// Colleague
public abstract class Aircraft
{
    protected readonly IControlTower _tower;
    public string FlightNumber { get; }

    protected Aircraft(string flightNumber, IControlTower tower)
    {
        FlightNumber = flightNumber;
        _tower = tower;
    }

    public abstract void Land();
    public abstract void TakeOff();
}

// Konkreettinen Mediator
public class ControlTower : IControlTower
{
    private bool _runwayFree = true;

    public void RequestLanding(Aircraft aircraft)
    {
        if (_runwayFree)
        {
            _runwayFree = false;
            Console.WriteLine($"Torni: {aircraft.FlightNumber}, kiitotie vapaa. Laskeutumislupa myönnetty.");
            aircraft.Land();
            _runwayFree = true;
        }
        else
        {
            Console.WriteLine($"Torni: {aircraft.FlightNumber}, kiitotie varattu. Odota vuoroasi.");
        }
    }

    public void RequestTakeoff(Aircraft aircraft)
    {
        if (_runwayFree)
        {
            _runwayFree = false;
            Console.WriteLine($"Torni: {aircraft.FlightNumber}, lentoonlähtölupa myönnetty.");
            aircraft.TakeOff();
            _runwayFree = true;
        }
        else
        {
            Console.WriteLine($"Torni: {aircraft.FlightNumber}, kiitotie varattu. Odota.");
        }
    }
}

// Konkreettinen lentokone
public class CommercialFlight : Aircraft
{
    public CommercialFlight(string flightNumber, IControlTower tower) 
        : base(flightNumber, tower) { }

    public override void Land()
    {
        Console.WriteLine($"{FlightNumber}: Laskeutumassa...");
    }

    public override void TakeOff()
    {
        Console.WriteLine($"{FlightNumber}: Nousemassa...");
    }

    public void RequestLanding() => _tower.RequestLanding(this);
    public void RequestTakeoff() => _tower.RequestTakeoff(this);
}
```

**Milloin käyttää Mediator-mallia?**

| Käytä kun | Älä käytä kun |
|---|---|
| ✅ Monta komponenttia kommunikoi keskenään | ❌ Vain 2 komponenttia kommunikoi |
| ✅ Riippuvuudet muodostuvat monimutkaiseksi | ❌ Kommunikaatio on yksinkertaista |
| ✅ Haluat löysän kytkennän (loose coupling) | ❌ Mediator paisuisi liian isoksi (God Object) |
| ✅ Kommunikaatiologiikka muuttuu usein | ❌ Suorituskyky on kriittistä (ylimääräinen kerros) |

**Mediator .NET-maailmassa:**

.NET-ekosysteemissä Mediator-malli toteutetaan useimmiten **MediatR**-kirjastolla, joka on de facto standardi ASP.NET Core -sovelluksissa. MediatR laajentaa perusmallia mm. CQRS-, Notification- ja Pipeline Behavior -tuen avulla.

> Katso myös: [MediatR](../Patterns/MediatR.md) - MediatR-kirjaston käyttö, CQRS, Pipeline Behaviors

### MVC Pattern (Model-View-Controller)

Tämä on laajasti käytetty malli ohjelmiston suunnitteluun, jolla on käyttöliittymä. Se jakaa ohjelmalogiikan kolmeen toisiinsa yhteydessä olevaan elementtiin: malliin (data), näkymään (käyttöliittymä) ja ohjaimeen (syötteen käsittelyprosessit). Tätä mallia käytetään paljon web-sovellusten kehittämisessä.

```csharp
// Model
public class User
{
    public int Id { get; set; }
    public string Name { get; set; }
}

// View
public class UserView
{
    public void DisplayUser(User user)
    {
        Console.WriteLine($"User: {user.Name} (ID: {user.Id})");
    }
}

// Controller
public class UserController
{
    private User _model;
    private UserView _view;

    public UserController(User model, UserView view)
    {
        _model = model;
        _view = view;
    }

    public void UpdateView()
    {
        _view.DisplayUser(_model);
    }
}

// Käyttö
User model = new User { Id = 1, Name = "Matti" };
UserView view = new UserView();
UserController controller = new UserController(model, view);
controller.UpdateView();
```

## Yhteenveto

Muista, että suunnittelumallien tehokkaan käytön avain on ymmärtää ne hyvin ja tietää, milloin niitä tulee soveltaa. Jokaisella mallilla on tietty käyttötapaus (oikea työkalu oikeaan hommaan), ja väärän mallin soveltaminen voi itse asiassa johtaa suurempaan monimutkaisuuteen eikä vähempään.

## Hyödyllisiä linkkejä

- [Refactoring Guru - Design Patterns in C#](https://refactoring.guru/design-patterns/csharp)
- [Microsoftin dokumentaatio](https://learn.microsoft.com/en-us/dotnet/standard/modern-web-apps-azure-architecture/architectural-principles)

