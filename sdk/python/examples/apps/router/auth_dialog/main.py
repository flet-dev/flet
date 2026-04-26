"""Auth with AlertDialog — shows a modal login dialog when not authenticated."""

from dataclasses import dataclass

import flet as ft


@ft.observable
@dataclass
class AuthState:
    is_authenticated: bool = False
    username: str = ""

    def login(self, username):
        self.username = username
        self.is_authenticated = True

    def logout(self):
        self.username = ""
        self.is_authenticated = False


AuthContext: ft.ContextProvider[AuthState | None] = ft.create_context(None)


@ft.component
def Home():
    auth = ft.use_context(AuthContext)
    if auth is None:
        return ft.ProgressRing()
    return ft.Column(
        [
            ft.Text(f"Home — Hello, {auth.username}!", size=24),
            ft.Button("Logout", on_click=auth.logout),
        ]
    )


@ft.component
def AuthGuard():
    """Layout route that shows a modal AlertDialog when not authenticated."""
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()
    username_ref = ft.use_ref(None)
    page = ft.context.page

    def do_login():
        if auth is not None:
            auth.login(username_ref.current.value or "user")
            page.pop_dialog()

    def show_login():
        page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Please log in"),
                content=ft.TextField(
                    label="Username",
                    value="admin",
                    ref=username_ref,
                ),
                actions=[
                    ft.TextButton("Login", on_click=do_login),
                ],
            )
        )

    ft.use_effect(
        lambda: show_login() if auth is None or not auth.is_authenticated else None,
        [auth.is_authenticated if auth else None],
    )

    return outlet


@ft.component
def App():
    auth, _ = ft.use_state(AuthState)

    return ft.SafeArea(
        content=AuthContext(
            auth,
            lambda: ft.Router(
                [
                    ft.Route(
                        component=AuthGuard,
                        children=[
                            ft.Route(index=True, component=Home),
                        ],
                    ),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
