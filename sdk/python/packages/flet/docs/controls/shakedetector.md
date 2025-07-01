::: flet.ShakeDetector

## Examples

### Shake detector sample

```python
import flet as ft

def main(page: ft.Page):
    shd = ft.ShakeDetector(
        minimum_shake_count=2,
        shake_slop_time_ms=300,
        shake_count_reset_time_ms=1000,
        on_shake=lambda _: print("SHAKE DETECTED!"),
    )
    page.overlay.append(shd)

    page.add(ft.Text("Program body"))

ft.run(main)
```
