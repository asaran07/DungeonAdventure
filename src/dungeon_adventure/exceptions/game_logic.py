from .base import DungeonAdventureError


class GameLogicError(DungeonAdventureError):
    """Base class for errors related to game logic"""


class GameStateError(GameLogicError):
    """Raised for invalid game state transitions"""
