from dataclasses import dataclass, field
from typing import List, Optional

from flet.controls.border import Border, BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.control_event import ControlEvent
from flet.controls.control_state import OptionalControlStateValue
from flet.controls.core.gesture_detector import TapEvent
from flet.controls.gradients import Gradient
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MainAxisAlignment,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    OptionalNumber,
    StrOrControl,
)


@dataclass
class DataColumnSortEvent(ControlEvent):
    column_index: int = field(metadata={"data_field": "i"})
    ascending: bool = field(metadata={"data_field": "a"}, default=False)


@control("column")
class DataColumn(Control):
    """
    Column configuration for a `DataTable`.

    One column configuration must be provided for each column to display in the table.
    """

    label: StrOrControl
    """
    The column heading.

    Typically, this will be a `Text` control. It could also be an `Icon` (typically using size 18), or a `Row` with an icon and some text.
    """

    tooltip_text: Optional[str]
    """
    The column heading's tooltip.

    This is a longer description of the column heading, for cases where the heading might have been abbreviated to keep the column width to a reasonable size.
    """

    numeric: bool = False
    """
    Whether this column represents numeric data or not.

    The contents of cells of columns containing numeric data are right-aligned.
    """

    column_tooltip: Optional[str] = None
    # No reference documentation provided for `column_tooltip`.

    heading_row_alignment: Optional[MainAxisAlignment] = None
    """
    Defines the horizontal layout of the label and sort indicator in the heading row.

    Value is of type [MainAxisAlignment](https://flet.dev/docs/reference/types/mainaxisalignment).
    """

    on_sort: OptionalEventCallable[DataColumnSortEvent] = None
    """
    Called when the user asks to sort the table using this column.

    If not set, the column will not be considered sortable.
    """

    # def before_update(self):
    #     super().before_update()
    #     assert self.label.visible, "label must be visible"


@control("cell")
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
        assert self.content.visible, "content must be visible"


@control("row")
class DataRow(Control):
    cells: List[DataCell] = field(default_factory=list)
    color: OptionalControlStateValue[ColorValue] = None
    selected: Optional[bool] = field(default=False)
    on_long_press: OptionalControlEventCallable = None
    on_select_changed: OptionalControlEventCallable = None

    def __contains__(self, item):
        return item in self.cells

    def before_update(self):
        super().before_update()
        assert any(
            cell.visible for cell in self.cells
        ), "cells must contain at minimum one visible DataCell"
        assert all(
            isinstance(cell, DataCell) for cell in self.cells
        ), "cells must contain only DataCell instances"  # todo: is this needed?


