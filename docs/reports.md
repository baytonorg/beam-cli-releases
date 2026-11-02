# Report exports

[Documentation index](index.md) | [User guide](user-guide.md#reports-and-bql)

**Requires 0.7**, currently a source/local build. The public installer provides
0.5.0 as of 2 November 2026. Only asynchronous `reports create/get` are available
in that release. See the [version table](index.md#choose-the-right-version).

The CLI reproduces the rows and calculations from Flare's report catalogue at
`65570a38591c313ca128a4f029bb0f1ddc7fac0b` (v1.5.5), with the Core `5aa1afe` API
contract. No Flare or Core changes are required.

## CSV records

```sh
beam reports device-inventory > inventory.csv
beam reports estate-summary --output estate.csv
beam reports spl-risk --json > patch-risk.json
```

CSV is the default for export commands and contains one header followed by data
records, without progress messages or metadata comments. It uses UTF-8 without a
BOM and CRLF record terminators; embedded cell text is preserved and quoted.
Spreadsheet formula prefixes are neutralised with an apostrophe, including when
preceded by whitespace. Arrays such as IMEIs use semicolon-separated values.
Dates retain the API's ISO timestamps instead of the browser's local presentation.
Application source values retain the API enum rather than the browser's label.

Multi-section reports have a `Section` column and the union of the sections'
columns, with irrelevant cells blank. For example, an application summary includes
its metadata, version records and coverage records in one CSV file.

`--json` returns a report document with generated time, scope IDs, sections, columns,
typed row values and freshness notes. Large integer version codes are preserved.
Notes are sent to stderr for CSV, and included in the JSON document for JSON.
`reports schema` and asynchronous `reports get/create` retain their API JSON shapes.

Shell redirection uses the shell's permissions and overwrites its destination
before BEAM runs. `--output PATH` instead creates a new file, refuses to overwrite
one, and removes an unsuccessful export. Its mode is 0600 on Unix; Windows inherits
the destination folder's permissions, so choose a protected folder there.

## Estate and device reports

| Command after `beam reports` | Flare report | Data source |
| --- | --- | --- |
| `spl-posture` | Security patch posture | `statistics/devices` |
| `update-state` | Device update state | `statistics/devices` |
| `enrolment-trend` | Enrolment trend (30 days) | `statistics/devices` |
| `estate-summary` | Estate summary | `statistics/devices` |
| `device-inventory` | Device inventory | All device entity pages |
| `spl-risk` | Security patch risk list | All device entity pages |
| `update-pending` | Update-pending devices | All device entity pages |

Patch statistics are cumulative on Core. The report differences the over-30,
over-90 and over-180-day counts into distinct buckets and keeps unknown patch
dates. Per-device ages use UTC date parsing and elapsed whole days against one
captured generation time. Boundaries match Flare: up to 30, 31-90, 91-180 and over
180 days. Invalid dates are unknown. Patch risk sorts oldest first, using Flare's
unknown-age ordering.

The update-pending export accepts Flare's four pending/available labels. It does
not treat a nonempty string, `Unknown`, or `Up to date` as a true boolean.
The aggregate update-state report uses Core's aggregate pending counter, just as
Flare does; this is not recalculated from the detail labels. Missing measurements
fail instead of being presented as observed zero or healthy devices.

Device columns mirror Flare's inventory export. Its `Last sync` column is backed
by `last_heartbeat_at`, as in Flare. Aggregate counts come from Core's cached
statistics (normally five minutes), while detail rows come from the entity API.
The enrolment trend preserves Core's cumulative series rather than inferring a
historic snapshot from the current device list.

## Applications

```sh
beam reports applications --search 'Managed Info' --sort devices --direction desc
beam reports application org.bayton.managedinfo
beam reports application-versions org.bayton.managedinfo --stale-days 30
beam reports application-devices org.bayton.managedinfo --version-code 1331
```

The application list reads the selected group's latest completed background
snapshot. It reports missing or stale snapshot metadata instead of claiming an
ungenerated report means no apps are installed. The summary, version distribution
and application-device rows use Flare's corresponding API calls. Inventory
snapshots and live reported version/device data can therefore differ in freshness.

`Missing or not reported` means no stored application-inventory row for those
active devices. It does not prove the app is absent. Stale-device counts use the
requested heartbeat threshold, from 1 to 365 days. AMAPI-only install/update times
can be null and remain blank.

List exports fetch all pages. `--per-page` is at most 100 for application APIs and
200 for device entity exports. Search, application type, sorting and version-code
filters use the same backend parameters as Flare. `--group` is the existing active
context assertion, not a report filter or an implicit context switch.

## BQL

```sh
beam reports schema
beam reports query --query 'entity(device|device_name,manufacturer) limit(50)'
beam reports query --query-file query.bql > results.csv
```

`query.bql` contains plain BQL text, not JSON. `--query-file -` reads it from stdin.
Exactly one query input is required; queries contain 1-2000 UTF-8 characters.
Core validates the syntax, entity permissions, columns, filters, sorting and scope.
Named queries call Core's read-only BQL executor. Generic API POST calls retain
their existing explicit approval requirements.

Core limits BQL to 500 rows, with a default of 100; it is not an unbounded device
export. The result columns are a deterministic union of returned keys. An empty
query result emits no CSV records when there are no returned column names; JSON
retains the empty result and metadata.

Known credential fields and opaque managed configurations are redacted, including
enrolment QR credentials returned by wildcard queries. This cannot identify
arbitrary secrets stored under innocuous field names; protect exported data
according to its contents. From public 0.7.0, use `--include-secrets` for deliberate verbatim credential and managed configuration values in BQL CSV/JSON. Protect those exports appropriately.

## Consistency and limits

All pages are fetched before CSV records are emitted. Network/page errors, duplicate
identities, inconsistent totals, changed application snapshot timestamps and
detected account-scope changes fail the export. Scope is checked around page reads
and before output. This cannot make Core's shared account context or changing
device data transactionally atomic; use fixed-group service tokens for automation
until request-scoped context is available.

Exports default to at most 100,000 input rows, configurable with `--max-items`, and
have a separate 64 MiB aggregate API-input ceiling plus the common per-response
limit. Exceeding a limit fails clearly, without returning a successful truncated
report. Narrow the search or use an appropriate query instead. No export command
automatically triggers report generation, changes a policy or sends a device command.
