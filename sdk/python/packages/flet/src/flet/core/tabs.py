from typing import Any, List, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.border import BorderSide
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.form_field_control import IconValueOrControl
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.types import (
    BorderRadiusValue,
    ClipBehavior,
    ColorEnums,
    ColorValue,
    ControlStateValue,
    IconEnums,
    IconValue,
    MarginValue,
    MouseCursor,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    TabAlignment,
)


class Tab(AdaptiveControl):
    def __init__(
        self,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        tab_content: Optional[Control] = None,
        icon: Optional[IconValueOrControl] = None,
        height: OptionalNumber = None,
        icon_margin: Optional[MarginValue] = None,
        #
        # Control and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        adaptive: Optional[bool] = None,
    ):
        Control.__init__(self, ref=ref, visible=visible)
        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.text = text
        self.icon = icon
        self.content = content
        self.tab_content = tab_content
        self.height = height
        self.icon_margin = icon_margin

    def _get_control_name(self):
        return "tab"

    def _get_children(self):
        children = []
        if self.__tab_content:
            self.__tab_content._set_attr_internal("n", "tab_content")
            children.append(self.__tab_content)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        if isinstance(self.__icon, Control):
            self.__icon._set_attr_internal("n", "icon")
            children.append(self.__icon)
        return children

    def before_update(self):
        super().before_update()
        self._set_attr_json("iconMargin", self.__icon_margin)
        if isinstance(self.__icon, IconValue):
            self._set_enum_attr("icon", self.__icon, IconEnums)

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("text")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("text", value)

    # height
    @property
    def height(self) -> Optional[float]:
        return self._get_attr("height", data_type="float")

    @height.setter
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # icon
    @property
    def icon(self) -> Optional[IconValueOrControl]:
        return self.__icon

    @icon.setter
    def icon(self, value: Optional[IconValueOrControl]):
        self.__icon = value

    # tab_content
    @property
    def tab_content(self) -> Optional[Control]:
        return self.__tab_content

    @tab_content.setter
    def tab_content(self, value: Optional[Control]):
        self.__tab_content = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # icon_margin
    @property
    def icon_margin(self) -> Optional[MarginValue]:
        return self.__icon_margin

    @icon_margin.setter
    def icon_margin(self, value: Optional[MarginValue]):
        self.__icon_margin = value


