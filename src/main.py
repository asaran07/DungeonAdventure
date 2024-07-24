from src.controllers.game_controller import GameController
from src.game.dungeon_adventure import GameModel
from src.views.console_view import ConsoleView


def main():
    # We create the GameModel and initialize the core game stuff we need like player and dungeon map etc.
    game_model = GameModel()
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
