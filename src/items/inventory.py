from typing import Dict, Optional, Tuple

from src.items.inventory_db import InventoryDatabase
from src.items.item import Item
from src.exceptions.player import InventoryFullError, ItemNotFoundError


class Inventory:
    def __init__(self, weight_limit: float = 50.0):
        self._items: Dict[str, Tuple[Item, int]] = {}
        self._weight_limit: float = weight_limit
        self._db = InventoryDatabase("")

    def add_item(self, item: Item) -> None:
        self.validate_weight(item)
        if item.id in self._items:
            self._items[item.id] = (item, self._items[item.id][1] + 1)
        else:
            self._items[item.id] = (item, 1)

    def validate_weight(self, item: Item) -> None:
        current_weight = self.get_total_weight()
        if current_weight + item.weight > self._weight_limit:
            raise InventoryFullError(
                "Adding this item would exceed the inventory weight limit"
            )

    def remove_item_by_id(self, item_id: str) -> Optional[Item]:
        if item_id in self._items:
            item, quantity = self._items[item_id]
            if quantity > 1:
                self._items[item_id] = (item, quantity - 1)
            else:
                del self._items[item_id]
            return item
        return None

    def remove_item(self, item: Item) -> bool:
        return self.remove_item_by_id(item.id) is not None

    def get_item_by_id(self, item_id: str) -> Optional[Item]:
        if item_id in self._items:
            return self._items[item_id][0]
        return None

    def get_item_by_name(self, name: str) -> Optional[Item]:
        for item, _ in self._items.values():
            if item.name.lower() == name.lower():
                return item
        return None

    def remove_item_by_name(self, item_name: str) -> Optional[Item]:
        """
        Removes an item from the inventory by its name.
        :param item_name: The name of the item to remove
        :return: The removed Item if found and removed, None otherwise
        """
        for item_id, (item, quantity) in self._items.items():
            if item.name.lower() == item_name.lower():
                if quantity > 1:
                    self._items[item_id] = (item, quantity - 1)
                else:
                    del self._items[item_id]
                return item
        return None

    def contains_item(self, item_name: str) -> bool:
        """
        Check if the inventory contains an item with the given name.
        :param item_name: The name of the item to check for
        :return: True if the item is in the inventory, False otherwise
        """
        return any(item.name.lower() == item_name.lower() for item, _ in self._items.values())

    def get_total_weight(self) -> float:
        return sum(item.weight * quantity for item, quantity in self._items.values())

    def get_item_quantity(self, item_id: str) -> int:
        return self._items[item_id][1] if item_id in self._items else 0

    def __str__(self) -> str:
        inventory_str = "Inventory:\n"
        for item_id, (item, quantity) in self._items.items():
            inventory_str += (
                f"  {item.name}: {quantity} (Weight: {item.weight * quantity})\n"
            )
        inventory_str += f"Total Weight: {self.get_total_weight()}/{self._weight_limit}"
        return inventory_str
