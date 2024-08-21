from enum import Enum
from typing import Any, Callable, List, Optional, Union

from flet_core.buttons import OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    OptionalNumber,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
)


class NavigationRailLabelType(Enum):
    NONE = "none"
    ALL = "all"
    SELECTED = "selected"


class NavigationRailDestination(Control):
    def __init__(
        self,
        icon: Optional[str] = None,
        icon_content: Optional[Control] = None,
        selected_icon: Optional[str] = None,
        selected_icon_content: Optional[Control] = None,
        label: Optional[str] = None,
        label_content: Optional[Control] = None,
        padding: PaddingValue = None,
        indicator_color: Optional[str] = None,
        indicator_shape: Optional[OutlinedBorder] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ) -> None:
        Control.__init__(self, ref=ref, disabled=disabled, data=data)
        self.label = label
        self.icon = icon
        self.icon_content = icon_content
        self.selected_icon = selected_icon
        self.selected_icon_content = selected_icon_content
        self.label_content = label_content
        self.padding = padding
        self.indicator_color = indicator_color
        self.indicator_shape = indicator_shape

    def _get_control_name(self):
        return "navigationraildestination"

    def before_update(self) -> None:
        super().before_update()
        self._set_attr_json("padding", self.__padding)
        if isinstance(self.__indicator_shape, OutlinedBorder):
            self._set_attr_json("indicatorShape", self.__indicator_shape)

    def _get_children(self):
        children = []
        if self.__label_content:
            self.__label_content._set_attr_internal("n", "label_content")
            children.append(self.__label_content)
        if self.__icon_content:
            self.__icon_content._set_attr_internal("n", "icon_content")
            children.append(self.__icon_content)
        if self.__selected_icon_content:
            self.__selected_icon_content._set_attr_internal(
                "n", "selected_icon_content"
            )
            children.append(self.__selected_icon_content)
        return children

    # icon
    @property
    def icon(self) -> Optional[str]:
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value: Optional[str]):
        self._set_attr("icon", value)

    # icon_content
    @property
    def icon_content(self) -> Optional[Control]:
        return self.__icon_content

    @icon_content.setter
    def icon_content(self, value: Optional[Control]):
        self.__icon_content = value

    # selected_icon
    @property
    def selected_icon(self) -> Optional[str]:
        return self._get_attr("selectedIcon")

    @selected_icon.setter
    def selected_icon(self, value: Optional[str]):
        self._set_attr("selectedIcon", value)

    # selected_icon_content
    @property
    def selected_icon_content(self) -> Optional[Control]:
        return self.__selected_icon_content

    @selected_icon_content.setter
    def selected_icon_content(self, value: Optional[Control]):
        self.__selected_icon_content = value

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # label_content
    @property
    def label_content(self) -> Optional[Control]:
        return self.__label_content

    @label_content.setter
    def label_content(self, value: Optional[Control]):
        self.__label_content = value

    # indicator_color
    @property
    def indicator_color(self) -> Optional[str]:
        return self._get_attr("indicatorColor")

    @indicator_color.setter
    def indicator_color(self, value: Optional[str]):
        self._set_attr("indicatorColor", value)

    # indicator_shape
    @property
    def indicator_shape(self) -> Optional[OutlinedBorder]:
        return self.__indicator_shape

    @indicator_shape.setter
    def indicator_shape(self, value: Optional[OutlinedBorder]):
        self.__indicator_shape = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value


