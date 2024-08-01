from abc import ABC, abstractmethod
from typing import Dict

from src.game.dungeon_adventure import GameModel


class View(ABC):
    """
    Core interface for game display and user interaction. This abstract class lets all view implementations show and
    work with game states, collect user inputs, and display messages regardless of the actual display method used (
    console, GUI, etc.)
    """

    @abstractmethod
    def display_available_actions(self, game_model: GameModel):
        pass

    @abstractmethod
    def get_user_input(self, prompt: str) -> str:
        pass

    @abstractmethod
    def display_title_screen(self):
        pass

    @abstractmethod
    def get_player_creation_input(self) -> Dict:
        pass

    @abstractmethod
    def display_message(self, message):
        pass

    @abstractmethod
    def display_player_status(self, game_model: GameModel):
        pass

    def display_combat_status(self, player, monsters):
        pass

    def get_combat_action(self):
        pass

    def get_combat_target(self, monsters):
        pass

    def display_xp_gained(self, xp_amount: int):
        pass
