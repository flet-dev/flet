import flet as ft

# Using Container for slot where the card should be dropped
# on_pan_start event for the card: remember position of card to bounce it back on_pan_end of needed.
# on_pan_end: check if card is in proximity of the slot and either place it to the slot or return to original position (bounce back).
# Solitaire class created for holding original position coordinates


class Solitaire:
    def __init__(self):
        self.start_top = 0
        self.start_left = 0


def main(page: ft.Page):
    def place(card, slot):
        """place card to the slot"""
        card.top = slot.top
        card.left = slot.left

    def bounce_back(game, card):
        """return card to its original position"""
        card.top = game.start_top
        card.left = game.start_left

    def start_drag(e: ft.DragStartEvent):
        solitaire.start_top = e.control.top
        solitaire.start_left = e.control.left

    def drag(e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        e.control.update()

    def drop(e: ft.DragEndEvent):
        if abs(e.control.top - slot.top) < 20 and abs(e.control.left - slot.left) < 20:
            place(e.control, slot)

        else:
            bounce_back(solitaire, e.control)

        e.control.update()

    slot = ft.Container(width=70, height=100, left=200, top=0, border=ft.border.all(1))

    card = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.MOVE,
        drag_interval=5,
        on_pan_start=start_drag,
        on_pan_update=drag,
        on_pan_end=drop,
        left=0,
        top=0,
        content=ft.Container(bgcolor=ft.Colors.GREEN, width=70, height=100),
    )

    solitaire = Solitaire()

    page.add(ft.Stack(controls=[slot, card], width=1000, height=500))


ft.app(target=main)
