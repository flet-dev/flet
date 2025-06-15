from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler

__all__ = ["FletApp"]


@control("FletApp")
class FletApp(ConstrainedControl):
    """
    Renders another Flet app in the current app, similar to HTML IFrame, but for Flet.
    """

    url: Optional[str] = None
    """
    Flet app URL, e.g. `http://localhost:8550` or `flet.sock`.
    """

    args: Optional[dict[str, Any]] = None
    """
    TBD
    """

    force_pyodide: bool = False
    """
    TBD
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
    TBD
    """

    app_startup_screen_message: Optional[str] = None
    """
    TBD
    """

    on_error: OptionalControlEventHandler["FletApp"] = None
    """
    Fires when a connection or any unhandled error occurs.
    """
