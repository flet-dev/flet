#
# Run this example with:
#   export GITHUB_CLIENT_ID=<your_github_oauth_app_client_id>
#   export GITHUB_CLIENT_SECRET=<your_github_oauth_app_client_secret>
#   flet run --web --port 8550 github_check_auth_results_and_toggle_ui.py
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

    async def login_button_click(e):
        await page.login(provider, scope=["public_repo"])

    def on_login(e: ft.LoginEvent):
        if not e.error:
            toggle_login_buttons()

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None

    login_button = ft.Button("Login with GitHub", on_click=login_button_click)
    logout_button = ft.Button("Logout", on_click=logout_button_click)
    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button)


ft.run(main)
