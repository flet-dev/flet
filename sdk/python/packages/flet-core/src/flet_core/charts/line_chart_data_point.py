from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class LineChartDataPoint(Control):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.x = x
        self.y = y

    def _get_control_name(self):
        return "p"

    def _get_children(self):
        children = []
        return children

    # x
    @property
    def x(self) -> OptionalNumber:
        return self._get_attr("x", data_type="float", def_value=1.0)

    @x.setter
    def x(self, value: OptionalNumber):
        self._set_attr("x", value)

    # y
    @property
    def y(self) -> OptionalNumber:
        return self._get_attr("y", data_type="float", def_value=1.0)

    @y.setter
    def y(self, value: OptionalNumber):
        self._set_attr("y", value)
