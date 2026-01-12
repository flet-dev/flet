#
# Run this example with:
#   export GITHUB_CLIENT_ID=<your_github_oauth_app_client_id>
#   export GITHUB_CLIENT_SECRET=<your_github_oauth_app_client_secret>
#   export MY_APP_SECRET_KEY=<your_app_secret_key_for_token_encryption>
#   flet run --web --port 8550 github_repos_browser.py
#
import json
import logging
import os

import httpx

import flet as ft
from flet.auth.providers import GitHubOAuthProvider
from flet.security import decrypt, encrypt

logging.basicConfig(level=logging.INFO)


def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    assert value, f"set {name} environment variable"
    return value


async def main(page: ft.Page):
    # encryption passphrase
    secret_key = get_env_variable("MY_APP_SECRET_KEY")

    # configure provider
    provider = GitHubOAuthProvider(
        client_id=get_env_variable("GITHUB_CLIENT_ID"),
        client_secret=get_env_variable("GITHUB_CLIENT_SECRET"),
        redirect_url="http://127.0.0.1:8550/oauth_callback",
    )

    # client storage keys
    AUTH_TOKEN_KEY = "myapp.auth_token"

    async def perform_login(e):
        login_button.disabled = True
        login_button.update()

        # perform login
        saved_token = None
        ejt = await ft.SharedPreferences().get(AUTH_TOKEN_KEY)
        if ejt:
            saved_token = decrypt(ejt, secret_key)
        if e is not None or saved_token is not None:
            await page.login(
                provider,
                redirect_to_page=True,
                on_open_authorization_url=lambda url: ft.UrlLauncher().launch_url(
                    ft.Url(url, target=ft.UrlTarget.SELF)
                ),
                saved_token=saved_token,
                scope=["public_repo"],
            )

    async def on_login(e: ft.LoginEvent):
        if e.error:
            raise Exception(e.error)

        assert page.auth

        # save token in a client storage
        jt = (await page.auth.get_token()).to_json()
        ejt = encrypt(jt, secret_key)
        await ft.SharedPreferences().set(AUTH_TOKEN_KEY, ejt)

        logged_user.value = f"Hello, {page.auth.user['name']}!"
        toggle_login_buttons()
        await list_github_repositories()
        page.update()

    async def list_github_repositories():
        repos_view.controls.clear()
        if page.auth:
            headers = {
                "User-Agent": "Flet",
                "Authorization": f"Bearer {(await page.auth.get_token()).access_token}",
            }
            async with httpx.AsyncClient() as client:
                repos_resp = await client.get(
                    "https://api.github.com/user/repos", headers=headers
                )
                repos_resp.raise_for_status()
                user_repos = json.loads(repos_resp.text)
                for repo in user_repos:
                    repos_view.controls.append(
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.FOLDER_ROUNDED),
                            title=ft.Text(repo["full_name"]),
                        )
                    )

    async def logout_button_click(e):
        await ft.SharedPreferences().remove(AUTH_TOKEN_KEY)
        page.logout()

    async def on_logout(e):
        toggle_login_buttons()
        await list_github_repositories()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        login_button.disabled = False
        logged_user.visible = logout_button.visible = page.auth is not None

    logged_user = ft.Text()
    login_button = ft.Button("Login with GitHub", on_click=perform_login)
    logout_button = ft.Button("Logout", on_click=logout_button_click)
    repos_view = ft.ListView(expand=True)
    page.on_login = on_login
    page.on_logout = on_logout
    toggle_login_buttons()
    page.add(ft.Row([logged_user, login_button, logout_button]), repos_view)
    await perform_login(None)


ft.run(main)
