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

### Identity and secrets
- [Managed Identity](Managed-Identity.md) - Authentication without passwords
  - Enable the identity, grant RBAC, DefaultAzureCredential in code
  - Local development with `az login`, the token flow, System- vs. User-assigned
- [Azure Key Vault](Key-Vault.md) - Secrets, keys and certificates
  - RBAC roles, Managed Identity, Key Vault references in App Service
  - Network configuration, audit logs, managing secrets with the CLI

### Cost
- [Cost Management](Cost-Management.md) - Tracking and controlling cloud spend
  - Meters, SKUs and the Retail Prices API; Cost analysis and the query API
  - Budgets, tags, rightsizing with metrics, hidden costs
  - Automatic shutdown: cron, alert processing rules; production price factors

### Related (Development guidelines)
- [CI/CD](../../../Development-guidelines/eng/CI-CD.md) - GitHub Actions, OIDC login to Azure, quality gates

## Learning order

1. [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md)
2. [Infrastructure as Code](Infrastructure-as-Code.md)
3. [Bicep](Bicep.md)
4. [CI/CD](../../../Development-guidelines/eng/CI-CD.md)
5. [Azure Monitor and Application Insights](Monitoring-and-Application-Insights.md)
6. [Cost Management](Cost-Management.md)
7. [Managed Identity](Managed-Identity.md)
8. [Azure Key Vault](Key-Vault.md)

## Not yet translated *(in Finnish)*

- [Cloud Concepts](../../Cloud-Concepts.md)
- [Azure App Service](../../Azure/App-Service.md)
- [Azure Blob Storage](../../Azure/Blob-Storage.md)
- [Azure Functions](../../Azure/Azure-Functions.md)
