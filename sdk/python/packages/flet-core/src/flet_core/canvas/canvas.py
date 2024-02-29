import json
from typing import Any, List, Optional, Union

from flet_core.canvas.shape import Shape
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
from flet_core.utils import deprecated


class Canvas(ConstrainedControl):
    def __init__(
        self,
        shapes: Optional[List[Shape]] = None,
        content: Optional[Control] = None,
        resize_interval: OptionalNumber = None,
        on_resize=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
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
        on_animation_end=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
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

        self.shapes = shapes
        self.content = content
        self.resize_interval = resize_interval
        self.on_resize = on_resize

    def _get_control_name(self):
        return "canvas"

    def _get_children(self):
        children = []
        children.extend(self.__shapes)
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def clean(self):
        super().clean()
        self.__shapes.clear()

    @deprecated(
        reason="Use clean() method instead.", version="0.21.0", delete_version="1.0"
    )
    async def clean_async(self):
        self.clean()

    # shapes
    @property
    def shapes(self) -> List[Shape]:
        return self.__shapes

    @shapes.setter
    def shapes(self, value: Optional[List[Shape]]):
        self.__shapes = value if value is not None else []

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # resize_interval
    @property
    def resize_interval(self) -> OptionalNumber:
        return self._get_attr("resizeInterval")

    @resize_interval.setter
    def resize_interval(self, value: OptionalNumber):
        self._set_attr("resizeInterval", value)

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
