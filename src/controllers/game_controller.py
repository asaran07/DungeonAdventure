from src.controllers.player_action_controller import PlayerActionController
from src.game.dungeon_adventure import GameModel
from src.views.view import View
from src.enums.game_state import GameState
from src.exceptions import (
    InvalidInputError,
    GameStateError,
    RoomNotFoundError,
    InvalidPlayerActionError
)


class GameController:
    """
    This class manages the game loop, processes user inputs by using the PlayerActionController, updates the game
    state, and ensures the view is refreshed. It's responsible for initializing the game manage any game mechanics
    not specific to player actions.
    """

    def __init__(self, game_model: GameModel, view: View):
        self.game_model = game_model
        self.view = view
        self.player_action_controller = PlayerActionController(game_model)

    def run_game(self):
        self.game_model.game_state = GameState.TITLE_SCREEN

        while not self.game_model.is_game_over():
            current_state = self.game_model.game_state

            try:
                if current_state == GameState.TITLE_SCREEN:
                    self.handle_title_screen()
                elif current_state == GameState.PLAYER_CREATION:
                    self.handle_player_creation()
                elif current_state == GameState.EXPLORING:
                    self.handle_exploration()
                else:
                    raise GameStateError(f"Invalid game state: {current_state}")
            except GameStateError as e:
                self.view.display_message(f"Game State Error: {e}")
                self.game_model.set_game_over(True)

    def handle_title_screen(self):
        self.view.display_title_screen()
        try:
            choice = self.view.get_user_input("Please enter your choice: ")
            if choice == "1":  # Start New Game
                self.game_model.game_state = GameState.PLAYER_CREATION
            elif choice == "2":  # Quit
                self.game_model.set_game_over(True)
            else:
                raise InvalidInputError("Invalid choice. Please enter 1 or 2.")
        except InvalidInputError as e:
            self.view.display_message(f"Input Error: {e}")

    def handle_player_creation(self):
        try:
            player_data = self.view.get_player_creation_input()
            self.game_model.create_player(player_data)
            self.game_model.make_rooms()
            entrance_room = self.game_model.dungeon.get_room("Room 1")
            if entrance_room is None:
                raise RoomNotFoundError("Entrance room 'Room 1' not found.")
            self.game_model.player.current_room = entrance_room
            entrance_room.explore()  # Mark the entrance room as explored
            self.player_action_controller.initialize_map()
            self.game_model.game_state = GameState.EXPLORING
        except RoomNotFoundError as e:
            self.view.display_message(f"Room Error: {e}")
            self.game_model.set_game_over(True)

    def handle_exploration(self):
        self.view.display_player_status(self.game_model)
        self.view.display_available_actions(self.game_model)
        try:
            action = self.view.get_user_input("Please enter your choice: ")
            self.player_action_controller.handle_action(action)
        except InvalidPlayerActionError as e:
            self.view.display_message(f"Action Error: {e}")
        except InvalidInputError as e:
            self.view.display_message(f"Input Error: {e}")

    def handle_input(self, user_input):
        # This method is currently not used, but we can add error handling if needed
        pass
