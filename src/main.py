from src.characters import Player
from src.controllers.game_controller import GameController
from src.controllers.player_action_controller import PlayerActionController
from src.dungeon import Room
from src.dungeon.dungeon_generator import DungeonGenerator
from src.game.dungeon_adventure import GameModel, GameModelError
from src.views.console_view import ConsoleView
from src.views.map_visualizer import MapVisualizer


def setup_game():
    try:
        dungeon = DungeonGenerator.generate_default_dungeon()
        player = Player("Player 1")
        if dungeon.entrance_room is None:
            raise ValueError("Dungeon has no entrance room")
        player.current_room = dungeon.entrance_room
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
        player_action_controller = PlayerActionController(game_model, map_visualizer, view)
        controller = GameController(game_model, player_action_controller, view)
        controller.run_game()
    else:
        print("Failed to set up the game. Exiting.")


if __name__ == "__main__":
    main()
