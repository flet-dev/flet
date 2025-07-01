::: flet.CupertinoSwitch

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/cupertinoswitch)

### CupertinoSwitch and adaptive Switch



```python
import logging
import flet as ft
import asyncio

logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    page.add(
        ft.CupertinoSwitch(
            label="Cupertino Switch",
            value=True,
        ),
        ft.Switch(
            label="Material Switch",
            value=True,
            thumb_color={ft.ControlState.SELECTED: ft.Colors.BLUE},
            track_color=ft.Colors.YELLOW,
            focus_color=ft.Colors.PURPLE,
        ),
        ft.Container(height=20),
        ft.Text(
            "Adaptive Switch shows as CupertinoSwitch on macOS and iOS and as Switch on other platforms:"
        ),
        ft.Switch(
            adaptive=True,
            label="Adaptive Switch",
            value=True,
        ),
    )


ft.run(main)
```


<img src="/img/docs/controls/cupertinoswitch/cupertino-switch.gif" className="screenshot-70"/>


### `value`

Current value of the switch.

## Events

### `on_blur`

Fires when the control has lost focus.

### `on_change`

Fires when the state of the switch is changed.

### `on_image_error`

Fires when the image (`active_thumb_image` or `inactive_thumb_image`) fails to load.

### `on_focus`

Fires when the control has received focus.