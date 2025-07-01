::: flet.Placeholder

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/placeholder)

### Basic example



```python
import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Placeholder(
            expand=True,
            color=ft.Colors.random_color()  # random material color
        )
    )


ft.run(main)
```


<img src="/img/docs/controls/placeholder/basic-example.png" className="screenshot-100"/>
