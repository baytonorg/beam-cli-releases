# BEAM CLI user guide

[Documentation index](index.md) | [All commands and flags](command-reference.md)

This guide uses placeholder IDs such as `DEVICE_ID` and `GROUP_ID`. Replace them
with IDs returned by your own BEAM deployment. Commands assume a terminal where
you can review writes. Flags, permissions and request schemas are also available
through `--help` and `api describe`.

The public release is currently **0.5.0**. Update checks require **0.6**; automatic
completion setup, named CSV reports and BQL exports require **0.7**, currently a source/local build. See the
[version table](index.md#choose-the-right-version) before using those commands.

## Contents

- [Getting started](#getting-started)
- [Context and profiles](#context-and-profiles)
- [Change previews and validation](#change-previews-and-validation)
- [Finding and reading resources](#finding-and-reading-resources)
- [Policy editing](#policy-editing)
- [Policy lifecycle](#policy-lifecycle)
- [Managed configurations](#managed-configurations)
- [Devices](#devices)
- [Device commands](#device-commands)
- [Bulk and dynamic actions](#bulk-and-dynamic-actions)
- [Groups and users](#groups-and-users)
- [Roles and tokens](#roles-and-tokens)
- [Enrolment](#enrolment)
- [Workflows and settings](#workflows-and-settings)
- [Reports and BQL](#reports-and-bql)
- [API access](#api-access)
- [Automation and output](#automation-and-output)
- [Shell completion](#shell-completion)
- [Updates and troubleshooting](#updates-and-troubleshooting)

## Getting started

Install on macOS or Linux:

```sh
curl -fsSL https://raw.githubusercontent.com/baytonorg/beam-cli-releases/main/install.sh | sh
beam --version
```

The executable goes in `~/.local/bin`. If your shell cannot find it, add that
directory to `PATH`. Windows users can download `beam.exe` in the appropriate ZIP.
See the [installation guide](https://github.com/baytonorg/beam-cli-releases#readme)
for manual installation, checksums, platforms and uninstall steps.

Create a personal access token in BEAM's **My Account** area. Use the API origin
for the deployment, not the web console URL or a URL ending in `/internal/api/v1`:

```sh
beam auth login --profile personal --host https://YOUR_API_ORIGIN
beam auth status
beam context
beam whoami --json
beam devices list
```

Paste the PAT at the hidden prompt. The CLI verifies it, saves it in macOS
Keychain, Windows Credential Manager or Linux Secret Service, and records the
current environment/group. Linux needs a Secret Service on the session bus. No
plaintext credential fallback is used. Browser/device-code login is future work.

A PAT can access your memberships within that deployment. It does not give new
permissions or carry between separate developer and production deployments. For a
fixed group or CI job, use a service token instead. To read a token from a secret
manager, pipe its output to `auth login --token-stdin`; the token is not a flag value.

## Context and profiles

Use profiles to save logins for different API origins:

```sh
beam auth login --profile development --host https://YOUR_DEV_API_ORIGIN
beam profile list
beam profile use personal
beam --profile development devices list
```

Selecting a profile changes local credential selection. Selecting an environment
or group changes Core's shared account context:

```sh
beam environments list --all
beam environments current
beam environments use ENVIRONMENT_ID --allow-context-switch
beam groups list --all
beam groups use GROUP_ID --allow-context-switch
beam groups current
beam context
```

`use` also accepts the alias `switch`. Interactive switches require confirmation;
add `--dry-run` to preview or `--yes` to approve without a prompt. A verified
switch updates the selected saved profile's expected IDs. Service accounts cannot
switch. A PAT switch also affects your browser and other PATs for the same user.
Separate profiles or PATs do not provide independent parallel account contexts.

The global `--group` and `--environment` flags are **assertions**, not filters or
switches. They require Core's active IDs to match before resource operations:

```sh
beam --group EXPECTED_GROUP_ID --environment EXPECTED_ENVIRONMENT_ID devices list
```

If your browser already switched context, inspect and explicitly adopt it locally:

```sh
beam auth status --json
beam context
beam context refresh --dry-run
beam context refresh
```

Refresh changes local saved expectations only. Explicit environment-variable/flag
assertions still have to match; refresh requires a saved keyring profile. If an
environment token supplies credentials, a switch returns new IDs instead of
rewriting a saved profile: update your assertions yourself. After a failed switch,
inspect `context` before retrying because the server might already have switched.

## Change previews and validation

Named writes accept `--dry-run` and `--yes`. With a terminal attached, omit both
to see a preview and answer `Continue? [y/N]`:

```sh
beam groups update GROUP_ID --name "Field tablets" --dry-run
beam groups update GROUP_ID --name "Field tablets"
```

A rename preview includes current and proposed values:

```text
PUT groups/GROUP_ID
Host: https://YOUR_API_ORIGIN
Group: CURRENT_GROUP_ID
Environment: ENVIRONMENT_ID
Update the displayed fields.
  /name: "Field devices" -> "Field tablets"
Continue? [y/N]
```

Only `y` or `yes` approves. Blank input, EOF or another answer cancels without
submitting the target request. `--dry-run` prints a redacted JSON plan and does not
submit the change, but may authenticate and read current values. Headless writes
need `--yes`. Input read from stdin also needs `--yes` or `--dry-run`, so JSON
cannot answer its own confirmation prompt.

Named updates show comparable current fields where an ordinary read exists;
creations show proposed fields. Device commands and deletion identify the targets
and requested action. They cannot predict final device state. Recognised secrets
and opaque managed configurations are redacted in previews.

Required flags, non-empty IDs/names, email syntax, input types and unknown fields
are checked locally for named forms. For example, this fails with exit 2 before
credential lookup because `--parent` is missing:

```sh
beam groups create --name "Field devices" --dry-run
```

Core still checks permissions, membership and state-dependent requirements. Named
forms accept either field flags **or** `--file request.json`, not both. Request
files contain writable fields, not API response envelopes. Use files for complex
payloads; do not build escaped JSON with `printf`.

The CLI rechecks context and relevant target fields after an interactive approval.
Core has no atomic conditional-write contract, so a final race remains. `--yes`
bypasses interactive review. Writes are not automatically retried; after a network
failure, inspect the resource before repeating a potentially completed operation.

## Finding and reading resources

Lists show one page by default. Add `--all` for every page or select a page:

```sh
beam devices list --search Samsung
beam devices list --page 2 --per-page 50
beam devices list --all --json
beam devices show DEVICE_ID
beam policies list --all
beam users list --all
beam groups show GROUP_ID
```

`show` emits nested JSON even without `--json`. A one-page JSON list preserves
Core's `data`, `links` and `meta`; `--all --json` returns combined `data` with
`meta.count` and `meta.pages_fetched`. All-pages reads default to at most 100,000
items (`--max-items`) and 64 MiB. They do not provide a point-in-time snapshot.

Discover filters and sortable fields through entity metadata:

```sh
beam entities meta device
beam devices list --filter android_policy_id=POLICY_ID
beam entities list deviceApplication --scope 'device:id|DEVICE_ID' --json
beam entities list auditLog --all --json
```

`--search`, `--filter KEY=VALUE`, `--sort FIELD` and `--direction asc|desc` are
checked against metadata. Repeated filters need different keys; use a JSON array
as the value for supported multi-select filters. Nested JSON values can express
date ranges. Known unsupported scope combinations and metadata-unsupported
search/filter/sort options fail. Other generic entity scopes are forwarded with
a warning; Core may ignore a scope it does not implement. Roles and
environments have a server-fixed page size and refuse `--per-page`.

Entity `--scope` is implementation-specific. It does not switch account context
or prove the response is scoped correctly. Verify IDs before acting on them.

## Policy editing

Use this workflow to edit configuration, name or description:

```sh
beam policies list
beam policies get POLICY_ID --output policy.json
# Open policy.json in your editor and change config, name or description.
beam policies validate --file policy.json
beam policies diff POLICY_ID --file policy.json
beam policies put POLICY_ID --file policy.json --dry-run
beam policies put POLICY_ID --file policy.json
```

`get` is an alias of `export`; `put` and `push` are aliases of `apply`. An export
is a `beam-policy/v2` document with `id`, `group_id`, `updated_at`, `base_sha256`,
`name`, `description` and an editable `config` object. Keep the identity, timestamp
and fingerprint unchanged. The fingerprint identifies the original server state,
not your edited configuration. Export into a fresh file to start over.

Do not feed `policies show` output to `put`. It is an API response, not the editable
document. Local `validate` checks the document structure; it does not validate all
AMAPI policy semantics. Core performs policy validation when applying.

Apply refuses a mismatched target/group or a stale base, including server changes
within the same timestamp second. It preserves lifecycle, inheritance, template,
administrator-lock and per-device-policy flags. Unchanged documents send no write.
Core rejects empty configuration updates, so applying an empty `config` is refused
locally. If Core normalises the result, a mismatch returns the saved document and
`residual_changes` with exit 8. Inspect that result before editing again.

Exports preserve large integer values, create a new file and refuse to overwrite
one. Unix permissions are 0600; Windows inherits destination-folder permissions,
so choose a protected folder there. Policies can contain credentials. Updating an active policy can
affect managed devices; a successful save does not establish device application.

## Policy lifecycle

```sh
beam policies types
beam policies metadata
beam api describe policies.store
beam policies create --file new-policy.json --dry-run
beam policies create --file new-policy.json
beam policies clone --file clone-policy.json
beam policies update POLICY_ID --file policy-fields.json
beam policies delete POLICY_ID --dry-run
```

Creation needs `name`, `group_id` and a valid `deployment_scenario` from Core. Use
`api describe policies.policyClone` for the clone request schema. These commands accept
Core request objects, rather than exported `beam-policy/v2` documents. Partial
`update` preserves omitted writable fields and supports lifecycle fields beyond
the guarded editor workflow. Core rejects immutable conversions and deletion of
policies associated with devices. Use guarded `put` for ordinary config editing.

## Managed configurations

Managed app configuration is part of the policy's application entry. Export the
policy, then inspect the application matching its package name. This optional
`jq` example extracts Managed Info's configuration:

```sh
beam policies get POLICY_ID --output policy.json
jq '.config.applications[]? | select(.packageName == "org.bayton.managedinfo") | .managedConfiguration' policy.json
```

To find the assigned policy, first inspect `beam devices show DEVICE_ID`. Then edit
the matching entry in the complete exported document and use `validate`, `diff`
and `put` above. Preserve the rest of the application and policy. Do not push only
the extracted managed-configuration object. This reads the assigned policy's
configuration; it does not prove a device has received or applied it.

## Devices

```sh
beam devices show DEVICE_ID
beam devices rename DEVICE_ID --name "Warehouse tablet"
beam devices assign-group DEVICE_ID GROUP_ID --dry-run
beam devices assign-group DEVICE_ID GROUP_ID
beam devices assign-policy DEVICE_ID POLICY_ID
beam devices sync DEVICE_ID
```

Group assignment requires an authorised group with the same enterprise bind.
The target group/policy is positional; global `--group` still asserts your current
account context. For other writable fields, use `devices update` with a request
file, for example:

```json
{"state": "DISABLED", "disabled_reason": "Held for inspection"}
```

```sh
beam devices update DEVICE_ID --file device-fields.json --dry-run
```

This request disables the device if applied. `devices delete DEVICE_ID` and
`devices wipe DEVICE_ID` both request deletion of the managed device through AMAPI.
`delete` then removes the Core record; `wipe` retains it marked `WIPED`. Device
effects depend on ownership and AMAPI behaviour. Device deletion is not just local
inventory cleanup. Preview either operation and review the target before approving.

## Device commands

```sh
beam devices command lock DEVICE_ID
beam devices command reboot DEVICE_ID --dry-run
beam devices command reboot DEVICE_ID
```

Available named commands are `lock`, `reboot`, `reset-password`,
`set-lost-mode-active`, `set-lost-mode-inactive`, `add-esim`, `remove-esim`,
`relinquish-ownership`, `request-device-info` and `clear-app-data`. Some need JSON
parameters. Inspect the request schema before preparing the file:

```sh
beam api describe deviceCommand.clearAppData
beam devices command clear-app-data DEVICE_ID --file clear-app-data.json --dry-run
beam devices command raw DEVICE_ID --file command.json --dry-run
```

For `clear-app-data.json`, the published request shape is:

```json
{"packageName": "com.example.app"}
```

Clearing app data removes that app's stored data if executed. `raw` requires a
Core command body containing its type. Parameters and support depend on Core,
AMAPI and the device. An accepted response is not evidence of completed execution.

## Bulk and dynamic actions

Discover the same action definitions and required fields the web console uses:

```sh
beam devices actions
beam entities meta device
beam entities action device lock --id DEVICE_ID --id SECOND_DEVICE_ID --dry-run
beam devices action assign_policy --id DEVICE_ID --file action-fields.json --dry-run
```

Action names and additional fields come from the deployment's metadata. A request
file supplies the action-specific fields; repeat `--id` for explicit targets.
Do not use a guessed `all` target: typed actions refuse the legacy literal
`ids: "all"` because backend implementations differ. Other entity actions use
`entities action ENTITY ACTION` with the same explicit-ID workflow.

Non-empty per-target errors produce exit 9 and retain structured results. Some
targets may already have changed. Review those results before retrying any subset.

## Groups and users

```sh
beam groups create --name "Field devices" --parent PARENT_GROUP_ID --dry-run
beam groups create --name "Field devices" --parent PARENT_GROUP_ID
beam groups update GROUP_ID --name "Field tablets" --description "Shared tablets"
beam groups update GROUP_ID --enforce-mfa
beam groups update GROUP_ID --enforce-mfa=false
```

Creation requires both name and parent. Named updates preserve omitted fields;
`--description ""` clears the description. Reparenting is blocked until Core can
safely rebuild permission ancestry. `groups delete` explains the backend gap and
sends no deletion request.

```sh
beam users list
beam roles list
beam users invite --email person@example.com --role ROLE_ID --target-group GROUP_ID
beam users add --first-name Pat --last-name Example --email person@example.com --role ROLE_ID
beam users show USER_ID
beam users update USER_ID --first-name Patrick
beam users set-role USER_ID --role ROLE_ID
```

`users add` aliases `users create` and invites to the active group. `users invite`
targets the explicitly supplied group. Both can send invitation email. Core checks
the role and membership; a role ID is required to avoid an implicit admin default.
Email changes use Core's confirmation flow. Password fields require a request
file: omit unchanged password fields rather than supplying null/empty values.

Removal has different scopes:

| Command | Effect |
| --- | --- |
| `users remove USER_ID` | Removes environment access through the web entity action |
| `users delete-account USER_ID` | Deletes the user account |
| Remove membership in only one group | Not currently supported by Core |

Use `--dry-run` to review the intended removal before choosing a command.

## Roles and tokens

```sh
beam roles permissions
beam roles get ROLE_ID
beam roles create --name operators --label "Operators" --permission device_view --permission policy_view
beam roles update ROLE_ID --label "Device operators"
beam roles update ROLE_ID --permission device_view --dry-run
beam roles update ROLE_ID --clear-permissions --dry-run
beam roles delete ROLE_ID --dry-run
```

Use permission names from `roles permissions`. Repeated `--permission` replaces
the complete permission list; it does not append. `--clear-permissions` removes
every permission. Core enforces authority and system-role restrictions.

```sh
beam tokens personal list
beam tokens personal create --name "Local script" --output new-pat.json
beam tokens personal revoke TOKEN_ID --dry-run
beam tokens service list
beam tokens service create --name "Inventory job" --target-group GROUP_ID --role ROLE_ID --output service-token.json
beam tokens service revoke TOKEN_ID --dry-run
```

Creation returns the plaintext credential once. `--output` protects a newly created
result file and refuses to overwrite an existing file. Unix mode is 0600; use a
protected folder on Windows. Without a private output destination, results can
appear in terminal output. Service accounts cannot mint either token type, even
with an administrator role.

Service creation supports `--expires-at YYYY-MM-DD` (UTC) or future RFC3339, or
`--no-expiry`. These cannot be combined. Omitting both leaves expiry to Core.
Token revocation is a server action; `auth logout --profile NAME` only removes the
local profile/keyring credential and does not revoke the token.

## Enrolment

```sh
beam enrollment-tokens list
beam enrollment-tokens create --name "One-time enrolment" --policy POLICY_ID --target-group GROUP_ID --days 1 --output enrolment.json
beam enrollment-tokens get TOKEN_ID --dry-run
beam enrollment-tokens get TOKEN_ID --output token-details.json
beam enrollment-tokens delete TOKEN_ID --dry-run
```

Creation defaults to one-time use and personal usage disallowed. Use
`--one-time=false` for a reusable token. `--personal-usage` takes
`PERSONAL_USAGE_ALLOWED`, `PERSONAL_USAGE_DISALLOWED` or
`PERSONAL_USAGE_DISALLOWED_USERLESS`. `--target-group` selects the receiving group.

Creation/details contain enrolment credentials. Lists redact QR credentials unless
`--include-credentials` is explicit. The detail GET can change expiry after an
upstream failure, so it also requires confirmation. List is the ordinary read-only
discovery path. Raw API/catalogue calls retain the same unsafe-read guard.

## Workflows and settings

Find workflows through the entity interface, then use named commands:

```sh
beam entities list workflow --all --json
beam workflows get WORKFLOW_ID
beam api describe workflow.store
beam workflows create --file workflow.json --dry-run
beam workflows update WORKFLOW_ID --file workflow-changes.json
beam workflows assign-devices WORKFLOW_ID DEVICE_ID
beam workflows assign-groups WORKFLOW_ID GROUP_ID
beam workflows unassign-devices WORKFLOW_ID DEVICE_ID --dry-run
beam workflows unassign-groups WORKFLOW_ID GROUP_ID --dry-run
```

Request files use Core's `name`, `description`, `triggers`, `conditions` and
`actions` fields. Partial updates preserve omitted fields and existing trigger IDs.
For example, `workflow-changes.json` can contain:

```json
{"name": "Warehouse workflow"}
```

Assignments take one device/group target per command. Dynamic entity actions can
offer additional bulk operations, depending on metadata.

```sh
beam settings general get
beam settings contact-info get
beam settings account get
beam settings general put --file general-settings.json --dry-run
beam settings contact-info put --file contact-settings.json --dry-run
beam settings account put --file account-settings.json --dry-run
```

Settings writes send the supplied JSON as-is, so prepare writable fields from the
appropriate request schema rather than blindly saving the GET response. Find
operation IDs with `beam api operations --search settings`, then use `api describe`.
Account settings can invalidate browser sessions and change remember-me state.

Environment creation is also exposed as `beam environments create --file
environment.json`. Inspect `api describe environments.store` and preview first.

## Reports and BQL

All versions in this guide support asynchronous application inventory requests:

```sh
beam reports create applications
beam reports get applications
```

Creation deliberately requests a background refresh; `get` reads its status.
That status command does not download a report file. `applications` is the
supported asynchronous report type in the captured backend.

**The following exports require 0.7**, not the current public 0.5 installer:

```sh
beam reports list
beam reports device-inventory --output inventory.csv
beam reports spl-posture > patch-posture.csv
beam reports spl-risk > patch-risk.csv
beam reports update-state > update-state.csv
beam reports update-pending > update-pending.csv
beam reports enrolment-trend > enrolments.csv
beam reports estate-summary > estate.csv
beam reports applications > applications.csv
beam reports application org.bayton.managedinfo > app-summary.csv
beam reports application-versions org.bayton.managedinfo --stale-days 7 > versions.csv
beam reports application-devices org.bayton.managedinfo --version-code 1331 > app-devices.csv
beam reports schema
beam reports query --query 'entity(device|device_name,manufacturer,model) limit(50)' > query.csv
beam reports query --query-file query.bql --output query.csv
```

CSV records go to stdout; diagnostics/freshness notes go to stderr. `--json`
instead emits a structured document with records and scope metadata. `--output`
creates a new file and refuses overwrites. Shell `>` overwrites its destination
before the CLI runs and uses your shell's file permissions.

Reports read the active group/environment. Application inventory uses the latest
completed background snapshot and does not refresh it automatically. Other app
reports use reported version/device data with potentially different freshness.
Missing inventory does not prove an app is absent. Named BQL is read-only and does
not require `--yes`; generic API POST requests still require confirmation.

See [report definitions](reports.md) for CSV layout, patch/update calculations,
freshness, pagination limits, BQL limits and credential redaction.

## API access

Discover the captured OpenAPI operations and inspect request schemas locally:

```sh
beam api operations --search roles
beam api describe roles.store
beam api call roles.show --param role=ROLE_ID
beam api policies/types
beam api entities/device/data --field per_page=10
```

For a write, prepare a request file from the schema and review the plan:

```sh
beam api call user.updateRole --param user=USER_ID --input role-assignment.json --dry-run
beam api call user.updateRole --param user=USER_ID --input role-assignment.json
```

For example, `role-assignment.json` contains:

```json
{"role_id": "ROLE_ID"}
```

Raw `api PATH` accepts `--method` (`-X`), repeatable `--field KEY=VALUE`,
`--input FILE` (`-` for stdin). Paths are relative to
`/internal/api/v1`, without leading slash, URL or embedded query string.
`api call` supplies the method/path from the operation ID and accepts repeatable
`--param NAME=VALUE` for path parameters and `--output FILE` for a new result file
(0600 on Unix; protect the destination folder on Windows).
Raw `api PATH` writes to stdout; redirect it to a protected destination when
needed. Both emit API JSON.

The catalogue covers 122 operations, including enterprise binding, licensing,
statistics, applications, activity, query and account/session routes beyond the
named helpers. [API coverage](api-coverage.md) lists every operation. Captured
schemas can lag the deployed server; Core remains authoritative.

Writes and known unsafe reads require confirmation. Account switches additionally
need `--allow-context-switch`; raw switches do not repin saved profiles, so prefer
named `environments use`/`groups use`. Public catalogue operations do not receive
your saved bearer token. Raw public calls need `--anonymous`. Public browser
login endpoints do not establish a CLI profile or import browser cookies.

Raw calls do not add the guarded policy editor's fingerprint, merge or read-back
checks. Responses can include credentials; use private output destinations.

## Automation and output

Inject credentials through your runner's secret manager/environment, rather than
putting tokens in scripts or command-line arguments:

```text
BEAM_HOST=https://YOUR_API_ORIGIN
BEAM_TOKEN=<injected by secret manager>
BEAM_GROUP=<expected active group ID>
BEAM_ENVIRONMENT=<optional expected environment ID>
```

These are configuration names, not literal values to paste into a script.
`BEAM_TOKEN` overrides a saved token. Supply `BEAM_HOST` or `BEAM_TOKEN_HOST` to
bind environment credentials to their destination. Flags override matching
environment variables, which override saved metadata. Changing hosts cannot reuse
another host's saved credential.

Headless writes require the expected group and `--yes`. Use fixed-group service
tokens for parallel jobs. `BEAM_PROFILE` selects a profile; `BEAM_CONFIG_DIR`
isolates local metadata. Tokens are never saved in `config.json`.

```sh
beam devices list --all --json | jq '.data[] | {id, device_name}'
beam groups update GROUP_ID --name "Field tablets" --dry-run
beam groups update GROUP_ID --name "Field tablets" --yes
beam --timeout 60s devices list --all --json
```

Data goes to stdout; prompts, warnings and pagination hints go to stderr.
`--timeout` applies to each HTTP request, not the entire multi-page operation.
Ctrl-C cancels requests. `--output` creates a new result file with private Unix
permissions; a failed write can retain a partial result if the server action
already completed, so inspect errors and server state before retrying.

| Exit | Meaning |
| --- | --- |
| 0 | Success, including a declined interactive confirmation |
| 1 | General, transport or server failure |
| 2 | Invalid arguments/input or missing confirmation/context assertion |
| 3 | Authentication failed (HTTP 401) |
| 4 | Permission denied (HTTP 403) |
| 5 | Not found (HTTP 404) |
| 6 | Conflict or failed precondition (HTTP 409/412) |
| 7 | Server validation failure (HTTP 422) |
| 8 | Policy saved but returned editable values differ from the request |
| 9 | Entity action errors or partial failure |
| 130 | Cancelled |

## Shell completion

**Automatic installation requires 0.7**, currently a source/local build. Run:

```sh
beam completion install
```

The installer detects the shell that launched BEAM, falling back to your `SHELL`
environment variable. It installs completion for your user and configures startup
automatically. Open a new terminal and type `beam ` followed by Tab. To activate
in your existing terminal, run the exact activation command printed by the
installer. A child process cannot load functions into the shell that launched it.

Choose a shell explicitly, inspect planned files, or get structured output:

```sh
beam completion install --shell zsh
beam completion install --dry-run
beam completion install --shell powershell --dry-run --json
```

This is local setup and needs no BEAM login or `--yes`. `--dry-run` performs
detection and validation but writes no files. An unknown shell fails with guidance
to choose `--shell`; it does not guess from the operating system alone.

| Shell | Automatic setup |
| --- | --- |
| Zsh | Adds a managed block to `${ZDOTDIR:-HOME}/.zshrc`, initialises `compinit` if needed, and loads the generated script |
| Bash | Adds a managed block to `.bashrc` and the first existing `.bash_profile`, `.bash_login` or `.profile`; creates `.bash_profile` only if none exists, so both login and non-login terminals load completion |
| Fish | Writes `${XDG_CONFIG_HOME:-~/.config}/fish/completions/beam.fish`, which Fish loads automatically |
| PowerShell | Queries the selected PowerShell executable for `$PROFILE.CurrentUserAllHosts` and adds a managed block there, including redirected profile locations |

Zsh, Bash and PowerShell scripts are saved under
`${XDG_DATA_HOME:-~/.local/share}/beam/completions/`. Zsh honours an exported
`ZDOTDIR`. Explicit XDG directory variables must be absolute. PowerShell must be
installed and on PATH; native Windows users should use PowerShell. The installer
does not change PowerShell execution policy if it prevents loading profiles.

Bash requires the `bash-completion` package. The installer finds and loads its
standard Linux/Homebrew startup script. If the dependency is missing, it stops
before changing files and asks you to install it through your package manager.

Existing files are backed up beside their targets as `NAME.beam-backup-*` before
replacement. Unrelated startup text, UTF-8 BOMs and line endings are retained, and
symlinked startup files keep their links. Existing Unix startup modes are
preserved, and new files/backups use 0600 on Unix. On Windows, replacements and
backups inherit destination-folder permissions; existing file-specific ACLs are
not copied, so use a protected folder. Existing startup files must be UTF-8 text; unsupported encodings or broken
BEAM markers stop setup before changes. Custom completion files at the destination
are not overwritten.

Repeat `beam completion install` after upgrading. Unchanged files are left alone;
the BEAM block is updated in place and does not accumulate duplicate entries.
To undo setup, remove that block and its generated script; Fish needs only its
generated `beam.fish` removed. Backups contain the original files if restoration
is needed.

The existing `beam completion bash`, `zsh`, `fish` and `powershell` commands still
**print a script** rather than install it. In older releases or for temporary
Zsh setup, load the generated output into your shell yourself:

```zsh
autoload -Uz compinit && compinit
source <(beam completion zsh)
```

Running `beam completion zsh` alone prints the script into the terminal. This is
expected generator output and does not enable tab completion by itself.

## Updates and troubleshooting

Rerun the installer to upgrade. Profiles and keyring credentials are retained.
**From 0.6**, you can also run `beam update check` or `beam update check --json`.
Normal interactive stable builds check public release metadata with a one-second
deadline and cache success for 24 hours. New-version notices go to stderr at most
once per newer version per day. No automatic binary installation occurs.

Automatic checks skip JSON, pipes, CI, help/version, completion, dry runs and
development/prerelease builds. Set `BEAM_NO_UPDATE_CHECK=1` or
`NO_UPDATE_NOTIFIER=1` to disable them. `BEAM_CACHE_DIR` overrides the update cache.
Checks do not send BEAM credentials or account metadata. Version 0.5 needs a manual
upgrade before update checks become available.

| Problem | Check or next step |
| --- | --- |
| `beam: command not found` | Add your installation directory to `PATH`; verify with its absolute executable path |
| Unknown command from this guide | Check `beam --version`; automatic completion setup and CSV/BQL helpers require 0.7, update checks 0.6 |
| No host configured | Log in with `--host` set to your API origin, or inject `BEAM_HOST` |
| Keyring unavailable | Use the correct logged-in OS session/Secret Service; for headless jobs inject a service token |
| HTTP 401 | Check token validity, expiry and API deployment; login again or replace the injected secret |
| HTTP 403 | Check your role, membership and whether the operation is allowed for service accounts |
| Context mismatch | Inspect `auth status` and `context`. For a saved profile, review and refresh local expectations. With `BEAM_TOKEN`, correct `BEAM_GROUP`/`BEAM_ENVIRONMENT` or explicit flag assertions. Named switches also require the starting assertions to match |
| Required flag/unknown field error | Use command `--help`; choose named fields or a writable request file, not both |
| Policy stale/base mismatch | Export a fresh document to a new file, reapply your intended edit and compare again |
| Output file already exists | Choose a new file; shell redirection overwrites but does not provide CLI file protection |
| Exit 8 or 9 | Inspect retained result and server state; some changes may already have occurred |
| Timeout/network failure after write | Inspect the target before retrying; submission may have reached Core |
| Group deletion or single-group user detach unavailable | These need a new Core contract; the CLI cannot provide them alone |

For help, include the CLI version, OS, failing command with placeholders and the
redacted error in a [documentation/distribution issue](https://github.com/baytonorg/beam-cli-releases/issues).
Do not attach tokens, enrolment credentials or unredacted managed configurations.
