"""Mobile page.login uses AppAuth; requires flet-appauth; skips web oauth_authorize."""

from __future__ import annotations

import asyncio
import sys
import types
from typing import Any
from unittest.mock import AsyncMock

import pytest

from flet.auth.authorization_service import AuthorizationService
from flet.auth.oauth_provider import OAuthProvider
from flet.controls.page import LoginEvent
from flet.controls.types import PagePlatform
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _Conn(Connection):
    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.page_name = "/"
        self.oauth_authorize_calls: list[dict[str, Any]] = []

    def send_message(self, message):
        pass

    def oauth_authorize(self, attrs: dict[str, Any]):
        self.oauth_authorize_calls.append(attrs)


def _make_provider(**kwargs) -> OAuthProvider:
    return OAuthProvider(
        client_id="cid",
        client_secret="csecret",
        authorization_endpoint="https://example.com/authorize",
        token_endpoint="https://example.com/token",
        redirect_url="myapp://oauth-callback",
        code_verifier="python-verifier-should-be-ignored",
        code_challenge="python-challenge",
        code_challenge_method="S256",
        **kwargs,
    )


def _install_fake_appauth(monkeypatch, authorize_result: dict[str, Any]):
    class FakeAppAuth:
        def __init__(self):
            self.authorize_calls = []

        async def authorize(self, **kwargs):
            self.authorize_calls.append(kwargs)
            return authorize_result

    fake_mod = types.ModuleType("flet_appauth")
    fake_appauth = FakeAppAuth()
    fake_mod.AppAuth = lambda: fake_appauth  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "flet_appauth", fake_mod)
    return fake_appauth


