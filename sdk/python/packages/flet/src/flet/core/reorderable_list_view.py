import json
from typing import Any, Optional, Sequence, Union

from flet.core.animation import AnimationValue
from flet.core.control import Control, OptionalNumber
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.list_view import ListView
from flet.core.ref import Ref
from flet.core.scrollable_control import OnScrollEvent
from flet.core.types import (
    ClipBehavior,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class OnReorderEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.new_index: Optional[int] = d.get("new")
        self.old_index: Optional[int] = d.get("old")


class ReorderableListView(ListView):
    """
    A scrollable list of controls that can be reordered.

    -----

    Online docs: https://flet.dev/docs/controls/reorderablelistview
    """

    def __init__(
            self,
            controls: Optional[Sequence[Control]] = None,
            horizontal: Optional[bool] = None,
            item_extent: OptionalNumber = None,
            first_item_prototype: Optional[bool] = None,
            padding: PaddingValue = None,
            clip_behavior: Optional[ClipBehavior] = None,
            cache_extent: OptionalNumber = None,
            anchor: OptionalNumber = None,
            auto_scroller_velocity_scalar: OptionalNumber = None,
            header: Optional[Control] = None,
            footer: Optional[Control] = None,
            build_controls_on_demand: Optional[bool] = None,
            on_reorder: OptionalEventCallable[OnReorderEvent] = None,
            on_reorder_start: OptionalEventCallable[OnReorderEvent] = None,
            on_reorder_end: OptionalEventCallable[OnReorderEvent] = None,
            #
            # ScrollableControl
            #
            auto_scroll: Optional[bool] = None,
            reverse: Optional[bool] = None,
            on_scroll_interval: OptionalNumber = None,
            on_scroll: OptionalEventCallable[OnScrollEvent] = None,
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
        ListView.__init__(
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
            auto_scroll=auto_scroll,
            reverse=reverse,
            on_scroll_interval=on_scroll_interval,
            on_scroll=on_scroll,
            adaptive=adaptive,
            controls=controls,
            horizontal=horizontal,
            item_extent=item_extent,
            first_item_prototype=first_item_prototype,
            padding=padding,
            clip_behavior=clip_behavior,
            cache_extent=cache_extent,
            build_controls_on_demand=build_controls_on_demand,
        )
        self.__on_reorder = EventHandler(lambda e: OnReorderEvent(e))
        self._add_event_handler("reorder", self.__on_reorder.get_handler())

        self.__on_reorder_start = EventHandler(lambda e: OnReorderEvent(e))
        self._add_event_handler("reorder_start", self.__on_reorder_start.get_handler())

        self.__on_reorder_end = EventHandler(lambda e: OnReorderEvent(e))
        self._add_event_handler("reorder_end", self.__on_reorder_end.get_handler())

        self.header = header
        self.footer = footer
        self.on_reorder = on_reorder
        self.anchor = anchor
        self.auto_scroller_velocity_scalar = auto_scroller_velocity_scalar
        self.on_reorder_start = on_reorder_start
        self.on_reorder_end = on_reorder_end

    def _get_control_name(self):
        return "reorderablelistview"

    def before_update(self):
        super().before_update()

    def _get_children(self):
        children = super()._get_children()
        if self.header:
            self.__header._set_attr_internal("n", "header")
            children.append(self.header)
        if self.footer:
            self.__footer._set_attr_internal("n", "footer")
            children.append(self.footer)
        return children

    # anchor
    @property
    def anchor(self) -> OptionalNumber:
        return self._get_attr("anchor", data_type="float", def_value=0.0)

    @anchor.setter
    def anchor(self, value: OptionalNumber):
        self._set_attr("anchor", value)

    # auto_scroller_velocity_scalar
    @property
    def auto_scroller_velocity_scalar(self) -> OptionalNumber:
        return self._get_attr("autoScrollerVelocityScalar", data_type="float")

    @auto_scroller_velocity_scalar.setter
    def auto_scroller_velocity_scalar(self, value: OptionalNumber):
        self._set_attr("autoScrollerVelocityScalar", value)

    # header
    @property
    def header(self) -> Optional[Control]:
        return self.__header

    @header.setter
    def header(self, value: Optional[Control]):
        self.__header = value

    # footer
    @property
    def footer(self) -> Optional[Control]:
        return self.__footer

    @footer.setter
    def footer(self, value: Optional[Control]):
        self.__footer = value

    # on_reorder
    @property
    def on_reorder(self) -> OptionalEventCallable[OnReorderEvent]:
        return self.__on_reorder.handler

    @on_reorder.setter
    def on_reorder(self, handler: OptionalEventCallable[OnReorderEvent]):
        self.__on_reorder.handler = handler

    # on_reorder_start
    @property
    def on_reorder_start(self) -> OptionalEventCallable[OnReorderEvent]:
        return self.__on_reorder_start.handler

    @on_reorder_start.setter
    def on_reorder_start(self, handler: OptionalEventCallable[OnReorderEvent]):
        self.__on_reorder_start.handler = handler

    # on_reorder_end
    @property
    def on_reorder_end(self) -> OptionalEventCallable[OnReorderEvent]:
        return self.__on_reorder_end.handler

    @on_reorder_end.setter
    def on_reorder_end(self, handler: OptionalEventCallable[OnReorderEvent]):
        self.__on_reorder_end.handler = handler
