from dataclasses import field
from typing import Annotated, Optional

import flet as ft
from flet.utils.validation import V, ValidationRules

__all__ = ["ResizablePanel", "ResizablePanelGroup"]


@ft.control("ShadResizablePanel")
class ResizablePanel(ft.Control):
    """
    One panel of a :class:`~flet_shadcn_ui.ResizablePanelGroup`.

    Sizes are fractions of the group's length along its axis, from `0` to `1`.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda p: p.min_size <= p.default_size <= p.max_size,
            message="default_size must be between min_size and max_size",
        ),
    )

    content: ft.Control
    """
    The control shown in this panel.
    """

    default_size: Annotated[
        ft.Number,
        V.between(0, 1),
    ]
    """
    The initial size of this panel.

    The default sizes of all panels in a group must add up to `1`.

    Raises:
        ValueError: If it is not between `0` and `1`, inclusive.
        ValueError: If it is not between :attr:`min_size` and
            :attr:`max_size`.
    """

    min_size: Annotated[
        ft.Number,
        V.between(0, 1),
        V.le_field("max_size"),
    ] = 0.0
    """
    The smallest size the user can shrink this panel to.

    Raises:
        ValueError: If it is not between `0` and `1`, inclusive.
        ValueError: If it is not less than or equal to :attr:`max_size`.
    """

    max_size: Annotated[
        ft.Number,
        V.between(0, 1),
        V.ge_field("min_size"),
    ] = 1.0
    """
    The largest size the user can grow this panel to.

    Raises:
        ValueError: If it is not between `0` and `1`, inclusive.
        ValueError: If it is not greater than or equal to :attr:`min_size`.
    """


@ft.control("ShadResizablePanelGroup")
class ResizablePanelGroup(ft.LayoutControl):
    """
    A Shadcn group of panels with draggable dividers between them.

    The group fills the space it is given, so give it a
    :attr:`~flet.LayoutControl.width` and :attr:`~flet.LayoutControl.height`,
    or let it :attr:`~flet.Control.expand`.

    Example:
    ```python
    shad.ResizablePanelGroup(
        width=500,
        height=200,
        panels=[
            shad.ResizablePanel(default_size=0.5, content=ft.Text("One")),
            shad.ResizablePanel(default_size=0.5, content=ft.Text("Two")),
        ],
    )
    ```
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda g: (
                not g.panels or abs(sum(p.default_size for p in g.panels) - 1) <= 0.01
            ),
            message="the default_size of all panels must add up to 1",
        ),
    )

    panels: list[ResizablePanel] = field(default_factory=list)
    """
    The panels, in order along the group's axis.

    Raises:
        ValueError: If the :attr:`~flet_shadcn_ui.ResizablePanel.default_size`
            of all panels does not add up to `1`.
    """

    vertical: bool = False
    """
    Whether the panels are stacked top to bottom instead of left to right.
    """

    show_handle: bool = False
    """
    Whether to show a grip on each divider.
    """

    divider_color: Optional[ft.ColorValue] = None
    """
    The color of the dividers.

    If `None`, the border color of the theme is used.
    """
