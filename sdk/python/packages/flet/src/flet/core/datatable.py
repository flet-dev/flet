import json
from dataclasses import dataclass, field
from typing import Any, List, Optional, Union

from flet.core.animation import AnimationValue
from flet.core.badge import BadgeValue
from flet.core.border import Border, BorderSide
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, OptionalNumber, control
from flet.core.control_event import ControlEvent
from flet.core.event_handler import EventHandler
from flet.core.gesture_detector import TapEvent
from flet.core.gradients import Gradient
from flet.core.ref import Ref
from flet.core.text_style import TextStyle
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    BorderRadiusValue,
    ClipBehavior,
    ColorEnums,
    ColorValue,
    ControlStateValue,
    MainAxisAlignment,
    OffsetValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


@dataclass
class DataColumnSortEvent(ControlEvent):
    column_index: int = field(metadata={"data_field": "i"})
    ascending: bool = field(metadata={"data_field": "a"}, default=False)


@control("DataColumn")
class DataColumn(Control):
    label: Control
    numeric: Optional[bool] = field(default=False)
    tooltip: Optional[str] = None
    heading_row_alignment: Optional[MainAxisAlignment] = None
    on_sort: OptionalEventCallable[DataColumnSortEvent] = None

    def before_update(self):
        super().before_update()
        assert self.__label.visible, "label must be visible"


@control("DataCell")
class DataCell(Control):
    content: Control
    placeholder: Optional[bool] = field(default=False)
    show_edit_icon: Optional[bool] = field(default=False)
    on_tap: OptionalControlEventCallable = None
    on_double_tap: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_tap_cancel: OptionalControlEventCallable = None
    on_tap_down: OptionalEventCallable[TapEvent] = None

    def before_update(self):
        super().before_update()
        assert self.__content.visible, "content must be visible"


@control("DataRow")
class DataRow(Control):

    cells: List[DataCell]
    color: ControlStateValue[ColorValue] = None
    selected: Optional[bool] = field(default=False)
    on_long_press: OptionalControlEventCallable = None
    on_select_changed: OptionalControlEventCallable = None

    def __contains__(self, item):
        return item in self.__cells

    def before_update(self):
        super().before_update()
        assert any(
            cell.visible for cell in self.__cells
        ), "cells must contain at minimum one visible DataCell"
        assert all(
            isinstance(cell, DataCell) for cell in self.__cells
        ), "cells must contain only DataCell instances"


@control("DataTable")
class DataTable(ConstrainedControl):

    columns: List[DataColumn]
    rows: Optional[List[DataRow]] = None
    sort_ascending: Optional[bool] = field(default=False)
    show_checkbox_column: Optional[bool] = field(default=False)
    sort_column_index: Optional[int] = (None,)
    show_bottom_border: Optional[bool] = field(default=False)
    border: Optional[Border] = None
    border_radius: Optional[BorderRadiusValue] = None
    horizontal_lines: Optional[BorderSide] = None
    vertical_lines: Optional[BorderSide] = None
    checkbox_horizontal_margin: OptionalNumber = None
    column_spacing: OptionalNumber = None
    data_row_color: ControlStateValue[ColorValue] = None
    data_row_min_height: OptionalNumber = None
    data_row_max_height: OptionalNumber = None
    data_text_style: Optional[TextStyle] = None
    bgcolor: Optional[ColorValue] = None
    gradient: Optional[Gradient] = None
    divider_thickness: OptionalNumber = field(default=1.0)
    heading_row_color: ControlStateValue[ColorValue] = None
    heading_row_height: OptionalNumber = None
    heading_text_style: Optional[TextStyle] = None
    horizontal_margin: OptionalNumber = None
    clip_behavior: Optional[ClipBehavior] = None
    on_select_all: OptionalControlEventCallable = None

    def __contains__(self, item):
        return item in self.__columns or item in self.__rows

    def before_update(self):
        super().before_update()
        visible_columns = list(filter(lambda column: column.visible, self.__columns))
        visible_rows = list(filter(lambda row: row.visible, self.__rows))
        assert (
            len(visible_columns) > 0
        ), "columns must contain at minimum one visible DataColumn"
        assert all(
            len(list(filter(lambda c: c.visible, row.cells))) == len(visible_columns)
            for row in visible_rows
        ), f"each visible DataRow must contain exactly as many visible DataCells as there are visible DataColumns ({len(visible_columns)})"
        assert (
            self.data_row_min_height is None
            or self.data_row_max_height is None
            or (self.data_row_min_height <= self.data_row_max_height)
        ), "data_row_min_height must be less than or equal to data_row_max_height"
        assert (
            self.divider_thickness is None or self.divider_thickness >= 0
        ), "divider_thickness must be greater than or equal to 0"
        assert self.sort_column_index is None or (
            0 <= self.sort_column_index < len(visible_columns)
        ), f"sort_column_index must be greater than or equal to 0 and less than the number of columns ({len(visible_columns)})"
        assert all(
            isinstance(column, DataColumn) for column in self.__columns
        ), "columns must contain only DataColumn instances"
        assert all(
            isinstance(row, DataRow) for row in self.__rows
        ), "rows must contain only DataRow instances"
