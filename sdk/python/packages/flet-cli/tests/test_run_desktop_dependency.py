"""`flet-desktop` is only required by the modes that open a native window.

`flet-desktop` is an optional extra of `flet`, so a plain `pip install flet`
does not have it, and `flet run --web` crashed on

    ModuleNotFoundError: No module named 'flet_desktop'

before the app had started - see
https://github.com/flet-dev/flet/issues/5826.
"""

import inspect
import io
import subprocess
import sys
import threading
import types

import pytest

from flet_cli.cli import parse_command_line


class _BlockFletDesktop:
    """A `sys.meta_path` finder that makes `flet_desktop` unimportable."""

    def find_spec(self, fullname, path=None, target=None):
        if fullname == "flet_desktop" or fullname.startswith("flet_desktop."):
            raise ModuleNotFoundError(f"No module named {fullname!r}", name=fullname)
        return None


@pytest.fixture
def without_flet_desktop():
    saved = {
        name: module
        for name, module in sys.modules.items()
        if name == "flet_desktop" or name.startswith("flet_desktop.")
    }
    for name in saved:
        del sys.modules[name]

    blocker = _BlockFletDesktop()
    sys.meta_path.insert(0, blocker)
    try:
        yield
    finally:
        sys.meta_path.remove(blocker)
        sys.modules.update(saved)


@pytest.fixture
def with_fake_flet_desktop(monkeypatch):
    closed = []
    module = types.ModuleType("flet_desktop")
    module.close_flet_view = closed.append
    monkeypatch.setitem(sys.modules, "flet_desktop", module)
    return closed


@pytest.fixture
def run_flet(monkeypatch, tmp_path):
    from flet_cli.commands import run as run_module

    def invoke(*argv, pid_file=None):
        ensured = []
        monkeypatch.setattr(
            "flet.utils.pip.ensure_flet_web_package_installed",
            lambda: ensured.append("flet-web"),
        )
        monkeypatch.setattr(
            "flet.utils.pip.ensure_flet_desktop_package_installed",
            lambda: ensured.append("flet-desktop"),
        )
        # Belt and braces: should the patches above ever stop applying, fail
        # loudly instead of quietly pip-installing into the developer's venv.
        monkeypatch.setattr(
            "flet.utils.pip.install_flet_package",
            lambda name: pytest.fail(f"test tried to install {name!r}"),
        )

        real_signature = inspect.signature(run_module.Handler.__init__)

        class StubHandler:
            def __init__(self, **kwargs):
                # Keep the stub honest: `handle()` must still be calling the
                # real `Handler` with a valid argument list.
                real_signature.bind(self, **kwargs)
                self.kwargs = kwargs
                self.pid_file = pid_file
                # Return control to `handle()` immediately.
                self.terminate = threading.Event()
                self.terminate.set()

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

        args = parse_command_line([*argv, str(script)])
        args.handler(args)
        return ensured

    return invoke


class TestServedModesDoNotNeedTheDesktopClient:
    """`--web`, `--ios` and `--android` run with `flet-desktop` absent."""

    @pytest.mark.parametrize("web_flag", ["-w", "--web"])
    def test_web(self, run_flet, without_flet_desktop, web_flag):
        """Both spellings of the web flag ensure `flet-web` and nothing else."""
        assert run_flet(web_flag) == ["flet-web"]

    def test_web_with_watched_directory(self, run_flet, without_flet_desktop):
        """`flet run -dw main.py`, the command line reported in #5826."""
        assert run_flet("-d", "-w") == ["flet-web"]

    @pytest.mark.parametrize("mobile_flag", ["--ios", "--android"])
    def test_mobile(self, run_flet, without_flet_desktop, mobile_flag):
        """The mobile modes serve over the same web server, so they match."""
        assert run_flet(mobile_flag) == ["flet-web"]


