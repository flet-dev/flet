from enum import Enum
from typing import Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.margin import OptionalMarginValue
from flet.core.types import ClipBehavior, OptionalColorValue, OptionalNumber

__all__ = ["Card", "CardVariant"]


class CardVariant(Enum):
    ELEVATED = "elevated"
    FILLED = "filled"
    OUTLINED = "outlined"


@control("Card")
class Card(ConstrainedControl, AdaptiveControl):
    """
    A material design card: a panel with slightly rounded corners and an elevation shadow.

    Example:
    ```
    import flet as ft

    def main(page):
        page.title = "Card Example"
        page.add(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.ALBUM),
                                title=ft.Text("The Enchanted Nightingale"),
                                subtitle=ft.Text(
                                    "Music by Julie Gable. Lyrics by Sidney Stein."
                                ),
                            ),
                            ft.Row(
                                [ft.TextButton("Buy tickets"), ft.TextButton("Listen")],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    padding=10,
                )
            )
        )

    ft.app(target=main)

    ```

    -----

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
