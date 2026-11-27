"""
Mobile Auth0 OAuth via page.login + core WebAuth (native/public client + PKCE).

Create a Native application in Auth0. Register a callback URI that matches
the WebAuth scheme from ``flet build`` (default ``<bundle id>.auth``).
Example: ``dev.flet.auth0-mobile.auth://callback``. Leave client_secret
empty — do not embed a secret in a packaged Flet app.

Requires:
  - AUTH0_DOMAIN / AUTH0_CLIENT_ID env vars (e.g. via python-dotenv + .env)
"""

import os

import flet as ft
from flet.auth.providers import Auth0OAuthProvider

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "").strip().removeprefix("https://").rstrip("/")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "").strip()
assert AUTH0_DOMAIN and AUTH0_CLIENT_ID, "set AUTH0_DOMAIN and AUTH0_CLIENT_ID"

# Must match tool.flet.web_auth.callback_scheme / --web-auth-callback-scheme
# ("WebAuth callback scheme: …").
CALLBACK_SCHEME = os.getenv("WEBAUTH_CALLBACK_SCHEME", "dev.flet.auth0-mobile.auth")


def main(page: ft.Page):
    provider = Auth0OAuthProvider(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret="",  # public native client
        redirect_url=f"{CALLBACK_SCHEME}://callback",
        audience=os.getenv("AUTH0_AUDIENCE") or None,
    )

    status = ft.Text()

    async def on_login(e: ft.LoginEvent):
        if e.error:
            status.value = f"Login error: {e.error}"
        else:
            status.value = f"Logged in as {page.auth.user}"

    page.on_login = on_login

    async def login_click(e):
        await page.login(provider, callback_scheme=CALLBACK_SCHEME)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button("Sign in with Auth0", on_click=login_click),
                    status,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
