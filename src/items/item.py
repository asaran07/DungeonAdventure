from abc import ABC, abstractmethod
from src.enums.item_types import ItemType


class Item(ABC):
    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        weight: float,
        item_type: ItemType,
    ):
        self._id = item_id
        self._name = name
        self._description = description
        self._weight = weight
        self._item_type = item_type

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def weight(self) -> float:
        return self._weight

    @property
    def item_type(self) -> ItemType:
        return self._item_type

    @abstractmethod
    def use(self, user):
        pass
