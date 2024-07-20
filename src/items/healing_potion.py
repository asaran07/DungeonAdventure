from src.items.potion import Potion
from src.enums.item_types import PotionType
class HealingPotion(Potion):
    name: str = "healing_potion"
    item_type = PotionType.HEALING
    description : str = "A vision potion. Grants the player sight to the surrounding 8 rooms."

    def get_name(self):
        return self.name