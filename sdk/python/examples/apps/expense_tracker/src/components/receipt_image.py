"""Load saved receipts by reference without placing photo bytes in ledger JSON."""

import logging

import theme
from state import StateContext

import flet as ft

log = logging.getLogger(f"app.{__name__}")


@ft.component
def ReceiptImage(receipt_ref: str, height: int = theme.RECEIPT_DETAIL_HEIGHT):
    state = ft.use_context(StateContext)
    loaded, set_loaded = ft.use_state(None)
    failed, set_failed = ft.use_state(False)

    async def load():
        set_loaded(None)
        set_failed(False)
        try:
            data = await state.load_receipt_photo(receipt_ref)
            set_loaded((receipt_ref, data))
            set_failed(not data)
        except Exception:
            log.exception("Receipt photo could not be loaded")
            set_failed(True)

    ft.use_effect(load, [receipt_ref])
    if failed:
        return ft.Column(
            tight=True,
            spacing=theme.Space.S,
            controls=[
                ft.Text(
                    "This receipt photo couldn't be loaded.", color=ft.Colors.ERROR
                ),
                ft.TextButton("Try again", on_click=load),
            ],
        )
    if not loaded or loaded[0] != receipt_ref:
        return ft.Container(
            height=height, alignment=ft.Alignment.CENTER, content=ft.ProgressRing()
        )
    return ft.Image(
        src=loaded[1],
        height=height,
        fit=ft.BoxFit.CONTAIN,
        border_radius=theme.Radius.M,
        semantics_label="Photo of expense receipt",
        error_content=ft.Text(
            "This image format can't be displayed. "
            "Edit the expense and choose a JPEG or PNG photo.",
            color=ft.Colors.ERROR,
        ),
    )
