from abc import ABC

from dungeon_adventure.enums.item_types import ItemType, PillarType
from dungeon_adventure.models.items import Item


class Pillar(Item, ABC):
    """Represents a pillar of OO in the game."""

    def __init__(
        self,
        item_id: str,
        name: str,
        description: str,
        pillar_type: PillarType,
        weight: float = 1.0,
    ):
        """Create a Pillar item
        :param str item_id: Unique identifier for the item
        :param str name: Name of the pillar
        :param str description: Description of the pillar
        :param PillarType pillar_type: Type of pillar
        :param float weight: Weight of the pillar. Defaults to 1
        """
        super().__init__(item_id, name, description, weight, ItemType.PILLAR)
        self._pillar_type = pillar_type

    @property
    def pillar_type(self) -> PillarType:
        """Type of pillar, e.g. Abstraction, Encapsulation"""
        return self._pillar_type


class AbstractionPillar(Pillar):
    def __init__(
        self,
        item_id: str,
        name: str = "Abstraction Pillar",
        description: str = "The abstraction pillar",
        weight: float = 1.0,
    ) -> None:
        super().__init__(item_id, name, description, PillarType.ABSTRACTION, weight)

    def use(self, user):
        # TODO: Implement use logic here
        pass


class EncapsulationPillar(Pillar):
    def __init__(
        self,
        item_id: str,
        name: str = "Encapsulation Pillar",
        description: str = "The encapsulation pillar",
        weight: float = 1.0,
    ) -> None:
        super().__init__(item_id, name, description, PillarType.ENCAPSULATION, weight)

    def use(self, user):
        # TODO: Implement use logic
        pass


class InheritancePillar(Pillar):
    def __init__(
        self,
        item_id: str,
        name: str = "Inheritance Pillar",
        description: str = "The inheritance pillar",
        weight: float = 1.0,
    ) -> None:
        super().__init__(item_id, name, description, PillarType.INHERITANCE, weight)

    def use(self, user):
        # TODO: Implement use logic here
        pass


class PolymorphismPillar(Pillar):
    def __init__(
        self,
        item_id: str,
        name: str = "Polymorphism Pillar",
        description: str = "The polymorphism pillar",
        weight: float = 1.0,
    ) -> None:
        super().__init__(item_id, name, description, PillarType.POLYMORPHISM, weight)

    def use(self, user):
        # TODO: Implement use logic here
        pass
