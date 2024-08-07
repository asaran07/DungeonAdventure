from typing import Final


class Resources:
    class Map:
        CURRENT_ROOM_MARKER: Final = "X"
        EXPLORED_ROOM_MARKER: Final = "O"
        UNEXPLORED_ROOM_MARKER: Final = " "
        ROOM_FORMAT: Final = "[{}]"
        EMPTY_SPACE: Final = "   "

    class Actions:
        MOVE = "move"
        MAP = "map"
        INVENTORY = "inventory"
        INVENTORY_SHORT = "inv"
        TAKE = "take"
        DROP = "drop"
        EQUIP = "equip"
        USE = "use"

    class Messages:
        EQUIP_SUCCESS = "You equipped {}."
        USE_SUCCESS = "You used {}."
        USE_FAILURE = "You couldn't use {}."
        PICKUP_SUCCESS = "You picked up {}."
        DROP_SUCCESS = "You dropped {}."

    class GameValues:
        PIT_DAMAGE = 50

    class Errors:
        ITEM_NOT_IN_ROOM = "{} wasn't found in this room."
        NOT_A_WEAPON = "{} is not a weapon."
        PLAYER_NOT_IN_ROOM = "Player is not in a room"
        ITEM_NOT_IN_INVENTORY = "You don't have an item named {}"
        INVALID_DIRECTION = "You can't move {} from here"
