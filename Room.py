from typing import List

from Item import Item


class Room:
    def __init__(self) -> None:
        self.items: List[Item] = []
        self.has_pit = False
        self.is_entrance = False
        self.is_exit = False

    def add_item(self, item: Item) -> None:
        """Adds an item to the room."""
        self.items.append(item)
