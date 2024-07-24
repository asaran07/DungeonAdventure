from typing import Dict, List, Optional

from src.enums import RoomType, Direction
from src.items.item import Item


class Room:
    def __init__(self, name: str) -> None:
        self.room_type = RoomType.NORMAL
        self.name = name
        self.is_visible: bool = False  # For Fog of War if we decide to add that
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

    def get_open_gates(self):
        return [
            (direction, room)
            for direction, room in self.connections.items()
            if room is not None
        ]

    def add_item(self, item: Item) -> None:
        """Adds an item to the room."""
        self.items.append(item)

    def remove_item(self, item: Item) -> None:
        self.items.remove(item)

    def set_room_type(self, room_type: RoomType) -> None:
        self.room_type = room_type

    def get_description(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        connections = ", ".join(
            [
                f"{d.name}: {r.name if r else 'None'}"
                for d, r in self.connections.items()
            ]
        )
        items = (
            ", ".join([item.name for item in self.items])
            if self.items
            else "None"
        )

        return (
            f"Room: {self.name}\n"
            f"Type: {self.room_type.name}\n"
            f"Visible: {'Yes' if self.is_visible else 'No'}\n"
            f"Connections: {connections}\n"
            f"Items: {items}"
        )

    @staticmethod
    def opposite(direction: Direction) -> Direction:
        return {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }[direction]
