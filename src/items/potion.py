from abc import ABC
from src.enums.item_types import ItemType, PotionType
from src.items.item import Item


class Potion(Item, ABC):
    def __init__(
        self, name: str, description: str, weight: float, potion_type: PotionType
    ):
        super().__init__(name, description, weight, ItemType.POTION)
        self._potion_type = potion_type

    def get_potion_type(self) -> PotionType:
        return self._potion_type


class HealingPotion(Potion):
    def __init__(
                 self,
                 name: str = "healing_potion",
                 description: str = "Heals the player by 15 health points.",
                 weight: float = .5,
                 hp_recovery: int = 15
    ) -> None:
        super().__init__(name, description, weight, PotionType.HEALING)
        self._hp_recovery = hp_recovery

    def get_hp_recovery(self) -> int:
        return self._hp_recovery

    def use(self):
        print(
            f"You drink the {self.name}, recovering {self.get_hp_recovery()} HP!"
        )


class VisionPotion(Potion):
    def __init__(self,
                 name: str = "vision_potion",
                 description: str = "Allows player to see the surrounding 8 rooms.",
                 weight: float = .5):
        super().__init__(name, description, weight, PotionType.VISION)

    def use(self):
        print(f"You drink the {self.name}, revealing nearby rooms!")
