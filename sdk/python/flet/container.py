import json
from typing import Optional, Union

from beartype import beartype

from flet.alignment import Alignment
from flet.border import Border
from flet.constrained_control import ConstrainedControl
from flet.control import BlendMode, Control, OptionalNumber
from flet.control_event import ControlEvent
from flet.event_handler import EventHandler
from flet.gradients import Gradient
from flet.image import ImageFit, ImageRepeat
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    BorderRadiusValue,
    MarginValue,
    OffsetValue,
    PaddingValue,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class Container(ConstrainedControl):
    def __init__(
        self,
        content: Control = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        padding: PaddingValue = None,
        margin: MarginValue = None,
        alignment: Alignment = None,
        bgcolor: str = None,
        gradient: Gradient = None,
        blend_mode: BlendMode = None,
        border: Border = None,
        border_radius: BorderRadiusValue = None,
        image_src: str = None,
        image_src_base64: str = None,
        image_repeat: ImageRepeat = None,
        image_fit: ImageFit = None,
        image_opacity: OptionalNumber = None,
        ink: bool = None,
        animate: AnimationValue = None,
        on_click=None,
        on_long_press=None,
        on_hover=None,
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
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        def convert_container_tap_event_data(e):
            if self.ink:
                return e
            d = json.loads(e.data)
            return ContainerTapEvent(**d)

        self.__on_click = EventHandler(convert_container_tap_event_data)
        self._add_event_handler("click", self.__on_click.handler)

        self.content = content
        self.padding = padding
        self.margin = margin
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.gradient = gradient
        self.blend_mode = blend_mode
        self.border = border
        self.border_radius = border_radius
        self.image_src = image_src
        self.image_src_base64 = image_src_base64
        self.image_repeat = image_repeat
        self.image_fit = image_fit
        self.image_opacity = image_opacity
        self.ink = ink
        self.animate = animate
        self.on_click = on_click
        self.on_long_press = on_long_press
        self.on_hover = on_hover

    def _get_control_name(self):
        return "container"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("border", self.__border)
        self._set_attr_json("margin", self.__margin)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("animate", self.__animate)

    def _get_children(self):
        children = []
        if self.__content != None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # alignment
    @property
    def alignment(self):
        return self.__alignment

    @alignment.setter
    @beartype
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # margin
    @property
    def margin(self):
        return self.__margin

    @margin.setter
    @beartype
    def margin(self, value: MarginValue):
        self.__margin = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # gradient
    @property
    def gradient(self):
        return self.__gradient

    @gradient.setter
    @beartype
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # blend_mode
    @property
    def blend_mode(self):
        return self._get_attr("blendMode")

    @blend_mode.setter
    @beartype
    def blend_mode(self, value: Optional[BlendMode]):
        self._set_attr("blendMode", value)

    # border
    @property
    def border(self):
        return self.__border

    @border.setter
    @beartype
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self):
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # image_src
    @property
    def image_src(self):
        return self._get_attr("imageSrc")

    @image_src.setter
    def image_src(self, value):
        self._set_attr("imageSrc", value)

    # image_src_base64
    @property
    def image_src_base64(self):
        return self._get_attr("imageSrcBase64")

    @image_src_base64.setter
    def image_src_base64(self, value):
        self._set_attr("imageSrcBase64", value)

    # image_fit
    @property
    def image_fit(self):
        return self._get_attr("imageFit")

    @image_fit.setter
    @beartype
    def image_fit(self, value: ImageFit):
        self._set_attr("imageFit", value)

    # image_repeat
    @property
    def image_repeat(self):
        return self._get_attr("imageRepeat")

    @image_repeat.setter
    @beartype
    def image_repeat(self, value: ImageRepeat):
        self._set_attr("imageRepeat", value)

    # image_opacity
    @property
    def image_opacity(self):
        return self._get_attr("imageOpacity", data_type="float", def_value=1.0)

    @image_opacity.setter
    @beartype
    def image_opacity(self, value: OptionalNumber):
        self._set_attr("imageOpacity", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # ink
    @property
    def ink(self):
        return self._get_attr("ink", data_type="bool", def_value=False)

    @ink.setter
    @beartype
    def ink(self, value: Optional[bool]):
        self._set_attr("ink", value)

    # animate
    @property
    def animate(self) -> AnimationValue:
        return self.__animate

    @animate.setter
    @beartype
    def animate(self, value: AnimationValue):
        self.__animate = value

    # on_click
    @property
    def on_click(self):
        return self.__on_click

    @on_click.setter
    def on_click(self, handler):
        self.__on_click.subscribe(handler)
        if handler != None:
            self._set_attr("onclick", True)
        else:
            self._set_attr("onclick", None)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        if handler != None:
            self._set_attr("onLongPress", True)
        else:
            self._set_attr("onLongPress", None)

    # on_hover
    @property
    def on_hover(self):
        return self._get_event_handler("hover")

    @on_hover.setter
    def on_hover(self, handler):
        self._add_event_handler("hover", handler)
        if handler != None:
            self._set_attr("onHover", True)
        else:
            self._set_attr("onHover", None)


class ContainerTapEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
