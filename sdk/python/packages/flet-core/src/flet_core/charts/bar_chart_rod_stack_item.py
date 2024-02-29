from typing import Any, Optional

from flet_core.border import BorderSide
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class BarChartRodStackItem(Control):
    def __init__(
        self,
        from_y: OptionalNumber = None,
        to_y: OptionalNumber = None,
        color: Optional[str] = None,
        border_side: Optional[BorderSide] = None,
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

        self.from_y = from_y
        self.to_y = to_y
        self.color = color
        self.border_side = border_side

    def _get_control_name(self):
        return "stack_item"

    def before_update(self):
        super().before_update()
        self._set_attr_json("borderSide", self.__border_side)

    # from_y
    @property
    def from_y(self) -> OptionalNumber:
        return self._get_attr("fromY", data_type="float")

    @from_y.setter
    def from_y(self, value: OptionalNumber):
        self._set_attr("fromY", value)

    # to_y
    @property
    def to_y(self) -> OptionalNumber:
        return self._get_attr("toY", data_type="float")

    @to_y.setter
    def to_y(self, value: OptionalNumber):
        self._set_attr("toY", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # border_side
    @property
    def border_side(self) -> Optional[BorderSide]:
        return self.__border_side

    @border_side.setter
    def border_side(self, value: Optional[BorderSide]):
        self.__border_side = value
