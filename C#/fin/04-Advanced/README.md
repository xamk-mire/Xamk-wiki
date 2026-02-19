# C# Edistyneet Aiheet

Tervetuloa C#-ohjelmoinnin edistyneisiin aiheisiin! Tämä osio käsittelee kehittyneempiä käsitteitä ja tekniikoita.

## Sisältö

### Testaus
- [Yksikkötestaus ja TDD](UnitTesting/) - Yksikkötestaus ja Test-Driven Development
  - [Yksikkötestaus - Teoria](UnitTesting/Unit-Testing.md) - Testauksen käsitteet, xUnit, Mocking, AAA-malli
  - [Yksikkötestaus - Esimerkit](UnitTesting/Unit-Testing-Examples.md) - Kattavat koodiesimerkit
  - [TDD - Teoria](UnitTesting/TDD.md) - Test-Driven Development, Red-Green-Refactor
  - [TDD - Esimerkit](UnitTesting/TDD-Examples.md) - TDD askel-askeleelta

### Edistyneet käsitteet
- [Attribuutit - Teoria](Attributes.md) - Mitä attribuutit ovat, sisäänrakennetut attribuutit, omien luominen
- [Attribuutit - Esimerkit](Attributes-Examples.md) - Kattavat koodiesimerkit attribuuteista

### Suunnittelu
- [Suunnitteluperiaatteet](Design-Principles.md) - Puhdas koodi, DRY, KISS, YAGNI, guard clauses, koodihajut, tarkistuslista
- [SOLID-periaatteet](SOLID.md) - Kattava materiaali SOLID-periaatteista C#-esimerkeillä
- [Dependency Injection](Dependency-Injection.md) - DI ja DIP, testattavuus, löysä kytkentä
- [Suunnittelumallit](Design-Patterns.md) - Yleisimmät design patternit (Singleton, Factory, Builder, Observer, jne.)
- [MediatR](Patterns/MediatR.md) - Mediator-malli, CQRS, Pipeline Behaviors, Notifications

### Ohjelmistoarkkitehtuuri
- [Johdanto - Mikä on arkkitehtuuri?](Architecture/Johdanto.md) - **Aloita tästä!** Historia, perusteet ja käsitteet
- [Arkkitehtuuri - Yleiskatsaus](Architecture/README.md) - Vertailu ja oppimisjärjestys
- [Layered Architecture](Architecture/Layered-Architecture.md) - Kerrosarkkitehtuuri, yksinkertainen ja yleinen
- [Clean Architecture](Architecture/Clean-Architecture.md) - Domain-keskinen, riippuvuudet sisäänpäin
- [Hexagonal Architecture](Architecture/Hexagonal-Architecture.md) - Portit ja adapterit -malli
- [CQRS](Architecture/CQRS.md) - Command Query Responsibility Segregation, luku- ja kirjoitusoperaatioiden erottaminen

