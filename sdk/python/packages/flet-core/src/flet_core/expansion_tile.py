from enum import Enum
from typing import Any, Optional, Union, Sequence

from flet_core.adaptive_control import AdaptiveControl
from flet_core.alignment import Alignment
from flet_core.buttons import OutlinedBorder
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    ClipBehavior,
    CrossAxisAlignment,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    ThemeVisualDensity,
    VisualDensity,
    OptionalControlEventCallable,
)


class TileAffinity(Enum):
    LEADING = "leading"
    TRAILING = "trailing"
    PLATFORM = "platform"


class ExpansionTile(ConstrainedControl, AdaptiveControl):
    """
    A single-line ListTile with an expansion arrow icon that expands or collapses the tile to reveal or hide its controls.

    -----

    Online docs: https://flet.dev/docs/controls/expansiontile
    """

    def __init__(
        self,
        title: Control,
        controls: Optional[Sequence[Control]] = None,
        subtitle: Optional[Control] = None,
        leading: Optional[Control] = None,
        trailing: Optional[Control] = None,
        controls_padding: PaddingValue = None,
        tile_padding: PaddingValue = None,
        affinity: Optional[TileAffinity] = None,
        expanded_alignment: Optional[Alignment] = None,
        expanded_cross_axis_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER,
        clip_behavior: Optional[ClipBehavior] = None,
        initially_expanded: Optional[bool] = None,
        maintain_state: Optional[bool] = None,
        text_color: Optional[str] = None,
        icon_color: Optional[str] = None,
        shape: Optional[OutlinedBorder] = None,
        bgcolor: Optional[str] = None,
        collapsed_bgcolor: Optional[str] = None,
        collapsed_icon_color: Optional[str] = None,
        collapsed_text_color: Optional[str] = None,
        collapsed_shape: Optional[OutlinedBorder] = None,
        dense: Optional[bool] = None,
        enable_feedback: Optional[bool] = None,
        show_trailing_icon: Optional[bool] = None,
        min_tile_height: OptionalNumber = None,
        visual_density: Union[None, ThemeVisualDensity, VisualDensity] = None,
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
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # AdaptiveControl
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.controls = controls
        self.controls_padding = controls_padding
        self.expanded_alignment = expanded_alignment
        self.expanded_cross_axis_alignment = expanded_cross_axis_alignment
        self.tile_padding = tile_padding
        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.trailing = trailing
        self.affinity = affinity
        self.clip_behavior = clip_behavior
        self.maintain_state = maintain_state
        self.initially_expanded = initially_expanded
        self.shape = shape
        self.text_color = text_color
        self.icon_color = icon_color
        self.bgcolor = bgcolor
        self.collapsed_bgcolor = collapsed_bgcolor
        self.collapsed_icon_color = collapsed_icon_color
        self.collapsed_text_color = collapsed_text_color
        self.collapsed_shape = collapsed_shape
        self.on_change = on_change
        self.dense = dense
        self.enable_feedback = enable_feedback
        self.visual_density = visual_density
        self.show_trailing_icon = show_trailing_icon
        self.min_tile_height = min_tile_height

    def _get_control_name(self):
        return "expansiontile"

    def before_update(self):
        super().before_update()
        assert self.__title.visible, "title must be visible"
        self._set_attr_json("expandedAlignment", self.__expanded_alignment)
        self._set_attr_json("controlsPadding", self.__controls_padding)
        self._set_attr_json("tilePadding", self.__tile_padding)
        self._set_attr_json("shape", self.__shape)
        self._set_attr_json("collapsedShape", self.__collapsed_shape)

    def _get_children(self):
        self.__title._set_attr_internal("n", "title")
        children = [self.__title]
        for c in self.__controls:
            c._set_attr_internal("n", "controls")
            children.append(c)
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__subtitle:
            self.__subtitle._set_attr_internal("n", "subtitle")
            children.append(self.__subtitle)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        return children

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[Sequence[Control]]):
        self.__controls = list(value) if value is not None else []

    # controls_padding
    @property
    def controls_padding(self) -> PaddingValue:
        return self.__controls_padding

    @controls_padding.setter
    def controls_padding(self, value: PaddingValue):
        self.__controls_padding = value

    # tile_padding
    @property
    def tile_padding(self) -> PaddingValue:
        return self.__tile_padding

    @tile_padding.setter
    def tile_padding(self, value: PaddingValue):
        self.__tile_padding = value

    # expanded_alignment
    @property
    def expanded_alignment(self) -> Optional[Alignment]:
        return self.__expanded_alignment

    @expanded_alignment.setter
    def expanded_alignment(self, value: Optional[Alignment]):
        self.__expanded_alignment = value

    # expanded_cross_axis_alignment
    @property
    def expanded_cross_axis_alignment(self) -> Optional[CrossAxisAlignment]:
        return self.__expanded_cross_axis_alignment

    @expanded_cross_axis_alignment.setter
    def expanded_cross_axis_alignment(self, value: Optional[CrossAxisAlignment]):
        self.__expanded_cross_axis_alignment = value
        self._set_enum_attr("crossAxisAlignment", value, CrossAxisAlignment)

    # affinity
    @property
    def affinity(self) -> Optional[TileAffinity]:
        return self.__affinity

    @affinity.setter
    def affinity(self, value: Optional[TileAffinity]):
        self.__affinity = value
        self._set_enum_attr("affinity", value, TileAffinity)

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

    # dense
    @property
    def dense(self) -> bool:
        return self._get_attr("dense", data_type="bool")

    @dense.setter
    def dense(self, value: Optional[bool]):
        self._set_attr("dense", value)

    # enable_feedback
    @property
    def enable_feedback(self) -> bool:
        return self._get_attr("enableFeedback", data_type="bool", def_value=True)

    @enable_feedback.setter
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # visual_density
    @property
    def visual_density(self) -> Union[None, ThemeVisualDensity, VisualDensity]:
        return self.__visual_density

    @visual_density.setter
    def visual_density(self, value: Union[None, ThemeVisualDensity, VisualDensity]):
        self.__visual_density = value
        self._set_enum_attr("visualDensity", value, ThemeVisualDensity, VisualDensity)

    # maintain_state
    @property
    def maintain_state(self) -> bool:
        return self._get_attr("maintainState", data_type="bool", def_value=False)

    @maintain_state.setter
    def maintain_state(self, value: Optional[bool]):
        self._set_attr("maintainState", value)

    # initially_expanded
    @property
    def initially_expanded(self) -> bool:
        return self._get_attr("initiallyExpanded", data_type="bool", def_value=False)

    @initially_expanded.setter
    def initially_expanded(self, value: Optional[bool]):
        self._set_attr("initiallyExpanded", value)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # text_color
    @property
    def text_color(self) -> Optional[str]:
        return self._get_attr("textColor")

    @text_color.setter
    def text_color(self, value: Optional[str]):
        self._set_attr("textColor", value)

    # icon_color
    @property
    def icon_color(self) -> Optional[str]:
        return self._get_attr("iconColor")

    @icon_color.setter
    def icon_color(self, value: Optional[str]):
        self._set_attr("iconColor", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgColor", value)

    # collapsed_bgcolor
    @property
    def collapsed_bgcolor(self) -> Optional[str]:
        return self._get_attr("collapsedBgColor")

    @collapsed_bgcolor.setter
    def collapsed_bgcolor(self, value: Optional[str]):
        self._set_attr("collapsedBgColor", value)

    # collapsed_icon_color
    @property
    def collapsed_icon_color(self) -> Optional[str]:
        return self._get_attr("collapsedIconColor")

    @collapsed_icon_color.setter
    def collapsed_icon_color(self, value: Optional[str]):
        self._set_attr("collapsedIconColor", value)

    # collapsed_text_color
    @property
    def collapsed_text_color(self) -> Optional[str]:
        return self._get_attr("collapsedTextColor")

    @collapsed_text_color.setter
    def collapsed_text_color(self, value: Optional[str]):
        self._set_attr("collapsedTextColor", value)

    # collapsed_shape
    @property
    def collapsed_shape(self) -> Optional[OutlinedBorder]:
        return self.__collapsed_shape

    @collapsed_shape.setter
    def collapsed_shape(self, value: Optional[OutlinedBorder]):
        self.__collapsed_shape = value

    # show_trailing_icon
    @property
    def show_trailing_icon(self) -> bool:
        return self._get_attr("showTrailingIcon", data_type="bool", def_value=True)

    @show_trailing_icon.setter
    def show_trailing_icon(self, value: Optional[bool]):
        self._set_attr("showTrailingIcon", value)

    # min_tile_height
    @property
    def min_tile_height(self) -> OptionalNumber:
        return self._get_attr("minTileHeight")

    @min_tile_height.setter
    def min_tile_height(self, value: OptionalNumber):
        self._set_attr("minTileHeight", value)

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("change", handler)
        self._set_attr("onChange", True if handler is not None else None)
