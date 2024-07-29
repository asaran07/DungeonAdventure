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
