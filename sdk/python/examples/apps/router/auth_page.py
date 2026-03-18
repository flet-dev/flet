"""Auth with page redirect — guards protected routes behind a login page."""

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
def LoginPage():
    auth = ft.use_context(AuthContext)
    username_ref = ft.use_ref("")

    def handle_login():
        auth.login(username_ref.current.value or "user")
        ft.context.page.navigate("/dashboard")

    return ft.Column(
        [
            ft.Text("Login", size=24),
            ft.TextField(label="Username", value="admin", ref=username_ref),
            ft.Button("Sign In", on_click=handle_login),
        ]
    )


@ft.component
def Dashboard():
    auth = ft.use_context(AuthContext)
    return ft.Column(
        [
            ft.Text(f"Dashboard — Welcome, {auth.username}!", size=24),
            ft.Button(
                "Logout",
                on_click=lambda: (
                    auth.logout(),
                    ft.context.page.navigate("/login"),
                ),
            ),
        ]
    )


@ft.component
def ProtectedRoute():
    """Layout route that redirects to /login when not authenticated."""
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()

    if not auth.is_authenticated:
        ft.context.page.navigate("/login")
        return ft.Text("Redirecting to login...")

    return outlet


@ft.component
def App():
    auth, _ = ft.use_state(AuthState)

    return AuthContext(
        auth,
        lambda: ft.Router(
            [
                ft.Route(path="login", component=LoginPage),
                ft.Route(
                    component=ProtectedRoute,
                    children=[
                        ft.Route(index=True, component=Dashboard),
                        ft.Route(path="dashboard", component=Dashboard),
                    ],
                ),
            ]
        ),
    )


ft.run(lambda page: page.render(App))
