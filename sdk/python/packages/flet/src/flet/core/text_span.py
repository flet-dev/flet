from typing import Any, List, Optional

from flet.core.control import Control, control
from flet.core.text_style import TextStyle
from flet.core.types import OptionalControlEventCallable, UrlTarget


@control("TextSpan")
class TextSpan(Control):
    text: Optional[str] = None
    style: Optional[TextStyle] = None
    spans: Optional[List["TextSpan"]] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    semantics_label: Optional[str] = None
    spell_out: Optional[bool] = None
    on_click: OptionalControlEventCallable = None
    on_enter: OptionalControlEventCallable = None
    on_exit: OptionalControlEventCallable = None
