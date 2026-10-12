# Azure services (English)

> 🇫🇮 Finnish version with all topics: [Azure-palvelut](../../Azure/README.md)

English translations of the Azure pages used in the Cloud technologies course. Pages that are not translated yet link to the Finnish version.

## Contents

### Databases
- [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md) - Managed PostgreSQL (Flexible Server)
  - Why a managed database: state out of the application process
  - Pricing tiers (Burstable B1ms) and cost management
  - Creating the server with the CLI, firewall rules
  - Connection strings and where to keep them
  - EF Core + Npgsql, the stop/start lifecycle

### Infrastructure as Code (IaC)
- [Infrastructure as Code](Infrastructure-as-Code.md) - What IaC is, why it is used and how
  - Declarative vs. imperative, idempotency
  - IaC tools in Azure (Bicep, Terraform, ARM, Pulumi)
  - Practical Bicep examples (Key Vault, App Service, SQL, PostgreSQL, a complete environment)
  - What-if, drift and deployment
- [Bicep - Azure's IaC language](Bicep.md) - Bicep syntax and advanced features
  - Development environment and the VS Code extension
  - Types, decorators, dependencies and `existing` resources
  - Modules, functions and User-Defined Types
  - Testing, validation and troubleshooting

## Learning order

1. [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md)
2. [Infrastructure as Code](Infrastructure-as-Code.md)
3. [Bicep](Bicep.md)

## Not yet translated *(in Finnish)*

- [Cloud Concepts](../../Cloud-Concepts.md)
- [Azure App Service](../../Azure/App-Service.md)
- [Azure Blob Storage](../../Azure/Blob-Storage.md)
- [Azure Functions](../../Azure/Azure-Functions.md)
- [Azure Key Vault](../../Azure/Key-Vault.md)
- [Managed Identity](../../Azure/Managed-Identity.md)
- [Monitoring and Application Insights](../../Azure/Monitoring-and-Application-Insights.md)
- [Cost Management](../../Azure/Cost-Management.md)
