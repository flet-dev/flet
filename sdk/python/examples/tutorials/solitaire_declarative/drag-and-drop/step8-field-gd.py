# Step 8: Move piles of cards from stackable slots to stackable slots.

from dataclasses import dataclass, field
from typing import Optional

import flet as ft


# ---------- Model ----------
@ft.observable
@dataclass
class Slot:
    id: str
    top: float
    left: float
    cards: list["Card"] = field(default_factory=list)
    stacking: bool = False  # whether cards in this slot stack with offset


@ft.observable
@dataclass
class Card:
    color: str
    top: float = 0
    left: float = 0
    home: Optional[Slot] = None  # <-- reference to a Slot, not a string


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(color=ft.Colors.GREEN),  # positions will be set in __post_init__
            Card(color=ft.Colors.RED),
            Card(color=ft.Colors.BLUE),
            Card(color=ft.Colors.YELLOW),
            Card(color=ft.Colors.PURPLE),
            Card(color=ft.Colors.ORANGE),
            Card(color=ft.Colors.BROWN),
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(left=0, top=0, id="deck"),
            Slot(left=100, top=0, id="waste"),
            Slot(left=200, top=0, id="foundation1"),
            Slot(left=300, top=0, id="foundation2"),
            Slot(left=0, top=200, id="slot1", stacking=True),
            Slot(left=100, top=200, id="slot2", stacking=True),
            Slot(left=200, top=200, id="slot3", stacking=True),
        ],
    )
    # snap_threshold: float = 20  # px

    def __post_init__(self):
        """Initialize homes & coordinates: place cards in the deck slot."""

        for card in self.cards:
            card.home = self.slots[0]
            card.left, card.top = self.slots[0].left, self.slots[0].top

        # Add cards to deck card list
        self.slots[0].cards = self.cards.copy()
        print("deck has cards:", len(self.slots[0].cards))


# Card visual constants
CARD_W = 70
CARD_H = 100
SNAP_THRESHOLD = 20  # px
OFFSET_Y = 20  # px


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card) -> ft.Control:
    return ft.Container(
        bgcolor=card.color,
        left=card.left,
        top=card.top,
        width=CARD_W,
        height=CARD_H,
        border_radius=5,
    )


@ft.component
def SlotView(slot: Slot) -> ft.Control:
    return ft.Container(
        left=slot.left,
        top=slot.top,
        width=CARD_W,
        height=CARD_H,
        border=ft.Border.all(1, ft.Colors.PRIMARY),
        border_radius=5,
        content=ft.Text(slot.id, size=10, color=ft.Colors.BLACK45),
    )


# ---------- App ----------
@ft.component
def App():
    game, _ = ft.use_state(lambda: Game())
    dragging, set_dragging = ft.use_state(None)  # None or list[Card] being dragged
    start_x, set_start_x = ft.use_state(None)  # initial x of the card being dragged
    start_y, set_start_y = ft.use_state(None)  # initial y of the card being dragged

    print("Current cards in deck:", len(game.slots[0].cards))

    def point_in_card_stack(x: float, y: float) -> Optional[list[Card]]:
        # Check topmost first so you can grab the card on top
        for c in reversed(game.cards):
            if (c.left <= x <= c.left + CARD_W) and (c.top <= y <= c.top + CARD_H):
                return [c] + c.home.cards[
                    c.home.cards.index(c) + 1 :
                ]  # return the card and all cards below it
        return None

    def move_to_top(cards: list[Card]):
        for card in cards:
            game.cards.remove(card)
            game.cards.append(card)

    def nearest_slot(card: Card) -> Optional[Slot]:
        """Return the nearest slot to the card within SNAP_THRESHOLD, or None."""
        for s in game.slots:
            if s != card.home:
                offset = (
                    (len(s.cards) - 1) * OFFSET_Y
                    if s.stacking and len(s.cards) > 0
                    else 0
                )
                near_x = abs(card.left - s.left) < SNAP_THRESHOLD
                near_y = abs(card.top - (s.top + offset)) < SNAP_THRESHOLD
                if near_x and near_y:
                    return s
        return None

    def on_pan_start(e: ft.DragStartEvent):
        grabbed = point_in_card_stack(e.local_position.x, e.local_position.y)
        print("grabbed", grabbed)
        # set_dragging(grabbed[0] if grabbed else None)
        set_dragging(grabbed)
        if grabbed is not None:
            move_to_top(grabbed)
            set_start_x(
                grabbed[0].left
            )  # remember initial x of the top card being dragged
            set_start_y(
                grabbed[0].top
            )  # remember initial y of the top card being dragged

    def on_pan_update(e: ft.DragUpdateEvent):
        if dragging is None:
            return
        print("length of dragging", len(dragging))
        for c in dragging:
            c.left = max(0, c.left + e.local_delta.x)
            c.top = max(0, c.top + e.local_delta.y)

    def on_pan_end(_: ft.DragEndEvent):
        if dragging is None:
            return

        s = nearest_slot(dragging[0])
        if s is not None:  # snap to this slot
            for c in dragging:
                c.left = s.left
                c.top = s.top + OFFSET_Y * (len(s.cards)) if s.stacking else s.top
                c.home.cards.remove(c)  # Remove card from previous slot's pile
                c.home = s  # <-- update to the Slot object
                s.cards.append(c)  # Add card to the slot's pile

        else:  # bounce back to where it was picked up
            for i, c in enumerate(dragging):
                c.left, c.top = start_x, start_y + i * OFFSET_Y

        set_dragging(None)

    return ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[
                *(SlotView(s) for s in game.slots),
                *(CardView(c) for c in game.cards),
            ],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
