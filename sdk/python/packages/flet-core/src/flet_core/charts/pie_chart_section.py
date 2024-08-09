from typing import Any, Optional

from flet_core.border import BorderSide
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle


class PieChartSection(Control):
    def __init__(
        self,
        value: OptionalNumber = None,
        radius: OptionalNumber = None,
        color: Optional[str] = None,
        border_side: Optional[BorderSide] = None,
        title: Optional[str] = None,
        title_style: Optional[TextStyle] = None,
        title_position: OptionalNumber = None,
        badge: Optional[Control] = None,
        badge_position: OptionalNumber = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.value = value
        self.radius = radius
        self.color = color
        self.border_side = border_side
        self.title = title
        self.title_style = title_style
        self.title_position = title_position
        self.badge = badge
        self.badge_position = badge_position

    def _get_control_name(self):
        return "section"

    def before_update(self):
        super().before_update()
        self._set_attr_json("borderSide", self.__border_side)
        self._set_attr_json("titleStyle", self.__title_style)

    def _get_children(self):
        children = []
        if self.__badge:
            self.__badge._set_attr_internal("n", "badge")
            children.append(self.__badge)
        return children

    # value
    @property
    def value(self) -> OptionalNumber:
        return self._get_attr("value", data_type="float")

    @value.setter
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # radius
    @property
    def radius(self) -> OptionalNumber:
        return self._get_attr("radius", data_type="float")

    @radius.setter
    def radius(self, value: OptionalNumber):
        self._set_attr("radius", value)

    # border_side
    @property
    def border_side(self) -> Optional[BorderSide]:
        return self.__border_side

    @border_side.setter
    def border_side(self, value: Optional[BorderSide]):
        self.__border_side = value

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # badge
    @property
    def badge(self) -> Optional[Control]:
        return self.__badge

    @badge.setter
    def badge(self, value: Optional[Control]):
        self.__badge = value

    # badge_position
    @property
    def badge_position(self) -> OptionalNumber:
        return self._get_attr("badgePosition", data_type="float")

    @badge_position.setter
    def badge_position(self, value: OptionalNumber):
        self._set_attr("badgePosition", value)

    # title
    @property
    def title(self):
        return self._get_attr("title")

    @title.setter
    def title(self, value: Optional[str]):
        self._set_attr("title", value)

    # title_style
    @property
    def title_style(self):
        return self.__title_style

    @title_style.setter
    def title_style(self, value: Optional[TextStyle]):
        self.__title_style = value

    # title_position
    @property
    def title_position(self) -> float:
        return self._get_attr("titlePosition", data_type="float", def_value=1.0)

    @title_position.setter
    def title_position(self, value: OptionalNumber):
        self._set_attr("titlePosition", value)
