from dataclasses import field
from typing import Any, List, Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import OptionalControlEventCallable

__all__ = ["FletApp"]


@control("FletApp")
class FletApp(ConstrainedControl):
    url: Optional[str] = None
    args: Optional[List[str]] = None
    reconnect_interval_ms: Optional[int] = None
    reconnect_timeout_ms: Optional[int] = None
    show_app_startup_screen: bool = False
    app_startup_screen_message: Optional[str] = None
    on_error: OptionalControlEventCallable = None
