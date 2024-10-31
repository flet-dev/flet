from flet.auth.oauth_provider import OAuthProvider


class GoogleOAuthProvider(OAuthProvider):
    def __init__(self, client_id: str, client_secret: str, redirect_url: str) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint="https://accounts.google.com/o/oauth2/auth",
            token_endpoint="https://oauth2.googleapis.com/token",
            redirect_url=redirect_url,
            user_scopes=[
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            user_endpoint="https://www.googleapis.com/oauth2/v3/userinfo",
            user_id_fn=lambda u: u["sub"],
            group_scopes=[],
        )
