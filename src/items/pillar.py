from src.items.item import Item


class Pillar(Item):
    # Pillar(Item) means pillar inherits from Item
    # Not complete implementation, just created this to complete Adventurer class
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def get_name(self) -> str:
        return super().get_name()