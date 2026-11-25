"""
Mobile OAuth via page.login + flet-appauth (public native client + PKCE).

Use an IdP that supports a public client with PKCE and an empty client secret
(for example Pocket ID, Auth0 native/public app, or similar). Do not use GitHub
here: GitHub still requires a client secret for the authorization-code exchange,
and that secret must not be embedded in a packaged Flet app.

Requires:
  - flet-appauth installed
  - IdP redirect URI matching the AppAuth scheme (default: flet://oauth-callback)
  - AUTH_ISSUER_URL / OIDC_CLIENT_ID env vars (no client secret)
"""

import os
from urllib.parse import urljoin

import flet as ft
from flet.auth import OAuthProvider

ISSUER = os.getenv("AUTH_ISSUER_URL", "").rstrip("/")
CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "").strip()
assert ISSUER and CLIENT_ID, "set AUTH_ISSUER_URL and OIDC_CLIENT_ID"


def main(page: ft.Page):
    provider = OAuthProvider(
        client_id=CLIENT_ID,
        client_secret="",  # public native client
        authorization_endpoint=urljoin(ISSUER + "/", "authorize"),
        token_endpoint=urljoin(ISSUER + "/", "api/oidc/token"),
        # Default AppAuth scheme is "flet" (override via tool.flet.appauth.redirect_scheme)
        redirect_url="flet://oauth-callback",
        scopes=["openid", "profile", "email"],
        user_endpoint=urljoin(ISSUER + "/", "api/oidc/userinfo"),
        user_id_fn=lambda u: u.get("sub") or u.get("id") or "",
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

    page.add(ft.Button("Sign in", on_click=login_click))


ft.run(main)
