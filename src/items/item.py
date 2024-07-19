from dataclasses import dataclass


@dataclass
class Item:
    name: str
    item_type: ItemType
    description: str
    weight: float = 1.0
