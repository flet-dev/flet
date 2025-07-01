::: flet.InteractiveViewer

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/interactiveviewer)

### Basic Example

```python
import flet as ft


def main(page: ft.Page):
    page.add([interactiveviewer.md](interactiveviewer.md)
        ft.InteractiveViewer(
            min_scale=0.1,
            max_scale=15,
            boundary_margin=ft.margin.all(20),
            on_interaction_start=lambda e: print(e),
            on_interaction_end=lambda e: print(e),
            on_interaction_update=lambda e: print(e),
            content=ft.Image(
                src="https://picsum.photos/500/500",
            ),
        )
    )


ft.run(main)
```

