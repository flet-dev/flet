---
class_name: flet.Page
---

{{ class_all_options(class_name) }}

## Locking device orientation

Use `page.device_orientations` to control which physical orientations are allowed when the app runs on Android or iOS. Provide a list of [`DeviceOrientation`](../types/deviceorientation.md) values— for example `[ft.DeviceOrientation.PORTRAIT_UP]` to force an upright portrait experience, or `list(ft.DeviceOrientation)` to restore all directions.

```python
import flet as ft

def main(page: ft.Page):
    page.device_orientations = [ft.DeviceOrientation.PORTRAIT_UP]
    page.add(ft.Text("The app is locked to portrait up on mobile devices."))

ft.app(target=main)
```

See the full example at `sdk/python/examples/controls/page/orientation_lock.py`.
