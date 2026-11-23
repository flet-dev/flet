"""Consistent feedback for persistence failures."""

import logging

import flet as ft

log = logging.getLogger(f"app.{__name__}")


def show_message(text: str, action=None, on_action=None):
    ft.context.page.show_dialog(
        ft.SnackBar(
            ft.Text(text),
            action=action,
            on_action=on_action,
            duration=8000 if action else 4000,
        )
    )


async def run_action(action, error: str = "That didn't work. Please try again."):
    try:
        return True, await action
    except Exception:
        log.exception("Expense action failed")
        show_message(error)
        return False, None
