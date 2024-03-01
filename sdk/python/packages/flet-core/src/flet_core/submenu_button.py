import time
from typing import Any, List, Optional, Union

from flet_core.buttons import ButtonStyle
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.menu_bar import MenuStyle
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    ClipBehavior,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)
from flet_core.utils import deprecated


class SubmenuButton(ConstrainedControl):
    """
    A menu button that displays a cascading menu. It can be used as part of a MenuBar, or as a standalone control.

    -----

    Online docs: https://flet.dev/docs/controls/submenubutton
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        controls: Optional[List[Control]] = None,
        leading: Optional[Control] = None,
        trailing: Optional[Control] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        menu_style: Optional[MenuStyle] = None,
        style: Optional[ButtonStyle] = None,
        alignment_offset: OffsetValue = None,
        on_open=None,
        on_close=None,
        on_hover=None,
        on_focus=None,
        on_blur=None,
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

        self.content = content
        self.controls = controls
        self.leading = leading
        self.trailing = trailing
        self.clip_behavior = clip_behavior
        self.style = style
        self.menu_style = menu_style
        self.alignment_offset = alignment_offset
        self.on_open = on_open
        self.on_close = on_close
        self.on_hover = on_hover
        self.on_focus = on_focus
        self.on_blur = on_blur

    def _get_control_name(self):
        return "submenubutton"

    def before_update(self):
        super().before_update()
        if self.__style is not None:
            self.__style.side = self._wrap_attr_dict(self.__style.side)
            self.__style.shape = self._wrap_attr_dict(self.__style.shape)
        if self.__menu_style is not None:
            self.__menu_style.side = self._wrap_attr_dict(self.__menu_style.side)
            self.__menu_style.shape = self._wrap_attr_dict(self.__menu_style.shape)
        self._set_attr_json("style", self.__style)
        self._set_attr_json("menuStyle", self.__menu_style)

    def _get_children(self):
        children = []
        if self.__controls:
            for c in self.__controls:
                c._set_attr_internal("n", "controls")
                children.append(c)
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    def focus(self):
        self._set_attr_json("focus", str(time.time()))
        self.update()

    @deprecated(
        reason="Use focus() method instead.",
        version="0.21.0",
        delete_version="1.0",
    )
    async def focus_async(self):
        self.focus()

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # style
    @property
    def style(self) -> Optional[ButtonStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[ButtonStyle]):
        self.__style = value

    # menu_style
    @property
    def menu_style(self) -> Optional[MenuStyle]:
        return self.__menu_style

    @menu_style.setter
    def menu_style(self, value: Optional[MenuStyle]):
        self.__menu_style = value

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_attr(
            "clipBehavior", value.value if isinstance(value, ClipBehavior) else value
        )

    # alignment_offset
    @property
    def alignment_offset(self) -> OffsetValue:
        return self.__alignment_offset

    @alignment_offset.setter
    def alignment_offset(self, value: OffsetValue):
        self.__alignment_offset = value

    # on_open
    @property
    def on_open(self):
        return self._get_event_handler("open")

    @on_open.setter
    def on_open(self, handler):
        self._add_event_handler("open", handler)
        self._set_attr("onOpen", True if handler is not None else None)

    # on_close
    @property
    def on_close(self):
        return self._get_event_handler("close")

    @on_close.setter
    def on_close(self, handler):
        self._add_event_handler("close", handler)
        self._set_attr("onClose", True if handler is not None else None)

    # on_hover
    @property
    def on_hover(self):
        return self._get_event_handler("hover")

    @on_hover.setter
    def on_hover(self, handler):
        self._add_event_handler("hover", handler)
        self._set_attr("onHover", True if handler is not None else None)

    # on_focus
    @property
    def on_focus(self):
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self):
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler):
        self._add_event_handler("blur", handler)
