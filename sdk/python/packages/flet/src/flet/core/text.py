import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union
from warnings import warn

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.text_span import TextSpan
from flet.core.text_style import TextOverflow, TextStyle, TextThemeStyle
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ColorEnums,
    ColorValue,
    FontWeight,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TextAlign,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class TextAffinity(Enum):
    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"


@dataclass
class TextSelection:
    start: Optional[int] = None
    end: Optional[int] = None
    selection: Optional[str] = None
    base_offset: Optional[int] = None
    extent_offset: Optional[int] = None
    affinity: Optional[TextAffinity] = None
    directional: Optional[bool] = None
    collapsed: Optional[bool] = None
    valid: Optional[bool] = None
    normalized: Optional[bool] = None


class TextSelectionChangeCause(Enum):
    UNKNOWN = "unknown"
    TAP = "tap"
    DOUBLE_TAP = "doubleTap"
    LONG_PRESS = "longPress"
    FORCE_PRESS = "forcePress"
    KEYBOARD = "keyboard"
    TOOLBAR = "toolbar"
    DRAG = "drag"
    SCRIBBLE = "scribble"


class TextSelectionChangeEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.text: str = d.get("text")
        self.cause = TextSelectionChangeCause(d.get("cause"))
        start = d.get("start")
        end = d.get("end")
        self.selection = TextSelection(
            start=start,
            end=end,
            selection=self.text[start:end] if (start != -1 and end != -1) else "",
            base_offset=d.get("base_offset"),
            extent_offset=d.get("extent_offset"),
            affinity=d.get("affinity"),
            directional=d.get("directional"),
            collapsed=d.get("collapsed"),
            valid=d.get("valid"),
            normalized=d.get("normalized"),
        )


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
        text_align: Optional[TextAlign] = None,
        font_family: Optional[str] = None,
        size: OptionalNumber = None,
        weight: Optional[FontWeight] = None,
        italic: Optional[bool] = None,
        style: Union[TextThemeStyle, TextStyle, None] = None,
        theme_style: Optional[TextThemeStyle] = None,
        max_lines: Optional[int] = None,
        overflow: Optional[TextOverflow] = None,
        selectable: Optional[bool] = None,
        no_wrap: Optional[bool] = None,
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        semantics_label: Optional[str] = None,
        show_selection_cursor: Optional[bool] = None,
        enable_interactive_selection: Optional[bool] = None,
        selection_cursor_width: OptionalNumber = None,
        selection_cursor_height: OptionalNumber = None,
        selection_cursor_color: Optional[ColorValue] = None,
        on_tap: OptionalControlEventCallable = None,
        on_selection_change: OptionalEventCallable[TextSelectionChangeEvent] = None,
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
        rotate: Optional[RotateValue] = None,
        scale: Optional[ScaleValue] = None,
        offset: Optional[OffsetValue] = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
        )

        self.__on_selection_change = EventHandler(lambda e: TextSelectionChangeEvent(e))

        self._add_event_handler(
            "selection_change", self.__on_selection_change.get_handler()
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
        self.on_tap = on_tap
        self.on_selection_change = on_selection_change
        self.show_selection_cursor = show_selection_cursor
        self.enable_interactive_selection = enable_interactive_selection
        self.selection_cursor_width = selection_cursor_width
        self.selection_cursor_height = selection_cursor_height
        self.selection_cursor_color = selection_cursor_color

    def _get_control_name(self):
        return "text"

    def _get_children(self):
        return self.__spans

    def before_update(self):
        super().before_update()
        if isinstance(self.__style, TextStyle):
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
    def spans(self) -> List[TextSpan]:
        return self.__spans

    @spans.setter
    def spans(self, value: Optional[List[TextSpan]]):
        self.__spans = value if value is not None else []

    # text_align
    @property
    def text_align(self) -> Optional[TextAlign]:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: Optional[TextAlign]):
        self.__text_align = value
        self._set_enum_attr("textAlign", value, TextAlign)

    # font_family
    @property
    def font_family(self) -> Optional[str]:
        return self._get_attr("fontFamily")

    @font_family.setter
    def font_family(self, value: Optional[str]):
        self._set_attr("fontFamily", value)

    # size
    @property
    def size(self) -> OptionalNumber:
        return self._get_attr("size", data_type="float")

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
        self._set_enum_attr("weight", value, FontWeight)

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
    def theme_style(self) -> Optional[TextThemeStyle]:
        return self.__theme_style

    @theme_style.setter
    def theme_style(self, value: Optional[TextThemeStyle]):
        self.__theme_style = value
        self._set_enum_attr("theme_style", value, TextThemeStyle)

    # italic
    @property
    def italic(self) -> bool:
        return self._get_attr("italic", data_type="bool", def_value=False)

    @italic.setter
    def italic(self, value: Optional[bool]):
        self._set_attr("italic", value)

    # no_wrap
    @property
    def no_wrap(self) -> bool:
        return self._get_attr("italic", data_type="noWrap", def_value=False)

    @no_wrap.setter
    def no_wrap(self, value: Optional[bool]):
        self._set_attr("noWrap", value)

    # selectable
    @property
    def selectable(self) -> bool:
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
    def overflow(self) -> Optional[TextOverflow]:
        return self.__overflow

    @overflow.setter
    def overflow(self, value: Optional[TextOverflow]):
        self.__overflow = value
        self._set_enum_attr("overflow", value, TextOverflow)

    # color
    @property
    def color(self) -> Optional[ColorValue]:
        return self.__color

    @color.setter
    def color(self, value: Optional[ColorValue]):
        self.__color = value
        self._set_enum_attr("color", value, ColorEnums)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # semantics_label
    @property
    def semantics_label(self) -> Optional[str]:
        return self._get_attr("semanticsLabel")

    @semantics_label.setter
    def semantics_label(self, value: Optional[str]):
        self._set_attr("semanticsLabel", value)

    # selection_cursor_color
    @property
    def selection_cursor_color(self) -> Optional[str]:
        return self._get_attr("selectionCursorColor")

    @selection_cursor_color.setter
    def selection_cursor_color(self, value: Optional[str]):
        self._set_attr("selectionCursorColor", value)

    # selection_cursor_height
    @property
    def selection_cursor_height(self) -> OptionalNumber:
        return self._get_attr("selectionCursorHeight", data_type="float")

    @selection_cursor_height.setter
    def selection_cursor_height(self, value: OptionalNumber):
        self._set_attr("selectionCursorHeight", value)

    # selection_cursor_width
    @property
    def selection_cursor_width(self) -> OptionalNumber:
        return self._get_attr("selectionCursorWidth", data_type="float", def_value=2.0)

    @selection_cursor_width.setter
    def selection_cursor_width(self, value: OptionalNumber):
        self._set_attr("selectionCursorWidth", value)

    # show_selection_cursor
    @property
    def show_selection_cursor(self) -> Optional[bool]:
        return self._get_attr("showSelectionCursor", data_type="bool", def_value=False)

    @show_selection_cursor.setter
    def show_selection_cursor(self, value: Optional[bool]):
        self._set_attr("showSelectionCursor", value)

    # enable_interactive_selection
    @property
    def enable_interactive_selection(self) -> Optional[bool]:
        return self._get_attr(
            "enableInteractiveSelection", data_type="bool", def_value=True
        )

    @enable_interactive_selection.setter
    def enable_interactive_selection(self, value: Optional[bool]):
        self._set_attr("enableInteractiveSelection", value)

    # on_tap
    @property
    def on_tap(self) -> OptionalControlEventCallable:
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler: OptionalControlEventCallable):
        self._add_event_handler("tap", handler)

    # on_selection_change
    @property
    def on_selection_change(
        self,
    ) -> OptionalEventCallable[TextSelectionChangeEvent]:
        return self.__on_selection_change.handler

    @on_selection_change.setter
    def on_selection_change(
        self, handler: OptionalEventCallable[TextSelectionChangeEvent]
    ):
        self.__on_selection_change.handler = handler
