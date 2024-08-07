from enum import Enum, auto
from typing import Tuple


class RoomType(Enum):
    """Choose from the following room types:
    NORMAL, ENTRANCE, EXIT, PIT
    """  # We can probably configure these later

    NORMAL = auto()
    ENTRANCE = auto()
    EXIT = auto()
    PIT = auto()


class Direction(Enum):
    # TODO: Add an opposite direction method for cleanliness
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def get_coordinate_change(self) -> Tuple[int, int]:
        changes = {
            Direction.NORTH: (0, -1),
            Direction.SOUTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.WEST: (-1, 0),
        }
        return changes[self]

    @classmethod
    def from_string(cls, direction_str: str):
        try:
            return cls[direction_str.upper()]
        except KeyError:
            raise ValueError(f"'{direction_str}' is not a valid direction.")
