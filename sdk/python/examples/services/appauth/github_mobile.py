"""
Mobile GitHub OAuth via page.login + flet-appauth.

Requires:
  - flet-appauth installed
  - [tool.flet.appauth] redirect_scheme matching provider.redirect_url
  - GITHUB_CLIENT_ID / GITHUB_CLIENT_SECRET env vars
"""

import os

import flet as ft
from flet.auth.providers import GitHubOAuthProvider

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
assert GITHUB_CLIENT_ID, "set GITHUB_CLIENT_ID environment variable"
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
assert GITHUB_CLIENT_SECRET, "set GITHUB_CLIENT_SECRET environment variable"


def main(page: ft.Page):
    provider = GitHubOAuthProvider(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        # Must match tool.flet.appauth.redirect_scheme + path registered with GitHub
        redirect_url="myapp://oauth-callback",
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

    page.add(ft.Button("Sign in with GitHub", on_click=login_click))


ft.run(main)
