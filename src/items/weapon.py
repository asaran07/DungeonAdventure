from dataclasses import dataclass

from src.enums.item_types import WeaponType
from src.items.item import Item


@dataclass
class Weapon(Item):
    """
    Weapon class for representing a weapon item.

    Attributes:
        weapon_type (WeaponType): The type of weapon.
        damage (int): The amount of damage the weapon inflicts.
        name (str): The name of the weapon. Default is "Unknown Weapon".
        description (str): The description of the weapon. Default is "A mysterious weapon".
        weight (float): The weight of the weapon. Default is 2.0.
        durability (int): The durability of the weapon. Default is 100.
    """
    weapon_type: WeaponType
    damage: int
    name: str = "Unknown Weapon"
    description: str = "A mysterious weapon"
    weight: float = 2.0
    durability: int = 100
