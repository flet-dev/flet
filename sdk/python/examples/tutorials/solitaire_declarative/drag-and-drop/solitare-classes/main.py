# Step 8: Move piles of cards from stackable slots to stackable slots.

import random
from dataclasses import dataclass, field
from typing import Optional

import flet as ft

# Card visual constants
CARD_W = 70
CARD_H = 100
SNAP_THRESHOLD = 20  # px
OFFSET_Y = 20  # px


# ---------- Model ----------
@dataclass
class Suite:
    name: str
    color: str


@dataclass
class Rank:
    name: str
    value: int


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
    # color: str
    id: str
    suite: Suite
    rank: Rank
    face_up: bool = False
    top: float = 0
    left: float = 0
    home: Optional[Slot] = None  # <-- reference to a Slot, not a string


@ft.observable
@dataclass
class Game:
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(id=f"{suite.name}_{rank.name}", suite=suite, rank=rank)
            for suite in suites
            for rank in ranks
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(left=0, top=0, id="deck"),
            Slot(left=100, top=0, id="waste"),
            Slot(left=300, top=0, id="foundation1"),
            Slot(left=400, top=0, id="foundation2"),
            Slot(left=500, top=0, id="foundation3"),
            Slot(left=600, top=0, id="foundation4"),
            Slot(left=0, top=200, id="tableau1", stacking=True),
            Slot(left=100, top=200, id="tableau2", stacking=True),
            Slot(left=200, top=200, id="tableau3", stacking=True),
            Slot(left=300, top=200, id="tableau4", stacking=True),
            Slot(left=400, top=200, id="tableau5", stacking=True),
            Slot(left=500, top=200, id="tableau6", stacking=True),
            Slot(left=600, top=200, id="tableau7", stacking=True),
        ],
    )

    def __post_init__(self):
        """Initialize homes & coordinates: place cards in the deck slot."""
        random.shuffle(self.cards)

        n = 6  # place first n cards in tableau1 for easier testing
        i = 0
        for card in self.cards:
            card.home = self.slots[n]
            self.slots[n].cards.append(card)
            card.left, card.top = (
                self.slots[n].left,
                self.slots[n].top + OFFSET_Y * (len(self.slots[n].cards) - 1),
            )
            n = n + 1 if n < 12 else 6 + i
            if n >= 12:
                if i < 7:
                    i = i + 1
                else:
                    print(
                        "number of cards in each tableau:", self.cards.index(card) + 1
                    )
                    break

        # Place remaining cards in the deck
        for c in self.cards[self.cards.index(card) + 1 :]:
            c.home = self.slots[0]
            self.slots[0].cards.append(c)
            c.left, c.top = self.slots[0].left, self.slots[0].top

        # Turn last card in each tableau face up
        for slot in self.slots[6:]:
            slot.cards[-1].face_up = True

        # for card in self.cards:
        #     card.home = self.slots[0]
        #     card.left, card.top = self.slots[0].left, self.slots[0].top

        # Add cards to deck card list
        # self.slots[0].cards = self.cards.copy()

    def move_to_top(self, cards: list[Card]):
        for card in cards:
            self.cards.remove(card)
            self.cards.append(card)

    def nearest_slot(self, card: Card) -> Optional[Slot]:
        """Return the nearest slot to the card within SNAP_THRESHOLD, or None."""
        for s in self.slots:
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

    def point_in_card_stack(self, x: float, y: float) -> Optional[list[Card]]:
        # Check topmost first so you can grab the card on top
        for c in reversed(self.cards):
            if (c.left <= x <= c.left + CARD_W) and (c.top <= y <= c.top + CARD_H):
                return [c] + c.home.cards[
                    c.home.cards.index(c) + 1 :
                ]  # return the card and all cards below it
        return None


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card) -> ft.Control:
    def click_on_card(_e):
        if not card.face_up:
            card.face_up = True

    return ft.Container(
        left=card.left,
        top=card.top,
        width=CARD_W,
        height=CARD_H,
        margin=5,
        border_radius=5,
        content=ft.Image(src=f"/images/{card.rank.name}_{card.suite.name}.svg")
        if card.face_up
        else ft.Image(src="/images/card_back.png"),
        on_click=click_on_card,
    )


@ft.component
def SlotView(slot: Slot) -> ft.Control:
    return ft.Container(
        margin=5,
        left=slot.left,
        top=slot.top,
        width=CARD_W,
        height=CARD_H,
        border=ft.Border.all(1, ft.Colors.SECONDARY_CONTAINER),
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

    def on_pan_start(e: ft.DragStartEvent):
        grabbed = game.point_in_card_stack(e.local_position.x, e.local_position.y)
        # set_dragging(grabbed[0] if grabbed else None)
        set_dragging(grabbed)
        if grabbed is not None and grabbed[0].face_up:
            game.move_to_top(grabbed)
            set_start_x(
                grabbed[0].left
            )  # remember initial x of the top card being dragged
            set_start_y(
                grabbed[0].top
            )  # remember initial y of the top card being dragged

    def on_pan_update(e: ft.DragUpdateEvent):
        if dragging is None or not dragging[0].face_up:
            return
        for c in dragging:
            c.left = max(0, c.left + e.local_delta.x)
            c.top = max(0, c.top + e.local_delta.y)

    def on_pan_end(_: ft.DragEndEvent):
        if dragging is None or not dragging[0].face_up:
            return

        s = game.nearest_slot(dragging[0])
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
                ft.Container(expand=True, bgcolor="#207F4C")
            ]  # to capture full area
            + [SlotView(s) for s in game.slots]
            + [CardView(c) for c in game.cards],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
