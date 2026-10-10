"""Assets directory handling in `flet run`.

`--assets` defaults to `"assets"`, resolved against the app's script directory,
whether or not the app has such a directory. Only a path set with `--assets` or
`FLET_ASSETS_DIR` is exported to the app process as `FLET_ASSETS_DIR`, which the
app treats as deliberate: it overrides `ft.run(assets_dir=...)`, and a missing
one is warned about. A defaulted directory that does not exist is dropped, so
nothing warns about a directory the user never chose. The app reports the
directory it resolved on a line of its own before the page URL, and `flet run`
opens the desktop window with it.
"""

import inspect
import io
import os
import subprocess
import sys
import threading
import types
from pathlib import Path

import pytest

from flet.app import DISPLAY_ASSETS_DIR_SUFFIX
from flet.utils import get_free_tcp_port
from flet_cli.cli import parse_command_line
from flet_cli.commands import run as run_module
from flet_cli.commands.run import resolve_assets_dir


class TestMissingDirectoryIsDropped:
    """Nothing is exported when the resolved directory is not there."""

    def test_defaulted_assets_dir_of_an_app_without_one(self, tmp_path):
        assert resolve_assets_dir(tmp_path, "assets") is None

    def test_missing_absolute_path(self, tmp_path):
        assert resolve_assets_dir(tmp_path, str(tmp_path / "nope")) is None

    def test_a_file_is_not_an_assets_dir(self, tmp_path):
        (tmp_path / "assets").write_text("not a directory")
        assert resolve_assets_dir(tmp_path, "assets") is None


class TestExistingDirectoryIsResolved:
    """A real directory is still found, and always returned absolute."""

    def test_relative_resolved_against_the_script_dir(self, tmp_path):
        (tmp_path / "assets").mkdir()
        resolved = resolve_assets_dir(tmp_path, "assets")
        assert resolved == str(tmp_path / "assets")
        assert Path(resolved).is_absolute()

    def test_custom_relative_name(self, tmp_path):
        (tmp_path / "media").mkdir()
        assert resolve_assets_dir(tmp_path, "media") == str(tmp_path / "media")

    def test_absolute_path_outside_the_script_dir(self, tmp_path):
        outside = tmp_path / "shared"
        outside.mkdir()
        app = tmp_path / "app"
        app.mkdir()
        assert resolve_assets_dir(app, str(outside)) == str(outside)


class TestOnlyADeliberateValueWarns:
    """The default is quiet when missing; anything else the user typed is not."""

    def test_default_is_silent(self, tmp_path, capsys):
        assert resolve_assets_dir(tmp_path, "assets") is None
        assert capsys.readouterr().out == ""

    def test_explicit_value_warns(self, tmp_path, capsys):
        assert resolve_assets_dir(tmp_path, "typo") is None
        out = capsys.readouterr().out
        assert "assets_dir does not exist" in out
        assert "typo" in out

    def test_explicit_value_that_exists_does_not_warn(self, tmp_path, capsys):
        (tmp_path / "media").mkdir()
        assert resolve_assets_dir(tmp_path, "media") is not None
        assert capsys.readouterr().out == ""


class TestUnset:
    """`None` and empty stay `None` without touching the filesystem."""

    def test_none(self, tmp_path):
        assert resolve_assets_dir(tmp_path, None) is None

    def test_empty_string(self, tmp_path):
        assert resolve_assets_dir(tmp_path, "") is None


