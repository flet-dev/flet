import dataclasses
import json
from dataclasses import field
from typing import Any, List, Optional, Union

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


@dataclasses.dataclass
class Paint:
    pass


class DrawShape(Control):
    def __init__(
        self,
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)


class DrawLine(DrawShape):
    def __init__(
        self,
        p1: OffsetValue = None,
        p2: OffsetValue = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.p1 = p1
        self.p2 = p2
        self.paint = paint

    def _get_control_name(self):
        return "line"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("p1", self.__p1)
        self._set_attr_json("p2", self.__p2)
        self._set_attr_json("paint", self.__paint)

    # p1
    @property
    def p1(self) -> OffsetValue:
        return self.__p1

    @p1.setter
    def p1(self, value: OffsetValue):
        self.__p1 = value

    # p2
    @property
    def p2(self) -> OffsetValue:
        return self.__p2

    @p2.setter
    def p2(self, value: OffsetValue):
        self.__p2 = value

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value


class DrawCircle(DrawShape):
    def __init__(
        self,
        center: OffsetValue = None,
        radius: OptionalNumber = None,
        paint: Optional[Paint] = None,
        # base
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        DrawShape.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.center = center
        self.radius = radius
        self.paint = paint

    def _get_control_name(self):
        return "circle"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("center", self.__center)
        self._set_attr_json("paint", self.__paint)

    # center
    @property
    def center(self) -> OffsetValue:
        return self.__center

    @center.setter
    def center(self, value: OffsetValue):
        self.__center = value

    # radius
    @property
    def radius(self) -> OptionalNumber:
        return self._get_attr("radius")

    @radius.setter
    def radius(self, value: OptionalNumber):
        self._set_attr("radius", value)

    # paint
    @property
    def paint(self) -> Optional[Paint]:
        return self.__paint

    @paint.setter
    def paint(self, value: Optional[Paint]):
        self.__paint = value


class CustomPaint(ConstrainedControl):
    def __init__(
        self,
        canvas: Optional[List[DrawShape]] = None,
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
            return CustomPaintResizeEvent(**d)

        self.__on_resize = EventHandler(convert_custom_paint_resize_event_data)
        self._add_event_handler("resize", self.__on_resize.get_handler())

        self.canvas = canvas
        self.resize_interval = resize_interval
        self.on_resize = on_resize

    def _get_control_name(self):
        return "custompaint"

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
    def canvas(self, value: Optional[List[DrawShape]]):
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


class CustomPaintResizeEvent(ControlEvent):
    def __init__(self, w, h) -> None:
        self.width: float = w
        self.height: float = h
