# BEAM CLI documentation

Use `beam` to inspect your BEAM estate, edit policies, manage access, issue device
commands and automate the API from a terminal.

Start with the [user guide](user-guide.md). It explains the workflows and includes
commands you can adapt. The [command reference](command-reference.md) lists every
command, argument, alias and flag from the current CLI source.

## Choose the right version

Run `beam --version` before following an example. As of 2 November 2026:

| Version | Availability | Features |
| --- | --- | --- |
| 0.5.0 | Latest public installer/release | Authentication, context switching, policy editing, device commands, access management, enrolment, workflows, settings, API catalogue, previews and confirmation |
| 0.6 | Source feature, not yet a public release | Explicit update checks and interactive update notices |
| 0.7 | Source/local build, not yet a public release | Flare CSV reports, application statistics and named BQL exports, plus 0.6 features |

The guide covers 0.5 unless a section is labelled otherwise. The generated
reference covers 0.7. An example does not change which version the installer
provides. Check [published releases](https://github.com/baytonorg/beam-cli-releases/releases)
for newer binaries; `beam COMMAND --help` reflects your installed version.

## What can I do?

| I want to... | Commands | Read next |
| --- | --- | --- |
| Install, sign in or use a second API deployment | `auth`, `profile`, `whoami` | [Getting started](user-guide.md#getting-started) |
| Select an environment or group | `environments list/current/use`, `groups list/current/use`, `context` | [Context and profiles](user-guide.md#context-and-profiles) |
| Find devices, policies, users or groups | Resource `list/show`, `entities meta/list/data` | [Finding-and-reading resources](user-guide.md#finding-and-reading-resources) |
| Get a policy, edit its JSON and push it back | `policies get/validate/diff/put` | [Policy editing](user-guide.md#policy-editing) |
| Create, clone or delete a policy | `policies create/clone/update/delete/types/metadata` | [Policy lifecycle](user-guide.md#policy-lifecycle) |
| Read an app's managed configuration | Policy export and `config.applications` | [Managed configurations](user-guide.md#managed-configurations) |
| Rename, move, reassign or synchronise a device | `devices rename/assign-group/assign-policy/update/sync` | [Devices](user-guide.md#devices) |
| Lock, reboot, wipe or run another device command | `devices command`, `devices wipe/delete` | [Device commands](user-guide.md#device-commands) |
| Run a web-console action on several targets | `devices actions/action`, `entities action` | [Bulk and dynamic actions](user-guide.md#bulk-and-dynamic-actions) |
| Create or change a group | `groups create/update` | [Groups and users](user-guide.md#groups-and-users) |
| Invite a user, change their role or remove access | `users invite/add/update/set-role/remove/delete-account` | [Groups and users](user-guide.md#groups-and-users) |
| Create a role and choose permissions | `roles list/get/permissions/create/update/delete` | [Roles and tokens](user-guide.md#roles-and-tokens) |
| Create or revoke a PAT/service token | `tokens personal/service list/create/revoke` | [Roles and tokens](user-guide.md#roles-and-tokens) |
| Create an enrolment token and inspect its credentials | `enrollment-tokens list/create/get/delete` | [Enrolment](user-guide.md#enrolment) |
| Configure a workflow and assign it to devices/groups | `workflows create/get/update/assign-*/unassign-*` | [Workflows and settings](user-guide.md#workflows-and-settings) |
| Read or change account, contact or general settings | `settings account/contact-info/general get/put` | [Workflows and settings](user-guide.md#workflows-and-settings) |
| Request an application inventory refresh | `reports create/get applications` | [Reports and BQL](user-guide.md#reports-and-bql) |
| Export Flare estate/device reports as CSV (0.7) | `reports device-inventory/spl-risk/spl-posture/update-state/enrolment-trend/estate-summary/update-pending` | [Report definitions](reports.md) |
| Export app distribution, versions and devices (0.7) | `reports applications/application/application-versions/application-devices` | [Application reports](reports.md#applications) |
| Run BQL and write records to a file (0.7) | `reports query/schema` | [BQL](reports.md#bql) |
| Call another published endpoint or inspect its request schema | `api operations/describe/call`, `api PATH` | [API access](user-guide.md#api-access) |
| Script safely, use JSON or install shell completion | `--json`, `--yes`, `--dry-run`, `completion` | [Automation and output](user-guide.md#automation-and-output) |
| Check for an update (0.6) | `update check` | [Updates and troubleshooting](user-guide.md#updates-and-troubleshooting) |

## Before making a change

Interactive writes show the proposed change and ask for confirmation. Use
`--dry-run` to inspect a plan, or `--yes` for an intentional unattended write.
See [change previews and validation](user-guide.md#change-previews-and-validation).

The token's BEAM permissions still apply. A PAT uses the account's shared active
context, including the browser's context. Fixed-group service tokens suit parallel
automation. A successful device command means the server accepted it; device
execution can happen later.

## Known limits

Group deletion and removal of a user from only one group need backend support.
Environment deletion is published but returns HTTP 501 in the captured Core
contract. Browser/device-code CLI login is not available. Policy concurrency checks
are preflight checks, not atomic conditional writes.

The [API coverage audit](api-coverage.md) lists all 122 captured operations, their
access types and backend boundaries. Coverage is tied to Core revision `5aa1afe`;
it is not a guarantee that every endpoint works for every deployment or role.

## Documentation map

- [User guide and worked examples](user-guide.md)
- [Complete command and flag reference](command-reference.md)
- [CSV, application report and BQL definitions](reports.md)
- [API operation catalogue and coverage limits](api-coverage.md)
- [Installation, upgrades and downloads](https://github.com/baytonorg/beam-cli-releases#readme)
- [Report a documentation or distribution problem](https://github.com/baytonorg/beam-cli-releases/issues)
