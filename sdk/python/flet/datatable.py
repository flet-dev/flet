from typing import Optional

from beartype import beartype
from beartype.typing import List

from flet.control import Control
from flet.ref import Ref


class DataColumn(Control):
    def __init__(
        self,
        label: Control,
        ref=None,
        numeric: Optional[bool] = None,
        tooltip: Optional[str] = None,
        on_sort=None,
    ):
        Control.__init__(self, ref=ref)

        self.label = label
        self.numeric = numeric
        self.tooltip = tooltip
        self.on_sort = on_sort

    def _get_control_name(self):
        return "c"

    def _get_children(self):
        children = []
        if self.__label:
            self.__label._set_attr_internal("n", "label")
            children.append(self.__label)
        return children

    # label
    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    # numeric
    @property
    def numeric(self) -> Optional[bool]:
        return self._get_attr("numeric", data_type="bool", def_value=False)

    @numeric.setter
    @beartype
    def numeric(self, value: Optional[bool]):
        self._set_attr("numeric", value)

    # tooltip
    @property
    def tooltip(self):
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value):
        self._set_attr("tooltip", value)

    # on_sort
    @property
    def on_sort(self):
        return self._get_event_handler("sort")

    @on_sort.setter
    def on_sort(self, handler):
        self._add_event_handler("sort", handler)


class Item(Control):
    def __init__(self, obj):
        Control.__init__(self)
        assert obj, "obj cannot be empty"
        self.obj = obj

    def _set_attr(self, name, value, dirty=True):

        if value is None:
            return

        orig_val = self._get_attr(name)
        if orig_val is not None:
            if isinstance(orig_val, bool):
                value = str(value).lower() == "true"
            elif isinstance(orig_val, float):
                value = float(str(value))

        self._set_attr_internal(name, value, dirty=False)
        if isinstance(self.obj, dict):
            self.obj[name] = value
        else:
            setattr(self.obj, name, value)

    def _fetch_attrs(self):
        # reflection
        obj = self.obj if isinstance(self.obj, dict) else vars(self.obj)

        for name, val in obj.items():
            data_type = (
                type(val).__name__ if isinstance(val, (bool, float)) else "string"
            )
            orig_val = self._get_attr(name, data_type=data_type)

            if val != orig_val:
                self._set_attr_internal(name, val, dirty=True)

    def _get_control_name(self):
        return "item"
