from .game_logic import GameLogicError


class PlayerError(GameLogicError):
    """Base class for player-related errors"""
    pass


class InventoryError(PlayerError):
    """Base class for inventory-related errors"""
    pass


class InventoryFullError(InventoryError):
    """Raised when trying to add an item to a full inventory"""
    pass


class ItemNotFoundError(InventoryError):
    """Raised when trying to use or remove a non-existent item"""
    pass


class InvalidPlayerActionError(PlayerError):
    """Raised when a player attempts an invalid action"""
    pass