class NavigationRail(ConstrainedControl):
    """
    A material widget that is meant to be displayed at the left or right of an app to navigate between a small number of views, typically between three and five.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):

        rail = ft.NavigationRail(
            selected_index=1,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=100,
            min_extended_width=400,
            leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.FAVORITE_BORDER, selected_icon=ft.icons.FAVORITE, label="First"
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.BOOKMARK_BORDER),
                    selected_icon_content=ft.Icon(ft.icons.BOOKMARK),
                    label="Second",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=lambda e: print("Selected destination:", e.control.selected_index),
        )

        page.add(
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Column([ ft.Text("Body!")], alignment=ft.MainAxisAlignment.START, expand=True),
                ],
                expand=True,
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/navigationrail
    """

    def __init__(
        self,
        destinations: Optional[List[NavigationRailDestination]] = None,
        elevation: OptionalNumber = None,
        selected_index: Optional[int] = None,
        extended: Optional[bool] = None,
        label_type: Optional[NavigationRailLabelType] = None,
        bgcolor: Optional[str] = None,
        indicator_color: Optional[str] = None,
        indicator_shape: Optional[OutlinedBorder] = None,
        leading: Optional[Control] = None,
        trailing: Optional[Control] = None,
        min_width: OptionalNumber = None,
        min_extended_width: OptionalNumber = None,
        group_alignment: OptionalNumber = None,
        selected_label_text_style: Optional[TextStyle] = None,
        unselected_label_text_style: Optional[TextStyle] = None,
        on_change: OptionalControlEventCallable = None,
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
        on_animation_end: Callable[..., None] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = False,
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
            rtl=rtl,
        )

        self.destinations = destinations
        self.selected_index = selected_index
        self.elevation = elevation
        self.extended = extended
        self.label_type = label_type
        self.bgcolor = bgcolor
        self.indicator_color = indicator_color
        self.indicator_shape = indicator_shape
        self.__leading = None
        self.leading = leading
        self.__trailing = trailing
        self.trailing = trailing
        self.min_width = min_width
        self.min_extended_width = min_extended_width
        self.group_alignment = group_alignment
        self.on_change = on_change
        self.selected_label_text_style = selected_label_text_style
        self.unselected_label_text_style = unselected_label_text_style

    def _get_control_name(self):
        return "navigationrail"

    def before_update(self):
        super().before_update()
        if isinstance(self.__indicator_shape, OutlinedBorder):
            self._set_attr_json("indicatorShape", self.__indicator_shape)
        if isinstance(self.__selected_label_text_style, TextStyle):
            self._set_attr_json(
                "selectedLabelTextStyle", self.__selected_label_text_style
            )
        if isinstance(self.__unselected_label_text_style, TextStyle):
            self._set_attr_json(
                "unselectedLabelTextStyle", self.__unselected_label_text_style
            )

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        return children + self.__destinations

    # destinations
    @property
    def destinations(self) -> Optional[List[NavigationRailDestination]]:
        return self.__destinations

    @destinations.setter
    def destinations(self, value: Optional[List[NavigationRailDestination]]):
        self.__destinations = value if value else []

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

    # label_type
    @property
    def label_type(self) -> Optional[NavigationRailLabelType]:
        return self.__label_type

    @label_type.setter
    def label_type(self, value: Optional[NavigationRailLabelType]):
        self.__label_type = value
        self._set_enum_attr("labelType", value, NavigationRailLabelType)

    # indicator_shape
    @property
    def indicator_shape(self) -> Optional[OutlinedBorder]:
        return self.__indicator_shape

    @indicator_shape.setter
    def indicator_shape(self, value: Optional[OutlinedBorder]):
        self.__indicator_shape = value

    # indicator_color
    @property
    def indicator_color(self) -> Optional[str]:
        return self._get_attr("indicatorColor")

    @indicator_color.setter
    def indicator_color(self, value: Optional[str]):
        self._set_attr("indicatorColor", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        assert value is None or value > 0, "elevation must be greater than 0"
        self._set_attr("elevation", value)

    # extended
    @property
    def extended(self) -> bool:
        return self._get_attr("extended", data_type="bool", def_value=False)

    @extended.setter
    def extended(self, value: Optional[bool]):
        self._set_attr("extended", value)

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # selected_label_text_style
    @property
    def selected_label_text_style(self) -> Optional[TextStyle]:
        return self.__selected_label_text_style

    @selected_label_text_style.setter
    def selected_label_text_style(self, value: Optional[TextStyle]):
        self.__selected_label_text_style = value

    # unselected_label_text_style
    @property
    def unselected_label_text_style(self) -> Optional[TextStyle]:
        return self.__unselected_label_text_style

    @unselected_label_text_style.setter
    def unselected_label_text_style(self, value: Optional[TextStyle]):
        self.__unselected_label_text_style = value

    # min_width
    @property
    def min_width(self) -> OptionalNumber:
        return self._get_attr("minWidth", data_type="float")

    @min_width.setter
    def min_width(self, value: OptionalNumber):
        self._set_attr("minWidth", value)

    # min_extended_width
    @property
    def min_extended_width(self) -> OptionalNumber:
        return self._get_attr("minExtendedWidth", data_type="float")

    @min_extended_width.setter
    def min_extended_width(self, value: OptionalNumber):
        self._set_attr("minExtendedWidth", value)

    # group_alignment
    @property
    def group_alignment(self) -> OptionalNumber:
        return self._get_attr("groupAlignment", data_type="float")

    @group_alignment.setter
    def group_alignment(self, value: OptionalNumber):
        self._set_attr("groupAlignment", value)
