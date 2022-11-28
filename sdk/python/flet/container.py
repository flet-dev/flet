import json
from typing import Any, Optional, Union

from beartype import beartype

from flet.alignment import Alignment
from flet.border import Border
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.control_event import ControlEvent
from flet.event_handler import EventHandler
from flet.gradients import Gradient
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    BlendMode,
    BlendModeString,
    BorderRadiusValue,
    BoxShape,
    ClipBehavior,
    ClipBehaviorString,
    ImageFit,
    ImageFitString,
    ImageRepeat,
    ImageRepeatString,
    MarginValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except:
    from typing_extensions import Literal


class Container(ConstrainedControl):
    """
    Container allows to decorate a control with background color and border and position it with padding, margin and alignment.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Container"

        c1 = ft.Container(
            content=ft.Text("Container with background"),
            bgcolor=ft.colors.AMBER_100,
            padding=5,
        )
        page.add(c1)

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/container
    """

    def __init__(
        self,
        content: Optional[Control] = None,
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
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        padding: PaddingValue = None,
        margin: MarginValue = None,
        alignment: Optional[Alignment] = None,
        bgcolor: Optional[str] = None,
        gradient: Optional[Gradient] = None,
        blend_mode: BlendMode = BlendMode.NONE,
        border: Optional[Border] = None,
        border_radius: BorderRadiusValue = None,
        image_src: Optional[str] = None,
        image_src_base64: Optional[str] = None,
        image_repeat: Optional[ImageRepeat] = None,
        image_fit: Optional[ImageFit] = None,
        image_opacity: OptionalNumber = None,
        shape: Optional[BoxShape] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        ink: Optional[bool] = None,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        def convert_container_tap_event_data(e):
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
        self.shape = shape
        self.clip_behavior = clip_behavior
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
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        """:obj:`Alignment`, optional: Align the child control within the container.

        Alignment is an instance of `alignment.Alignment` class object with `x` and `y` properties
        representing the distance from the center of a rectangle.
        """
        return self.__alignment

    @alignment.setter
    @beartype
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # margin
    @property
    def margin(self) -> MarginValue:
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
    def gradient(self) -> Optional[Gradient]:
        return self.__gradient

    @gradient.setter
    @beartype
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # blend_mode
    @property
    def blend_mode(self) -> BlendMode:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: BlendMode):
        self.__blend_mode = value
        if isinstance(value, BlendMode):
            self._set_attr("blendMode", value.value)
        else:
            self.__set_blend_mode(value)

    @beartype
    def __set_blend_mode(self, value: BlendModeString):
        self._set_attr("blendMode", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    @beartype
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
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
    def image_fit(self) -> Optional[ImageFit]:
        return self.__image_fit

    @image_fit.setter
    def image_fit(self, value: Optional[ImageFit]):
        self.__image_fit = value
        if isinstance(value, ImageFit):
            self._set_attr("imageFit", value.value)
        else:
            self.__set_image_fit(value)

    @beartype
    def __set_image_fit(self, value: ImageFitString):
        self._set_attr("imageFit", value)

    # image_repeat
    @property
    def image_repeat(self) -> Optional[ImageRepeat]:
        return self.__image_repeat

    @image_repeat.setter
    def image_repeat(self, value: Optional[ImageRepeat]):
        self.__image_repeat = value
        if isinstance(value, ImageRepeat):
            self._set_attr("imageRepeat", value.value)
        else:
            self.__set_image_repeat(value)

    @beartype
    def __set_image_repeat(self, value: ImageRepeatString):
        self._set_attr("imageRepeat", value)

    # image_opacity
    @property
    def image_opacity(self) -> OptionalNumber:
        return self._get_attr("imageOpacity", data_type="float", def_value=1.0)

    @image_opacity.setter
    @beartype
    def image_opacity(self, value: OptionalNumber):
        self._set_attr("imageOpacity", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # shape
    @property
    def shape(self):
        return self._get_attr("shape")

    @shape.setter
    @beartype
    def shape(self, value: Optional[BoxShape]):
        self._set_attr("shape", value.value if value is not None else None)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        if isinstance(value, ClipBehavior):
            self._set_attr("clipBehavior", value.value)
        else:
            self.__set_clip_behavior(value)

    @beartype
    def __set_clip_behavior(self, value: Optional[ClipBehaviorString]):
        self._set_attr("clipBehavior", value)

    # ink
    @property
    def ink(self) -> Optional[bool]:
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
        if handler is not None:
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
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_hover
    @property
    def on_hover(self):
        return self._get_event_handler("hover")

    @on_hover.setter
    def on_hover(self, handler):
        self._add_event_handler("hover", handler)
        if handler is not None:
            self._set_attr("onHover", True)
        else:
            self._set_attr("onHover", None)


class ContainerTapEvent(ControlEvent):
    def __init__(self, lx, ly, gx, gy) -> None:
        self.local_x: float = lx
        self.local_y: float = ly
        self.global_x: float = gx
        self.global_y: float = gy
