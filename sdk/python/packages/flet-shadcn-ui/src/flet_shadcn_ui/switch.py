from typing import Optional

import flet as ft

__all__ = ["Switch"]


@ft.control("ShadSwitch")
class Switch(ft.LayoutControl):
    """
    A shadcn/ui switch.

    Example:
    ```python
    shad.Switch(label="Airplane mode")
    ```
    """

    value: bool = False
    """
    Whether this switch is on.
    """

    label: Optional[ft.StrOrControl] = None
    """
    The label shown next to this switch.
    """

    sublabel: Optional[ft.StrOrControl] = None
    """
    Secondary text shown below :attr:`label`.
    """

    thumb_color: Optional[ft.ColorValue] = None
    """
    The color of the thumb.

    If `None`, the background color of the theme is used.
    """

    track_color: Optional[ft.ColorValue] = None
    """
    The color of the track when this switch is on.

    If `None`, the primary color of the theme is used.
    """

    inactive_track_color: Optional[ft.ColorValue] = None
    """
    The color of the track when this switch is off.

    If `None`, the input color of the theme is used.
    """

    on_change: Optional[ft.ControlEventHandler["Switch"]] = None
    """
    Called when :attr:`value` changes.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new value.
    """
