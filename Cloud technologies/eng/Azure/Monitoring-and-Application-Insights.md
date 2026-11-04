# Azure Monitor and Application Insights — seeing inside your application
> 🇫🇮 Finnish version: [Monitoring-and-Application-Insights.md](../../Azure/Monitoring-and-Application-Insights.md)

## Table of Contents

1. [What is observability?](#what-is-observability)
2. [The Azure Monitor family](#the-azure-monitor-family)
3. [Application Insights](#application-insights)
4. [Setting it up in a .NET application](#setting-it-up-in-a-net-application)
5. [Good logging practices](#good-logging-practices)
6. [KQL — asking the telemetry questions](#kql--asking-the-telemetry-questions)
7. [Alerts and Action Groups](#alerts-and-action-groups)
8. [Availability tests](#availability-tests)
9. [Costs](#costs)
10. [Best practices](#best-practices)

---

## What is observability?

**Observability** is the ability to infer the internal state of a system from the data it produces — without adding new code for every fault you want to investigate. It rests on three pillars:

| Pillar | What it is | Example | Answers the question |
|--------|------------|---------|----------------------|
| **Logs** | Timestamped events, as text or structured records | "Registration created for event X" | *What happened?* |
| **Metrics** | Numeric time series | Response time, request count, 5xx errors per minute | *How much and how fast?* |
| **Traces** | The full path of one request through services and dependencies | HTTP request → API → PostgreSQL query | *Where in the chain is the problem?* |

```
Without observability:                With observability:

User: "The page is broken!"           Alert e-mail at 14:02
You: "Hmm, works on my machine..."    → Failures view: 500s started at 14:00
→ guessing, ssh, print debugging      → Exception: "connection refused (postgres)"
→ hours                               → Root cause in minutes: the database is down
```

---

## The Azure Monitor family

**Azure Monitor** is the umbrella term for Azure's monitoring services. Its parts fit together like this:

```
┌───────────────────────────────────────────────────────────────┐
│  AZURE MONITOR (umbrella term)                                │
│                                                               │
│  Data sources:               Store:                Use:       │
│  ┌─────────────────┐    ┌──────────────────┐   ┌───────────┐ │
│  │ Application      │    │                  │   │ KQL       │ │
│  │ (App Insights    │───►│  Log Analytics   │──►│ queries   │ │
│  │  SDK)            │    │  Workspace       │   ├───────────┤ │
│  ├─────────────────┤    │                  │   │ Dashboard │ │
│  │ Azure resources  │───►│  (all data in    │   │ Workbook  │ │
│  │ (platform        │    │   one place)     │   ├───────────┤ │
│  │  metrics, e.g.   │    │                  │──►│ Alerts    │ │
│  │  Http5xx)        │    │                  │   │ + Action  │ │
│  └─────────────────┘    └──────────────────┘   │   Groups  │ │
│                                                 └───────────┘ │
└───────────────────────────────────────────────────────────────┘
```

| Service | Role |
|---------|------|
| **Log Analytics Workspace** | The central store for all log and telemetry data; the target of KQL queries |
| **Application Insights** | Application-level telemetry (requests, dependencies, exceptions) — stored in Log Analytics |
| **Platform metrics** | Collected automatically from every Azure resource (e.g. App Service `Http5xx`, CPU) — free |
| **Alerts + Action Groups** | A rule ("5xx > 0") plus a reaction ("send an e-mail") |

---

## Application Insights

**Application Insights** is the application-monitoring part (APM) of Azure Monitor. Once the App Insights SDK is added to a .NET application it collects, **automatically**:

| Telemetry type | What is collected | Table in KQL |
|----------------|-------------------|--------------|
| **Requests** | Every HTTP request: path, duration, status code | `requests` |
| **Dependencies** | Outgoing calls: database queries, HTTP calls to other services | `dependencies` |
| **Exceptions** | Unhandled exceptions with their stack traces | `exceptions` |
| **Traces** | `ILogger` log lines | `traces` |
| **Custom events** | Events you send yourself (`TelemetryClient.TrackEvent`) | `customEvents` |

The most important feature is **correlation**: under a single HTTP request you see the database queries, log lines and exceptions it caused, as one tree (the end-to-end transaction). Troubleshooting starts from the request that failed, not from guesswork.

### Key views in the Portal

| View | Use |
|------|-----|
| **Live Metrics** | Real-time traffic (one-second latency) — watch a deployment land |
| **Failures** | Failed requests and exceptions, grouped — the starting point of every investigation |
| **Performance** | Response times per endpoint, slowest dependencies |
| **Transaction search** | Search individual events and open their end-to-end view |
| **Availability** | Results of availability tests from around the world |
| **Logs** | KQL queries over all data |

---

## Setting it up in a .NET application

### 1. Infrastructure (Bicep)

Application Insights is **workspace-based**: first a Log Analytics workspace, then an App Insights component that points at it.

```bicep
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'log-myapp-dev'
  location: location
  properties: {
    sku: { name: 'PerGB2018' }
    retentionInDays: 30
  }
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-myapp-dev'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

output connectionString string = appInsights.properties.ConnectionString
```

### 2. The application is wired up through configuration

The SDK finds App Insights through an **environment variable** — the same backing-service principle as with the database:

```bicep
appSettings: [
  {
    name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
    value: appInsights.properties.ConnectionString
  }
]
```

### 3. The SDK in the application

```bash
dotnet add package Microsoft.ApplicationInsights.AspNetCore
```

```csharp
// Program.cs
using OpenTelemetry.Trace;

if (builder.Configuration["APPLICATIONINSIGHTS_CONNECTION_STRING"] is not null)
{
    builder.Services.AddApplicationInsightsTelemetry();

    // Npgsql (PostgreSQL) publishes its own traces under the "Npgsql" source —
    // without this line the dependencies table stays empty.
    builder.Services.ConfigureOpenTelemetryTracerProvider(t => t.AddSource("Npgsql"));
}
```

`AddApplicationInsightsTelemetry()` switches on automatic collection (requests, exceptions, HttpClient and SqlClient dependencies) and routes `ILogger` output to App Insights.

Two things that **version 3** of the SDK (OpenTelemetry-based) changed:

| Topic | Before (2.x) | Now (3.x) |
|-------|--------------|-----------|
| No connection string | The SDK stayed silent | The SDK **crashes at startup**: `A connection string was not found` → register the SDK only when the setting exists (the `if` above) |
| PostgreSQL dependencies | – | Only ASP.NET Core, HttpClient and SqlClient are listened to by default. Npgsql's traces arrive once you subscribe with `AddSource("Npgsql")` |
| Sampling | adaptive | **rate limiting** (traces per second); the rows that are kept carry a `microsoft.sample_rate` field, and `sum(itemCount)` estimates the true count |

> **Note (Bicep + pipeline):** Log Analytics and App Insights require the resource providers `Microsoft.OperationalInsights`, `Microsoft.Insights` and `Microsoft.AlertsManagement` to be registered in the subscription. From your own CLI as Owner, ARM registers them automatically — but a pipeline identity (Contributor on one resource group) is not allowed to, and the deployment fails with `MissingSubscriptionRegistration`. Register once by hand: `az provider register --namespace Microsoft.OperationalInsights --wait` (and likewise the other two).

---

## Good logging practices

### Structured logging

Use a **message template** — do not interpolate values into the string:

```csharp
// ✅ Structured: EventId is a queryable field in KQL
logger.LogInformation("Registration created for event {EventId}", eventId);

// ❌ Interpolated: plain text, no field to query by
logger.LogInformation($"Registration created for event {eventId}");
```

In a structured log `{EventId}` is stored as its own field (`customDimensions.EventId`), so KQL can filter and group by it.

### PII and secrets do NOT belong in logs

**PII** (personally identifiable information) — names, e-mail addresses, phone numbers — and secrets (tokens, passwords, connection strings) never belong in a log:

```csharp
// ❌ PII leaks into telemetry (and stays there for the retention period)
logger.LogInformation("Registration by {Email} for {EventId}", request.AttendeeEmail, id);

// ✅ An identifier is enough for troubleshooting — the person can be looked up in the database if needed
logger.LogInformation("Registration {RegistrationId} created for event {EventId}", reg.Id, id);
```

Why this is serious: log data gets copied (workspace, exports, developers' screens), its access control is looser than the database's, and the GDPR right to erasure does not reach into logs in practice. The easiest solution: PII never enters the log in the first place.

### Log levels

| Level | Use |
|-------|-----|
| `LogDebug` | Development-time detail — not for production |
| `LogInformation` | A normal event: "registration created" |
| `LogWarning` | An expected exceptional situation: "event full", "duplicate email" |
| `LogError` | An error that needs attention: unhandled exception, dependency down |

---

## KQL — asking the telemetry questions

**KQL** (Kusto Query Language) is the query language of Log Analytics. It is a pipeline: table → filter → transform → summarize.

```kusto
// Failed requests in the last hour
requests
| where timestamp > ago(1h)
| where success == false
| order by timestamp desc

// Request counts by status code
requests
| where timestamp > ago(24h)
| summarize count() by resultCode

// Average response time per endpoint
requests
| where timestamp > ago(24h)
| summarize avg(duration), count() by name
| order by avg_duration desc

// Latest exceptions
exceptions
| order by timestamp desc
| take 10

// Slowest database queries
dependencies
| where type == "SQL" or type contains "postgres"
| order by duration desc
| take 10

// Your own log lines, filtered by a structured field
traces
| where customDimensions.EventId == "11111111-1111-1111-1111-111111111111"
```

| Operator | Meaning |
|----------|---------|
| `where` | Filter |
| `summarize ... by` | Group and aggregate (`count()`, `avg()`, `percentile()`) |
| `order by` / `take` | Sort and limit |
| `ago(1h)` | Relative time |
| `render timechart` | Draw the result as a chart |

> **AI and KQL:** language models generate KQL well when you name the table and the goal ("from the App Insights `requests` table, 5xx count in 5-minute windows, as a timechart"). Always check the column names against your own data — AI invents them without hesitation.

---

## Alerts and Action Groups

The alerting system has two parts, configured separately:

```
┌──────────────────────┐          ┌──────────────────────┐
│  ALERT RULE           │  fires   │  ACTION GROUP        │
│  "Http5xx > 0         │ ───────► │  "send an e-mail to  │
│   in a 5 min window"  │          │   student@edu.fi"    │
└──────────────────────┘          └──────────────────────┘
   WHAT is watched?                   HOW do we react?
```

The same Action Group can be attached to many alerts (5xx, availability, budget...).

### Creating them with the CLI

```bash
# Action Group: e-mail notification
az monitor action-group create \
  --resource-group $RG \
  --name ag-myapp-email \
  --short-name myappmail \
  --action email primary-email me@example.com

# Metric alert: App Service 5xx errors
az monitor metrics alert create \
  --resource-group $RG \
  --name alert-http5xx \
  --scopes $(az webapp show -g $RG -n $APP --query id -o tsv) \
  --condition "total Http5xx > 0" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --severity 2 \
  --action ag-myapp-email \
  --description "The app is returning server errors"
```

| Parameter | Meaning |
|-----------|---------|
| `--condition "total Http5xx > 0"` | Aggregation + metric + condition |
| `--window-size 5m` | Look-back window: the sum of 5xx over the last 5 minutes |
| `--evaluation-frequency 1m` | The condition is evaluated every minute |
| `--severity 2` | 0 = critical ... 4 = verbose; affects classification only |

An alert also **resolves** automatically when the condition no longer holds — and that sends its own e-mail.

> **Note:** the e-mail comes from `azure-noreply@microsoft.com` and may land in spam — look there first if nothing arrives.
>
> **Verify the address:** when an e-mail address is added to an Action Group, Azure sends a *"Verify your email address"* message with a one-time code. Until it is verified the recipient gets no alerts at all, even though the rule shows *Fired* in the Portal. The code expires in 30 minutes.

### Alerts in your pocket: the Azure mobile app

Nobody on call sits in front of a mailbox. The [Azure mobile app](https://azure.microsoft.com/en-us/get-started/azure-portal/mobile-app/) (Android/iOS) signs in with the same account and shows the same alerts as **push notifications** the moment they fire. It also shows resource state (e.g. a PostgreSQL server that is *Stopped*), lets you **start or stop** a resource, change an alert's user response (*Acknowledged* / *Closed*), follow Service Health and the current month's cost — and Cloud Shell gives you `az` commands without a laptop. The app is a window, not a replacement: KQL, dashboards and Bicep still happen in the Portal and in the pipeline.

---

## Availability tests

An **availability test** calls your application from Azure data centres around the world and alerts when the application does not respond — even when no user is around to notice.

- **Standard test**: an HTTP call to a chosen URL (e.g. `/health`) every 5–15 minutes from several locations
- Success criteria: status code (e.g. 200) and/or response time
- Attached to an Action Group → e-mail when X out of Y locations fail

Creation: App Insights → **Availability** → **Add Standard test**. Test a `/health`-style endpoint that also checks the dependencies — then the test says "the service works", not merely "the process is up".

---

## Costs

| Item | Price (order of magnitude) | Note |
|------|----------------------------|------|
| Log Analytics ingestion | ~2–3 €/GB, **first 5 GB/month free** (per billing account) | A small course app produces megabytes — free in practice |
| Data retention | 31 days free (App Insights data 90 days), then ~0.1 €/GB/month | 30-day retention is enough for the course |
| Metric alert rule | ~0.1 €/month per rule | |
| Availability standard test | ~1 €/month per test | Delete it at the end of the course |
| Action Group e-mail | Free | |

> **Sampling:** when a lot of data is produced, App Insights keeps only a sample of the telemetry (the .NET SDK 3.x limits traces per second by default). Even a few requests per second mark some rows as a 50 % sample. Know the phenomenon: in production a "missing" request may have been sampled out, and `count()` counts stored rows — `sum(itemCount)` estimates the real number.

---

## Best practices

### ✅ Do

- **Workspace-based App Insights** — all data in one Log Analytics workspace
- **Connection string from an environment variable** — the same build for every environment
- **Structured logging with message templates** — fields queryable in KQL
- **No PII and no secrets in logs** — identifiers are enough
- **An alert + Action Group for every "wake me up" condition**: 5xx, availability, (budget)
- **An availability test on the /health endpoint** — tests the service, not just the process
- **Test the alerts by breaking the application on purpose** — an alert that has never been seen firing is not an alert

### ❌ Avoid

- Do not log every request yourself with `LogInformation` — the requests telemetry already does it
- Do not create an alert that has no clear reaction ("who does what when this fires?")
- Do not let alert e-mails go unread in a "they always shout anyway" state — tune the threshold instead
- Do not use the Instrumentation Key based (deprecated) configuration — use the connection string

---

## Next

- [Azure App Service](../../Azure/App-Service.md) *(in Finnish)* - Hosting the application and its logs
- [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md) - The dependency App Insights shows in the dependencies table
- [Infrastructure as Code](Infrastructure-as-Code.md) - The monitoring infrastructure in Bicep
- [CI/CD](../../../Development-guidelines/eng/CI-CD.md) - The pipeline that deploys all of it

## Back

- [Azure services](README.md)
