from enum import Enum, auto


class GameState(Enum):
    TITLE_SCREEN = auto()
    LOAD = auto()
    EXPLORING = auto()
    COMBAT = auto()
    INVENTORY = auto()
    GAME_OVER = auto()
    PLAYER_CREATION = auto()
    IN_COMBAT = auto()
