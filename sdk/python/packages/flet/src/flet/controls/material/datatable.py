from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.border import Border, BorderSide
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import (
    Event,
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.control_state import ControlStateValue
from flet.controls.events import TapEvent
from flet.controls.gradients import Gradient
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    MainAxisAlignment,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
)


@dataclass
class DataColumnSortEvent(Event["DataColumn"]):
    column_index: int = field(metadata={"data_field": "ci"})
    ascending: bool = field(metadata={"data_field": "asc"})


@control("DataColumn")
class DataColumn(Control):
    """
    Column configuration for a `DataTable`.

    One column configuration must be provided for each column to display in the table.
    """

    label: StrOrControl
    """
    The column heading.

    Typically, this will be a `Text` control. It could also be an `Icon` (typically 
    using size 18), or a `Row` with an icon and some text.
    """

    tooltip_text: Optional[str] = None
    """
    The column heading's tooltip.

    This is a longer description of the column heading, for cases where the heading 
    might have been abbreviated to keep the column width to a reasonable size.
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

    Value is of type [`MainAxisAlignment`](https://flet.dev/docs/reference/types/mainaxisalignment).
    """

    on_sort: OptionalEventHandler[DataColumnSortEvent] = None
    """
    Called when the user asks to sort the table using this column.

    If not set, the column will not be considered sortable.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.label, str) or (
            isinstance(self.label, Control) and self.label.visible
        ), "label must be visible"


@control("DataCell")
class DataCell(Control):
    """
    The data for a cell of a `DataTable`.

    One list of DataCell objects must be provided for each `DataRow` in the `DataTable`.
    """

    content: StrOrControl
    """
    The data for the row.

    Typically a `Text` control or a `Dropdown` control.

    If the cell has no data, then a `Text` widget with placeholder text should be 
    provided instead, and `placeholder` should be set to `True`.

    This control can only have one child. To lay out multiple children, let this 
    control's child be a widget such as `Row`, `Column`, or `Stack`, which have 
    `controls` property, and then provide the children to that widget.
    """

    placeholder: bool = False
    """
    Whether the child is actually a placeholder.

    If this is `True`, the default text style for the cell is changed to be appropriate 
    for placeholder text.
    """

    show_edit_icon: bool = False
    """
    Whether to show an edit icon at the end of the cell.

    This does not make the cell actually editable; the caller must implement editing 
    behavior if desired (initiated from the `on_tap` callback).

    If this is set, `on_tap` should also be set, otherwise tapping the icon will have 
    no effect.
    """

    on_tap: OptionalControlEventHandler["DataCell"] = None
    """
    Called if the cell is tapped.

    If specified, tapping the cell will call this callback, else tapping the cell will 
    attempt to select the row (if `DataRow.on_select_changed` is provided).
    """

    on_double_tap: OptionalControlEventHandler["DataCell"] = None
    """
    Called when the cell is double tapped.

    If specified, tapping the cell will call this callback, else (tapping the cell will 
    attempt to select the row (if `DataRow.on_select_changed` is provided).
    """

    on_long_press: OptionalControlEventHandler["DataCell"] = None
    """
    Called if the cell is long-pressed.

    If specified, tapping the cell will invoke this callback, else tapping the cell 
    will attempt to select the row (if `DataRow.on_select_changed` is provided).
    """

    on_tap_cancel: OptionalControlEventHandler["DataCell"] = None
    """
    Called if the user cancels a tap was started on cell.

    If specified, cancelling the tap gesture will invoke this callback, else tapping 
    the cell will attempt to select the row (if `DataRow.on_select_changed` is 
    provided).
    """

    on_tap_down: OptionalEventHandler[TapEvent["DataCell"]] = None
    """
    Called if the cell is tapped down.

    If specified, tapping the cell will call this callback, else tapping the cell will 
    attempt to select the row (if `DataRow.on_select_changed` is provided).
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"


@control("DataRow")
class DataRow(Control):
    """
    Row configuration and cell data for a DataTable.

    One row configuration must be provided for each row to display in the table.

    The data for this row of the table is provided in the `cells` property of the
    `DataRow` object.
    """

    cells: list[DataCell] = field(default_factory=list)
    """
    The data for this row - a list of [`DataCell`](https://flet.dev/docs/reference/datacell) 
    controls.

    There must be exactly as many cells as there are columns in the table.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) for the row.

    By default, the color is transparent unless selected. Selected rows has a grey 
    translucent color.

    The effective color can depend on the [`ControlState`](https://flet.dev/docs/reference/types/controlstate) 
    state, if the row is selected, pressed, hovered, focused, disabled or enabled. The 
    color is painted as an overlay to the row. To make sure that the row's InkWell is 
    visible (when pressed, hovered and focused), it is recommended to use a translucent 
    color.
    """

    selected: bool = False
    """
    Whether the row is selected.

    If `on_select_changed` is non-null for any row in the table, then a checkbox is 
    shown at the start of each row. If the row is selected (`True`), the checkbox will 
    be checked and the row will be highlighted.

    Otherwise, the checkbox, if present, will not be checked.
    """

    on_long_press: OptionalControlEventHandler["DataRow"] = None
    """
    Called if the row is long-pressed.

    If a `DataCell` in the row has its `DataCell.on_tap`, `DataCell.on_double_tap`, 
    `DataCell.on_long_press`, `DataCell.on_tap_cancel` or `DataCell.on_tap_down` 
    callback defined, that callback behavior overrides the gesture behavior of the row 
    for that particular cell.
    """

    on_select_changed: OptionalControlEventHandler["DataRow"] = None
    """
    Called when the user selects or unselects a selectable row.

    If this is not null, then the row is selectable. The current selection state of the 
    row is given by selected.

    If any row is selectable, then the table's heading row will have a checkbox that 
    can be checked to select all selectable rows (and which is checked if all the rows 
    are selected), and each subsequent row will have a checkbox to toggle just that row.

    A row whose `on_select_changed` callback is null is ignored for the purposes of 
    determining the state of the "all" checkbox, and its checkbox is disabled.

    If a `DataCell` in the row has its `DataCell.on_tap` callback defined, that 
    callback behavior overrides the gesture behavior of the row for that particular 
    cell.
    """

    def __contains__(self, item):
        return item in self.cells

    def before_update(self):
        super().before_update()
        assert any(cell.visible for cell in self.cells), (
            "cells must contain at minimum one visible DataCell"
        )


@control("DataTable")
class DataTable(ConstrainedControl):
    """
    A Material Design data table.

    Online docs: https://flet.dev/docs/controls/datatable
    """

    columns: list[DataColumn]
    """
    A list of [DataColumn](https://flet.dev/docs/controls/datatable#datacolumn) 
    controls describing table columns.
    """

    rows: list[DataRow] = field(default_factory=list)
    """
    A list of [DataRow](https://flet.dev/docs/controls/datatable#datarow) controls 
    defining table rows.
    """

    sort_ascending: bool = False
    """
    Whether the column mentioned in `sort_column_index`, if any, is sorted in ascending 
    order.

    If `True`, the order is ascending (meaning the rows with the smallest values for 
    the current sort column are first in the table).

    If `False`, the order is descending (meaning the rows with the smallest values for 
    the current sort column are last in the table).
    """

    show_checkbox_column: bool = False
    """
    Whether the control should display checkboxes for selectable rows.

    If `True`, a `Checkbox` will be placed at the beginning of each row that is 
    selectable. However, if `DataRow.on_select_changed` is not set for any row, 
    checkboxes will not be placed, even if this value is `True`.

    If `False`, all rows will not display a `Checkbox`.
    """

    sort_column_index: Optional[int] = None
    """
    The current primary sort key's column.

    If specified, indicates that the indicated column is the column by which the data 
    is sorted. The number must correspond to the index of the relevant column in 
    `columns`.

    Setting this will cause the relevant column to have a sort indicator displayed.

    When this is `None`, it implies that the table's sort order does not correspond to 
    any of the columns.
    """

    show_bottom_border: bool = False
    """
    Whether a border at the bottom of the table is displayed.

    By default, a border is not shown at the bottom to allow for a border around the 
    table defined by decoration.
    """

    border: Optional[Border] = None
    """
    The border around the table. 

    The value is an instance of [Border](https://flet.dev/docs/reference/types/border) 
    class.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Border corners.

    Border radius is an instance of [BorderRadius](https://flet.dev/docs/reference/types/borderradius) 
    class.
    """

    horizontal_lines: Optional[BorderSide] = None
    """
    Set the [color](https://flet.dev/docs/reference/colors) and width of horizontal 
    lines between rows. An instance of [BorderSide](https://flet.dev/docs/reference/types/borderside) 
    class.
    """

    vertical_lines: Optional[BorderSide] = None
    """
    Set the [color](https://flet.dev/docs/reference/colors) and width of vertical lines 
    between columns.

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

    data_row_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The background [color](https://flet.dev/docs/reference/colors) for the data rows.

    The effective background color can be made to depend on the [ControlState](https://flet.dev/docs/reference/types/controlstate) 
    state, i.e. if the row is selected, pressed, hovered, focused, disabled or enabled. 
    The color is painted as an overlay to the row. To make sure that the row's InkWell 
    is visible (when pressed, hovered and focused), it is recommended to use a 
    translucent background color.
    """

    data_row_min_height: OptionalNumber = None
    """
    The minimum height of each row (excluding the row that contains column headings).

    Defaults to `48.0` and must be less than or equal to `data_row_max_height`.
    """

    data_row_max_height: OptionalNumber = None
    """
    The maximum height of each row (excluding the row that contains column headings). 
    Set to `float("inf")` for the height of each row to adjust automatically with its 
    content.

    Defaults to `48.0` and must be greater than or equal to `data_row_min_height`.
    """

    data_text_style: Optional[TextStyle] = None
    """
    The text style for data rows. An instance of [TextStyle](https://flet.dev/docs/reference/types/textstyle)
    class.
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
    The width of the divider that appears between `TableRow`s. Must be greater than or 
    equal to zero.

    Defaults to 1.0.
    """

    heading_row_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The background [color](https://flet.dev/docs/reference/colors) for the heading row.

    The effective background color can be made to depend on the [ControlState](https://flet.dev/docs/reference/types/controlstate) 
    state, i.e. if the row is pressed, hovered, focused when sorted. The color is 
    painted as an overlay to the row. To make sure that the row's InkWell is visible 
    (when pressed, hovered and focused), it is recommended to use a translucent color.
    """

    heading_row_height: OptionalNumber = None
    """
    The height of the heading row.
    """

    heading_text_style: Optional[TextStyle] = None
    """
    The text style for the heading row. An instance of [TextStyle](https://flet.dev/docs/reference/types/textstyle) 
    class.
    """

    horizontal_margin: OptionalNumber = None
    """
    The horizontal margin between the edges of the table and the content in the first 
    and last cells of each row.

    When a checkbox is displayed, it is also the margin between the checkbox the 
    content in the first data column.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option. 

    Value is of type [ClipBehavior](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.ANTI_ALIAS` if `border_radius!=None`; otherwise 
    `ClipBehavior.HARD_EDGE`.
    """

    on_select_all: OptionalControlEventHandler["DataTable"] = None
    """
    Invoked when the user selects or unselects every row, using the checkbox in the 
    heading row.

    If this is `None`, then the `DataRow.on_select_changed` callback of every row in 
    the table is invoked appropriately instead.

    To control whether a particular row is selectable or not, see 
    `DataRow.on_select_changed`. This callback is only relevant if any row is 
    selectable.
    """

    def __contains__(self, item):
        return item in self.columns or item in self.rows

    def before_update(self):
        super().before_update()
        visible_columns = list(filter(lambda column: column.visible, self.columns))
        visible_rows = list(filter(lambda row: row.visible, self.rows))
        assert len(visible_columns) > 0, (
            "columns must contain at minimum one visible DataColumn"
        )
        assert all(
            [
                len([c for c in row.cells if c.visible]) == len(visible_columns)
                for row in visible_rows
            ]
        ), (
            f"each visible DataRow must contain exactly as many visible DataCells as "
            f"there are visible DataColumns ({len(visible_columns)})"
        )
        assert (
            self.data_row_min_height is None
            or self.data_row_max_height is None
            or (self.data_row_min_height <= self.data_row_max_height)
        ), "data_row_min_height must be less than or equal to data_row_max_height"
        assert self.divider_thickness is None or self.divider_thickness >= 0, (
            "divider_thickness must be greater than or equal to 0"
        )
        assert self.sort_column_index is None or (
            0 <= self.sort_column_index < len(visible_columns)
        ), (
            f"sort_column_index must be greater than or equal to 0 and less than the "
            f"number of visible columns ({len(visible_columns)})"
        )
