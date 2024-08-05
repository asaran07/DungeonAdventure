from abc import ABC, abstractmethod
from typing import Dict

from src.dungeon import Room
from src.game.dungeon_adventure import GameModel
from src.items.inventory import Inventory


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

    @abstractmethod
    def display_current_status(self, game_model: GameModel):
        pass

    @abstractmethod
    def display_room_entrance(self, room: Room):
        pass

    @abstractmethod
    def display_room_contents(self, room: Room):
        pass

    @abstractmethod
    def display_combat_start(self):
        pass

    @abstractmethod
    def display_empty_room(self):
        pass

    @abstractmethod
    def display_inventory(self, inventory: "Inventory"):
        pass

    @abstractmethod
    def display_map(self, current_room: Room):
        pass

    @abstractmethod
    def display_pit_damage(self, damage: int):
        pass

    @abstractmethod
    def display_game_over(self):
        pass

    @abstractmethod
    def display_combat_status(self, player, monsters):
        pass

    @abstractmethod
    def get_combat_action(self):
        pass

    @abstractmethod
    def get_combat_target(self, monsters):
        pass

    @abstractmethod
    def display_xp_gained(self, xp_amount: int):
        pass
