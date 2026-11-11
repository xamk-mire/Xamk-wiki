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
9. [Dashboards and workbooks](#dashboards-and-workbooks)
10. [Costs](#costs)
11. [Best practices](#best-practices)

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

### Correlation: operation_Id

Correlation is not magic — it is one column. When a request arrives, the SDK gives it an identifier, **`operation_Id`**, and stamps it on everything the request produces: the `requests` row, every `dependencies` row (SQL statements), the `traces` rows (`ILogger`) and the `exceptions` rows. The "end-to-end transaction" tree in Transaction search is nothing more than these tables joined on that column.

```kusto
// One request and everything it caused
requests
| where name startswith "POST /api/events"
| take 1
| join kind=inner (dependencies) on operation_Id
| project timestamp, name, duration, dependency = name1, sql = data, dependencyDuration = duration1
```

Whenever you write KQL that joins tables, `operation_Id` is the key — not `id`, not `session_Id`, and not a `correlationId` an AI tool invents. Inside a request, dependencies also carry their own `id` and a parent id, which is how the tree is built; for the course, `operation_Id` is enough.

### Key views in the Portal

| View | Use |
|------|-----|
| **Live Metrics** | Real-time traffic (one-second latency) — watch a deployment land |
| **Failures** | Failed requests and exceptions, grouped — the starting point of every investigation |
| **Performance** | Response times per endpoint, slowest dependencies |
| **Transaction search** | Search individual events and open their end-to-end view |
| **Application map** | A map of the application and its dependencies (PostgreSQL, Storage, other APIs) with call counts and failure rates — "which box is red?" |
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

**OpenTelemetry** (OTel) is the vendor-neutral standard for how an application produces traces, metrics and logs — the same code can send its data to App Insights, Grafana or Jaeger. In .NET a trace starts from an `ActivitySource`: a library (ASP.NET Core, HttpClient, Npgsql) creates an `Activity` for each operation and publishes it under a named source. The SDK **subscribes** to sources: only Microsoft's own by default, and `AddSource("Npgsql")` adds the PostgreSQL driver's source to the subscription. That is why a missing line breaks nothing — the `dependencies` table just stays quietly empty.

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
| `LogTrace` | The most detailed level (variable values, loop iterations) — switched on briefly, never permanently |
| `LogDebug` | Development-time detail — not for production |
| `LogInformation` | A normal event: "registration created" |
| `LogWarning` | An expected exceptional situation: "event full", "duplicate email" |
| `LogError` | An error that needs attention: unhandled exception, dependency down |
| `LogCritical` | The application cannot continue: startup failed, disk full |

Pick the level by **what the reader does on seeing the line**: Information is statistics, Warning is "look if it repeats", Error is "somebody fixes this". If every line is an Error, none of them is.

### Log levels in configuration (appsettings)

The code does not decide what gets stored — configuration does. The `Logging` section of `appsettings.json` sets a **threshold per category**; the category is the logger's type name (`ILogger<Program>` → `Program`) or a library's namespace:

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore.Database.Command": "Warning"
    }
  }
}
```

| Line | Effect |
|------|--------|
| `Default` | The threshold for every category not listed explicitly |
| `Microsoft.AspNetCore: Warning` | Drops the framework's own Information lines (one per request) |
| `Microsoft.EntityFrameworkCore.Database.Command: Warning` | Drops EF Core's `Executed DbCommand` lines (one per SQL statement) — the noisiest category in your telemetry, but sometimes the only evidence of what the database was asked during an incident |

The most specific match wins: `Microsoft.EntityFrameworkCore.Database.Command` overrides `Microsoft.EntityFrameworkCore`, which overrides `Default`. The environment-specific file (`appsettings.Development.json`) overrides the base file, and on App Service the same setting is given as an environment variable, `Logging__LogLevel__Microsoft.EntityFrameworkCore=Warning` (double underscore = `:`). The filter runs **inside the application before anything is sent**, so it also saves ingestion cost — unlike a KQL filter, which only works on data already stored.

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
| `where` | Filter. On text: `==` exact, `startswith`, `has` (whole word, fast), `contains` (substring, slow) |
| `project` | Choose and rename columns (`project timestamp, name, ms = duration`) |
| `extend` | Add a computed column (`extend slow = duration > 1000`) |
| `summarize ... by` | Group and aggregate (`count()`, `avg()`, `percentile(duration, 95)`, `sum(itemCount)`) |
| `bin(timestamp, 5m)` | Round time into buckets — `summarize count() by bin(timestamp, 5m)` is a time series |
| `order by` / `take` | Sort and limit |
| `ago(1h)` | Relative time |
| `join kind=inner (table) on operation_Id` | Combine two tables on a shared column (see [Correlation](#correlation-operation_id)) |
| `tostring(customDimensions.X)` | `customDimensions` is a `dynamic` JSON value — convert it before grouping `by` it or comparing it |
| `render timechart` | Draw the result as a chart |

A pipeline is read top to bottom: each `|` takes the previous line's result and hands it to the next. `summarize` produces columns named `count_`, `avg_duration` and so on — those are the names you use in `order by`.

### Tables and columns

| Table | One row is | The columns you ask for most |
|-------|------------|------------------------------|
| `requests` | one HTTP request into your application | `name` (`GET /api/events`), `resultCode` (`"200"`, a string), `success`, `duration` (ms), `operation_Id` |
| `dependencies` | one outgoing call: an SQL statement, an HTTP call | `type` (`postgresql`, `Http`), `name` (for PostgreSQL just `postgresql`), `target` (server name), `data` (the SQL text), `success`, `duration` |
| `traces` | one `ILogger` line | `message`, `severityLevel` (1 = Information, 2 = Warning, 3 = Error), `customDimensions` (template fields, `CategoryName`, `EventId`) |
| `exceptions` | one exception | `type` (`Npgsql.NpgsqlException`), `outerMessage`, `innermostMessage`, `details[0].rawStack` |
| `availabilityResults` | one availability-test run from one location | `name`, `location`, `success`, `duration` |
| `customMetrics` | one measurement | `name`, `value` |

Two surprises worth knowing in advance: `resultCode` is a **string** (`resultCode == "500"`), and a PostgreSQL dependency's SQL lives in `data`, not `name`. When you do not know the columns, look at one raw row: `dependencies | take 1`.

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

### Metric alert vs. log alert

Azure Monitor has two kinds of alert, and the difference is the signal:

| | **Metric alert** | **Log alert** (scheduled query) |
|---|---|---|
| Signal | A numeric time series: a platform metric (`Http5xx`, CPU) or an App Insights metric | A KQL query whose result crosses a threshold |
| Example | "the sum of `Http5xx` > 0 in a 5-minute window" | "`exceptions \| where type has 'Npgsql'` returns > 5 rows in 15 minutes" |
| Latency | About a minute (metrics are near real time) | Ingestion delay (minutes) + the evaluation interval |
| Price | First 10 time series free | Per rule and evaluation frequency, more expensive |
| Use when | The condition is a number that already exists | The condition needs a filter or a combination no metric provides |

Three numbers define a metric alert's behaviour: the **threshold** (`> 0`), the **window** (`--window-size 5m`: the time span the aggregate covers) and the **evaluation frequency** (`--evaluation-frequency 1m`: how often the window is examined). A window longer than the frequency means the same error is seen by several consecutive evaluations — the alert stays *Fired* until the window is clean.

### Alert fatigue and the resolved notification

**Alert fatigue** is monitoring's own failure mode: when more alerts arrive than anyone can act on, people learn to ignore them — the real one included. The course's `Http5xx > 0` is a teaching threshold; in production one 5xx in a thousand requests is noise. Three dials:

1. **Threshold** based on normal traffic (for example a 5xx *ratio* above 2 %, not an absolute count)
2. **Window** long enough that a momentary spike does not fire (5 → 15 minutes)
3. **Alert processing rule** for planned outages — a nightly stop is not an incident (see [Cost Management](Cost-Management.md#alert-suppression-the-alert-processing-rule))

And every alert needs a **reaction**: if nobody does anything when it fires, it belongs on a dashboard, not in an alert rule.

The **resolved notification** is the same alert in the other direction: when the condition no longer holds, the state changes *Fired* → *Resolved* and the Action Group sends a second message. That is not spam: the on-call person knows the fix worked, the duration of alerts gives you mean time to recovery, and an alert that never resolves tells you the rule is broken. On the Portal's Alerts page the column is *Monitor condition*; the user-managed *Alert state* (New / Acknowledged / Closed) is a different thing and is changed by hand.

### Smart detection (Failure Anomalies)

When an App Insights resource is created, Azure automatically creates a **Smart detection** rule next to it, *Failure Anomalies*, with its own Action Group (*Application Insights Smart Detection*). The rule learns the application's normal failure rate and alerts when the share of failed requests **deviates** from it suddenly — with no threshold set by you. It complements your own rules rather than replacing them: it needs traffic to learn from, and its message is "something changed", not "what".

Practical consequences: the resource group contains resources Bicep did not create (`microsoft.alertsmanagement/smartDetectorAlertRules/...` and two extra Action Groups), and what-if lists them as `* Ignore` rows — that is correct, not an error. The rule can be disabled in the Portal (App Insights → Smart detection); for the course it can stay.

### Alerts in your pocket: the Azure mobile app

Nobody on call sits in front of a mailbox. The [Azure mobile app](https://azure.microsoft.com/en-us/get-started/azure-portal/mobile-app/) (Android/iOS) signs in with the same account and shows the same alerts as **push notifications** the moment they fire. It also shows resource state (e.g. a PostgreSQL server that is *Stopped*), lets you **start or stop** a resource, change an alert's user response (*Acknowledged* / *Closed*), follow Service Health and the current month's cost — and Cloud Shell gives you `az` commands without a laptop. The app is a window, not a replacement: KQL, dashboards and Bicep still happen in the Portal and in the pipeline.

---

## Availability tests

An **availability test** calls your application from Azure data centres around the world and alerts when the application does not respond — even when no user is around to notice.

- **Standard test**: an HTTP call to a chosen URL (e.g. `/health`) every 5–15 minutes from several locations
- Success criteria: status code (e.g. 200) and/or response time
- Attached to an Action Group → e-mail when X out of Y locations fail

The test creates its own metric alert rule (`availabilityResults/availabilityPercentage`) whose condition is **"X of Y locations failed"**. Several locations matter: one data centre can fail for network reasons that have nothing to do with your application, and "2 of 5" separates an application fault from a single bad route. Every run is one row in the `availabilityResults` table, and every run is a billable execution (see [Costs](#costs)).

Creation: App Insights → **Availability** → **Add Standard test**. Test a `/health`-style endpoint that also checks the dependencies — then the test says "the service works", not merely "the process is up".

---

## Dashboards and workbooks

An alert wakes you up; a **dashboard** answers "is everything OK?" at a glance, so nobody composes KQL from memory in the middle of an incident.

| | **Dashboard** | **Workbook** |
|---|---|---|
| What | A grid of pinned tiles: charts, KQL results, resource lists | An interactive report: text, parameters (time range, environment) and KQL charts in one document |
| How it is made | From a Portal view with the **pin** icon (Failures, Performance, Availability, Logs) | App Insights → **Workbooks** → from a template or from scratch |
| Sharing | *Share* publishes it to the resource group — the team sees the same screen; private by default | Saved as a resource, always shared |
| Use when | "The picture on the wall": the on-call person's first look | Repeated analysis with parameters: a weekly report, a post mortem, a capacity review |

A good first dashboard is four tiles: failed requests over time (Failures), response time (Performance), availability-test results per location (Availability) and one KQL chart of your own. The dashboard tells you *that* something is wrong; the *why* comes from the Failures view and KQL.

---

## Costs

| Item | Price (order of magnitude) | Note |
|------|----------------------------|------|
| Log Analytics ingestion | ~2–3 €/GB, **first 5 GB/month free** (per billing account) | A small course app produces megabytes — free in practice |
| Data retention | 31 days free (App Insights data 90 days), then ~0.1 €/GB/month | 30-day retention is enough for the course |
| Metric alert rule | ~0.1 €/month per monitored time series, **first 10 free** | The course's two rules: 0 € |
| Availability standard test | List price **~0.0006 € per execution** — 5 locations × every 5 min ≈ 43 000 executions/month ≈ 25 €/month | Check your own Cost analysis: the course staff's first day of billing showed no such line. If it appears, a longer interval or fewer locations cuts it directly. Delete it at the end of the course |
| Action Group e-mail | Free | |
| Daily ingestion cap (*daily cap*, workspace → Usage and estimated costs) | Free setting | Protects the bill if something starts logging in a loop; once the cap is hit, data is **dropped** for the rest of the day — including what your alerts need |

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
