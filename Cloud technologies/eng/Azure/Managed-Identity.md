# Azure Managed Identity — authentication without passwords
> 🇫🇮 Finnish version: [Managed-Identity.md](../../Azure/Managed-Identity.md)

## Table of Contents

1. [What is a Managed Identity?](#what-is-a-managed-identity)
2. [Three steps in practice](#three-steps-in-practice)
3. [Step 1 — Enable the Managed Identity](#step-1--enable-the-managed-identity)
4. [Step 2 — Grant RBAC permissions](#step-2--grant-rbac-permissions)
5. [Step 3 — DefaultAzureCredential in code](#step-3--defaultazurecredential-in-code)
6. [Local development](#local-development)
7. [How does it work under the hood?](#how-does-it-work-under-the-hood)
8. [System-assigned vs. User-assigned](#system-assigned-vs-user-assigned)
9. [Best practices](#best-practices)

---

## What is a Managed Identity?

Imagine your App Service application is a new employee in a company. Before it can touch sensitive resources — such as the secrets in a Key Vault — it needs an **ID card** and **access rights** to the right rooms.

A **Managed Identity** gives your Azure resource (an App Service, for example) an identity of its own in Azure. Azure creates and manages that identity automatically — you never create passwords, certificates or API keys for it.

### The problem without a Managed Identity

The traditional way to give an application access to a Key Vault is to create an **App Registration** in Azure and store its `client_id` and `client_secret` in environment variables:

```
❌ WITHOUT A MANAGED IDENTITY:

App Service                        Key Vault
──────────────────────────────     ───────────────
AZURE_CLIENT_ID = "abc-123"   ──→  "Who are you?"
AZURE_CLIENT_SECRET = "xyz"   ──→  "Are you allowed?"

Problem: reading a secret from the Key Vault needs
another secret (the client_secret). Where is that stored?
In an environment variable — which is one more secret to manage.
```

That is a vicious circle. A Managed Identity breaks it:

```
✅ WITH A MANAGED IDENTITY:

App Service                        Key Vault
──────────────────────────────     ───────────────
(Managed Identity enabled)    ──→  "Who are you?"
                                   "I am app-myapi,
                                    Azure vouches for it."
                              ──→  "Are you allowed?"
                                   "Checking RBAC..."
                              ←──  The secret is returned

No passwords, no API keys. Azure handles the authentication.
```

> **The core idea:** Azure knows that a particular App Service instance is what it claims to be — just as a company's access-control system knows whose badge is whose. You never say a password; the badge itself is the proof.

> **Not only for Key Vault:** the examples on this page use Key Vault, but the same identity works directly against many other services — Storage, Service Bus and **Azure Database for PostgreSQL** ([Entra authentication](Azure-Database-PostgreSQL.md#microsoft-entra-authentication--connecting-without-a-password)) among them. At its best no secret is needed at all, because the connection itself is identity-based.

### Vocabulary: Entra ID, tenant, service principal and the identifiers

| Term | What it is |
|------|------------|
| **Microsoft Entra ID** | Azure's identity service (formerly *Azure Active Directory*, Azure AD). Every user, application and managed identity is an object in Entra ID, and every Azure token is signed by Entra ID |
| **Tenant** | One Entra ID directory: an organisation's users and applications. Identified by `tenantId` (a GUID). A subscription always belongs to one tenant; a signed-in user can be a guest in several |
| **User** | A human. Identifiers: the **UPN** (*user principal name*, `firstname.lastname@edu.xamk.fi`) and the **objectId**. A guest from another tenant has a UPN of the form `name_domain.com#EXT#@tenant.onmicrosoft.com` |
| **Service principal** | An application's identity in a tenant — "a user account for a program". **A managed identity is a service principal whose secret Azure manages for you** |
| **objectId / principalId** | The object's unique identifier in Entra ID. RBAC roles are bound to it. A managed identity's `principalId` is the same thing |
| **clientId / appId** | An application's public identifier, used to *sign in* (for example the OIDC pipeline's `AZURE_CLIENT_ID`). Not a secret — but a different GUID from the objectId |

Three GUIDs are easy to mix up: `tenantId` says *in which directory*, `clientId` *which application signs in*, `objectId`/`principalId` *which object the permission is granted to*. A role is always granted to an objectId.

---

## Three steps in practice

Adopting a Managed Identity always consists of three clear steps:

```
STEP 1                     STEP 2                     STEP 3
─────────────────────      ─────────────────────      ─────────────────────
Enable the identity        Grant permissions          Use it in code

The App Service gets       The Key Vault allows        The .NET code reads
its own identifier         the App Service to          the secret with the
in Azure.                  read secrets.               DefaultAzureCredential
                                                       class.
az webapp                  az role assignment          new SecretClient(
  identity assign            create                      uri,
                               --role                    new DefaultAzureCredential()
                               "Key Vault              )
                               Secrets User"
```

All three steps are required — without any one of them the application cannot read secrets.

---

## Step 1 — Enable the Managed Identity

In this step the App Service gets an identity of its own in Azure. The result is an **Object ID** (also known as the Principal ID) — a unique identifier that the next step uses to grant permissions.

### Option A: Azure CLI

```bash
# Enable a system-assigned Managed Identity
az webapp identity assign \
  --resource-group $RG \
  --name $APP
```

The command prints a JSON response with the created identity:

```json
{
  "principalId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "tenantId": "...",
  "type": "SystemAssigned"
}
```

`principalId` is the unique identifier of the App Service's identity. Keep it — you need it in step 2.

```bash
# Store the principalId in a variable for later
$IDENTITY_ID = az webapp identity show \
  --resource-group $RG \
  --name $APP \
  --query principalId \
  --output tsv

# Print it to check
Write-Output "Identity ID: $IDENTITY_ID"
```

### Option B: Azure Portal

1. Open the **App Service** in the Portal
2. Left menu: **Settings** → **Identity**
3. On the **System assigned** tab switch **Status** → **On**
4. Click **Save** and confirm the dialog
5. An **Object (principal) ID** appears on the page — copy it

---

## Step 2 — Grant RBAC permissions

The Managed Identity now exists, but it has no rights to anything yet. Rights are granted with **RBAC** (Role-Based Access Control).

### What is RBAC?

RBAC is Azure's way of managing access with roles. Instead of giving someone "access to everything", you grant a precise role on a specific resource:

```
Who may do what, where:
──────────────────────────────────────────────────────────
  WHO             ROLE                     WHERE
  ─────           ─────────────────────    ─────────────
  App Service  →  Key Vault Secrets User → Vault: my-kv
  App Service  →  Storage Blob Data Reader→ Storage: myfiles
  Developer    →  Contributor             → Resource group: rg-dev
```

### Roles for using Key Vault

| Role | What it allows | When to use it |
|------|----------------|----------------|
| **Key Vault Secrets User** | Read secrets | A production application — enough almost always |
| **Key Vault Secrets Officer** | Read, create, update and delete | An application that also stores secrets |
| **Key Vault Reader** | Read metadata — **not** secret values | Audit tooling |
| **Key Vault Administrator** | Everything | Administrators only |

> **The key principle — least privilege:** always grant the **smallest possible permission**. If the application only reads secrets, give it `Key Vault Secrets User` — nothing more. If the identity is stolen or misused, the damage stays minimal.

### Option A: Azure CLI

```bash
# 1. Get the Key Vault's unique resource id
$KV_ID = az keyvault show \
  --name $KV_NAME \
  --query id \
  --output tsv

# 2. Grant the Key Vault Secrets User role to the App Service's identity
az role assignment create \
  --assignee-object-id $IDENTITY_ID \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

`--scope $KV_ID` means: the right is granted **on this Key Vault only**, not on other resources. `--assignee-object-id` + `--assignee-principal-type` state the type directly, so the command needs no Graph lookup (see below).

### Option B: Azure Portal

1. Open the **Key Vault** in the Portal
2. Left menu: **Access control (IAM)**
3. Click **+ Add** → **Add role assignment**
4. On the **Role** tab:
   - Search for `Key Vault Secrets User`
   - Select it from the list → click **Next**
5. On the **Members** tab:
   - **Assign access to**: choose **Managed identity**
   - Click **+ Select members**
   - **Subscription**: choose your subscription
   - **Managed identity**: choose **App Service**
   - Pick your App Service from the list → **Select**
6. Click **Review + assign** → **Review + assign**

> **Note:** a role change does not take effect immediately. Wait **1–6 minutes** before testing the application (in the course's test run the Key Vault data plane accepted the role after about six minutes).

### A role assignment: who, which role, where — and the two planes

A **role assignment** is always a triple: a *principal* (objectId) + a *role definition* (for example `Key Vault Secrets User`) + a *scope* (a resource, a resource group or a subscription). Scope **inherits downwards**: an Owner at subscription level is an Owner in every resource group and resource too — which is why `az role assignment list --resource-group` shows neither subscription-level roles nor roles assigned on a single vault; the full picture comes from `az role assignment list --all` with a scope filter.

Roles live on two planes:

| Plane | What it controls | Example roles | Note |
|-------|------------------|---------------|------|
| **Control plane** | The resources themselves: creation, settings, deletion — `management.azure.com` | Owner, Contributor, Reader | A Contributor can create a Key Vault but **cannot** grant roles (no `roleAssignments/write`) and cannot read secrets |
| **Data plane** | The resource's *contents*: a secret's value, a blob's bytes, a database's rows — the resource's own endpoint | Key Vault Secrets User/Officer, Storage Blob Data Contributor | **An Owner does not automatically reach the data** — the subscription owner gets `Forbidden` when reading a secret until they hold a data-plane role |

This is the course's recurring pattern: the pipeline identity is a Contributor and builds everything, but granting roles and data-plane access is a separate **access session** done by a human with the Owner or *User Access Administrator* role.

**The CLI form that always works.** `--assignee <guid>` first asks the Graph API whether the GUID is a user or an application — and fails when the signed-in account lacks Graph access (pipelines, guest tenants). State the type yourself:

```bash
az role assignment create \
  --assignee-object-id $IDENTITY_ID \
  --assignee-principal-type ServicePrincipal \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

For a user, `--assignee-principal-type User`. The same line works in a script, in a pipeline and instead of the Portal.

---

## Step 3 — DefaultAzureCredential in code

Once the identity is enabled and the permissions granted, code can read secrets. This is done with the `DefaultAzureCredential` class from the `Azure.Identity` package.

### What does DefaultAzureCredential do?

`DefaultAzureCredential` is a clever class that **works out how to authenticate** based on the environment:

```
In Azure (App Service):
  → Uses the Managed Identity automatically ✅

On a development machine:
  → Uses your az login session ✅

In both cases the code is exactly the same.
```

This means you write the code once — and never change it between the development machine and production.

### NuGet packages

```bash
dotnet add package Azure.Identity
dotnet add package Azure.Security.KeyVault.Secrets
```

### Basic example — reading a secret

```csharp
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;

var client = new SecretClient(
    vaultUri: new Uri("https://my-keyvault.vault.azure.net/"),
    credential: new DefaultAzureCredential());

// Read a secret by name
KeyVaultSecret secret = await client.GetSecretAsync("weather-api-secret");

// secret.Value.Value holds the secret's value
Console.WriteLine(secret.Value.Value);
```

### In an ASP.NET Core application (IOptions + DI)

Register the `SecretClient` once in `Program.cs`, so it can be injected anywhere:

```csharp
// Program.cs
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using WeatherApi;

var builder = WebApplication.CreateBuilder(args);

// The Key Vault URL comes from configuration (User Secrets in development,
// App Service Application Settings in production)
builder.Services.Configure<KeyVaultOptions>(
    builder.Configuration.GetSection(KeyVaultOptions.SectionName));

// Register the SecretClient — created once, shared by everyone
builder.Services.AddSingleton(serviceProvider =>
{
    var options = serviceProvider
        .GetRequiredService<IOptions<KeyVaultOptions>>().Value;

    if (string.IsNullOrEmpty(options.VaultUrl))
        throw new InvalidOperationException("KeyVault:VaultUrl is not set.");

    return new SecretClient(
        new Uri(options.VaultUrl),
        new DefaultAzureCredential());
});
```

```csharp
// Controller or service — inject the SecretClient directly
[ApiController]
[Route("[controller]")]
public class KeyVaultController : ControllerBase
{
    private readonly SecretClient _secretClient;

    public KeyVaultController(SecretClient secretClient)
    {
        _secretClient = secretClient;
    }

    [HttpGet("secret")]
    public async Task<IActionResult> GetSecret()
    {
        var secret = await _secretClient.GetSecretAsync("weather-api-secret");

        return Ok(new
        {
            Source = "Azure Key Vault",
            SecretName = secret.Value.Name,
            ValuePreview = secret.Value.Value[..4] + "***",
            Version = secret.Value.Properties.Version
        });
    }
}
```

---

## Local development

A development machine has no Managed Identity — but `DefaultAzureCredential` can use your **Azure CLI sign-in** instead. The same code works without changes.

### 1. Sign in with the Azure CLI

```bash
az login
# Pick the right subscription if you have several
az account set --subscription "<your subscription name or id>"
```

### 2. Grant yourself Key Vault permissions

On the development machine *you* are the "identity" that reads secrets — you need the same role that the App Service has been granted in Azure.

```bash
# Get the Object ID of your own Azure account
$MY_ID = az ad signed-in-user show --query id --output tsv

# Grant yourself the Key Vault Secrets User role
az role assignment create \
  --assignee-object-id $MY_ID \
  --assignee-principal-type User \
  --role "Key Vault Secrets User" \
  --scope $KV_ID
```

> **Several tenants?** `az ad signed-in-user show` answers from the CLI's *default tenant*. If the subscription lives in another tenant (for example a personal account as a guest), get the objectId from Graph with the subscription's token, or from the Portal (Entra ID → Users → your account → Object ID).

### 3. Put the Key Vault URL in User Secrets

On the development machine the Key Vault URL comes from User Secrets; in Azure it comes from Application Settings:

```bash
dotnet user-secrets set "KeyVault:VaultUrl" "https://my-keyvault.vault.azure.net/"
```

Now `DefaultAzureCredential` works automatically:

```
Development machine:   DefaultAzureCredential → az login identity    → Key Vault
Azure:                 DefaultAzureCredential → Managed Identity     → Key Vault
```

> **Why is this neat?** You do not maintain two code paths — development and production use exactly the same code. The environment decides the authentication method automatically.

---

## How does it work under the hood?

This section explains what happens behind the scenes. **It is not required reading** — you can use Managed Identity without it — but it helps you understand why the solution is secure.

### Token-based authentication

A Managed Identity is built on short-lived **access tokens**. A token is a digitally signed proof of who you are and what you may do — like a digital access pass.

```
What happens when code calls GetSecretAsync():

  1. DefaultAzureCredential notices it is running in Azure App Service

  2. It requests an access token from Azure's internal service
     (the Azure Instance Metadata Service)

  3. Azure returns a short-lived token (valid ~1 hour)
     The token says, among other things: "I am App Service X, tenant Y"

  4. SecretClient sends the request to the Key Vault with the token

  5. The Key Vault verifies the token (Azure signed it)
     and checks RBAC: "Does this identity hold the Key Vault Secrets User role?"

  6. All good → the secret is returned
     No permission → 403 Forbidden

  7. DefaultAzureCredential renews the token automatically before it expires
```

**Why this is safer than a password:**
- A token has a short lifetime — even if it leaks, it expires soon
- The token is not stored anywhere — it is fetched when needed
- Azure signs the token — it cannot be forged

### The DefaultAzureCredential authentication chain

`DefaultAzureCredential` walks the following list in order and uses the first method that works:

```
Order        Method                       When it kicks in
─────────    ────────────────────────     ────────────────────────────────
1.           EnvironmentCredential        When AZURE_CLIENT_ID etc. are set
2.           WorkloadIdentityCredential   Kubernetes environments
3.           ManagedIdentityCredential    ← Azure App Service, VM, Functions
4.           SharedTokenCacheCredential   Visual Studio (Windows)
5.           VisualStudioCodeCredential   VS Code Azure extension
6.           AzureCliCredential           ← az login (development machine)
7.           AzurePowerShellCredential    Connect-AzAccount
8.           AzureDeveloperCliCredential  azd login
             ─────────────────────────────────────────────────────────────
             If none succeeds → AuthenticationFailedException
```

In practice the ones that matter to you are **number 3** (production in Azure) and **number 6** (the development machine).

---

## System-assigned vs. User-assigned

There are two kinds of Managed Identity. For a beginner **System-assigned is the right choice** — it is simpler and enough for most situations.

### System-assigned (recommended for beginners)

The identity is tied to one resource and deleted automatically when the resource is deleted.

```
┌──────────────────────────────────┐
│  App Service: my-weatherapi      │
│                                  │
│  System-assigned identity:       │
│  Object ID: a1b2c3d4-e5f6-...   │
│                                  │
│  ✅ Created automatically        │
│  ✅ Deleted with the resource    │
│  ✅ No separate resources        │
└──────────────────────────────────┘
```

**Use it when:** one application needs access to certain resources. That covers most situations.

### User-assigned (more advanced)

The identity is an independent Azure resource that can be attached to several applications.

```
┌─────────────────────────────┐
│  Managed Identity: mi-myapp │  ← An independent resource
│  Object ID: f1e2d3c4-...    │
└──────────┬──────────────────┘
           │ attached to both
    ┌──────▼──────┐    ┌──────────────┐
    │  App Service│    │  Function App│
    │  my-api     │    │  my-worker   │
    └─────────────┘    └──────────────┘
```

**Use it when:** several different applications need exactly the same rights to the same resources. The rights do not have to be granted separately to each one.

| | System-assigned | User-assigned |
|-|-----------------|---------------|
| **Lifecycle** | Tied to the resource | Independent |
| **Sharing** | No — one per resource | Yes — across several resources |
| **Complexity** | Simple | More complex |
| **Recommendation** | Beginners, simple projects | When the identity is shared |

---

## Best practices

### ✅ Do

- **Use a System-assigned Managed Identity** for simple projects — easy to enable and cleaned up automatically
- **Grant the smallest possible permission** — `Key Vault Secrets User` is enough for reading; do not grant `Key Vault Administrator`
- **Test locally with `az login`** before shipping the code to Azure — it confirms that DefaultAzureCredential and the RBAC permissions work
- **Use `DefaultAzureCredential`** — the same code works on the development machine and in production without changes
- **Keep the Key Vault URL in configuration** (User Secrets in development, Application Settings in Azure) — do not hard-code it

### ❌ Avoid

- Do not store `client_id` + `client_secret` pairs in environment variables for Key Vault access — Managed Identity exists for exactly this
- Do not grant broad roles such as `Owner` or `Contributor` to an application — limit the rights to exactly the resource that is needed
- Do not forget to wait 1–6 minutes after RBAC changes before testing

---

## Next

- [Azure Key Vault](Key-Vault.md) — The Key Vault service and its concepts
- [Azure App Service](../../Azure/App-Service.md) *(in Finnish)* — Hosting .NET applications in Azure
- [Azure Key Vault .NET integration](../../../C%23/fin/04-Advanced/Secrets-Management/Azure-Key-Vault.md) *(in Finnish)* — Code examples for Key Vault + Managed Identity

## Back

- [Azure services](README.md)
