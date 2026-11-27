"""OIDCProvider.discover — OIDC issuer discovery only."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from flet.auth.oidc_provider import OIDCProvider


DISCOVERY_DOC = {
    "issuer": "https://example.auth0.com/",
    "authorization_endpoint": "https://example.auth0.com/authorize",
    "token_endpoint": "https://example.auth0.com/oauth/token",
    "userinfo_endpoint": "https://example.auth0.com/userinfo",
    "jwks_uri": "https://example.auth0.com/.well-known/jwks.json",
    "end_session_endpoint": "https://example.auth0.com/v2/logout",
}


def _mock_response(payload: dict, status_code: int = 200) -> MagicMock:
    resp = MagicMock()
    resp.status_code = status_code
    resp.text = json.dumps(payload)
    resp.json.return_value = payload
    if status_code >= 400:
        resp.raise_for_status.side_effect = httpx.HTTPStatusError(
            "error",
            request=MagicMock(),
            response=resp,
        )
    else:
        resp.raise_for_status.return_value = None
    return resp


@pytest.mark.asyncio
async def test_discover_populates_endpoints_not_redirect():
    mock_get = AsyncMock(return_value=_mock_response(DISCOVERY_DOC))
    with patch("httpx.AsyncClient") as client_cls:
        client = AsyncMock()
        client.__aenter__.return_value = client
        client.__aexit__.return_value = None
        client.get = mock_get
        client_cls.return_value = client

        provider = await OIDCProvider.discover(
            "https://example.auth0.com",
            client_id="cid",
            client_secret="",
            scopes=["openid", "profile"],
        )

    assert isinstance(provider, OIDCProvider)
    assert provider.client_id == "cid"
    assert provider.client_secret == ""
    assert provider.authorization_endpoint == DISCOVERY_DOC["authorization_endpoint"]
    assert provider.token_endpoint == DISCOVERY_DOC["token_endpoint"]
    assert provider.user_endpoint == DISCOVERY_DOC["userinfo_endpoint"]
    assert provider.redirect_url in (None, "")
    assert provider.scopes == ["openid", "profile"]
    assert provider.issuer == DISCOVERY_DOC["issuer"]
    assert provider.jwks_uri == DISCOVERY_DOC["jwks_uri"]
    assert provider.end_session_endpoint == DISCOVERY_DOC["end_session_endpoint"]
    called_url = mock_get.await_args.args[0]
    assert called_url == "https://example.auth0.com/.well-known/openid-configuration"


@pytest.mark.asyncio
async def test_discover_strips_trailing_slash_on_issuer():
    mock_get = AsyncMock(return_value=_mock_response(DISCOVERY_DOC))
    with patch("httpx.AsyncClient") as client_cls:
        client = AsyncMock()
        client.__aenter__.return_value = client
        client.__aexit__.return_value = None
        client.get = mock_get
        client_cls.return_value = client

        await OIDCProvider.discover(
            "https://example.auth0.com/",
            client_id="cid",
        )

    assert (
        mock_get.await_args.args[0]
        == "https://example.auth0.com/.well-known/openid-configuration"
    )


@pytest.mark.asyncio
async def test_discover_missing_authorization_endpoint_raises():
    bad = dict(DISCOVERY_DOC)
    del bad["authorization_endpoint"]
    mock_get = AsyncMock(return_value=_mock_response(bad))
    with patch("httpx.AsyncClient") as client_cls:
        client = AsyncMock()
        client.__aenter__.return_value = client
        client.__aexit__.return_value = None
        client.get = mock_get
        client_cls.return_value = client

        with pytest.raises(ValueError, match="authorization_endpoint"):
            await OIDCProvider.discover("https://example.auth0.com", client_id="cid")


@pytest.mark.asyncio
async def test_discover_http_error_raises():
    mock_get = AsyncMock(return_value=_mock_response({}, status_code=404))
    with patch("httpx.AsyncClient") as client_cls:
        client = AsyncMock()
        client.__aenter__.return_value = client
        client.__aexit__.return_value = None
        client.get = mock_get
        client_cls.return_value = client

        with pytest.raises(httpx.HTTPStatusError):
            await OIDCProvider.discover("https://example.auth0.com", client_id="cid")
