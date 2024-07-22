from dataclasses import dataclass

from src.items.item import Item
from src.enums.item_types import PotionType


@dataclass
class Potion(Item):
    name: str = "Potion"
    item_type = PotionType
    description: str = "An Unknown Potion"
    weight: float = 0.5

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


@dataclass
class VisionPotion(Potion):
    name: str = "vision_potion"
    item_type = PotionType.VISION
    description: str = "A healing potion. Heals the player by 5-15 Health Points."

    def get_name(self):
        return self.name


@dataclass
class HealingPotion(Potion):
    name: str = "healing_potion"
    item_type = PotionType.HEALING
    description: str = "A vision potion. Grants the player sight to the surrounding 8 rooms."
    hp_recovery: int = 15

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
