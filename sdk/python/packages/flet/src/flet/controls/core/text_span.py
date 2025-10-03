from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.text_style import TextStyle
from flet.controls.types import Url

__all__ = ["TextSpan"]


@control("TextSpan")
class TextSpan(Control):
    """
    A text span.

    Usage Example: As a child of [`Text.spans`][flet.].

    For the object to be useful, at least one of [`text`][(c).] or
    [`spans`][(c).] should be set.
    """

    text: Optional[str] = None
    """
    The text contained in this span.

    Note:
        If both `text` and [`spans`][(c).] are defined,
        the `text` takes precedence.
    """

    style: Optional[TextStyle] = None
    """
    Defines the style of this text span.
    """

    spans: Optional[list["TextSpan"]] = None
    """
    Additional spans to include as children.

    Note:
        If both `spans` and [`text`][(c).] are defined,
        the `text` takes precedence.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][(c).] event callback is provided,
    it is fired after that.
    """

    semantics_label: Optional[str] = None
    """
    An alternative semantics label for this text.

    If present, the semantics of this control will contain this value instead of the
    actual text.

    Raises:
        ValueError: If [`semantics_label`][(c).] is set when [`text`][(c).] is `None`.
    """

    spell_out: Optional[bool] = None
    """
    Whether the assistive technologies should spell out this text
    character by character.

    If the text is 'hello world', setting this to true causes the assistive
    technologies, such as VoiceOver or TalkBack, to pronounce
    'h-e-l-l-o-space-w-o-r-l-d' instead of complete words.
    This is useful for texts, such as passwords or verification codes.

    If this span contains other text span children, they also inherit the property from
    this span unless explicitly set.

    If the property is not set, this text span inherits the spell out setting
    from its parent. If this text span does not have a parent or the parent does
    not have a spell out setting, this text span does not spell out the text by default.
    """

    on_click: Optional[ControlEventHandler["TextSpan"]] = None
    """
    Called when this span is clicked.
    """

    on_enter: Optional[ControlEventHandler["TextSpan"]] = None
    """
    Called when a mouse pointer has entered this span.
    """

    on_exit: Optional[ControlEventHandler["TextSpan"]] = None
    """
    Called when a mouse pointer has exited this span.
    """

    def before_update(self):
        super().before_update()
        if self.text is None and self.semantics_label is not None:
            raise ValueError("semantics_label can be set only when text is not None")
