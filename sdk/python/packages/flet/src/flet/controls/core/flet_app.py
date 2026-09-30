from dataclasses import dataclass
from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler, Event, EventHandler
from flet.controls.layout_control import LayoutControl

__all__ = ["FletApp", "FletAppOutputEvent"]


@dataclass
class FletAppOutputEvent(Event["FletApp"]):
    """One stdout/stderr line from the embedded Pyodide app."""

    text: str
    """The line of text. Pyodide line-buffers stdout/stderr by default,
    so each event is typically one `print(...)` worth of output (with
    its trailing newline)."""

    is_stderr: bool = False
    """True for stderr writes; False for stdout."""


@control("FletApp")
class FletApp(LayoutControl):
    """
    Renders another Flet app in the current app, similar to HTML IFrame, but for Flet.
    """

    url: Optional[str] = None
    """
    Flet app URL, e.g. `http://localhost:8550` or `flet.sock`.
    """

    args: Optional[dict[str, Any]] = None
    """
    Optional dictionary of arguments to pass to the Flet app.
    """

    assets_dir: Optional[str] = None
    """
    Base location for assets referenced by the embedded app. On web this
    is a URL prefix joined with relative `src` values (e.g. on
    `Image`/`Lottie`/`Markdown`); on desktop it is a filesystem path.
    """

    force_pyodide: bool = False
    """
    Whether to force the use of Pyodide.
    """

    reconnect_interval_ms: Optional[int] = None
    """
    Delay, in milliseconds, between reconnection attempts.
    """

    reconnect_timeout_ms: Optional[int] = None
    """
    Total time to try reconnecting.
    """

    boot_screen_name: Optional[str] = None
    """
    Name of the boot screen to show while the embedded app starts up.

    When `None`, the built-in `"flet"` boot screen is used. Custom boot screens
    are provided by extensions; see the
    [boot screen docs](https://flet.dev/docs/publish/#boot-screen).
    """

    boot_screen_options: Optional[dict[str, Any]] = None
    """
    Options for the boot screen, passed through to the boot screen widget.

    For the built-in `"flet"` screen these include `spinner_size`,
    `startup_message`, `bgcolor_light`/`bgcolor_dark`, etc. See the
    [boot screen docs](https://flet.dev/docs/publish/#boot-screen).
    """

    app_error_message: Optional[str] = None
    """
    Template message to display when the app fails to load.
    Use `{message}` placeholder to include the error message
    and `{details}` to include error details.
    """

    on_error: Optional[ControlEventHandler["FletApp"]] = None
    """
    Called when a connection or any unhandled error occurs.
    """

    on_connect: Optional[ControlEventHandler["FletApp"]] = None
    """
    Fires when the client allocates an in-process `dart_bridge` channel for this
    embedded app (`url="dartbridge://"`). The event `data` is the Dart native
    port the host must serve with a `FletDartBridgeServer` so the embedded app
    connects over it instead of a socket.

    Advanced / embedder use — hosts that run another Flet program in-process
    (e.g. a gallery or preview) start their server on this port in the handler.
    """

    on_python_output: Optional[EventHandler[FletAppOutputEvent]] = None
    """
    Fires once per stdout/stderr write inside the embedded Pyodide app.
    Pyodide line-buffers by default, so each event is typically one
    `print(...)` call. Only fires for embedded FletApps with
    `force_pyodide=True`; root-level Pyodide pages have nowhere to
    bubble the event.
    """

    async def wait_idle(
        self, idle_ms: int = 300, timeout_ms: int = 30000
    ) -> dict[str, Any]:
        """
        Waits until the embedded app has rendered its UI and gone quiet.

        Useful for a host that needs to know when the embedded app is ready,
        e.g. before taking a screenshot of it or reading its output after a
        restart.

        Args:
            idle_ms: How long, in milliseconds, the embedded app must send no
                UI updates after its first one to count as idle.
            timeout_ms: Give up after this many milliseconds.

        Returns:
            A dict with `status` and `error`. `status` is `"idle"` once the
            app sent at least one UI update, then none for `idle_ms`, and
            that update is on screen; `"error"` if the app failed to start
            or crashed (`error` holds the message; `on_error` fires as
            well); `"timeout"` if it didn't settle within `timeout_ms`, for
            example an app that updates continuously. A new call supersedes
            a pending one, which returns `"timeout"`.
        """
        return await self._invoke_method(
            "wait_idle",
            arguments={"idle_ms": idle_ms, "timeout_ms": timeout_ms},
            timeout=timeout_ms / 1000 + 5,
        )
