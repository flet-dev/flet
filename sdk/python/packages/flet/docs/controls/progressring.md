::: flet.ProgressRing

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/progressring)



```python
from time import sleep
import flet as ft

def main(page: ft.Page):
    pr = ft.ProgressRing(width=16, height=16, stroke_width = 2)

    page.add(
        ft.Text("Circular progress indicator", style="headlineSmall"),
        ft.Row([pr, ft.Text("Wait for the completion...")]),
        ft.Text("Indeterminate cicrular progress", style="headlineSmall"),
        ft.Column(
            [ft.ProgressRing(), ft.Text("I'm going to run for ages...")],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    for i in range(0, 101):
        pr.value = i * 0.01
        sleep(0.1)
        page.update()

ft.run(main)
```


<img src="/img/docs/controls/progress-ring/custom-progress-rings.gif" className="screenshot-30"/>
