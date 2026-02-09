# Salaisuuksien hallinta (Secrets Management)

Tervetuloa salaisuuksien hallinnan oppimateriaaliin! Tämä materiaali käsittelee, miksi ja miten sovelluksen salaisuuksia hallitaan turvallisesti eri ympäristöissä.

## Mikä on salaisuus?

**Salaisuus** (secret) on mikä tahansa tieto, jonka paljastuminen voi aiheuttaa tietoturvariskin. Esimerkkejä:

| Salaisuuden tyyppi | Esimerkki |
|---|---|
| **Tietokantayhteys** | `Server=mydb.database.windows.net;Password=S3cret!` |
| **API-avain** | `sk-abc123def456...` |
| **JWT-salausavain** | `MySecretSigningKey2024!` |
| **OAuth Client Secret** | `client_secret=XyZ789...` |
| **Sähköpostipalvelun tunnus** | SendGrid API Key |
| **Tallennustilin avain** | Azure Storage Account Key |

---

## Miksi salaisuuksia ei saa tallentaa koodiin?

### ❌ Näin EI pidä tehdä

```csharp
// ❌ VÄÄRIN: Salaisuus suoraan koodissa
public class MyService
{
    private readonly string _apiKey = "sk-abc123def456";
    private readonly string _connectionString = 
        "Server=mydb;Database=prod;User=admin;Password=S3cret!";
}
```

```json
// ❌ VÄÄRIN: Salaisuus appsettings.json-tiedostossa (versionhallinnassa!)
{
  "ConnectionStrings": {
    "Default": "Server=mydb;Password=S3cret!"
  },
  "ApiKeys": {
    "SendGrid": "SG.real-api-key-here"
  }
}
```

### Miksi tämä on vaarallista?

1. **Versionhallinta tallentaa kaiken** - Vaikka poistat salaisuuden myöhemmin, se jää Git-historiaan
2. **Koodikatselmointi** - Pull requesteissa salaisuudet näkyvät kaikille tiimin jäsenille
3. **Julkiset repositoryt** - Botit skannaavat GitHubia jatkuvasti etsien vuotaneita avaimia
4. **Ei ympäristökohtaisuutta** - Sama salaisuus kaikissa ympäristöissä on turvallisuusriski
5. **Vaikea kierrättää** - Salaisuuden vaihtaminen vaatii koodimuutoksen ja uudelleendeployauksen

---

## Salaisuuksien hallinnan tasot

Salaisuuksien hallinta vaihtelee ympäristön mukaan:

```
┌─────────────────────────────────────────────────────────────┐
│                    TUOTANTO (Production)                     │
│  Azure Key Vault + Managed Identity                         │
│  → Korkein turvallisuustaso                                 │
│  → Ei salaisuuksia koodissa tai konfiguraatiossa            │
│  → Automaattinen autentikointi ilman tunnuksia              │
├─────────────────────────────────────────────────────────────┤
│                    STAGING / TEST                            │
│  Azure Environment Variables / Key Vault                    │
│  → Ympäristökohtaiset asetukset                             │
│  → Eristetty tuotannosta                                    │
├─────────────────────────────────────────────────────────────┤
│                    LOKAALI KEHITYS                           │
│  .NET User Secrets / .env-tiedostot                         │
│  → Kehittäjäkohtaiset asetukset                             │
│  → Ei versionhallinnassa                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Lähestymistavat vertailussa

| Ominaisuus | User Secrets | Environment Variables | Azure Key Vault |
|---|---|---|---|
| **Käyttöympäristö** | Lokaali kehitys | Azure App Service | Azure (kaikki palvelut) |
| **Turvallisuustaso** | Matala (ei salattu) | Keskitaso | Korkea (salattu, auditoitu) |
| **Salaus** | ❌ Ei | ⚠️ Palvelimen taso | ✅ HSM-suojattu |
| **Versiointi** | ❌ Ei | ❌ Ei | ✅ Kyllä |
| **Audit-loki** | ❌ Ei | ❌ Ei | ✅ Kyllä |
| **Keskitetty hallinta** | ❌ Ei | ❌ Ei | ✅ Kyllä |
| **Pääsynhallinta** | Käyttöjärjestelmätaso | Azure Portal / RBAC | RBAC / Managed Identity |
| **Hinta** | Ilmainen | Ilmainen | Edullinen (~0.03€/10k operaatiota) |
| **Soveltuvuus** | Kehitys | Staging / pieni tuotanto | Tuotanto |

---

## .gitignore-käytännöt

Varmista, että seuraavat tiedostot ovat `.gitignore`-tiedostossa:

```gitignore
# Salaisuudet - ÄLÄ KOSKAAN lisää versionhallintaan!
appsettings.Development.json
appsettings.Local.json
.env
.env.local
.env.development

# User Secrets (tallennetaan käyttäjäprofiilin alle, ei projektissa)
# Nämä eivät normaalisti ole projektikansiossa, mutta varmuuden vuoksi:
secrets.json
```

> **Huom:** `appsettings.json` voi olla versionhallinnassa, mutta siinä **ei saa olla salaisuuksia**. Käytä sitä vain ei-salaisille asetuksille (esim. logging-tasot, CORS-asetukset).

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä User Secrets -työkalua** lokaalissa kehityksessä
- **Käytä Azure Key Vaultia** tuotannossa ja staging-ympäristössä
- **Käytä Managed Identity:ä** Azuressa - ei salasanoja palveluiden välillä
- **Kierrätä salaisuudet säännöllisesti** - vaihda avaimet esim. 90 päivän välein
- **Noudata vähimmän oikeuden periaatetta** - anna vain tarvittavat oikeudet
- **Auditoi pääsy** - seuraa kuka käyttää mitäkin salaisuutta

### ❌ Yleisiä virheitä

- Salaisuuksien tallentaminen `appsettings.json`-tiedostoon
- Salaisuuksien kovakoodaaminen lähdekoodiin
- Saman salaisuuden käyttö kaikissa ympäristöissä
- API-avainten jakaminen sähköpostilla tai chatissa
- `.gitignore`-tiedoston unohtaminen ennen ensimmäistä commitia

---

## Teknologiakohtaiset materiaalit

- [Salaisuuksien hallinta .NET-sovelluksissa](../../C%23/fin/04-Advanced/Secrets-Management/) - User Secrets, Azure-integraatiot ja koodiesimerkit

## Pilvipalvelumateriaalit

- [Azure Key Vault](../../Cloud%20technologies/Azure/Key-Vault.md) - Key Vault pilvipalveluna

## Hyödyllisiä linkkejä

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [Microsoft: Safe storage of app secrets in development](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets)
- [Azure Key Vault Documentation](https://learn.microsoft.com/en-us/azure/key-vault/)
