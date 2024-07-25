from enum import Enum, auto


class RoomType(Enum):
    """Choose from the following room types:
    NORMAL, ENTRANCE, EXIT, PIT
    """  # We can probably configure these later

    NORMAL = auto()
    ENTRANCE = auto()
    EXIT = auto()
    PIT = auto()


class Direction(Enum):
    # TODO: Add an opposite direction method for cleaniness
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    @classmethod
    def from_string(cls, direction_str: str):
        try:
            return cls[direction_str.upper()]
        except KeyError:
            raise ValueError(f"'{direction_str}' is not a valid direction.")
