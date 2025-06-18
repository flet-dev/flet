from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.text_style import TextStyle
from flet.controls.types import UrlTarget

__all__ = ["TextSpan"]


@control("TextSpan")
class TextSpan(Control):
    """
    A span of [Text](https://flet.dev/docs/controls/text).
    """

    text: Optional[str] = None
    """
    The text contained in this span.

    If both `text` and `spans` are defined, the `text` will precede the `spans`.
    """

    style: Optional[TextStyle] = None
    """
    The [`TextStyle`](https://flet.dev/docs/reference/types/textstyle) to apply to
    this span.
    """

    spans: Optional[list["TextSpan"]] = None
    """
    Additional spans to include as children.

    If both `text` and `spans` are defined, the `text` will precede the `spans`.
    """

    url: Optional[str] = None
    """
    The URL to open when the span is clicked. If registered, `on_click` event is fired
    after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget) enum.
    Defaults to `UrlTarget.BLANK`.
    """

    semantics_label: Optional[str] = None
    """
    An alternative semantics label for this text.

    If present, the semantics of this control will contain this value instead of the
    actual text.
    """

    spell_out: Optional[bool] = None
    """
    TBD
    """

    on_click: OptionalControlEventHandler["TextSpan"] = None
    """
    Fires when the span is clicked.
    """

    on_enter: OptionalControlEventHandler["TextSpan"] = None
    """
    Triggered when a mouse pointer has entered the span.
    """

    on_exit: OptionalControlEventHandler["TextSpan"] = None
    """
    Triggered when a mouse pointer has exited the span.
    """
