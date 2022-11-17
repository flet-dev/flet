import json
from typing import Optional, Union

from beartype import beartype
from beartype.typing import Dict, List

from flet.buttons import MaterialState
from flet.control import Control
from flet.control_event import ControlEvent
from flet.event_handler import EventHandler
from flet.gesture_detector import TapEvent
from flet.ref import Ref


class DataColumnSortEvent(ControlEvent):
    def __init__(self, i, a) -> None:
        self.column_index: int = i
        self.ascending: bool = a


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

        self.__on_sort = EventHandler(
            lambda e: DataColumnSortEvent(**json.loads(e.data))
        )
        self._add_event_handler("sort", self.__on_sort.handler)

        self.label = label
        self.numeric = numeric
        self.tooltip = tooltip
        self.on_sort = on_sort

    def _get_control_name(self):
        return "c"

    def _get_children(self):
        children = []
        if self.__label:
            self.__label._set_attr_internal("n", "l")
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
        return self.__on_sort

    @on_sort.setter
    def on_sort(self, handler):
        self.__on_sort.subscribe(handler)
        self._set_attr("onSort", True if handler is not None else None)


class DataCell(Control):
    def __init__(
        self,
        content: Control,
        ref=None,
        on_double_tap=None,
        on_long_press=None,
        on_tap=None,
        on_tap_cancel=None,
        on_tap_down=None,
        placeholder: Optional[bool] = None,
        show_edit_icon: Optional[bool] = None,
    ):
        Control.__init__(self, ref=ref)

        self.__on_tap_down = EventHandler(lambda e: TapEvent(**json.loads(e.data)))
        self._add_event_handler("tap_down", self.__on_tap_down.handler)

        self.content = content
        self.on_double_tap = on_double_tap
        self.on_long_press = on_long_press
        self.on_tap = on_tap
        self.on_tap_cancel = on_tap_cancel
        self.on_tap_down = on_tap_down
        self.placeholder = placeholder
        self.show_edit_icon = show_edit_icon

    def _get_control_name(self):
        return "c"

    def _get_children(self):
        return [self.__content]

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # placeholder
    @property
    def placeholder(self) -> Optional[bool]:
        return self._get_attr("placeholder", data_type="bool", def_value=False)

    @placeholder.setter
    @beartype
    def placeholder(self, value: Optional[bool]):
        self._set_attr("placeholder", value)

    # show_edit_icon
    @property
    def show_edit_icon(self) -> Optional[bool]:
        return self._get_attr("showEditIcon", data_type="bool", def_value=False)

    @show_edit_icon.setter
    @beartype
    def show_edit_icon(self, value: Optional[bool]):
        self._set_attr("showEditIcon", value)

    # on_double_tap
    @property
    def on_double_tap(self):
        return self._get_event_handler("double_tap")

    @on_double_tap.setter
    def on_double_tap(self, handler):
        self._add_event_handler("double_tap", handler)
        self._set_attr("onDoubleTap", True if handler is not None else None)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_tap
    @property
    def on_tap(self):
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler):
        self._add_event_handler("tap", handler)
        self._set_attr("onTap", True if handler is not None else None)

    # on_tap_cancel
    @property
    def on_tap_cancel(self):
        return self._get_event_handler("tap_cancel")

    @on_tap_cancel.setter
    def on_tap_cancel(self, handler):
        self._add_event_handler("tap_cancel", handler)
        self._set_attr("onTapCancel", True if handler is not None else None)

    # on_tap_down
    @property
    def on_tap_down(self):
        return self.__on_tap_down

    @on_tap_down.setter
    def on_tap_down(self, handler):
        self.__on_tap_down.subscribe(handler)
        self._set_attr("onTapDown", True if handler is not None else None)


class DataRow(Control):
    def __init__(
        self,
        cells: Optional[List[Control]] = None,
        ref=None,
        color: Union[None, str, Dict[MaterialState, str]] = None,
        selected: Optional[bool] = None,
        on_long_press=None,
        on_select_changed=None,
    ):
        Control.__init__(self, ref=ref)

        self.cells = cells
        self.selected = selected
        self.on_long_press = on_long_press
        self.on_select_changed = on_select_changed

    def _get_control_name(self):
        return "r"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("color", self._wrap_attr_dict(self.__color))

    def _get_children(self):
        return self.__cells

    # cells
    @property
    def cells(self):
        return self.__cells

    @cells.setter
    def cells(self, value):
        self.__cells = value if value is not None else []

    # color
    @property
    def color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__color

    @color.setter
    @beartype
    def color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__color = value

    # selected
    @property
    def selected(self) -> Optional[bool]:
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    @beartype
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_select_changed
    @property
    def on_select_changed(self):
        return self._get_event_handler("select_changed")

    @on_select_changed.setter
    def on_select_changed(self, handler):
        self._add_event_handler("select_changed", handler)
        self._set_attr("onSelectChanged", True if handler is not None else None)


class DataTable(Control):
    def __init__(
        self,
        columns: Optional[List[DataColumn]] = None,
        rows: Optional[List[DataRow]] = None,
        ref=None,
        show_bottom_border: Optional[bool] = None,
        on_select_all=None,
    ):
        Control.__init__(self, ref=ref)

        self.columns = columns
        self.rows = rows
        self.show_bottom_border = show_bottom_border
        self.on_select_all = on_select_all

    def _get_control_name(self):
        return "datatable"

    def _get_children(self):
        children = []
        children.extend(self.__columns)
        children.extend(self.__rows)
        return children

    # columns
    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, value: Optional[List[DataColumn]]):
        self.__columns = value if value is not None else []

    # rows
    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, value: Optional[List[DataRow]]):
        self.__rows = value if value is not None else []

    # show_bottom_border
    @property
    def show_bottom_border(self) -> Optional[bool]:
        return self._get_attr("showBottomBorder", data_type="bool", def_value=False)

    @show_bottom_border.setter
    @beartype
    def show_bottom_border(self, value: Optional[bool]):
        self._set_attr("showBottomBorder", value)

    # on_select_all
    @property
    def on_select_all(self):
        return self._get_event_handler("select_all")

    @on_select_all.setter
    def on_select_all(self, handler):
        self._add_event_handler("select_all", handler)
        self._set_attr("onSelectAll", True if handler is not None else None)


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
