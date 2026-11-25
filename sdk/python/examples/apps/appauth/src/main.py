"""
Public native OAuth (PKCE, no client secret) via page.login + flet-appauth.

Uses a generic OIDC provider (e.g. Pocket ID) registered as a public native
client. GitHub is not used here — GitHub still requires a client secret for
token exchange, which must not ship inside a packaged app.

Build (from this directory):

  uv venv
  uv pip install -e ../../../packages/flet -e ../../../packages/flet-cli \\
    -e ../../../packages/flet-desktop -e ../../../packages/flet-appauth \\
    -e ../../../packages/flet-platform-assets
  # Copy .env.example → .env and fill AUTH_ISSUER_URL / OIDC_CLIENT_ID
  .venv/Scripts/flet.exe build apk -v --yes   # Windows
  # .venv/bin/flet build apk -v --yes         # macOS/Linux

IdP callback URL: flet://oauth-callback
"""

from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import urljoin

import flet as ft
from flet.auth import OAuthProvider

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


def build_provider() -> OAuthProvider:
    issuer = os.environ.get("AUTH_ISSUER_URL", "").rstrip("/")
    client_id = os.environ.get("OIDC_CLIENT_ID", "").strip()
    if not issuer or not client_id:
        raise RuntimeError(
            "Set AUTH_ISSUER_URL and OIDC_CLIENT_ID in .env "
            "(public native client; no client secret)."
        )
    return OAuthProvider(
        client_id=client_id,
        client_secret="",  # public native client + PKCE
        authorization_endpoint=urljoin(issuer + "/", "authorize"),
        token_endpoint=urljoin(issuer + "/", "api/oidc/token"),
        redirect_url=os.environ.get("OIDC_ANDROID_REDIRECT", REDIRECT_URL),
        scopes=os.environ.get("OIDC_SCOPES", "openid profile email").split(),
        user_endpoint=urljoin(issuer + "/", "api/oidc/userinfo"),
        user_id_fn=lambda u: u.get("sub") or u.get("id") or "",
    )


async def main(page: ft.Page) -> None:
    page.title = "AppAuth"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    status = ft.Text("Sign in with a public OIDC client", size=16)
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
        status.value = "Sign in with a public OIDC client"
        login_btn.visible = True
        logout_btn.visible = False
        page.update()

    page.on_login = on_login
    login_btn = ft.FilledButton(content="Sign in", on_click=login_click)
    logout_btn = ft.OutlinedButton(
        content="Sign out", on_click=logout_click, visible=False
    )
    page.add(
        ft.Text("AppAuth (public PKCE client)", size=20, weight=ft.FontWeight.BOLD),
        status,
        login_btn,
        logout_btn,
        error,
        ft.Text(
            f"redirect={os.environ.get('OIDC_ANDROID_REDIRECT', REDIRECT_URL)}",
            size=11,
            color=ft.Colors.ON_SURFACE_VARIANT,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
