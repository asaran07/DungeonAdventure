from enum import Enum, auto


class HeroType(Enum):
    WARRIOR = auto()
    PRIESTESS = auto()
    THIEF = auto()


class MonsterType(Enum):
    OGRE = auto()
    GREMLIN = auto()
    SKELETON = auto()
