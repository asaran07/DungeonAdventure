from src.characters.player import Player
from src.dungeon import Dungeon


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
        self.player = None
        self.current_room = None
        self.game_over = False

    def initialize_game(self):
        self.dungeon = Dungeon()
        self.player = Player("Player1", 100, 0, 0, [])
        self.current_room = self.dungeon.get_entrance_room()
        self.player.current_room = self.current_room

    def is_game_over(self):
        return self.game_over
