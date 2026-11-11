# Azure Cost Management — tracking and controlling cloud spend
> 🇫🇮 Finnish version: [Cost-Management.md](../../Azure/Cost-Management.md)

## Table of Contents

1. [CapEx vs. OpEx — why a cloud bill is different](#capex-vs-opex--why-a-cloud-bill-is-different)
2. [How an Azure bill is born: meters](#how-an-azure-bill-is-born-meters)
3. [Cost Management tools](#cost-management-tools)
4. [Budgets and alerts](#budgets-and-alerts)
5. [Tags for cost allocation](#tags-for-cost-allocation)
6. [Rightsizing — the right SKU for the real need](#rightsizing--the-right-sku-for-the-real-need)
7. [Hidden costs](#hidden-costs)
8. [Ways to save](#ways-to-save)
9. [Automatic shutdown](#automatic-shutdown)
10. [AI in cost analysis](#ai-in-cost-analysis)
11. [Best practices](#best-practices)

---

## CapEx vs. OpEx — why a cloud bill is different

| | **CapEx** (capital expense) | **OpEx** (operating expense) |
|--|------------------------------|-------------------------------|
| Model | Buy a server up front | Pay for usage afterwards |
| Cost | One large sum, depreciated over years | A running monthly bill |
| Risk | Over- or under-sizing locked in for years | Sizing can change today |
| Whose problem | Finance budgets once | **Every developer affects the bill every day** |

In the cloud, architecture decisions **are** cost decisions: the SKU you pick, the scaling rules, the amount of logging and the forgotten test environment all show up on next month's bill. That is why cost literacy belongs to developers, not only to finance — the discipline is called **FinOps**.

The flip side: an OpEx bill can also **surprise** you. A CapEx server does not cost more when it is used badly — a cloud resource costs exactly as long and as much as it exists and does.

---

## How an Azure bill is born: meters

Azure bills by **meters**. One resource typically produces several meters — and some of them run even when nobody is using the service:

| Resource | Meters (examples) | Runs while idle? |
|----------|-------------------|------------------|
| App Service Plan | Instance hours by SKU | **Yes** — the plan costs money even if the app gets no requests |
| PostgreSQL Flexible Server | vCore hours + storage (GB/month) + backups | Compute **yes** while started; **storage always**, even stopped |
| Log Analytics | Ingested data (GB) + retention beyond the free allowance | No — only for data |
| Availability test (standard) | Test executions | Yes — it runs on a schedule |
| Metric alert rules | Fixed monthly price per rule | Yes (cents) |
| Bandwidth (egress) | Outbound data (GB) | No |

Two consequences:

1. **"I did not use it" does not mean "it did not cost anything".** Provisioned capacity (an App Service plan, database compute) bills for time, not for usage.
2. **Deleting and stopping are different things.** A stopped PostgreSQL server does not bill for compute, but its storage still does. Only a deleted resource is free.

### SKU, meter and unit of measure

Three words the price list speaks:

| Term | What it is | Example |
|------|------------|---------|
| **SKU** (stock keeping unit) | The *size class* of a product that you choose: the name by which Azure knows what capacity to give you | App Service `F1`, `B1`, `S1`; PostgreSQL `Standard_B1ms`; Storage `Standard_LRS` |
| **Meter** | One billable thing inside a SKU. One resource typically has several | A B1ms server: *compute hours*, *storage GB/month*, *backup storage GB/month* |
| **Unit of measure** | The unit the meter counts in | `1 Hour`, `1 GB/Month`, `10K` (operations), `1/Execution` |

The bill is therefore a sum of lines, each *meter × units used × unit price*. When you predict your own bill, start from the SKU, list its meters and estimate the units for each — that is the "Meters" column of the first table on this page.

### List price vs. the bill: the Retail Prices API

The pricing calculator is one source of list prices. The other is the **Retail Prices API**: a public endpoint, no sign-in, that returns the same price list as JSON.

```powershell
$Filter = "armRegionName eq 'francecentral' and priceType eq 'Consumption' and serviceName eq 'Azure Database for PostgreSQL'"
(Invoke-RestMethod "https://prices.azure.com/api/retail/prices?currencyCode=EUR&`$filter=$Filter").Items |
  Select-Object skuName, meterName, retailPrice, unitOfMeasure | Format-Table
```

| Parameter | Meaning |
|-----------|---------|
| `armRegionName` | The region — the same SKU costs different amounts in different regions |
| `priceType eq 'Consumption'` | Pay-as-you-go price (alternatives: `Reservation`, `DevTestConsumption`) |
| `currencyCode=EUR` | Currency; the default is USD |
| `NextPageLink` | The response is paged (100 rows) — the next page is in this field |

**The list price is a prediction; the bill is the truth.** The real bill differs from the list price for at least these reasons: free tiers (Log Analytics' 5 GB, App Service F1), student and sponsorship credits, a meter that is not applied to that subscription or shows up late, and rounding to the unit's precision. So estimate from the API or the calculator, but **check Cost analysis** a few days later.

---

## Cost Management tools

Portal → resource group (or subscription) → **Cost Management**:

| Tool | For what |
|------|----------|
| **Cost analysis** | Actual consumption: daily, per resource, per tag, per service; also the forecast |
| **Budgets** | Spending limits + alerts (see below) |
| **Cost alerts** | The list of budget alerts that have fired |
| **Advisor recommendations** | Azure's own savings suggestions (e.g. under-used resources) |

### Getting the most out of Cost analysis

- **Scope** first: resource group = the project's costs, subscription = everything
- **Group by: Resource** — what costs the most?
- **Group by: Tag → Environment** — dev vs. test vs. prod (requires the tags to be in order!)
- **Granularity: Daily** — when did consumption change? (The date of the spike + `git log` = the culprit is usually found at once)
- **Download** — CSV out, for analysis or for AI

> **Lag:** consumption data **is not real time** — it typically updates 8–24 hours behind. A resource created today shows up in the costs tomorrow at the earliest. This is the most common source of confusion.

### Accumulated, Daily and the two forecasts

The Cost analysis chart has two basic shapes. **Accumulated** draws the month's running total as a rising line — "how much so far, and where is it heading"; the budget appears in the same picture as a dashed line. **Daily** draws each day as its own bar — "when did something change": the day the plan was scaled or the database was created stands out at once, and `git log` tells the rest.

There are **two different forecasts**, and they do not show the same number:

| Forecast | Where | How it is computed | When it appears |
|----------|-------|--------------------|-----------------|
| The chart's *Forecast* | Cost analysis | Modelled from the month's trend | Only after several days of data — in a new resource group *"Forecast unavailable"* is normal |
| The budget's `forecastSpend` | The Budgets list, the budget API | A cruder estimate from the current daily rate | Already in the first days, before `currentSpend` has even updated |

**The Untagged bucket.** When you group by a tag you often see an *Untagged* slice even though Bicep tags everything you create. The reason: Azure creates resources *for* you — the availability test, the smart-detection rule, alert rules made by a Portal wizard — and they do not inherit tags. Harmless in a small environment; in a large organisation it is the reason to adopt an Azure Policy that denies untagged resources.

### The same data from the command line: the Cost Management API and az rest

Cost analysis is a user interface over the **Cost Management query API** — you can call the same endpoint yourself when you need the numbers in a script or a screenshot:

```powershell
$Body = @{
  type      = "ActualCost"          # what was billed; "AmortizedCost" spreads reservation purchases over the days they cover
  timeframe = "MonthToDate"         # or Custom + timePeriod
  dataset   = @{
    granularity = "None"            # or "Daily"
    aggregation = @{ totalCost = @{ name = "Cost"; function = "Sum" } }
    grouping    = @(@{ type = "Dimension"; name = "ResourceId" })   # or TagKey + the tag name
  }
} | ConvertTo-Json -Depth 5 -Compress

az rest --method post `
  --url "https://management.azure.com$Scope/providers/Microsoft.CostManagement/query?api-version=2023-11-01" `
  --body $Body --query "properties.rows" --output table
```

**`az rest`** sends a signed HTTP request to any Azure Resource Manager endpoint with the signed-in user's token. You need it when a CLI command is missing or lives in a preview extension (budgets, alert processing rules, cost queries) — and the call doubles as documentation of what the Portal does behind its button.

**`--query`** is a JMESPath expression that filters and reshapes the response JSON before it is printed. The basic forms:

| Expression | Does |
|------------|------|
| `properties.rows` | Picks a path |
| `[].{name:name, state:properties.state}` | Projects a new object with chosen fields from every array element |
| `[?average != null]` | Filters elements by a condition |
| `value[0].timeseries[0].data` | Indexes into arrays |
| `--output table` / `tsv` / `json` | Output format; `tsv` is the one to capture into a variable |

> **Throttling:** the query API answers `429 Too many requests` if more than a handful of calls per minute hit the same scope. Wait a minute (the `Retry-After` header says how long) and do not put the query in a loop.

---

## Budgets and alerts

A **budget** is a watch limit, not a circuit breaker: it **alerts** by e-mail but does **not** stop consumption or delete resources.

| Setting | Recommendation for a study environment |
|---------|-----------------------------------------|
| Scope | The course resource group (+ optionally a second budget for the whole subscription) |
| Reset period | Monthly |
| Alert thresholds | **Actual** 50 % / 80 % / 100 % + **Forecasted** 100 % |

**Actual vs. Forecasted:**

- **Actual** fires when realised spend crosses the threshold — the damage has (partly) happened
- **Forecasted** fires when Azure's projection of the month-end total crosses the threshold — an **early warning**, you can react before the limit is really crossed

Budgets are evaluated periodically (in hours, not minutes) — a budget does not replace metric alerts, and a metric alert does not replace a budget. Different tools for different time scales.

---

## Tags for cost allocation

Cost analysis can group costs **by tag** — but only if tags are set consistently. Without tags, the subscription's bill is one big lump and nobody knows whose project caused it.

A recommended base set (the same as in the course's Bicep templates):

| Tag | Example | Answers the question |
|-----|---------|----------------------|
| `Environment` | `dev` / `test` / `prod` | Which environment's cost? |
| `Project` / `Course` | `cloud26` | Which project's cost? |
| `Owner` | `firstname.lastname@edu.xamk.fi` | Whom to ask "is this still needed?" |
| `CostCenter` | `IT-1234` | Which cost centre pays? |

Practices that make tags trustworthy:

- Tags come from **IaC** (the Bicep `tags` object) — hand-added ones get forgotten
- Note: resource-group tags **do not inherit** to resources automatically — so tags are set on every resource (or inheritance is enforced with Azure Policy)

---

## Rightsizing — the right SKU for the real need

**Rightsizing** = matching capacity to real, *measured* need — not to a guess and not to a "just in case" multiplier.

The process:

1. **Measure** actual usage: App Service CPU/memory, database CPU/connections, response times (Application Insights / Metrics)
2. **Compare** with provisioned capacity: if a B1 plan runs at 3 % CPU, you are paying for 97 % of nothing
3. **Shrink** one step at a time and watch the effect — monitoring tells you if you went too small
4. **Repeat** — the need changes over time

Remember the **feature thresholds** of the SKU ladder: a cheaper tier may drop features, not just power (e.g. App Service F1: no Always On and no scaling; Basic: no staging slots). A rightsizing decision is therefore a feature **and** a capacity decision.

The opposite direction matters just as much: if the metrics show a constant 80 %+ load or queuing, the SKU is **undersized** — and it costs you in response times and errors.

### The evidence: the plan's CPU and memory metrics

The numbers behind a rightsizing decision are **platform metrics**: Azure collects them from every resource for free and without any SDK. For App Service you read them at the **plan** level (`Microsoft.Web/serverfarms`), because the plan is what you pay for the size of: `CpuPercentage` and `MemoryPercentage`.

Two aggregations tell different stories: **Avg** is the level the application lives at, **Max** is the spikes — typically deployments and restarts, not users. The decision is made on the average, but the spikes tell you whether the peak still fits a smaller SKU.

```powershell
az monitor metrics list `
  --resource plan-myapp-dev --resource-group $RG --resource-type Microsoft.Web/serverfarms `
  --metric CpuPercentage --offset 7d --interval PT6H --aggregation Average Maximum `
  --query "value[0].timeseries[0].data[?average != null].{time:timeStamp, avg:average, max:maximum}" --output table
# the same with --metric MemoryPercentage
```

`--interval` accepts only certain values (`PT1M`, `PT5M`, `PT15M`, `PT30M`, `PT1H`, `PT6H`, `PT12H`, `P1D`); for a week, `PT6H` or `P1D` is readable. Look at **both** metrics: on the course app CPU is in single digits, but memory may sit at 70 % of B1's 1.75 GB — and F1 gives 1 GB. Rightsizing is decided on the metric that is closest to its ceiling.

### Feature thresholds: Always On and the F1 quota

A cheaper tier drops features, not just power. Two App Service examples you only notice when they are missing:

- **Always On** (Basic and above): App Service keeps the process warm even without traffic. Without it (F1, Shared) the app goes to sleep after ~20 minutes of silence and the next request takes seconds — to an availability test that looks like an outage, and the alerts *flap*. In Bicep it is `siteConfig.alwaysOn`; when scaling down it must be switched off **before** the plan changes (`az webapp config set --always-on false`), or the deployment fails with `Conflict … AlwaysOn … not allowed in the target compute mode`.
- **The F1 daily quota**: 60 CPU minutes per day. When it is used up, App Service stops the app: `/health` answers an HTML page saying *Error 403 - This web app is stopped*, `az webapp show` reports `state: QuotaExceeded`, a deployment fails with `Site Disabled (CODE: 403)`, and the quota resets at midnight UTC. Note that **monitoring itself consumes the quota**: an availability test from five locations every five minutes is 1 440 calls a day, each opening a database connection.

The rightsizing question is therefore not "is F1 enough for my users" but "is F1 enough for my users *and everything else that calls the app*".

---

## Hidden costs

Items that do not appear in the architecture diagram but do appear on the bill:

| Hidden cost | Where it comes from | Antidote |
|-------------|---------------------|----------|
| **Idle resources** | A forgotten test environment, a POC, "I'll look at this later" | Tags (Owner!), regular clean-up, automatic shutdown |
| **Egress** | Data leaving Azure | Keep data and compute in the same region; watch it with large volumes |
| **Diagnostics and logs** | Log Analytics ingestion priced per GB; verbose debug logging in production | Sensible log levels, sampling, sane retention |
| **Over-provisioned storage** | A database disk cannot be shrunk afterwards (only grown) | Start small |
| **Backups and retention** | Backup storage beyond the free allowance and long retention | Check the defaults — do not keep things "forever" out of habit |
| **Storage of a stopped resource** | A stopped VM/database still bills for its disk | Delete it if you do not really need it |
| **Availability test executions** | List price per execution: 5 locations × every 5 min ≈ 43 000 executions/month | Check your own bill; a longer interval or fewer locations cuts it directly; delete it at the end of the course |

---

## Ways to save

A rough order for a study / small environment — most effective first:

1. **Delete what you do not need** — zeroes the cost entirely
2. **Stop when not in use** — stopping the database for the night and the weekend removes the compute cost (storage stays)
3. **Rightsizing** — a smaller SKU according to measured need
4. **Log discipline** — do not ingest data nobody queries
5. **Free tiers** — the F1 plan, the Log Analytics free allowance, student credits

At production scale the list also gets **reservations** (Reserved Instances / Savings Plan: commit for 1–3 years, get a 30–60 % discount) and **scaling rules** (pay for peak capacity only while the peak is on) — not tools for a student environment, but worth knowing.

### Production price factors: HA, reservations and savings plans

When the same architecture is priced for production, the bill multiplies for a few reasons you should be able to name:

| Factor | What you pay | Why |
|--------|--------------|-----|
| **PostgreSQL High Availability** | Compute **×2** | HA = *a second server that is already running* (a standby) in another availability zone (*zone-redundant*) or in the same one (*same-zone*); failover in about a minute without data loss. A single course server is not HA |
| **App Service Standard / Premium** | 5–10× the Basic instance price | Deployment slots, autoscale, more instances, a better SLA |
| **Bigger SKUs and more instances** | Linearly | Scaling out multiplies the plan price by the instance count |

In return, production has **commitment discounts** that a student environment does not:

| | **Reserved Instance** | **Savings Plan** |
|--|----------------------|------------------|
| You commit to | A specific SKU and region for 1 or 3 years | An hourly spend (e.g. 5 €/h of compute) for 1 or 3 years |
| Discount | The largest (up to 60–70 %) | Smaller (up to ~65 % on paper, less in practice) |
| Flexibility | Little — changing SKU is an exchange operation | Covers any SKU and region up to the commitment |
| Worth it when | The base load is steady and known for years | The load is steady but its shape changes |

In both you give up what was the advantage of OpEx: the ability to shrink today. That is why a commitment is made only for a measured base load — never for the whole capacity.

---

## Automatic shutdown

Human memory is a poor savings mechanism. Scheduled automation does not forget:

- **GitHub Actions schedule** — the same pipeline that deploys can also shut down: `on: schedule: cron` + OIDC sign-in + `az postgres flexible-server stop`. No new tools if CI/CD is already in place
- **Azure Automation / Logic Apps** — the Azure-native alternative for the same
- **DevTest Labs auto-shutdown** — built in for VM environments

Remember the side effect: if the environment is monitored (availability tests, alerts), a scheduled shutdown **fires the alerts every evening**. A planned outage needs **alert suppression** for the same window (an alert processing rule / maintenance window, see below) — otherwise you train yourself to ignore alerts, and that is the most dangerous outcome of monitoring ([alert fatigue](Monitoring-and-Application-Insights.md#alert-fatigue-and-the-resolved-notification)).

### GitHub Actions schedule: cron, UTC and best effort

```yaml
on:
  schedule:
    - cron: '0 18 * * *'   # minute hour day-of-month month day-of-week
  workflow_dispatch:       # manual run: testing and proof
```

| Field | Value | Examples |
|-------|-------|----------|
| minute, hour | `0 18` | `30 5` = 05:30; `*/15 * * * *` = every 15 minutes |
| day, month | `* *` | `1 *` = the 1st of every month |
| day of week | `*` | `1-5` = Mon–Fri (0 = Sunday) |

Four rules that surprise people:

1. **Cron is always UTC.** `0 18` is 20:00 in Helsinki in winter and 21:00 in summer — daylight saving moves your clock, not cron.
2. **Runs are best effort.** GitHub starts the run "some time after the slot": under load minutes to hours late (5 hours in the course test), and a freshly merged schedule can skip its first slot entirely. A to-the-minute schedule belongs to an Azure-native timer (Logic Apps, Automation).
3. **Default branch only.** The schedule is read from the file on `main` — on a PR branch it never fires.
4. **The 60-day rule.** If a repository has no activity for 60 days, GitHub switches its schedules off.

`workflow_dispatch` in the same file gives you the *Run workflow* button: use it to test at once and to prove the OIDC sign-in. The proof of the *schedule* is still only a run whose event is `schedule` (`gh run list --event schedule`). Make the stop step **idempotent** — check the state before the command — so that a manual run on top of an already stopped server does not fail ([idempotency](Infrastructure-as-Code.md#idempotency)).

### Alert suppression: the alert processing rule

An **alert processing rule** is an Azure Monitor rule that changes how fired alerts are handled inside a scope (a resource group, for example). The suppression form, `RemoveAllActionGroups`, means: the alert **fires and is recorded** in the history as usual, but no Action Group is invoked — the e-mail never goes out. The truth is preserved, the inbox is spared. The schedule can be one-off (a maintenance window) or recurring (Daily, Weekly), and a window that crosses midnight, 20:00 → 08:00, is a single Daily recurrence.

```powershell
$Body = @{
  location   = "Global"
  properties = @{
    scopes   = @($Scope)
    enabled  = $true
    actions  = @(@{ actionType = "RemoveAllActionGroups" })
    schedule = @{
      timeZone    = "FLE Standard Time"
      recurrences = @(@{ recurrenceType = "Daily"; startTime = "20:00:00"; endTime = "08:00:00" })
    }
  }
} | ConvertTo-Json -Depth 6 -Compress
az rest --method put --body $Body `
  --url "https://management.azure.com$Scope/providers/Microsoft.AlertsManagement/actionRules/apr-quiet-hours?api-version=2021-08-08"
```

**Time zones** are given as Windows time-zone IDs, not IANA names: Helsinki is `FLE Standard Time` (Finland, Lithuania, Estonia), Central Europe `W. Europe Standard Time`, UTC is `UTC`. The ID covers daylight saving automatically — the rule follows the wall clock. Cron does not, so the UTC schedule and the local window must cover each other **in both winter and summer time** (18:00 UTC = 20:00 or 21:00 Helsinki → a 20:00–08:00 window works for both). The CLI command `az monitor alert-processing-rule` lives in a preview extension; the REST call is stable, and the same resource can be written in Bicep (`Microsoft.AlertsManagement/actionRules`).

---

## AI in cost analysis

Consumption data is tabular and explainable — natural ground for AI:

| Use | How |
|-----|-----|
| **Interpreting a consumption report** | Export Cost analysis as CSV → ask AI to break down the biggest drivers and anomalies |
| **Savings proposals** | Ask for 2–3 concrete actions with € estimates from your own data |
| **SKU comparisons** | "App Service B1 vs. F1 vs. Container Apps for this load" — mapping the alternatives |
| **Copilot in Azure** | Cost questions directly in the Portal, in natural language |

**Critical thinking is part of the picture:** AI's price data may be outdated or for the wrong region or currency. Always check € claims against the [pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/) or your own consumption data before making decisions. AI is a good *structurer of analysis* and a poor *rememberer of price lists*.

---

## Best practices

### ✅ Do

- **A budget + alerts before the first paid resource** — Actual 50/80/100 % + Forecasted 100 %
- **Tags on every resource through IaC** — costs allocate themselves
- **Look at Cost analysis weekly** — small surprises do not have time to grow
- **Shut down and clean up automatically** — and do not forget alert suppression for the outage window
- **Rightsizing based on measurements** — the monitoring data already exists, use it
- **Deleted > stopped > shrunk** — the order of impact

### ❌ Avoid

- Do not trust "I'll notice it on the bill" — the data arrives 8–24 h late and the bill once a month
- Do not leave a resource running "just in case" — tag the Owner and delete when the owner no longer needs it
- Do not pick a SKU by guessing upwards "so it won't run out" — measure and adjust
- Do not make cost decisions on AI's memory of prices alone — the calculator and your own data decide

---

## Next

- [Azure Monitor and Application Insights](Monitoring-and-Application-Insights.md) - The measurement data that rightsizing is based on
- [Azure App Service](../../Azure/App-Service.md) *(in Finnish)* - The SKU ladder and its features
- [Azure Database for PostgreSQL](Azure-Database-PostgreSQL.md) - Stop/start and the storage cost
- [Infrastructure as Code](Infrastructure-as-Code.md) - Tags and SKUs in code

## Back

- [Azure services](README.md)
