# Autentikointi ASP.NET Core -sovelluksissa

Tervetuloa autentikoinnin oppimateriaaliin! Tämä materiaali käsittelee, miten käyttäjien tunnistaminen (autentikointi) ja oikeuksien hallinta toteutetaan ASP.NET Core -sovelluksissa JWT-tokenien avulla.

## Autentikointi vs. Autorisaatio

Nämä kaksi käsitettä sekoitetaan usein, mutta ne ovat eri asioita:

```
Autentikointi (Authentication)          Autorisaatio (Authorization)
─────────────────────────────           ─────────────────────────────
"Kuka sinä olet?"                       "Mitä sinä saat tehdä?"
                                        
Käyttäjä todistaa henkilöllisyytensä    Järjestelmä tarkistaa käyttäjän
esim. käyttäjätunnuksella ja            oikeudet esim. roolin perusteella
salasanalla                             

Esimerkki:                              Esimerkki:
─────────                               ─────────
Kirjaudut sisään                        Admin-käyttäjä voi poistaa
käyttäjätunnuksella                     käyttäjiä, tavallinen käyttäjä
ja salasanalla                          ei voi
→ Järjestelmä tietää kuka olet          → Järjestelmä tietää mitä saat tehdä
```

### Prosessi käytännössä

```
┌─────────┐      1. Kirjautuminen       ┌──────────┐
│         │ ──────────────────────────→  │          │
│ Käyttäjä│      (tunnus + salasana)     │ Palvelin │
│         │                              │          │
│         │  2. Autentikointi OK         │          │
│         │  ←─────────────────────────  │          │
│         │     (JWT-token palautetaan)  │          │
│         │                              │          │
│         │  3. Pyyntö + token           │          │
│         │  ──────────────────────────→ │          │
│         │     Authorization: Bearer... │          │
│         │                              │          │
│         │  4. Autorisaatio tarkistettu │          │
│         │  ←─────────────────────────  │          │
│         │     (data tai 403 Forbidden) │          │
└─────────┘                              └──────────┘
```

---

## Token-pohjainen vs. Session-pohjainen autentikointi

| Ominaisuus | Session-pohjainen | Token-pohjainen (JWT) |
|---|---|---|
| **Tila (State)** | Palvelin tallentaa session | Tilaton (stateless) - ei palvelinmuistia |
| **Tallennus** | Session ID evästessä | Token evästessä tai localStoragessa |
| **Skaalautuvuus** | Haastavampaa (session jaettava palvelinten kesken) | Helpompaa (jokainen palvelin voi validoida tokenin) |
| **Mikropalvelut** | Vaatii keskitetyn session hallinnan | Token kulkee palvelusta toiseen |
| **Mobiilisovellukset** | Evästeet hankalia mobiilissa | Tokenit toimivat hyvin |
| **Vanheneminen** | Palvelin hallinnoi | Tokenissa itsessään (`exp`-claim) |
| **Mitätöinti** | Helppo (poista session palvelimelta) | Haastavampaa (token on voimassa kunnes vanhenee) |

**Miksi JWT on suosittu?**
- Tilaton → ei tarvita palvelinpuolen sessiota
- Skaalautuu helposti useille palvelimille
- Toimii hyvin API-pohjaisissa sovelluksissa ja mikropalveluissa
- Sisältää käyttäjätiedot (claims) suoraan tokenissa

---

## Sisältö

### 1. [JWT (JSON Web Token)](JWT.md)
- Mikä on JWT?
- JWT:n rakenne (Header, Payload, Signature)
- Claims-käsite
- JWT:n elinkaari
- ASP.NET Core JWT-autentikoinnin toteutus C#-esimerkein

### 2. [Refresh Tokens](Refresh-Tokens.md)
- Mikä on Refresh Token?
- Access Token vs. Refresh Token
- Token Rotation -strategia
- Refresh Token -toteutus C#-esimerkein (Entity Framework, kontrollerit)

---

## Oppimisjärjestys

Suosittelemme opiskelua seuraavassa järjestyksessä:

1. **Lue tämä sivu ensin** - Ymmärrä autentikoinnin ja autorisaation ero
2. **[JWT](JWT.md)** - Opi JWT:n teoria ja perus toteutus ASP.NET Coressa
3. **[Refresh Tokens](Refresh-Tokens.md)** - Opi turvallinen tokenien uusimisstrategia

### Esitiedot

Ennen tätä materiaalia sinun tulisi hallita:
- [C# perusteet](../../00-Basics/) - Muuttujat, luokat, rajapinnat
- [Dependency Injection](../Dependency-Injection.md) - DI-perusteet ASP.NET Coressa
- [Salaisuuksien hallinta](../Secrets-Management/) - JWT-avaimien turvallinen tallennus

---

## Hyödyllisiä linkkejä

- [Microsoft: ASP.NET Core Authentication](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/)
- [Microsoft: JWT Bearer Authentication](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/jwt)
- [JWT.io - JWT Debugger](https://jwt.io/)
- [RFC 7519 - JSON Web Token](https://datatracker.ietf.org/doc/html/rfc7519)
