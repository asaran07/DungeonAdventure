from typing import Dict
from src.enums.game_state import GameState
from src.game.dungeon_adventure import GameModel
from src.views.view import View


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

    # TODO: Update this method to use a custom string as params
    def get_user_input(self, prompt: str) -> str:
        return input(prompt)

    def get_player_creation_input(self) -> Dict:
        name = input("Enter your character's name: ")
        # We can add more inputs later
        return {"name": name}

    def display_player_status(self, game_model: GameModel):
        """Displays the Player's info and location, along with room details"""
        player = game_model.player
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

    def display_available_actions(self, game_model) -> str:
        if game_model.game_state == GameState.EXPLORING:
            print("Available actions:")
            print("- move [direction]")
            print("- use [item]")
            print("- inventory")
            return self.get_user_input("Please enter your action: ")
        else:
            return "No info on what to display using game state"
