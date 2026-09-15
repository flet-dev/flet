---
title: "Auto-update"
---

Flet automatically calls `page.update()` (or `.update()` on the nearest isolated ancestor) at the end of every event handler and `main()` function. This means you don't need to call `.update()` yourself in most cases:

```python
import flet as ft

def main(page: ft.Page):
    def button_click(e):
        page.controls.append(ft.Text("Clicked!"))
        # no need to call page.update() — it happens automatically

    page.controls.append(ft.Button("Click me", on_click=button_click))
    # no need to call page.update() here either

ft.run(main)
```

:::note[Note]
If your event handler already calls `.update()` explicitly (e.g. code written for Flet 0.x), the automatic update is skipped to avoid a redundant double update.
:::

## Updating part-way through a handler

Because the update is sent when the handler finishes, a handler that loops shows
nothing until it returns. To push an update mid-handler, make it a generator - each
`yield` flushes the pending update and lets the event loop run:

```python
import flet as ft

def main(page: ft.Page):
    progress = ft.ProgressBar(value=0)

    def process(e):
        for i in range(10):
            do_chunk(i)
            progress.value = (i + 1) / 10
            yield  # the bar advances here

    page.add(progress, ft.Button(content="Process", on_click=process))

ft.run(main)
```

Async handlers can yield too. An `await` lets other tasks run, but does not
trigger Flet's auto-update by itself. Yield after changing the control to publish
intermediate progress:

```python
async def process(e):
    for i in range(10):
        await asyncio.to_thread(do_chunk, i)
        progress.value = (i + 1) / 10
        yield
```

Alternatively, keep a regular async handler and call `progress.update()` after
each assignment. The next `await` gives the connection a chance to send the update.

:::note[Keep each chunk short]
A generator handler still runs on the event loop, so the UI is blocked between
yields. If a chunk takes long enough to notice, move it off the loop - see
[Async apps](async-apps.md#threading).
:::

## Disabling auto-update

You can disable auto-update for fine-grained control over when updates are sent to the client. Use `ft.context.disable_auto_update()` and `ft.context.enable_auto_update()` to toggle the behavior.

When called inside a handler, the setting applies to the current handler context only:

```python
import flet as ft

def main(page: ft.Page):
    def add_many_items(e):
        ft.context.disable_auto_update()
        for i in range(100):
            page.controls.append(ft.Text(f"Item {i}"))
        page.update()  # single update for all 100 items

    page.controls.append(ft.Button("Add items", on_click=add_many_items))

ft.run(main)
```

When called outside of event handlers (e.g. at the module level), it controls the global default for the entire app:

```python
import flet as ft

# disable auto-update globally
ft.context.disable_auto_update()

def main(page: ft.Page):
    def button_click(e):
        page.controls.append(ft.Text("Clicked!"))
        page.update()  # must call explicitly since auto-update is off

    page.controls.append(ft.Button("Click me", on_click=button_click))
    page.update()

ft.run(main)
```
