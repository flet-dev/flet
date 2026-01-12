#
# Run this example with:
#   export GITHUB_CLIENT_ID=<your_github_oauth_app_client_id>
#   export GITHUB_CLIENT_SECRET=<your_github_oauth_app_client_secret>
#   flet run --web --port 8550 github_login_same_page.py
#
import os

import flet as ft
from flet.auth.providers import GitHubOAuthProvider


def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    assert value, f"set {name} environment variable"
    return value


def main(page: ft.Page):
    provider = GitHubOAuthProvider(
        client_id=get_env_variable("GITHUB_CLIENT_ID"),
        client_secret=get_env_variable("GITHUB_CLIENT_SECRET"),
        redirect_url="http://127.0.0.1:8550/oauth_callback",
    )

    async def login_click(e):
        await page.login(
            provider,
            redirect_to_page=True,
            on_open_authorization_url=lambda url: ft.UrlLauncher().launch_url(
                ft.Url(url, target=ft.UrlTarget.SELF)
            ),
        )

    async def on_login(e):
        page.add(
            ft.Text(f"Login error: {e.error}"),
            ft.Text(f"User ID: {page.auth.user.id}"),
        )

    page.on_login = on_login
    page.add(ft.Button("Login with GitHub", on_click=login_click))


ft.run(main)
