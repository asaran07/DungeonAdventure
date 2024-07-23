from abc import ABC, abstractmethod
from src.enums.item_types import ItemType


class Item(ABC):
    def __init__(self, name: str, description: str, weight: float, item_type: ItemType):
        self._name = name
        self._description = description
        self._weight = weight
        self._item_type = item_type

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_weight(self) -> float:
        return self._weight

    def get_item_type(self) -> ItemType:
        return self._item_type

    @abstractmethod
    def use(self):
        pass
