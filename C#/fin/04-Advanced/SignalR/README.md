# SignalR — Reaaliaikainen viestintä

## Sisällysluettelo

1. [Johdanto](#johdanto)
2. [Reaaliaikaisen viestinnän menetelmät](#reaaliaikaisen-viestinnän-menetelmät)
3. [WebSocket-protokolla](#websocket-protokolla)
4. [ASP.NET Core SignalR](#aspnet-core-signalr)
5. [Hub-luokat](#hub-luokat)
6. [Client-Server kommunikaatio](#client-server-kommunikaatio)
7. [Ryhmät (Groups)](#ryhmät-groups)
8. [Strongly Typed Hubs](#strongly-typed-hubs)
9. [Autentikointi ja auktorisointi](#autentikointi-ja-auktorisointi)
10. [Käyttöesimerkkejä](#käyttöesimerkkejä)
11. [Azure SignalR Service](#azure-signalr-service)
12. [Best Practices](#best-practices)
13. [Yhteenveto](#yhteenveto)

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
| **Polling** | Client → Server | Korkea (väli) | Korkea | Kaikki |
| **Long Polling** | Server → Client | Keskiverto | Keskiverto | Kaikki |
| **SSE** | Server → Client | Matala | Matala | Modernit selaimet |
| **WebSocket** | Kaksisuuntainen | Matala | Matala | Modernit selaimet |

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

**Hub** on SignalR:n keskeinen konsepti. Se on palvelinpuolen luokka, joka käsittelee asiakkaiden kutsuja ja lähettää viestejä takaisin.

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
// ✅ Delegoi logiikka palvelulle
public async Task CreateBooking(CreateBookingDto dto)
{
    var result = await _bookingService.CreateAsync(dto);
    await Clients.Group($"hotel-{dto.HotelId}").SendAsync("BookingCreated", result);
}

// ❌ Raskas logiikka suoraan Hubissa
public async Task CreateBooking(CreateBookingDto dto)
{
    var room = await _db.Rooms.FindAsync(dto.RoomId);
    // ... 50 riviä validointia ja logiikkaa ...
}
```

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
| **Hub** | Palvelinpuolen luokka joka käsittelee viestejä |
| **Clients** | API viestien lähettämiseen (All, Caller, Others, Group, Client) |
| **Groups** | Mekanismi viestien kohdentamiseen tietyille asiakkaille |
| **IHubContext** | Viestien lähettäminen Hubin ulkopuolelta (Controller, Service) |
| **Strongly Typed Hub** | Rajapintapohjainen Hub — käännösaikainen tyyppitarkistus |
| **Azure SignalR Service** | Hallittu palvelu yhteyksien skaalaamiseen |

**Muista:**
- SignalR **valitsee automaattisesti** parhaan kuljetustavan (WebSocket → SSE → Long Polling)
- Käytä **Strongly Typed Hubeja** välttääksesi magic string -ongelmia
- Käytä **ryhmiä** viestien kohdentamiseen — älä lähetä kaikille
- **IHubContext** mahdollistaa viestien lähettämisen mistä tahansa (Controller, BackgroundService)
- **Azure SignalR Service** tarvitaan kun skaalataan useisiin instansseihin

---

## Hyödyllisiä linkkejä

- [Microsoft: Introduction to SignalR](https://learn.microsoft.com/en-us/aspnet/core/signalr/introduction)
- [Microsoft: SignalR Hubs](https://learn.microsoft.com/en-us/aspnet/core/signalr/hubs)
- [Microsoft: SignalR JavaScript Client](https://learn.microsoft.com/en-us/aspnet/core/signalr/javascript-client)
- [Microsoft: SignalR .NET Client](https://learn.microsoft.com/en-us/aspnet/core/signalr/dotnet-client)
- [Microsoft: Azure SignalR Service](https://learn.microsoft.com/en-us/azure/azure-signalr/signalr-overview)
- [Microsoft: SignalR Authentication](https://learn.microsoft.com/en-us/aspnet/core/signalr/authn-and-authz)
