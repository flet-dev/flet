from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class ChartAxisLabel(Control):
    def __init__(
        self,
        value: OptionalNumber = None,
        label: Optional[Control] = None,
        #
        # Specific
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
        self.label = label

    def _get_control_name(self):
        return "l"

    def _get_children(self):
        children = []
        if self.__label:
            children.append(self.__label)
        return children

    # value
    @property
    def value(self) -> float:
        return self._get_attr("value", data_type="float", def_value=1.0)

    @value.setter
    def value(self, value: OptionalNumber):
        self._set_attr("value", value)

    # label
    @property
    def label(self) -> Optional[Control]:
        return self.__label

    @label.setter
    def label(self, value: Optional[Control]):
        self.__label = value
