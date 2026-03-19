"""Featured Router example — layout, nav, nested routes, params, loaders, auth."""

from dataclasses import dataclass

import flet as ft

# ---------------------------------------------------------------------------
# Auth context
# ---------------------------------------------------------------------------


@ft.observable
@dataclass
class AuthState:
    is_authenticated: bool = False
    username: str = ""
    is_admin: bool = False

    def login(self, username, admin=False):
        self.username = username
        self.is_authenticated = True
        self.is_admin = admin

    def logout(self):
        self.username = ""
        self.is_authenticated = False
        self.is_admin = False


AuthContext: ft.ContextProvider[AuthState | None] = ft.create_context(None)


# ---------------------------------------------------------------------------
# Data loaders
# ---------------------------------------------------------------------------


def home_loader(params):
    return {"greeting": "Welcome to the Router Demo!", "featured_count": 3}


def projects_loader(params):
    return [
        {"id": 1, "name": "Flet", "status": "Active"},
        {"id": 2, "name": "Flutter", "status": "Active"},
        {"id": 3, "name": "FastAPI", "status": "Maintenance"},
    ]


def project_detail_loader(params):
    projects = {
        "1": {"id": 1, "name": "Flet", "description": "Build apps in Python"},
        "2": {"id": 2, "name": "Flutter", "description": "UI toolkit by Google"},
        "3": {"id": 3, "name": "FastAPI", "description": "Modern Python web framework"},
    }
    return projects.get(params.get("projectId"), {"name": "Unknown", "description": ""})


def settings_loader(params):
    return {"sections": ["Profile", "Security", "Notifications"]}


# ---------------------------------------------------------------------------
# Auth components
# ---------------------------------------------------------------------------


@ft.component
def LoginPage():
    auth = ft.use_context(AuthContext)
    username_ref = ft.use_ref(None)

    def handle_login():
        auth.login(username_ref.current.value or "user")
        ft.context.page.navigate("/")

    def handle_admin_login():
        auth.login(username_ref.current.value or "admin", admin=True)
        ft.context.page.navigate("/")

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Sign In", size=28),
                ft.TextField(label="Username", value="admin", ref=username_ref),
                ft.Row(
                    [
                        ft.Button("Login", on_click=handle_login),
                        ft.Button("Login as Admin", on_click=handle_admin_login),
                    ]
                ),
            ],
            width=300,
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )


@ft.component
def ProtectedRoute():
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()

    if not auth.is_authenticated:
        ft.context.page.navigate("/login")
        return ft.ProgressRing()

    return outlet


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------


@ft.component
def NavLink(label, path):
    active = ft.is_route_active(path)
    return ft.Container(
        content=ft.Text(
            label,
            weight=ft.FontWeight.BOLD if active else ft.FontWeight.NORMAL,
            color=ft.Colors.PRIMARY if active else ft.Colors.ON_SURFACE,
        ),
        bgcolor=ft.Colors.PRIMARY_CONTAINER if active else None,
        padding=ft.Padding.symmetric(horizontal=16, vertical=8),
        border_radius=8,
        on_click=lambda: ft.context.page.navigate(path),
    )


@ft.component
def AppLayout():
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()

    if auth is None:
        return ft.ProgressRing()

    return ft.Column(
        [
            # Header
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Router Demo", size=20, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                NavLink("Home", "/"),
                                NavLink("Projects", "/projects"),
                                NavLink("Settings", "/settings"),
                            ]
                        ),
                        ft.Row(
                            [
                                ft.Text(f"Hi, {auth.username}"),
                                ft.IconButton(
                                    ft.Icons.LOGOUT,
                                    on_click=lambda: (
                                        auth.logout(),
                                        ft.context.page.navigate("/login"),
                                    ),
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10,
                bgcolor=ft.Colors.SURFACE_BRIGHT,
            ),
            ft.Divider(height=1),
            # Content
            ft.Container(content=outlet, padding=20, expand=True),
        ],
        expand=True,
    )


