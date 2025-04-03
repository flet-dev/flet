from dataclasses import dataclass

from flet.core.control import Control
from flet.core.types import OptionalControlEventCallable


@dataclass(kw_only=True)
class DialogControl(Control):
    open: bool = False
    on_dismiss: OptionalControlEventCallable = None
