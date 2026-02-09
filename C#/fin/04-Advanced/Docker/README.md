# Docker C#/.NET-kehityksessä

Tervetuloa Docker-oppimateriaaliin C#/.NET-kehittäjille! Tämä osio käsittelee Dockerin käyttöä .NET-sovellusten kehityksessä ja käyttöönotossa.

> **Edellytykset:** Tutustu ensin [Docker-perusteisiin](https://github.com/xamk-mire/Xamk-wiki/tree/main/Development-guidelines/Docker) ennen tätä materiaalia.

## Sisältö

### .NET-sovelluksen kontitus
- [.NET ja Docker](DotNet-Docker.md) - .NET-imaget, Dockerfile konsolisovellukselle ja Web API:lle, multi-stage build, debuggaus

### Docker Compose .NET-projekteissa
- [Docker Compose .NET-projekteissa](DotNet-Docker-Compose.md) - ASP.NET Core + SQL Server/PostgreSQL, connection stringit, health checkit, hot reload

## Oppimisjärjestys

1. **Docker-perusteet** - [Yleiset Docker-materiaalit](https://github.com/xamk-mire/Xamk-wiki/tree/main/Development-guidelines/Docker)
2. **.NET ja Docker** - [.NET-sovelluksen kontitus](DotNet-Docker.md)
3. **Docker Compose** - [Docker Compose .NET-projekteissa](DotNet-Docker-Compose.md)

## Hyödyllisiä linkkejä

- [Microsoft: .NET Docker images](https://hub.docker.com/_/microsoft-dotnet)
- [Microsoft: Containerize a .NET app](https://learn.microsoft.com/en-us/dotnet/core/docker/build-container)
- [Microsoft: ASP.NET Core Docker samples](https://github.com/dotnet/dotnet-docker/tree/main/samples)
