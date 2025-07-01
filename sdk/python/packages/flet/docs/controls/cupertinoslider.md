::: flet.CupertinoSlider

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/cupertinoslider)

### CupertinoSlider with `on_change`, `on_change_start` and `on_change_end` events



```python
import flet as ft

def main(page):
    page.horizontal_alignment = page.vertical_alignment = "center"
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_change_start(e):
        slider_status.value = "Sliding"
        page.update()

    def handle_change(e):
        slider_value.value = str(e.control.value)
        page.update()

    def handle_change_end(e):
        slider_status.value = "Finished sliding"
        page.update()

    page.add(
        slider_value := ft.Text("0.0"),
        ft.CupertinoSlider(
            divisions=5,
            max=100,
            active_color=ft.Colors.PURPLE,
            thumb_color=ft.Colors.PURPLE,
            on_change_start=handle_change_start,
            on_change_end=handle_change_end,
            on_change=handle_change,
        ),
        slider_status := ft.Text(),
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertinoslider/cupertino-slider-with-events.gif" className="screenshot-30"/>
