"""Auth with dialog — shows a login dialog overlay when not authenticated."""

from dataclasses import dataclass

import flet as ft

AuthContext = ft.create_context(None)


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
    """Layout route that shows a login dialog when not authenticated."""
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()
    username_ref = ft.use_ref(None)

    def do_login():
        if auth is not None:
            auth.login(username_ref.current.value or "user")

    if auth is None or not auth.is_authenticated:
        return ft.Stack(
            [
                ft.Container(content=outlet, opacity=0.3),
                ft.Container(
                    content=ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text("Please log in", size=20),
                                    ft.TextField(
                                        label="Username",
                                        value="admin",
                                        ref=username_ref,
                                    ),
                                    ft.Button("Login", on_click=do_login),
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            padding=30,
                            width=300,
                        ),
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                ),
            ],
            expand=True,
        )

    return outlet


@ft.component
def App():
    auth, _ = ft.use_state(AuthState)

    return AuthContext(
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


ft.run(lambda page: page.render(App))
