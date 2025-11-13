from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl


@control("ReorderableDraggable")
class ReorderableDraggable(LayoutControl, AdaptiveControl):
    """
    Used to drag an item in a [`ReorderableListView`][flet.].

    It creates a listener for a drag immediately following a pointer down
    event over the given [`content`][(c).] control.

    Example:
    ```python
    ft.ReorderableListView(
        expand=True,
        show_default_drag_handles=False,
        controls=[
            ft.ReorderableDraggable(
                content=ft.ListTile(
                    title=f"Draggable Item {i}",
                    bgcolor=ft.Colors.GREY if i % 2 == 0 else ft.Colors.BLUE_ACCENT,
                ),
            )
            for i in range(10)
        ],
    )
    ```
    """

    content: Control
    """
    The control for which the application would like to respond to a tap and
    drag gesture by starting a reordering drag on a reorderable list.

    Must be visible.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
