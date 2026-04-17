"""Repro for the ``use_dialog`` multi-host race.

Two sibling components each own a dialog via ``ft.use_dialog``: an
``AlertHost`` shows an AlertDialog while a ``ToastHost`` shows a SnackBar.
A single click handler flips both in the same scheduler tick — the
AlertDialog is dismissed while the SnackBar is shown.  Before the fix the
AlertDialog stays stuck open because the two hosts emit conflicting patches
(an immediate ``patch_control(prev)`` for dismissal and a deferred
``schedule_update(_dialogs)`` for show) and the Flutter overlay rebuild
recreates the AlertDialog Element mid-dismiss.

Run with ``uv run flet run path/to/multi_host``.
"""

from __future__ import annotations

from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class Session:
    alert_open: bool = False
    toast: str | None = None
    toast_nonce: int = 0


session = Session()
SessionContext = ft.create_context(session)


def use_session() -> Session:
    return ft.use_context(SessionContext)


def show_toast(text: str) -> None:
    session.toast = text
    session.toast_nonce += 1


def _log(msg: str):
    with open("/tmp/multi_host.log", "a") as f:
        f.write(msg + "\n")


@ft.component
def AlertHost():
    s = use_session()

    def cancel(_):
        _log(f"[CLICK] cancel; alert_open={s.alert_open}")
        s.alert_open = False

    def delete(_):
        _log(f"[CLICK] delete; alert_open={s.alert_open}")
        s.alert_open = False
        show_toast("Deleted")

    dialog = (
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete item?"),
            content=ft.Text(
                "Clicking 'Delete' dismisses this dialog and shows a "
                "snackbar in the same scheduler tick."
            ),
            actions=[
                ft.TextButton("Cancel", on_click=cancel),
                ft.FilledButton("Delete", on_click=delete),
            ],
            on_dismiss=cancel,
        )
        if s.alert_open
        else None
    )
    ft.use_dialog(dialog)
    return ft.Container(width=0, height=0)


@ft.component
def ToastHost():
    s = use_session()
    text = s.toast
    _ = s.toast_nonce  # subscribe so duplicate toasts re-fire

    def clear(_):
        s.toast = None

    dialog = ft.SnackBar(content=ft.Text(text), on_dismiss=clear) if text else None
    ft.use_dialog(dialog)
    return ft.Container(width=0, height=0)


@ft.component
def Body():
    s = use_session()

    def open_dialog():
        _log(f"[CLICK] open_dialog; alert_open={s.alert_open}")
        s.alert_open = True

    return ft.View(
        route="/",
        appbar=ft.AppBar(title=ft.Text("use_dialog multi-host race")),
        controls=[
            AlertHost(),
            ToastHost(),
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Text(
                            "1. Click 'Open dialog' to show an AlertDialog with a\n"
                            "   Delete button.\n"
                            "2. Click 'Delete' inside the dialog — its on_click\n"
                            "   dismisses the dialog AND fires a snackbar in the\n"
                            "   same scheduler tick (two `use_dialog` hosts).\n\n"
                            "Before the fix the dialog stays stuck on step 2.",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.FilledButton("Open dialog", on_click=open_dialog),
                    ],
                ),
            ),
        ],
    )


@ft.component
def App():
    return SessionContext(session, Body)


def main(page: ft.Page):
    page.render_views(lambda: [App()])


if __name__ == "__main__":
    ft.run(main)
