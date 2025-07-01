::: flet.CupertinoActivityIndicator

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/cupertinoactivityindicator)

### Basic Example



```python
import flet as ft

def main(page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.CupertinoActivityIndicator(
            radius=50,
            color=ft.Colors.RED,
            animating=True,
        )
    )

ft.run(main)
```



<img src="/img/docs/controls/cupertino-activity-indicator/basic-cupertino-activity-indicator.png" className="screenshot-40"/>

