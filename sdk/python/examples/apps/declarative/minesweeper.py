# Step 1: Basic drag-and-drop of rectangles (cards) within a bounded area.

import random
from dataclasses import dataclass
from typing import Optional

import flet as ft

# ----------- Visual constants ----------
SQUARE_SIZE = 40


# ---------- Model ----------
@ft.observable
@dataclass
class Square:
    top: float = 0
    left: float = 0
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    adjacent_mines: int = 0


@ft.observable
@dataclass
class Game:
    squares: Optional[list[Square]] = None  # to be initialized in __post_init__
    rows: int = 9
    cols: int = 9
    mine_count: int = 10

    def __post_init__(self):
        """Initialize the grid of squares."""
        self.squares = []
        for r in range(self.rows):
            for c in range(self.cols):
                self.squares.append(Square(left=c * SQUARE_SIZE, top=r * SQUARE_SIZE))

        # place mines
        mine_positions = random.sample(range(len(self.squares)), self.mine_count)
        for pos in mine_positions:
            self.squares[pos].mine = True

    def square_revealed(self, square: Square):
        square.revealed = True


# ---------- View (pure) ----------
@ft.component
def SquareView(square: Square, square_revealed) -> ft.Control:
    # Pure view: just render from state
    return ft.Container(
        bgcolor=ft.Colors.GREY if not square.revealed else ft.Colors.GREY_100,
        align=ft.Alignment.CENTER,
        content=ft.Text(
            "💣"
            if square.revealed and square.mine
            else "🚩"
            if square.flagged
            else str(square.adjacent_mines)
            if square.revealed and square.adjacent_mines > 0
            else "",
            size=30,
        ),
        left=square.left,
        top=square.top,
        border=ft.Border.all(1, ft.Colors.BLACK),
        width=SQUARE_SIZE,
        height=SQUARE_SIZE,
        on_click=lambda _e: square_revealed(square),
    )


# ---------- App ----------
@ft.component
def App():
    game, _ = ft.use_state(lambda: Game())

    return ft.GestureDetector(
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        content=ft.Stack(
            controls=[SquareView(c, game.square_revealed) for c in game.squares],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
