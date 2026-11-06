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

### Monitoring
- [Azure Monitor and Application Insights](Monitoring-and-Application-Insights.md) - Observability for your application
  - Logs, metrics, traces and correlation
  - Log Analytics + App Insights in Bicep, the .NET SDK (version 3 / OpenTelemetry)
  - Structured logging, PII, KQL
  - Alerts, Action Groups, availability tests, the Azure mobile app

### Related (Development guidelines)
- [CI/CD](../../../Development-guidelines/eng/CI-CD.md) - GitHub Actions, OIDC login to Azure, quality gates

## Learning order

1. [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md)
2. [Infrastructure as Code](Infrastructure-as-Code.md)
3. [Bicep](Bicep.md)
4. [CI/CD](../../../Development-guidelines/eng/CI-CD.md)
5. [Azure Monitor and Application Insights](Monitoring-and-Application-Insights.md)

## Not yet translated *(in Finnish)*

- [Cloud Concepts](../../Cloud-Concepts.md)
- [Azure App Service](../../Azure/App-Service.md)
- [Azure Blob Storage](../../Azure/Blob-Storage.md)
- [Azure Functions](../../Azure/Azure-Functions.md)
- [Azure Key Vault](../../Azure/Key-Vault.md)
- [Managed Identity](../../Azure/Managed-Identity.md)
- [Cost Management](Cost-Management.md)
