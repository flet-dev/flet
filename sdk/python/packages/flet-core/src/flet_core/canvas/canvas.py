import json
from typing import Any, List, Optional, TypeVar, Union

from flet_core.canvas.shape import Shape
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
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

TShape = TypeVar("TShape", bound=Shape)


class Canvas(ConstrainedControl):
    def __init__(
        self,
        canvas: Optional[List[TShape]] = None,
        ref: Optional[Ref] = None,
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
        # CustomPaint specific
        #
        resize_interval: OptionalNumber = None,
        on_resize=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
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

        def convert_custom_paint_resize_event_data(e):
            d = json.loads(e.data)
            return CanvasResizeEvent(**d)

        self.__on_resize = EventHandler(convert_custom_paint_resize_event_data)
        self._add_event_handler("resize", self.__on_resize.get_handler())

        self.canvas = canvas
        self.resize_interval = resize_interval
        self.on_resize = on_resize

    def _get_control_name(self):
        return "canvas"

    def _get_children(self):
        return self.__canvas

    def clean(self):
        super().clean()
        self.__canvas.clear()

    async def clean_async(self):
        await super().clean_async()
        self.__canvas.clear()

    # resize_interval
    @property
    def resize_interval(self) -> OptionalNumber:
        return self._get_attr("resizeInterval")

    @resize_interval.setter
    def resize_interval(self, value: OptionalNumber):
        self._set_attr("resizeInterval", value)

    # canvas
    @property
    def canvas(self):
        return self.__canvas

    @canvas.setter
    def canvas(self, value: Optional[List[TShape]]):
        self.__canvas = value if value is not None else []

    # on_resize
    @property
    def on_resize(self):
        return self.__on_resize

    @on_resize.setter
    def on_resize(self, handler):
        self.__on_resize.subscribe(handler)
        if handler is not None:
            self._set_attr("onresize", True)
        else:
            self._set_attr("onresize", None)


class CanvasResizeEvent(ControlEvent):
    def __init__(self, w, h) -> None:
        self.width: float = w
        self.height: float = h
