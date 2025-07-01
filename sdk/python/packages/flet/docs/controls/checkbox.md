::: flet.Checkbox

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/checkbox)

### Basic checkboxes



```python
import flet as ft

def main(page):
    def button_clicked(e):
        t.value = (
            f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}, {c5.value}."
        )
        page.update()

    t = ft.Text()
    c1 = ft.Checkbox(label="Unchecked by default checkbox", value=False)
    c2 = ft.Checkbox(label="Undefined by default tristate checkbox", tristate=True)
    c3 = ft.Checkbox(label="Checked by default checkbox", value=True)
    c4 = ft.Checkbox(label="Disabled checkbox", disabled=True)
    c5 = ft.Checkbox(
        label="Checkbox with rendered label_position='left'", label_position=ft.LabelPosition.LEFT
    )
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(c1, c2, c3, c4, c5, b, t)

ft.run(main)
```


<img src="/img/docs/controls/checkbox/basic-checkbox.gif" className="screenshot-40" />

### Checkbox with `on_change` event



```python
import flet as ft

def main(page):
  def checkbox_changed(e):
    t.value = f"Checkbox value changed to {c.value}" 
    t.update()

  c = ft.Checkbox(label="Checkbox with 'change' event", on_change=checkbox_changed)
  t = ft.Text()

  page.add(c, t)

ft.run(main)
```


<img src="/img/docs/controls/checkbox/checkbox-with-change-event.gif" className="screenshot-40" />
