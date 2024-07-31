from typing import Optional

from src.characters.player import Player
from src.combat.combat_handler import CombatHandler
from src.dungeon import Room
from src.enums.room_types import Direction
from src.game.dungeon_adventure import GameModel
from src.items.item import Item
from src.items.potion import HealingPotion
from src.views.map_visualizer import MapVisualizer
from src.views.view import View


class PlayerActionController:
    """
    Includes methods for executing player actions.
    """

    def __init__(self, game_model: GameModel, map_visualizer: MapVisualizer, view2: View):
        self.game_model = game_model
        self.map_visualizer = map_visualizer
        self._view = view2
        self.combat_handler: CombatHandler = CombatHandler(game_model, self._view)

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
        current_room = player.current_room

        if current_room is None:
            return False  # Can't move if not in a room

        if direction in dict(current_room.get_open_gates()):
            new_room = current_room.connections[direction]
            if new_room is not None:
                player.current_room = new_room
                new_room.explore()
                self.map_visualizer.update_explored_rooms(new_room)  # Update explored rooms in map
                self.enter_room()
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
            print("Player not in a room?")
            return False

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
        elif action_parts[0] == "take" or action_parts[0] == "drop":
            item_str = ' '.join(action_parts[1:])  # get all words except the first
            item_str = item_str.title()  # Capitalize each word
            if action_parts[0] == "take" and len(action_parts) > 1:
                self.handle_pickup(item_str)
            elif len(action_parts) > 1:
                self.handle_drop(item_str)

    def handle_pickup(self, item_str: str):
        try:
            # Make an empty item with only the name
            item: Item = HealingPotion(item_str)
            player: Player = self.game_model.player
            current_room: Optional[Room] = player.current_room
            for room_item in current_room.items:
                if item_str in room_item.name:
                    item: Item = room_item
            successful = self.pick_up_item(item)
            if successful:
                print(f"You picked up {item.name.lower()}.")
            else:
                print(f"{item.name.lower()} wasn't found in this room.")
        except ValueError as e:
            print(str(e))

    def handle_drop(self, item_str: str):
        try:
            successful = False
            player: Player = self.game_model.player
            current_room: Optional[Room] = player.current_room
            item = player.remove_from_inventory(item_str)
            current_room.add_item(item)
            if item is not None:
                successful = True
            if successful:
                print(f"You dropped {item.name.lower()}.")
            else:
                print(f"'{item_str.lower()}' wasn't found in your inventory.")
        except ValueError as e:
            print(str(e))

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

    def enter_room(self):
        room = self.game_model.player.current_room
        print(f"You enter {room.name}")
        print(room.get_description())
        if room.has_monsters:
            print(f"You encounter monsters!")
            self.combat_handler.initiate_combat()
        else:
            print("The room appears to be empty.")
