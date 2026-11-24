import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_semantics_identifier_is_independent_of_label(
    flet_app_function: ftt.FletTestApp,
):
    tapped = {"id": None}

    def handle_click(item_id: str):
        def _on_click(e):
            tapped["id"] = item_id

        return _on_click

    flet_app_function.page.add(
        ft.Column(
            controls=[
                ft.Semantics(
                    identifier="save_btn",
                    label="Submit",
                    content=ft.Button(
                        "Save",
                        on_click=handle_click("save_btn"),
                    ),
                ),
                ft.Semantics(
                    identifier="cancel_btn",
                    label="Submit",
                    content=ft.Button(
                        "Cancel",
                        on_click=handle_click("cancel_btn"),
                    ),
                ),
            ]
        )
    )
    await flet_app_function.tester.pump_and_settle()

    save = await flet_app_function.tester.find_by_semantics_identifier("save_btn")
    cancel = await flet_app_function.tester.find_by_semantics_identifier("cancel_btn")
    assert save.count == 1
    assert cancel.count == 1

    await flet_app_function.tester.tap(save)
    await flet_app_function.tester.pump_and_settle()
    assert tapped["id"] == "save_btn"

    await flet_app_function.tester.tap(cancel)
    await flet_app_function.tester.pump_and_settle()
    assert tapped["id"] == "cancel_btn"
