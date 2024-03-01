import dataclasses
from enum import Enum
from typing import Any, List, Optional, Union
from warnings import warn

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import OptionalNumber
from flet_core.ref import Ref
from flet_core.text_span import TextSpan
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    FontWeight,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

TextOverflowString = Literal[None, "clip", "ellipsis", "fade", "visible"]


class TextOverflow(Enum):
    NONE = None
    CLIP = "clip"
    ELLIPSIS = "ellipsis"
    FADE = "fade"
    VISIBLE = "visible"


class TextThemeStyle(Enum):
    DISPLAY_LARGE = "displayLarge"
    DISPLAY_MEDIUM = "displayMedium"
    DISPLAY_SMALL = "displaySmall"
    HEADLINE_LARGE = "headlineLarge"
    HEADLINE_MEDIUM = "headlineMedium"
    HEADLINE_SMALL = "headlineSmall"
    TITLE_LARGE = "titleLarge"
    TITLE_MEDIUM = "titleMedium"
    TITLE_SMALL = "titleSmall"
    LABEL_LARGE = "labelLarge"
    LABEL_MEDIUM = "labelMedium"
    LABEL_SMALL = "labelSmall"
    BODY_LARGE = "bodyLarge"
    BODY_MEDIUM = "bodyMedium"
    BODY_SMALL = "bodySmall"


class Text(ConstrainedControl):
    """
    Text is a control for displaying text.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Text examples"

        page.add(
            ft.Text("Size 10", size=10),
            ft.Text("Size 30, Italic", size=20, color="pink600", italic=True),
            ft.Text("Limit long text to 2 lines and fading", style=ft.TextThemeStyle.HEADLINE_SMALL),
            ft.Text(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur quis nibh vitae purus consectetur facilisis sed vitae ipsum. Quisque faucibus sed nulla placerat sagittis. Phasellus condimentum risus vitae nulla vestibulum auctor. Curabitur scelerisque, nibh eget imperdiet consequat, odio ante tempus diam, sed volutpat nisl erat eget turpis. Sed viverra, diam sit amet blandit vulputate, mi tellus dapibus lorem, vitae vehicula diam mauris placerat diam. Morbi sit amet pretium turpis, et consequat ligula. Nulla velit sem, suscipit sit amet dictum non, tincidunt sed nulla. Aenean pellentesque odio porttitor sagittis aliquam. Nam varius at metus vitae vulputate. Praesent faucibus nibh lorem, eu pretium dolor dictum nec. Phasellus eget dui laoreet, viverra magna vitae, pellentesque diam.",
                max_lines=2,
            ),
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/text
    """

    def __init__(
        self,
        value: Optional[str] = None,
        spans: Optional[List[TextSpan]] = None,
        text_align: TextAlign = TextAlign.NONE,
        font_family: Optional[str] = None,
        size: OptionalNumber = None,
        weight: Optional[FontWeight] = None,
        italic: Optional[bool] = None,
        style: Union[TextThemeStyle, TextStyle, None] = None,
        theme_style: Optional[TextThemeStyle] = None,
        max_lines: Optional[int] = None,
        overflow: TextOverflow = TextOverflow.NONE,
        selectable: Optional[bool] = None,
        no_wrap: Optional[bool] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        semantics_label: Optional[str] = None,
        #
        # ConstrainedControl
        #
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

        self.value = value
        self.spans = spans
        self.text_align = text_align
        self.font_family = font_family
        self.size = size
        self.weight = weight
        self.italic = italic
        self.no_wrap = no_wrap
        self.style = style
        self.theme_style = theme_style
        self.max_lines = max_lines
        self.overflow = overflow
        self.selectable = selectable
        self.color = color
        self.bgcolor = bgcolor
        self.semantics_label = semantics_label

    def _get_control_name(self):
        return "text"

    def _get_children(self):
        children = []
        children.extend(self.__spans)
        return children

    def before_update(self):
        super().before_update()
        if dataclasses.is_dataclass(self.__style):
            self._set_attr_json("style", self.__style)

    # value
    @property
    def value(self) -> Optional[str]:
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # spans
    @property
    def spans(self) -> Optional[List[TextSpan]]:
        return self.__spans

    @spans.setter
    def spans(self, value: Optional[List[TextSpan]]):
        self.__spans = value if value is not None else []

    # text_align
    @property
    def text_align(self) -> TextAlign:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: TextAlign):
        self.__text_align = value
        self._set_attr(
            "textAlign", value.value if isinstance(value, TextAlign) else value
        )

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
    def size(self, value: OptionalNumber):
        self._set_attr("size", value)

    # weight
    @property
    def weight(self) -> Optional[FontWeight]:
        return self.__weight

    @weight.setter
    def weight(self, value: Optional[FontWeight]):
        self.__weight = value
        self._set_attr(
            "weight", value.value if isinstance(value, FontWeight) else value
        )

    # style
    @property
    def style(self) -> Union[TextThemeStyle, TextStyle, None]:
        return self.__style

    @style.setter
    def style(self, value: Union[TextThemeStyle, TextStyle, None]):
        self.__style = value
        if isinstance(value, (TextThemeStyle, str)) or value is None:
            self._set_attr(
                "style", value.value if isinstance(value, TextThemeStyle) else value
            )
            if value is not None:
                warn(
                    "If you wish to set the TextThemeStyle, use `Text.theme_style` instead. "
                    "The `Text.style` property should be used to set the TextStyle only.",
                    stacklevel=2,
                    category=DeprecationWarning,
                )

    # theme_style
    @property
    def theme_style(self):
        return self._get_attr("theme_style")

    @theme_style.setter
    def theme_style(self, value: Optional[TextThemeStyle]):
        self._set_attr(
            "theme_style", value.value if isinstance(value, TextThemeStyle) else value
        )

    # italic
    @property
    def italic(self) -> Optional[bool]:
        return self._get_attr("italic", data_type="bool", def_value=False)

    @italic.setter
    def italic(self, value: Optional[bool]):
        self._set_attr("italic", value)

    # no_wrap
    @property
    def no_wrap(self) -> Optional[bool]:
        return self._get_attr("italic", data_type="noWrap", def_value=False)

    @no_wrap.setter
    def no_wrap(self, value: Optional[bool]):
        self._set_attr("noWrap", value)

    # selectable
    @property
    def selectable(self) -> Optional[bool]:
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    def selectable(self, value: Optional[bool]):
        self._set_attr("selectable", value)

    # max_lines
    @property
    def max_lines(self) -> Optional[int]:
        return self._get_attr("maxLines")

    @max_lines.setter
    def max_lines(self, value: Optional[int]):
        self._set_attr("maxLines", value)

    # overflow
    @property
    def overflow(self) -> TextOverflow:
        return self.__overflow

    @overflow.setter
    def overflow(self, value: TextOverflow):
        self.__overflow = value
        self._set_attr(
            "overflow", value.value if isinstance(value, TextOverflow) else value
        )

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
