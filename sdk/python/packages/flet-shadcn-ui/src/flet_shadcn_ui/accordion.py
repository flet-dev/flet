from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["Accordion", "AccordionItem"]


@ft.control("ShadAccordionItem")
class AccordionItem(ft.Control):
    """
    One collapsible section of an :class:`~flet_shadcn_ui.Accordion`.
    """

    value: str
    """
    The identifier of this item, used in :attr:`flet_shadcn_ui.Accordion.value`.
    """

    title: ft.StrOrControl
    """
    The header that the user clicks to expand or collapse this item.
    """

    content: ft.Control
    """
    The control shown when this item is expanded.
    """


@ft.control("ShadAccordion")
class Accordion(ft.LayoutControl):
    """
    A Shadcn accordion: a vertical list of sections that expand to show their
    content.

    Example:
    ```python
    shad.Accordion(
        items=[
            shad.AccordionItem(
                value="a11y",
                title="Is it accessible?",
                content=ft.Text("Yes. It adheres to the WAI-ARIA design pattern."),
            ),
        ]
    )
    ```
    """

    items: list[AccordionItem] = field(default_factory=list)
    """
    The sections of this accordion.
    """

    value: list[str] = field(default_factory=list)
    """
    The :attr:`~flet_shadcn_ui.AccordionItem.value` of each expanded item.

    Unless :attr:`multiple` is `True`, at most one item is expanded.
    """

    multiple: bool = False
    """
    Whether several items can be expanded at the same time.
    """

    on_change: Optional[ft.ControlEventHandler["Accordion"]] = None
    """
    Called when the user expands or collapses an item.

    The :attr:`~flet.Event.data` property of the event handler argument
    contains the new :attr:`value`.
    """
