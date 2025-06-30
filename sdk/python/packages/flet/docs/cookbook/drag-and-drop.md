---
title: Drag and drop
sidebar_label: Drag and drop
---

The mechanics of drag-and-drop in Flet is pretty simple - a user starts dragging [`Draggable`](/docs/controls/draggable) control and "drops" it on [`DragTarget`](/docs/controls/dragtarget). If both draggable and drag target has the same `group` a drag target will call `on_accept` event handler and pass draggable control ID as event data. In this case draggable serves as a source "data" for drag-and-drop operation.

Let's take a look at the following example. In the program below you can drag left control displaying "1" on top of the right control displaying "0" and when drag operation completes left control is replaced with "0" and the right control becomes "1":

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Drag and Drop example"

    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        src.content.content.value = "0"
        # update text inside drag target control
        e.control.content.content.value = "1"
        page.update()

    page.add(
        ft.Row(
            [
                ft.Draggable(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.CYAN_200,
                        border_radius=5,
                        content=ft.Text("1", size=20),
                        alignment=ft.alignment.center,
                    ),
                ),
                ft.Container(width=100),
                ft.DragTarget(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.PINK_200,
                        border_radius=5,
                        content=ft.Text("0", size=20),
                        alignment=ft.alignment.center,
                    ),
                    on_accept=drag_accept,
                ),
            ]
        )
    )

ft.run(main)
```

![Drag and drop number](../assets/getting-started/drag-and-drop-number.gif)

So, it's developer's responsibility to determine what happens with "source" (draggable) and "destination" (drag target) controls when `on_accept` event occurs.

/// admonition | Try something
    type: note
Change DragTarget's group property to `number1` and note `on_accept` is not called any more when you drop "1" on the target.
///

There are additional properties and event handlers to make drag-and-drop operation even more interactive. For example, draggable has `content_when_dragging` property to display a different control instead of `content` when drag operation is under way. There is also `content_feedback` property to show a different control under the pointer. By default, the same `content` control, but with 50% opacity is displayed under cursor when dragging.

Let's modify Draggable in our example to display a "hole" in place of dragged control and just "1" under cursor while dragging:

```python
...
                ft.Draggable(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.CYAN_200,
                        border_radius=5,
                        content=ft.Text("1", size=20),
                        alignment=ft.alignment.center,
                    ),
                    content_when_dragging=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.BLUE_GREY_200,
                        border_radius=5,
                    ),
                    content_feedback=ft.Text("1"),
                ),
...
```

![Drag and drop number 2](../assets/getting-started/drag-and-drop-number-2.gif)

Drag target control additionally has `on_will_accept` and `on_leave` event handlers which help better visualize when it's a good time to "drop" something on the target. Let's modify DragTarget in our example to draw a border around target control when it's ready to accept incoming drag:

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Drag and Drop example 2"

    def drag_accept(e):
        # get draggable (source) control by its ID
        src = page.get_control(e.src_id)
        # update text inside draggable control
        src.content.content.value = "0"
        # reset source group, so it cannot be dropped to a target anymore
        src.group = ""
        # update text inside drag target control
        e.control.content.content.value = "1"
        # reset border
        e.control.content.border = None
        page.update()

    def drag_will_accept(e):
        # black border when it's allowed to drop and red when it's not
        e.control.content.border = ft.border.all(
            2, ft.Colors.BLACK45 if e.data == "true" else ft.Colors.RED
        )
        e.control.update()

    def drag_leave(e):
        e.control.content.border = None
        e.control.update()

    page.add(
        ft.Row(
            [
                ft.Draggable(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.CYAN_200,
                        border_radius=5,
                        content=ft.Text("1", size=20),
                        alignment=ft.alignment.center,
                    ),
                    content_when_dragging=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.BLUE_GREY_200,
                        border_radius=5,
                    ),
                    content_feedback=ft.Text("1"),
                ),
                ft.Container(width=100),
                ft.DragTarget(
                    group="number",
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.PINK_200,
                        border_radius=5,
                        content=ft.Text("0", size=20),
                        alignment=ft.alignment.center,
                    ),
                    on_accept=drag_accept,
                    on_will_accept=drag_will_accept,
                    on_leave=drag_leave,
                ),
            ]
        )
    )

ft.run(main)
```

![Drag and drop number 3](../assets/getting-started/drag-and-drop-number-3.gif)
