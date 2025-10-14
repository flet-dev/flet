from dataclasses import field
from typing import Optional, Union

import flet as ft
from flet_datatable2.datacolumn2 import DataColumn2
from flet_datatable2.datarow2 import DataRow2

__all__ = ["DataTable2"]


@ft.control("DataTable2")
class DataTable2(ft.DataTable):
    """
    Provides sticky header row, scrollable data rows,
    and additional layout flexibility with [`DataColumn2`][(p).]
    and [`DataRow2`][(p).].

    Note:
        `DataTable2` doesn't support
        [`DataTable.data_row_min_height`][flet.DataTable.data_row_min_height]
        and [`DataTable.data_row_max_height`][flet.DataTable.data_row_max_height]
        properties present in the parent [`DataTable`][flet.DataTable].
        Use [`data_row_height`][(c).] instead.
    """

    columns: list[Union[DataColumn2, ft.DataColumn]]
    """
    A list of table columns.
    """

    rows: list[Union[ft.DataRow, DataRow2]] = field(default_factory=list)
    """
    A list of table rows.
    """

    empty: Optional[ft.Control] = None
    """
    Placeholder control shown when there are no data rows.
    """

    bottom_margin: Optional[ft.Number] = None
    """
    Adds space after the last row if set.
    """

    lm_ratio: ft.Number = 1.2
    """
    Ratio of Large column width to Medium.
    """

    sm_ratio: ft.Number = 0.67
    """
    Ratio of Small column width to Medium.
    """

    fixed_left_columns: int = 0
    """
    Number of sticky columns on the left. Includes checkbox column, if present.
    """

    fixed_top_rows: int = 1
    """
    Number of sticky rows from the top. Includes heading row by default.
    """

    fixed_columns_color: Optional[ft.ColorValue] = None
    """
    Background color for sticky left columns.
    """

    fixed_corner_color: Optional[ft.ColorValue] = None
    """
    Background color of the fixed top-left corner cell.
    """

    sort_arrow_icon_color: Optional[ft.ColorValue] = None
    """
    When set always overrides/preceeds default arrow icon color.
    """

    min_width: Optional[ft.Number] = None
    """
    Minimum table width before horizontal scrolling kicks in.
    """

    show_heading_checkbox: bool = True
    """
    Controls visibility of the heading checkbox.
    """

    heading_checkbox_theme: Optional[ft.CheckboxTheme] = None
    """
    Overrides theme of the heading checkbox.
    """

    data_row_checkbox_theme: Optional[ft.CheckboxTheme] = None
    """
    Overrides theme of checkboxes in each data row.
    """

    sort_arrow_icon: ft.IconData = ft.Icons.ARROW_UPWARD
    """
    Icon shown when sorting is applied.
    """

    sort_arrow_animation_duration: ft.DurationValue = field(
        default_factory=lambda: ft.Duration(milliseconds=150)
    )
    """
    Duration of sort arrow animation.
    """

    visible_horizontal_scroll_bar: Optional[bool] = None
    """
    Determines visibility of the horizontal scrollbar.
    """

    visible_vertical_scroll_bar: Optional[bool] = None
    """
    Determines visibility of the vertical scrollbar.
    """

    checkbox_alignment: ft.Alignment = field(
        default_factory=lambda: ft.Alignment.CENTER
    )
    """
    Alignment of the checkbox.
    """

    data_row_height: Optional[ft.Number] = None
    """
    Height of each data row.
    """

    # present in parent (DataTable) but of no use in DataTable2
    data_row_min_height: None = field(
        init=False, repr=False, compare=False, metadata={"skip": True}
    )
    data_row_max_height: None = field(
        init=False, repr=False, compare=False, metadata={"skip": True}
    )
