from typing import Optional

from flet.auth.oauth_provider import OAuthProvider

__all__ = ["AzureOAuthProvider"]


class AzureOAuthProvider(OAuthProvider):
    """
    OAuth provider preset for Microsoft Entra ID (Azure AD).

    Uses v2 endpoints for the selected tenant and Microsoft Graph `/me` for
    user profile retrieval, with Graph `id` used as the user id.
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        tenant: Optional[str] = "common",
    ) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize",
            token_endpoint=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token",
            redirect_url=redirect_url,
            user_scopes=["user.read"],
            user_endpoint="https://graph.microsoft.com/v1.0/me",
            user_id_fn=lambda u: u["id"],
            group_scopes=[],
        )
        self.tenant = tenant
