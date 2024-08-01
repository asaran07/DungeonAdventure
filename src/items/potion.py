from src.items.item import Item
from src.enums.item_types import ItemType, PotionType


class Potion(Item):
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        weight: float,
        potion_type: PotionType,
    ):
        super().__init__(item_id, name, description, weight, ItemType.POTION)
        self._potion_type = potion_type

    @property
    def potion_type(self) -> PotionType:
        return self._potion_type

    def use(self, user):
        # TODO: Implement general potion using logic
        pass


class HealingPotion(Potion):
    def __init__(self, item_id: str, name: str, heal_amount: int, weight: float):
        super().__init__(
            item_id, name, f"Heals for {heal_amount} HP", weight, PotionType.HEALING
        )
        self._heal_amount = heal_amount

    def use(self, user):
        user.heal(self._heal_amount)
        return True


class VisionPotion(Potion):
    def __init__(
        self,
        name: str = "Vision Potion",
        description: str = "Allows player to see the surrounding 8 rooms.",
        weight: float = 0.5,
    ):
        super().__init__(name, description, weight, PotionType.VISION)

    def use(self, user):
        print(f"You drink the {self.name}, revealing nearby rooms!")
