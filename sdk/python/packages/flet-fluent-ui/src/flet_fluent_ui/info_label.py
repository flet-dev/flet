from typing import Optional

import flet as ft

__all__ = ["InfoLabel"]


@ft.control("FluentInfoLabel")
class InfoLabel(ft.LayoutControl):
    """
    A Fluent label for a field: a short text shown above (or after) another
    control, such as a :class:`~flet_fluent_ui.TextBox`.

    Example:
    ```python
    fluent.InfoLabel(
        label="Email",
        content=fluent.TextBox(placeholder="name@example.com"),
    )
    ```
    """

    label: str
    """
    The text of the label.
    """

    content: Optional[ft.Control] = None
    """
    The control the label is for.
    """

    horizontal: bool = False
    """
    Whether :attr:`label` is shown after :attr:`content`, on the same line,
    instead of above it. Use it for controls such as a
    :class:`~flet_fluent_ui.ToggleSwitch` without a label of their own.
    """
