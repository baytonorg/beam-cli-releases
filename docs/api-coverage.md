# API coverage

[Documentation index](index.md) | [User guide](user-guide.md#api-access)

This page covers the current source. Native CSV/application/BQL report helpers
need 0.7; the public installer currently provides 0.5.0. Generic API/catalogue
access exists in 0.5. See the [version table](index.md#choose-the-right-version).

This is a source-contract audit, not a claim that every operation succeeded on a
live deployment. The deployed documentation remains subject to Core issue #896.

Core revision: `5aa1afe`. OpenAPI: `3.1.0`. Captured operations: **122**.
Every listed method/path is cross-checked against Core's registered routes. Fixture
tests invoke every operation through `beam api call`, checking method, path, query
encoding and public/authenticated credential handling. They do not prove backend
schema acceptance, all permission combinations, Google AMAPI outcomes or device
completion. Selected developer reads and dry runs are recorded separately.

## Management workflows

| Area | CLI coverage | Backend boundary |
| --- | --- | --- |
| API tokens | Personal/service list, create and revoke; private result files | Core denies token creation by service accounts, including administrator-role accounts |
| Groups | List/show/create/update | No deletion endpoint or entity action; Core #898. Named updates block unsafe reparenting pending Core #900 |
| Users | List/show/create/invite/update/set-role/remove environment access/delete account | Single-group membership removal is missing; #898. Account deletion is a separate action |
| Roles | List/get/permissions/create/update/delete | Core enforces custom/system-role and authority restrictions |
| Policies | Get/edit/put with base fingerprint and response verification; create/clone/update/delete | Atomic conditional writes require Core support; per-device conversion remains immutable |
| Devices | Read/update/group/policy assignment/rename/sync/delete/wipe and all published command endpoints | Submission does not establish device completion |
| Web entity actions | Metadata discovery and action invocation with explicit IDs, including bulk arrays | Typed commands refuse legacy literal `ids: all`; Core action closures do not uniformly implement it |
| Workflows/settings/reports | Named read/write, assignment and Flare CSV report helpers | Read/merge/write helpers and report pagination are not atomic; see [report definitions](reports.md) |
| Enterprise/licensing/applications/statistics/activities/query | Full catalogue and generic API invocation | Request schemas and permissions remain Core-authoritative |
| Environments | Named paginated list/current/create/use plus catalogue operations | Published deletion currently returns HTTP 501 |
| Account/session bootstrap | Public catalogue operations and explicit anonymous transport | Cookies are not imported into CLI profiles; device login is Core #897 |

Other than the explicit named safeguards, raw API/catalogue calls send the request
the user supplies. They do not add the guarded policy document's stale-value checks
or infer safe bulk targets. Known unsafe reads and context switches are still
guarded centrally. Raw responses can contain credentials.

## Published operation catalogue

Use `beam api describe OPERATION` for request schemas and their bundled components.
Use `beam api call OPERATION --param NAME=VALUE --input request.json --yes` for a
write, or omit input/confirmation for an ordinary read. Public operations never
receive a saved bearer credential. Core errors and restrictions are not bypassed.

| Operation ID | Method | Relative path | Access | Known boundary |
| --- | --- | --- | --- | --- |
| `activities.index` | GET | `activities` | Authenticated |  |
| `v1.config` | GET | `app-config` | Public |  |
| `installedApplication.index` | GET | `applications` | Authenticated |  |
| `installedApplication.show` | GET | `applications/{packageName}` | Authenticated |  |
| `installedApplication.devices` | GET | `applications/{packageName}/devices` | Authenticated |  |
| `v1.statistics.statistics.applicationVersions_0.applications.package.versions` | GET | `applications/{package}/versions` | Authenticated |  |
| `userInviteAcceptance.store` | POST | `auth/accept-invite` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `login.identify` | POST | `auth/identify` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `login.login` | POST | `auth/login` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `v1.logout` | POST | `auth/logout` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `magicLink.retrieve` | POST | `auth/magic-link` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `check-magic-link` | GET | `auth/magic-link/validate/{token}` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `register.store` | POST | `auth/register` | Public | Public account/session endpoint. Cookies are not imported into saved CLI profiles; normal CLI login remains token-based until Core #897. |
| `devices.index` | GET | `devices` | Authenticated |  |
| `deviceActivity.index` | GET | `devices/activities` | Authenticated |  |
| `deviceLocation.index` | GET | `devices/locations` | Authenticated |  |
| `devices.destroy` | DELETE | `devices/{device}` | Authenticated |  |
| `devices.show` | GET | `devices/{device}` | Authenticated |  |
| `devices.update` | PUT | `devices/{device}` | Authenticated |  |
| `deviceActivity.show` | GET | `devices/{device}/activities` | Authenticated |  |
| `deviceCommand.store` | POST | `devices/{device}/command` | Authenticated |  |
| `deviceCommand.addEsim` | POST | `devices/{device}/commands/add-esim` | Authenticated |  |
| `deviceCommand.clearAppData` | POST | `devices/{device}/commands/clear-app-data` | Authenticated |  |
| `deviceCommand.lockDevice` | POST | `devices/{device}/commands/lock` | Authenticated |  |
| `deviceCommand.rebootDevice` | POST | `devices/{device}/commands/reboot` | Authenticated |  |
| `deviceCommand.relinquishOwnership` | POST | `devices/{device}/commands/relinquish-ownership` | Authenticated |  |
| `deviceCommand.removeEsim` | POST | `devices/{device}/commands/remove-esim` | Authenticated |  |
| `deviceCommand.requestDeviceInfo` | POST | `devices/{device}/commands/request-device-info` | Authenticated |  |
| `deviceCommand.resetPassword` | POST | `devices/{device}/commands/reset-password` | Authenticated |  |
| `deviceCommand.setLostModeActive` | POST | `devices/{device}/commands/set-lost-mode-active` | Authenticated |  |
| `deviceCommand.setLostModeInactive` | POST | `devices/{device}/commands/set-lost-mode-inactive` | Authenticated |  |
| `v1.devices.device.destroy_0` | DELETE | `devices/{device}/delete` | Authenticated |  |
| `devices.deviceName` | PUT | `devices/{device}/rename-device` | Authenticated |  |
| `device.sync` | POST | `devices/{device}/sync` | Authenticated |  |
| `device.wipe` | DELETE | `devices/{device}/wipe` | Authenticated |  |
| `enrollment-tokens.index` | GET | `enrollment-tokens` | Authenticated |  |
| `enrollment-tokens.store` | POST | `enrollment-tokens` | Authenticated |  |
| `enrollment-tokens.destroy` | DELETE | `enrollment-tokens/{enrollmentToken}` | Authenticated |  |
| `enrollment-tokens.show` | GET | `enrollment-tokens/{enrollmentToken}` | Authenticated | This GET can change server state and requires --yes. |
| `entity.action` | POST | `entities/{key}/actions/{action}` | Authenticated |  |
| `entity.data` | GET | `entities/{key}/data` | Authenticated |  |
| `entity.meta` | GET | `entities/{key}/meta` | Authenticated |  |
| `environments.index` | GET | `environments` | Authenticated |  |
| `environments.store` | POST | `environments` | Authenticated |  |
| `environment.current` | GET | `environments/current` | Authenticated |  |
| `environment.switch` | POST | `environments/switch` | Authenticated | Changes shared account context; Core denies service accounts and saved group checks can refuse subsequent calls. |
| `environments.destroy` | DELETE | `environments/{environment}` | Authenticated | Core currently returns HTTP 501: environment deletion is not implemented. |
| `passwordResetLink.store` | POST | `forgot-password` | Public |  |
| `group.index` | GET | `groups` | Authenticated |  |
| `group.store` | POST | `groups` | Authenticated |  |
| `group.current` | GET | `groups/current` | Authenticated |  |
| `group.switch` | POST | `groups/switch` | Authenticated | Changes shared account context; Core denies service accounts and saved group checks can refuse subsequent calls. |
| `group.show` | GET | `groups/{group}` | Authenticated |  |
| `group.update` | PUT | `groups/{group}` | Authenticated |  |
| `enterprise.destroy` | DELETE | `groups/{group}/enterprise` | Authenticated |  |
| `enterprise.show` | GET | `groups/{group}/enterprise` | Authenticated |  |
| `enterprise.update` | PATCH | `groups/{group}/enterprise` | Authenticated |  |
| `enterprise.store` | POST | `groups/{group}/enterprise` | Authenticated |  |
| `enterprise.finalize` | PATCH | `groups/{group}/enterprise/finalize` | Authenticated |  |
| `web-token.create` | POST | `groups/{group}/web-token` | Authenticated |  |
| `licenseStripe.store` | POST | `licenses/stripe` | Authenticated |  |
| `licenses.show` | GET | `licenses/{license}` | Authenticated |  |
| `licenses.update` | PUT | `licenses/{license}` | Authenticated |  |
| `v1.me` | GET | `me` | Authenticated |  |
| `personalAccessToken.store` | POST | `me/token` | Authenticated | Core denies service accounts even when their group role is administrator. |
| `v1.emailChange` | POST | `password-change-confirmation/{emailChangeRequest}` | Authenticated |  |
| `play-applications.lookup` | GET | `play-applications/lookup/{packageName}` | Authenticated |  |
| `policies.index` | GET | `policies` | Authenticated |  |
| `policies.store` | POST | `policies` | Authenticated |  |
| `policies.policyClone` | POST | `policies/clone` | Authenticated |  |
| `policyMetadata.metadata` | GET | `policies/metadata` | Authenticated |  |
| `policyMetadata.substitutionVariables` | GET | `policies/substitution-variables` | Authenticated |  |
| `policyMetadata.types` | GET | `policies/types` | Authenticated |  |
| `policies.destroy` | DELETE | `policies/{policy}` | Authenticated |  |
| `policies.show` | GET | `policies/{policy}` | Authenticated |  |
| `policies.update` | PUT | `policies/{policy}` | Authenticated |  |
| `policyEnrollmentToken.index` | GET | `policies/{policy}/enrollment-tokens` | Authenticated |  |
| `bql.run` | POST | `query` | Authenticated |  |
| `bql.schema` | GET | `query/schema` | Authenticated |  |
| `report.show` | GET | `reports/{type}` | Authenticated |  |
| `report.store` | POST | `reports/{type}` | Authenticated |  |
| `passwordReset.store` | POST | `reset-password` | Public |  |
| `rolePermission.index` | GET | `role-permissions` | Authenticated |  |
| `roles.index` | GET | `roles` | Authenticated |  |
| `roles.store` | POST | `roles` | Authenticated |  |
| `roles.destroy` | DELETE | `roles/{role}` | Authenticated |  |
| `roles.show` | GET | `roles/{role}` | Authenticated |  |
| `roles.update` | PUT | `roles/{role}` | Authenticated |  |
| `serviceToken.store` | POST | `service-tokens` | Authenticated | Core denies service accounts even when their group role is administrator. |
| `accountSetting.show` | GET | `settings/account` | Authenticated |  |
| `accountSetting.update` | PUT | `settings/account` | Authenticated |  |
| `contactInfoSetting.show` | GET | `settings/contact-info` | Authenticated |  |
| `contactInfoSetting.update` | PUT | `settings/contact-info` | Authenticated |  |
| `generalSetting.show` | GET | `settings/general` | Authenticated |  |
| `generalSetting.update` | PUT | `settings/general` | Authenticated |  |
| `settingsMetadata.show` | GET | `settings/meta` | Authenticated |  |
| `v1.statistics.statistics.applicationVersions_0.statistics.applications.package.versions` | GET | `statistics/applications/{package}/versions` | Authenticated |  |
| `statistics.deviceStatistics` | GET | `statistics/devices` | Authenticated |  |
| `statistics.deviceHeartbeat` | GET | `statistics/heartbeat` | Authenticated |  |
| `statistics.licenseStatistics` | GET | `statistics/licenses` | Authenticated |  |
| `statistics.workflowStatistics` | GET | `statistics/workflows` | Authenticated |  |
| `user-invites.store` | POST | `user-invites` | Authenticated |  |
| `user.index` | GET | `users` | Authenticated |  |
| `user.store` | POST | `users` | Authenticated |  |
| `userActivity.index` | GET | `users/activities` | Authenticated |  |
| `twoFactor.destroy` | DELETE | `users/two-factor-authentication` | Authenticated |  |
| `twoFactor.store` | POST | `users/two-factor-authentication` | Authenticated |  |
| `twoFactor.update` | PUT | `users/two-factor-authentication` | Authenticated |  |
| `user.destroy` | DELETE | `users/{user}` | Authenticated | Deletes the user account, not a single group membership. |
| `user.show` | GET | `users/{user}` | Authenticated |  |
| `user.update` | PUT | `users/{user}` | Authenticated |  |
| `userActivity.show` | GET | `users/{user}/activities` | Authenticated |  |
| `userPassword.destroy` | DELETE | `users/{user}/password` | Authenticated |  |
| `userPassword.update` | PUT | `users/{user}/password` | Authenticated |  |
| `user.updateRole` | PATCH | `users/{user}/role` | Authenticated |  |
| `workflow.store` | POST | `workflows` | Authenticated |  |
| `workflow.show` | GET | `workflows/{workflow}` | Authenticated |  |
| `workflow.update` | PUT | `workflows/{workflow}` | Authenticated |  |
| `deviceWorkflow.destroy` | DELETE | `workflows/{workflow}/devices/{device}` | Authenticated |  |
| `deviceWorkflow.store` | POST | `workflows/{workflow}/devices/{device}` | Authenticated |  |
| `groupWorkflow.destroy` | DELETE | `workflows/{workflow}/groups/{group}` | Authenticated |  |
| `groupWorkflow.store` | POST | `workflows/{workflow}/groups/{group}` | Authenticated |  |
