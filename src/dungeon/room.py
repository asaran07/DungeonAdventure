from typing import List

from src.enums.room_types import RoomType
from src.items.item import Item


class Room:
    def __init__(self, room_type: RoomType) -> None:
        self.room_type = room_type
        self.items: List[Item] = []
        self.has_pit = False
        self.is_entrance = False
        self.is_exit = False

    def add_item(self, item: Item) -> None:
        """Adds an item to the room."""
        self.items.append(item)

    def set_room_type(self, room_type: RoomType) -> None:
        self.room_type = room_type
