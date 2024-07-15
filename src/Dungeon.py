from typing import List, Optional

from src.Item import Item
from src.Room import Room


class Dungeon:
    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.dungeon: List[List[Room]] = self._generate_dungeon()

    def _generate_dungeon(self) -> List[List[Room]]:
        return [[Room() for _ in range(self.width)] for _ in range(self.height)]

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
