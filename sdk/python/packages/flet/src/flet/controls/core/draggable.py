from typing import Optional

from flet.controls.alignment import Axis
from flet.controls.control import Control, control
from flet.controls.types import OptionalControlEventCallable

__all__ = ["Draggable"]


@control("Draggable")
class Draggable(Control):
    """
    A control that can be dragged from to a `DragTarget`.

    When a draggable control recognizes the start of a drag gesture, it displays a `content_feedback` control that tracks the user's finger across the screen. If the user lifts their finger while on top of a `DragTarget`, that target is given the opportunity to complete drag-and-drop flow.

    Example:
    ```
    import flet
    from flet import (
        Column,
        Container,
        Draggable,
        DragTarget,
        DragTargetAcceptEvent,
        Page,
        Row,
        border,
        colors,
    )


    def main(page: Page):
        page.title = "Drag and Drop example"

        def drag_will_accept(e):
            e.control.content.border = border.all(
                2, colors.BLACK45 if e.data == "true" else colors.RED
            )
            e.control.update()

        def drag_accept(e: DragTargetAcceptEvent):
            src = page.get_control(e.src_id)
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None
            e.control.update()

        def drag_leave(e):
            e.control.content.border = None
            e.control.update()

        page.add(
            Row(
                [
                    Column(
                        [
                            Draggable(
                                group="color",
                                content=Container(
                                    width=50,
                                    height=50,
                                    bgcolor=colors.CYAN,
                                    border_radius=5,
                                ),
                                content_feedback=Container(
                                    width=20,
                                    height=20,
                                    bgcolor=colors.CYAN,
                                    border_radius=3,
                                ),
                            ),
                            Draggable(
                                group="color",
                                content=Container(
                                    width=50,
                                    height=50,
                                    bgcolor=colors.YELLOW,
                                    border_radius=5,
                                ),
                            ),
                            Draggable(
                                group="color1",
                                content=Container(
                                    width=50,
                                    height=50,
                                    bgcolor=colors.GREEN,
                                    border_radius=5,
                                ),
                            ),
                        ]
                    ),
                    Container(width=100),
                    DragTarget(
                        group="color",
                        content=Container(
                            width=50,
                            height=50,
                            bgcolor=colors.BLUE_GREY_100,
                            border_radius=5,
                        ),
                        on_will_accept=drag_will_accept,
                        on_accept=drag_accept,
                        on_leave=drag_leave,
                    ),
                ]
            )
        )


    flet.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/draggable
    """

    content: Control
    group: str = "default"
    content_when_dragging: Optional[Control] = None
    content_feedback: Optional[Control] = None
    axis: Optional[Axis] = None
    affinity: Optional[Axis] = None
    max_simultaneous_drags: Optional[int] = None
    on_drag_start: OptionalControlEventCallable = None
    on_drag_complete: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
        assert self.max_simultaneous_drags is None or (
            self.max_simultaneous_drags >= 0
        ), "max_simultaneous_drags must be greater than or equal to 0"
