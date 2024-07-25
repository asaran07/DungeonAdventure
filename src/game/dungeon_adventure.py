from typing import Dict
from src.characters import Player
from src.dungeon import Dungeon, Room
from src.enums import Direction
from src.enums.game_state import GameState
from src.enums.item_types import WeaponType
from src.items.weapon import Weapon


class GameModel:
    """
    Represents the complete state of the game world.
    This class holds all game entities and their current states,
    including the dungeon layout, rooms and their contents,
    the player's status and inventory, and any other game-specific data.
    The GameModel is the 'single source of truth' for the current game state.
    """

    def __init__(self):
        self._dungeon: Dungeon = Dungeon()
        self._player: Player = self._create_default_player()
        self._game_state = GameState.TITLE_SCREEN
        self.game_over = False
        self.current_room = self._dungeon.get_entrance_room()
        self._player.current_room = self.current_room

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
        self._game_state = game_state

    def make_rooms(self):
        self._dungeon.add_room("Room 1")
        self._dungeon.add_and_connect_room("Room 2", "Room 1", Direction.NORTH)
        self._dungeon.get_room("Room 1").add_item(
            Weapon("Basic Sword", "A basic sword", 1, WeaponType.SWORD, 2, 10)
        )
        self._dungeon.set_entrance_room("Room 1")

    def is_game_over(self) -> bool:
        return self.game_over

    def set_game_over(self, boolean: bool) -> None:
        if boolean:
            self._game_state = GameState.GAME_OVER
        self.game_over = boolean

    def _create_default_player(self) -> Player:
        return Player(
            name="Player1",
            hit_points=100,
            total_healing_potions=0,
            total_vision_potions=0,
            pillars_found=[],
        )

    def create_player(self, player_data: Dict):
        """
        Creates or updates the player instance based on the provided player data.
        :param player_data: A dictionary containing player attributes
        """
        self._player = Player(
            name=player_data.get("name", self._player.get_name),
            hit_points=player_data.get("hit_points", self._player.get_hp),
            total_healing_potions=player_data.get(
                "total_healing_potions", self._player._total_healing_potions
            ),
            total_vision_potions=player_data.get(
                "total_vision_potions", self._player._total_vision_potions
            ),
            pillars_found=player_data.get("pillars_found", self._player._pillars_found),
        )
        self._player.current_room = self.current_room

    def update_player(self, player_data: Dict):
        """
        Updates the player instance based on the provided player data.
        :param player_data: A dictionary containing player attributes
        """
        for key, value in player_data.items():
            if hasattr(self._player, key):
                setattr(self._player, key, value)
            else:
                print(f"Warning: Attribute '{key}' not found in Player class.")