@control("DataTable")
class DataTable(ConstrainedControl):
    """
    A Material Design data table.
    """

    columns: List[DataColumn] = field(default_factory=list)
    """
    A list of [DataColumn](https://flet.dev/docs/controls/datatable#datacolumn) controls describing table columns.
    """

    rows: List[DataRow] = field(default_factory=list)
    """
    A list of [DataRow](https://flet.dev/docs/controls/datatable#datarow) controls defining table rows.
    """

    sort_ascending: bool = False
    """
    Whether the column mentioned in `sort_column_index`, if any, is sorted in ascending order.

    If `True`, the order is ascending (meaning the rows with the smallest values for the current sort column are first in the table).

    If `False`, the order is descending (meaning the rows with the smallest values for the current sort column are last in the table).
    """

    show_checkbox_column: bool = False
    """
    Whether the control should display checkboxes for selectable rows.

    If `True`, a `Checkbox` will be placed at the beginning of each row that is selectable. However, if `DataRow.on_select_changed` is not set for any row, checkboxes will not be placed, even if this value is `True`.

    If `False`, all rows will not display a `Checkbox`.
    """

    sort_column_index: Optional[int] = None
    """
    The current primary sort key's column.

    If specified, indicates that the indicated column is the column by which the data is sorted. The number must correspond to the index of the relevant column in `columns`.

    Setting this will cause the relevant column to have a sort indicator displayed.

    When this is `None`, it implies that the table's sort order does not correspond to any of the columns.
    """

    show_bottom_border: bool = False
    """
    Whether a border at the bottom of the table is displayed.

    By default, a border is not shown at the bottom to allow for a border around the table defined by decoration.
    """

    border: Optional[Border] = None
    """
    The border around the table. 

    The value is an instance of [Border](https://flet.dev/docs/reference/types/border) class.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Border corners.

    Border radius is an instance of [BorderRadius](https://flet.dev/docs/reference/types/borderradius) class.
    """

    horizontal_lines: Optional[BorderSide] = None
    """
    Set the [color](https://flet.dev/docs/reference/colors) and width of horizontal lines between rows. An instance of [BorderSide](https://flet.dev/docs/reference/types/borderside) class.
    """

    vertical_lines: Optional[BorderSide] = None
    """
    Set the [color](https://flet.dev/docs/reference/colors) and width of vertical lines between columns.

    Value is of type [BorderSide](https://flet.dev/docs/reference/types/borderside).
    """

    checkbox_horizontal_margin: OptionalNumber = None
    """
    Horizontal margin around the checkbox, if it is displayed.
    """

    column_spacing: OptionalNumber = None
    """
    The horizontal margin between the contents of each data column.
    """

    data_row_color: OptionalControlStateValue[ColorValue] = None
    """
    The background [color](https://flet.dev/docs/reference/colors) for the data rows.

    The effective background color can be made to depend on the [ControlState](https://flet.dev/docs/reference/types/controlstate) state, i.e. if the row is selected, pressed, hovered, focused, disabled or enabled. The color is painted as an overlay to the row. To make sure that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent background color.
    """

    data_row_min_height: OptionalNumber = None
    """
    The minimum height of each row (excluding the row that contains column headings).

    Defaults to `48.0` and must be less than or equal to `data_row_max_height`.
    """

    data_row_max_height: OptionalNumber = None
    """
    The maximum height of each row (excluding the row that contains column headings). Set to `float("inf")` for the height of each row to adjust automatically with its content.

    Defaults to `48.0` and must be greater than or equal to `data_row_min_height`.
    """

    data_text_style: Optional[TextStyle] = None
    """
    The text style for data rows. An instance of [TextStyle](https://flet.dev/docs/reference/types/textstyle) class.
    """

    bgcolor: OptionalColorValue = None
    """
    The background [color](https://flet.dev/docs/reference/colors) for the table.
    """

    gradient: Optional[Gradient] = None
    """
    The background gradient for the table.

    Value is of type [Gradient](https://flet.dev/docs/reference/types/gradient).
    """

    divider_thickness: Number = 1.0
    """
    The width of the divider that appears between `TableRow`s. Must be greater than or equal to zero.

    Defaults to 1.0.
    """

    heading_row_color: OptionalControlStateValue[ColorValue] = None
    """
    The background [color](https://flet.dev/docs/reference/colors) for the heading row.

    The effective background color can be made to depend on the [ControlState](https://flet.dev/docs/reference/types/controlstate) state, i.e. if the row is pressed, hovered, focused when sorted. The color is painted as an overlay to the row. To make sure that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent color.
    """

    heading_row_height: OptionalNumber = None
    """
    The height of the heading row.
    """

    heading_text_style: Optional[TextStyle] = None
    """
    The text style for the heading row. An instance of [TextStyle](https://flet.dev/docs/reference/types/textstyle) class.
    """

    horizontal_margin: OptionalNumber = None
    """
    The horizontal margin between the edges of the table and the content in the first and last cells of each row.

    When a checkbox is displayed, it is also the margin between the checkbox the content in the first data column.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    The content will be clipped (or not) according to this option. 

    Value is of type [ClipBehavior](https://flet.dev/docs/reference/types/clipbehavior) and defaults to `ClipBehavior.ANTI_ALIAS` if `border_radius!=None`; otherwise `ClipBehavior.HARD_EDGE`.
    """

    on_select_all: OptionalControlEventCallable = None
    """
    Invoked when the user selects or unselects every row, using the checkbox in the heading row.

    If this is `None`, then the `DataRow.on_select_changed` callback of every row in the table is invoked appropriately instead.

    To control whether a particular row is selectable or not, see `DataRow.on_select_changed`. This callback is only relevant if any row is selectable.
    """

    def __contains__(self, item):
        return item in self.columns or item in self.rows

    def before_update(self):
        super().before_update()
        visible_columns = list(filter(lambda column: column.visible, self.columns))
        visible_rows = list(filter(lambda row: row.visible, self.rows))
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
            isinstance(column, DataColumn) for column in self.columns
        ), "columns must contain only DataColumn instances"
        assert all(
            isinstance(row, DataRow) for row in self.rows
        ), "rows must contain only DataRow instances"  # todo: is this needed?
