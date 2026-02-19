#
# Run this example with:
#   export LINKEDIN_CLIENT_ID=<your_linkedin_oauth_app_client_id>
#   export LINKEDIN_CLIENT_SECRET=<your_linkedin_oauth_app_client_secret>
#   flet run --web --port 8550 linkedin_login.py
#
import os

import flet as ft
from flet.auth import OAuthProvider


def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    assert value, f"set {name} environment variable"
    return value


def main(page: ft.Page):
    provider = OAuthProvider(
        client_id=get_env_variable("LINKEDIN_CLIENT_ID"),
        client_secret=get_env_variable("LINKEDIN_CLIENT_SECRET"),
        authorization_endpoint="https://www.linkedin.com/oauth/v2/authorization",
        token_endpoint="https://www.linkedin.com/oauth/v2/accessToken",
        user_endpoint="https://api.linkedin.com/v2/me",
        user_scopes=["r_liteprofile", "r_emailaddress"],
        user_id_fn=lambda u: u["id"],
        redirect_url="http://127.0.0.1:8550/oauth_callback",
    )

    async def login_click(e):
        await page.login(provider)

    async def on_login(e):
        if e.error:
            page.add(ft.Text(f"Login error: {e.error}"))
        else:
            access_token = (await page.auth.get_token()).access_token
            page.add(
                ft.Text(f"Access token: {access_token}"),
                ft.Text(f"User ID: {page.auth.user.id}"),
            )

    page.on_login = on_login
    page.add(ft.Button("Login with LinkedIn", on_click=login_click))


ft.run(main)
