---
class_name: flet.Badge
examples: ../../examples/controls/badge
example_images: ../test-images/examples/material/golden/macos/badge
example_media: ../examples/controls/badge/media
---

{{ class_summary(class_name, example_images + "/image_for_docs.png", image_caption="Basic Badge") }}

## Examples

[Live example](https://flet-controls-gallery.fly.dev/displays/badge)

### Badge decorating an icon on a NavigationBar

<Tabs groupId="language">
  <TabItem value="python" label="Python" default>

```python
import flet as ft


def main(page: ft.Page):
    page.title = "Badge example"

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon_content=ft.Icon(
                    ft.Icons.EXPLORE,
                    badge=ft.Badge(small_size=10),
                ),
                label="Explore",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE,
                label="Commute",
            ),
            ft.NavigationBarDestination(
                icon_content=ft.Icon(
                    ft.Icons.PHONE,
                    badge="10",
                )
            ),
        ]
    )
    page.add(ft.Text("Body!"))


ft.run(main)
```


{{ image(example_media + "/badge-navigation-bar.png", alt="badge-navigation-bar", width="80%") }}

{{ class_members(class_name) }}
