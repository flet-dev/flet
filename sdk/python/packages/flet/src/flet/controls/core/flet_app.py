from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl

__all__ = ["FletApp"]


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
