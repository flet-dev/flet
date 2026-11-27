"""Optional receipt draft: photo picker, phone camera, preview and removal."""

import logging

import theme
from components.receipt_camera import ReceiptCamera
from components.receipt_image import ReceiptImage
from models import ExpenseDraft
from services.receipts import ReceiptError
from state import StateContext

import flet as ft

log = logging.getLogger(f"app.{__name__}")


@ft.component
def ExpenseReceipt(draft: ExpenseDraft, saving: bool, edit, on_busy):
    state = ft.use_context(StateContext)
    picking, set_picking = ft.use_state(False)
    camera_open, set_camera_open = ft.use_state(False)
    error, set_error = ft.use_state("")
    attached = draft.receipt_data is not None or bool(draft.receipt_ref)

    def captured(data: bytes):
        set_camera_open(False)
        try:
            edit(receipt_data=state.validate_receipt_photo(data), receipt_ref=None)
            set_error("")
        except ReceiptError as exc:
            set_error(str(exc))
        except Exception:
            log.exception("Receipt capture could not be attached")
            set_error("Couldn't attach this photo. Please try another one.")

    async def pick():
        if picking or saving:
            return
        set_error("")
        set_picking(True)
        on_busy(True)
        try:
            data = await state.pick_receipt_photo()
            if data is not None:
                edit(receipt_data=data, receipt_ref=None)
        except ReceiptError as exc:
            set_error(str(exc))
        except Exception:
            log.exception("Receipt picker failed")
            set_error(
                "Couldn't open your photos. Check photo access in your phone's "
                "Settings and try again."
            )
        finally:
            set_picking(False)
            on_busy(False)

    def remove():
        edit(receipt_data=None, receipt_ref=None)
        set_error("")

    ft.use_dialog(
        ft.BottomSheet(
            show_drag_handle=True,
            scrollable=True,
            use_safe_area=True,
            on_dismiss=lambda: set_camera_open(False),
            content=ft.Container(
                padding=theme.Space.L,
                content=ReceiptCamera(
                    on_capture=captured,
                    on_close=lambda: set_camera_open(False),
                ),
            ),
        )
        if camera_open
        else None
    )
    preview = (
        ft.Image(
            src=draft.receipt_data,
            height=theme.RECEIPT_PREVIEW_HEIGHT,
            fit=ft.BoxFit.CONTAIN,
            border_radius=theme.Radius.M,
            semantics_label="Attached receipt preview",
            error_content=ft.Text(
                "This photo can't be displayed. Choose a JPEG or PNG photo instead.",
                color=ft.Colors.ERROR,
            ),
        )
        if draft.receipt_data is not None
        else ReceiptImage(
            draft.receipt_ref,
            height=theme.RECEIPT_PREVIEW_HEIGHT,
        )
        if draft.receipt_ref
        else None
    )
    return ft.Container(
        padding=theme.Space.L,
        border_radius=theme.Radius.L,
        border=ft.Border.all(theme.LINE_WIDTH, ft.Colors.OUTLINE),
        content=ft.Column(
            tight=True,
            spacing=theme.Space.M,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Receipt photo (optional)", theme_style=theme.Text.TITLE),
                *([preview] if preview else []),
                ft.OutlinedButton(
                    "Opening photos…"
                    if picking
                    else "Replace photo"
                    if attached
                    else "Choose from photos",
                    icon=ft.Icons.PHOTO_LIBRARY,
                    disabled=saving or picking,
                    on_click=pick,
                ),
                *(
                    [
                        ft.OutlinedButton(
                            "Take a photo",
                            icon=ft.Icons.PHOTO_CAMERA,
                            disabled=saving or picking,
                            on_click=lambda: set_camera_open(True),
                        )
                    ]
                    if state.can_take_receipt_photo()
                    else [
                        ft.Text(
                            "Taking photos is available in the installed phone "
                            "app. You can choose an image here.",
                            theme_style=theme.Text.LABEL,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ]
                ),
                *(
                    [
                        ft.TextButton(
                            "Remove receipt",
                            icon=ft.Icons.CLOSE,
                            disabled=saving or picking,
                            on_click=remove,
                        )
                    ]
                    if attached
                    else []
                ),
                *([ft.Text(error, color=ft.Colors.ERROR)] if error else []),
            ],
        ),
    )
