---
title: "Declarative dialogs"
---

[`ft.use_dialog()`](../types/usedialog.md) lets a component show and update dialogs declaratively.
Instead of imperatively calling [`page.show_dialog()`](../controls/page.md#flet.Page.show_dialog) and later
remembering to close or remove the dialog, you render a [`DialogControl`](../controls/dialogcontrol.md)
from component state:

- pass a dialog instance to show it;
- pass `None` to hide it.

This keeps dialog logic in the same state flow as the rest of a declarative app:

- state decides whether the dialog is visible;
- dialog content updates when state changes;
- there is no [`page.update()`](../controls/page.md#flet.Page.update) call in the component.

## Basic pattern

Call [`ft.use_dialog()`](../types/usedialog.md) on every render. When the dialog should be open,
return a dialog control; otherwise return `None`.

```python
import flet as ft


@ft.component
def App():
    show, set_show = ft.use_state(False)

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete report.pdf?"),
            content=ft.Text("This cannot be undone."),
            actions=[
                ft.TextButton("Delete", on_click=lambda: set_show(False)),
                ft.TextButton("Cancel", on_click=lambda: set_show(False)),
            ],
            on_dismiss=lambda: set_show(False),
        )
        if show
        else None
    )

    return ft.Column(
        controls=[
            ft.TextButton("Open dialog", on_click=lambda: set_show(True)),
        ]
    )


ft.run(lambda page: page.render(App))
```

The important part is that `show` is the source of truth. The dialog is not opened by
mutating the page tree directly; it appears because the component renders it.

## Updating dialog content from state

Because the dialog is declarative, its content can react to state changes while it is open.
This is useful for confirmations, form validation, and async workflows:

```python
import asyncio
import flet as ft


@ft.component
def App():
    show, set_show = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)

    async def handle_delete():
        set_deleting(True)
        await asyncio.sleep(2)
        set_deleting(False)
        set_show(False)

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete report.pdf?"),
            content=ft.Text(
                "Deleting, please wait..." if deleting else "This cannot be undone."
            ),
            actions=[
                ft.Button(
                    "Deleting..." if deleting else "Delete",
                    disabled=deleting,
                    on_click=handle_delete,
                ),
                ft.TextButton(
                    "Cancel",
                    disabled=deleting,
                    on_click=lambda: set_show(False),
                ),
            ],
            on_dismiss=lambda: set_show(False),
        )
        if show
        else None
    )

    return ft.TextButton("Delete file", on_click=lambda: set_show(True))

ft.run(lambda page: page.render(App))
```

This pattern works well with `asyncio` and other async APIs in Flet apps. For more
background, see [Async apps](async-apps.md).

## Chaining dialogs

You can call [`ft.use_dialog()`](../types/usedialog.md) more than once in the same component. That
makes follow-up flows straightforward, for example:

- confirmation dialog;
- async action;
- success dialog after the first dialog fully closes.

```python
import flet as ft


@ft.component
def App():
    show_confirm, set_show_confirm = ft.use_state(False)
    show_success, set_show_success = ft.use_state(False)
    should_chain = ft.use_ref(False)

    def confirm_delete():
        should_chain.current = True
        set_show_confirm(False)

    def on_confirm_dismiss():
        if should_chain.current:
            should_chain.current = False
            set_show_success(True)

    ft.use_dialog(
        ft.AlertDialog(
            title=ft.Text("Delete file?"),
            actions=[
                ft.TextButton("Delete", on_click=confirm_delete),
                ft.TextButton("Cancel", on_click=lambda: set_show_confirm(False)),
            ],
            on_dismiss=on_confirm_dismiss,
        )
        if show_confirm
        else None
    )

    ft.use_dialog(
        ft.AlertDialog(
            title=ft.Text("Done"),
            content=ft.Text("The file was deleted."),
            actions=[
                ft.TextButton("OK", on_click=lambda: set_show_success(False)),
            ],
        )
        if show_success
        else None
    )

    return ft.TextButton("Open", on_click=lambda: set_show_confirm(True))

ft.run(lambda page: page.render(App))
```

[`ft.use_ref()`](../types/useref.md) is helpful here because the value survives re-renders without
causing another render by itself.

## `on_dismiss` timing

[`DialogControl.on_dismiss`](../controls/dialogcontrol.md#flet.DialogControl.on_dismiss) fires after the dialog close
animation completes, not immediately when `open` changes to `False`. This makes it safe to
start follow-up UI after the dialog has actually finished closing.

Use `on_dismiss` for logic that should happen after the dialog is fully gone, such as:

- opening the next dialog in a chain;
- resetting temporary dialog-local state;
- starting a follow-up animation or toast.

## When to use `page.show_dialog()` instead

[`ft.use_dialog()`](../types/usedialog.md) is a better fit inside [`@ft.component`](../types/component.md)
functions and other declarative flows.

[`page.show_dialog()`](../controls/page.md#flet.Page.show_dialog) is still a good option when:

- the app is written imperatively;
- dialog lifecycle is handled outside the component tree;
- you need to trigger a dialog from existing page-level event code and do not want to convert
  that part of the app to declarative style yet.

In practice, the two APIs serve different styles:

- use declarative dialogs when UI should follow component state;
- use imperative dialogs when UI is managed by direct page mutation.
