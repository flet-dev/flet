import warnings
from enum import Enum
from typing import Any, Callable, List, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.border import Border
from flet.core.buttons import OutlinedBorder
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.types import (
    ColorEnums,
    ColorValue,
    ControlStateValue,
    IconEnums,
    IconValueOrControl,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalNumber,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class NavigationBarLabelBehavior(Enum):
    """Defines how the destinations' labels will be laid out and when they'll be displayed."""

    ALWAYS_SHOW = "alwaysShow"
    ALWAYS_HIDE = "alwaysHide"
    ONLY_SHOW_SELECTED = "onlyShowSelected"


class NavigationBarDestination(AdaptiveControl, Control):
    """Defines the appearance of the button items that are arrayed within the navigation bar.

    The value must be a list of two or more NavigationBarDestination instances."""

    def __init__(
        self,
        label: Optional[str] = None,
        icon: Optional[IconValueOrControl] = None,
        icon_content: Optional[Control] = None,
        selected_icon: Optional[IconValueOrControl] = None,
        selected_icon_content: Optional[Control] = None,
        bgcolor: Optional[ColorValue] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        tooltip: Optional[str] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # AdaptiveControl
        #
        adaptive: Optional[bool] = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            tooltip=tooltip,
            disabled=disabled,
            visible=visible,
            data=data,
        )
        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.label = label
        self.icon = icon
        self.icon_content = icon_content
        self.selected_icon = selected_icon
        self.selected_icon_content = selected_icon_content
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "navigationbardestination"

    def _get_children(self):
        children = []
        if isinstance(self.__icon, Control):
            self.__icon._set_attr_internal("n", "icon")
            children.append(self.__icon)
        if self.__icon_content:
            self.__icon_content._set_attr_internal("n", "icon_content")
            children.append(self.__icon_content)
        if isinstance(self.__selected_icon, Control):
            self.__selected_icon._set_attr_internal("n", "selected_icon")
            children.append(self.__selected_icon)
        if self.__selected_icon_content:
            self.__selected_icon_content._set_attr_internal(
                "n", "selected_icon_content"
            )
            children.append(self.__selected_icon_content)
        return children

    # icon
    @property
    def icon(self) -> Optional[IconValueOrControl]:
        return self.__icon

    @icon.setter
    def icon(self, value: Optional[IconValueOrControl]):
        self.__icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("icon", value, IconEnums)

    # icon_content
    @property
    def icon_content(self) -> Optional[Control]:
        warnings.warn(
            f"icon_content is deprecated since version 0.25.0 "
            f"and will be removed in version 0.28.0. Use icon instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.__icon_content

    @icon_content.setter
    def icon_content(self, value: Optional[Control]):
        self.__icon_content = value
        if value is not None:
            warnings.warn(
                f"icon_content is deprecated since version 0.25.0 "
                f"and will be removed in version 0.28.0. Use icon instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # selected_icon
    @property
    def selected_icon(self) -> Optional[IconValueOrControl]:
        return self.__selected_icon

    @selected_icon.setter
    def selected_icon(self, value: Optional[IconValueOrControl]):
        self.__selected_icon = value
        if not isinstance(value, Control):
            self._set_enum_attr("selectedIcon", value, IconEnums)

    # selected_icon_content
    @property
    def selected_icon_content(self) -> Optional[Control]:
        warnings.warn(
            f"selected_icon_content is deprecated since version 0.25.0 "
            f"and will be removed in version 0.28.0. Use selected_icon instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self.__selected_icon_content

    @selected_icon_content.setter
    def selected_icon_content(self, value: Optional[Control]):
        self.__selected_icon_content = value
        if value is not None:
            warnings.warn(
                f"selected_icon_content is deprecated since version 0.25.0 "
                f"and will be removed in version 0.28.0. Use selected_icon instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # tooltip
    @property
    def tooltip(self) -> Optional[str]:
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value: Optional[str]):
        self._set_attr("tooltip", value)


class NavigationBar(ConstrainedControl, AdaptiveControl):
    """
    Material 3 Navigation Bar component.

    Navigation bars offer a persistent and convenient way to switch between primary destinations in an app.

    Example:

    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "NavigationBar Example"
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.icons.BOOKMARK_BORDER,
                    selected_icon=ft.icons.BOOKMARK,
                    label="Explore"
                ),
            ]
        )
        page.add(ft.Text("Body!"))

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/navigationbar
    """

    def __init__(
        self,
        destinations: Optional[List[NavigationBarDestination]] = None,
        selected_index: Optional[int] = None,
        bgcolor: Optional[ColorValue] = None,
        label_behavior: Optional[NavigationBarLabelBehavior] = None,
        elevation: OptionalNumber = None,
        shadow_color: Optional[ColorValue] = None,
        indicator_color: Optional[ColorValue] = None,
        indicator_shape: Optional[OutlinedBorder] = None,
        surface_tint_color: Optional[ColorValue] = None,
        border: Optional[Border] = None,
        animation_duration: Optional[int] = None,
        overlay_color: ControlStateValue[ColorValue] = None,
        on_change: OptionalControlEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
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
        on_animation_end: Callable[..., None] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
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
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.destinations = destinations
        self.selected_index = selected_index
        self.label_behavior = label_behavior
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.shadow_color = shadow_color
        self.indicator_color = indicator_color
        self.indicator_shape = indicator_shape
        self.surface_tint_color = surface_tint_color
        self.border = border
        self.on_change = on_change
        self.animation_duration = animation_duration
        self.overlay_color = overlay_color

    def _get_control_name(self):
        return "navigationbar"

    def before_update(self):
        super().before_update()
        self._set_attr_json("indicatorShape", self.__indicator_shape)
        self._set_attr_json("border", self.__border)
        self._set_attr_json("overlayColor", self.__overlay_color, wrap_attr_dict=True)

    def _get_children(self):
        return self.__destinations

    # destinations
    @property
    def destinations(self) -> Optional[List[NavigationBarDestination]]:
        return self.__destinations

    @destinations.setter
    def destinations(self, value: Optional[List[NavigationBarDestination]]):
        self.__destinations = value if value else []

    # selected_index
    @property
    def selected_index(self) -> int:
        return self._get_attr("selectedIndex", data_type="int", def_value=0)

    @selected_index.setter
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # label_behavior
    @property
    def label_behavior(self) -> Optional[NavigationBarLabelBehavior]:
        return self.__label_behavior

    @label_behavior.setter
    def label_behavior(self, value: Optional[NavigationBarLabelBehavior]):
        self.__label_behavior = value
        self._set_enum_attr("labelBehavior", value, NavigationBarLabelBehavior)

    # overlay_color
    @property
    def overlay_color(self) -> ControlStateValue[str]:
        return self.__overlay_color

    @overlay_color.setter
    def overlay_color(self, value: ControlStateValue[str]):
        self.__overlay_color = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # shadow_color
    @property
    def shadow_color(self) -> Optional[ColorValue]:
        return self.__shadow_color

    @shadow_color.setter
    def shadow_color(self, value: Optional[ColorValue]):
        self.__shadow_color = value
        self._set_enum_attr("shadowColor", value, ColorEnums)

    # indicator_color
    @property
    def indicator_color(self) -> Optional[ColorValue]:
        return self.__indicator_color

    @indicator_color.setter
    def indicator_color(self, value: Optional[ColorValue]):
        self.__indicator_color = value
        self._set_enum_attr("indicatorColor", value, ColorEnums)

    # indicator_shape
    @property
    def indicator_shape(self) -> Optional[OutlinedBorder]:
        return self.__indicator_shape

    @indicator_shape.setter
    def indicator_shape(self, value: Optional[OutlinedBorder]):
        self.__indicator_shape = value

    # surface_tint_color
    @property
    def surface_tint_color(self) -> Optional[ColorValue]:
        return self.__surface_tint_color

    @surface_tint_color.setter
    def surface_tint_color(self, value: Optional[ColorValue]):
        self.__surface_tint_color = value
        self._set_enum_attr("surfaceTintColor", value, ColorEnums)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # animation_duration
    @property
    def animation_duration(self) -> Optional[int]:
        return self._get_attr("animationDuration", data_type="int")

    @animation_duration.setter
    def animation_duration(self, value: Optional[int]):
        self._set_attr("animationDuration", value)

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
