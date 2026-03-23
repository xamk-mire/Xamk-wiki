# Azure-palvelut

Tervetuloa Azure-oppimateriaaliin! Tämä materiaali käsittelee Microsoftin Azure-pilvipalvelun keskeisiä palveluita ja niiden käyttöä sovelluskehityksessä.

## Mikä on Azure?

**Microsoft Azure** on pilvipalvelualusta, joka tarjoaa yli 200 palvelua sovelluskehitykseen, tietojen tallentamiseen, tekoälyyn ja infrastruktuurin hallintaan. Azure tukee useita ohjelmointikieliä ja kehyksiä, ja se integroituu saumattomasti .NET-ekosysteemiin.

## Sisältö

### Sovellusten isännöinti
- [Azure App Service](App-Service.md) - .NET-sovellusten isännöinti ja julkaisu
  - App Service Plan -tasot (F1, B1, S1...)
  - Web Appin luominen (Portal + CLI)
  - .NET-sovelluksen julkaisu: ZIP-deploy, Visual Studio Publish, GitHub Actions
  - Deployment Slots, lokit ja monitorointi

### Serverless
- [Azure Functions](Azure-Functions.md) - Serverless-sovellukset ja event-driven arkkitehtuuri
  - Serverless-arkkitehtuuri ja sen hyödyt
  - Triggerit (HTTP, Timer, Queue, Blob, Service Bus)
  - Bindings (Input/Output)
  - Azure Functions .NET:llä (Isolated Worker Model)
  - Paikallinen kehitys ja julkaisu
  - Durable Functions
  - Azure Functions vs. App Service -vertailu

### Infrastructure as Code (IaC)
- [Infrastructure as Code](Infrastructure-as-Code.md) - Mikä on IaC, miksi sitä käytetään ja miten
  - IaC-lähestymistavat (deklaratiivinen vs. imperatiivinen)
  - IaC-työkalut Azuressa (Bicep, Terraform, ARM, Pulumi)
  - Käytännön Bicep-esimerkit (Key Vault, App Service, SQL, kokonainen ympäristö)
  - Moduulit, parametrit ja deployment
- [Bicep - Azuren IaC-kieli](Bicep.md) - Bicepin syntaksi ja edistyneet ominaisuudet
  - Kehitysympäristön pystytys ja VS Code -laajennus
  - Resurssimäärittelyt, tyypit ja dekoraattorit
  - Moduulit, funktiot ja User-Defined Types
  - Yleiset kuviot (nimeäminen, tagit, ympäristökonfiguraatio, monitorointi)

### Turvallisuus ja identiteetti
- [Azure Key Vault](Key-Vault.md) - Salaisuuksien, avainten ja sertifikaattien turvallinen hallinta
  - Key Vaultin käsitteet (Secrets, Keys, Certificates)
  - RBAC-pääsynhallinta
  - Hinnoittelu ja verkkokonfiguraatio
- [Managed Identity](Managed-Identity.md) - Autentikointi ilman salasanoja
  - System-assigned vs. User-assigned Managed Identity
  - RBAC-oikeuksien myöntäminen
  - DefaultAzureCredential -autentikointiketju
  - Paikallinen kehitys Azure CLI -kirjautumisella

## Teknologiakohtaiset materiaalit

### .NET ja Azure
- [Salaisuuksien hallinta .NET-sovelluksissa](../../C%23/fin/04-Advanced/Secrets-Management/) - User Secrets, Azure-integraatiot ja koodiesimerkit
  - [Azure Environment Variables](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Environment-Variables.md) - Ympäristömuuttujat App Servicessa
  - [Azure Key Vault .NET-integraatio](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Key-Vault.md) - Key Vault + RBAC + Managed Identity + .NET-koodi

### Yleiset periaatteet
- [Salaisuuksien hallinnan yleiset periaatteet](../../Development-guidelines/Secrets-Management/) - Miksi ja miten salaisuuksia hallitaan

## Oppimisjärjestys

### Sovelluskehittäjille (.NET + Azure)
1. **App Service** - Opi isännöimään .NET-sovellus Azuressa
2. **Managed Identity** - Ymmärrä autentikointi ilman salasanoja
3. **Key Vault** - Opi hallitsemaan salaisuuksia turvallisesti
4. **Salaisuuksien hallinta .NET:ssä** - Integroi Key Vault .NET-sovellukseen

### Infrastruktuuri ja DevOps
1. **Infrastructure as Code** - Ymmärrä miten infrastruktuuria hallitaan koodina
2. **Bicep** - Opi Azuren oma IaC-kieli ja sen syntaksi

## Hyödyllisiä linkkejä

- [Azure Documentation](https://learn.microsoft.com/en-us/azure/)
- [Azure Portal](https://portal.azure.com)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure for .NET Developers](https://learn.microsoft.com/en-us/dotnet/azure/)
