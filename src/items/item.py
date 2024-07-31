from abc import ABC, abstractmethod

from src.enums.item_types import ItemType


class Item(ABC):
    """
    Abstract base class for game items.
    Each Item must implement a `use` method.
    """

    def __init__(self, name: str, description: str, weight: float, item_type: ItemType):
        """
        Creates an Item object
        :param name: The name of the item
        :param description: The description of the item
        :param weight: The weight of the item
        :param item_type: The type of the item (should be an instance of ItemType)
        """
        self._name = name
        self._description = description
        self._weight = weight
        self._item_type = item_type

    @property
    def name(self) -> str:
        """Returns the name of the item"""
        return self._name

    @property
    def description(self) -> str:
        """Returns the description of the item"""
        return self._description

    @property
    def weight(self) -> float:
        """Returns the weight of the item"""
        return self._weight

    @property
    def item_type(self) -> ItemType:
        """Returns the item type of the item"""
        return self._item_type

    def __eq__(self, other):
        """
        Compares items based on name
        :param other: Is the other item to compare with

        Return: whether names are equal
        """
        if isinstance(other, Item):
            return self.name == other.name

    @abstractmethod
    def use(self):
        """
        Method to be implemented by child classes that
        defines the behavior when the item is used.
        """
        pass
