from dataclasses import field
from typing import List, Optional

from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.material.menu_bar import MenuStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import ClipBehavior, OptionalControlEventCallable

__all__ = ["SubmenuButton"]


@control("SubmenuButton")
class SubmenuButton(ConstrainedControl):
    """
    A menu button that displays a cascading menu. It can be used as part of a MenuBar, or as a standalone control.

    -----

    Online docs: https://flet.dev/docs/controls/submenubutton
    """

    content: Optional[Control] = None
    controls: List[Control] = field(default_factory=list)
    leading: Optional[Control] = None
    trailing: Optional[Control] = None
    clip_behavior: Optional[ClipBehavior] = None
    menu_style: Optional[MenuStyle] = None
    style: Optional[ButtonStyle] = None
    alignment_offset: Optional[OffsetValue] = None
    on_open: OptionalControlEventCallable = None
    on_close: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    # def before_update(self):
    #     super().before_update()
    #     if self.__style is not None:
    #         self.__style.side = self._wrap_attr_dict(self.__style.side)
    #         self.__style.shape = self._wrap_attr_dict(self.__style.shape)
    #     if self.__menu_style is not None:
    #         self.__menu_style.side = self._wrap_attr_dict(self.__menu_style.side)
    #         self.__menu_style.shape = self._wrap_attr_dict(self.__menu_style.shape)
    #     self._set_attr_json("style", self.__style)
    #     self._set_attr_json("menuStyle", self.__menu_style)
