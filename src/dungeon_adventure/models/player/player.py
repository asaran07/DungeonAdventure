import logging
from typing import Optional

from dungeon_adventure.models.characters.hero import Hero
from dungeon_adventure.models.dungeon.room import Room
from dungeon_adventure.models.inventory.inventory import Inventory
from dungeon_adventure.models.items import Item, Weapon


class Player:
    def __init__(self, name: str, inventory_weight_limit: float = 50.0):
        self._name: str = name
        self._inventory: Inventory = Inventory(inventory_weight_limit)
        self._hero: Hero = Hero()
        self.current_room: Optional["Room"] = None
        self.logger = logging.getLogger(self.__class__.__name__)

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
            self.logger.info(f"Removed item {item} from inventory")
            return item.use(self)
        return False

    def use_item_by_id(self, item_id: str) -> bool:
        item = self._inventory.get_item_by_id(item_id)
        if item:
            self.logger.info(f"Using item with ID:{item_id}")
            return self.use_item(item)
        return False

    def equip_weapon(self, weapon: Weapon) -> bool:
        self.logger.info(f"Equipping {weapon.name}")
        if self._inventory.remove_item(weapon):
            if self._hero.equipped_weapon:
                self._inventory.add_item(self._hero.equipped_weapon)
            self._hero.equip_weapon(weapon)
            return True
        return False

    def heal(self, heal_amount: int):
        self.logger.info(f"Healing {self.name} for {heal_amount} points")
        self._hero.heal(heal_amount)

    def hurt(self, hurt_amount: int):
        self.logger.info(f"Hurting {self.name} for {hurt_amount} points")
        self._hero.hurt(hurt_amount)

    def __str__(self) -> str:
        return (
            f"Player: {self._name}\nHP: {self._hero.current_hp}\n{str(self._inventory)}"
        )
