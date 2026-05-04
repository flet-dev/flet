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

    show_app_startup_screen: bool = False
    """
    Whether to show the app startup screen.
    """

    app_startup_screen_message: Optional[str] = None
    """
    Message to display on the app startup screen.
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

    on_python_output: Optional[EventHandler[FletAppOutputEvent]] = None
    """
    Fires once per stdout/stderr write inside the embedded Pyodide app.
    Pyodide line-buffers by default, so each event is typically one
    `print(...)` call. Only fires for embedded FletApps with
    `force_pyodide=True`; root-level Pyodide pages have nowhere to
    bubble the event.
    """
