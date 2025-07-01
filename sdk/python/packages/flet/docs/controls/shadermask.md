::: flet.ShaderMask

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/shadermask)

### Adding a pink glow around image edges

<img src="/img/docs/controls/shader-mask/shader-mask-pink-glow.png" className="screenshot-20" />



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            [
                ft.ShaderMask(
                    ft.Image(
                        src="https://picsum.photos/200/200?1",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.FILL,
                    ),
                    blend_mode=ft.BlendMode.MULTIPLY,
                    shader=ft.RadialGradient(
                        center=ft.alignment.center,
                        radius=2.0,
                        colors=[ft.Colors.WHITE, ft.Colors.PINK],
                        tile_mode=ft.GradientTileMode.CLAMP,
                    ),
                )
            ]
        )
    )

ft.run(main)
```



### Gradually fade out image to the bottom edge

<img src="/img/docs/controls/shader-mask/shader-mask-gradient.png" className="screenshot-20" />



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            [
                ft.ShaderMask(
                    ft.Image(src="https://picsum.photos/100/200?2"),
                    blend_mode=ft.BlendMode.DST_IN,
                    shader=ft.LinearGradient(
                        begin=ft.alignment.top_center,
                        end=ft.alignment.bottom_center,
                        colors=[ft.Colors.BLACK, ft.Colors.TRANSPARENT],
                        stops=[0.5, 1.0],
                    ),
                    border_radius=10,
                ),
            ]
        )
    )

ft.run(main)
```
