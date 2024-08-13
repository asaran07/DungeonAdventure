import logging

import pygame

from dungeon_adventure.controllers.player_action_controller import PlayerActionController
from dungeon_adventure.game_model import GameModel, GameModelError
from dungeon_adventure.logging_config import setup_logging
from dungeon_adventure.models.player.player import Player
from dungeon_adventure.services.dungeon_generator import DungeonGenerator
from dungeon_adventure.views.console.console_view import ConsoleView
from dungeon_adventure.views.console.map_visualizer import MapVisualizer
from dungeon_adventure.views.pygame.game.game_screen import GameScreen
from dungeon_adventure.views.pygame.game.game_world import GameWorld
from dungeon_adventure.views.pygame.game.main_game_controller import MainGameController
from dungeon_adventure.views.pygame.game.py_game_view import PyGameView
from dungeon_adventure.views.pygame.services.debug_manager import DebugManager
from dungeon_adventure.views.pygame.sprites.composite_player import CompositePlayer
from dungeon_adventure.views.pygame.sprites.py_player import PyPlayer


def setup_game_model():
    try:
        dungeon = DungeonGenerator.generate_default_dungeon()
        player = Player("Player 1")
        if dungeon.get_room("Room 1 - Entrance Hall") is None:
            raise ValueError("Dungeon has no entrance room")
        player.current_room = dungeon.get_room("Room 1 - Entrance Hall")
        game_model = GameModel(player, dungeon)
        return game_model
    except (ValueError, GameModelError) as e:
        print(f"Error setting up the game: {e}")
        return None


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info(f"Starting Dungeon Adventure | Pygame version: {pygame.version.ver}")
    game_model = setup_game_model()
    if game_model:
        py_player = PyPlayer()
        composite_player = CompositePlayer(game_model.player, py_player)
        map_visualizer = MapVisualizer(game_model.dungeon)
        console_view = ConsoleView()
        player_action_controller = PlayerActionController(game_model, map_visualizer, console_view)
        game_world = GameWorld(game_model, composite_player)
        game_screen = GameScreen()
        debug_manager = DebugManager()
        pygame_view = PyGameView(
            game_screen.width, game_screen.height, game_screen.scale_factor
        )
        main_game_controller = MainGameController(
            game_world, game_screen, pygame_view, debug_manager
        )
        main_game_controller.run()

    else:
        print("Failed to set up the game. Exiting.")


if __name__ == "__main__":
    main()
