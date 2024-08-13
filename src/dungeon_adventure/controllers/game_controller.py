from dungeon_adventure.controllers.player_action_controller import (
    PlayerActionController,
)
from dungeon_adventure.enums.game_state import GameState
from dungeon_adventure.exceptions.dungeon import RoomNotFoundError
from dungeon_adventure.exceptions.game_logic import GameStateError
from dungeon_adventure.exceptions.input import InvalidInputError
from dungeon_adventure.exceptions.player import InvalidPlayerActionError
from dungeon_adventure.game_model import GameModel
from dungeon_adventure.views.view import View
from serialization.game_snapshot import GameSnapshot, load_game


class GameController:
    def __init__(
        self,
        game_model: GameModel,
        player_action_controller: PlayerActionController,
        view: View,
    ):
        self.game_model = game_model
        self.player_action_controller = player_action_controller
        self.view = view

    def run_game(self):
        self.game_model.game_state = GameState.TITLE_SCREEN
        # Run loop until GameState is 'game over'
        while not self.game_model.is_game_over():
            # Here we figure out what needs to happen depending on the current state
            self.handle_current_state()

    def handle_current_state(self):
        current_state = self.game_model.game_state

        if current_state == GameState.TITLE_SCREEN:
            self.handle_title_screen()
        elif current_state == GameState.PLAYER_CREATION:
            self.handle_player_creation()
        elif current_state == GameState.LOAD:
            self.handle_load()
        elif current_state == GameState.EXPLORING:
            self.handle_exploration()
        else:
            raise GameStateError(f"Invalid game state: {current_state}")

    def handle_title_screen(self):
        self.view.display_title_screen()
        while True:
            choice = self.view.get_user_input(
                "Please enter your choice (1 to Start, 2 to Load, 3 to Quit)"
            )
            if choice == "1":
                self.game_model.game_state = GameState.PLAYER_CREATION
                break
            elif choice == "2":
                self.game_model.game_state = GameState.LOAD
                break
            elif choice == "3":
                self.game_model.set_game_over(True)
                break
            else:
                raise InvalidInputError("Invalid choice. Please enter 1, 2, or 3.")

    def handle_player_creation(self):
        try:
            player_data = self.view.get_player_creation_input()
            self.game_model.update_player(player_data)
            entrance_room = self.game_model.dungeon.get_room("Room 1 - Entrance Hall")
            if entrance_room is None:
                raise RoomNotFoundError("Entrance room not found.")
            entrance_room.explore()
            self.player_action_controller.initialize_map()
            self.game_model.game_state = GameState.EXPLORING
        except RoomNotFoundError as e:
            self.view.display_message(f"Room Error: {e}. Resetting game...")
            self.reset_to_safe_state()

    def handle_load(self):
        try:
            proj_state: GameSnapshot = load_game("save.pkl")
            self.game_model = proj_state.get_game_model()
            self.player_action_controller = PlayerActionController(
                proj_state.game_model, proj_state.map_visualizer, proj_state.view
            )
        except FileNotFoundError as e:
            self.view.display_message(f"File not found: {e}")

    def handle_exploration(self):
        # self.view.display_player_status(self.game_model)
        # self.view.display_available_actions(self.game_model)
        # self.view.display_game_state(self.game_model)
        try:
            action = self.view.get_user_input("Please enter your choice")
            self.player_action_controller.handle_action(action)
        except (InvalidPlayerActionError, InvalidInputError) as e:
            self.view.display_message(f"Action Error: {e}. Please try again.")

    def reset_to_safe_state(self):
        self.view.display_message("Resetting to a safe state...")
        self.game_model.game_state = GameState.TITLE_SCREEN
        # TODO: need to add reset logic

    def handle_input(self, user_input):
        # This method is currently not used, but we can add error handling if needed
        pass
