from typing import Dict, Optional

from src.characters import Player
from src.characters.monster import Monster
from src.dungeon import Dungeon
from src.enums import Direction
from src.enums.game_state import GameState
from src.enums.item_types import WeaponType
from src.exceptions import GameStateError, PlayerError, DungeonError, InvalidInputError
from src.items.weapon import Weapon


class GameModelError(Exception):
    """Base exception for GameModel-related errors"""


class PlayerNotInitializedError(GameModelError):
    """Raised when trying to access an uninitialized player"""


class DungeonNotInitializedError(GameModelError):
    """Raised when trying to access an uninitialized dungeon"""


class GameModel:
    """
    Represents the complete state of the game world.
    The GameModel is the 'single source of truth' for the current game state.
    """

    def __init__(self):
        self._dungeon: Optional[Dungeon] = None
        self._player: Optional[Player] = None
        self._game_state = GameState.TITLE_SCREEN
        self.game_over = False
        self._initialize_game()

    def _initialize_game(self):
        try:
            self._dungeon = Dungeon()
            self._player = self._create_default_player()
            entrance_room = self._dungeon.get_entrance_room()
            if entrance_room is not None:
                self._player.current_room = entrance_room
            else:
                raise DungeonError("Entrance room not set in the dungeon")
        except Exception as e:
            raise GameModelError(f"Failed to initialize game: {str(e)}")

    @property
    def dungeon(self) -> Dungeon:
        if self._dungeon is None:
            raise DungeonNotInitializedError("Dungeon has not been initialized")
        return self._dungeon

    @property
    def player(self) -> Player:
        if self._player is None:
            raise PlayerNotInitializedError("Player has not been initialized")
        return self._player

    @property
    def game_state(self) -> GameState:
        return self._game_state

    @game_state.setter
    def game_state(self, game_state: GameState) -> None:
        if not isinstance(game_state, GameState):
            raise GameStateError(f"Invalid game state: {game_state}")
        self._game_state = game_state

    def make_rooms(self):
        try:
            self.dungeon.add_room("Room 1")
            self.dungeon.add_and_connect_room("Room 2", "Room 1", Direction.NORTH)
            test_monster = Monster()
            room2 = self.dungeon.get_room("Room 2")
            if room2 is not None:
                room2.add_monster(test_monster)
            else:
                raise DungeonError("Room 2 not found")

            room1 = self.dungeon.get_room("Room 1")
            if room1 is not None:
                room1.add_item(Weapon("Basic Sword", "A basic sword", 1, WeaponType.SWORD, 2, 10))
            else:
                raise DungeonError("Room 1 not found")

            self.dungeon.add_and_connect_room("Room 3", "Room 2", Direction.EAST)
            self.dungeon.set_entrance_room("Room 1")
            self.dungeon.add_and_connect_room("Room 4", "Room 3", Direction.EAST)
            self.dungeon.add_and_connect_room("Room 5", "Room 3", Direction.NORTH)
        except DungeonError as e:
            raise GameModelError(f"Failed to create rooms: {str(e)}")

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self, boolean: bool) -> None:
        if not isinstance(boolean, bool):
            raise InvalidInputError("Game over status must be a boolean")
        if boolean:
            self._game_state = GameState.GAME_OVER
        self.game_over = boolean

    def _create_default_player(self) -> Player:
        return Player(
            name="Player1",
            hit_points=100,
        )

    def create_player(self, player_data: Dict):
        """
        Creates or updates the player instance based on the provided player data.
        :param player_data: A dictionary containing player attributes
        """
        if not isinstance(player_data, dict):
            raise InvalidInputError("Player data must be a dictionary")
        try:
            self._player = Player(
                name=player_data.get("name", "Player1"),
                hit_points=player_data.get("hit_points", 100),
            )
            if self._dungeon is not None:
                entrance_room = self._dungeon.get_entrance_room()
                if entrance_room is not None:
                    self._player.current_room = entrance_room
                else:
                    raise DungeonError("Entrance room not set in the dungeon")
            else:
                raise DungeonNotInitializedError("Dungeon has not been initialized")
        except Exception as e:
            raise PlayerError(f"Failed to create player: {str(e)}")

    def update_player(self, player_data: Dict):
        """
        Updates the player instance based on the provided player data.
        :param player_data: A dictionary containing player attributes
        """
        if not isinstance(player_data, dict):
            raise InvalidInputError("Player data must be a dictionary")
        if self._player is None:
            raise PlayerNotInitializedError("Player has not been initialized")
        for key, value in player_data.items():
            if hasattr(self._player, key):
                setattr(self._player, key, value)
            else:
                print(f"Warning: Attribute '{key}' not found in Player class.")
