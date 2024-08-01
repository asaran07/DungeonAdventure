from typing import Dict, Optional, Tuple

from src.items.inventory_db import InventoryDatabase
from src.items.item import Item
from src.exceptions.player import InventoryFullError, ItemNotFoundError


class Inventory:
    def __init__(self, entity_id: str, weight_limit: float = 50.0):
        self._items: Dict[str, Tuple[Item, int]] = {}
        self._weight_limit: float = weight_limit
        self._entity_id = entity_id
        self._db = InventoryDatabase('')

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

    def get_total_weight(self) -> float:
        return sum(item.weight * quantity for item, quantity in self._items.values())

    def get_item_quantity(self, item_id: str) -> int:
        return self._items[item_id][1] if item_id in self._items else 0

    def __str__(self) -> str:
        inventory_str = "Inventory:\n"
        for item_name, (item, quantity) in self._items.items():
            inventory_str += (
                f"  {item_name}: {quantity} (Weight: {item.weight * quantity})\n"
            )
        inventory_str += f"Total Weight: {self.get_total_weight()}/{self._weight_limit}"
        return inventory_str
