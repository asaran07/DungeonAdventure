from typing import Dict
from src.game.dungeon_adventure import GameModel
from src.views.view import View


class ConsoleView(View):
    """
    Implements the 'View' interface for text-based gameplay. This class handles all console I/O operations,
    including displaying the current game state, room descriptions, player status etc.
    """

    def display_message(self, message):
        print(message)

    def display_title_screen(self):
        print("Welcome to Dungeon Adventure!")
        print("1. Start New Game")
        print("2. Quit")

    # TODO: Update this method to use a custom string as params
    def get_user_input(self):
        return input("Enter your choice: ")

    def get_player_creation_input(self) -> Dict:
        name = input("Enter your character's name: ")
        # We can add more inputs later
        return {"name": name}

    def display_game_state(self, game_model: GameModel):
        player = game_model.get_player()
        if player is not None:
            print(f"Player: {player.get_name()}")
            print(f"HP: {player.get_hp()}")
            current_room = player.get_current_room()
            if current_room is not None:
                print(f"Player is in room: {current_room.name}")
                print(f"Current Room: {current_room.get_description()}")
            else:
                print("Player is not in a room!")
        else:
            print("Player does not exist.")

        print("Available actions:")
        print("- move [direction]")
        print("- use [item]")
        print("- inventory")
