from src.items.potion import Potion
from src.enums.item_types import PotionType
class VisionPotion(Potion):
    name: str = "vision_potion"
    item_type = PotionType.VISION
    description : str = "A healing potion. Heals the player by 5-15 Health Points."

    def get_name(self):
        return self.name