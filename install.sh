#!/bin/sh
# Install an official BEAM CLI release. POSIX sh, no sudo or GitHub login required.
set -eu

main() (
    umask 077
    release_root=https://github.com/baytonorg/beam-cli-releases/releases
    version=latest
    bin_dir=${HOME:?HOME must be set}/.local/bin
    work_dir=
    staged_binary=

    fail() { printf 'beam installer: %s\n' "$*" >&2; exit 1; }
    # Invoked by the EXIT trap.
    # shellcheck disable=SC2329,SC2317
    cleanup() {
        [ -z "$staged_binary" ] || rm -f "$staged_binary"
        [ -z "$work_dir" ] || rm -rf "$work_dir"
    }
    trap cleanup EXIT
    trap 'exit 1' HUP INT TERM

    usage() {
        cat <<'EOF'
Usage: install.sh [--version VERSION] [--bin-dir DIRECTORY]

Install the latest stable BEAM CLI for macOS or Linux into ~/.local/bin.
  --version VERSION   Install a specific release, for example 0.5.0 or v0.5.0
  --bin-dir DIRECTORY Install into this directory (must be an absolute path)
  -h, --help          Show this help

Run again to upgrade. No sudo is used and shell startup files are not changed.
EOF
    }

    while [ "$#" -gt 0 ]; do
        case "$1" in
            --version|--bin-dir)
                [ "$#" -ge 2 ] || fail "$1 requires a value"
                [ -n "$2" ] || fail "$1 requires a value"
                case "$2" in --*) fail "$1 requires a value" ;; esac
                case "$1" in
                    --version) version=$2 ;;
                    --bin-dir) bin_dir=$2 ;;
                esac
                shift 2 ;;
            -h|--help) usage; exit 0 ;;
            *) fail "unknown argument: $1 (use --help)" ;;
        esac
    done
    case "$bin_dir" in /*) ;; *) fail '--bin-dir must be an absolute path' ;; esac

    case "$(uname -s)" in
        Darwin) target_os=darwin ;;
        Linux) target_os=linux ;;
        *) fail 'supported systems: macOS and Linux; download Windows ZIPs from GitHub Releases' ;;
    esac
    case "$(uname -m)" in
        x86_64|amd64) target_arch=amd64 ;;
        aarch64|arm64) target_arch=arm64 ;;
        *) fail 'supported processors: x86-64 and ARM64' ;;
    esac

    if command -v curl >/dev/null 2>&1; then
        download() { curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' --connect-timeout 15 --max-time 300 --retry 2 --output "$2" "$1"; }
    elif command -v wget >/dev/null 2>&1; then
        download() { wget --https-only --timeout=30 --tries=3 -q -O "$2" "$1"; }
    else
        fail 'install curl or wget first'
    fi
    if command -v sha256sum >/dev/null 2>&1; then
        digest() { sha256sum "$1" | awk '{print $1}'; }
    elif command -v shasum >/dev/null 2>&1; then
        digest() { shasum -a 256 "$1" | awk '{print $1}'; }
    elif command -v openssl >/dev/null 2>&1; then
        digest() { openssl dgst -sha256 "$1" | awk '{print $NF}'; }
    else
        fail 'install sha256sum, shasum or openssl first'
    fi
    for tool in tar awk grep mktemp chmod mv mkdir; do
        command -v "$tool" >/dev/null 2>&1 || fail "required command not found: $tool"
    done

    work_dir=$(mktemp -d "${TMPDIR:-/tmp}/beam-install.XXXXXX")
    if [ "$version" = latest ]; then
        download "$release_root/latest/download/version.txt" "$work_dir/version.txt" || fail 'could not discover the latest release'
        version=$(cat "$work_dir/version.txt")
    fi
    version=${version#v}
    case "$version" in ''|*[!0-9A-Za-z.-]*) fail 'invalid release version' ;; esac
    printf '%s\n' "$version" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z]+([.-][0-9A-Za-z]+)*)?$' || fail 'invalid release version'
    archive="beam_${version}_${target_os}_${target_arch}.tar.gz"
    download "$release_root/download/v$version/checksums_$version.txt" "$work_dir/checksums.txt" || fail 'could not download release checksums'
    expected=$(awk -v name="$archive" '$2 == name {count++; hash=$1} END {if (count == 1) print hash; else exit 1}' "$work_dir/checksums.txt") || fail 'release checksum is missing or duplicated'
    printf '%s\n' "$expected" | grep -Eq '^[0-9a-f]{64}$' || fail 'invalid release checksum'
    printf 'Downloading BEAM CLI %s for %s/%s...\n' "$version" "$target_os" "$target_arch"
    download "$release_root/download/v$version/$archive" "$work_dir/$archive" || fail 'could not download the release archive'
    actual=$(digest "$work_dir/$archive") || fail 'could not calculate archive checksum'
    [ "$actual" = "$expected" ] || fail 'checksum mismatch; nothing was installed'
    tar -xzf "$work_dir/$archive" -C "$work_dir" beam || fail 'could not extract the BEAM executable'
    [ -f "$work_dir/beam" ] || fail 'archive does not contain a regular BEAM executable'
    [ ! -L "$work_dir/beam" ] || fail 'archive executable is a symbolic link'

    mkdir -p "$bin_dir" || fail "could not create $bin_dir"
    [ ! -L "$bin_dir/beam" ] || fail 'destination is a symbolic link; upgrade it through its package manager or choose another --bin-dir'
    [ ! -e "$bin_dir/beam" ] || [ -f "$bin_dir/beam" ] || fail 'destination is not a regular file'
    staged_binary=$(mktemp "$bin_dir/.beam-install.XXXXXX") || fail "cannot write to $bin_dir; choose a writable --bin-dir"
    cat "$work_dir/beam" > "$staged_binary"
    chmod 0755 "$staged_binary"
    mv -f "$staged_binary" "$bin_dir/beam"
    staged_binary=
    printf 'Installed BEAM CLI %s to %s/beam\n' "$version" "$bin_dir"
    case ":${PATH:-}:" in
        *:"$bin_dir":*) printf 'Run: beam --version\n' ;;
        *) printf 'Add this directory to your PATH: %s\nThen run: beam --version\n' "$bin_dir" ;;
    esac
)

# Parse the entire script before starting installation when piped into sh.
main "$@"
