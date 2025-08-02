CARD_WIDTH = 70
CARD_HEIGTH = 100
DROP_PROXIMITY = 20

import flet as ft


class Card(ft.GestureDetector):
    def __init__(self, solitaire, color):
        super().__init__()
        self.slot = None
        self.mouse_cursor = ft.MouseCursor.MOVE
        self.drag_interval = 5
        self.on_pan_start = self.start_drag
        self.on_pan_update = self.drag
        self.on_pan_end = self.drop
        self.left = None
        self.top = None
        self.solitaire = solitaire
        self.color = color
        self.content = ft.Container(
            bgcolor=self.color, width=CARD_WIDTH, height=CARD_HEIGTH
        )

    def move_on_top(self):
        """Moves draggable card to the top of the stack"""
        self.solitaire.controls.remove(self)
        self.solitaire.controls.append(self)
        self.solitaire.update()

    def bounce_back(self):
        """Returns card to its original position"""
        self.top = self.slot.top
        self.left = self.slot.left
        self.update()

    def place(self, slot):
        """Place card to the slot"""
        self.top = slot.top
        self.left = slot.left
        self.slot = slot

    def start_drag(self, e: ft.DragStartEvent):
        self.move_on_top()
        self.update()

    def drag(self, e: ft.DragUpdateEvent):
        self.top = max(0, self.top + e.delta_y)
        self.left = max(0, self.left + e.delta_x)
        self.update()

    def drop(self, e: ft.DragEndEvent):
        for slot in self.solitaire.slots:
            if (
                abs(self.top - slot.top) < DROP_PROXIMITY
                and abs(self.left - slot.left) < DROP_PROXIMITY
            ):
                self.place(slot)
                self.update()
                return

        self.bounce_back()
        self.update()
