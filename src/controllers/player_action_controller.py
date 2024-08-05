from typing import Optional

from src.characters.player import Player
from src.combat.combat_handler import CombatHandler
from src.dungeon import Room
from src.enums.room_types import Direction, RoomType
from src.exceptions.player import (
    PlayerNotInRoomError,
    InvalidDirectionError,
    ItemNotInRoomError,
    ItemNotInInventoryError,
)
from src.game.dungeon_adventure import GameModel
from src.items.item import Item
from src.items.potion import HealingPotion
from src.items.weapon import Weapon
from src.views.map_visualizer import MapVisualizer
from src.views.view import View


class PlayerActionController:
    """
    Includes methods for executing player actions.
    """

    def __init__(
        self, game_model: GameModel, map_visualizer: MapVisualizer, view2: View
    ):
        self.game_model = game_model
        self.map_visualizer = map_visualizer
        self.view = view2
        self.combat_handler: CombatHandler = CombatHandler(game_model, self.view)
        self.player: Player = game_model.player
        self.current_room: Optional[Room] = self.player.current_room

    @property
    def view(self) -> View:
        return self.view

    def _check_player_in_room(self):
        if self.current_room is None:
            raise PlayerNotInRoomError("Player is not in a room")

    def _check_item_in_room(self, item: Item):
        self._check_player_in_room()
        if item not in self.current_room.items:
            raise ItemNotInRoomError(f"{item.name} is not in this room")

    def _check_item_in_inventory(self, item_name: str) -> Item:
        item = self.player.inventory.get_item_by_name(item_name)
        if item is None:
            raise ItemNotInInventoryError(f"You don't have an item named {item_name}")
        return item

    def _check_valid_direction(self, direction: Direction):
        if direction not in dict(self.current_room.get_open_gates()):
            raise InvalidDirectionError(
                f"You can't move {direction.name.lower()} from here"
            )

    def initialize_map(self):
        """Initialize the map visualizer after the dungeon has been set up."""
        self.map_visualizer.initialize()

    def move_player(self, direction: Direction) -> bool:
        """
        Moves the player to specified direction.

        :param direction: The direction in which to move to
        :return: True if player was moved, False otherwise
        """
        try:
            self._check_player_in_room()
            self._check_valid_direction(direction)

            new_room = self.current_room.connections[direction]
            self.player.current_room = new_room
            self.current_room = new_room
            new_room.explore()
            self.map_visualizer.update_explored_rooms(new_room)
            self.enter_room()
            return True
        except (PlayerNotInRoomError, InvalidDirectionError) as e:
            self.view.display_message(str(e))
            return False

    def pick_up_item(self, item: Item) -> bool:
        """
        Adds specified item to the player's inventory.

        :param item: The item to pick up
        :return: True if item was picked up, False otherwise
        """
        try:
            self._check_item_in_room(item)
            self.current_room.remove_item(item)
            self.player.inventory.add_item(item)
            return True
        except (PlayerNotInRoomError, ItemNotInRoomError) as e:
            self.view.display_message(str(e))
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
            item_str = " ".join(action_parts[1:])  # get all words except the first
            item_str = item_str.title()  # Capitalize each word
            if action_parts[0] == "take" and len(action_parts) > 1:
                self.handle_pickup(item_str)
            elif len(action_parts) > 1:
                self.handle_drop(item_str)
        elif action_parts[0] == "equip" and len(action_parts) > 1:
            weapon_name = " ".join(action_parts[1:])
            self.handle_equip(weapon_name)
        elif action_parts[0] == "use" and len(action_parts) > 1:
            item_name = " ".join(action_parts[1:])
            self.handle_use_item(item_name)

    def handle_equip(self, weapon_name: str):
        try:
            weapon = self._check_item_in_inventory(weapon_name)
            if isinstance(weapon, Weapon):
                self.player.hero.equip_weapon(weapon)
                self.view.display_message(f"You equipped {weapon.name}.")
            else:
                self.view.display_message(f"{weapon_name} is not a weapon.")
        except ItemNotInInventoryError as e:
            self.view.display_message(str(e))

    def handle_use_item(self, item_name: str):
        try:
            item = self._check_item_in_inventory(item_name)
            if self.player.use_item(item):
                self.view.display_message(f"You used {item.name}.")
            else:
                self.view.display_message(f"You couldn't use {item.name}.")
        except ItemNotInInventoryError as e:
            self.view.display_message(str(e))

    def handle_pickup(self, item_str: str):
        try:
            self._check_player_in_room()
            item = next(
                (i for i in self.current_room.items if item_str in i.name), None
            )
            if item is None:
                raise ItemNotInRoomError(f"{item_str} wasn't found in this room.")

            if self.pick_up_item(item):
                self.view.display_message(f"You picked up {item.name.lower()}.")
        except (PlayerNotInRoomError, ItemNotInRoomError) as e:
            self.view.display_message(str(e))

    def handle_drop(self, item_str: str):
        try:
            self._check_player_in_room()
            item = self.player.inventory.remove_item_by_id(item_str)
            if item is None:
                raise ItemNotInInventoryError(
                    f"'{item_str.lower()}' wasn't found in your inventory."
                )

            self.current_room.add_item(item)
            self.view.display_message(f"You dropped {item.name.lower()}.")
        except (PlayerNotInRoomError, ItemNotInInventoryError) as e:
            self.view.display_message(str(e))

    def display_inventory(self):
        self.view.display_inventory(self.player.inventory)

    def display_map(self):
        self.view.display_map(self.current_room)

    def handle_movement(self, direction_str: str):
        try:
            direction = Direction.from_string(direction_str)
            self.move_player(direction)
        except ValueError as e:
            self.view.display_message(str(e))

    def enter_room(self):
        self.view.display_room_entrance(self.current_room)
        self.display_map()

        if self.current_room.room_type == RoomType.PIT:
            damage = 50
            self.player.hero.take_damage(damage)
            self.view.display_pit_damage(damage)
            if not self.player.hero.is_alive:
                self.game_model.set_game_over(True)
                self.view.display_game_over()

        if self.current_room.has_items:
            self.view.display_room_contents(self.current_room)
        if self.current_room.has_monsters:
            self.view.display_combat_start()
            self.combat_handler.initiate_combat()
        else:
            self.view.display_empty_room()
