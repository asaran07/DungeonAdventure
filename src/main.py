from src.controllers.game_controller import GameController
from src.dungeon import Room
from src.enums import Direction
from src.enums.item_types import ItemType, WeaponType
from src.game.dungeon_adventure import GameModel
from src.items.weapon import Weapon
from src.views.console_view import ConsoleView


def main():
    game_model = GameModel()
    game_model.initialize_game()

    view = ConsoleView()
    controller = GameController(game_model, view)

    controller.run_game()


if __name__ == "__main__":
    main()

# TODO: Move everything below into their appropriate classes.
# room = Room("Main Entrance")
# room2 = Room("Lobby")
# room.connect(Direction.NORTH, room2)
# sword = Weapon("Excalibur", ItemType.WEAPON, "A legendary sword", 5.0, WeaponType.SWORD, 100)
#
# print(room)
