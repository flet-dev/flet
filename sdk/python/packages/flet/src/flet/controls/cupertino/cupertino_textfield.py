from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import BoxShadowValue, DecorationImage
from flet.controls.gradients import Gradient
from flet.controls.material.textfield import TextField
from flet.controls.padding import Padding, PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import BlendMode

__all__ = ["CupertinoTextField", "OverlayVisibilityMode"]


class OverlayVisibilityMode(Enum):
    NEVER = "never"
    EDITING = "editing"
    NOT_EDITING = "notEditing"
    ALWAYS = "always"


@control("CupertinoTextField")
class CupertinoTextField(TextField):
    """
    An iOS-style text field.
    """

    placeholder_text: Optional[str] = None
    """
    A lighter colored placeholder hint that appears on the first line of the text
    field when the text entry is empty.

    Defaults to an empty string.
    """

    placeholder_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] to use for
    [`placeholder_text`][flet.CupertinoTextField.placeholder_text].
    """

    gradient: Optional[Gradient] = None
    """
    Configures the gradient background.
    """

    blend_mode: Optional[BlendMode] = None
    """
    The blend mode applied to the [`bgcolor`][flet.CupertinoTextField.bgcolor] or
    [`gradient`][flet.CupertinoTextField.gradient] background.
    """

    shadows: Optional[BoxShadowValue] = None
    """
    A list of shadows behind the text field.
    """

    prefix_visibility_mode: OverlayVisibilityMode = OverlayVisibilityMode.ALWAYS
    """
    Defines the visibility of the [`prefix`][flet.CupertinoTextField.prefix] control
    based on the state of text entry.

    Has no effect if `prefix` is not specified.
    """

    suffix_visibility_mode: OverlayVisibilityMode = OverlayVisibilityMode.ALWAYS
    """
    Defines the visibility of the [`suffix`][flet.CupertinoTextField.suffix] control
    based on the state of text entry.

    Has no effect if `suffix` is not specified.
    """

    clear_button_visibility_mode: OverlayVisibilityMode = OverlayVisibilityMode.NEVER
    """
    Defines the visibility of the clear button based on the state of text entry.

    Will appear only if no [`suffix`][flet.CupertinoTextField.suffix] is provided.
    """

    clear_button_semantics_label: Optional[str] = "Clear"
    """
    The semantic label for the clear button used by screen readers.

    This will be used by screen reading software to identify the clear button widget.
    """

    image: Optional[DecorationImage] = None
    """
    An image to paint above the [`bgcolor`][flet.CupertinoTextField.bgcolor] or
    [`gradient`][flet.CupertinoTextField.gradient] background.
    """

    padding: PaddingValue = field(default_factory=lambda: Padding.all(7))
    """
    The padding around the text entry area between the
    [`prefix`][flet.CupertinoTextField.prefix]
    and [`suffix`][flet.CupertinoTextField.suffix] or the
    clear button when
    [`clear_button_visibility_mode`][flet.CupertinoTextField.clear_button_visibility_mode]
    is not [`OverlayVisibilityMode.NEVER`][flet.OverlayVisibilityMode.NEVER].
    """
