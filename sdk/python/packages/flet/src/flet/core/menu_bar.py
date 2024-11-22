from dataclasses import dataclass
from typing import Any, List, Optional, Sequence, Union

from flet.core.alignment import Alignment
from flet.core.border import BorderSide
from flet.core.buttons import OutlinedBorder
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.types import (
    ClipBehavior,
    ColorValue,
    ControlState,
    ControlStateValue,
    MouseCursor,
    OptionalNumber,
    PaddingValue,
    ResponsiveNumber,
)


@dataclass
class MenuStyle:
    alignment: Optional[Alignment] = None
    bgcolor: ControlStateValue[ColorValue] = None
    shadow_color: ControlStateValue[ColorValue] = None
    surface_tint_color: ControlStateValue[ColorValue] = None
    elevation: ControlStateValue[OptionalNumber] = None
    padding: ControlStateValue[PaddingValue] = None
    side: ControlStateValue[BorderSide] = None
    shape: ControlStateValue[OutlinedBorder] = None
    mouse_cursor: ControlStateValue[MouseCursor] = None

    def __post_init__(self):
        if not isinstance(self.padding, dict):
            self.padding = {ControlState.DEFAULT: self.padding}

        if not isinstance(self.side, dict):
            self.side = {ControlState.DEFAULT: self.side}

        if not isinstance(self.shape, dict):
            self.shape = {ControlState.DEFAULT: self.shape}


class MenuBar(Control):
    """
    A menu bar that manages cascading child menus.

    It could be placed anywhere but typically resides above the main body of the application
    and defines a menu system for invoking callbacks in response to user selection of a menu item.

    -----

    Online docs: https://flet.dev/docs/controls/menubar
    """

    def __init__(
        self,
        controls: Sequence[Control],
        clip_behavior: Optional[ClipBehavior] = None,
        style: Optional[MenuStyle] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            expand_loose=expand_loose,
            col=col,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.controls = controls
        self.clip_behavior = clip_behavior
        self.style = style

    def _get_control_name(self):
        return "menubar"

    def before_update(self):
        super().before_update()
        assert any(
            c.visible for c in self.__controls
        ), "MenuBar must have at minimum one visible control"
        if self.__style is not None:
            self.__style.side = self._wrap_attr_dict(self.__style.side)
            self.__style.shape = self._wrap_attr_dict(self.__style.shape)
            self.__style.mouse_cursor = self._wrap_attr_dict(self.__style.mouse_cursor)
            if self.__style.mouse_cursor:
                for k, v in self.__style.mouse_cursor.items():
                    self.__style.mouse_cursor[k] = (
                        v.value if isinstance(v, MouseCursor) else str(v)
                    )
        self._set_attr_json("style", self.__style)

    def _get_children(self):
        return self.__controls

    def __contains__(self, item):
        return item in self.__controls

    # controls
    @property
    def controls(self) -> List[Control]:
        return self.__controls

    @controls.setter
    def controls(self, value: Sequence[Control]):
        self.__controls = list(value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # style
    @property
    def style(self) -> Optional[MenuStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[MenuStyle]):
        self.__style = value
