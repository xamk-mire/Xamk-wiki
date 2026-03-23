# Web API -kehitys ASP.NET Corella

Tervetuloa Web API -kehityksen materiaaleihin! Tämä osio käsittelee backendin ja REST API:n perusteita sekä ASP.NET Core -sovelluskehitystä.

---

## Sisältö

### Teoria — Perusteet
- [Backend ja API](Backend-and-API.md) - Mikä on backend, API, REST, HTTP-metodit ja statuskoodit
- [HTTP-metodit ja statuskoodit — Referenssi](HTTP-Reference.md) - Kattava hakuteos kaikista HTTP-metodeista ja statuskoodeista esimerkkeineen
- [Controllers](Controllers.md) - ASP.NET Core -kontrollerit, reititys, attribuutit ja toimintametodit

### Teoria — Jatkokurssi
- [Entity Framework Core](Entity-Framework.md) - ORM, DbContext, DbSet, migraatiot ja async-metodit
- [Service-kerros ja Dependency Injection](Services-and-DI.md) - Miksi service, interface vs toteutus, DI:n elinkaaret
- [Health Checks](Health-Checks.md) - Sovelluksen terveystarkistukset tuotannossa (ASP.NET Core Health Checks middleware)

### Harjoitukset
- [Vaihe 1: Backend Basics](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Backend%20basics) - Ensimmäinen Web API controllereilla ja staattisella listalla
- [Vaihe 2: Tietokanta](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Database) - EF Core ja SQLite
- [Vaihe 3: Service-kerros](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Services) - Logiikka service-luokkaan
- [Vaihe 4: Autentikointi](https://github.com/xamk-mire/Xamk-wiki/tree/main/Assigments/Backend/Authentication) - JWT ja käyttäjähallinto

---

## Oppimisjärjestys

1. **Backend ja API** - Ymmärrä mitä backend tarkoittaa, mikä on API ja miten REST toimii
2. **Controllers** - Opi miten ASP.NET Core käsittelee HTTP-pyyntöjä kontrollerien avulla
3. **Vaihe 1: Backend Basics** - Rakenna ensimmäinen Web API käytännössä
4. **Entity Framework Core** - Korvaa staattinen lista oikealla tietokannalla
5. **Vaihe 2: Tietokanta** - Käytä EF Corea harjoituksessa
6. **Service-kerros ja DI** - Opi erottamaan logiikka controllerista
7. **Vaihe 3: Service-kerros** - Refaktoroi rakenne paremmaksi
8. **JWT** (Authentication-kansio) - Opi tokenipohjainen autentikointi
9. **Vaihe 4: Autentikointi** - Lisää kirjautuminen ja suojatut endpointit

---

## Ulkoiset linkit

- [Microsoft: ASP.NET Core Web API](https://learn.microsoft.com/en-us/aspnet/core/web-api/)
- [Microsoft: Controller-based API](https://learn.microsoft.com/en-us/aspnet/core/web-api/?view=aspnetcore-8.0#controllerbase-class)
- [RESTful API Design](https://restfulapi.net/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
