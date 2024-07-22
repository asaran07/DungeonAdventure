from src.views.view import View


class ConsoleView(View):
    """
    Implements the 'View' interface for text-based gameplay. This class handles all console I/O operations,
    including displaying the current game state, room descriptions, player status etc.
    """

    def display_game_state(self, game_model):
        # our console logic
        pass

    def get_user_input(self):
        pass

    def display_message(self, message):
        print(message)
