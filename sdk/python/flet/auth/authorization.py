from typing import List, Optional

from oauthlib.oauth2 import WebApplicationClient

from flet.auth.oauth_provider import OAuthProvider
from flet.auth.oauth_token import OAuthToken
from flet.auth.user import User


class Authorization():
    def __init__(self, page, provider: OAuthProvider, fetch_user: bool, fetch_groups: bool, scope: Optional[List[str]]=None) -> None:
        self.page = page
        self.fetch_user = fetch_user
        self.fetch_groups = fetch_groups
        self.scope = scope
        self.provider = provider
        self.token: Optional[OAuthToken] = None
        self.user: Optional[User] = None

    def authorize(self):
        client = WebApplicationClient(self.provider.client_id)
        url = client.prepare_request_uri(self.provider.authorization_endpoint, self.provider.redirect_url, 
        scope=["read:user"],
        state="state-123")
        print(url)
