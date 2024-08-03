from src.items.item import Item
from src.enums.item_types import ItemType


class UtilityItem(Item):
    def __init__(
            self,
            item_id: str,
            name: str,
            description: str,
            weight: float,
            use_type: str,
            durability: int,
            auto_use: bool = True
    ):
        super().__init__(item_id, name, description, weight, ItemType.UTILITY)
        self._use_type = use_type
        self._durability = durability
        self._auto_use = auto_use

    @property
    def use_type(self) -> str:
        return self._use_type

    @property
    def durability(self) -> int:
        return self._durability

    @property
    def auto_use(self) -> bool:
        return self._auto_use

    def use(self, user):
        if self._durability > 0:
            self._durability -= 1
            print(f"{self.name} used. Durability: {self._durability}")
            return True
        else:
            print(f"{self.name} is depleted and cannot be used.")
            return False

    def __str__(self):
        return f"{self.name} (Utility - {self._use_type}, Durability: {self._durability})"
