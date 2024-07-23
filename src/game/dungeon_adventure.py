from typing import Dict, Optional
from src.characters.player import Player
from src.dungeon import Dungeon
from src.enums.game_state import GameState


class GameModel:
    """
    Represents the complete state of the game world.
    This class holds all game entities and their current states,
    including the dungeon layout, rooms and their contents,
    the player's status and inventory, and any other game-specific data.
    The GameModel is the 'single source of truth' for the current game state.
    """

    def __init__(self):
        # NOTE: Not sure if the Dungeon should be passed from the main class or not
        self.dungeon: Dungeon = Dungeon()
        self.player: Optional[Player] = None
        self.current_room = None
        self.game_over = False
        self.game_state = GameState.TITLE_SCREEN

    def initialize_game(self):
        self.player = Player("Player1", 100, 0, 0, [])
        self.player.current_room = self.current_room

    def is_game_over(self):
        return self.game_over

    def get_player(self) -> Optional[Player]:
        return self.player

    def set_state(self, game_state: GameState) -> None:
        self.game_state = game_state

    def get_state(self) -> GameState:
        return self.game_state

    def set_game_over(self, boolean: bool) -> None:
        if boolean:
            self.game_state = GameState.GAME_OVER

    def create_player(self, player_data: dict):
        """
        Creates or updates the player instance based on the provided player data.

        :param player_data: A dictionary containing player attributes
        """
        if self.player is None:
            # Create a new player instance if it doesn't exist
            self.player = Player(
                name=player_data.get("name", "Unnamed Hero"),
                hit_points=player_data.get("hit_points", 100),
                total_healing_potions=player_data.get("total_healing_potions", 0),
                total_vision_potions=player_data.get("total_vision_potions", 0),
                pillars_found=player_data.get("pillars_found", []),
            )
        else:
            # Update existing player instance
            for key, value in player_data.items():
                if hasattr(self.player, key):
                    setattr(self.player, key, value)
                else:
                    print(f"Warning: Attribute '{key}' not found in Player class.")

        # Set the player's starting room
        if self.current_room is None:
            self.current_room = self.dungeon.get_entrance_room()
        self.player.current_room = self.current_room
