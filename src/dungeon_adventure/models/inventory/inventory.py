from typing import Dict, List, Optional, Tuple

from dungeon_adventure.exceptions.player import InventoryFullError, ItemNotFoundError
from dungeon_adventure.models.inventory.inventory_db import InventoryDatabase
from dungeon_adventure.models.items import Item


class Inventory:
    def __init__(self, weight_limit: float = 50.0):
        self._items: Dict[str, Tuple[Item, int]] = {}
        self._weight_limit: float = weight_limit
        self._db = InventoryDatabase("")

    # pickle methods to exclude database since sqlite3 not serializable
    def __getstate__(self):
        return self._items, self._weight_limit

    def __setstate__(self, state):
        self._items, self._weight_limit = state

    def get_all_items(self) -> List[Tuple[Item, int]]:
        return [(item, quantity) for item, quantity in self._items.values()]

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

    def remove_item_by_id(self, item_id: str) -> Item:
        if item_id in self._items:
            item, quantity = self._items[item_id]
            if quantity > 1:
                self._items[item_id] = (item, quantity - 1)
            else:
                del self._items[item_id]
            return item
        raise ItemNotFoundError(f"Item with id {item_id} not found in inventory")

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

    def get_total_weight(self) -> float:
        return sum(item.weight * quantity for item, quantity in self._items.values())

    def get_item_quantity(self, item_id: str) -> int:
        return self._items[item_id][1] if item_id in self._items else 0

    @property
    def weight_limit(self) -> float:
        return self._weight_limit

    def __str__(self) -> str:
        inventory_str = "Inventory:\n"
        for item, quantity in self._items.values():
            inventory_str += (
                f"  {item.name}: {quantity} (Weight: {item.weight * quantity})\n"
            )
        inventory_str += f"Total Weight: {self.get_total_weight()}/{self._weight_limit}"
        return inventory_str
