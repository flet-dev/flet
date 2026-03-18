"""Splats — catch-all routes with :path*."""

import flet as ft


@ft.component
def Home():
    return ft.Column(
        [
            ft.Text("File Browser Demo", size=24),
            ft.Button(
                "Browse /files/docs/readme.md",
                on_click=lambda: ft.context.page.navigate("/files/docs/readme.md"),
            ),
            ft.Button(
                "Browse /files/images/photo.png",
                on_click=lambda: ft.context.page.navigate("/files/images/photo.png"),
            ),
            ft.Button(
                "Browse /files",
                on_click=lambda: ft.context.page.navigate("/files"),
            ),
        ]
    )


@ft.component
def FileBrowser():
    params = ft.use_route_params()
    file_path = params.get("path", "(root)")
    return ft.Column(
        [
            ft.Text("File Browser", size=24),
            ft.Text(f"Current path: {file_path}"),
            ft.Text(f"All params: {params}"),
            ft.Button(
                "Home",
                on_click=lambda: ft.context.page.navigate("/"),
            ),
        ]
    )


@ft.component
def App():
    return ft.Router(
        [
            ft.Route(index=True, component=Home),
            ft.Route(path="files/:path*", component=FileBrowser),
        ]
    )


ft.run(lambda page: page.render(App))
