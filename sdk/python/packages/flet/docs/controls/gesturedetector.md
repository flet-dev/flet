::: flet.GestureDetector

## Examples

[Live example](https://flet-controls-gallery.fly.dev/utility/gesturedetector)

[Solitare game tutorial](https://flet.dev/docs/tutorials/python-solitaire)

### Draggable containers

The following example demonstrates how a control can be freely dragged inside a Stack.

The sample also shows that GestureDetector can have a child control (blue container) as well as be nested inside another control (yellow container) giving the same results.

<img src="/img/docs/controls/gesture-detector/gesture-detector-two-containers.gif" className="screenshot-50" />



```python
import flet as ft

def main(page: ft.Page):
    def on_pan_update1(e: ft.DragUpdateEvent):
        c.top = max(0, c.top + e.delta_y)
        c.left = max(0, c.left + e.delta_x)
        c.update()

    def on_pan_update2(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    gd = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=50,
        on_pan_update=on_pan_update1,
    )

    c = ft.Container(gd, bgcolor=ft.Colors.AMBER, width=50, height=50, left=0, top=0)

    gd1 = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=10,
        on_vertical_drag_update=on_pan_update2,
        left=100,
        top=100,
        content=ft.Container(bgcolor=ft.Colors.BLUE, width=50, height=50),
    )

    page.add( ft.Stack([c, gd1], width=1000, height=500))

ft.run(main)
```


