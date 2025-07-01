::: flet.Column

## Examples

[Live example](https://flet-controls-gallery.fly.dev/layout/column)

### Column spacing

<img src="/img/docs/controls/column/column-spacing.gif" className="screenshot-50"/>



```python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    def spacing_slider_change(e):
        col.spacing = int(e.control.value)
        col.update()

    gap_slider = ft.Slider(
        min=0,
        max=100,
        divisions=10,
        value=0,
        label="{value}",
        width=500,
        on_change=spacing_slider_change,
    )

    col = ft.Column(spacing=0, controls=items(5))

    page.add(ft.Column([ ft.Text("Spacing between items"), gap_slider]), col)

ft.run(main)
```


### Column wrapping

<img src="/img/docs/controls/column/column-wrapping.gif" className="screenshot-70"/>



```python
import flet as ft

HEIGHT = 400

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=30,
                    height=30,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.border_radius.all(5),
                )
            )
        return items

    def slider_change(e):
        col.height = float(e.control.value)
        col.update()

    width_slider = ft.Slider(
        min=0,
        max=HEIGHT,
        divisions=20,
        value=HEIGHT,
        label="{value}",
        width=500,
        on_change=slider_change,
    )

    col = ft.Column(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=items(10),
        height=HEIGHT,
    )

    page.add(
        ft.Column(
            [
                ft.Text(
                    "Change the column height to see how child items wrap onto multiple columns:"
                ),
                width_slider,
            ]
        ),
        ft.Container(content=col, bgcolor=ft.Colors.AMBER_100),
    )

ft.run(main)
```


### Column vertical alignments

<img src="/img/docs/controls/column/column-alignment.png"  className="screenshot-70"/>



```python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_alignment(align: ft.MainAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=10),
                ft.Container(
                    content=ft.Column(items(3), alignment=align),
                    bgcolor=ft.Colors.AMBER_100,
                    height=400,
                ),
            ]
        )

    page.add(
        ft.Row(
            [
                column_with_alignment(ft.MainAxisAlignment.START),
                column_with_alignment(ft.MainAxisAlignment.CENTER),
                column_with_alignment(ft.MainAxisAlignment.END),
                column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
                column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
                column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )
    )

ft.run(main)
```


### Column horizontal alignments

<img src="/img/docs/controls/column/column-horiz-alignment.png"  className="screenshot-50" />



```python
import flet as ft

def main(page: ft.Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.alignment.center,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER_500,
                )
            )
        return items

    def column_with_horiz_alignment(align: ft.CrossAxisAlignment):
        return ft.Column(
            [
                ft.Text(str(align), size=16),
                ft.Container(
                    content=ft.Column(
                        items(3),
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=align,
                    ),
                    bgcolor=ft.Colors.AMBER_100,
                    width=100,
                ),
            ]
        )

    page.add(
        ft.Row(
            [
                column_with_horiz_alignment(ft.CrossAxisAlignment.START),
                column_with_horiz_alignment(ft.CrossAxisAlignment.CENTER),
                column_with_horiz_alignment(ft.CrossAxisAlignment.END),
            ],
            spacing=30,
            alignment=ft.MainAxisAlignment.START,
        )
    )

ft.run(main)
```


### Infinite scroll list

The following example demonstrates adding of list items on-the-fly, as user scroll to the bottom, creating the illusion of infinite list:

```python
import threading
import flet as ft

class State:
    i = 0

s = State()
sem = threading.Semaphore()

def main(page: ft.Page):
    def on_scroll(e: ft.OnScrollEvent):
        if e.pixels >= e.max_scroll_extent - 100:
            if sem.acquire(blocking=False):
                try:
                    for i in range(0, 10):
                        cl.controls.append(ft.Text(f"Text line {s.i}", key=str(s.i)))
                        s.i += 1
                    cl.update()
                finally:
                    sem.release()

    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
        on_scroll_interval=0,
        on_scroll=on_scroll,
    )
    for i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {s.i}", key=str(s.i)))
        s.i += 1

    page.add(ft.Container(cl, border=ft.border.all(1)))

ft.run(main)
```

### Scrolling column programmatically

<img src="/img/docs/controls/column/column-scroll-to.png"  className="screenshot-50" />

The following example demonstrates various `scroll_to()` options as well as defines a custom scrollbar theme:

```python
import flet as ft

def main(page: ft.Page):
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.ControlState.HOVERED: ft.Colors.AMBER,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.Colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.ControlState.HOVERED: ft.Colors.RED,
                ft.ControlState.DEFAULT: ft.Colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
            # interactive=False,
        )
    )

    cl = ft.Column(
        spacing=10,
        height=200,
        width=float("inf"),
        scroll=ft.ScrollMode.ALWAYS,
    )
    for i in range(0, 100):
        cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

    def scroll_to_offset(e):
        cl.scroll_to(offset=100, duration=1000)

    def scroll_to_start(e):
        cl.scroll_to(offset=0, duration=1000)

    def scroll_to_end(e):
        cl.scroll_to(offset=-1, duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT)

    def scroll_to_key(e):
        cl.scroll_to(key="20", duration=1000)

    def scroll_to_delta(e):
        cl.scroll_to(delta=40, duration=200)

    def scroll_to_minus_delta(e):
        cl.scroll_to(delta=-40, duration=200)

    page.add(
        ft.Container(cl, border=ft.border.all(1)),
        ft.ElevatedButton("Scroll to offset 100", on_click=scroll_to_offset),
        ft.Row(
            [
                ft.ElevatedButton("Scroll to start", on_click=scroll_to_start),
                ft.ElevatedButton("Scroll to end", on_click=scroll_to_end),
            ]
        ),
        ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
        ft.Row(
            [
                ft.ElevatedButton("Scroll -40", on_click=scroll_to_minus_delta),
                ft.ElevatedButton("Scroll +40", on_click=scroll_to_delta),
            ]
        ),
    )

ft.run(main)
```
