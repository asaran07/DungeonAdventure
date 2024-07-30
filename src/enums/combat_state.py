from enum import Enum, auto


class CombatState(Enum):
    WAITING = auto()
    PLAYER_TURN = auto()
    MONSTER_TURN = auto()
