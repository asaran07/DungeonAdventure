from abc import ABC

from src.enums.item_types import ItemType, PillarType
from src.items.item import Item


class Pillar(Item, ABC):
    """Represents a pillar of OO in the game."""
    def __init__(self,
                 name: str,
                 description: str,
                 pillar_type: PillarType,
                 weight: float = 1.0):
        """Create a Pillar item

        :param str name: Name of the pillar
        :param str description: Description of the pillar
        :param PillarType pillar_type: Type of pillar
        :param float weight: Weight of the pillar. Defaults to 1
        """
        super().__init__(name, description, weight, ItemType.PILLAR)
        self._pillar_type = pillar_type

    @property
    def get_pillar_type(self) -> PillarType:
        """Type of pillar, e.g. Abstraction, Encapsulation"""
        return self._pillar_type


class AbstractionPillar(Pillar):
    def __init__(self,
                 name: str = "Abstraction Pillar",
                 description: str = "The abstraction pillar"
                 ) -> None:
        super().__init__(name, description, PillarType.ABSTRACTION)

    def use(self):
        pass


class EncapsulationPillar(Pillar):
    def __init__(self,
                 name: str = "Encapsulation Pillar",
                 description: str = "The encapsulation pillar"
                 ) -> None:
        super().__init__(name, description, PillarType.ENCAPSULATION)

    def use(self):
        pass


class InheritancePillar(Pillar):
    def __init__(self,
                 name: str = "Inheritance Pillar",
                 description: str = "The inheritance pillar"
                 ) -> None:
        super().__init__(name, description, PillarType.INHERITANCE)

    def use(self):
        pass


class PolymorphismPillar(Pillar):
    def __init__(self,
                 name: str = "Polymorphism Pillar",
                 description: str = "The polymorphism pillar"
                 ) -> None:
        super().__init__(name, description, PillarType.POLYMORPHISM)

    def use(self):
        pass
