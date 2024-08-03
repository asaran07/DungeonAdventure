from typing import Dict, List

from src.characters import Player
from src.characters.monster import Monster
from src.enums.game_state import GameState
from src.game.dungeon_adventure import GameModel
from src.views.view import View


class ConsoleViewException(Exception):
    """Base exception for ConsoleView"""

    pass


class InvalidInputException(ConsoleViewException):
    """Raised when user input is invalid"""

    pass


class PlayerNotExistException(ConsoleViewException):
    """Raised when player does not exist in the game model"""

    pass


class RoomNotExistException(ConsoleViewException):
    """Raised when current room does not exist for the player"""

    pass


class UnsupportedGameStateException(ConsoleViewException):
    """Raised when trying to display actions for an unsupported game state"""

    pass


class ConsoleView(View):
    """
    This class displays things to the console and gets input from the player
    """

    def display_message(self, message):
        print(message)

    def display_title_screen(self):
        print("Welcome to Dungeon Adventure!")
        print("1. Start New Game")
        print("2. Quit")

    def get_user_input(self, prompt: str) -> str:
        user_input = input(prompt + ": ").strip()
        if not user_input:
            raise InvalidInputException("Input cannot be empty")
        return user_input

    def get_player_creation_input(self) -> Dict:
        try:
            name = self.get_user_input("Enter your character's name: ")
            return {"name": name}
        except InvalidInputException:
            raise InvalidInputException("Player name cannot be empty")

    def display_current_state(self, game_model: GameModel):
        player = game_model.player
        if player is None:
            raise PlayerNotExistException("Player does not exist in the game model")
        print(f"HP: {player.hero.current_hp}/{player.hero.max_hp}")
        print(f"XP: {player.hero.xp}/{player.hero.xp_to_next_level}")


    def display_combat_status(self, player: Player, monsters: List[Monster]):
        print("\n=== Combat Status ===")
        print(f"Player: {player.name}")
        print(f"HP: {player.hero.current_hp}/{player.hero.max_hp}")
        print("\nMonsters:")
        for i, monster in enumerate(monsters, 1):
            print(f"{i}. {monster.name} - HP: {monster.current_hp}/{monster.max_hp}")
        print("====================\n")

    def display_xp_gained(self, xp_amount: int):
        print("\n=== XP Gained ===")
        print("You gained " + str(xp_amount) + " XP!")

    def get_combat_action(self) -> str:
        print("Combat Actions:")
        print("1. Attack")
        print("2. Use Item")
        print("3. Flee")
        while True:
            try:
                choice = self.get_user_input("Choose an action (1-3): ")
                if choice in ["1", "2", "3"]:
                    if choice == "1":
                        return "attack"
                    elif choice == "2":
                        return "use_item"
                    else:
                        return "flee"
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")

    def display_player_status(self, game_model: GameModel):
        """Displays the Player's info and location, along with room details"""
        player = game_model.player
        if player is None:
            raise PlayerNotExistException("Player does not exist in the game model")

        # print(f"Player: {player.name}")
        # print(f"HP: {player.hero.current_hp}/{player.hero.max_hp}")
        # print(f"XP: {player.hero.xp}/{player.hero.xp_to_next_level}")
        # print(f"Current Room: {player.current_room.get_desc()}")

    def display_available_actions(self, game_model):
        if game_model.game_state == GameState.EXPLORING:
            print(
                "Available actions: move, map, inventory, take, drop, stats, equip, use"
            )
            # print("- move [direction]")
            # print("- use [item]")
            # print("- inventory")
        else:
            raise UnsupportedGameStateException(
                f"Cannot display actions for game state: {game_model.game_state}"
            )

    def get_combat_target(self, monsters):
        print("Choose a target:")
        for i, monster in enumerate(monsters, 1):
            print(f"{i}. {monster.name}")
        while True:
            try:
                choice = self.get_user_input("Enter the number of the target: ")
                if choice.isdigit() and 1 <= int(choice) <= len(monsters):
                    return monsters[int(choice) - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")

    def display_game_state(self, game_model: GameModel):
        pass
