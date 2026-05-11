# Step 8: Move piles of cards from stackable slots to stackable slots.

import random
from dataclasses import dataclass, field
from typing import Optional

import flet as ft

# Constants for layout and styling
BG_COLOR = "#207F4C"

# Card aspect ratio (height / width)
CARD_ASPECT = 100 / 70
COLS = 7
# gap as a fraction of card width — used for sides, top, and between cards
GAP_FACTOR = 0.15


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
    col: int  # column index (0..6)
    row: int  # row index (0=top, 1=bottom)
    top: float = 0
    left: float = 0
    cards: list["Card"] = field(default_factory=list)
    stacking: bool = False  # whether cards in this slot stack with offset


@ft.observable
@dataclass
class Card:
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
    card_w: float = 70
    card_h: float = 100
    offset_y: float = 15
    snap_threshold: float = 25
    cards: list[Card] = field(
        default_factory=lambda: [
            Card(id=f"{suite.name}_{rank.name}", suite=suite, rank=rank)
            for suite in suites
            for rank in ranks
        ]
    )
    slots: list[Slot] = field(
        default_factory=lambda: [
            Slot(id="deck", col=0, row=0),
            Slot(id="waste", col=1, row=0),
            Slot(id="foundation1", col=3, row=0),
            Slot(id="foundation2", col=4, row=0),
            Slot(id="foundation3", col=5, row=0),
            Slot(id="foundation4", col=6, row=0),
            Slot(id="tableau1", col=0, row=1, stacking=True),
            Slot(id="tableau2", col=1, row=1, stacking=True),
            Slot(id="tableau3", col=2, row=1, stacking=True),
            Slot(id="tableau4", col=3, row=1, stacking=True),
            Slot(id="tableau5", col=4, row=1, stacking=True),
            Slot(id="tableau6", col=5, row=1, stacking=True),
            Slot(id="tableau7", col=6, row=1, stacking=True),
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

    def layout(self, width: float):
        """Recompute slot positions and card sizes for the given board width."""
        if width <= 0:
            return
        # width = card_w * COLS + gap * (COLS + 1), where gap = card_w * GAP_FACTOR
        factor = COLS + GAP_FACTOR * (COLS + 1)
        self.card_w = width / factor
        self.card_h = self.card_w * CARD_ASPECT
        gap = self.card_w * GAP_FACTOR
        self.offset_y = self.card_h * 0.18
        self.snap_threshold = self.card_w * 0.4

        col_step = self.card_w + gap
        # Equal gap on top, between rows, and sides
        row_y = [gap, gap + self.card_h + gap]

        for s in self.slots:
            s.left = gap + s.col * col_step
            s.top = row_y[s.row]

        # Snap each card back to its home slot's new coordinates
        for slot in self.slots:
            for i, c in enumerate(slot.cards):
                c.left = slot.left
                c.top = slot.top + (self.offset_y * i if slot.stacking else 0)

    def move_to_top(self, cards: list[Card]):
        for card in cards:
            self.cards.remove(card)
            self.cards.append(card)

    def nearest_slot(self, card: Card) -> Optional[Slot]:
        """Return the nearest slot to the card within snap_threshold, or None."""
        for s in self.slots:
            if s != card.home:
                offset = (
                    (len(s.cards) - 1) * self.offset_y
                    if s.stacking and len(s.cards) > 0
                    else 0
                )
                near_x = abs(card.left - s.left) < self.snap_threshold
                near_y = abs(card.top - (s.top + offset)) < self.snap_threshold
                if near_x and near_y:
                    return s
        return None

    def point_in_card_stack(self, x: float, y: float) -> Optional[list[Card]]:
        # Check topmost first so you can grab the card on top
        for c in reversed(self.cards):
            if (c.left <= x <= c.left + self.card_w) and (
                c.top <= y <= c.top + self.card_h
            ):
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
            slot.top + self.offset_y * (len(slot.cards) - 1)
            if slot.stacking
            else slot.top
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
def CardView(
    card: Card, card_w: float, card_h: float, on_card_click, key=None
) -> ft.Control:
    return ft.Container(
        left=card.left,
        top=card.top,
        width=card_w,
        height=card_h,
        border_radius=5,
        content=(
            ft.Image(src=f"/images/{card.rank.name}_{card.suite.name}.svg")
            if card.face_up
            else ft.Image(src="/images/card_back.png")
        ),
        on_click=lambda _e: on_card_click(card),
    )


@ft.component
def SlotView(
    slot: Slot, card_w: float, card_h: float, on_slot_click, key=None
) -> ft.Control:
    return ft.Container(
        left=slot.left,
        top=slot.top,
        width=card_w,
        height=card_h,
        border=ft.Border.all(1, ft.Colors.BLACK_12),
        border_radius=10,
        on_click=lambda _e: on_slot_click(slot),
    )


# ---------- App ----------


@ft.component
def App():
    page = ft.context.page
    page.title = "Solitaire"
    page.padding = 0
    page.bgcolor = BG_COLOR

    game, set_game = ft.use_state(lambda: Game())
    board_w, set_board_w = ft.use_state(0.0)
    dragging, set_dragging = ft.use_state(None)  # None or list[Card] being dragged
    start_x, set_start_x = ft.use_state(None)  # initial x of the card being dragged
    start_y, set_start_y = ft.use_state(None)  # initial y of the card being dragged

    ft.use_effect(lambda: game.layout(board_w), [game, board_w])

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
        game.notify()

    def on_pan_end(_: ft.DragEndEvent):
        if dragging is None or not dragging[0].face_up:
            return

        s = game.nearest_slot(dragging[0])

        if s is not None and game.rules_allow_move(dragging, s):
            for c in dragging:
                game.place_card_in_slot(c, s)  # snap to this slot

        else:  # bounce back to where it was picked up
            for i, c in enumerate(dragging):
                c.left, c.top = start_x, start_y + i * game.offset_y

        game.notify()
        set_dragging(None)

    def open_card_and_notify(card: Card):
        game.open_card(card)
        game.notify()

    def reset_deck_and_notify(slot: Slot):
        game.reset_deck(slot)
        game.notify()

    cb_reset_deck = ft.use_callback(reset_deck_and_notify, [game])
    cb_open_card = ft.use_callback(open_card_and_notify, [game])

    MemoSlotView = ft.memo(SlotView)
    MemoCardView = ft.memo(CardView)

    board = ft.GestureDetector(
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=5,
        on_size_change=lambda e: set_board_w(e.width),
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(expand=True, bgcolor=BG_COLOR, key="bg")
            ]  # to capture full area
            + [
                MemoSlotView(s, game.card_w, game.card_h, cb_reset_deck, key=s.id)
                for s in game.slots
            ]
            + [
                MemoCardView(c, game.card_w, game.card_h, cb_open_card, key=c.id)
                for c in game.cards
            ],
        ),
    )

    bottom_bar = ft.Container(
        bottom=0,
        padding=10,
        content=ft.Row(
            controls=[
                ft.FilledButton("New Game", on_click=lambda _: set_game(Game())),
                ft.Text(
                    f"Cards in deck: {len(game.slots[0].cards)}",
                    color=ft.Colors.WHITE,
                ),
                ft.Text(
                    f"Cards in waste: {len(game.slots[1].cards)}",
                    color=ft.Colors.WHITE,
                ),
            ],
        ),
    )

    return ft.Stack(
        expand=True,
        controls=[
            ft.Container(expand=True, content=board),
            bottom_bar,
        ],
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
