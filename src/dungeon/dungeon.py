from typing import Dict, TYPE_CHECKING

from src.dungeon.room import Room
from src.enums.room_types import Direction


class DungeonError(Exception):
    """Custom exception for Dungeon-related errors"""

    pass


if TYPE_CHECKING:
    from .room import Room


class Dungeon:
    def __init__(self):
        self.rooms: Dict[str, "Room"] = {}

    def get_rooms(self):
        return list(self.rooms.values())

    def room_exists(self, room_name: str) -> bool:
        return room_name in self.rooms

    def get_room(self, room_name: str) -> Room:
        if not self.room_exists(room_name):
            raise DungeonError(f"Room '{room_name}' does not exist in the dungeon.")
        return self.rooms[room_name]

    def add_room(self, name: str) -> Room:
        """Creates and adds a room to the dungeon, then returns the newly created room"""
        if self.room_exists(name):
            raise DungeonError(f"Room '{name}' already exists in the dungeon.")
        room = Room(name)
        self.rooms[name] = room
        return room

    def remove_room(self, name: str) -> Room:
        if not self.room_exists(name):
            raise DungeonError(f"Room '{name}' does not exist in the dungeon.")
        room_to_remove = self.rooms[name]
        self.disconnect_rooms(room_to_remove)
        removed_room = self.rooms.pop(name)
        return removed_room

    def disconnect_rooms(self, room_to_disconnect: Room) -> None:
        """Disconnect the provided room from any other rooms it was connected to"""
        for direction in Direction:
            connected_room = room_to_disconnect.connections[direction]
            if connected_room:
                opposite_direction = Room.opposite(direction)
                connected_room.connections[opposite_direction] = None
                room_to_disconnect.connections[direction] = None

    def connect_rooms(
        self, room1_name: str, direction: Direction, room2_name: str
    ) -> bool:
        """Connect two rooms in the dungeon by their names"""
        room1 = self.get_room(room1_name)
        room2 = self.get_room(room2_name)
        return room1.connect(direction, room2)

    def add_and_connect_room(
        self, new_room_name: str, existing_room_name: str, direction: Direction
    ) -> Room:
        """Add a new room to the dungeon and connect it to an existing room"""
        existing_room = self.get_room(existing_room_name)
        new_room = self.add_room(new_room_name)

        if existing_room.connect(direction, new_room):
            return new_room
        else:
            self.remove_room(new_room_name)
            raise DungeonError(
                f"Failed to connect room '{new_room_name}' to '{existing_room_name}'. Connection might already exist."
            )
