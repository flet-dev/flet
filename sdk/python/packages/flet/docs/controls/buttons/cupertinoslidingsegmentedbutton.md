::: flet.CupertinoSlidingSegmentedButton

## Examples

[Live example](https://flet-controls-gallery.fly.dev/buttons/cupertinoslidingsegmentedbutton)

### Basic Example



```python
import flet as ft

def main(page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.CupertinoSlidingSegmentedButton(
            selected_index=1,
            thumb_color=ft.Colors.BLUE_400,
            on_change=lambda e: print(f"selected_index: {e.data}"),
            padding=ft.padding.symmetric(0, 10),
            controls=[
                ft.Text("One"),
                ft.Text("Two"),
                ft.Text("Three"),
            ],
        ),
    )

ft.run(main)
```



<img src="/img/docs/controls/cupertino-sliding-segmented-button/basic-cupertino-sliding-segmented-button.gif" className="screenshot-40"/>
