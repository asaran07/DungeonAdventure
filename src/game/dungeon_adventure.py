from typing import Dict

from src.characters import Player
from src.dungeon import Dungeon
from src.enums.game_state import GameState
from src.exceptions import GameStateError, InvalidInputError


class GameModelError(Exception):
    """Base exception for GameModel-related errors"""


class GameModel:
    """
    Represents the complete state of the game world.
    The GameModel is the 'single source of truth' for the current game state.
    """

    def __init__(self, player: Player, dungeon: Dungeon):
        if not isinstance(player, Player):
            raise GameModelError("Invalid player instance provided")
        if not isinstance(dungeon, Dungeon):
            raise GameModelError("Invalid dungeon instance provided")

        self._player: Player = player
        self._dungeon: Dungeon = dungeon
        self._game_state = GameState.TITLE_SCREEN
        self.game_over = False

        # Ensure the player is in the entrance room
        entrance_room = self._dungeon.entrance_room
        if entrance_room is not None:
            self._player.current_room = entrance_room
        else:
            raise GameModelError("Dungeon has no entrance room set")

    @property
    def dungeon(self) -> Dungeon:
        return self._dungeon

    @property
    def player(self) -> Player:
        return self._player

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @game_state.setter
    def game_state(self, game_state: GameState) -> None:
        if not isinstance(game_state, GameState):
            raise GameStateError(f"Invalid game state: {game_state}")
        self._game_state = game_state

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self, boolean: bool) -> None:
        if boolean:
            self._game_state = GameState.GAME_OVER
        self.game_over = boolean

    def update_player(self, player_data: Dict):
        """
        Updates the player instance based on the provided player data.
        :param player_data: A dictionary containing player attributes
        """
        if not isinstance(player_data, dict):
            raise InvalidInputError("Player data must be a dictionary")
        for key, value in player_data.items():
            if hasattr(self._player, key):
                setattr(self._player, key, value)
            else:
                print(f"Warning: Attribute '{key}' not found in Player class.")
