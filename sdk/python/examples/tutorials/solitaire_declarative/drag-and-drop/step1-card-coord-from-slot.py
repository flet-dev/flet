from dataclasses import dataclass

import flet as ft

# Visual constants
CARD_W, CARD_H = 70, 100
BASE_X, BASE_Y = 200, 40  # base position for the card (not stored on the card)


# -------- Model (no coordinates on the card) --------
@ft.observable
@dataclass
class Card:
    id: str
    color: str


# -------- Presentational card --------
@ft.component
def CardView(card: Card, left: float, top: float) -> ft.Control:
    return ft.Container(
        key=card.id,
        left=left,
        top=top,
        width=CARD_W,
        height=CARD_H,
        bgcolor=card.color,
        border_radius=5,
    )


# -------- App --------
@ft.component
def App():
    card, _ = ft.use_state(Card(id="c1", color=ft.Colors.GREEN))

    # Ephemeral drag offsets (not in the card)
    dx, set_dx = ft.use_state(0.0)
    dy, set_dy = ft.use_state(0.0)
    dragging, set_dragging = ft.use_state(False)

    def card_left():
        return BASE_X + dx

    def card_top():
        return BASE_Y + dy

    def hit_card(x: float, y: float) -> bool:
        return (
            card_left() <= x <= card_left() + CARD_W
            and card_top() <= y <= card_top() + CARD_H
        )

    def on_tap_down(e: ft.TapEvent):
        if hit_card(e.local_position.x, e.local_position.y):
            print("Card clicked")

    def on_pan_start(e: ft.DragStartEvent):
        # Only start dragging if the gesture begins inside the card
        set_dragging(hit_card(e.local_position.x, e.local_position.y))

    def on_pan_update(e: ft.DragUpdateEvent):
        if dragging:
            set_dx(dx + e.local_delta.x)
            set_dy(dy + e.local_delta.y)

    def on_pan_end(_: ft.DragEndEvent):
        set_dragging(False)  # keep dx/dy so the card stays where you dropped it
        # If you want it to bounce back, uncomment:
        # set_dx(0.0); set_dy(0.0)

    slot = ft.Container(  # optional visual reference for base position
        left=BASE_X,
        top=BASE_Y,
        width=CARD_W,
        height=CARD_H,
        border=ft.Border.all(1, ft.Colors.BLACK45),
        border_radius=5,
    )

    return ft.GestureDetector(
        drag_interval=5,
        on_tap_down=on_tap_down,
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        content=ft.Stack(
            width=500,
            height=300,
            controls=[
                slot,
                CardView(card, left=card_left(), top=card_top()),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
