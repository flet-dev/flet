::: flet.RangeSlider

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/rangeslider)

### Range slider with divisions and labels



```python
import flet as ft


def main(page: ft.Page):
    range_slider = ft.RangeSlider(
        min=0,
        max=50,
        start_value=10,
        divisions=10,
        end_value=20,
        inactive_color=ft.Colors.GREEN_300,
        active_color=ft.Colors.GREEN_700,
        overlay_color=ft.Colors.GREEN_100,
        label="{value}%",
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Range slider with divisions and labels",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=30),
                range_slider,
            ],
        )
    )


ft.run(main)
```


<img src="/img/docs/controls/rangeslider/rangeslider.gif" className="screenshot-70"/>

### RangeSlider with events



```python
import flet as ft


def main(page: ft.Page):
    def slider_change_start(e):
        print(f"on_change_start: {e.control.start_value}, {e.control.end_value}")

    def slider_is_changing(e):
        print(f"on_change: {e.control.start_value}, {e.control.end_value}")

    def slider_change_end(e):
        print(f"on_change_end: {e.control.start_value}, {e.control.end_value}")

    range_slider = ft.RangeSlider(
        min=0,
        max=50,
        start_value=10,
        end_value=20,
        on_change_start=slider_change_start,
        on_change=slider_is_changing,
        on_change_end=slider_change_end,
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Range slider with events",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=30),
                range_slider,
            ],
        )
    )


ft.run(main)
```
