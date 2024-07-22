from abc import ABC, abstractmethod


class View(ABC):
    """
    Core interface for game display and user interaction. This abstract class lets all view implementations show and
    work with game states, collect user inputs, and display messages regardless of the actual display method used (
    console, GUI, etc.)
    """
    @abstractmethod
    def display_game_state(self, game_model):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

    @abstractmethod
    def display_message(self, message):
        pass