class TestDesktopModeStillUsesTheDesktopClient:
    """Plain `flet run` installs the client and closes the window it opened."""

    def test_client_is_installed(self, run_flet, with_fake_flet_desktop):
        """Desktop mode is the one mode that ensures `flet-desktop`."""
        assert run_flet() == ["flet-desktop"]

    def test_window_is_closed_on_teardown(self, run_flet, with_fake_flet_desktop):
        """A window that was opened is still closed, guard or no guard."""
        run_flet(pid_file="/tmp/flet-view.pid")
        assert with_fake_flet_desktop == ["/tmp/flet-view.pid"]

    def test_served_mode_has_no_window_to_close(self, run_flet, with_fake_flet_desktop):
        """Teardown is skipped where no window was opened."""
        run_flet("--web")
        assert with_fake_flet_desktop == []


def _route_page_url(monkeypatch, expect_desktop=False, **modes):
    from flet_cli.commands import run as run_module

    handler = run_module.Handler.__new__(run_module.Handler)
    handler.page_url_prefix = "PAGE_URL_TEST"
    handler.page_url = None
    handler.hidden = False
    handler.web = modes.get("web", False)
    handler.ios = modes.get("ios", False)
    handler.android = modes.get("android", False)

    took = []
    opened = threading.Event()

    def _desktop_view(self):
        took.append("desktop-view")
        opened.set()

    monkeypatch.setattr(run_module.Handler, "open_flet_view_and_wait", _desktop_view)
    monkeypatch.setattr(
        run_module.Handler,
        "print_qr_code",
        lambda self, url, android: took.append("qr-code"),
    )
    monkeypatch.setattr(
        run_module, "open_in_browser", lambda url: took.append("browser")
    )

    stdout = io.StringIO("PAGE_URL_TEST http://127.0.0.1:8550\n")
    handler.print_output(types.SimpleNamespace(stdout=stdout))
    # Only the desktop path hands off to a thread; the rest are synchronous.
    if expect_desktop:
        assert opened.wait(5), "desktop view thread never ran"
    return took


class TestRoutingMatchesTheInstalledPackage:
    """
    The modes `handle()` installs `flet-web` for are exactly the modes that
    never reach `open_flet_view_and_wait`, which imports `flet_desktop`.
    """

    @pytest.mark.parametrize(
        "modes",
        [{"web": True}, {"ios": True}, {"android": True}, {"ios": True, "web": True}],
    )
    def test_served_modes_open_no_window(self, monkeypatch, modes):
        """Every mode that ensures `flet-web` routes away from the client."""
        assert "desktop-view" not in _route_page_url(monkeypatch, **modes)

    def test_desktop_mode_opens_a_window(self, monkeypatch):
        """And the mode that ensures `flet-desktop` routes to it."""
        assert _route_page_url(monkeypatch, expect_desktop=True) == ["desktop-view"]


class TestTheImportIsNeverReachedUnnecessarily:
    """`flet_desktop` is imported at its call sites, and nowhere earlier."""

    def test_not_imported_at_module_scope(self):
        """
        `flet_cli.cli` imports the run command eagerly, so a module-scope
        import would break every `flet` subcommand. This runs in a subprocess
        because the fixtures above only block once this module is loaded.
        """
        probe = (
            "import sys\n"
            "class Block:\n"
            "    def find_spec(self, name, path=None, target=None):\n"
            "        if name == 'flet_desktop' or name.startswith('flet_desktop.'):\n"
            "            raise ModuleNotFoundError(name)\n"
            "sys.meta_path.insert(0, Block())\n"
            "import flet_cli.cli\n"
            "import flet_cli.commands.run\n"
        )
        result = subprocess.run(
            [sys.executable, "-c", probe], capture_output=True, text=True
        )

        assert result.returncode == 0, result.stderr


class TestAFailedDesktopViewEndsTheRun:
    """
    `open_flet_view_and_wait` holds the only `terminate.set()` there is, so a
    failure in it must still end the run rather than leave `handle()` waiting.
    """

    def test_unimportable_client(self, monkeypatch):
        """`terminate` is set even when the import raises."""
        from flet_cli.commands import run as run_module

        handler = run_module.Handler.__new__(run_module.Handler)
        handler.terminate = threading.Event()
        handler.page_url = "http://127.0.0.1:8550"
        handler.assets_dir = None
        handler.hidden = False
        monkeypatch.setitem(sys.modules, "flet_desktop", None)

        with pytest.raises(ImportError):
            handler.open_flet_view_and_wait()

        assert handler.terminate.is_set()
