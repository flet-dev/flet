"""Mobile page.login uses WebAuth; skips web oauth_authorize."""

from __future__ import annotations

import asyncio
from typing import Any, Optional
from unittest.mock import AsyncMock
from urllib.parse import parse_qs, urlparse

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
        code_verifier="provider-verifier",
        code_challenge="provider-challenge",
        code_challenge_method="S256",
        **kwargs,
    )


class _FakeWebAuthSession:
    def __init__(
        self,
        redirect_url: str,
        *,
        callback_url: Optional[str] = None,
        raise_error: Optional[str] = None,
    ):
        self.redirect_url = redirect_url
        self._callback_url = callback_url
        self._raise_error = raise_error
        self.authenticate_calls: list[dict[str, Any]] = []

    async def authenticate(self, url: str, *, ephemeral: bool = False, timeout: float = 300):
        self.authenticate_calls.append({"url": url, "ephemeral": ephemeral})
        if self._raise_error:
            raise RuntimeError(self._raise_error)
        assert self._callback_url is not None
        return self._callback_url


class _FakeWebAuth:
    last: Optional["_FakeWebAuth"] = None

    def __init__(self):
        _FakeWebAuth.last = self
        self.start_calls: list[Optional[str]] = []
        self._callback_url: Optional[str] = None
        self._raise_on_auth: Optional[str] = None
        self.session: Optional[_FakeWebAuthSession] = None

    async def start(self, *, callback_scheme: Optional[str] = None):
        self.start_calls.append(callback_scheme)
        if not callback_scheme:
            raise ValueError("callback_scheme is required on Android/iOS for WebAuth.")
        self.session = _FakeWebAuthSession(
            f"{callback_scheme}://callback",
            callback_url=self._callback_url,
            raise_error=self._raise_on_auth,
        )
        return self.session


def _install_fake_webauth(
    monkeypatch,
    *,
    callback_url: Optional[str] = None,
    raise_on_auth: Optional[str] = None,
) -> type[_FakeWebAuth]:
    def factory():
        fake = _FakeWebAuth()
        fake._callback_url = callback_url
        fake._raise_on_auth = raise_on_auth
        return fake

    monkeypatch.setattr("flet.controls.page.WebAuth", factory)
    return _FakeWebAuth


