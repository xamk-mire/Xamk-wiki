# Azure Blob Storage — tiedostot pilvessä

## Sisällysluettelo

- [Miksi object storage?](#miksi-object-storage)
- [Rakenne: tili, kontti, blobi](#rakenne-tili-kontti-blobi)
- [Nimeämissäännöt](#nimeämissäännöt)
- [Redundanssi (LRS, ZRS, GRS)](#redundanssi-lrs-zrs-grs)
- [Access tierit ja kustannukset](#access-tierit-ja-kustannukset)
- [Storage-tilin luominen](#storage-tilin-luominen)
- [Pääsynhallinta: avaimet, SAS ja Entra ID](#pääsynhallinta-avaimet-sas-ja-entra-id)
- [Käyttö .NET-sovelluksesta](#käyttö-net-sovelluksesta)
- [Elinkaarisäännöt (lifecycle management)](#elinkaarisäännöt-lifecycle-management)
- [Parhaat käytännöt](#parhaat-käytännöt)

## Miksi object storage?

Web-palvelimen levy on väärä paikka käyttäjien lataamille tiedostoille:

- **Levy on prosessikohtaista tilaa.** Konteissa ja skaalatuissa ympäristöissä jokaisella instanssilla on oma levynsä — tiedosto tallentuu yhdelle instanssille ja "katoaa", kun pyyntö osuu toiseen. Sama ongelma kuin muistissa pidetyllä datalla.
- **Levy kuolee palvelun mukana.** Uudelleenluonti (IaC, konttien vaihto, planin poisto) hävittää tiedostot. (App Servicessä on poikkeuksena jaettu `/home`-kansio, mutta sekin on sidottu planin elinkaareen eikä ole tiedosto*palvelu*.)
- **Web-palvelin ei ole tiedostopalvelu.** Ei versiointia, ei elinkaarisääntöjä, ei CDN-integraatiota, ei tapaa jakaa linkkiä ohittamatta sovellusta, ja tiedostojen tarjoilu syö sovelluksen kapasiteettia.

**Object storage** (Azuressa Blob Storage, AWS:ssä S3) on pilven vastaus: rajattomasti skaalautuva, erittäin halpa, HTTP:llä käytettävä tiedostosäilö, jonka elinkaari on riippumaton sovelluksesta. Sovellus pysyy tilattomana: rivit tietokantaan, tiedostot blobiin.

## Rakenne: tili, kontti, blobi

```
Storage account  (stcloud26mattidev)     ← globaalisti uniikki nimi, laskutusyksikkö
  ├── Container  (posters)               ← "kansio", jolla oma pääsypolitiikka
  │     ├── Blob (7b0efc71-....jpg)      ← itse tiedosto + metadata (mm. Content-Type)
  │     └── Blob (a3c9d2e0-....png)
  └── Container  (thumbnails)
```

- **Storage account** on ylätaso: nimi, sijainti, redundanssi ja verkkoasetukset. Sama tili voi sisältää blobien lisäksi myös jonoja (Queue), taulukoita (Table) ja tiedostojakoja (Azure Files).
- **Container** ryhmittelee blobit ja määrittää pääsytason (yksityinen vai anonyymi luku).
- **Blob** on yksittäinen tiedosto. Tavallisin tyyppi on *block blob* (tiedostot); lisäksi on *append blob* (lokit) ja *page blob* (levykuvat).

## Nimeämissäännöt

Storage-tilin nimi on Azuren tunnetuin poikkeus nimeämiskäytäntöihin:

| Sääntö | Storage account |
|--------|-----------------|
| Merkit | **Vain pienet kirjaimet ja numerot — ei väliviivoja!** |
| Pituus | 3–24 merkkiä |
| Uniikkius | Globaalisti uniikki (nimestä tulee osa URL:ia: `https://<nimi>.blob.core.windows.net`) |

Kurssin käytäntö: `st<projekti><omanimi><ympäristö>` → esim. `stcloud26mattidev`.

## Redundanssi (LRS, ZRS, GRS)

| SKU | Kopiot | Kestää | Hinta |
|-----|--------|--------|-------|
| **Standard_LRS** | 3 kopiota yhdessä datacenterissä | Levyrikot | Halvin — oikea valinta kurssille ja useimmille dev-ympäristöille |
| **Standard_ZRS** | 3 kopiota eri availability zoneissa | Datacenterin vikaantuminen | ~25 % kalliimpi |
| **Standard_GRS** | LRS + 3 kopiota toisessa regionissa | Koko regionin tuho | ~2× LRS |

Data ei siis koskaan ole yhden levyn varassa — edes halvimmalla tasolla.

## Access tierit ja kustannukset

Blob-tallennuksessa ei ole tuntilaskutettavaa computea — maksat tavuista ja operaatioista:

| Tier | Tallennushinta | Lukuhinta | Käyttötarkoitus |
|------|----------------|-----------|-----------------|
| **Hot** | ~0,02 €/GB/kk | Halvin | Aktiivisesti käytetyt tiedostot (oletus) |
| **Cool** | ~0,01 €/GB/kk | Kalliimpi/operaatio | Harvoin luettava (varmuuskopiot) |
| **Archive** | ~0,002 €/GB/kk | Palautus kestää tunteja | Arkistointi |

Mittakaava: tuhat 500 kt:n kuvaa Hot-tierissä ≈ **1 sentti kuukaudessa**. Kurssikäytössä storage-tilin kustannus on käytännössä nolla — mutta se näkyy silti Cost analysis -näkymässä omana rivinään, mikä on hyvä havaita.

## Storage-tilin luominen

```powershell
az storage account create `
  --name stcloud26mattidev `
  --resource-group rg-cloud26-matti-dev `
  --location northeurope `
  --sku Standard_LRS `
  --kind StorageV2 `
  --allow-blob-public-access false `
  --min-tls-version TLS1_2 `
  --tags Environment=dev Course=cloud26 Owner=matti@edu.xamk.fi

az storage container create `
  --name posters `
  --account-name stcloud26mattidev `
  --auth-mode key
```

- `--allow-blob-public-access false` estää anonyymin pääsyn koko tilin tasolla — mikään kontti ei voi vahingossakaan olla julkinen. Tämä on nykyään suositeltu oletus.
- `--auth-mode key` käyttää tilin avainta. Vaihtoehto `--auth-mode login` käyttää Entra ID -identiteettiäsi, mutta vaatii **data-tason** RBAC-roolin (esim. *Storage Blob Data Contributor*) — Owner-rooli on vain *hallintatason* rooli eikä yksin riitä datan lukemiseen. Tämä hallinta- ja datatason ero on tärkeä ymmärtää.

## Pääsynhallinta: avaimet, SAS ja Entra ID

Kolme tapaa päästä blobeihin, heikoimmasta vahvimpaan:

1. **Tilin avaimet (account keys)** — kaksi täysvaltaista, pitkäikäistä avainta. Yhteysmerkkijono (`DefaultEndpointsProtocol=...;AccountKey=...`) sisältää avaimen, joten se on salaisuus siinä missä tietokannan salasanakin. Helpoin aloittaa, huonoin ylläpitää.
2. **SAS (Shared Access Signature)** — allekirjoitettu, **aikarajattu ja oikeusrajattu** URL yksittäiseen blobiin tai konttiin (esim. "lukuoikeus tähän kuvaan 15 minuutiksi"). Oikea tapa antaa selaimelle suora latauslinkki ilman, että kontista tehdään julkista tai liikenne kierrätetään sovelluksen läpi.
3. **Entra ID + Managed Identity** — ei avaimia lainkaan: sovelluksen identiteetille annetaan data-tason rooli (*Storage Blob Data Contributor*) ja SDK hakee tokenin automaattisesti (`DefaultAzureCredential`). Tuotannon paras käytäntö. Katso [Managed Identity](Managed-Identity.md).

## Käyttö .NET-sovelluksesta

Paketti: `dotnet add package Azure.Storage.Blobs`

```csharp
// Rekisteröinti (Program.cs) — yhteysmerkkijonolla:
builder.Services.AddSingleton(
    new BlobContainerClient(connectionString, "posters"));

// ...tai ilman salaisuuksia Managed Identityllä:
builder.Services.AddSingleton(
    new BlobContainerClient(
        new Uri("https://stcloud26mattidev.blob.core.windows.net/posters"),
        new DefaultAzureCredential()));
```

```csharp
// Lataus blobiin (upload) — ylikirjoittaa saman nimisen blobin
var blob = containerClient.GetBlobClient(id.ToString());
await blob.UploadAsync(stream, new BlobUploadOptions
{
    HttpHeaders = new BlobHttpHeaders { ContentType = "image/jpeg" }
});

// Luku (download stream)
var download = await blob.DownloadStreamingAsync();
return Results.Stream(download.Value.Content, download.Value.Details.ContentType);
```

`BlobContainerClient` on säieturvallinen ja tarkoitettu jaettavaksi — rekisteröi singletonina. Muista, että käyttäjän lataama tiedosto on **järjestelmän raja**: validoi koko ja sisältötyyppi ennen tallennusta.

## Elinkaarisäännöt (lifecycle management)

Storage-tilille voi määrittää sääntöjä, jotka Azure ajaa automaattisesti — esimerkiksi "siirrä Cool-tieriin 30 päivän jälkeen, poista 365 päivän jälkeen":

```powershell
az storage account management-policy create `
  --account-name stcloud26mattidev `
  --resource-group rg-cloud26-matti-dev `
  --policy '{
    "rules": [{
      "enabled": true,
      "name": "expire-old-posters",
      "type": "Lifecycle",
      "definition": {
        "filters": { "blobTypes": ["blockBlob"], "prefixMatch": ["posters/"] },
        "actions": { "baseBlob": {
          "tierToCool":  { "daysAfterModificationGreaterThan": 30 },
          "delete":      { "daysAfterModificationGreaterThan": 365 }
        }}
      }
    }]
  }'
```

Tämä on kustannushallintaa ilman yhtäkään ajastettua skriptiä — alusta hoitaa.

## Parhaat käytännöt

- **Nimeä blobit sovelluksen avaimilla** (esim. tapahtuman id), älä käyttäjän antamilla tiedostonimillä — ei polkuinjektioita, ei nimikirjanpitoa.
- **Pidä kontit yksityisinä** (`--allow-blob-public-access false`) ja tarjoile joko sovelluksen läpi tai SAS-linkeillä.
- **Validoi lataukset**: koko, sisältötyyppi ja tarvittaessa sisältö — käyttäjän tiedosto on epäluotettavaa syötettä.
- **Aseta Content-Type** ladatessa, jotta selain osaa näyttää tiedoston oikein.
- **Standard_LRS + Hot** riittää lähes aina dev-käyttöön; älä osta redundanssia jota et tarvitse.
- **Tuotannossa: Managed Identity**, ei tilin avaimia — ja jos avaimia on pakko käyttää, kierrätä niitä.

## Seuraavaksi

- [Managed Identity](Managed-Identity.md) — pääsy ilman avaimia
- [Key Vault](Key-Vault.md) — jos avain on pakko säilyttää, säilytä se oikein
- [Cost Management](Cost-Management.md) — mistä storage-rivi löytyy Cost analysisista

## Takaisin

- [Azure-materiaalit](README.md)
