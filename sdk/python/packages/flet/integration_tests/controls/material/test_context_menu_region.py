import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_primary_select(flet_app: ftt.FletTestApp):
    status = ft.Text("idle", key="status")

    def handle_select(e: ft.ContextMenuEvent):
        status.value = e.item_key
        e.page.update()

    region = ft.ContextMenuRegion(
        primary_trigger=ft.ContextMenuTrigger.DOWN,
        primary_items=[
            ft.PopupMenuItem(content="Rename", key="rename"),
            ft.PopupMenuItem(content="Duplicate", key="duplicate"),
        ],
        on_select=handle_select,
        content=ft.Container(
            key="context-region",
            width=160,
            height=100,
            bgcolor=ft.Colors.SURFACE_VARIANT,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Primary menu"),
        ),
    )

    flet_app.page.add(status, region)
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap(await flet_app.tester.find_by_key("context-region"))
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap(await flet_app.tester.find_by_text("Rename"))
    await flet_app.tester.pump_and_settle()

    assert status.value == "rename"


@pytest.mark.asyncio(loop_scope="function")
async def test_dismiss_event(flet_app: ftt.FletTestApp):
    status = ft.Text("idle", key="status")

    def handle_dismiss(e: ft.ContextMenuEvent):
        status.value = e.reason
        e.page.update()

    region = ft.ContextMenuRegion(
        primary_trigger=ft.ContextMenuTrigger.DOWN,
        primary_items=[ft.PopupMenuItem(content="Rename", key="rename")],
        on_dismiss=handle_dismiss,
        content=ft.Container(
            key="context-region",
            width=160,
            height=100,
            bgcolor=ft.Colors.SURFACE_VARIANT,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Dismiss menu"),
        ),
    )

    flet_app.page.add(status, region)
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap(await flet_app.tester.find_by_key("context-region"))
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap(await flet_app.tester.find_by_key("status"))
    await flet_app.tester.pump_and_settle()

    assert status.value == "cancelled"
