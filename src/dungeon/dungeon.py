from typing import Dict, Optional

from src.dungeon.room import Room
from src.enums.room_types import Direction


def connect_rooms(room1: Room, direction: Direction, room2: Room) -> bool:
    return room1.connect(direction, room2)


class Dungeon:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}
        self.entrance_room: Optional[Room] = None

    def get_entrance_room(self) -> Optional[Room]:
        return self.entrance_room

    def add_room(self, name: str) -> Room:
        """Creates and adds a room to the dungeon, then returns the newly created room"""
        room = Room(name)
        self.rooms[name] = room
        return room

    def remove_room(self, name: str) -> Optional[Room]:
        if name not in self.rooms:
            print(f"Room '{name}' does not exist in the dungeon.")
            return None

        room_to_remove = self.rooms[name]

        # Check if the room is connected to any other rooms
        for direction in Direction:
            connected_room = room_to_remove.connections[direction]
            if connected_room:
                # Disconnect the rooms
                opposite_direction = Room.opposite(direction)
                connected_room.connections[opposite_direction] = None
                room_to_remove.connections[direction] = None

        # Remove the room from the dungeon
        removed_room = self.rooms.pop(name)
        print(f"Room '{name}' has been removed from the dungeon.")

        return removed_room
