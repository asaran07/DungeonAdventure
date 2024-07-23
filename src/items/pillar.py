from src.enums.item_types import ItemType
from src.items.item import Item


class Pillar(Item):

    def __init__(self, name: str, description: str, weight: float):
        super().__init__(name, description, weight, ItemType.PILLAR)

    def get_name(self) -> str:
        return super().get_name()

    def use(self):
        pass
