# Azure Key Vault

## Sisällysluettelo

1. [Mikä on Key Vault?](#mikä-on-key-vault)
2. [Key Vaultin käsitteet](#key-vaultin-käsitteet)
3. [Hinnoittelu](#hinnoittelu)
4. [RBAC-pääsynhallinta](#rbac-pääsynhallinta)
5. [Managed Identity](#managed-identity)
6. [Verkkokonfiguraatio](#verkkokonfiguraatio)
7. [Audit-lokit ja monitorointi](#audit-lokit-ja-monitorointi)
8. [Key Vaultin luominen](#key-vaultin-luominen)
9. [Salaisuuksien hallinta CLI:llä](#salaisuuksien-hallinta-clillä)
10. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Mikä on Key Vault?

**Azure Key Vault** on Microsoftin pilvipalvelu, joka tarjoaa turvallisen tallennuspaikan:

- **Salaisuuksille** (Secrets) - API-avaimet, salasanat, connection stringit
- **Salausavaimille** (Keys) - Datan salaus ja allekirjoitus
- **Sertifikaateille** (Certificates) - TLS/SSL-sertifikaattien hallinta

### Miksi Key Vault?

| Ongelma | Ratkaisu Key Vaultilla |
|---|---|
| Salaisuudet koodissa tai konfiguraatiossa | Keskitetty, salattu tallennus |
| Kuka pääsee salaisuuksiin? | RBAC-pääsynhallinta |
| Onko salaisuutta käytetty? | Audit-lokit |
| Salaisuus vuotanut - mitä tehdä? | Versiointi ja kierrätys |
| Sertifikaatti vanhenee | Automaattinen uusinta |

---

## Key Vaultin käsitteet

### Secrets (Salaisuudet)

Salaisuudet ovat avain-arvo -pareja, joissa arvo on salattu.

```
Esimerkki:
─────────────────────────────────────────────────
Nimi:     DatabaseConnectionString
Arvo:     Server=prod-db.database.windows.net;...  (salattu)
Versio:   3 (nykyinen), 2 (edellinen), 1 (vanhin)
Voimassa: 2024-01-01 – 2025-01-01
─────────────────────────────────────────────────
```

**Käyttökohteet:**
- Tietokantayhteydet (connection strings)
- API-avaimet (SendGrid, OpenAI, jne.)
- JWT-salausavaimet
- Salasanat

### Keys (Salausavaimet)

Kryptografiset avaimet datan salaukseen ja allekirjoitukseen. Key Vault voi käyttää **HSM** (Hardware Security Module) -suojausta.

**Käyttökohteet:**
- Datan salaus/purku (encrypt/decrypt)
- Allekirjoitus/varmennus (sign/verify)
- Avainten kääriminen (wrap/unwrap)

### Certificates (Sertifikaatit)

TLS/SSL-sertifikaattien hallinta, mukaan lukien automaattinen uusinta.

**Käyttökohteet:**
- HTTPS-sertifikaatit
- Koodiallekirjoitus
- Autentikointi

---

## Hinnoittelu

### SKU-vaihtoehdot

| Ominaisuus | Standard | Premium |
|---|---|---|
| **Salaisuudet** | ✅ Ohjelmistopohjainen salaus | ✅ Ohjelmistopohjainen salaus |
| **Avaimet** | Ohjelmistopohjainen | HSM-suojattu (FIPS 140-2 Level 2) |
| **Sertifikaatit** | ✅ | ✅ |
| **Hinta (salaisuudet)** | ~0.028 €/10 000 operaatiota | ~0.028 €/10 000 operaatiota |
| **Hinta (HSM-avaimet)** | - | ~0.93 €/avain/kk |
| **Käyttökohteet** | Useimmat sovellukset | Korkean turvallisuuden vaatimukset |

> **Suositus:** **Standard**-taso riittää useimpiin sovelluksiin. Premium tarvitaan vain jos regulaatio vaatii HSM-suojausta (esim. finanssiala).

### Ilmaiset operaatiot

- Key Vaultin luominen on ilmaista
- Maksat vain operaatioista (luku, kirjoitus, listaus)
- Tyypillisen sovelluksen kuukausikustannus: **muutamia senttejä**

---

## RBAC-pääsynhallinta

### Permission Model: RBAC vs. Access Policy

Key Vault tukee kahta pääsynhallintamallia. **RBAC on suositeltu.**

```
RBAC (suositeltu):
──────────────────
Azure AD → RBAC-rooli → Key Vault -resurssi
                ↓
    Sama malli kuin muissa Azure-palveluissa

Access Policy (legacy):
───────────────────────
Azure AD → Key Vault Access Policy → Key Vault
                    ↓
    Key Vault-kohtainen, ei yhdenmukainen
```

### Key Vault RBAC -roolit

| Rooli | Salaisuudet | Avaimet | Sertifikaatit | Hallinta |
|---|---|---|---|---|
| **Key Vault Administrator** | CRUD | CRUD | CRUD | ✅ |
| **Key Vault Secrets Officer** | CRUD | - | - | ❌ |
| **Key Vault Secrets User** | Luku | - | - | ❌ |
| **Key Vault Crypto Officer** | - | CRUD | - | ❌ |
| **Key Vault Certificates Officer** | - | - | CRUD | ❌ |
| **Key Vault Reader** | Metatiedot | Metatiedot | Metatiedot | ❌ |

### Suositellut roolimääritykset

| Kuka/Mikä | Rooli | Miksi |
|---|---|---|
| **Sovellus (Managed Identity)** | Key Vault Secrets User | Vain lukuoikeus salaisuuksiin |
| **DevOps/CI/CD** | Key Vault Secrets Officer | Salaisuuksien päivittäminen |
| **Ylläpitäjä** | Key Vault Administrator | Kaikki hallintaoikeudet |
| **Kehittäjä (lokaali)** | Key Vault Secrets User | Salaisuuksien lukeminen kehityksessä |
| **Monitorointi** | Key Vault Reader | Metatietojen lukeminen |

---

## Managed Identity

**Managed Identity** mahdollistaa Azure-resurssien autentikoitumisen muihin Azure-palveluihin **ilman salasanoja tai avaimia**.

### Toimintaperiaate

```
PERINTEINEN TAPA (❌):
┌──────────────┐  client_id + secret  ┌──────────────┐
│  App Service │ ───────────────────→ │  Key Vault   │
└──────────────┘  (salasana koodissa) └──────────────┘

MANAGED IDENTITY (✅):
┌──────────────┐  Managed Identity   ┌──────────────┐
│  App Service │ ──────────────────→ │  Key Vault   │
└──────────────┘  (Azure AD hoitaa)  └──────────────┘
  Ei salasanoja missään!
```

### System-assigned vs. User-assigned

| | System-assigned | User-assigned |
|---|---|---|
| **Luominen** | Resurssin asetuksissa | Erillinen Azure-resurssi |
| **Elinkaari** | Poistetaan resurssin mukana | Itsenäinen |
| **Jakaminen** | Yksi per resurssi | Usean resurssin kesken |
| **Suositus** | Yksinkertaiset tapaukset | Monimutkaiset arkkitehtuurit |

---

## Verkkokonfiguraatio

### Pääsyvaihtoehdot

| Vaihtoehto | Turvallisuus | Käyttökohteet |
|---|---|---|
| **Public (kaikki verkot)** | ⚠️ Matala | Kehitys, pienet projektit |
| **Valitut verkot + IP** | ✅ Keskitaso | Useimmat tuotantosovellukset |
| **Private Endpoint** | ✅ Korkea | Korkean turvallisuuden vaatimukset |
| **Ei julkista pääsyä** | ✅ Korkein | Vain Private Endpoint |

### Firewall-konfiguraatio CLI:llä

```bash
# Salli pääsy tietystä IP-osoitteesta
az keyvault network-rule add \
  --name myapp-kv \
  --ip-address 203.0.113.50

# Salli pääsy Azure-palveluista
az keyvault update \
  --name myapp-kv \
  --bypass AzureServices

# Estä julkinen pääsy (vain Private Endpoint)
az keyvault update \
  --name myapp-kv \
  --public-network-access Disabled
```

---

## Audit-lokit ja monitorointi

### Diagnostiikka-asetukset

Key Vaultin kaikki operaatiot voidaan kirjata **Azure Monitor** -lokeihin:

```bash
# Ota diagnostiikka-lokit käyttöön
az monitor diagnostic-settings create \
  --name kv-diagnostics \
  --resource $(az keyvault show --name myapp-kv --query id --output tsv) \
  --workspace $(az monitor log-analytics workspace show \
    --resource-group MyResourceGroup \
    --workspace-name myapp-logs \
    --query id --output tsv) \
  --logs '[{"category":"AuditEvent","enabled":true}]'
```

### Mitä lokit kertovat?

| Tieto | Esimerkki |
|---|---|
| **Kuka** | Managed Identity, käyttäjä, sovellus |
| **Mitä** | SecretGet, SecretSet, SecretList |
| **Milloin** | Aikaleima |
| **Tulos** | Success, Forbidden, NotFound |
| **IP-osoite** | Kutsun lähde |

### Hälytykset

```bash
# Luo hälytys epäonnistuneista pääsyyrityksistä
az monitor metrics alert create \
  --name kv-unauthorized-alert \
  --resource-group MyResourceGroup \
  --scopes $(az keyvault show --name myapp-kv --query id --output tsv) \
  --condition "total ServiceApiResult > 0 where StatusCode includes 403" \
  --description "Unauthorized access to Key Vault"
```

---

## Key Vaultin luominen

### Azure CLI (suositeltu RBAC-mallilla)

```bash
# 1. Luo Key Vault
az keyvault create \
  --name myapp-kv \
  --resource-group MyResourceGroup \
  --location northeurope \
  --enable-rbac-authorization true \
  --enable-soft-delete true \
  --soft-delete-retention-days 90

# 2. Myönnä itsellesi oikeudet
az role assignment create \
  --role "Key Vault Administrator" \
  --assignee $(az ad signed-in-user show --query id --output tsv) \
  --scope $(az keyvault show --name myapp-kv --query id --output tsv)
```

---

## Salaisuuksien hallinta CLI:llä

### Salaisuuden luominen

```bash
az keyvault secret set \
  --vault-name myapp-kv \
  --name "MySecret" \
  --value "secret-value-here"
```

### Salaisuuden lukeminen

```bash
az keyvault secret show \
  --vault-name myapp-kv \
  --name "MySecret" \
  --query value \
  --output tsv
```

### Salaisuuksien listaaminen

```bash
az keyvault secret list \
  --vault-name myapp-kv \
  --output table
```

### Salaisuuden päivittäminen (uusi versio)

```bash
# Uusi arvo luo automaattisesti uuden version
az keyvault secret set \
  --vault-name myapp-kv \
  --name "MySecret" \
  --value "new-secret-value"
```

### Salaisuuden poistaminen

```bash
# Soft delete - voidaan palauttaa retention-periodin aikana
az keyvault secret delete \
  --vault-name myapp-kv \
  --name "MySecret"

# Palauttaminen
az keyvault secret recover \
  --vault-name myapp-kv \
  --name "MySecret"
```

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Käytä RBAC:ia** Access Policyn sijaan
- **Ota Soft Delete käyttöön** - suojaa vahingossa poistamiselta
- **Erota Key Vaultit ympäristöittäin** (`myapp-dev-kv`, `myapp-prod-kv`)
- **Käytä Managed Identity:ä** sovelluksille
- **Rajaa verkkopääsy** - salli vain tarvittavat IP:t ja Azure-palvelut
- **Ota audit-lokit käyttöön** - seuraa kuka käyttää mitäkin salaisuutta
- **Kierrätä salaisuudet** - vaihda avaimet säännöllisesti
- **Noudata least privilege -periaatetta** - anna vain tarvittavat roolit

### ❌ Vältä näitä

- Älä käytä yhtä Key Vaultia kaikille ympäristöille
- Älä anna **Key Vault Administrator** -roolia sovelluksille
- Älä jätä verkkopääsyä rajoittamatta tuotannossa
- Älä unohda audit-lokeja

---

## .NET-integraatio

Katso yksityiskohtaiset .NET-integrointiohjeet ja koodiesimerkit:

- [Azure Key Vault .NET-integraatio](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Key-Vault.md) - DefaultAzureCredential, AddAzureKeyVault, koodiesimerkit

## Takaisin

- [Azure-palvelut](README.md)

## Hyödyllisiä linkkejä

- [Azure Key Vault Documentation](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Azure Key Vault Pricing](https://azure.microsoft.com/en-us/pricing/details/key-vault/)
- [Azure RBAC for Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide)
- [Managed Identities](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
