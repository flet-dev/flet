from enum import Enum
from typing import Optional

from flet.controls.box import DecorationImage, OptionalShadowValue
from flet.controls.control import control
from flet.controls.gradients import Gradient
from flet.controls.material.textfield import TextField
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import BlendMode

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
    value: str = ""
    placeholder_style: Optional[TextStyle] = None
    gradient: Optional[Gradient] = None
    blend_mode: Optional[BlendMode] = None
    shadow: OptionalShadowValue = None
    prefix_visibility_mode: VisibilityMode = VisibilityMode.ALWAYS
    suffix_visibility_mode: VisibilityMode = VisibilityMode.ALWAYS
    clear_button_visibility_mode: VisibilityMode = VisibilityMode.NEVER
    clear_button_semantics_label: Optional[str] = None
    image: Optional[DecorationImage] = None
    padding: OptionalPaddingValue = None
