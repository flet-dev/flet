::: flet.HapticFeedback

## Examples

### Haptic feedback sample

```python
import flet as ft

def main(page: ft.Page):
    hf = ft.HapticFeedback()
    page.overlay.append(hf)

    page.add(
        ft.ElevatedButton("Heavy impact", on_click=lambda _: hf.heavy_impact()),
        ft.ElevatedButton("Medium impact", on_click=lambda _: hf.medium_impact()),
        ft.ElevatedButton("Light impact", on_click=lambda _: hf.light_impact()),
        ft.ElevatedButton("Vibrate", on_click=lambda _: hf.vibrate()),
    )

ft.run(main)
```

## Methods

### `heavy_impact()`

Provides a haptic feedback corresponding a collision impact with a heavy mass.

### `light_impact()`

Provides a haptic feedback corresponding a collision impact with a light mass.

### `medium_impact()`

Provides a haptic feedback corresponding a collision impact with a medium mass.

### `vibrate()`

Provides vibration haptic feedback to the user for a short duration.