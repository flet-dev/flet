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
    tapped: bool = False
    adjacent_mines: int = 0


@ft.observable
@dataclass
class Game:
    squares: Optional[list[Square]] = None  # to be initialized in __post_init__
    rows: int = 9
    cols: int = 9
    mine_count: int = 10
    over = False

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
        square.tapped = True
        if square.mine:
            self.over = True
            for sq in self.squares:
                if sq.mine:
                    sq.revealed = True
            print("Game Over!")
        elif square.adjacent_mines == 0:
            # reveal adjacent squares
            r = int(square.top / SQUARE_SIZE)
            c = int(square.left / SQUARE_SIZE)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        nidx = nr * self.cols + nc
                        nsq = self.squares[nidx]
                        if not nsq.revealed and not nsq.mine:
                            self.square_revealed(nsq)

    def square_flagged(self, square: Square):
        if not square.revealed:
            square.flagged = not square.flagged


# ---------- View (pure) ----------
@ft.component
def SquareView(square: Square, square_revealed) -> ft.Control:
    # Pure view: just render from state
    return ft.Container(
        bgcolor=(
            ft.Colors.RED_400
            if (square.revealed and square.mine and square.tapped)
            else ft.Colors.GREY_300
            if square.revealed
            else ft.Colors.GREY_400
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
            text_align=ft.TextAlign.CENTER,
            align=ft.Alignment.CENTER,
            weight=ft.FontWeight.BOLD,
            color=(
                ft.Colors.BLUE
                if square.adjacent_mines == 1
                else ft.Colors.GREEN
                if square.adjacent_mines == 2
                else ft.Colors.RED
                if square.adjacent_mines == 3
                else ft.Colors.ORANGE
                if square.adjacent_mines == 4
                else ft.Colors.PURPLE
                if square.adjacent_mines == 5
                else ft.Colors.BROWN
                if square.adjacent_mines == 6
                else ft.Colors.TEAL
                if square.adjacent_mines == 7
                else ft.Colors.BLACK
                if square.adjacent_mines == 8
                else ft.Colors.BLACK
            ),
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
    game, set_game = ft.use_state(lambda: Game())
    new_game_tapped, set_new_game_tapped = ft.use_state(False)

    def on_tap_down(e: ft.TapEvent):
        # e.local_position.x / e.local_position.y are relative to the GestureDetector
        # content (the Stack)
        if game.over:
            return
        for s in game.squares:
            if (
                s.left <= e.local_position.x <= s.left + SQUARE_SIZE
                and s.top <= e.local_position.y <= s.top + SQUARE_SIZE
            ):
                game.square_revealed(s)
                break

    def on_right_pan_start(e):
        print("right pan start", e)
        for s in game.squares:
            if (
                s.left <= e.local_position.x <= s.left + SQUARE_SIZE
                and s.top <= e.local_position.y <= s.top + SQUARE_SIZE
            ):
                game.square_flagged(s)
                break

    board = ft.GestureDetector(
        drag_interval=5,
        mouse_cursor=ft.MouseCursor.MOVE,
        on_tap_down=on_tap_down,
        on_right_pan_start=on_right_pan_start,
        content=ft.Stack(
            controls=[SquareView(c, game.square_revealed) for c in game.squares],
            width=1000,
            height=500,
        ),
    )

    top_menu = ft.Row(
        controls=[
            ft.Text("000", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Image(
                    src="/images/neutral.png" if not game.over else "/images/cry.png",
                    width=30,
                ),
                bgcolor=ft.Colors.GREY_400,
                on_tap_down=lambda e: set_new_game_tapped(True),
                on_click=lambda e: (set_game(Game()), set_new_game_tapped(False)),
                width=60,
                height=60,
                foreground_decoration=ft.BoxDecoration(
                    border=ft.Border(
                        bottom=ft.BorderSide(4, ft.Colors.BLACK38),
                        right=ft.BorderSide(4, ft.Colors.BLACK38),
                        top=ft.BorderSide(4, ft.Colors.WHITE70),
                        left=ft.BorderSide(4, ft.Colors.WHITE70),
                    )
                    if not new_game_tapped
                    else None
                ),
            ),
            ft.Text(f"Mines: {game.mine_count}"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        width=300,
    )

    return ft.Column(
        controls=[
            top_menu,
            board,
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        spacing=10,
    )


ft.run(lambda page: page.render(App))
