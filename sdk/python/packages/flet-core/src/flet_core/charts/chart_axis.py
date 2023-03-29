from typing import Any, List, Optional

from flet_core.charts.chart_axis_label import ChartAxisLabel
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class ChartAxis(Control):
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
        title_size: OptionalNumber = None,
        show_labels: Optional[bool] = None,
        labels: Optional[List[ChartAxisLabel]] = None,
        labels_interval: OptionalNumber = None,
        labels_size: OptionalNumber = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.title = title
        self.title_size = title_size
        self.show_labels = show_labels
        self.labels = labels
        self.labels_interval = labels_interval
        self.labels_size = labels_size

    def _get_control_name(self):
        return "axis"

    def _get_children(self):
        children = []
        for label in self.__labels:
            label._set_attr_internal("n", "l")
            children.append(label)
        if self.__title:
            self.__title._set_attr_internal("n", "t")
            children.append(self.__title)
        return children

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # title_size
    @property
    def title_size(self) -> OptionalNumber:
        return self._get_attr("titleSize", data_type="float")

    @title_size.setter
    def title_size(self, value: OptionalNumber):
        self._set_attr("titleSize", value)

    # show_labels
    @property
    def show_labels(self) -> Optional[bool]:
        return self._get_attr("showLabels", data_type="bool", def_value=True)

    @show_labels.setter
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
    def labels_interval(self, value: OptionalNumber):
        self._set_attr("labelsInterval", value)

    # labels_size
    @property
    def labels_size(self) -> OptionalNumber:
        return self._get_attr("labelsSize", data_type="float")

    @labels_size.setter
    def labels_size(self, value: OptionalNumber):
        self._set_attr("labelsSize", value)
