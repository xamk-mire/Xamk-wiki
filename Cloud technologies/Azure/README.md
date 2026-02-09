# Azure-palvelut

Tervetuloa Azure-oppimateriaaliin! Tämä materiaali käsittelee Microsoftin Azure-pilvipalvelun keskeisiä palveluita ja niiden käyttöä sovelluskehityksessä.

## Mikä on Azure?

**Microsoft Azure** on pilvipalvelualusta, joka tarjoaa yli 200 palvelua sovelluskehitykseen, tietojen tallentamiseen, tekoälyyn ja infrastruktuurin hallintaan. Azure tukee useita ohjelmointikieliä ja kehyksiä, ja se integroituu saumattomasti .NET-ekosysteemiin.

## Sisältö

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

1. **Key Vault** - Ymmärrä miten salaisuuksia hallitaan Azuressa
2. **Salaisuuksien hallinta .NET:ssä** - Opi integroimaan Key Vault .NET-sovellukseen

## Hyödyllisiä linkkejä

- [Azure Documentation](https://learn.microsoft.com/en-us/azure/)
- [Azure Portal](https://portal.azure.com)
- [Azure CLI Documentation](https://learn.microsoft.com/en-us/cli/azure/)
- [Azure for .NET Developers](https://learn.microsoft.com/en-us/dotnet/azure/)
