import json
from enum import Enum
from typing import Any, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class MouseCursor(Enum):
    ALIAS = "alias"
    ALL_SCROLL = "allScroll"
    BASIC = "basic"
    CELL = "cell"
    CLICK = "click"
    CONTEXT_MENU = "contextMenu"
    COPY = "copy"
    DISAPPEARING = "disappearing"
    FORBIDDEN = "forbidden"
    GRAB = "grab"
    GRABBING = "grabbing"
    HELP = "help"
    MOVE = "move"
    NO_DROP = "noDrop"
    NONE = "none"
    PRECISE = "precise"
    PROGRESS = "progress"
    RESIZE_COLUMN = "resizeColumn"
    RESIZE_DOWN = "resizeDown"
    RESIZE_DOWN_LEFT = "resizeDownLeft"
    RESIZE_DOWN_RIGHT = "resizeDownRight"
    RESIZE_LEFT = "resizeLeft"
    RESIZE_LEFT_RIGHT = "resizeLeftRight"
    RESIZE_RIGHT = "resizeRight"
    RESIZE_ROW = "resizeRow"
    RESIZE_UP = "resizeUp"
    RESIZE_UP_DOWN = "resizeUpDown"
    RESIZE_UP_LEFT = "resizeUpLeft"
    RESIZE_UP_LEFT_DOWN_RIGHT = "resizeUpLeftDownRight"
    RESIZE_UP_RIGHT = "resizeUpRight"
    RESIZE_UP_RIGHT_DOWN_LEFT = "resizeUpRightDownLeft"
    TEXT = "text"
    VERTICAL_TEXT = "verticalText"
    WAIT = "wait"
    ZOOM_IN = "zoomIn"
    ZOOM_OUT = "zoomOut"


