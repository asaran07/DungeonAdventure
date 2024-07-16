from enum import Enum, auto


class RoomType(Enum):
    """Choose from the following room types:
    NORMAL, ENTRANCE, EXIT, PIT
    """  # We can probably configure these later

    NORMAL = auto()
    ENTRANCE = auto()
    EXIT = auto()
    PIT = auto()
