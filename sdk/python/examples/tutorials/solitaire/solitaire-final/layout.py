import flet as ft
from settings import SettingsDialog


def create_appbar(page, settings, on_new_game):
    def new_game_clicked(e):
        on_new_game(settings)

    def show_rules(e):
        page.dialog = rules_dialog
        rules_dialog.open = True
        page.update()

    def show_settings(e):
        page.dialog = SettingsDialog(settings, on_new_game)
        page.dialog.open = True
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Image(src="/images/card.png"),
        leading_width=30,
        title=ft.Text("Flet solitaire"),
        bgcolor=ft.Colors.SURFACE_VARIANT,
        actions=[
            ft.TextButton(text="New game", on_click=new_game_clicked),
            ft.TextButton(text="Rules", on_click=show_rules),
            ft.IconButton(ft.Icons.SETTINGS, on_click=show_settings),
        ],
    )

    rules_md = ft.Markdown(
        """
    Klondike is played with a standard 52-card deck, without Jokers.

    The four foundations (light rectangles in the upper right of the figure) are built up by suit from Ace (low in this game) to King, and the tableau piles can be built down by alternate colors. Every face-up card in a partial pile, or a complete pile, can be moved, as a unit, to another tableau pile on the basis of its highest card. Any empty piles can be filled with a King, or a pile of cards with a King. The aim of the game is to build up four stacks of cards starting with Ace and ending with King, all of the same suit, on one of the four foundations, at which time the player would have won. There are different ways of dealing the remainder of the deck from the stock to the waste, which can be selected in the Settings:

    - Turning three cards at once to the waste, with no limit on passes through the deck.
    - Turning three cards at once to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with three passes through the deck.
    - Turning one card at a time to the waste, with no limit on passes through the deck.

    If the player can no longer make any meaningful moves, the game is considered lost.
        """
    )

    rules_dialog = ft.AlertDialog(
        title=ft.Text("Solitaire rules"),
        content=rules_md,
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )
