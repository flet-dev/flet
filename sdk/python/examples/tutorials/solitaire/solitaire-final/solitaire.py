# from settings import Settings
import random

import flet as ft
from card import Card
from slot import Slot


class Suite:
    def __init__(self, suite_name, suite_color):
        self.name = suite_name
        self.color = suite_color


class Rank:
    def __init__(self, card_name, card_value):
        self.name = card_name
        self.value = card_value


class Solitaire(ft.Stack):
    def __init__(self, settings, on_win):
        super().__init__()
        self.width = 1000
        self.height = 500
        self.current_top = 0
        self.current_left = 0
        self.card_offset = 20
        self.settings = settings
        self.deck_passes_remaining = int(self.settings.deck_passes_allowed)
        self.controls = []
        self.on_win = on_win

    def did_mount(self):
        self.create_slots()
        self.create_card_deck()
        self.deal_cards()

    def create_slots(self):
        self.stock = Slot(
            solitaire=self, slot_type="stock", top=0, left=0, border=ft.border.all(1)
        )

        self.waste = Slot(
            solitaire=self, slot_type="waste", top=0, left=100, border=None
        )

        self.foundation = []
        x = 300
        for i in range(4):
            self.foundation.append(
                Slot(
                    solitaire=self,
                    slot_type="foundation",
                    top=0,
                    left=x,
                    border=ft.border.all(1, "outline"),
                )
            )
            x += 100

        self.tableau = []
        x = 0
        for i in range(7):
            self.tableau.append(
                Slot(
                    solitaire=self,
                    slot_type="tableau",
                    top=150,
                    left=x,
                    # border=ft.border.all(1),
                    border=None,
                )
            )
            x += 100

        self.controls.append(self.stock)
        self.controls.append(self.waste)
        self.controls.extend(self.foundation)
        self.controls.extend(self.tableau)
        self.update()

    def create_card_deck(self):
        suites = [
            Suite("hearts", "RED"),
            Suite("diamonds", "RED"),
            Suite("clubs", "BLACK"),
            Suite("spades", "BLACK"),
        ]
        ranks = [
            Rank("Ace", 1),
            Rank("2", 2),
            Rank("3", 3),
            Rank("4", 4),
            Rank("5", 5),
            Rank("6", 6),
            Rank("7", 7),
            Rank("8", 8),
            Rank("9", 9),
            Rank("10", 10),
            Rank("Jack", 11),
            Rank("Queen", 12),
            Rank("King", 13),
        ]

        self.cards = []

        for suite in suites:
            for rank in ranks:
                file_name = f"{rank.name}_{suite.name}.svg"
                # print(file_name)
                self.cards.append(Card(solitaire=self, suite=suite, rank=rank))
        # self.stock = self.cards
        random.shuffle(self.cards)
        self.controls.extend(self.cards)
        self.update()

    def deal_cards(self):
        # Tableau
        card_index = 0
        first_slot = 0
        while card_index <= 27:
            for slot_index in range(first_slot, len(self.tableau)):
                self.cards[card_index].place(self.tableau[slot_index])
                card_index += 1
            first_slot += 1

        # Reveal top cards in slot piles:
        for number in range(len(self.tableau)):
            # self.tableau[number].pile[-1].turn_face_up()
            self.tableau[number].get_top_card().turn_face_up()

        # Stock pile
        for i in range(28, len(self.cards)):
            self.cards[i].place(self.stock)

    def move_on_top(self, cards_to_drag):
        """Brings draggable card pile to the top of the stack"""

        for card in cards_to_drag:
            self.controls.remove(card)
            self.controls.append(card)
        self.update()

    def bounce_back(self, cards):
        i = 0
        for card in cards:
            card.top = self.current_top
            if card.slot.type == "tableau":
                card.top += i * self.card_offset
            card.left = self.current_left
            i += 1

    def display_waste(self):
        if self.settings.waste_size == 3:
            self.waste.fan_top_three()
        self.update()

    def restart_stock(self):
        self.waste.pile.reverse()
        while len(self.waste.pile) > 0:
            card = self.waste.pile[0]
            card.turn_face_down()
            card.place(self.stock)
        self.update()

    def check_foundation_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.name == top_card.suite.name
                and current_card.rank.value - top_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "Ace"

    def check_tableau_rules(self, current_card, top_card=None):
        if top_card is not None:
            return (
                current_card.suite.color != top_card.suite.color
                and top_card.rank.value - current_card.rank.value == 1
            )
        else:
            return current_card.rank.name == "King"

    def check_if_you_won(self):
        cards_num = 0
        for slot in self.foundation:
            cards_num += len(slot.pile)
        if cards_num == 52:
            return True
        return False
