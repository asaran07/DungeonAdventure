from .base import DungeonAdventureError


class GameLogicError(DungeonAdventureError):
    """Base class for errors related to game logic"""
    pass


class GameStateError(GameLogicError):
    """Raised for invalid game state transitions"""
    pass
