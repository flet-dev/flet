import json
from enum import Enum
from typing import Any, Optional, Union

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


class GestureDetector(ConstrainedControl):
    """
    A control that detects gestures.

    Attempts to recognize gestures that correspond to its non-null callbacks.

    If this control has a content, it defers to that child control for its sizing behavior. If it does not have a content, it grows to fit the parent instead.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def on_pan_update1(e: ft.DragUpdateEvent):
            c.top = max(0, c.top + e.delta_y)
            c.left = max(0, c.left + e.delta_x)
            c.update()

        def on_pan_update2(e: ft.DragUpdateEvent):
            e.control.top = max(0, e.control.top + e.delta_y)
            e.control.left = max(0, e.control.left + e.delta_x)
            e.control.update()

        gd = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=50,
            on_pan_update=on_pan_update1,
        )

        c = ft.Container(gd, bgcolor=ft.colors.AMBER, width=50, height=50, left=0, top=0)

        gd1 = ft.GestureDetector(
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=10,
            on_vertical_drag_update=on_pan_update2,
            left=100,
            top=100,
            content=ft.Container(bgcolor=ft.colors.BLUE, width=50, height=50),
        )

        page.add( ft.Stack([c, gd1], width=1000, height=500))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/gesturedetector
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
        on_animation_end=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        mouse_cursor: Optional[MouseCursor] = None,
        drag_interval: Optional[int] = None,
        hover_interval: Optional[int] = None,
        on_tap=None,
        on_tap_down=None,
        on_tap_up=None,
        on_multi_tap=None,
        multi_tap_touches=None,
        on_multi_long_press=None,
        on_secondary_tap=None,
        on_secondary_tap_down=None,
        on_secondary_tap_up=None,
        on_long_press_start=None,
        on_long_press_end=None,
        on_secondary_long_press_start=None,
        on_secondary_long_press_end=None,
        on_double_tap=None,
        on_double_tap_down=None,
        on_horizontal_drag_start=None,
        on_horizontal_drag_update=None,
        on_horizontal_drag_end=None,
        on_vertical_drag_start=None,
        on_vertical_drag_update=None,
        on_vertical_drag_end=None,
        on_pan_start=None,
        on_pan_update=None,
        on_pan_end=None,
        on_scale_start=None,
        on_scale_update=None,
        on_scale_end=None,
        on_hover=None,
        on_enter=None,
        on_exit=None,
        on_scroll=None,
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
            on_animation_end=on_animation_end,
            visible=visible,
            disabled=disabled,
            data=data,
        )

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

        self.__on_long_press_start = EventHandler(
            lambda e: LongPressStartEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "long_press_start", self.__on_long_press_start.get_handler()
        )

        self.__on_long_press_end = EventHandler(
            lambda e: LongPressEndEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "long_press_end", self.__on_long_press_end.get_handler()
        )

        self.__on_secondary_long_press_start = EventHandler(
            lambda e: LongPressStartEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_long_press_start",
            self.__on_secondary_long_press_start.get_handler(),
        )

        self.__on_secondary_long_press_end = EventHandler(
            lambda e: LongPressEndEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "secondary_long_press_end",
            self.__on_secondary_long_press_end.get_handler(),
        )
        self.__on_double_tap_down = EventHandler(
            lambda e: TapEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "double_tap_down", self.__on_double_tap_down.get_handler()
        )

        # on_horizontal_drag

        self.__on_horizontal_drag_start = EventHandler(
            lambda e: DragStartEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "horizontal_drag_start", self.__on_horizontal_drag_start.get_handler()
        )
        self.__on_horizontal_drag_update = EventHandler(
            lambda e: DragUpdateEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "horizontal_drag_update", self.__on_horizontal_drag_update.get_handler()
        )
        self.__on_horizontal_drag_end = EventHandler(
            lambda e: DragEndEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "horizontal_drag_end", self.__on_horizontal_drag_end.get_handler()
        )

        # on_vertical_drag

        self.__on_vertical_drag_start = EventHandler(
            lambda e: DragStartEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "vertical_drag_start", self.__on_vertical_drag_start.get_handler()
        )
        self.__on_vertical_drag_update = EventHandler(
            lambda e: DragUpdateEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "vertical_drag_update", self.__on_vertical_drag_update.get_handler()
        )
        self.__on_vertical_drag_end = EventHandler(
            lambda e: DragEndEvent(**json.loads(e.data))
        )
        self._add_event_handler(
            "vertical_drag_end", self.__on_vertical_drag_end.get_handler()
        )

        # on_pan

        self.__on_pan_start = EventHandler(
            lambda e: DragStartEvent(**json.loads(e.data))
        )
        self._add_event_handler("pan_start", self.__on_pan_start.get_handler())
        self.__on_pan_update = EventHandler(
            lambda e: DragUpdateEvent(**json.loads(e.data))
        )
        self._add_event_handler("pan_update", self.__on_pan_update.get_handler())
        self.__on_pan_end = EventHandler(lambda e: DragEndEvent(**json.loads(e.data)))
        self._add_event_handler("pan_end", self.__on_pan_end.get_handler())

        # on_scale

        self.__on_scale_start = EventHandler(
            lambda e: ScaleStartEvent(**json.loads(e.data))
        )
        self._add_event_handler("scale_start", self.__on_scale_start.get_handler())
        self.__on_scale_update = EventHandler(
            lambda e: ScaleUpdateEvent(**json.loads(e.data))
        )
        self._add_event_handler("scale_update", self.__on_scale_update.get_handler())
        self.__on_scale_end = EventHandler(
            lambda e: ScaleEndEvent(**json.loads(e.data))
        )
        self._add_event_handler("scale_end", self.__on_scale_end.get_handler())

        # on_hover

        self.__on_hover = EventHandler(lambda e: HoverEvent(**json.loads(e.data)))
        self._add_event_handler("hover", self.__on_hover.get_handler())
        self.__on_enter = EventHandler(lambda e: HoverEvent(**json.loads(e.data)))
        self._add_event_handler("enter", self.__on_enter.get_handler())
        self.__on_exit = EventHandler(lambda e: HoverEvent(**json.loads(e.data)))
        self._add_event_handler("exit", self.__on_exit.get_handler())

        # on_scroll
        self.__on_scroll = EventHandler(lambda e: ScrollEvent(**json.loads(e.data)))
        self._add_event_handler("scroll", self.__on_scroll.get_handler())

        self.content = content
        self.mouse_cursor = mouse_cursor
        self.drag_interval = drag_interval
        self.hover_interval = hover_interval
        self.on_tap = on_tap
        self.on_tap_down = on_tap_down
        self.on_tap_up = on_tap_up
        self.on_multi_tap = on_multi_tap
        self.multi_tap_touches = multi_tap_touches
        self.on_multi_long_press = on_multi_long_press
        self.on_secondary_tap = on_secondary_tap
        self.on_secondary_tap_down = on_secondary_tap_down
        self.on_secondary_tap_up = on_secondary_tap_up
        self.on_long_press_start = on_long_press_start
        self.on_long_press_end = on_long_press_end
        self.on_secondary_long_press_start = on_secondary_long_press_start
        self.on_secondary_long_press_end = on_secondary_long_press_end
        self.on_double_tap = on_double_tap
        self.on_double_tap_down = on_double_tap_down
        self.on_horizontal_drag_start = on_horizontal_drag_start
        self.on_horizontal_drag_update = on_horizontal_drag_update
        self.on_horizontal_drag_end = on_horizontal_drag_end
        self.on_vertical_drag_start = on_vertical_drag_start
        self.on_vertical_drag_update = on_vertical_drag_update
        self.on_vertical_drag_end = on_vertical_drag_end
        self.on_pan_start = on_pan_start
        self.on_pan_update = on_pan_update
        self.on_pan_end = on_pan_end
        self.on_scale_start = on_scale_start
        self.on_scale_update = on_scale_update
        self.on_scale_end = on_scale_end
        self.on_hover = on_hover
        self.on_enter = on_enter
        self.on_exit = on_exit
        self.on_scroll = on_scroll

    def _get_control_name(self):
        return "gesturedetector"

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

    # mouse_cursor
    @property
    def mouse_cursor(self):
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_attr("mouseCursor", value.value if value is not None else None)

    # drag_interval
    @property
    def drag_interval(self) -> Optional[int]:
        return self._get_attr("dragInterval")

    @drag_interval.setter
    def drag_interval(self, value: Optional[int]):
        self._set_attr("dragInterval", value)

    # hover_interval
    @property
    def hover_interval(self) -> Optional[int]:
        return self._get_attr("hoverInterval")

    @hover_interval.setter
    def hover_interval(self, value: Optional[int]):
        self._set_attr("hoverInterval", value)

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

    # on_multi_long_press
    @property
    def on_multi_long_press(self):
        return self._get_event_handler("multi_long_press")

    @on_multi_long_press.setter
    def on_multi_long_press(self, handler):
        self._add_event_handler("multi_long_press", handler)
        self._set_attr("onMultiLongPress", True if handler is not None else None)

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

    # on_long_press_start
    @property
    def on_long_press_start(self):
        return self.__on_long_press_start

    @on_long_press_start.setter
    def on_long_press_start(self, handler):
        self.__on_long_press_start.subscribe(handler)
        self._set_attr("onLongPressStart", True if handler is not None else None)

    # on_long_press_end
    @property
    def on_long_press_end(self):
        return self.__on_long_press_end

    @on_long_press_end.setter
    def on_long_press_end(self, handler):
        self.__on_long_press_end.subscribe(handler)
        self._set_attr("onLongPressEnd", True if handler is not None else None)

    # on_secondary_long_press_start
    @property
    def on_secondary_long_press_start(self):
        return self.__on_secondary_long_press_start

    @on_secondary_long_press_start.setter
    def on_secondary_long_press_start(self, handler):
        self.__on_secondary_long_press_start.subscribe(handler)
        self._set_attr(
            "onSecondaryLongPressStart", True if handler is not None else None
        )

    # on_secondary_long_press_end
    @property
    def on_secondary_long_press_end(self):
        return self.__on_secondary_long_press_end

    @on_secondary_long_press_end.setter
    def on_secondary_long_press_end(self, handler):
        self.__on_secondary_long_press_end.subscribe(handler)
        self._set_attr("onSecondaryLongPressEnd", True if handler is not None else None)

    # on_double_tap
    @property
    def on_double_tap(self):
        return self._get_event_handler("double_tap")

    @on_double_tap.setter
    def on_double_tap(self, handler):
        self._add_event_handler("double_tap", handler)
        self._set_attr("onDoubleTap", True if handler is not None else None)

    # on_double_tap_down
    @property
    def on_double_tap_down(self):
        return self.__on_double_tap_down

    @on_double_tap_down.setter
    def on_double_tap_down(self, handler):
        self.__on_double_tap_down.subscribe(handler)
        self._set_attr("onDoubleTapDown", True if handler is not None else None)

    # on_horizontal_drag_start
    @property
    def on_horizontal_drag_start(self):
        return self.__on_horizontal_drag_start

    @on_horizontal_drag_start.setter
    def on_horizontal_drag_start(self, handler):
        self.__on_horizontal_drag_start.subscribe(handler)
        self._set_attr("onHorizontalDragStart", True if handler is not None else None)

    # on_horizontal_drag_update
    @property
    def on_horizontal_drag_update(self):
        return self.__on_horizontal_drag_update

    @on_horizontal_drag_update.setter
    def on_horizontal_drag_update(self, handler):
        self.__on_horizontal_drag_update.subscribe(handler)
        self._set_attr("onHorizontalDragUpdate", True if handler is not None else None)

    # on_horizontal_drag_end
    @property
    def on_horizontal_drag_end(self):
        return self.__on_horizontal_drag_end

    @on_horizontal_drag_end.setter
    def on_horizontal_drag_end(self, handler):
        self.__on_horizontal_drag_end.subscribe(handler)
        self._set_attr("onHorizontalDragEnd", True if handler is not None else None)

    # on_vertical_drag_start
    @property
    def on_vertical_drag_start(self):
        return self.__on_vertical_drag_start

    @on_vertical_drag_start.setter
    def on_vertical_drag_start(self, handler):
        self.__on_vertical_drag_start.subscribe(handler)
        self._set_attr("onVerticalDragStart", True if handler is not None else None)

    # on_vertical_drag_update
    @property
    def on_vertical_drag_update(self):
        return self.__on_vertical_drag_update

    @on_vertical_drag_update.setter
    def on_vertical_drag_update(self, handler):
        self.__on_vertical_drag_update.subscribe(handler)
        self._set_attr("onVerticalDragUpdate", True if handler is not None else None)

    # on_vertical_drag_end
    @property
    def on_vertical_drag_end(self):
        return self.__on_vertical_drag_end

    @on_vertical_drag_end.setter
    def on_vertical_drag_end(self, handler):
        self.__on_vertical_drag_end.subscribe(handler)
        self._set_attr("onVerticalDragEnd", True if handler is not None else None)

    # on_pan_start
    @property
    def on_pan_start(self):
        return self.__on_pan_start

    @on_pan_start.setter
    def on_pan_start(self, handler):
        self.__on_pan_start.subscribe(handler)
        self._set_attr("onPanStart", True if handler is not None else None)

    # on_pan_updatevertical_drag
    @property
    def on_pan_update(self):
        return self.__on_pan_update

    @on_pan_update.setter
    def on_pan_update(self, handler):
        self.__on_pan_update.subscribe(handler)
        self._set_attr("onPanUpdate", True if handler is not None else None)

    # on_pan_end
    @property
    def on_pan_end(self):
        return self.__on_pan_end

    @on_pan_end.setter
    def on_pan_end(self, handler):
        self.__on_pan_end.subscribe(handler)
        self._set_attr("onPanEnd", True if handler is not None else None)

    # on_scale_start
    @property
    def on_scale_start(self):
        return self.__on_scale_start

    @on_scale_start.setter
    def on_scale_start(self, handler):
        self.__on_scale_start.subscribe(handler)
        self._set_attr("onScaleStart", True if handler is not None else None)

    # on_scale_update
    @property
    def on_scale_update(self):
        return self.__on_scale_update

    @on_scale_update.setter
    def on_scale_update(self, handler):
        self.__on_scale_update.subscribe(handler)
        self._set_attr("onScaleUpdate", True if handler is not None else None)

    # on_scale_end
    @property
    def on_scale_end(self):
        return self.__on_scale_end

    @on_scale_end.setter
    def on_scale_end(self, handler):
        self.__on_scale_end.subscribe(handler)
        self._set_attr("onScaleEnd", True if handler is not None else None)

    # on_hover
    @property
    def on_hover(self):
        return self.__on_hover

    @on_hover.setter
    def on_hover(self, handler):
        self.__on_hover.subscribe(handler)
        self._set_attr("onHover", True if handler is not None else None)

    # on_enter
    @property
    def on_enter(self):
        return self.__on_enter

    @on_enter.setter
    def on_enter(self, handler):
        self.__on_enter.subscribe(handler)
        self._set_attr("onEnter", True if handler is not None else None)

    # on_exit
    @property
    def on_exit(self):
        return self.__on_exit

    @on_exit.setter
    def on_exit(self, handler):
        self.__on_exit.subscribe(handler)
        self._set_attr("onExit", True if handler is not None else None)

    # on_scroll
    @property
    def on_scroll(self):
        return self.__on_scroll

    @on_scroll.setter
    def on_scroll(self, handler):
        self.__on_scroll.subscribe(handler)
        self._set_attr("onScroll", True if handler is not None else None)


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


class LongPressStartEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy


class LongPressEndEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy, vx, vy) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.velocity_x: float = vx
        self.velocity_y: float = vy


class DragStartEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy, kind, ts) -> None:
        self.kind: str = kind
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.timestamp: Optional[int] = ts


class DragUpdateEvent(ControlEvent):
    def __init__(self, dx, dy, pd, lx, ly, gx, gy, ts) -> None:
        self.delta_x: float = dx
        self.delta_y: float = dy
        self.primary_delta: Optional[float] = pd
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
        self.timestamp: Optional[int] = ts


class DragEndEvent(ControlEvent):
    def __init__(self, pv, vx, vy) -> None:
        self.primary_velocity: Optional[float] = pv
        self.velocity_x: float = vx
        self.velocity_y: float = vy


class ScaleStartEvent(ControlEvent):
    def __init__(self, fpx, fpy, lfpx, lfpy, pc) -> None:
        self.focal_point_x: float = fpx
        self.focal_point_y: float = fpy
        self.local_focal_point_x: float = lfpx
        self.local_focal_point_y: float = lfpy
        self.pointer_count: int = pc


class ScaleUpdateEvent(ControlEvent):
    def __init__(self, fpx, fpy, fpdx, fpdy, lfpx, lfpy, pc, hs, vs, s, r) -> None:
        self.focal_point_x: float = fpx
        self.focal_point_y: float = fpy
        self.focal_point_delta_x: float = fpdx
        self.focal_point_delta_y: float = fpdy
        self.local_focal_point_x: float = lfpx
        self.local_focal_point_y: float = lfpy
        self.pointer_count: int = pc
        self.horizontal_scale: float = hs
        self.vertical_scale: float = vs
        self.scale: float = s
        self.rotation: float = r


class ScaleEndEvent(ControlEvent):
    def __init__(self, pc, vx, vy) -> None:
        self.pointer_count: int = pc
        self.velocity_x: float = vx
        self.velocity_y: float = vy


class HoverEvent(ControlEvent):
    def __init__(self, ts, kind, gx, gy, lx, ly, dx=None, dy=None) -> None:
        self.timestamp: float = ts
        self.kind: str = kind
        self.global_x: float = gx
        self.global_y: float = gy
        self.local_x: float = lx
        self.local_y: float = ly
        self.delta_x: Optional[float] = dx
        self.delta_y: Optional[float] = dy


class ScrollEvent(ControlEvent):
    def __init__(self, gx, gy, lx, ly, dx=None, dy=None) -> None:
        self.global_x: float = gx
        self.global_y: float = gy
        self.local_x: float = lx
        self.local_y: float = ly
        self.scroll_delta_x: Optional[float] = dx
        self.scroll_delta_y: Optional[float] = dy
