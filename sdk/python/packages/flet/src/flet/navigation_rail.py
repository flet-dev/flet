from enum import Enum
from typing import Any, Optional, Union

from beartype import beartype
from beartype.typing import List

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

NavigationRailLabelTypeString = Literal[None, "none", "all", "selected"]


class NavigationRailLabelType(Enum):
    NONE = "none"
    ALL = "all"
    SELECTED = "selected"


class NavigationRailDestination(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        icon: Optional[str] = None,
        icon_content: Optional[Control] = None,
        selected_icon: Optional[str] = None,
        selected_icon_content: Optional[Control] = None,
        label: Optional[str] = None,
        label_content: Optional[Control] = None,
        padding: PaddingValue = None,
    ):
        Control.__init__(self, ref=ref)
        self.label = label
        self.icon = icon
        self.__icon_content: Optional[Control] = None
        self.icon_content = icon_content
        self.selected_icon = selected_icon
        self.__selected_icon_content: Optional[Control] = None
        self.selected_icon_content = selected_icon_content
        self.__label_content: Optional[Control] = None
        self.label_content = label_content
        self.padding = padding

    def _get_control_name(self):
        return "navigationraildestination"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("padding", self.__padding)

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
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_content
    @property
    def icon_content(self) -> Optional[Control]:
        return self.__icon_content

    @icon_content.setter
    @beartype
    def icon_content(self, value: Optional[Control]):
        self.__icon_content = value

    # selected_icon
    @property
    def selected_icon(self):
        return self._get_attr("selectedIcon")

    @selected_icon.setter
    def selected_icon(self, value):
        self._set_attr("selectedIcon", value)

    # selected_icon_content
    @property
    def selected_icon_content(self) -> Optional[Control]:
        return self.__selected_icon_content

    @selected_icon_content.setter
    @beartype
    def selected_icon_content(self, value: Optional[Control]):
        self.__selected_icon_content = value

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # label_content
    @property
    def label_content(self) -> Optional[Control]:
        return self.__label_content

    @label_content.setter
    @beartype
    def label_content(self, value: Optional[Control]):
        self.__label_content = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    @beartype
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # NavigationRail-specific
        destinations: Optional[List[NavigationRailDestination]] = None,
        selected_index: Optional[int] = None,
        extended: Optional[bool] = None,
        label_type: Optional[NavigationRailLabelType] = None,
        bgcolor: Optional[str] = None,
        leading: Optional[Control] = None,
        trailing: Optional[Control] = None,
        min_width: OptionalNumber = None,
        min_extended_width: OptionalNumber = None,
        group_alignment: OptionalNumber = None,
        on_change=None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.destinations = destinations
        self.selected_index = selected_index
        self.extended = extended
        self.label_type = label_type
        self.bgcolor = bgcolor
        self.__leading = None
        self.leading = leading
        self.__trailing = trailing
        self.trailing = trailing
        self.min_width = min_width
        self.min_extended_width = min_extended_width
        self.group_alignment = group_alignment
        self.on_change = on_change

    def _get_control_name(self):
        return "navigationrail"

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        children.extend(self.__destinations)
        return children

    # destinations
    @property
    def destinations(self) -> Optional[List[NavigationRailDestination]]:
        return self.__destinations

    @destinations.setter
    @beartype
    def destinations(self, value: Optional[List[NavigationRailDestination]]):
        self.__destinations = value if value is not None else []

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # selected_index
    @property
    def selected_index(self) -> Optional[int]:
        return self._get_attr("selectedIndex", data_type="int")

    @selected_index.setter
    @beartype
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # label_type
    @property
    def label_type(self) -> Optional[NavigationRailLabelType]:
        return self.__label_type

    @label_type.setter
    def label_type(self, value: Optional[NavigationRailLabelType]):
        self.__label_type = value
        if isinstance(value, NavigationRailLabelType):
            self._set_attr("labelType", value.value)
        else:
            self.__set_label_type(value)

    @beartype
    def __set_label_type(self, value: NavigationRailLabelTypeString):
        self._set_attr("labelType", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # extended
    @property
    def extended(self) -> Optional[bool]:
        return self._get_attr("extended", data_type="bool", def_value=False)

    @extended.setter
    @beartype
    def extended(self, value: Optional[bool]):
        self._set_attr("extended", value)

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    @beartype
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    @beartype
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # min_width
    @property
    def min_width(self) -> OptionalNumber:
        return self._get_attr("minWidth")

    @min_width.setter
    @beartype
    def min_width(self, value: OptionalNumber):
        self._set_attr("minWidth", value)

    # min_extended_width
    @property
    def min_extended_width(self) -> OptionalNumber:
        return self._get_attr("minExtendedWidth")

    @min_extended_width.setter
    @beartype
    def min_extended_width(self, value: OptionalNumber):
        self._set_attr("minExtendedWidth", value)

    # group_alignment
    @property
    def group_alignment(self) -> OptionalNumber:
        return self._get_attr("groupAlignment")

    @group_alignment.setter
    @beartype
    def group_alignment(self, value: OptionalNumber):
        self._set_attr("groupAlignment", value)
