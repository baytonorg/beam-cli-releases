# BEAM CLI

Official downloads for `beam`, the command-line client for BEAM device management.
This repository contains the installer, documentation and compiled releases. The
application source is maintained separately in a private repository.

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
archives contain the complete command guide in `README.md` and operation coverage
in `docs/api-coverage.md`.

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
