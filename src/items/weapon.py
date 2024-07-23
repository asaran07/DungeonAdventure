from src.enums.item_types import ItemType, WeaponType
from src.items.item import Item


class Weapon(Item):
    """Represents a weapon item in the game"""

    def __init__(self, name: str, description: str, weight: float, weapon_type: WeaponType, damage: int,
                 durability: int = 100):
        """
        Create a weapon item

        :param str name: Name of the weapon
        :param str description: Description of the weapon
        :param float weight: Weight of the weapon
        :param WeaponType weapon_type: Type of the weapon
        :param int damage: Damage the weapon can inflict
        :param int durability: Durability of the weapon. Defaults to 100
        """
        super().__init__(name, description, weight, ItemType.WEAPON)
        self._weapon_type = weapon_type
        self._damage = damage
        self._durability = durability

    @property
    def weapon_type(self) -> WeaponType:
        """Weapon type of the weapon, e.g. Sword, Bow"""
        return self._weapon_type

    @property
    def damage(self) -> int:
        """Damage points the weapon can inflict"""
        return self._damage

    @property
    def durability(self) -> int:
        """Durability of the weapon."""
        return self._durability

    def use(self):
        """Use the weapon to inflict damage, durability decreases by 1"""
        print(f"You swing the {self.get_name()}, dealing {self._damage} damage!")
        self._durability -= 1
