from dataclasses import dataclass, field
from typing import Optional, Literal

import flet as ft

ScreenType = Literal["boards", "board", "members", "settings"]


@ft.observable
@dataclass
class Card:
    text: str
    board_list: "BoardList"

    def __post_init__(self):
        self.card_id = id(self)

    def move_to_list(self, dst: "BoardList", *, index: Optional[int] = None) -> None:
        if self.board_list == dst and index is None:
            return
        self.board_list.cards.remove(self)
        self.board_list = dst
        if index is None:
            dst.cards.append(self)
        else:
            dst.cards.insert(index, self)


@ft.observable
@dataclass
class BoardList:
    title: str
    color: str
    board: "Board"
    cards: list[Card] = field(default_factory=list)

    def __post_init__(self):
        self.board_list_id = id(self)

    def add_card(self, text: str) -> None:
        text = text.strip()
        if not text:
            return
        self.cards.append(Card(text=text, board_list=self))

    def remove_card(self, card: Card) -> None:
        self.cards.remove(card)

    def move_card_at(self, card: Card, to_card: Card) -> None:
        if card == to_card:
            return
        dst_list = to_card.board_list
        to_index = dst_list.cards.index(to_card)
        card.move_to_list(dst_list, index=to_index)

    def move_card_into(self, card: Card) -> None:
        card.move_to_list(self)


@ft.observable
@dataclass
class Board:
    name: str
    lists: list[BoardList] = field(default_factory=list)

    def __post_init__(self):
        self.board_id = id(self)

    def add_list(self, title: str, color: str) -> None:
        title = title.strip()
        if not title:
            return
        self.lists.append(BoardList(title=title, color=color, board=self))

    def remove_list(self, board_list: BoardList) -> None:
        self.lists.remove(board_list)

    def move_list(self, src: BoardList, dst: BoardList) -> None:
        src_index = self.lists.index(src)
        dst_index = self.lists.index(dst)
        if src_index != dst_index:
            self.lists.insert(dst_index, self.lists.pop(src_index))


@ft.observable
@dataclass
class TrolliState:
    route: str
    active_screen: ScreenType = "boards"
    current_board_id: Optional[int] = None
    user: Optional[str] = None
    nav_visible: bool = True
    boards: list[Board] = field(default_factory=list)

    def route_change(self, e: ft.RouteChangeEvent):
        self.route = e.route

    def get_board_by_id(self, board_id: int) -> Optional[Board]:
        for b in self.boards:
            if b.board_id == board_id:
                return b
        return None

    def create_board(self, name: str) -> Board:
        name = name.strip()
        if not name:
            name = "Untitled board"
        board = Board(name=name)
        self.boards.append(board)
        return board

    def delete_board(self, board: Board) -> None:
        self.boards.remove(board)
