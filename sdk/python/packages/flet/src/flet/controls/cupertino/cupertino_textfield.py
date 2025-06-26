from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import DecorationImage, OptionalShadowValue
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

    Online docs: https://flet.dev/docs/controls/cupertinotextfield
    """

    placeholder_text: Optional[str] = None
    """
    A lighter colored placeholder hint that appears on the first line of the text 
    field when the text entry is empty.

    Defaults to an empty string.
    """

    placeholder_style: Optional[TextStyle] = None
    """
    The [TextStyle](https://flet.dev/docs/reference/types/textstyle) to use for 
    `placeholder_text`.
    """

    gradient: Optional[Gradient] = None
    """
    Configures gradient background.

    Value is of type [Gradient](https://flet.dev/docs/reference/types/gradient).
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode applied to the `color` or `gradient` background.

    Value is of type [BlendMode](https://flet.dev/docs/reference/types/blendmode) and 
    defaults to `BlendMode.MODULATE`.
    """

    shadow: OptionalShadowValue = None
    """
    A list of shadows behind the text field.
    """

    prefix_visibility_mode: VisibilityMode = VisibilityMode.ALWAYS
    """
    Defines the visibility of the `prefix` control based on the state of text entry.

    Has no effect if `prefix` is not specified.

    Value is of type 
    [VisibilityMode](https://flet.dev/docs/reference/types/visibilitymode) and 
    defaults to `VisibilityMode.ALWAYS`.
    """

    suffix_visibility_mode: VisibilityMode = VisibilityMode.ALWAYS
    """
    Defines the visibility of the `suffix` control based on the state of text entry.

    Has no effect if `suffix` is not specified.

    Value is of type 
    [VisibilityMode](https://flet.dev/docs/reference/types/visibilitymode) and 
    defaults to `VisibilityMode.ALWAYS`.
    """

    clear_button_visibility_mode: VisibilityMode = VisibilityMode.NEVER
    """
    Defines the visibility of the clear button based on the state of text entry.

    Will appear only if no `suffix` is provided.

    Value is of type 
    [VisibilityMode](https://flet.dev/docs/reference/types/visibilitymode) and 
    defaults to `VisibilityMode.NEVER`.
    """

    clear_button_semantics_label: Optional[str] = None
    """
    The semantic label for the clear button used by screen readers.

    This will be used by screen reading software to identify the clear button widget.

    Defaults to `"Clear"`.
    """

    image: Optional[DecorationImage] = None
    """
    An image to paint above the `bgcolor` or `gradient`.

    Value is of type 
    [DecorationImage](https://flet.dev/docs/reference/types/decorationimage).
    """

    padding: OptionalPaddingValue = None
    """
    The padding around the text entry area between the `prefix` and `suffix` or the 
    clear button when `clear_button_mode` is not `VisibilityMode.NEVER`.

    Value is of type 
    [Padding](https://flet.dev/docs/reference/types/padding) and defaults to padding 
    of `7` pixels on all sides.
    """
