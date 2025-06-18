
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalEventHandler
from flet.controls.core.window import WindowEvent
from flet.controls.events import DragEndEvent, DragStartEvent


@control("WindowDragArea")
class WindowDragArea(ConstrainedControl):
    """
    A control for drag to move, maximize and restore application window.

    When you have hidden the title bar with `page.window_title_bar_hidden`, you can add
    this control to move the window position.

    Online docs: https://flet.dev/docs/controls/windowdragarea
    """

    content: Control
    """
    The content of this `WindowDragArea`.
    """

    maximizable: bool = True
    """
    Whether double-clicking on the `WindowDragArea` should maximize/maximize the app's 
    window.
    Defaults to `True`.
    """

    on_double_tap: OptionalEventHandler[WindowEvent["WindowDragArea"]] = None
    """
    Fires when the `WindowDragArea` is double-tapped and `maximizable=True`.
    
    Event handler argument is of type `WindowEvent`, 
    with its `type` property being one of the following: `WindowEventType.MAXIMIZE`, 
    `WindowEventType.UNMAXIMIZE`
    """

    on_drag_start: OptionalEventHandler[DragStartEvent["WindowDragArea"]] = None
    """
    Fires when a pointer has contacted the screen and has begun to move/drag.

    Event handler argument is of type
    [`DragStartEvent`](https://flet.dev/docs/reference/types/dragstartevent).
    """

    on_drag_end: OptionalEventHandler[DragEndEvent["WindowDragArea"]] = None
    """
    Fires when a pointer that was previously in contact with the screen and 
    moving/dragging is no longer in contact with the screen.
    
    Event handler argument is of type
    [`DragEndEvent`](https://flet.dev/docs/reference/types/dragendevent).
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
