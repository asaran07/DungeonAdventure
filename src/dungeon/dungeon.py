from typing import Dict

from src.dungeon.room import Room
from src.enums.room_types import Direction


def connect_rooms(room1: Room, direction: Direction, room2: Room) -> bool:
    return room1.connect(direction, room2)


class Dungeon:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def add_room(self, name: str) -> Room:
        room = Room(name)
        self.rooms[name] = room
        return room

    def get_entrance_room(self):
        pass
