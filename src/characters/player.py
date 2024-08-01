from typing import Dict, Optional, Tuple

from src.characters.hero import Hero
from src.dungeon.room import Room
from src.enums.item_types import ItemType
from src.exceptions.player import InventoryFullError
from src.items.item import Item


class InvalidPlayerAttributeError(Exception):
    """Custom exception for invalid player attributes."""

    pass


class Player:
    """Represents the player in the game."""

    def __init__(self, name: str, inventory_weight_limit: float = 50.0) -> None:
        """
        Initialize a new Player instance.

        :param name: The name of the player
        :param inventory_weight_limit: The maximum weight the player can carry
        :raises InvalidPlayerAttributeError: If name or hit_points are invalid
        """
        # NOTE: Raising an exception might seem weird because we don't want the game to break when
        # the player enters wrong info. However, this is the player class, checking for correct input
        # should already be delt with somewhere else. As if we let this slide deep here in the player
        # class, things would break further.
        if not name or not isinstance(name, str):
            raise InvalidPlayerAttributeError("Name must be a non-empty string")
        self._name: str = name
        self._inventory: Dict[str, Tuple[Item, int]] = {}
        self._inventory_weight_limit: float = inventory_weight_limit
        self.current_room: Optional[Room] = None
        self._hero: Hero = Hero()

    @property
    def hero(self) -> Hero:
        """Get the player's selected Hero character."""
        return self._hero

    @property
    def name(self) -> str:
        """Get the player's name."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def add_to_inventory(self, item: Item) -> None:
        """
        Add an item to the player's inventory.

        :param item: The item to add
        :raises InventoryFullError: If adding the item would exceed the weight limit
        """
        current_weight = sum(
            item.weight * quantity for item, quantity in self._inventory.values()
        )
        if current_weight + item.weight > self._inventory_weight_limit:
            raise InventoryFullError(
                "Adding this item would exceed the inventory weight limit"
            )

        if item.name in self._inventory:
            self._inventory[item.name] = (item, self._inventory[item.name][1] + 1)
        else:
            self._inventory[item.name] = (item, 1)

    def remove_from_inventory(self, item_name: str) -> Optional[Item]:
        """
        Remove an item from the player's inventory.

        :param item_name: The name of the item to remove
        :return: The removed item, or None if the item was not in the inventory
        """
        if item_name in self._inventory:
            item, quantity = self._inventory[item_name]
            if quantity > 1:
                self._inventory[item_name] = (item, quantity - 1)
            else:
                del self._inventory[item_name]
            return item
        return None

    def use_item(self, item_name: str) -> bool:
        """
        Use an item from the player's inventory.

        :param item_name: The name of the item to use
        :return: True if the item was used successfully, False otherwise
        """
        if item_name in self._inventory:
            item, quantity = self._inventory[item_name]
            use_result = item.use()

            if use_result:
                # If the item is a consumable (like a potion), remove it after use
                if item.item_type == ItemType.POTION:
                    if quantity > 1:
                        self._inventory[item_name] = (item, quantity - 1)
                    else:
                        del self._inventory[item_name]
                # For other item types (like weapons), we keep them in the inventory
                return True

        return False

    def inventory_to_string(self) -> str:
        """
        Get a string representation of the player's inventory.

        :return: A formatted string describing the inventory contents
        """
        if not self._inventory:
            return "Inventory is empty"

        inventory_str = "Inventory:\n"
        for item_name, (item, quantity) in self._inventory.items():
            inventory_str += (
                f"  {item_name}: {quantity} (Weight: {item.weight * quantity})\n"
            )
        inventory_str += f"Total Weight: {self.get_inventory_weight()}/{self._inventory_weight_limit}"
        return inventory_str

    def get_inventory_weight(self) -> float:
        """
        Calculate the current total weight of the inventory.

        :return: The total weight of all items in the inventory
        """
        return sum(
            item.weight * quantity for item, quantity in self._inventory.values()
        )

    def __str__(self) -> str:
        """
        Get a string representation of the player.

        :return: A formatted string describing the player
        """
        return f"Player: {self._name}\nHP: {self.hero.current_hp}\n{self.inventory_to_string()}"
