import os

import flet
from flet import ElevatedButton, Page
from flet.auth import OAuthProvider


def main(page: Page):
    provider = OAuthProvider(
        client_id=os.getenv("LINKEDIN_CLIENT_ID"),
        client_secret=os.getenv("LINKEDIN_CLIENT_SECRET"),
        authorization_endpoint="https://www.linkedin.com/oauth/v2/authorization",
        token_endpoint="https://www.linkedin.com/oauth/v2/accessToken",
        user_endpoint="https://api.linkedin.com/v2/me",
        user_scopes=["r_liteprofile", "r_emailaddress"],
        user_id_fn=lambda u: u["id"],
        redirect_url="http://localhost:8550/api/oauth/redirect",
    )

    def login_click(e):
        page.login(provider)

    def on_login(e):
        if e.error:
            raise Exception(e.error)
        print("User ID:", page.auth.user.id)
        print("Access token:", page.auth.token.access_token)

    page.on_login = on_login
    page.add(ElevatedButton("Login with LinkedIn", on_click=login_click))


flet.app(target=main, port=8550, view=flet.AppView.WEB_BROWSER)
