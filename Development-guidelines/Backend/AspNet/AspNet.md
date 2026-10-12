# ASP.NET Core -backend (ASP.NET Core)

ASP.NET Core on Microsoftin avoimen lähdekoodin sovelluskehys web-sovelluksille ja REST API -rajapinnoille. Tällä sivulla on ohjeet ja suositellut käytännöt ASP.NET Core -backendin kehittämiseen. Teoria löytyy C#-materiaaleista, ja tämä sivu kokoaa sen yhteen järjestykseen.

**Microsoft:** [ASP.NET Core -dokumentaatio](https://learn.microsoft.com/en-us/aspnet/core/)

## Sisällysluettelo

1. [Uuden projektin luonti](#1-uuden-projektin-luonti)
2. [Suositeltu projektirakenne](#2-suositeltu-projektirakenne)
3. [Käytännöt](#3-käytännöt)
4. [Materiaalit aiheittain](#4-materiaalit-aiheittain)

---

## 1. Uuden projektin luonti

```bash
dotnet new webapi -n MyApi --use-controllers
cd MyApi
dotnet run
```

- `--use-controllers` luo controller-pohjaisen API:n. Ilman sitä syntyy Minimal API -projekti.
- Käytä kurssin ilmoittamaa .NET-versiota (tarkista: `dotnet --version`).
- Swagger/OpenAPI-näkymä on kehitysympäristössä käytettävissä projektipohjan mukaisesti. Testaa endpointit sillä tai `.http`-tiedostolla.

---

## 2. Suositeltu projektirakenne

Pieni API voi aloittaa yhdellä projektilla:

```
MyApi/
├─ Controllers/     HTTP-pyynnöt sisään, vastaukset ulos — ei liiketoimintalogiikkaa
├─ Services/        liiketoimintalogiikka (interface + toteutus)
├─ Data/            DbContext, migraatiot
├─ Models/          entiteetit
├─ DTOs/            pyyntö- ja vastausmallit
└─ Program.cs       palveluiden rekisteröinti (DI) ja middleware-putki
```

Kun sovellus kasvaa, jaa se kerroksiin tai Clean Architecture -projekteihin. Katso [Arkkitehtuuri](../../../C%23/fin/04-Advanced/Architecture/README.md).

---

## 3. Käytännöt

| Käytäntö | Miksi |
|---|---|
| Ohut controller, logiikka serviceen | Testattava ja uudelleenkäytettävä logiikka |
| Rekisteröi palvelut DI:hin (`AddScoped`, `AddSingleton`…) | Ei `new`-kutsuja controllereissa, helppo vaihtaa toteutusta |
| Palauta DTO, älä entiteettiä | API-sopimus ei muutu tietokannan mukana, ei vuoda kenttiä |
| Oikeat statuskoodit (`200`, `201`, `400`, `404`…) | Asiakas tietää mitä tapahtui |
| `async`/`await` tietokanta- ja I/O-kutsuissa | Säikeet eivät jää odottamaan |
| Salaisuudet pois koodista (User Secrets, Key Vault) | Ei salasanoja GitHubiin |
| Validointi syötteelle | Virheellinen data pysähtyy rajapintaan |
| Yksikkö- ja integraatiotestit | Muutokset eivät riko vanhaa toimintaa |

---

## 4. Materiaalit aiheittain

**Perusteet**
- [Web API -kehitys (osion etusivu)](../../../C%23/fin/04-Advanced/WebAPI/README.md)
- [Backend ja API](../../../C%23/fin/04-Advanced/WebAPI/Backend-and-API.md) · [HTTP-referenssi](../../../C%23/fin/04-Advanced/WebAPI/HTTP-Reference.md) · [Controllers](../../../C%23/fin/04-Advanced/WebAPI/Controllers.md)

**Data ja logiikka**
- [Entity Framework Core](../../../C%23/fin/04-Advanced/WebAPI/Entity-Framework.md) · [Service-kerros ja DI](../../../C%23/fin/04-Advanced/WebAPI/Services-and-DI.md) · [DTO:t ja mappaus](../../../C%23/fin/04-Advanced/WebAPI/DTOs-and-Mapping.md)
- [Repository](../../../C%23/fin/04-Advanced/Patterns/Repository-Pattern.md) · [Result](../../../C%23/fin/04-Advanced/Patterns/Result-Pattern.md) · [Sivutus](../../../C%23/fin/04-Advanced/Patterns/Pagination.md) · [Välimuisti](../../../C%23/fin/04-Advanced/Patterns/Caching.md)

**Tietoturva ja konfiguraatio**
- [Autentikointi (JWT)](../../../C%23/fin/04-Advanced/Authentication/README.md)
- [Salaisuuksien hallinta](../../../C%23/fin/04-Advanced/Secrets-Management/README.md)

**Laatu ja julkaisu**
- [Yksikkötestaus .NETissä](UnitTests.md)
- [Health Checks](../../../C%23/fin/04-Advanced/WebAPI/Health-Checks.md)
- [.NET ja Docker](../../../C%23/fin/04-Advanced/Docker/README.md) · [CI/CD](../../CI-CD.md)
- [Azure App Service](../../../Cloud%20technologies/Azure/App-Service.md)

**Reaaliaikaisuus**
- [SignalR](../../../C%23/fin/04-Advanced/SignalR/README.md)

---

## Hyödyllisiä linkkejä

- [ASP.NET Core -dokumentaatio](https://learn.microsoft.com/en-us/aspnet/core/)
- [Tutorial: Create a controller-based web API](https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api)
