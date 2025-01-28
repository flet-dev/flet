import json
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from flet.core.border_radius import BorderRadius
from flet.core.differ import Differ
from flet.core.text_span import TextSpan
from flet.core.types import FontWeight, OptionalNumber, TextAlign


def event(convertor: Optional[Callable]):
    return field(default=None, metadata={"convertor": convertor})


@dataclass(kw_only=True)
class Control:
    x: Optional[List[str]] = None
    _control: Optional[str] = None

    def is_isolated(self) -> bool:
        return False

    def before_update(self):
        pass

    def __post_init__(self):
        # print("post init!")
        # self.__class__.__hash__ = Control.__hash__
        self._control = self.__class__.__name__

    def _get_event(self):
        return 1

    def _set_event(self, e):
        pass


@dataclass(kw_only=True)
class Page(Control):
    controls: list[Control] = field(default_factory=lambda: [])


@dataclass
class Text(Control):
    value: Optional[str] = None
    spans: Optional[List[TextSpan]] = None
    text_align: Optional[TextAlign] = None
    font_family: Optional[str] = None
    size: OptionalNumber = None
    weight: Optional[FontWeight] = None
    italic: Optional[bool] = None


@dataclass
class Button(Control):
    """This is button"""

    text: str
    """Button display text"""

    content: Control | str | None = (
        None  # this was introduced in Python 3.10: https://peps.python.org/pep-0604/
    )
    """Content - Control or str"""

    border_radius: BorderRadius | None = None
    """Border radius"""

    padding: Optional[int] = 5
    """Button padding"""

    on_click: Optional[Callable[[Any], Any]] = None
    """Handler for click events. 

    This should be a callable that accepts an argument and returns a value.
    Example:

    ```
    def handle_click(event: Event) -> None:
        print("Button clicked!")
    ```
    """
