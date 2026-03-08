import builtins
import importlib
import sys

import pytest


def _clear_flet_modules():
    """Remove loaded `flet` modules to force fresh import behavior in each test."""
    for module_name in list(sys.modules):
        if module_name == "flet" or module_name.startswith("flet."):
            del sys.modules[module_name]


def _blocked_import_factory(blocked_modules: set[str]):
    """Create an import hook that raises for selected top-level module names."""
    original_import = builtins.__import__

    def blocked_import(name, globals=None, locals=None, fromlist=(), level=0):
        """Raise `ModuleNotFoundError` for blocked modules and delegate otherwise."""
        top_name = name.split(".")[0]
        if top_name in blocked_modules:
            raise ModuleNotFoundError(f"No module named '{top_name}'")
        return original_import(name, globals, locals, fromlist, level)

    return blocked_import


def test_import_flet_without_httpx_oauthlib(monkeypatch):
    """Ensure `import flet` succeeds when optional auth dependencies are absent."""
    _clear_flet_modules()
    monkeypatch.setattr(
        builtins,
        "__import__",
        _blocked_import_factory({"httpx", "oauthlib"}),
    )

    flet = importlib.import_module("flet")

    assert flet is not None
    assert hasattr(flet, "Page")


def test_auth_exports_stay_importable_without_httpx_oauthlib(monkeypatch):
    """Ensure lazy `flet.auth` exports resolve without importing optional deps."""
    _clear_flet_modules()
    monkeypatch.setattr(
        builtins,
        "__import__",
        _blocked_import_factory({"httpx", "oauthlib"}),
    )

    auth = importlib.import_module("flet.auth")

    assert auth.AuthorizationService.__name__ == "AuthorizationService"
    assert auth.GitHubOAuthProvider.__name__ == "GitHubOAuthProvider"


def test_authorization_service_loads_oauthlib_on_use(monkeypatch):
    """Ensure oauthlib is required only when auth service logic is actually used."""
    _clear_flet_modules()
    monkeypatch.setattr(
        builtins,
        "__import__",
        _blocked_import_factory({"httpx", "oauthlib"}),
    )

    auth = importlib.import_module("flet.auth")
    provider = auth.OAuthProvider(
        client_id="client_id",
        client_secret="client_secret",
        authorization_endpoint="https://example.com/authorize",
        token_endpoint="https://example.com/token",
        redirect_url="https://example.com/callback",
    )
    service = auth.AuthorizationService(
        provider=provider,
        fetch_user=False,
        fetch_groups=False,
    )

    with pytest.raises(ModuleNotFoundError, match="oauthlib"):
        service.get_authorization_data()
