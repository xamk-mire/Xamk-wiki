# Azure Key Vault
> 🇫🇮 Finnish version: [Key-Vault.md](../../Azure/Key-Vault.md)

## Table of Contents

1. [What is Key Vault?](#what-is-key-vault)
2. [Key Vault concepts](#key-vault-concepts)
3. [Pricing](#pricing)
4. [RBAC access control](#rbac-access-control)
5. [Managed Identity](#managed-identity)
6. [Key Vault references in App Service](#key-vault-references-in-app-service)
7. [Network configuration](#network-configuration)
8. [Audit logs and monitoring](#audit-logs-and-monitoring)
9. [Creating a Key Vault](#creating-a-key-vault)
10. [Managing secrets with the CLI](#managing-secrets-with-the-cli)
11. [Best practices](#best-practices)

---

## What is Key Vault?

**Azure Key Vault** is Microsoft's cloud service for storing securely:

- **Secrets** - API keys, passwords, connection strings
- **Keys** - Cryptographic keys for encrypting and signing data
- **Certificates** - TLS/SSL certificate management

### Why Key Vault?

| Problem | Solution with Key Vault |
|---|---|
| Secrets in code or configuration | Centralised, encrypted storage |
| Who can reach the secrets? | RBAC access control |
| Has a secret been used? | Audit logs |
| A secret leaked - what now? | Versioning and rotation |
| A certificate is expiring | Automatic renewal |

---

## Key Vault concepts

### Secrets

Secrets are key-value pairs whose value is encrypted.

```
Example:
─────────────────────────────────────────────────
Name:     DatabaseConnectionString
Value:    Server=prod-db.database.windows.net;...  (encrypted)
Version:  3 (current), 2 (previous), 1 (oldest)
Valid:    2024-01-01 – 2025-01-01
─────────────────────────────────────────────────
```

**Typical uses:**
- Database connections (connection strings)
- API keys (SendGrid, OpenAI, etc.)
- JWT signing keys
- Passwords

### Keys

Cryptographic keys for encrypting and signing data. Key Vault can protect them with an **HSM** (Hardware Security Module).

**Typical uses:**
- Encrypting/decrypting data
- Signing/verifying
- Key wrapping (wrap/unwrap)

### Certificates

TLS/SSL certificate management, including automatic renewal.

**Typical uses:**
- HTTPS certificates
- Code signing
- Authentication

### Name, version and soft delete

- **The vault name is globally unique** and part of a DNS name (`https://<name>.vault.azure.net/`): 3–24 characters, letters, digits and hyphens, starting with a letter. The course's `kv-cloud26-<name>-dev` fits only if `<name>` is short.
- **Every `secret set` creates a new version.** A secret URI without a version (`.../secrets/AdminApiKey/`) always means the latest — which is why Key Vault references are written without a version, and rotation needs no configuration change.
- **Soft delete is always on.** A deleted secret or a whole vault stays recoverable for 7–90 days (`--soft-delete-retention-days`). Side effect: a deleted vault's **name stays reserved** for the whole period — `az keyvault create` with the same name fails until the vault is recovered (`az keyvault recover`) or destroyed for good (`az keyvault purge`). *Purge protection* blocks the latter entirely; worth it in production, not on the course.

---

## Pricing

### SKU options

| Feature | Standard | Premium |
|---|---|---|
| **Secrets** | ✅ Software-based encryption | ✅ Software-based encryption |
| **Keys** | Software-based | HSM-protected (FIPS 140-2 Level 2) |
| **Certificates** | ✅ | ✅ |
| **Price (secrets)** | ~0.028 €/10 000 operations | ~0.028 €/10 000 operations |
| **Price (HSM keys)** | - | ~0.93 €/key/month |
| **Use cases** | Most applications | High-security requirements |

> **Recommendation:** the **Standard** tier is enough for most applications. Premium is needed only when regulation requires HSM protection (e.g. finance).

### Free operations

- Creating a Key Vault is free
- You pay only for operations (read, write, list)
- A typical application's monthly cost: **a few cents**

---

## RBAC access control

### Permission model: RBAC vs. Access Policy

Key Vault supports two access-control models. **RBAC is the recommended one.**

```
RBAC (recommended):
───────────────────
Entra ID → RBAC role → Key Vault resource
                ↓
    The same model as in other Azure services

Access Policy (legacy):
───────────────────────
Entra ID → Key Vault Access Policy → Key Vault
                    ↓
    Key Vault specific, not uniform
```

> **Two planes:** *managing* a Key Vault (creation, network settings, deletion) is a control-plane right that Owner and Contributor get automatically. The *values* of secrets are a data-plane right that **no control-plane role grants** — a subscription Owner gets `Forbidden` until they hold `Key Vault Secrets User` or `Officer`. See [a role assignment and the two planes](Managed-Identity.md#a-role-assignment-who-which-role-where--and-the-two-planes).

### Key Vault RBAC roles

| Role | Secrets | Keys | Certificates | Management |
|---|---|---|---|---|
| **Key Vault Administrator** | CRUD | CRUD | CRUD | ✅ |
| **Key Vault Secrets Officer** | CRUD | - | - | ❌ |
| **Key Vault Secrets User** | Read | - | - | ❌ |
| **Key Vault Crypto Officer** | - | CRUD | - | ❌ |
| **Key Vault Certificates Officer** | - | - | CRUD | ❌ |
| **Key Vault Reader** | Metadata | Metadata | Metadata | ❌ |

### Recommended role assignments

| Who/what | Role | Why |
|---|---|---|
| **Application (Managed Identity)** | Key Vault Secrets User | Read-only access to secrets |
| **DevOps/CI/CD** | Key Vault Secrets Officer | Updating secrets |
| **Administrator** | Key Vault Administrator | Full management rights |
| **Developer (local)** | Key Vault Secrets User | Reading secrets during development |
| **Monitoring** | Key Vault Reader | Reading metadata |

---

## Managed Identity

A **Managed Identity** lets Azure resources authenticate to other Azure services **without passwords or keys**.

### How it works

```
TRADITIONAL WAY (❌):
┌──────────────┐  client_id + secret  ┌──────────────┐
│  App Service │ ───────────────────→ │  Key Vault   │
└──────────────┘  (password in code)  └──────────────┘

MANAGED IDENTITY (✅):
┌──────────────┐  Managed Identity   ┌──────────────┐
│  App Service │ ──────────────────→ │  Key Vault   │
└──────────────┘  (Entra ID handles  └──────────────┘
  No passwords anywhere!   it)
```

### System-assigned vs. User-assigned

| | System-assigned | User-assigned |
|---|---|---|
| **Creation** | In the resource's settings | A separate Azure resource |
| **Lifecycle** | Deleted with the resource | Independent |
| **Sharing** | One per resource | Shared across several resources |
| **Recommendation** | Simple cases | Complex architectures |

---

## Key Vault references in App Service

The application does not always have to call Key Vault itself (`SecretClient`). App Service can fetch the secret on your behalf with a **Key Vault reference**: an Application Setting whose value is a pointer into Key Vault. The application sees an ordinary environment variable — it knows nothing about Key Vault.

### Syntax

```
@Microsoft.KeyVault(SecretUri=https://<vault-name>.vault.azure.net/secrets/<secret-name>/)
```

When the version is left out (note the trailing `/`), App Service always fetches the **latest version** — rotating the secret needs no configuration change.

### Prerequisites

1. The App Service has a **Managed Identity** (system-assigned is enough)
2. The identity holds the **Key Vault Secrets User** role on that vault
3. The Application Setting value is in the form above (set in Bicep, with the CLI or in the Portal)

### Bicep example

```bicep
appSettings: [
  {
    name: 'AdminApiKey'
    value: '@Microsoft.KeyVault(SecretUri=${keyVault.properties.vaultUri}secrets/AdminApiKey/)'
  }
]
```

Note: **Bicep only sets the pointer** — the secret's value is not in the template or in version control. The value is set once, separately (`az keyvault secret set ...`).

### Troubleshooting

Portal → App Service → **Environment variables**: every Key Vault reference shows a status next to it (green ✓ / red ✗). Red almost always means the Managed Identity is missing or the role has not been granted — and a role change can take 1–6 minutes.

The same status from the command line, for a script or a screenshot (`az webapp config appsettings list` shows only the raw `@Microsoft.KeyVault(...)` string, not the status):

```powershell
$AppId = az webapp show --resource-group $RG --name $APP --query id --output tsv
az rest --method get `
  --url "https://management.azure.com$AppId/config/configreferences/appsettings?api-version=2023-12-01" `
  --query "value[].{setting:name, status:properties.status, details:properties.details}" --output table
```

| `status` | Meaning |
|----------|---------|
| `Resolved` | The value was fetched; the application sees it as an ordinary setting |
| `AccessToKeyVaultDenied` | The identity has no data-plane role (or it is not in effect yet) |
| `SecretNotFound` / `VaultNotFound` | A typo in the URI, or the secret has not been set |
| `MSINotEnabled` | The application has no managed identity |

App Service fetches the reference's value at startup and refreshes it in the background about once a day — a new version is picked up immediately by restarting the application.

### SecretClient vs. Key Vault reference

| | Key Vault reference | SecretClient in code |
|--|---------------------|----------------------|
| Code change | No — the application reads ordinary configuration | Yes — an SDK call |
| Changing the secret at run time | No — read at startup/update | Yes — can be fetched at any time |
| Works locally | No (an App Service feature) — locally the value comes from e.g. user secrets | Yes (`DefaultAzureCredential` + `az login`) |
| Suits | Settings read at startup (the most common case) | Dynamic secret handling |

---

## Network configuration

### Access options

| Option | Security | Use cases |
|---|---|---|
| **Public (all networks)** | ⚠️ Low | Development, small projects |
| **Selected networks + IP** | ✅ Medium | Most production applications |
| **Private Endpoint** | ✅ High | High-security requirements |
| **No public access** | ✅ Highest | Private Endpoint only |

### Firewall configuration with the CLI

```bash
# Allow access from a specific IP address
az keyvault network-rule add \
  --name myapp-kv \
  --ip-address 203.0.113.50

# Allow access from Azure services
az keyvault update \
  --name myapp-kv \
  --bypass AzureServices

# Deny public access (Private Endpoint only)
az keyvault update \
  --name myapp-kv \
  --public-network-access Disabled
```

---

## Audit logs and monitoring

### Diagnostic settings

Every Key Vault operation can be written to **Azure Monitor** logs:

```bash
# Enable diagnostic logs
az monitor diagnostic-settings create \
  --name kv-diagnostics \
  --resource $(az keyvault show --name myapp-kv --query id --output tsv) \
  --workspace $(az monitor log-analytics workspace show \
    --resource-group MyResourceGroup \
    --workspace-name myapp-logs \
    --query id --output tsv) \
  --logs '[{"category":"AuditEvent","enabled":true}]'
```

### What do the logs tell you?

| Information | Example |
|---|---|
| **Who** | Managed Identity, user, application |
| **What** | SecretGet, SecretSet, SecretList |
| **When** | Timestamp |
| **Result** | Success, Forbidden, NotFound |
| **IP address** | Source of the call |

### Alerts

```bash
# Create an alert for failed access attempts
az monitor metrics alert create \
  --name kv-unauthorized-alert \
  --resource-group MyResourceGroup \
  --scopes $(az keyvault show --name myapp-kv --query id --output tsv) \
  --condition "total ServiceApiResult > 0 where StatusCode includes 403" \
  --description "Unauthorized access to Key Vault"
```

---

## Creating a Key Vault

### Azure CLI (recommended, with the RBAC model)

```bash
# 1. Create the Key Vault
az keyvault create \
  --name myapp-kv \
  --resource-group MyResourceGroup \
  --location northeurope \
  --enable-rbac-authorization true \
  --enable-soft-delete true \
  --soft-delete-retention-days 90     # 7–90; short for a course, long for production

# 2. Grant yourself permissions (a data-plane role — Owner is not enough to read secrets)
az role assignment create \
  --role "Key Vault Administrator" \
  --assignee-object-id $(az ad signed-in-user show --query id --output tsv) \
  --assignee-principal-type User \
  --scope $(az keyvault show --name myapp-kv --query id --output tsv)
```

---

## Managing secrets with the CLI

### Creating a secret

```bash
az keyvault secret set \
  --vault-name myapp-kv \
  --name "MySecret" \
  --value "secret-value-here"
```

### Reading a secret

```bash
az keyvault secret show \
  --vault-name myapp-kv \
  --name "MySecret" \
  --query value \
  --output tsv
```

### Listing secrets

```bash
az keyvault secret list \
  --vault-name myapp-kv \
  --output table
```

### Updating a secret (a new version)

```bash
# A new value automatically creates a new version
az keyvault secret set \
  --vault-name myapp-kv \
  --name "MySecret" \
  --value "new-secret-value"
```

### Deleting a secret

```bash
# Soft delete - can be recovered during the retention period
az keyvault secret delete \
  --vault-name myapp-kv \
  --name "MySecret"

# Recovery
az keyvault secret recover \
  --vault-name myapp-kv \
  --name "MySecret"
```

---

## Best practices

### ✅ Do

- **Use RBAC** instead of Access Policies
- **Enable Soft Delete** - protects against accidental deletion
- **Separate Key Vaults per environment** (`myapp-dev-kv`, `myapp-prod-kv`)
- **Use Managed Identity** for applications
- **Restrict network access** - allow only the IPs and Azure services you need
- **Enable audit logs** - see who uses which secret
- **Rotate secrets** - change keys regularly
- **Follow least privilege** - grant only the roles that are needed

### ❌ Avoid

- Do not use one Key Vault for every environment
- Do not grant the **Key Vault Administrator** role to applications
- Do not leave network access unrestricted in production
- Do not forget the audit logs

---

## .NET integration

Detailed .NET integration instructions and code examples:

- [Azure Key Vault .NET integration](../../../C%23/fin/04-Advanced/Secrets-Management/Azure-Key-Vault.md) *(in Finnish)* - DefaultAzureCredential, AddAzureKeyVault, code examples

## Back

- [Azure services](README.md)

## Useful links

- [Azure Key Vault Documentation](https://learn.microsoft.com/en-us/azure/key-vault/)
- [Azure Key Vault Pricing](https://azure.microsoft.com/en-us/pricing/details/key-vault/)
- [Azure RBAC for Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/rbac-guide)
- [Managed Identities](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)
