import asyncio
from typing import Optional, cast

import httpx

import flet as ft


# ---------- DIALOG COMPONENT ----------
@ft.component
def UserDialogContent():
    """Component that loads and displays user data"""
    loading, set_loading = ft.use_state(True)
    name, set_name = ft.use_state("")
    email, set_email = ft.use_state("")
    error, set_error = ft.use_state("")

    async def load_user():
        set_loading(True)
        set_error("")
        try:
            await asyncio.sleep(2)  # Simulate network delay
            async with httpx.AsyncClient(timeout=5) as client:
                r = await client.get("https://jsonplaceholder.typicode.com/users/1")
                r.raise_for_status()
                data = r.json()
                set_name(data["name"])
                set_email(data["email"])
        except Exception as e:
            set_error(str(e))
        finally:
            set_loading(False)

    # Load data when component mounts
    ft.use_effect(lambda: asyncio.create_task(load_user()), [])

    return ft.Column(
        tight=True,
        controls=[
            ft.Text("User Panel", weight=ft.FontWeight.BOLD, size=18),
            ft.ProgressRing(visible=loading),
            ft.Text(f"Name: {name}"),
            ft.Text(f"Email: {email}"),
            ft.Text(error, color=ft.Colors.RED) if error else ft.Container(),
        ],
    )


# ---------- PARENT COMPONENT ----------
@ft.component
def App():
    dlg_ref = ft.use_ref(cast(Optional[ft.AlertDialog], None))

    if dlg_ref.current is None:
        dlg_ref.current = ft.AlertDialog(
            modal=True,
            title=ft.Text("User Information"),
            content=UserDialogContent(),
            actions=[ft.TextButton("Close", on_click=lambda e: e.page.pop_dialog())],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def open_user_dialog():
        if dlg_ref.current:
            ft.context.page.show_dialog(dlg_ref.current)

    return ft.Container(
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text("Main App", size=22, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "Open User Panel",
                    on_click=open_user_dialog,
                ),
            ]
        ),
    )


ft.run(lambda page: page.render(App))
