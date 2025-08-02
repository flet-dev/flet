import flet as ft


class Slot(ft.Container):
    def __init__(self, solitaire, slot_type, top, left, border):
        super().__init__()
        self.solitaire = solitaire
        self.pile = []
        self.type = slot_type
        self.width = 70
        self.height = 100
        self.left = left
        self.top = top
        self.border_radius = ft.border_radius.all(6)
        self.border = border
        self.on_click = self.click

    def get_top_card(self):
        if len(self.pile) > 0:
            return self.pile[-1]

    def get_top_three_cards(self):
        n = len(self.pile)
        return self.pile[max(0, n - 3) :]

    def fan_top_three(self):
        for i, card in enumerate(self.get_top_three_cards()):
            card.left = self.left + self.solitaire.card_offset * i
            card.visible = True

    def upper_card_top(self):
        if self.type == "tableau":
            if len(self.pile) > 1:
                return self.top + self.solitaire.card_offset * (len(self.pile) - 1)
        return self.top

    def click(self, e):
        if self.type == "stock" and self.solitaire.deck_passes_remaining > 1:
            self.solitaire.deck_passes_remaining -= 1
            self.solitaire.restart_stock()
