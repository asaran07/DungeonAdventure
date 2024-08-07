from dungeon_adventure.controllers.game_controller import GameController
from dungeon_adventure.controllers.player_action_controller import PlayerActionController
from dungeon_adventure.game_model import GameModelError
from dungeon_adventure.models.player import Player
from dungeon_adventure.services.dungeon_generator import DungeonGenerator
from dungeon_adventure.views.console.console_view import ConsoleView
from dungeon_adventure.views.console.map_visualizer import MapVisualizer
from src import GameModel


def setup_game():
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
    game_model = setup_game()
    if game_model:
        view = ConsoleView()
        map_visualizer = MapVisualizer(game_model.dungeon)
        player_action_controller = PlayerActionController(
            game_model, map_visualizer, view
        )
        controller = GameController(game_model, player_action_controller, view)
        controller.run_game()
    else:
        print("Failed to set up the game. Exiting.")


if __name__ == "__main__":
    main()
