from typing import Any, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import OptionalNumber, TextAlign
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

FontWeight = Literal[
    None,
    "normal",
    "bold",
    "w100",
    "w200",
    "w300",
    "w400",
    "w500",
    "w600",
    "w700",
    "w800",
    "w900",
]

TextOverflow = Literal[None, "clip", "ellipsis", "fade", "visible"]

TextThemeStyle = Literal[
    "displayLarge",
    "displayMedium",
    "displaySmall",
    "headlineLarge",
    "headlineMedium",
    "headlineSmall",
    "titleLarge",
    "titleMedium",
    "titleSmall",
    "labelLarge",
    "labelMedium",
    "labelSmall",
    "bodyLarge",
    "bodyMedium",
    "bodySmall",
]


class Text(ConstrainedControl):
    def __init__(
        self,
        value: Optional[str] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # text-specific
        #
        text_align: TextAlign = None,
        font_family: Optional[str] = None,
        size: OptionalNumber = None,
        weight: FontWeight = None,
        italic: Optional[bool] = None,
        style: Optional[TextThemeStyle] = None,
        max_lines: Optional[int] = None,
        overflow: TextOverflow = None,
        selectable: Optional[bool] = None,
        no_wrap: Optional[bool] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        semantics_label: Optional[str] = None,
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
            on_animation_end=on_animation_end,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.value = value
        self.text_align = text_align
        self.font_family = font_family
        self.size = size
        self.weight = weight
        self.italic = italic
        self.no_wrap = no_wrap
        self.style = style
        self.max_lines = max_lines
        self.overflow = overflow
        self.selectable = selectable
        self.color = color
        self.bgcolor = bgcolor
        self.semantics_label = semantics_label

    def _get_control_name(self):
        return "text"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # text_align
    @property
    def text_align(self) -> TextAlign:
        return self._get_attr("textAlign")

    @text_align.setter
    @beartype
    def text_align(self, value: TextAlign):
        self._set_attr("textAlign", value)

    # font_family
    @property
    def font_family(self):
        return self._get_attr("fontFamily")

    @font_family.setter
    def font_family(self, value):
        self._set_attr("fontFamily", value)

    # size
    @property
    def size(self) -> OptionalNumber:
        return self._get_attr("size")

    @size.setter
    @beartype
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)

    # weight
    @property
    def weight(self) -> FontWeight:
        return self._get_attr("weight")

    @weight.setter
    @beartype
    def weight(self, value: FontWeight):
        self._set_attr("weight", value)

    # style
    @property
    def style(self) -> Optional[TextThemeStyle]:
        return self._get_attr("style")

    @style.setter
    @beartype
    def style(self, value: Optional[TextThemeStyle]):
        self._set_attr("style", value)

    # italic
    @property
    def italic(self) -> Optional[bool]:
        return self._get_attr("italic", data_type="bool", def_value=False)

    @italic.setter
    @beartype
    def italic(self, value: Optional[bool]):
        self._set_attr("italic", value)

    # no_wrap
    @property
    def no_wrap(self) -> Optional[bool]:
        return self._get_attr("italic", data_type="noWrap", def_value=False)

    @no_wrap.setter
    @beartype
    def no_wrap(self, value: Optional[bool]):
        self._set_attr("noWrap", value)

    # selectable
    @property
    def selectable(self) -> Optional[bool]:
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    @beartype
    def selectable(self, value: Optional[bool]):
        self._set_attr("selectable", value)

    # max_lines
    @property
    def max_lines(self) -> Optional[int]:
        return self._get_attr("maxLines")

    @max_lines.setter
    @beartype
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

    # overflow
    @property
    def overflow(self) -> TextOverflow:
        return self._get_attr("overflow")

    @overflow.setter
    @beartype
    def overflow(self, value: TextOverflow):
        self._set_attr("overflow", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # semantics_label
    @property
    def semantics_label(self):
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value):
        self._set_attr("semanticsLabel", value)
