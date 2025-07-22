# CARD_OFFSET = 20
SOLITAIRE_WIDTH = 1000
SOLITAIRE_HEIGHT = 500

import flet as ft
from card import Card
from slot import Slot


class Solitaire(ft.Stack):
    def __init__(self):
        super().__init__()
        # self.start_top = 0
        # self.start_left = 0
        self.controls = []
        self.slots = []
        # self.card_offset = CARD_OFFSET
        self.width = SOLITAIRE_WIDTH
        self.height = SOLITAIRE_HEIGHT

    def did_mount(self):
        self.create_card_deck()
        self.create_slots()
        self.deal_cards()

    def create_card_deck(self):
        card1 = Card(self, color="GREEN")
        card2 = Card(self, color="YELLOW")
        card3 = Card(self, color="RED")
        card4 = Card(self, color="BLUE")
        self.cards = [card1, card2, card3, card4]

    def create_slots(self):
        self.slots.append(Slot(top=0, left=0))
        self.slots.append(Slot(top=0, left=200))
        self.slots.append(Slot(top=0, left=300))
        self.controls.extend(self.slots)
        self.update()

    def deal_cards(self):
        self.controls.extend(self.cards)

        for card in self.cards:
            card.place(self.slots[0])
        self.update()
