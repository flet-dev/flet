from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board
    from board_list import BoardList
    from item import Item
    from user import User


class DataStore:
    def add_board(self, model) -> None:
        raise NotImplementedError

    def get_board(self, id) -> "Board":
        raise NotImplementedError

    def get_boards(self) -> list["Board"]:
        raise NotImplementedError

    def update_board(self, model, update):
        raise NotImplementedError

    def remove_board(self, board) -> None:
        raise NotImplementedError

    def add_user(self, model) -> None:
        raise NotImplementedError

    def get_users(self) -> list["User"]:
        raise NotImplementedError

    def get_user(self, id) -> "User":
        raise NotImplementedError

    def remove_user(self, id) -> None:
        raise NotImplementedError

    def add_list(self, board, model) -> None:
        raise NotImplementedError

    def get_lists(self) -> list["BoardList"]:
        raise NotImplementedError

    def get_list(self, id) -> "BoardList":
        raise NotImplementedError

    def get_lists_by_board(self, board) -> list["BoardList"]:
        raise NotImplementedError

    def remove_list(self, board, id) -> None:
        raise NotImplementedError

    def add_item(self, board_list, model) -> None:
        raise NotImplementedError

    def get_items(self, board_list) -> list["Item"]:
        raise NotImplementedError

    def get_item(self, id) -> "Item":
        raise NotImplementedError

    def get_items_by_board(self, board) -> list["Item"]:
        raise NotImplementedError

    def remove_item(self, board_list, id) -> None:
        raise NotImplementedError
