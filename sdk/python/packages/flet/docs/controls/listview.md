::: flet.ListView

::info
ListView is very effective for large lists (thousands of items). 
Prefer it over [`Column`][flet.Column] 
or [`Row`][flet.Row] for smooth scrolling.
::



## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/listview)

### Auto-scrolling ListView



```python
from time import sleep
import flet as ft

def main(page: ft.Page):
    page.title = "Auto-scrolling ListView"

    lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    count = 1

    for i in range(0, 60):
        lv.controls.append(ft.Text(f"Line {count}"))
        count += 1

    page.add(lv)

    for i in range(0, 60):
        sleep(1)
        lv.controls.append(ft.Text(f"Line {count}"))
        count += 1
        page.update()

ft.run(main)
```


<img src="/img/docs/controls/listview/custom-listview.gif" className="screenshot-40"/>
