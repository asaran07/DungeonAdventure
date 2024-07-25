from typing import Optional
from src.characters.player import Player
from src.dungeon import Room
from src.enums.room_types import Direction
from src.game.dungeon_adventure import GameModel
from src.items.item import Item


class PlayerActionController:
    """
    Includes methods for executing player actions.
    """

    def __init__(self, game_model: GameModel):
        self.game_model = game_model

    def move_player(self, direction: Direction) -> bool:
        """
        Moves the player to specified direction.

        :param direction: The direction in which to move to
        :return: True if player was moved, False otherwise
        """
        player: Player = self.game_model.player
        current_room: Optional[Room] = player.current_room

        if current_room is None:
            return False  # Can't move if not in a room

        if direction in dict(current_room.get_open_gates()):
            new_room = current_room.connections[direction]
            if new_room is not None:
                player.current_room = new_room
                return True
        return False

    def pick_up_item(self, item: Item) -> bool:
        """
        Adds speficied item to the player's inventory.

        :param item: The item to pick up
        :return: True if item was picked up, False otherwise
        """
        player: Player = self.game_model.player
        current_room: Optional[Room] = player.current_room

        if current_room is None:
            return False  # Can't pick up an item if not in a room

        if item in current_room.items:
            current_room.remove_item(item)
            player.add_to_inventory(item)
            return True
        return False

    # and we can add other player actions like use_item or attack etc
    def handle_action(self, action):
        pass
