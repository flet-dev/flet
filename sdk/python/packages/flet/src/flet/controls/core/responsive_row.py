from dataclasses import field
from typing import List, Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, ResponsiveNumber

__all__ = ["ResponsiveRow"]


@control("ResponsiveRow")
class ResponsiveRow(ConstrainedControl, AdaptiveControl):
    """
    ResponsiveRow allows aligning child controls to virtual columns. By default, a virtual grid has 12 columns, but that can be customized with `ResponsiveRow.columns` property.

    Similar to `expand` property, every control now has `col` property which allows specifying how many columns a control should span.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):

        page.add(
            ft.ResponsiveRow(
                [
                    ft.TextField(label="TextField 1", col={"md": 4}),
                    ft.TextField(label="TextField 2", col={"md": 4}),
                    ft.TextField(label="TextField 3", col={"md": 4}),
                ],
                run_spacing={"xs": 10},
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/responsiverow
    """

    controls: List[Control] = field(default_factory=list)
    columns: ResponsiveNumber = 12
    alignment: MainAxisAlignment = MainAxisAlignment.START
    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.START
    spacing: ResponsiveNumber = 10
    run_spacing: ResponsiveNumber = 10
    rtl: Optional[bool] = None

    def clean(self):
        super().clean()
        self.controls.clear()