@pytest.mark.asyncio
async def test_login_android_missing_flet_appauth_raises(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID

    real_import = __import__

    def fake_import(name, *args, **kwargs):
        if name == "flet_appauth" or name.startswith("flet_appauth."):
            raise ModuleNotFoundError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr("builtins.__import__", fake_import)

    with pytest.raises(RuntimeError, match="flet-appauth"):
        await page.login(_make_provider())

    assert conn.oauth_authorize_calls == []


@pytest.mark.asyncio
async def test_login_android_appauth_success_skips_oauth_authorize(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    login_events: list[LoginEvent] = []

    async def on_login(e: LoginEvent):
        login_events.append(e)

    page.on_login = on_login

    fake_appauth = _install_fake_appauth(
        monkeypatch,
        {
            "authorization_code": "auth-code",
            "code_verifier": "appauth-verifier",
        },
    )

    async def fake_request_token(self, code: str):
        assert code == "auth-code"
        assert self.provider.code_verifier == "appauth-verifier"

    monkeypatch.setattr(AuthorizationService, "request_token", fake_request_token)

    provider = _make_provider()
    auth = await page.login(
        provider,
        on_open_authorization_url=AsyncMock(),
        complete_page_html="<html/>",
        redirect_to_page=True,
    )

    assert conn.oauth_authorize_calls == []
    assert fake_appauth.authorize_calls, "AppAuth.authorize should be called"
    call = fake_appauth.authorize_calls[0]
    assert call["client_id"] == "cid"
    assert call["redirect_url"] == "myapp://oauth-callback"
    assert "code_challenge" not in call or call.get("code_challenge") is None
    # Provider PKCE fields must not be permanently mutated for shared reuse.
    assert provider.code_verifier == "python-verifier-should-be-ignored"
    assert provider.code_challenge == "python-challenge"
    assert provider.code_challenge_method == "S256"
    assert auth is page.auth

    await asyncio.sleep(0)
    assert login_events
    assert not login_events[0].error


@pytest.mark.asyncio
async def test_login_android_appauth_cancelled_emits_error(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    login_events: list[LoginEvent] = []

    async def on_login(e: LoginEvent):
        login_events.append(e)

    page.on_login = on_login

    _install_fake_appauth(
        monkeypatch,
        {
            "error": "cancelled",
            "error_description": "User cancelled authorization.",
        },
    )

    request_token = AsyncMock()
    monkeypatch.setattr(AuthorizationService, "request_token", request_token)

    await page.login(_make_provider())
    await asyncio.sleep(0)

    assert conn.oauth_authorize_calls == []
    request_token.assert_not_awaited()
    assert login_events
    assert login_events[0].error == "cancelled"


@pytest.mark.asyncio
async def test_login_android_appauth_missing_code_emits_error(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    login_events: list[LoginEvent] = []

    async def on_login(e: LoginEvent):
        login_events.append(e)

    page.on_login = on_login

    _install_fake_appauth(
        monkeypatch,
        {
            "authorization_code": None,
            "code_verifier": "appauth-verifier",
        },
    )

    request_token = AsyncMock()
    monkeypatch.setattr(AuthorizationService, "request_token", request_token)

    await page.login(_make_provider())
    await asyncio.sleep(0)

    assert conn.oauth_authorize_calls == []
    request_token.assert_not_awaited()
    assert login_events
    assert login_events[0].error == "missing_authorization_code"


@pytest.mark.asyncio
async def test_login_desktop_raises_clear_error():
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.WINDOWS

    with pytest.raises(RuntimeError, match="not supported on this platform"):
        await page.login(_make_provider())

    assert conn.oauth_authorize_calls == []


@pytest.mark.asyncio
async def test_login_web_still_calls_oauth_authorize(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = True
    page.platform = PagePlatform.ANDROID  # platform irrelevant when web=True

    opened: list[str] = []

    async def fake_open_window(self, url, **kwargs):
        opened.append(url)

    monkeypatch.setattr(
        "flet.controls.page.UrlLauncher.open_window",
        fake_open_window,
    )

    await page.login(_make_provider())

    assert len(conn.oauth_authorize_calls) == 1
    assert "state" in conn.oauth_authorize_calls[0]
    assert opened


@pytest.mark.asyncio
async def test_logout_forces_ephemeral_reauth_on_next_login(monkeypatch):
    """After logout, next authorize must not silently reuse IdP SSO cookies."""
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID

    fake_appauth = _install_fake_appauth(
        monkeypatch,
        {
            "authorization_code": "auth-code",
            "code_verifier": "appauth-verifier",
        },
    )
    monkeypatch.setattr(
        AuthorizationService, "request_token", AsyncMock(return_value=None)
    )

    provider = _make_provider(authorization_params={"resource": "api"})

    # First login: normal (shared) browser session.
    await page.login(provider)
    assert fake_appauth.authorize_calls[-1]["prefer_ephemeral_session"] is False
    assert fake_appauth.authorize_calls[-1]["additional_parameters"] == {
        "resource": "api"
    }

    page.logout()
    assert page.auth is None

    # Second login after logout: ephemeral only (no prompt in additional —
    # AppAuth-Android rejects built-in prompt there).
    await page.login(provider)
    call = fake_appauth.authorize_calls[-1]
    assert call["prefer_ephemeral_session"] is True
    assert call["additional_parameters"] == {"resource": "api"}
    assert "prompt" not in call["additional_parameters"]
    assert provider.authorization_params == {"resource": "api"}

    # Third login: flag consumed; back to non-ephemeral.
    await page.login(provider)
    assert fake_appauth.authorize_calls[-1]["prefer_ephemeral_session"] is False


@pytest.mark.asyncio
async def test_logout_reauth_flag_survives_authorize_error(monkeypatch):
    """AppAuth error after logout must still force ephemeral on retry."""
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    page.on_login = AsyncMock()

    fake_appauth = _install_fake_appauth(
        monkeypatch,
        {
            "error": "authorize_failed",
            "error_description": "Parameter prompt is directly supported...",
        },
    )

    provider = _make_provider()
    page.logout()
    await page.login(provider)
    assert fake_appauth.authorize_calls[-1]["prefer_ephemeral_session"] is True

    # Flag still set — retry stays ephemeral.
    fake_ok = _install_fake_appauth(
        monkeypatch,
        {
            "authorization_code": "auth-code",
            "code_verifier": "appauth-verifier",
        },
    )
    monkeypatch.setattr(
        AuthorizationService, "request_token", AsyncMock(return_value=None)
    )
    await page.login(provider)
    assert fake_ok.authorize_calls[-1]["prefer_ephemeral_session"] is True
