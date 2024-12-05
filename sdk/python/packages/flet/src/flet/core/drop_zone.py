import asyncio
from enum import Enum
import json
from typing import Any, List, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.animation import AnimationValue
from flet.core.tooltip import TooltipValue
from flet.core.badge import BadgeValue


from flet.core.constrained_control import ConstrainedControl
from flet.core.control_event import ControlEvent
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.types import (
    ClipBehavior,
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class StackFit(Enum):
    LOOSE = "loose"
    EXPAND = "expand"
    PASS_THROUGH = "passThrough"

class ListFiles(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.files: float = d.get("files")

class EventHandler:
    def __init__(self, result_converter=None) -> None:
        self.__result_converter = result_converter
        self.handler: OptionalControlEventCallable = None

    def get_handler(self):
        async def fn(e: ControlEvent):
            if self.handler is not None:
                ce = e
                if self.__result_converter is not None:
                    ce = self.__result_converter(e)
                    if ce is not None:
                        # ce.target = e.target
                        # ce.name = e.name
                        # ce.data = e.data
                        # ce.control = e.control
                        # ce.page = e.page
                        data = json.loads(e.data)
                        ce.files = data.get("files",[])

                if ce is not None:
                    if asyncio.iscoroutinefunction(self.handler):
                        await self.handler(ce)
                    else:
                        e.page.run_thread(self.handler, ce)

        return fn
        

class DropZone(ConstrainedControl, AdaptiveControl):
    def __init__(
        self,
        content: Optional[Control] = None,

        on_dropped: Optional[callable] = None,
        on_exited: Optional[callable] = None,
        on_entered: Optional[callable] = None,

        allowed_file_types: Optional[list] = [],


        
        clip_behavior: Optional[ClipBehavior] = None,
        alignment: Optional[Alignment] = None,
        fit: Optional[StackFit] = None,
        
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
        animate_opacity: Optional[AnimationValue] = None,
        animate_size: Optional[AnimationValue] = None,
        animate_position: Optional[AnimationValue] = None,
        animate_rotation: Optional[AnimationValue] = None,
        animate_scale: Optional[AnimationValue] = None,
        animate_offset: Optional[AnimationValue] = None,
        on_animation_end: OptionalControlEventCallable = None,
        tooltip: TooltipValue = None,
        badge: Optional[BadgeValue] = None,
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
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__on_dropped = EventHandler(lambda e: ListFiles(e))
        self._add_event_handler("dropped", self.__on_dropped.get_handler())


        self.content = content
        self.clip_behavior = clip_behavior
        self.alignment = alignment
        self.fit = fit

        self.on_dropped = on_dropped
        self.on_entered = on_entered
        self.on_exited = on_exited

        self.allowed_file_types = allowed_file_types
        
 
    def _get_control_name(self):
        return "dropzone"

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def before_update(self):
        super().before_update()
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("allowedFileTypes", self.allowed_file_types)
        self._set_attr_json("disabled", self.disabled)
        
  
    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

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
    

    # on_dropped
    @property
    def on_dropped(self) -> OptionalControlEventCallable:
        return self.__on_dropped.handler

    @on_dropped.setter
    def on_dropped(self, handler: OptionalControlEventCallable):
        self.__on_dropped.handler = handler


    # on_entered
    @property
    def on_entered(self) -> OptionalControlEventCallable:
        return self._get_event_handler("entered")

    @on_entered.setter
    def on_entered(self, handler: OptionalControlEventCallable):
        self._add_event_handler("entered", handler)
    
    # on_exited
    @property
    def on_exited(self) -> OptionalControlEventCallable:
        return self._get_event_handler("exited")

    @on_exited.setter
    def on_exited(self, handler: OptionalControlEventCallable):
        self._add_event_handler("exited", handler)
    
