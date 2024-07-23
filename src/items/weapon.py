from src.enums.item_types import ItemType, WeaponType
from src.items.item import Item


class Weapon(Item):
    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        weapon_type: WeaponType,
        damage: int,
        durability: int = 100,
    ):
        super().__init__(name, description, weight, ItemType.WEAPON)
        self._weapon_type = weapon_type
        self._damage = damage
        self._durability = durability

    def get_weapon_type(self) -> WeaponType:
        return self._weapon_type

    def get_damage(self) -> int:
        return self._damage

    def get_durability(self) -> int:
        return self._durability

    def use(self):
        print(f"You swing the {self.get_name()}, dealing {self.get_damage()} damage!")
        self._durability -= 1
