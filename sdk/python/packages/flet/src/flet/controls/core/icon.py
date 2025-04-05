from typing import Optional

from flet.controls.box import ShadowValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.types import BlendMode, IconValue, OptionalColorValue, OptionalNumber

__all__ = ["Icon"]


@control("Icon")
class Icon(ConstrainedControl):
    """
    Displays a Material icon.

    Icon browser: https://flet-icons-browser.fly.dev/#/

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.Row(
                [
                    ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.PINK),
                    ft.Icon(name=ft.icons.AUDIOTRACK, color=ft.colors.GREEN_400, size=30),
                    ft.Icon(name=ft.icons.BEACH_ACCESS, color=ft.colors.BLUE, size=50),
                    ft.Icon(name="settings", color="#c1c1c1"),
                ]
            )
        )

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/icon
    """

    name: Optional[IconValue] = None
    color: OptionalColorValue = None
    size: OptionalNumber = None
    semantics_label: Optional[str] = None
    shadows: Optional[ShadowValue] = None
    fill: OptionalNumber = None
    apply_text_scaling: Optional[bool] = None
    grade: OptionalNumber = None
    weight: OptionalNumber = None
    optical_size: OptionalNumber = None
    blend_mode: Optional[BlendMode] = None
