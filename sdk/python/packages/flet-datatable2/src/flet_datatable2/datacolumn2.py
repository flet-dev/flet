from enum import Enum
from typing import Optional

import flet as ft

__all__ = ["DataColumn2", "DataColumnSize"]


class DataColumnSize(Enum):
    """
    Relative size of a column determines the share of total table
    width allocated to each individual column.

    When determining column widths, ratios between `S`, `M` and `L`
    columns are kept (i.e. Large columns are set to 1.2x width of Medium ones).

    See [`DataTable2.sm_ratio`][(p).], [`DataTable2.lm_ratio`][(p).].
    """

    S = "s"
    M = "m"
    L = "l"


@ft.control("DataColumn2")
class DataColumn2(ft.DataColumn):
    """
    Extends [`flet.DataColumn`][flet.DataColumn],
    adding the ability to set relative column size and fixed column width.

    Meant to be used as an item of [`DataTable2.columns`][(p).].
    """

    fixed_width: Optional[ft.Number] = None
    """
    Defines absolute width of the column in pixels
    (as opposed to relative [`size`][(c).] used by default).
    """

    size: Optional[DataColumnSize] = DataColumnSize.S
    """
    Column sizes are determined based on available width by distributing
    it to individual columns accounting for their relative sizes.
    """
