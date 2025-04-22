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
    A material design card: a panel with slightly rounded corners and an elevation shadow.

    Online docs: https://flet.dev/docs/controls/card
    """

    content: Optional[Control] = None
    margin: OptionalMarginValue = None
    elevation: OptionalNumber = None
    color: OptionalColorValue = None
    shadow_color: OptionalColorValue = None
    surface_tint_color: OptionalColorValue = None
    shape: Optional[OutlinedBorder] = None
    clip_behavior: Optional[ClipBehavior] = None
    is_semantic_container: Optional[bool] = None
    show_border_on_foreground: Optional[bool] = None
    variant: Optional[CardVariant] = None
