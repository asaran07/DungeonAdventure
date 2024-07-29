from .game_logic import GameLogicError


class DungeonError(GameLogicError):
    """Base class for dungeon-related errors"""
    pass


class RoomError(DungeonError):
    """Base class for room-related errors"""
    pass


class RoomNotFoundError(RoomError):
    """Raised when trying to access a non-existent room"""
    pass


class InvalidMovementError(DungeonError):
    """Raised when attempting an invalid movement"""
    pass
