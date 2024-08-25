import time
from typing import Any, Optional, Union

from flet_core.alignment import Axis
from flet_core.buttons import ButtonStyle
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.tooltip import TooltipValue
from flet_core.types import (
    AnimationValue,
    ClipBehavior,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
    OptionalControlEventCallable,
)
from flet_core.utils import deprecated


class MenuItemButton(ConstrainedControl):
    """
    A button for use in a MenuBar or on its own, that can be activated by click or keyboard navigation.

    -----

    Online docs: https://flet.dev/docs/controls/menuitembutton
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        close_on_click: Optional[bool] = None,
        focus_on_hover: Optional[bool] = None,
        leading: Optional[Control] = None,
        trailing: Optional[Control] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        style: Optional[ButtonStyle] = None,
        semantic_label: Optional[str] = None,
        autofocus: Optional[bool] = None,
        overflow_axis: Optional[Axis] = None,
        on_click: OptionalControlEventCallable = None,
        on_hover: OptionalControlEventCallable = None,
        on_focus: OptionalControlEventCallable = None,
        on_blur: OptionalControlEventCallable = None,
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
        self.leading = leading
        self.trailing = trailing
        self.clip_behavior = clip_behavior
        self.style = style
        self.close_on_click = close_on_click
        self.focus_on_hover = focus_on_hover
        self.on_click = on_click
        self.on_hover = on_hover
        self.on_focus = on_focus
        self.on_blur = on_blur
        self.semantic_label = semantic_label
        self.autofocus = autofocus
        self.overflow_axis = overflow_axis

    def _get_control_name(self):
        return "menuitembutton"

    def before_update(self):
        super().before_update()
        if self.__style is not None:
            self.__style.side = self._wrap_attr_dict(self.__style.side)
            self.__style.shape = self._wrap_attr_dict(self.__style.shape)
            self.__style.padding = self._wrap_attr_dict(self.__style.padding)
        self._set_attr_json("style", self.__style)

    def _get_children(self):
        children = []
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
        delete_version="0.26.0",
    )
    async def focus_async(self):
        self.focus()

    # focus_on_hover
    @property
    def focus_on_hover(self) -> bool:
        return self._get_attr("focusOnHover", data_type="bool", def_value=True)

    @focus_on_hover.setter
    def focus_on_hover(self, value: Optional[bool]):
        self._set_attr("focusOnHover", value)

    # close_on_click
    @property
    def close_on_click(self) -> bool:
        return self._get_attr("closeOnClick", data_type="bool", def_value=True)

    @close_on_click.setter
    def close_on_click(self, value: Optional[bool]):
        self._set_attr("closeOnClick", value)

    # semantic_label
    @property
    def semantic_label(self) -> Optional[str]:
        return self._get_attr("semanticLabel")

    @semantic_label.setter
    def semantic_label(self, value: Optional[str]):
        self._set_attr("semanticLabel", value)

    # autofocus
    @property
    def autofocus(self) -> bool:
        return self._get_attr("autofocus", data_type="bool", def_value=False)

    @autofocus.setter
    def autofocus(self, value: Optional[bool]):
        self._set_attr("autofocus", value)

    # overflow_axis
    @property
    def overflow_axis(self) -> Optional[Axis]:
        return self.__overflow_axis

    @overflow_axis.setter
    def overflow_axis(self, value: Optional[Axis]):
        self.__overflow_axis = value
        self._set_enum_attr("overflowAxis", value, Axis)

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

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
        self._set_attr("onClick", True if handler is not None else None)

    # on_hover
    @property
    def on_hover(self) -> OptionalControlEventCallable:
        return self._get_event_handler("hover")

    @on_hover.setter
    def on_hover(self, handler: OptionalControlEventCallable):
        self._add_event_handler("hover", handler)
        self._set_attr("onHover", True if handler is not None else None)

    # on_focus
    @property
    def on_focus(self) -> OptionalControlEventCallable:
        return self._get_event_handler("focus")

    @on_focus.setter
    def on_focus(self, handler: OptionalControlEventCallable):
        self._add_event_handler("focus", handler)

    # on_blur
    @property
    def on_blur(self) -> OptionalControlEventCallable:
        return self._get_event_handler("blur")

    @on_blur.setter
    def on_blur(self, handler: OptionalControlEventCallable):
        self._add_event_handler("blur", handler)
