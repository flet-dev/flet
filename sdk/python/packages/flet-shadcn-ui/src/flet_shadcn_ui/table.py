from dataclasses import field
from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V, ValidationRules

__all__ = ["Table", "TableCell", "TableColumn", "TableRow"]


@ft.control("ShadTableCell")
class TableCell(ft.Control):
    """
    A cell of a :class:`~flet_shadcn_ui.TableRow`, or of the
    :attr:`~flet_shadcn_ui.Table.footer`.
    """

    content: ft.StrOrControl
    """
    The content of this cell.

    If a string is provided, it is wrapped in a :class:`~flet.Text` control.
    """

    alignment: Optional[ft.Alignment] = None
    """
    How :attr:`content` is aligned within the cell.

    If `None`, the column's :attr:`~flet_shadcn_ui.TableColumn.alignment` is
    used.
    """


@ft.control("ShadTableRow")
class TableRow(ft.Control):
    """
    A row of a :class:`~flet_shadcn_ui.Table`.
    """

    cells: list[TableCell] = field(default_factory=list)
    """
    The cells of this row, one per column.
    """


@ft.control("ShadTableColumn")
class TableColumn(ft.Control):
    """
    A column of a :class:`~flet_shadcn_ui.Table`: its header and width.
    """

    header: Optional[ft.StrOrControl] = None
    """
    The content of this column's header cell.

    The table shows a header row if any column has a header.
    """

    width: Annotated[
        ft.Number,
        V.gt(0),
    ] = 100
    """
    The width of this column.

    When :attr:`fill` is `True`, the smallest width of this column.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    fill: bool = False
    """
    Whether this column takes the width left over by the fixed-width columns.
    Several filling columns share it equally. If there is not enough width
    left, the column keeps its :attr:`width` and the table scrolls
    horizontally.
    """

    alignment: Optional[ft.Alignment] = None
    """
    How the header and cells of this column are aligned.

    If `None`, they are aligned to the start and vertically centered.
    """


@ft.control("ShadTable")
class Table(ft.LayoutControl):
    """
    A Shadcn table with a header row, data rows and an optional footer.

    The table sizes itself to its content. When it is given less space, for
    example with :attr:`~flet.LayoutControl.height`, it scrolls.

    Example:
    ```python
    shad.Table(
        columns=[
            shad.TableColumn("Invoice"),
            shad.TableColumn("Status", fill=True),
            shad.TableColumn("Amount", alignment=ft.Alignment.CENTER_RIGHT),
        ],
        rows=[
            shad.TableRow(
                cells=[
                    shad.TableCell("INV001"),
                    shad.TableCell("Paid"),
                    shad.TableCell("$250.00"),
                ]
            ),
        ],
    )
    ```
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda t: (
                all(len(r.cells) == len(t.columns) for r in t.rows)
                and (not t.footer or len(t.footer) == len(t.columns))
            ),
            message="every row and the footer must have one cell per column",
        ),
    )

    columns: list[TableColumn] = field(default_factory=list)
    """
    The columns of this table.
    """

    rows: list[TableRow] = field(default_factory=list)
    """
    The data rows.

    Raises:
        ValueError: If a row or the :attr:`footer` does not have one cell per
            column.
    """

    footer: list[TableCell] = field(default_factory=list)
    """
    The cells of a footer row shown after the data rows, one per column.

    If empty, there is no footer.
    """

    row_height: Annotated[
        ft.Number,
        V.gt(0),
    ] = 48
    """
    The height of every row, including the header and footer.

    Raises:
        ValueError: If it is not strictly greater than `0`.
    """

    pinned_row_count: Annotated[
        int,
        V.ge(0),
    ] = 0
    """
    How many rows, counting the header, stay in place when the table scrolls
    vertically. Use `1` to keep the header visible.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
    """

    on_row_click: Optional[ft.ControlEventHandler["Table"]] = None
    """
    Called when a data row is clicked.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the index of the row in :attr:`rows`.
    """
