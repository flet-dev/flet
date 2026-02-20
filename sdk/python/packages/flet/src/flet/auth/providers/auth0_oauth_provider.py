from flet.auth.oauth_provider import OAuthProvider


class Auth0OAuthProvider(OAuthProvider):
    """
    OAuth provider preset for Auth0.

    Configures Auth0 authorization/token endpoints and user-info retrieval via
    `/userinfo`, using the `sub` claim as the user id.
    """

    def __init__(
        self, domain: str, client_id: str, client_secret: str, redirect_url: str
    ) -> None:
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
        )
        self.domain = domain
