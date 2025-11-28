from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.types import MouseCursor


@control("ReorderableDragHandle")
class ReorderableDragHandle(LayoutControl, AdaptiveControl):
    """
    Used to drag an item in a [`ReorderableListView`][flet.].

    It creates a listener for a drag immediately following a pointer down
    event over the given [`content`][(c).] control.

    Example:
    ```python
    ft.ReorderableListView(
        show_default_drag_handles=False,
        controls=[
            ft.ListTile(
                title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                leading=ft.ReorderableDragHandle(
                    content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
                    mouse_cursor=ft.MouseCursor.GRAB,
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

    mouse_cursor: Optional[MouseCursor] = None
    """
    The mouse cursor for mouse pointers that are hovering over the control.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
