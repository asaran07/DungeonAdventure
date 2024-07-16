from typing import List, Optional

from src.dungeon.room import Room
from src.enums.room_types import RoomType
from src.items.item import Item


class Dungeon:
    def __init__(self, width=5, height=5):
        """
        Creates an empty dungeon with a 2D list of rooms.

        :param width: The width of the dungeon. Default is 5.
        :param height: The height of the dungeon. Default is 5.
        """
        self.height = height
        self.width = width
        self.dungeon: List[List[Room]] = self._generate_dungeon()

    def _generate_dungeon(self) -> List[List[Room]]:
        return [
            [Room(RoomType.NORMAL) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def get_room(self, x: int, y: int) -> Optional[Room]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.dungeon[y][x]
        return None

    def set_entrance(self, x: int, y: int) -> None:
        room = self.get_room(x, y)
        if room:
            room.is_entrance = True

    def set_exit(self, x: int, y: int) -> None:
        room = self.get_room(x, y)
        if room:
            room.is_exit = True

    def add_pit(self, x: int, y: int) -> None:
        room = self.get_room(x, y)
        if room:
            room.has_pit = True

    def add_item_to_room(self, x: int, y: int, item: Item) -> None:
        room = self.get_room(x, y)
        if room:
            room.add_item(item)

    def get_size(self) -> tuple[int, int]:
        """Returns a tuple of the dungeon's size. E.g. (height, width)"""
        return self.width, self.height
