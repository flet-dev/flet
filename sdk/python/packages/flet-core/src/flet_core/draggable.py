from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


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

    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        group: Optional[str] = None,
        content: Optional[Control] = None,
        content_when_dragging: Optional[Control] = None,
        content_feedback: Optional[Control] = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__content: Optional[Control] = None
        self.__content_when_dragging: Optional[Control] = None
        self.__content_feedback: Optional[Control] = None

        self.group = group
        self.content = content
        self.content_when_dragging = content_when_dragging
        self.content_feedback = content_feedback

    def _get_control_name(self):
        return "draggable"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        if self.__content_when_dragging:
            self.__content_when_dragging._set_attr_internal(
                "n", "content_when_dragging"
            )
            children.append(self.__content_when_dragging)
        if self.__content_feedback:
            self.__content_feedback._set_attr_internal("n", "content_feedback")
            children.append(self.__content_feedback)
        return children

    # group
    @property
    def group(self):
        return self._get_attr("group")

    @group.setter
    def group(self, value):
        self._set_attr("group", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # content_when_dragging
    @property
    def content_when_dragging(self):
        return self.__content_when_dragging

    @content_when_dragging.setter
    def content_when_dragging(self, value):
        self.__content_when_dragging = value

    # content_feedback
    @property
    def content_feedback(self):
        return self.__content_feedback

    @content_feedback.setter
    def content_feedback(self, value):
        self.__content_feedback = value
