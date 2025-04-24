import inspect
import sys
from dataclasses import InitVar, dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    ForwardRef,
    Optional,
    _eval_type,
    get_args,
    get_origin,
)

if TYPE_CHECKING:
    from .control import Control
    from .page import Page
__all__ = ["ControlEvent"]


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

            clb = get_args(annotation)  # callable
            event_type = get_args(clb[0])[0][0]

            if isinstance(event_type, ForwardRef):
                event_type = _eval_type(event_type, globalns, localns)

            return event_type
        except Exception as e:
            raise Exception(f"[resolve error] {field_name}: {e}")
