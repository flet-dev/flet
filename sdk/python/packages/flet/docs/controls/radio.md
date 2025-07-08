::: flet.Radio

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/radio)

### Basic RadioGroup



```python
import flet as ft

def main(page):
  def button_clicked(e):
    t.value = f"Your favorite color is:  {cg.value}"
    page.update()

  t = ft.Text()
  b = ft.ElevatedButton(text='Submit', on_click=button_clicked)
  cg = ft.RadioGroup(content=ft.Column([
    ft.Radio(value="red", label="Red"),
    ft.Radio(value="green", label="Green"),
    ft.Radio(value="blue", label="Blue")]))
  
  page.add(ft.Text("Select your favorite color:"), cg, b, t)

ft.run(main)
```


<img src="/img/docs/controls/radio/basic-radio.gif" className="screenshot-30"/>

### RadioGroup with `on_change` event



```python
import flet as ft

def main(page):
  def radiogroup_changed(e):
    t.value = f"Your favorite color is:  {e.control.value}"
    page.update()

  t = ft.Text()
  cg = ft.RadioGroup(content=ft.Column([
    ft.Radio(value="red", label="Red"),
    ft.Radio(value="green", label="Green"),
    ft.Radio(value="blue", label="Blue")]), on_change=radiogroup_changed)
  
  page.add(ft.Text("Select your favorite color:"), cg, t)

ft.run(main)
```


<img src="/img/docs/controls/radio/radio-with-change-event.gif" className="screenshot-30"/>
