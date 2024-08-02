from src.characters.hero import Hero
from src.dungeon import Room
from src.items.inventory import Inventory
from src.items.item import Item


class Player:
    def __init__(self, name: str, inventory_weight_limit: float = 50.0):
        self._name: str = name
        self._inventory: Inventory = Inventory(inventory_weight_limit)
        self._hero: Hero = Hero()
        self.current_room = Room

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def hero(self) -> Hero:
        return self._hero

    @property
    def inventory(self) -> Inventory:
        return self._inventory

    def use_item(self, item: Item) -> bool:
        if self._inventory.remove_item(item):
            return item.use(self)
        return False

    def use_item_by_id(self, item_id: str) -> bool:
        item = self._inventory.get_item_by_id(item_id)
        if item:
            return self.use_item(item)
        return False

    def __str__(self) -> str:
        return (
            f"Player: {self._name}\nHP: {self._hero.current_hp}\n{str(self._inventory)}"
        )
