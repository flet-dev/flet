import json
import logging
import os

import flet as ft
import httpx
from flet.auth.providers import GitHubOAuthProvider
from flet.security import decrypt, encrypt

logging.basicConfig(level=logging.INFO)

MY_APP_SECRET_KEY = os.getenv("MY_APP_SECRET_KEY")
assert MY_APP_SECRET_KEY, "set MY_APP_SECRET_KEY environment variable"
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
assert GITHUB_CLIENT_ID, "set GITHUB_CLIENT_ID environment variable"
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
assert GITHUB_CLIENT_SECRET, "set GITHUB_CLIENT_SECRET environment variable"


async def main(page: ft.Page):
    # encryption passphrase
    secret_key = MY_APP_SECRET_KEY

    # configure provider
    provider = GitHubOAuthProvider(
        client_id=GITHUB_CLIENT_ID,
        client_secret=GITHUB_CLIENT_SECRET,
        redirect_url="http://localhost:8550/oauth_callback",
    )

    # client storage keys
    AUTH_TOKEN_KEY = "myapp.auth_token"

    async def perform_login(e):
        # perform login
        saved_token = None
        ejt = await page.shared_preferences.get_async(AUTH_TOKEN_KEY)
        if ejt:
            saved_token = decrypt(ejt, secret_key)
        if e is not None or saved_token is not None:
            page.login(provider, saved_token=saved_token, scope=["public_repo"])

    async def on_login(e: ft.LoginEvent):
        if e.error:
            raise Exception(e.error)

        # save token in a client storage
        jt = page.auth.token.to_json()
        ejt = encrypt(jt, secret_key)
        await page.shared_preferences.set_async(AUTH_TOKEN_KEY, ejt)

        logged_user.value = f"Hello, {page.auth.user['name']}!"
        toggle_login_buttons()
        list_github_repositories()
        page.update()

    def list_github_repositories():
        repos_view.controls.clear()
        if page.auth:
            headers = {
                "User-Agent": "Flet",
                "Authorization": f"Bearer {page.auth.token.access_token}",
            }
            repos_resp = httpx.get("https://api.github.com/user/repos", headers=headers)
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
        await page.shared_preferences.remove_async(AUTH_TOKEN_KEY)
        page.logout()

    def on_logout(e):
        toggle_login_buttons()
        list_github_repositories()
        page.update()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logged_user.visible = logout_button.visible = page.auth is not None

    logged_user = ft.Text()
    login_button = ft.ElevatedButton("Login with GitHub", on_click=perform_login)
    logout_button = ft.ElevatedButton("Logout", on_click=logout_button_click)
    repos_view = ft.ListView(expand=True)
    page.on_login = on_login
    page.on_logout = on_logout
    toggle_login_buttons()
    await perform_login(None)
    page.add(ft.Row([logged_user, login_button, logout_button]), repos_view)


ft.run(main)
