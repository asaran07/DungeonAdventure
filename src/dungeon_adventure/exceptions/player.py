from .game_logic import GameLogicError


class PlayerError(GameLogicError):
    """Base class for player-related errors"""


class InventoryError(PlayerError):
    """Base class for inventory-related errors"""


class InventoryFullError(InventoryError):
    """Raised when trying to add an item to a full inventory"""


class ItemNotFoundError(InventoryError):
    """Raised when trying to use or remove a non-existent item"""


class InvalidPlayerActionError(PlayerError):
    """Raised when a player attempts an invalid action"""


class PlayerNotInRoomError(PlayerError):
    """Raised when a player action requires being in a room, but the player is not in one"""


class ItemNotInRoomError(PlayerError):
    """Raised when trying to interact with an item that's not in the current room"""


class ItemNotInInventoryError(PlayerError):
    """Raised when trying to use or drop an item that's not in the player's inventory"""


class InvalidDirectionError(PlayerError):
    """Raised when trying to move in an invalid direction"""


class InvalidPlayerAttributeError(PlayerError):
    """Raised when an attribute set to player is invalid"""
    pass
