from enum import Enum
import json
from typing import Any, List, Optional, Sequence, Union

from flet.core.adaptive_control import AdaptiveControl
from flet.core.alignment import Alignment
from flet.core.event_handler import EventHandler

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

class LayoutDimensions(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.width: float = d.get("width")
        self.height: float = d.get("height")
        

class LayoutBuilder(ConstrainedControl, AdaptiveControl):
    def __init__(
        self,
        content: Optional[Control] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        alignment: Optional[Alignment] = None,
        fit: Optional[StackFit] = None,
        expand: Union[None, bool, int] = None,
        on_change: OptionalControlEventCallable = None,
        #
        # ConstrainedControl and AdaptiveControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        adaptive: Optional[bool] = None,
        update_size_on_init: Optional[bool] = True
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
            expand=expand,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.content = content
        self.clip_behavior = clip_behavior
        self.alignment = alignment
        self.fit = fit
        self.__on_change_callback = on_change
        self.__update_size_on_init = update_size_on_init
        self.__old_width = None
        self.__old_height = None
        self.on_change = self.__on_change
        
    
    def __on_change(self,e):
        e = LayoutDimensions(e)
        if e.width!=self.__old_width or e.height!=self.__old_height:
            self.__old_height = e.height
            self.__old_width = e.width
            if self.__on_change_callback:
                self.__on_change_callback(e)

    def _get_control_name(self):
        return "layoutbuilder"

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def before_update(self):
        super().before_update()
        if self.__update_size_on_init==True:
            self._set_attr_json("update_on_build", self.__update_size_on_init)
        self._set_attr_json("alignment", self.__alignment)
  
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
    
    # on_change
    @property
    def on_change(self) -> OptionalControlEventCallable:
        return self._get_event_handler("layout_change")

    @on_change.setter
    def on_change(self, handler: OptionalControlEventCallable):
        self._add_event_handler("layout_change", handler)
    
    @property
    def layout_size(self):
        width = self._get_attr("layoutWidth")
        height = self._get_attr("layoutHeight")
        return (float(width),float(height))
    