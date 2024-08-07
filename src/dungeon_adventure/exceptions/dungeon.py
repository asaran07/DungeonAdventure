from .game_logic import GameLogicError


class DungeonError(GameLogicError):
    """Base class for dungeon-related errors"""


class RoomNotFoundError(DungeonError):
    """Raised when trying to access a non-existent room"""


class InvalidMovementError(DungeonError):
    """Raised when attempting an invalid movement"""
