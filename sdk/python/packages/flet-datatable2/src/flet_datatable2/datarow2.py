from typing import Optional

import flet as ft

__all__ = ["DataRow2"]


@ft.control("DataRow2")
class DataRow2(ft.DataRow):
    """
    Extends [`flet.DataRow`][flet.DataRow], adding row-level `tap` events.

    There are also [`on_secondary_tap`][(c).] and [`on_secondary_tap_down`][(c).],
    which are not available in [`DataCell`][flet.DataCell]s and can be useful in
    desktop settings to handle right-click actions.
    """

    decoration: Optional[ft.BoxDecoration] = None
    """
    Decoration to be applied to this row.

    Note:
        If provided, [`DataTable2.divider_thickness`][(p).] has no effect.
    """

    specific_row_height: Optional[ft.Number] = None
    """
    Specific row height.

    Falls back to [`DataTable2.data_row_height`][(p).] if not set.
    """

    on_double_tap: Optional[ft.ControlEventHandler["DataRow2"]] = None
    """
    Fires when the row is double-tapped.

    Note:
        Won't be called if tapped cell has any tap event handlers
        ([`on_tap`][flet.DataCell.on_tap],
        [`on_double_tap`][flet.DataCell.on_double_tap],
        [`on_long_press`][flet.DataCell.on_long_press],
        [`on_tap_cancel`][flet.DataCell.on_tap_cancel],
        [`on_tap_down`][flet.DataCell.on_tap_down]) set.
    """

    on_secondary_tap: Optional[ft.ControlEventHandler["DataRow2"]] = None
    """
    Fires when the row is right-clicked (secondary tap).

    Note:
        Won't be called if tapped cell has any tap event handlers
        ([`on_tap`][flet.DataCell.on_tap],
        [`on_double_tap`][flet.DataCell.on_double_tap],
        [`on_long_press`][flet.DataCell.on_long_press],
        [`on_tap_cancel`][flet.DataCell.on_tap_cancel],
        [`on_tap_down`][flet.DataCell.on_tap_down]) set.
    """

    on_secondary_tap_down: Optional[ft.ControlEventHandler["DataRow2"]] = None
    """
    Fires when the row is right-clicked (secondary tap down).

    Note:
        Won't be called if tapped cell has any tap event handlers
        ([`on_tap`][flet.DataCell.on_tap],
        [`on_double_tap`][flet.DataCell.on_double_tap],
        [`on_long_press`][flet.DataCell.on_long_press],
        [`on_tap_cancel`][flet.DataCell.on_tap_cancel],
        [`on_tap_down`][flet.DataCell.on_tap_down]) set.
    """

    on_tap: Optional[ft.EventHandler[ft.TapEvent["DataRow2"]]] = None
    """
    Fires when the row is tapped.

    Note:
        Won't be called if tapped cell has any tap event handlers
        ([`on_tap`][flet.DataCell.on_tap],
        [`on_double_tap`][flet.DataCell.on_double_tap],
        [`on_long_press`][flet.DataCell.on_long_press],
        [`on_tap_cancel`][flet.DataCell.on_tap_cancel],
        [`on_tap_down`][flet.DataCell.on_tap_down]) set.
    """
