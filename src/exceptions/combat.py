from src.exceptions import GameLogicError


class CombatError(GameLogicError):
    """Base exception for combat-related errors"""


class InvalidCombatStateError(CombatError):
    """Raised when an invalid combat state is encountered"""


class CharacterNotInCombatError(CombatError):
    """Raised when trying to perform an action with a character not in combat"""
