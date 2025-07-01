::: flet.DataTable

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/datatable)

### A simple DataTable

<img src="/img/docs/controls/datatable/datatable-minimal.png" className="screenshot-50"/>

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("First name")),
                ft.DataColumn(ft.Text("Last name")),
                ft.DataColumn(ft.Text("Age"), numeric=True),
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("John")),
                        ft.DataCell(ft.Text("Smith")),
                        ft.DataCell(ft.Text("43")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Jack")),
                        ft.DataCell(ft.Text("Brown")),
                        ft.DataCell(ft.Text("19")),
                    ],
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("Alice")),
                        ft.DataCell(ft.Text("Wong")),
                        ft.DataCell(ft.Text("25")),
                    ],
                ),
            ],
        ),
    )

ft.run(main)
```

### A styled DataTable

<img src="/img/docs/controls/datatable/datatable-styled.png" className="screenshot-70"/>

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DataTable(
            width=700,
            bgcolor="yellow",
            border=ft.border.all(2, "red"),
            border_radius=10,
            vertical_lines=ft.BorderSide(3, "blue"),
            horizontal_lines=ft.BorderSide(1, "green"),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.BLACK12,
            heading_row_height=100,
            data_row_color={ft.ControlState.HOVERED: "0x30FF0000"},
            show_checkbox_column=True,
            divider_thickness=0,
            column_spacing=200,
            columns=[
                ft.DataColumn(
                    ft.Text("Column 1"),
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
                ft.DataColumn(
                    ft.Text("Column 2"),
                    tooltip="This is a second column",
                    numeric=True,
                    on_sort=lambda e: print(f"{e.column_index}, {e.ascending}"),
                ),
            ],
            rows=[
                ft.DataRow(
                    [ft.DataCell(ft.Text("A")), ft.DataCell(ft.Text("1"))],
                    selected=True,
                    on_select_changed=lambda e: print(f"row select changed: {e.data}"),
                ),
                ft.DataRow([ft.DataCell(ft.Text("B")), ft.DataCell(ft.Text("2"))]),
            ],
        ),
    )

ft.run(main)
```


## `DataTable` properties

### `bgcolor`

The background [color](/docs/reference/colors) for the table.

### `border`

The border around the table. 

The value is an instance of [`Border`](/docs/reference/types/border) class.

### `border_radius`

Border corners.

Border radius is an instance of [`BorderRadius`](/docs/reference/types/borderradius) class.

### `checkbox_horizontal_margin`

Horizontal margin around the checkbox, if it is displayed.

### `clip_behavior`

The content will be clipped (or not) according to this option. 

Value is of type [`ClipBehavior`](/docs/reference/types/clipbehavior) and defaults to `ClipBehavior.ANTI_ALIAS`
if `border_radius!=None`; otherwise `ClipBehavior.HARD_EDGE`.

### `column_spacing`

The horizontal margin between the contents of each data column.

### `columns`

