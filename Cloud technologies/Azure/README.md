# Azure-palvelut

Tervetuloa Azure-oppimateriaaliin! Tämä materiaali käsittelee Microsoftin Azure-pilvipalvelun keskeisiä palveluita ja niiden käyttöä sovelluskehityksessä.

## Mikä on Azure?

**Microsoft Azure** on pilvipalvelualusta, joka tarjoaa yli 200 palvelua sovelluskehitykseen, tietojen tallentamiseen, tekoälyyn ja infrastruktuurin hallintaan. Azure tukee useita ohjelmointikieliä ja kehyksiä, ja se integroituu saumattomasti .NET-ekosysteemiin.

## Sisältö

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

### Turvallisuus ja salaisuudet
- [Azure Key Vault](Key-Vault.md) - Salaisuuksien, avainten ja sertifikaattien turvallinen hallinta
  - Key Vaultin käsitteet (Secrets, Keys, Certificates)
  - RBAC-pääsynhallinta
  - Hinnoittelu ja verkkokonfiguraatio

## Teknologiakohtaiset materiaalit

### .NET ja Azure
- [Salaisuuksien hallinta .NET-sovelluksissa](../../C%23/fin/04-Advanced/Secrets-Management/) - User Secrets, Azure-integraatiot ja koodiesimerkit
  - [Azure Environment Variables](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Environment-Variables.md) - Ympäristömuuttujat App Servicessa
  - [Azure Key Vault .NET-integraatio](../../C%23/fin/04-Advanced/Secrets-Management/Azure-Key-Vault.md) - Key Vault + RBAC + Managed Identity + .NET-koodi

### Yleiset periaatteet
- [Salaisuuksien hallinnan yleiset periaatteet](../../Development-guidelines/Secrets-Management/) - Miksi ja miten salaisuuksia hallitaan

## Oppimisjärjestys

1. **Infrastructure as Code** - Ymmärrä miten infrastruktuuria hallitaan koodina
2. **Bicep** - Opi Azuren oma IaC-kieli ja sen syntaksi
3. **Key Vault** - Ymmärrä miten salaisuuksia hallitaan Azuressa
4. **Salaisuuksien hallinta .NET:ssä** - Opi integroimaan Key Vault .NET-sovellukseen

## Hyödyllisiä linkkejä

- [Azure Documentation](https://learn.microsoft.com/en-us/azure/)
- [Azure Portal](https://portal.azure.com)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure for .NET Developers](https://learn.microsoft.com/en-us/dotnet/azure/)
