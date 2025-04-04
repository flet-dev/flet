from typing import Any, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.animation import AnimationValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.types import (
    ColorEnums,
    ColorValue,
    OffsetValue,
    OptionalControlEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class ExpansionPanel(ConstrainedControl, AdaptiveControl):
    """
    A material expansion panel. It can either be expanded or collapsed. Its body is only visible when it is expanded.

    -----

    Online docs: https://flet.dev/docs/controls/expansionpanel
    """

    def __init__(
        self,
        header: Optional[Control] = None,
        content: Optional[Control] = None,
        bgcolor: Optional[ColorValue] = None,
        expanded: Optional[bool] = None,
        can_tap_header: Optional[bool] = None,
        splash_color: Optional[ColorValue] = None,
        highlight_color: Optional[ColorValue] = None,
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Adaptive
        #
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

        self.header = header
        self.content = content
        self.bgcolor = bgcolor
        self.expanded = expanded
        self.can_tap_header = can_tap_header
        self.splash_color = splash_color
        self.highlight_color = highlight_color

    def _get_control_name(self):
        return "expansionpanel"

    def before_update(self):
        super().before_update()

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
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgColor", value, ColorEnums)

    # splash_color
    @property
    def splash_color(self) -> Optional[ColorValue]:

        return self.__splash_color

    @splash_color.setter
    def splash_color(self, value: Optional[ColorValue]):
        self.__splash_color = value
        self._set_enum_attr("splashColor", value, ColorEnums)

    # highlight_color
    @property
    def highlight_color(self) -> Optional[ColorValue]:
        return self.__highlight_color

    @highlight_color.setter
    def highlight_color(self, value: Optional[ColorValue]):
        self.__highlight_color = value
        self._set_enum_attr("highlightColor", value, ColorEnums)

    # expanded
    @property
    def expanded(self) -> bool:
        return self._get_attr("expanded", data_type="bool", def_value=False)

    @expanded.setter
    def expanded(self, value: Optional[bool]):
        self._set_attr("expanded", value)

    # can_tap_header
    @property
    def can_tap_header(self) -> bool:
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
        controls: Optional[Sequence[ExpansionPanel]] = None,
        divider_color: Optional[ColorValue] = None,
        elevation: OptionalNumber = None,
        expanded_header_padding: Optional[PaddingValue] = None,
        expand_icon_color: Optional[ColorValue] = None,
        spacing: OptionalNumber = None,
        on_change: OptionalControlEventCallable = None,
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
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
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

        self.controls = controls
        self.divider_color = divider_color
        self.expanded_icon_color = expand_icon_color
        self.expanded_header_padding = expanded_header_padding
        self.elevation = elevation
        self.spacing = spacing
        self.on_change = on_change

    def _get_control_name(self):
        return "expansionpanellist"

    def before_update(self):
        super().before_update()
        self._set_attr_json("expandedHeaderPadding", self.__expanded_header_padding)

    def _get_children(self):
        children = []
        for c in self.__controls:
            c._set_attr_internal("n", "expansionpanel")
            children.append(c)
        return children

    # divider_color
    @property
    def divider_color(self) -> Optional[ColorValue]:
        return self.__divider_color

    @divider_color.setter
    def divider_color(self, value: Optional[ColorValue]):
        self.__divider_color = value
        self._set_enum_attr("dividerColor", value, ColorEnums)

    # expanded_icon_color
    @property
    def expanded_icon_color(self) -> Optional[ColorValue]:
        return self.__expanded_icon_color

    @expanded_icon_color.setter
    def expanded_icon_color(self, value: Optional[ColorValue]):
        self.__expanded_icon_color = value
        self._set_enum_attr("expandedIconColor", value, ColorEnums)

    # expanded_header_padding
    @property
    def expanded_header_padding(self) -> Optional[PaddingValue]:
        return self.__expanded_header_padding

    @expanded_header_padding.setter
    def expanded_header_padding(self, value: Optional[PaddingValue]):
        self.__expanded_header_padding = value

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation", data_type="float")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        assert value is None or value >= 0, "elevation cannot be negative"
        self._set_attr("elevation", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing", data_type="float")

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[Sequence[ExpansionPanel]]):
        self.__controls = list(value) if value is not None else []

    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
        self._set_attr("onChange", True if handler is not None else None)
