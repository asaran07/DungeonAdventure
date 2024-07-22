from enum import Enum, auto


class GameState(Enum):
    TITLE_SCREEN = auto()
    EXPLORING = auto()
    COMBAT = auto()
    INVENTORY = auto()
    GAME_OVER = auto()
