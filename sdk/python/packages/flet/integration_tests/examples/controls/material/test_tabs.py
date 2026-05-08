import pytest

import examples.controls.material.tabs.basic.main as basic
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Tabs(
            selected_index=1,
            length=3,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Tab 1", icon=ft.Icons.SETTINGS_PHONE),
                            ft.Tab(label="Tab 2", icon=ft.Icons.SETTINGS),
                            ft.Tab(
                                label=ft.CircleAvatar(
                                    foreground_image_src="https://avatars.githubusercontent.com/u/102273996?s=200&amp;v=4",
                                ),
                            ),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text("This is Tab 1"),
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text("This is Tab 2"),
                            ),
                            ft.Container(
                                alignment=ft.Alignment.CENTER,
                                content=ft.Text("This is Tab 3"),
                            ),
                        ],
                    ),
                ],
            ),
        ),
        expand_screenshot=True,
    )


@pytest.mark.skip(reason="Will fix later")
@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.take_page_controls_screenshot(
            pump_times=10,
            pump_duration=1000,
        ),
    )
