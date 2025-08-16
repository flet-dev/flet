# @pytest.mark.asyncio(loop_scope="module")
# async def test_pagelet_basic(flet_app: ftt.FletTestApp, request):
#     flet_app.page.theme_mode = ft.ThemeMode.LIGHT
#     await flet_app.assert_control_screenshot(
#         request.node.name,
#         ft.Pagelet(
#             ft.Container(bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content"))
#         ),
#     )


# @pytest.mark.asyncio(loop_scope="module")
# async def test_pagelet_basic(flet_app: ftt.FletTestApp, request):
#     flet_app.page.theme_mode = ft.ThemeMode.LIGHT

#     flet_app.page.enable_screenshots = True
#     flet_app.page.window.width = 400
#     flet_app.page.window.height = 600
#     flet_app.page.add(
#         ft.Pagelet(
#             ft.Container(bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content"))
#         ),
#     )
#     flet_app.page.update()
#     await flet_app.tester.pump_and_settle()

#     flet_app.assert_screenshot(
#         "pagelet_basic",
#         await flet_app.page.take_screenshot(
#             pixel_ratio=flet_app.screenshots_pixel_ratio
#         ),
#     )
