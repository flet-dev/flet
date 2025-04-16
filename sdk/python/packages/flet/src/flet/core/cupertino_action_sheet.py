from typing import Any, List, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    OffsetValue,
    OptionalControlEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoActionSheet(ConstrainedControl):
    """
    An iOS-style action sheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheet
    """

    def __init__(
        self,
        title: Optional[Control] = None,
        message: Optional[Control] = None,
        actions: Optional[List[Control]] = None,
        cancel: Optional[Control] = None,
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
        tooltip: Optional[TooltipValue] = None,
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

        self.cancel = cancel
        self.title = title
        self.message = message
        self.actions = actions

    def _get_control_name(self):
        return "cupertinoactionsheet"

    def _get_children(self):
        children = []
        if self.__cancel:
            self.__cancel._set_attr_internal("n", "cancel")
            children.append(self.__cancel)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__message:
            self.__message._set_attr_internal("n", "message")
            children.append(self.__message)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # cancel
    @property
    def cancel(self) -> Optional[Control]:
        return self.__cancel

    @cancel.setter
    def cancel(self, value: Optional[Control]):
        self.__cancel = value

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # message
    @property
    def message(self) -> Optional[Control]:
        return self.__message

    @message.setter
    def message(self, value: Optional[Control]):
        self.__message = value

    # actions
    @property
    def actions(self) -> List[Control]:
        return self.__actions

    @actions.setter
    def actions(self, value: Optional[List[Control]]):
        self.__actions = value if value is not None else []
