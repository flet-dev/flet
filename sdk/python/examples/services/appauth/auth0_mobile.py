"""
Mobile Auth0 OAuth via page.login + flet-appauth (native/public client + PKCE).

Create a Native application in Auth0. Register redirect URI
`flet://oauth-callback`. Leave client_secret empty — do not embed a secret
in a packaged Flet app.

Requires:
  - flet-appauth installed
  - AUTH0_DOMAIN / AUTH0_CLIENT_ID env vars
"""

import os

import flet as ft
from flet.auth.providers import Auth0OAuthProvider

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "").strip().removeprefix("https://").rstrip("/")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "").strip()
assert AUTH0_DOMAIN and AUTH0_CLIENT_ID, "set AUTH0_DOMAIN and AUTH0_CLIENT_ID"


def main(page: ft.Page):
    provider = Auth0OAuthProvider(
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret="",  # public native client
        # Default AppAuth scheme is "flet" (override via tool.flet.appauth.redirect_scheme)
        redirect_url="flet://oauth-callback",
        audience=os.getenv("AUTH0_AUDIENCE") or None,
    )

    async def on_login(e: ft.LoginEvent):
        if e.error:
            page.add(ft.Text(f"Login error: {e.error}"))
        else:
            page.add(ft.Text(f"Logged in as {page.auth.user}"))
        page.update()

    page.on_login = on_login

    async def login_click(e):
        await page.login(provider)

    page.add(ft.Button("Sign in with Auth0", on_click=login_click))


ft.run(main)
