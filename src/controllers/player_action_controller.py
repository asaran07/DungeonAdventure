from typing import Optional
from src.characters.player import Player
from src.dungeon import Room
from src.enums.room_types import Direction
from src.game.dungeon_adventure import GameModel
from src.items.item import Item
from src.views.map_visualizer import MapVisualizer


class PlayerActionController:
    """
    Includes methods for executing player actions.
    """

    def __init__(self, game_model: GameModel):
        self.game_model = game_model
        self.map_visualizer = MapVisualizer(game_model.dungeon)

    def initialize_map(self):
        """Initialize the map visualizer after the dungeon has been set up."""
        self.map_visualizer.initialize()

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
                new_room.explore()
                self.map_visualizer.update_explored_rooms(new_room)  # Update explored rooms in map
                return True
        return False

    def pick_up_item(self, item: Item) -> bool:
        """
        Adds specified item to the player's inventory.

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

    def handle_action(self, action: str):
        action_parts = action.lower().split()
        if action_parts[0] == "move" and len(action_parts) > 1:
            direction_str = action_parts[1]
            self.handle_movement(direction_str)
        elif action_parts[0] == "map":
            self.display_map()
        elif action_parts[0] == "inventory" or action_parts[0] == "inv":
            self.display_inventory()

    def display_inventory(self):
        """Displays player's current inventory."""
        print(self.game_model.player.inventory_to_string())

    def display_map(self):
        current_room = self.game_model.player.current_room
        self.map_visualizer.display_map(current_room)

    def handle_movement(self, direction_str: str):
        try:
            direction = Direction.from_string(direction_str)
            success = self.move_player(direction)
            if success:
                print(f"You moved {direction.name.lower()}.")
            else:
                print(f"You can't move {direction.name.lower()} from here.")
        except ValueError as e:
            print(str(e))
