from typing import Any, List, Optional

from flet_core.border import BorderSide
from flet_core.charts.bar_chart_rod_stack_item import BarChartRodStackItem
from flet_core.control import Control, OptionalNumber
from flet_core.gradients import Gradient
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import BorderRadiusValue, TextAlign


class BarChartRod(Control):
    def __init__(
        self,
        rod_stack_items: Optional[List[BarChartRodStackItem]] = None,
        from_y: OptionalNumber = None,
        to_y: OptionalNumber = None,
        width: OptionalNumber = None,
        color: Optional[str] = None,
        gradient: Optional[Gradient] = None,
        border_radius: BorderRadiusValue = None,
        border_side: Optional[BorderSide] = None,
        bg_from_y: OptionalNumber = None,
        bg_to_y: OptionalNumber = None,
        bg_color: Optional[str] = None,
        bg_gradient: Optional[Gradient] = None,
        selected: Optional[bool] = None,
        show_tooltip: Optional[bool] = None,
        tooltip: Optional[str] = None,
        tooltip_style: Optional[TextStyle] = None,
        tooltip_align: Optional[TextAlign] = None,
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

        self.rod_stack_items = rod_stack_items
        self.from_y = from_y
        self.to_y = to_y
        self.width = width
        self.color = color
        self.gradient = gradient
        self.border_side = border_side
        self.border_radius = border_radius
        self.bg_from_y = bg_from_y
        self.bg_to_y = bg_to_y
        self.bg_color = bg_color
        self.bg_gradient = bg_gradient
        self.selected = selected
        self.show_tooltip = show_tooltip
        self.tooltip = tooltip
        self.tooltip_align = tooltip_align
        self.tooltip_style = tooltip_style

    def _get_control_name(self):
        return "rod"

    def before_update(self):
        super().before_update()
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("borderSide", self.__border_side)
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("bgGradient", self.__bg_gradient)

    def _get_children(self):
        return self.__rod_stack_items

    # rod_stack_items
    @property
    def rod_stack_items(self):
        return self.__rod_stack_items

    @rod_stack_items.setter
    def rod_stack_items(self, value):
        self.__rod_stack_items = value if value is not None else []

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

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width", data_type="float")

    @width.setter
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

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

    # border_radius
    @property
    def border_radius(self) -> Optional[BorderRadiusValue]:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: Optional[BorderRadiusValue]):
        self.__border_radius = value

    # gradient
    @property
    def gradient(self) -> Optional[Gradient]:
        return self.__gradient

    @gradient.setter
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # bg_from_y
    @property
    def bg_from_y(self) -> OptionalNumber:
        return self._get_attr("bgFromY", data_type="float")

    @bg_from_y.setter
    def bg_from_y(self, value: OptionalNumber):
        self._set_attr("bgFromY", value)

    # bg_to_y
    @property
    def bg_to_y(self) -> OptionalNumber:
        return self._get_attr("bgToY", data_type="float")

    @bg_to_y.setter
    def bg_to_y(self, value: OptionalNumber):
        self._set_attr("bgToY", value)

    # bg_color
    @property
    def bg_color(self) -> Optional[str]:
        return self._get_attr("bgColor")

    @bg_color.setter
    def bg_color(self, value: Optional[str]):
        self._set_attr("bgColor", value)

    # bg_gradient
    @property
    def bg_gradient(self) -> Optional[Gradient]:
        return self.__bg_gradient

    @bg_gradient.setter
    def bg_gradient(self, value: Optional[Gradient]):
        self.__bg_gradient = value

    # selected
    @property
    def selected(self) -> bool:
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # show_tooltip
    @property
    def show_tooltip(self) -> bool:
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
    def tooltip_align(self) -> Optional[TextAlign]:
        return self.__tooltip_align

    @tooltip_align.setter
    def tooltip_align(self, value: Optional[TextAlign]):
        self.__tooltip_align = value
        self._set_attr(
            "tooltipAlign", value.value if isinstance(value, TextAlign) else value
        )

    # tooltip_style
    @property
    def tooltip_style(self):
        return self.__tooltip_style

    @tooltip_style.setter
    def tooltip_style(self, value: Optional[TextStyle]):
        self.__tooltip_style = value
