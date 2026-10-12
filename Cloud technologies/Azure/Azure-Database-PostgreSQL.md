# Azure Database for PostgreSQL — hallittu tietokanta pilvessä

## Sisällysluettelo

1. [Miksi hallittu tietokanta?](#miksi-hallittu-tietokanta)
2. [Flexible Server -palvelumalli](#flexible-server--palvelumalli)
3. [Hintatasot ja kustannukset](#hintatasot-ja-kustannukset)
4. [Palvelimen luominen](#palvelimen-luominen)
5. [Verkko ja palomuuri](#verkko-ja-palomuuri)
6. [Yhteysmerkkijono (connection string)](#yhteysmerkkijono-connection-string)
7. [Käyttö .NET-sovelluksesta (EF Core + Npgsql)](#käyttö-net-sovelluksesta-ef-core--npgsql)
8. [Microsoft Entra -autentikointi — yhteys ilman salasanaa](#microsoft-entra--autentikointi--yhteys-ilman-salasanaa)
9. [Stop, start ja kustannusten hallinta](#stop-start-ja-kustannusten-hallinta)
10. [Parhaat käytännöt](#parhaat-käytännöt)

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
