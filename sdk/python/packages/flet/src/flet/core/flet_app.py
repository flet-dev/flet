from dataclasses import field
from typing import Optional

from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import OptionalControlEventCallable


@control("FletApp")
class FletApp(ConstrainedControl):

    url: Optional[str] = None
    reconnect_interval_ms: Optional[int] = None
    reconnect_timeout_ms: Optional[int] = None
    show_app_startup_screen: Optional[bool] = None
    app_startup_screen_message: Optional[str] = field(default=False)
    on_error: OptionalControlEventCallable = None
