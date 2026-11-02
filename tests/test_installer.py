"""Exercise the actual POSIX installer with local download fixtures, no network."""
import hashlib
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

INSTALLER = Path(__file__).resolve().parents[1] / "install.sh"
ROOT = "https://github.com/baytonorg/beam-cli-releases/releases"


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="beam-installer-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tools = self.root / "tools"
        self.tools.mkdir()
        self.fixtures = self.root / "fixtures"
        self.fixtures.mkdir()
        self.destination = self.root / "install with spaces" / "bin"
        self.log = self.root / "downloads"
        self.env = dict(os.environ, HOME=str(self.root / "home"),
                        PATH=str(self.tools) + os.pathsep + os.environ["PATH"],
                        FIXTURES=str(self.fixtures), DOWNLOAD_LOG=str(self.log),
                        TEST_OS="Linux", TEST_ARCH="x86_64")
        self.tool("uname", 'case "$1" in -s) echo "$TEST_OS";; -m) echo "$TEST_ARCH";; esac\n')
        # Fake only the network transport. tar, hashes and installation are real.
        curl = f'''#!{sys.executable}
import os, pathlib, shutil, sys
args = sys.argv[1:]
url = args[-1]
with open(os.environ['DOWNLOAD_LOG'], 'a') as log:
    log.write(url + '\\n')
if not url.startswith('{ROOT}/'):
    sys.exit(22)
source = pathlib.Path(os.environ['FIXTURES']) / url.rsplit('/', 1)[-1]
if not source.is_file():
    sys.exit(22)
shutil.copyfile(source, args[args.index('--output') + 1])
'''
        (self.tools / "curl").write_text(curl)
        (self.tools / "curl").chmod(0o755)
        (self.fixtures / "version.txt").write_text("0.5.0\n")
        self.archive()

    def tool(self, name, body):
        path = self.tools / name
        path.write_text("#!/bin/sh\n" + body)
        path.chmod(0o755)

    def archive(self, target_os="linux", arch="amd64", symlink=False):
        name = f"beam_0.5.0_{target_os}_{arch}.tar.gz"
        path = self.fixtures / name
        with tarfile.open(path, "w:gz") as archive:
            entry = tarfile.TarInfo("beam")
            if symlink:
                entry.type = tarfile.SYMTYPE
                entry.linkname = "/bin/sh"
                archive.addfile(entry)
            else:
                body = b"#!/bin/sh\necho 'beam version 0.5.0'\n"
                entry.size = len(body)
                entry.mode = 0o755
                archive.addfile(entry, io.BytesIO(body))
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.fixtures / "checksums_0.5.0.txt").write_text(f"{checksum}  {name}\n")
        return path

    def run_installer(self, *args, success=True, pipe=False):
        command = ["sh", "-s", "--"] if pipe else ["sh", str(INSTALLER)]
        result = subprocess.run(command + ["--bin-dir", str(self.destination), *args],
                                env=self.env, input=INSTALLER.read_text() if pipe else None,
                                text=True, capture_output=True)
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def test_latest_install_through_stdin(self):
        self.run_installer(pipe=True)
        executable = self.destination / "beam"
        self.assertTrue(os.access(executable, os.X_OK))
        self.assertEqual(subprocess.check_output([executable], text=True).strip(), "beam version 0.5.0")
        self.assertIn("/latest/download/version.txt", self.log.read_text())
        self.assertFalse(list(self.destination.glob(".beam-install.*")))

    def test_pinned_version_skips_latest(self):
        self.run_installer("--version", "v0.5.0")
        self.assertNotIn("/latest/", self.log.read_text())
        self.assertIn("/download/v0.5.0/", self.log.read_text())

    def test_all_platforms(self):
        for os_name, target in [("Darwin", "darwin"), ("Linux", "linux")]:
            for machine, arch in [("x86_64", "amd64"), ("arm64", "arm64"), ("aarch64", "arm64")]:
                with self.subTest(os=os_name, machine=machine):
                    self.env.update(TEST_OS=os_name, TEST_ARCH=machine)
                    self.archive(target, arch)
                    self.run_installer()
                    self.assertIn(f"beam_0.5.0_{target}_{arch}.tar.gz", self.log.read_text())

    def test_corrupt_archive_preserves_installed_binary(self):
        self.run_installer()
        existing = (self.destination / "beam").read_bytes()
        (self.fixtures / "beam_0.5.0_linux_amd64.tar.gz").write_bytes(b"corrupt")
        result = self.run_installer(success=False)
        self.assertIn("checksum mismatch", result.stderr)
        self.assertEqual((self.destination / "beam").read_bytes(), existing)

    def test_missing_or_duplicate_checksum(self):
        manifest = self.fixtures / "checksums_0.5.0.txt"
        valid = manifest.read_text()
        for contents in ["", valid + valid, "bad  beam_0.5.0_linux_amd64.tar.gz\n"]:
            with self.subTest(contents=contents):
                manifest.write_text(contents)
                self.run_installer(success=False)
                self.assertFalse(self.destination.exists())

    def test_network_failure_does_not_install(self):
        (self.fixtures / "beam_0.5.0_linux_amd64.tar.gz").unlink()
        self.run_installer(success=False)
        self.assertFalse(self.destination.exists())

    def test_bad_archive_does_not_install(self):
        path = self.archive()
        path.write_bytes(b"not a tar file")
        checksum = hashlib.sha256(path.read_bytes()).hexdigest()
        (self.fixtures / "checksums_0.5.0.txt").write_text(f"{checksum}  {path.name}\n")
        self.run_installer(success=False)
        self.assertFalse(self.destination.exists())

    def test_symlink_payload_rejected(self):
        self.archive(symlink=True)
        self.run_installer(success=False)
        self.assertFalse(self.destination.exists())

    def test_symlink_destination_rejected(self):
        self.destination.mkdir(parents=True)
        target = self.root / "original"
        target.write_text("unchanged")
        (self.destination / "beam").symlink_to(target)
        self.run_installer(success=False)
        self.assertEqual(target.read_text(), "unchanged")
        self.assertTrue((self.destination / "beam").is_symlink())

    def test_unsupported_platforms(self):
        for name, arch in [("MINGW64_NT", "x86_64"), ("FreeBSD", "arm64"), ("Linux", "i686")]:
            with self.subTest(os=name, arch=arch):
                self.env.update(TEST_OS=name, TEST_ARCH=arch)
                self.run_installer(success=False)
                self.assertFalse(self.log.exists())

    def test_invalid_version(self):
        for version in ["../0.5.0", "v0.5.0/evil", "-bad", "0.5", "0.5.0\n0.5.1"]:
            with self.subTest(version=version):
                self.run_installer("--version", version, success=False)
                self.assertFalse(self.log.exists())

    def test_invalid_latest_version(self):
        (self.fixtures / "version.txt").write_text("../../evil\n")
        self.run_installer(success=False)
        self.assertEqual(len(self.log.read_text().splitlines()), 1)

    def test_argument_validation(self):
        for args in [("--version",), ("--bin-dir",), ("--bin-dir", "relative"), ("--unknown",)]:
            with self.subTest(args=args):
                self.run_installer(*args, success=False)
                self.assertFalse(self.log.exists())

    def test_help_does_not_download(self):
        result = self.run_installer("--help")
        self.assertIn("Usage:", result.stdout)
        self.assertFalse(self.log.exists())


if __name__ == "__main__":
    unittest.main()
