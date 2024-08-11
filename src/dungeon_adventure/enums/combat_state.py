from enum import Enum, auto


class CombatState(Enum):
    SUMMARY = auto()
    WAITING = auto()
    PLAYER_TURN = auto()
    MONSTER_TURN = auto()
    READY = auto()
