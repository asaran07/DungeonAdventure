import os
import pickle
from typing import Any, Optional

from src.characters import Player
from src.dungeon import Room
from src.game.dungeon_adventure import GameModel
from src.views import map_visualizer
from src.views.map_visualizer import MapVisualizer
from src.views.view import View


class ProjectState:
    """Saves and loads the current project state."""

    def __init__(self,
                 game_model: GameModel,
                 map_visualizer: MapVisualizer,
                 view,
                 player: Player,
                 current_room: Optional[Room]) -> None:
        self.game_model: GameModel = game_model
        self.map_visualizer: MapVisualizer = map_visualizer
        self.view: View = view
        self.player: Player = player
        self.current_room: Room = current_room

    # def __getstate__(self):
    #     return self.game_model, self.map_visualizer

    # def __setstate__(self, state):
    #     self.game_model, self.map_visualizer = state

    def get_game_model(self) -> GameModel:
        return self.game_model

    def get_map_visualizer(self) -> MapVisualizer:
        return self.map_visualizer

    def get_view(self) -> View:
        return self.view

    def get_player(self) -> Player:
        return self.player

    def get_current_room(self) -> Room:
        return self.current_room


def load_game(file_path: str) -> ProjectState:
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


def save_game(game_state: ProjectState, file_name: str) -> None:
    with open(file_name, 'wb') as file:
        # wb means write binary
        pickle.dump(game_state, file)
        print(f"Game saved to {file_name}")
