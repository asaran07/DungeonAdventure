from typing import Dict
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
        user_input = input(prompt).strip()
        if not user_input:
            raise InvalidInputException("Input cannot be empty")
        return user_input

    def get_player_creation_input(self) -> Dict:
        try:
            name = self.get_user_input("Enter your character's name: ")
            return {"name": name}
        except InvalidInputException:
            raise InvalidInputException("Player name cannot be empty")

    def display_player_status(self, game_model: GameModel):
        """Displays the Player's info and location, along with room details"""
        player = game_model.player
        if player is None:
            raise PlayerNotExistException("Player does not exist in the game model")

        # print(f"Player: {player.name}")
        # print(f"HP: {player.hit_points}")
        current_room = player.current_room
        if current_room is None:
            raise RoomNotExistException("Player is not in a room")

        # print(f"Current Room: {current_room.get_description()}")

    def display_available_actions(self, game_model):
        if game_model.game_state == GameState.EXPLORING:
            print("Available actions: move, map, inventory, take")
            # print("- move [direction]")
            # print("- use [item]")
            # print("- inventory")
        else:
            raise UnsupportedGameStateException(
                f"Cannot display actions for game state: {game_model.game_state}"
            )
