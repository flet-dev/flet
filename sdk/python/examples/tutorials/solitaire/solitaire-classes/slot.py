SLOT_WIDTH = 70
SLOT_HEIGHT = 100

import flet as ft


class Slot(ft.Container):
    def __init__(self, top, left):
        super().__init__()
        self.pile = []
        self.width = SLOT_WIDTH
        self.height = SLOT_HEIGHT
        self.left = left
        self.top = top
        self.border = ft.border.all(1)