class Tabs(ConstrainedControl, AdaptiveControl):
    """
    The Tabs control is used for navigating frequently accessed, distinct content categories. Tabs allow for navigation between two or more content views and relies on text headers to articulate the different sections of content.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):

        t = ft.Tabs(
            selected_index=1,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Tab 1",
                    content=ft.Container(
                        content=ft.Text("This is Tab 1"), alignment=ft.alignment.center
                    ),
                ),
                ft.Tab(
                    tab_content=ft.Icon(ft.icons.SEARCH),
                    content=ft.Text("This is Tab 2"),
                ),
                ft.Tab(
                    text="Tab 3",
                    icon=ft.icons.SETTINGS,
                    content=ft.Text("This is Tab 3"),
                ),
            ],
            expand=1,
        )

        page.add(t)


    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/tabs
    """

    def __init__(
        self,
        tabs: Optional[List[Tab]] = None,
        selected_index: Optional[int] = None,
        scrollable: Optional[bool] = None,
        tab_alignment: Optional[TabAlignment] = None,
        animation_duration: Optional[int] = None,
        divider_color: Optional[ColorValue] = None,
        indicator_color: Optional[ColorValue] = None,
        indicator_border_radius: Optional[BorderRadiusValue] = None,
        indicator_border_side: Optional[BorderSide] = None,
        indicator_padding: Optional[PaddingValue] = None,
        indicator_tab_size: Optional[bool] = None,
        is_secondary: Optional[bool] = None,
        label_color: Optional[ColorValue] = None,
        label_padding: Optional[PaddingValue] = None,
        label_text_style: Optional[TextStyle] = None,
        unselected_label_color: Optional[ColorValue] = None,
        unselected_label_text_style: Optional[TextStyle] = None,
        overlay_color: ControlStateValue[ColorValue] = None,
        divider_height: OptionalNumber = None,
        indicator_thickness: OptionalNumber = None,
        enable_feedback: Optional[str] = None,
        mouse_cursor: Optional[MouseCursor] = None,
        padding: Optional[PaddingValue] = None,
        splash_border_radius: Optional[BorderRadiusValue] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        on_click: OptionalControlEventCallable = None,
        on_change: OptionalControlEventCallable = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.tabs = tabs
        self.selected_index = selected_index
        self.scrollable = scrollable
        self.tab_alignment = tab_alignment
        self.animation_duration = animation_duration
        self.divider_color = divider_color
        self.label_color = label_color
        self.unselected_label_color = unselected_label_color
        self.indicator_color = indicator_color
        self.indicator_border_radius = indicator_border_radius
        self.indicator_border_side = indicator_border_side
        self.indicator_padding = indicator_padding
        self.indicator_tab_size = indicator_tab_size
        self.overlay_color = overlay_color
        self.on_change = on_change
        self.divider_height = divider_height
        self.indicator_thickness = indicator_thickness
        self.enable_feedback = enable_feedback
        self.is_secondary = is_secondary
        self.mouse_cursor = mouse_cursor
        self.clip_behavior = clip_behavior
        self.label_padding = label_padding
        self.label_text_style = label_text_style
        self.unselected_label_text_style = unselected_label_text_style
        self.padding = padding
        self.splash_border_radius = splash_border_radius
        self.on_click = on_click

    def _get_control_name(self):
        return "tabs"

    def before_update(self):
        super().before_update()
        self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)
        self._set_attr_json("indicatorBorderRadius", self.__indicator_border_radius)
        self._set_attr_json("indicatorBorderSide", self.__indicator_border_side)
        self._set_attr_json("indicatorPadding", self.__indicator_padding)
        self._set_attr_json("labelPadding", self.__label_padding)
        self._set_attr_json("labelTextStyle", self.__label_text_style)
        self._set_attr_json(
            "unselectedLabelTextStyle", self.__unselected_label_text_style
        )

    def _get_children(self):
        return self.__tabs

    def __contains__(self, item):
        return item in self.__tabs

    # tabs
    @property
    def tabs(self) -> List[Tab]:
        return self.__tabs

    @tabs.setter
    def tabs(self, value: Optional[List[Tab]]):
        self.__tabs = value if value is not None else []

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)

    # selected_index
    @property
    def selected_index(self) -> int:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # scrollable
    @property
    def scrollable(self) -> bool:
        return self._get_attr("scrollable", data_type="bool", def_value=True)

    @scrollable.setter
    def scrollable(self, value: Optional[bool]):
        self._set_attr("scrollable", value)

    # mouse_cursor
    @property
    def mouse_cursor(self) -> Optional[MouseCursor]:
        return self.__mouse_cursor

    @mouse_cursor.setter
    def mouse_cursor(self, value: Optional[MouseCursor]):
        self.__mouse_cursor = value
        self._set_enum_attr("mouseCursor", value, MouseCursor)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # is_secondary
    @property
    def is_secondary(self) -> bool:
        return self._get_attr("isSecondary", data_type="bool", def_value=False)

    @is_secondary.setter
    def is_secondary(self, value: Optional[bool]):
        self._set_attr("isSecondary", value)

    # tab_alignment
    @property
    def tab_alignment(self) -> Optional[TabAlignment]:
        return self.__tab_alignment

    @tab_alignment.setter
    def tab_alignment(self, value: Optional[TabAlignment]):
        self.__tab_alignment = value
        self._set_enum_attr("tabAlignment", value, TabAlignment)

    # animation_duration
    @property
    def animation_duration(self) -> Optional[int]:
        return self._get_attr("animationDuration", data_type="int")

    @animation_duration.setter
    def animation_duration(self, value: Optional[int]):
        self._set_attr("animationDuration", value)

    # divider_height
    @property
    def divider_height(self) -> float:
        return self._get_attr("dividerHeight", data_type="float", def_value=1.0)

    @divider_height.setter
    def divider_height(self, value: OptionalNumber):
        self._set_attr("dividerHeight", value)

    # enable_feedback
    @property
    def enable_feedback(self):
        return self._get_attr("enableFeedback")

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # indicator_thickness
    @property
    def indicator_thickness(self) -> float:
        return self._get_attr("indicatorThickness", data_type="float", def_value=2.0)

    @indicator_thickness.setter
    def indicator_thickness(self, value: OptionalNumber):
        assert value is None or value > 0, "indicator_thickness must be greater than 0"
        self._set_attr("indicatorThickness", value)

    # divider_color
    @property
    def divider_color(self) -> Optional[ColorValue]:
        return self.__divider_color

    @divider_color.setter
    def divider_color(self, value: Optional[ColorValue]):
        self.__divider_color = value
        self._set_enum_attr("dividerColor", value, ColorEnums)

    # indicator_color
    @property
    def indicator_color(self) -> Optional[ColorValue]:
        return self.__indicator_color

    @indicator_color.setter
    def indicator_color(self, value: Optional[ColorValue]):
        self.__indicator_color = value
        self._set_enum_attr("indicatorColor", value, ColorEnums)

    # indicator_border_radius
    @property
    def indicator_border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__indicator_border_radius

    @indicator_border_radius.setter
    def indicator_border_radius(self, value: Optional[BorderRadiusValue]):
        self.__indicator_border_radius = value

    # indicator_border_side
    @property
    def indicator_border_side(self) -> Optional[BorderSide]:
        return self.__indicator_border_side

    @indicator_border_side.setter
    def indicator_border_side(self, value: Optional[BorderSide]):
        self.__indicator_border_side = value

    # indicator_padding
    @property
    def indicator_padding(self) -> Optional[PaddingValue]:
        return self.__indicator_padding

    @indicator_padding.setter
    def indicator_padding(self, value: Optional[PaddingValue]):
        self.__indicator_padding = value

    # indicator_tab_size
    @property
    def indicator_tab_size(self) -> bool:
        return self._get_attr("indicatorTabSize", data_type="bool", def_value=False)

    @indicator_tab_size.setter
    def indicator_tab_size(self, value: Optional[bool]):
        self._set_attr("indicatorTabSize", value)

    # label_color
    @property
    def label_color(self) -> Optional[ColorValue]:
        return self.__label_color

    @label_color.setter
    def label_color(self, value: Optional[ColorValue]):
        self.__label_color = value
        self._set_enum_attr("labelColor", value, ColorEnums)

    # unselected_label_color
    @property
    def unselected_label_color(self) -> Optional[ColorValue]:
        return self.__unselected_label_color

    @unselected_label_color.setter
    def unselected_label_color(self, value: Optional[ColorValue]):
        self.__unselected_label_color = value
        self._set_enum_attr("unselectedLabelColor", value, ColorEnums)

    # overlay_color
    @property
    def overlay_color(self) -> ControlStateValue[ColorValue]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: ControlStateValue[ColorValue]):
        self.__overlay_color = value

    # label_padding
    @property
    def label_padding(self) -> Optional[PaddingValue]:
        return self.__label_padding

    @label_padding.setter
    def label_padding(self, value: Optional[PaddingValue]):
        self.__label_padding = value

    # label_text_style
    @property
    def label_text_style(self) -> Optional[TextStyle]:
        return self.__label_text_style

    @label_text_style.setter
    def label_text_style(self, value: Optional[TextStyle]):
        self.__label_text_style = value

    # unselected_label_text_style
    @property
    def unselected_label_text_style(self) -> Optional[TextStyle]:
        return self.__unselected_label_text_style

    @unselected_label_text_style.setter
    def unselected_label_text_style(self, value: Optional[TextStyle]):
        self.__unselected_label_text_style = value

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # splash_border_radius
    @property
    def splash_border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__splash_border_radius

    @splash_border_radius.setter
    def splash_border_radius(self, value: Optional[BorderRadiusValue]):
        self.__splash_border_radius = value

    # on_click
    @property
    def on_click(self) -> OptionalControlEventCallable:
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler: OptionalControlEventCallable):
        self._add_event_handler("click", handler)