@pytest.fixture
def handler_kwargs(monkeypatch, tmp_path):
    """
    Return a function that runs `flet run` on `tmp_path/main.py`.

    The returned function takes extra `flet run` arguments and returns the
    keyword arguments `flet run` created its `Handler` with.
    """

    monkeypatch.delenv("FLET_ASSETS_DIR", raising=False)

    def invoke(*argv):
        captured = {}
        monkeypatch.setattr(
            "flet.utils.pip.ensure_flet_desktop_package_installed", lambda: None
        )
        monkeypatch.setattr(
            "flet.utils.pip.install_flet_package",
            lambda name: pytest.fail(f"test tried to install {name!r}"),
        )
        real_signature = inspect.signature(run_module.Handler.__init__)

        class StubHandler:
            def __init__(self, **kwargs):
                real_signature.bind(self, **kwargs)
                captured.update(kwargs)
                self.pid_file = None
                self.terminate = threading.Event()
                self.terminate.set()

            def start_process(self): ...

        class StubObserver:
            def schedule(self, *args, **kwargs): ...

            def start(self): ...

            def stop(self): ...

            def join(self): ...

        monkeypatch.setattr(run_module, "Handler", StubHandler)
        monkeypatch.setattr(run_module, "Observer", StubObserver)
        script = tmp_path / "main.py"
        script.write_text("import flet as ft\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        args = parse_command_line(["run", *argv, str(script)])
        args.handler(args)
        return captured

    return invoke


def _start_app_env(monkeypatch, tmp_path, exported_assets_dir):
    """
    Return the environment `Handler.start_process()` starts the app with.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        tmp_path: pytest tmp dir, used for the storage dirs.
        exported_assets_dir: The `Handler`'s `exported_assets_dir`.

    Returns:
        The `env` passed to `subprocess.Popen`.
    """

    started = {}

    def popen(args, env, **kwargs):
        started["env"] = env
        return types.SimpleNamespace(stdout=io.StringIO(""))

    monkeypatch.setattr(run_module.subprocess, "Popen", popen)
    handler = run_module.Handler(
        args=[sys.executable, "main.py"],
        watch_directory=False,
        script_path=str(tmp_path / "main.py"),
        port=None,
        host=None,
        page_name="",
        uds_path=None,
        web=False,
        ios=False,
        android=False,
        hidden=False,
        assets_dir=None,
        exported_assets_dir=exported_assets_dir,
        ignore_dirs=[],
        flet_app_data_dir=str(tmp_path),
        flet_app_cache_dir=str(tmp_path),
        flet_app_temp_dir=str(tmp_path),
        verbose=0,
    )
    handler.start_process()
    return started["env"]


class TestExportedOnlyWhenRequested:
    """`FLET_ASSETS_DIR` reaches the app only for an explicit `--assets` or env."""

    def test_default_assets_dir_is_not_exported(self, tmp_path, handler_kwargs):
        """The defaulted `assets` dir is resolved for the window but not exported."""
        (tmp_path / "assets").mkdir()
        kwargs = handler_kwargs()
        assert kwargs["assets_dir"] == str(tmp_path / "assets")
        assert kwargs["exported_assets_dir"] is None

    def test_assets_flag_is_exported(self, tmp_path, handler_kwargs):
        """`--assets` is resolved against the script dir and exported."""
        (tmp_path / "media").mkdir()
        kwargs = handler_kwargs("--assets", "media")
        assert kwargs["assets_dir"] == str(tmp_path / "media")
        assert kwargs["exported_assets_dir"] == str(tmp_path / "media")

    def test_env_var_is_exported(self, tmp_path, handler_kwargs, monkeypatch):
        """`FLET_ASSETS_DIR` set by the user is exported like `--assets`."""
        (tmp_path / "media").mkdir()
        monkeypatch.setenv("FLET_ASSETS_DIR", str(tmp_path / "media"))
        kwargs = handler_kwargs()
        assert kwargs["exported_assets_dir"] == str(tmp_path / "media")

    def test_missing_assets_flag_is_still_exported(self, tmp_path, handler_kwargs):
        """A missing `--assets` dir is exported anyway, so it beats `ft.run()`."""
        (tmp_path / "images").mkdir()
        kwargs = handler_kwargs("--assets", "missing")
        assert kwargs["assets_dir"] is None
        assert kwargs["exported_assets_dir"] == str((tmp_path / "missing").resolve())

    def test_assets_flag_beats_an_inherited_env_var(
        self, tmp_path, handler_kwargs, monkeypatch
    ):
        """`--assets` wins over `FLET_ASSETS_DIR` from the shell, missing or not."""
        (tmp_path / "other").mkdir()
        monkeypatch.setenv("FLET_ASSETS_DIR", str(tmp_path / "other"))
        kwargs = handler_kwargs("--assets", "missing")
        assert kwargs["exported_assets_dir"] == str((tmp_path / "missing").resolve())

    @pytest.mark.parametrize("exported", [None, "/requested/assets"])
    def test_app_environment(self, tmp_path, monkeypatch, exported):
        """The app gets exactly the exported dir, over an inherited value."""
        monkeypatch.delenv("FLET_ASSETS_DIR", raising=False)
        env = _start_app_env(monkeypatch, tmp_path, exported)
        assert env.get("FLET_ASSETS_DIR") == exported

    def test_exported_dir_replaces_an_inherited_env_var(self, tmp_path, monkeypatch):
        """An exported dir replaces `FLET_ASSETS_DIR` inherited from the shell."""
        monkeypatch.setenv("FLET_ASSETS_DIR", "/from/the/shell")
        env = _start_app_env(monkeypatch, tmp_path, "/requested/assets")
        assert env["FLET_ASSETS_DIR"] == "/requested/assets"


def _window_assets_dir(monkeypatch, capsys, output):
    """
    Feed app `output` to `Handler.print_output()` and return the window's assets dir.

    Args:
        monkeypatch: pytest monkeypatch fixture.
        capsys: pytest capsys fixture, drained before returning.
        output: Lines the app prints, with `PAGE_URL_TEST` as the URL prefix.

    Returns:
        A `(assets_dir, printed)` tuple: the assets dir the desktop window was
            opened with, and what `flet run` printed.
    """

    handler = run_module.Handler.__new__(run_module.Handler)
    handler.page_url_prefix = "PAGE_URL_TEST"
    handler.page_url = None
    handler.hidden = False
    handler.web = handler.ios = handler.android = False
    handler.assets_dir = "/from/flet/run"
    opened = threading.Event()
    seen = {}

    def open_view(self):
        seen["assets_dir"] = self.assets_dir
        opened.set()

    monkeypatch.setattr(run_module.Handler, "open_flet_view_and_wait", open_view)
    handler.print_output(types.SimpleNamespace(stdout=io.StringIO(output)))
    assert opened.wait(5), "desktop window was never opened"
    return seen["assets_dir"], capsys.readouterr().out


class TestTheWindowUsesTheAppsAssetsDir:
    """The desktop window opens with the directory the app reports."""

    def test_reported_dir(self, monkeypatch, capsys):
        """The reported dir replaces the one `flet run` resolved."""
        assets_dir, _ = _window_assets_dir(
            monkeypatch,
            capsys,
            f"PAGE_URL_TEST{DISPLAY_ASSETS_DIR_SUFFIX} /app/my images\n"
            "PAGE_URL_TEST http://127.0.0.1:8550\n",
        )
        assert assets_dir == "/app/my images"

    def test_empty_report_means_no_assets_dir(self, monkeypatch, capsys):
        """An app without an assets dir opens a window without one."""
        assets_dir, _ = _window_assets_dir(
            monkeypatch,
            capsys,
            f"PAGE_URL_TEST{DISPLAY_ASSETS_DIR_SUFFIX} \n"
            "PAGE_URL_TEST http://127.0.0.1:8550\n",
        )
        assert assets_dir is None

    def test_without_a_report_the_resolved_dir_is_kept(self, monkeypatch, capsys):
        """An app that reports nothing keeps the dir `flet run` resolved."""
        assets_dir, _ = _window_assets_dir(
            monkeypatch, capsys, "PAGE_URL_TEST http://127.0.0.1:8550\n"
        )
        assert assets_dir == "/from/flet/run"

    def test_report_is_not_printed(self, monkeypatch, capsys):
        """The report line is consumed; the app's other output is printed."""
        _, printed = _window_assets_dir(
            monkeypatch,
            capsys,
            "hello from the app\n"
            f"PAGE_URL_TEST{DISPLAY_ASSETS_DIR_SUFFIX} /app/images\n"
            "PAGE_URL_TEST http://127.0.0.1:8550\n",
        )
        assert "hello from the app" in printed
        assert DISPLAY_ASSETS_DIR_SUFFIX not in printed


def test_app_reports_its_assets_dir_before_the_url(tmp_path):
    """A real app started with a URL prefix prints its resolved assets dir first."""
    assets = tmp_path / "my images é"
    assets.mkdir()
    script = tmp_path / "main.py"
    script.write_text(
        f"import flet as ft\nft.run(lambda page: None, assets_dir={assets.name!r})\n",
        encoding="utf-8",
    )
    env = {
        **os.environ,
        "FLET_DISPLAY_URL_PREFIX": "PAGE_URL_TEST",
        "FLET_SERVER_PORT": str(get_free_tcp_port()),
        "PYTHONIOENCODING": "utf-8",
    }
    env.pop("FLET_ASSETS_DIR", None)
    p = subprocess.Popen(
        [sys.executable, "-u", str(script)],
        cwd=tmp_path,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        encoding="utf-8",
    )
    lines = []

    def read_until_url():
        for line in p.stdout:
            lines.append(line.rstrip("\n"))
            if line.startswith("PAGE_URL_TEST "):
                return

    try:
        reader = threading.Thread(target=read_until_url, daemon=True)
        reader.start()
        reader.join(60)
    finally:
        p.kill()
        p.wait()
    prefixed = [line for line in lines if line.startswith("PAGE_URL_TEST")]
    assert prefixed[0] == (
        f"PAGE_URL_TEST{DISPLAY_ASSETS_DIR_SUFFIX} {assets.resolve()}"
    )
    assert prefixed[1].startswith("PAGE_URL_TEST ")
