from typing import Dict, List, Optional

from src.enums.room_types import Direction, RoomType
from src.items.item import Item


class Room:
    def __init__(self, name: str) -> None:
        self.room_type = RoomType.NORMAL
        self.name = name
        self.items: List[Item] = []
        self.connections: Dict[Direction, Optional["Room"]] = {
            d: None for d in Direction
        }  # Creating a map in Python is goated

    def connect(self, direction: Direction, other_room: "Room") -> bool:
        if (
            self.connections[direction] is None
            and other_room.connections[Room.opposite(direction)] is None
        ):
            self.connections[direction] = other_room
            other_room.connections[Room.opposite(direction)] = self
            return True
        return False

    def add_item(self, item: Item) -> None:
        """Adds an item to the room."""
        self.items.append(item)

    def set_room_type(self, room_type: RoomType) -> None:
        self.room_type = room_type

    @staticmethod
    def opposite(direction: Direction) -> Direction:
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }[direction]
