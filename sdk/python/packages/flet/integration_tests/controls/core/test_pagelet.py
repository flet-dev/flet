# @pytest.mark.asyncio(loop_scope="module")
# async def test_pagelet_basic(flet_app: ftt.FletTestApp, request):
#     await flet_app.assert_control_screenshot(
#         request.node.name,
#         ft.Pagelet(
#             ft.Container(bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content"))
#         ),
#     )


# @pytest.mark.asyncio(loop_scope="module")
# async def test_pagelet_basic(flet_app: ftt.FletTestApp, request):

#     flet_app.page.enable_screenshots = True
#     flet_app.resize_page(400, 300)
#     flet_app.page.add(
#         ft.Pagelet(
#             ft.Container(bgcolor=ft.Colors.AMBER, content=ft.Text("Pagelet Content"))
#         ),
#     )
#     await flet_app.tester.pump_and_settle()

#     flet_app.assert_screenshot(
#         "pagelet_basic",
#         await flet_app.page.take_screenshot(
#             pixel_ratio=flet_app.screenshots_pixel_ratio
#         ),
#     )
