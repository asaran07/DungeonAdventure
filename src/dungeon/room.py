from typing import Dict, List, Optional, Tuple

from src.characters.monster import Monster
from src.enums import RoomType, Direction
from src.items.item import Item


class Room:
    def __init__(self, name: str, detailed_description: str = "") -> None:
        """
        Initialize a new room.

        :param name: The name of room
        """
        self._room_type = RoomType.NORMAL
        self.name: str = name
        self.is_visible: bool = False
        self.is_explored: bool = False  # This is for fog of war
        self.detailed_description: str = detailed_description
        self.items: List[Item] = []
        self._monsters: List[Monster] = []
        self.connections: Dict[Direction, Optional["Room"]] = {
            d: None for d in Direction
        }  # Creating a map in Python is goated

    @property
    def monsters(self) -> List[Monster]:
        return self._monsters

    @monsters.setter
    def monsters(self, value):
        self._monsters = value

    def add_monster(self, monster: Monster) -> None:
        self.monsters.append(monster)

    @property
    def has_monsters(self) -> bool:
        return len(self.monsters) > 0

    @property
    def has_items(self) -> bool:
        return len(self.items) > 0

    @property
    def room_type(self) -> RoomType:
        return self._room_type

    @room_type.setter
    def room_type(self, room_type: RoomType) -> None:
        self._room_type = room_type

    def remove_monster(self, monster: Monster):
        self.monsters.remove(monster)

    def explore(self):
        self.is_explored = True

    @property
    def detailed_description(self) -> str:
        """
        Get a detailed description of the room.
        """
        return (
            self.detailed_description
            if self.detailed_description
            else "You see nothing special about this room."
        )

    @detailed_description.setter
    def detailed_description(self, desc: str) -> None:
        self._detailed_description = desc

    def connect(self, direction: Direction, other_room: "Room") -> bool:
        """
        Connect this room to another room in the specified direction.

        :param direction: The direction of the connection
        :param other_room: The room to connect to
        :return: True if the connection was made, False otherwise
        """
        if (
            self.connections[direction] is None
            and other_room.connections[Room.opposite(direction)] is None
        ):
            self.connections[direction] = other_room
            other_room.connections[Room.opposite(direction)] = self
            return True
        return False

    def get_open_gates(self) -> List[Tuple[Direction, "Room"]]:
        """
        Get a list of open connections from this room.

        :return: A list of tuples containing the direction and connected room
        """
        return [
            (direction, room)
            for direction, room in self.connections.items()
            if room is not None
        ]

    def add_item(self, item: Item) -> None:
        """
        Add an item to the room.

        :param item: The item to add
        """
        self.items.append(item)

    def remove_item(self, item: Item) -> Item:
        """
        Remove an item from the room.

        :param item: The item to remove
        """
        self.items.remove(item)
        return item

    def print_items(self) -> None:
        """
        Prints out the items in the room in a clean, organized format.
        """
        if not self.items:
            print("This room is empty.")
            return

        print("Items in this room:")
        for index, item in enumerate(self.items, 1):
            print(f"{index}. {item.name} - {item.description}")
            print(f"   Weight: {item.weight}")
            if hasattr(item, 'item_type'):
                print(f"   Type: {item.item_type.name}")
            print()

    def set_room_type(self, room_type: RoomType) -> None:
        """
        Set the type of the room.

        :param room_type: The type to set for the room
        """
        self.room_type = room_type

    def get_desc(self) -> str:
        """
        Get a description of the room.

        :return: A string description of the room
        """
        return str(self)

    def __str__(self) -> str:
        """
        Get a string representation of the room.

        :return: A string representation of the room
        """
        connections = ", ".join(
            f"{d.name}: {r.name if r else 'None'}" for d, r in self.connections.items()
        )
        items = ", ".join(item.name for item in self.items) if self.items else "None"

        return (
            # f"Room: {self.name}\n"
            # f"Type: {self.room_type.name}\n"
            # f"Visible: {'Yes' if self.is_visible else 'No'}\n"
            f"{self.get_desc()}\n"
            f"Connections: {connections}\n"
            f"Items: {items}"
        )

    @staticmethod
    def opposite(direction: Direction) -> Direction:
        """
        Get the opposite direction.

        :param direction: The direction to find the opposite of
        :return: The opposite direction
        """
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[direction]
