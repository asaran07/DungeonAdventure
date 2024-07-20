from abc import ABC, abstractmethod


class View(ABC):
    @abstractmethod
    def display_game_state(self, game_model):
        pass

    @abstractmethod
    def get_user_input(self):
        pass

    @abstractmethod
    def display_message(self, message):
        pass
