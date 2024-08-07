from .base import DungeonAdventureError


class InputError(DungeonAdventureError):
    """Base class for input-related errors"""


class InvalidInputError(InputError):
    """Raised when the user provides invalid input"""
