from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from board_list import BoardList
    from item import Item
    from user import User

from data_store import DataStore


class InMemoryStore(DataStore):
    def __init__(self):
        self.boards: dict[int, Board] = {}
        self.users: dict[str, User] = {}
        self.board_lists: dict[int, list[BoardList]] = {}
        self.items: dict[int, list[Item]] = {}

    def add_board(self, board: "Board"):
        self.boards[board.board_id] = board

    def get_board(self, id: int):
        return self.boards[id]

    def update_board(self, board: "Board", update: dict):
        for k in update:
            setattr(board, k, update[k])

    def get_boards(self):
        return [self.boards[b] for b in self.boards]

    def remove_board(self, board: "Board"):
        del self.boards[board.board_id]
        self.board_lists[board.board_id] = []

    def add_list(self, board: int, list: "BoardList"):
        if board in self.board_lists:
            self.board_lists[board].append(list)
        else:
            self.board_lists[board] = [list]

    def get_lists_by_board(self, board: int):
        return self.board_lists.get(board, [])

    def remove_list(self, board: int, id: int):
        self.board_lists[board] = [
            l for l in self.board_lists[board] if not l.board_list_id == id
        ]

    def add_user(self, user: "User"):
        self.users[user.name] = user

    def get_users(self):
        return [self.users[u] for u in self.users]

    def add_item(self, board_list: int, item: "Item"):
        if board_list in self.items:
            self.items[board_list].append(item)
        else:
            self.items[board_list] = [item]

    def get_items(self, board_list: int):
        return self.items.get(board_list, [])

    def remove_item(self, board_list: int, id: int):
        self.items[board_list] = [
            i for i in self.items[board_list] if not i.item_id == id
        ]
