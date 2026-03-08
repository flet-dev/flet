import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ExpansionPanelList(
            controls=[ft.ExpansionPanel(ft.Text("Expansion Panel"))],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_scrollable_many_panels_and_change_event(flet_app: ftt.FletTestApp):
    changes: list[tuple[int, bool]] = []
    flet_app.resize_page(400, 500)

    flet_app.page.add(
        ft.Column(
            expand=True,
            controls=[
                panel_list := ft.ExpansionPanelList(
                    expand=True,
                    scroll=ft.ScrollMode.ALWAYS,
                    on_change=lambda e: changes.append((e.index, e.expanded)),
                    controls=[
                        ft.ExpansionPanel(
                            can_tap_header=True,
                            header=ft.Text(f"Panel {i + 1}"),
                            content=ft.Text(f"Details {i + 1}"),
                        )
                        for i in range(35)
                    ],
                )
            ],
        )
    )
    await flet_app.tester.pump_and_settle()

    assert panel_list.scroll == ft.ScrollMode.ALWAYS
    assert panel_list.controls[0].expanded is False

    await flet_app.tester.tap((await flet_app.tester.find_by_text("Panel 1")).first)
    await flet_app.tester.pump_and_settle()

    assert panel_list.controls[0].expanded is True
    assert changes == [(0, True)]

    await flet_app.tester.tap((await flet_app.tester.find_by_text("Panel 1")).first)
    await flet_app.tester.pump_and_settle()

    assert panel_list.controls[0].expanded is False
    assert changes == [(0, True), (0, False)]
