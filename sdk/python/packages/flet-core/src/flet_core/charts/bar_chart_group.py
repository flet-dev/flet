from typing import Any, List, Optional

from flet_core.charts.bar_chart_rod import BarChartRod
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class BarChartGroup(Control):
    def __init__(
        self,
        x: Optional[int] = None,
        bar_rods: Optional[List[BarChartRod]] = None,
        group_vertically: Optional[bool] = None,
        bars_space: OptionalNumber = None,
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

        self.x = x
        self.bar_rods = bar_rods
        self.group_vertically = group_vertically
        self.bars_space = bars_space

    def _get_control_name(self):
        return "group"

    def before_update(self):
        super().before_update()

    def _get_children(self):
        return self.__bar_rods

    # bar_rods
    @property
    def bar_rods(self):
        return self.__bar_rods

    @bar_rods.setter
    def bar_rods(self, value):
        self.__bar_rods = value if value is not None else []

    # x
    @property
    def x(self) -> Optional[int]:
        return self._get_attr("x", data_type="int")

    @x.setter
    def x(self, value: Optional[int]):
        self._set_attr("x", value)

    # group_vertically
    @property
    def group_vertically(self) -> bool:
        return self._get_attr("groupVertically", data_type="bool", def_value=False)

    @group_vertically.setter
    def group_vertically(self, value: Optional[bool]):
        self._set_attr("groupVertically", value)

    # bars_space
    @property
    def bars_space(self) -> OptionalNumber:
        return self._get_attr("barsSpace", data_type="float")

    @bars_space.setter
    def bars_space(self, value: OptionalNumber):
        self._set_attr("barsSpace", value)
