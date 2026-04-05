from typing import Optional

import flet as ft

__all__ = ["DataRow2"]


@ft.control("DataRow2")
class DataRow2(ft.DataRow):
    """
    Extends :class:`flet.DataRow`, adding row-level `tap` events.

    There are also :attr:`on_secondary_tap` and :attr:`on_secondary_tap_down`,
    which are not available in :class:`~flet.DataCell`s and can be useful in
    desktop settings to handle right-click actions.
    """

    decoration: Optional[ft.BoxDecoration] = None
    """
    Decoration to be applied to this row.

    Note:
        If provided,
        :attr:`flet.DataTable.divider_thickness`
        has no effect.
    """

    specific_row_height: Optional[ft.Number] = None
    """
    Specific row height.

    Falls back to :attr:`flet_datatable2.DataTable2.data_row_height` if not set.
    """

    on_double_tap: Optional[ft.ControlEventHandler["DataRow2"]] = None
    """
    Fires when the row is double-tapped.

    Note:
        Won't be called if tapped cell has any tap event handlers
        (:attr:`~flet.DataCell.on_tap`,
        :attr:`~flet.DataCell.on_double_tap`,
        :attr:`~flet.DataCell.on_long_press`,
        :attr:`~flet.DataCell.on_tap_cancel`,
        :attr:`~flet.DataCell.on_tap_down`) set.
    """

    on_secondary_tap: Optional[ft.ControlEventHandler["DataRow2"]] = None
    """
    Fires when the row is right-clicked (secondary tap).

    Note:
        Won't be called if tapped cell has any tap event handlers
        (:attr:`~flet.DataCell.on_tap`,
        :attr:`~flet.DataCell.on_double_tap`,
        :attr:`~flet.DataCell.on_long_press`,
        :attr:`~flet.DataCell.on_tap_cancel`,
        :attr:`~flet.DataCell.on_tap_down`) set.
    """

    on_secondary_tap_down: Optional[ft.ControlEventHandler["DataRow2"]] = None
    """
    Fires when the row is right-clicked (secondary tap down).

    Note:
        Won't be called if tapped cell has any tap event handlers
        (:attr:`~flet.DataCell.on_tap`,
        :attr:`~flet.DataCell.on_double_tap`,
        :attr:`~flet.DataCell.on_long_press`,
        :attr:`~flet.DataCell.on_tap_cancel`,
        :attr:`~flet.DataCell.on_tap_down`) set.
    """

    on_tap: Optional[ft.EventHandler[ft.TapEvent["DataRow2"]]] = None
    """
    Fires when the row is tapped.

    Note:
        Won't be called if tapped cell has any tap event handlers
        (:attr:`~flet.DataCell.on_tap`,
        :attr:`~flet.DataCell.on_double_tap`,
        :attr:`~flet.DataCell.on_long_press`,
        :attr:`~flet.DataCell.on_tap_cancel`,
        :attr:`~flet.DataCell.on_tap_down`) set.
    """
