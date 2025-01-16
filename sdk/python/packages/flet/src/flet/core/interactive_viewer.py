import json
from typing import Any, Callable, Optional, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ClipBehavior,
    DurationValue,
    MarginValue,
    Number,
    Offset,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class InteractiveViewerInteractionStartEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.pointer_count: int = d.get("pc")
        self.global_focal_point: Offset = Offset(d.get("fp_x"), d.get("fp_y"))
        self.local_focal_point: Offset = Offset(d.get("lfp_x"), d.get("lfp_y"))


class InteractiveViewerInteractionUpdateEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.pointer_count: int = d.get("pc")
        self.global_focal_point: Offset = Offset(d.get("fp_x"), d.get("fp_y"))
        self.local_focal_point: Offset = Offset(d.get("lfp_x"), d.get("lfp_y"))
        self.scale: float = d.get("s")
        self.horizontal_scale: float = d.get("hs")
        self.vertical_scale: float = d.get("vs")
        self.rotation: float = d.get("rot")


class InteractiveViewerInteractionEndEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.pointer_count: int = d.get("pc")
        self.scale_velocity: float = d.get("sv")


class InteractiveViewer(ConstrainedControl, AdaptiveControl):
    """
    InteractiveViewer allows users to pan, zoom, and rotate content.

    -----

    Online docs: https://flet.dev/docs/controls/interactiveviewer
    """

    def __init__(
        self,
        content: Control,
        pan_enabled: Optional[bool] = None,
        scale_enabled: Optional[bool] = None,
        trackpad_scroll_causes_scale: Optional[bool] = None,
        constrained: Optional[bool] = None,
        max_scale: OptionalNumber = None,
        min_scale: OptionalNumber = None,
        interaction_end_friction_coefficient: OptionalNumber = None,
        scale_factor: OptionalNumber = None,
        clip_behavior: Optional[ClipBehavior] = None,
        alignment: Optional[Alignment] = None,
        boundary_margin: Optional[MarginValue] = None,
        interaction_update_interval: Optional[int] = None,
        on_interaction_start: Optional[
            Callable[[InteractiveViewerInteractionStartEvent], None]
        ] = None,
        on_interaction_update: Optional[
            Callable[[InteractiveViewerInteractionUpdateEvent], None]
        ] = None,
        on_interaction_end: Optional[
            Callable[[InteractiveViewerInteractionEndEvent], None]
        ] = None,
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
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
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
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__on_interaction_start = EventHandler(
            lambda e: InteractiveViewerInteractionStartEvent(e)
        )
        self._add_event_handler(
            "interaction_start", self.__on_interaction_start.get_handler()
        )
        self.__on_interaction_update = EventHandler(
            lambda e: InteractiveViewerInteractionUpdateEvent(e)
        )
        self._add_event_handler(
            "interaction_update", self.__on_interaction_update.get_handler()
        )
        self.__on_interaction_end = EventHandler(
            lambda e: InteractiveViewerInteractionEndEvent(e)
        )
        self._add_event_handler(
            "interaction_end", self.__on_interaction_end.get_handler()
        )

        self.content = content
        self.pan_enabled = pan_enabled
        self.scale_enabled = scale_enabled
        self.trackpad_scroll_causes_scale = trackpad_scroll_causes_scale
        self.constrained = constrained
        self.max_scale = max_scale
        self.min_scale = min_scale
        self.interaction_end_friction_coefficient = interaction_end_friction_coefficient
        self.scale_factor = scale_factor
        self.clip_behavior = clip_behavior
        self.alignment = alignment
        self.boundary_margin = boundary_margin
        self.on_interaction_start = on_interaction_start
        self.on_interaction_end = on_interaction_end
        self.on_interaction_update = on_interaction_update
        self.interaction_update_interval = interaction_update_interval

    def _get_control_name(self):
        return "interactiveviewer"

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("boundaryMargin", self.__boundary_margin)

    def _get_children(self):
        return [self.__content]

    def reset(self, animation_duration: Optional[DurationValue] = None):
        self.invoke_method(
            "reset", arguments={"duration": self._convert_attr_json(animation_duration)}
        )

    def save_state(self):
        self.invoke_method("save_state")

    def restore_state(self):
        self.invoke_method("restore_state")

    def zoom(self, factor: Number):
        self.invoke_method("zoom", arguments={"factor": str(factor)})

    def pan(self, dx: Number, dy: Number):
        self.invoke_method("pan", arguments={"dx": str(dx), "dy": str(dy)})

    # min_scale
    @property
    def min_scale(self) -> float:
        return self._get_attr("minScale", data_type="float", def_value=0.8)

    @min_scale.setter
    def min_scale(self, value: OptionalNumber):
        self._set_attr("minScale", value)

    # interaction_update_interval
    @property
    def interaction_update_interval(self) -> int:
        return self._get_attr("interactionUpdateInterval", data_type="int", def_value=0)

    @interaction_update_interval.setter
    def interaction_update_interval(self, value: Optional[int]):
        self._set_attr("interactionUpdateInterval", value)

    # max_scale
    @property
    def max_scale(self) -> float:
        return self._get_attr("maxScale", data_type="float", def_value=2.5)

    @max_scale.setter
    def max_scale(self, value: OptionalNumber):
        self._set_attr("maxScale", value)

    # interaction_end_friction_coefficient
    @property
    def interaction_end_friction_coefficient(self) -> float:
        return self._get_attr(
            "interactionEndFrictionCoefficient", data_type="float", def_value=0.0000135
        )

    @interaction_end_friction_coefficient.setter
    def interaction_end_friction_coefficient(self, value: OptionalNumber):
        self._set_attr("interactionEndFrictionCoefficient", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # pan_enabled
    @property
    def pan_enabled(self) -> bool:
        return self._get_attr("panEnabled", data_type="bool", def_value=True)

    @pan_enabled.setter
    def pan_enabled(self, value: Optional[bool]):
        self._set_attr("panEnabled", value)

    # scale_enabled
    @property
    def scale_enabled(self) -> bool:
        return self._get_attr("scaleEnabled", data_type="bool", def_value=True)

    @scale_enabled.setter
    def scale_enabled(self, value: Optional[bool]):
        self._set_attr("scaleEnabled", value)

    # trackpad_scroll_causes_scale
    @property
    def trackpad_scroll_causes_scale(self) -> bool:
        return self._get_attr(
            "trackpadScrollCausesScale", data_type="bool", def_value=False
        )

    @trackpad_scroll_causes_scale.setter
    def trackpad_scroll_causes_scale(self, value: Optional[bool]):
        self._set_attr("trackpadScrollCausesScale", value)

    # constrained
    @property
    def constrained(self) -> bool:
        return self._get_attr("constrained", data_type="bool", def_value=True)

    @constrained.setter
    def constrained(self, value: Optional[bool]):
        self._set_attr("constrained", value)

    # scale_factor
    @property
    def scale_factor(self) -> float:
        return self._get_attr("scaleFactor", data_type="float", def_value=200)

    @scale_factor.setter
    def scale_factor(self, value: OptionalNumber):
        self._set_attr("scaleFactor", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # boundary_margin
    @property
    def boundary_margin(self) -> Optional[MarginValue]:
        return self.__boundary_margin

    @boundary_margin.setter
    def boundary_margin(self, value: Optional[MarginValue]):
        self.__boundary_margin = value

    # on_interaction_start
    @property
    def on_interaction_start(
        self,
    ) -> OptionalEventCallable[InteractiveViewerInteractionStartEvent]:
        return self.__on_interaction_start.handler

    @on_interaction_start.setter
    def on_interaction_start(
        self,
        handler: OptionalEventCallable[InteractiveViewerInteractionStartEvent],
    ):
        self.__on_interaction_start.handler = handler

    # on_interaction_update
    @property
    def on_interaction_update(
        self,
    ) -> OptionalEventCallable[InteractiveViewerInteractionUpdateEvent]:
        return self.__on_interaction_update.handler

    @on_interaction_update.setter
    def on_interaction_update(
        self,
        handler: OptionalEventCallable[InteractiveViewerInteractionUpdateEvent],
    ):
        self.__on_interaction_update.handler = handler

    # on_interaction_end
    @property
    def on_interaction_end(
        self,
    ) -> OptionalEventCallable[InteractiveViewerInteractionEndEvent]:
        return self.__on_interaction_end.handler

    @on_interaction_end.setter
    def on_interaction_end(
        self, handler: OptionalEventCallable[InteractiveViewerInteractionEndEvent]
    ):
        self.__on_interaction_end.handler = handler
