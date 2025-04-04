from dataclasses import dataclass

from flet.core.adaptive_control import AdaptiveControl
from flet.core.types import OptionalControlEventCallable


@dataclass(kw_only=True)
class DialogControl(AdaptiveControl):
    open: bool = False
    on_dismiss: OptionalControlEventCallable = None
