# Patterns — Suunnittelumallit käytännössä

Tämä osio käsittelee yleisimpiä suunnittelumalleja ja -käytäntöjä, joita käytetään moderneissa .NET-sovelluksissa.

---

## Sisältö

### Arkkitehtuuripatternit

- **[Repository Pattern](Repository-Pattern.md)** — Tietokantakäsittelyn abstrahointi rajapinnan taakse
  - IRepository-rajapinta ja toteutus
  - Generic vs. spesifi repository
  - Repository Clean Architecturessa (DIP)
  - Unit of Work

- **[MediatR](MediatR.md)** — Mediator-malli ja viestipohjainen arkkitehtuuri
  - Request/Handler -malli
  - CQRS MediatR:llä (Commands ja Queries)
  - Pipeline Behaviors (logging, validointi)
  - FluentValidation-integraatio
  - Notifications

### Datankäsittelypatternit

- **[Result Pattern](Result-Pattern.md)** — Funktionaalinen virheenkäsittely
  - Result vs. Exceptions
  - Railway Oriented Programming
  - Result<T> toteutus C#:ssa

- **[Pagination](Pagination.md)** — Paginointi suurille tietojoukoille
  - Offset-based pagination (Skip/Take)
  - Cursor-based pagination
  - PagedResult<T> pattern

### Suorituskykypatternit

- **[Caching](Caching.md)** — Välimuistitus suorituskyvyn parantamiseksi
  - IMemoryCache (In-Memory)
  - Distributed Caching (Redis)
  - Cache Invalidation
  - Caching-strategiat

- **[Decorator Pattern](Decorator-Pattern.md)** — Toiminnallisuuden lisääminen ilman alkuperäisen koodin muuttamista
  - Decorator vs. Inheritance
  - Käytännön esimerkit (Caching, Logging, Retry)
  - Open/Closed Principle

---

## Oppimisjärjestys

1. **Repository Pattern** — Ymmärrä tietokantakäsittelyn abstrahointi
2. **Result Pattern** — Opi funktionaalinen virheenkäsittely
3. **Pagination** — Opi käsittelemään suuria tietojoukkoja
4. **Decorator Pattern** — Ymmärrä miten toiminnallisuutta lisätään dekoraattoreilla
5. **Caching** — Opi välimuistitus ja Decorator Patternin käytännön sovellus
6. **MediatR** — Yhdistä kaikki: CQRS, Pipeline Behaviors, Clean Architecture

---

## Katso myös

- [Suunnitteluperiaatteet](../Design-Principles.md) — SOLID, DRY, KISS, YAGNI
- [Suunnittelumallit (yleiskatsaus)](../Design-Patterns.md) — Singleton, Factory, Observer, jne.
- [Clean Architecture](../Architecture/Clean-Architecture.md) — Arkkitehtuuri jossa näitä patterneita käytetään
- [CQRS](../Architecture/CQRS.md) — Command Query Responsibility Segregation
