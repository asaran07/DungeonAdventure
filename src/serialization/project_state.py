import os
import pickle

from src.game.dungeon_adventure import GameModel


def load_game(file_path: str) -> GameModel:
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            return pickle.load(file)


def save_game(model: GameModel, file_path: str) -> None:
    with open(file_path, 'wb') as file:
        # wb means write binary
        pickle.dump(model, file)


class ProjectState:
    """Saves and loads the current project state."""
    def __init__(self, game_model: GameModel) -> None:
        self.game_model: GameModel = game_model

