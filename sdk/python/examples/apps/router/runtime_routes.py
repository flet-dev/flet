"""Runtime routes — adding and removing routes dynamically."""

import flet as ft


@ft.component
def Home():
    return ft.Text("Home page", size=24)


@ft.component
def About():
    return ft.Text("About page", size=24)


@ft.component
def Admin():
    return ft.Text("Admin panel (dynamically added!)", size=24)


@ft.component
def App():
    routes, set_routes = ft.use_state(
        [
            ft.Route(index=True, component=Home),
            ft.Route(path="about", component=About),
        ]
    )

    admin_added, set_admin_added = ft.use_state(False)

    def add_admin():
        set_routes(lambda r: r + [ft.Route(path="admin", component=Admin)])
        set_admin_added(True)

    def remove_admin():
        ft.context.page.navigate("/")
        set_routes(lambda r: [route for route in r if route.path != "admin"])
        set_admin_added(False)

    return ft.Column(
        [
            ft.Row(
                [
                    ft.Button(
                        "Home",
                        on_click=lambda: ft.context.page.navigate("/"),
                    ),
                    ft.Button(
                        "About",
                        on_click=lambda: ft.context.page.navigate("/about"),
                    ),
                    *(
                        [
                            ft.Button(
                                "Admin",
                                on_click=lambda: ft.context.page.navigate("/admin"),
                            )
                        ]
                        if admin_added
                        else []
                    ),
                ]
            ),
            ft.Row(
                [
                    ft.Button(
                        "Add Admin Route",
                        on_click=lambda: add_admin(),
                        disabled=admin_added,
                    ),
                    ft.Button(
                        "Remove Admin Route",
                        on_click=lambda: remove_admin(),
                        disabled=not admin_added,
                    ),
                ]
            ),
            ft.Divider(),
            ft.Router(routes),
        ]
    )


ft.run(lambda page: page.render(App))
