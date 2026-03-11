Create a new directory (or directory with `pyproject.toml` already exists if initialized with a project manager) and switch into it.

To create a new "minimal" Flet app run the following command:

/// tab | uv
```bash
uv run flet create
```
///
/// tab | pip
```bash
flet create
```
///

/// admonition | Important
    type: danger
Any existing `README.md` or `pyproject.toml` (for example, created by `uv init`)
will be replaced by the one created by [`flet create`](../cli/flet-create.md) command.
///

The command will create the following directory structure:

```tree
README.md
pyproject.toml
src
    assets
        icon.png
    main.py # (1)!
storage
    data
    temp
```

1. Contains a simple Flet program.
    It has `main()` function where you would add UI elements (controls) to a page or a window.
    The application ends with a `ft.run()` function which initializes the Flet app and [runs](running-app.md) `main()`.

You can find more information about `flet create` command [here](../cli/flet-create.md).

## Auto-update

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

/// admonition | Note
    type: note
If your event handler already calls `.update()` explicitly (e.g. code written for Flet 0.x), the automatic update is skipped to avoid a redundant double update.
///

### Disabling auto-update

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

**Now let's see Flet in action by [running the app](running-app.md)!**
