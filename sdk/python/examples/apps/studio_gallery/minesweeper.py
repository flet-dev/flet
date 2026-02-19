import asyncio
import random
from dataclasses import dataclass
from typing import Optional

import flet as ft

SQUARE_SIZE = 30

LIGHT = ft.Colors.WHITE_70
DARK = ft.Colors.BLACK_38

BEVEL_RAISED = ft.Border(
    bottom=ft.BorderSide(4, DARK),
    right=ft.BorderSide(4, DARK),
    top=ft.BorderSide(4, LIGHT),
    left=ft.BorderSide(4, LIGHT),
)

BEVEL_SUNKEN = ft.Border(
    bottom=ft.BorderSide(4, LIGHT),
    right=ft.BorderSide(4, LIGHT),
    top=ft.BorderSide(4, DARK),
    left=ft.BorderSide(4, DARK),
)


@ft.observable
@dataclass
class Square:
    top: float = 0
    left: float = 0
    mine: bool = False
    revealed: bool = False
    flagged: bool = False
    exploded: bool = False
    adjacent_mines: int = 0


@ft.observable
@dataclass
class Game:
    squares: Optional[list[Square]] = None  # to be initialized in __post_init__
    rows: int = 9
    cols: int = 9
    mine_count: int = 10
    mines_left: int = 10
    over = False
    won = False
    # timer
    seconds: int = 0  # elapsed time
    running: bool = False  # ticking or not
    first_click_done: bool = False

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
        if square.mine:
            square.exploded = True
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
                        if not nsq.revealed and not nsq.mine and not nsq.flagged:
                            self.square_revealed(nsq)
        # check for win
        if all(sq.revealed or sq.mine for sq in self.squares):
            self.over = True
            self.won = True
            for sq in self.squares:
                if sq.mine and not sq.flagged:
                    sq.flagged = True
            print("You Win!")

    def square_flagged(self, square: Square):
        if not square.revealed:
            square.flagged = not square.flagged
            self.mines_left += -1 if square.flagged else 1


@ft.component
def SquareView(square: Square) -> ft.Control:
    return ft.Container(
        bgcolor=(
            ft.Colors.RED_900
            if square.exploded
            else ft.Colors.GREY_300
            if square.revealed
            else ft.Colors.GREY_400
        ),
        alignment=ft.Alignment.CENTER,
        foreground_decoration=ft.BoxDecoration(
            border=BEVEL_RAISED if not square.revealed else None
        ),
        content=ft.Text(
            "💥"
            if square.exploded
            else "💣"
            if square.revealed and square.mine
            else "🚩"
            if square.flagged
            else str(square.adjacent_mines)
            if square.revealed and square.adjacent_mines > 0
            else "",
            size=SQUARE_SIZE * 0.6,
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
    )


@ft.component
def App():
    game, set_game = ft.use_state(lambda: Game())
    new_game_tapped, set_new_game_tapped = ft.use_state(False)

    ticker_task, set_ticker_task = ft.use_state(None)
    is_mobile = ft.context.page.platform in (
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.IOS,
    )

    def end_game():
        game.running = False
        if ticker_task and not ticker_task.done():
            ticker_task.cancel()

    ft.on_unmounted(end_game)

    async def tick_loop():
        try:
            while True:
                await asyncio.sleep(1)
                if not game.running or game.over:
                    break
                game.seconds += 1
                print("Timer:", game.seconds)
        except asyncio.CancelledError:
            pass

    def ensure_ticker():
        if ticker_task is None or ticker_task.done():
            t = ft.context.page.run_task(tick_loop)
            set_ticker_task(t)

    last_tap_pos_ref = ft.use_ref(None)

    def on_tap_down(e: ft.TapEvent):
        last_tap_pos_ref.current = (e.local_position.x, e.local_position.y)

    def on_tap(e: ft.TapEvent):
        if game.over:
            return

        x, y = last_tap_pos_ref.current

        if not game.first_click_done:
            game.first_click_done = True
            game.running = True
            ensure_ticker()
            print("Timer started")

        for s in game.squares:
            if (
                s.left <= x <= s.left + SQUARE_SIZE
                and s.top <= y <= s.top + SQUARE_SIZE
            ):
                if s.flagged:
                    print("square is flagged, cannot reveal")
                    return
                game.square_revealed(s)
                break

    def on_right_pan_start(e):
        if game.over:
            return
        if not game.first_click_done:
            game.first_click_done = True
            game.running = True
            print("Timer started")
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
        on_tap=on_tap,
        on_right_pan_start=on_right_pan_start if not is_mobile else None,
        on_long_press_start=on_right_pan_start if is_mobile else None,
        content=ft.Stack(
            controls=[SquareView(c) for c in game.squares],
        ),
    )

    top_menu = ft.Row(
        controls=[
            ft.Container(
                height=50,
                width=90,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    f"{game.mines_left:03d}",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED,
                ),
                foreground_decoration=ft.BoxDecoration(border=BEVEL_SUNKEN),
            ),
            ft.Container(
                content=ft.Text(
                    "🙂" if not game.over else "😎" if game.won else "😵", size=35
                ),
                # 😎 😵😢
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.GREY_400,
                on_tap_down=lambda e: set_new_game_tapped(True),
                on_click=lambda e: (
                    set_game(Game()),
                    set_new_game_tapped(False),
                    ticker_task.cancel()
                    if ticker_task and not ticker_task.done()
                    else None,
                ),
                width=50,
                height=50,
                foreground_decoration=ft.BoxDecoration(
                    border=BEVEL_RAISED if not new_game_tapped else None
                ),
            ),
            ft.Container(
                height=50,
                width=90,
                alignment=ft.Alignment.CENTER,
                content=ft.Text(
                    f"{game.seconds:03d}",
                    size=25,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.RED,
                ),
                foreground_decoration=ft.BoxDecoration(border=BEVEL_SUNKEN),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        expand=True,
    )

    return ft.Container(
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            controls=[
                ft.Container(
                    content=top_menu,
                    foreground_decoration=ft.BoxDecoration(border=BEVEL_SUNKEN),
                    padding=10,
                ),
                ft.Container(
                    content=board,
                    foreground_decoration=ft.BoxDecoration(border=BEVEL_SUNKEN),
                    padding=5,
                    height=SQUARE_SIZE * game.rows + 10,
                    width=SQUARE_SIZE * game.cols + 10,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            spacing=10,
        ),
        bgcolor=ft.Colors.GREY_400,
        foreground_decoration=ft.BoxDecoration(border=BEVEL_RAISED),
        width=SQUARE_SIZE * (game.cols + 1),
        height=SQUARE_SIZE * (game.rows + 1) + 100,
        padding=10,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
