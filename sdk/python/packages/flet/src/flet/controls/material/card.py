from enum import Enum
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ClipBehavior, ColorValue, Number

__all__ = ["Card", "CardVariant"]


class CardVariant(Enum):
    ELEVATED = "elevated"
    FILLED = "filled"
    OUTLINED = "outlined"


@control("Card")
class Card(LayoutControl, AdaptiveControl):
    """
    A material design card: a panel with slightly rounded corners and an elevation
    shadow.
    """

    content: Optional[Control] = None
    """
    The Control to display inside the card.

    Tip:
        To display multiple children, wrap them in a control like [`Row`][flet.Row],
        [`Column`][flet.Column], or [`Stack`][flet.Stack], which accept
        a `controls` list.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate at which to place this card.
    Defines the size of the shadow below the card.

    Defaults to [`CardTheme.elevation`][flet.CardTheme.elevation], or if that is `None`,
    falls back to `1.0`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The card's background color.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color to paint the shadow below this
    card.

    Defaults to [`CardTheme.shadow_color`][flet.CardTheme.shadow_color],
    or if that is `None`, falls back to [`Theme.shadow_color`][flet.Theme.shadow_color]
    (which defaults to `Colors.BLACK`).
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of this card.

    Defaults to [`CardTheme.shape`][flet.CardTheme.shape], or if that is `None`,
    falls back to `RoundedRectangleBorder(radius=12.0)`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Defines how the [`content`][flet.Card.content] will be clipped.

    Defaults to [`CardTheme.clip_behavior`][flet.CardTheme.clip_behavior],
    or if that is `None`, falls back to `ClipBehavior.NONE`.
    """

    semantic_container: bool = True
    """
    Whether this card represents a single semantic container, or
    if it instead represents a collection of individual semantic nodes
    (different types of content).
    """

    show_border_on_foreground: bool = True
    """
    Whether the shape of the border should be painted in front of the
    [`content`][flet.Card.content] or behind.
    """

    variant: CardVariant = CardVariant.ELEVATED
    """
    Defines the card variant to be used.
    """

    def init(self):
        super().init()
        self._internals["skip_properties"] = ["margin"]