@pytest.mark.asyncio
async def test_login_android_missing_callback_scheme_raises(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    _install_fake_webauth(monkeypatch)

    with pytest.raises(ValueError, match="callback_scheme"):
        await page.login(_make_provider())

    assert conn.oauth_authorize_calls == []


@pytest.mark.asyncio
async def test_login_android_webauth_success_skips_oauth_authorize(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    login_events: list[LoginEvent] = []

    async def on_login(e: LoginEvent):
        login_events.append(e)

    page.on_login = on_login

    # callback built after we know state — use a side-effecting fake
    captured: dict[str, Any] = {}

    class _DynamicFake(_FakeWebAuth):
        async def start(self, *, callback_scheme=None):
            session = await super().start(callback_scheme=callback_scheme)

            async def authenticate(url, *, ephemeral=False, timeout=300):
                session.authenticate_calls.append(
                    {"url": url, "ephemeral": ephemeral}
                )
                qs = parse_qs(urlparse(url).query)
                state = qs.get("state", [""])[0]
                captured["auth_url"] = url
                return f"{session.redirect_url}?code=auth-code&state={state}"

            session.authenticate = authenticate  # type: ignore[method-assign]
            return session

    monkeypatch.setattr("flet.controls.page.WebAuth", _DynamicFake)

    async def fake_request_token(self, code: str, *, code_verifier=None):
        assert code == "auth-code"
        # Shared provider PKCE fields must not be mutated.
        assert self.provider.code_verifier == "provider-verifier"
        assert self.provider.code_challenge == "provider-challenge"
        # ensure_pkce stored a per-request verifier on the auth service.
        assert self._AuthorizationService__request_code_verifier
        captured["request_verifier"] = (
            self._AuthorizationService__request_code_verifier
        )

    monkeypatch.setattr(AuthorizationService, "request_token", fake_request_token)

    provider = _make_provider()
    auth = await page.login(
        provider,
        callback_scheme="com.example.app.auth",
        on_open_authorization_url=AsyncMock(),
        complete_page_html="<html/>",
        redirect_to_page=True,
    )

    assert conn.oauth_authorize_calls == []
    assert "redirect_uri=com.example.app.auth" in captured["auth_url"]
    assert "code_challenge=" in captured["auth_url"]
    assert provider.code_verifier == "provider-verifier"
    assert provider.code_challenge == "provider-challenge"
    assert auth is page.auth

    await asyncio.sleep(0)
    assert login_events
    assert not login_events[0].error


@pytest.mark.asyncio
async def test_login_android_invalid_state_skips_token(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    login_events: list[LoginEvent] = []

    async def on_login(e: LoginEvent):
        login_events.append(e)

    page.on_login = on_login

    _install_fake_webauth(
        monkeypatch,
        callback_url="com.example.app.auth://callback?code=auth-code&state=wrong",
    )
    request_token = AsyncMock()
    monkeypatch.setattr(AuthorizationService, "request_token", request_token)

    await page.login(_make_provider(), callback_scheme="com.example.app.auth")
    await asyncio.sleep(0)

    request_token.assert_not_awaited()
    assert login_events
    assert login_events[0].error == "invalid_state"


@pytest.mark.asyncio
async def test_login_android_webauth_cancelled_emits_error(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID
    login_events: list[LoginEvent] = []

    async def on_login(e: LoginEvent):
        login_events.append(e)

    page.on_login = on_login

    _install_fake_webauth(monkeypatch, raise_on_auth="cancelled")
    request_token = AsyncMock()
    monkeypatch.setattr(AuthorizationService, "request_token", request_token)

    await page.login(_make_provider(), callback_scheme="com.example.app.auth")
    await asyncio.sleep(0)

    assert conn.oauth_authorize_calls == []
    request_token.assert_not_awaited()
    assert login_events
    assert login_events[0].error == "authorize_failed"


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
    page.platform = PagePlatform.ANDROID

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
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = False
    page.platform = PagePlatform.ANDROID

    class _DynamicFake(_FakeWebAuth):
        async def start(self, *, callback_scheme=None):
            sess = await super().start(callback_scheme=callback_scheme)

            async def authenticate(url, *, ephemeral=False, timeout=300):
                sess.authenticate_calls.append(
                    {"url": url, "ephemeral": ephemeral}
                )
                qs = parse_qs(urlparse(url).query)
                state = qs.get("state", [""])[0]
                return f"{sess.redirect_url}?code=auth-code&state={state}"

            sess.authenticate = authenticate  # type: ignore[method-assign]
            return sess

    monkeypatch.setattr("flet.controls.page.WebAuth", _DynamicFake)
    monkeypatch.setattr(
        AuthorizationService, "request_token", AsyncMock(return_value=None)
    )

    provider = _make_provider(authorization_params={"resource": "api"})

    await page.login(provider, callback_scheme="com.example.app.auth")
    fake1 = _DynamicFake.last
    assert fake1 and fake1.session
    assert fake1.session.authenticate_calls[-1]["ephemeral"] is False
    assert "prompt=login" not in fake1.session.authenticate_calls[-1]["url"]

    page.logout()
    assert page.auth is None

    await page.login(provider, callback_scheme="com.example.app.auth")
    fake2 = _DynamicFake.last
    assert fake2 and fake2.session
    call = fake2.session.authenticate_calls[-1]
    assert call["ephemeral"] is True
    assert "prompt=login" in call["url"]
    assert "max_age=0" in call["url"]
    assert "resource=api" in call["url"]
    assert provider.authorization_params == {"resource": "api"}

    await page.login(provider, callback_scheme="com.example.app.auth")
    fake3 = _DynamicFake.last
    assert fake3 and fake3.session
    assert fake3.session.authenticate_calls[-1]["ephemeral"] is False
    assert "prompt=login" not in fake3.session.authenticate_calls[-1]["url"]


@pytest.mark.asyncio
async def test_web_logout_reauth_does_not_mutate_provider(monkeypatch):
    conn = _Conn()
    session = Session(conn)
    page = session.page
    page.web = True
    page.platform = PagePlatform.ANDROID

    opened: list[str] = []

    async def fake_open_window(self, url, **kwargs):
        opened.append(url)

    monkeypatch.setattr(
        "flet.controls.page.UrlLauncher.open_window",
        fake_open_window,
    )

    provider = _make_provider(authorization_params={"resource": "api"})
    page.logout()
    await page.login(provider)

    assert provider.authorization_params == {"resource": "api"}
    assert opened
    assert "prompt=login" in opened[0]
    assert "max_age=0" in opened[0]
    assert "resource=api" in opened[0]
