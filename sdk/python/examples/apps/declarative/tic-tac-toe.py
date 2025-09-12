import flet as ft


@ft.component
def Square(value: str, on_click):
    return ft.Button(
        ft.Icon(ft.Icons.CIRCLE_OUTLINED)
        if value == "O"
        else ft.Icon(ft.Icons.CLOSE)
        if value == "X"
        else "",
        width=50,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5), padding=0),
        on_click=on_click,
    )


@ft.component
def Board(x_is_next: bool, squares: list[str], on_play):
    def handle_click(i: int):
        if squares[i] or calculate_winner(squares):
            return
        next_squares = squares[:]
        next_squares[i] = "X" if x_is_next else "O"
        on_play(next_squares)

    winner = calculate_winner(squares)

    return ft.Column(
        [
            ft.Text(
                f"Winner: {winner}"
                if winner
                else f"Next player: {'X' if x_is_next else 'O'}"
            ),
            ft.Row(
                [Square(squares[i], lambda e, i=i: handle_click(i)) for i in range(3)]
            ),
            ft.Row(
                [
                    Square(squares[i], lambda e, i=i: handle_click(i))
                    for i in range(3, 6)
                ]
            ),
            ft.Row(
                [
                    Square(squares[i], lambda e, i=i: handle_click(i))
                    for i in range(6, 9)
                ]
            ),
        ]
    )


@ft.component
def Game():
    history, set_history = ft.use_state([[""] * 9])
    current_move, set_current_move = ft.use_state(0)
    x_is_next = current_move % 2 == 0

    def handle_play(next_squares: list[str]):
        next_history = history[: current_move + 1] + [next_squares]
        set_history(next_history)
        set_current_move(len(next_history) - 1)

    def jump_to(move: int):
        set_current_move(move)

    moves: list[ft.Control] = [
        ft.TextButton(
            ft.Text(f"Go to move #{move}" if move > 0 else "Go to game start"),
            on_click=lambda e, m=move: jump_to(m),
        )
        for move, _ in enumerate(history)
    ]

    return ft.Row(
        [
            Board(x_is_next, history[current_move], handle_play),
            ft.Column(moves),
        ],
        vertical_alignment=ft.CrossAxisAlignment.START,
    )


def calculate_winner(squares: list[str]):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for line in lines:
        a, b, c = line
        if squares[a] and squares[a] == squares[b] == squares[c]:
            return squares[a]
    return None


ft.run(lambda page: page.render(Game))
