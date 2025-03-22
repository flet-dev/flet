from enum import Enum
from typing import Any, List, Optional

from flet.core.app_bar import AppBar
from flet.core.buttons import OutlinedBorder
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.sliver import Sliver
from flet.core.text_style import TextStyle
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    PaddingValue,
)


class SliverAppBarType(Enum):
    MEDIUM = "medium"
    LARGE = "large"
    DEFAULT = "default"


class SliverAppBar(AppBar, Sliver):
    """
    A Material Design app bar that integrates with a SliverScrollView.

    -----

    Online docs: https://flet.dev/docs/controls/sliverappbar
    """

    def __init__(
        self,
        leading: Optional[Control] = None,
        title: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        flexible_space: Optional[Control] = None,
        actions_padding: Optional[PaddingValue] = None,
        collapsed_height: OptionalNumber = None,
        pinned: Optional[bool] = None,
        snap: Optional[bool] = None,
        floating: Optional[bool] = None,
        stretch: Optional[bool] = None,
        expanded_height: OptionalNumber = None,
        force_elevated: Optional[bool] = None,
        stretch_trigger_offset: OptionalNumber = None,
        type: Optional[SliverAppBarType] = None,
        primary: Optional[bool] = None,
        on_stretch: OptionalControlEventCallable = None,
        #
        # AppBar
        #
        leading_width: OptionalNumber = None,
        automatically_imply_leading: Optional[bool] = None,
        center_title: Optional[bool] = None,
        toolbar_height: OptionalNumber = None,
        color: Optional[ColorValue] = None,
        bgcolor: Optional[ColorValue] = None,
        elevation: OptionalNumber = None,
        elevation_on_scroll: OptionalNumber = None,
        shadow_color: Optional[ColorValue] = None,
        surface_tint_color: Optional[ColorValue] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        force_material_transparency: Optional[bool] = None,
        title_spacing: OptionalNumber = None,
        exclude_header_semantics: Optional[bool] = None,
        title_text_style: Optional[TextStyle] = None,
        toolbar_text_style: Optional[TextStyle] = None,
        shape: Optional[OutlinedBorder] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        #
        # AdaptiveControl
        #
        adaptive: Optional[bool] = None,
    ):
        AppBar.__init__(
            self,
            leading=leading,
            leading_width=leading_width,
            automatically_imply_leading=automatically_imply_leading,
            title=title,
            center_title=center_title,
            toolbar_height=toolbar_height,
            color=color,
            bgcolor=bgcolor,
            elevation=elevation,
            elevation_on_scroll=elevation_on_scroll,
            shadow_color=shadow_color,
            surface_tint_color=surface_tint_color,
            clip_behavior=clip_behavior,
            force_material_transparency=force_material_transparency,
            title_spacing=title_spacing,
            exclude_header_semantics=exclude_header_semantics,
            actions=actions,
            title_text_style=title_text_style,
            toolbar_text_style=toolbar_text_style,
            shape=shape,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
            adaptive=adaptive,
        )

        self.flexible_space = flexible_space
        self.actions_padding = actions_padding
        self.collapsed_height = collapsed_height
        self.pinned = pinned
        self.snap = snap
        self.floating = floating
        self.stretch = stretch
        self.expanded_height = expanded_height
        self.force_elevated = force_elevated
        self.stretch_trigger_offset = stretch_trigger_offset
        self.type = type
        self.primary = primary
        self.on_stretch = on_stretch

    def _get_control_name(self):
        return "sliverappbar"

    def before_update(self):
        super().before_update()
        assert (
            self.floating or not self.snap
        ), "snap can only be True when floating is True"
        assert (
            self.collapsed_height is None
            or self.collapsed_height >= self.toolbar_height
        ), f"collapsed_height ({self.collapsed_height}) must be greater than or equal to toolbar_height ({self.toolbar_height})"
        if isinstance(self.__actions_padding, PaddingValue):
            self._set_attr_json("actionsPadding", self.__actions_padding)

    def _get_children(self):
        children = super()._get_children()
        if self.__flexible_space:
            self.__flexible_space._set_attr_internal("n", "flexibleSpace")
            children.append(self.__flexible_space)
        return children

    # flexible_space
    @property
    def flexible_space(self) -> Optional[Control]:
        return self.__flexible_space

    @flexible_space.setter
    def flexible_space(self, value: Optional[Control]):
        self.__flexible_space = value

    # actions_padding
    @property
    def actions_padding(self) -> Optional[PaddingValue]:
        return self.__actions_padding

    @actions_padding.setter
    def actions_padding(self, value: Optional[PaddingValue]):
        self.__actions_padding = value

    # collapsed_height
    @property
    def collapsed_height(self) -> OptionalNumber:
        return self._get_attr("collapsedHeight")

    @collapsed_height.setter
    def collapsed_height(self, value: OptionalNumber):
        self._set_attr("collapsedHeight", value)

    # pinned
    @property
    def pinned(self) -> bool:
        return self._get_attr("pinned", data_type="bool", def_value=False)

    @pinned.setter
    def pinned(self, value: bool):
        self._set_attr("pinned", value)

    # primary
    @property
    def primary(self) -> bool:
        return self._get_attr("primary", data_type="bool", def_value=False)

    @primary.setter
    def primary(self, value: bool):
        self._set_attr("primary", value)

    # snap
    @property
    def snap(self) -> bool:
        return self._get_attr("snap", data_type="bool", def_value=False)

    @snap.setter
    def snap(self, value: bool):
        self._set_attr("snap", value)

    # floating
    @property
    def floating(self) -> bool:
        return self._get_attr("floating", data_type="bool", def_value=False)

    @floating.setter
    def floating(self, value: bool):
        self._set_attr("floating", value)

    # stretch
    @property
    def stretch(self) -> bool:
        return self._get_attr("stretch", data_type="bool", def_value=False)

    @stretch.setter
    def stretch(self, value: bool):
        self._set_attr("stretch", value)

    # expanded_height
    @property
    def expanded_height(self) -> OptionalNumber:
        return self._get_attr("expandedHeight")

    @expanded_height.setter
    def expanded_height(self, value: OptionalNumber):
        self._set_attr("expandedHeight", value)

    # force_elevated
    @property
    def force_elevated(self) -> bool:
        return self._get_attr("forceElevated", data_type="bool", def_value=False)

    @force_elevated.setter
    def force_elevated(self, value: bool):
        self._set_attr("forceElevated", value)

    # stretch_trigger_offset
    @property
    def stretch_trigger_offset(self) -> OptionalNumber:
        return self._get_attr(
            "stretchTriggerOffset", data_type="float", def_value=100.0
        )

    @stretch_trigger_offset.setter
    def stretch_trigger_offset(self, value: OptionalNumber):
        assert (
            value is None or value > 0
        ), "stretch_trigger_offset must be greater than 0"
        self._set_attr("stretchTriggerOffset", value)

    # type
    @property
    def type(self) -> Optional[SliverAppBarType]:
        return self.__type

    @type.setter
    def type(self, value: Optional[SliverAppBarType]):
        self.__type = value
        self._set_enum_attr("type", value, SliverAppBarType)

    # on_stretch
    @property
    def on_stretch(self) -> OptionalControlEventCallable:
        return self._get_event_handler("stretch")

    @on_stretch.setter
    def on_stretch(self, handler: OptionalControlEventCallable):
        self._add_event_handler("stretch", handler)