### Docker
- [Docker C#/.NET-kehityksessä](Docker/) - Docker .NET-sovellusten kehityksessä ja käyttöönotossa
  - [.NET ja Docker](Docker/DotNet-Docker.md) - .NET-imaget, Dockerfile, multi-stage build, debuggaus
  - [Docker Compose .NET-projekteissa](Docker/DotNet-Docker-Compose.md) - ASP.NET Core + SQL Server/PostgreSQL, health checkit
- [Docker-perusteet (yleiset)](https://github.com/xamk-mire/Xamk-wiki/tree/main/Development-guidelines/Docker) - Dockerin yleiset perusteet, komennot, volumet ja verkot

### Salaisuuksien hallinta
- [Salaisuuksien hallinta .NET-sovelluksissa](Secrets-Management/) - Salaisuuksien turvallinen hallinta eri ympäristöissä
  - [User Secrets](Secrets-Management/User-Secrets.md) - Lokaalikehityksen salaisuudet (`dotnet user-secrets`)
  - [Azure Environment Variables](Secrets-Management/Azure-Environment-Variables.md) - Ympäristömuuttujat Azure App Servicessa
  - [Azure Key Vault](Secrets-Management/Azure-Key-Vault.md) - Key Vault, RBAC ja Managed Identity
- [Salaisuuksien hallinnan yleiset periaatteet](https://github.com/xamk-mire/Xamk-wiki/tree/main/Development-guidelines/Secrets-Management) - Miksi ja miten salaisuuksia hallitaan

### Autentikointi
- [Autentikointi ASP.NET Core -sovelluksissa](Authentication/) - JWT-autentikointi ja tokenien hallinta
  - [JWT (JSON Web Token)](Authentication/JWT.md) - JWT:n teoria, rakenne, claims ja ASP.NET Core -toteutus
  - [Refresh Tokens](Authentication/Refresh-Tokens.md) - Token Rotation, refresh-strategia ja toteutus

### Rinnakkaisuus ja asynkronisuus
- [Rinnakkaisuus ja asynkronisuus](Concurrency/) - Moniajo, asynkroninen ohjelmointi ja synkronointi
  - [Async/Await](Concurrency/Async-Await.md) - Asynkronisen ohjelmoinnin perusteet, Task, CancellationToken
  - [Synkronointi](Concurrency/Synchronization.md) - lock, SemaphoreSlim, Mutex, Interlocked, deadlock
  - [Concurrent Collections](Concurrency/Concurrent-Collections.md) - ConcurrentDictionary, Channel, BlockingCollection
  - [Parallel-ohjelmointi](Concurrency/Parallel-Programming.md) - Parallel.ForEach, PLINQ, rinnakkaistaminen

## Oppimisjärjestys

Suosittelemme opiskelua seuraavassa järjestyksessä:
1. **Suunnitteluperiaatteet** - Ymmärrä perusperiaatteet (SOLID, DRY, KISS, jne.)
2. **Yksikkötestaus ja TDD** - Opettele testaamaan koodia ja Test-Driven Development
   - Aloita yksikkötestauksesta
   - Jatka TDD:hen
3. **Attribuutit** - Opettele käyttämään ja luomaan attribuutteja
4. **Suunnittelumallit** - Opettele yleisimmät mallit ja niiden käyttökohteet
5. **Ohjelmistoarkkitehtuuri** - Ymmärrä eri arkkitehtuurimallit
   - Aloita Layered Architecture:sta
   - Jatka Clean Architecture:en
   - Syventyminen: Hexagonal Architecture
6. **MediatR** - Opi Mediator-malli ja CQRS
   - Aloita [Request/Handler-perusteista](Patterns/MediatR.md#request-ja-handler)
   - Jatka [CQRS-malliin](Patterns/MediatR.md#cqrs-mediatrllä)
   - Syventyminen: [Pipeline Behaviors](Patterns/MediatR.md#pipeline-behaviors)
7. **Docker** - Opettele kontittamaan .NET-sovelluksia
   - Aloita [Docker-perusteista](https://github.com/xamk-mire/Xamk-wiki/tree/main/Development-guidelines/Docker)
   - Jatka [.NET-kontitukseen](Docker/DotNet-Docker.md)
   - Syventyminen: [Docker Compose .NET-projekteissa](Docker/DotNet-Docker-Compose.md)
8. **Salaisuuksien hallinta** - Opi hallitsemaan salaisuuksia turvallisesti
   - Aloita [User Secrets:stä](Secrets-Management/User-Secrets.md) (lokaali kehitys)
   - Jatka [Azure Environment Variables](Secrets-Management/Azure-Environment-Variables.md) (Azure-ympäristö)
   - Syventyminen: [Azure Key Vault](Secrets-Management/Azure-Key-Vault.md) (tuotanto)
9. **Autentikointi** - Opi JWT-autentikointi ja tokenien hallinta
   - Aloita [JWT:stä](Authentication/JWT.md) (teoria ja perustoteutus)
   - Jatka [Refresh Tokens](Authentication/Refresh-Tokens.md) (turvallinen tokenien uusiminen)
10. **Rinnakkaisuus ja asynkronisuus** - Opi asynkroninen ohjelmointi ja moniajo
    - Aloita [Async/Await:sta](Concurrency/Async-Await.md) (asynkronisen ohjelmoinnin perusta)
    - Jatka [Synkronointiin](Concurrency/Synchronization.md) (lock, SemaphoreSlim, deadlock)
    - Jatka [Concurrent Collections](Concurrency/Concurrent-Collections.md) (ConcurrentDictionary, Channel)
    - Syventyminen: [Parallel-ohjelmointi](Concurrency/Parallel-Programming.md) (Parallel.ForEach, PLINQ)

## Seuraavaksi

Kun olet hallinnut edistyneet aiheet, voit syventää tietämystäsi:
- [OOP-konsepteista](https://github.com/xamk-mire/Xamk-wiki/tree/main/C%23/fin/02-OOP-Concepts) - Olio-ohjelmoinnin syvempi ymmärrys
- [Perusteista](https://github.com/xamk-mire/Xamk-wiki/tree/main/C%23/fin/00-Basics) - Palauttele peruskäsitteitä

