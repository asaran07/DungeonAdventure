from enum import Enum, auto


class ItemType(Enum):
    WEAPON = auto()
    POTION = auto()
    KEY = auto()
    TREASURE = auto()


class PotionType(Enum):
    HEALING = auto()
    VISION = auto()


class PillarType(Enum):
    ABSTRACTION = auto()
    ENCAPSULATION = auto()
    INHERITANCE = auto()
    POLYMORPHISM = auto()


class WeaponType(Enum):
    SWORD = auto()
    AXE = auto()
    BOW = auto()
