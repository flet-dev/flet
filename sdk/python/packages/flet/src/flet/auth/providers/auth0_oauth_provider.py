from typing import Optional

from flet.auth.oauth_provider import OAuthProvider

__all__ = ["Auth0OAuthProvider"]


class Auth0OAuthProvider(OAuthProvider):
    """
    OAuth provider preset for Auth0.

    Configures Auth0 authorization/token endpoints and user-info retrieval via
    `/userinfo`, using the `sub` claim as the user id.

    Attributes:
        domain: Auth0 tenant domain (without protocol), for example
            `example.us.auth0.com`.
        audience: Optional API identifier passed as `audience` authorization
            query parameter.
    """

    def __init__(
        self,
        domain: str,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        audience: Optional[str] = None,
    ) -> None:
        """
        Initialize Auth0 OAuth provider configuration.

        Args:
            domain: Auth0 tenant domain (without protocol), for example,
                `example.us.auth0.com`.
            client_id: Auth0 application client ID.
            client_secret: Auth0 application client secret.
            redirect_url: Redirect/callback URL registered in Auth0.
            audience: Auth0 API identifier used to request an access
                token targeted for a specific API resource server.
        """
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint=f"https://{domain}/authorize",
            token_endpoint=f"https://{domain}/oauth/token",
            redirect_url=redirect_url,
            scopes=["offline_access"],
            user_scopes=["openid", "profile", "email"],
            user_endpoint=f"https://{domain}/userinfo",
            user_id_fn=lambda u: u["sub"],
            group_scopes=[],
            authorization_params=(
                {"audience": audience} if audience is not None else None
            ),
        )
        self.domain = domain
        self.audience = audience
