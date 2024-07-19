from dataclasses import dataclass
from typing import Optional

from src.enums.item_types import ItemType


@dataclass
class Item:
    name: str
    item_type: ItemType
    description: str
    weight: float

    def get_name(self):
        return self.name
