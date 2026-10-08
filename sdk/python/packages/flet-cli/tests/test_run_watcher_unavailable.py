"""`flet run` runs the app without hot reload when file watching can't start.

On Linux the watchdog observer is backed by inotify, and starting it raises
`OSError` with `ENOSPC` or `EMFILE` once the user's inotify watch or instance
limit is used up. `flet run` then prints a warning, links the docs on raising
those limits, and starts the app anyway.
"""

import errno
import inspect
import threading

import pytest

from flet_cli.cli import parse_command_line

DOCS_URL = "https://flet.dev/docs/getting-started/running-app#linux-inotify-limits"


@pytest.fixture
def run_flet(monkeypatch, tmp_path):
    from flet_cli.commands import run as run_module

    def invoke(observer_error=None, linux=None):
        events = []
        monkeypatch.setattr(
            "flet.utils.pip.ensure_flet_desktop_package_installed", lambda: None
        )
        monkeypatch.setattr(
            "flet.utils.pip.ensure_flet_web_package_installed", lambda: None
        )
        # Belt and braces: should the patches above ever stop applying, fail
        # loudly instead of quietly pip-installing into the developer's venv.
        monkeypatch.setattr(
            "flet.utils.pip.install_flet_package",
            lambda name: pytest.fail(f"test tried to install {name!r}"),
        )
        if linux is not None:
            monkeypatch.setattr(run_module, "is_linux", lambda: linux)

        real_signature = inspect.signature(run_module.Handler.__init__)

        class StubHandler:
            def __init__(self, **kwargs):
                real_signature.bind(self, **kwargs)
                self.pid_file = None
                # Return control to `handle()` immediately.
                self.terminate = threading.Event()
                self.terminate.set()

            def start_process(self):
                events.append("start_process")

        class StubObserver:
            """Tears down like a watchdog observer, which is a `Thread`."""

            started = False

            def schedule(self, *args, **kwargs): ...

            def start(self):
                events.append("start")
                if observer_error is not None:
                    raise observer_error
                self.started = True

            def is_alive(self):
                return self.started

            def stop(self):
                events.append("stop")

            def join(self):
                if not self.started:
                    raise RuntimeError("cannot join thread before it is started")
                events.append("join")

        monkeypatch.setattr(run_module, "Handler", StubHandler)
        monkeypatch.setattr(run_module, "Observer", StubObserver)

        script = tmp_path / "main.py"
        script.write_text("import flet as ft\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)

        args = parse_command_line([str(script)])
        args.handler(args)
        return events

    return invoke


class TestTheAppRunsWithoutFileWatching:
    """An observer that fails to start costs hot reload, not the run."""

    def test_app_is_started(self, run_flet):
        """The app starts, and the never-started observer is not joined."""
        events = run_flet(OSError(errno.ENOSPC, "inotify watch limit reached"))
        assert "start_process" in events

    def test_watching_starts_before_the_app(self, run_flet):
        """An observer error is raised before any app process exists."""
        events = run_flet(OSError(errno.ENOSPC, "inotify watch limit reached"))
        assert events.index("start") < events.index("start_process")

    def test_started_observer_is_torn_down(self, run_flet):
        """An observer that did start is stopped and joined when the run ends."""
        assert run_flet()[-2:] == ["stop", "join"]


class TestTheWarning:
    """The warning names the error and links the docs for inotify limits only."""

    @pytest.mark.parametrize(
        ("linux", "error", "detail", "hinted"),
        [
            (
                True,
                OSError(errno.ENOSPC, "inotify watch limit reached"),
                "inotify watch limit reached",
                True,
            ),
            (
                True,
                OSError(errno.EMFILE, "inotify instance limit reached"),
                "inotify instance limit reached",
                True,
            ),
            (
                True,
                OSError(errno.EPERM, "Operation not permitted"),
                "Operation not permitted",
                False,
            ),
            (
                False,
                OSError(errno.ENOSPC, "No space left on device"),
                "No space left on device",
                False,
            ),
            (True, OSError("watcher failed"), "watcher failed", False),
        ],
        ids=[
            "linux-watch-limit",
            "linux-instance-limit",
            "linux-other-errno",
            "not-linux",
            "no-errno",
        ],
    )
    def test_docs_link(self, run_flet, capsys, linux, error, detail, hinted):
        """Only a Linux inotify watch or instance limit error links the docs."""
        run_flet(error, linux=linux)
        out = capsys.readouterr().out
        assert f"file watching is unavailable ({detail})" in out
        assert (DOCS_URL in out) is hinted
