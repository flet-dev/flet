from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.base_control import BaseControl
from flet.controls.material.badge import BadgeValue
from flet.controls.material.tooltip import TooltipValue
from flet.controls.types import Number, ResponsiveNumber

__all__ = ["Control", "OptionalControl"]


@dataclass(kw_only=True)
class Control(BaseControl):
    """
    TBD
    """

    expand: Optional[Union[bool, int]] = None
    """
    When a child Control is placed into a [`Column`](https://flet.dev/docs/controls/column) 
    or a [`Row`](https://flet.dev/docs/controls/row) you can "expand" it to fill the 
    available space. 
    `expand` property could be a boolean value (`True` - expand control to fill all 
    available space) or an integer - an "expand factor" specifying how to divide a free 
    space with other expanded child controls.

    For more information and examples about `expand` property see "Expanding children" 
    sections in [`Column`](https://flet.dev/docs/controls/column#expanding-children) or 
    [`Row`](https://flet.dev/docs/controls/row#expanding-children).

    Here is an example of expand being used in action for both [`Column`](https://flet.dev/docs/controls/column) 
    and [`Row`](https://flet.dev/docs/controls/row):

    ```python
    import flet as ft

    def main(page: ft.Page):
        page.spacing = 0
        page.padding = 0
        page.add(
            ft.Column(
                controls=[
                    ft.Row(
                        [
                            ft.Card(
                                content=ft.Text("Card_1"),
                                color=ft.Colors.ORANGE_300,
                                expand=True,
                                height=page.height,
                                margin=0,
                            ),
                            ft.Card(
                                content=ft.Text("Card_2"),
                                color=ft.Colors.GREEN_100,
                                expand=True,
                                height=page.height,
                                margin=0,
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                ],
                expand=True,
                spacing=0,
            ),
        )

    ft.app(main)
    ```
    """

    expand_loose: Optional[bool] = None
    """
    Effective only if `expand` is `True`. 

    If `expand_loose` is `True`, the child control of a 
    [`Column`](https://flet.dev/docs/controls/column) or a [`Row`](https://flet.dev/docs/controls/row) 
    will be given the flexibility to expand to fill the available space in the main 
    axis (e.g., horizontally for a Row or vertically for a Column), but will not be 
    required to fill the available space.

    The default value is `False`.

    Here is the example of Containers placed in Rows with `expand_loose = True`:
    ```python
    import flet as ft


    class Message(ft.Container):
        def __init__(self, author, body):
            super().__init__()
            self.content = ft.Column(
                controls=[
                    ft.Text(author, weight=ft.FontWeight.BOLD),
                    ft.Text(body),
                ],
            )
            self.border = ft.border.all(1, ft.Colors.BLACK)
            self.border_radius = ft.border_radius.all(10)
            self.bgcolor = ft.Colors.GREEN_200
            self.padding = 10
            self.expand = True
            self.expand_loose = True


    def main(page: ft.Page):
        chat = ft.ListView(
            padding=10,
            spacing=10,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        Message(
                            author="John",
                            body="Hi, how are you?",
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        Message(
                            author="Jake",
                            body="Hi I am good thanks, how about you?",
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        Message(
                            author="John",
                            body="Lorem Ipsum is simply dummy text of the printing and 
                            typesetting industry. Lorem Ipsum has been the industry's 
                            standard dummy text ever since the 1500s, when an unknown 
                            printer took a galley of type and scrambled it to make a 
                            type specimen book.",
                        ),
                    ],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.END,
                    controls=[
                        Message(
                            author="Jake",
                            body="Thank you!",
                        ),
                    ],
                ),
            ],
        )

        page.window.width = 393
        page.window.height = 600
        page.window.always_on_top = False

        page.add(chat)


    ft.run(main)

    ``` 

    <img src="https://flet.dev/img/docs/controls/overview/expand = True, 
    expand_loose = True.png" className="screenshot-50" />
    """

    col: ResponsiveNumber = 12  # todo: if dict, validate keys with those in parent (ResponsiveRow.breakpoints)
    """
    If a parent of the control is ResponsiveRow, `col` property is used to determine 
    how many virtual columns of a screen the control will span. 
    
    Can be a number or a dictionary configured to have a different value for specific 
    breakpoints, for example `col={"sm": 6}`. Breakpoints are named dimension ranges:

    | Breakpoint | Dimension |
    |---|---|
    | xs | <576px |
    | sm | ≥576px |
    | md | ≥768px |
    | lg | ≥992px |
    | xl | ≥1200px |
    | xxl | ≥1400px |

    If `col` property is not specified, it spans the maximum number of columns (12).
    """

    opacity: Number = 1.0
    """
    Defines the transparency of the control.

    Value ranges from `0.0` (completely transparent) to `1.0` (completely opaque 
    without any transparency) and defaults to `1.0`.
    """

    tooltip: Optional[TooltipValue] = None
    """
    The `tooltip` property supports both strings 
    and [`Tooltip`](https://flet.dev/docs/reference/types/tooltip.md) objects.
    """

    badge: Optional[BadgeValue] = None
    """
    The `badge` property supports both strings and 
    [`Badge`](https://flet.dev/docs/reference/types/badge.md) objects.
    """

    visible: bool = True
    """
    Every control has `visible` property which is `True` by default - control is 
    rendered on the page. Setting `visible` to `False` completely prevents control (and 
    all its children if any) from rendering on a page canvas. Hidden controls cannot be 
    focused or selected with a keyboard or mouse and they do not emit any events.
    """

    disabled: bool = False
    """
    Every control has `disabled` property which is `False` by default - control and all 
    its children are enabled.
    `disabled` property is mostly used with data entry controls like `TextField`, 
    `Dropdown`, `Checkbox`, buttons.
    However, `disabled` could be set to a parent control and its value will be 
    propagated down to all children recursively.

    For example, if you have a form with multiple entry controls you can disable them 
    all together by disabling container:

    ```python
    c = ft.Column(controls=[
        ft.TextField(),
        ft.TextField()
    ])
    c.disabled = True
    page.add(c)
    ```
    """

    rtl: bool = False
    """
    `True` to set text direction to right-to-left.
    """

    def before_update(self):
        super().before_update()
        assert 0.0 <= self.opacity <= 1.0, (
            "opacity must be between 0.0 and 1.0 inclusive"
        )
        assert self.expand is None or isinstance(self.expand, (bool, int)), (
            "expand must be of bool or int type"
        )

    def clean(self) -> None:
        raise Exception("Deprecated!")


# Typing
OptionalControl = Optional[Control]
