from dataclasses import field
from typing import Optional

import flet as ft
from flet_fluent_ui.types import CommandBarOverflowBehavior

__all__ = ["CommandBar", "CommandBarButton", "CommandBarSeparator"]


@ft.control("FluentCommandBarButton")
class CommandBarButton(ft.Control):
    """
    A command in a :class:`~flet_fluent_ui.CommandBar`: an icon with a label
    in the bar, or a menu item in its "More" menu.

    Example:
    ```python
    fluent.CommandBarButton(
        icon=fluent.FluentIcons.ADD, content="New", on_click=new_item
    )
    ```
    """

    content: Optional[ft.StrOrControl] = None
    """
    The label of this command.

    A compact bar shows it only when there is no :attr:`icon`.
    """

    icon: Optional[ft.IconDataOrControl] = None
    """
    The icon of this command.
    """

    tooltip: Optional[str] = None
    """
    Text shown when the mouse pointer rests on this command.

    In the "More" menu, it is also shown at the end of the item.
    """

    on_click: Optional[ft.ControlEventHandler["CommandBarButton"]] = None
    """
    Called when this command is clicked.
    """


@ft.control("FluentCommandBarSeparator")
class CommandBarSeparator(ft.Control):
    """
    A vertical line between groups of commands in a
    :class:`~flet_fluent_ui.CommandBar`.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the line.

    Use :attr:`flet.Colors.TRANSPARENT` for an empty gap.
    """

    thickness: Optional[ft.Number] = None
    """
    The width of the line.
    """


@ft.control("FluentCommandBar")
class CommandBar(ft.LayoutControl):
    """
    A Fluent command bar: a toolbar of commands, with a "More" menu for
    commands that are used less often or don't fit.

    Example:
    ```python
    fluent.CommandBar(
        primary_items=[
            fluent.CommandBarButton(icon=fluent.FluentIcons.ADD, content="New"),
            fluent.CommandBarButton(
                icon=fluent.FluentIcons.DELETE, content="Delete"
            ),
            fluent.CommandBarSeparator(),
            fluent.CommandBarButton(icon=fluent.FluentIcons.SHARE, content="Share"),
        ],
        secondary_items=[
            fluent.CommandBarButton(
                icon=fluent.FluentIcons.SETTINGS, content="Settings"
            ),
        ],
    )
    ```
    """

    primary_items: list[ft.Control] = field(default_factory=list)
    """
    The commands shown in the bar: :class:`~flet_fluent_ui.CommandBarButton`
    and :class:`~flet_fluent_ui.CommandBarSeparator` controls.

    Other controls, such as a search box, are shown as they are.
    """

    secondary_items: list[ft.Control] = field(default_factory=list)
    """
    The commands shown in the "More" menu, which opens from a "..." button at
    the end of the bar.
    """

    overflow_behavior: CommandBarOverflowBehavior = (
        CommandBarOverflowBehavior.DYNAMIC_OVERFLOW
    )
    """
    What happens when :attr:`primary_items` don't fit in the bar.
    """

    compact: bool = False
    """
    Whether the bar shows only the icons of commands that have one.
    """

    alignment: ft.MainAxisAlignment = ft.MainAxisAlignment.START
    """
    How the commands are placed along the bar.
    """

    card: bool = False
    """
    Whether the bar is shown on a card: a rounded background with a border.
    """
