# Step 8: Move piles of cards from stackable slots to stackable slots.

import random
from dataclasses import dataclass, field
from typing import Optional

import flet as ft

# Card visual constants
CARD_W = 70
CARD_H = 100
SNAP_THRESHOLD = 25  # px
OFFSET_Y = 15  # px


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

        # Deal cards in tableau1..tableau7
        n = 6
        i = 0
        for card in self.cards:
            self.place_card_in_slot(card, self.slots[n])
            n = n + 1 if n < 12 else 6 + i
            if n >= 12:
                if i < 7:
                    i = i + 1
                else:
                    break

        # Place remaining cards in the deck
        for c in self.cards[self.cards.index(card) + 1 :]:
            self.place_card_in_slot(c, self.slots[0])

        # Turn last card in each tableau face up
        for slot in self.slots[6:]:
            slot.cards[-1].face_up = True

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

    def place_card_in_slot(self, card: Card, slot: Slot):
        """Place a card in a slot, updating its home and position."""
        if card.home is not None:
            card.home.cards.remove(card)  # Remove card from previous slot's pile
        card.home = slot  # <-- update to the Slot object
        slot.cards.append(card)  # Add card to the slot's pile
        card.left = slot.left
        card.top = (
            slot.top + OFFSET_Y * (len(slot.cards) - 1) if slot.stacking else slot.top
        )
        if self.check_win():
            ft.context.page.show_dialog(
                ft.AlertDialog(
                    title=ft.Text("You won!"),
                    actions=[
                        ft.TextButton(
                            "OK", on_click=lambda e: ft.context.page.pop_dialog()
                        )
                    ],
                )
            )

    def open_card(self, card: Card):
        # Only flip/move if: face-down, in deck, and it's the top card of the deck
        if (
            not card.face_up and card.home.cards[-1] == card
        ):  # flip only if it's face down and the top card in the slot
            card.face_up = True
            self.move_to_top([card])
            if card.home.id == "deck":  # move to waste
                self.place_card_in_slot(card, self.slots[1])  # move to waste slot

    def reset_deck(self, slot: Slot):
        # Move all cards from waste back to deck in REVERSED order, face down.
        if slot.id != "deck":
            return

        if len(slot.cards) > 0:
            return  # only reset if deck is empty

        # deck = self.slots[0]  # or self.find_slot_by_id("deck")
        # waste = self.slots[1]  # or self.find_slot_by_id("waste")

        while len(self.slots[1].cards) > 0:
            card = self.slots[1].cards[-1]
            card.face_up = False
            self.move_to_top([card])
            self.place_card_in_slot(card, self.slots[0])

        print("Current cards in deck:", len(self.slots[0].cards))

    def rules_allow_move(self, cards: list[Card], slot: Slot) -> bool:
        """Basic Solitaire rules for moving cards between slots"""
        # Moving to foundation slots
        if slot.id.startswith("foundation"):
            if len(cards) != 1:
                return False  # can move only one card at a time to foundation
            else:
                if len(slot.cards) == 0 and cards[0].rank.value == 1:
                    return True  # Ace can be placed in empty foundation
                elif len(slot.cards) > 0:
                    top_card = slot.cards[-1]
                    if (
                        cards[0].suite == top_card.suite
                        and cards[0].rank.value == top_card.rank.value + 1
                    ):
                        return True  # same suite, one rank higher
            return False  # otherwise not allowed
        elif slot.id.startswith("tableau"):
            # Moving to tableau slots
            if len(slot.cards) == 0:
                return cards[0].rank.value == 13  # King can be placed in empty tableau
            else:
                top_card = slot.cards[-1]
                if (
                    cards[0].suite.color != top_card.suite.color
                    and cards[0].rank.value == top_card.rank.value - 1
                ):
                    return True  # alternating colors, one rank lower
            return False  # otherwise not allowed
        else:  # moving to deck or waste (not allowed)
            return False

    def check_win(self):
        # Win if all 4 foundation slots have 13 cards each
        return all(len(slot.cards) == 13 for slot in self.slots[2:6])


# ---------- View (pure) ----------
@ft.component
def CardView(card: Card, on_card_click) -> ft.Control:
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
        on_click=lambda _e: on_card_click(card),
    )


@ft.component
def SlotView(slot: Slot, on_slot_click) -> ft.Control:
    return ft.Container(
        margin=5,
        left=slot.left,
        top=slot.top,
        width=CARD_W,
        height=CARD_H,
        border=ft.Border.all(1, ft.Colors.SECONDARY_CONTAINER),
        border_radius=5,
        content=ft.Text(slot.id, size=10, color=ft.Colors.BLACK45),
        on_click=lambda _e: on_slot_click(slot),
    )


# ---------- App ----------
@ft.component
def App():
    game, set_game = ft.use_state(lambda: Game())
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

        if s is not None and game.rules_allow_move(dragging, s):
            for c in dragging:
                game.place_card_in_slot(c, s)  # snap to this slot

        else:  # bounce back to where it was picked up
            for i, c in enumerate(dragging):
                c.left, c.top = start_x, start_y + i * OFFSET_Y

        set_dragging(None)

    board = ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[
                ft.Container(expand=True, bgcolor="#207F4C")
            ]  # to capture full area
            + [SlotView(s, game.reset_deck) for s in game.slots]
            + [CardView(c, game.open_card) for c in game.cards],
            width=1000,
            height=500,
        ),
    )

    bottom_bar = ft.Row(
        controls=[
            ft.FilledButton("New Game", on_click=lambda _: set_game(Game())),
            ft.Text(f"Cards in deck: {len(game.slots[0].cards)}"),
            ft.Text(f"Cards in waste: {len(game.slots[1].cards)}"),
        ]
    )

    return ft.Column(
        expand=True,
        spacing=0,
        controls=[
            ft.Container(expand=True, content=board),
            bottom_bar,
        ],
    )


ft.run(lambda page: page.render(App))
