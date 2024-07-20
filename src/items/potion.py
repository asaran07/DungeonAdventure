from src.items.item import Item
from src.enums.item_types import PotionType
class Potion(Item):
    name: str = "Potion"
    item_type = PotionType
    description: str = "An Unknown Potion"
    weight: float = 0.5
    def get_name(self):
        return self.name