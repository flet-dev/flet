from dataclasses import field
from enum import Enum
from typing import Optional

from flet.core.box import DecorationImage, ShadowValue
from flet.core.control import control
from flet.core.gradients import Gradient
from flet.core.padding import OptionalPaddingValue
from flet.core.text_style import TextStyle
from flet.core.textfield import TextField
from flet.core.types import BlendMode

__all__ = ["CupertinoTextField", "VisibilityMode"]


class VisibilityMode(Enum):
    NEVER = "never"
    EDITING = "editing"
    NOT_EDITING = "notEditing"
    ALWAYS = "always"


@control("CupertinoTextField")
class CupertinoTextField(TextField):
    """
    An iOS-style text field.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinotextfield
    """

    placeholder_text: Optional[str] = None
    value: Optional[str] = None
    placeholder_style: Optional[TextStyle] = None
    gradient: Optional[Gradient] = None
    blend_mode: Optional[BlendMode] = None
    shadow: Optional[ShadowValue] = field(default=list)
    prefix_visibility_mode: Optional[VisibilityMode] = None
    suffix_visibility_mode: Optional[VisibilityMode] = None
    clear_button_visibility_mode: Optional[VisibilityMode] = None
    clear_button_semantics_label: Optional[str] = None
    image: Optional[DecorationImage] = None
    padding: OptionalPaddingValue = None