A list of [`DataColumn`](#datacolumn) controls describing table columns.

### `data_row_color`

The background [color](/docs/reference/colors) for the data rows.

The effective background color can be made to depend on the [`ControlState`](/docs/reference/types/controlstate) state,
i.e. if the row is selected, pressed, hovered, focused, disabled or enabled. The color is painted as an overlay to the
row. To make sure that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a
translucent background color.

### `data_row_min_height`

The minimum height of each row (excluding the row that contains column headings).

Defaults to `48.0` and must be less than or equal to `data_row_max_height`.

### `data_row_max_height`

The maximum height of each row (excluding the row that contains column headings). Set to `float("inf")` for the height
of each row to adjust automatically with its content.

Defaults to `48.0` and must be greater than or equal to `data_row_min_height`.

### `data_text_style`

The text style for data rows. An instance of [`TextStyle`](/docs/reference/types/textstyle) class.

### `divider_thickness`

The width of the divider that appears between `TableRow`s. Must be greater than or equal to zero.

Defaults to 1.0.

### `gradient`

The background gradient for the table.

Value is of type [`Gradient`](/docs/reference/types/gradient).

### `heading_row_alignment`

The alignment of the heading row.

Value is of type [`MainAxisAlignment`](/docs/reference/types/mainaxisalignment).

### `heading_row_color`

The background [color](/docs/reference/colors) for the heading row.

The effective background color can be made to depend on the [`ControlState`](/docs/reference/types/controlstate) state,
i.e. if the row is pressed, hovered, focused when sorted. The color is painted as an overlay to the row. To make sure
that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent color.

### `heading_row_height`

The height of the heading row.

### `heading_text_style`

The text style for the heading row. An instance of [`TextStyle`](/docs/reference/types/textstyle) class.

### `horizontal_lines`

Set the [color](/docs/reference/colors) and width of horizontal lines between rows. An instance of [`BorderSide`](/docs/reference/types/borderside) class.

### `horizontal_margin`

The horizontal margin between the edges of the table and the content in the first and last cells of each row.

When a checkbox is displayed, it is also the margin between the checkbox the content in the first data column.

### `rows`

A list of [`DataRow`](#datarow) controls defining table rows.

### `show_bottom_border`

Whether a border at the bottom of the table is displayed.

By default, a border is not shown at the bottom to allow for a border around the table defined by decoration.

### `show_checkbox_column`

Whether the control should display checkboxes for selectable rows.

If `True`, a `Checkbox` will be placed at the beginning of each row that is selectable. However, if `DataRow.on_select_changed` is not set for any row, checkboxes will not be placed, even if this value is `True`.

If `False`, all rows will not display a `Checkbox`.

### `sort_ascending`

Whether the column mentioned in `sort_column_index`, if any, is sorted in ascending order.

If `True`, the order is ascending (meaning the rows with the smallest values for the current sort column are first in the table).

If `False`, the order is descending (meaning the rows with the smallest values for the current sort column are last in the table).

### `sort_column_index`

The current primary sort key's column.

If specified, indicates that the indicated column is the column by which the data is sorted. The number must correspond to the index of the relevant column in `columns`.

Setting this will cause the relevant column to have a sort indicator displayed.

When this is `None`, it implies that the table's sort order does not correspond to any of the columns.

### `vertical_lines`

Set the [color](/docs/reference/colors) and width of vertical lines between columns.

Value is of type [`BorderSide`](/docs/reference/types/borderside).

## `DataTable` events

### `on_select_all`

Invoked when the user selects or unselects every row, using the checkbox in the heading row.

If this is `None`, then the `DataRow.on_select_changed` callback of every row in the table is invoked appropriately instead.

To control whether a particular row is selectable or not, see `DataRow.on_select_changed`. This callback is only relevant if any row is selectable.

## `DataColumn`

Column configuration for a `DataTable`.

One column configuration must be provided for each column to display in the table.

### `label`

The column heading.

Typically, this will be a `Text` control. It could also be an `Icon` (typically using size 18), or a `Row` with an icon and some text.

### `numeric`

Whether this column represents numeric data or not.

The contents of cells of columns containing numeric data are right-aligned.

### `tooltip`

The column heading's tooltip.

This is a longer description of the column heading, for cases where the heading might have been abbreviated to keep the column width to a reasonable size.

## `DataColumn` events

### `on_sort`

Called when the user asks to sort the table using this column.

If not set, the column will not be considered sortable.

## `DataRow`

Row configuration and cell data for a DataTable.

One row configuration must be provided for each row to display in the table.

The data for this row of the table is provided in the `cells` property of the `DataRow` object.

### `cells`

The data for this row - a list of [`DataCell`](#datacell) controls.

There must be exactly as many cells as there are columns in the table.

### `color`

The [color](/docs/reference/colors) for the row.

By default, the color is transparent unless selected. Selected rows has a grey translucent color.

The effective color can depend on the [`ControlState`](/docs/reference/types/controlstate) state, if the row is
selected, pressed, hovered, focused, disabled or enabled. The color is painted as an overlay to the row. To make sure
that the row's InkWell is visible (when pressed, hovered and focused), it is recommended to use a translucent color.

### `selected`

Whether the row is selected.

If `on_select_changed` is non-null for any row in the table, then a checkbox is shown at the start of each row. If the row is selected (`True`), the checkbox will be checked and the row will be highlighted.

Otherwise, the checkbox, if present, will not be checked.

## `DataRow` events

### `on_long_press`

Called if the row is long-pressed.

If a `DataCell` in the row has its `DataCell.on_tap`, `DataCell.on_double_tap`, `DataCell.on_long_press`, `DataCell.on_tap_cancel` or `DataCell.on_tap_down` callback defined, that callback behavior overrides the gesture behavior of the row for that particular cell.

### `on_select_changed`

Called when the user selects or unselects a selectable row.

If this is not null, then the row is selectable. The current selection state of the row is given by selected.

If any row is selectable, then the table's heading row will have a checkbox that can be checked to select all selectable rows (and which is checked if all the rows are selected), and each subsequent row will have a checkbox to toggle just that row.

A row whose `on_select_changed` callback is null is ignored for the purposes of determining the state of the "all" checkbox, and its checkbox is disabled.

If a `DataCell` in the row has its `DataCell.on_tap` callback defined, that callback behavior overrides the gesture behavior of the row for that particular cell.

## `DataCell`

The data for a cell of a `DataTable`.

One list of DataCell objects must be provided for each `DataRow` in the `DataTable`.

### `content`

The data for the row.

Typically a `Text` control or a `Dropdown` control.

If the cell has no data, then a `Text` widget with placeholder text should be provided instead, and `placeholder` should be set to `True`.

This control can only have one child. To lay out multiple children, let this control's child be a widget such as `Row`, `Column`, or `Stack`, which have `controls` property, and then provide the children to that widget.

### `placeholder`

Whether the child is actually a placeholder.

If this is `True`, the default text style for the cell is changed to be appropriate for placeholder text.

### `show_edit_icon`

Whether to show an edit icon at the end of the cell.

This does not make the cell actually editable; the caller must implement editing behavior if desired (initiated from the `on_tap` callback).

If this is set, `on_tap` should also be set, otherwise tapping the icon will have no effect.

## `DataCell` events

### `on_double_tap`

Called when the cell is double tapped.

If specified, tapping the cell will call this callback, else (tapping the cell will attempt to select the row (
if `DataRow.on_select_changed` is provided).

### `on_long_press`

Called if the cell is long-pressed.

If specified, tapping the cell will invoke this callback, else tapping the cell will attempt to select the row (
if `DataRow.on_select_changed` is provided).

### `on_tap`

Called if the cell is tapped.

If specified, tapping the cell will call this callback, else tapping the cell will attempt to select the row (
if `DataRow.on_select_changed` is provided).

### `on_tap_cancel`

Called if the user cancels a tap was started on cell.

If specified, cancelling the tap gesture will invoke this callback, else tapping the cell will attempt to select the
row (if `DataRow.on_select_changed` is provided).

### `on_tap_down`

Called if the cell is tapped down.

If specified, tapping the cell will call this callback, else tapping the cell will attempt to select the row (
if `DataRow.on_select_changed` is provided).