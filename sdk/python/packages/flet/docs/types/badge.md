::: flet.Badge

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
  </TabItem>
</Tabs>

<img src="/img/docs/controls/badge/badge-navigation-bar.png" className="screenshot-50" />
