import os
import pickle
from typing import Any

from src.game.dungeon_adventure import GameModel


def load_game(file_path: str) -> GameModel:
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as file:
    #         return pickle.load(file)

    # with open(file_path, 'rb') as file:
    #     return pickle.load(file)

    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:
            with open(file_path, 'rb') as file:
                return pickle.load(file)
        else:
            print("Error: File is empty.")

    else:
        print(f"Error: File {file_path} does not exist.")


def save_game(model: GameModel, file_name: str) -> None:
    with open(file_name, 'wb') as file:
        # wb means write binary
        pickle.dump(model, file)
        print(f"Game saved to {file_name}")


class ProjectState:
    """Saves and loads the current project state."""
    def __init__(self, game_model: GameModel) -> None:
        self.game_model: GameModel = game_model


