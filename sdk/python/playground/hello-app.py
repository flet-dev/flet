import flet
from flet import Text


def main(page):
    print(page.user_auth_provider, page.user_name, page.user_email)
    page.add(Text(f"Hello to session {page.session_id}!"))


flet.app(target=main, permissions="")
