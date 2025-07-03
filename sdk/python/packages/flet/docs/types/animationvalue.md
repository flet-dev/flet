::: flet.AnimationValue

## Usage example

<img src="/img/docs/controls/container/animate-container.gif" className="screenshot-20" />

```python
import flet as ft

def main(page: ft.Page):

    c = ft.Container(
        width=200,
        height=200,
        bgcolor="red",
        animate=ft.animation.Animation(1000, ft.AnimationCurve.BOUNCE_OUT),
    )

    def animate_container(e):
        c.width = 100 if c.width == 200 else 200
        c.height = 100 if c.height == 200 else 200
        c.bgcolor = "blue" if c.bgcolor == "red" else "red"
        c.update()

    page.add(c, ft.ElevatedButton("Animate container", on_click=animate_container))

ft.app(main)
```