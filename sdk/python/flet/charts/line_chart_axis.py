from typing import Any, List, Optional

from beartype import beartype
from flet.charts.line_chart_axis_label import LineChartAxisLabel

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class LineChartAxis(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        title: Optional[Control] = None,
        show_labels: Optional[bool] = None,
        labels: Optional[List[LineChartAxisLabel]] = None,
        labels_interval: OptionalNumber = None,
        reserved_size: OptionalNumber = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.title = title
        self.show_labels = show_labels
        self.labels = labels
        self.labels_interval = labels_interval
        self.reserved_size = reserved_size

    def _get_control_name(self):
        return "axis"

    def _get_children(self):
        children = []
        for label in self.__labels:
            label._set_attr_internal("n", "label")
            children.append(label)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        return children

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    @beartype
    def title(self, value: Optional[Control]):
        self.__title = value

    # show_labels
    @property
    def show_labels(self) -> Optional[bool]:
        return self._get_attr("showLabels", data_type="bool", def_value=False)

    @show_labels.setter
    @beartype
    def show_labels(self, value: Optional[bool]):
        self._set_attr("showLabels", value)

    # labels
    @property
    def labels(self):
        return self.__labels

    @labels.setter
    def labels(self, value):
        self.__labels = value if value is not None else []

    # labels_interval
    @property
    def labels_interval(self) -> OptionalNumber:
        return self._get_attr("labelsInterval", data_type="float", def_value=1.0)

    @labels_interval.setter
    @beartype
    def labels_interval(self, value: OptionalNumber):
        self._set_attr("labelsInterval", value)

    # reserved_size
    @property
    def reserved_size(self) -> OptionalNumber:
        return self._get_attr("reservedSize", data_type="float", def_value=1.0)

    @reserved_size.setter
    @beartype
    def reserved_size(self, value: OptionalNumber):
        self._set_attr("reservedSize", value)
