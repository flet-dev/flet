import flet as ft

CARD_WIDTH = 70
CARD_HEIGTH = 100
DROP_PROXIMITY = 30
CARD_OFFSET = 20


class Card(ft.GestureDetector):
    def __init__(self, solitaire, suite, rank):
        super().__init__()
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.on_tap = self.click
        self.on_double_tap = self.doubleclick
        self.suite = suite
        self.rank = rank
        self.face_up = False
        self.top = None
        self.left = None
        self.solitaire = solitaire
        self.slot = None
        self.content = ft.Container(
            width=CARD_WIDTH,
            height=CARD_HEIGTH,
            border_radius=ft.border_radius.all(6),
            content=ft.Image(src="/images/card_back.png"),
        )
        self.draggable_pile = [self]

    def turn_face_up(self):
        """Reveals card"""
        self.face_up = True
        self.content.content.src = f"/images/{self.rank.name}_{self.suite.name}.svg"
        self.solitaire.update()

    def turn_face_down(self):
        """Hides card"""
        self.face_up = False
        self.content.content.src = "/images/card_back.png"
        self.solitaire.update()

    def move_on_top(self):
        """Brings draggable card pile to the top of the stack"""

        for card in self.draggable_pile:
            self.solitaire.controls.remove(card)
            self.solitaire.controls.append(card)
        self.solitaire.update()

    def bounce_back(self):
        """Returns draggable pile to its original position"""
        for card in self.draggable_pile:
            if card.slot in self.solitaire.tableau:
                card.top = card.slot.top + card.slot.pile.index(card) * CARD_OFFSET
            else:
                card.top = card.slot.top
            card.left = card.slot.left
        self.solitaire.update()

    def place(self, slot):
        """Place draggable pile to the slot"""

        for card in self.draggable_pile:
            if slot in self.solitaire.tableau:
                card.top = slot.top + len(slot.pile) * CARD_OFFSET
            else:
                card.top = slot.top
            card.left = slot.left

            # remove card from it's original slot, if exists
            if card.slot is not None:
                card.slot.pile.remove(card)

            # change card's slot to a new slot
            card.slot = slot

            # add card to the new slot's pile
            slot.pile.append(card)

        self.solitaire.update()

    def get_draggable_pile(self):
        """returns list of cards that will be dragged together, starting with the current card"""

        if (
            self.slot is not None
            and self.slot != self.solitaire.stock
            and self.slot != self.solitaire.waste
        ):
            self.draggable_pile = self.slot.pile[self.slot.pile.index(self) :]
        else:  # slot == None when the cards are dealed and need to be place in slot for the first time
            self.draggable_pile = [self]

    def start_drag(self, e: ft.DragStartEvent):
        if self.face_up:
            self.get_draggable_pile()
            self.move_on_top()

    def drag(self, e: ft.DragUpdateEvent):
        if self.face_up:
            for card in self.draggable_pile:
                card.top = (
                    max(0, self.top + e.delta_y)
                    + self.draggable_pile.index(card) * CARD_OFFSET
                )
                card.left = max(0, self.left + e.delta_x)
                self.solitaire.update()

    def drop(self, e: ft.DragEndEvent):
        if self.face_up:
            for slot in self.solitaire.tableau:
                if (
                    abs(self.top - (slot.top + len(slot.pile) * CARD_OFFSET))
                    < DROP_PROXIMITY
                    and abs(self.left - slot.left) < DROP_PROXIMITY
                ) and self.solitaire.check_tableau_rules(self, slot):
                    self.place(slot)
                    return

            if len(self.draggable_pile) == 1:
                for slot in self.solitaire.foundations:
                    if (
                        abs(self.top - slot.top) < DROP_PROXIMITY
                        and abs(self.left - slot.left) < DROP_PROXIMITY
                    ) and self.solitaire.check_foundations_rules(self, slot):
                        self.place(slot)
                        return

            self.bounce_back()

    def click(self, e):
        self.get_draggable_pile()
        if self.slot in self.solitaire.tableau:
            if not self.face_up and len(self.draggable_pile) == 1:
                self.turn_face_up()
        elif self.slot == self.solitaire.stock:
            self.move_on_top()
            self.place(self.solitaire.waste)
            self.turn_face_up()

    def doubleclick(self, e):
        self.get_draggable_pile()
        if self.face_up and len(self.draggable_pile) == 1:
            self.move_on_top()
            for slot in self.solitaire.foundations:
                if self.solitaire.check_foundations_rules(self, slot):
                    self.place(slot)
                    return
