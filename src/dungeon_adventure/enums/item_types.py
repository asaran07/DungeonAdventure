from enum import Enum, auto


class ItemType(Enum):
    UTILITY = auto()
    WEAPON = auto()
    POTION = auto()
    KEY = auto()
    TREASURE = auto()
    PILLAR = auto()


class PotionType(Enum):
    HEALING = auto()
    VISION = auto()


class PillarType(Enum):
    ABSTRACTION = auto()
    ENCAPSULATION = auto()
    INHERITANCE = auto()
    POLYMORPHISM = auto()


class WeaponType(Enum):
    DAGGER = auto()
    SWORD = auto()
    AXE = auto()
    BOW = auto()
