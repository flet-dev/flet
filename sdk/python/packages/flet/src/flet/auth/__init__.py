from typing import TYPE_CHECKING, Any

from flet.auth.authorization import Authorization
from flet.auth.group import Group
from flet.auth.oauth_provider import OAuthProvider
from flet.auth.oauth_token import OAuthToken
from flet.auth.user import User

if TYPE_CHECKING:
    from flet.auth.authorization_service import AuthorizationService
    from flet.auth.providers import (
        Auth0OAuthProvider,
        AzureOAuthProvider,
        GitHubOAuthProvider,
        GoogleOAuthProvider,
    )

__all__ = [
    "Auth0OAuthProvider",
    "Authorization",
    "AuthorizationService",
    "AzureOAuthProvider",
    "GitHubOAuthProvider",
    "GoogleOAuthProvider",
    "Group",
    "OAuthProvider",
    "OAuthToken",
    "User",
]


def __getattr__(name: str) -> Any:
    if name == "AuthorizationService":
        from flet.auth.authorization_service import AuthorizationService

        return AuthorizationService
    if name == "Auth0OAuthProvider":
        from flet.auth.providers.auth0_oauth_provider import Auth0OAuthProvider

        return Auth0OAuthProvider
    if name == "AzureOAuthProvider":
        from flet.auth.providers.azure_oauth_provider import AzureOAuthProvider

        return AzureOAuthProvider
    if name == "GitHubOAuthProvider":
        from flet.auth.providers.github_oauth_provider import GitHubOAuthProvider

        return GitHubOAuthProvider
    if name == "GoogleOAuthProvider":
        from flet.auth.providers.google_oauth_provider import GoogleOAuthProvider

        return GoogleOAuthProvider
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
