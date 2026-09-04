"""Tests concerning the Flutter SDK the Flet CLI provisions and drives."""

import os
from types import SimpleNamespace
from unittest.mock import patch

from flet_cli.commands.flutter_base import BaseFlutterCommand
from flet_cli.commands.test import _flutter_path_env

# Built with the native separator so `Path(...).parent` round-trips on Windows
# too - `flet test` derives the bin dir from the executable path.
FLUTTER_BIN = os.path.join(os.sep + "opt", "flutter", "3.32.0", "bin")
FLUTTER_EXE = os.path.join(FLUTTER_BIN, "flutter")


def _install_flutter(monkeypatch, path_env, flutter_dir="/opt/flutter/3.32.0"):
    """
    Run `install_flutter()` with everything but the `PATH` maths stubbed out.

    Args:
        monkeypatch: pytest fixture used to set the inherited `PATH`.
        path_env: Value to expose as the process `PATH`.
        flutter_dir: Directory the managed SDK is pretended to live in.

    Returns:
        The `PATH` the command would hand to its Flutter subprocesses.
    """

    monkeypatch.setenv("PATH", path_env)
    cmd = SimpleNamespace(
        env={},
        verbose=0,
        required_flutter_version="3.32.0",
        emojis={"checkmark": ""},
        update_status=lambda *_, **__: None,
        log_stdout=lambda *_, **__: None,
        progress=None,
        run=lambda *_, **__: SimpleNamespace(returncode=0, stdout="", stderr=""),
        cleanup=lambda *_, **__: None,
    )
    with patch(
        "flet_cli.commands.flutter_base.install_flutter", return_value=flutter_dir
    ):
        BaseFlutterCommand.install_flutter(cmd)
    return cmd.env["PATH"]


def _test_command_path(monkeypatch, path_env, flutter_exe=FLUTTER_EXE):
    """
    Run `flet test`'s `_flutter_path_env()` against a given inherited `PATH`.

    Args:
        monkeypatch: pytest fixture used to set the inherited `PATH`.
        path_env: Value to expose as the process `PATH`.
        flutter_exe: Flutter executable the command resolved during provisioning.

    Returns:
        The `PATH` the command would hand to the pytest subprocess.
    """

    monkeypatch.setenv("PATH", path_env)
    cmd = SimpleNamespace(
        env={},
        flutter_exe=flutter_exe,
        flutter_packages_temp_dir=None,
        _serious_python_build_env=lambda: {},
    )
    return _flutter_path_env(cmd)["PATH"]


# ---------------------------------------------------------------------------
# PATH handed to Flutter subprocesses
# ---------------------------------------------------------------------------


class TestFlutterPathEnv:
    """How `install_flutter()` builds the `PATH` for Flutter subprocesses.

    It must only ever *prepend* the managed SDK. It used to also delete every
    `PATH` directory that merely contained a file named `flutter` or `dart` -
    which on a merged-`/usr` distro with `/usr/bin/dart` installed removed both
    `/usr/bin` and `/bin`, leaving the `#!/usr/bin/env bash` Flutter launcher
    with no shell to run: `/usr/bin/env: 'bash': No such file or directory`
    (#5118). Losing a system `bin` directory also strips `git`, `unzip` and
    `java`, which Flutter's own `shared.sh` requires.
    """

    def test_path_is_never_reduced(self, tmp_path, monkeypatch):
        """Every inherited entry survives, in its original order."""
        # Including the ones carrying a rival `flutter`/`dart` - and the
        # `.bat`/`.cmd` launcher variants the old filter also matched on.
        dirs = []
        for i, planted in enumerate(
            [None, "flutter", "dart", "flutter.bat", "dart.cmd", None]
        ):
            d = tmp_path / f"bin{i}"
            d.mkdir()
            if planted:
                (d / planted).write_text("#!/bin/sh\n")
            dirs.append(str(d))

        original = os.pathsep.join(dirs)
        result = _install_flutter(monkeypatch, original)
        assert result.split(os.pathsep)[1:] == dirs

    def test_system_bin_survives_a_dart_installed_next_to_bash(
        self, tmp_path, monkeypatch
    ):
        """#5118: `/usr/bin/dart` must not cost us `/usr/bin` - and with it `bash`."""
        system_bin = tmp_path / "usr" / "bin"
        system_bin.mkdir(parents=True)
        (system_bin / "dart").write_text("#!/bin/sh\n")
        (system_bin / "flutter").write_text("#!/bin/sh\n")
        (system_bin / "bash").write_text("#!/bin/sh\n")

        result = _install_flutter(monkeypatch, str(system_bin))
        assert str(system_bin) in result.split(os.pathsep)

    def test_managed_sdk_is_first(self, monkeypatch):
        """Prepending is what makes a bare `flutter`/`dart` resolve to our SDK."""
        result = _install_flutter(monkeypatch, "/usr/bin", flutter_dir="/opt/flutter/x")
        assert result.split(os.pathsep)[0] == os.path.join("/opt/flutter/x", "bin")

    def test_empty_path_does_not_add_the_current_directory(self, monkeypatch):
        """A trailing separator means "current directory" - never emit one."""
        result = _install_flutter(monkeypatch, "")
        assert result == os.path.join("/opt/flutter/3.32.0", "bin")
        assert "" not in result.split(os.pathsep)


# ---------------------------------------------------------------------------
# PATH handed to the `flet test` subprocess
# ---------------------------------------------------------------------------


class TestFletTestPathEnv:
    """How `flet test` builds the `PATH` for the pytest subprocess it spawns.

    `_flutter_path_env()` prepends the provisioned SDK so the on-device run
    (`flutter test integration_test`) uses the same Flutter the build did. The
    prepend-only rule of `TestFlutterPathEnv` applies here for the same reason.
    """

    def test_managed_sdk_is_first(self, monkeypatch):
        """The provisioned SDK outranks any other Flutter on `PATH`."""
        result = _test_command_path(monkeypatch, "/usr/bin")
        assert result.split(os.pathsep)[0] == FLUTTER_BIN

    def test_path_is_never_reduced(self, monkeypatch):
        """Every inherited entry survives, in its original order."""
        dirs = ["/usr/local/bin", "/usr/bin", "/bin"]
        result = _test_command_path(monkeypatch, os.pathsep.join(dirs))
        assert result.split(os.pathsep)[1:] == dirs

    def test_empty_path_does_not_add_the_current_directory(self, monkeypatch):
        """A trailing separator means "current directory" - never emit one."""
        result = _test_command_path(monkeypatch, "")
        assert result == FLUTTER_BIN
        assert "" not in result.split(os.pathsep)

    def test_path_untouched_when_flutter_was_not_resolved(self, monkeypatch):
        """No provisioned SDK means nothing to prepend - leave `PATH` alone."""
        result = _test_command_path(monkeypatch, "/usr/bin", flutter_exe=None)
        assert result == "/usr/bin"
