import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.tabs import basic, custom_indicator, nested


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Tabs(
            length=3,
            selected_index=1,
            content=ft.TabBar(
                tabs=[
                    ft.Tab(label="Tab 1", icon=ft.Icons.SETTINGS),
                    ft.Tab(label="Tab 2", icon=ft.Icons.SETTINGS_PHONE),
                    ft.Tab(label="Tab 3", icon=ft.Icons.SETTINGS_APPLICATIONS),
                ]
            ),
        ),
    )


# @pytest.mark.asyncio(loop_scope="function")
# async def test_basic(flet_app_function: ftt.FletTestApp, request):
#     flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
#     await flet_app_function.assert_control_screenshot(
#         request.node.name,
#         ft.Tabs(
#             animation_duration=0,
#             selected_index=1,
#             length=3,
#             expand=True,
#             content=ft.Column(
#                 expand=True,
#                 controls=[
#                     ft.TabBar(
#                         tabs=[
#                             ft.Tab(label="Tab 1", icon=ft.Icons.SETTINGS_PHONE),
#                             ft.Tab(label="Tab 2", icon=ft.Icons.SETTINGS),
#                             ft.Tab(
#                                 label=ft.CircleAvatar(
#                                     foreground_image_src="https://avatars.githubusercontent.com/u/102273996?s=200&amp;v=4",
#                                 ),
#                             ),
#                         ]
#                     ),
#                     ft.TabBarView(
#                         expand=True,
#                         controls=[
#                             ft.Container(
#                                 content=ft.Text("This is Tab 1"),
#                                 alignment=ft.Alignment.CENTER,
#                             ),
#                             ft.Container(
#                                 content=ft.Text("This is Tab 2"),
#                                 alignment=ft.Alignment.CENTER,
#                             ),
#                             ft.Container(
#                                 content=ft.Text("This is Tab 3"),
#                                 alignment=ft.Alignment.CENTER,
#                             ),
#                         ],
#                     ),
#                 ],
#             ),
#         ),
#     )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "basic",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": custom_indicator.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_custom_indicator(flet_app_function: ftt.FletTestApp):
#     flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
#     flet_app_function.page.enable_screenshots = True
#     flet_app_function.page.window.width = 350
#     flet_app_function.page.window.height = 300
#     await flet_app_function.tester.pump_and_settle()
#     flet_app_function.assert_screenshot(
#         "custom_indicator",
#         await flet_app_function.take_page_controls_screenshot(),
#     )


# @pytest.mark.parametrize(
#     "flet_app_function",
#     [{"flet_app_main": nested.main}],
#     indirect=True,
# )
# @pytest.mark.asyncio(loop_scope="function")
# async def test_nested(flet_app_function: ftt.FletTestApp):
#     flet_app_function.page.enable_screenshots = True

#     flet_app_function.assert_screenshot(
#         "nested",
#         await flet_app_function.take_page_controls_screenshot(
#             pixel_ratio=flet_app_function.screenshots_pixel_ratio
#         ),
#     )
