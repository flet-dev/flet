import inspect
import sys
from dataclasses import InitVar, dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ForwardRef,
    Generic,
    Optional,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from flet.utils.typing_utils import eval_type

if TYPE_CHECKING:
    from .base_control import BaseControl  # noqa
    from .page import Page
    from .base_page import BasePage

    _BaseControlType = BaseControl
else:
    _BaseControlType = Any

__all__ = [
    "ControlEvent",
    "ControlEventHandler",
    "Event",
    "EventControlType",
    "EventHandler",
    "get_event_field_type",
]


def get_event_field_type(control: Any, field_name: str):
    """
    Resolve the concrete event payload type for an event-handler field.

    Inspects merged annotations across the control MRO and evaluates forward
    references so runtime event objects can be created with the right type.
    """
    frame = inspect.currentframe().f_back
    localns = frame.f_globals.copy()
    localns.update(frame.f_locals)

    merged_annotations = {}
    annotation_modules = {}

    for cls in control.__class__.__mro__:
        annotations = getattr(cls, "__annotations__", {})
        module = sys.modules.get(cls.__module__)
        module_dict = module.__dict__ if module else {}

        for name, annotation in annotations.items():
            if get_origin(annotation) is InitVar or str(annotation).startswith(
                "dataclasses.InitVar"
            ):
                continue  # Skip InitVar
            if name not in merged_annotations:
                merged_annotations[name] = annotation
                annotation_modules[name] = module_dict

    if field_name not in merged_annotations:
        return None

    annotation = merged_annotations[field_name]

    globalns = {}
    current_module = sys.modules.get(control.__class__.__module__)
    if current_module:
        globalns.update(current_module.__dict__)

    owner_module_dict = annotation_modules.get(field_name)
    if owner_module_dict:
        for key, value in owner_module_dict.items():
            globalns.setdefault(key, value)

    globalns.setdefault("__builtins__", __builtins__)
    type_params = getattr(control.__class__, "__type_params__", ())

    try:
        # Resolve forward refs manually
        if isinstance(annotation, ForwardRef):
            annotation = eval_type(
                annotation, globalns, localns, type_params=type_params
            )

        clbs = get_args(annotation)  # callable(s)
        clb = clbs[1] if len(clbs) > 2 else clbs[0]
        event_type = get_args(clb)[0][0]

        if isinstance(event_type, ForwardRef):
            event_type = eval_type(
                event_type, globalns, localns, type_params=type_params
            )

        return event_type
    except Exception as e:
        raise RuntimeError(f"[resolve error] {field_name}: {e}") from e


EventControlType = TypeVar("EventControlType", bound=_BaseControlType)
"""Type variable bound to a control type for typed event payloads."""


@dataclass
class Event(Generic[EventControlType]):
    """
    Base event payload passed to control event handlers.
    """

    name: str
    data: Optional[Any] = field(default=None, kw_only=True)
    control: EventControlType = field(repr=False)

    @property
    def page(self) -> Union["Page", "BasePage"]:
        """
        Page that owns the event source control.
        """
        if not self.control.page:
            raise RuntimeError("event control is not attached to a page")
        return self.control.page

    @property
    def target(self) -> int:
        """
        Internal id of the control that emitted this event.
        """
        return self.control._i


EventType = TypeVar("EventType", bound=Event)

ControlEventHandler = Union[Callable[[], Any], Callable[[Event[EventControlType]], Any]]
"""Type alias for typed control event callback handlers.

Represents a callback that accepts either:
- no arguments,
- or a typed [`Event`][flet.] for a specific control type.
"""

EventHandler = Union[Callable[[], Any], Callable[[EventType], Any]]
"""Type alias for generic event callback handlers.

Represents a callback that accepts either:
- no arguments,
- or an [`Event`][flet.]-derived payload.
"""

ControlEvent = Event[_BaseControlType]
"""Type alias for an event emitted by any base control."""