# ---------------------------------------------------------------------------
# Page components
# ---------------------------------------------------------------------------


@ft.component
def Home():
    data = ft.use_route_loader_data()
    return ft.Column(
        [
            ft.Text(data["greeting"], size=24),
            ft.Text(f"{data['featured_count']} featured projects available"),
            ft.Button(
                "Browse projects",
                on_click=lambda: ft.context.page.navigate("/projects"),
            ),
        ]
    )


@ft.component
def ProjectsList():
    data = ft.use_route_loader_data()
    return ft.Column(
        [
            ft.Text("Projects", size=24),
            *[
                ft.ListTile(
                    title=ft.Text(p["name"]),
                    subtitle=ft.Text(p["status"]),
                    on_click=lambda _, pid=p["id"]: ft.context.page.navigate(
                        f"/projects/{pid}"
                    ),
                )
                for p in data
            ],
        ]
    )


@ft.component
def ProjectDetails():
    data = ft.use_route_loader_data()
    params = ft.use_route_params()
    location = ft.use_route_location()

    return ft.Column(
        [
            ft.Text(data["name"], size=24),
            ft.Text(data["description"]),
            ft.Text(f"Project ID: {params['projectId']}", italic=True),
            ft.Text(f"Location: {location}", italic=True, size=12),
            ft.Button(
                "Back to projects",
                on_click=lambda: ft.context.page.navigate("/projects"),
            ),
        ]
    )


@ft.component
def ProjectsLayout():
    outlet = ft.use_route_outlet()
    return ft.Column(
        [
            ft.Container(
                content=ft.Text(
                    "PROJECTS",
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_SECONDARY_CONTAINER,
                ),
                bgcolor=ft.Colors.SECONDARY_CONTAINER,
                padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                border_radius=4,
            ),
            outlet,
        ]
    )


@ft.component
def SettingsHome():
    data = ft.use_route_loader_data()
    return ft.Column(
        [
            ft.Text("Settings", size=24),
            ft.Text("Available sections:"),
            *[
                ft.ListTile(
                    title=ft.Text(section),
                    on_click=lambda _, s=section: ft.context.page.navigate(
                        f"/settings/{s.lower()}"
                    ),
                )
                for section in data["sections"]
            ],
        ]
    )


@ft.component
def SettingsSection():
    params = ft.use_route_params()
    return ft.Column(
        [
            ft.Text(f"{params['section'].title()} Settings", size=24),
            ft.Text(f"Configure your {params['section']} preferences here."),
            ft.Button(
                "Back to settings",
                on_click=lambda: ft.context.page.navigate("/settings"),
            ),
        ]
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------


@ft.component
def App():
    auth, _ = ft.use_state(AuthState)

    return ft.SafeArea(
        content=AuthContext(
            auth,
            lambda: ft.Router(
                [
                    ft.Route(path="login", component=LoginPage),
                    ft.Route(
                        component=ProtectedRoute,
                        children=[
                            ft.Route(
                                component=AppLayout,
                                children=[
                                    ft.Route(
                                        index=True,
                                        component=Home,
                                        loader=home_loader,
                                    ),
                                    ft.Route(
                                        path="projects",
                                        component=ProjectsLayout,
                                        children=[
                                            ft.Route(
                                                index=True,
                                                component=ProjectsList,
                                                loader=projects_loader,
                                            ),
                                            ft.Route(
                                                path=":projectId",
                                                component=ProjectDetails,
                                                loader=project_detail_loader,
                                            ),
                                        ],
                                    ),
                                    ft.Route(
                                        path="settings",
                                        children=[
                                            ft.Route(
                                                index=True,
                                                component=SettingsHome,
                                                loader=settings_loader,
                                            ),
                                            ft.Route(
                                                path=":section",
                                                component=SettingsSection,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
