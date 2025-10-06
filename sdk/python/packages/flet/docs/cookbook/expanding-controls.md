## `expand`

When a child control is placed into a [`Row`][flet.Row], [`Column`][flet.Column], [`View`][flet.View]
or [`Page`][flet.Page] you can "expand" it to fill the available space.

When adding child controls to a [`Row`][flet.Row], you can make them automatically
grow to fill available horizontal space using the [`expand`][flet.Control.expand] property,
which all Flet controls (inheriting from [`Control`][flet.Control]) have.

It lets you control how they use free space inside a
layout like [`Row`][flet.Row] or [`Column`][flet.Column].

You can set `expand` to one of the following values:

* a boolean — Whether the control should take all the available space.
* an integer — Used to proportionally divide free space among multiple expanding controls (useful when you want more control over sizing).

### Example 1

In this example, a [`TextField`][flet.TextField] stretches to fill all remaining space in the row,
while the [`Button`][flet.Button] stays sized to its content:

```python
ft.Row(
    controls=[
      ft.TextField(hint_text="Enter your name", expand=True),
      ft.Button(text="Join chat")
    ]
)
```

### Example 2

In this example, we create a [`Row`][flet.Row] with three [`Container`][flet.Container]s, distributed like 20% / 60% / 20%:

```python
ft.Row(
    controls=[
      ft.Container(content=ft.Text("A"), expand=1),
      ft.Container(content=ft.Text("B"), expand=3),
      ft.Container(content=ft.Text("C"), expand=1)
    ]
)
```

Here, the available space is split into 5 total parts (1+3+1).
The first and third containers get 1 part each (20%), and the middle one gets 3 parts (60%).

### Example 3

This example demonstrates how two [`Card`][flet.Card] controls inside a [`Row`][flet.Row] can
each expand to fill half of the available horizontal space using expand=True.

The layout uses a full-screen [`Column`][flet.Column] and a nested Row, where both cards are
expanded equally — resulting in a 50/50 split.

```python
import flet as ft

def main(page: ft.Page):
    page.spacing = 0
    page.padding = 0

    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
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
                ),
            ],
        ),
    )

ft.run(main)
```

## `expand_loose`

The [`expand_loose`][flet.Control.expand_loose] property allows a control to *optionally* expand
and fill the available space along the main axis of its parent container
(e.g., horizontally in a [`Row`][flet.Row], or vertically in a [`Column`][flet.Column]).

Unlike [`expand`][flet.Control.expand], which *forces* the control to occupy all available space,
`expand_loose` gives the control **flexibility** to grow **if needed**, but it’s not required to fill the space.

/// admonition | Note
For this property to have effect:

- it must be used on child controls within the following layout containers,
or any of their subclasses: [`Row`][flet.Row], [`Column`][flet.Column], [`View`][flet.View], [`Page`][flet.Page]
- the control using this property must have a non-none value for [`expand`][flet.Control.expand].
///

### Example 1

In this example, [`Container`][flet.Container]s being placed in [`Row`][flet.Row]s with `expand_loose = True`:

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
    page.window.width = 393
    page.window.height = 600
    page.window.always_on_top = False

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

    page.add(chat)


ft.run(main)
```

{{ image("../assets/controls/control/expand-loose.png", alt="expand_loose", width="65%") }}
