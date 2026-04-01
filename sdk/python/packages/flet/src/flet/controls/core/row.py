from dataclasses import field

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.scrollable_control import ScrollableControl
from flet.controls.types import CrossAxisAlignment, MainAxisAlignment, Number

__all__ = ["Row"]


@control("Row")
class Row(LayoutControl, ScrollableControl, AdaptiveControl):
    """
    Displays its children in a horizontal array.

    To cause a child control to expand and fill the available horizontal space, set
    its :attr:`~flet.Control.expand` property.

    Example:
    ```python
        ft.Row(
            controls=[
                ft.Card(
                    shape=ft.ContinuousRectangleBorder(radius=10),
                    content=ft.Container(
                        padding=5,
                        border_radius=ft.BorderRadius.all(5),
                        bgcolor=ft.Colors.AMBER_100,
                        content=ft.Text(f"Control {i}"),
                    ),
                )
                for i in range(1, 6)
            ],
        )
    ```
    """

    controls: list[Control] = field(default_factory=list)
    """
    A list of Controls to display.
    """

    alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    Defines how the child :attr:`controls` should be placed horizontally.
    """

    vertical_alignment: CrossAxisAlignment = CrossAxisAlignment.CENTER
    """
    Defines how the child :attr:`controls` should be placed vertically.

    Note:
        When :attr:`wrap` is `True`, this property doesn't support
        :attr:`flet.CrossAxisAlignment.STRETCH` or
        :attr:`flet.CrossAxisAlignment.BASELINE`. If either is used,
        :attr:`flet.CrossAxisAlignment.CENTER` will be applied instead.
    """

    spacing: Number = 10
    """
    The spacing between the child :attr:`controls`.

    Note:
        Has effect only when :attr:`alignment` is set to
        :attr:`flet.MainAxisAlignment.START`, :attr:`flet.MainAxisAlignment.END`,
        or :attr:`flet.MainAxisAlignment.CENTER`.
    """

    tight: bool = False
    """
    Whether this row should occupy all available horizontal space (`True`), or only as \
    much as needed by its children :attr:`controls` (`False`).

    Note:
        Has effect only when :attr:`wrap` is `False`.
    """

    wrap: bool = False
    """
    Whether this row should put child :attr:`controls` into additional rows (runs) if \
    they don't fit in a single row.
    """

    run_spacing: Number = 10
    """
    The spacing between runs when :attr:`wrap` is `True`.
    """

    run_alignment: MainAxisAlignment = MainAxisAlignment.START
    """
    How the runs should be placed in the cross-axis when :attr:`wrap` is `True`.
    """

    intrinsic_height: bool = False
    """
    Whether this row should be as tall as the tallest child control in \
    :attr:`controls`.
    """

    def init(self):
        super().init()
        self._internals["host_expanded"] = True
