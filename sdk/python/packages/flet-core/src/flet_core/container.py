import json
from typing import Any, List, Optional, Tuple, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.alignment import Alignment
from flet_core.blur import Blur
from flet_core.border import Border
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.gradients import Gradient
from flet_core.ref import Ref
from flet_core.shadow import BoxShadow
from flet_core.theme import Theme
from flet_core.types import (
    AnimationValue,
    BlendMode,
    BorderRadiusValue,
    BoxShape,
    ClipBehavior,
    ImageFit,
    ImageRepeat,
    MarginValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ThemeMode,
)


class Container(ConstrainedControl, AdaptiveControl):
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
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
        ink_color: Optional[str] = None,
        animate: AnimationValue = None,
        blur: Union[
            None, float, int, Tuple[Union[float, int], Union[float, int]], Blur
        ] = None,
        shadow: Union[None, BoxShadow, List[BoxShadow]] = None,
        url: Optional[str] = None,
        url_target: Optional[str] = None,
        theme: Optional[Theme] = None,
        theme_mode: Optional[ThemeMode] = None,
        on_click=None,
        on_long_press=None,
        on_hover=None,
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
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        def convert_container_tap_event_data(e):
            d = json.loads(e.data)
            return ContainerTapEvent(**d)

        self.__on_click = EventHandler(convert_container_tap_event_data)
        self._add_event_handler("click", self.__on_click.get_handler())

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
        self.ink_color = ink_color
        self.animate = animate
        self.blur = blur
        self.shadow = shadow
        self.url = url
        self.url_target = url_target
        self.theme = theme
        self.theme_mode = theme_mode
        self.on_click = on_click
        self.on_long_press = on_long_press
        self.on_hover = on_hover

    def _get_control_name(self):
        return "container"

    def before_update(self):
        super().before_update()
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("border", self.__border)
        self._set_attr_json("margin", self.__margin)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("animate", self.__animate)
        self._set_attr_json("blur", self.__blur)
        self._set_attr_json("shadow", self.__shadow if self.__shadow else None)
        self._set_attr_json("theme", self.__theme)

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
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # margin
    @property
    def margin(self) -> MarginValue:
        return self.__margin

    @margin.setter
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
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # blend_mode
    @property
    def blend_mode(self) -> BlendMode:
        return self.__blend_mode

    @blend_mode.setter
    def blend_mode(self, value: BlendMode):
        self.__blend_mode = value
        self._set_attr(
            "blendMode", value.value if isinstance(value, BlendMode) else value
        )

    # blur
    @property
    def blur(self):
        return self.__blur

    @blur.setter
    def blur(
        self,
        value: Union[
            None, float, int, Tuple[Union[float, int], Union[float, int]], Blur
        ],
    ):
        self.__blur = value

    # shadow
    @property
    def shadow(self):
        return self.__shadow

    @shadow.setter
    def shadow(self, value: Union[None, BoxShadow, List[BoxShadow]]):
        self.__shadow = value if value is not None else []

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
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
        self._set_attr(
            "imageFit", value.value if isinstance(value, ImageFit) else value
        )

    # image_repeat
    @property
    def image_repeat(self) -> Optional[ImageRepeat]:
        return self.__image_repeat

    @image_repeat.setter
    def image_repeat(self, value: Optional[ImageRepeat]):
        self.__image_repeat = value
        self._set_attr(
            "imageRepeat", value.value if isinstance(value, ImageRepeat) else value
        )

    # image_opacity
    @property
    def image_opacity(self) -> OptionalNumber:
        return self._get_attr("imageOpacity", data_type="float", def_value=1.0)

    @image_opacity.setter
    def image_opacity(self, value: OptionalNumber):
        self._set_attr("imageOpacity", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # shape
    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[BoxShape]):
        self.__shape = value
        self._set_attr("shape", value.value if value is not None else None)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_attr(
            "clipBehavior", value.value if isinstance(value, ClipBehavior) else value
        )

    # ink
    @property
    def ink(self) -> Optional[bool]:
        return self._get_attr("ink", data_type="bool", def_value=False)

    @ink.setter
    def ink(self, value: Optional[bool]):
        self._set_attr("ink", value)

    # ink color
    @property
    def ink_color(self):
        return self._get_attr("inkColor")

    @ink_color.setter
    def ink_color(self, value):
        self._set_attr("inkColor", value)

    # animate
    @property
    def animate(self) -> AnimationValue:
        return self.__animate

    @animate.setter
    def animate(self, value: AnimationValue):
        self.__animate = value

    # url
    @property
    def url(self):
        return self._get_attr("url")

    @url.setter
    def url(self, value):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self):
        return self._get_attr("urlTarget")

    @url_target.setter
    def url_target(self, value):
        self._set_attr("urlTarget", value)

    # theme
    @property
    def theme(self) -> Optional[Theme]:
        return self.__theme

    @theme.setter
    def theme(self, value: Optional[Theme]):
        self.__theme = value

    # theme_mode
    @property
    def theme_mode(self) -> Optional[ThemeMode]:
        return self.__theme_mode

    @theme_mode.setter
    def theme_mode(self, value: Optional[ThemeMode]):
        self.__theme_mode = value
        self._set_attr("themeMode", value.value if value is not None else None)

    # on_click
    @property
    def on_click(self):
        return self.__on_click

    @on_click.setter
    def on_click(self, handler):
        self.__on_click.subscribe(handler)
        self._set_attr("onClick", True if handler is not None else None)


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