class InkWell(ConstrainedControl, AdaptiveControl):
    """
    A control that detects gestures.

    Attempts to recognize gestures that correspond to its non-null callbacks.

    If this control has a content, it defers to that child control for its sizing behavior. If it does not have a content, it grows to fit the parent instead.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def change_color(e):
            if box.bgcolor == ft.colors.AMBER:
                box.bgcolor = ft.colors.BLUE
            else:
                box.bgcolor = ft.colors.AMBER
            box.update()
            print("on_tap")

        page.add(
            ft.InkWell(
                on_tap=lambda e: print("on_tap"),
                content=ft.Container(
                    ft.Text("Click me!"),
                ),
            ),
            ft.InkWell(
                on_double_tap=change_color,
                content=ft.Container(
                    box := ft.Container(
                        bgcolor=ft.colors.AMBER,
                        height=100,
                        content=ft.Text(
                            "double tap to change color", color=ft.colors.BLACK
                        ),
                    ),
                ),
            ),
            ft.Row(
                [
                    ft.Text("Don't have an account?"),
                    ft.InkWell(
                        on_tap=lambda e: print("Sign Up"),
                        content=ft.Text("Click me for Sign Up", color=ft.colors.BLUE),
                    ),
                ],
                spacing=4,
            ),
        )


    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/inkwell
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        mouse_cursor: Optional[MouseCursor] = None,
        on_tap=None,
        on_tap_down=None,
        on_tap_up=None,
        on_multi_tap=None,
        multi_tap_touches=None,
        on_secondary_tap=None,
        on_secondary_tap_down=None,
        on_secondary_tap_up=None,
        on_double_tap=None,
        #
        # Adaptive
        #
        adaptive: Optional[bool] = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__on_tap_down = EventHandler(lambda e: TapEvent(**json.loads(e.data)))
        self._add_event_handler("tap_down", self.__on_tap_down.get_handler())

        self.__on_tap_up = EventHandler(lambda e: TapEvent(**json.loads(e.data)))
        self._add_event_handler("tap_up", self.__on_tap_up.get_handler())

        self.__on_multi_tap = EventHandler(
            lambda e: MultiTapEvent(e.data.lower() == "true")
        )
        self._add_event_handler("multi_tap", self.__on_multi_tap.get_handler())

        self.__on_secondary_tap_down = EventHandler(
            lambda e: TapEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_tap_down", self.__on_secondary_tap_down.get_handler()
        )

        self.__on_secondary_tap_up = EventHandler(
            lambda e: TapEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_tap_up", self.__on_secondary_tap_up.get_handler()
        )

        self.mouse_cursor = mouse_cursor
        self.content = content
        self.on_tap = on_tap
        self.on_tap_down = on_tap_down
        self.on_tap_up = on_tap_up
        self.on_multi_tap = on_multi_tap
        self.multi_tap_touches = multi_tap_touches
        self.on_secondary_tap = on_secondary_tap
        self.on_secondary_tap_down = on_secondary_tap_down
        self.on_secondary_tap_up = on_secondary_tap_up
        self.on_double_tap = on_double_tap

    def _get_control_name(self):
        return "inkwell"

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_tap
    @property
    def on_tap(self):
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler):
        self._add_event_handler("tap", handler)
        self._set_attr("onTap", True if handler is not None else None)

    # on_tap_down
    @property
    def on_tap_down(self):
        return self.__on_tap_down

    @on_tap_down.setter
    def on_tap_down(self, handler):
        self.__on_tap_down.subscribe(handler)
        self._set_attr("onTapDown", True if handler is not None else None)

    # on_tap_up
    @property
    def on_tap_up(self):
        return self.__on_tap_up

    @on_tap_up.setter
    def on_tap_up(self, handler):
        self.__on_tap_up.subscribe(handler)
        self._set_attr("onTapUp", True if handler is not None else None)

    # on_multi_tap
    @property
    def on_multi_tap(self):
        return self.__on_multi_tap

    @on_multi_tap.setter
    def on_multi_tap(self, handler):
        self.__on_multi_tap.subscribe(handler)
        self._set_attr("onMultiTap", True if handler is not None else None)

    # multi_tap_touches
    @property
    def multi_tap_touches(self) -> Optional[int]:
        return self._get_attr("multiTapTouches")

    @multi_tap_touches.setter
    def multi_tap_touches(self, value: Optional[int]):
        self._set_attr("multiTapTouches", value)

    # on_secondary_tap
    @property
    def on_secondary_tap(self):
        return self._get_event_handler("secondary_tap")

    @on_secondary_tap.setter
    def on_secondary_tap(self, handler):
        self._add_event_handler("secondary_tap", handler)
        self._set_attr("onSecondaryTap", True if handler is not None else None)

    # on_tap_down
    @property
    def on_secondary_tap_down(self):
        return self.__on_secondary_tap_down

    @on_secondary_tap_down.setter
    def on_secondary_tap_down(self, handler):
        self.__on_secondary_tap_down.subscribe(handler)
        self._set_attr("onSecondaryTapDown", True if handler is not None else None)

    # on_secondary_tap_up
    @property
    def on_secondary_tap_up(self):
        return self.__on_secondary_tap_up

    @on_secondary_tap_up.setter
    def on_secondary_tap_up(self, handler):
        self.__on_secondary_tap_up.subscribe(handler)
        self._set_attr("onSecondaryTapUp", True if handler is not None else None)

    # on_double_tap
    @property
    def on_double_tap(self):
        return self._get_event_handler("double_tap")

    @on_double_tap.setter
    def on_double_tap(self, handler):
        self._add_event_handler("double_tap", handler)
        self._set_attr("onDoubleTap", True if handler is not None else None)

    # mouse_cursor
    @property
    def mouse_cursor(self):
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_attr("mouseCursor", value.value if value is not None else None)


class TapEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy, kind) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.kind: str = kind


class MultiTapEvent(ControlEvent):
    def __init__(self, correct_touches: bool) -> None:
        self.correct_touches: bool = correct_touches
