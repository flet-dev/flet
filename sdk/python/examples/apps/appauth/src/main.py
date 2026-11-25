"""
Auth0 native OAuth (PKCE, no client secret) via page.login + flet-appauth.

Create a Native application in Auth0 (public client). Register the callback
URI below. Do not use a Regular Web Application that requires a client secret.

Build (from this directory):

  uv venv
  uv pip install -e ../../../packages/flet -e ../../../packages/flet-cli \\
    -e ../../../packages/flet-desktop -e ../../../packages/flet-appauth \\
    -e ../../../packages/flet-platform-assets
  # Copy .env.example → .env and fill AUTH0_DOMAIN / AUTH0_CLIENT_ID
  .venv/Scripts/flet.exe build apk -v --yes   # Windows
  # .venv/bin/flet build apk -v --yes         # macOS/Linux

IdP callback URL: flet://oauth-callback
"""

from __future__ import annotations

import os
from pathlib import Path

import flet as ft
from flet.auth.providers import Auth0OAuthProvider

REDIRECT_URL = "flet://oauth-callback"


def _load_dotenv() -> None:
    """Load src/.env into os.environ (packaged via tool.flet.app.include)."""
    path = Path(__file__).resolve().parent / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = value.strip().strip("'").strip('"')


_load_dotenv()


def build_provider() -> Auth0OAuthProvider:
    domain = os.environ.get("AUTH0_DOMAIN", "").strip().removeprefix("https://").rstrip("/")
    client_id = os.environ.get("AUTH0_CLIENT_ID", "").strip()
    if not domain or not client_id:
        raise RuntimeError(
            "Set AUTH0_DOMAIN and AUTH0_CLIENT_ID in .env "
            "(Auth0 Native app; no client secret)."
        )
    audience = os.environ.get("AUTH0_AUDIENCE", "").strip() or None
    return Auth0OAuthProvider(
        domain=domain,
        client_id=client_id,
        client_secret="",  # public native client + PKCE
        redirect_url=os.environ.get("AUTH0_REDIRECT_URL", REDIRECT_URL),
        audience=audience,
    )


async def main(page: ft.Page) -> None:
    page.title = "AppAuth"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    status = ft.Text("Sign in with Auth0", size=16)
    error = ft.Text("", color=ft.Colors.RED)

    async def on_login(e: ft.LoginEvent) -> None:
        if e.error:
            error.value = f"{e.error}: {e.error_description or ''}".strip(": ")
            page.update()
            return
        user = page.auth.user if page.auth else None
        who = getattr(user, "email", None) or getattr(user, "name", None) or user
        status.value = f"Signed in as {who}"
        error.value = ""
        login_btn.visible = False
        logout_btn.visible = True
        page.update()

    async def login_click(_e: ft.ControlEvent) -> None:
        error.value = ""
        page.update()
        try:
            provider = build_provider()
        except RuntimeError as ex:
            error.value = str(ex)
            page.update()
            return
        await page.login(provider, fetch_user=True)

    def logout_click(_e: ft.ControlEvent) -> None:
        page.logout()
        status.value = "Sign in with Auth0"
        login_btn.visible = True
        logout_btn.visible = False
        page.update()

    page.on_login = on_login
    login_btn = ft.FilledButton(content="Sign in with Auth0", on_click=login_click)
    logout_btn = ft.OutlinedButton(
        content="Sign out", on_click=logout_click, visible=False
    )
    page.add(
        ft.Text("AppAuth (Auth0 native)", size=20, weight=ft.FontWeight.BOLD),
        status,
        login_btn,
        logout_btn,
        error,
        ft.Text(
            f"redirect={os.environ.get('AUTH0_REDIRECT_URL', REDIRECT_URL)}",
            size=11,
            color=ft.Colors.ON_SURFACE_VARIANT,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
