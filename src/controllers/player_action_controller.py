from typing import Optional

from src.characters.player import Player
from src.controllers.combat_controller import CombatHandler
from src.constants import Resources as Res
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
from src.items.weapon import Weapon
from src.views.map_visualizer import MapVisualizer
from src.views.view import View


class PlayerActionController:
    """
    Includes methods for executing player actions.
    """

    def __init__(
        self, game_model: GameModel, map_visualizer: MapVisualizer, view: View
    ):
        self.game_model = game_model
        self.map_visualizer = map_visualizer
        self._view = view
        self.player: Player = game_model.player
        self.current_room: Optional[Room] = self.player.current_room
        self.combat_handler: CombatHandler = CombatHandler(game_model, self._view)

    @property
    def view(self) -> View:
        return self._view

    @view.setter
    def view(self, new_view: View) -> None:
        self._view = new_view
        # Update the combat handler's view as well
        self.combat_handler = CombatHandler(self.game_model, self._view)

    def _check_player_in_room(self):
        if self.current_room is None:
            raise PlayerNotInRoomError(Res.Errors.PLAYER_NOT_IN_ROOM)

    def _check_item_in_room(self, item: Item):
        self._check_player_in_room()
        if item not in self.current_room.items:
            raise ItemNotInRoomError(Res.Errors.ITEM_NOT_IN_ROOM.format(item.name))

    def _check_item_in_inventory(self, item_name: str) -> Item:
        item = self.player.inventory.get_item_by_name(item_name)
        if item is None:
            raise ItemNotInInventoryError(
                Res.Errors.ITEM_NOT_IN_INVENTORY.format(item_name)
            )
        return item

    def _check_valid_direction(self, direction: Direction):
        if direction not in dict(self.current_room.get_open_gates()):
            raise InvalidDirectionError(
                Res.Errors.INVALID_DIRECTION.format(direction.name.lower())
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
        if action_parts[0] == Res.Actions.MOVE and len(action_parts) > 1:
            direction_str = action_parts[1]
            self.handle_movement(direction_str)
        elif action_parts[0] == Res.Actions.MAP:
            self.display_map()
        elif action_parts[0] in [Res.Actions.INVENTORY, Res.Actions.INVENTORY_SHORT]:
            self.display_inventory()
        elif action_parts[0] in [Res.Actions.TAKE, Res.Actions.DROP]:
            item_str = " ".join(action_parts[1:]).title()
            if action_parts[0] == Res.Actions.TAKE and len(action_parts) > 1:
                self.handle_pickup(item_str)
            elif len(action_parts) > 1:
                self.handle_drop(item_str)
        elif action_parts[0] == Res.Actions.EQUIP and len(action_parts) > 1:
            weapon_name = " ".join(action_parts[1:])
            self.handle_equip(weapon_name)
        elif action_parts[0] == Res.Actions.USE and len(action_parts) > 1:
            item_name = " ".join(action_parts[1:])
            self.handle_use_item(item_name)

    def handle_equip(self, weapon_name: str):
        try:
            weapon = self._check_item_in_inventory(weapon_name)
            if isinstance(weapon, Weapon):
                self.player.hero.equip_weapon(weapon)
                self.view.display_message(
                    Res.Messages.EQUIP_SUCCESS.format(weapon.name)
                )
            else:
                self.view.display_message(Res.Errors.NOT_A_WEAPON.format(weapon_name))
        except ItemNotInInventoryError as e:
            self.view.display_message(str(e))

    def handle_use_item(self, item_name: str):
        try:
            item = self._check_item_in_inventory(item_name)
            if self.player.use_item(item):
                self.view.display_message(Res.Messages.USE_SUCCESS.format(item_name))
            else:
                self.view.display_message(Res.Messages.USE_FAILURE.format(item_name))
        except ItemNotInInventoryError as e:
            self.view.display_message(str(e))

    def handle_pickup(self, item_str: str):
        try:
            self._check_player_in_room()
            item = next(
                (i for i in self.current_room.items if item_str in i.name), None
            )
            if item is None:
                raise ItemNotInRoomError(Res.Errors.ITEM_NOT_IN_ROOM.format(item_str))

            if self.pick_up_item(item):
                self.view.display_message(Res.Messages.PICKUP_SUCCESS.format(item.name))
        except (PlayerNotInRoomError, ItemNotInRoomError) as e:
            self.view.display_message(str(e))

    def handle_drop(self, item_str: str):
        try:
            self._check_player_in_room()
            item = self.player.inventory.remove_item_by_id(item_str)
            if item is None:
                raise ItemNotInInventoryError(
                    Res.Errors.ITEM_NOT_IN_INVENTORY.format(item_str)
                )

            self.current_room.add_item(item)
            self.view.display_message(Res.Messages.DROP_SUCCESS.format(item.name))
        except (PlayerNotInRoomError, ItemNotInInventoryError) as e:
            self.view.display_message(str(e))

    def display_inventory(self):
        self.view.display_inventory(self.player.inventory)

    def display_map(self):
        self.view.display_map(self.current_room, self.map_visualizer)

    def handle_movement(self, direction_str: str):
        try:
            direction = Direction.from_string(direction_str)
            self.move_player(direction)
        except ValueError as e:
            self.view.display_message(str(e))

    def enter_room(self):
        self.view.display_room_entrance(self.current_room)
        self.display_map()

        self._handle_room_hazards()
        self._display_room_contents()
        self._handle_room_encounters()
        if self.current_room.room_type == RoomType.EXIT:
            if self._check_item_in_inventory("Abstraction Pillar"):
                # and self._check_item_in_inventory("Encapsulation Pillar") and self._check_item_in_inventory("Inheritance Pillar") and self._check_item_in_inventory("Polymorphism Pillar"):
                print(f"{self.player.name} has defeated the dungeon and won the game!")
                self._end_game()

    def _handle_room_hazards(self):
        if self.current_room.room_type == RoomType.PIT:
            self._handle_pit_hazard()

    def _handle_pit_hazard(self):
        self.player.hero.take_damage(Res.GameValues.PIT_DAMAGE)
        self.view.display_pit_damage(Res.GameValues.PIT_DAMAGE)
        if not self.player.hero.is_alive:
            self._end_game()

    def _end_game(self):
        self.game_model.set_game_over(True)
        self.view.display_game_over()

    def _display_room_contents(self):
        if self.current_room.has_items:
            self.view.display_room_contents(self.current_room)

    def _handle_room_encounters(self):
        if self.current_room.has_monsters:
            self._initiate_combat()
        else:
            self.view.display_empty_room()

    def _initiate_combat(self):
        self.view.display_combat_start()
        self.combat_handler.initiate_combat()
