from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import TextAlign, TextAlignString


class LineChartDataPoint(Control):
    def __init__(
        self,
        x: OptionalNumber = None,
        y: OptionalNumber = None,
        show_tooltip: Optional[bool] = None,
        tooltip: Optional[str] = None,
        tooltip_style: Optional[TextStyle] = None,
        tooltip_align: TextAlign = TextAlign.NONE,
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
        self.show_tooltip = show_tooltip
        self.tooltip = tooltip
        self.tooltip_align = tooltip_align
        self.tooltip_style = tooltip_style

    def _get_control_name(self):
        return "p"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("tooltipStyle", self.__tooltip_style)

    def _get_children(self):
        children = []
        return children

    # x
    @property
    def x(self) -> OptionalNumber:
        return self._get_attr("x", data_type="float", def_value=0)

    @x.setter
    def x(self, value: OptionalNumber):
        self._set_attr("x", value)

    # y
    @property
    def y(self) -> OptionalNumber:
        return self._get_attr("y", data_type="float", def_value=0)

    @y.setter
    def y(self, value: OptionalNumber):
        self._set_attr("y", value)

    # show_tooltip
    @property
    def show_tooltip(self) -> Optional[bool]:
        return self._get_attr("showTooltip", data_type="bool", def_value=True)

    @show_tooltip.setter
    def show_tooltip(self, value: Optional[bool]):
        self._set_attr("showTooltip", value)

    # tooltip
    @property
    def tooltip(self) -> Optional[str]:
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value: Optional[str]):
        self._set_attr("tooltip", value)

    # tooltip_align
    @property
    def tooltip_align(self) -> TextAlign:
        return self.__tooltip_align

    @tooltip_align.setter
    def tooltip_align(self, value: TextAlign):
        self.__tooltip_align = value
        if isinstance(value, TextAlign):
            self._set_attr("tooltipAlign", value.value)
        else:
            self.__set_tooltip_align(value)

    def __set_tooltip_align(self, value: TextAlignString):
        self._set_attr("tooltipAlign", value)

    # tooltip_style
    @property
    def tooltip_style(self):
        return self.__tooltip_style

    @tooltip_style.setter
    def tooltip_style(self, value: Optional[TextStyle]):
        self.__tooltip_style = value
