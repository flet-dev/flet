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

        # calculate adjacent mine counts
        for r in range(self.rows):
            for c in range(self.cols):
                idx = r * self.cols + c
                if self.squares[idx].mine:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            nidx = nr * self.cols + nc
                            if self.squares[nidx].mine:
                                count += 1
                self.squares[idx].adjacent_mines = count

    def square_revealed(self, square: Square):
        square.revealed = True


# ---------- View (pure) ----------
@ft.component
def SquareView(square: Square, square_revealed) -> ft.Control:
    # Pure view: just render from state
    return ft.Container(
        bgcolor=(
            ft.Colors.RED_400
            if (square.revealed and square.mine)
            else ft.Colors.GREY_300
            if square.revealed
            else ft.Colors.GREY
        ),
        align=ft.Alignment.CENTER,
        foreground_decoration=ft.BoxDecoration(
            border=ft.Border(
                bottom=ft.BorderSide(4, ft.Colors.BLACK38),
                right=ft.BorderSide(4, ft.Colors.BLACK38),
                top=ft.BorderSide(4, ft.Colors.WHITE70),
                left=ft.BorderSide(4, ft.Colors.WHITE70),
            )
            if not square.revealed
            else None
        ),
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
        border=ft.Border.all(1, ft.Colors.GREY_500) if square.revealed else None,
        width=SQUARE_SIZE,
        height=SQUARE_SIZE,
        # on_click=lambda _e: square_revealed(square),
    )


# ---------- App ----------
@ft.component
def App():
    game, _ = ft.use_state(lambda: Game())

    def on_tap_down(e: ft.TapEvent):
        # e.local_position.x / e.local_position.y are relative to the GestureDetector
        # content (the Stack)
        for s in game.squares:
            if (
                s.left <= e.local_position.x <= s.left + SQUARE_SIZE
                and s.top <= e.local_position.y <= s.top + SQUARE_SIZE
            ):
                game.square_revealed(s)
                break

    return ft.GestureDetector(
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        on_tap_down=on_tap_down,
        content=ft.Stack(
            controls=[SquareView(c, game.square_revealed) for c in game.squares],
            width=1000,
            height=500,
        ),
    )


ft.run(lambda page: page.render(App))
