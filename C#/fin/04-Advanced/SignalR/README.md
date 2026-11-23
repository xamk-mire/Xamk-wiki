# SignalR — Reaaliaikainen viestintä

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Reaaliaikaisen viestinnän menetelmät](#reaaliaikaisen-viestinnän-menetelmät)
3. [WebSocket-protokolla](#websocket-protokolla)
4. [ASP.NET Core SignalR](#aspnet-core-signalr)
5. [Hub-luokat](#hub-luokat)
6. [Client-Server kommunikaatio](#client-server-kommunikaatio)
7. [SignalR Clean Architecturessa](#signalr-clean-architecturessa)
8. [Ryhmät (Groups)](#ryhmät-groups)
9. [Strongly Typed Hubs](#strongly-typed-hubs)
10. [Autentikointi ja auktorisointi](#autentikointi-ja-auktorisointi)
11. [Käyttöesimerkkejä](#käyttöesimerkkejä)
12. [Azure SignalR Service](#azure-signalr-service)
13. [Milloin SignalR:ää ei tarvita](#milloin-signalrää-ei-tarvita)
14. [Best Practices](#best-practices)
15. [Yhteenveto](#yhteenveto)

---

## Johdanto

**Reaaliaikainen viestintä** tarkoittaa, että palvelin voi lähettää dataa asiakkaalle heti kun sitä on saatavilla — ilman että asiakas pyytää sitä erikseen. Tämä on vastakohta perinteiselle HTTP request-response -mallille.

**Perusidea:**

```
Perinteinen HTTP (request-response):
Client → "Onko uusia viestejä?"  → Server
Client ← "Ei"                    ← Server
Client → "Entä nyt?"             → Server
Client ← "Ei"                    ← Server
Client → "Entäs nyt?"            → Server
Client ← "Kyllä! Tässä viesti."  ← Server

Reaaliaikainen (SignalR):
Client ←→ Pysyvä yhteys ←→ Server
                    ...odottaa...
Server → "Uusi viesti saapui!" → Client  (heti kun viesti tulee)
Server → "Toinen viesti!"     → Client  (heti kun seuraava tulee)
```

**SignalR** on ASP.NET Coren kirjasto, joka tekee reaaliaikaisesta viestinnästä helppoa. Se abstrahoi WebSocket-yhteyden ja tarjoaa korkean tason API:n palvelimen ja asiakkaan väliseen kaksisuuntaiseen kommunikaatioon.

---

## Reaaliaikaisen viestinnän menetelmät

### Polling

Asiakas kysyy palvelimelta tasaisin väliajoin:

```
Client → GET /messages (joka 5 sek)
Client ← 200 OK []
Client → GET /messages (joka 5 sek)
Client ← 200 OK []
Client → GET /messages (joka 5 sek)
Client ← 200 OK [{viesti}]
```

**Ongelma:** Turhia pyyntöjä, viive jopa 5 sekuntia, kuormittaa palvelinta.

### Long Polling

Asiakas lähettää pyynnön, ja palvelin pitää yhteyttä auki kunnes dataa on saatavilla:

```
Client → GET /messages (jää odottamaan)
         ... 30 sekuntia kuluu ...
Client ← 200 OK [{viesti}]
Client → GET /messages (uusi pyyntö heti)
```

**Parempi** kuin polling, mutta silti HTTP-overhead jokaiselle viestille.

### Server-Sent Events (SSE)

Yksisuuntainen yhteys palvelimelta asiakkaalle:

```
Client → GET /stream
Client ← event: message
         data: {"text": "Hei"}

Client ← event: message
         data: {"text": "Moi"}
```

**Rajoitus:** Vain palvelin → asiakas -suuntaan.

### WebSocket

Täysi kaksisuuntainen yhteys:

```
Client ←→ WebSocket-yhteys ←→ Server
Client → "Hei palvelin!"
Server → "Hei asiakas!"
Server → "Tässä päivitys!"
Client → "Kiitos!"
```

**Paras vaihtoehto** — matala latenssi, kaksisuuntainen, vähän overheadia.

### Vertailu

| Menetelmä | Suunta | Latenssi | Overhead | Yhteensopivuus |
|-----------|--------|---------|---------|---------------|
| **Polling** | Asiakas kysyy toistuvasti | Korkea (väli) | Korkea | Kaikki |
| **Long Polling** | Asiakas kysyy, palvelin pidättää vastausta kunnes dataa on | Keskiverto | Keskiverto | Kaikki |
| **SSE** | Palvelin → asiakas | Matala | Matala | Modernit selaimet |
| **WebSocket** | Molempiin suuntiin | Matala | Matala | Modernit selaimet |

**SignalR valitsee automaattisesti parhaan menetelmän** asiakkaan ja palvelimen tuekemista vaihtoehdoista: WebSocket → SSE → Long Polling.

---

## WebSocket-protokolla

WebSocket on TCP-pohjainen protokolla, joka mahdollistaa pysyvän kaksisuuntaisen yhteyden:

```
1. HTTP Upgrade -pyyntö:
   Client → GET /chat HTTP/1.1
            Upgrade: websocket
            Connection: Upgrade

2. Palvelin hyväksyy:
   Server ← HTTP/1.1 101 Switching Protocols
             Upgrade: websocket

3. Pysyvä yhteys avattu — molemmat voivat lähettää dataa milloin tahansa
   Client ←→ WebSocket ←→ Server
```

SignalR käyttää WebSocketia oletuksena, mutta **kehittäjän ei tarvitse käsitellä WebSocket-protokollaa suoraan** — SignalR abstrahoi kaiken.

---

## ASP.NET Core SignalR

### Asennus ja konfiguraatio

SignalR tulee ASP.NET Coren mukana — erillistä NuGet-pakettia ei tarvita palvelimelle.

```csharp
// Program.cs

// 1. Rekisteröi SignalR-palvelut
builder.Services.AddSignalR();

var app = builder.Build();

// 2. Mappaa Hub-endpoint
app.MapHub<ChatHub>("/chatHub");

app.Run();
```

### JavaScript-asiakas

```bash
npm install @microsoft/signalr
```

```javascript
import * as signalR from "@microsoft/signalr";

const connection = new signalR.HubConnectionBuilder()
    .withUrl("/chatHub")
    .withAutomaticReconnect()
    .build();

// Kuuntele palvelimen viestejä
connection.on("ReceiveMessage", (user, message) => {
    console.log(`${user}: ${message}`);
});

// Yhdistä
await connection.start();

// Lähetä viesti palvelimelle
await connection.invoke("SendMessage", "Matti", "Hei kaikille!");
```

### .NET-asiakas

```bash
dotnet add package Microsoft.AspNetCore.SignalR.Client
```

```csharp
var connection = new HubConnectionBuilder()
    .WithUrl("https://localhost:5001/chatHub")
    .WithAutomaticReconnect()
    .Build();

connection.On<string, string>("ReceiveMessage", (user, message) =>
{
    Console.WriteLine($"{user}: {message}");
});

await connection.StartAsync();
await connection.InvokeAsync("SendMessage", "Bot", "Hei!");
```

---

## Hub-luokat

**Hub** on palvelimen päätepiste, johon selaimet pitävät yhteyden auki. Se on SignalR:n keskeinen käsite: palvelinpuolen luokka, joka ottaa vastaan asiakkaiden kutsuja ja jonka kautta palvelin lähettää viestejä yhdistetyille asiakkaille.

### Perus-Hub

```csharp
public class ChatHub : Hub
{
    public async Task SendMessage(string user, string message)
    {
        // Lähetä kaikille yhdistetyille asiakkaille
        await Clients.All.SendAsync("ReceiveMessage", user, message);
    }

    public async Task SendPrivateMessage(string connectionId, string message)
    {
        // Lähetä yhdelle asiakkaalle
        await Clients.Client(connectionId).SendAsync("ReceiveMessage", "Private", message);
    }

    // Kutsutaan automaattisesti kun asiakas yhdistää
    public override async Task OnConnectedAsync()
    {
        await Clients.All.SendAsync("UserConnected", Context.ConnectionId);
        await base.OnConnectedAsync();
    }

    // Kutsutaan automaattisesti kun asiakas katkaistaan
    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        await Clients.All.SendAsync("UserDisconnected", Context.ConnectionId);
        await base.OnDisconnectedAsync(exception);
    }
}
```

### Clients-rajapinta

`Clients`-property tarjoaa useita tapoja kohdentaa viestejä:

| Metodi | Kohderyhmä |
|--------|-----------|
| `Clients.All` | Kaikki yhdistetyt asiakkaat |
| `Clients.Caller` | Kutsujan (tämän pyynnön lähettäjä) |
| `Clients.Others` | Kaikki paitsi kutsujan |
| `Clients.Client(connectionId)` | Tietty asiakas |
| `Clients.Group("groupName")` | Tietyn ryhmän jäsenet |
| `Clients.OthersInGroup("groupName")` | Ryhmän muut jäsenet paitsi kutsuja |

### Context

`Context`-property sisältää tietoja nykyisestä yhteydestä:

```csharp
public class ChatHub : Hub
{
    public async Task WhoAmI()
    {
        string connectionId = Context.ConnectionId;
        string? userId = Context.UserIdentifier;  // autentikoidulla käyttäjällä
        ClaimsPrincipal? user = Context.User;      // claims-tiedot

        await Clients.Caller.SendAsync("YourId", connectionId);
    }
}
```

---

## Client-Server kommunikaatio

### Palvelin → Asiakas

```csharp
// Hub-metodissa:

// Kaikille
await Clients.All.SendAsync("ReceiveNotification", "Palvelin päivitetty!");

// Kutsujalle
await Clients.Caller.SendAsync("PersonalMessage", "Tämä on vain sinulle");

// Muille
await Clients.Others.SendAsync("UserTyping", Context.ConnectionId);
```

### Asiakas → Palvelin

```javascript
// JavaScript-asiakas kutsuu Hub-metodia:

// invoke — odottaa vastausta
const result = await connection.invoke("GetOnlineUsers");

// send — ei odota vastausta (fire-and-forget)
connection.send("SendMessage", "Matti", "Hei!");
```

### Palvelin → Asiakas Hubin ulkopuolelta

Voit lähettää viestejä myös Controllereista tai palveluista `IHubContext`:n avulla:

```csharp
public class NotificationController : ControllerBase
{
    private readonly IHubContext<ChatHub> _hubContext;

    public NotificationController(IHubContext<ChatHub> hubContext)
    {
        _hubContext = hubContext;
    }

    [HttpPost("broadcast")]
    public async Task<IActionResult> Broadcast([FromBody] string message)
    {
        await _hubContext.Clients.All.SendAsync("ReceiveNotification", message);
        return Ok();
    }
}
```

```csharp
// Palvelussa:
public class OrderService
{
    private readonly IHubContext<NotificationHub> _hubContext;

    public OrderService(IHubContext<NotificationHub> hubContext)
    {
        _hubContext = hubContext;
    }

    public async Task CreateOrderAsync(Order order)
    {
        // ... tallenna tilaus ...

        // Ilmoita reaaliajassa
        await _hubContext.Clients.All.SendAsync("NewOrder", new
        {
            orderId = order.Id,
            customer = order.CustomerName,
            total = order.Total
        });
    }
}
```

> **Huom:** Tässä esimerkissä viestin mukana lähetetään dataa (asiakkaan nimi ja summa). Silloin selaimella on kaksi lähdettä samalle tiedolle: HTTP-rajapinta ja SignalR-viesti. Ne voivat poiketa toisistaan. Usein on turvallisempaa lähettää vain tunniste ja antaa selaimen hakea tuore data tavallisella kyselyllä. Lisäksi palvelu riippuu tässä suoraan SignalR:stä. Molemmat asiat käsitellään seuraavassa luvussa.

---

## SignalR Clean Architecturessa

Yllä olevissa esimerkeissä palvelu saa `IHubContext`in suoraan konstruktoriinsa. Kerrosarkkitehtuurissa se on ongelma: Application-kerroksen koodi riippuisi SignalR-kirjastosta, joka on ulkokehän tekniikkaa. Ratkaisu on sama kuin tietokannan kanssa.

| | Tietokanta | Reaaliaikainen ilmoitus |
|---|---|---|
| **Rajapinta (Application)** | `IMatchRepository` | `IStandingsNotifier` |
| **Toteutus (ulompi kerros)** | EF Core -repository (Infrastructure) | SignalR-toteutus, joka käyttää `IHubContext`ia (API) |

Handler tuntee vain rajapinnan. Se tietää, että "sarjataulukko muuttui" pitää ilmoittaa, mutta ei sitä, että ilmoitus kulkee SignalR:llä.

### Rajapinta ja toteutus

Esimerkki sarjataulukkosovelluksesta:

```csharp
// Application: rajapinta, ei viittausta SignalR:ään
public interface IStandingsNotifier
{
    Task StandingsChangedAsync(int leagueId, CancellationToken ct);
}
```

```csharp
// API: toteutus, ainoa luokka joka tuntee IHubContextin
public class SignalRStandingsNotifier : IStandingsNotifier
{
    private readonly IHubContext<LeagueHub> _hub;

    public SignalRStandingsNotifier(IHubContext<LeagueHub> hub)
    {
        _hub = hub;
    }

    public Task StandingsChangedAsync(int leagueId, CancellationToken ct)
    {
        // Viestissä kulkee vain tunniste, ei sarjataulukkoa
        return _hub.Clients.Group($"league-{leagueId}")
            .SendAsync("StandingsChanged", leagueId, ct);
    }
}

// Program.cs
builder.Services.AddScoped<IStandingsNotifier, SignalRStandingsNotifier>();
```

### Hubissa ei ole sääntöjä eikä kirjoituksia

Hub hoitaa vain yhteydet: kuka kuuntelee mitäkin ryhmää.

```csharp
public class LeagueHub : Hub
{
    public Task JoinLeague(int leagueId)
    {
        return Groups.AddToGroupAsync(Context.ConnectionId, $"league-{leagueId}");
    }
}
```

Tuloksen kirjaus **ei** kulje Hubin kautta. Kirjoitus tehdään tavallisella HTTP-pyynnöllä, joka päätyy commandiin ja handleriin. Jos saman kirjoituksen voisi tehdä myös Hubin metodilla, kirjoituksille olisi kaksi sisäänkäyntiä. Silloin validointi, oikeustarkistus ja lokitus pitäisi muistaa tehdä molemmissa.

### Ilmoita vasta tallennuksen jälkeen

```csharp
// Command-handlerissa
match.RecordResult(request.HomeGoals, request.AwayGoals);

await _matches.SaveAsync(match, ct);                          // 1. tallenna
await _notifier.StandingsChangedAsync(match.LeagueId, ct);    // 2. ilmoita
```

Jos ilmoitus lähtee ennen tallennusta, selaimet hakevat datan liian aikaisin ja saavat vanhan tilan. Jos tallennus epäonnistuu, ilmoitusta ei saa lähteä lainkaan. Kun välissä on välimuisti, järjestys on: tallenna, tyhjennä välimuisti, ilmoita. Katso [Caching: Järjestys](../Patterns/Caching.md#järjestys-tallenna-tyhjennä-ilmoita).

### Viesti on heräte, ei data

Viesti kertoo vain, **että** jokin muuttui ja mitä se koskee (tunniste). Selain hakee tuoreen datan samalla kyselyllä kuin sivun latauksessa.

```javascript
connection.on("StandingsChanged", () => {
    reloadStandings();   // tavallinen GET /api/standings
});
```

Näin datalla on yksi lähde. Jos viestissä kulkisi koko sarjataulukko, selaimella olisi toinen totuus, joka voi poiketa rajapinnan vastauksesta. Jos yhteys katkeaa hetkeksi, seuraava haku korjaa näkymän joka tapauksessa.

Sama asia selaimen puolelta: [Frontend-arkkitehtuuri: Reaaliaikaisuus](../Architecture/Frontend-Architecture.md#reaaliaikaisuus).

**Milloin rajapintaa ei tarvita?** Pienessä sovelluksessa, jossa ei ole erillisiä kerroksia, `IHubContext`in voi injektoida suoraan. Rajapinta kannattaa, kun Application-kerros halutaan pitää riippumattomana ulkokehän kirjastoista ja handleri halutaan testata ilman SignalR:ää.

---

## Ryhmät (Groups)

Ryhmät mahdollistavat viestien kohdentamisen tietyille asiakkaille. Asiakas voi kuulua useisiin ryhmiin samanaikaisesti.

### Ryhmiin liittyminen ja poistuminen

```csharp
public class ChatHub : Hub
{
    public async Task JoinRoom(string roomName)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, roomName);
        await Clients.Group(roomName).SendAsync(
            "SystemMessage", $"{Context.ConnectionId} liittyi huoneeseen {roomName}");
    }

    public async Task LeaveRoom(string roomName)
    {
        await Groups.RemoveFromGroupAsync(Context.ConnectionId, roomName);
        await Clients.Group(roomName).SendAsync(
            "SystemMessage", $"{Context.ConnectionId} poistui huoneesta {roomName}");
    }

    public async Task SendToRoom(string roomName, string user, string message)
    {
        await Clients.Group(roomName).SendAsync("ReceiveMessage", user, message);
    }
}
```

### Käyttöesimerkki: Hotellivarausjärjestelmä

```csharp
public class BookingHub : Hub
{
    // Hotellin henkilökunta liittyy oman hotellinen ryhmään
    public async Task JoinHotelGroup(int hotelId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, $"hotel-{hotelId}");
    }

    // Kun uusi varaus tehdään, ilmoitetaan hotellin henkilökunnalle
    public async Task NotifyNewBooking(int hotelId, BookingDto booking)
    {
        await Clients.Group($"hotel-{hotelId}")
            .SendAsync("NewBooking", booking);
    }
}
```

> **Huom:** Esimerkki näyttää ryhmän käytön. Siinä asiakas pyytää ilmoituksen lähettämistä ja viestissä kulkee koko varaus. Kerrosarkkitehtuurissa ilmoituksen lähettää palvelin itse tallennuksen jälkeen, ja viestissä kulkee vain tunniste. Katso [SignalR Clean Architecturessa](#signalr-clean-architecturessa).

---

## Strongly Typed Hubs

Strongly Typed Hub käyttää rajapintaa viestien lähettämiseen — kirjoitusvirheet havaitaan käännösaikaisesti:

### Rajapinta

```csharp
public interface IChatClient
{
    Task ReceiveMessage(string user, string message);
    Task UserConnected(string connectionId);
    Task UserDisconnected(string connectionId);
    Task SystemMessage(string message);
}
```

### Strongly Typed Hub

```csharp
public class ChatHub : Hub<IChatClient>
{
    public async Task SendMessage(string user, string message)
    {
        // Käännösaikainen tyyppitarkistus — ei enää "magic string" -ongelmaa
        await Clients.All.ReceiveMessage(user, message);
    }

    public override async Task OnConnectedAsync()
    {
        await Clients.All.UserConnected(Context.ConnectionId);
        await base.OnConnectedAsync();
    }
}
```

**Edut:**
- ✅ Käännösaikainen tyyppitarkistus
- ✅ IntelliSense IDE:ssä
- ✅ Ei kirjoitusvirheriskiä `SendAsync("ReceiveMessage", ...)` -kutsuissa
- ✅ Refaktorointi toimii

---

## Autentikointi ja auktorisointi

### Hub-tason autentikointi

```csharp
[Authorize]
public class SecureChatHub : Hub
{
    public async Task SendMessage(string message)
    {
        string userName = Context.User?.Identity?.Name ?? "Anonymous";
        await Clients.All.SendAsync("ReceiveMessage", userName, message);
    }
}
```

### Metodi-tason autentikointi

```csharp
public class AdminHub : Hub
{
    // Kaikki voivat lukea
    public async Task GetPublicData()
    {
        await Clients.Caller.SendAsync("PublicData", "Tämä on julkista");
    }

    // Vain admin-roolilla
    [Authorize(Roles = "Admin")]
    public async Task GetAdminData()
    {
        await Clients.Caller.SendAsync("AdminData", "Salaista dataa");
    }
}
```

### JWT-token SignalR:ssä

SignalR ei voi lähettää JWT:tä HTTP-headerissa WebSocket-yhteyden aikana. Token lähetetään query stringissä:

```javascript
// Asiakas
const connection = new signalR.HubConnectionBuilder()
    .withUrl("/chatHub", {
        accessTokenFactory: () => localStorage.getItem("token")
    })
    .build();
```

```csharp
// Palvelin — lue token query stringistä
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Events = new JwtBearerEvents
        {
            OnMessageReceived = context =>
            {
                var accessToken = context.Request.Query["access_token"];
                var path = context.HttpContext.Request.Path;

                if (!string.IsNullOrEmpty(accessToken) &&
                    path.StartsWithSegments("/chatHub"))
                {
                    context.Token = accessToken;
                }
                return Task.CompletedTask;
            }
        };
    });
```

---

## Käyttöesimerkkejä

### 1. Chat-sovellus

```csharp
public class ChatHub : Hub<IChatClient>
{
    public async Task SendToRoom(string room, string user, string message)
    {
        await Clients.Group(room).ReceiveMessage(user, message);
    }

    public async Task JoinRoom(string room)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, room);
        await Clients.Group(room).SystemMessage(
            $"{Context.User?.Identity?.Name} liittyi");
    }
}
```

### 2. Live-notifikaatiot

```csharp
public class NotificationHub : Hub
{
    public override async Task OnConnectedAsync()
    {
        string? userId = Context.UserIdentifier;
        if (userId != null)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, $"user-{userId}");
        }
    }
}

// Palvelussa:
public class OrderService
{
    private readonly IHubContext<NotificationHub> _hub;

    public async Task CompleteOrderAsync(Order order)
    {
        // ... logiikka ...
        await _hub.Clients.Group($"user-{order.CustomerId}")
            .SendAsync("OrderCompleted", order.Id);
    }
}
```

Viestissä kulkee vain tilauksen tunniste, mikä on hyvä. Palvelu riippuu kuitenkin suoraan `IHubContext`ista. Kerrosarkkitehtuurissa väliin tehdään rajapinta: katso [SignalR Clean Architecturessa](#signalr-clean-architecturessa).

### 3. Live-dashboard (reaaliaikainen data)

```csharp
public class DashboardHub : Hub
{
    public async Task SubscribeToDashboard(string dashboardId)
    {
        await Groups.AddToGroupAsync(Context.ConnectionId, $"dashboard-{dashboardId}");
    }
}

// Taustapalvelu päivittää dashboardia
public class DashboardUpdater : BackgroundService
{
    private readonly IHubContext<DashboardHub> _hub;

    protected override async Task ExecuteAsync(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested)
        {
            var stats = await GetLatestStatsAsync();
            await _hub.Clients.Group("dashboard-main")
                .SendAsync("StatsUpdated", stats, ct);

            await Task.Delay(TimeSpan.FromSeconds(5), ct);
        }
    }
}
```

---

## Azure SignalR Service

Kun sovellus skaalautuu useisiin instansseihin, SignalR-yhteyksien hallinta muuttuu haastavaksi. **Azure SignalR Service** ratkaisee tämän:

```
Ilman Azure SignalR Service:
┌──────────┐     ┌──────────┐
│ Server 1 │     │ Server 2 │
│ 500 yht. │     │ 500 yht. │
└──────────┘     └──────────┘
   ↑ Viesti lähetetään vain Server 1:n asiakkaille!

Azure SignalR Servicen kanssa:
┌──────────┐     ┌──────────┐
│ Server 1 │     │ Server 2 │
└─────┬────┘     └─────┬────┘
      │                │
      ▼                ▼
┌──────────────────────────┐
│  Azure SignalR Service   │
│  (hallinnoi yhteydet)    │
│  1000 yhteyttä           │
└──────────────────────────┘
   ↑ Viesti tavoittaa KAIKKI asiakkaat
```

### Konfigurointi

```bash
dotnet add package Microsoft.Azure.SignalR
```

```csharp
// Program.cs
builder.Services.AddSignalR()
    .AddAzureSignalR(options =>
    {
        options.ConnectionString =
            builder.Configuration["Azure:SignalR:ConnectionString"];
    });
```

### Hyödyt

- ✅ Automaattinen skaalaus tuhansiin yhtäaikaisiin yhteyksiin
- ✅ Ei tarvitse hallita WebSocket-yhteyksiä itse
- ✅ Toimii useiden sovellusinstanssien kanssa
- ✅ Sisäänrakennettu korkea saatavuus

---

## Milloin SignalR:ää ei tarvita

SignalR ratkaisee yhden ongelman: käyttäjän pitää nähdä **toisen** tekemä muutos heti, ilman sivun päivitystä. Jos tätä tarvetta ei ole, SignalR lisää vain ylläpidettävää: pysyvät yhteydet, uudelleenyhdistämisen ja skaalauksen.

Et tarvitse SignalR:ää, kun:

- **Käyttäjä näkee vain omat muutoksensa.** Kun hän tallentaa, selain hakee datan uudestaan. Kukaan muu ei odota päivitystä.
- **Muutaman sekunnin viive riittää.** Silloin polling on tarpeeksi: selain kysyy rajapinnasta esimerkiksi 10 sekunnin välein. Se on yksinkertaisempi rakentaa ja testata.
- **Data muuttuu harvoin.** Jos sarjataulukko muuttuu kerran päivässä, pysyvä yhteys jokaiselle selaimelle on turha.

SignalR kannattaa, kun usea käyttäjä katsoo samaa dataa samaan aikaan ja muutoksen pitää näkyä kaikille heti: live-tulokset, chat, yhteinen työtila.

---

## Best Practices

### 1. Käytä Strongly Typed Hubeja

```csharp
// ✅ Käännösaikainen tarkistus
public class ChatHub : Hub<IChatClient> { }

// ❌ Magic stringit — virheet vasta ajon aikana
await Clients.All.SendAsync("RecieveMessage", ...);  // kirjoitusvirhe!
```

### 2. Käsittele yhteyden katkeaminen

```csharp
public override async Task OnDisconnectedAsync(Exception? exception)
{
    // Siivoa käyttäjän tiedot
    await _userTracker.RemoveUserAsync(Context.ConnectionId);
    await base.OnDisconnectedAsync(exception);
}
```

### 3. Käytä ryhmiä viestien kohdentamiseen

```csharp
// ✅ Ryhmäpohjainen — skaalautuu
await Clients.Group("hotel-1").SendAsync("Update", data);

// ❌ Kaikille — turhaa dataa useimmille
await Clients.All.SendAsync("Update", data);
```

### 4. Pidä Hub-metodit kevyinä

```csharp
// ✅ Hub hoitaa vain yhteydet: ei liiketoimintalogiikkaa, ei kirjoituksia
public class BookingHub : Hub
{
    public Task JoinHotelGroup(int hotelId)
    {
        return Groups.AddToGroupAsync(Context.ConnectionId, $"hotel-{hotelId}");
    }
}

// ❌ Kirjoitus ja logiikka Hubissa
public async Task CreateBooking(CreateBookingDto dto)
{
    var room = await _db.Rooms.FindAsync(dto.RoomId);
    // ... 50 riviä validointia ja logiikkaa ...
}
```

Varaus luodaan HTTP-pyynnöllä (`POST /api/bookings`), joka kulkee saman validoinnin ja saman handlerin läpi kuin muutkin kirjoitukset. Tallennuksen jälkeen palvelin ilmoittaa ryhmälle. Jos varauksen voisi luoda myös Hubin kautta, kirjoituksille olisi kaksi sisäänkäyntiä. Katso [SignalR Clean Architecturessa](#signalr-clean-architecturessa).

### 5. Käytä CancellationTokenia

```csharp
public async Task<List<Message>> GetHistory(
    string room,
    CancellationToken cancellationToken)
{
    return await _messageService.GetRoomHistoryAsync(room, cancellationToken);
}
```

---

## Yhteenveto

| Käsite | Selitys |
|--------|---------|
| **Reaaliaikainen viestintä** | Palvelin lähettää dataa asiakkaalle ilman erillistä pyyntöä |
| **WebSocket** | Kaksisuuntainen pysyvä yhteys — SignalR:n ensisijainen kuljetustapa |
| **SignalR** | ASP.NET Core -kirjasto joka abstrahoi reaaliaikaisen viestinnän |
| **Hub** | Palvelimen päätepiste, johon selaimet pitävät yhteyden auki |
| **Notifier-rajapinta** | Application-kerroksen rajapinta ilmoitukselle; SignalR-toteutus on API-kerroksessa |
| **Heräte** | Viesti, jossa kulkee vain tunniste; selain hakee datan tavallisella kyselyllä |
| **Clients** | API viestien lähettämiseen (All, Caller, Others, Group, Client) |
| **Groups** | Mekanismi viestien kohdentamiseen tietyille asiakkaille |
| **IHubContext** | Viestien lähettäminen Hubin ulkopuolelta (Controller, Service) |
| **Strongly Typed Hub** | Rajapintapohjainen Hub — käännösaikainen tyyppitarkistus |
| **Azure SignalR Service** | Hallittu palvelu yhteyksien skaalaamiseen |

**Muista:**
- SignalR **valitsee automaattisesti** parhaan kuljetustavan (WebSocket → SSE → Long Polling)
- Käytä **Strongly Typed Hubeja** välttääksesi magic string -ongelmia
- Käytä **ryhmiä** viestien kohdentamiseen — älä lähetä kaikille
- **IHubContext** mahdollistaa viestien lähettämisen Hubin ulkopuolelta (Controller, BackgroundService); kerrosarkkitehtuurissa se piilotetaan rajapinnan taakse
- **Kirjoitukset kulkevat HTTP:n kautta**, eivät Hubin; Hubissa ei ole liiketoimintasääntöjä
- **Ilmoita vasta tallennuksen jälkeen** ja lähetä vain tunniste
- **Azure SignalR Service** tarvitaan kun skaalataan useisiin instansseihin

---

## Hyödyllisiä linkkejä

- [Microsoft: Introduction to SignalR](https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction)
- [Microsoft: SignalR Hubs](https://learn.microsoft.com/en-us/aspnet/core/signalr/hubs)
- [Microsoft: SignalR JavaScript Client](https://learn.microsoft.com/en-us/aspnet/core/signalr/javascript-client)
- [Microsoft: SignalR .NET Client](https://learn.microsoft.com/en-us/aspnet/core/signalr/dotnet-client)
- [Microsoft: Azure SignalR Service](https://learn.microsoft.com/en-us/azure/azure-signalr/signalr-overview)
- [Microsoft: SignalR Authentication](https://learn.microsoft.com/en-us/aspnet/core/signalr/authn-and-authz)
