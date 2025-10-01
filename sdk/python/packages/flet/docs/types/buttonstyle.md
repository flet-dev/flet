{{ class_all_options("flet.ButtonStyle") }}

## Usage example

You can configure a different shape, background color for a hovered state and configure fallback values for all other states.

To configure style attribute for all Material states set its value to a literal (or class instance). For example, if you set `color` property to a literal the value will be applied to all button states:

```python
ButtonStyle(
    color=ft.Colors.WHITE
)
```

To configure style attribute for specific Material states set its value to a dictionary where the key is state name. For example, to configure different background colors for `HOVERED` and `FOCUSED` states and another colors for all other states:

```python
ButtonStyle(
    color={
        ft.ControlState.HOVERED: ft.Colors.WHITE,
        ft.ControlState.FOCUSED: ft.Colors.BLUE,
        ft.ControlState.DEFAULT: ft.Colors.BLACK,
    }
)
```


### Various button shapes example

<img src="/img/blog/gradients/button-shapes.png" className="screenshot-20" />

```python
import flet as ft

def main(page: ft.Page):
    page.padding = 30
    page.spacing = 30
    page.add(
        ft.FilledButton(
            "Stadium",
            style=ft.ButtonStyle(
                shape=ft.StadiumBorder(),
            ),
        ),
        ft.FilledButton(
            "Rounded rectangle",
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        ),
        ft.FilledButton(
            "Continuous rectangle",
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=30),
            ),
        ),
        ft.FilledButton(
            "Beveled rectangle",
            style=ft.ButtonStyle(
                shape=ft.BeveledRectangleBorder(radius=10),
            ),
        ),
        ft.FilledButton(
            "Circle",
            style=ft.ButtonStyle(shape=ft.CircleBorder(), padding=30),
        ),
    )

ft.run(main)
```

### Styled button example

Check the following example:

<img src="/img/blog/gradients/styled-button.gif" className="screenshot-30" />

```python
import flet as ft

def main(page: ft.Page):

    page.add(
        ft.Button(
            "Styled button 1",
            style=ft.ButtonStyle(
                color={
                    ft.ControlState.HOVERED: ft.Colors.WHITE,
                    ft.ControlState.FOCUSED: ft.Colors.BLUE,
                    ft.ControlState.DEFAULT: ft.Colors.BLACK,
                },
                bgcolor={ft.ControlState.FOCUSED: ft.Colors.PINK_200, "": ft.Colors.YELLOW},
                padding={ft.ControlState.HOVERED: 20},
                overlay_color=ft.Colors.TRANSPARENT,
                elevation={"pressed": 0, "": 1},
                animation_duration=500,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, ft.Colors.BLUE),
                    ft.ControlState.HOVERED: ft.BorderSide(2, ft.Colors.BLUE),
                },
                shape={
                    ft.ControlState.HOVERED: ft.RoundedRectangleBorder(radius=20),
                    ft.ControlState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                },
            ),
        )
    )

ft.run(main)
```
