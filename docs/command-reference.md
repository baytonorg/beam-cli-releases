# Command reference

[Documentation index](index.md) | [User guide](user-guide.md)

Generated from the 0.7 command tree. The public installer currently provides 0.5.0. `beam update` requires 0.6 or newer; CSV report exports, `reports list`, `reports query`, `reports schema` and `completion install` require 0.7 or newer. `reports create/get` also exist in 0.5. Use `beam --version` and your installed `--help` to confirm availability.

Arguments in capitals are placeholders. Flags shown under **Local flags** apply to that command; **Global flags** apply throughout the tree. Defaults are shown by the CLI's flag formatter. A flag appearing here does not imply permission or backend support. See the user guide for validation, request-file examples and backend gaps.

File flags described as private request mode 0600 on Unix. On Windows, files inherit destination-folder permissions; choose a protected folder for policy exports, tokens and raw responses.

## Contents

- [beam api](#beam-api): Call a relative console API endpoint
- [beam auth](#beam-auth): Authenticate with an API token
- [beam completion](#beam-completion): Generate the autocompletion script for the specified shell
- [beam context](#beam-context): Inspect actual server context, even when the saved assertion differs
- [beam devices](#beam-devices): Inspect BEAM devices
- [beam enrollment-tokens](#beam-enrollment-tokens): Inspect BEAM enrollment-tokens
- [beam entities](#beam-entities): Discover and invoke the same dynamic actions used by the web console
- [beam environments](#beam-environments): Inspect, switch and create environments
- [beam groups](#beam-groups): Inspect BEAM groups
- [beam help](#beam-help): Help about any command
- [beam policies](#beam-policies): Inspect BEAM policies
- [beam profile](#beam-profile): Select saved API profiles without switching server-side group context
- [beam reports](#beam-reports): Export Flare reports as CSV records or JSON
- [beam roles](#beam-roles): Inspect and manage custom roles and permissions
- [beam settings](#beam-settings): Read and update Core settings
- [beam tokens](#beam-tokens): Manage personal and group-scoped service API tokens
- [beam update](#beam-update): Check for a newer public CLI release
- [beam users](#beam-users): Inspect BEAM users
- [beam whoami](#beam-whoami): Show the authenticated account, role and permissions
- [beam workflows](#beam-workflows): Read, create, update and assign workflows

## Global flags

```text
      --environment string   Require this environment ID (or BEAM_ENVIRONMENT); never switches context
      --group string         Require this active group ID; never switches account context
      --host string          API origin (or BEAM_HOST); saved credentials are bound to their host
      --json                 Output JSON
      --profile string       Saved profile (or BEAM_PROFILE)
      --timeout duration     HTTP timeout per request (default 30s)
```

## beam

Manage BEAM from your terminal

BEAM command-line client. Use scoped service tokens for automation.
Credentials are stored in the OS keyring or supplied with BEAM_TOKEN.

User guide and command reference:
https://github.com/baytonorg/beam-cli-releases/blob/main/docs/index.md

```text
beam [flags]
```

Subcommands:

- [api](#beam-api): Call a relative console API endpoint
- [auth](#beam-auth): Authenticate with an API token
- [completion](#beam-completion): Generate the autocompletion script for the specified shell
- [context](#beam-context): Inspect actual server context, even when the saved assertion differs
- [devices](#beam-devices): Inspect BEAM devices
- [enrollment-tokens](#beam-enrollment-tokens): Inspect BEAM enrollment-tokens
- [entities](#beam-entities): Discover and invoke the same dynamic actions used by the web console
- [environments](#beam-environments): Inspect, switch and create environments
- [groups](#beam-groups): Inspect BEAM groups
- [help](#beam-help): Help about any command
- [policies](#beam-policies): Inspect BEAM policies
- [profile](#beam-profile): Select saved API profiles without switching server-side group context
- [reports](#beam-reports): Export Flare reports as CSV records or JSON
- [roles](#beam-roles): Inspect and manage custom roles and permissions
- [settings](#beam-settings): Read and update Core settings
- [tokens](#beam-tokens): Manage personal and group-scoped service API tokens
- [update](#beam-update): Check for a newer public CLI release
- [users](#beam-users): Inspect BEAM users
- [whoami](#beam-whoami): Show the authenticated account, role and permissions
- [workflows](#beam-workflows): Read, create, update and assign workflows

**Local flags**

```text
  -h, --help      help for beam
  -v, --version   version for beam
```

## beam api

Call a relative console API endpoint

```text
beam api PATH [flags]
```

Subcommands:

- [call](#beam-api-call): Invoke a published operation by ID (including public endpoints)
- [describe](#beam-api-describe): Show an operation's path parameters and request schema
- [operations](#beam-api-operations): List every operation in the captured Core OpenAPI contract

**Local flags**

```text
      --allow-context-switch   Permit explicit shared group/environment switching; saved group assertions remain pinned
      --anonymous              Call a public endpoint without a credential or account preflight
      --dry-run                Preview without sending any request
  -f, --field stringArray      Query parameter KEY=VALUE (repeatable)
  -h, --help                   help for api
      --input string           JSON request file, or - for stdin
  -X, --method string          HTTP method (default "GET")
      --yes                    Approve a mutating API request without prompting
```

**Examples**

```sh
  beam api policies/types
  beam api entities/device/data --field per_page=10
  beam api policies/ID --method PUT --input policy.json --yes
```

## beam api call

Invoke a published operation by ID (including public endpoints)

```text
beam api call OPERATION [flags]
```

**Local flags**

```text
      --allow-context-switch   Permit explicit shared account context changes
      --dry-run                Prepare the operation without sending any request
  -f, --field stringArray      Query parameter KEY=VALUE (repeatable)
  -h, --help                   help for call
      --input string           JSON request file, or - for stdin
  -o, --output string          New private output file, or - for stdout
      --param stringArray      Path parameter NAME=VALUE (repeatable)
      --yes                    Approve changes or a known unsafe read without prompting
```

**Examples**

```sh
  beam api call roles.show --param role=ROLE_ID
  beam api call user.updateRole --param user=USER_ID --input role.json --yes
```

## beam api describe

Show an operation's path parameters and request schema

```text
beam api describe OPERATION [flags]
```

**Local flags**

```text
  -h, --help   help for describe
```

## beam api operations

List every operation in the captured Core OpenAPI contract

```text
beam api operations [flags]
```

**Local flags**

```text
  -h, --help            help for operations
      --search string   Filter operation IDs, paths and summaries
```

## beam auth

Authenticate with an API token

```text
beam auth [flags]
```

Subcommands:

- [login](#beam-auth-login): Validate and save a token in the OS keyring
- [logout](#beam-auth-logout): Remove the selected local credential (does not revoke it on the server)
- [status](#beam-auth-status): Check authentication and the active group

**Local flags**

```text
  -h, --help   help for auth
```

## beam auth login

Validate and save a token in the OS keyring

```text
beam auth login [flags]
```

**Local flags**

```text
  -h, --help          help for login
      --token-stdin   Read the token from standard input instead of a hidden prompt
```

## beam auth logout

Remove the selected local credential (does not revoke it on the server)

```text
beam auth logout [flags]
```

**Local flags**

```text
  -h, --help   help for logout
```

## beam auth status

Check authentication and the active group

```text
beam auth status [flags]
```

**Local flags**

```text
  -h, --help   help for status
```

## beam completion

Generate the autocompletion script for the specified shell

Generate the autocompletion script for beam for the specified shell.
See each sub-command's help for details on how to use the generated script.


Use 'beam completion install' to detect your shell and configure completion automatically.
The bash, zsh, fish and powershell subcommands print scripts without installing them.

```text
beam completion [flags]
```

Subcommands:

- [bash](#beam-completion-bash): Generate the autocompletion script for bash
- [fish](#beam-completion-fish): Generate the autocompletion script for fish
- [install](#beam-completion-install): Detect your shell and install tab completion for your user
- [powershell](#beam-completion-powershell): Generate the autocompletion script for powershell
- [zsh](#beam-completion-zsh): Generate the autocompletion script for zsh

**Local flags**

```text
  -h, --help   help for completion
```

## beam completion bash

Generate the autocompletion script for bash

Generate the autocompletion script for the bash shell.

This script depends on the 'bash-completion' package.
If it is not installed already, you can install it via your OS's package manager.

To load completions in your current shell session:

	source <(beam completion bash)

To load completions for every new session, execute once:

#### Linux:

	beam completion bash > /etc/bash_completion.d/beam

#### macOS:

	beam completion bash > $(brew --prefix)/etc/bash_completion.d/beam

You will need to start a new shell for this setup to take effect.


```text
beam completion bash
```

**Local flags**

```text
  -h, --help              help for bash
      --no-descriptions   disable completion descriptions
```

## beam completion fish

Generate the autocompletion script for fish

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

	beam completion fish | source

To load completions for every new session, execute once:

	beam completion fish > ~/.config/fish/completions/beam.fish

You will need to start a new shell for this setup to take effect.


```text
beam completion fish [flags]
```

**Local flags**

```text
  -h, --help              help for fish
      --no-descriptions   disable completion descriptions
```

## beam completion install

Detect your shell and install tab completion for your user

Detect the parent shell (falling back to SHELL) and install user-scoped completion.
Supports Bash, Zsh, Fish and PowerShell. Existing startup files are backed up,
and only a BEAM-managed block is added or updated. No BEAM login is required.
Open a new terminal after installing, or run the activation command printed.
Bash requires the bash-completion package. Use --dry-run to inspect file paths.

```text
beam completion install [flags]
```

**Local flags**

```text
      --dry-run        Show planned file paths without changing files
  -h, --help           help for install
      --shell string   Override shell detection: bash, zsh, fish or powershell
```

**Examples**

```sh
  beam completion install
  beam completion install --shell zsh
  beam completion install --dry-run
```

## beam completion powershell

Generate the autocompletion script for powershell

Generate the autocompletion script for powershell.

To load completions in your current shell session:

	beam completion powershell | Out-String | Invoke-Expression

To load completions for every new session, add the output of the above command
to your powershell profile.


```text
beam completion powershell [flags]
```

**Local flags**

```text
  -h, --help              help for powershell
      --no-descriptions   disable completion descriptions
```

## beam completion zsh

Generate the autocompletion script for zsh

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

	source <(beam completion zsh)

To load completions for every new session, execute once:

#### Linux:

	beam completion zsh > "${fpath[1]}/_beam"

#### macOS:

	beam completion zsh > $(brew --prefix)/share/zsh/site-functions/_beam

You will need to start a new shell for this setup to take effect.


```text
beam completion zsh [flags]
```

**Local flags**

```text
  -h, --help              help for zsh
      --no-descriptions   disable completion descriptions
```

## beam context

Inspect actual server context, even when the saved assertion differs

```text
beam context [flags]
```

Subcommands:

- [refresh](#beam-context-refresh): Adopt the account's current context in this saved keyring profile, without switching Core

**Local flags**

```text
  -h, --help   help for context
```

## beam context refresh

Adopt the account's current context in this saved keyring profile, without switching Core

```text
beam context refresh [flags]
```

**Local flags**

```text
      --dry-run   Inspect the proposed local profile update without saving it
  -h, --help      help for refresh
      --yes       Adopt current server context in this local profile without prompting
```

## beam devices

Inspect BEAM devices

```text
beam devices [flags]
```

Subcommands:

- [action](#beam-devices-action): Run an entity action with explicit IDs and JSON fields
- [actions](#beam-devices-actions): Discover web entity actions and required fields
- [assign-group](#beam-devices-assign-group): Move a device to an authorised group with the same bind
- [assign-policy](#beam-devices-assign-policy): Assign a device to a policy
- [command](#beam-devices-command): Issue a device command through a published endpoint
- [delete](#beam-devices-delete): Delete a device from management; this can affect the managed device
- [list](#beam-devices-list): List resources with explicit pagination
- [rename](#beam-devices-rename): Rename a device with --name or --file
- [show](#beam-devices-show): Show one resource
- [sync](#beam-devices-sync): Request a device synchronisation
- [update](#beam-devices-update): Set device policy_id, group_id, state or disabled_reason
- [wipe](#beam-devices-wipe): Wipe a managed device

**Local flags**

```text
  -h, --help   help for devices
```

## beam devices action

Run an entity action with explicit IDs and JSON fields

```text
beam devices action ACTION [flags]
```

**Local flags**

```text
      --all              Unsupported: provide explicit IDs instead
      --dry-run          Prepare without executing
  -f, --file string      JSON fields, or - for stdin
  -h, --help             help for action
      --id stringArray   Target ID (repeat for a bulk selection)
      --yes              Approve action execution without prompting
```

## beam devices actions

Discover web entity actions and required fields

```text
beam devices actions [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for actions
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam devices assign-group

Move a device to an authorised group with the same bind

```text
beam devices assign-group ID GROUP_ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for assign-group
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices assign-policy

Assign a device to a policy

```text
beam devices assign-policy ID POLICY_ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for assign-policy
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command

Issue a device command through a published endpoint

```text
beam devices command [flags]
```

Subcommands:

- [add-esim](#beam-devices-command-add-esim): Request add-esim (acceptance does not prove device completion)
- [clear-app-data](#beam-devices-command-clear-app-data): Request clear-app-data (acceptance does not prove device completion)
- [lock](#beam-devices-command-lock): Request lock (acceptance does not prove device completion)
- [raw](#beam-devices-command-raw): Issue an arbitrary command body containing its type
- [reboot](#beam-devices-command-reboot): Request reboot (acceptance does not prove device completion)
- [relinquish-ownership](#beam-devices-command-relinquish-ownership): Request relinquish-ownership (acceptance does not prove device completion)
- [remove-esim](#beam-devices-command-remove-esim): Request remove-esim (acceptance does not prove device completion)
- [request-device-info](#beam-devices-command-request-device-info): Request request-device-info (acceptance does not prove device completion)
- [reset-password](#beam-devices-command-reset-password): Request reset-password (acceptance does not prove device completion)
- [set-lost-mode-active](#beam-devices-command-set-lost-mode-active): Request set-lost-mode-active (acceptance does not prove device completion)
- [set-lost-mode-inactive](#beam-devices-command-set-lost-mode-inactive): Request set-lost-mode-inactive (acceptance does not prove device completion)

**Local flags**

```text
  -h, --help   help for command
```

## beam devices command add-esim

Request add-esim (acceptance does not prove device completion)

```text
beam devices command add-esim ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for add-esim
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command clear-app-data

Request clear-app-data (acceptance does not prove device completion)

```text
beam devices command clear-app-data ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for clear-app-data
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command lock

Request lock (acceptance does not prove device completion)

```text
beam devices command lock ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for lock
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command raw

Issue an arbitrary command body containing its type

```text
beam devices command raw ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for raw
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command reboot

Request reboot (acceptance does not prove device completion)

```text
beam devices command reboot ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for reboot
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command relinquish-ownership

Request relinquish-ownership (acceptance does not prove device completion)

```text
beam devices command relinquish-ownership ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for relinquish-ownership
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command remove-esim

Request remove-esim (acceptance does not prove device completion)

```text
beam devices command remove-esim ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for remove-esim
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command request-device-info

Request request-device-info (acceptance does not prove device completion)

```text
beam devices command request-device-info ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for request-device-info
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command reset-password

Request reset-password (acceptance does not prove device completion)

```text
beam devices command reset-password ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for reset-password
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command set-lost-mode-active

Request set-lost-mode-active (acceptance does not prove device completion)

```text
beam devices command set-lost-mode-active ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for set-lost-mode-active
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices command set-lost-mode-inactive

Request set-lost-mode-inactive (acceptance does not prove device completion)

```text
beam devices command set-lost-mode-inactive ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for set-lost-mode-inactive
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices delete

Delete a device from management; this can affect the managed device

```text
beam devices delete ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for delete
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices list

List resources with explicit pagination

```text
beam devices list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam devices rename

Rename a device with --name or --file

```text
beam devices rename ID [flags]
```

**Local flags**

```text
      --dry-run         Prepare the request without sending a write
  -f, --file string     JSON request file, or - for stdin; alternative to field flags
  -h, --help            help for rename
      --name string     Name (required unless using --file)
  -o, --output string   New private output file, or - for stdout
      --yes             Approve this change without prompting
```

## beam devices show

Show one resource

```text
beam devices show ID [flags]
```

**Local flags**

```text
  -h, --help   help for show
```

## beam devices sync

Request a device synchronisation

```text
beam devices sync ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for sync
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices update

Set device policy_id, group_id, state or disabled_reason

```text
beam devices update ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for update
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam devices wipe

Wipe a managed device

```text
beam devices wipe ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for wipe
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam enrollment-tokens

Inspect BEAM enrollment-tokens

```text
beam enrollment-tokens [flags]
```

Aliases: `enrolment-tokens`.

Subcommands:

- [create](#beam-enrollment-tokens-create): Create an enrolment token for a policy
- [delete](#beam-enrollment-tokens-delete): Delete an enrolment token
- [get](#beam-enrollment-tokens-get): Read token details (can update expiry state)
- [list](#beam-enrollment-tokens-list): List resources with explicit pagination

**Local flags**

```text
  -h, --help   help for enrollment-tokens
```

## beam enrollment-tokens create

Create an enrolment token for a policy

```text
beam enrollment-tokens create [flags]
```

**Local flags**

```text
      --days int                Lifetime in days (default 1)
      --dry-run                 Preview without creating a credential
  -h, --help                    help for create
      --name string             Token name
      --one-time                Allow only one enrolment (default true)
  -o, --output string           New private output file, or - for stdout
      --personal-usage string   PERSONAL_USAGE_ALLOWED, PERSONAL_USAGE_DISALLOWED, or PERSONAL_USAGE_DISALLOWED_USERLESS (default "PERSONAL_USAGE_DISALLOWED")
      --policy string           Policy ID
      --target-group string     Group receiving the token (explicit, within the token's authorised scope)
      --yes                     Approve creation without prompting; output contains enrolment credentials
```

## beam enrollment-tokens delete

Delete an enrolment token

```text
beam enrollment-tokens delete ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for delete
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam enrollment-tokens get

Read token details (can update expiry state)

```text
beam enrollment-tokens get ID [flags]
```

**Local flags**

```text
      --dry-run             Preview without calling the state-changing endpoint
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam enrollment-tokens list

List resources with explicit pagination

```text
beam enrollment-tokens list [flags]
```

**Local flags**

```text
      --all                   Fetch all pages; JSON returns data and aggregate metadata
      --direction string      Sort direction: asc or desc (default "asc")
      --field stringArray     Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray    Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                  help for list
      --include-credentials   Include enrolment QR credentials in JSON output
      --max-items int         Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int              Page number (default 1)
      --per-page int          Results per page (1-200) (default 50)
      --scope string          Entity-specific scope (only supported by some Core entities; see README)
      --search string         Search using this entity's server-side search
      --sort string           Sortable field ID from entity metadata
```

## beam entities

Discover and invoke the same dynamic actions used by the web console

```text
beam entities [flags]
```

Subcommands:

- [action](#beam-entities-action): Run an entity action with explicit IDs and JSON fields
- [data](#beam-entities-data): Read entity data with --field page/per_page/filters
- [list](#beam-entities-list): List resources with explicit pagination
- [meta](#beam-entities-meta): Read entity fields, filters and action definitions

**Local flags**

```text
  -h, --help   help for entities
```

## beam entities action

Run an entity action with explicit IDs and JSON fields

```text
beam entities action KEY ACTION [flags]
```

**Local flags**

```text
      --all              Unsupported: provide explicit IDs instead
      --dry-run          Prepare without executing
  -f, --file string      JSON fields, or - for stdin
  -h, --help             help for action
      --id stringArray   Target ID (repeat for a bulk selection)
      --yes              Approve action execution without prompting
```

## beam entities data

Read entity data with --field page/per_page/filters

```text
beam entities data KEY [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for data
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam entities list

List resources with explicit pagination

```text
beam entities list KEY [flags]
```

**Local flags**

```text
      --all                   Fetch all pages; JSON returns data and aggregate metadata
      --direction string      Sort direction: asc or desc (default "asc")
      --field stringArray     Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray    Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                  help for list
      --include-credentials   Include enrolment QR credentials in JSON output
      --max-items int         Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int              Page number (default 1)
      --per-page int          Results per page (1-200) (default 50)
      --scope string          Entity-specific scope (only supported by some Core entities; see README)
      --search string         Search using this entity's server-side search
      --sort string           Sortable field ID from entity metadata
```

## beam entities meta

Read entity fields, filters and action definitions

```text
beam entities meta KEY [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for meta
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam environments

Inspect, switch and create environments

```text
beam environments [flags]
```

Subcommands:

- [create](#beam-environments-create): Create an environment
- [current](#beam-environments-current): Read the current environment
- [list](#beam-environments-list): List resources with explicit pagination
- [use](#beam-environments-use): Switch the account's active environment and update this saved profile

**Local flags**

```text
  -h, --help   help for environments
```

## beam environments create

Create an environment

```text
beam environments create [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for create
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam environments current

Read the current environment

```text
beam environments current [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for current
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam environments list

List resources with explicit pagination

```text
beam environments list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam environments use

Switch the account's active environment and update this saved profile

Switch Core's shared account context. This also affects browser sessions and other personal tokens. Requires interactive approval or --yes, plus --allow-context-switch. Service accounts cannot switch. The selected saved keyring profile is updated only after verification.

```text
beam environments use ENVIRONMENT_ID [flags]
```

Aliases: `switch`.

**Local flags**

```text
      --allow-context-switch   Allow a change that also affects browser sessions and other tokens
      --dry-run                Show the target request without switching or updating the profile
  -h, --help                   help for use
      --yes                    Approve the shared account context change without prompting
```

## beam groups

Inspect BEAM groups

```text
beam groups [flags]
```

Subcommands:

- [create](#beam-groups-create): Create a group under --parent (or group_id in --file)
- [current](#beam-groups-current): Read the active group
- [delete](#beam-groups-delete): Explain the missing Core group deletion capability
- [list](#beam-groups-list): List resources with explicit pagination
- [show](#beam-groups-show): Show one resource
- [update](#beam-groups-update): Update group fields, preserving omitted values
- [use](#beam-groups-use): Switch the account's active group and update this saved profile

**Local flags**

```text
  -h, --help   help for groups
```

## beam groups create

Create a group under --parent (or group_id in --file)

```text
beam groups create [flags]
```

**Local flags**

```text
      --description string   Description (empty clears it)
      --dry-run              Prepare the request without sending a write
      --enforce-mfa          Require MFA (use --enforce-mfa=false to disable)
  -f, --file string          JSON request file, or - for stdin; alternative to field flags
  -h, --help                 help for create
      --name string          Name (required unless using --file)
  -o, --output string        New private output file, or - for stdout
      --parent string        Parent group ID (required unless using --file)
      --yes                  Approve this change without prompting
```

## beam groups current

Read the active group

```text
beam groups current [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for current
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam groups delete

Explain the missing Core group deletion capability

```text
beam groups delete ID [flags]
```

**Local flags**

```text
  -h, --help   help for delete
      --yes    Does not enable the missing Core operation
```

## beam groups list

List resources with explicit pagination

```text
beam groups list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam groups show

Show one resource

```text
beam groups show ID [flags]
```

**Local flags**

```text
  -h, --help   help for show
```

## beam groups update

Update group fields, preserving omitted values

```text
beam groups update ID [flags]
```

**Local flags**

```text
      --description string   Description (empty clears it)
      --dry-run              Prepare the request without sending a write
      --enforce-mfa          Require MFA (use --enforce-mfa=false to disable)
  -f, --file string          JSON request file, or - for stdin; alternative to field flags
  -h, --help                 help for update
      --name string          Name
  -o, --output string        New private output file, or - for stdout
      --yes                  Approve this change without prompting
```

## beam groups use

Switch the account's active group and update this saved profile

Switch Core's shared account context. This also affects browser sessions and other personal tokens. Requires interactive approval or --yes, plus --allow-context-switch. Service accounts cannot switch. The selected saved keyring profile is updated only after verification.

```text
beam groups use GROUP_ID [flags]
```

Aliases: `switch`.

**Local flags**

```text
      --allow-context-switch   Allow a change that also affects browser sessions and other tokens
      --dry-run                Show the target request without switching or updating the profile
  -h, --help                   help for use
      --yes                    Approve the shared account context change without prompting
```

## beam help

Help about any command

Help provides help for any command in the application.
Simply type beam help [path to command] for full details.

```text
beam help [command] [flags]
```

**Local flags**

```text
  -h, --help   help for help
```

## beam policies

Inspect BEAM policies

```text
beam policies [flags]
```

Subcommands:

- [apply](#beam-policies-apply): Apply reviewed policy configuration, name and description
- [clone](#beam-policies-clone): Clone a policy through Core's clone endpoint
- [create](#beam-policies-create): Create a policy with Core's full request contract
- [delete](#beam-policies-delete): Delete a policy; Core rejects policies associated with devices
- [diff](#beam-policies-diff): Compare an exported policy with Core
- [export](#beam-policies-export): Export an editable policy document
- [list](#beam-policies-list): List resources with explicit pagination
- [metadata](#beam-policies-metadata): Read policy metadata
- [show](#beam-policies-show): Show one resource
- [types](#beam-policies-types): List policy types
- [update](#beam-policies-update): Update all Core-supported policy fields, preserving omitted values
- [validate](#beam-policies-validate): Validate the CLI policy document structure locally (not AMAPI semantics)

**Local flags**

```text
  -h, --help   help for policies
```

## beam policies apply

Apply reviewed policy configuration, name and description

```text
beam policies apply ID [flags]
```

Aliases: `put`, `push`.

**Local flags**

```text
      --dry-run       Fetch and display differences without sending a write
  -f, --file string   Exported policy document, or - for stdin
  -h, --help          help for apply
      --yes           Approve the policy update without prompting
```

## beam policies clone

Clone a policy through Core's clone endpoint

```text
beam policies clone [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for clone
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam policies create

Create a policy with Core's full request contract

```text
beam policies create [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for create
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam policies delete

Delete a policy; Core rejects policies associated with devices

```text
beam policies delete ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for delete
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam policies diff

Compare an exported policy with Core

```text
beam policies diff ID [flags]
```

**Local flags**

```text
  -f, --file string   Exported policy document, or - for stdin
  -h, --help          help for diff
```

## beam policies export

Export an editable policy document

```text
beam policies export ID [flags]
```

Aliases: `get`.

**Local flags**

```text
  -h, --help            help for export
  -o, --output string   New output file (mode 0600), or - for stdout
```

## beam policies list

List resources with explicit pagination

```text
beam policies list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam policies metadata

Read policy metadata

```text
beam policies metadata [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for metadata
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam policies show

Show one resource

```text
beam policies show ID [flags]
```

**Local flags**

```text
  -h, --help   help for show
```

## beam policies types

List policy types

```text
beam policies types [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for types
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam policies update

Update all Core-supported policy fields, preserving omitted values

```text
beam policies update ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for update
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam policies validate

Validate the CLI policy document structure locally (not AMAPI semantics)

```text
beam policies validate [flags]
```

**Local flags**

```text
  -f, --file string   Exported policy document, or - for stdin
  -h, --help          help for validate
```

## beam profile

Select saved API profiles without switching server-side group context

```text
beam profile [flags]
```

Subcommands:

- [list](#beam-profile-list)
- [use](#beam-profile-use)

**Local flags**

```text
  -h, --help   help for profile
```

## beam profile list



```text
beam profile list [flags]
```

**Local flags**

```text
  -h, --help   help for list
```

## beam profile use



```text
beam profile use NAME [flags]
```

**Local flags**

```text
  -h, --help   help for use
```

## beam reports

Export Flare reports as CSV records or JSON

Export Flare's estate, device and application report rows to stdout as CSV. Use --json for report data and scope metadata. These reads never generate or refresh an application snapshot automatically.

```text
beam reports [flags]
```

Subcommands:

- [application](#beam-reports-application): Application summary and version distribution (CSV by default)
- [application-devices](#beam-reports-application-devices): Devices reporting an application (CSV by default)
- [application-versions](#beam-reports-application-versions): Application version distribution (CSV by default)
- [applications](#beam-reports-applications): Application inventory (CSV by default)
- [create](#beam-reports-create): Request asynchronous report generation
- [device-inventory](#beam-reports-device-inventory): Device inventory (CSV by default)
- [enrolment-trend](#beam-reports-enrolment-trend): Enrolment trend (30 days) (CSV by default)
- [estate-summary](#beam-reports-estate-summary): Estate summary (CSV by default)
- [get](#beam-reports-get): Get the latest asynchronous report status
- [list](#beam-reports-list): List the available report exports
- [query](#beam-reports-query): Run a read-only BQL query and export CSV records
- [schema](#beam-reports-schema): Discover BQL entities, columns and filters
- [spl-posture](#beam-reports-spl-posture): Security patch posture (CSV by default)
- [spl-risk](#beam-reports-spl-risk): Security patch risk list (CSV by default)
- [update-pending](#beam-reports-update-pending): Update-pending devices (CSV by default)
- [update-state](#beam-reports-update-state): Device update state (CSV by default)

**Local flags**

```text
  -h, --help   help for reports
```

## beam reports application

Application summary and version distribution (CSV by default)

```text
beam reports application PACKAGE [flags]
```

**Local flags**

```text
  -h, --help             help for application
  -o, --output string    New output file (0600 on Unix), or - for stdout
      --stale-days int   Heartbeat age threshold (1-365 days) (default 7)
```

## beam reports application-devices

Devices reporting an application (CSV by default)

```text
beam reports application-devices PACKAGE [flags]
```

**Local flags**

```text
      --direction string      Sort direction: asc or desc (default "asc")
  -h, --help                  help for application-devices
      --max-items int         Maximum rows, with a separate 64 MiB input limit; exceeding either fails without partial records (default 100000)
  -o, --output string         New output file (0600 on Unix), or - for stdout
      --per-page int          Page size (1-100); all pages are exported (default 100)
      --search string         Filter using the same server search as Flare
      --sort string           Backend sort field
      --version-code string   Only devices reporting this version code; kept as text
```

## beam reports application-versions

Application version distribution (CSV by default)

```text
beam reports application-versions PACKAGE [flags]
```

**Local flags**

```text
  -h, --help             help for application-versions
  -o, --output string    New output file (0600 on Unix), or - for stdout
      --stale-days int   Heartbeat age threshold (1-365 days) (default 7)
```

## beam reports applications

Application inventory (CSV by default)

```text
beam reports applications [flags]
```

**Local flags**

```text
      --direction string   Sort direction: asc or desc (default "asc")
  -h, --help               help for applications
      --max-items int      Maximum rows, with a separate 64 MiB input limit; exceeding either fails without partial records (default 100000)
  -o, --output string      New output file (0600 on Unix), or - for stdout
      --per-page int       Page size (1-100); all pages are exported (default 100)
      --search string      Filter using the same server search as Flare
      --sort string        Backend sort field
      --type string        Application source filter
```

## beam reports create

Request asynchronous report generation

```text
beam reports create TYPE [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for create
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam reports device-inventory

Device inventory (CSV by default)

```text
beam reports device-inventory [flags]
```

**Local flags**

```text
  -h, --help            help for device-inventory
      --max-items int   Maximum rows, with a separate 64 MiB input limit; exceeding either fails without partial records (default 100000)
  -o, --output string   New output file (0600 on Unix), or - for stdout
      --per-page int    Page size (1-200); all pages are exported (default 200)
      --search string   Filter using the same server search as Flare
```

## beam reports enrolment-trend

Enrolment trend (30 days) (CSV by default)

```text
beam reports enrolment-trend [flags]
```

Aliases: `enrollment-trend`.

**Local flags**

```text
  -h, --help            help for enrolment-trend
  -o, --output string   New output file (0600 on Unix), or - for stdout
```

## beam reports estate-summary

Estate summary (CSV by default)

```text
beam reports estate-summary [flags]
```

**Local flags**

```text
  -h, --help            help for estate-summary
  -o, --output string   New output file (0600 on Unix), or - for stdout
```

## beam reports get

Get the latest asynchronous report status

```text
beam reports get TYPE [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam reports list

List the available report exports

```text
beam reports list [flags]
```

**Local flags**

```text
  -h, --help   help for list
```

## beam reports query

Run a read-only BQL query and export CSV records

```text
beam reports query [flags]
```

Aliases: `bql`.

**Local flags**

```text
  -h, --help                help for query
  -o, --output string       New output file (0600 on Unix), or - for stdout
      --query string        BQL query text
      --query-file string   Plain-text BQL file, or - for stdin
```

## beam reports schema

Discover BQL entities, columns and filters

```text
beam reports schema [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for schema
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam reports spl-posture

Security patch posture (CSV by default)

```text
beam reports spl-posture [flags]
```

**Local flags**

```text
  -h, --help            help for spl-posture
  -o, --output string   New output file (0600 on Unix), or - for stdout
```

## beam reports spl-risk

Security patch risk list (CSV by default)

```text
beam reports spl-risk [flags]
```

**Local flags**

```text
  -h, --help            help for spl-risk
      --max-items int   Maximum rows, with a separate 64 MiB input limit; exceeding either fails without partial records (default 100000)
  -o, --output string   New output file (0600 on Unix), or - for stdout
      --per-page int    Page size (1-200); all pages are exported (default 200)
      --search string   Filter using the same server search as Flare
```

## beam reports update-pending

Update-pending devices (CSV by default)

```text
beam reports update-pending [flags]
```

**Local flags**

```text
  -h, --help            help for update-pending
      --max-items int   Maximum rows, with a separate 64 MiB input limit; exceeding either fails without partial records (default 100000)
  -o, --output string   New output file (0600 on Unix), or - for stdout
      --per-page int    Page size (1-200); all pages are exported (default 200)
      --search string   Filter using the same server search as Flare
```

## beam reports update-state

Device update state (CSV by default)

```text
beam reports update-state [flags]
```

**Local flags**

```text
  -h, --help            help for update-state
  -o, --output string   New output file (0600 on Unix), or - for stdout
```

## beam roles

Inspect and manage custom roles and permissions

```text
beam roles [flags]
```

Subcommands:

- [create](#beam-roles-create): Create a custom role from name, label and permissions
- [delete](#beam-roles-delete): Delete a custom role (Core enforces restrictions)
- [get](#beam-roles-get): Show a role and its effective permissions
- [list](#beam-roles-list): List resources with explicit pagination
- [permissions](#beam-roles-permissions): List the permission catalogue
- [update](#beam-roles-update): Update role label, description and permissions

**Local flags**

```text
  -h, --help   help for roles
```

## beam roles create

Create a custom role from name, label and permissions

```text
beam roles create [flags]
```

**Local flags**

```text
      --clear-permissions        Explicitly replace permissions with an empty list
      --description string       Description (empty clears it)
      --dry-run                  Prepare the request without sending a write
  -f, --file string              JSON request file, or - for stdin; alternative to field flags
  -h, --help                     help for create
      --label string             Display label (required unless using --file)
      --name string              Name (required unless using --file)
  -o, --output string            New private output file, or - for stdout
      --permission stringArray   Permission key (repeat to set the complete list)
      --yes                      Approve this change without prompting
```

## beam roles delete

Delete a custom role (Core enforces restrictions)

```text
beam roles delete ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for delete
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam roles get

Show a role and its effective permissions

```text
beam roles get ID [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam roles list

List resources with explicit pagination

```text
beam roles list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam roles permissions

List the permission catalogue

```text
beam roles permissions [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for permissions
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam roles update

Update role label, description and permissions

```text
beam roles update ID [flags]
```

**Local flags**

```text
      --clear-permissions        Explicitly replace permissions with an empty list
      --description string       Description (empty clears it)
      --dry-run                  Prepare the request without sending a write
  -f, --file string              JSON request file, or - for stdin; alternative to field flags
  -h, --help                     help for update
      --label string             Display label
  -o, --output string            New private output file, or - for stdout
      --permission stringArray   Permission key (repeat to set the complete list)
      --yes                      Approve this change without prompting
```

## beam settings

Read and update Core settings

```text
beam settings [flags]
```

Subcommands:

- [account](#beam-settings-account)
- [contact-info](#beam-settings-contact-info)
- [general](#beam-settings-general)

**Local flags**

```text
  -h, --help   help for settings
```

## beam settings account



```text
beam settings account [flags]
```

Subcommands:

- [get](#beam-settings-account-get): Read settings
- [put](#beam-settings-account-put): Update settings from JSON

**Local flags**

```text
  -h, --help   help for account
```

## beam settings account get

Read settings

```text
beam settings account get [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam settings account put

Update settings from JSON

```text
beam settings account put [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for put
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam settings contact-info



```text
beam settings contact-info [flags]
```

Subcommands:

- [get](#beam-settings-contact-info-get): Read settings
- [put](#beam-settings-contact-info-put): Update settings from JSON

**Local flags**

```text
  -h, --help   help for contact-info
```

## beam settings contact-info get

Read settings

```text
beam settings contact-info get [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam settings contact-info put

Update settings from JSON

```text
beam settings contact-info put [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for put
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam settings general



```text
beam settings general [flags]
```

Subcommands:

- [get](#beam-settings-general-get): Read settings
- [put](#beam-settings-general-put): Update settings from JSON

**Local flags**

```text
  -h, --help   help for general
```

## beam settings general get

Read settings

```text
beam settings general get [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam settings general put

Update settings from JSON

```text
beam settings general put [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for put
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam tokens

Manage personal and group-scoped service API tokens

```text
beam tokens [flags]
```

Subcommands:

- [personal](#beam-tokens-personal): Manage personal API tokens
- [service](#beam-tokens-service): Manage service API tokens

**Local flags**

```text
  -h, --help   help for tokens
```

## beam tokens personal

Manage personal API tokens

```text
beam tokens personal [flags]
```

Subcommands:

- [create](#beam-tokens-personal-create): Create a token; output contains the one-time credential (Core denies service accounts)
- [list](#beam-tokens-personal-list): List resources with explicit pagination
- [revoke](#beam-tokens-personal-revoke): Revoke a token using the entity action

**Local flags**

```text
  -h, --help   help for personal
```

## beam tokens personal create

Create a token; output contains the one-time credential (Core denies service accounts)

```text
beam tokens personal create [flags]
```

**Local flags**

```text
      --dry-run         Prepare the request without sending a write
  -f, --file string     JSON request file, or - for stdin; alternative to field flags
  -h, --help            help for create
      --name string     Name (required unless using --file)
  -o, --output string   New private output file, or - for stdout
      --yes             Approve this change without prompting
```

## beam tokens personal list

List resources with explicit pagination

```text
beam tokens personal list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam tokens personal revoke

Revoke a token using the entity action

```text
beam tokens personal revoke ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for revoke
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam tokens service

Manage service API tokens

```text
beam tokens service [flags]
```

Subcommands:

- [create](#beam-tokens-service-create): Create a token; output contains the one-time credential (Core denies service accounts)
- [list](#beam-tokens-service-list): List resources with explicit pagination
- [revoke](#beam-tokens-service-revoke): Revoke a token using the entity action

**Local flags**

```text
  -h, --help   help for service
```

## beam tokens service create

Create a token; output contains the one-time credential (Core denies service accounts)

```text
beam tokens service create [flags]
```

**Local flags**

```text
      --dry-run               Prepare the request without sending a write
      --expires-at string     Future expiry: RFC3339 timestamp or YYYY-MM-DD (UTC)
  -f, --file string           JSON request file, or - for stdin; alternative to field flags
  -h, --help                  help for create
      --name string           Name (required unless using --file)
      --no-expiry             Create without expiry
  -o, --output string         New private output file, or - for stdout
      --role string           Role ID for the service account (required unless using --file)
      --target-group string   Group to scope the service token to (required unless using --file)
      --yes                   Approve this change without prompting
```

## beam tokens service list

List resources with explicit pagination

```text
beam tokens service list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam tokens service revoke

Revoke a token using the entity action

```text
beam tokens service revoke ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for revoke
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam update

Check for a newer public CLI release

```text
beam update [flags]
```

Subcommands:

- [check](#beam-update-check): Check the latest stable version without BEAM authentication

**Local flags**

```text
  -h, --help   help for update
```

## beam update check

Check the latest stable version without BEAM authentication

```text
beam update check [flags]
```

**Local flags**

```text
  -h, --help   help for check
```

## beam users

Inspect BEAM users

```text
beam users [flags]
```

Subcommands:

- [create](#beam-users-create): Invite a user to the active group (Core sends an invitation)
- [delete-account](#beam-users-delete-account): Delete the user account, not just environment membership
- [invite](#beam-users-invite): Invite a user to an explicit group_id
- [list](#beam-users-list): List resources with explicit pagination
- [remove](#beam-users-remove): Remove the user's environment access through the web entity action
- [set-role](#beam-users-set-role): Assign role_id within the active group
- [show](#beam-users-show): Show one resource
- [update](#beam-users-update): Update user details; email changes require Core's confirmation flow

**Local flags**

```text
  -h, --help   help for users
```

## beam users create

Invite a user to the active group (Core sends an invitation)

```text
beam users create [flags]
```

Aliases: `add`.

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --email string        Email address (required unless using --file)
  -f, --file string         JSON request file, or - for stdin; alternative to field flags
      --first-name string   First name (required unless using --file)
  -h, --help                help for create
      --last-name string    Last name (required unless using --file)
  -o, --output string       New private output file, or - for stdout
      --role string         Role ID (required unless using --file)
      --yes                 Approve this change without prompting
```

## beam users delete-account

Delete the user account, not just environment membership

```text
beam users delete-account ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for delete-account
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam users invite

Invite a user to an explicit group_id

```text
beam users invite [flags]
```

**Local flags**

```text
      --dry-run               Prepare the request without sending a write
      --email string          Email address (required unless using --file)
      --enforce-mfa           Require MFA (use --enforce-mfa=false to disable)
  -f, --file string           JSON request file, or - for stdin; alternative to field flags
      --first-name string     First name
  -h, --help                  help for invite
      --last-name string      Last name
  -o, --output string         New private output file, or - for stdout
      --role string           Role ID (required unless using --file)
      --target-group string   Group to invite into (required unless using --file)
      --yes                   Approve this change without prompting
```

## beam users list

List resources with explicit pagination

```text
beam users list [flags]
```

**Local flags**

```text
      --all                  Fetch all pages; JSON returns data and aggregate metadata
      --direction string     Sort direction: asc or desc (default "asc")
      --field stringArray    Additional query field KEY=VALUE, including nested filter fields
      --filter stringArray   Entity filter KEY=VALUE (repeatable; see API metadata for supported keys)
  -h, --help                 help for list
      --max-items int        Maximum rows retained by --all (also bounded to 64 MiB) (default 100000)
      --page int             Page number (default 1)
      --per-page int         Results per page (1-200) (default 50)
      --scope string         Entity-specific scope (only supported by some Core entities; see README)
      --search string        Search using this entity's server-side search
      --sort string          Sortable field ID from entity metadata
```

## beam users remove

Remove the user's environment access through the web entity action

```text
beam users remove ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for remove
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam users set-role

Assign role_id within the active group

```text
beam users set-role ID [flags]
```

**Local flags**

```text
      --dry-run         Prepare the request without sending a write
  -f, --file string     JSON request file, or - for stdin; alternative to field flags
  -h, --help            help for set-role
  -o, --output string   New private output file, or - for stdout
      --role string     Role ID within the active group (required unless using --file)
      --yes             Approve this change without prompting
```

## beam users show

Show one resource

```text
beam users show ID [flags]
```

**Local flags**

```text
  -h, --help   help for show
```

## beam users update

Update user details; email changes require Core's confirmation flow

```text
beam users update ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --email string        Email address
  -f, --file string         JSON request file, or - for stdin; alternative to field flags
      --first-name string   First name
  -h, --help                help for update
      --last-name string    Last name
  -o, --output string       New private output file, or - for stdout
      --remember-me         Remember-me setting (explicit true/false)
      --yes                 Approve this change without prompting
```

## beam whoami

Show the authenticated account, role and permissions

```text
beam whoami [flags]
```

**Local flags**

```text
  -h, --help   help for whoami
```

## beam workflows

Read, create, update and assign workflows

```text
beam workflows [flags]
```

Subcommands:

- [assign-devices](#beam-workflows-assign-devices): assign a workflow to/from devices
- [assign-groups](#beam-workflows-assign-groups): assign a workflow to/from groups
- [create](#beam-workflows-create): Create a workflow
- [get](#beam-workflows-get): Read a workflow
- [unassign-devices](#beam-workflows-unassign-devices): unassign a workflow to/from devices
- [unassign-groups](#beam-workflows-unassign-groups): unassign a workflow to/from groups
- [update](#beam-workflows-update): Update a workflow, preserving omitted triggers and their IDs

**Local flags**

```text
  -h, --help   help for workflows
```

## beam workflows assign-devices

assign a workflow to/from devices

```text
beam workflows assign-devices WORKFLOW_ID TARGET_ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for assign-devices
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam workflows assign-groups

assign a workflow to/from groups

```text
beam workflows assign-groups WORKFLOW_ID TARGET_ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for assign-groups
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam workflows create

Create a workflow

```text
beam workflows create [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for create
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam workflows get

Read a workflow

```text
beam workflows get ID [flags]
```

**Local flags**

```text
  -f, --field stringArray   Query parameter KEY=VALUE (repeatable)
  -h, --help                help for get
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve a state-changing read without prompting
```

## beam workflows unassign-devices

unassign a workflow to/from devices

```text
beam workflows unassign-devices WORKFLOW_ID TARGET_ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for unassign-devices
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam workflows unassign-groups

unassign a workflow to/from groups

```text
beam workflows unassign-groups WORKFLOW_ID TARGET_ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for unassign-groups
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```

## beam workflows update

Update a workflow, preserving omitted triggers and their IDs

```text
beam workflows update ID [flags]
```

**Local flags**

```text
      --dry-run             Prepare the request without sending a write
      --field stringArray   Query parameter KEY=VALUE (repeatable)
  -f, --file string         JSON request file, or - for stdin
  -h, --help                help for update
  -o, --output string       New private output file, or - for stdout
      --yes                 Approve this change without prompting
```
