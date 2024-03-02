import dataclasses
from dataclasses import field
from typing import Any, Dict, List, Optional, Union

from flet_core.alignment import Alignment
from flet_core.border import BorderSide
from flet_core.buttons import OutlinedBorder
from flet_core.control import Control, OptionalNumber
from flet_core.gesture_detector import MouseCursor
from flet_core.ref import Ref
from flet_core.types import ClipBehavior, MaterialState, PaddingValue, ResponsiveNumber


@dataclasses.dataclass
class MenuStyle:
    alignment: Optional[Alignment] = field(default=None)
    bgcolor: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    shadow_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    surface_tint_color: Union[None, str, Dict[Union[str, MaterialState], str]] = field(
        default=None
    )
    elevation: Union[
        None, float, int, Dict[Union[str, MaterialState], Union[float, int]]
    ] = field(default=None)
    padding: Union[PaddingValue, Dict[Union[str, MaterialState], PaddingValue]] = field(
        default=None
    )
    side: Union[None, BorderSide, Dict[Union[str, MaterialState], BorderSide]] = field(
        default=None
    )
    shape: Union[
        None, OutlinedBorder, Dict[Union[str, MaterialState], OutlinedBorder]
    ] = field(default=None)
    mouse_cursor: Union[
        None, MouseCursor, Dict[Union[str, MaterialState], MouseCursor]
    ] = field(default=None)


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
        controls: Optional[List[Control]] = None,
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

        self.__controls: List[Control] = []
        self.controls = controls
        self.clip_behavior = clip_behavior
        self.style = style

    def _get_control_name(self):
        return "menubar"

    def before_update(self):
        super().before_update()
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

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value if value is not None else []

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

    # style
    @property
    def style(self) -> Optional[MenuStyle]:
        return self.__style

    @style.setter
    def style(self, value: Optional[MenuStyle]):
        self.__style = value
