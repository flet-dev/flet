from typing import List, Optional

import httpx
from flet_runtime.auth.oauth_provider import OAuthProvider
from flet_runtime.auth.user import User
from flet_runtime.version import version


class WeChatOAuthProvider(OAuthProvider):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_url: str,
        scopes: Optional[List[str]] = ["snsapi_login"],
    ) -> None:
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorization_endpoint="https://open.weixin.qq.com/connect/qrconnect",
            token_endpoint="https://api.weixin.qq.com/sns/oauth2/access_token",
            user_endpoint="https://api.weixin.qq.com/sns/userinfo",
            redirect_url=redirect_url,
            scopes=scopes,
        )

    def _fetch_user(self, access_token: str, openid: str) -> Optional[User]:
        user_req = self.__get_user_details_requests(access_token, openid)
        with httpx.Client(follow_redirects=True) as client:
            user_resp = client.send(user_req)
            return self.__complete_fetch_user_details(user_resp)

    async def _fetch_user_async(self, access_token: str, openid: str) -> Optional[User]:
        user_req = self.__get_user_details_requests(access_token, openid)
        async with httpx.AsyncClient() as client:
            user_resp = await client.send(user_req)
            return self.__complete_fetch_user_details(user_resp)

    def __get_user_details_requests(self, access_token, openid):
        params = {
            "access_token": access_token,
            "openid": openid,
        }
        return httpx.Request(
            "GET",
            self.user_endpoint,
            params=params,
            headers=self.__get_client_headers(),
        )

    def __complete_fetch_user_details(self, user_resp):
        user_resp.raise_for_status()
        uj = user_resp.json()
        return User(id=str(uj["unionid"]), **uj)

    def __get_client_headers(self):
        return {
            "User-Agent": f"Flet/{version}",
        }
