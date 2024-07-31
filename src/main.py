from src.characters import Player
from src.controllers.game_controller import GameController
from src.dungeon import Dungeon, Room
from src.dungeon.dungeon_generator import DungeonGenerator
from src.game.dungeon_adventure import GameModel, GameModelError
from src.views.console_view import ConsoleView


def setup_game():
    try:
        dungeon = DungeonGenerator.generate_default_dungeon()
        player = Player("Player 1")
        entrance_room = Room("Entrance Room")
        if entrance_room is None:
            raise ValueError("Dungeon has no entrance room")
        player.current_room = entrance_room
        game_model = GameModel(player, dungeon)
        return game_model
    except (ValueError, GameModelError) as e:
        print(f"Error setting up the game: {e}")
        return None


def main():
    game_model = setup_game()
    if game_model:
        view = ConsoleView()
        controller = GameController(game_model, view)
        controller.run_game()
    else:
        print("Failed to set up the game. Exiting.")


if __name__ == "__main__":
    main()
