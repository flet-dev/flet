from typing import Optional

from flet.controls.base_control import control
from flet.controls.box import BoxShadowValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import BlendMode, ColorValue, IconData, Number

__all__ = ["Icon"]


@control("Icon")
class Icon(LayoutControl):
    """
    A control that displays an icon from a built-in or custom icon set.

    Icons can be customized in color, size, and visual style using various
    parameters such as stroke weight, fill level, and shadows.

    ```python
    ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.PRIMARY, size=40)
    ```
    """

    icon: IconData
    """
    The icon to display, selected from a predefined icon set.

    You can explore available icons using the
    [Flet Icons Browser](https://gallery.flet.dev/icons-browser/).
    """

    color: Optional[ColorValue] = None
    """
    The color to use when drawing the icon.
    """

    size: Optional[Number] = None
    """
    The size (width and height) of the square area the icon will occupy.

    If not set, a default size will be used. When placing this icon
    inside other controls (such as buttons), those controls may also affect sizing.
    """

    semantics_label: Optional[str] = None
    """
    An accessibility label for the icon.

    This text is not displayed visually but may be announced by screen readers
    or other assistive technologies.
    """

    shadows: Optional[BoxShadowValue] = None
    """
    A list of shadows to apply beneath the icon.

    Use multiple shadows to simulate complex lighting effects.
    The order of shadows matters for how transparency is blended.
    """

    fill: Optional[Number] = None
    """
    The fill amount of the icon, between `0.0` (outline) and `1.0` (solid).

    This feature requires the icon's font to support fill variation.
    It can be used to indicate state transitions or selection visually.

    Raises:
        ValueError: If [`fill`][(c).] is less than `0.0` or greater than `1.0`.
    """

    apply_text_scaling: Optional[bool] = None
    """
    Whether to scale the icon based on the system or user's preferred text size.

    Useful when placing icons alongside text, ensuring both scale consistently
    for better readability and accessibility.
    """

    grade: Optional[Number] = None
    """
    A fine-tuning adjustment for the stroke thickness of the icon.

    This requires support from the icon's font. Grade values can be negative or
    positive.
    It allows precise visual adjustments without changing icon size.
    """

    weight: Optional[Number] = None
    """
    The stroke weight (thickness) of the icon's lines.

    This requires the icon font to support weight variation.
    Must be greater than `0`.

    Raises:
        ValueError: If [`weight`][(c).] is less than or equal to `0.0`.
    """

    optical_size: Optional[Number] = None
    """
    Adjusts the icon's visual style for different sizes to maintain clarity and balance.

    This requires the icon font to support optical sizing.
    Must be greater than `0`.

    Raises:
        ValueError: If [`optical_size`][(c).] is less than or equal to `0.0`.
    """

    blend_mode: Optional[BlendMode] = BlendMode.SRC_OVER
    """
    The blend mode used when rendering the icon.

    Blend modes control how the icon's color interacts with the background.
    The default is normal blending (`SRC_OVER`).
    """

    def before_update(self):
        super().before_update()
        if self.fill is not None and not (0.0 <= self.fill <= 1.0):
            raise ValueError(
                f"fill must be between 0.0 and 1.0 inclusive, got {self.fill}"
            )
        if self.weight is not None and self.weight <= 0.0:
            raise ValueError(
                f"weight must be strictly greater than 0.0, got {self.weight}"
            )
        if self.optical_size is not None and self.optical_size <= 0.0:
            raise ValueError(
                f"optical_size must be strictly greater than 0.0, "
                f"got {self.optical_size}"
            )
