from flet.core.control import Control, control
from flet.core.types import OptionalControlEventCallable

__all__ = ["SelectionArea"]


@control("SelectionArea")
class SelectionArea(Control):
    """
    Flet controls are not selectable by default. SelectionArea is used to enable selection for its child control.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.add(
            ft.SelectionArea(
                content=ft.Column([ft.Text("Selectable text"), ft.Text("Also selectable")])
            )
        )
        page.add(ft.Text("Not selectable"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/selectionarea
    """

    content: Control
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
