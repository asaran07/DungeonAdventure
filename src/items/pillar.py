from dataclasses import dataclass

from src.items.item import Item


# Pillar(Item) means pillar inherits from Item
# Not complete implementation, just created this to complete Adventurer class -Austin
# Make into data class
@dataclass
class Pillar(Item):
    name: str = super().__init__()

    def get_name(self) -> str:
        return super().get_name()
