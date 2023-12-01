from typing import Any, List, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    PaddingValue,
)


class ExpansionPanel(ConstrainedControl):
    """
    A material expansion panel. It can either be  expanded or collapsed. Its body is only visible when it is expanded.

    -----

    Online docs: https://flet.dev/docs/controls/expansionpanel
    """

    def __init__(
        self,
        header: Optional[Control] = None,
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
        # Specific
        #
        bgcolor: Optional[str] = None,
        expanded: Optional[bool] = None,
        can_tap_header: Optional[bool] = None,
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

        self.header = header
        self.content = content
        self.bgcolor = bgcolor
        self.expanded = expanded
        self.can_tap_header = can_tap_header

    def _get_control_name(self):
        return "expansionpanel"

    def _before_build_command(self):
        super()._before_build_command()

    def _get_children(self):
        children = []
        if self.__header:
            self.__header._set_attr_internal("n", "header")
            children.append(self.__header)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # expanded
    @property
    def expanded(self) -> Optional[bool]:
        return self._get_attr("expanded", data_type="bool", def_value=False)

    @expanded.setter
    def expanded(self, value: Optional[bool]):
        self._set_attr("expanded", value)

    # can_tap_header
    @property
    def can_tap_header(self) -> Optional[bool]:
        return self._get_attr("canTapHeader", data_type="bool", def_value=False)

    @can_tap_header.setter
    def can_tap_header(self, value: Optional[bool]):
        self._set_attr("canTapHeader", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # header
    @property
    def header(self) -> Optional[Control]:
        return self.__header

    @header.setter
    def header(self, value: Optional[Control]):
        self.__header = value


class ExpansionPanelList(ConstrainedControl):
    """
    A material expansion panel list that lays out its children and animates expansions.

    -----

    Online docs: https://flet.dev/docs/controls/expansionpanellist
    """

    def __init__(
        self,
        controls: Optional[List[ExpansionPanel]] = None,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
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
        # Specific
        #
        divider_color: Optional[str] = None,
        elevation: OptionalNumber = None,
        expanded_header_padding: PaddingValue = None,
        expand_icon_color: Optional[str] = None,
        spacing: OptionalNumber = None,
        on_change=None,
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

        self.controls = controls
        self.divider_color = divider_color
        self.expanded_icon_color = expand_icon_color
        self.expanded_header_padding = expanded_header_padding
        self.elevation = elevation
        self.spacing = spacing
        self.on_change = on_change

    def _get_control_name(self):
        return "expansionpanellist"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("expandedHeaderPadding", self.__expanded_header_padding)

    def _get_children(self):
        children = []
        for c in self.__controls:
            c._set_attr_internal("n", "expansionpanel")
            children.append(c)
        return children

    # divider_color
    @property
    def divider_color(self):
        return self._get_attr("dividerColor")

    @divider_color.setter
    def divider_color(self, value):
        self._set_attr("dividerColor", value)

    # expanded_icon_color
    @property
    def expanded_icon_color(self):
        return self._get_attr("expandedIconColor")

    @expanded_icon_color.setter
    def expanded_icon_color(self, value):
        self._set_attr("expandedIconColor", value)

    # expanded_header_padding
    @property
    def expanded_header_padding(self) -> PaddingValue:
        return self.__expanded_header_padding

    @expanded_header_padding.setter
    def expanded_header_padding(self, value: PaddingValue):
        self.__expanded_header_padding = value

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[ExpansionPanel]]):
        self.__controls = value if value is not None else []

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)
        self._set_attr("onChange", True if handler is not None else None)
