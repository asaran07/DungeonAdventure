from src.controllers.player_action_controller import PlayerActionController
from src.game.dungeon_adventure import GameModel
from src.views.view import View


class GameController:
    """
    This class manages the game loop, processes user inputs by using the PlayerActionController, updates the game
    state, and ensures the view is refreshed. It's responsible for initializing the game, handling turn-based logic,
    checking for game-over conditions, and manage any game mechanics not specific to player actions.
    """

    def __init__(self, game_model: GameModel, view: View):
        self.game_model = game_model
        self.view = view
        self.player_action_controller = PlayerActionController(game_model)

    def run_game(self):
        while not self.game_model.is_game_over():
            self.view.display_game_state(self.game_model)
            user_input = self.view.get_user_input()
            self.handle_input(user_input)

    def handle_input(self, user_input):
        pass
