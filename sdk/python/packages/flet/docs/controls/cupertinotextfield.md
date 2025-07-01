::: flet.CupertinoTextField

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/cupertinotextfield)

### Basic textfields



```python
import flet as ft

def main(page: ft.Page):

    page.add(
        ft.TextField(
            label="Material",
        ),
        ft.CupertinoTextField(
            placeholder_text="Placeholder",
        ),
        ft.TextField(
            adaptive=True,
            label="Adaptive",
        ),
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertinotextfield/basic-cupertino-textfield.png" className="screenshot-40"/>
