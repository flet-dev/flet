from enum import Enum
from typing import Any, Optional, Union

from flet_core.adaptive_control import AdaptiveControl
from flet_core.buttons import OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.theme import ThemeVisualDensity
from flet_core.types import (
    AnimationValue,
    MouseCursor,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    UrlTarget,
    OptionalEventCallable,
)


class ListTileTitleAlignment(Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"
    THREE_LINE = "threeLine"
    TITLE_HEIGHT = "titleHeight"


class ListTileStyle(Enum):
    LIST = "list"
    DRAWER = "drawer"


class ListTile(ConstrainedControl, AdaptiveControl):
    """
    A single fixed-height row that typically contains some text as well as a leading or trailing icon.

    Example:

    ```
    import flet as ft

    def main(page):
        page.title = "ListTile Example"
        page.add(
            ft.Card(
                content=ft.Container(
                    width=500,
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text("One-line list tile"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.SETTINGS),
                                title=ft.Text("One-line selected list tile"),
                                selected=True,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.symmetric(vertical=10),
                )
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/listtile
    """

    def __init__(
        self,
        content_padding: PaddingValue = None,
        bgcolor: Optional[str] = None,
        bgcolor_activated: Optional[str] = None,
        hover_color: Optional[str] = None,
        leading: Optional[Control] = None,
        title: Optional[Control] = None,
        subtitle: Optional[Control] = None,
        trailing: Optional[Control] = None,
        is_three_line: Optional[bool] = None,
        selected: Optional[bool] = None,
        dense: Optional[bool] = None,
        autofocus: Optional[bool] = None,
        toggle_inputs: Optional[bool] = None,
        selected_color: Optional[str] = None,
        selected_tile_color: Optional[str] = None,
        style: Optional[ListTileStyle] = None,
        enable_feedback: Optional[bool] = None,
        horizontal_spacing: OptionalNumber = None,
        min_leading_width: OptionalNumber = None,
        min_vertical_padding: OptionalNumber = None,
        url: Optional[str] = None,
        url_target: Optional[UrlTarget] = None,
        title_alignment: Optional[ListTileTitleAlignment] = None,
        icon_color: Optional[str] = None,
        text_color: Optional[str] = None,
        shape: Optional[OutlinedBorder] = None,
        visual_density: Optional[ThemeVisualDensity] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        title_text_style: Optional[TextStyle] = None,
        subtitle_text_style: Optional[TextStyle] = None,
        leading_and_trailing_text_style: Optional[TextStyle] = None,
        min_height: OptionalNumber = None,
        on_click=None,
        on_long_press=None,
        #
        # ConstrainedControl and AdaptiveControl
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
        on_animation_end: OptionalEventCallable = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
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
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.content_padding = content_padding
        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.trailing = trailing
        self.is_three_line = is_three_line
        self.selected = selected
        self.dense = dense
        self.autofocus = autofocus
        self.toggle_inputs = toggle_inputs
        self.url = url
        self.url_target = url_target
        self.bgcolor = bgcolor
        self.bgcolor_activated = bgcolor_activated
        self.hover_color = hover_color
        self.on_click = on_click
        self.on_long_press = on_long_press
        self.style = style
        self.selected_color = selected_color
        self.selected_tile_color = selected_tile_color
        self.enable_feedback = enable_feedback
        self.horizontal_spacing = horizontal_spacing
        self.min_leading_width = min_leading_width
        self.min_vertical_padding = min_vertical_padding
        self.title_alignment = title_alignment
        self.icon_color = icon_color
        self.text_color = text_color
        self.shape = shape
        self.visual_density = visual_density
        self.mouse_cursor = mouse_cursor
        self.title_text_style = title_text_style
        self.subtitle_text_style = subtitle_text_style
        self.leading_and_trailing_text_style = leading_and_trailing_text_style
        self.min_height = min_height

    def _get_control_name(self):
        return "listtile"

    def before_update(self):
        super().before_update()
        self._set_attr_json("contentPadding", self.__content_padding)
        if isinstance(self.__shape, OutlinedBorder):
            self._set_attr_json("shape", self.__shape)
        if isinstance(self.__title_text_style, TextStyle):
            self._set_attr_json("titleTextStyle", self.__title_text_style)
        if isinstance(self.__subtitle_text_style, TextStyle):
            self._set_attr_json("subtitleTextStyle", self.__subtitle_text_style)
        if isinstance(self.__leading_and_trailing_text_style, TextStyle):
            self._set_attr_json(
                "leadingAndTrailingTextStyle", self.__leading_and_trailing_text_style
            )

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__subtitle:
            self.__subtitle._set_attr_internal("n", "subtitle")
            children.append(self.__subtitle)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        return children

    # content_padding
    @property
    def content_padding(self) -> PaddingValue:
        return self.__content_padding

    @content_padding.setter
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # selected_color
    @property
    def selected_color(self) -> Optional[str]:
        return self._get_attr("selectedColor")

    @selected_color.setter
    def selected_color(self, value: Optional[str]):
        self._set_attr("selectedColor", value)

    # selected_tile_color
    @property
    def selected_tile_color(self) -> Optional[str]:
        return self._get_attr("selectedTileColor")

    @selected_tile_color.setter
    def selected_tile_color(self, value: Optional[str]):
        self._set_attr("selectedTileColor", value)

    # bgcolor_activated
    @property
    def bgcolor_activated(self) -> Optional[str]:
        return self._get_attr("bgcolorActivated")

    @bgcolor_activated.setter
    def bgcolor_activated(self, value: Optional[str]):
        self._set_attr("bgcolorActivated", value)

    # min_leading_width
    @property
    def min_leading_width(self) -> OptionalNumber:
        return self._get_attr("minLeadingWidth", data_type="float", def_value=40)

    @min_leading_width.setter
    def min_leading_width(self, value: OptionalNumber):
        self._set_attr("minLeadingWidth", value)

    # horizontal_spacing
    @property
    def horizontal_spacing(self) -> OptionalNumber:
        return self._get_attr("horizontalSpacing", data_type="float", def_value=16)

    @horizontal_spacing.setter
    def horizontal_spacing(self, value: OptionalNumber):
        self._set_attr("horizontalSpacing", value)

    # min_height
    @property
    def min_height(self) -> OptionalNumber:
        return self._get_attr("minHeight", data_type="float")

    @min_height.setter
    def min_height(self, value: OptionalNumber):
        self._set_attr("minHeight", value)

    # hover_color
    @property
    def hover_color(self) -> Optional[str]:
        return self._get_attr("hoverColor")

    @hover_color.setter
    def hover_color(self, value: Optional[str]):
        self._set_attr("hoverColor", value)

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # min_vertical_padding
    @property
    def min_vertical_padding(self) -> OptionalNumber:
        return self._get_attr("minVerticalPadding", data_type="float", def_value=4.0)

    @min_vertical_padding.setter
    def min_vertical_padding(self, value: OptionalNumber):
        self._set_attr("minVerticalPadding", value)

    # subtitle
    @property
    def subtitle(self) -> Optional[Control]:
        return self.__subtitle

    @subtitle.setter
    def subtitle(self, value: Optional[Control]):
        self.__subtitle = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # is_three_line
    @property
    def is_three_line(self) -> Optional[bool]:
        return self._get_attr("isThreeLine", data_type="bool", def_value=False)

    @is_three_line.setter
    def is_three_line(self, value: Optional[bool]):
        self._set_attr("isThreeLine", value)

    # enable_feedback
    @property
    def enable_feedback(self) -> Optional[bool]:
        return self._get_attr("enableFeedback", data_type="bool", def_value=True)

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # style
    @property
    def style(self) -> Optional[ListTileStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ListTileStyle]):
        self.__style = value
        self._set_enum_attr("style", value, ListTileStyle)

    # title_alignment
    @property
    def title_alignment(self) -> Optional[ListTileTitleAlignment]:
        return self.__title_alignment

    @title_alignment.setter
    def title_alignment(self, value: Optional[ListTileTitleAlignment]):
        self.__title_alignment = value
        self._set_enum_attr("titleAlignment", value, ListTileTitleAlignment)

    # selected
    @property
    def selected(self) -> Optional[bool]:
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # dense
    @property
    def dense(self) -> Optional[bool]:
        return self._get_attr("dense", data_type="bool", def_value=False)

    @dense.setter
    def dense(self, value: Optional[bool]):
        self._set_attr("dense", value)

    # autofocus
    @property
    def autofocus(self) -> Optional[bool]:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # toggle_inputs
    @property
    def toggle_inputs(self) -> Optional[bool]:
        return self._get_attr("toggleInputs", data_type="bool", def_value=False)

    @toggle_inputs.setter
    def toggle_inputs(self, value: Optional[bool]):
        self._set_attr("toggleInputs", value)

    # url
    @property
    def url(self) -> Optional[str]:
        return self._get_attr("url")

    @url.setter
    def url(self, value: Optional[str]):
        self._set_attr("url", value)

    # icon_color
    @property
    def icon_color(self) -> Optional[str]:
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value: Optional[str]):
        self._set_attr("iconColor", value)

    # text_color
    @property
    def text_color(self) -> Optional[str]:
        return self._get_attr("textColor")

    @text_color.setter
    def text_color(self, value: Optional[str]):
        self._set_attr("textColor", value)

    # url_target
    @property
    def url_target(self) -> Optional[UrlTarget]:
        return self.__url_target

    @url_target.setter
    def url_target(self, value: Optional[UrlTarget]):
        self.__url_target = value
        self._set_enum_attr("urlTarget", value, UrlTarget)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # visual_density
    @property
    def visual_density(self) -> Optional[ThemeVisualDensity]:
        return self.__visual_density

    @visual_density.setter
    def visual_density(self, value: Optional[ThemeVisualDensity]):
        self.__visual_density = value
        self._set_enum_attr("visualDensity", value, ThemeVisualDensity)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # title_text_style
    @property
    def title_text_style(self) -> Optional[TextStyle]:
        return self.__title_text_style

    @title_text_style.setter
    def title_text_style(self, value: Optional[TextStyle]):
        self.__title_text_style = value

    # subtitle_text_style
    @property
    def subtitle_text_style(self) -> Optional[TextStyle]:
        return self.__subtitle_text_style

    @subtitle_text_style.setter
    def subtitle_text_style(self, value: Optional[TextStyle]):
        self.__subtitle_text_style = value

    # leading_and_trailing_text_style
    @property
    def leading_and_trailing_text_style(self) -> Optional[TextStyle]:
        return self.__leading_and_trailing_text_style

    @leading_and_trailing_text_style.setter
    def leading_and_trailing_text_style(self, value: Optional[TextStyle]):
        self.__leading_and_trailing_text_style = value

    # on_click
    @property
    def on_click(self) -> OptionalEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalEventCallable):
        self._add_event_handler("click", handler)
        self._set_attr("onclick", True if handler is not None else None)

    # on_long_press
    @property
    def on_long_press(self) -> OptionalEventCallable:
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler: OptionalEventCallable):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_focus
    @property
    def on_focus(self) -> OptionalEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalEventCallable):
        self._add_event_handler("blur", handler)
