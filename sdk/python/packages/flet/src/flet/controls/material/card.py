from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.margin import OptionalMarginValue
from flet.controls.types import ClipBehavior, OptionalColorValue, OptionalNumber

__all__ = ["Card", "CardVariant"]


class CardVariant(Enum):
    ELEVATED = "elevated"
    FILLED = "filled"
    OUTLINED = "outlined"


@control("Card")
class Card(ConstrainedControl, AdaptiveControl):
    """
    A material design card: a panel with slightly rounded corners and an elevation
    shadow.

    Online docs: https://flet.dev/docs/controls/card
    """

    content: Optional[Control] = None
    """
    The `Control` that should be displayed inside the card.

    This control can only have one child. To lay out multiple children, let this 
    control's child be a control such as [`Row`](https://flet.dev/docs/controls/row), 
    [`Column`](https://flet.dev/docs/controls/column), or [`Stack`](https://flet.dev/docs/controls/stack), 
    which have a children property, and then provide the children to that control.
    """

    margin: OptionalMarginValue = None
    """
    The empty space that surrounds the card.

    Value can be one of the following types: `int`, `float`, or [`Margin`](https://flet.dev/docs/reference/types/margin).
    """

    elevation: OptionalNumber = None
    """
    Controls the size of the shadow below the card. Default value is `1.0`.
    """

    color: OptionalColorValue = None
    """
    The card's background [color](https://flet.dev/docs/reference/colors).
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) to paint the shadow below the 
    card.
    """

    surface_tint_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used as an overlay on `color` 
    to indicate elevation.

    If this is `None`, no overlay will be applied. Otherwise this color will be 
    composited on top of `color` with an opacity related to `elevation` and used to 
    paint the background of the card.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the card.

    Value is of type [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder)`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The `content` will be clipped (or not) according to this option.

    """

    is_semantic_container: bool = True
    """
    Set to `True` (default) if this card represents a single semantic container, or to 
    `False` if it instead represents a collection of individual semantic nodes 
    (different types of content).
    """

    show_border_on_foreground: bool = True
    """
    Whether the shape of the border should be painted in front of the `content` or 
    behind.

    Defaults to `True`.
    """

    variant: CardVariant = CardVariant.ELEVATED
    """
    Defines the card variant to be used.

    Value is of type [`CardVariant`](https://flet.dev/docs/reference/types/cardvariant) 
    and defaults to `CardVariant.ELEVATED`.
    """
