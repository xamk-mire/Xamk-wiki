# CI/CD — Continuous Integration and Delivery
> 🇫🇮 Finnish version: [CI-CD.md](../CI-CD.md)

## Table of Contents

1. [Introduction](#introduction)
2. [What is CI?](#what-is-ci)
3. [What is CD?](#what-is-cd)
4. [The CI/CD pipeline](#the-cicd-pipeline)
5. [GitHub Actions](#github-actions)
6. [Practical example: .NET CI/CD](#practical-example-net-cicd)
7. [Secrets and environment variables](#secrets-and-environment-variables)
8. [Logging in to Azure from the pipeline: OIDC](#logging-in-to-azure-from-the-pipeline-oidc)
9. [Quality gates and branch protection](#quality-gates-and-branch-protection)
10. [Failure notifications](#failure-notifications)
11. [Best practices](#best-practices)
12. [Summary](#summary)

---

## Introduction

**CI/CD** (Continuous Integration / Continuous Delivery) is a set of practices whose purpose is to automate building, testing and releasing code. It removes manual work and reduces the risk of human error.

**The basic idea:**

```
Without CI/CD:
1. The developer writes code
2. The developer maybe remembers to run the tests
3. The developer builds the application by hand
4. The developer copies the files to the server over FTP
5. Something breaks — nobody knows at which step
6. Finding the error takes hours

With CI/CD:
1. The developer pushes the code to GitHub
2. An automated pipeline:
   ✅ Builds the application
   ✅ Runs the tests
   ✅ Releases to production
3. If any step fails → immediate notification
```

---

## What is CI?

**Continuous Integration** means that developers' code changes are merged into the main branch often (daily or more), and every merge triggers an automated build and test process.

### The CI stages

```
The developer pushes code
        │
        ▼
┌──────────────────┐
│  1. Build        │  Compile the application (dotnet build)
├──────────────────┤
│  2. Test         │  Run the unit tests (dotnet test)
├──────────────────┤
│  3. Analyze      │  Code quality checks (optional)
└──────────────────┘
        │
        ▼
   ✅ Passed → the code can be integrated
   ❌ Failed → the developer fixes it before anyone else pulls the code
```

### What CI solves

| Problem | CI's solution |
|---------|---------------|
| "Works on my machine" | Built in a clean environment |
| Broken code in the main branch | Tests run automatically before merge |
| Merge-conflict pile-ups | Small, frequent changes |
| Manual testing gets forgotten | Automated tests on every push |

---

## What is CD?

**CD** can mean two things:

### Continuous Delivery

The code is **always in a releasable state**. Releasing to production happens with a manual approval (pressing a button).

```
CI → Build → Test → ✅ → Artifact ready → [Manual approval] → Production
```

### Continuous Deployment

Every successful CI run is released to production automatically — without a manual step in between.

```
CI → Build → Test → ✅ → Automatic release → Production
```

### Comparison

| Property | Continuous Delivery | Continuous Deployment |
|----------|---------------------|-----------------------|
| Production release | Manual approval | Automatic |
| Risk | Lower (a human checks) | Requires very good tests |
| Speed | Faster than manual | The fastest possible |
| Suits | Critical systems | Fast iteration, good test coverage |

---

## The CI/CD pipeline

A **pipeline** is an automated process that runs a series of stages from a code push to a production release.

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Source  │ →  │  Build  │ →  │   Test   │ →  │  Deploy  │ →  │  Prod    │
│  (Git)  │    │ (dotnet │    │ (dotnet  │    │ (Azure)  │    │ (Live)   │
│         │    │  build) │    │  test)   │    │          │    │          │
└─────────┘    └─────────┘    └──────────┘    └──────────┘    └──────────┘
     │              │              │                │
     │              │         ❌ Fail?             │
     │              │         → STOP               │
     │              │         → Notification       │
```

### CI/CD tools

| Tool | Provider | Use |
|------|----------|-----|
| **GitHub Actions** | GitHub | The most common; built into the repository |
| Azure DevOps Pipelines | Microsoft | Enterprise, Azure integration |
| GitLab CI/CD | GitLab | GitLab repositories |
| Jenkins | Open source | Self-hosted, configurable |
| CircleCI | CircleCI | SaaS-based |

This course focuses on **GitHub Actions**.

---

## GitHub Actions

**GitHub Actions** is GitHub's built-in CI/CD platform. Workflow files define what is done and when.

### Concepts

```
Repository
└── .github/
    └── workflows/
        └── ci.yml          ← Workflow file

Workflow (ci.yml)
├── Trigger (when does it run?)    → push, pull_request, schedule
├── Job 1: "build"                  → Runs on an Ubuntu machine
│   ├── Step 1: Checkout code       → actions/checkout@v5
│   ├── Step 2: Setup .NET          → actions/setup-dotnet@v5
│   ├── Step 3: dotnet restore
│   ├── Step 4: dotnet build
│   └── Step 5: dotnet test
└── Job 2: "deploy"                 → Runs after the build job
    ├── Step 1: Download artifact
    └── Step 2: Deploy to Azure
```

| Concept | Explanation |
|---------|-------------|
| **Workflow** | A YAML file in `.github/workflows/` — defines the whole pipeline |
| **Trigger** | The event that starts the workflow (`push`, `pull_request`, `schedule`) |
| **Job** | A set of steps that run on the same machine |
| **Step** | A single action in a job (a command or a ready-made action) |
| **Runner** | The machine that executes the job (provided by GitHub, or your own) |
| **Action** | A reusable component (e.g. `actions/checkout@v5`) |
| **Artifact** | A built file passed between jobs |

### Triggers

```yaml
on:
  push:
    branches: [main]          # Runs on a push to the main branch
  pull_request:
    branches: [main]          # Runs when a PR is opened against main
  schedule:
    - cron: '0 2 * * 1'       # Every Monday at 02:00 UTC
  workflow_dispatch:           # Manual start from GitHub
```

`workflow_dispatch` can take **inputs** (`inputs:` — `boolean`, `choice`, `string`) that appear on the *Run workflow* form and are read as `${{ inputs.name }}`. The form always shows the **default branch's** version of the file — a new checkbox appears only after the merge.

### Reusable workflows: workflow_call, secrets: inherit and concurrency

When the same release chain has to run against several environments, the steps are not copied. A **reusable workflow** (`on: workflow_call`) defines the steps once and takes the differences as `inputs`; a **caller workflow** runs it as a job:

```yaml
# .github/workflows/deploy-env.yml — the steps, once
on:
  workflow_call:
    inputs:
      environment: { type: string, required: true }
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}   # vars./secrets. resolve from THIS environment
    steps: [ ... ]

# .github/workflows/deploy.yml — the caller
jobs:
  dev:
    uses: ./.github/workflows/deploy-env.yml
    with: { environment: dev }
    secrets: inherit                          # the called workflow sees secrets only this way
  test:
    needs: dev
    uses: ./.github/workflows/deploy-env.yml
    with: { environment: test }
    secrets: inherit
```

| Keyword | Meaning |
|---------|---------|
| `uses: ./.github/workflows/x.yml` | The job *is* a call to another workflow; its jobs appear nested |
| `secrets: inherit` | A called workflow sees **no** secrets by default; `inherit` passes every secret of the caller (and of the job's environment). The alternative is listing them by name — more precise when the workflow is shared between repositories |
| `needs:` + `if:` | Order and condition: `if: ${{ !cancelled() && needs.infra.result != 'failure' }}` runs the job even when the previous one was *skipped* on purpose |
| `concurrency: { group: deploy, cancel-in-progress: false }` | Only one run per group at a time; the next one queues (`false`) or cancels the previous (`true`). For deploys, queue — a half-finished release is worse than a wait |

---

## Practical example: .NET CI/CD

### CI — build and tests

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v5

      - name: Setup .NET
        uses: actions/setup-dotnet@v5
        with:
          dotnet-version: '8.0.x'

      - name: Restore dependencies
        run: dotnet restore

      - name: Build
        run: dotnet build --configuration Release --no-restore

      - name: Test
        run: dotnet test --configuration Release --no-build --verbosity normal
```

### CD — deploy to Azure App Service

```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5

      - name: Setup .NET
        uses: actions/setup-dotnet@v5
        with:
          dotnet-version: '8.0.x'

      - name: Build and publish
        run: dotnet publish --configuration Release --output ./publish

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: app
          path: ./publish

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: app

      - name: Deploy to Azure Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: my-app-name
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

> **Note:** a publish profile is a **long-lived secret** — a simple way to start, but the recommended way is **OIDC** (`azure/login@v3` + federated identity), where no password or key is stored in the repository at all. See the [OIDC section](#logging-in-to-azure-from-the-pipeline-oidc) below.

### IaC deploy — Bicep with GitHub Actions

```yaml
# .github/workflows/deploy-infra.yml
name: Deploy Infrastructure

on:
  push:
    branches: [main]
    paths:
      - 'infra/**'

permissions:
  id-token: write   # OIDC token (see the OIDC section below)
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v5

      - name: Azure Login (OIDC — no long-lived secrets)
        uses: azure/login@v3
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: What-if (preview into the log)
        run: |
          az deployment group what-if \
            --resource-group my-resource-group \
            --template-file infra/main.bicep \
            --parameters infra/dev.bicepparam

      - name: Deploy Bicep
        run: |
          az deployment group create \
            --resource-group my-resource-group \
            --template-file infra/main.bicep \
            --parameters infra/dev.bicepparam
```

---

### Expand-contract: a risky change in two PRs

When a change touches both infrastructure and code (a new authentication method, a new column, a new dependency), one big PR is dangerous: if the second half fails, the first is already in production. **Expand-contract** splits the change into phases, each of which is safe on its own:

| Phase | What you do | Principle |
|-------|-------------|-----------|
| **Expand** | Add the new next to the old without breaking it: managed identity *and* password, a nullable column, Key Vault *and* the old app setting | The old code keeps working; what-if shows only `+` and `~` |
| **Cutover** | Switch the code to the new path | The first PR whose smoke test can reveal a gap — and at that point the old path still exists |
| **Contract** | Remove the old: the password, the old column, the old setting | Only once the new is proven in use; `-` rows in what-if |

The same rhythm applies to database migrations (add nullable → backfill → tighten) and to API versioning (new field alongside → clients move → old one removed). For the pipeline the benefit is that every PR can be reverted on its own.

## Secrets and environment variables

### GitHub Actions Secrets

Sensitive values (API keys, passwords, connection strings) are stored in **GitHub Secrets**, from where workflows can use them.

```
GitHub → Repository → Settings → Secrets and variables → Actions → New repository secret
```

```yaml
# Using a secret in a workflow
steps:
  - name: Deploy
    env:
      CONNECTION_STRING: ${{ secrets.DB_CONNECTION_STRING }}
    run: echo "Deploying with secret..."
```

**Rules:**
- Secrets do not appear in logs (GitHub masks them automatically)
- Secrets cannot be read back — only overwritten
- Secrets are per repository (or per organisation)

### Environment variables

```yaml
env:
  DOTNET_VERSION: '8.0.x'
  CONFIGURATION: Release

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: dotnet build --configuration ${{ env.CONFIGURATION }}
```

### GitHub Environments: variables, secrets and approval

Repository-level secrets and variables are the same for every run. A **GitHub Environment** (Settings → Environments) is a named target — `dev`, `test`, `production` — with **its own** variables and secrets *under the same names* and its own protection rules:

```yaml
jobs:
  deploy:
    environment: test                        # ← without this line vars.RESOURCE_GROUP is empty
    env:
      RESOURCE_GROUP: ${{ vars.RESOURCE_GROUP }}   # the test environment's value
```

| Topic | Repository level | Environment level |
|-------|------------------|-------------------|
| Variables (`vars.X`) | One value for everyone | The same *name*, a different value per environment — the YAML does not know which environment it deploys to |
| Secrets (`secrets.X`) | Available at once | Released to the job only after the environment's **protection rules** have passed |
| Protection rules | — | *Required reviewers* (the run stops at *Waiting for review*), branch restrictions, a wait timer — Continuous Delivery with one setting |
| OIDC subject | `…:ref:refs/heads/main` | `…:environment:<name>` — every environment needs its own federated credential ([subject format](#githubs-subject-format--mind-the-ids)) |

The most common mistake: the variable was created at repository level, or the job lacks `environment:` — then `vars.X` is empty and the command fails on a missing parameter.

---

## Logging in to Azure from the pipeline: OIDC

The pipeline needs permissions in Azure. The worst way is to store a **long-lived secret** (a service principal password or a publish profile) in GitHub Secrets: it does not expire, it must be rotated by hand, and if it leaks it works from anywhere.

**OIDC (OpenID Connect) / federated identity** removes the problem: GitHub Actions proves its identity to Azure with a **short-lived token**, which Azure exchanges for access. No password is stored in the repository — only three *identifiers* (client id, tenant id, subscription id), which are not secrets even though they are stored in the secrets section.

```
Long-lived secret (❌):                   OIDC / federated identity (✅):

GitHub Secrets:                          GitHub Secrets:
  AZURE_CREDENTIALS = {                    AZURE_CLIENT_ID       = <guid>
    "clientSecret": "a real password       AZURE_TENANT_ID       = <guid>
     that works everywhere and             AZURE_SUBSCRIPTION_ID = <guid>
     forever" }                            (identifiers, not secrets)
        │                                      │
        ▼                                      ▼
  Leaks → the attacker has                The workflow gets a one-time token
  permanent access to Azure               that is valid ONLY from this repo,
                                          ONLY from the configured branch
```

### Which identity for the pipeline?

On the Azure side the pipeline needs an identity to which the trust (federated credential) and the permissions are attached. There are two options:

| Identity | Created with | Who may create it | When |
|---|---|---|---|
| **User-assigned managed identity** | `az identity create` in the resource group | Anyone with Contributor on the subscription | The default for a student and for most projects — no Entra ID permissions needed, deleted together with the resource group |
| **App registration** | `az ad app create` in the Entra ID directory | Only if the organisation allows it (in a school tenant an ordinary user **may not**) | When the same identity serves several subscriptions or needs API permissions |

Granting the role (step 2 below) requires the **Owner** role on the subscription (or User Access Administrator) in both cases. Azure for Students grants it.

### GitHub's subject format — mind the IDs

The federated credential is bound to the `subject` value of GitHub's token. **In repositories created after July 2026** the subject includes the numeric IDs of the owner and the repository:

```
repo:<owner>@<owner-id>/<repo>@<repo-id>:ref:refs/heads/main      # push to the main branch
repo:<owner>@<owner-id>/<repo>@<repo-id>:pull_request              # pull request runs
repo:<owner>@<owner-id>/<repo>@<repo-id>:environment:production    # a job with an environment:
```

The old format `repo:<owner>/<repo>:…` (which most guides still show) **does not match** a new repository's token — the login fails with `AADSTS700213`. Get your own repository's prefix with the GitHub CLI:

```powershell
$Prefix = gh api repos/<owner>/<repo>/actions/oidc/customization/sub --jq .sub_claim_prefix
# → repo:<owner>@12345678/<repo>@987654321
```

### Setup (Azure CLI, managed identity)

```powershell
# 1. An identity in the resource group
az identity create --name id-github-myapp --resource-group <rg-name>
$ClientId    = az identity show --name id-github-myapp --resource-group <rg-name> --query clientId --output tsv
$PrincipalId = az identity show --name id-github-myapp --resource-group <rg-name> --query principalId --output tsv

# 2. Permissions: Contributor ONLY on your own resource group (least privilege)
az role assignment create `
  --assignee-object-id $PrincipalId `
  --assignee-principal-type ServicePrincipal `
  --role Contributor `
  --scope "/subscriptions/<sub-id>/resourceGroups/<rg-name>"

# 3. Federated credential: trust EXACTLY this repository and branch
az identity federated-credential create `
  --name github-main `
  --identity-name id-github-myapp `
  --resource-group <rg-name> `
  --issuer "https://token.actions.githubusercontent.com" `
  --subject "${Prefix}:ref:refs/heads/main" `
  --audiences "api://AzureADTokenExchange"
```

Store `AZURE_CLIENT_ID` = `$ClientId`, `AZURE_TENANT_ID` and `AZURE_SUBSCRIPTION_ID` (`az account show`) in GitHub Secrets.

<details>
<summary>The same with an app registration</summary>

```powershell
$AppId = az ad app create --display-name "gh-myapp-deploy" --query appId --output tsv
az ad sp create --id $AppId
az role assignment create --assignee $AppId --role Contributor --scope "/subscriptions/<sub-id>/resourceGroups/<rg-name>"

# Parameters from a file — multi-line JSON on the command line breaks in Windows PowerShell
@{ name = "github-main"; issuer = "https://token.actions.githubusercontent.com"; subject = "${Prefix}:ref:refs/heads/main"; audiences = @("api://AzureADTokenExchange") } | ConvertTo-Json | Set-Content fc.json
az ad app federated-credential create --id $AppId --parameters fc.json
```

In that case the `AZURE_CLIENT_ID` secret holds `$AppId`.

</details>

The `subject` field is the core of the security: the token is accepted only when the workflow runs from exactly this repository and this branch. Another repository's (or a fork's) workflow gets no access even if the identifiers leak. Every different context (pull request, environment) needs its own credential — one identity can carry several.

### Use in a workflow

```yaml
permissions:
  id-token: write   # without this no OIDC token is issued
  contents: read

steps:
  - name: Azure Login
    uses: azure/login@v3
    with:
      client-id: ${{ secrets.AZURE_CLIENT_ID }}
      tenant-id: ${{ secrets.AZURE_TENANT_ID }}
      subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

---

## Quality gates and branch protection

CI checks are useless if they can be bypassed. **Branch protection** makes the checks mandatory: the main branch can only be reached through a pull request, and the PR does not merge until every gate is green.

```
Developer ──► feature branch ──► Pull Request ──► main ──► automatic deploy
                                     │
                           ┌─────────┴──────────┐
                           │  QUALITY GATES      │
                           │  ✅ Build           │
                           │  ✅ Tests           │
                           │  ✅ Lint/format     │
                           │  ✅ Review          │
                           │     (human/AI)      │
                           └────────────────────┘
                           All green → merge allowed
                           One red → merge blocked
```

### Setting it up in GitHub

`Repository → Settings → Branches → Add branch protection rule`:

| Setting | Effect |
|---------|--------|
| **Require a pull request before merging** | No direct pushes to main |
| **Require status checks to pass** | The selected CI jobs (e.g. `build-and-test`) are mandatory |
| **Require branches to be up to date** | The PR is tested against the latest main |
| **Do not allow bypassing the above settings** | The rules apply to admins (you) as well |

> **Note:** in private repositories branch protection requires the GitHub Pro tier (students get it from the [GitHub Student Developer Pack](https://education.github.com/pack)). In public repositories it is free.

### AI review as a gate

Alongside human review (or, in a study project, instead of it) you can attach **AI code review** — e.g. GitHub Copilot code review — which comments on the PR's changes automatically. AI review finds mechanical problems (suspected bugs, naming, forgotten error handling) but **does not understand context**: its remarks are suggestions that a human accepts or rejects with a reason. Good practice: react to every AI comment — either a fix or a short justification for not fixing.

### The supply-chain gate: vulnerable packages and Dependabot

The **software supply chain** is all the code you did not write but that ends up in your release: NuGet packages, their **transitive dependencies** (packages your packages need — you never typed their names) and the actions in your workflows. A vulnerability in them is your vulnerability.

```yaml
- name: Vulnerable packages (supply-chain gate)
  run: |
    dotnet list package --vulnerable --include-transitive | tee vulnerable.txt
    if grep -q "has the following vulnerable packages" vulnerable.txt; then
      echo "::error::Vulnerable packages found — update them before merging."
      exit 1
    fi
```

| Piece | Meaning |
|-------|---------|
| `--vulnerable` | Compares the packages against the **GitHub Advisory Database** (the same source Dependabot uses) |
| `--include-transitive` | Without it only direct packages are checked; the dangerous ones are the ones you never saw |
| `grep` + `exit 1` | The command's exit code varies between SDK versions, the text does not — a gate must fail deterministically |
| NuGetAudit `NU1901`–`NU1904` | The same data already at `dotnet restore` as warnings: NU1901 low, NU1902 moderate, NU1903 high, NU1904 critical. A warning does not fail the build; the gate does |
| `NU1605` | A different thing: a *package downgrade* — two dependencies demand different versions and restore fails before the gate is reached |

**Dependabot** is the gate's partner: `.github/dependabot.yml` lists the ecosystems (`nuget`, `github-actions`, …) and a schedule, and GitHub opens **update PRs** automatically — the first ones within minutes of the file being merged, then on schedule (`open-pull-requests-limit` caps how many are open). *Version updates* bump versions in general; *security updates* (Settings → Code security) open a PR only because of a vulnerability. Every PR goes through the same gates — but green means "it builds and the tests pass", not "nothing changed": a **major-version** bump (SemVer `6.x → 10.x`) can carry breaking changes the tests do not cover. The bot proposes, a human merges.

---

## Failure notifications

An automated pipeline without notifications is dangerous: a broken deployment can go unnoticed for days. The minimum is an **e-mail notification for a failed workflow run**:

1. GitHub → your profile → **Settings → Notifications → Actions**
2. Choose **Only notify for failed workflows**

After this every red run on main produces an e-mail — including a failed deploy step or a failed post-deployment **smoke test**. A smoke test (e.g. `curl /health` after the deploy) should always be the last step of the pipeline: it turns "the deploy went through" into "the application actually answers".

---

## Best practices

### 1. Run CI on every pull request

```yaml
on:
  pull_request:
    branches: [main]
```

A PR must not be mergeable until CI is green.

### 2. Keep pipelines fast

- Cache dependencies
- Run only the relevant tests in a PR, all tests on merge

```yaml
- name: Cache NuGet packages
  uses: actions/cache@v5
  with:
    path: ~/.nuget/packages
    key: ${{ runner.os }}-nuget-${{ hashFiles('**/*.csproj') }}
```

### 3. Separate build and deploy

```yaml
jobs:
  build:    # Always built
    ...
  deploy:   # Released only from the main branch
    needs: build
    if: github.ref == 'refs/heads/main'
```

### 4. Never store secrets in code

```yaml
# ✅ From GitHub Secrets
${{ secrets.API_KEY }}

# ❌ In code or YAML
API_KEY: "sk-1234567890abcdef"
```

### 5. Use versioned actions

```yaml
# ✅ Pinned version — safe and repeatable
uses: actions/checkout@v5

# ❌ Refers to a branch — can change
uses: actions/checkout@main
```

---

## Summary

| Concept | Explanation |
|---------|-------------|
| **CI** | Continuous Integration — automatic build + tests on every push |
| **CD** | Continuous Delivery/Deployment — automatic release to production |
| **Pipeline** | The automated process: Source → Build → Test → Deploy |
| **GitHub Actions** | GitHub's built-in CI/CD platform |
| **Workflow** | The YAML file that defines the pipeline |
| **Trigger** | The event that starts the workflow (push, PR, schedule) |
| **Job** | A set of steps on the same runner |
| **Step** | A single action (a command or an action) |
| **Runner** | The machine that executes the job |
| **Action** | A reusable component |
| **Secrets** | Sensitive values in GitHub — never shown in logs |
| **Artifact** | A built file passed between jobs |

**Remember:**
- CI/CD **automates** the build, test and release process
- **CI** makes sure broken code never reaches the main branch
- **CD** gets working code to production quickly and safely
- **GitHub Actions** is the most common tool in GitHub projects
- **Secrets** go in GitHub's Secrets section — never in code

---

## Useful links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions: Quickstart](https://docs.github.com/en/actions/quickstart)
- [Microsoft: Deploy to Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions)
- [Azure App Service (wiki, in Finnish)](../../Cloud%20technologies/Azure/App-Service.md)
- [Infrastructure as Code (wiki)](../../Cloud%20technologies/eng/Azure/Infrastructure-as-Code.md)
- [Azure Monitor and Application Insights (wiki)](../../Cloud%20technologies/eng/Azure/Monitoring-and-Application-Insights.md)
