import asyncio

import flet as ft


def main(page: ft.Page):
    page.title = "Routes Example"

    result_text = ft.Text("No result yet", size=18)

    def route_change():
        page.views.clear()

        # Home View (/)
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.SURFACE_BRIGHT),
                    result_text,
                    ft.Button(
                        "Start flow",
                        on_click=lambda _: asyncio.create_task(
                            page.push_route("/step1")
                        ),
                    ),
                ],
            )
        )

        if page.route == "/step1" or page.route == "/step2" or page.route == "/step3":
            page.views.append(
                ft.View(
                    route="/step1",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Step 1"),
                            bgcolor=ft.Colors.SURFACE_BRIGHT,
                        ),
                        ft.Text("Step 1 of the flow"),
                        ft.Button(
                            "Go to Step 2",
                            on_click=lambda _: asyncio.create_task(
                                page.push_route("/step2")
                            ),
                        ),
                    ],
                )
            )

        if page.route == "/step2" or page.route == "/step3":
            page.views.append(
                ft.View(
                    route="/step2",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Step 2"),
                            bgcolor=ft.Colors.SURFACE_BRIGHT,
                        ),
                        ft.Text("Step 2 of the flow"),
                        ft.Button(
                            "Go to Step 3",
                            on_click=lambda _: asyncio.create_task(
                                page.push_route("/step3")
                            ),
                        ),
                    ],
                )
            )

        if page.route == "/step3":
            page.views.append(
                ft.View(
                    route="/step3",
                    controls=[
                        ft.AppBar(
                            title=ft.Text("Step 3 (Final)"),
                            bgcolor=ft.Colors.SURFACE_BRIGHT,
                        ),
                        ft.Text("Flow complete!"),
                        ft.Button(
                            "Finish and go Home",
                            on_click=lambda _: asyncio.create_task(
                                page.pop_views_until("/", result="Flow completed!")
                            ),
                        ),
                    ],
                )
            )

        page.update()

    def on_pop_result(e: ft.ViewsPopUntilEvent):
        result_text.value = f"Result: {e.result}"
        page.show_dialog(ft.SnackBar(ft.Text(f"Got result: {e.result}")))
        page.update()

    async def view_pop(e: ft.ViewPopEvent):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.on_views_pop_until = on_pop_result

    route_change()


if __name__ == "__main__":
    ft.run(main)
