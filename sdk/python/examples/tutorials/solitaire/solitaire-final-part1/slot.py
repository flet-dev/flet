SLOT_WIDTH = 70
SLOT_HEIGHT = 100

import flet as ft


class Slot(ft.Container):
    def __init__(self, solitaire, top, left, border):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.left = left
        self.top = top
        self.on_click = self.click
        self.solitaire = solitaire
        self.border = border
        self.border_radius = ft.border_radius.all(6)

    def get_top_card(self):
        if len(self.pile) > 0:
            return self.pile[-1]

    def click(self, e):
        if self == self.solitaire.stock:
            self.solitaire.restart_stock()
