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
    _eval_type,
    get_args,
    get_origin,
)

if TYPE_CHECKING:
    from .base_control import BaseControl  # noqa
    from .page import Page
    from .base_page import BasePage

__all__ = [
    "ControlEvent",
    "ControlEventHandler",
    "Event",
    "EventControlType",
    "EventHandler",
    "get_event_field_type",
]


def get_event_field_type(control: Any, field_name: str):
    frame = inspect.currentframe().f_back
    globalns = sys.modules[control.__class__.__module__].__dict__
    localns = frame.f_globals.copy()
    localns.update(frame.f_locals)

    merged_annotations = {}

    for cls in control.__class__.__mro__:
        annotations = getattr(cls, "__annotations__", {})
        for name, annotation in annotations.items():
            if get_origin(annotation) is InitVar or str(annotation).startswith(
                "dataclasses.InitVar"
            ):
                continue  # Skip InitVar
            if name not in merged_annotations:
                merged_annotations[name] = annotation

    if field_name not in merged_annotations:
        return None

    annotation = merged_annotations[field_name]

    try:
        # Resolve forward refs manually
        if isinstance(annotation, ForwardRef):
            annotation = _eval_type(annotation, globalns, localns)

        clbs = get_args(annotation)  # callable(s)
        clb = clbs[1] if len(clbs) > 2 else clbs[0]
        event_type = get_args(clb)[0][0]

        if isinstance(event_type, ForwardRef):
            event_type = _eval_type(event_type, globalns, localns)

        return event_type
    except Exception as e:
        raise Exception(f"[resolve error] {field_name}: {e}") from e


EventControlType = TypeVar("EventControlType", bound="BaseControl")


@dataclass
class Event(Generic[EventControlType]):
    name: str
    data: Optional[Any] = field(default=None, kw_only=True)
    control: EventControlType = field(repr=False)

    @property
    def page(self) -> Optional[Union["Page", "BasePage"]]:
        return self.control.page

    @property
    def target(self) -> int:
        return self.control._i


EventType = TypeVar("EventType", bound=Event)

ControlEventHandler = Union[Callable[[], Any], Callable[[Event[EventControlType]], Any]]

EventHandler = Union[Callable[[], Any], Callable[[EventType], Any]]

ControlEvent = Event["BaseControl"]
