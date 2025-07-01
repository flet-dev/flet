::: flet.CupertinoCheckbox


## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/cupertinocheckbox)

### CupertinoCheckbox and adaptive CheckBox example



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.CupertinoCheckbox(label="Cupertino Checkbox", value=True),
        ft.Checkbox(label="Material Checkbox", value=True),
        ft.Container(height=20),
        ft.Text(
            "Adaptive Checkbox shows as CupertinoCheckbox on macOS and iOS and as Checkbox on other platforms:"
        ),
        ft.Checkbox(adaptive=True, label="Adaptive Checkbox", value=True),
    )

ft.run(main)
```


<img src="/img/docs/controls/cupertinocheckbox/cupertinocheckbox.png" className="screenshot-70" />

