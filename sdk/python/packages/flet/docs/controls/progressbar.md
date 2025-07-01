::: flet.ProgressBar

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/progressbar)



```python
from time import sleep

import flet as ft

def main(page: ft.Page):
    pb = ft.ProgressBar(width=400)

    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.Column([ ft.Text("Doing something..."), pb]),
        ft.Text("Indeterminate progress bar", style="headlineSmall"),
        ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
    )

    for i in range(0, 101):
        pb.value = i * 0.01
        sleep(0.1)
        page.update()

ft.run(main)
```


<img src="/img/docs/controls/progress-bar/custom-progress-bars.gif" className="screenshot-30"/>
