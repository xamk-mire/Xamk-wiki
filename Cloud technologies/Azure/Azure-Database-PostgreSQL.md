# Azure Database for PostgreSQL — hallittu tietokanta pilvessä
> 🇬🇧 English version: [Azure-Database-PostgreSQL.md](../eng/Azure/Azure-Database-PostgreSQL.md)

## Sisällysluettelo

1. [Miksi hallittu tietokanta?](#miksi-hallittu-tietokanta)
2. [Flexible Server -palvelumalli](#flexible-server--palvelumalli)
3. [Hintatasot ja kustannukset](#hintatasot-ja-kustannukset)
4. [Palvelimen luominen](#palvelimen-luominen)
5. [Verkko ja palomuuri](#verkko-ja-palomuuri)
6. [Yhteysmerkkijono (connection string)](#yhteysmerkkijono-connection-string)
7. [Käyttö .NET-sovelluksesta (EF Core + Npgsql)](#käyttö-net-sovelluksesta-ef-core--npgsql)
8. [Microsoft Entra -autentikointi — yhteys ilman salasanaa](#microsoft-entra--autentikointi--yhteys-ilman-salasanaa)
9. [Varmuuskopiot ja palautus (PITR)](#varmuuskopiot-ja-palautus-pitr)
10. [Stop, start ja kustannusten hallinta](#stop-start-ja-kustannusten-hallinta)
11. [Parhaat käytännöt](#parhaat-käytännöt)

---

## Miksi hallittu tietokanta?

Pilvisovelluksen **tila** (data) ei saa asua sovellusprosessin muistissa eikä sovellusinstanssin levyllä — muuten horisontaalinen skaalaus ja uudelleenkäynnistykset rikkovat datan. Tila siirretään **ulkoiseen, hallittuun tietokantaan**.

**Hallittu tietokanta (PaaS)** tarkoittaa, että Azure huolehtii:

| Azure hoitaa | Sinä hoidat |
|--------------|-------------|
| Palvelinraudan ja käyttöjärjestelmän | Skeeman ja datan |
| PostgreSQL-asennuksen ja päivitykset | Kyselyt ja indeksit |
| Varmuuskopiot (oletuksena 7 pv) | Yhteysmerkkijonon ja salaisuuksien hallinnan |
| Korkean käytettävyyden (valinnainen) | SKU:n valinnan ja kustannukset |
| Levytilan laajennuksen | Palomuurisäännöt |

Vaihtoehto olisi asentaa PostgreSQL itse virtuaalikoneelle (IaaS) — silloin kaikki vasemman sarakkeen työt olisivat sinun. Opiskelu- ja tuotantoprojekteissa hallittu palvelu on lähes aina oikea valinta.

```
Sovellus (App Service, stateless)          Tietokanta (Flexible Server)
┌──────────────┐  ┌──────────────┐         ┌────────────────────────┐
│  Instanssi A │  │  Instanssi B │  ─────► │  PostgreSQL            │
│  (ei tilaa)  │  │  (ei tilaa)  │         │  → data, varmuuskopiot │
└──────────────┘  └──────────────┘         │  → jaettu totuus       │
                                           └────────────────────────┘
```

---

## Flexible Server -palvelumalli

**Azure Database for PostgreSQL – Flexible Server** on Azuren nykyinen PostgreSQL-palvelumalli (vanha "Single Server" on poistunut). Nimi "flexible" viittaa siihen, että voit valita laskentatehon ja tallennustilan erikseen sekä pysäyttää palvelimen.

Keskeiset ominaisuudet:

- Täysi PostgreSQL — normaalit työkalut toimivat (psql, pgAdmin, EF Core, Npgsql)
- **Burstable-taso** opiskeluun ja kehitykseen (halpa, purskahteleva CPU)
- **Stop/Start** — pysäytetyltä palvelimelta ei laskuteta laskentaa
- Automaattiset varmuuskopiot, point-in-time restore
- Palomuurisäännöt tai VNet-integraatio

---

## Hintatasot ja kustannukset

Hinta muodostuu **kahdesta osasta**: laskenta (compute, per tunti) ja tallennustila (storage, per GB/kk).

### Kehitys ja opiskelu

| SKU | vCores | RAM | Laskenta ~/kk | Huomioitavaa |
|-----|--------|-----|---------------|--------------|
| **B1ms** (Burstable) | 1 | 2 GB | ~13 € | Riittää mainiosti kurssiprojektiin |
| **B2s** (Burstable) | 2 | 4 GB | ~26 € | Jos B1ms ei riitä |

### Tuotanto

| SKU | vCores | RAM | Laskenta ~/kk | Huomioitavaa |
|-----|--------|-----|---------------|--------------|
| **D2ds_v5** (General Purpose) | 2 | 8 GB | ~130 € | Tasainen suorituskyky, ei burstausta |

Lisäksi tallennustila: pienin koko **32 GB ≈ 4 €/kk**. 

> **Tärkeä kustannushuomio:** Tallennustila laskutetaan **myös pysäytetyltä palvelimelta**. Vain poistaminen lopettaa laskutuksen kokonaan.

> **Opiskeluprojekteissa:** käytä **Burstable B1ms + 32 GB**. Pysäytä palvelin, kun et käytä sitä — tai poista se ja luo tarvittaessa uudelleen skriptillä/Bicepillä.

---

## Palvelimen luominen

### Azure CLI

```bash
# Muuttujat
$RG = "rg-myapp-dev"
$PG = "pg-myapp-<uniikki-tunniste>"     # nimen pitää olla globaalisti uniikki
$LOCATION = "northeurope"

# Luo Flexible Server (Burstable B1ms, PostgreSQL 16)
az postgres flexible-server create `
  --resource-group $RG `
  --name $PG `
  --location $LOCATION `
  --tier Burstable `
  --sku-name Standard_B1ms `
  --storage-size 32 `
  --version 16 `
  --admin-user myadmin `
  --admin-password "<vahva-salasana>" `
  --database-name myappdb `
  --public-access <oma-ip>
```

| Parametri | Selitys |
|-----------|---------|
| `--tier Burstable` + `--sku-name Standard_B1ms` | Halvin taso — CPU "burstaa" tarvittaessa |
| `--storage-size 32` | Pienin mahdollinen levy (GB) |
| `--version 16` | PostgreSQL-versio |
| `--admin-user` / `--admin-password` | Pääkäyttäjän tunnukset — **eivät saa päätyä versionhallintaan** |
| `--database-name` | Luo samalla sovelluksen tietokannan |
| `--public-access <oma-ip>` | Avaa palomuurin omalle koneellesi (kehitystä varten) |

Luonti kestää tyypillisesti 5–10 minuuttia.

> **Salasanavinkki:** generoi vahva salasana äläkä kirjoita sitä skriptiin. PowerShellissä voit lukea sen ajon aikana: `$pw = Read-Host -AsSecureString "DB password"`.

---

## Verkko ja palomuuri

Flexible Serverin julkinen päätepiste on oletuksena **kokonaan kiinni**. Yhteydet sallitaan palomuurisäännöillä:

```bash
# Salli Azure-palvelut (esim. App Service) — erikoissääntö 0.0.0.0
az postgres flexible-server firewall-rule create `
  --resource-group $RG `
  --name $PG `
  --rule-name AllowAzureServices `
  --start-ip-address 0.0.0.0 `
  --end-ip-address 0.0.0.0

# Salli oma kehityskone
az postgres flexible-server firewall-rule create `
  --resource-group $RG `
  --name $PG `
  --rule-name MyDevMachine `
  --start-ip-address <oma-ip> `
  --end-ip-address <oma-ip>
```

| Sääntö | Merkitys |
|--------|----------|
| `0.0.0.0 – 0.0.0.0` | Erikoisarvo: "salli liikenne Azuren sisältä" (App Service, Functions...). **Ei** tarkoita koko internetiä |
| `<oma-ip> – <oma-ip>` | Yksittäinen IP — oma koneesi kehityskäyttöön |

> **Huom:** `AllowAzureServices` sallii liikenteen *kaikista* Azure-palveluista, myös muiden asiakkaiden. Se on hyväksyttävä oikotie kehityksessä ja opiskeluprojekteissa; tuotannossa käytetään VNet-integraatiota tai private endpointia.

---

## Yhteysmerkkijono (connection string)

PostgreSQL-yhteysmerkkijono Npgsql-muodossa:

```
Host=pg-myapp-xyz.postgres.database.azure.com;Database=myappdb;Username=myadmin;Password=<salasana>;Ssl Mode=Require
```

| Osa | Selitys |
|-----|---------|
| `Host` | Palvelimen täysi DNS-nimi (`<nimi>.postgres.database.azure.com`) |
| `Database` | Tietokannan nimi |
| `Username` / `Password` | Pääkäyttäjä tai sovellukselle luotu käyttäjä |
| `Ssl Mode=Require` | Azure vaatii TLS-salatun yhteyden |

### Minne yhteysmerkkijono laitetaan?

| Ympäristö | Paikka | Miksi |
|-----------|--------|-------|
| Paikallinen kehitys | `appsettings.Development.json` (paikallinen kanta) tai User Secrets (Azure-kanta) | Ei tuotantosalaisuuksia repoon |
| Azure App Service | **Application Settings**: `ConnectionStrings__DefaultConnection` | Ympäristömuuttuja yliajaa appsettings.json:in |
| Tuotanto (paras taso) | Key Vault + Managed Identity | Ei salasanoja missään konfiguraatiossa |

```bash
# Aseta App Serviceen
az webapp config appsettings set `
  --resource-group $RG `
  --name $APP `
  --settings ConnectionStrings__DefaultConnection="Host=...;Database=...;Username=...;Password=...;Ssl Mode=Require"
```

> **Kaksi alaviivaa (`__`)** vastaa JSON-hierarkiaa: `ConnectionStrings__DefaultConnection` = `{ "ConnectionStrings": { "DefaultConnection": "..." } }`. Koodi ei muutu ympäristöjen välillä — vain konfiguraatio.

---

## Käyttö .NET-sovelluksesta (EF Core + Npgsql)

```bash
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL
```

```csharp
// Program.cs
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("DefaultConnection")));
```

```csharp
// Data/AppDbContext.cs
public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Product> Products => Set<Product>();
}
```

### Skeeman luonti: EnsureCreated vs. migraatiot

| | `Database.EnsureCreated()` | EF Core -migraatiot |
|---|---|---|
| **Mitä tekee** | Luo skeeman suoraan mallista, jos kantaa ei ole | Versioidut muutosskriptit (`dotnet ef migrations add`) |
| **Skeeman muutos** | Ei osaa päivittää olemassa olevaa kantaa | Päivittää hallitusti (`database update`) |
| **Sopii** | Harjoitukset, prototyypit | Tuotanto ja kaikki pidempi kehitys |

```csharp
// Harjoituskäyttöön: luo skeema käynnistyksessä
using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    db.Database.EnsureCreated();
}
```

### Migraatiot käytännössä: historiataulu, baseline ja omistajuus

Kun siirryt `EnsureCreated`ista migraatioihin, nämä käsitteet tulevat vastaan heti:

| Käsite | Mikä se on |
|--------|------------|
| **`dotnet-ef`** + `Microsoft.EntityFrameworkCore.Design` | Komentorivityökalu (`dotnet tool install --global dotnet-ef`) ja paketti, jonka avulla se osaa rakentaa sovelluksesi `DbContext`in. `dotnet ef` käynnistää `Program.cs`:n vain DI-säiliön rakentamiseen asti — startup-lohko (seed, `Migrate()`) ei aja |
| **Migraatiotiedostot** | `Migrations/<aikaleima>_<Nimi>.cs` (`Up()` tekee muutoksen, `Down()` peruu), `.Designer.cs` (metatiedot) ja `<Context>ModelSnapshot.cs` — EF:n muisti mallista, jota vasten seuraava `migrations add` lasketaan. Kaikki versionhallintaan |
| **`__EFMigrationsHistory`** | Taulu kannassa: yksi rivi per ajettu migraatio (`MigrationId`, `ProductVersion` = EF:n versio). `Migrate()` vertaa sitä assemblyn migraatioihin ja ajaa puuttuvat järjestyksessä |
| **`Migrate()` käynnistyksessä** | Yksinkertaisin tapa: sovellus päivittää skeeman ennen kuin se vastaa pyyntöihin. EF Core 9+ ottaa tietokantalukon (PostgreSQL: advisory lock), joten kaksi instanssia eivät aja samaa migraatiota päällekkäin — mutta kumpikaan ei palvele ennen kuin migraatio on valmis |
| **Migraatio putkessa** | Tuotantomalli: `dotnet ef migrations bundle` tuottaa itsenäisen suoritettavan, jonka deploy-workflow ajaa kantaa vasten *ennen* sovelluksen julkaisua. Vaatii, että runner pääsee kantaan (palomuuri) ja että putkella on oma tietokantaprincipal |
| **`IsRelational()`** | Integraatiotestit käyttävät InMemory-provideria, jolla ei ole migraatioita — `Migrate()` heittää. Haara `if (db.Database.IsRelational()) db.Database.Migrate(); else db.Database.EnsureCreated();` pitää yhden `Program.cs`:n molemmille |
| **Baseline** | Olemassa oleva kanta (jonka `EnsureCreated` rakensi) ei tunne historiataulua → `Migrate()` yrittäisi luoda taulut uudelleen (`relation "Events" already exists`). Ratkaisu: luo historiataulu ja lisää ensimmäisen migraation rivi **käsin** — "skeema vastaa migraatiota 1" ajamatta sitä |
| **Omistajuus** | Vain taulun **omistaja** saa `ALTER TABLE`. Jos sovellus kirjautuu omalla principalillaan (Entra) ja taulut loi admin, migraatio kaatuu virheeseen `42501: must be owner of table` — `ALTER TABLE … OWNER TO <sovelluksen rooli>` adminina korjaa. DML-grantit (`SELECT/INSERT/UPDATE/DELETE`) eivät riitä skeemamuutoksiin |
| **Nullable ensin** | Uusi sarake lisätään `NULL`-sallivana (tai oletusarvolla), koska rivejä on jo olemassa — `NOT NULL` ilman oletusta kaatuu ensimmäiseen riviin. Tiukennus on oma, myöhempi migraationsa (expand → contract) |

### Transientit viat: EnableRetryOnFailure

Tietokantayhteys voi katketa hetkeksi ilman että mikään on "rikki": failover, huoltokäynnistys, verkkokatkos sekunneiksi. EF Coren **execution strategy** uusii epäonnistuneen operaation automaattisesti:

```csharp
options.UseNpgsql(dataSource, npgsql => npgsql.EnableRetryOnFailure(
    maxRetryCount: 3,                        // yritysten määrä ensimmäisen jälkeen
    maxRetryDelay: TimeSpan.FromSeconds(5),  // kasvava viive, enintään tämä
    errorCodesToAdd: null));                 // lisää omat SQLSTATE-koodit transienteiksi
```

Yhdistä se lyhyempään yhteysaikakatkaisuun (`Timeout=5` yhteysmerkkijonossa; Npgsql:n oletus on 15 s). Huomaa kääntöpuoli: oikeassa **katkossa** (palvelin pysäytetty) retry tekee vastauksesta hitaamman — neljä yritystä × 5 s + viiveet ≈ 25 s — ja `/health`-päätepisteen pitäisi mieluummin epäonnistua *nopeasti*, jotta valvonta huomaa katkon. Retry auttaa sekuntien vikoihin, ei minuuttien. Lisäksi retry-strategia ei salli käsin avattuja transaktioita ilman `ExecuteAsync`-käärettä.

---

## Microsoft Entra -autentikointi — yhteys ilman salasanaa

Flexible Server tukee salasanan lisäksi (tai sijasta) **Microsoft Entra -autentikointia**: tietokantaan kirjaudutaan Entra-identiteetillä ja lyhytikäisellä tokenilla. Sovellukselle tämä tarkoittaa yhdistettynä [Managed Identityyn](Managed-Identity.md): **yhteysmerkkijonossa ei ole salasanaa lainkaan**.

### Käyttöönotto pääpiirteissään

1. **Entra-autentikointi päälle palvelimella** (Bicep `authConfig` tai `az postgres flexible-server update --active-directory-auth Enabled`)
2. **Entra-admin palvelimelle**: `az postgres flexible-server microsoft-entra-admin create ...` (vanhemmissa CLI-versioissa `ad-admin create`)
3. **Sovelluksen identiteetistä tietokantarooli**: Entra-adminina yhdistettynä ajetaan `postgres`-kannassa:

```sql
select * from pgaadauth_create_principal('<app-service-nimi>', false, false);
```

4. **Oikeudet roolille** sovelluksen tietokannassa (`GRANT` normaalisti)
5. **Sovellus hakee tokenin** scopella `https://ossrdbms-aad.database.windows.net/.default` ja käyttää sitä salasanana — Npgsql:ssä `NpgsqlDataSourceBuilder.UsePeriodicPasswordProvider` uusii tokenin automaattisesti

### Entra-admin, tietokantaprincipal ja GRANTit

Kolme asiaa, jotka yllä oleva luettelo nimeää mutta ei selitä:

- **Entra-admin** on palvelintason asetus (`Microsoft.DBforPostgreSQL/flexibleServers/administrators`), ei tietokantarooli: se nimeää Entra-olion (käyttäjä tai ryhmä) objectId:n ja tenantId:n perusteella ja antaa sille superkäyttäjän kaltaiset oikeudet. Admin on se, joka luo muut principalit. Bicepissä se on oma resurssinsa `parent: postgresServer`, nimi = objectId. Jos CLI ja tilaus ovat eri tenanteissa, komento kaatuu "Tenant identifier does not match" — anna tenantId eksplisiittisesti (REST `PUT …/administrators/{objectId}` body `tenantId`).
- **`pgaadauth_create_principal(nimi, isAdmin, isMfa)`** luo kantaan roolin, jonka nimi on Entra-olion näyttönimi (managed identityllä sovelluksen nimi). `isAdmin = false` → tavallinen rooli, `isMfa = false` → ei vaadi monivaiheista tunnistusta (palvelulle ei voi vaatia). Rooli **kirjautuu tokenilla**, jonka audience on `https://ossrdbms-aad.database.windows.net/.default` (CLI: `--resource-type oss-rdbms`) — token toiseen palveluun (Key Vault, ARM) ei kelpaa, vaikka se on saman identiteetin.
- **GRANTit ovat tavallista PostgreSQL:ää.** `GRANT USAGE ON SCHEMA public` antaa luvan *nähdä* skeeman oliot, `CREATE ON SCHEMA` luvan luoda tauluja (migraatiot!), `SELECT, INSERT, UPDATE, DELETE ON ALL TABLES` ovat DML-oikeudet. Omistajuus on erikseen: `ALTER TABLE` saa tehdä vain taulun **omistaja**, joten migraatioita ajava sovellus tarvitsee `ALTER TABLE … OWNER TO <rooli>` — DML-grantit eivät riitä.

```csharp
// Npgsql: token salasanana, uusitaan ennen vanhenemista
var credential = new DefaultAzureCredential();
var dsb = new NpgsqlDataSourceBuilder(connectionString);   // Host=…;Database=…;Username=<app-nimi>;Ssl Mode=Require — ei salasanaa
dsb.UsePeriodicPasswordProvider(
    async (_, ct) => (await credential.GetTokenAsync(
        new TokenRequestContext(["https://ossrdbms-aad.database.windows.net/.default"]), ct)).Token,
    TimeSpan.FromMinutes(45),   // uusi token reilusti ennen ~60 min vanhenemista
    TimeSpan.FromSeconds(10));  // epäonnistuessa yritä pian uudelleen
builder.Services.AddDbContext<AppDbContext>(o => o.UseNpgsql(dsb.Build()));
```

### Tokenilla kirjautuminen psql:llä (kehittäjä itse)

```powershell
$env:PGPASSWORD = az account get-access-token --resource-type oss-rdbms --query accessToken --output tsv
psql "host=<server>.postgres.database.azure.com dbname=postgres user=<oma-upn> sslmode=require"
```

### Miksi tämä on parempi kuin salasana?

| Salasana | Entra-token |
|----------|-------------|
| Pitkäikäinen — vuoto on pysyvä ongelma | Voimassa ~1 h — vuoto vanhenee itsestään |
| Säilytettävä jossain (secret, vault) | Ei säilytetä — haetaan tarvittaessa |
| Kierrätys on manuaalinen projekti | "Kierrätys" tapahtuu joka tunti itsestään |
| Sama kaikille käyttäjille helposti | Identiteettikohtainen — audit kertoo kuka teki |

Salasana-autentikoinnin voi lopulta poistaa kokonaan (`passwordAuth: 'Disabled'`), jolloin palvelimeen ei ole olemassa yhtään salasanaa.

---

## Varmuuskopiot ja palautus (PITR)

Flexible Server ottaa **automaattiset varmuuskopiot** jatkuvasti: täysi kopio kerran vuorokaudessa ja transaktioloki sen päälle, jolloin palautus onnistuu **mihin tahansa hetkeen** säilytysajalta (point-in-time restore, PITR). Säilytysaika (`backupRetentionDays`) on 7–35 päivää, oletus 7; varmuuskopiotila on ilmaista provisioidun levyn kokoon asti.

| Asia | Miten se toimii |
|------|-----------------|
| Palautuspiste | Mikä tahansa UTC-aikaleima välillä `earliestRestoreDate` (`az postgres flexible-server show --query backup.earliestRestoreDate`) ja nyt. Uuden palvelimen ensimmäinen täysi kopio voi kestää vuorokauden |
| Palautus luo **uuden palvelimen** | `az postgres flexible-server restore --name <uusi> --source-server <lähde> --restore-time <UTC>` — lähde jää koskematta, voit vertailla ja perua. Komento kestää 5–15 min (kurssin testissä 7 min) |
| Mitä palautuu | Data ja skeema palautushetken mukaan (myös `__EFMigrationsHistory` — sen hetken migraatiot), admin-asetukset, Entra-admin, `authConfig`, SKU |
| Mitä **ei** palaudu | **Palomuurisäännöt** (uudella palvelimella ei ole yhtään — ensimmäinen `psql` saa *Connection refused*), sovelluksen yhteysmerkkijono (osoittaa yhä vanhaan), tagit |
| Lähde pysäytetty? | Palautus vaatii käynnissä olevan lähdepalvelimen |

Kaksi lukua, joita ei voi tietää tekemättä palautusta kerran:

- **RTO** (Recovery Time Objective): kuinka kauan palvelu on poissa — palautuskomennon kesto + palomuurisäännöt + yhteysmerkkijonon vaihto putken kautta + `/health` vihreäksi. Kurssimittakaavassa 15 min harjoitelleena, tunti harjoittelematta.
- **RPO** (Recovery Point Objective): kuinka paljon tuoreinta dataa hyväksyt menettäväsi — palautuspisteen ja virheen välinen aika. PITR:llä se on niin pieni kuin tiedät virheen hetken.

**Testaamaton varmuuskopio on huhu.** Palautusharjoitus (restore drill) — palauta, tarkista kirjautuminen ja data, mittaa, poista uusi palvelin — toistetaan säännöllisesti, koska kanta kasvaa, asetukset muuttuvat ja ihmiset vaihtuvat.

---

## Stop, start ja kustannusten hallinta

Flexible Serverin voi **pysäyttää**, jolloin laskentaa ei laskuteta (tallennustilaa laskutetaan silti):

```bash
# Pysäytä (compute-laskutus loppuu)
az postgres flexible-server stop --resource-group $RG --name $PG

# Käynnistä
az postgres flexible-server start --resource-group $RG --name $PG

# Poista kokonaan (kaikki laskutus loppuu — data häviää!)
az postgres flexible-server delete --resource-group $RG --name $PG --yes
```

> **Huom:** Pysäytetty palvelin **käynnistyy automaattisesti 7 päivän kuluttua**. Pysäytys on siis tauko, ei pysyvä ratkaisu. Jos et tarvitse kantaa viikkoihin, poista se ja luo uudelleen skriptillä tai Bicepillä.

### Kustannusmuistilista

1. Tarkista SKU:n hinta ennen luontia (Pricing Calculator)
2. Burstable B1ms riittää opiskeluun
3. Pysäytä, kun et käytä — muista 7 päivän automaattikäynnistys
4. Tallennustila laskuttaa aina — poista turha palvelin kokonaan
5. Tagit (`Environment`, `Owner`) kantaan siinä missä muihinkin resursseihin

---

## Parhaat käytännöt

### ✅ Hyvät käytännöt

- **Yhteysmerkkijono ympäristömuuttujaan** (App Service Application Settings) — ei koskaan koodiin tai repoon
- **`Ssl Mode=Require`** aina Azure-yhteyksissä
- **Pienin riittävä SKU** ja stop/delete kun ei käytetä
- **Migraatiot** heti, kun skeema alkaa elää (EnsureCreated vain harjoituksiin)
- **Palomuuri minimiin**: oma IP kehitykseen, AllowAzureServices sovellukselle — ei `0.0.0.0–255.255.255.255`

### ❌ Vältä näitä

- Älä commitoi salasanaa — edes "väliaikaisesti"
- Älä käytä pääkäyttäjätunnusta sovelluksen tunnuksena tuotannossa (luo erillinen käyttäjä)
- Älä jätä B1ms-palvelinta pyörimään kuukausiksi käyttämättömänä — se on ~17 €/kk tyhjäkäyntiä
- Älä aja `EnsureCreated()`-kutsua tuotantokannassa, jossa on jo dataa ja migraatioita

---

## Seuraavaksi

- [Azure App Service](App-Service.md) - Sovelluksen isännöinti ja Application Settings
- [Azure Key Vault](Key-Vault.md) - Salaisuuksien hallinta tuotantotasolla
- [Infrastructure as Code](Infrastructure-as-Code.md) - Tietokannan luonti Bicepillä

## Takaisin

- [Azure-palvelut — Yleiskatsaus](README.md)
