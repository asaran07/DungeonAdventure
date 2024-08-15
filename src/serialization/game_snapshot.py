import os
import pickle
from typing import Optional

from dungeon_adventure.game_model import GameModel
from dungeon_adventure.models.dungeon.dungeon import Dungeon
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.player.player import Player
from dungeon_adventure.views.console.map_visualizer import MapVisualizer
from dungeon_adventure.views.view import View


class GameSnapshot:
    """Represents the serializable object for saving and loading the game."""

    def __init__(
            self,
            game_model: GameModel,
            map_visualizer: MapVisualizer,
            view,
            player: Player,
            current_room: Optional[Room],
    ) -> None:
        self.game_model: GameModel = game_model
        self.map_visualizer: MapVisualizer = map_visualizer
        self.view: View = view
        self.player: Player = player
        self.current_room: Room = current_room

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


class GameSnapshotPygame:
    """Represents serializable object for saving and loading in Pygame."""

    def __init__(
            self,
            dungeon,
            # room_dict,
            current_room,
            player,
            game_model: GameModel,

    ):
        self.dungeon = dungeon
        # self.room_dict: dict = room_dict
        self.current_room: Room = current_room
        self.player: Player = player
        self.game_model: GameModel = game_model

    def get_dungeon(self) -> Dungeon:
        return self.dungeon

    # def get_room_dict(self) -> dict:
    #     return self.room_dict
    #
    def get_current_room(self) -> Room:
        return self.current_room

    def get_player(self) -> Player:
        return self.player

    def get_game_model(self) -> GameModel:
        return self.game_model


def load_game(file_path: str):
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:
            with open(file_path, "rb") as file:
                return pickle.load(file)
        else:
            print("Error: File is empty.")

    else:
        print(f"Error: File {file_path} does not exist.")


def save_game(game_state, file_name: str) -> None:
    with open(file_name, "wb") as file:
        pickle.dump(game_state, file)
        print(f"Game saved to {file_name}")
