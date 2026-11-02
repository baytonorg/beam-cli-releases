# BEAM CLI

Official downloads for `beam`, the command-line client for BEAM device management.
This repository contains the installer, documentation and compiled releases. The
application source is maintained separately in a private repository.

**[Browse the complete documentation](docs/index.md)** for everything the CLI
can do. Start with the [worked user guide](docs/user-guide.md), or look up a
command in the [command and flag reference](docs/command-reference.md).

**Version status (2 November 2026):** the public installer currently provides
**0.5.0**. Automatic update notices require 0.6; automatic completion setup and
native CSV/application/BQL exports and the new MDM safeguards require 0.7. Those newer features are documented and available in source/local
builds, but are not yet published binaries. Check `beam --version` and the
[version table](docs/index.md#choose-the-right-version).

The upcoming safety build adds [bulk acknowledgement, destructive-action intent, enrolment preconditions and explicit secret output](docs/user-guide.md#mdm-safeguards). Those fixes are not included in the current public 0.5.0 download.

## What can I do with it?

| Area | Capabilities | Guide |
| --- | --- | --- |
| Authentication and context | PAT/service-token login, profiles, environments, group switching and context checks | [Get started](docs/user-guide.md#getting-started) |
| Policies | Export editable JSON, validate, diff and push; create, clone, update and delete | [Policy editing](docs/user-guide.md#policy-editing) |
| Managed configurations | Inspect and edit an app's complete configuration within an exported policy | [Managed configurations](docs/user-guide.md#managed-configurations) |
| Devices | Search/list/details, rename, assign group/policy, sync, delete and wipe | [Devices](docs/user-guide.md#devices) |
| Commands and bulk actions | Lock, reboot, password/lost-mode/eSIM/app-data commands and web entity actions with explicit targets | [Device commands](docs/user-guide.md#device-commands) |
| Groups and users | Create/update groups, invite/add users, change roles, remove environment access and delete accounts | [Groups and users](docs/user-guide.md#groups-and-users) |
| Roles and tokens | Discover permissions; create/update/delete roles; create/list/revoke personal and service tokens | [Roles and tokens](docs/user-guide.md#roles-and-tokens) |
| Enrolment | Create, inspect and delete one-time/reusable enrolment tokens | [Enrolment](docs/user-guide.md#enrolment) |
| Workflows and settings | Create/update workflows, assign/unassign devices/groups, read/write account/contact/general settings | [Workflows and settings](docs/user-guide.md#workflows-and-settings) |
| Reports | Request/check application inventory generation; from 0.7, export Flare reports, app distribution and BQL as CSV/JSON | [Reports and BQL](docs/user-guide.md#reports-and-bql) |
| API and automation | All 122 captured API operations, schemas, raw requests, JSON output, dry runs and shell completion | [API access](docs/user-guide.md#api-access) |

Commands still require your BEAM permissions and backend support. Group deletion,
single-group user detach and browser/device-code login need Core changes. See
[coverage and known limits](docs/api-coverage.md) rather than assuming every web
operation is implemented successfully by the backend.

## Install on macOS or Linux

```sh
curl -fsSL https://raw.githubusercontent.com/baytonorg/beam-cli-releases/main/install.sh | sh
```

The installer chooses the correct binary for macOS or Linux on x86-64 or ARM64,
verifies its SHA256 checksum, and installs to `~/.local/bin/beam`. It requires
`curl` or `wget`, `tar`, and a SHA256 tool (`sha256sum`, `shasum` or `openssl`).
Go, Node.js, GitHub authentication and sudo are not required. The installer does
not change your shell configuration or BEAM account settings.

If `~/.local/bin` is not on your PATH, add this to your shell configuration:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

Open a new terminal, then check the installation:

```sh
beam --version
beam --help
```

Pin a version or select a different installation directory:

```sh
curl -fsSL https://raw.githubusercontent.com/baytonorg/beam-cli-releases/main/install.sh | sh -s -- --version 0.5.0
curl -fsSL https://raw.githubusercontent.com/baytonorg/beam-cli-releases/main/install.sh | sh -s -- --bin-dir "$HOME/bin"
```

To inspect the installer first:

```sh
curl -fsSLo install-beam.sh https://raw.githubusercontent.com/baytonorg/beam-cli-releases/main/install.sh
less install-beam.sh
sh install-beam.sh
```

Each release also includes a snapshot of `install.sh`, `version.txt` and a checksum
manifest. SHA256 checks detect damaged or mismatched downloads; these releases are
not currently signed or notarised.

## Install on Windows or download manually

Choose an archive from [Releases](https://github.com/baytonorg/beam-cli-releases/releases/latest):

| System | Processor | Archive suffix |
| --- | --- | --- |
| macOS | Apple silicon | `darwin_arm64.tar.gz` |
| macOS | Intel | `darwin_amd64.tar.gz` |
| Linux | ARM64 | `linux_arm64.tar.gz` |
| Linux | x86-64 | `linux_amd64.tar.gz` |
| Windows | ARM64 | `windows_arm64.zip` |
| Windows | x86-64 | `windows_amd64.zip` |

Download the archive and `checksums_VERSION.txt`. Compare the archive's SHA256
using `shasum -a 256 ARCHIVE` on macOS, `sha256sum ARCHIVE` on Linux, or
`Get-FileHash -Algorithm SHA256 ARCHIVE.zip` in PowerShell. Extract it and put
`beam` or `beam.exe` in a directory on your PATH. Archives include the full command
guide, API coverage notes, licence and third-party notices. Windows binaries are
also currently unsigned.

## Sign in

Create a personal access token in BEAM's My Account area, then run:

```sh
beam auth login --profile personal --host https://YOUR_API_ORIGIN
beam auth status
beam context
```

Paste the token at the hidden prompt. It is verified with BEAM and stored in the
operating system's keyring: macOS Keychain, Windows Credential Manager, or Linux
Secret Service. Linux keyring authentication needs a Secret Service on the session
bus. There is no plaintext credential fallback. Browser/device-code login is not
yet available.

A personal token accesses the environments your user belongs to in that deployment,
with the permissions granted there. For headless automation, use a group-scoped
service token through your secret manager and the `BEAM_HOST`, `BEAM_TOKEN` and
`BEAM_GROUP` environment variables. Never put tokens in scripts or command arguments.

## Use BEAM

```sh
beam environments list --all
beam groups list
beam devices list
beam policies list
beam roles list
beam --help
```

Use `beam COMMAND --help` to explore flags and subcommands. Commands cover policies,
devices, groups, users, roles, API tokens, enrolment, workflows and generic API access.
Some operations depend on backend support and your account permissions. The
online [user guide](docs/user-guide.md) explains the workflows, while the
[command reference](docs/command-reference.md) lists every command and flag.
Release archives also contain a documentation snapshot for that release.

For a policy get-edit-put workflow:

```sh
beam policies get POLICY_ID --output policy.json
# Edit policy.json in your editor.
beam policies put POLICY_ID --file policy.json --dry-run
beam policies put POLICY_ID --file policy.json
```

Interactive writes show a preview and ask `Continue? [y/N]`. Use `--dry-run` to
inspect a plan, or `--yes` for intentional unattended writes. Treat device wipe,
deletion, credential output and account changes according to their impact.

Personal-token environment/group switches change the account context shared with
your browser and other personal tokens. Check `beam context` before writes and use
fixed-group service tokens for parallel automation.

## Enable shell completion

From **0.7** (currently a source/local build), run:

```sh
beam completion install
```

It detects your shell and configures completion automatically for future terminals.
For an already-open terminal, run the activation command it prints. Use
`--dry-run` to preview files or `--shell zsh` (also Bash, Fish or PowerShell) to
override detection. Repeat runs update the same BEAM block, preserve unrelated
settings and back up changed existing files. Bash needs `bash-completion`.

The current public 0.5 release has script generators only. Running
`beam completion zsh` prints a script; it does not install or enable it.
See [shell completion](docs/user-guide.md#shell-completion) for temporary setup,
paths, prerequisites and restoration.

## Upgrade and uninstall

Run the installer again to upgrade, or use `--version` to select an older release.
It replaces only the executable, retaining your saved profiles and keyring entries.
If an installation is managed by a package manager, use that package manager to
upgrade it. The installer refuses to replace a symbolic link.

To uninstall the default installation:

```sh
rm "$HOME/.local/bin/beam"
```

Use your chosen directory if you installed elsewhere. To remove a saved login,
run `beam auth logout --profile PROFILE` before uninstalling. Local logout does not
revoke the token on BEAM; revoke it in My Account if required.

## Support and licence

Report installer or distribution problems in this repository's
[issues](https://github.com/baytonorg/beam-cli-releases/issues), including the release
version, operating system and processor. Do not include tokens or credentials.

BEAM CLI is distributed under the [MIT licence](LICENSE). Third-party notices are
included in each archive. The application source repository remains private.
