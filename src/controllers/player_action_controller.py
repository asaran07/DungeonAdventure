from typing import Optional
from src.characters.player import Player
from src.dungeon import Room
from src.enums.item_types import WeaponType, ItemType
from src.enums.room_types import Direction
from src.game.dungeon_adventure import GameModel
from src.items.item import Item
from src.items.potion import HealingPotion
from src.items.weapon import Weapon
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
        print(current_room.items)
        print(item, "asdf")
        # if item in current_room.items: ==> wont work
        #     current_room.remove_item(item)
        #     player.add_to_inventory(item)
        #     return True
        for index, room_item in enumerate(current_room.items):
            print("bruh ", item.name in room_item.name, item.name, room_item.name)
            print("a", room_item == item)
            if room_item == item : # or item.name in room_item.name
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
        elif action_parts[0] == "take" and len(action_parts) > 1:
            item_str = ' '.join(action_parts[1:])  # get all words except "take"
            item_str = item_str.title()  # Capitalize each word
            self.handle_item(item_str)

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

    def handle_item(self, item_str: str):
        try:
            item: Item = Weapon(item_str, "A basic sword", 1, WeaponType.SWORD, 2, 10)
            successful = self.pick_up_item(item)
            if successful:
                print(f"You picked up {item.name.lower()}.")
            else:
                print(f"{item.name.lower()} isn't in this room.")
        except ValueError as e:
            print(str(e))
