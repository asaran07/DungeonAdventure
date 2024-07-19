from enum import Enum, auto


class ItemType(Enum):
    WEAPON = "Weapon"
    POTION = "Potion"
    KEY = "Key"
    TREASURE = "Treasure"


class PotionType(Enum):
    HEALING = auto()
    VISION = auto()


class PillarType(Enum):
    ABSTRACTION = auto()
    ENCAPSULATION = auto()
    INHERITANCE = auto()
    POLYMORPHISM = auto()
