::: flet.GridView

::info
GridView is very effective for large lists (thousands of items). #
Prefer it over wrapping [`Column`][flet.Column] or [`Row`][flet.Row] for smooth scrolling. 
See [Flet Icons Browser](https://github.com/flet-dev/examples/blob/main/python/apps/icons-browser/main.py) 
for GridView usage example.
::



## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/gridview)

### Photo gallery

<img src="/img/docs/controls/gridview/photo-gallery.png" className="screenshot-50"/>



```python
import flet as ft

def main(page: ft.Page):
    page.title = "GridView Example"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.update()

    images = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=150,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    page.add(images)

    for i in range(0, 60):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/150/150?{i}",
                fit=ft.ImageFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

ft.run(main, view=ft.AppView.WEB_BROWSER)
```

