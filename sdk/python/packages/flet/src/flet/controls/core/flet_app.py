from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import OptionalControlEventCallable

__all__ = ["FletApp"]


@control("FletApp")
class FletApp(ConstrainedControl):
    url: Optional[str] = None
    args: Optional[dict[str, Any]] = None
    force_pyodide: bool = False
    reconnect_interval_ms: Optional[int] = None
    reconnect_timeout_ms: Optional[int] = None
    show_app_startup_screen: bool = False
    app_startup_screen_message: Optional[str] = None
    on_error: OptionalControlEventCallable = None
