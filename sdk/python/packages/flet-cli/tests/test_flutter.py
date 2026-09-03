"""Tests concerning the Flutter SDK the Flet CLI provisions and drives."""

import os
from types import SimpleNamespace
from unittest.mock import patch

from flet_cli.commands.flutter_base import BaseFlutterCommand


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
