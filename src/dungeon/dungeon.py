from typing import Dict, List, Optional

from src.dungeon.room import Room
from src.enums.room_types import Direction, RoomType
from src.items.item import Item


class Dungeon:
    def __init__(self):
        self.rooms: Dict[str, Room] = {}

    def add_room(self, name: str) -> Room:
        room = Room(name)
        self.rooms[name] = room
        return room

    def connect_rooms(self, room1: Room, direction: Direction, room2: Room) -> bool:
        return room1.connect(direction, room2)
