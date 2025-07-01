::: flet.Slider

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/slider)

### Basic sliders



```python
import flet as ft

def main(page):
    page.add(
        ft.Text("Default slider:"),
        ft.Slider(),
        ft.Text("Default disabled slider:"),
        ft.Slider(disabled=True))

ft.run(main)
```


### Sliders with values



```python
import flet as ft

def main(page):
    page.add(
        ft.Text("Slider with value:"),
        ft.Slider(value=0.3),
        ft.Text("Slider with a custom range and label:"),
        ft.Slider(min=0, max=100, divisions=10, label="{value}%"))

ft.run(main)
```


<img src="/img/docs/controls/slider/slider-with-custom-content.gif" className="screenshot-30"/>

### Slider with `on_change` event



```python
import flet as ft

def main(page):

    def slider_changed(e):
        t.value = f"Slider changed to {e.control.value}"
        page.update()

    t = ft.Text()
    page.add(
        ft.Text("Slider with 'on_change' event:"),
        ft.Slider(min=0, max=100, divisions=10, label="{value}%", on_change=slider_changed), t)

ft.run(main)
```


<img src="/img/docs/controls/slider/slider-with-change-event.gif" className="screenshot-30"/>
