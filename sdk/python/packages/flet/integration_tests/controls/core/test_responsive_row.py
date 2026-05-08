import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_responsive_row_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ResponsiveRow(
            controls=[
                ft.TextField(label="TextField 1"),
                ft.TextField(label="TextField 2"),
                ft.TextField(label="TextField 3"),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_unbounded_width(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            controls=[
                ft.ResponsiveRow(
                    controls=[
                        ft.Text("Item 1"),
                        ft.Text("Item 2"),
                    ]
                )
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_zero_col_controls_are_hidden_at_breakpoint(
    flet_app: ftt.FletTestApp, request
):
    flet_app.resize_page(360, 240)
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 0, "xl": 2},
                    bgcolor=ft.Colors.GREEN,
                    content=ft.Text("Left"),
                ),
                ft.Container(
                    col={"xs": 12, "xl": 8},
                    bgcolor=ft.Colors.RED,
                    content=ft.Text("Center"),
                ),
                ft.Container(
                    col={"xs": 0, "xl": 2},
                    bgcolor=ft.Colors.BLUE,
                    content=ft.Text("Right"),
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_scroll_to(flet_app: ftt.FletTestApp):
    events = []

    def on_scroll(e: ft.OnScrollEvent):
        events.append(e)

    flet_app.page.add(
        row := ft.ResponsiveRow(
            height=120,
            width=320,
            scroll=ft.ScrollMode.HIDDEN,
            on_scroll=on_scroll,
            controls=[
                ft.Container(
                    col=12,
                    height=70,
                    bgcolor=ft.Colors.BLUE_50,
                    content=ft.Text(f"Item {i}"),
                )
                for i in range(6)
            ],
        )
    )
    await flet_app.tester.pump_and_settle()

    await row.scroll_to(offset=160, duration=0)
    await flet_app.tester.pump_and_settle()

    assert events
    assert events[-1].pixels > 0
