import json
from typing import Any, Optional
from warnings import warn

from flet_core.control import Control
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref


class DragTarget(Control):
    """
    A control that completes drag operation when a `Draggable` widget is dropped.

    When a draggable is dragged on top of a drag target, the drag target is asked whether it will accept the data the draggable is carrying. The drag target will accept incoming drag if it belongs to the same group as draggable. If the user does drop the draggable on top of the drag target (and the drag target has indicated that it will accept the draggable's data), then the drag target is asked to accept the draggable's data.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Drag and Drop example"

        def drag_will_accept(e):
            e.control.content.border = ft.border.all(
                2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
            )
            e.control.update()

        def drag_accept(e: ft.DragTargetEvent):
            src = page.get_control(e.src_id)
            e.control.content.bgcolor = src.content.bgcolor
            e.control.content.border = None
            e.control.update()

        def drag_leave(e):
            e.control.content.border = None
            e.control.update()

        page.add(
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Draggable(
                                group="color",
                                content=ft.Container(
                                    width=50,
                                    height=50,
                                    bgcolor=ft.colors.CYAN,
                                    border_radius=5,
                                ),
                                content_feedback=ft.Container(
                                    width=20,
                                    height=20,
                                    bgcolor=ft.colors.CYAN,
                                    border_radius=3,
                                ),
                            ),
                            ft.Draggable(
                                group="color",
                                content=ft.Container(
                                    width=50,
                                    height=50,
                                    bgcolor=ft.colors.YELLOW,
                                    border_radius=5,
                                ),
                            ),
                            ft.Draggable(
                                group="color1",
                                content=ft.Container(
                                    width=50,
                                    height=50,
                                    bgcolor=ft.colors.GREEN,
                                    border_radius=5,
                                ),
                            ),
                        ]
                    ),
                    ft.Container(width=100),
                    ft.DragTarget(
                        group="color",
                        content=ft.Container(
                            width=50,
                            height=50,
                            bgcolor=ft.colors.BLUE_GREY_100,
                            border_radius=5,
                        ),
                        on_will_accept=drag_will_accept,
                        on_accept=drag_accept,
                        on_leave=drag_leave,
                    ),
                ]
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/dragtarget
    """

    def __init__(
        self,
        group: Optional[str] = None,
        content: Optional[Control] = None,
        on_will_accept=None,
        on_accept=None,
        on_leave=None,
        on_move=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        def convert_event_data(e):
            d = json.loads(e.data)
            return DragTargetEvent(**d)

        self.__on_accept = EventHandler(convert_event_data)
        self.__on_move = EventHandler(convert_event_data)
        self._add_event_handler("accept", self.__on_accept.get_handler())
        self._add_event_handler("move", self.__on_move.get_handler())

        self.__content: Optional[Control] = None

        self.group = group
        self.content = content
        self.on_will_accept = on_will_accept
        self.on_accept = on_accept
        self.on_leave = on_leave
        self.on_move = on_move

    def _get_control_name(self):
        return "dragtarget"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # group
    @property
    def group(self) -> Optional[str]:
        return self._get_attr("group")

    @group.setter
    def group(self, value: Optional[str]):
        self._set_attr("group", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_will_accept
    @property
    def on_will_accept(self):
        return self._get_event_handler("will_accept")

    @on_will_accept.setter
    def on_will_accept(self, handler):
        self._add_event_handler("will_accept", handler)

    # on_accept
    @property
    def on_accept(self):
        return self.__on_accept

    @on_accept.setter
    def on_accept(self, handler):
        self.__on_accept.subscribe(handler)

    # on_leave
    @property
    def on_leave(self):
        return self._get_event_handler("leave")

    @on_leave.setter
    def on_leave(self, handler):
        self._add_event_handler("leave", handler)

    # on_move
    @property
    def on_move(self):
        return self.__on_move

    @on_move.setter
    def on_move(self, handler):
        self.__on_move.subscribe(handler)


class DragTargetAcceptEvent(ControlEvent):
    def __init__(self, src_id, x, y) -> None:
        warn(
            f"{self.__class__.__name__} is deprecated since version 0.22.0 "
            f"and will be removed in version 1.0. Use DragTargetEvent instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        self.src_id: float = src_id
        self.x: float = x
        self.y: float = y


class DragTargetEvent(ControlEvent):
    def __init__(self, src_id, x, y) -> None:
        self.src_id: float = src_id
        self.x: float = x
        self.y: float = y
