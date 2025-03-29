import dataclasses
import inspect
import sys
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Optional, get_args, get_type_hints

if TYPE_CHECKING:
    from .control import Control
    from .page import Page


@dataclass
class ControlEvent:
    name: str
    data: Optional[Any]
    control: "Control" = field(repr=False)

    @property
    def page(self) -> Optional["Page"]:
        return self.control.page

    @property
    def target(self) -> int:
        return self.control._i

    @staticmethod
    def get_event_field_type(control: Any, field_name: str):
        frame = inspect.currentframe().f_back
        globalns = sys.modules[control.__class__.__module__].__dict__
        localns = frame.f_globals.copy()
        localns.update(frame.f_locals)
        hints = get_type_hints(control, globalns=globalns, localns=localns)
        if field_name in hints:
            callable_type = get_args(hints[field_name])[
                0
            ]  # Get `Callable[[EventType], None]`
            return get_args(callable_type)[0][0]  # Get `EventType`
        else:
            return None
