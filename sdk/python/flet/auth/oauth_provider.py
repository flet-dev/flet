from typing import Optional

from flet.auth.user import User


class OAuthProvider():
    def __init__(self, client_id: str, client_secret: str, authorization_endpoint: str,
        token_endpoint: str, redirect_url: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorization_endpoint = authorization_endpoint
        self.token_endpoint = token_endpoint
        self.redirect_url = redirect_url

    def _name(self):
        raise Exception("Not implemented")

    

    def get_user(self) -> Optional[User]:
        return 
