from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoActionSheetAction(ConstrainedControl):
    """
    An action button typically used in a CupertinoActionSheet.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoactionsheetaction
    """

    def __init__(
        self,
        text: Optional[str] = None,
        content: Optional[Control] = None,
        is_default_action: Optional[bool] = None,
        is_destructive_action: Optional[bool] = None,
        on_click=None,
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
        on_animation_end=None,
        tooltip: Optional[str] = None,
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
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.text = text
        self.content = content
        self.is_default_action = is_default_action
        self.is_destructive_action = is_destructive_action
        self.on_click = on_click

    def _get_control_name(self):
        return "cupertinoactionsheetaction"

    def before_update(self):
        super().before_update()

    def _get_children(self):
        children = []
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # text
    @property
    def text(self):
        return self._get_attr("text")

    @text.setter
    def text(self, value):
        self._set_attr("text", value)

    # is_default_action
    @property
    def is_default_action(self) -> Optional[bool]:
        return self._get_attr("isDefaultAction")

    @is_default_action.setter
    def is_default_action(self, value: Optional[bool]):
        self._set_attr("isDefaultAction", value)

    # is_destructive_action
    @property
    def is_destructive_action(self) -> Optional[bool]:
        return self._get_attr("isDestructiveAction")

    @is_destructive_action.setter
    def is_destructive_action(self, value: Optional[bool]):
        self._set_attr("isDestructiveAction", value)

    # content
    @property
    def content(self) -> Control:
        return self.__content

    @content.setter
    def content(self, value: Control):
        self.__content = value

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
